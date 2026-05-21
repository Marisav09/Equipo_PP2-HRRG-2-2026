from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    import fitz  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - depends on the local environment.
    fitz = None


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
MANIFEST_PATH = PROCESSED_DIR / "pdf_name_manifest.csv"
CURATION_CSV_PATH = PROCESSED_DIR / "reporte_curaduria_pdfs.csv"
CURATION_MD_PATH = PROCESSED_DIR / "reporte_curaduria_pdfs.md"

NORMALIZED_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.pdf$")
DOCUMENT_TYPE_TOKENS = {
    "manual",
    "manual_servicio",
    "manual_tecnico",
    "manual_usuario",
    "calibracion",
    "capacitacion",
    "fallas_frecuentes",
    "folleto",
    "guia_rapida",
}

DECISION_LABELS_ES = {
    "accepted": "aceptado",
    "review_metadata": "revisar_metadatos",
    "review_duplicate": "revisar_duplicado",
    "quarantine": "cuarentena",
}

ISSUE_LABELS_ES = {
    "duplicate_content": "contenido_duplicado",
    "empty_file": "archivo_vacio",
    "invalid_pdf_header": "cabecera_pdf_invalida",
    "missing_document_type_token": "falta_tipo_documental_en_nombre",
    "no_extractable_text": "sin_texto_extraible",
    "non_normalized_name": "nombre_no_normalizado",
    "non_pdf_file": "archivo_no_pdf",
    "not_listed_in_manifest": "no_figura_en_manifiesto",
    "unreadable_pdf": "pdf_no_legible",
}

PDF_STATUS_LABELS_ES = {
    "not_inspected_pymupdf_missing": "no_inspeccionado_falta_pymupdf",
    "readable": "legible",
}


@dataclass
class FileAudit:
    file_name: str
    relative_path: str
    extension: str
    size_bytes: int
    sha256: str
    is_pdf_extension: bool
    has_pdf_header: bool
    name_is_normalized: bool
    name_has_document_type: bool
    listed_in_manifest: bool
    duplicate_group_size: int
    duplicate_of: str
    pdf_status: str
    page_count: str
    extracted_text_chars: str
    image_count: str
    issues: list[str]

    @property
    def decision(self) -> str:
        blocking = {
            "non_pdf_file",
            "invalid_pdf_header",
            "unreadable_pdf",
            "empty_file",
        }
        if any(issue in blocking for issue in self.issues):
            return "quarantine"
        if "duplicate_content" in self.issues:
            return "review_duplicate"
        if self.issues:
            return "review_metadata"
        return "accepted"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_pdf_header(path: Path) -> bool:
    with path.open("rb") as file:
        return file.read(5) == b"%PDF-"


def load_manifest_names(path: Path) -> set[str]:
    if not path.exists():
        return set()

    with path.open(newline="", encoding="utf-8") as manifest_file:
        reader = csv.DictReader(manifest_file)
        return {
            row["normalized_file"].strip()
            for row in reader
            if row.get("normalized_file") and row["normalized_file"].strip()
        }


def detect_document_type_token(file_name: str) -> bool:
    stem = Path(file_name).stem
    return any(
        token in stem
        for token in DOCUMENT_TYPE_TOKENS
    )


def translate_decision(decision: str) -> str:
    return DECISION_LABELS_ES.get(decision, decision)


def translate_issue(issue: str) -> str:
    return ISSUE_LABELS_ES.get(issue, issue)


def translate_pdf_status(status: str) -> str:
    if not status:
        return ""
    if status.startswith("unreadable_pdf"):
        return status.replace("unreadable_pdf", ISSUE_LABELS_ES["unreadable_pdf"], 1)
    return PDF_STATUS_LABELS_ES.get(status, status)


def inspect_pdf(path: Path) -> tuple[str, str, str, str]:
    if fitz is None:
        return "not_inspected_pymupdf_missing", "", "", ""

    try:
        document = fitz.open(path)
    except Exception as exc:  # noqa: BLE001 - diagnostic script.
        return f"unreadable_pdf: {exc}", "", "", ""

    with document:
        text_chars = 0
        image_count = 0
        for page in document:
            try:
                text_chars += len(page.get_text("text").strip())
                image_count += len(page.get_images(full=True))
            except Exception:
                continue
        return "readable", str(document.page_count), str(text_chars), str(image_count)


