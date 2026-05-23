from __future__ import annotations

import re
import unicodedata
from pathlib import Path


GENERAL_EQUIPMENT_LABEL = "Busqueda general"
UNCLASSIFIED_EQUIPMENT_LABEL = "Sin clasificar"

EQUIPMENT_ALIASES: dict[str, tuple[str, ...]] = {
    "Bomba de infusion": (
        "bomba de infusion",
        "bomba infusion",
        "bomba_infusion",
        "infusomat",
        "infusomat space",
    ),
    "Monitor multiparametrico": (
        "monitor multiparametrico",
        "monitor multiparámetro",
        "monitor multiparametro",
        "multiparametro",
        "multiparametrico",
        "hr-1000",
        "hr 1000",
        "meditech",
        "benevision",
        "mindray",
    ),
    "Ventilador mecanico": (
        "ventilador mecanico",
        "ventilador mecánico",
        "hamilton",
        "hamilton c6",
    ),
    "Desfibrilador": (
        "desfibrilador",
        "zoll",
        "zoll r series",
    ),
    "Incubadora neonatal": (
        "incubadora neonatal",
        "incubadora",
        "isolette",
        "drager",
        "draeger",
        "dräger",
    ),
    "Analizador de tonos": (
        "analizador de tonos",
        "perfect pitch",
    ),
    "Rodantes MAC GMM": (
        "rodantes mac gmm",
        "mac gmm",
        "hd-67",
        "hd 67",
    ),
    "Esterilizadora Sterrad 100": (
        "esterilizadora sterrad 100",
        "sterrad 100",
        "sterrad 100 s",
        "sterilization system",
    ),
}


def normalize_equipment_text(value: str | None) -> str:
    if not value:
        return ""
    without_accents = unicodedata.normalize("NFKD", value)
    ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
    compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).strip().lower()
    return re.sub(r"\s+", " ", compact)


def canonical_equipment_label(value: str | None) -> str | None:
    normalized = normalize_equipment_text(value)
    if not normalized:
        return None

    if normalized == normalize_equipment_text(GENERAL_EQUIPMENT_LABEL):
        return GENERAL_EQUIPMENT_LABEL

    for canonical, aliases in EQUIPMENT_ALIASES.items():
        searchable = (canonical, *aliases)
        if any(normalized == normalize_equipment_text(alias) for alias in searchable):
            return canonical

    return value.strip() if value else None


def infer_equipment_from_path(pdf_path: Path, source_dir: Path) -> str | None:
    try:
        relative_parts = pdf_path.relative_to(source_dir).parts
    except ValueError:
        relative_parts = pdf_path.parts

    candidates = [pdf_path.stem, *relative_parts[:-1]]
    for candidate in candidates:
        equipment = canonical_equipment_label(candidate)
        if equipment in EQUIPMENT_ALIASES:
            return equipment

    return None


def infer_equipment_from_text(text: str) -> str | None:
    normalized_text = normalize_equipment_text(text)
    if not normalized_text:
        return None

    for canonical, aliases in EQUIPMENT_ALIASES.items():
        searchable = (canonical, *aliases)
        if any(normalize_equipment_text(alias) in normalized_text for alias in searchable):
            return canonical

    return None
