from __future__ import annotations

from urllib.parse import unquote

import fitz
from flask import Blueprint, abort, redirect, render_template, request, send_file, send_from_directory, url_for

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


@web_bp.get("/manual-thumbnails/<path:filename>/page/<int:page>.png")
def serve_manual_thumbnail(filename: str, page: int):
    safe_filename = unquote(filename)
    pdf_path = (settings.raw_documents_dir / safe_filename).resolve()
    raw_root = settings.raw_documents_dir.resolve()
    if raw_root not in pdf_path.parents or not pdf_path.is_file() or pdf_path.suffix.lower() != ".pdf":
        abort(404)

    cache_dir = settings.base_dir / "data" / "page_thumbnails"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_source = safe_filename.replace("/", "__").replace("\\", "__")
    cache_name = f"{cache_source}__p{page}.png"
    cache_path = cache_dir / cache_name

    if not cache_path.exists():
        try:
            with fitz.open(pdf_path) as pdf:
                if page < 1 or page > pdf.page_count:
                    abort(404)
                pixmap = pdf[page - 1].get_pixmap(dpi=96, alpha=False)
                pixmap.save(cache_path)
        except Exception:
            abort(404)

    return send_file(cache_path, mimetype="image/png", max_age=86400)
