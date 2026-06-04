from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.qr_service import QrService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera codigos QR de acceso por equipo.")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:5000",
        help="URL base que quedara codificada en el QR.",
    )
    parser.add_argument(
        "--equipment-id",
        help="ID de equipo especifico. Si se omite, genera QR para todo el catalogo.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = QrService()
    if args.equipment_id:
        results = [service.generate_for_equipment(args.equipment_id, args.base_url)]
    else:
        results = service.generate_all(args.base_url)

    print(json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
