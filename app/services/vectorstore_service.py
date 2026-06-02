from __future__ import annotations

from functools import cached_property
import json
import re
import unicodedata
from typing import Any

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings
from app.core.equipment_catalog import canonical_equipment_name
from app.core.exceptions import EquipmentScopeError, VectorstoreNotReadyError
from app.models.schemas import RetrievedChunk, SourceCitation
from app.services.ingestion_audit_service import IngestionAuditService


class VectorstoreService:
    """Single access point for ChromaDB.

    The service intentionally refuses unscoped retrieval. Clinical equipment
    manuals must not be mixed, even when a query looks generic.
    """

    def __init__(self) -> None:
        settings.ensure_directories()

    @cached_property
    def embeddings(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    def get_store(self) -> Chroma:
        return Chroma(
            collection_name=settings.collection_name,
            persist_directory=str(settings.vectorstore_dir),
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: list[Document]) -> int:
        if not documents:
            return 0

        vectorstore = self.get_store()
        for start in range(0, len(documents), settings.embedding_batch_size):
            batch = documents[start : start + settings.embedding_batch_size]
            ids = [
                self._document_id(document, start + index)
                for index, document in enumerate(batch)
            ]
            vectorstore.add_documents(documents=batch, ids=ids)
        return len(documents)

    def delete_source(self, source_file: str) -> None:
        self.get_store()._collection.delete(where={"source_file": source_file})

    def delete_sources_except(self, allowed_sources: set[str]) -> int:
        collection = self.get_store()._collection
        if collection.count() == 0:
            return 0

        result = collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []
        stale_sources = {
            str(metadata.get("source_file", "")).strip()
            for metadata in metadatas
            if metadata and str(metadata.get("source_file", "")).strip() not in allowed_sources
        }
        for source_file in stale_sources:
            collection.delete(where={"source_file": source_file})
        return len(stale_sources)

    def list_equipments(self) -> list[str]:
        collection = self.get_store()._collection
        if collection.count() == 0:
            return []

        result = collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []
        equipments = {
            str(metadata.get("equipment_name") or metadata.get("equipo")).strip()
            for metadata in metadatas
            if metadata and (metadata.get("equipment_name") or metadata.get("equipo"))
        }
        return sorted(equipments)

    def list_indexed_sources(self) -> list[dict[str, Any]]:
        """Devuelve las fuentes realmente presentes en ChromaDB.

        Esta lista representa el estado real del indice vectorial, no la auditoria
        historica de ingestas. Se usa para que la interfaz no muestre documentos
        excluidos o registros viejos que ya no estan indexados.

        La cantidad de paginas se calcula solo con paginas PDF verificadas.
        No se usa markdown_page ni page como reemplazo de pagina PDF oficial.
        """
        collection = self.get_store()._collection
        if collection.count() == 0:
            return []

        result = collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []

        sources: dict[str, dict[str, Any]] = {}
        pages_by_source: dict[str, set[int]] = {}
        audits_by_source = {
            str(item.get("source_file") or ""): item
            for item in IngestionAuditService().list_latest()
        }

        for metadata in metadatas:
            if not metadata:
                continue

            source_file = str(metadata.get("source_file") or "").strip()
            if not source_file:
                continue

            display_source = str(
                metadata.get("display_source")
                or metadata.get("original_pdf")
                or source_file
            ).strip()

            current = sources.setdefault(
                source_file,
                {
                    "source_file": source_file,
                    "display_source": display_source,
                    "original_pdf": metadata.get("original_pdf") or "",
                    "status": "indexed",
                    "equipment_id": metadata.get("equipment_id"),
                    "equipment_name": metadata.get("equipment_name") or metadata.get("equipo"),
                    "page_count": 0,
                    "chunk_count": 0,
                    "image_count": 0,
                    "message": "Documento presente en ChromaDB.",
                    "created_at": str(audits_by_source.get(source_file, {}).get("created_at") or ""),
                    "source_url": str(metadata.get("source_url") or ""),
                },
            )

            if not current.get("source_url") and metadata.get("source_url"):
                current["source_url"] = str(metadata.get("source_url") or "")

            current["chunk_count"] += 1

            pdf_page_confidence = str(metadata.get("pdf_page_confidence") or "").strip().lower()
            if pdf_page_confidence == "verified":
                page = metadata.get("pdf_page")
                if page not in (None, "", "sin_pagina"):
                    try:
                        page_number = int(page)
                    except (TypeError, ValueError):
                        page_number = 0

                    if page_number > 0:
                        pages_by_source.setdefault(source_file, set()).add(page_number)

            try:
                current["image_count"] += int(metadata.get("image_count", 0) or 0)
            except (TypeError, ValueError):
                pass

        for source_file, pages in pages_by_source.items():
            if source_file in sources:
                sources[source_file]["page_count"] = len(pages)

        return sorted(sources.values(), key=lambda item: str(item["source_file"]))

    def retrieve(
        self,
        question: str,
        equipment_name: str | None,
        k: int | None = None,
    ) -> list[RetrievedChunk]:
        canonical_equipment = canonical_equipment_name(equipment_name)
        if not canonical_equipment:
            raise EquipmentScopeError("La busqueda documental requiere un equipo exacto.")

        vectorstore = self.get_store()
        if vectorstore._collection.count() == 0:
            raise VectorstoreNotReadyError("La base vectorial no tiene documentos indexados.")

        requested_k = k or settings.retrieval_k
        candidate_k = self._candidate_k(question, requested_k)
        search_filter = self._equipment_filter(canonical_equipment)
        expanded_question = self._expand_question(question)

        results = vectorstore.similarity_search_with_score(
            expanded_question,
            k=candidate_k,
            filter=search_filter,
        )

        chunks: list[RetrievedChunk] = []
        for document, score in results:
            chunk = self._document_to_chunk(document, float(score), canonical_equipment)
            if chunk.citation.equipment_name == canonical_equipment:
                chunks.append(chunk)

        ranked_chunks = self._rerank_chunks(question, chunks)
        focused_chunks = self._focus_curated_alarm_context(question, ranked_chunks)
        return focused_chunks[:requested_k]

    def _candidate_k(self, question: str, requested_k: int) -> int:
        normalized = self._normalize_for_ranking(question)
        alarm_or_failure = any(
            term in normalized
            for term in (
                "alarma",
                "mensaje",
                "falla",
                "fallo",
                "error",
                "problema",
                "no funciona",
                "no prende",
                "no responde",
                "obstru",
                "oclusion",
                "bloqueo",
                "circuito",
            )
        )

        if alarm_or_failure:
            return max(requested_k, 80)

        return max(requested_k, settings.retrieval_k)

    def _expand_question(self, question: str) -> str:
        normalized = self._normalize_for_ranking(question)
        expansions: list[str] = []

        if any(term in normalized for term in ("alarma", "mensaje", "falla", "fallo", "error")):
            expansions.append(
                "alarma resolucion de problemas mensaje prioridad posible causa accion medidas"
            )

        if "circuito" in normalized and any(
            term in normalized
            for term in ("oclusion", "obstru", "bloqueo", "destap", "tapado")
        ):
            expansions.append(
                "bloqueo circuito paciente oclusion circuito circuito obstruido "
                "filtro bloqueado cuerpos extranos circuito paciente puerto salida gas obstruido "
                "presion inspiratoria presion espiratoria"
            )

        if not expansions:
            return question

        return f"{question}\n\n" + "\n".join(expansions)

    def _rerank_chunks(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        normalized_question = self._normalize_for_ranking(question)

        def ranking_key(index_and_chunk: tuple[int, RetrievedChunk]) -> tuple[float, int]:
            index, chunk = index_and_chunk
            bonus = self._lexical_bonus(normalized_question, chunk)
            penalty = self._lexical_penalty(normalized_question, chunk)
            adjusted_score = float(chunk.score) - bonus + penalty
            return (adjusted_score, index)

        return [
            chunk
            for _, chunk in sorted(
                enumerate(chunks),
                key=ranking_key,
            )
        ]

    def _focus_curated_alarm_context(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        normalized_question = self._normalize_for_ranking(question)
        circuit_obstruction_query = (
            "circuito" in normalized_question
            and any(
                term in normalized_question
                for term in ("oclusion", "obstru", "bloqueo", "destap", "tapado")
            )
        )
        if not circuit_obstruction_query:
            return chunks

        curated_chunks = [
            chunk
            for chunk in chunks
            if "alarma curada bloqueo circuito paciente" in self._normalize_for_ranking(chunk.text)
        ]
        if not curated_chunks:
            return chunks

        primary = curated_chunks[0]
        focused: list[RetrievedChunk] = [primary]

        for chunk in chunks:
            if chunk is primary:
                continue

            text = self._normalize_for_ranking(chunk.text)
            exact_same_alarm = (
                "bloqueo circuito paciente" in text
                and "presion inspiratoria" in text
                and "presion espiratoria" in text
            )
            exact_actions = (
                "cuerpos extranos" in text
                and "puerto de salida de gas" in text
            )

            if exact_same_alarm or exact_actions:
                focused.append(chunk)

            if len(focused) >= 3:
                break

        return focused

    def _lexical_bonus(self, normalized_question: str, chunk: RetrievedChunk) -> float:
        text = self._normalize_for_ranking(chunk.text)
        source = self._normalize_for_ranking(
            " ".join(
                (
                    chunk.citation.display_source or "",
                    chunk.citation.original_pdf or "",
                    chunk.citation.source_file or "",
                )
            )
        )

        bonus = 0.0

        circuit_obstruction_query = (
            "circuito" in normalized_question
            and any(
                term in normalized_question
                for term in ("oclusion", "obstru", "bloqueo", "destap", "tapado")
            )
        )

        if circuit_obstruction_query:
            exact_phrases = (
                "alarma curada bloqueo circuito paciente",
                "bloqueo circuito paciente",
                "circuito obstruido",
                "filtro bloqueado",
                "cuerpos extranos",
                "puerto de salida de gas",
                "presion inspiratoria",
                "presion espiratoria",
            )
            for phrase in exact_phrases:
                if phrase in text:
                    bonus += 4.0

            if "manual de usuario" in text or "manual de usuario" in source:
                bonus += 1.5
            if "manual tecnico" in source:
                bonus -= 0.5
            if "acciones indicadas por el manual" in text:
                bonus += 4.0
            if "posible causa indicada por el manual" in text:
                bonus += 3.0
            if "alarma resolucion de problemas" in text:
                bonus += 2.0

        question_terms = {
            term
            for term in normalized_question.split()
            if len(term) >= 5 and term not in {"equipo", "mensaje", "manual", "seguir"}
        }
        if question_terms:
            overlap = sum(1 for term in question_terms if term in text)
            bonus += min(overlap * 0.2, 2.0)

        return bonus

    def _lexical_penalty(self, normalized_question: str, chunk: RetrievedChunk) -> float:
        text = self._normalize_for_ranking(chunk.text)
        source = self._normalize_for_ranking(
            " ".join(
                (
                    chunk.citation.display_source or "",
                    chunk.citation.original_pdf or "",
                    chunk.citation.source_file or "",
                )
            )
        )

        penalty = 0.0

        # Caso VN500:
        # BabyFlow / CPAP nasal es una fuente lateral del respirador Draeger VN500.
        # Debe usarse cuando la consulta menciona explícitamente BabyFlow, CPAP,
        # nCPAP, nasal, canula, mascara o contexto neonatal.
        # Para consultas generales del respirador sobre test, alarmas, presion,
        # ventilacion o funcionamiento, se penaliza para evitar respuestas con
        # una fuente correcta por equipo pero incorrecta por alcance documental.
        babyflow_source = any(
            term in source
            for term in (
                "babyflow",
                "cpap nasal",
                "ncpap",
            )
        ) or any(
            term in text
            for term in (
                "babyflow",
                "cpap nasal",
                "ncpap",
                "canulas nasales",
                "mascaras",
                "gorros",
            )
        )

        babyflow_query = any(
            term in normalized_question
            for term in (
                "babyflow",
                "cpap",
                "ncpap",
                "nasal",
                "canula",
                "canulas",
                "mascara",
                "mascaras",
                "neonatal",
                "neonato",
                "neonatos",
                "interfaz",
                "gorros",
            )
        )

        if babyflow_source and not babyflow_query:
            penalty += 3.0

        circuit_obstruction_query = (
            "circuito" in normalized_question
            and any(
                term in normalized_question
                for term in ("oclusion", "obstru", "bloqueo", "destap", "tapado")
            )
        )

        if circuit_obstruction_query:
            false_positive_phrases = (
                "barra favoritos",
                "pantalla tactil",
                "bloqueo desbloqueo",
                "bloquear o desbloquear la pantalla",
                "tendencias",
                "configuracion de favoritos",
                "visualizacion de curvas",
                "piezas",
            )
            for phrase in false_positive_phrases:
                if phrase in text:
                    penalty += 4.0

        return penalty

    def _normalize_for_ranking(self, value: str | None) -> str:
        if not value:
            return ""

        without_accents = unicodedata.normalize("NFKD", value)
        ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
        compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).strip().lower()
        return re.sub(r"\s+", " ", compact)

    def _equipment_filter(self, equipment_name: str) -> dict[str, str]:
        return {"equipment_name": equipment_name}

    def _document_to_chunk(
        self,
        document: Document,
        score: float,
        expected_equipment: str,
    ) -> RetrievedChunk:
        metadata: dict[str, Any] = document.metadata or {}
        equipment_name = str(metadata.get("equipment_name") or metadata.get("equipo") or "").strip()

        pdf_page = metadata.get("pdf_page") or ""
        markdown_page = metadata.get("markdown_page", "")
        pdf_page_confidence = str(metadata.get("pdf_page_confidence") or "").strip()
        page_mapping_method = str(metadata.get("page_mapping_method") or "").strip()
        page_mapping_status = str(metadata.get("page_mapping_status") or "").strip()

        citation = SourceCitation(
            source_file=str(metadata.get("source_file", "sin_fuente")),
            page=pdf_page or "sin_pagina",
            chunk_id=str(metadata.get("chunk_id", "sin_chunk")),
            equipment_name=equipment_name or expected_equipment,
            has_images=bool(metadata.get("has_images", False)),
            image_count=int(metadata.get("image_count", 0) or 0),
            url=str(metadata.get("source_url") or ""),
            images=self._decode_images(metadata.get("image_refs")),
            display_source=str(metadata.get("display_source") or ""),
            original_pdf=str(metadata.get("original_pdf") or ""),
            pdf_page=pdf_page,
            pdf_page_confidence=pdf_page_confidence,
            page_mapping_method=page_mapping_method,
            page_mapping_status=page_mapping_status,
            markdown_page=markdown_page,
        )
        return RetrievedChunk(
            text=document.page_content,
            citation=citation,
            score=score,
        )

    def _document_id(self, document: Document, index: int) -> str:
        metadata = document.metadata or {}
        equipment = str(metadata.get("equipment_name", "sin_equipo")).replace(" ", "_")
        source = str(metadata.get("source_file", "documento")).replace(" ", "_")
        page = metadata.get("markdown_page") or metadata.get("page", "sin_pagina")
        chunk_id = metadata.get("chunk_id", index)
        return f"{equipment}::{source}::p{page}::c{chunk_id}"

    def _decode_images(self, value: Any) -> tuple[dict[str, Any], ...]:
        if not value:
            return ()
        try:
            parsed = json.loads(str(value))
        except (TypeError, ValueError):
            return ()
        if not isinstance(parsed, list):
            return ()
        images = []
        for item in parsed:
            if isinstance(item, dict) and item.get("url"):
                images.append(
                    {
                        "url": str(item.get("url")),
                        "page": item.get("page"),
                        "label": str(item.get("label") or "Imagen"),
                    }
                )
        return tuple(images)