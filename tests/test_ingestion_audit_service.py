from __future__ import annotations

from app.services.ingestion_audit_service import IngestionAuditService


def test_audit_records_latest_status(tmp_path):
    audit = IngestionAuditService(tmp_path / "audit.sqlite3")
    audit.record(
        source_file="manual.pdf",
        file_hash="hash-1",
        status="indexed",
        equipment_id="sterrad-100",
        equipment_name="Esterilizadora Sterrad 100",
        page_count=10,
        chunk_count=20,
        image_count=3,
        message="ok",
    )
    audit.record(
        source_file="manual.pdf",
        file_hash="hash-1",
        status="unchanged",
        equipment_id="sterrad-100",
        equipment_name="Esterilizadora Sterrad 100",
        page_count=10,
        chunk_count=20,
        image_count=3,
        message="sin cambios",
    )

    latest = audit.get_latest_by_source("manual.pdf")
    manifest = audit.list_latest()

    assert latest is not None
    assert latest["status"] == "unchanged"
    assert len(manifest) == 1
    assert manifest[0]["chunk_count"] == 20
