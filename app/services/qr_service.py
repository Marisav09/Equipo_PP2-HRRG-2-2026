from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import qrcode

from app.core.config import settings
from app.core.equipment_catalog import EQUIPMENT_CATALOG, Equipment, find_equipment_by_id


@dataclass(frozen=True)
class QrResult:
    equipment_id: str
    equipment_name: str
    url: str
    output_path: Path

    def to_dict(self) -> dict[str, str]:
        return {
            "equipment_id": self.equipment_id,
            "equipment_name": self.equipment_name,
            "url": self.url,
            "output_path": str(self.output_path),
        }


class QrService:
    def __init__(self, output_dir: Path | None = None) -> None:
        self.output_dir = output_dir or settings.qr_output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_for_equipment(self, equipment_id: str, base_url: str) -> QrResult:
        equipment = find_equipment_by_id(equipment_id)
        if not equipment:
            raise ValueError(f"Equipo no encontrado en catalogo: {equipment_id}")
        return self._generate(equipment, base_url)

    def generate_all(self, base_url: str) -> list[QrResult]:
        return [self._generate(equipment, base_url) for equipment in EQUIPMENT_CATALOG]

    def _generate(self, equipment: Equipment, base_url: str) -> QrResult:
        clean_base_url = base_url.rstrip("/")
        url = f"{clean_base_url}/equipo/{equipment.id}"
        output_path = self.output_dir / f"qr_{equipment.id}.png"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        image = qr.make_image(fill_color="#17212b", back_color="white")
        image.save(output_path)

        return QrResult(
            equipment_id=equipment.id,
            equipment_name=equipment.name,
            url=url,
            output_path=output_path,
        )
