from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    return float(value)


@dataclass(frozen=True)
class Settings:
    project_name: str = "Asistente IA para Ingenieria Clinica HRRG"
    base_dir: Path = BASE_DIR
    raw_documents_dir: Path = Path(os.getenv("RAW_DOCUMENTS_DIR", BASE_DIR / "data" / "raw"))
    vectorstore_dir: Path = Path(os.getenv("VECTORSTORE_DIR", BASE_DIR / "data" / "chroma"))
    audit_db_path: Path = Path(os.getenv("AUDIT_DB_PATH", BASE_DIR / "data" / "audit" / "queries.sqlite3"))
    tickets_db_path: Path = Path(os.getenv("TICKETS_DB_PATH", BASE_DIR / "data" / "tickets" / "tickets.sqlite3"))
    logs_dir: Path = Path(os.getenv("LOGS_DIR", BASE_DIR / "logs"))
    collection_name: str = os.getenv("COLLECTION_NAME", "manuales_hrrg")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.2:3b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chunk_size: int = _get_int("CHUNK_SIZE", 1000)
    chunk_overlap: int = _get_int("CHUNK_OVERLAP", 180)
    retrieval_k: int = _get_int("RETRIEVAL_K", 4)
    embedding_batch_size: int = _get_int("EMBEDDING_BATCH_SIZE", 4)
    llm_timeout_seconds: int = _get_int("LLM_TIMEOUT_SECONDS", 300)
    memory_window_messages: int = _get_int("MEMORY_WINDOW_MESSAGES", 6)
    ollama_health_timeout_seconds: float = _get_float("OLLAMA_HEALTH_TIMEOUT_SECONDS", 3.0)
    enable_ocr: bool = _get_bool("ENABLE_OCR", False)
    technical_user_password: str = os.getenv("TECHNICAL_USER_PASSWORD", "tecnico-hrrg")
    admin_user_password: str = os.getenv("ADMIN_USER_PASSWORD", "admin-hrrg")

    def ensure_directories(self) -> None:
        for directory in (
            self.raw_documents_dir,
            self.vectorstore_dir,
            self.audit_db_path.parent,
            self.tickets_db_path.parent,
            self.logs_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
