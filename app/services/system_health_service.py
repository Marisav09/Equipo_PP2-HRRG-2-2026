from __future__ import annotations

from typing import Any, Callable

import requests

from app.core.config import settings
from app.services.ingestion_audit_service import IngestionAuditService
from app.services.vectorstore_service import VectorstoreService


class SystemHealthService:
    def __init__(
        self,
        vectorstore: VectorstoreService | None = None,
        audit_service: IngestionAuditService | None = None,
        http_get: Callable[..., Any] | None = None,
    ) -> None:
        self.vectorstore = vectorstore or VectorstoreService()
        self.audit_service = audit_service or IngestionAuditService()
        self.http_get = http_get or requests.get

    def check(self) -> dict[str, Any]:
        ollama = self._check_ollama()
        vectorstore = self._check_vectorstore()
        ingestion = self._check_ingestion_audit()

        components = {
            "ollama": ollama,
            "vectorstore": vectorstore,
            "ingestion_audit": ingestion,
        }
        overall_ok = all(component["ok"] for component in components.values())

        return {
            "ok": overall_ok,
            "status": "ok" if overall_ok else "degraded",
            "components": components,
        }

    def _check_ollama(self) -> dict[str, Any]:
        try:
            response = self.http_get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=settings.ollama_health_timeout_seconds,
            )
            response.raise_for_status()
            payload = response.json()
            models = [model.get("name") or model.get("model") for model in payload.get("models", [])]
            required_models = [settings.llm_model, settings.embedding_model]
            missing_models = [
                model
                for model in required_models
                if model not in models and f"{model}:latest" not in models
            ]
            return {
                "ok": not missing_models,
                "message": "Ollama disponible." if not missing_models else "Faltan modelos locales.",
                "models": models,
                "required_models": required_models,
                "missing_models": missing_models,
            }
        except Exception as exc:
            return {
                "ok": False,
                "message": f"Ollama no responde: {exc}",
                "models": [],
                "required_models": [settings.llm_model, settings.embedding_model],
                "missing_models": [settings.llm_model, settings.embedding_model],
            }

    def _check_vectorstore(self) -> dict[str, Any]:
        try:
            store = self.vectorstore.get_store()
            count = store._collection.count()
            return {
                "ok": count > 0,
                "message": "ChromaDB tiene documentos indexados." if count > 0 else "ChromaDB no tiene documentos.",
                "document_count": count,
            }
        except Exception as exc:
            return {
                "ok": False,
                "message": f"No se pudo consultar ChromaDB: {exc}",
                "document_count": 0,
            }

    def _check_ingestion_audit(self) -> dict[str, Any]:
        try:
            documents = self.audit_service.list_latest()
            active = [item for item in documents if item["status"] in {"indexed", "unchanged"}]
            return {
                "ok": bool(active),
                "message": "Existe manifiesto de ingesta." if active else "No hay documentos activos en auditoria.",
                "document_count": len(documents),
                "active_document_count": len(active),
            }
        except Exception as exc:
            return {
                "ok": False,
                "message": f"No se pudo consultar auditoria de ingesta: {exc}",
                "document_count": 0,
                "active_document_count": 0,
            }
