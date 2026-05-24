from __future__ import annotations

import argparse
import csv
import io
import subprocess
import time
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/ocr_output")
REPORT_DIR = Path("reports")
REPORT_CSV = REPORT_DIR / "ocr_pdfs_requieren_ocr.csv"

TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TARGET_FILES = [
    "drager_vn500_entrar_en_servicio_y_copiar_log_errores_recarga_soft.pdf",
    "drager_vn500_manual_usuario_vn500_es.pdf",
    "ventilador_crossvent_manual_de_servicio_crossvent_biomed_devices_crossvent_4.pdf",
    "ventilador_leistung_luft3_6_nivel_3_terapia_fallas_frecuentes_presion_1.pdf",
    "ventilador_maquet_servo_i_maquet_servo_i_service_manual_2_of_2.pdf",
]


def configure_tesseract() -> None:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE


def get_available_languages() -> set[str]:
    try:
        result = subprocess.run(
            [TESSERACT_EXE, "--list-langs"],
            capture_output=True,
            text=True,
            check=False,
        )
        lines = [line.strip() for line in result.stdout.splitlines()]
        return {line for line in lines if line and not line.lower().startswith("list of")}
    except Exception:
        return set()


def choose_language() -> str:
    langs = get_available_languages()

    if "spa" in langs and "eng" in langs:
        return "spa+eng"

    if "spa" in langs:
        return "spa"

    if "eng" in langs:
        return "eng"

    return "eng"


def count_text_chars(pdf_path: Path) -> int:
    try:
        doc = fitz.open(pdf_path)
    except Exception:
        return 0

    total = 0
    try:
        for page in doc:
            text = page.get_text("text") or ""
            total += len(text.strip())
    finally:
        doc.close()

    return total


def ocr_pdf(input_pdf: Path, output_pdf: Path, lang: str, dpi: int = 200) -> dict:
    start = time.time()

    result = {
        "archivo_original": input_pdf.name,
        "archivo_ocr": output_pdf.name,
        "paginas": 0,
        "caracteres_antes": 0,
        "caracteres_despues": 0,
        "estado": "PENDIENTE",
        "observacion": "",
        "segundos": 0,
    }

    if not input_pdf.exists():
        result["estado"] = "ERROR"
        result["observacion"] = f"No existe el archivo de entrada: {input_pdf}"
        return result

    result["caracteres_antes"] = count_text_chars(input_pdf)

    try:
        source_doc = fitz.open(input_pdf)
    except Exception as exc:
        result["estado"] = "ERROR"
        result["observacion"] = f"No se pudo abrir el PDF: {exc}"
        return result

    result["paginas"] = len(source_doc)

    output_doc = fitz.open()

    try:
        for page_index, page in enumerate(source_doc, start=1):
            print(f"  OCR página {page_index}/{len(source_doc)}...")

            pix = page.get_pixmap(dpi=dpi, alpha=False)
            image_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(image_bytes))

            pdf_bytes = pytesseract.image_to_pdf_or_hocr(
                image,
                extension="pdf",
                lang=lang,
                config="--psm 6",
            )

            page_pdf = fitz.open("pdf", pdf_bytes)
            output_doc.insert_pdf(page_pdf)
            page_pdf.close()

        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        output_doc.save(output_pdf, garbage=4, deflate=True)
        output_doc.close()
        source_doc.close()

        result["caracteres_despues"] = count_text_chars(output_pdf)

        if result["caracteres_despues"] > result["caracteres_antes"]:
            result["estado"] = "OK"
            result["observacion"] = "OCR generado y aumentó el texto extraíble."
        else:
            result["estado"] = "REVISAR"
            result["observacion"] = "OCR generado, pero no aumentó claramente el texto extraíble."

    except Exception as exc:
        try:
            output_doc.close()
        except Exception:
            pass
        try:
            source_doc.close()
        except Exception:
            pass

        result["estado"] = "ERROR"
        result["observacion"] = f"Error durante OCR: {exc}"

    result["segundos"] = round(time.time() - start, 2)
    return result


def write_report(rows: list[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "archivo_original",
        "archivo_ocr",
        "paginas",
        "caracteres_antes",
        "caracteres_despues",
        "estado",
        "observacion",
        "segundos",
    ]

    with REPORT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera versiones OCR de PDFs críticos sin pisar data/raw."
    )
    parser.add_argument(
        "--file",
        type=str,
        default="",
        help="Nombre exacto de un PDF dentro de data/raw para procesar solo ese archivo.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Procesa los 5 PDFs críticos definidos en TARGET_FILES.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Resolución de renderizado para OCR. Default: 200.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sobrescribe PDFs OCR existentes.",
    )
    return parser.parse_args()


def main() -> None:
    configure_tesseract()
    args = parse_args()

    lang = choose_language()
    print(f"Tesseract: {pytesseract.get_tesseract_version()}")
    print(f"Idioma OCR seleccionado: {lang}")

    if args.file:
        files_to_process = [args.file]
    elif args.all:
        files_to_process = TARGET_FILES
    else:
        print()
        print("No se indicó qué procesar.")
        print("Para probar con un archivo:")
        print(
            "python scripts\\ocr_pdfs_requieren_ocr.py --file "
            "drager_vn500_entrar_en_servicio_y_copiar_log_errores_recarga_soft.pdf"
        )
        print()
        print("Para procesar los 5 críticos:")
        print("python scripts\\ocr_pdfs_requieren_ocr.py --all")
        return

    rows = []

    for filename in files_to_process:
        input_pdf = RAW_DIR / filename
        output_pdf = OUTPUT_DIR / f"{input_pdf.stem}_ocr.pdf"

        print()
        print(f"Procesando: {filename}")
        print(f"Salida: {output_pdf}")

        if output_pdf.exists() and not args.force:
            print("  Ya existe OCR. Se omite. Usá --force para sobrescribir.")
            rows.append(
                {
                    "archivo_original": input_pdf.name,
                    "archivo_ocr": output_pdf.name,
                    "paginas": "",
                    "caracteres_antes": count_text_chars(input_pdf),
                    "caracteres_despues": count_text_chars(output_pdf),
                    "estado": "OMITIDO",
                    "observacion": "El archivo OCR ya existía.",
                    "segundos": 0,
                }
            )
            continue

        rows.append(ocr_pdf(input_pdf, output_pdf, lang=lang, dpi=args.dpi))

    write_report(rows)

    print()
    print("Proceso OCR finalizado.")
    print(f"Reporte generado: {REPORT_CSV}")

    for row in rows:
        print(
            f"- {row['archivo_original']} | {row['estado']} | "
            f"antes: {row['caracteres_antes']} | después: {row['caracteres_despues']}"
        )


if __name__ == "__main__":
    main()