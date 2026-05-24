from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.services.qr_service import QrService


qr_bp = Blueprint("qr", __name__)
qr_service = QrService()


@qr_bp.post("/")
def generate_qr():
    payload = request.get_json(silent=True) or {}
    base_url = str(payload.get("base_url") or request.host_url).rstrip("/")
    equipment_id = str(payload.get("equipment_id", "")).strip()

    try:
        if equipment_id:
            results = [qr_service.generate_for_equipment(equipment_id, base_url)]
        else:
            results = qr_service.generate_all(base_url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"generated": [result.to_dict() for result in results]})
