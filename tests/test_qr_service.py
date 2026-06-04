from __future__ import annotations

import pytest

from app.services.qr_service import QrService


def test_generate_qr_for_equipment(tmp_path):
    service = QrService(output_dir=tmp_path)

    result = service.generate_for_equipment("sterrad-100", "http://localhost:5000/")

    assert result.equipment_id == "sterrad-100"
    assert result.url == "http://localhost:5000/qr/sterrad-100"
    assert result.output_path.exists()
    assert result.output_path.name == "qr_sterrad-100.png"


def test_generate_qr_rejects_unknown_equipment(tmp_path):
    service = QrService(output_dir=tmp_path)

    with pytest.raises(ValueError):
        service.generate_for_equipment("equipo-inexistente", "http://localhost:5000")
