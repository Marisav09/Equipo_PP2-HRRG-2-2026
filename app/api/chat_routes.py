from __future__ import annotations

from uuid import uuid4

from flask import Blueprint, jsonify, make_response, request

from app.models.schemas import ChatRequest
from app.services.memory_service import MemoryService
from app.services.rag_service import RagService


chat_bp = Blueprint("chat", __name__)
rag_service = RagService()
memory_service = MemoryService()
cancelled_requests: set[str] = set()


@chat_bp.post("/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    chat_request = ChatRequest.from_payload(payload)
    session_id = request.cookies.get("hrrg_session_id") or str(uuid4())

    if not chat_request.query:
        return jsonify({"error": "La consulta no puede estar vacia."}), 400

    response = rag_service.answer_question(
        chat_request=chat_request,
        session_id=session_id,
        should_cancel=lambda: chat_request.request_id in cancelled_requests,
    )
    cancelled_requests.discard(chat_request.request_id)

    flask_response = make_response(jsonify(response))
    flask_response.set_cookie(
        "hrrg_session_id",
        session_id,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="Lax",
    )
    return flask_response


@chat_bp.post("/cancel")
def cancel():
    payload = request.get_json(silent=True) or {}
    request_id = str(payload.get("request_id", "")).strip()
    if request_id:
        cancelled_requests.add(request_id)
    return jsonify({"status": "cancelado"})


@chat_bp.post("/memory/clear")
def clear_memory():
    session_id = request.cookies.get("hrrg_session_id")
    if session_id:
        memory_service.clear_session(session_id)
    return jsonify({"status": "memoria_limpiada"})
