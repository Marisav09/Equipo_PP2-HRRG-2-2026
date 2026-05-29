from __future__ import annotations

from flask import Blueprint, jsonify

from app.services.ingestion_service import IngestionService
from app.services.vectorstore_service import VectorstoreService


ingest_bp = Blueprint("ingest", __name__)
ingestion_service = IngestionService()
vectorstore_service = VectorstoreService()


@ingest_bp.post("/")
def ingest_documents():
    result = ingestion_service.ingest_directory()
    status_code = 207 if result["errors"] else 200
    return jsonify(result), status_code


@ingest_bp.get("/audit")
def ingestion_audit():
    return jsonify({"documents": vectorstore_service.list_indexed_sources()})