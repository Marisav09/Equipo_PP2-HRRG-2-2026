from __future__ import annotations

from flask import Blueprint, jsonify, make_response, request

from app.core.config import settings


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    password = str(payload.get("password", "")).strip()

    if password != settings.technical_user_password:
        return jsonify({"error": "Credenciales invalidas."}), 401

    response = make_response(jsonify({"status": "ok", "redirect_url": "/tecnico"}))
    response.set_cookie(
        "hrrg_technician_auth",
        "ok",
        max_age=60 * 60 * 8,
        httponly=True,
        samesite="Lax",
    )
    return response


@auth_bp.post("/api/auth/logout")
def logout():
    response = make_response(jsonify({"status": "ok", "redirect_url": "/login"}))
    response.delete_cookie("hrrg_technician_auth")
    return response
