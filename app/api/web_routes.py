from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, send_from_directory, url_for

from app.core.config import settings
from app.services.equipment_service import EquipmentService


web_bp = Blueprint("web", __name__)
equipment_service = EquipmentService()


@web_bp.get("/")
def home():
    return redirect(url_for("web.login"))


@web_bp.get("/login")
def login():
    return render_template("login.html")


@web_bp.get("/tecnico")
def technician_console():
    if request.cookies.get("hrrg_technician_auth") != "ok":
        return redirect(url_for("web.login"))
    return render_template(
        "technician.html",
        equipments=equipment_service.list_equipments(),
    )


@web_bp.get("/equipo/<equipment_id>")
def operator_console(equipment_id: str):
    equipment = equipment_service.get_by_id(equipment_id)
    return render_template("operator.html", equipment=equipment)


@web_bp.get("/manuals/<path:filename>")
def serve_manual(filename: str):
    return send_from_directory(settings.raw_documents_dir, filename, as_attachment=False)


@web_bp.get("/processed/<path:filename>")
def serve_processed(filename: str):
    return send_from_directory(settings.processed_documents_dir, filename, as_attachment=False)


@web_bp.get("/images/<path:filename>")
def serve_extracted_image(filename: str):
    return send_from_directory(settings.base_dir / "data" / "imagenes", filename, as_attachment=False)
