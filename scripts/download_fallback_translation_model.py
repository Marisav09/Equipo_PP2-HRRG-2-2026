from __future__ import annotations

import sys
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings


def main() -> None:
    model_name = settings.fallback_translation_model
    print(f"Descargando modelo de traduccion fallback: {model_name}")
    AutoTokenizer.from_pretrained(model_name)
    AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("Modelo de traduccion fallback disponible localmente.")


if __name__ == "__main__":
    main()
