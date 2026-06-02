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

        query_type = self._classify_query(chat_request.query)
        if query_type == "consulta_administrativa_manuales":
            response = {
                "answer": self._build_document_inventory_answer(equipment_name),
                "mode": "consulta_administrativa",
                "sources": [],
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        # Guardrail deterministico para operador clinico.
        # Se ejecuta antes de recuperar contexto y antes de llamar al LLM:
        # en situaciones criticas no debe quedar librado al modelo.
        if chat_request.role == "operador":
            normalized_operator_query = self._normalize_for_match(chat_request.query)

            operator_test_or_check_query = (
                any(
                    term in normalized_operator_query
                    for term in (
                        "no pasa prueba",
                        "no pasa la prueba",
                        "no pasa test",
                        "no pasa el test",
                        "no pasa pre use",
                        "no pasa preuse",
                        "pre use check",
                        "preuse check",
                        "prueba del sistema",
                        "comprobacion del sistema",
                        "check del sistema",
                        "falla prueba",
                        "falla test",
                        "test fall",
                        "test unsuccessful",
                    )
                )
                or (
                    any(
                        term in normalized_operator_query
                        for term in ("prueba", "test", "check", "comprobacion")
                    )
                    and any(
                        term in normalized_operator_query
                        for term in ("no pasa", "falla", "error", "usar igual", "puedo usar")
                    )
                )
            )

            operator_active_use_failure = (
                any(
                    term in normalized_operator_query
                    for term in (
                        "paciente",
                        "bebe",
                        "tratamiento",
                        "dialisis",
                        "ventilacion",
                        "ventilando",
                    )
                )
                and any(
                    term in normalized_operator_query
                    for term in (
                        "trabado",
                        "trabada",
                        "alarma",
                        "falla",
                        "error",
                        "no ventila",
                        "no prende",
                        "se apaga",
                        "no responde",
                    )
                )
            )

            if operator_test_or_check_query or operator_active_use_failure:
                if operator_active_use_failure and not operator_test_or_check_query:
                    critical_answer = (
                        "No intente intervenir el equipo durante un tratamiento o situacion clinica en curso.\n\n"
                        "Si hay paciente conectado, tratamiento en curso o riesgo clinico, pida asistencia clinica inmediata y actue segun el protocolo del servicio.\n\n"
                        "No intente apagar, desconectar, reiniciar, calibrar ni intervenir el equipo por indicacion del asistente.\n\n"
                        "Contacte inmediatamente al Tecnico de Ingenieria Clinica."
                    )
                else:
                    critical_answer = (
                        "No use el equipo si no pasa una prueba, test o comprobacion del sistema.\n\n"
                        "No intente apagar, desconectar, reiniciar, calibrar ni intervenir el equipo por indicacion del asistente.\n\n"
                        "Si hay paciente conectado, tratamiento en curso o riesgo clinico, pida asistencia clinica inmediata y asegure soporte alternativo segun el protocolo del servicio.\n\n"
                        "Deje el equipo fuera de uso si corresponde y contacte inmediatamente al Tecnico de Ingenieria Clinica."
                    )

                response = {
                    "answer": critical_answer,
                    "mode": "guardrail_operador_seguridad_critica",
                    "sources": [],
                    "session_id": session_id,
                }
                self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
                return response

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
            retrieval_question = self._build_retrieval_question(chat_request.query, history, equipment_name)
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
        except Exception as exc:
            logger.exception("Error durante recuperacion documental: %s", exc)
            return {
                "answer": (
                    "No se pudo completar la recuperacion documental local.\n\n"
                    "Motivo tecnico: el motor de busqueda rechazo o no pudo procesar la consulta. "
                    "No voy a responder sin respaldo documental recuperado. "
                    "Reintente con una consulta mas acotada o revise el servicio local de Ollama/embeddings."
                ),
                "mode": "error_recuperacion",
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

        exact_codes = self._detect_exact_codes(chat_request.query)
        if exact_codes:
            code_chunks = self._chunks_containing_codes(chunks, exact_codes)
            if code_chunks:
                response = {
                    "answer": self._build_code_lookup_answer(chat_request.query, exact_codes, code_chunks),
                    "mode": "code_lookup",
                    "sources": self._sources_for_role(chat_request.role, code_chunks),
                    "session_id": session_id,
                }
            else:
                response = {
                    "answer": self._build_code_not_found_answer(equipment_name, exact_codes),
                    "mode": "code_lookup_sin_evidencia",
                    "sources": [],
                    "session_id": session_id,
                }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        if self._is_power_on_question(chat_request.query):
            power_on_chunks = self._power_on_chunks(chunks)
            if power_on_chunks:
                answer = self._build_power_on_answer(
                    question=chat_request.query,
                    equipment_name=equipment_name,
                    role=chat_request.role,
                    chunks=power_on_chunks,
                )
                answer = self._strip_markdown_markers(answer)
                response = {
                    "answer": answer,
                    "mode": "extractivo_encendido",
                    "sources": self._sources_for_role(chat_request.role, power_on_chunks),
                    "session_id": session_id,
                }
                self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
                return response

        evidence = self._evaluate_retrieval_evidence(
            question=chat_request.query,
            equipment_name=equipment_name,
            chunks=chunks,
            query_type=query_type,
        )
        usable_chunks = evidence["chunks"] or chunks

        if chat_request.role == "operador" and not self._has_enough_operator_context(usable_chunks):
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

        if evidence["quality"] == "debil" and not chat_request.force_fallback:
            response = {
                "answer": self._build_weak_evidence_answer(
                    question=chat_request.query,
                    equipment_name=equipment_name,
                    role=chat_request.role,
                    evidence=evidence,
                ),
                "mode": "evidencia_debil",
                "sources": [],
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        if chat_request.force_fallback:
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    usable_chunks,
                    role=chat_request.role,
                    translate_english=True,
                ),
                "mode": "fallback_chromadb",
                "sources": self._sources_for_role(chat_request.role, usable_chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response

        try:
            answer = self._generate_with_timeout(chat_request, equipment_name, usable_chunks, history)
            if should_cancel():
                return {
                    "answer": "Respuesta cancelada por el usuario.",
                    "mode": "cancelled",
                    "sources": self._sources_for_role(chat_request.role, usable_chunks),
                    "session_id": session_id,
                }

            if chat_request.role == "tecnico":
                answer = self._strip_source_lines(answer)
            else:
                answer = self._strip_operator_citations(answer)
            answer = self._strip_markdown_markers(answer)

            if evidence["quality"] == "parcial" and chat_request.role == "tecnico":
                answer = self._prepend_partial_evidence_notice(answer)

            response = {
                "answer": answer,
                "mode": "llm" if evidence["quality"] == "suficiente" else "llm_evidencia_parcial",
                "sources": self._sources_for_role(chat_request.role, usable_chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response
        except concurrent.futures.TimeoutError:
            logger.warning("Fallback documental por timeout del LLM")
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    usable_chunks,
                    role=chat_request.role,
                    reason=f"Ollama supero el timeout de {settings.llm_timeout_seconds} segundos.",
                    translate_english=chat_request.role == "tecnico",
                ),
                "mode": "fallback_timeout",
                "sources": self._sources_for_role(chat_request.role, usable_chunks),
                "session_id": session_id,
            }
            self._store_turn(session_id, chat_request.query, response["answer"], equipment_name)
            return response
        except Exception as exc:
            logger.warning("Fallback documental por falla del LLM: %s", exc)
            response = {
                "answer": self._build_fallback_answer(
                    chat_request.query,
                    usable_chunks,
                    role=chat_request.role,
                    reason=f"Falla del LLM local: {exc}",
                    translate_english=chat_request.role == "tecnico",
                ),
                "mode": "fallback_llm_error",
                "sources": self._sources_for_role(chat_request.role, usable_chunks),
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
                f"{self._source_reference(chunk)}, "
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
                    f"{self._source_reference(chunk)}\n"
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

    def _verified_pdf_page(self, chunk: RetrievedChunk) -> int | None:
        return chunk.citation.reliable_pdf_page()

    def _source_reference(self, chunk: RetrievedChunk) -> str:
        pdf_page = self._verified_pdf_page(chunk)
        if pdf_page:
            return f"Fuente: {self._visible_source_name(chunk)}, pag. {pdf_page}"

        return f"Fuente: {self._visible_source_name(chunk)}"

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

        reliable_chunks = [chunk for chunk in chunks if self._verified_pdf_page(chunk) is not None]
        chunks_to_show = reliable_chunks if reliable_chunks else chunks

        for chunk in chunks_to_show:
            pdf_page = self._verified_pdf_page(chunk)
            key = (
                chunk.citation.source_file,
                str(pdf_page or chunk.citation.chunk_id),
            )
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

    def _classify_query(self, question: str) -> str:
        normalized = self._normalize_for_match(question)

        if self._detect_exact_codes(question):
            return "codigo_tecnico_exacto"

        if any(
            phrase in normalized
            for phrase in (
                "manuales cargados",
                "manuales indexados",
                "documentos cargados",
                "documentos indexados",
                "que manuales",
                "cuales manuales",
                "que documentos",
                "cuales documentos",
                "centro de monitoreo",
            )
        ):
            return "consulta_administrativa_manuales"

        if any(
            token in normalized
            for token in (
                "alarma",
                "alarm",
                "error",
                "falla",
                "fallo",
                "no prende",
                "no enciende",
                "no arranca",
                "no funciona",
                "no calibra",
                "no pasa test",
                "no pasa el test",
                "test unsuccessful",
                "test fall",
                "bloqueo",
                "occlusion",
                "oclusion",
            )
        ):
            return "falla_alarma"

        if any(
            token in normalized
            for token in (
                "mantenimiento",
                "preventivo",
                "calibracion",
                "calibrar",
                "verificacion",
                "verificar",
                "reemplazo",
                "reemplazar",
                "limpieza",
                "test",
            )
        ):
            return "mantenimiento"

        return "consulta_tecnica_general"

    def _evaluate_retrieval_evidence(
        self,
        question: str,
        equipment_name: str,
        chunks: list[RetrievedChunk],
        query_type: str,
    ) -> dict:
        question_terms = self._content_terms(question)
        intent_terms = self._intent_evidence_terms(question, query_type)
        is_power_on_question = self._is_power_on_question(question)
        scored: list[tuple[float, RetrievedChunk]] = []

        for chunk in chunks:
            score = self._evidence_score_for_chunk(
                question_terms,
                intent_terms,
                query_type,
                chunk,
                is_power_on_question=is_power_on_question,
            )
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        useful_chunks = [
            chunk
            for score, chunk in scored
            if self._is_useful_evidence(
                score,
                intent_terms,
                query_type,
                chunk,
                is_power_on_question=is_power_on_question,
            )
        ]

        if query_type == "falla_alarma" and not is_power_on_question:
            specific_terms = self._specific_fault_terms(question)
            if specific_terms and not self._chunks_contain_specific_terms(useful_chunks, specific_terms):
                return {
                    "quality": "debil",
                    "query_type": query_type,
                    "chunks": [],
                    "reason": "termino_especifico_de_falla_no_encontrado_en_evidencia",
                    "scores": [score for score, _chunk in scored[:5]],
                }

        if is_power_on_question:
            strong_power_chunks = [
                chunk for chunk in useful_chunks if self._has_strong_power_on_evidence(chunk.text)
            ]
            if not strong_power_chunks:
                return {
                    "quality": "debil",
                    "query_type": query_type,
                    "chunks": [],
                    "reason": "sin_procedimiento_literal_de_encendido_alimentacion",
                    "scores": [score for score, _chunk in scored[:5]],
                }

            if len(strong_power_chunks) == 1:
                return {
                    "quality": "parcial",
                    "query_type": query_type,
                    "chunks": strong_power_chunks,
                    "reason": "un_solo_fragmento_con_evidencia_de_encendido_alimentacion",
                    "scores": [score for score, _chunk in scored[:5]],
                }

            return {
                "quality": "suficiente",
                "query_type": query_type,
                "chunks": strong_power_chunks[: min(6, len(strong_power_chunks))],
                "reason": "evidencia_de_encendido_alimentacion_suficiente",
                "scores": [score for score, _chunk in scored[:5]],
            }

        if query_type == "consulta_tecnica_general" and not useful_chunks and chunks:
            useful_chunks = chunks[: min(3, len(chunks))]
            return {
                "quality": "parcial",
                "query_type": query_type,
                "chunks": useful_chunks,
                "reason": "recuperacion_general_sin_indicadores_fuertes",
                "scores": [score for score, _chunk in scored[:5]],
            }

        if not useful_chunks:
            return {
                "quality": "debil",
                "query_type": query_type,
                "chunks": [],
                "reason": "sin_fragmentos_utiles_para_la_consulta",
                "scores": [score for score, _chunk in scored[:5]],
            }

        if len(useful_chunks) == 1:
            return {
                "quality": "parcial",
                "query_type": query_type,
                "chunks": useful_chunks,
                "reason": "un_solo_fragmento_util",
                "scores": [score for score, _chunk in scored[:5]],
            }

        return {
            "quality": "suficiente",
            "query_type": query_type,
            "chunks": useful_chunks[: min(8, len(useful_chunks))],
            "reason": "fragmentos_utiles_suficientes",
            "scores": [score for score, _chunk in scored[:5]],
        }

    def _evidence_score_for_chunk(
        self,
        question_terms: set[str],
        intent_terms: set[str],
        query_type: str,
        chunk: RetrievedChunk,
        is_power_on_question: bool = False,
    ) -> float:
        text = chunk.text.strip()
        if not text:
            return 0.0

        normalized_text = self._normalize_for_match(text)
        chunk_terms = self._content_terms(text)
        overlap = len(question_terms.intersection(chunk_terms))
        intent_hits = sum(1 for term in intent_terms if term in normalized_text)
        procedure_hits = sum(
            1
            for term in (
                "verifique",
                "verificar",
                "compruebe",
                "comprobar",
                "revise",
                "revisar",
                "controle",
                "controlar",
                "conecte",
                "conectar",
                "desconecte",
                "desconectar",
                "reemplace",
                "reemplazar",
                "ajuste",
                "ajustar",
                "medir",
                "mida",
                "calibrar",
                "calibracion",
            )
            if term in normalized_text
        )
        source_bonus = 0.5 if chunk.citation.equipment_name else 0.0
        page_bonus = 0.25 if chunk.citation.has_reliable_pdf_page() else 0.0
        length_bonus = 0.5 if len(text) >= 180 else 0.0
        penalty = self._evidence_penalty(
            normalized_text,
            query_type,
            is_power_on_question=is_power_on_question,
        )

        return (overlap * 1.0) + (intent_hits * 2.0) + (procedure_hits * 0.35) + source_bonus + page_bonus + length_bonus - penalty

    def _is_useful_evidence(
        self,
        score: float,
        intent_terms: set[str],
        query_type: str,
        chunk: RetrievedChunk,
        is_power_on_question: bool = False,
    ) -> bool:
        text = chunk.text.strip()
        normalized_text = self._normalize_for_match(text)
        intent_hits = sum(1 for term in intent_terms if term in normalized_text)

        if query_type == "falla_alarma":
            if is_power_on_question:
                return (
                    score >= 5.5
                    and len(text) >= 120
                    and self._has_strong_power_on_evidence(text)
                    and intent_hits >= 1
                )
            return score >= 3.0 and len(text) >= 80

        if query_type == "mantenimiento":
            return score >= 3.0 and len(text) >= 80

        return score >= 2.5 and len(text) >= 80

    def _evidence_penalty(
        self,
        normalized_text: str,
        query_type: str,
        is_power_on_question: bool = False,
    ) -> float:
        if query_type != "falla_alarma":
            return 0.0

        penalty = 0.0

        hydraulic_noise = sum(
            1
            for term in (
                "hidraulica",
                "hidraulico",
                "presion de entrada de agua",
                "bomba de desgas",
                "camara de equilibrio",
                "valvula",
                "flujo de 800",
                "manometro",
            )
            if term in normalized_text
        )
        if hydraulic_noise:
            penalty += 4.0

        if is_power_on_question:
            diagram_noise = sum(
                1
                for term in (
                    "circuit diagram",
                    "diagrama de circuito",
                    "component layout diagram",
                    "layout diagram",
                    "output-board",
                    "memoria no volatil",
                    "memoria no volátil",
                    "circuito de monitoreo de voltaje",
                    "monitoring circuit",
                    "celulas de la memoria",
                    "maquina se apaga",
                    "maquina se apaga",
                    "se apaga",
                    "preservados despues",
                )
                if term in normalized_text
            )
            if diagram_noise:
                penalty += 5.0

            if not self._has_strong_power_on_evidence(normalized_text):
                penalty += 3.5

        return penalty

    def _specific_fault_terms(self, question: str) -> set[str]:
        """Extrae t?rminos espec?ficos de una falla/alarma, excluyendo palabras gen?ricas.

        Evita que una consulta como "alarma Oclusi?n en el circuito" sea respondida
        usando chunks que solo contienen palabras gen?ricas como "alarma" o "circuito".
        """
        generic_terms = {
            "alarma",
            "alarm",
            "error",
            "falla",
            "fallo",
            "problema",
            "equipo",
            "maquina",
            "manual",
            "hacer",
            "debo",
            "ante",
            "revisar",
            "verificar",
            "comprobar",
            "circuito",
            "sistema",
            "procedimiento",
            "indica",
            "indicar",
        }
        terms = {
            term
            for term in self._content_terms(question)
            if len(term) >= 4 and term not in generic_terms
        }

        normalized = self._normalize_for_match(question)
        for phrase in (
            "oclusion",
            "occlusion",
            "obstruccion",
            "obstruction",
            "bloqueo",
            "no calibra",
            "no pasa test",
            "no pasa el test",
        ):
            if phrase in normalized:
                terms.add(phrase)

        return terms

    def _chunks_contain_specific_terms(
        self,
        chunks: list[RetrievedChunk],
        specific_terms: set[str],
    ) -> bool:
        if not chunks or not specific_terms:
            return False

        for chunk in chunks:
            normalized_text = self._normalize_for_match(chunk.text)
            if any(term in normalized_text for term in specific_terms):
                return True

        return False

    def _is_power_on_question(self, question: str) -> bool:
        normalized = self._normalize_for_match(question)
        return any(
            phrase in normalized
            for phrase in (
                "no prende",
                "no enciende",
                "no arranca",
                "no funciona",
                "no inicia",
                "no energiza",
                "no tiene energia",
                "no tiene alimentacion",
                "no recibe alimentacion",
                "no recibe energia",
                "no prende la maquina",
                "no enciende la maquina",
            )
        )

    def _has_strong_power_on_evidence(self, text: str) -> bool:
        normalized_text = self._normalize_for_match(text)

        noise_without_procedure = any(
            term in normalized_text
            for term in (
                "circuit diagram",
                "diagrama de circuito",
                "component layout diagram",
                "layout diagram",
                "output-board",
                "memoria no volatil",
                "memoria no volátil",
                "circuito de monitoreo de voltaje",
                "celulas de la memoria",
                "preservados despues",
            )
        )

        power_terms = sum(
            1
            for term in (
                "no prende",
                "no enciende",
                "no arranca",
                "encendido",
                "interruptor de alimentacion",
                "interruptor principal",
                "interruptor",
                "alimentacion electrica",
                "fuente de alimentacion",
                "red electrica",
                "cable de alimentacion",
                "cable de red",
                "enchufe",
                "tomacorriente",
                "fusible",
                "fusibles",
                "tension de red",
                "tension de linea",
                "voltaje de linea",
                "mains",
                "mains voltage",
                "line voltage",
                "power supply",
                "power failure",
                "power switch",
                "main switch",
                "on/off",
            )
            if term in normalized_text
        )

        procedure_terms = sum(
            1
            for term in (
                "verifique",
                "verificar",
                "compruebe",
                "comprobar",
                "revise",
                "revisar",
                "controle",
                "controlar",
                "conecte",
                "conectar",
                "desconecte",
                "desconectar",
                "reemplace",
                "reemplazar",
                "medir",
                "mida",
                "chequear",
                "check",
                "replace",
                "measure",
                "verify",
            )
            if term in normalized_text
        )

        explicit_fault_context = any(
            phrase in normalized_text
            for phrase in (
                "no prende",
                "no enciende",
                "no arranca",
                "does not switch on",
                "does not turn on",
                "will not turn on",
                "power failure",
            )
        )

        if noise_without_procedure and procedure_terms == 0:
            return False

        if explicit_fault_context and power_terms >= 1:
            return True

        return power_terms >= 2 and procedure_terms >= 1

    def _power_on_chunks(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Selecciona evidencia tecnica para la familia de falla 'no prende/no enciende'.

        Es una logica general de Self-RAG: prioriza secciones de alimentacion,
        logica de encendido, tension, fusibles, standby y rele/senal de encendido.
        No esta limitada a un equipo: puede reconocer nombres de placas/senales
        solo cuando aparecen en los fragmentos recuperados o en aliases del equipo.
        """
        scored: list[tuple[float, RetrievedChunk]] = []
        for chunk in chunks:
            text = chunk.text.strip()
            if not text:
                continue

            normalized = self._normalize_for_match(text)
            score = 0.0

            generic_section_terms = (
                "power supply",
                "power logic",
                "power-on logic",
                "power turnon logic",
                "switchon logic",
                "turnon logic",
                "voltage supply",
                "standby voltage",
                "mains",
                "ac input",
                "input voltage",
                "fuente de alimentacion",
                "alimentacion electrica",
                "logica de encendido",
                "lógica de encendido",
                "logica de poder",
                "lógica de poder",
                "logica de potencia",
                "lógica de potencia",
                "tension de descanso",
                "tensión de descanso",
            )
            equipment_specific_section_terms = (
                "p.c.b. lp 638 power supply",
                "lp 638 power supply",
                "lp 638",
                "p.c.b. lp 639 power logic",
                "lp 639 power logic",
                "lp 639",
                "p.c.b. lp 647 power logic",
                "lp 647 power logic",
                "lp 647",
                "fig.: block diagram p.c.b. lp 638 power supply",
                "fig.: block diagram p.c.b. lp 639 power logic",
            )
            control_terms = (
                "on/off key",
                "on/off key on machine",
                "power switch",
                "sw_on_off",
                "cpu_off",
                "auto_on",
                "pwr_off",
                "pwr_res",
                "boton on/off",
                "botón on/off",
                "llave de encendido/apagado",
                "tecla on/off",
                "interruptor de encendido",
                "maquina se encienda",
                "maquina se enciende",
                "machine to be switched on",
                "machine is switched on",
            )
            electrical_detail_terms = (
                "power relay",
                "rele de potencia",
                "relé de potencia",
                "battery relay",
                "current surge relay",
                "standby",
                "220v_l1",
                "220v_n",
                "to_trans",
                "from_trans",
                "+5 v",
                "+12 v",
                "+24 v",
                "5 v",
                "12 v",
                "24 v",
                "undervoltage",
                "overvoltage",
                "baja tension",
                "baja tensión",
                "sobretension",
                "sobretensión",
                "fuse",
                "fusible",
                "fusibles",
                "rectification",
                "rectificacion",
                "rectificación",
            )

            for term in equipment_specific_section_terms:
                if term in normalized:
                    score += 6.5
            for term in generic_section_terms:
                if term in normalized:
                    score += 4.0
            for term in electrical_detail_terms:
                if term in normalized:
                    score += 1.6
            for term in control_terms:
                if term in normalized:
                    score += 1.1

            reliable_page = chunk.citation.reliable_pdf_page()
            if reliable_page is not None:
                score += 1.75
            else:
                confidence = str(chunk.citation.pdf_page_confidence or "").strip().lower()
                if confidence == "approximate":
                    score -= 0.25
                else:
                    score -= 0.75

            hydraulic_noise = any(
                term in normalized
                for term in (
                    "hidraulica",
                    "hidraulico",
                    "bomba de desgas",
                    "camara de equilibrio",
                    "presion de entrada de agua",
                    "flujo de 800",
                )
            )
            if hydraulic_noise:
                score -= 6.0

            generic_settings_noise = any(
                term in normalized
                for term in (
                    "menu item",
                    "default value",
                    "selectable options",
                    "online plus settings",
                    "t1-test autostart",
                    "set rinse-volume",
                )
            )
            if generic_settings_noise:
                score -= 4.0

            has_power_section = any(term in normalized for term in generic_section_terms + equipment_specific_section_terms)
            has_electrical_detail = any(term in normalized for term in electrical_detail_terms)
            if not has_power_section and not has_electrical_detail:
                # Una mencion aislada a la tecla ON/OFF o a una tabla de señales no alcanza.
                score -= 4.0

            if score >= 5.0:
                scored.append((score, chunk))

        scored.sort(
            key=lambda item: (
                item[1].citation.reliable_pdf_page() is not None,
                item[0],
            ),
            reverse=True,
        )

        selected: list[RetrievedChunk] = []
        seen: set[str] = set()
        for _score, chunk in scored:
            key = f"{chunk.citation.source_file}:{chunk.citation.reliable_pdf_page() or chunk.citation.chunk_id}"
            if key in seen:
                continue
            seen.add(key)
            selected.append(chunk)
            if len(selected) >= 5:
                break

        reliable_selected = [chunk for chunk in selected if chunk.citation.reliable_pdf_page() is not None]
        if len(reliable_selected) >= 2:
            # Si existen fuentes verificadas suficientes, se evita mostrar al usuario
            # referencias sin pagina aunque hayan servido como apoyo semantico.
            return reliable_selected[:5]

        return selected

    def _build_power_on_answer(
        self,
        question: str,
        equipment_name: str,
        role: str,
        chunks: list[RetrievedChunk],
    ) -> str:
        if role == "operador":
            return (
                "No hay una indicacion segura para operador sobre una maquina que no enciende. "
                "No intentes abrir el equipo ni revisar componentes internos. "
                "Deja el equipo fuera de uso y contacta al Tecnico de Ingenieria Clinica."
            )

        references = self._summarize_power_on_references(chunks)
        detected_focus = self._summarize_power_on_focus(chunks)

        return (
            f"No encontre en los fragmentos recuperados un checklist unico titulado 'maquina no prende'. "
            f"Si recupere evidencia electrica relacionada con encendido y alimentacion de {equipment_name}.\n\n"
            f"Consulta evaluada: {question}\n\n"
            "Zonas documentales a revisar como tecnico, segun la evidencia recuperada:\n"
            f"{detected_focus}\n\n"
            "Criterio tecnico: no asumir una causa unica. Con esta evidencia, la revision debe orientarse a alimentacion electrica, control de encendido, fusibles/protecciones, tensiones reguladas, standby, senales de ON/OFF y rele o logica de potencia solo cuando esos elementos aparezcan en el manual del equipo consultado.\n\n"
            "Fuentes documentales recuperadas como base tecnica:\n"
            f"{references}\n\n"
            "Limite de la respuesta: esto orienta la busqueda tecnica dentro del manual. No reemplaza el procedimiento oficial de servicio ni autoriza intervenciones fuera de competencia."
        )

    def _summarize_power_on_focus(self, chunks: list[RetrievedChunk]) -> str:
        normalized_text = "\n".join(self._normalize_for_match(chunk.text) for chunk in chunks)
        focus_items: list[str] = []

        checks = (
            (
                "Fuente/alimentacion electrica",
                (
                    "power supply",
                    "fuente de alimentacion",
                    "alimentacion electrica",
                    "mains",
                    "ac input",
                    "input voltage",
                    "line voltage",
                    "tension de red",
                    "tension de linea",
                    "voltaje de linea",
                ),
                "revisar la seccion de fuente o alimentacion electrica recuperada para el equipo.",
            ),
            (
                "Control de encendido",
                (
                    "on/off",
                    "on/off key",
                    "power switch",
                    "interruptor",
                    "tecla on/off",
                    "boton on/off",
                    "llave de encendido",
                    "sw_on_off",
                    "auto_on",
                    "cpu_off",
                    "pwr_off",
                ),
                "revisar tecla/interruptor/senal de encendido solo si el manual la vincula con el encendido del equipo.",
            ),
            (
                "Tensiones y protecciones",
                (
                    "+5 v",
                    "+12 v",
                    "+24 v",
                    "5 v",
                    "12 v",
                    "24 v",
                    "fuse",
                    "fusible",
                    "fusibles",
                    "undervoltage",
                    "overvoltage",
                    "baja tension",
                    "sobretension",
                    "rectification",
                    "rectificacion",
                ),
                "verificar tensiones, fusibles, rectificacion y protecciones segun el procedimiento tecnico del manual.",
            ),
            (
                "Logica de potencia/standby",
                (
                    "power logic",
                    "power-on logic",
                    "power turnon logic",
                    "switchon logic",
                    "standby",
                    "standby voltage",
                    "power relay",
                    "rele de potencia",
                    "power failure",
                    "pwr_res",
                ),
                "revisar logica de potencia, standby, rele o reconocimiento de falla de alimentacion si aparece en las fuentes recuperadas.",
            ),
        )

        for title, terms, recommendation in checks:
            if any(term in normalized_text for term in terms):
                focus_items.append(f"{len(focus_items) + 1}. {title}: {recommendation}")

        if not focus_items:
            return "1. Revisar las secciones electricas recuperadas asociadas a alimentacion o encendido, sin inferir componentes que no aparezcan en el manual."

        return "\n".join(focus_items)

    def _summarize_power_on_references(self, chunks: list[RetrievedChunk]) -> str:
        lines: list[str] = []
        seen: set[str] = set()

        reliable_chunks = [chunk for chunk in chunks if chunk.citation.reliable_pdf_page() is not None]
        chunks_for_references = reliable_chunks if reliable_chunks else chunks

        ordered_chunks = sorted(
            chunks_for_references,
            key=lambda chunk: (
                chunk.citation.reliable_pdf_page() is not None,
                self._power_reference_priority(chunk.text),
            ),
            reverse=True,
        )

        for chunk in ordered_chunks:
            normalized = self._normalize_for_match(chunk.text)

            has_power_section = any(
                term in normalized
                for term in (
                    "lp 638",
                    "lp 639",
                    "lp 647",
                    "power supply",
                    "power logic",
                    "power-on logic",
                    "power turnon logic",
                    "switchon logic",
                    "standby voltage",
                    "power relay",
                    "sw_on_off",
                    "220v_l1",
                    "220v_n",
                    "fuse",
                    "fusible",
                    "+5 v",
                    "+12 v",
                    "+24 v",
                    "fuente de alimentacion",
                    "logica de encendido",
                    "alimentacion electrica",
                )
            )
            if not has_power_section:
                continue

            source = self._source_reference(chunk)
            if source in seen:
                continue
            seen.add(source)

            if "lp 638" in normalized or "power supply" in normalized or "fuente de alimentacion" in normalized:
                topic = "fuente de alimentacion / tensiones reguladas / fusibles / protecciones"
            elif "lp 639" in normalized or "lp 647" in normalized or "power logic" in normalized:
                topic = "logica de encendido / standby / senal ON-OFF / rele de potencia"
            elif "on/off" in normalized or "sw_on_off" in normalized:
                topic = "tecla o senal ON-OFF asociada al encendido"
            else:
                topic = "seccion electrica relacionada con alimentacion o encendido"

            lines.append(f"- {source}: {topic}.")
            if len(lines) >= 4:
                break

        return "\n".join(lines) if lines else "- Se recuperaron fragmentos de alimentacion/encendido, pero sin pagina PDF confiable para mostrar."

    def _power_reference_priority(self, text: str) -> float:
        normalized = self._normalize_for_match(text)
        priority = 0.0
        for term, weight in (
            ("lp 638", 4.0),
            ("lp 639", 4.0),
            ("lp 647", 4.0),
            ("power supply", 3.5),
            ("power logic", 3.5),
            ("power-on logic", 3.5),
            ("power turnon logic", 3.5),
            ("switchon logic", 3.5),
            ("standby voltage", 2.5),
            ("sw_on_off", 2.5),
            ("on/off key", 2.0),
            ("power relay", 2.0),
            ("fuse", 1.5),
            ("fusible", 1.5),
            ("+5 v", 1.0),
            ("+12 v", 1.0),
            ("+24 v", 1.0),
        ):
            if term in normalized:
                priority += weight
        return priority

    def _intent_evidence_terms(self, question: str, query_type: str) -> set[str]:
        normalized = self._normalize_for_match(question)
        terms: set[str] = set()

        if query_type == "falla_alarma":
            terms.update(
                {
                    "alarma",
                    "alarm",
                    "error",
                    "falla",
                    "fallo",
                    "causa",
                    "solucion",
                    "verificar",
                    "compruebe",
                    "revise",
                }
            )

            if any(
                phrase in normalized
                for phrase in (
                    "no prende",
                    "no enciende",
                    "no arranca",
                    "no funciona",
                    "encender",
                    "enciende",
                    "prende",
                    "arranca",
                )
            ):
                terms.update(
                    {
                        "no prende",
                        "no enciende",
                        "no arranca",
                        "encendido",
                        "interruptor",
                        "alimentacion",
                        "alimentacion electrica",
                        "red electrica",
                        "cable",
                        "enchufe",
                        "fusible",
                        "bateria",
                        "fuente de alimentacion",
                        "tension",
                        "voltaje",
                        "voltage",
                        "power",
                        "power failure",
                        "power supply",
                        "mains",
                    }
                )

        if query_type == "mantenimiento":
            terms.update(
                {
                    "mantenimiento",
                    "preventivo",
                    "verificacion",
                    "verificar",
                    "calibracion",
                    "calibrar",
                    "test",
                    "prueba",
                    "control",
                    "ajuste",
                    "reemplazo",
                    "limpieza",
                }
            )

        terms.update(self._content_terms(question))
        return terms

    def _is_power_on_question_text(self, intent_terms: set[str]) -> bool:
        return bool(
            {
                "no prende",
                "no enciende",
                "no arranca",
                "encendido",
                "power failure",
                "power supply",
                "fuente de alimentacion",
            }.intersection(intent_terms)
        )

    def _build_weak_evidence_answer(
        self,
        question: str,
        equipment_name: str,
        role: str,
        evidence: dict,
    ) -> str:
        if role == "operador":
            return (
                "La informacion recuperada no permite resolver esto de forma segura.\n\n"
                "Detene la accion y contacta al Tecnico de Ingenieria Clinica."
            )

        query_type = evidence.get("query_type") or "consulta_tecnica_general"
        reason = str(evidence.get("reason") or "").strip()

        if role == "tecnico" and query_type == "falla_alarma":
            if reason == "sin_procedimiento_literal_de_encendido_alimentacion":
                return (
                    f"No encontre evidencia documental suficiente para indicar un procedimiento tecnico seguro sobre {equipment_name}.\n\n"
                    f"Consulta evaluada: {question}\n\n"
                    "Evaluacion de evidencia: los fragmentos recuperados no contienen instrucciones verificables y directamente aplicables a la falla consultada. "
                    "En particular, no se recupero un procedimiento literal sobre alimentacion electrica, interruptor principal, fusibles, cable de red, tension de linea o fuente de alimentacion.\n\n"
                    "Por seguridad tecnica, no voy a inferir pasos de diagnostico, mediciones, causas probables ni componentes a revisar si no aparecen respaldados en los manuales cargados.\n\n"
                    "Accion tecnica recomendada: consultar el manual de servicio oficial o la seccion electrica correspondiente, o ampliar la consulta con el mensaje, codigo, pantalla observada o condicion exacta del equipo. "
                    "Si el equipo queda inseguro o indisponible, mantenerlo fuera de uso segun el procedimiento del servicio hasta contar con respaldo tecnico suficiente."
                )

            return (
                f"No encontre evidencia documental suficiente para indicar un procedimiento tecnico seguro sobre {equipment_name}.\n\n"
                f"Consulta evaluada: {question}\n\n"
                "Evaluacion de evidencia: los fragmentos recuperados no contienen un procedimiento verificable y directamente relacionado con la falla consultada. "
                "Por seguridad tecnica, no voy a inferir pasos, causas, valores, mediciones ni componentes que no aparezcan respaldados en los manuales cargados.\n\n"
                "Accion tecnica recomendada: revisar el manual de servicio oficial correspondiente o ampliar la consulta con el codigo, alarma, mensaje en pantalla o condicion observada."
            )

        if query_type == "falla_alarma":
            return (
                f"No encontre evidencia documental suficiente para responder de forma segura sobre {equipment_name}.\n\n"
                f"Consulta: {question}\n\n"
                "Los fragmentos recuperados no contienen un procedimiento verificable y directamente relacionado con la falla consultada. "
                "Por seguridad, no voy a inferir pasos, causas, valores ni componentes que no aparezcan respaldados en los manuales cargados.\n\n"
                "Recomendacion segura: detener la intervencion si hay riesgo para paciente, operador o equipo, revisar el manual oficial correspondiente y escalar a Ingenieria Clinica."
            )

        if role == "tecnico":
            return (
                f"No encontre evidencia documental suficiente para indicar una respuesta tecnica segura sobre {equipment_name}.\n\n"
                f"Consulta evaluada: {question}\n\n"
                "La recuperacion fue debil o ambigua. Por seguridad tecnica, no voy a completar la respuesta con conocimiento general ni inferencias fuera de los manuales cargados. "
                "Revise el manual oficial correspondiente o amplie la consulta con datos mas especificos del equipo, alarma, codigo o condicion observada."
            )

        return (
            f"No encontre evidencia documental suficiente para responder de forma segura sobre {equipment_name}.\n\n"
            f"Consulta: {question}\n\n"
            "La recuperacion fue debil o ambigua. Por seguridad, no voy a completar la respuesta con conocimiento general ni inferencias fuera de los manuales cargados."
        )

    def _prepend_partial_evidence_notice(self, answer: str) -> str:
        notice = (
            "Aviso: la evidencia documental recuperada es parcial. "
            "La respuesta se limita a los fragmentos disponibles y no debe interpretarse como procedimiento completo si el manual no lo respalda.\n\n"
        )
        if answer.startswith("Aviso: la evidencia documental recuperada es parcial"):
            return answer
        return notice + answer

    def _detect_exact_codes(self, question: str) -> list[str]:
        normalized = question.upper()
        codes: list[str] = []

        patterns = [
            r"\b[A-Z]{2,}[A-Z0-9]*_[A-Z0-9_]{2,}\b",
            r"\bF\d{1,3}\b",
            r"\bT\d+\s+TEST(?:\s+UNSUCCESSFUL)?\b",
            r"\bM\d+\s*-\s*\d+[A-Z0-9]+\b",
        ]
        for pattern in patterns:
            for match in re.findall(pattern, normalized):
                clean = re.sub(r"\s+", " ", match.strip())
                if clean not in codes:
                    codes.append(clean)

        return codes

    def _chunks_containing_codes(self, chunks: list[RetrievedChunk], codes: list[str]) -> list[RetrievedChunk]:
        matches: list[RetrievedChunk] = []
        for chunk in chunks:
            normalized_text = chunk.text.upper()
            compact_text = re.sub(r"\s+", "", normalized_text)
            for code in codes:
                compact_code = re.sub(r"\s+", "", code.upper())
                if code.upper() in normalized_text or compact_code in compact_text:
                    matches.append(chunk)
                    break
        return matches[:5]

    def _build_code_lookup_answer(
        self,
        question: str,
        codes: list[str],
        chunks: list[RetrievedChunk],
    ) -> str:
        blocks = []
        for index, chunk in enumerate(chunks, start=1):
            extract = self._extract_code_context(chunk.text, codes)
            if not extract:
                extract = self._compact_extract_text(chunk.text.strip())[:700]
            extract = self._strip_markdown_markers(extract)
            blocks.append(
                f"{self._source_reference(chunk)}\n"
                f"Extracto literal {index}\n"
                f"{extract}"
            )

        return (
            "Modo extractivo para codigo tecnico exacto.\n"
            f"Consulta: {question}\n"
            f"Codigo detectado: {', '.join(codes)}\n\n"
            "A continuacion se muestra solo lo que aparece en los fragmentos recuperados. "
            "No se infiere causa, efecto, activacion, desactivacion ni procedimiento si el manual no lo indica literalmente.\n\n"
            + "\n\n---\n\n".join(blocks)
        )

    def _build_code_not_found_answer(self, equipment_name: str, codes: list[str]) -> str:
        return (
            f"No encontre el codigo tecnico exacto {', '.join(codes)} en los fragmentos recuperados para {equipment_name}.\n\n"
            "Por seguridad, no voy a interpretar el codigo ni deducir su funcion sin respaldo literal del manual. "
            "Revise el manual oficial o amplie la consulta con el mensaje completo de alarma/error."
        )

    def _extract_code_context(self, text: str, codes: list[str]) -> str:
        normalized_lines = [line.strip() for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines()]
        selected: list[str] = []
        for index, line in enumerate(normalized_lines):
            upper_line = line.upper()
            compact_line = re.sub(r"\s+", "", upper_line)
            found = any(
                code.upper() in upper_line or re.sub(r"\s+", "", code.upper()) in compact_line
                for code in codes
            )
            if not found:
                continue

            start = max(0, index - 2)
            end = min(len(normalized_lines), index + 3)
            for context_line in normalized_lines[start:end]:
                if context_line and context_line not in selected:
                    selected.append(context_line)

        if selected:
            return "\n".join(selected)[:1200]

        upper_text = text.upper()
        for code in codes:
            position = upper_text.find(code.upper())
            if position >= 0:
                start = max(0, position - 350)
                end = min(len(text), position + 650)
                return text[start:end].strip()

        return ""

    def _build_document_inventory_answer(self, equipment_name: str) -> str:
        return (
            "Esta consulta corresponde al estado de manuales/documentos cargados, no a una pregunta tecnica del equipo seleccionado.\n\n"
            "Para ver manuales cargados, fuentes, fecha de indexacion o auditoria documental, use la pantalla de Manuales cargados o el Centro de Monitoreo.\n\n"
            f"En este chat puedo responder consultas tecnicas sobre {equipment_name}, siempre con respaldo en los manuales recuperados."
        )

    def _content_terms(self, text: str) -> set[str]:
        normalized = self._normalize_for_match(text)
        stopwords = {
            "que",
            "debo",
            "debe",
            "deben",
            "para",
            "como",
            "cuando",
            "donde",
            "cual",
            "cuales",
            "esta",
            "este",
            "esto",
            "esa",
            "ese",
            "los",
            "las",
            "una",
            "uno",
            "por",
            "con",
            "sin",
            "del",
            "las",
            "los",
            "equipo",
            "maquina",
            "máquina",
            "revisar",
            "revise",
            "hacer",
            "hago",
            "debe",
        }
        return {
            token
            for token in re.findall(r"[a-z0-9_]+", normalized)
            if len(token) >= 3 and token not in stopwords
        }

    def _normalize_for_match(self, value: str | None) -> str:
        normalized = (value or "").lower()
        replacements = {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n",
        }
        for source, target in replacements.items():
            normalized = normalized.replace(source, target)
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized.strip()

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
        cleaned = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+", "", cleaned)
        cleaned = re.sub(r"(?m)^\s*[¹²³⁴⁵⁶⁷⁸⁹⁰]+\s*", "", cleaned)
        cleaned = re.sub(r"\s+([.,;:])", r"\1", cleaned)
        cleaned = re.sub(r" {2,}", " ", cleaned)
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

    def _build_retrieval_question(self, question: str, history: list[dict], equipment_name: str | None = None) -> str:
        expanded_question = question
        normalized = question.lower()

        expansion_terms: list[str] = []

        if self._is_power_on_question(question):
            # Self-RAG general por familia de falla: una pregunta corta como
            # "no prende" se expande hacia conceptos de alimentacion/encendido.
            # La expansion se mantiene corta para no exceder el contexto del modelo
            # de embeddings de Ollama.
            expansion_terms.extend(
                [
                    "no prende",
                    "no enciende",
                    "no arranca",
                    "power on",
                    "power-on logic",
                    "power turnon logic",
                    "on/off key",
                    "power switch",
                    "power supply",
                    "power logic",
                    "standby voltage",
                    "power relay",
                    "mains",
                    "AC input",
                    "fuse",
                    "battery relay",
                    "undervoltage",
                    "overvoltage",
                    "+5 V",
                    "+12 V",
                    "+24 V",
                ]
            )

            # Aliases especificos por equipo para mejorar recuperacion.
            # No fuerzan la respuesta: solo agregan vocabulario tecnico que el manual usa.
            equipment_normalized = self._normalize_for_match(equipment_name)
            if "fresenius" in equipment_normalized and "4008" in equipment_normalized:
                expansion_terms.extend(
                    [
                        "P.C.B. LP 638 Power supply",
                        "P.C.B. LP 639 Power logic",
                        "P.C.B. LP 647 Power logic A",
                        "SW_ON_OFF",
                        "AUTO_ON",
                        "CPU_OFF",
                        "PWR_OFF",
                        "PWR_RES",
                        "220V_L1",
                        "220V_N",
                    ]
                )

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

        expanded_question = self._limit_retrieval_query(expanded_question)

        # Para fallas de encendido, no se usa historial conversacional en la busqueda:
        # una respuesta previa mala puede contaminar la recuperacion y, ademas,
        # puede exceder el limite de contexto del modelo de embeddings.
        if not history or self._is_power_on_question(question):
            return expanded_question

        recent_context = "\n".join(
            f"{message['role']}: {message['content'][:220]}"
            for message in history[-2:]
        )
        return self._limit_retrieval_query(f"{recent_context}\nPregunta actual: {expanded_question}")

    def _limit_retrieval_query(self, text: str, max_chars: int = 1800) -> str:
        normalized = text.strip()
        if len(normalized) <= max_chars:
            return normalized
        return normalized[:max_chars].rsplit(" ", 1)[0].strip()

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
