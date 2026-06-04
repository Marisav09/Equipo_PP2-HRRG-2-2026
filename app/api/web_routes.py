from __future__ import annotations

from urllib.parse import unquote

import fitz
from flask import Blueprint, abort, make_response, redirect, render_template, request, send_file, send_from_directory, url_for

from app.core.config import settings
from app.services.equipment_service import EquipmentService


web_bp = Blueprint("web", __name__)
equipment_service = EquipmentService()


def _redirect_home_with_qr_equipment(equipment_id: str):
    response = make_response(redirect(url_for("web.home")))
    response.set_cookie(
        "hrrg_qr_equipment_id",
        equipment_id,
        max_age=60 * 15,
        httponly=True,
        samesite="Lax",
    )
    return response


@web_bp.get("/")
def home():
    return render_template("landing.html")


@web_bp.get("/qr/<equipment_id>")
def qr_landing(equipment_id: str):
    equipment = equipment_service.get_by_id(equipment_id)
    if not equipment:
        abort(404)

    return _redirect_home_with_qr_equipment(equipment.id)


@web_bp.get("/login")
def login():
    raw_profile = request.args.get("perfil", "tecnico").strip().lower()
    profile = "operador" if raw_profile == "operador" else "tecnico"
    return render_template("login.html", profile=profile)


@web_bp.get("/tecnico")
def technician_equipment_selector():
    if request.cookies.get("hrrg_technician_auth") != "ok":
        return redirect(url_for("web.login", perfil="tecnico"))
    return render_template(
        "operator_select.html",
        profile="tecnico",
        equipments=equipment_service.list_equipments(),
    )


@web_bp.get("/operador")
def operator_equipment_selector():
    if request.cookies.get("hrrg_operator_auth") != "ok":
        return redirect(url_for("web.login", perfil="operador"))
    return render_template(
        "operator_select.html",
        profile="operador",
        equipments=equipment_service.list_equipments(),
    )


@web_bp.get("/equipo/<equipment_id>")
def operator_console(equipment_id: str):
    equipment = equipment_service.get_by_id(equipment_id)
    if not equipment:
        abort(404)
    if request.cookies.get("hrrg_operator_auth") != "ok":
        return _redirect_home_with_qr_equipment(equipment.id)
    return render_template("operator.html", equipment=equipment)


@web_bp.get("/tecnico/equipo/<equipment_id>")
def technician_console(equipment_id: str):
    equipment = equipment_service.get_by_id(equipment_id)
    if not equipment:
        abort(404)
    if request.cookies.get("hrrg_technician_auth") != "ok":
        return _redirect_home_with_qr_equipment(equipment.id)
    return render_template("technician.html", equipment=equipment)


@web_bp.get("/manuals/<path:filename>")
def serve_manual(filename: str):
    return send_from_directory(settings.raw_documents_dir, filename, as_attachment=False)


@web_bp.get("/processed/<path:filename>")
def serve_processed(filename: str):
    return send_from_directory(settings.processed_documents_dir, filename, as_attachment=False)


@web_bp.get("/images/<path:filename>")
def serve_extracted_image(filename: str):
    return send_from_directory(settings.base_dir / "data" / "images", filename, as_attachment=False)


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
