from __future__ import annotations

import re
import unicodedata
from pathlib import Path


GENERAL_EQUIPMENT_LABEL = "Busqueda general"
UNCLASSIFIED_EQUIPMENT_LABEL = "Sin clasificar"


# IMPORTANTE:
# El orden importa. Las reglas más específicas deben ir antes que las generales.
# Evitar alias de marca solos cuando puedan capturar equipos distintos.
EQUIPMENT_ALIASES: dict[str, tuple[str, ...]] = {
    "Bomba de infusion": (
        "bomba_de_infusion",
        "bomba de infusion",
        "bomba infusion",
        "infusomat",
        "infusomat space",
    ),

    "Bilirrubinometro Drager JM-105": (
        "bilirrubinometro_drager_jm105",
        "bilirrubinometro",
        "bilirrubinómetro",
        "drager jm 105",
        "drager jm-105",
        "drager_jm105",
        "drager_jm_105",
        "dräger jm 105",
        "dräger jm-105",
        "draeger jm 105",
        "draeger jm-105",
        "jm-105",
        "jm 105",
        "jm105",
        "jm_105",
        "checklist bilirrubinometro",
        "manual tecnico bilirrubinometro",
        "manual de usuario bilirrubinometro",
        "material educativo bilirrubinometro",
    ),

    "Desfibrilador Mindray BeneHeart D3": (
        "desfibrilador_mindray_beneheart",
        "desfibrilador",
        "desfibrilador mindray",
        "mindray beneheart",
        "beneheart",
        "beneheart d3",
        "beneheart d2",
        "beneheart d3 d2",
        "d3 d2",
        "d3d2",
        "defib",
        "new defib",
        "monitor beneheart",
        "desfibrilador monitor beneheart",
        "manual de servicio desfibrilador monitor beneheart",
    ),

    "Maquina de dialisis Fresenius 4008": (
        "fresenius_4008",
        "fresenius",
        "fressenius",
        "fresenius 4008",
        "fresenius 4008s",
        "fresenius 4008b",
        "4008",
        "4008s",
        "4008b",
        "dialisis",
        "diálisis",
        "hemodialisis",
        "hemodiálisis",
        "maquina de dialisis",
        "máquina de diálisis",
        "service manual fresenius",
        "fresenius service manual",
    ),

    "Monitor multiparametrico": (
        "monitor_multiparametrico",
        "monitor multiparametrico",
        "monitor multiparámetro",
        "monitor multiparametro",
        "multiparametrico",
        "multiparamétrico",
        "multiparametro",
        "multiparámetro",
        "epm series",
        "imec",
        "pm-9000",
        "pm 9000",
        "compact monitor",
    ),

    "Respirador Drager VN500": (
        "drager_vn500",
        "drager vn500",
        "draeger vn500",
        "dräger vn500",
        "draguer respirador",
        "respirador drager vn500",
        "respirador draeger vn500",
        "vn500",
        "v500",
        "ps500",
        "ps 500",
        "gs500",
        "gs 500",
        "babyflow",
        "baby flow",
        "babylog",
        "baby log",
        "evita v300",
        "volume guarantee",
        "volumeguarantee",
        "recarga soft",
        "entrar en servicio",
        "training gs500",
        "training ps500",
    ),

    "Ventilador Neumovent GraphNet": (
        "ventilador_neumovent",
        "neumovent",
        "graphnet",
        "graphnet neo",
        "advance ts neo",
        "nv graph",
        "nv-graph",
        "tecme graphnet",
        "manualtecnico bebe",
        "respimeradores",
    ),

    "Ventilador Maquet Servo-i": (
        "ventilador_maquet_servo_i",
        "maquet",
        "servo i",
        "servo-i",
        "maquet servo",
        "maquet servo i",
    ),

    "Ventilador Engstrom": (
        "ventilador_engstrom",
        "engstrom",
        "engström",
        "engstrom carestation",
        "carestation",
        "datex ohmeda",
        "datex-ohmeda",
        "ge engstrom",
        "ventilacion no invasiva",
        "ventilación no invasiva",
    ),

    "Ventilador Crossvent": (
        "ventilador_crossvent",
        "crossvent",
        "crossvent 2i",
        "crossvent 3",
        "crossvent 4",
        "biomed devices",
        "globe trotter",
        "gt5400",
    ),

    "Ventilador Newport HT-70": (
        "ventilador_newport_ht70",
        "newport",
        "ht-70",
        "ht 70",
        "newport ht-70",
    ),

    "Ventilador Leistung LUFT3": (
        "ventilador_leistung_luft3",
        "leistung",
        "luft3",
        "luft3apn",
        "l3apn",
        "nivel 3 terapia",
        "terapia fallas frecuentes",
        "fallas frecuentes",
        "fuga",
        "presion",
        "presión",
        "flujo",
    ),

    "Incubadora Medix": (
        "incubadora_medix",
        "incubadora",
        "medix",
        "tr200",
        "tr 200",
        "tr306",
        "tr 306",
        "natal care",
        "natalcare",
    ),

    "Electrobisturi": (
        "electrobisturi",
        "electrobisturí",
        "esu",
        "kairos",
        "minicomp",
        "leep",
        "valleylab",
        "force fx",
        "force fx-c",
        "force fx-8c",
        "electrosurgical generator",
    ),

    "Esterilizadora Sterrad 100": (
        "sterrad_100",
        "sterrad",
        "sterrad 100",
        "sterrad 100s",
        "esterilizadora",
        "esterilizador",
        "sterilization system",
    ),

    "Procesador Leica TP1020": (
        "leica_tp1020",
        "leica tp1020",
        "leica tp 1020",
        "tp1020",
        "tp 1020",
        "tp-1020",
        "procesador de tejidos",
        "procesador de tejido",
        "tissue processor",
    ),

    "Microtomo Leica RM2125": (
        "leica_rm2125",
        "leica rm2125",
        "leica rm 2125",
        "rm2125",
        "rm 2125",
        "rm2125 rts",
        "microtomo",
        "micrótomo",
        "microtomo de rotacion",
        "micrótomo de rotación",
    ),

    "Cama electronica": (
        "cama_electronica",
        "cama",
        "cama electronica",
        "cama electrónica",
        "linet",
        "eleganza",
        "pardo",
        "hitech",
        "komplet",
    ),

    "Agitador Presvac AE-500": (
        "agitador_presvac_ae500",
        "agitador",
        "presvac",
        "ae-500",
        "ae500",
    ),

    "Dinan AF-500": (
        "dinan_af500",
        "dinan",
        "af-500",
        "af500",
        "dr console",
        "sm500",
    ),

    "Cabina de bioseguridad": (
        "cabina_bioseguridad",
        "cabina",
        "bioseguridad",
        "cabina microbiologica",
        "cabina microbiológica",
        "euroclone",
        "safemate",
    ),

    "Rodantes MAC GMM": (
        "rodantes_mac_gmm",
        "rodantes",
        "mac gmm",
        "hd-67",
        "hd 67",
        "equipos rodantes",
    ),

    "TP 100": (
        "tp_100",
        "tp 100",
        "tp-100",
        "tp-80",
        "fg-tp-80",
        "plano electrico tp",
        "plano eléctrico tp",
    ),

    "Pimax": (
        "pimax",
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

    if normalized == normalize_equipment_text(UNCLASSIFIED_EQUIPMENT_LABEL):
        return UNCLASSIFIED_EQUIPMENT_LABEL

    for canonical, aliases in EQUIPMENT_ALIASES.items():
        searchable = (canonical, *aliases)

        for alias in searchable:
            normalized_alias = normalize_equipment_text(alias)

            if not normalized_alias:
                continue

            if normalized == normalized_alias:
                return canonical

            if normalized.startswith(normalized_alias + " "):
                return canonical

            if normalized_alias in normalized:
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

        for alias in searchable:
            normalized_alias = normalize_equipment_text(alias)

            if normalized_alias and normalized_alias in normalized_text:
                return canonical

    return None