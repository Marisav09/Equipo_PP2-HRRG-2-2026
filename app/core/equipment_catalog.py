from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Equipment:
    id: str
    name: str
    aliases: tuple[str, ...]


EQUIPMENT_CATALOG: tuple[Equipment, ...] = (
    Equipment(
        id="sterrad-100",
        name="Esterilizadora Sterrad 100",
        aliases=("sterrad 100", "sterrad 100s", "esterilizadora sterrad"),
    ),
    Equipment(
        id="rodantes-mac-gmm",
        name="Rodantes MAC GMM",
        aliases=("mac gmm", "hd-67", "hd 67"),
    ),
    Equipment(
        id="perfect-pitch",
        name="Analizador de tonos Perfect Pitch",
        aliases=("perfect pitch", "analizador de tonos"),
    ),
    Equipment(
        id="draeger-vn500",
        name="Respirador Draeger - VN500",
        aliases=("draeger vn500", "draeger v n500", "vn500", "evita v300", "babylog vn500", "draguer respirador"),
    ),
    Equipment(
        id="incubadora-medix-tr306",
        name="Incubadora Medix TR306",
        aliases=("medix tr306", "incubadora medix", "natal care", "camilla de hemodinamia stille q2"),
    ),
)


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    without_accents = unicodedata.normalize("NFKD", value)
    ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
    compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).strip().lower()
    return re.sub(r"\s+", " ", compact)


def find_equipment_by_id(equipment_id: str) -> Equipment | None:
    normalized_id = equipment_id.strip().lower()
    return next((item for item in EQUIPMENT_CATALOG if item.id == normalized_id), None)


def canonical_equipment_name(value: str | None) -> str | None:
    normalized = normalize_text(value)
    if not normalized:
        return None

    for equipment in EQUIPMENT_CATALOG:
        candidates = (equipment.name, equipment.id, *equipment.aliases)
        if any(normalized == normalize_text(candidate) for candidate in candidates):
            return equipment.name

    return None


def find_equipment_by_text(value: str | None) -> Equipment | None:
    normalized = normalize_text(value)
    if not normalized:
        return None

    for equipment in EQUIPMENT_CATALOG:
        candidates = (equipment.name, equipment.id, *equipment.aliases)
        if any(normalize_text(candidate) in normalized for candidate in candidates):
            return equipment

    return None


def infer_equipment_from_path(pdf_path, source_dir) -> Equipment | None:
    try:
        relative_parts = pdf_path.relative_to(source_dir).parts
    except ValueError:
        relative_parts = pdf_path.parts

    candidates = [pdf_path.stem, *relative_parts[:-1]]
    for candidate in candidates:
        equipment = find_equipment_by_text(candidate)
        if equipment:
            return equipment
    return None


def infer_equipment_from_text(text: str) -> Equipment | None:
    return find_equipment_by_text(text)
