from __future__ import annotations

from app.models.schemas import ChatRequest, RetrievedChunk, SourceCitation
from app.services.rag_service import RagService


class FakeVectorstore:
    def __init__(self) -> None:
        self.last_role = ""
        self.chunks = [
            RetrievedChunk(
                text="El interruptor del sistema permite poner en funcionamiento el equipo.",
                citation=SourceCitation(
                    source_file="manual.md",
                    page=10,
                    chunk_id="a",
                    equipment_name="Esterilizadora Sterrad 100",
                    pdf_page=10,
                    pdf_page_confidence="verified",
                ),
                score=0.9,
            )
        ]

    def retrieve(self, question: str, equipment_name: str | None, k=None, role="tecnico"):
        self.last_role = role
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


def _request(role: str = "operador", query: str = "Como se utiliza?") -> ChatRequest:
    return ChatRequest(
        query=query,
        equipment_id="sterrad-100",
        equipment_name="Esterilizadora Sterrad 100",
        role=role,
        force_fallback=False,
        request_id="test",
    )


def test_rag_passes_role_to_hybrid_retrieval_and_calls_llm():
    vectorstore = FakeVectorstore()
    ollama = FakeOllama()
    service = _service(vectorstore=vectorstore, ollama_service=ollama)

    response = service.answer_question(_request(), "session", should_cancel=lambda: False)

    assert response["mode"] == "llm_hibrido"
    assert vectorstore.last_role == "operador"
    assert "Contexto documental recuperado" in ollama.last_prompt
    assert response["sources"] == []


def test_technician_response_exposes_verified_sources():
    service = _service(ollama_service=FakeOllama("Diagnostico tecnico."))

    response = service.answer_question(_request(role="tecnico"), "session", should_cancel=lambda: False)

    assert response["mode"] == "llm_hibrido"
    assert response["sources"][0]["page"] == 10


def test_patient_connected_guardrail_runs_before_retrieval():
    class FailingVectorstore:
        def retrieve(self, *args, **kwargs):
            raise AssertionError("No debe recuperar documentos.")

    service = _service(vectorstore=FailingVectorstore())
    response = service.answer_question(
        _request(query="Tengo un paciente conectado y necesito intervenir el equipo"),
        "session",
        should_cancel=lambda: False,
    )

    assert response["mode"] == "guardrail_paciente_conectado"
    assert "asistencia clinica inmediata" in response["answer"]


def test_operator_output_removes_prohibited_internal_instructions():
    service = _service(
        ollama_service=FakeOllama(
            "Abra la tapa del gabinete y mida tension.\n"
            "Observe el indicador visible y contacte a Ingenieria Clinica."
        )
    )

    response = service.answer_question(_request(), "session", should_cancel=lambda: False)

    assert "Abra la tapa" not in response["answer"]
    assert "mida tension" not in response["answer"]
    assert "Observe el indicador visible" in response["answer"]


def test_rag_falls_back_to_document_context_when_llm_fails():
    service = _service(ollama_service=FailingOllama())

    response = service.answer_question(_request(role="tecnico"), "session", should_cancel=lambda: False)

    assert response["mode"] == "fallback_llm_error"
    assert "interruptor del sistema" in response["answer"]


def test_operator_response_removes_prompt_echo():
    service = _service()
    cleaned = service._strip_operator_prompt_echo(
        "Indica la accion segura inmediata. Observe el indicador visible."
    )

    assert "indica la accion segura inmediata" not in cleaned.lower()
    assert "Observe el indicador visible" in cleaned
