from __future__ import annotations

import logging
from uuid import uuid4

from flask import Blueprint, jsonify, make_response, render_template, request, send_from_directory

from app.core.config import settings
from app.services.audit_service import AuditService
from app.services.ingestion_service import IngestionService
from app.services.memory_service import MemoryService
from app.services.rag_service import RagService
from app.services.ticket_service import TicketService

logger = logging.getLogger(__name__)
api = Blueprint("api", __name__)

rag_service = RagService()
ingestion_service = IngestionService()
ticket_service = TicketService()
audit_service = AuditService()
memory_service = MemoryService()
cancelled_requests: set[str] = set()


MOCK_CHATS = [
    {
        "id": index,
        "title": title,
        "equipment": equipment,
        "preview": preview,
    }
    for index, (title, equipment, preview) in enumerate(
        [
            ("Bomba de infusion", "Infusomat Space", "Consulta sobre alarma de oclusion distal."),
            ("Monitor multiparametrico", "Mindray BeneVision N15", "Revision de mantenimiento."),
            ("Ventilador mecanico", "Hamilton C6", "Parametros de prueba funcional."),
            ("Desfibrilador", "Zoll R Series", "Verificacion de bateria."),
            ("Incubadora neonatal", "Drager Isolette", "Control de temperatura."),
        ],
        start=1,
    )
]


@api.get("/")
def index():
    return render_template(
        "index.html",
        chats=MOCK_CHATS,
        active_equipment="Busqueda general",
    )


@api.post("/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    query = str(payload.get("query", "")).strip()
    equipment = str(payload.get("equipment", "")).strip() or None
    force_fallback = bool(payload.get("force_fallback", False))
    request_id = str(payload.get("request_id", "")).strip()
    session_id = request.cookies.get("hrrg_session_id") or str(uuid4())

    if not query:
        return jsonify({"error": "La consulta no puede estar vacia."}), 400

    try:
        response = rag_service.answer_question(
            question=query,
            equipment=equipment,
            session_id=session_id,
            force_fallback=force_fallback,
            should_cancel=lambda: request_id in cancelled_requests,
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


@api.post("/tickets")
def create_manual_ticket():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    equipment = str(payload.get("equipment", "")).strip() or None
    reason = str(payload.get("reason", "Ticket manual del usuario tecnico.")).strip()

    if not question:
        return jsonify({"error": "Debe indicar una descripcion para el ticket."}), 400

    from app.models.schemas import TicketRecord

    ticket_id = ticket_service.create_ticket(
        TicketRecord(question=question, equipment=equipment, reason=reason)
    )
    return jsonify({"ticket_id": ticket_id, "status": "abierto"}), 201


@api.get("/admin/audit")
def admin_audit():
    password = request.args.get("password", "")
    if password != settings.admin_user_password:
        return jsonify({"error": "No autorizado."}), 401
    return jsonify({"queries": audit_service.get_recent_queries()})


@api.get("/admin/tickets")
def admin_tickets():
    password = request.args.get("password", "")
    if password != settings.admin_user_password:
        return jsonify({"error": "No autorizado."}), 401
    return jsonify({"tickets": ticket_service.list_tickets()})
