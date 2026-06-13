from __future__ import annotations

from functools import cached_property
import json
import logging
import math
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


logger = logging.getLogger(__name__)


class VectorstoreService:
    """Hybrid retrieval over child chunks with role-aware parent-page expansion."""

    def __init__(self) -> None:
        settings.ensure_directories()
        self._lexical_cache: dict[str, tuple[list[Document], Any]] = {}

    @cached_property
    def embeddings(self) -> OllamaEmbeddings:
        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    @cached_property
    def reranker(self):
        from sentence_transformers import CrossEncoder

        device = self._resolve_reranker_device()
        try:
            return CrossEncoder(settings.reranker_model, device=device)
        except Exception:
            if device == "cpu":
                raise
            logger.exception(
                "No se pudo inicializar el reranker en %s; se reintenta en CPU.",
                device,
            )
            return CrossEncoder(settings.reranker_model, device="cpu")

    def _resolve_reranker_device(self) -> str:
        configured = str(settings.reranker_device or "auto").strip().lower()
        if configured != "auto":
            return configured

        try:
            import torch

            return "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            return "cpu"

    def get_store(self) -> Chroma:
        return Chroma(
            collection_name=settings.collection_name,
            persist_directory=str(settings.vectorstore_dir),
            embedding_function=self.embeddings,
        )

    def get_page_store(self) -> Chroma:
        return Chroma(
            collection_name=settings.page_collection_name,
            persist_directory=str(settings.vectorstore_dir),
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: list[Document]) -> int:
        if not documents:
            return 0
        self._add_in_batches(self.get_store(), documents, parent=False)
        self._lexical_cache.clear()
        return len(documents)

    def add_page_documents(self, documents: list[Document]) -> int:
        if not documents:
            return 0

        store = self.get_page_store()
        collection = store._collection
        for start in range(0, len(documents), settings.embedding_batch_size):
            batch = documents[start : start + settings.embedding_batch_size]
            embedding_inputs = [
                document.page_content[: settings.parent_embedding_max_chars]
                for document in batch
            ]
            collection.add(
                ids=[self._document_id(document, start + index) for index, document in enumerate(batch)],
                embeddings=self.embeddings.embed_documents(embedding_inputs),
                documents=[document.page_content for document in batch],
                metadatas=[document.metadata for document in batch],
            )
        return len(documents)

    def _add_in_batches(self, store: Chroma, documents: list[Document], parent: bool) -> None:
        for start in range(0, len(documents), settings.embedding_batch_size):
            batch = documents[start : start + settings.embedding_batch_size]
            ids = [self._document_id(document, start + index) for index, document in enumerate(batch)]
            store.add_documents(documents=batch, ids=ids)

    def delete_source(self, source_file: str) -> None:
        self.get_store()._collection.delete(where={"source_file": source_file})
        self.get_page_store()._collection.delete(where={"source_file": source_file})
        self._lexical_cache.clear()

    def delete_sources_except(self, allowed_sources: set[str]) -> int:
        stale_sources: set[str] = set()
        for collection in (self.get_store()._collection, self.get_page_store()._collection):
            if collection.count() == 0:
                continue
            result = collection.get(include=["metadatas"])
            for metadata in result.get("metadatas") or []:
                source = str((metadata or {}).get("source_file") or "").strip()
                if source and source not in allowed_sources:
                    stale_sources.add(source)
        for source in stale_sources:
            self.delete_source(source)
        return len(stale_sources)

    def list_equipments(self) -> list[str]:
        collection = self.get_store()._collection
        if collection.count() == 0:
            return []
        result = collection.get(include=["metadatas"])
        return sorted(
            {
                str(metadata.get("equipment_name") or metadata.get("equipo")).strip()
                for metadata in result.get("metadatas") or []
                if metadata and (metadata.get("equipment_name") or metadata.get("equipo"))
            }
        )

    def list_indexed_sources(self) -> list[dict[str, Any]]:
        collection = self.get_store()._collection
        if collection.count() == 0:
            return []

        result = collection.get(include=["metadatas"])
        audits_by_source = {
            str(item.get("source_file") or ""): item
            for item in IngestionAuditService().list_latest()
        }
        sources: dict[str, dict[str, Any]] = {}
        pages_by_source: dict[str, set[int]] = {}

        for metadata in result.get("metadatas") or []:
            if not metadata:
                continue
            source_file = str(metadata.get("source_file") or "").strip()
            if not source_file:
                continue
            current = sources.setdefault(
                source_file,
                {
                    "source_file": source_file,
                    "display_source": metadata.get("display_source") or metadata.get("original_pdf") or source_file,
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
            current["chunk_count"] += 1
            current["image_count"] += int(metadata.get("image_count", 0) or 0)
            if str(metadata.get("pdf_page_confidence") or "").lower() == "verified":
                try:
                    pages_by_source.setdefault(source_file, set()).add(int(metadata.get("pdf_page")))
                except (TypeError, ValueError):
                    pass

        for source_file, pages in pages_by_source.items():
            sources[source_file]["page_count"] = len(pages)
        return sorted(sources.values(), key=lambda item: str(item["source_file"]))

    def retrieve(
        self,
        question: str,
        equipment_name: str | None,
        k: int | None = None,
        role: str = "tecnico",
    ) -> list[RetrievedChunk]:
        canonical_equipment = canonical_equipment_name(equipment_name)
        if not canonical_equipment:
            raise EquipmentScopeError("La busqueda documental requiere un equipo exacto.")

        store = self.get_store()
        if store._collection.count() == 0:
            raise VectorstoreNotReadyError("La base vectorial no tiene documentos indexados.")

        semantic = self._semantic_candidates(question, canonical_equipment)
        lexical = self._lexical_candidates(question, canonical_equipment)
        candidates = self._merge_candidates(semantic, lexical)
        ranked = self._cross_encoder_rerank(question, candidates)
        if not ranked:
            return []

        if role == "operador":
            return self._operator_context(question, canonical_equipment, ranked, k)
        return self._technician_context(question, canonical_equipment, ranked)

    def _semantic_candidates(self, question: str, equipment_name: str) -> list[RetrievedChunk]:
        results = self.get_store().similarity_search_with_score(
            question,
            k=settings.semantic_candidate_k,
            filter={"equipment_name": equipment_name},
        )
        chunks = []
        for document, distance in results:
            chunk = self._document_to_chunk(document, self._semantic_score(float(distance)), equipment_name)
            if chunk.citation.equipment_name == equipment_name:
                chunks.append(chunk)
        return chunks

    def _lexical_candidates(self, question: str, equipment_name: str) -> list[RetrievedChunk]:
        documents, bm25 = self._lexical_index(equipment_name)
        if not documents:
            return []

        tokens = self._tokenize(question)
        if not tokens:
            return []
        raw_scores = list(bm25.get_scores(tokens))
        normalized_scores = self._minmax(raw_scores)
        query_terms = set(tokens)
        tokenized_documents = [self._tokenize(document.page_content) for document in documents]
        overlap_scores = [
            len(query_terms.intersection(document_tokens)) / max(1, len(query_terms))
            for document_tokens in tokenized_documents
        ]
        lexical_scores = [
            (0.8 * normalized_scores[index]) + (0.2 * overlap_scores[index])
            for index in range(len(documents))
        ]
        ranked_indexes = sorted(
            range(len(documents)),
            key=lambda index: lexical_scores[index],
            reverse=True,
        )[: settings.lexical_candidate_k]
        return [
            self._document_to_chunk(documents[index], lexical_scores[index], equipment_name)
            for index in ranked_indexes
            if lexical_scores[index] > 0
        ]

    def _lexical_index(self, equipment_name: str) -> tuple[list[Document], Any]:
        if not hasattr(self, "_lexical_cache"):
            self._lexical_cache = {}
        if equipment_name in self._lexical_cache:
            return self._lexical_cache[equipment_name]

        result = self.get_store()._collection.get(
            where={"equipment_name": equipment_name},
            include=["documents", "metadatas"],
        )
        documents = [
            Document(page_content=str(text or ""), metadata=metadata or {})
            for text, metadata in zip(result.get("documents") or [], result.get("metadatas") or [])
        ]
        tokenized_documents = [self._tokenize(document.page_content) for document in documents]
        bm25 = self._build_bm25(tokenized_documents)
        if len(self._lexical_cache) >= 2:
            self._lexical_cache.pop(next(iter(self._lexical_cache)))
        self._lexical_cache[equipment_name] = (documents, bm25)
        return documents, bm25

    def _build_bm25(self, tokenized_documents: list[list[str]]):
        try:
            from rank_bm25 import BM25Okapi

            return BM25Okapi(tokenized_documents)
        except ImportError:
            return _FallbackBM25Okapi(tokenized_documents)

    def _merge_candidates(
        self,
        semantic: list[RetrievedChunk],
        lexical: list[RetrievedChunk],
    ) -> list[tuple[RetrievedChunk, float, float]]:
        merged: dict[tuple[str, str], dict[str, Any]] = {}
        for chunk in semantic:
            key = self._chunk_key(chunk)
            merged.setdefault(key, {"chunk": chunk, "semantic": 0.0, "lexical": 0.0})
            merged[key]["semantic"] = float(chunk.score or 0.0)
        for chunk in lexical:
            key = self._chunk_key(chunk)
            merged.setdefault(key, {"chunk": chunk, "semantic": 0.0, "lexical": 0.0})
            merged[key]["lexical"] = float(chunk.score or 0.0)

        candidates = sorted(
            merged.values(),
            key=lambda item: (
                settings.semantic_weight * item["semantic"]
                + settings.lexical_weight * item["lexical"]
            ),
            reverse=True,
        )[: settings.reranker_candidate_k]
        return [(item["chunk"], item["semantic"], item["lexical"]) for item in candidates]

    def _cross_encoder_rerank(
        self,
        question: str,
        candidates: list[tuple[RetrievedChunk, float, float]],
    ) -> list[RetrievedChunk]:
        if not candidates:
            return []
        pairs = [(question, chunk.text) for chunk, _semantic, _lexical in candidates]
        raw_scores = self.reranker.predict(
            pairs,
            batch_size=settings.reranker_batch_size,
            show_progress_bar=False,
        )
        reranker_scores = self._minmax([float(score) for score in raw_scores])

        ranked = []
        for index, (chunk, semantic, lexical) in enumerate(candidates):
            final_score = (
                settings.reranker_weight * reranker_scores[index]
                + settings.semantic_weight * semantic
                + settings.lexical_weight * lexical
            )
            ranked.append(self._with_score(chunk, final_score))
        return sorted(ranked, key=lambda chunk: float(chunk.score or 0.0), reverse=True)

    def _technician_context(
        self,
        question: str,
        equipment_name: str,
        ranked: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        pages = []
        seen = set()
        for chunk in ranked:
            page = self._parent_page(chunk, equipment_name)
            if not page or self._page_key(page) in seen:
                continue
            seen.add(self._page_key(page))
            pages.append(self._truncate_page_around_match(page, chunk.text, settings.technician_context_max_chars))
            if len(pages) >= settings.technician_page_context_k:
                break
        return pages or ranked[: settings.retrieval_k]

    def _operator_context(
        self,
        question: str,
        equipment_name: str,
        ranked: list[RetrievedChunk],
        k: int | None,
    ) -> list[RetrievedChunk]:
        target_k = k or settings.operator_context_k
        selected = ranked[:target_k]
        if not selected:
            return []

        page_candidates = []
        seen_pages = set()
        for chunk in selected:
            page = self._parent_page(chunk, equipment_name)
            if page and self._page_key(page) not in seen_pages:
                seen_pages.add(self._page_key(page))
                page_candidates.extend(self._split_parent_for_operator(page))

            for adjacent in self._adjacent_parent_pages(chunk, equipment_name):
                if self._page_key(adjacent) in seen_pages:
                    continue
                seen_pages.add(self._page_key(adjacent))
                page_candidates.extend(self._split_parent_for_operator(adjacent))

        expanded = self._rerank_context_fragments(question, page_candidates)
        if not expanded:
            return selected

        best = float(expanded[0].score or 0.0)
        threshold = best * settings.adjacent_page_relative_threshold
        useful_expanded = [chunk for chunk in expanded if float(chunk.score or 0.0) >= threshold]
        return self._deduplicate_chunks((selected + useful_expanded)[: target_k + settings.operator_adjacent_pages_max])

    def _rerank_context_fragments(self, question: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        if not chunks:
            return []
        pairs = [(question, chunk.text) for chunk in chunks]
        raw_scores = self.reranker.predict(
            pairs,
            batch_size=settings.reranker_batch_size,
            show_progress_bar=False,
        )
        normalized = self._minmax([float(score) for score in raw_scores])
        return sorted(
            [self._with_score(chunk, normalized[index]) for index, chunk in enumerate(chunks)],
            key=lambda chunk: float(chunk.score or 0.0),
            reverse=True,
        )

    def _parent_page(self, chunk: RetrievedChunk, equipment_name: str) -> RetrievedChunk | None:
        result = self.get_page_store()._collection.get(
            where={
                "$and": [
                    {"equipment_name": equipment_name},
                    {"source_file": chunk.citation.source_file},
                    {"markdown_page": chunk.citation.markdown_page},
                ]
            },
            include=["documents", "metadatas"],
            limit=1,
        )
        documents = result.get("documents") or []
        metadatas = result.get("metadatas") or []
        if not documents:
            return None
        return self._document_to_chunk(
            Document(page_content=documents[0], metadata=metadatas[0] or {}),
            float(chunk.score or 0.0),
            equipment_name,
        )

    def _adjacent_parent_pages(self, chunk: RetrievedChunk, equipment_name: str) -> list[RetrievedChunk]:
        try:
            page_number = int(chunk.citation.markdown_page)
        except (TypeError, ValueError):
            return []
        pages = []
        for adjacent_page in (page_number - 1, page_number + 1):
            if adjacent_page <= 0:
                continue
            result = self.get_page_store()._collection.get(
                where={
                    "$and": [
                        {"equipment_name": equipment_name},
                        {"source_file": chunk.citation.source_file},
                        {"markdown_page": adjacent_page},
                    ]
                },
                include=["documents", "metadatas"],
                limit=1,
            )
            documents = result.get("documents") or []
            metadatas = result.get("metadatas") or []
            if documents:
                pages.append(
                    self._document_to_chunk(
                        Document(page_content=documents[0], metadata=metadatas[0] or {}),
                        0.0,
                        equipment_name,
                    )
                )
        return pages

    def _split_parent_for_operator(self, page: RetrievedChunk) -> list[RetrievedChunk]:
        text = page.text.strip()
        size = settings.operator_chunk_size
        overlap = settings.operator_chunk_overlap
        fragments = []
        start = 0
        index = 0
        while start < len(text):
            end = min(len(text), start + size)
            if end < len(text):
                boundary = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
                if boundary > start + size // 2:
                    end = boundary + 1
            fragment = text[start:end].strip()
            if fragment:
                citation = self._citation_with_chunk_id(page.citation, f"{page.citation.chunk_id}-op-{index}")
                fragments.append(RetrievedChunk(text=fragment, citation=citation, score=0.0))
            if end >= len(text):
                break
            start = max(start + 1, end - overlap)
            index += 1
        return fragments

    def _truncate_page_around_match(
        self,
        page: RetrievedChunk,
        matched_text: str,
        max_chars: int,
    ) -> RetrievedChunk:
        if len(page.text) <= max_chars:
            return page
        normalized_page = self._normalize_for_ranking(page.text)
        match_terms = [token for token in self._tokenize(matched_text) if len(token) >= 5]
        positions = [normalized_page.find(term) for term in match_terms if normalized_page.find(term) >= 0]
        center = min(positions) if positions else len(page.text) // 2
        start = max(0, center - max_chars // 2)
        end = min(len(page.text), start + max_chars)
        start = max(0, end - max_chars)
        text = page.text[start:end].strip()
        return RetrievedChunk(text=text, citation=page.citation, score=page.score)

    def _citation_with_chunk_id(self, citation: SourceCitation, chunk_id: str) -> SourceCitation:
        return SourceCitation(
            source_file=citation.source_file,
            page=citation.page,
            chunk_id=chunk_id,
            equipment_name=citation.equipment_name,
            has_images=citation.has_images,
            image_count=citation.image_count,
            url=citation.url,
            images=citation.images,
            display_source=citation.display_source,
            original_pdf=citation.original_pdf,
            pdf_page=citation.pdf_page,
            pdf_page_confidence=citation.pdf_page_confidence,
            page_mapping_method=citation.page_mapping_method,
            page_mapping_status=citation.page_mapping_status,
            markdown_page=citation.markdown_page,
        )

    def _semantic_score(self, distance: float) -> float:
        return 1.0 / (1.0 + max(0.0, distance))

    def _tokenize(self, text: str) -> list[str]:
        return [
            token
            for token in self._normalize_for_ranking(text).split()
            if len(token) >= 2
        ]

    def _minmax(self, values: list[float]) -> list[float]:
        if not values:
            return []
        minimum = min(values)
        maximum = max(values)
        if math.isclose(minimum, maximum):
            return [1.0 if maximum > 0 else 0.0 for _ in values]
        return [(value - minimum) / (maximum - minimum) for value in values]

    def _normalize_for_ranking(self, value: str | None) -> str:
        if not value:
            return ""
        without_accents = unicodedata.normalize("NFKD", value)
        ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
        compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).strip().lower()
        return re.sub(r"\s+", " ", compact)

    def _with_score(self, chunk: RetrievedChunk, score: float) -> RetrievedChunk:
        return RetrievedChunk(text=chunk.text, citation=chunk.citation, score=score)

    def _chunk_key(self, chunk: RetrievedChunk) -> tuple[str, str]:
        return chunk.citation.source_file, chunk.citation.chunk_id

    def _page_key(self, chunk: RetrievedChunk) -> tuple[str, Any]:
        return chunk.citation.source_file, chunk.citation.markdown_page

    def _deduplicate_chunks(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        unique = []
        seen = set()
        for chunk in chunks:
            key = self._chunk_key(chunk)
            if key in seen:
                continue
            seen.add(key)
            unique.append(chunk)
        return unique

    def _document_to_chunk(
        self,
        document: Document,
        score: float,
        expected_equipment: str,
    ) -> RetrievedChunk:
        metadata: dict[str, Any] = document.metadata or {}
        equipment_name = str(metadata.get("equipment_name") or metadata.get("equipo") or "").strip()
        pdf_page = metadata.get("pdf_page") or ""
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
            pdf_page_confidence=str(metadata.get("pdf_page_confidence") or ""),
            page_mapping_method=str(metadata.get("page_mapping_method") or ""),
            page_mapping_status=str(metadata.get("page_mapping_status") or ""),
            markdown_page=metadata.get("markdown_page", ""),
        )
        return RetrievedChunk(text=document.page_content, citation=citation, score=score)

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
        return tuple(
            {
                "url": str(item.get("url")),
                "page": item.get("page"),
                "label": str(item.get("label") or "Imagen"),
            }
            for item in parsed
            if isinstance(item, dict) and item.get("url")
        )


class _FallbackBM25Okapi:
    """Small BM25 fallback used only until rank-bm25 is installed."""

    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.avgdl = sum(len(document) for document in corpus) / max(1, len(corpus))
        self.document_frequencies: dict[str, int] = {}
        for document in corpus:
            for token in set(document):
                self.document_frequencies[token] = self.document_frequencies.get(token, 0) + 1

    def get_scores(self, query_tokens: list[str]) -> list[float]:
        total_documents = max(1, len(self.corpus))
        scores = []
        for document in self.corpus:
            frequencies: dict[str, int] = {}
            for token in document:
                frequencies[token] = frequencies.get(token, 0) + 1
            score = 0.0
            for token in query_tokens:
                frequency = frequencies.get(token, 0)
                if not frequency:
                    continue
                document_frequency = self.document_frequencies.get(token, 0)
                inverse_document_frequency = math.log(
                    1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5)
                )
                denominator = frequency + self.k1 * (
                    1 - self.b + self.b * len(document) / max(1.0, self.avgdl)
                )
                score += inverse_document_frequency * frequency * (self.k1 + 1) / denominator
            scores.append(score)
        return scores