def collect_audits(raw_dir: Path, manifest_names: set[str]) -> list[FileAudit]:
    paths = sorted(path for path in raw_dir.rglob("*") if path.is_file())
    hash_by_path = {path: sha256_file(path) for path in paths}

    paths_by_hash: dict[str, list[Path]] = defaultdict(list)
    for path, file_hash in hash_by_path.items():
        paths_by_hash[file_hash].append(path)

    audits: list[FileAudit] = []
    for path in paths:
        relative_path = path.relative_to(ROOT_DIR).as_posix()
        extension = path.suffix.lower()
        size_bytes = path.stat().st_size
        is_pdf_extension = extension == ".pdf"
        pdf_header = has_pdf_header(path) if size_bytes else False
        normalized_name = bool(NORMALIZED_NAME_PATTERN.fullmatch(path.name))
        has_document_type = detect_document_type_token(path.name)
        listed_in_manifest = path.name in manifest_names
        duplicates = sorted(paths_by_hash[hash_by_path[path]], key=lambda item: item.as_posix())
        duplicate_of = ""
        duplicate_group_size = len(duplicates)
        if duplicate_group_size > 1 and path != duplicates[0]:
            duplicate_of = duplicates[0].relative_to(ROOT_DIR).as_posix()

        issues: list[str] = []
        if size_bytes == 0:
            issues.append("empty_file")
        if not is_pdf_extension:
            issues.append("non_pdf_file")
        if is_pdf_extension and not pdf_header:
            issues.append("invalid_pdf_header")
        if is_pdf_extension and not normalized_name:
            issues.append("non_normalized_name")
        if is_pdf_extension and not has_document_type:
            issues.append("missing_document_type_token")
        if manifest_names and is_pdf_extension and not listed_in_manifest:
            issues.append("not_listed_in_manifest")
        if duplicate_group_size > 1:
            issues.append("duplicate_content")

        pdf_status = ""
        page_count = ""
        extracted_text_chars = ""
        image_count = ""
        if is_pdf_extension and pdf_header:
            pdf_status, page_count, extracted_text_chars, image_count = inspect_pdf(path)
            if pdf_status.startswith("unreadable_pdf"):
                issues.append("unreadable_pdf")
            if pdf_status == "readable" and extracted_text_chars == "0":
                issues.append("no_extractable_text")

        audits.append(
            FileAudit(
                file_name=path.name,
                relative_path=relative_path,
                extension=extension,
                size_bytes=size_bytes,
                sha256=hash_by_path[path],
                is_pdf_extension=is_pdf_extension,
                has_pdf_header=pdf_header,
                name_is_normalized=normalized_name,
                name_has_document_type=has_document_type,
                listed_in_manifest=listed_in_manifest,
                duplicate_group_size=duplicate_group_size,
                duplicate_of=duplicate_of,
                pdf_status=pdf_status,
                page_count=page_count,
                extracted_text_chars=extracted_text_chars,
                image_count=image_count,
                issues=issues,
            )
        )

    return audits


