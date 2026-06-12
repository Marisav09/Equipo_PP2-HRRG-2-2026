from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.logging_config import configure_logging
from app.services.ingestion_service import IngestionService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingesta documentos Markdown procesados en ChromaDB."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reindexa aunque el hash del Markdown no haya cambiado.",
    )
    parser.add_argument(
        "--rebuild-parent-child",
        action="store_true",
        help=(
            "Reconstruye el indice con chunks hijos para busqueda y paginas padre completas "
            "para expansion de contexto."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging()

    force = args.force or args.rebuild_parent_child
    result = IngestionService().ingest_directory(force=force)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
