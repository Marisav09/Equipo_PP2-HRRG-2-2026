from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from app.core.config import settings


class IngestionAuditService:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.ingestion_audit_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def get_latest_by_source(self, source_file: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM ingested_documents
                WHERE source_file = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (source_file,),
            ).fetchone()
        return dict(row) if row else None

    def record(
        self,
        *,
        source_file: str,
        file_hash: str,
        status: str,
        equipment_id: str | None = None,
        equipment_name: str | None = None,
        page_count: int = 0,
        chunk_count: int = 0,
        image_count: int = 0,
        message: str = "",
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO ingested_documents (
                    source_file,
                    file_hash,
                    status,
                    equipment_id,
                    equipment_name,
                    page_count,
                    chunk_count,
                    image_count,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_file,
                    file_hash,
                    status,
                    equipment_id,
                    equipment_name,
                    page_count,
                    chunk_count,
                    image_count,
                    message,
                ),
            )

    def list_latest(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT d.*
                FROM ingested_documents d
                INNER JOIN (
                    SELECT source_file, MAX(id) AS max_id
                    FROM ingested_documents
                    GROUP BY source_file
                ) latest
                ON d.source_file = latest.source_file AND d.id = latest.max_id
                ORDER BY d.source_file
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ingested_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_file TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    equipment_id TEXT,
                    equipment_name TEXT,
                    page_count INTEGER NOT NULL DEFAULT 0,
                    chunk_count INTEGER NOT NULL DEFAULT 0,
                    image_count INTEGER NOT NULL DEFAULT 0,
                    message TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_ingested_documents_source
                ON ingested_documents (source_file, id)
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection
