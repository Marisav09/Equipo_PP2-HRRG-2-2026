from __future__ import annotations

from functools import cached_property
import json
from typing import Any

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings
from app.core.equipment_catalog import canonical_equipment_name
from app.core.exceptions import EquipmentScopeError, VectorstoreNotReadyError
from app.models.schemas import RetrievedChunk, SourceCitation


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

        Esta lista representa el estado real del índice vectorial, no la auditoría
        histórica de ingestas. Se usa para que la interfaz no muestre documentos
        excluidos o registros viejos que ya no están indexados.
        """
        collection = self.get_store()._collection
        if collection.count() == 0:
            return []

        result = collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []

        sources: dict[str, dict[str, Any]] = {}
        pages_by_source: dict[str, set[int]] = {}

        for metadata in metadatas:
            if not metadata:
                continue

            source_file = str(metadata.get("source_file") or "").strip()
            if not source_file:
                continue

            current = sources.setdefault(
                source_file,
                {
                    "source_file": source_file,
                    "status": "indexed",
                    "equipment_id": metadata.get("equipment_id"),
                    "equipment_name": metadata.get("equipment_name") or metadata.get("equipo"),
                    "page_count": 0,
                    "chunk_count": 0,
                    "image_count": 0,
                    "message": "Documento presente en ChromaDB.",
                    "created_at": "",
                },
            )

            current["chunk_count"] += 1

            page = metadata.get("page")
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

        search_filter = self._equipment_filter(canonical_equipment)
        results = vectorstore.similarity_search_with_score(
            question,
            k=k or settings.retrieval_k,
            filter=search_filter,
        )

        chunks: list[RetrievedChunk] = []
        for document, score in results:
            chunk = self._document_to_chunk(document, float(score), canonical_equipment)
            if chunk.citation.equipment_name == canonical_equipment:
                chunks.append(chunk)
        return chunks

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
        citation = SourceCitation(
            source_file=str(metadata.get("source_file", "sin_fuente")),
            page=metadata.get("page", "sin_pagina"),
            chunk_id=str(metadata.get("chunk_id", "sin_chunk")),
            equipment_name=equipment_name or expected_equipment,
            has_images=bool(metadata.get("has_images", False)),
            image_count=int(metadata.get("image_count", 0) or 0),
            url=str(metadata.get("source_url") or ""),
            images=self._decode_images(metadata.get("image_refs")),
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
        page = metadata.get("page", "sin_pagina")
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