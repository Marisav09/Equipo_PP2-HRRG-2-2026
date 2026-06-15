from __future__ import annotations

import concurrent.futures
import logging
import re
import threading
from functools import lru_cache

from app.core.config import settings


logger = logging.getLogger(__name__)


class FallbackTranslationService:
    """Translate predominantly English fallback extracts without depending on Ollama."""

    _ENGLISH_MARKERS = {
        "and",
        "are",
        "before",
        "button",
        "check",
        "device",
        "display",
        "do",
        "equipment",
        "error",
        "for",
        "from",
        "has",
        "if",
        "is",
        "manual",
        "must",
        "not",
        "of",
        "on",
        "or",
        "press",
        "remove",
        "replace",
        "service",
        "system",
        "the",
        "this",
        "to",
        "turn",
        "unit",
        "warning",
        "when",
        "with",
    }
    _SPANISH_MARKERS = {
        "antes",
        "con",
        "cuando",
        "de",
        "del",
        "debe",
        "dispositivo",
        "el",
        "equipo",
        "error",
        "esta",
        "la",
        "manual",
        "no",
        "para",
        "por",
        "presione",
        "que",
        "servicio",
        "sistema",
        "una",
        "unidad",
        "y",
    }

    def __init__(self) -> None:
        self._translator = None
        self._load_lock = threading.Lock()
        self._translation_unavailable = False

    def translate_if_english(self, text: str) -> str:
        cleaned = str(text or "").strip()
        if (
            not settings.fallback_translation_enabled
            or self._translation_unavailable
            or not self.is_english(cleaned)
        ):
            return cleaned

        try:
            return self._translate_with_timeout(cleaned)
        except concurrent.futures.TimeoutError:
            logger.warning("Traduccion de fallback cancelada por timeout")
        except Exception as exc:
            self._translation_unavailable = True
            logger.warning("No se pudo traducir el fallback; se conserva el original: %s", exc)
        return cleaned

    def is_english(self, text: str) -> bool:
        words = re.findall(r"[a-zA-Z]+", text.lower())
        if len(words) < settings.fallback_language_min_words:
            return False

        english_hits = sum(word in self._ENGLISH_MARKERS for word in words)
        spanish_hits = sum(word in self._SPANISH_MARKERS for word in words)
        required_hits = max(2, round(len(words) * 0.08))
        return english_hits >= required_hits and english_hits >= (spanish_hits * 2)

    def _translate_with_timeout(self, text: str) -> str:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self._translate, text)
        try:
            return future.result(timeout=settings.fallback_translation_timeout_seconds)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    @lru_cache(maxsize=256)
    def _translate(self, text: str) -> str:
        tokenizer, model = self._get_translator()
        translated_parts = []
        for part in self._split_text(text):
            inputs = tokenizer(
                part,
                return_tensors="pt",
                truncation=True,
                max_length=settings.fallback_translation_max_tokens,
            )
            generated = model.generate(
                **inputs,
                max_new_tokens=settings.fallback_translation_max_tokens,
            )
            translated = tokenizer.decode(generated[0], skip_special_tokens=True).strip()
            translated_parts.append(translated or part)
        return "\n\n".join(translated_parts).strip() or text

    def _get_translator(self):
        if self._translator is not None:
            return self._translator

        with self._load_lock:
            if self._translator is not None:
                return self._translator

            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

            tokenizer = AutoTokenizer.from_pretrained(
                settings.fallback_translation_model,
                local_files_only=settings.fallback_translation_local_files_only,
            )
            model = AutoModelForSeq2SeqLM.from_pretrained(
                settings.fallback_translation_model,
                local_files_only=settings.fallback_translation_local_files_only,
            )
            model.eval()
            self._translator = (tokenizer, model)
        return self._translator

    def _split_text(self, text: str) -> list[str]:
        max_chars = max(200, settings.fallback_translation_max_chars)
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
        parts: list[str] = []
        for paragraph in paragraphs or [text]:
            while len(paragraph) > max_chars:
                split_at = paragraph.rfind(" ", 0, max_chars)
                split_at = split_at if split_at > 0 else max_chars
                parts.append(paragraph[:split_at].strip())
                paragraph = paragraph[split_at:].strip()
            if paragraph:
                parts.append(paragraph)
        return parts
