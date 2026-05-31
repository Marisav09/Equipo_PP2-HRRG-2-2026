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
        self.page_mapping_index = self._page_mapping_index()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest_directory(self, directory: Path | None = None, force: bool = False) -> dict[str, object]:
        source_dir = directory or settings.processed_documents_dir
        source_dir.mkdir(parents=True, exist_ok=True)
        markdown_files = sorted(path for path in source_dir.rglob("*.md") if path.is_file())

        curation_index = self._curation_index()
        if curation_index:
            markdown_files = [
                path for path in markdown_files
                if path.name in curation_index
            ]

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

                chunks = self.text_splitter.split_documents(documents)
                for index, chunk in enumerate(chunks, start=1):
                    chunk.metadata["chunk_id"] = f"{markdown_path.stem}-{index}"

                self.vectorstore.delete_source(markdown_path.name)
                indexed_chunks += self.vectorstore.add_documents(chunks)
                processed_files += 1
                first_metadata = documents[0].metadata
                self.audit_service.record(
                    source_file=markdown_path.name,
                    file_hash=file_hash,
                    status="indexed",
                    equipment_id=str(first_metadata["equipment_id"]),
                    equipment_name=str(first_metadata["equipment_name"]),
                    page_count=len(documents),
                    chunk_count=len(chunks),
                    image_count=sum(int(document.metadata.get("image_count", 0)) for document in documents),
                    message="Markdown indexado correctamente.",
                )
                logger.info("Markdown indexado: %s (%s chunks)", markdown_path.name, len(chunks))
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
        matches = list(re.finditer(r"(?im)^#\s*P(?:a|ÃƒÂ¡|Ã¡|á)gina\s+(\d+)\s*$", text))
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

        mapped_pdf_page = self._verified_pdf_page_from_mapping(mapping)
        page_confidence = (mapping.get("page_confidence") or "unmapped").strip()
        mapping_method = (mapping.get("mapping_method") or "unmapped").strip()
        mapping_status = (mapping.get("status") or "unmapped").strip()

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

        Solo las filas verified deben usarse para exponer/citar pagina PDF.
        Las filas approximate/unresolved quedan como trazabilidad interna, pero no
        habilitan enlaces con #page.
        """
        mapping_path = settings.processed_documents_dir.parent / "inventory" / "page_mapping_markdown_to_official.csv"

        if not mapping_path.exists():
            return {}

        index: dict[tuple[str, int], dict[str, str]] = {}

        with mapping_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
            for row in csv.DictReader(file):
                source_file = (row.get("source_file") or "").strip()
                markdown_page = self._safe_int(row.get("markdown_page"))

                if not source_file or markdown_page is None:
                    continue

                index[(source_file, markdown_page)] = row

        return index

    def _verified_pdf_page_from_mapping(self, mapping: dict[str, str]) -> int | None:
        if not mapping:
            return None

        confidence = (mapping.get("page_confidence") or "").strip().lower()
        if confidence != "verified":
            return None

        return self._safe_int(mapping.get("official_pdf_page"))

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