from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from app.core.config import settings


class MemoryService:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.memory_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        equipment_name: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO messages (session_id, role, content, equipment_name)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, role, content, equipment_name),
            )

    def get_recent_messages(
        self,
        session_id: str,
        equipment_name: str,
        limit: int = 6,
    ) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content, equipment_name, created_at
                FROM messages
                WHERE session_id = ? AND equipment_name = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, equipment_name, limit),
            ).fetchall()

        return [
            {
                "role": row["role"],
                "content": row["content"],
                "equipment_name": row["equipment_name"],
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]

    def get_last_equipment(self, session_id: str) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT equipment_name
                FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (session_id,),
            ).fetchone()
        return str(row["equipment_name"]) if row else None

    def clear_session(self, session_id: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    equipment_name TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_session_equipment
                ON messages (session_id, equipment_name, id)
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
