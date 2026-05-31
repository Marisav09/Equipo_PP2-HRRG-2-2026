from __future__ import annotations

from functools import lru_cache

from app.core.config import settings
from app.core.equipment_catalog import (
    EQUIPMENT_CATALOG,
    Equipment,
    find_equipment_by_id,
    infer_equipment_from_path,
)


EQUIPMENT_PRESENTATION: dict[str, dict[str, str]] = {
    "draeger-vn500": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-maquet-servo-i": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-neumovent": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-crossvent": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-engstrom": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-leistung-luft3": {"category": "Ventiladores", "icon": "lungs"},
    "ventilador-newport-ht70": {"category": "Ventiladores", "icon": "lungs"},
    "sterrad-100": {"category": "Esterilizacion", "icon": "sparkles"},
    "fresenius-4008": {"category": "Dialisis", "icon": "activity"},
    "leica-tp1020": {"category": "Laboratorio", "icon": "microscope"},
    "leica-rm2125": {"category": "Laboratorio", "icon": "microscope"},
    "bilirrubinometro-draeger-jm105": {"category": "Diagnostico", "icon": "stethoscope"},
    "desfibrilador-mindray-beneheart": {"category": "Emergencia", "icon": "zap"},
    "electrobisturi": {"category": "Quirofano", "icon": "zap"},
    "monitor-multiparametrico": {"category": "Monitoreo", "icon": "activity"},
    "cama-electronica": {"category": "Internacion", "icon": "bed"},
    "incubadora-medix-tr306": {"category": "Neonatologia", "icon": "baby"},
    "cabina-bioseguridad": {"category": "Laboratorio", "icon": "shield"},
    "agitador-presvac-ae500": {"category": "Laboratorio", "icon": "flask"},
    "dinan-af500": {"category": "Equipamiento clinico", "icon": "settings"},
    "tp-100": {"category": "Equipamiento clinico", "icon": "settings"},
    "rodantes-mac-gmm": {"category": "Imagenes medicas", "icon": "scan"},
}


CATEGORY_ORDER = (
    "Ventiladores",
    "Esterilizacion",
    "Dialisis",
    "Laboratorio",
    "Diagnostico",
    "Monitoreo",
    "Emergencia",
    "Quirofano",
    "Neonatologia",
    "Internacion",
    "Imagenes medicas",
    "Equipamiento clinico",
)


@lru_cache(maxsize=1)
def _manual_counts_by_equipment() -> dict[str, int]:
    counts = {item.id: 0 for item in EQUIPMENT_CATALOG}
    raw_dir = settings.raw_documents_dir

    if not raw_dir.exists():
        return counts

    for pdf_path in raw_dir.rglob("*.pdf"):
        equipment = infer_equipment_from_path(pdf_path, raw_dir)
        if equipment:
            counts[equipment.id] = counts.get(equipment.id, 0) + 1

    return counts


class EquipmentService:
    def list_equipments(self) -> list[dict[str, str | int]]:
        counts = _manual_counts_by_equipment()
        order = {category: index for index, category in enumerate(CATEGORY_ORDER)}
        equipments: list[dict[str, str | int]] = []

        for item in EQUIPMENT_CATALOG:
            presentation = EQUIPMENT_PRESENTATION.get(
                item.id,
                {"category": "Equipamiento clinico", "icon": "settings"},
            )
            equipments.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "category": presentation["category"],
                    "icon": presentation["icon"],
                    "manual_count": counts.get(item.id, 0),
                    "search_text": " ".join((item.name, item.id, *item.aliases)),
                }
            )

        return sorted(
            equipments,
            key=lambda item: (order.get(str(item["category"]), 999), str(item["name"]).lower()),
        )

    def get_by_id(self, equipment_id: str) -> Equipment | None:
        return find_equipment_by_id(equipment_id)