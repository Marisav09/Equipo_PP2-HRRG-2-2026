from __future__ import annotations

import argparse
import csv
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT_DIR / "data" / "raw_original"
TARGET_DIR = ROOT_DIR / "data" / "raw"
MANIFEST_PATH = ROOT_DIR / "data" / "processed" / "pdf_name_manifest.csv"


@dataclass(frozen=True)
class PdfNameMapping:
    source_path: Path
    target_path: Path
    category: str
    document_type: str


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = ascii_text.replace("&", " y ")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text or "documento"


def detect_document_type(stem: str, parent_parts: list[str]) -> str:
    text = slugify(" ".join(parent_parts + [stem]))

    if "service" in text or "servicio" in text:
        return "manual_servicio"
    if "tecnico" in text or "technical" in text:
        return "manual_tecnico"
    if "usuario" in text or "user" in text or "ifu" in text:
        return "manual_usuario"
    if "calibracion" in text:
        return "calibracion"
    if "guia" in text or "rapida" in text:
        return "guia_rapida"
    if "training" in text or "introduccion" in text:
        return "capacitacion"
    if "brochure" in text or "_br_" in text:
        return "folleto"
    if "troubleshooting" in text or "fallas" in text:
        return "fallas_frecuentes"

    return "manual"


def build_category(pdf_path: Path) -> str:
    relative_parent = pdf_path.parent.relative_to(SOURCE_DIR)
    parts = [slugify(part) for part in relative_parent.parts if slugify(part)]
    return "_".join(parts) if parts else "sin_categoria"


def build_target_name(pdf_path: Path, used_names: set[str]) -> tuple[str, str, str]:
    category = build_category(pdf_path)
    document_type = detect_document_type(pdf_path.stem, list(pdf_path.parent.relative_to(SOURCE_DIR).parts))
    stem = clean_document_stem(slugify(pdf_path.stem))

    base_name = f"{category}_{document_type}_{stem}"
    base_name = re.sub(r"_+", "_", base_name).strip("_")

    candidate = f"{base_name}.pdf"
    suffix = 2
    while candidate in used_names:
        candidate = f"{base_name}_{suffix:02d}.pdf"
        suffix += 1

    used_names.add(candidate)
    return candidate, category, document_type


def clean_document_stem(stem: str) -> str:
    patterns = [
        r"^manual_usuario_y_tecnico_",
        r"^manual_de_usuario_y_tecnico_",
        r"^manual_de_usuario_",
        r"^manual_usuario_",
        r"^manual_de_servicio_",
        r"^manual_servicio_",
        r"^manual_service_",
        r"^service_manual_",
        r"^manual_tecnico_",
        r"^manual_technical_",
        r"^manual_",
        r"_service_manual$",
        r"_manual_de_servicio$",
        r"_manual_tecnico$",
        r"_manual_usuario$",
    ]
    cleaned = stem
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or stem


def create_mappings() -> list[PdfNameMapping]:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta de origen: {SOURCE_DIR}")

    mappings: list[PdfNameMapping] = []
    used_names: set[str] = set()

    for pdf_path in sorted(SOURCE_DIR.rglob("*.pdf")):
        target_name, category, document_type = build_target_name(pdf_path, used_names)
        mappings.append(
            PdfNameMapping(
                source_path=pdf_path,
                target_path=TARGET_DIR / target_name,
                category=category,
                document_type=document_type,
            )
        )

    return mappings


def write_manifest(mappings: list[PdfNameMapping]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as manifest_file:
        writer = csv.DictWriter(
            manifest_file,
            fieldnames=[
                "source_relative_path",
                "normalized_file",
                "category",
                "document_type",
            ],
        )
        writer.writeheader()
        for mapping in mappings:
            writer.writerow(
                {
                    "source_relative_path": mapping.source_path.relative_to(SOURCE_DIR),
                    "normalized_file": mapping.target_path.name,
                    "category": mapping.category,
                    "document_type": mapping.document_type,
                }
            )


def copy_normalized_pdfs(mappings: list[PdfNameMapping]) -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for mapping in mappings:
        shutil.copy2(mapping.source_path, mapping.target_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normaliza nombres de PDFs crudos y los copia a data/raw."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Copia los PDFs normalizados. Sin este flag solo genera el manifiesto.",
    )
    args = parser.parse_args()

    mappings = create_mappings()
    write_manifest(mappings)

    if args.apply:
        copy_normalized_pdfs(mappings)

    print(f"PDFs detectados: {len(mappings)}")
    print(f"Manifiesto: {MANIFEST_PATH.relative_to(ROOT_DIR)}")
    if args.apply:
        print(f"PDFs copiados en: {TARGET_DIR.relative_to(ROOT_DIR)}")
    else:
        print("Modo simulacion: no se copiaron PDFs. Usa --apply para aplicar.")


if __name__ == "__main__":
    main()
