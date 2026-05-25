from __future__ import annotations

from flask import Blueprint, jsonify

from app.services.equipment_service import EquipmentService


equipment_bp = Blueprint("equipment", __name__)
equipment_service = EquipmentService()


@equipment_bp.get("/")
def list_equipments():
    return jsonify({"equipments": equipment_service.list_equipments()})
