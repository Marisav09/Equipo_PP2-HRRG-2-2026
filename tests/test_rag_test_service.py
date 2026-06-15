from __future__ import annotations

import csv
import json

import pytest

from app.services.rag_test_service import RagTestService, load_questions


class FakeRagService:
    def __init__(self) -> None:
        self.calls = []

    def answer_question(self, chat_request, session_id, should_cancel):
        self.calls.append((chat_request, session_id))
        return {
            "answer": f"Respuesta a: {chat_request.query}",
            "mode": "llm_hibrido",
            "sources": [{"source_file": "manual.pdf", "page": 7}],
        }


def test_load_questions_accepts_strings_and_enabled_objects(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(
        json.dumps(
            {
                "questions": [
                    "Pregunta uno",
                    {"question": "Pregunta dos", "enabled": True},
                    {"question": "Pregunta deshabilitada", "enabled": False},
                ]
            }
        ),
        encoding="utf-8",
    )

    assert load_questions(path) == ["Pregunta uno", "Pregunta dos"]


def test_load_questions_rejects_empty_configuration(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text('{"questions": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="No hay preguntas"):
        load_questions(path)


def test_runner_uses_selected_equipment_role_and_isolated_sessions():
    fake = FakeRagService()
    ticks = iter([1.0, 2.25, 3.0, 4.5])
    runner = RagTestService(rag_service=fake, clock=lambda: next(ticks))

    rows = runner.run(
        questions=["Primera", "Segunda"],
        equipment_id="ventilador-engstrom",
        equipment_name="Ventilador Engstrom",
        role="operador",
    )

    assert len(rows) == 2
    assert rows[0]["answer"] == "Respuesta a: Primera"
    assert rows[0]["elapsed_seconds"] == 1.25
    assert rows[0]["source_files"] == "manual.pdf"
    assert rows[0]["pages"] == "7"
    assert fake.calls[0][0].role == "operador"
    assert fake.calls[0][0].equipment_id == "ventilador-engstrom"
    assert fake.calls[0][1] != fake.calls[1][1]


def test_runner_can_share_session_and_write_csv(tmp_path):
    fake = FakeRagService()
    runner = RagTestService(rag_service=fake, clock=lambda: 1.0)

    rows = runner.run(
        questions=["Primera", "Segunda"],
        equipment_id="ventilador-engstrom",
        equipment_name="Ventilador Engstrom",
        role="tecnico",
        shared_session=True,
    )
    output = tmp_path / "results.csv"
    runner.write_csv(rows, output)

    assert fake.calls[0][1] == fake.calls[1][1]
    with output.open("r", encoding="utf-8-sig", newline="") as file:
        saved = list(csv.DictReader(file))
    assert saved[0]["question"] == "Primera"
    assert saved[0]["answer"] == "Respuesta a: Primera"
    assert saved[0]["role"] == "tecnico"
