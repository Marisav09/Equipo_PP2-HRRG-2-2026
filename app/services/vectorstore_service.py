from __future__ import annotations

from functools import cached_property

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings
from app.core.equipment_catalog import GENERAL_EQUIPMENT_LABEL, canonical_equipment_label
from app.core.exceptions import VectorstoreNotReadyError
from app.models.schemas import RetrievedChunk, SourceCitation


class VectorstoreService:
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
                f"{doc.metadata.get('source_file', 'documento')}::p{doc.metadata.get('page', 'sin_pagina')}::c{doc.metadata.get('chunk_id', start + index)}"
                for index, doc in enumerate(batch, start=1)
            ]
            vectorstore.add_documents(documents=batch, ids=ids)
        return len(documents)

    def delete_source(self, source_file: str) -> None:
        vectorstore = self.get_store()
        vectorstore._collection.delete(where={"source_file": source_file})

    def list_equipments(self) -> list[str]:
        vectorstore = self.get_store()
        if vectorstore._collection.count() == 0:
            return []

        result = vectorstore._collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []
        equipments = {
            str(metadata.get("equipo")).strip()
            for metadata in metadatas
            if metadata and metadata.get("equipo")
        }
        return sorted(equipments)

    def retrieve(self, question: str, equipment: str | None = None, k: int | None = None) -> list[RetrievedChunk]:
        vectorstore = self.get_store()
        collection_count = vectorstore._collection.count()

        if collection_count == 0:
            raise VectorstoreNotReadyError(
                "La base vectorial no tiene documentos. Ejecuta primero la ingesta."
            )

        # ARQUITECTURA DE SEGURIDAD: Filtro duro por metadatos
        canonical_equipment = canonical_equipment_label(equipment)
        if not canonical_equipment or canonical_equipment == GENERAL_EQUIPMENT_LABEL:
            return []

        search_filter = {"equipo": canonical_equipment}

        results = vectorstore.similarity_search_with_score(
            question,
            k=k or settings.retrieval_k,
            filter=search_filter  # ChromaDB aplicará este filtro antes de calcular la similitud
        )

        chunks: list[RetrievedChunk] = []
        for document, score in results:
            metadata = document.metadata
            citation = SourceCitation(
                source_file=str(metadata.get("source_file", "sin_fuente")),
                page=metadata.get("page", "sin_pagina"),
                chunk_id=str(metadata.get("chunk_id", "sin_chunk")),
                has_images=bool(metadata.get("has_images", False)),
                image_count=int(metadata.get("image_count", 0) or 0),
            )
            chunks.append(
                RetrievedChunk(
                    text=document.page_content,
                    citation=citation,
                    score=float(score),
                )
            )

        return chunks
