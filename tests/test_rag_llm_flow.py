from __future__ import annotations

from app.models.schemas import ChatRequest, RetrievedChunk, SourceCitation
from app.services.rag_service import RagService


class FakeVectorstore:
    def __init__(self) -> None:
        self.chunks = [
            RetrievedChunk(
                text=(
                    "Si la alarma no puede resolverse con seguridad, detener la accion. "
                    "El procedimiento indica confirmar el estado mostrado en pantalla antes de continuar. "
                    "Esta informacion proviene del manual y describe una accion documentada para el operador "
                    "cuando el equipo indica una condicion que podria afectar la seguridad del proceso."
                ),
                citation=SourceCitation(
                    source_file="manual_sterrad.pdf",
                    page=10,
                    chunk_id="a",
                    equipment_name="Esterilizadora Sterrad 100",
                ),
                score=0.1,
            ),
            RetrievedChunk(
                text=(
                    "El operador debe seguir solamente instrucciones documentadas y contactar al servicio "
                    "tecnico cuando el procedimiento no sea concluyente o exista riesgo. "
                    "El fragmento tambien indica que no se debe continuar con acciones no verificadas "
                    "si la condicion no queda resuelta con la informacion recuperada."
                ),
                citation=SourceCitation(
                    source_file="manual_sterrad.pdf",
                    page=11,
                    chunk_id="b",
                    equipment_name="Esterilizadora Sterrad 100",
                ),
                score=0.2,
            )
        ]

    def retrieve(self, question: str, equipment_name: str | None, k=None):
        return self.chunks


class FakeOllama:
    def __init__(self, answer: str = "Respuesta basada en contexto.") -> None:
        self.answer = answer
        self.last_prompt = ""

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.answer


class FailingOllama:
    def generate(self, prompt: str) -> str:
        raise RuntimeError("ollama offline")


class EmptyMemory:
    def get_last_equipment(self, session_id: str):
        return None

    def clear_session(self, session_id: str) -> None:
        return None

    def get_recent_messages(self, session_id: str, equipment_name: str):
        return []

    def add_message(self, session_id: str, role: str, content: str, equipment_name: str) -> None:
        return None


def _service(vectorstore=None, ollama_service=None) -> RagService:
    return RagService(
        vectorstore=vectorstore or FakeVectorstore(),
        ollama_service=ollama_service or FakeOllama(),
        memory_service=EmptyMemory(),
    )


def _request(role: str = "operador") -> ChatRequest:
    return ChatRequest(
        query="Que hago con la alarma?",
        equipment_id="sterrad-100",
        equipment_name="Esterilizadora Sterrad 100",
        role=role,
        force_fallback=False,
        request_id="test",
    )


def test_rag_generates_llm_answer_with_context_prompt():
    ollama = FakeOllama()
    service = _service(ollama_service=ollama)

    response = service.answer_question(_request(), "session", should_cancel=lambda: False)

    assert response["mode"] == "llm"
    assert response["answer"] == "Respuesta basada en contexto."
    assert "Contexto documental recuperado exclusivamente desde Markdown" in ollama.last_prompt
    assert "Esterilizadora Sterrad 100" in ollama.last_prompt
    assert "Fuente:" not in ollama.last_prompt
    assert "pagina 10" not in ollama.last_prompt


def test_technician_response_gets_sources_when_model_omits_them():
    service = _service(ollama_service=FakeOllama("Diagnostico tecnico."))

    response = service.answer_question(_request(role="tecnico"), "session", should_cancel=lambda: False)

    assert response["mode"] == "llm"
    assert "Fuente: manual_sterrad.pdf, pag. 10" in response["answer"]


def test_rag_falls_back_to_chromadb_when_llm_fails():
    service = _service(ollama_service=FailingOllama())

    response = service.answer_question(_request(role="tecnico"), "session", should_cancel=lambda: False)

    assert response["mode"] == "fallback_llm_error"
    assert "Respuesta directa desde la base documental local" in response["answer"]
    assert "ollama offline" in response["answer"]


def test_force_fallback_labels_english_extract_as_translated():
    class EnglishVectorstore:
        def retrieve(self, question: str, equipment_name: str | None, k=None):
            return [
                RetrievedChunk(
                    text="Press START and verify the cassette door opens. Replace wire harness if the alarm remains active.",
                    citation=SourceCitation(
                        source_file="manual_sterrad.pdf",
                        page=260,
                        chunk_id="door-test",
                        equipment_name="Esterilizadora Sterrad 100",
                    ),
                )
            ]

    request = _request(role="tecnico")
    request = ChatRequest(
        query=request.query,
        equipment_id=request.equipment_id,
        equipment_name=request.equipment_name,
        role=request.role,
        force_fallback=True,
        request_id=request.request_id,
    )
    service = _service(
        vectorstore=EnglishVectorstore(),
        ollama_service=FakeOllama("Presione START y verifique que la puerta del cassette se abra."),
    )

    response = service.answer_question(request, "session", should_cancel=lambda: False)

    assert response["mode"] == "fallback_chromadb"
    assert "Extracto traducido 1" in response["answer"]
    assert "Presione START" in response["answer"]


def test_translation_preamble_is_removed():
    service = _service()

    cleaned = service._strip_translation_preamble(
        "A continuación, te presento la traducción al español técnico:\n\nPrueba de puerta"
    )

    assert cleaned == "Prueba de puerta"


def test_operator_blocks_llm_when_context_is_too_sparse():
    class SparseVectorstore:
        def retrieve(self, question: str, equipment_name: str | None, k=None):
            return [
                RetrievedChunk(
                    text="The door opens.",
                    citation=SourceCitation(
                        source_file="manual_sterrad.pdf",
                        page=10,
                        chunk_id="a",
                        equipment_name="Esterilizadora Sterrad 100",
                    ),
                )
            ]

    service = _service(vectorstore=SparseVectorstore())

    response = service.answer_question(_request(), "session", should_cancel=lambda: False)

    assert response["mode"] == "contexto_insuficiente_operador"
    assert "contacte INMEDIATAMENTE" in response["answer"]