def write_csv(audits: list[FileAudit], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "decision_sugerida",
        "nombre_archivo",
        "ruta_relativa",
        "extension",
        "tamano_bytes",
        "sha256",
        "tiene_extension_pdf",
        "tiene_cabecera_pdf_valida",
        "nombre_normalizado",
        "nombre_incluye_tipo_documental",
        "figura_en_manifiesto",
        "cantidad_en_grupo_duplicado",
        "duplicado_de",
        "estado_pdf",
        "cantidad_paginas",
        "caracteres_texto_extraido",
        "cantidad_imagenes",
        "observaciones",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for audit in audits:
            writer.writerow(
                {
                    "decision_sugerida": translate_decision(audit.decision),
                    "nombre_archivo": audit.file_name,
                    "ruta_relativa": audit.relative_path,
                    "extension": audit.extension,
                    "tamano_bytes": audit.size_bytes,
                    "sha256": audit.sha256,
                    "tiene_extension_pdf": audit.is_pdf_extension,
                    "tiene_cabecera_pdf_valida": audit.has_pdf_header,
                    "nombre_normalizado": audit.name_is_normalized,
                    "nombre_incluye_tipo_documental": audit.name_has_document_type,
                    "figura_en_manifiesto": audit.listed_in_manifest,
                    "cantidad_en_grupo_duplicado": audit.duplicate_group_size,
                    "duplicado_de": audit.duplicate_of,
                    "estado_pdf": translate_pdf_status(audit.pdf_status),
                    "cantidad_paginas": audit.page_count,
                    "caracteres_texto_extraido": audit.extracted_text_chars,
                    "cantidad_imagenes": audit.image_count,
                    "observaciones": ";".join(translate_issue(issue) for issue in audit.issues),
                }
            )


def write_markdown(audits: list[FileAudit], output_path: Path, raw_dir: Path) -> None:
    decisions = Counter(audit.decision for audit in audits)
    issues = Counter(issue for audit in audits for issue in audit.issues)
    duplicate_sets = {
        audit.sha256: [
            item.relative_path
            for item in audits
            if item.sha256 == audit.sha256 and audit.duplicate_group_size > 1
        ]
        for audit in audits
        if audit.duplicate_group_size > 1
    }
    reviewed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pymupdf_status = "disponible" if fitz is not None else "no disponible"

    lines = [
        "# Curaduria de PDFs crudos",
        "",
        f"- Fecha de auditoria: {reviewed_at}",
        f"- Carpeta auditada: `{raw_dir.relative_to(ROOT_DIR).as_posix()}`",
        f"- Archivos analizados: {len(audits)}",
        f"- PyMuPDF: {pymupdf_status}",
        "",
        "## Decisiones sugeridas",
        "",
    ]
    for decision, count in sorted(decisions.items()):
        lines.append(f"- `{translate_decision(decision)}`: {count}")

    lines.extend(["", "## Issues detectados", ""])
    if issues:
        for issue, count in issues.most_common():
            lines.append(f"- `{translate_issue(issue)}`: {count}")
    else:
        lines.append("- No se detectaron issues.")

    lines.extend(["", "## Archivos que requieren accion", ""])
    actionable = [audit for audit in audits if audit.decision != "accepted"]
    if actionable:
        lines.append("| Decision sugerida | Archivo | Observaciones |")
        lines.append("| --- | --- | --- |")
        for audit in actionable:
            issue_text = ", ".join(f"`{translate_issue(issue)}`" for issue in audit.issues)
            lines.append(
                f"| `{translate_decision(audit.decision)}` | `{audit.relative_path}` | {issue_text} |"
            )
    else:
        lines.append("- Todos los archivos quedaron aceptados.")

    lines.extend(["", "## Posibles duplicados exactos", ""])
    if duplicate_sets:
        for index, paths in enumerate(duplicate_sets.values(), start=1):
            lines.append(f"### Grupo {index}")
            for path in paths:
                lines.append(f"- `{path}`")
            lines.append("")
    else:
        lines.append("- No se detectaron duplicados exactos por SHA-256.")

    lines.extend(
        [
            "## Criterio aplicado",
            "",
            "- `aceptado`: PDF con extension y cabecera validas, sin observaciones detectadas.",
            "- `revisar_metadatos`: PDF utilizable, pero con nombre/metadatos a revisar.",
            "- `revisar_duplicado`: contenido exacto repetido; conservar solo la version correcta.",
            "- `cuarentena`: archivo no PDF, vacio, cabecera invalida o PDF ilegible.",
            "",
            "El CSV contiene el detalle completo por archivo.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita y cura la coleccion de PDFs alojada en data/raw."
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DIR,
        help="Carpeta con PDFs crudos normalizados.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_PATH,
        help="Manifiesto generado durante la normalizacion.",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=CURATION_CSV_PATH,
        help="Ruta del reporte CSV.",
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=CURATION_MD_PATH,
        help="Ruta del reporte Markdown.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = args.raw_dir if args.raw_dir.is_absolute() else ROOT_DIR / args.raw_dir
    manifest_path = args.manifest if args.manifest.is_absolute() else ROOT_DIR / args.manifest
    csv_output = args.csv_output if args.csv_output.is_absolute() else ROOT_DIR / args.csv_output
    md_output = args.md_output if args.md_output.is_absolute() else ROOT_DIR / args.md_output

    if not raw_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta a auditar: {raw_dir}")

    manifest_names = load_manifest_names(manifest_path)
    audits = collect_audits(raw_dir, manifest_names)
    write_csv(audits, csv_output)
    write_markdown(audits, md_output, raw_dir)

    decisions = Counter(audit.decision for audit in audits)
    print(f"Archivos analizados: {len(audits)}")
    for decision, count in sorted(decisions.items()):
        print(f"{translate_decision(decision)}: {count}")
    print(f"CSV: {csv_output.relative_to(ROOT_DIR)}")
    print(f"Markdown: {md_output.relative_to(ROOT_DIR)}")
    if fitz is None:
        print("Aviso: PyMuPDF no esta instalado; no se calcularon paginas/texto/imagenes.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - diagnostic script.
        print(f"Error: {exc}", file=sys.stderr)
        raise
