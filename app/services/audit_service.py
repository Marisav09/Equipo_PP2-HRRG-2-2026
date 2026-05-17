from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from datetime import datetime

from app.core.config import settings
from app.models.schemas import AssistantResponse


class AuditService:
    def __init__(self, db_path=settings.audit_db_path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS query_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    equipment TEXT,
                    sources_json TEXT NOT NULL,
                    ticket_id INTEGER
                )
                """
            )
            connection.commit()

    def record_query(
        self,
        question: str,
        response: AssistantResponse,
        equipment: str | None = None,
    ) -> int:
        sources_json = json.dumps(
            [source.__dict__ for source in response.sources],
            ensure_ascii=False,
        )
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO query_audit (
                    created_at, question, answer, mode, equipment, sources_json, ticket_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(),
                    question,
                    response.answer,
                    response.mode,
                    equipment,
                    sources_json,
                    response.ticket_id,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def get_recent_queries(self, limit: int = 50) -> list[dict[str, object]]:
        with closing(self._connect()) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, created_at, question, answer, mode, equipment, sources_json, ticket_id
                FROM query_audit
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
