class AssistantError(Exception):
    """Base para errores controlados del asistente."""


class VectorstoreNotReadyError(AssistantError):
    """La base vectorial no existe o no tiene documentos cargados."""


class LLMUnavailableError(AssistantError):
    """Ollama o el modelo local no estan disponibles."""


class DocumentIngestionError(AssistantError):
    """Un documento no pudo procesarse correctamente."""
