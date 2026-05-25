from __future__ import annotations

from app.models.schemas import ChatRequest, RetrievedChunk, SourceCitation
from app.services.memory_service import MemoryService
from app.services.rag_service import RagService


def test_memory_service_keeps_messages_scoped_by_equipment(tmp_path):
    memory = MemoryService(tmp_path / "memory.sqlite3")
    memory.add_message("s1", "user", "alarma puerta", "Esterilizadora Sterrad 100")
    memory.add_message("s1", "user", "hd 67", "Rodantes MAC GMM")

    sterrad_history = memory.get_recent_messages("s1", "Esterilizadora Sterrad 100")

    assert len(sterrad_history) == 1
    assert sterrad_history[0]["content"] == "alarma puerta"


def test_memory_service_clears_session(tmp_path):
    memory = MemoryService(tmp_path / "memory.sqlite3")
    memory.add_message("s1", "user", "alarma", "Esterilizadora Sterrad 100")

    memory.clear_session("s1")

    assert memory.get_recent_messages("s1", "Esterilizadora Sterrad 100") == []


class TrackingVectorstore:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def retrieve(self, question: str, equipment_name: str | None, k=None):
        self.questions.append(question)
        return [
            RetrievedChunk(
                text=(
                    "Fragmento suficientemente largo para que el tecnico pueda recibir una respuesta "
                    "basada en contexto documental sin activar bloqueos de operador."
                ),
                citation=SourceCitation(
                    source_file="manual.pdf",
                    page=1,
                    chunk_id="a",
                    equipment_name=equipment_name or "Equipo",
                ),
            )
        ]


class StaticOllama:
    def generate(self, prompt: str) -> str:
        return "Respuesta."


def _chat_request(equipment_id: str, equipment_name: str, query: str = "Primera pregunta") -> ChatRequest:
    return ChatRequest(
        query=query,
        equipment_id=equipment_id,
        equipment_name=equipment_name,
        role="tecnico",
        force_fallback=False,
        request_id="test",
    )


def test_rag_uses_history_for_same_equipment_and_clears_on_change(tmp_path):
    memory = MemoryService(tmp_path / "memory.sqlite3")
    vectorstore = TrackingVectorstore()
    service = RagService(
        vectorstore=vectorstore,
        ollama_service=StaticOllama(),
        memory_service=memory,
    )

    service.answer_question(
        _chat_request("sterrad-100", "Esterilizadora Sterrad 100", "Primera pregunta"),
        "session",
        should_cancel=lambda: False,
    )
    service.answer_question(
        _chat_request("sterrad-100", "Esterilizadora Sterrad 100", "Y eso?"),
        "session",
        should_cancel=lambda: False,
    )

    assert "Primera pregunta" in vectorstore.questions[-1]

    service.answer_question(
        _chat_request("rodantes-mac-gmm", "Rodantes MAC GMM", "Nueva pregunta"),
        "session",
        should_cancel=lambda: False,
    )

    assert memory.get_recent_messages("session", "Esterilizadora Sterrad 100") == []
    assert memory.get_last_equipment("session") == "Rodantes MAC GMM"
