from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from pathlib import Path


# Si ya existe el respaldo de originales únicos, usamos ese como fuente.
# Si no existe, usamos data/raw.
SOURCE_DIR = Path("data/raw_original_unicos") if Path("data/raw_original_unicos").exists() else Path("data/raw")
DEST_DIR = Path("data/raw_normalized")
REPORT_PATH = Path("data/processed/reporte_normalizacion_nombres_pdf.csv")


# IMPORTANTE:
# El orden importa. Las reglas más específicas deben ir antes que las generales.
# Evitar alias demasiado genéricos como "drager", "mindray", "monitor" cuando puedan
# capturar manuales de otros equipos de la misma marca o familia.
EQUIPMENT_RULES: list[tuple[str, tuple[str, ...]]] = [
    (
        "bilirrubinometro_drager_jm105",
        (
            "bilirrubinometro",
            "bilirrubinómetro",
            "jm105",
            "jm_105",
            "jm-105",
            "jm 105",
            "drager_jm_105",
            "dräger_jm_105",
            "draeger_jm_105",
            "checklist_bilirrubinometro",
            "manual_de_usuario_bilirrubinometro",
            "manual_tecnico_bilirrubinometro",
            "material_educativo_bilirrubinometro",
            "material educativo bilirrubinometro",
            "material educativo bilirrubinómetro",
        ),
    ),
    (
        "desfibrilador_mindray_beneheart",
        (
            "desfibrilador",
            "beneheart",
            "beneheart_d3",
            "beneheart_d2",
            "beneheart d3",
            "beneheart d2",
            "d3_d2",
            "d3d2",
            "defib",
            "new_defib",
            "monitor_beneheart",
            "monitor beneheart",
            "manual_de_servicio_desfibrilador_monitor_beneheart",
            "manual de servicio desfibrilador monitor beneheart",
        ),
    ),
    (
        "drager_vn500",
        (
            "vn500",
            "v500",
            "ps500",
            "ps_500",
            "ps-500",
            "gs500",
            "gs_500",
            "gs-500",
            "babyflow",
            "baby_flow",
            "baby flow",
            "babylog",
            "baby_log",
            "baby log",
            "evita",
            "draguer_respirador",
            "respirador_draeger_vn500",
            "respirador_drager_vn500",
            "draeger_vn500",
            "drager_vn500",
            "manual_usuario_vn500",
            "manual usuario vn500",
            "training_gs500",
            "training gs500",
            "training_ps500",
            "training ps500",
            "cc_other_br",
            "9066227",
            "9066343",
            "9066364",
            "9066465",
            "volume_guarantee",
            "volumeguarantee",
            "volume guarantee",
            "recarga_soft",
            "recarga soft",
            "entrar_en_servicio",
            "entrar en servicio",
            "abreviaturas_y_simbolos_evita",
            "abreviaturas y simbolos evita",
            "pdf1805_ad_babylog_vn500",
        ),
    ),
    (
        "ventilador_leistung_luft3",
        (
            "leistung",
            "luft3",
            "luft3apn",
            "l3apn",
            "l3apnmu",
            "nivel_3_terapia",
            "nivel 3 terapia",
            "terapia_fallas_frecuentes",
            "terapia fallas frecuentes",
            "fallas_frecuentes",
            "fallas frecuentes",
            "fuga",
            "presion",
            "presión",
            "flujo",
        ),
    ),
    (
        "ventilador_neumovent",
        (
            "neumovent",
            "graphnet",
            "nv_graph",
            "nv-graph",
            "nv graph",
            "tecme",
            "manualtecnico_bebe",
            "manualtecnico bebe",
            "advance_ts_neo",
            "advance ts neo",
            "neo_ts",
            "neo ts",
            "respimeradores",
            "calibracion_neumovent",
            "calibración_neumovent",
            "manual_de_calibracion_neumovent",
            "manual de calibracion neumovent",
        ),
    ),
    (
        "ventilador_maquet_servo_i",
        (
            "maquet",
            "servo_i",
            "servo-i",
            "servo i",
        ),
    ),
    (
        "ventilador_engstrom",
        (
            "engstrom",
            "engström",
            "carestation",
            "datex_ohmeda",
            "datex-ohmeda",
            "datex ohmeda",
            "guia_rapida",
            "guía rápida",
            "guia rapida",
            "ventilacion_no_invasiva",
            "ventilación no invasiva",
            "ventilacion no invasiva",
            "manual_service_engstrom",
            "manual_tecnico_ventilador_engstrom",
            "manual_tecnico_ventilador_ge_engstrom",
        ),
    ),
    (
        "ventilador_crossvent",
        (
            "crossvent",
            "biomed",
            "globe_trotter",
            "globe trotter",
            "gt5400",
        ),
    ),
    (
        "ventilador_newport_ht70",
        (
            "newport",
            "ht_70",
            "ht-70",
            "ht 70",
        ),
    ),
    (
        "electrobisturi",
        (
            "electrobisturi",
            "electrobisturí",
            "kairos",
            "minicomp",
            "leep",
            "valleylab",
            "force_fx",
            "force_fx_c",
            "force_fx_8c",
            "force fx",
            "force fx-c",
            "force fx-8c",
            "esu",
            "electrosurgical",
        ),
    ),
    (
        "monitor_multiparametrico",
        (
            "multiparametrico",
            "multiparamétrico",
            "multiparametro",
            "multiparámetro",
            "epm",
            "imec",
            "pm_9000",
            "pm-9000",
            "pm 9000",
            "compact_monitor",
            "compact monitor",
            "monitor_service_manual",
            "monitor service manual",
        ),
    ),
    (
        "incubadora_medix",
        (
            "incubadora",
            "medix",
            "tr200",
            "tr_200",
            "tr-200",
            "tr306",
            "tr_306",
            "tr-306",
            "natal_care",
            "natal care",
        ),
    ),
    (
        "cama_electronica",
        (
            "cama",
            "linet",
            "eleganza",
            "pardo",
            "hitech",
            "hi_tech",
            "hi-tech",
            "komplet",
        ),
    ),
    (
        "leica_tp1020",
        (
            "tp1020",
            "tp_1020",
            "tp-1020",
            "tp 1020",
            "procesador_de_tejidos",
            "procesador de tejidos",
            "leica_tp1020",
            "leica tp1020",
            "leica_tp_1020",
            "leica tp 1020",
        ),
    ),
    (
        "leica_rm2125",
        (
            "rm2125",
            "rm_2125",
            "rm-2125",
            "rm 2125",
            "microtomo",
            "micrótomo",
            "microtomo_de_rotacion",
            "micrótomo de rotación",
            "microtomo de rotacion",
            "leica_rm2125",
            "leica rm2125",
            "leica_rm_2125",
            "leica rm 2125",
        ),
    ),
    (
        "sterrad_100",
        (
            "sterrad",
            "sterrad_100",
            "sterrad 100",
            "sterrad_100s",
            "sterrad 100s",
        ),
    ),
    (
        "fresenius_4008",
        (
            "fresenius",
            "fressenius",
            "4008",
            "4008s",
            "4008b",
            "dialisis",
            "diálisis",
            "hemodialisis",
            "hemodiálisis",
            "service_manual",
            "service manual",
        ),
    ),
    (
        "agitador_presvac_ae500",
        (
            "agitador",
            "presvac",
            "ae500",
            "ae_500",
            "ae-500",
        ),
    ),
    (
        "dinan_af500",
        (
            "dinan",
            "af500",
            "af_500",
            "af-500",
            "sm500",
            "sm_500",
            "sm-500",
            "dr_console",
            "dr console",
            "mtm_af_500",
            "mu_af_500",
            "mu_dr_console",
        ),
    ),
    (
        "cabina_bioseguridad",
        (
            "cabina",
            "bioseguridad",
            "euroclone",
            "safemate",
            "microbiologica",
            "microbiológica",
        ),
    ),
    (
        "rodantes_mac_gmm",
        (
            "rodantes",
            "mac_gmm",
            "mac gmm",
            "hd67",
            "hd_67",
            "hd-67",
        ),
    ),
    (
        "tp_100",
        (
            "tp100",
            "tp_100",
            "tp-100",
            "tp80",
            "tp_80",
            "tp-80",
            "fg_tp",
            "fg-tp",
            "plano_electrico_tp",
            "plano eléctrico tp",
            "plano electrico tp",
        ),
    ),
    (
        "pimax",
        (
            "pimax",
        ),
    ),
]


