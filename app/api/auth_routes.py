from __future__ import annotations

from flask import Blueprint, jsonify, make_response, request

from app.core.config import settings


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
    else:
        expected_username = "tecnico"
        expected_password = settings.technical_user_password
        cookie_name = "hrrg_technician_auth"
        redirect_url = "/tecnico"
        user_service = "TECNICO"

    if username != expected_username or password != expected_password:
        return jsonify({"error": "Credenciales invalidas."}), 401

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
    return response


@auth_bp.post("/api/auth/logout")
def logout():
    response = make_response(jsonify({"status": "ok", "redirect_url": "/"}))
    response.delete_cookie("hrrg_technician_auth")
    response.delete_cookie("hrrg_operator_auth")
    response.delete_cookie("hrrg_username")
    response.delete_cookie("hrrg_user_service")
    return response
