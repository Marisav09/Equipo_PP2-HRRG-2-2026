from __future__ import annotations

import concurrent.futures
import logging
from typing import Callable

from app.core.config import settings
from app.core.equipment_catalog import canonical_equipment_name, find_equipment_by_id
from app.core.exceptions import EquipmentScopeError, VectorstoreNotReadyError
from app.core.guardrails import require_equipment_scope
from app.core.prompts import system_prompt_for_role
from app.models.schemas import ChatRequest, RetrievedChunk
from app.services.memory_service import MemoryService
from app.services.ollama_service import OllamaService
from app.services.vectorstore_service import VectorstoreService


logger = logging.getLogger(__name__)


class RagService:
    def __init__(
        self,
        vectorstore: VectorstoreService | None = None,
        ollama_service: OllamaService | None = None,
        memory_service: MemoryService | None = None,
    ) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.ollama_service = ollama_service or OllamaService()
        self.memory_service = memory_service or MemoryService()

    def answer_question(
        self,
        chat_request: ChatRequest,
        session_id: str,
        should_cancel: Callable[[], bool],
    ) -> dict:
        equipment_name = chat_request.equipment_name
        if chat_request.equipment_id:
            equipment = find_equipment_by_id(chat_request.equipment_id)
            equipment_name = equipment.name if equipment else equipment_name

        equipment_name = canonical_equipment_name(equipment_name) or equipment_name
        decision = require_equipment_scope(equipment_name)
        if not decision.allowed:
            return {
                "answer": decision.reason,
                "mode": "guardrail",
                "sources": [],
                "session_id": session_id,
            }

        self._clear_memory_if_equipment_changed(session_id, equipment_name)
        history = self.memory_service.get_recent_messages(session_id, equipment_name)

        if should_cancel():
            return {
                "answer": "Solicitud cancelada por el usuario.",
                "mode": "cancelled",
                "sources": [],
                "session_id": session_id,
            }

        try:
            retrieval_question = self._build_retrieval_question(chat_request.query, history)
            chunks = self.vectorstore.retrieve(
                question=retrieval_question,
                equipment_name=equipment_name,
            )
        except EquipmentScopeError as exc:
            return {
                "answer": str(exc),
                "mode": "guardrail",
                "sources": [],
                "session_id": session_id,
            }
        except VectorstoreNotReadyError:
            return {
                "answer": (
                    "Todavia no hay manuales indexados en ChromaDB para responder con respaldo documental.\n\n"
                    "Por seguridad, no voy a inferir procedimientos fuera de manuales cargados."
                ),
                "mode": "sin_documentos",
                "sources": [],
                "session_id": session_id,
            }

        if not chunks:
            return {
                "answer": (
                    f"No encontre fragmentos documentales para {equipment_name} que respalden una respuesta segura.\n\n"
                    "Detenga la accion si hay riesgo y contacte a Ingenieria Clinica."
                ),
                "mode": "sin_informacion",
                "sources": [],
                "session_id": session_id,
            }

        if chat_request.role == "operador" and not self._has_enough_operator_context(chunks):
            response = {
                "answer": (
                    "La informacion recuperada no permite resolver esto de forma segura.\n\n"
                    "Detenga la accion y contacte INMEDIATAMENTE al Tecnico de Ingenieria Clinica."
                ),
                "mode": "contexto_insuficiente_operador",
                "sources": [],
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        if chat_request.force_fallback:
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    chunks,
                    role=chat_request.role,
                    translate_english=True,
                ),
                "mode": "fallback_chromadb",
                "sources": self._sources_for_role(chat_request.role, chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        try:
            answer = self._generate_with_timeout(chat_request, equipment_name, chunks, history)
            if should_cancel():
                return {
                    "answer": "Respuesta cancelada por el usuario.",
                    "mode": "cancelled",
                    "sources": [chunk.citation.to_dict() for chunk in chunks],
                    "session_id": session_id,
                }

            if chat_request.role == "tecnico":
                answer = self._ensure_sources_section(answer, chunks)
            else:
                answer = self._strip_operator_citations(answer)

            response = {
                "answer": answer,
                "mode": "llm",
                "sources": self._sources_for_role(chat_request.role, chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response
        except concurrent.futures.TimeoutError:
            logger.warning("Fallback documental por timeout del LLM")
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    chunks,
                    role=chat_request.role,
                    reason=f"Ollama supero el timeout de {settings.llm_timeout_seconds} segundos.",
                ),
                "mode": "fallback_timeout",
                "sources": self._sources_for_role(chat_request.role, chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response
        except Exception as exc:
            logger.warning("Fallback documental por falla del LLM: %s", exc)
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    chunks,
                    role=chat_request.role,
                    reason=f"Falla del LLM local: {exc}",
                ),
                "mode": "fallback_llm_error",
                "sources": self._sources_for_role(chat_request.role, chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

    def _generate_with_timeout(
        self,
        chat_request: ChatRequest,
        equipment_name: str,
        chunks: list[RetrievedChunk],
        history: list[dict],
    ) -> str:
        prompt = self._build_prompt(chat_request, equipment_name, chunks, history)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.ollama_service.generate, prompt)
        try:
            return future.result(timeout=settings.llm_timeout_seconds)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _build_prompt(
        self,
        chat_request: ChatRequest,
        equipment_name: str,
        chunks: list[RetrievedChunk],
        history: list[dict],
    ) -> str:
        context = self._format_context_for_role(chat_request.role, chunks)
        history_block = self._format_history(history)
        system_prompt = system_prompt_for_role(chat_request.role, equipment_name)
        return f"""{system_prompt}

INSTRUCCION DE SEGURIDAD:
Si el contexto documental no contiene la respuesta, dilo explicitamente. No uses conocimiento general.
En modo operador, no menciones paginas, fuentes, manuales, citas, diagramas ni nombres de archivo.

Pregunta del usuario:
{chat_request.query}

Historial reciente de esta misma sesion y equipo:
{history_block}

Contexto documental recuperado exclusivamente desde Markdown en data/processed por ChromaDB:
{context}

Respuesta:""".strip()

    def _format_context_for_role(self, role: str, chunks: list[RetrievedChunk]) -> str:
        if role == "operador":
            clean_chunks = [
                chunk
                for chunk in chunks
                if not chunk.text.strip().lower().startswith("pagina con imagenes")
            ]
            usable_chunks = clean_chunks or chunks
            return "\n\n".join(
                f"Fragmento documental {index}:\n{chunk.text.strip()}"
                for index, chunk in enumerate(usable_chunks, start=1)
            )

        return "\n\n".join(
            (
                f"Fuente: {chunk.citation.source_file}, pagina {chunk.citation.page}, "
                f"equipo: {chunk.citation.equipment_name}\n"
                f"Imagenes: {self._format_image_context(chunk)}\n"
                f"Texto:\n{chunk.text.strip()}"
            )
            for chunk in chunks
        )

    def _ensure_sources_section(self, answer: str, chunks: list[RetrievedChunk]) -> str:
        if "Fuentes" in answer:
            return answer

        sources = "\n".join(
            f"Fuente: {chunk.citation.source_file}, pag. {chunk.citation.page}"
            for chunk in chunks
        )
        return f"{answer}\n\n{sources}"

    def _build_fallback_answer(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        role: str = "tecnico",
        reason: str | None = None,
        translate_english: bool = False,
    ) -> str:
        if role == "operador":
            return self._build_operator_fallback_answer(chunks)

        extracts = []
        for index, chunk in enumerate(chunks, start=1):
            raw_text = chunk.text.strip()[:900]
            is_english = self._is_likely_english(raw_text)
            extract_label = "Extracto traducido" if is_english and translate_english else "Extracto literal"
            display_text = (
                self._translate_extract_to_spanish(raw_text)
                if is_english and translate_english
                else raw_text
            )
            image_note = (
                "\nNota visual: esta pagina contiene imagenes o diagramas; revise el PDF original."
                if chunk.citation.has_images
                else ""
            )
            extracts.append(
                (
                    f"{extract_label} {index}\n"
                    f"Fuente: {chunk.citation.source_file}, pagina {chunk.citation.page}\n"
                    f"{display_text}{image_note}"
                )
            )

        return (
            "Respuesta directa desde la base documental local.\n"
            f"Consulta: {question}\n\n"
            + (f"Motivo: {reason}\n\n" if reason else "")
            + "\n\n---\n\n".join(extracts)
        )

    def _build_operator_fallback_answer(self, chunks: list[RetrievedChunk]) -> str:
        usable = [
            chunk.text.strip()
            for chunk in chunks
            if chunk.text.strip()
            and not chunk.text.strip().lower().startswith("pagina con imagenes")
        ]
        if not usable:
            return (
                "No tengo informacion suficiente para indicarte un paso seguro. "
                "Detene la accion y contacta al Tecnico de Ingenieria Clinica."
            )
        text = usable[0][:420].strip()
        return self._strip_operator_citations(text)

    def _sources_for_role(self, role: str, chunks: list[RetrievedChunk]) -> list[dict]:
        if role != "tecnico":
            return []
        seen: set[tuple[str, str]] = set()
        sources = []
        for chunk in chunks:
            key = (chunk.citation.source_file, str(chunk.citation.page))
            if key in seen:
                continue
            seen.add(key)
            sources.append(chunk.citation.to_dict())
        return sources

    def _format_image_context(self, chunk: RetrievedChunk) -> str:
        if not chunk.citation.images:
            return "sin imagenes asociadas"
        return "; ".join(
            f"{image.get('label', 'Imagen')} ({image.get('url')})"
            for image in chunk.citation.images
        )

    def _strip_operator_citations(self, answer: str) -> str:
        lines = []
        for line in answer.splitlines():
            normalized = line.strip().lower()
            if normalized.startswith("fuente:") or normalized.startswith("fuentes:"):
                continue
            if "pagina " in normalized or "pag." in normalized or "manual" in normalized:
                continue
            lines.append(line)
        return "\n".join(lines).strip() or answer.strip()

    def _is_likely_english(self, text: str) -> bool:
        normalized = f" {text.lower()} "
        english_hits = sum(
            token in normalized
            for token in (
                " the ",
                " and ",
                " door ",
                " alarm ",
                " system ",
                " verify ",
                " replace ",
                " press ",
                " open ",
                " close ",
            )
        )
        spanish_hits = sum(
            token in normalized
            for token in (
                " el ",
                " la ",
                " los ",
                " las ",
                " equipo ",
                " alarma ",
                " puerta ",
                " verificar ",
            )
        )
        return english_hits >= 2 and english_hits > spanish_hits

    def _translate_extract_to_spanish(self, text: str) -> str:
        prompt = (
            "Traduce al espanol tecnico rioplatense el siguiente extracto de manual. "
            "No agregues informacion, no resumas y conserva nombres tecnicos, codigos y valores.\n\n"
            f"{text}"
        )
        try:
            translated = self.ollama_service.generate(prompt)
            return self._strip_translation_preamble(translated)
        except Exception:
            return text

    def _strip_translation_preamble(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        while lines and (
            "traduccion" in lines[0].lower()
            or "traducción" in lines[0].lower()
            or lines[0].lower().startswith("a continuacion")
            or lines[0].lower().startswith("a continuación")
        ):
            lines.pop(0)
        while lines and not lines[0]:
            lines.pop(0)
        return "\n".join(lines).strip() or text.strip()

    def _has_enough_operator_context(self, chunks: list[RetrievedChunk]) -> bool:
        clean_chunks = [
            chunk
            for chunk in chunks
            if not chunk.text.strip().lower().startswith("pagina con imagenes")
            and len(chunk.text.strip()) >= 180
        ]
        return len(clean_chunks) >= 2

    def _build_retrieval_question(self, question: str, history: list[dict]) -> str:
        if not history:
            return question

        recent_context = "\n".join(
            f"{message['role']}: {message['content'][:450]}"
            for message in history[-4:]
        )
        return f"{recent_context}\nPregunta actual: {question}"

    def _format_history(self, history: list[dict]) -> str:
        if not history:
            return "Sin historial previo para este equipo."

        return "\n".join(
            f"{message['role']}: {message['content'][:700]}"
            for message in history
        )

    def _clear_memory_if_equipment_changed(self, session_id: str, equipment_name: str) -> None:
        last_equipment = self.memory_service.get_last_equipment(session_id)
        if last_equipment and last_equipment != equipment_name:
            self.memory_service.clear_session(session_id)

    def _store_turn(
        self,
        session_id: str,
        question: str,
        answer: str,
        equipment_name: str,
    ) -> None:
        self.memory_service.add_message(session_id, "user", question, equipment_name)
        self.memory_service.add_message(session_id, "assistant", answer, equipment_name)
