from __future__ import annotations

import hashlib
import csv
import json
import logging
import re
from pathlib import Path
from urllib.parse import quote

import fitz
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.equipment_catalog import (
    Equipment,
    infer_equipment_from_path,
    infer_equipment_from_text,
)
from app.core.exceptions import DocumentIngestionError
from app.services.ingestion_audit_service import IngestionAuditService
from app.services.vectorstore_service import VectorstoreService


logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(
        self,
        vectorstore: VectorstoreService | None = None,
        audit_service: IngestionAuditService | None = None,
    ) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.audit_service = audit_service or IngestionAuditService()

        # Mapeo Markdown -> PDF oficial.
        # page_mapping_offsets se calcula desde filas text_similarity confiables
        # para detectar y rechazar falsos positivos de visual_similarity en documentos largos.
        self.page_mapping_offsets: dict[str, int] = {}
        self.page_mapping_index = self._page_mapping_index()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest_directory(self, directory: Path | None = None, force: bool = False) -> dict[str, object]:
        source_dir = directory or settings.processed_documents_dir
        source_dir.mkdir(parents=True, exist_ok=True)
        all_markdown_files = sorted(path for path in source_dir.rglob("*.md") if path.is_file())
        markdown_files = all_markdown_files

        curation_index = self._curation_index()
        excluded_by_curation = []
        if curation_index:
            included_names = set(curation_index)
            excluded_by_curation = [
                path for path in all_markdown_files
                if path.name not in included_names
            ]
            markdown_files = [
                path for path in all_markdown_files
                if path.name in included_names
            ]

            for excluded_path in excluded_by_curation:
                self.audit_service.record(
                    source_file=excluded_path.name,
                    file_hash=self._hash_file(excluded_path),
                    status="excluded",
                    message="Excluido del corpus activo por curaduria_activa.csv.",
                )

        if not markdown_files:
            return {
                "processed_files": 0,
                "indexed_chunks": 0,
                "skipped_files": [],
                "errors": [],
                "message": f"No se encontraron Markdown en {source_dir}.",
            }

        processed_files = 0
        indexed_chunks = 0
        stale_sources_removed = 0
        unchanged_files: list[str] = []
        skipped_files: list[str] = []
        errors: list[str] = []

        if hasattr(self.vectorstore, "delete_sources_except"):
            stale_sources_removed = self.vectorstore.delete_sources_except(
                {path.name for path in markdown_files}
            )

        for markdown_path in markdown_files:
            file_hash = self._hash_file(markdown_path)
            try:
                latest = self.audit_service.get_latest_by_source(markdown_path.name)
                if (
                    not force
                    and latest
                    and latest["file_hash"] == file_hash
                    and latest["status"] == "indexed"
                ):
                    unchanged_files.append(markdown_path.name)
                    self.audit_service.record(
                        source_file=markdown_path.name,
                        file_hash=file_hash,
                        status="unchanged",
                        equipment_id=latest["equipment_id"],
                        equipment_name=latest["equipment_name"],
                        page_count=int(latest["page_count"]),
                        chunk_count=int(latest["chunk_count"]),
                        image_count=int(latest["image_count"]),
                        message="Markdown sin cambios; se omite reindexado.",
                    )
                    continue

                documents = self._load_markdown_as_documents(markdown_path, source_dir)
                if not documents:
                    skipped_files.append(f"{markdown_path.name}: sin texto util para indexar.")
                    self.audit_service.record(
                        source_file=markdown_path.name,
                        file_hash=file_hash,
                        status="skipped",
                        message="Sin texto util para indexar.",
                    )
                    continue

                added_chunks, generated_chunks = self._index_documents_with_safe_retry(
                    markdown_path=markdown_path,
                    documents=documents,
                )

                indexed_chunks += added_chunks
                processed_files += 1
                first_metadata = documents[0].metadata
                self.audit_service.record(
                    source_file=markdown_path.name,
                    file_hash=file_hash,
                    status="indexed",
                    equipment_id=str(first_metadata["equipment_id"]),
                    equipment_name=str(first_metadata["equipment_name"]),
                    page_count=len(documents),
                    chunk_count=generated_chunks,
                    image_count=sum(int(document.metadata.get("image_count", 0)) for document in documents),
                    message="Markdown indexado correctamente.",
                )
                logger.info("Markdown indexado: %s (%s chunks)", markdown_path.name, generated_chunks)
            except DocumentIngestionError as exc:
                skipped_files.append(str(exc))
                self.audit_service.record(
                    source_file=markdown_path.name,
                    file_hash=file_hash,
                    status="skipped",
                    message=str(exc),
                )
            except Exception as exc:
                logger.exception("Error inesperado al ingerir %s", markdown_path)
                errors.append(f"{markdown_path.name}: {exc}")
                self.audit_service.record(
                    source_file=markdown_path.name,
                    file_hash=file_hash,
                    status="error",
                    message=str(exc),
                )

        return {
            "processed_files": processed_files,
            "indexed_chunks": indexed_chunks,
            "unchanged_files": unchanged_files,
            "skipped_files": skipped_files,
            "errors": errors,
            "stale_sources_removed": stale_sources_removed,
            "message": "Ingesta finalizada.",
            "audit": self.audit_service.list_latest(),
        }

    def _index_documents_with_safe_retry(
        self,
        markdown_path: Path,
        documents: list[Document],
    ) -> tuple[int, int]:
        """
        Indexa documentos con reintento seguro.

        Motivo:
        Algunos Markdown curados/OCR pueden producir chunks que, aunque no sean
        enormes en caracteres, exceden el contexto del modelo de embeddings por
        tokenizacion o contenido tecnico denso. En ese caso se reintenta con:
        - batches mas chicos;
        - chunks mas chicos;
        - limpieza previa de la fuente en Chroma para no dejar indexacion parcial.
        """
        attempts = self._split_attempts()
        last_exception: Exception | None = None

        for chunk_size, chunk_overlap, batch_size, label in attempts:
            chunks = self._split_documents_for_attempt(
                documents=documents,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            self._assign_chunk_ids(markdown_path, chunks)

            if not chunks:
                raise DocumentIngestionError(f"{markdown_path.name}: no se generaron chunks para indexar.")

            try:
                self.vectorstore.delete_source(markdown_path.name)
                added_chunks = self._add_documents_in_batches(chunks, batch_size=batch_size)

                if label != "default":
                    logger.warning(
                        "Markdown indexado con modo seguro: %s (%s chunks, %s)",
                        markdown_path.name,
                        len(chunks),
                        label,
                    )

                return added_chunks, len(chunks)

            except Exception as exc:
                last_exception = exc
                self.vectorstore.delete_source(markdown_path.name)

                if not self._is_context_length_error(exc):
                    raise

                logger.warning(
                    "Reintentando ingesta segura para %s por limite de contexto "
                    "(modo %s, chunk_size=%s, batch_size=%s): %s",
                    markdown_path.name,
                    label,
                    chunk_size,
                    batch_size,
                    exc,
                )

        if last_exception:
            raise last_exception

        raise DocumentIngestionError(f"{markdown_path.name}: no se pudo completar la ingesta segura.")

    def _split_attempts(self) -> list[tuple[int, int, int, str]]:
        default_chunk_size = int(settings.chunk_size)
        default_chunk_overlap = int(settings.chunk_overlap)

        raw_attempts = [
            (default_chunk_size, default_chunk_overlap, 16, "default"),
            (default_chunk_size, default_chunk_overlap, 1, "default_batch_1"),
            (500, min(default_chunk_overlap, 80), 1, "safe_500"),
            (250, min(default_chunk_overlap, 40), 1, "safe_250"),
            (120, min(default_chunk_overlap, 20), 1, "safe_120"),
        ]

        attempts: list[tuple[int, int, int, str]] = []
        seen: set[tuple[int, int, int]] = set()

        for chunk_size, chunk_overlap, batch_size, label in raw_attempts:
            chunk_size = max(80, int(chunk_size))
            chunk_overlap = max(0, min(int(chunk_overlap), chunk_size // 3))
            batch_size = max(1, int(batch_size))

            key = (chunk_size, chunk_overlap, batch_size)
            if key in seen:
                continue

            seen.add(key)
            attempts.append((chunk_size, chunk_overlap, batch_size, label))

        return attempts

    def _split_documents_for_attempt(
        self,
        documents: list[Document],
        chunk_size: int,
        chunk_overlap: int,
    ) -> list[Document]:
        if chunk_size == int(settings.chunk_size) and chunk_overlap == int(settings.chunk_overlap):
            return self.text_splitter.split_documents(documents)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return splitter.split_documents(documents)

    def _assign_chunk_ids(self, markdown_path: Path, chunks: list[Document]) -> None:
        for index, chunk in enumerate(chunks, start=1):
            chunk.metadata["chunk_id"] = f"{markdown_path.stem}-{index}"

    def _add_documents_in_batches(self, chunks: list[Document], batch_size: int) -> int:
        added_chunks = 0

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            added_chunks += self.vectorstore.add_documents(batch)

        return added_chunks

    def _is_context_length_error(self, exc: Exception) -> bool:
        message = str(exc).lower()
        return (
            "input length exceeds the context length" in message
            or "context length" in message
            or "too many tokens" in message
            or "maximum context" in message
        )

    def _curation_index(self) -> dict[str, dict[str, str]]:
        """Lee data/inventory/curaduria_activa.csv y devuelve solo fuentes incluidas."""
        curation_path = settings.processed_documents_dir.parent / "inventory" / "curaduria_activa.csv"

        if not curation_path.exists():
            return {}

        included: dict[str, dict[str, str]] = {}

        with curation_path.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                source_file = (row.get("source_file") or "").strip()
                decision = (row.get("decision_curaduria") or "").strip().lower()
                estado = (row.get("estado_producto") or "").strip().lower()

                if not source_file:
                    continue

                if decision == "incluir" and estado in {"validado", "activo", "aprobado"}:
                    included[source_file] = row

        return included

    def _load_markdown_as_documents(self, markdown_path: Path, source_dir: Path) -> list[Document]:
        text = markdown_path.read_text(encoding="utf-8", errors="replace")
        equipment = infer_equipment_from_path(markdown_path, source_dir) or infer_equipment_from_text(text)
        if not equipment:
            raise DocumentIngestionError(
                f"{markdown_path.name}: omitido porque no se pudo inferir un equipo del catalogo."
            )

        pages = self._split_markdown_pages(text)
        if not pages:
            pages = [(1, text)]

        documents: list[Document] = []
        for page_number, page_text in pages:
            clean_text = self._strip_markdown_image_noise(page_text).strip()
            image_refs = self._extract_image_refs(page_text, page_number)
            source_reference = self._source_reference_for_markdown(markdown_path, page_number)

            if not clean_text and not image_refs:
                continue
            if not clean_text:
                clean_text = "Pagina con imagenes o esquemas tecnicos sin texto digital extraible."

            documents.append(
                Document(
                    page_content=clean_text,
                    metadata={
                        "equipment_id": equipment.id,
                        "equipment_name": equipment.name,

                        # Fuente interna del RAG: Markdown procesado.
                        "source_file": markdown_path.name,
                        "markdown_page": page_number,

                        # Fuente visible para usuario final: PDF/manual original.
                        "original_pdf": source_reference["original_pdf"],
                        "display_source": source_reference["display_source"],
                        "pdf_page": source_reference["pdf_page"],
                        "pdf_page_confidence": source_reference["pdf_page_confidence"],
                        "page_mapping_method": source_reference["page_mapping_method"],
                        "page_mapping_status": source_reference["page_mapping_status"],

                        # Campo legado: se conserva para compatibilidad.
                        # Solo contiene pagina PDF cuando el mapeo esta verificado.
                        "page": source_reference["pdf_page"] or "sin_pagina",

                        "document_type": "manual_markdown",
                        "has_images": bool(image_refs),
                        "image_count": len(image_refs),
                        "image_refs": json.dumps(image_refs, ensure_ascii=False),
                        "source_url": source_reference["source_url"],
                    },
                )
            )

        if not documents:
            raise DocumentIngestionError(f"{markdown_path.name}: no se pudo extraer texto util.")
        return documents

    def _split_markdown_pages(self, text: str) -> list[tuple[int, str]]:
        matches = list(re.finditer(r"(?im)^#{1,6}\s*P(?:a|ÃƒÂ¡|Ã¡|á)gina\s+(\d+)\s*$", text))
        if not matches:
            return []

        pages: list[tuple[int, str]] = []
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            pages.append((int(match.group(1)), text[start:end]))
        return pages

    def _extract_image_refs(self, text: str, page_number: int) -> list[dict[str, object]]:
        refs: list[dict[str, object]] = []
        seen: set[str] = set()
        for match in re.finditer(r"!\[(?P<label>[^\]]*)\]\((?P<path>[^)]+)\)|imagen:\s*(?P<meta>\S+)", text):
            raw_path = match.group("path") or match.group("meta")
            if not raw_path or raw_path in seen:
                continue
            seen.add(raw_path)
            image_url = self._image_url(raw_path)
            if not image_url:
                continue
            refs.append(
                {
                    "url": image_url,
                    "page": page_number,
                    "label": match.group("label") or f"Imagen pagina {page_number}",
                }
            )
        return refs

    def _image_url(self, raw_path: str) -> str | None:
        normalized = raw_path.strip().replace("\\", "/").replace("data/images/", "data/imagenes/")
        marker = "data/imagenes/"
        if marker not in normalized:
            return None
        relative = normalized.split(marker, 1)[1]
        return f"/images/{relative}"

    def _strip_markdown_image_noise(self, text: str) -> str:
        text = re.sub(r"```metadata.*?```", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
        return text

    def _source_reference_for_markdown(self, markdown_path: Path, markdown_page: int) -> dict[str, object]:
        original_pdf = self._original_pdf_for_markdown(markdown_path)
        mapping = self.page_mapping_index.get((markdown_path.name, markdown_page), {})
        resolved_mapping = self._resolve_page_mapping(mapping)

        mapped_pdf_page = resolved_mapping["pdf_page"]
        page_confidence = str(resolved_mapping["pdf_page_confidence"])
        mapping_method = str(resolved_mapping["page_mapping_method"])
        mapping_status = str(resolved_mapping["page_mapping_status"])

        if original_pdf:
            display_source = Path(original_pdf.replace("\\", "/")).name
            source_url = f"/manuals/{quote(original_pdf)}"
            if mapped_pdf_page:
                source_url = f"{source_url}#page={mapped_pdf_page}"

            return {
                "original_pdf": original_pdf,
                "display_source": display_source,
                "markdown_page": markdown_page,
                "pdf_page": mapped_pdf_page or "",
                "pdf_page_confidence": page_confidence,
                "page_mapping_method": mapping_method,
                "page_mapping_status": mapping_status,
                "source_url": source_url,
            }

        return {
            "original_pdf": "",
            "display_source": markdown_path.name,
            "markdown_page": markdown_page,
            "pdf_page": "",
            "pdf_page_confidence": "unmapped",
            "page_mapping_method": "unmapped",
            "page_mapping_status": "missing_original_pdf",
            "source_url": f"/processed/{markdown_path.name}#page-{markdown_page}",
        }

    def _page_mapping_index(self) -> dict[tuple[str, int], dict[str, str]]:
        """Carga el mapeo Markdown -> pagina PDF oficial.

        Reglas de confianza:
        - Se lee con utf-8-sig porque el CSV puede traer BOM en la primera columna.
        - text_similarity verified se considera confiable.
        - visual_similarity verified NO se acepta automaticamente: en manuales largos
          puede dar falsos positivos por esquemas repetidos.
        - Para visual_similarity, se acepta si respeta el offset dominante calculado
          desde filas text_similarity verified del mismo documento.
        """
        mapping_path = settings.processed_documents_dir.parent / "inventory" / "page_mapping_markdown_to_official.csv"

        if not mapping_path.exists():
            self.page_mapping_offsets = {}
            return {}

        index: dict[tuple[str, int], dict[str, str]] = {}
        rows: list[dict[str, str]] = []

        with mapping_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
            for row in csv.DictReader(file):
                source_file = (row.get("source_file") or "").strip()
                markdown_page = self._safe_int(row.get("markdown_page"))

                if not source_file or markdown_page is None:
                    continue

                rows.append(row)
                index[(source_file, markdown_page)] = row

        self.page_mapping_offsets = self._dominant_page_offsets(rows)
        return index

    def _dominant_page_offsets(self, rows: list[dict[str, str]]) -> dict[str, int]:
        offsets_by_source: dict[str, dict[int, int]] = {}

        for row in rows:
            if not self._is_text_verified_mapping(row):
                continue

            source_file = (row.get("source_file") or "").strip()
            markdown_page = self._safe_int(row.get("markdown_page"))
            official_pdf_page = self._safe_int(row.get("official_pdf_page"))

            if not source_file or markdown_page is None or official_pdf_page is None:
                continue

            offset = official_pdf_page - markdown_page
            offsets_by_source.setdefault(source_file, {})
            offsets_by_source[source_file][offset] = offsets_by_source[source_file].get(offset, 0) + 1

        dominant_offsets: dict[str, int] = {}
        for source_file, counts in offsets_by_source.items():
            if not counts:
                continue

            offset, count = max(counts.items(), key=lambda item: item[1])

            # Se exige al menos dos coincidencias textuales para usar el offset
            # como correccion de mapeos visuales dudosos.
            if count >= 2:
                dominant_offsets[source_file] = offset

        return dominant_offsets

    def _resolve_page_mapping(self, mapping: dict[str, str]) -> dict[str, object]:
        if not mapping:
            return {
                "pdf_page": "",
                "pdf_page_confidence": "unmapped",
                "page_mapping_method": "unmapped",
                "page_mapping_status": "unmapped",
            }

        raw_confidence = (mapping.get("page_confidence") or "unmapped").strip()
        raw_method = (mapping.get("mapping_method") or "unmapped").strip()
        raw_status = (mapping.get("status") or "unmapped").strip()

        confidence = raw_confidence.lower()
        method = raw_method.lower()
        status = raw_status.lower()
        official_pdf_page = self._safe_int(mapping.get("official_pdf_page"))

        if confidence != "verified" or official_pdf_page is None:
            return {
                "pdf_page": "",
                "pdf_page_confidence": raw_confidence,
                "page_mapping_method": raw_method,
                "page_mapping_status": raw_status,
            }

        if self._is_text_verified_mapping(mapping):
            return {
                "pdf_page": official_pdf_page,
                "pdf_page_confidence": "verified",
                "page_mapping_method": raw_method,
                "page_mapping_status": raw_status,
            }

        if "visual" in method:
            visual_resolution = self._resolve_visual_mapping(mapping, official_pdf_page)
            if visual_resolution is not None:
                return visual_resolution

            return {
                "pdf_page": "",
                "pdf_page_confidence": "unreliable_visual",
                "page_mapping_method": raw_method,
                "page_mapping_status": f"{raw_status}_rejected_by_consistency_rule",
            }

        # Otros metodos verificados se aceptan solo si no son visuales.
        if "visual" not in method and "visual" not in status:
            return {
                "pdf_page": official_pdf_page,
                "pdf_page_confidence": "verified",
                "page_mapping_method": raw_method,
                "page_mapping_status": raw_status,
            }

        return {
            "pdf_page": "",
            "pdf_page_confidence": "unreliable_mapping",
            "page_mapping_method": raw_method,
            "page_mapping_status": f"{raw_status}_rejected_unknown_mapping",
        }

    def _is_text_verified_mapping(self, mapping: dict[str, str]) -> bool:
        confidence = (mapping.get("page_confidence") or "").strip().lower()
        method = (mapping.get("mapping_method") or "").strip().lower()
        status = (mapping.get("status") or "").strip().lower()
        official_pdf_page = self._safe_int(mapping.get("official_pdf_page"))

        return (
            confidence == "verified"
            and official_pdf_page is not None
            and ("text" in method or status == "text_matched")
        )

    def _resolve_visual_mapping(
        self,
        mapping: dict[str, str],
        official_pdf_page: int,
    ) -> dict[str, object] | None:
        source_file = (mapping.get("source_file") or "").strip()
        markdown_page = self._safe_int(mapping.get("markdown_page"))
        raw_method = (mapping.get("mapping_method") or "visual_similarity").strip()
        raw_status = (mapping.get("status") or "visual_matched").strip()

        if not source_file or markdown_page is None:
            return None

        dominant_offset = self.page_mapping_offsets.get(source_file)
        if dominant_offset is None:
            return None

        expected_pdf_page = markdown_page + dominant_offset
        if expected_pdf_page <= 0:
            return None

        if abs(official_pdf_page - expected_pdf_page) <= 1:
            return {
                "pdf_page": official_pdf_page,
                "pdf_page_confidence": "verified",
                "page_mapping_method": raw_method,
                "page_mapping_status": raw_status,
            }

        # Si el mapeo visual es inconsistente con el offset textual dominante,
        # NO se corrige automaticamente. Se descarta como pagina visible para
        # evitar abrir paginas equivocadas. La trazabilidad interna conserva
        # metodo y estado con marca de rechazo.
        logger.debug(
            "Rechazando mapeo visual inconsistente: %s markdown_page=%s "
            "official_pdf_page=%s expected_pdf_page=%s offset=%s",
            source_file,
            markdown_page,
            official_pdf_page,
            expected_pdf_page,
            dominant_offset,
        )

        return None

    def _verified_pdf_page_from_mapping(self, mapping: dict[str, str]) -> int | None:
        resolved = self._resolve_page_mapping(mapping)
        return self._safe_int(resolved.get("pdf_page"))

    def _safe_int(self, value: object) -> int | None:
        try:
            if value in (None, ""):
                return None
            number = int(str(value))
        except (TypeError, ValueError):
            return None

        return number if number > 0 else None

    def _original_pdf_for_markdown(self, markdown_path: Path) -> str | None:
        override = self._original_pdf_from_overrides(markdown_path.name)
        if override:
            return override

        direct_match = self._original_pdf_from_raw(markdown_path)
        if direct_match:
            return direct_match

        manifest_match = self._original_pdf_from_manifest(markdown_path)
        if manifest_match:
            return manifest_match

        return None

    def _original_pdf_from_overrides(self, source_file: str) -> str | None:
        overrides_path = settings.processed_documents_dir.parent / "inventory" / "pdf_source_overrides.csv"
        if not overrides_path.exists():
            return None

        with overrides_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
            for row in csv.DictReader(file):
                if (row.get("source_file") or "").strip() == source_file:
                    original_pdf = (row.get("original_pdf") or "").strip()
                    if original_pdf:
                        return original_pdf.replace("\\", "/")

        return None

    def _original_pdf_from_raw(self, markdown_path: Path) -> str | None:
        expected_pdf_name = f"{markdown_path.stem}.pdf"
        raw_dir = settings.raw_documents_dir

        if not raw_dir.exists():
            return None

        for pdf_path in raw_dir.rglob("*.pdf"):
            if pdf_path.name == expected_pdf_name:
                return pdf_path.relative_to(raw_dir).as_posix()

        return None

    def _original_pdf_from_manifest(self, markdown_path: Path) -> str | None:
        manifest_path = settings.processed_documents_dir / "pdf_name_manifest.csv"
        normalized_name = f"{markdown_path.stem}.pdf"

        if not manifest_path.exists():
            return None

        with manifest_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
            for row in csv.DictReader(file):
                if (row.get("normalized_file") or "").strip() == normalized_name:
                    original_pdf = (row.get("source_relative_path") or "").strip()
                    if original_pdf:
                        return original_pdf.replace("\\", "/")

        return None

    def _load_pdf_as_documents(self, pdf_path: Path, source_dir: Path) -> list[Document]:
        try:
            pdf = fitz.open(pdf_path)
        except Exception as exc:
            raise DocumentIngestionError(f"{pdf_path.name}: no se pudo abrir el PDF ({exc}).") from exc

        equipment = infer_equipment_from_path(pdf_path, source_dir)
        pages: list[dict[str, object]] = []
        detection_text: list[str] = []

        try:
            for page_number, page in enumerate(pdf, start=1):
                image_count = len(page.get_images(full=True))
                text = page.get_text("text").strip()

                if not text and image_count > 0:
                    text = self._extract_ocr_text(page, pdf_path.name, page_number)

                if not text and image_count > 0:
                    text = (
                        "Pagina con imagenes o esquemas tecnicos sin texto digital extraible. "
                        "Revisar visualmente el PDF original."
                    )

                if not text:
                    continue

                if page_number <= 3:
                    detection_text.append(text)

                if not equipment:
                    equipment = infer_equipment_from_text("\n".join(detection_text))

                pages.append(
                    {
                        "text": text,
                        "page": page_number,
                        "has_images": image_count > 0,
                        "image_count": image_count,
                    }
                )
        finally:
            pdf.close()

        if not pages:
            raise DocumentIngestionError(f"{pdf_path.name}: no se pudo extraer texto util.")

        if not equipment:
            raise DocumentIngestionError(
                f"{pdf_path.name}: omitido porque no se pudo inferir un equipo del catalogo."
            )

        return [self._page_to_document(pdf_path, equipment, page) for page in pages]

    def _page_to_document(
        self,
        pdf_path: Path,
        equipment: Equipment,
        page: dict[str, object],
    ) -> Document:
        pdf_page = int(page["page"])
        return Document(
            page_content=str(page["text"]),
            metadata={
                "equipment_id": equipment.id,
                "equipment_name": equipment.name,
                "source_file": pdf_path.name,
                "original_pdf": pdf_path.name,
                "display_source": pdf_path.name,
                "markdown_page": pdf_page,
                "pdf_page": pdf_page,
                "pdf_page_confidence": "verified",
                "page_mapping_method": "direct_pdf_page",
                "page_mapping_status": "direct_pdf_ingestion",
                "page": pdf_page,
                "document_type": "manual_tecnico",
                "has_images": bool(page["has_images"]),
                "image_count": int(page["image_count"]),
                "source_url": f"/manuals/{quote(pdf_path.name)}#page={pdf_page}",
            },
        )

    def _extract_ocr_text(self, page: fitz.Page, source_file: str, page_number: int) -> str:
        if not settings.enable_ocr:
            return ""

        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            logger.warning("OCR habilitado, pero pytesseract/Pillow no estan disponibles.")
            return ""

        try:
            pixmap = page.get_pixmap(dpi=220)
            image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            return pytesseract.image_to_string(image, lang="spa+eng").strip()
        except Exception as exc:
            logger.warning("OCR fallido en %s pagina %s: %s", source_file, page_number, exc)
            return ""

    def _hash_file(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for block in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()