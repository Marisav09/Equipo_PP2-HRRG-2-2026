from __future__ import annotations

from app.core.equipment_catalog import EQUIPMENT_CATALOG, Equipment, find_equipment_by_id


class EquipmentService:
    def list_equipments(self) -> list[dict[str, str]]:
        return [{"id": item.id, "name": item.name} for item in EQUIPMENT_CATALOG]

    def get_by_id(self, equipment_id: str) -> Equipment | None:
        return find_equipment_by_id(equipment_id)
