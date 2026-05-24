from __future__ import annotations

from pathlib import Path

import pytest
from langchain_core.documents import Document

from app.core.equipment_catalog import infer_equipment_from_path, infer_equipment_from_text
from app.core.exceptions import DocumentIngestionError
from app.services.ingestion_audit_service import IngestionAuditService
from app.services.ingestion_service import IngestionService


def test_infer_equipment_from_pdf_name():
    equipment = infer_equipment_from_path(
        Path("Manual de Servicio Esterilizadora Sterrad 100.pdf"),
        Path("."),
    )

    assert equipment is not None
    assert equipment.id == "sterrad-100"


def test_infer_equipment_from_text_alias():
    equipment = infer_equipment_from_text("Troubleshooting HD-67 para equipos rodantes MAC GMM")

    assert equipment is not None
    assert equipment.id == "rodantes-mac-gmm"


def test_load_pdf_rejects_unknown_file(tmp_path):
    pdf_path = tmp_path / "manual_desconocido.pdf"
    pdf_path.write_text("no es un pdf real", encoding="utf-8")
    service = IngestionService(vectorstore=None)

    with pytest.raises(DocumentIngestionError):
        service._load_pdf_as_documents(pdf_path, tmp_path)


class FakeVectorstore:
    def __init__(self) -> None:
        self.add_calls = 0

    def delete_source(self, source_file: str) -> None:
        return None

    def add_documents(self, documents: list[Document]) -> int:
        self.add_calls += 1
        return len(documents)


class FakeIngestionService(IngestionService):
    def _load_markdown_as_documents(self, markdown_path: Path, source_dir: Path):
        return [
            Document(
                page_content="manual tecnico sterrad con texto suficiente",
                metadata={
                    "equipment_id": "sterrad-100",
                    "equipment_name": "Esterilizadora Sterrad 100",
                    "source_file": markdown_path.name,
                    "page": 1,
                    "document_type": "manual_markdown",
                    "has_images": False,
                    "image_count": 0,
                },
            )
        ]


def test_ingestion_skips_unchanged_markdown_after_first_index(tmp_path):
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    markdown_path = processed_dir / "Manual de Servicio Esterilizadora Sterrad 100.md"
    markdown_path.write_text("# Pagina 1\nmanual tecnico sterrad", encoding="utf-8")
    vectorstore = FakeVectorstore()
    audit = IngestionAuditService(tmp_path / "audit.sqlite3")
    service = FakeIngestionService(vectorstore=vectorstore, audit_service=audit)

    first = service.ingest_directory(processed_dir)
    second = service.ingest_directory(processed_dir)

    assert first["processed_files"] == 1
    assert second["processed_files"] == 0
    assert second["unchanged_files"] == [markdown_path.name]
    assert vectorstore.add_calls == 1
