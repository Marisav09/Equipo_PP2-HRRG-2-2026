from __future__ import annotations

from flask import Blueprint, jsonify

from app.services.system_health_service import SystemHealthService


system_bp = Blueprint("system", __name__)
health_service = SystemHealthService()


@system_bp.get("/health")
def health():
    result = health_service.check()
    status_code = 200 if result["ok"] else 503
    return jsonify(result), status_code
