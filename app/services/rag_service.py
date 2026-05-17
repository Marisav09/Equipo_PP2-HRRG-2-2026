from __future__ import annotations

import concurrent.futures
import logging
from collections.abc import Callable

import requests
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.core.exceptions import LLMUnavailableError, VectorstoreNotReadyError
from app.models.schemas import AssistantResponse, RetrievedChunk, TicketRecord
from app.services.audit_service import AuditService
from app.services.memory_service import MemoryService
from app.services.ticket_service import TicketService
from app.services.vectorstore_service import VectorstoreService

logger = logging.getLogger(__name__)


class RagService:
    def __init__(
        self,
        vectorstore: VectorstoreService | None = None,
        audit_service: AuditService | None = None,
        ticket_service: TicketService | None = None,
        memory_service: MemoryService | None = None,
    ) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.audit_service = audit_service or AuditService()
        self.ticket_service = ticket_service or TicketService()
        self.memory_service = memory_service or MemoryService()

    def answer_question(
        self,
        question: str,
        equipment: str | None = None,
        session_id: str | None = None,
        force_fallback: bool = False,
        should_cancel: Callable[[], bool] | None = None,
    ) -> AssistantResponse:
        active_session_id = session_id or "default"
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("La consulta no puede estar vacia.")

        history = self.memory_service.get_recent_messages(active_session_id)
        retrieval_question = self._build_retrieval_question(normalized_question, history)

        try:
            chunks = self.vectorstore.retrieve(retrieval_question)
        except VectorstoreNotReadyError:
            ticket_id = self._create_ticket(
                normalized_question,
                "La base vectorial no esta inicializada o no tiene documentos.",
                equipment,
            )
            response = AssistantResponse(
                answer=(
                    "Todavia no hay manuales indexados en la base documental. "
                    f"Se genero el ticket #{ticket_id} para revision administrativa."
                ),
                mode="ticket",
                ticket_id=ticket_id,
            )
            self.audit_service.record_query(normalized_question, response, equipment)
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        if not chunks:
            ticket_id = self._create_ticket(
                normalized_question,
                "No se recuperaron fragmentos relevantes desde ChromaDB.",
                equipment,
            )
            response = AssistantResponse(
                answer=(
                    "No encontre informacion respaldada en los manuales cargados. "
                    f"Se genero el ticket #{ticket_id} para que un administrador lo revise."
                ),
                mode="ticket",
                ticket_id=ticket_id,
            )
            self.audit_service.record_query(normalized_question, response, equipment)
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        if force_fallback:
            response = AssistantResponse(
                answer=self._build_fallback_answer(
                    normalized_question,
                    chunks,
                    "El tecnico solicito ver la respuesta documental de ChromaDB sin esperar al LLM.",
                ),
                sources=[chunk.citation for chunk in chunks],
                mode="fallback",
            )
            self.audit_service.record_query(normalized_question, response, equipment)
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        try:
            self._check_ollama()
            answer = self._generate_with_timeout(normalized_question, chunks, equipment, history)
            if should_cancel and should_cancel():
                logger.info("Respuesta LLM descartada por cancelacion del usuario.")
                return AssistantResponse(
                    answer="Respuesta LLM cancelada por el usuario.",
                    sources=[chunk.citation for chunk in chunks],
                    mode="cancelled",
                )
            response = AssistantResponse(
                answer=self._append_sources(answer, chunks),
                sources=[chunk.citation for chunk in chunks],
                mode="llm",
            )
        except concurrent.futures.TimeoutError:
            reason = (
                f"Ollama excedio el limite de {settings.llm_timeout_seconds} segundos. "
                "Se usa fallback documental."
            )
            logger.warning("Fallback activado por timeout del LLM")
            response = AssistantResponse(
                answer=self._build_fallback_answer(normalized_question, chunks, reason),
                sources=[chunk.citation for chunk in chunks],
                mode="fallback",
            )
        except Exception as exc:
            reason = str(exc) or exc.__class__.__name__
            logger.warning("Fallback activado por falla del LLM: %s", reason)
            response = AssistantResponse(
                answer=self._build_fallback_answer(normalized_question, chunks, reason),
                sources=[chunk.citation for chunk in chunks],
                mode="fallback",
            )

        self.audit_service.record_query(normalized_question, response, equipment)
        self._store_turn(active_session_id, normalized_question, response.answer, equipment)
        return response

    def _check_ollama(self) -> None:
        try:
            response = requests.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=settings.ollama_health_timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMUnavailableError(
                "Ollama no esta respondiendo. Se usa fallback documental."
            ) from exc

    def _generate_with_timeout(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        equipment: str | None,
        history: list[dict[str, str]],
    ) -> str:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self._generate_answer, question, chunks, equipment, history)
        try:
            return future.result(timeout=settings.llm_timeout_seconds)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _generate_answer(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        equipment: str | None,
        history: list[dict[str, str]],
    ) -> str:
        llm = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0.0,
        )
        prompt = self._build_prompt(question, chunks, equipment, history)
        response = llm.invoke(prompt)
        return str(response.content).strip()

    def _build_prompt(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        equipment: str | None,
        history: list[dict[str, str]],
    ) -> str:
        context = "\n\n".join(
            (
                f"Fuente: {chunk.citation.label()}\n"
                f"Texto:\n{chunk.text.strip()}"
            )
            for chunk in chunks
        )

        equipment_line = f"Equipo seleccionado: {equipment}\n" if equipment else ""
        history_block = self._format_history(history)
        return f"""
Eres un asistente tecnico para Ingenieria Clinica del Hospital Regional Rio Grande.
Debes responder exclusivamente con la informacion contenida en el contexto documental.
Si la respuesta no esta respaldada por el contexto, indica que no se encuentra en los manuales cargados.
Incluye una seccion final llamada "Fuentes" con documento y pagina.
Si una fuente indica que contiene imagenes, orienta al tecnico a revisar visualmente esa pagina del PDF.
Usa el historial conversacional solo para entender referencias como "eso", "ese equipo" o "la alarma anterior"; no inventes datos fuera del contexto documental.

{equipment_line}Pregunta del tecnico:
{question}

Historial reciente:
{history_block}

Contexto documental:
{context}

Respuesta:
""".strip()

    def _append_sources(self, answer: str, chunks: list[RetrievedChunk]) -> str:
        if "Fuentes" in answer:
            return answer

        sources = "\n".join(
            f"- [*{chunk.citation.source_file}, pagina {chunk.citation.page}*]({chunk.citation.pdf_url()})"
            for chunk in chunks
        )
        return f"{answer}\n\nFuentes:\n{sources}"

    def _build_fallback_answer(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        reason: str,
    ) -> str:
        extracts = []
        for index, chunk in enumerate(chunks, start=1):
            image_note = (
                "\nNota visual: esta pagina contiene imagenes o esquemas; conviene revisar el PDF original."
                if chunk.citation.has_images
                else ""
            )
            extracts.append(
                (
                    f"Extracto {index}\n"
                    f"Fuente: [*{chunk.citation.source_file}, pagina {chunk.citation.page}*]({chunk.citation.pdf_url()})\n"
                    f"{chunk.text.strip()[:900]}{image_note}"
                )
            )

        return (
            "El modelo generativo local no respondio correctamente, asi que active el "
            "fallback documental. No es una respuesta redactada por el LLM, pero estos "
            "fragmentos recuperados desde ChromaDB pueden orientar la intervencion.\n\n"
            f"Consulta: {question}\n"
            f"Situacion tecnica: {reason}\n\n"
            + "\n\n---\n\n".join(extracts)
        )

    def _create_ticket(self, question: str, reason: str, equipment: str | None) -> int:
        return self.ticket_service.create_ticket(
            TicketRecord(
                question=question,
                equipment=equipment,
                reason=reason,
            )
        )

    def _build_retrieval_question(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        if not history:
            return question

        recent_context = "\n".join(
            f"{message['role']}: {message['content'][:450]}"
            for message in history[-4:]
        )
        return f"{recent_context}\nPregunta actual: {question}"

    def _format_history(self, history: list[dict[str, str]]) -> str:
        if not history:
            return "Sin historial previo para esta sesion."

        return "\n".join(
            f"{'Tecnico' if message['role'] == 'user' else 'Asistente'}: {message['content'][:900]}"
            for message in history
        )

    def _store_turn(
        self,
        session_id: str,
        question: str,
        answer: str,
        equipment: str | None,
    ) -> None:
        self.memory_service.add_message(session_id, "user", question, equipment)
        self.memory_service.add_message(session_id, "assistant", answer, equipment)
