from __future__ import annotations

import concurrent.futures
import logging
from collections.abc import Callable

import requests
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.core.exceptions import LLMUnavailableError, VectorstoreNotReadyError
from app.models.schemas import AssistantResponse, RetrievedChunk
from app.services.memory_service import MemoryService
from app.services.vectorstore_service import VectorstoreService

logger = logging.getLogger(__name__)


class RagService:
    def __init__(
        self,
        vectorstore: VectorstoreService | None = None,
        memory_service: MemoryService | None = None,
    ) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.memory_service = memory_service or MemoryService()

    def answer_question(
        self,
        question: str,
        equipment: str | None = None,
        session_id: str | None = None,
        force_fallback: bool = False,
        should_cancel: Callable[[], bool] | None = None,
        user_role: str = "tecnico",
    ) -> AssistantResponse:
        active_session_id = session_id or "default"
        user_role = "operador" if user_role == "operador" else "tecnico"
        normalized_question = question.strip()
        if not normalized_question:
            raise ValueError("La consulta no puede estar vacía.")

        history = self.memory_service.get_recent_messages(active_session_id)
        retrieval_question = self._build_retrieval_question(normalized_question, history)

        try:
            chunks = self.vectorstore.retrieve(retrieval_question, equipment=equipment)
        except VectorstoreNotReadyError:
            response = self._build_no_information_response(
                "Todavía no hay manuales indexados en la base documental. Ejecuta la ingesta antes de consultar."
            )
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        if not chunks:
            response = self._build_no_information_response(
                "No encontré información respaldada en los manuales indexados para el equipo seleccionado."
            )
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        if force_fallback:
            response = AssistantResponse(
                answer=self._build_fallback_answer(
                    normalized_question,
                    chunks,
                    "El técnico solicitó ver la respuesta documental de ChromaDB sin esperar al LLM.",
                ),
                sources=[chunk.citation for chunk in chunks],
                mode="fallback",
            )
            self._store_turn(active_session_id, normalized_question, response.answer, equipment)
            return response

        try:
            self._check_ollama()
            answer = self._generate_with_timeout(normalized_question, chunks, equipment, history, user_role)
            if should_cancel and should_cancel():
                logger.info("Respuesta LLM descartada por cancelación del usuario.")
                return AssistantResponse(
                    answer="Respuesta LLM cancelada por el usuario.",
                    sources=[chunk.citation for chunk in chunks],
                    mode="cancelled",
                )

            final_answer = self._append_sources(answer, chunks) if user_role == "tecnico" else answer
            response = AssistantResponse(
                answer=final_answer,
                sources=[chunk.citation for chunk in chunks],
                mode="llm",
            )
        except concurrent.futures.TimeoutError:
            reason = (
                f"Ollama excedió el límite de {settings.llm_timeout_seconds} segundos. "
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

        self._store_turn(active_session_id, normalized_question, response.answer, equipment)
        return response

    def _build_no_information_response(self, message: str) -> AssistantResponse:
        return AssistantResponse(
            answer=(
                f"{message}\n\n"
                "Por seguridad, no voy a inferir procedimientos ni diagnósticos fuera de los manuales cargados."
            ),
            mode="sin_informacion",
        )

    def _check_ollama(self) -> None:
        try:
            response = requests.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=settings.ollama_health_timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMUnavailableError(
                "Ollama no está respondiendo. Se usa fallback documental."
            ) from exc

    def _generate_with_timeout(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        equipment: str | None,
        history: list[dict[str, str]],
        user_role: str,
    ) -> str:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self._generate_answer, question, chunks, equipment, history, user_role)
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
        user_role: str,
    ) -> str:
        llm = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0.0,
        )
        prompt = self._build_prompt(question, chunks, equipment, history, user_role)
        response = llm.invoke(prompt)
        return str(response.content).strip()

    def _build_prompt(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        equipment: str | None,
        history: list[dict[str, str]],
        user_role: str,
    ) -> str:
        context = "\n\n".join(
            (
                f"Fuente: {chunk.citation.label()}\n"
                f"Texto:\n{chunk.text.strip()}"
            )
            for chunk in chunks
        )

        nombre_equipo = equipment or "el equipo consultado"
        history_block = self._format_history(history)

        if user_role == "operador":
            system_instruction = f"""
Eres un Asistente Clínico de Primera Línea del Hospital Regional Río Grande. Estás ayudando a un profesional de la salud que está operando el equipo: {nombre_equipo}.
REGLAS ESTRICTAS:
1. CERO ALUCINACIONES: Tu respuesta debe basarse ÚNICA Y EXCLUSIVAMENTE en la información del contexto documental. Si no está en el texto, NO la inventes.
2. AISLAMIENTO: Responde SOLO para el equipo {nombre_equipo}.
3. ESTILO WIZARD: Guía al usuario paso a paso para encontrar el diagnóstico o solución. Sé directo, claro y conciso.
4. SIN FUENTES: NO incluyas referencias a páginas ni citas bibliográficas en tu respuesta final.
5. SEGURIDAD CRÍTICA: Si el contexto no resuelve el problema de forma segura y certera, advierte al operador que detenga su acción y se comunique inmediatamente con Ingeniería Clínica.
6. IDIOMA Y ORTOGRAFÍA: Responde SIEMPRE en español, con ortografía impecable. Respeta nombres propios, siglas o denominaciones técnicas originales del equipamiento.
"""
        else:
            system_instruction = f"""
Eres un Asistente Experto para Ingeniería Clínica del Hospital Regional Río Grande. Estás asistiendo a un técnico especializado en el equipo: {nombre_equipo}.
REGLAS ESTRICTAS:
1. CERO ALUCINACIONES: Responde EXCLUSIVAMENTE utilizando el contexto documental. Si no está la respuesta, indica: 'Información no disponible en los manuales indexados'.
2. AISLAMIENTO: Tu análisis corresponde ÚNICAMENTE al equipo {nombre_equipo}.
3. TRAZABILIDAD TOTAL: Al final de tu respuesta, incluye siempre una sección de 'Fuentes', detallando documento y página.
4. MANEJO DE GRÁFICOS: Si el contexto indica que hay un diagrama, esquema eléctrico o figura, indica: 'Para ver el diagrama técnico, consulte la página [X] del manual [Archivo]'.
5. IDIOMA Y ORTOGRAFÍA: Responde SIEMPRE en español, con ortografía impecable. Respeta nombres propios, siglas o denominaciones técnicas originales del equipamiento.
"""

        return f"""
{system_instruction.strip()}

Usa el historial conversacional solo para entender referencias como "eso" o "la alarma anterior".

Pregunta del usuario:
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
            f"- [*{chunk.citation.source_file}, página {chunk.citation.page}*]({chunk.citation.pdf_url()})"
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
                "\nNota visual: esta página contiene imágenes o esquemas; conviene revisar el PDF original."
                if chunk.citation.has_images
                else ""
            )
            extracts.append(
                (
                    f"Extracto {index}\n"
                    f"Fuente: [*{chunk.citation.source_file}, página {chunk.citation.page}*]({chunk.citation.pdf_url()})\n"
                    f"{chunk.text.strip()[:900]}{image_note}"
                )
            )

        return (
            "El modelo generativo local no respondió correctamente, así que activé el "
            "fallback documental. No es una respuesta redactada por el LLM, pero estos "
            "fragmentos recuperados desde ChromaDB pueden orientar la intervención.\n\n"
            f"Consulta: {question}\n"
            f"Situación técnica: {reason}\n\n"
            + "\n\n---\n\n".join(extracts)
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
            return "Sin historial previo para esta sesión."

        return "\n".join(
            f"{'Técnico' if message['role'] == 'user' else 'Asistente'}: {message['content'][:900]}"
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
