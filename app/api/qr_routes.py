from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request, send_file

from app.services.qr_service import QrService


qr_bp = Blueprint("qr", __name__)
qr_service = QrService()


def _technician_allowed() -> bool:
    return request.cookies.get("hrrg_technician_auth") == "ok"


@qr_bp.post("/")
def generate_qr():
    payload = request.get_json(silent=True) or {}
    base_url = str(payload.get("base_url") or request.host_url).rstrip("/")
    equipment_id = str(payload.get("equipment_id", "")).strip()
    if not equipment_id and not _technician_allowed():
        return jsonify({"error": "Acceso restringido a técnicos."}), 403

    try:
        if equipment_id:
            results = [qr_service.generate_for_equipment(equipment_id, base_url)]
        else:
            results = qr_service.generate_all(base_url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"generated": [result.to_dict() for result in results]})


@qr_bp.get("/<equipment_id>/download")
def download_qr(equipment_id: str):
    base_url = str(request.args.get("base_url") or request.host_url).rstrip("/")
    try:
        result = qr_service.generate_for_equipment(equipment_id, base_url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return send_file(
        result.output_path,
        mimetype="image/png",
        as_attachment=True,
        download_name=f"qr_{result.equipment_id}.png",
    )


@qr_bp.get("/<equipment_id>/print")
def print_qr(equipment_id: str):
    base_url = str(request.args.get("base_url") or request.host_url).rstrip("/")
    try:
        label = qr_service.label_for_equipment(equipment_id, base_url)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return render_template("qr_print.html", labels=[label], auto_print=True, title="Imprimir QR")


@qr_bp.get("/all.pdf")
def download_all_qr_pdf():
    if not _technician_allowed():
        return jsonify({"error": "Acceso restringido a técnicos."}), 403

    base_url = str(request.args.get("base_url") or request.host_url).rstrip("/")
    pdf_path = qr_service.generate_all_pdf(base_url)
    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="qr_equipos_hrrg.pdf",
    )


@qr_bp.get("/print-all")
def print_all_qr():
    if not _technician_allowed():
        return jsonify({"error": "Acceso restringido a técnicos."}), 403

    base_url = str(request.args.get("base_url") or request.host_url).rstrip("/")
    labels = qr_service.labels_for_all(base_url)
    return render_template("qr_print.html", labels=labels, auto_print=True, title="Imprimir todos los QR")
