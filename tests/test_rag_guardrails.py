from __future__ import annotations

from app.models.schemas import ChatRequest
from app.services.rag_service import RagService


class FailingVectorstore:
    def retrieve(self, question: str, equipment_name: str | None, k=None):
        raise AssertionError("No debe consultar ChromaDB sin equipo exacto.")


def test_rag_blocks_request_without_equipment_scope():
    service = RagService(vectorstore=FailingVectorstore())
    request = ChatRequest(
        query="Que significa esta alarma?",
        equipment_id=None,
        equipment_name=None,
        role="tecnico",
        force_fallback=False,
        request_id="test",
    )

    response = service.answer_question(
        chat_request=request,
        session_id="session",
        should_cancel=lambda: False,
    )

    assert response["mode"] == "guardrail"
    assert "equipo exacto" in response["answer"].lower()
