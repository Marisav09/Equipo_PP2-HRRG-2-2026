from __future__ import annotations


class AssistantError(Exception):
    """Base exception for controlled assistant failures."""


class VectorstoreNotReadyError(AssistantError):
    """Raised when ChromaDB has no indexed documents."""


class EquipmentScopeError(AssistantError):
    """Raised when a request cannot be safely scoped to one equipment."""


class DocumentIngestionError(AssistantError):
    """Raised when a PDF cannot be safely converted into chunks."""


class LLMUnavailableError(AssistantError):
    """Raised when the local language model cannot produce an answer."""
