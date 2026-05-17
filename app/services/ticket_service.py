from __future__ import annotations

import sqlite3
from contextlib import closing

from app.core.config import settings
from app.models.schemas import TicketRecord


class TicketService:
    def __init__(self, db_path=settings.tickets_db_path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    question TEXT NOT NULL,
                    equipment TEXT,
                    reason TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def create_ticket(self, record: TicketRecord) -> int:
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO tickets (created_at, question, equipment, reason, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    record.created_at,
                    record.question,
                    record.equipment,
                    record.reason,
                    record.status,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def list_tickets(self, limit: int = 100) -> list[dict[str, object]]:
        with closing(self._connect()) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, created_at, question, equipment, reason, status
                FROM tickets
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