def normalize_text(value: str) -> str:
    without_accents = unicodedata.normalize("NFKD", value)
    ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    ascii_text = re.sub(r"_+", "_", ascii_text).strip("_")
    return ascii_text


def infer_prefix(normalized_stem: str) -> str:
    for prefix, aliases in EQUIPMENT_RULES:
        for alias in aliases:
            normalized_alias = normalize_text(alias)
            if normalized_alias and normalized_alias in normalized_stem:
                return prefix

    return "sin_clasificar"


def remove_existing_known_prefix(normalized_stem: str) -> str:
    """
    Si el archivo ya tenía un prefijo generado por una ejecución anterior,
    se lo elimina para evitar nombres del tipo:
    bilirrubinometro_drager_jm105_drager_vn500_checklist...
    """
    known_prefixes = [prefix for prefix, _ in EQUIPMENT_RULES]
    known_prefixes.append("sin_clasificar")

    for prefix in sorted(known_prefixes, key=len, reverse=True):
        if normalized_stem == prefix:
            return normalized_stem

        if normalized_stem.startswith(prefix + "_"):
            return normalized_stem[len(prefix) + 1 :]

    return normalized_stem


def build_filename(original_name: str, used_names: set[str]) -> tuple[str, str]:
    stem = Path(original_name).stem
    normalized_stem = normalize_text(stem)

    # Evita arrastrar un prefijo incorrecto de ejecuciones previas.
    stem_without_old_prefix = remove_existing_known_prefix(normalized_stem)

    prefix = infer_prefix(stem_without_old_prefix)
    base = f"{prefix}_{stem_without_old_prefix}"

    candidate = f"{base}.pdf"
    counter = 2

    while candidate in used_names:
        candidate = f"{base}_{counter}.pdf"
        counter += 1

    used_names.add(candidate)
    return candidate, prefix


