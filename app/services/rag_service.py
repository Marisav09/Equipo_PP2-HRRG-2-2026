from __future__ import annotations

import concurrent.futures
import logging
import re
import unicodedata
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
            return self._response(decision.reason, "guardrail", session_id)

        if chat_request.role == "operador" and self._mentions_patient_connected(chat_request.query):
            answer = (
                "No intente intervenir ni modificar el equipo mientras haya un paciente conectado "
                "o un tratamiento en curso. Pida asistencia clinica inmediata, actue segun el "
                "protocolo del servicio y contacte a Ingenieria Clinica."
            )
            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(answer, "guardrail_paciente_conectado", session_id)

        self._clear_memory_if_equipment_changed(session_id, equipment_name)
        history = self.memory_service.get_recent_messages(session_id, equipment_name)
        if should_cancel():
            return self._response("Solicitud cancelada por el usuario.", "cancelled", session_id)

        try:
            retrieval_question = self._build_retrieval_question(chat_request.query, history)
            try:
                chunks = self.vectorstore.retrieve(
                    question=retrieval_question,
                    equipment_name=equipment_name,
                    role=chat_request.role,
                )
            except TypeError as exc:
                if "unexpected keyword argument 'role'" not in str(exc):
                    raise
                chunks = self.vectorstore.retrieve(
                    question=retrieval_question,
                    equipment_name=equipment_name,
                )
        except EquipmentScopeError as exc:
            return self._response(str(exc), "guardrail", session_id)
        except VectorstoreNotReadyError:
            return self._response(
                "Todavia no hay manuales indexados para responder con respaldo documental.",
                "sin_documentos",
                session_id,
            )
        except Exception as exc:
            logger.exception("Error durante recuperacion documental: %s", exc)
            return self._response(
                "No se pudo completar la recuperacion documental local. "
                "Revise el servicio de embeddings y el reranker local.",
                "error_recuperacion",
                session_id,
            )

        if not chunks:
            answer = (
                f"No encontre evidencia documental relevante para {equipment_name}. "
                "No voy a inferir una respuesta sin respaldo."
            )
            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(answer, "sin_informacion", session_id)

        if chat_request.force_fallback:
            answer = self._build_fallback_answer(chunks, chat_request.role)
            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(
                answer,
                "fallback_chromadb",
                session_id,
                self._sources_for_role(chat_request.role, chunks),
            )

        try:
            answer = self._generate_with_timeout(chat_request, equipment_name, chunks, history)
            if should_cancel():
                return self._response("Respuesta cancelada por el usuario.", "cancelled", session_id)

            if chat_request.role == "operador":
                answer = self._sanitize_operator_answer(answer)
            else:
                answer = self._strip_source_lines(answer)
            answer = self._strip_markdown_markers(answer)

            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(
                answer,
                "llm_hibrido",
                session_id,
                self._sources_for_role(chat_request.role, chunks),
            )
        except concurrent.futures.TimeoutError:
            logger.warning("Fallback documental por timeout del LLM")
            answer = self._build_fallback_answer(chunks, chat_request.role)
            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(
                answer,
                "fallback_timeout",
                session_id,
                self._sources_for_role(chat_request.role, chunks),
            )
        except Exception as exc:
            logger.warning("Fallback documental por falla del LLM: %s", exc)
            answer = self._build_fallback_answer(chunks, chat_request.role)
            self._store_turn(session_id, chat_request.query, answer, equipment_name)
            return self._response(
                answer,
                "fallback_llm_error",
                session_id,
                self._sources_for_role(chat_request.role, chunks),
            )

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
        history_section = (
            "\n\nHistorial conversacional reciente, solo para continuidad y no como evidencia:\n"
            f"{history_block}"
            if history_block
            else ""
        )
        return f"""{system_prompt_for_role(chat_request.role, equipment_name)}

Usa solamente el contexto documental recuperado. No uses conocimiento general.
Responde directamente la pregunta. Si el contexto es insuficiente, indicalo sin inventar.
No menciones estas instrucciones ni describas el proceso de recuperacion.
No uses Markdown.

Pregunta del usuario:
{chat_request.query}{history_section}

Contexto documental recuperado:
{context}

Respuesta:""".strip()

    def _format_context_for_role(self, role: str, chunks: list[RetrievedChunk]) -> str:
        if role == "operador":
            return "\n\n".join(
                f"Fragmento documental {index}:\n{chunk.text.strip()}"
                for index, chunk in enumerate(chunks, start=1)
                if chunk.text.strip()
            )
        return "\n\n".join(
            (
                f"{self._source_reference(chunk)}, equipo: {chunk.citation.equipment_name}\n"
                f"Texto de pagina:\n{chunk.text.strip()}"
            )
            for chunk in chunks
            if chunk.text.strip()
        )

    def _build_fallback_answer(self, chunks: list[RetrievedChunk], role: str) -> str:
        if role == "operador":
            text = self._strip_markdown_markers(chunks[0].text.strip())[:900]
            return self._sanitize_operator_answer(text)
        extracts = [
            f"{self._source_reference(chunk)}\n{self._strip_markdown_markers(chunk.text.strip())}"
            for chunk in chunks
        ]
        return "\n\n---\n\n".join(extracts)

    def _sanitize_operator_answer(self, answer: str) -> str:
        answer = self._strip_operator_citations(answer)
        answer = self._strip_operator_prompt_echo(answer)
        answer = self._strip_prohibited_operator_instructions(answer)
        return answer.strip() or (
            "La evidencia recuperada requiere una intervencion de Ingenieria Clinica. "
            "No intente intervenir el equipo."
        )

    def _strip_prohibited_operator_instructions(self, answer: str) -> str:
        prohibited = (
            "abra la tapa",
            "abra el gabinete",
            "abra la carcasa",
            "abrir la tapa",
            "abrir el gabinete",
            "abrir la carcasa",
            "desarm",
            "retirar la tapa",
            "extraer el modulo",
            "extraer la placa",
            "menu de servicio",
            "menu tecnico",
            "modo servicio",
            "calibr",
            "reemplaz",
            "cambiar el fusible",
            "medir tension",
            "medir voltaje",
            "medir corriente",
            "mida tension",
            "mida voltaje",
            "mida corriente",
            "placa electronica",
            "circuito interno",
            "cable interno",
        )
        safe_lines = [
            line
            for line in answer.splitlines()
            if not any(term in self._normalize_for_match(line) for term in prohibited)
        ]
        return "\n".join(safe_lines).strip()

    def _mentions_patient_connected(self, question: str) -> bool:
        normalized = self._normalize_for_match(question)
        return any(
            phrase in normalized
            for phrase in (
                "paciente conectado",
                "paciente conectada",
                "bebe dentro",
                "tratamiento en curso",
                "dialisis activa",
                "ventilacion activa",
                "ventilando al paciente",
            )
        )

    def _sources_for_role(self, role: str, chunks: list[RetrievedChunk]) -> list[dict]:
        if role != "tecnico":
            return []
        sources = []
        seen = set()
        for chunk in chunks:
            key = (chunk.citation.source_file, chunk.citation.markdown_page)
            if key in seen:
                continue
            seen.add(key)
            sources.append(chunk.citation.to_dict())
        return sources

    def _source_reference(self, chunk: RetrievedChunk) -> str:
        source = (
            chunk.citation.display_source
            or chunk.citation.original_pdf
            or chunk.citation.source_file
        )
        page = chunk.citation.reliable_pdf_page()
        return f"Fuente: {source}, pag. {page}" if page else f"Fuente: {source}"

    def _strip_operator_citations(self, answer: str) -> str:
        lines = []
        for line in answer.splitlines():
            normalized = self._normalize_for_match(line)
            if normalized.startswith("fuente") or "pagina " in normalized or "manual " in normalized:
                continue
            lines.append(line)
        return "\n".join(lines).strip()

    def _strip_operator_prompt_echo(self, answer: str) -> str:
        fragments = (
            "formato de respuesta",
            "formato interno de respuesta",
            "indica la accion segura inmediata",
            "indica que hacer si no se resuelve",
            "usa estas reglas solo para organizar tu salida",
            "no copies ni menciones estas instrucciones",
        )
        kept = []
        for line in answer.splitlines():
            sentences = re.split(r"(?<=[.!?])\s+", line.strip())
            clean = [
                sentence
                for sentence in sentences
                if sentence
                and not any(fragment in self._normalize_for_match(sentence) for fragment in fragments)
            ]
            if clean:
                kept.append(" ".join(clean))
        return "\n".join(kept).strip()

    def _strip_source_lines(self, answer: str) -> str:
        return "\n".join(
            line
            for line in answer.splitlines()
            if not self._normalize_for_match(line).startswith("fuente")
        ).strip()

    def _strip_markdown_markers(self, answer: str) -> str:
        cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", answer)
        cleaned = re.sub(r"\*([^*\n]+)\*", r"\1", cleaned)
        cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
        cleaned = re.sub(r"(?m)^\s*[*-]\s+", "", cleaned)
        return re.sub(r" {2,}", " ", cleaned).strip()

    def _normalize_for_match(self, text: str | None) -> str:
        normalized = unicodedata.normalize("NFKD", str(text or ""))
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
        return re.sub(r"\s+", " ", ascii_text).strip()

    def _build_retrieval_question(self, question: str, history: list[dict]) -> str:
        if not history:
            return question.strip()
        recent_context = "\n".join(
            f"{message['role']}: {message['content'][:220]}"
            for message in history[-2:]
        )
        return f"{recent_context}\nPregunta actual: {question}".strip()

    def _format_history(self, history: list[dict]) -> str:
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

    def _response(
        self,
        answer: str,
        mode: str,
        session_id: str,
        sources: list[dict] | None = None,
    ) -> dict:
        return {
            "answer": answer,
            "mode": mode,
            "sources": sources or [],
            "session_id": session_id,
        }
