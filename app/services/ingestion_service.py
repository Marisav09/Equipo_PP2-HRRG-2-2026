from __future__ import annotations

import logging
from pathlib import Path
from uuid import uuid4

import fitz
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.equipment_catalog import (
    UNCLASSIFIED_EQUIPMENT_LABEL,
    infer_equipment_from_path,
    infer_equipment_from_text,
)
from app.core.exceptions import DocumentIngestionError
from app.services.vectorstore_service import VectorstoreService

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, vectorstore: VectorstoreService | None = None) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ingest_directory(self, directory: Path | None = None) -> dict[str, object]:
        source_dir = directory or settings.raw_documents_dir
        source_dir.mkdir(parents=True, exist_ok=True)
        pdf_files = sorted(source_dir.rglob("*.pdf"))

        if not pdf_files:
            return {
                "processed_files": 0,
                "indexed_chunks": 0,
                "errors": [],
                "message": f"No se encontraron PDFs en {source_dir}.",
            }

        indexed_chunks = 0
        errors: list[str] = []
        skipped_files: list[str] = []

        for pdf_path in pdf_files:
            try:
                documents = self._load_pdf_as_documents(pdf_path, source_dir)
                equipment = documents[0].metadata.get("equipo")
                if equipment == UNCLASSIFIED_EQUIPMENT_LABEL:
                    self.vectorstore.delete_source(pdf_path.name)
                    skipped_files.append(
                        f"{pdf_path.name}: no se pudo inferir el equipo desde la ruta, nombre o contenido."
                    )
                    continue

                chunks = self.text_splitter.split_documents(documents)
                for chunk_index, chunk in enumerate(chunks, start=1):
                    chunk.metadata["chunk_id"] = f"{pdf_path.stem}-{chunk_index}"
                    chunk.metadata["equipo"] = equipment

                self.vectorstore.delete_source(pdf_path.name)
                indexed_chunks += self.vectorstore.add_documents(chunks)
                logger.info(
                    "PDF indexado: %s | equipo=%s (%s chunks)",
                    pdf_path.name,
                    equipment,
                    len(chunks),
                )
            except DocumentIngestionError as exc:
                logger.exception("Error controlado durante la ingesta de %s", pdf_path)
                errors.append(str(exc))
            except Exception as exc:
                logger.exception("Error inesperado durante la ingesta de %s", pdf_path)
                errors.append(f"{pdf_path.name}: {exc}")

        return {
            "processed_files": len(pdf_files) - len(errors) - len(skipped_files),
            "indexed_chunks": indexed_chunks,
            "errors": errors,
            "skipped_files": skipped_files,
            "message": "Ingesta finalizada.",
        }

    def _load_pdf_as_documents(self, pdf_path: Path, source_dir: Path) -> list[Document]:
        try:
            pdf = fitz.open(pdf_path)
        except Exception as exc:
            raise DocumentIngestionError(f"No se pudo abrir el PDF {pdf_path.name}: {exc}") from exc

        documents: list[Document] = []
        equipment = infer_equipment_from_path(pdf_path, source_dir)
        detection_text: list[str] = []

        try:
            for page_index, page in enumerate(pdf, start=1):
                image_count = len(page.get_images(full=True))
                text = page.get_text("text").strip()

                if not text and image_count > 0:
                    text = self._extract_ocr_text(page, pdf_path.name, page_index)

                if not text and image_count > 0:
                    text = (
                        "Esta pagina contiene imagenes o esquemas tecnicos, pero no se pudo "
                        "extraer texto digital. Revisar visualmente la pagina indicada del PDF."
                    )

                if not text:
                    continue

                if page_index <= 3:
                    detection_text.append(text)

                if not equipment:
                    equipment = infer_equipment_from_text("\n".join(detection_text))

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "equipo": equipment or UNCLASSIFIED_EQUIPMENT_LABEL,
                            "source_file": pdf_path.name,
                            "page": page_index,
                            "document_type": "manual_tecnico",
                            "chunk_id": str(uuid4()),
                            "has_images": image_count > 0,
                            "image_count": image_count,
                        },
                    )
                )
        finally:
            pdf.close()

        if not documents:
            raise DocumentIngestionError(
                f"No se pudo extraer texto util del PDF {pdf_path.name}."
            )

        final_equipment = equipment or UNCLASSIFIED_EQUIPMENT_LABEL
        for document in documents:
            document.metadata["equipo"] = final_equipment

        return documents

    def _extract_ocr_text(self, page: fitz.Page, source_file: str, page_number: int) -> str:
        if not settings.enable_ocr:
            return ""

        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            logger.warning("OCR habilitado, pero pytesseract/Pillow no estan instalados.")
            return ""

        pixmap = page.get_pixmap(dpi=220)
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        try:
            return pytesseract.image_to_string(image, lang="spa+eng").strip()
        except Exception as exc:
            logger.warning(
                "No se pudo aplicar OCR en %s pagina %s: %s",
                source_file,
                page_number,
                exc,
            )
            return ""
