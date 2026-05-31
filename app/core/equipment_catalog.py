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
        aliases=(
            "sterrad 100",
            "sterrad 100s",
            "esterilizadora sterrad",
            "esterilizador sterrad",
            "advanced sterilization products",
        ),
    ),
    Equipment(
        id="rodantes-mac-gmm",
        name="Rodantes MAC GMM",
        aliases=(
            "mac gmm",
            "hd-67",
            "hd 67",
            "rodantes mac",
            "equipos rodantes",
        ),
    ),
    Equipment(
        id="draeger-vn500",
        name="Respirador Draeger - VN500",
        aliases=(
            "draeger vn500",
            "drager vn500",
            "draguer vn500",
            "draeger v n500",
            "vn500",
            "evita v300",
            "babylog vn500",
            "babyflow",
            "gs500",
            "ps500",
            "volume guarantee",
            "draguer respirador",
            "draeger respirador",
            "respirador draeger",
        ),
    ),
    Equipment(
        id="incubadora-medix-tr306",
        name="Incubadora Medix TR306",
        aliases=(
            "medix tr306",
            "medix tr 306",
            "incubadora medix",
            "incubadora medix tr306",
            "incubadora medix tr200",
            "incubadora medix tr 200",
            "natal care",
            "camilla de hemodinamia stille q2",
        ),
    ),
    Equipment(
        id="ventilador-maquet-servo-i",
        name="Ventilador Maquet Servo-i",
        aliases=(
            "maquet servo i",
            "servo i",
            "servo-i",
            "ventilador maquet",
            "ventilador maquet servo",
            "maquet servo",
            "maquet",
        ),
    ),
    Equipment(
        id="ventilador-neumovent",
        name="Ventilador Neumovent GraphNet",
        aliases=(
            "neumovent",
            "graphnet",
            "graph net",
            "ventilador neumovent",
            "respimeradores",
            "tecme graphnet",
            "neo ts",
            "advance neo",
        ),
    ),
    Equipment(
        id="ventilador-crossvent",
        name="Ventilador Crossvent",
        aliases=(
            "crossvent",
            "biomed devices crossvent",
            "globe trotter",
            "crossvent 3",
            "crossvent 4",
        ),
    ),
    Equipment(
        id="ventilador-engstrom",
        name="Ventilador Engström",
        aliases=(
            "engstrom",
            "engström",
            "engstrom carestation",
            "ventilador engstrom",
            "ventilador engström",
            "ventilacion no invasiva",
            "ventilación no invasiva",
        ),
    ),
    Equipment(
        id="ventilador-leistung-luft3",
        name="Ventilador Leistung LUFT3",
        aliases=(
            "leistung",
            "luft3",
            "luft 3",
            "ventilador leistung",
            "terapia fallas frecuentes",
        ),
    ),
    Equipment(
        id="ventilador-newport-ht70",
        name="Ventilador Newport HT70",
        aliases=(
            "newport ht70",
            "newport ht 70",
            "ht70",
            "ht 70",
            "newport",
        ),
    ),
    Equipment(
        id="fresenius-4008",
        name="Máquina de diálisis Fresenius 4008",
        aliases=(
            "fresenius 4008",
            "fresenius",
            "dialisis fresenius",
            "diálisis fresenius",
            "hemodialisis fresenius",
            "hemodiálisis fresenius",
        ),
    ),
    Equipment(
        id="leica-tp1020",
        name="Procesador de tejidos Leica TP1020",
        aliases=(
            "leica tp1020",
            "tp1020",
            "tp 1020",
            "procesador de tejidos leica",
            "procesador de tejidos",
        ),
    ),
    Equipment(
        id="leica-rm2125",
        name="Micrótomo Leica RM2125",
        aliases=(
            "leica rm2125",
            "rm2125",
            "rm 2125",
            "microtomo",
            "micrótomo",
            "microtomo de rotacion",
            "micrótomo de rotación",
        ),
    ),
    Equipment(
        id="tp-100",
        name="Equipo TP 100",
        aliases=(
            "tp100",
            "tp 100",
            "tp_100",
            "tp80",
            "tp 80",
            "tp_80",
        ),
    ),
    Equipment(
        id="bilirrubinometro-draeger-jm105",
        name="Bilirrubinómetro Draeger JM-105",
        aliases=(
            "jm105",
            "jm 105",
            "bilirubinometro",
            "bilirrubinometro",
            "bilirubinómetro",
            "drager jm105",
            "draeger jm105",
            "draguer jm105",
        ),
    ),
    Equipment(
        id="desfibrilador-mindray-beneheart",
        name="Desfibrilador Mindray BeneHeart",
        aliases=(
            "beneheart",
            "bene heart",
            "mindray beneheart",
            "desfibrilador mindray",
            "desfibrilador beneheart",
        ),
    ),
    Equipment(
        id="electrobisturi",
        name="Electrobisturí",
        aliases=(
            "electrobisturi",
            "electrobisturí",
            "electrosurgical",
            "valleylab",
            "leep system",
            "kairos",
            "force fx",
            "minicomp",
        ),
    ),
    Equipment(
        id="monitor-multiparametrico",
        name="Monitor multiparamétrico",
        aliases=(
            "monitor multiparametrico",
            "monitor multiparamétrico",
            "multiparametrico",
            "multiparamétrico",
            "pm 9000",
            "pm9000",
            "imec",
            "epm series",
            "compact monitor",
        ),
    ),
    Equipment(
        id="cama-electronica",
        name="Cama electrónica",
        aliases=(
            "cama electronica",
            "cama electrónica",
            "cama linet",
            "cama pardo",
            "hitech",
            "komplet",
        ),
    ),
    Equipment(
        id="dinan-af500",
        name="Dinan AF500",
        aliases=(
            "dinan af500",
            "dinan af 500",
            "af500",
            "af 500",
            "sm500",
        ),
    ),
    Equipment(
        id="agitador-presvac-ae500",
        name="Agitador Presvac AE500",
        aliases=(
            "agitador presvac",
            "presvac ae500",
            "presvac ae 500",
            "ae500",
            "ae 500",
        ),
    ),
    Equipment(
        id="cabina-bioseguridad",
        name="Cabina de bioseguridad",
        aliases=(
            "cabina bioseguridad",
            "cabina de bioseguridad",
            "cabina microbiologica",
            "cabina microbiológica",
            "bioseguridad",
        ),
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