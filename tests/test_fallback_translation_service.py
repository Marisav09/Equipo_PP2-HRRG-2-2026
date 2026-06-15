from __future__ import annotations

from app.services.fallback_translation_service import FallbackTranslationService


ENGLISH_TEXT = (
    "Before using the device, check that the system is connected and press the start button."
)


def test_detects_predominantly_english_text():
    service = FallbackTranslationService()

    assert service.is_english(ENGLISH_TEXT)


def test_does_not_treat_spanish_with_technical_terms_as_english():
    service = FallbackTranslationService()

    assert not service.is_english(
        "Antes de utilizar el equipo, presione el botón de inicio y revise el error del sistema."
    )


def test_short_or_ambiguous_text_is_not_translated():
    service = FallbackTranslationService()

    assert not service.is_english("System error")


def test_translates_english_but_does_not_translate_spanish():
    class FakeTranslationService(FallbackTranslationService):
        def __init__(self) -> None:
            super().__init__()
            self.translated = []

        def _translate(self, text: str) -> str:
            self.translated.append(text)
            return "Traduccion"

    service = FakeTranslationService()

    assert service.translate_if_english(ENGLISH_TEXT) == "Traduccion"
    assert service.translate_if_english("Antes de utilizar el equipo revise el sistema.") == (
        "Antes de utilizar el equipo revise el sistema."
    )
    assert service.translated == [ENGLISH_TEXT]


def test_translation_failure_preserves_original_and_disables_retries():
    class FailingTranslationService(FallbackTranslationService):
        def __init__(self) -> None:
            super().__init__()
            self.attempts = 0

        def _translate(self, text: str) -> str:
            self.attempts += 1
            raise RuntimeError("modelo no disponible")

    service = FailingTranslationService()

    assert service.translate_if_english(ENGLISH_TEXT) == ENGLISH_TEXT
    assert service.translate_if_english(ENGLISH_TEXT) == ENGLISH_TEXT
    assert service.attempts == 1
