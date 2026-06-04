from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz
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


@dataclass(frozen=True)
class QrLabel:
    equipment_id: str
    equipment_name: str
    url: str
    image_path: Path
    sector: str = ""


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

    def label_for_equipment(self, equipment_id: str, base_url: str) -> QrLabel:
        result = self.generate_for_equipment(equipment_id, base_url)
        return QrLabel(
            equipment_id=result.equipment_id,
            equipment_name=result.equipment_name,
            url=result.url,
            image_path=result.output_path,
        )

    def labels_for_all(self, base_url: str) -> list[QrLabel]:
        return [
            QrLabel(
                equipment_id=result.equipment_id,
                equipment_name=result.equipment_name,
                url=result.url,
                image_path=result.output_path,
            )
            for result in self.generate_all(base_url)
        ]

    def generate_all_pdf(self, base_url: str) -> Path:
        labels = self.labels_for_all(base_url)
        pdf_path = self.output_dir / "qr_equipos_hrrg.pdf"
        if pdf_path.exists():
            pdf_path.unlink()

        page_width = 595
        page_height = 842
        margin = 34
        gap = 14
        columns = 2
        rows = 4
        label_width = (page_width - (margin * 2) - gap) / columns
        label_height = (page_height - (margin * 2) - (gap * (rows - 1))) / rows
        qr_size = 104

        doc = fitz.open()
        page = None
        for index, label in enumerate(labels):
            slot = index % (columns * rows)
            if slot == 0:
                page = doc.new_page(width=page_width, height=page_height)

            assert page is not None
            col = slot % columns
            row = slot // columns
            x = margin + col * (label_width + gap)
            y = margin + row * (label_height + gap)
            rect = fitz.Rect(x, y, x + label_width, y + label_height)

            page.draw_rect(rect, color=(0.78, 0.84, 0.90), width=0.7)
            qr_rect = fitz.Rect(x + 12, y + 18, x + 12 + qr_size, y + 18 + qr_size)
            page.insert_image(qr_rect, filename=str(label.image_path))

            text_x = x + 128
            page.insert_textbox(
                fitz.Rect(text_x, y + 18, x + label_width - 10, y + 58),
                label.equipment_name,
                fontsize=10.5,
                fontname="helv",
                color=(0.06, 0.13, 0.22),
            )
            page.insert_textbox(
                fitz.Rect(text_x, y + 62, x + label_width - 10, y + 84),
                f"ID: {label.equipment_id}",
                fontsize=8.5,
                fontname="helv",
                color=(0.22, 0.28, 0.36),
            )
            if label.sector:
                page.insert_textbox(
                    fitz.Rect(text_x, y + 86, x + label_width - 10, y + 108),
                    f"Sector: {label.sector}",
                    fontsize=8.5,
                    fontname="helv",
                    color=(0.22, 0.28, 0.36),
                )
            page.insert_textbox(
                fitz.Rect(x + 12, y + label_height - 30, x + label_width - 12, y + label_height - 10),
                label.url,
                fontsize=6.8,
                fontname="helv",
                color=(0.35, 0.42, 0.50),
            )

        doc.save(pdf_path, deflate=True, garbage=4)
        doc.close()
        return pdf_path

    def _generate(self, equipment: Equipment, base_url: str) -> QrResult:
        clean_base_url = base_url.rstrip("/")
        url = f"{clean_base_url}/qr/{equipment.id}"
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
