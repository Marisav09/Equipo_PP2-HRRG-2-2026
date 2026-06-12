from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value is not None else default


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value is not None else default


@dataclass(frozen=True)
class Settings:
    project_name: str = "Asistente IA para Ingenieria Clinica HRRG"
    base_dir: Path = BASE_DIR
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    raw_documents_dir: Path = Path(os.getenv("RAW_DOCUMENTS_DIR", BASE_DIR / "data" / "raw"))
    vectorstore_dir: Path = Path(os.getenv("VECTORSTORE_DIR", BASE_DIR / "data" / "chroma"))
    processed_documents_dir: Path = Path(os.getenv("PROCESSED_DOCUMENTS_DIR", BASE_DIR / "data" / "processed"))
    ingestion_audit_db_path: Path = Path(os.getenv("INGESTION_AUDIT_DB_PATH", BASE_DIR / "data" / "processed" / "ingestion_audit.sqlite3"))
    memory_db_path: Path = Path(os.getenv("MEMORY_DB_PATH", BASE_DIR / "data" / "memory" / "conversation.sqlite3"))
    qr_output_dir: Path = Path(os.getenv("QR_OUTPUT_DIR", BASE_DIR / "static" / "img" / "qr"))
    logs_dir: Path = Path(os.getenv("LOGS_DIR", BASE_DIR / "logs"))
    collection_name: str = os.getenv("COLLECTION_NAME", "manuales_hrrg")
    page_collection_name: str = os.getenv("PAGE_COLLECTION_NAME", "manuales_hrrg_pages")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.2:3b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    reranker_model: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
    reranker_device: str = os.getenv("RERANKER_DEVICE", "cuda")
    reranker_batch_size: int = _get_int("RERANKER_BATCH_SIZE", 4)
    llm_timeout_seconds: int = _get_int("LLM_TIMEOUT_SECONDS", 300)
    ollama_health_timeout_seconds: float = _get_float("OLLAMA_HEALTH_TIMEOUT_SECONDS", 3.0)
    retrieval_k: int = _get_int("RETRIEVAL_K", 4)
    semantic_candidate_k: int = _get_int("SEMANTIC_CANDIDATE_K", 40)
    lexical_candidate_k: int = _get_int("LEXICAL_CANDIDATE_K", 40)
    reranker_candidate_k: int = _get_int("RERANKER_CANDIDATE_K", 60)
    semantic_weight: float = _get_float("SEMANTIC_WEIGHT", 0.30)
    lexical_weight: float = _get_float("LEXICAL_WEIGHT", 0.20)
    reranker_weight: float = _get_float("RERANKER_WEIGHT", 0.50)
    operator_context_k: int = _get_int("OPERATOR_CONTEXT_K", 4)
    operator_adjacent_pages_max: int = _get_int("OPERATOR_ADJACENT_PAGES_MAX", 2)
    adjacent_page_relative_threshold: float = _get_float("ADJACENT_PAGE_RELATIVE_THRESHOLD", 0.70)
    technician_page_context_k: int = _get_int("TECHNICIAN_PAGE_CONTEXT_K", 1)
    technician_context_max_chars: int = _get_int("TECHNICIAN_CONTEXT_MAX_CHARS", 14000)
    chunk_size: int = _get_int("CHUNK_SIZE", 1000)
    chunk_overlap: int = _get_int("CHUNK_OVERLAP", 180)
    operator_chunk_size: int = _get_int("OPERATOR_CHUNK_SIZE", 750)
    operator_chunk_overlap: int = _get_int("OPERATOR_CHUNK_OVERLAP", 120)
    parent_embedding_max_chars: int = _get_int("PARENT_EMBEDDING_MAX_CHARS", 3500)
    embedding_batch_size: int = _get_int("EMBEDDING_BATCH_SIZE", 4)
    enable_ocr: bool = _get_bool("ENABLE_OCR", False)
    technical_user_password: str = os.getenv("TECHNICAL_USER_PASSWORD", "tecnico-hrrg")
    operator_user_password: str = os.getenv("OPERATOR_USER_PASSWORD", "operador-hrrg")

    def ensure_directories(self) -> None:
        for directory in (
            self.raw_documents_dir,
            self.vectorstore_dir,
            self.processed_documents_dir,
            self.ingestion_audit_db_path.parent,
            self.memory_db_path.parent,
            self.qr_output_dir,
            self.logs_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
