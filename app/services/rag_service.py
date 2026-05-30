from __future__ import annotations

import concurrent.futures
import logging
import re
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
                    "sources": self._sources_for_role(chat_request.role, chunks),
                    "session_id": session_id,
                }

            if chat_request.role == "tecnico":
                answer = self._strip_source_lines(answer)
            else:
                answer = self._strip_operator_citations(answer)
            answer = self._strip_markdown_markers(answer)

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
                    translate_english=chat_request.role == "tecnico",
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
                    translate_english=chat_request.role == "tecnico",
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
        history_section = (
            "\n\nHistorial conversacional reciente "
            "(solo para continuidad del dialogo; NO es fuente tecnica, "
            "NO es historial de mantenimiento del equipo y NO debe mencionarse en la respuesta):\n"
            f"{history_block}"
            if history_block
            else ""
        )
        system_prompt = system_prompt_for_role(chat_request.role, equipment_name)
        return f"""{system_prompt}

INSTRUCCION DE SEGURIDAD:
Usa solamente el contexto documental recuperado. No uses conocimiento general.
Si el contexto contiene pasos, controles, verificaciones, alarmas, valores, codigos, placas, conectores o procedimientos relacionados con la consulta, responde con esa evidencia disponible.
No cierres la respuesta diciendo que no se encontro informacion si ya diste pasos, controles o recomendaciones basadas en el contexto recuperado.
Si la evidencia recuperada es parcial, ambigua o incompleta, indicalo claramente y limita la respuesta a lo que aparece en el contexto.
Solo indica que no hay informacion disponible cuando ningun fragmento recuperado contenga datos tecnicos utiles relacionados con la consulta.
No menciones historial conversacional, historial reciente, historial de mantenimiento ni reparaciones previas salvo que esa informacion aparezca literalmente en el contexto documental recuperado.
En modo operador, no menciones paginas, fuentes, manuales, citas, diagramas ni nombres de archivo.
No uses Markdown en la respuesta: no uses asteriscos, negritas, encabezados Markdown ni viñetas con asterisco.

Pregunta del usuario:
{chat_request.query}{history_section}

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
                f"Fuente: {self._visible_source_name(chunk)}, pagina {self._visible_page(chunk)}, "
                f"equipo: {chunk.citation.equipment_name}\n"
                f"Imagenes: {self._format_image_context(chunk)}\n"
                f"Texto:\n{chunk.text.strip()}"
            )
            for chunk in chunks
        )

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
            raw_text = self._compact_extract_text(chunk.text.strip())[:900]
            is_english = self._is_likely_english(raw_text)
            extract_label = "Extracto traducido" if is_english and translate_english else "Extracto literal"
            display_text = (
                self._translate_extract_to_spanish(raw_text)
                if is_english and translate_english
                else raw_text
            )
            display_text = self._strip_markdown_markers(display_text)
            extracts.append(
                (
                    f"Fuente: {self._visible_source_name(chunk)}, pag. {self._visible_page(chunk)}\n"
                    f"{extract_label} {index}\n"
                    f"{display_text}"
                )
            )

        return (
            "Respuesta directa desde la base documental local.\n"
            f"Consulta: {question}\n\n"
            + (f"Motivo: {reason}\n\n" if reason else "")
            + "\n\n---\n\n".join(extracts)
        )

    def _visible_source_name(self, chunk: RetrievedChunk) -> str:
        return (
            chunk.citation.display_source
            or chunk.citation.original_pdf
            or chunk.citation.source_file
        )

    def _visible_page(self, chunk: RetrievedChunk) -> int:
        return (
            chunk.citation.pdf_page
            or chunk.citation.page
            or chunk.citation.markdown_page
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

        seen_sources: set[tuple[str, str]] = set()
        seen_images: set[str] = set()
        sources: list[dict] = []

        max_image_sources = 3
        max_total_images = 4
        total_images = 0

        for chunk in chunks:
            key = (chunk.citation.source_file, str(chunk.citation.page))
            if key in seen_sources:
                continue

            seen_sources.add(key)
            source = chunk.citation.to_dict()

            # Se conservan todas las fuentes documentales, pero se limita
            # la cantidad de imagenes enviadas al frontend para evitar ruido visual.
            # La curaduria visual fina queda para Marisa/Dario; aca solo se controla
            # trazabilidad, duplicados y sobrecarga de miniaturas.
            filtered_images = []
            if len(sources) < max_image_sources and total_images < max_total_images:
                for image in source.get("images", []):
                    image_url = str(image.get("url") or "").strip()
                    if not image_url or image_url in seen_images:
                        continue

                    seen_images.add(image_url)
                    filtered_images.append(image)
                    total_images += 1

                    if total_images >= max_total_images:
                        break

            source["images"] = filtered_images
            sources.append(source)

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

    def _strip_source_lines(self, answer: str) -> str:
        lines = []
        skipping_sources = False
        for line in answer.splitlines():
            normalized = line.strip().lower()
            if normalized.startswith("fuente:") or normalized.startswith("fuentes:"):
                skipping_sources = True
                continue
            if skipping_sources and normalized.startswith("- fuente:"):
                continue
            skipping_sources = False
            lines.append(line)
        return "\n".join(lines).strip() or answer.strip()

    def _strip_markdown_markers(self, answer: str) -> str:
        cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", answer)
        cleaned = re.sub(r"\*([^*\n]+)\*", r"\1", cleaned)
        cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
        cleaned = re.sub(r"(?m)^\s*[*-]\s+", "", cleaned)
        cleaned = cleaned.replace("**", "").replace("__", "")
        cleaned = re.sub(r"\s+\*", " ", cleaned)
        cleaned = re.sub(r"\*\s+", " ", cleaned)
        return cleaned.strip()

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

    def _compact_extract_text(self, text: str) -> str:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = "\n".join(line.rstrip() for line in normalized.splitlines())
        normalized = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", normalized)
        return normalized.strip()

    def _has_enough_operator_context(self, chunks: list[RetrievedChunk]) -> bool:
        clean_chunks = [
            chunk
            for chunk in chunks
            if not chunk.text.strip().lower().startswith("pagina con imagenes")
            and len(chunk.text.strip()) >= 180
        ]
        return len(clean_chunks) >= 2

    def _build_retrieval_question(self, question: str, history: list[dict]) -> str:
        expanded_question = question
        normalized = question.lower()

        expansion_terms: list[str] = []

        if (
            "bloque" in normalized
            or "desbloque" in normalized
            or "pantalla táctil" in normalized
            or "pantalla tactil" in normalized
        ):
            expansion_terms.extend(
                [
                    "bloqueo",
                    "desbloqueo",
                    "bloquear",
                    "desbloquear",
                    "pantalla tactil",
                    "pantalla táctil",
                    "icono de bloqueo",
                    "tecla de bloqueo/desbloqueo",
                    "tecla de bloqueo y desbloqueo",
                    "barra favoritos",
                    "funciones de la pantalla tactil",
                ]
            )

        if (
            "no agita" in normalized
            or "no gira" in normalized
            or "no se mueve" in normalized
            or "no mueve" in normalized
            or "bandeja no se mueve" in normalized
        ):
            expansion_terms.extend(
                [
                    "la bandeja no se mueve",
                    "bandeja",
                    "motor dañado",
                    "motor 12v 78rpm",
                    "objeto que obstruye el movimiento",
                    "obstruccion",
                    "falla mecanica",
                    "circuito electronico",
                    "conexion",
                    "conectores",
                    "cables dañados",
                    "funcion agita si no",
                    "mecanismo de agitacion",
                ]
            )

        if (
            "bateria baja" in normalized
            or "batería baja" in normalized
            or "bateria se mantiene baja" in normalized
            or "batería se mantiene baja" in normalized
        ):
            expansion_terms.extend(
                [
                    "la bateria se mantiene siempre baja",
                    "la batería se mantiene siempre baja",
                    "conexion",
                    "conectores",
                    "cables",
                    "seccion 4.2",
                    "sección 4.2",
                    "circuito electronico",
                    "circuito regulador de tension",
                    "lectura de carga de bateria",
                    "bateria dañada",
                    "batería dañada",
                    "bateria 12v 3.4Ah",
                    "test bateria",
                ]
            )

        if (
            "no dispara" in normalized
            or "no realiza exposicion" in normalized
            or "no realiza exposición" in normalized
            or "no emite radiacion" in normalized
            or "no emite radiación" in normalized
        ):
            expansion_terms.extend(
                [
                    "no realiza exposicion",
                    "no realiza exposición",
                    "disparo",
                    "pulsador de disparo",
                    "PREP RAD",
                    "PREP+RAD",
                    "radiacion",
                    "radiación",
                    "exposicion",
                    "exposición",
                    "filamento",
                    "filament failure",
                    "inverter fail",
                    "autocalibracion",
                    "auto-calibracion",
                    "carga de capacitores",
                    "fusibles",
                    "fusible F1",
                    "230 V",
                    "135 V",
                ]
            )

        if (
            "no pasa test" in normalized
            or "no pasa el test" in normalized
            or "falla test" in normalized
            or "test fall" in normalized
            or "test unsuccessful" in normalized
        ):
            expansion_terms.extend(
                [
                    "T1 test",
                    "T1 TEST UNSUCCESSFUL",
                    "incorrect test step",
                    "error display",
                    "storage error number",
                    "test bypass",
                    "blood system test",
                    "display test",
                    "accumulator test",
                    "arterial pressure test",
                    "venous pressure test",
                    "temperature test",
                    "air detector test",
                    "blood leak detector test",
                    "conductivity test",
                    "UF function test",
                    "Diasafe HDF filter test",
                    "self test",
                    "function test",
                    "subtest",
                ]
            )

        if (
            "no carga energia" in normalized
            or "no carga energía" in normalized
            or "no carga bateria" in normalized
            or "no carga batería" in normalized
            or "no carga" in normalized
            or "carga energia" in normalized
            or "carga energía" in normalized
        ):
            expansion_terms.extend(
                [
                    "power failure",
                    "AC/DC power supply",
                    "power management board",
                    "battery",
                    "fully charged battery",
                    "charge",
                    "charging",
                    "charging prohibited",
                    "capacitor",
                    "capacitor charge",
                    "energy charging",
                    "energy disarming",
                    "discharging failed",
                    "defibrillator energy",
                    "self-test",
                    "M0 -2V5 power failure",
                    "DVDD power failure",
                    "ASIC_VREF power failure",
                ]
            )

        if (
            "no completa ciclo" in normalized
            or "no termina ciclo" in normalized
            or "ciclo incompleto" in normalized
            or "ciclo abortado" in normalized
            or "ciclo cancelado" in normalized
            or "cycle abort" in normalized
            or "cycle aborted" in normalized
            or "cycle cancelled" in normalized
        ):
            expansion_terms.extend(
                [
                    "cycle cancelled",
                    "cycle aborted",
                    "cycle abort",
                    "sterilization cycle",
                    "restart sterilizer",
                    "vacuum insufficient",
                    "vacuum not low enough",
                    "pre-plasma",
                    "plasma stage",
                    "RF subsystem",
                    "low plasma power",
                    "moisture in load",
                    "load may be out-gassing",
                    "repackage load",
                    "cassette",
                    "pressure",
                    "error",
                ]
            )

        if (
            "alarma oxigeno" in normalized
            or "alarma oxígeno" in normalized
            or "alarma o2" in normalized
            or "o2 alarm" in normalized
            or "oxygen alarm" in normalized
            or "fio2" in normalized
            or "fiO2" in question
        ):
            expansion_terms.extend(
                [
                    "oxygen alarm",
                    "O2 alarm",
                    "O2 concentration",
                    "FiO2",
                    "measured O2 concentration",
                    "O2 cell",
                    "oxygen cell",
                    "expected cell life",
                    "replace O2 cell",
                    "gas supply",
                    "gas supply pressure",
                    "O2 supply",
                    "Air and O2",
                    "gas modules",
                    "replace gas modules",
                    "Pre-use check",
                    "calibration",
                ]
            )

        if expansion_terms:
            unique_terms = list(dict.fromkeys(expansion_terms))
            expanded_question = (
                f"{question}\n"
                "Terminos relacionados para recuperar documentacion tecnica relevante: "
                + ", ".join(unique_terms)
                + "."
            )

        if not history:
            return expanded_question

        recent_context = "\n".join(
            f"{message['role']}: {message['content'][:450]}"
            for message in history[-4:]
        )
        return f"{recent_context}\nPregunta actual: {expanded_question}"

    def _format_history(self, history: list[dict]) -> str:
        if not history:
            return ""

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
