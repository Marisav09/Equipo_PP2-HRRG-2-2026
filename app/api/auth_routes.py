from __future__ import annotations

from flask import Blueprint, jsonify, make_response, request

from app.core.config import settings
from app.core.equipment_catalog import find_equipment_by_id


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip().lower()
    password = str(payload.get("password", "")).strip()
    profile = str(payload.get("profile", "tecnico")).strip().lower()

    if profile == "operador":
        expected_username = "operador"
        expected_password = settings.operator_user_password
        cookie_name = "hrrg_operator_auth"
        redirect_url = "/operador"
        user_service = "OPERADOR"
        qr_redirect_prefix = "/equipo"
    else:
        expected_username = "tecnico"
        expected_password = settings.technical_user_password
        cookie_name = "hrrg_technician_auth"
        redirect_url = "/tecnico"
        user_service = "TECNICO"
        qr_redirect_prefix = "/tecnico/equipo"

    if username != expected_username or password != expected_password:
        return jsonify({"error": "Credenciales invalidas."}), 401

    qr_equipment_id = str(request.cookies.get("hrrg_qr_equipment_id") or "").strip()
    if qr_equipment_id and find_equipment_by_id(qr_equipment_id):
        redirect_url = f"{qr_redirect_prefix}/{qr_equipment_id}"

    response = make_response(jsonify({"status": "ok", "redirect_url": redirect_url}))
    response.set_cookie(
        cookie_name,
        "ok",
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "hrrg_username",
        username,
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "hrrg_user_service",
        user_service,
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="Lax",
    )
    response.delete_cookie("hrrg_qr_equipment_id")
    return response


@auth_bp.post("/api/auth/logout")
def logout():
    response = make_response(jsonify({"status": "ok", "redirect_url": "/"}))
    response.delete_cookie("hrrg_technician_auth")
    response.delete_cookie("hrrg_operator_auth")
    response.delete_cookie("hrrg_username")
    response.delete_cookie("hrrg_user_service")
    response.delete_cookie("hrrg_qr_equipment_id")
    return response
