from __future__ import annotations

import requests
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.core.exceptions import LLMUnavailableError


class OllamaService:
    def check_health(self) -> None:
        try:
            response = requests.get(
                f"{settings.ollama_base_url}/api/tags",
                timeout=settings.ollama_health_timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMUnavailableError("Ollama no esta respondiendo.") from exc

    def generate(self, prompt: str) -> str:
        self.check_health()
        llm = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0.0,
        )
        response = llm.invoke(prompt)
        answer = str(response.content).strip()
        if not answer:
            raise LLMUnavailableError("El modelo local devolvio una respuesta vacia.")
        return answer
