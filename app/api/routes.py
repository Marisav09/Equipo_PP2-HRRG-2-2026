from __future__ import annotations

import logging
from uuid import uuid4

from flask import Blueprint, jsonify, make_response, render_template, request, send_from_directory

from app.core.config import settings
from app.core.equipment_catalog import canonical_equipment_label
from app.services.ingestion_service import IngestionService
from app.services.memory_service import MemoryService
from app.services.rag_service import RagService

logger = logging.getLogger(__name__)
api = Blueprint("api", __name__)

rag_service = RagService()
ingestion_service = IngestionService()
memory_service = MemoryService()
cancelled_requests: set[str] = set()


@api.get("/")
def index():
    equipments = rag_service.vectorstore.list_equipments()
    return render_template(
        "index.html",
        equipments=equipments,
        active_equipment=equipments[0] if equipments else "Sin equipo seleccionado",
    )


@api.post("/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    query = str(payload.get("query", "")).strip()
    equipment = canonical_equipment_label(str(payload.get("equipment", "")).strip()) or None
    force_fallback = bool(payload.get("force_fallback", False))
    request_id = str(payload.get("request_id", "")).strip()
    raw_role = str(payload.get("user_role", "tecnico")).strip().lower()
    user_role = "operador" if raw_role == "operador" else "tecnico"

    session_id = request.cookies.get("hrrg_session_id") or str(uuid4())

    if not query:
        return jsonify({"error": "La consulta no puede estar vacía."}), 400

    try:
        response = rag_service.answer_question(
            question=query,
            equipment=equipment,
            session_id=session_id,
            force_fallback=force_fallback,
            should_cancel=lambda: request_id in cancelled_requests,
            user_role=user_role,
        )
        if request_id:
            cancelled_requests.discard(request_id)
        flask_response = make_response(jsonify(response.to_dict()))
        flask_response.set_cookie(
            "hrrg_session_id",
            session_id,
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="Lax",
        )
        return flask_response
    except Exception as exc:
        logger.exception("Error no controlado en /ask")
        return jsonify({"error": f"Error interno del asistente: {exc}"}), 500


@api.post("/requests/cancel")
def cancel_request():
    payload = request.get_json(silent=True) or {}
    request_id = str(payload.get("request_id", "")).strip()
    if request_id:
        cancelled_requests.add(request_id)
    return jsonify({"status": "cancelado"})


@api.post("/memory/clear")
def clear_memory():
    session_id = request.cookies.get("hrrg_session_id")
    if session_id:
        memory_service.clear_session(session_id)
    return jsonify({"status": "memoria_limpiada"})


@api.post("/ingest")
def ingest_documents():
    result = ingestion_service.ingest_directory(settings.raw_documents_dir)
    status_code = 207 if result["errors"] else 200
    return jsonify(result), status_code


@api.get("/manuals/<path:filename>")
def serve_manual(filename: str):
    return send_from_directory(settings.raw_documents_dir, filename, as_attachment=False)
