from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import datetime

from app.core.config import settings


class MemoryService:
    def __init__(self, db_path=settings.memory_db_path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    equipment TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_conversation_memory_session
                ON conversation_memory (session_id, id)
                """
            )
            connection.commit()

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        equipment: str | None = None,
    ) -> int:
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO conversation_memory (created_at, session_id, role, content, equipment)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    datetime.utcnow().isoformat(),
                    session_id,
                    role,
                    content,
                    equipment,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def get_recent_messages(
        self,
        session_id: str,
        limit: int | None = None,
    ) -> list[dict[str, str]]:
        with closing(self._connect()) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT role, content, equipment, created_at
                FROM conversation_memory
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit or settings.memory_window_messages),
            ).fetchall()

        return [dict(row) for row in reversed(rows)]

    def clear_session(self, session_id: str) -> None:
        with closing(self._connect()) as connection:
            connection.execute(
                "DELETE FROM conversation_memory WHERE session_id = ?",
                (session_id,),
            )
            connection.commit()
