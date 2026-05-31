from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.services.knowledge_audit_service import KnowledgeAuditService


monitoring_bp = Blueprint("monitoring", __name__)
audit_service = KnowledgeAuditService()


def _technician_allowed() -> bool:
    return request.cookies.get("hrrg_technician_auth") == "ok"


def _authenticated_profile() -> str | None:
    if request.cookies.get("hrrg_operator_auth") == "ok":
        return "operador"
    if request.cookies.get("hrrg_technician_auth") == "ok":
        return "tecnico"
    return None


def _current_username(default: str) -> str:
    return request.cookies.get("hrrg_username") or default


@monitoring_bp.get("/dashboard")
def dashboard():
    if not _technician_allowed():
        return jsonify({"error": "Acceso restringido a técnicos."}), 403
    return jsonify(audit_service.dashboard())


@monitoring_bp.get("/consultations")
def consultations():
    if not _technician_allowed():
        return jsonify({"error": "Acceso restringido a técnicos."}), 403
    search = str(request.args.get("search", "")).strip()
    username = str(request.args.get("username", "")).strip()
    equipment = str(request.args.get("equipment", "")).strip()
    date_from = str(request.args.get("date_from", "")).strip()
    date_to = str(request.args.get("date_to", "")).strip()
    return jsonify(
        {
            "items": audit_service.search_consultations(
                search,
                username=username,
                equipment=equipment,
                date_from=date_from,
                date_to=date_to,
            )
        }
    )


@monitoring_bp.get("/my-consultations")
def my_consultations():
    profile = _authenticated_profile()
    if not profile:
        return jsonify({"error": "Debe iniciar sesión para ver sus consultas."}), 403

    username = _current_username(profile)
    raw_limit = request.args.get("limit", "10")
    try:
        limit = int(raw_limit)
    except ValueError:
        limit = 10
    limit = max(1, min(limit, 10))
    return jsonify({"items": audit_service.list_user_consultations(username, limit=limit, profile=profile)})


@monitoring_bp.get("/my-chats")
def my_chats():
    profile = _authenticated_profile()
    if not profile:
        return jsonify({"error": "Debe iniciar sesión para ver su historial."}), 403

    username = _current_username(profile)
    raw_limit = request.args.get("limit", "5")
    try:
        limit = int(raw_limit)
    except ValueError:
        limit = 5
    limit = max(1, min(limit, 5))
    return jsonify({"items": audit_service.list_user_chats(username, limit=limit, profile=profile)})


@monitoring_bp.get("/my-chats/<chat_id>")
def my_chat(chat_id: str):
    profile = _authenticated_profile()
    if not profile:
        return jsonify({"error": "Debe iniciar sesión para ver su historial."}), 403

    username = _current_username(profile)
    chat = audit_service.get_user_chat(username, chat_id, profile=profile)
    if not chat:
        return jsonify({"error": "Chat no encontrado para el usuario autenticado."}), 404
    return jsonify(chat)


@monitoring_bp.post("/consultations/<int:consultation_id>/incident")
def mark_incident(consultation_id: int):
    username = _current_username("operador")
    result = audit_service.mark_incident(consultation_id, username)
    if not result:
        return jsonify({"error": "Consulta no encontrada."}), 404
    return jsonify(result)
