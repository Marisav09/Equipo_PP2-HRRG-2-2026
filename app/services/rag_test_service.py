from __future__ import annotations

import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable
from uuid import uuid4

from app.models.schemas import ChatRequest
from app.services.rag_service import RagService


CSV_FIELDS = (
    "timestamp",
    "equipment_id",
    "equipment_name",
    "role",
    "question_number",
    "question",
    "answer",
    "mode",
    "elapsed_seconds",
    "source_files",
    "pages",
    "sources_json",
    "error",
)


def load_questions(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    raw_questions = payload.get("questions", []) if isinstance(payload, dict) else payload
    if not isinstance(raw_questions, list):
        raise ValueError("El archivo debe contener una lista o un objeto con la clave 'questions'.")

    questions = []
    for item in raw_questions:
        if isinstance(item, str):
            question = item.strip()
            enabled = True
        elif isinstance(item, dict):
            question = str(item.get("question", "")).strip()
            enabled = bool(item.get("enabled", True))
        else:
            continue
        if question and enabled:
            questions.append(question)

    if not questions:
        raise ValueError("No hay preguntas habilitadas en el archivo.")
    return questions


class RagTestService:
    def __init__(
        self,
        rag_service: RagService | None = None,
        clock: Callable[[], float] = time.perf_counter,
    ) -> None:
        self.rag_service = rag_service or RagService()
        self.clock = clock

    def run(
        self,
        questions: Iterable[str],
        equipment_id: str,
        equipment_name: str,
        role: str,
        shared_session: bool = False,
        force_fallback: bool = False,
        on_result: Callable[[dict[str, Any]], None] | None = None,
    ) -> list[dict[str, Any]]:
        shared_session_id = f"rag-test-{uuid4()}"
        rows = []
        for index, question in enumerate(questions, start=1):
            session_id = shared_session_id if shared_session else f"rag-test-{uuid4()}"
            row = self._run_question(
                question=str(question).strip(),
                question_number=index,
                equipment_id=equipment_id,
                equipment_name=equipment_name,
                role=role,
                session_id=session_id,
                force_fallback=force_fallback,
            )
            rows.append(row)
            if on_result:
                on_result(row)
        return rows

    def _run_question(
        self,
        question: str,
        question_number: int,
        equipment_id: str,
        equipment_name: str,
        role: str,
        session_id: str,
        force_fallback: bool,
    ) -> dict[str, Any]:
        started_at = self.clock()
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
        try:
            response = self.rag_service.answer_question(
                ChatRequest(
                    query=question,
                    equipment_id=equipment_id,
                    equipment_name=equipment_name,
                    role=role,
                    force_fallback=force_fallback,
                    request_id=f"rag-test-{uuid4()}",
                ),
                session_id=session_id,
                should_cancel=lambda: False,
            )
            sources = response.get("sources") or []
            if not isinstance(sources, list):
                sources = [sources] if isinstance(sources, dict) else []
            return self._row(
                timestamp=timestamp,
                equipment_id=equipment_id,
                equipment_name=equipment_name,
                role=role,
                question_number=question_number,
                question=question,
                answer=str(response.get("answer", "")),
                mode=str(response.get("mode", "")),
                elapsed=round(self.clock() - started_at, 3),
                sources=sources,
                error="",
            )
        except Exception as exc:
            return self._row(
                timestamp=timestamp,
                equipment_id=equipment_id,
                equipment_name=equipment_name,
                role=role,
                question_number=question_number,
                question=question,
                answer="",
                mode="ERROR",
                elapsed=round(self.clock() - started_at, 3),
                sources=[],
                error=f"{type(exc).__name__}: {exc}",
            )

    def _row(
        self,
        timestamp: str,
        equipment_id: str,
        equipment_name: str,
        role: str,
        question_number: int,
        question: str,
        answer: str,
        mode: str,
        elapsed: float,
        sources: list[dict],
        error: str,
    ) -> dict[str, Any]:
        return {
            "timestamp": timestamp,
            "equipment_id": equipment_id,
            "equipment_name": equipment_name,
            "role": role,
            "question_number": question_number,
            "question": question,
            "answer": answer,
            "mode": mode,
            "elapsed_seconds": elapsed,
            "source_files": " | ".join(str(source.get("source_file", "")) for source in sources),
            "pages": " | ".join(str(source.get("page", "")) for source in sources),
            "sources_json": json.dumps(sources, ensure_ascii=False),
            "error": error,
        }

    def write_csv(self, rows: Iterable[dict[str, Any]], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