def main() -> None:
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"No existe la carpeta de origen: {SOURCE_DIR}")

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    for old_file in DEST_DIR.glob("*.pdf"):
        old_file.unlink()

    pdfs = sorted(SOURCE_DIR.glob("*.pdf"), key=lambda p: p.name.lower())
    used_names: set[str] = set()
    rows: list[dict[str, str]] = []

    for pdf in pdfs:
        new_name, equipment_prefix = build_filename(pdf.name, used_names)
        destination = DEST_DIR / new_name
        shutil.copy2(pdf, destination)

        rows.append(
            {
                "original_name": pdf.name,
                "normalized_name": new_name,
                "equipment_prefix": equipment_prefix,
                "source_path": str(pdf),
                "destination_path": str(destination),
            }
        )

    with REPORT_PATH.open("w", newline="", encoding="utf-8") as report_file:
        writer = csv.DictWriter(
            report_file,
            fieldnames=[
                "original_name",
                "normalized_name",
                "equipment_prefix",
                "source_path",
                "destination_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Fuente: {SOURCE_DIR}")
    print(f"PDFs normalizados: {len(rows)}")
    print(f"Carpeta destino: {DEST_DIR}")
    print(f"Reporte: {REPORT_PATH}")


if __name__ == "__main__":
    main()