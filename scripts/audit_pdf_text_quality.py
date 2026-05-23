from __future__ import annotations

import csv
from pathlib import Path

import fitz  # PyMuPDF


RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
OUTPUT_CSV = REPORT_DIR / "auditoria_calidad_texto_pdfs.csv"


# Criterios simples para clasificar la calidad textual.
# Se pueden ajustar después según los resultados reales.
MIN_TOTAL_CHARS_OK = 3000
MIN_AVG_CHARS_PER_PAGE_OK = 200
MIN_TOTAL_CHARS_REVIEW = 500
MIN_AVG_CHARS_PER_PAGE_REVIEW = 50


def classify_pdf(total_chars: int, pages: int) -> tuple[str, str]:
    if pages == 0:
        return "REQUIERE_REVISION", "No se pudieron leer páginas del PDF."

    avg_chars = total_chars / pages if pages else 0

    if total_chars >= MIN_TOTAL_CHARS_OK and avg_chars >= MIN_AVG_CHARS_PER_PAGE_OK:
        return "OK", "Texto extraíble suficiente para ingesta textual."

    if total_chars >= MIN_TOTAL_CHARS_REVIEW and avg_chars >= MIN_AVG_CHARS_PER_PAGE_REVIEW:
        return "REVISAR", "Texto extraíble parcial o bajo; conviene revisar calidad."

    return "REQUIERE_OCR", "Texto insuficiente; posible PDF escaneado o con bajo texto extraíble."


def audit_pdf(pdf_path: Path) -> dict:
    try:
        doc = fitz.open(pdf_path)
    except Exception as exc:
        return {
            "archivo": pdf_path.name,
            "paginas": 0,
            "caracteres_extraidos": 0,
            "promedio_caracteres_por_pagina": 0,
            "estado": "ERROR",
            "observacion": f"No se pudo abrir el PDF: {exc}",
        }

    total_chars = 0
    pages = len(doc)

    try:
        for page in doc:
            text = page.get_text("text") or ""
            total_chars += len(text.strip())
    except Exception as exc:
        doc.close()
        return {
            "archivo": pdf_path.name,
            "paginas": pages,
            "caracteres_extraidos": total_chars,
            "promedio_caracteres_por_pagina": round(total_chars / pages, 2) if pages else 0,
            "estado": "ERROR",
            "observacion": f"Error durante extracción de texto: {exc}",
        }

    doc.close()

    avg_chars = round(total_chars / pages, 2) if pages else 0
    estado, observacion = classify_pdf(total_chars, pages)

    return {
        "archivo": pdf_path.name,
        "paginas": pages,
        "caracteres_extraidos": total_chars,
        "promedio_caracteres_por_pagina": avg_chars,
        "estado": estado,
        "observacion": observacion,
    }


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No se encontraron PDFs en {RAW_DIR}")
        return

    rows = []

    print(f"Auditando {len(pdf_files)} PDFs en {RAW_DIR}...")

    for pdf_path in pdf_files:
        print(f"Revisando: {pdf_path.name}")
        rows.append(audit_pdf(pdf_path))

    fieldnames = [
        "archivo",
        "paginas",
        "caracteres_extraidos",
        "promedio_caracteres_por_pagina",
        "estado",
        "observacion",
    ]

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    ok = sum(1 for row in rows if row["estado"] == "OK")
    revisar = sum(1 for row in rows if row["estado"] == "REVISAR")
    requiere_ocr = sum(1 for row in rows if row["estado"] == "REQUIERE_OCR")
    errores = sum(1 for row in rows if row["estado"] == "ERROR")

    print()
    print("Auditoría finalizada.")
    print(f"Reporte generado: {OUTPUT_CSV}")
    print(f"Total PDFs: {total}")
    print(f"OK: {ok}")
    print(f"REVISAR: {revisar}")
    print(f"REQUIERE_OCR: {requiere_ocr}")
    print(f"ERROR: {errores}")


if __name__ == "__main__":
    main()