from __future__ import annotations

from flask import Blueprint, jsonify

from app.services.ingestion_audit_service import IngestionAuditService
from app.services.ingestion_service import IngestionService


ingest_bp = Blueprint("ingest", __name__)
ingestion_service = IngestionService()
audit_service = IngestionAuditService()


@ingest_bp.post("/")
def ingest_documents():
    result = ingestion_service.ingest_directory()
    status_code = 207 if result["errors"] else 200
    return jsonify(result), status_code


@ingest_bp.get("/audit")
def ingestion_audit():
    return jsonify({"documents": audit_service.list_latest()})
