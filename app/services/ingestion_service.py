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
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest_directory(self, directory: Path | None = None, force: bool = False) -> dict[str, object]:
        source_dir = directory or settings.processed_documents_dir
        source_dir.mkdir(parents=True, exist_ok=True)
        markdown_files = sorted(path for path in source_dir.rglob("*.md") if path.is_file())

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

        source_url_by_page = self._document_source_urls(markdown_path)
        documents: list[Document] = []
        for page_number, page_text in pages:
            clean_text = self._strip_markdown_image_noise(page_text).strip()
            image_refs = self._extract_image_refs(page_text, page_number)
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
                        "source_file": markdown_path.name,
                        "page": page_number,
                        "document_type": "manual_markdown",
                        "has_images": bool(image_refs),
                        "image_count": len(image_refs),
                        "image_refs": json.dumps(image_refs, ensure_ascii=False),
                        "source_url": source_url_by_page(page_number),
                    },
                )
            )

        if not documents:
            raise DocumentIngestionError(f"{markdown_path.name}: no se pudo extraer texto util.")
        return documents

    def _split_markdown_pages(self, text: str) -> list[tuple[int, str]]:
        matches = list(re.finditer(r"(?im)^#\s*P(?:a|Ã¡|á)gina\s+(\d+)\s*$", text))
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

    def _document_source_urls(self, markdown_path: Path):
        original_pdf = self._original_pdf_for_markdown(markdown_path)

        def build(page_number: int) -> str:
            if original_pdf:
                return f"/manuals/{quote(original_pdf)}#page={page_number}"
            return f"/processed/{markdown_path.name}#page-{page_number}"

        return build

    def _original_pdf_for_markdown(self, markdown_path: Path) -> str | None:
        manifest_path = settings.processed_documents_dir / "pdf_name_manifest.csv"
        normalized_name = f"{markdown_path.stem}.pdf"
        if not manifest_path.exists():
            return None
        with manifest_path.open("r", encoding="utf-8", errors="replace", newline="") as file:
            for row in csv.DictReader(file):
                if row.get("normalized_file") == normalized_name:
                    return str(row.get("source_relative_path") or "").replace("\\", "/")
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
        return Document(
            page_content=str(page["text"]),
            metadata={
                "equipment_id": equipment.id,
                "equipment_name": equipment.name,
                "source_file": pdf_path.name,
                "page": int(page["page"]),
                "document_type": "manual_tecnico",
                "has_images": bool(page["has_images"]),
                "image_count": int(page["image_count"]),
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
