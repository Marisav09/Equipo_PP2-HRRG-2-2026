from __future__ import annotations

import re
import sqlite3
import unicodedata
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from app.core.config import settings


class KnowledgeAuditService:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or settings.memory_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def record_consultation(
        self,
        *,
        session_id: str,
        chat_id: str,
        username: str,
        profile: str,
        user_service: str,
        equipment_id: str | None,
        equipment_name: str,
        question: str,
        answer: str,
    ) -> dict[str, Any]:
        category = self.classify_category(question)
        incident_candidate = self.looks_like_incident(question)
        now = datetime.now()
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO consultations (
                    session_id, chat_id, username, profile, user_service, equipment_id,
                    equipment_name, question, answer, date, time, category,
                    es_incidente, incident_candidate
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    chat_id,
                    username,
                    profile,
                    user_service,
                    equipment_id or "",
                    equipment_name,
                    question,
                    answer,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    category,
                    0,
                    1 if incident_candidate else 0,
                ),
            )
            consultation_id = int(cursor.lastrowid)

        return {
            "consultation_id": consultation_id,
            "category": category,
            "incident_candidate": incident_candidate,
        }

    def mark_incident(self, consultation_id: int, username: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM consultations WHERE id = ?",
                (consultation_id,),
            ).fetchone()
            if not row:
                return None

            connection.execute(
                """
                UPDATE consultations
                SET es_incidente = 1
                WHERE id = ?
                """,
                (consultation_id,),
            )
            connection.execute(
                """
                INSERT INTO incidents (
                    consultation_id, username, user_service, equipment_id,
                    equipment_name, question, category, date, time, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    consultation_id,
                    username or row["username"],
                    row["user_service"],
                    row["equipment_id"],
                    row["equipment_name"],
                    row["question"],
                    row["category"],
                    row["date"],
                    row["time"],
                    "registrado",
                ),
            )

        return {"status": "registrado", "consultation_id": consultation_id}

    def list_user_consultations(self, username: str, limit: int = 30, profile: str = "") -> list[dict[str, Any]]:
        profile_clause = "AND profile = ?" if profile else ""
        params: tuple[Any, ...] = (username, profile, limit) if profile else (username, limit)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT id, equipment_name, question, answer, date, time, category, es_incidente
                FROM consultations
                WHERE username = ?
                {profile_clause}
                ORDER BY date DESC, time DESC, id DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def list_user_chats(self, username: str, limit: int = 5, profile: str = "") -> list[dict[str, Any]]:
        profile_clause = "AND profile = ?" if profile else ""
        params: tuple[Any, ...] = (username, profile, limit) if profile else (username, limit)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT
                    chat_id,
                    MAX(id) AS last_id,
                    MAX(date || ' ' || time) AS last_at,
                    (
                        SELECT equipment_name
                        FROM consultations c2
                        WHERE c2.username = consultations.username
                          AND c2.chat_id = consultations.chat_id
                        ORDER BY id DESC
                        LIMIT 1
                    ) AS equipment_name,
                    (
                        SELECT question
                        FROM consultations c2
                        WHERE c2.username = consultations.username
                          AND c2.chat_id = consultations.chat_id
                        ORDER BY id DESC
                        LIMIT 1
                    ) AS last_question,
                    COUNT(*) AS message_count
                FROM consultations
                WHERE username = ?
                {profile_clause}
                GROUP BY chat_id
                ORDER BY last_id DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def get_user_chat(self, username: str, chat_id: str, profile: str = "") -> dict[str, Any] | None:
        profile_clause = "AND profile = ?" if profile else ""
        params: tuple[Any, ...] = (username, chat_id, profile) if profile else (username, chat_id)
        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT id, chat_id, equipment_id, equipment_name, question, answer,
                       date, time, category, es_incidente
                FROM consultations
                WHERE username = ? AND chat_id = ?
                {profile_clause}
                ORDER BY id ASC
                """,
                params,
            ).fetchall()

        if not rows:
            return None

        first = rows[0]
        last = rows[-1]
        return {
            "chat_id": chat_id,
            "equipment_id": last["equipment_id"],
            "equipment_name": last["equipment_name"],
            "created_at": f"{first['date']} {first['time']}",
            "updated_at": f"{last['date']} {last['time']}",
            "turns": [dict(row) for row in rows],
        }

    def search_consultations(
        self,
        search: str = "",
        *,
        username: str = "",
        equipment: str = "",
        date_from: str = "",
        date_to: str = "",
        limit: int = 80,
    ) -> list[dict[str, Any]]:
        clauses = ["date >= ?"]
        params: list[Any] = [date_from or self._retention_cutoff(90)]

        if date_to:
            clauses.append("date <= ?")
            params.append(date_to)

        if search.strip():
            like = f"%{search.strip()}%"
            clauses.append(
                """
                (
                    question LIKE ?
                    OR answer LIKE ?
                    OR equipment_name LIKE ?
                    OR username LIKE ?
                    OR category LIKE ?
                    OR user_service LIKE ?
                )
                """
            )
            params.extend([like, like, like, like, like, like])

        if username.strip():
            clauses.append("username LIKE ?")
            params.append(f"%{username.strip()}%")

        if equipment.strip():
            clauses.append("equipment_name LIKE ?")
            params.append(f"%{equipment.strip()}%")

        where = "WHERE " + " AND ".join(clauses)
        params.append(limit)

        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT id, username, profile, user_service, equipment_name, question,
                       date, time, category, es_incidente
                FROM consultations
                {where}
                ORDER BY date DESC, time DESC, id DESC
                LIMIT ?
                """,
                tuple(params),
            ).fetchall()
        return [dict(row) for row in rows]

    def dashboard(self) -> dict[str, Any]:
        rows = self._all_consultations()
        today = datetime.now().strftime("%Y-%m-%d")
        equipment_counter = Counter(row["equipment_name"] for row in rows)
        user_counter = Counter(row["username"] for row in rows)
        profile_counter = Counter(self.profile_label(row["profile"]) for row in rows)
        category_counter = Counter(row["category"] for row in rows)
        active_users = {row["username"] for row in rows}
        consulted_equipment = {row["equipment_name"] for row in rows}
        recurrent_failures = [
            item
            for item in self.failure_map(rows)
            if item["total"] >= 2 or len(item["failures"]) >= 2
        ]

        return {
            "indicators": {
                "consultations_today": sum(1 for row in rows if row["date"] == today),
                "consulted_equipment": len(consulted_equipment),
                "active_users": len(active_users),
                "recurrent_failures": len(recurrent_failures),
                "total_consultations": len(rows),
            },
            "top_equipment": self._counter_items(equipment_counter),
            "top_users": self._counter_items(user_counter),
            "by_profile": self._counter_items(profile_counter),
            "by_category": self._counter_items(category_counter),
            "failure_map": recurrent_failures[:8],
            "alerts": self.alerts(recurrent_failures),
            "timeline": self.timeline(rows),
            "retention": {
                "detail_days": 90,
                "summary_days": 365,
                "detail_from": self._retention_cutoff(90),
                "summary_from": self._retention_cutoff(365),
            },
        }

    def alerts(self, recurrent_failures: list[dict[str, Any]]) -> list[dict[str, Any]]:
        alerts = []
        for item in recurrent_failures:
            main_failure = item["failures"][0] if item.get("failures") else None
            if item["total"] < 3 and not (main_failure and main_failure["count"] >= 3):
                continue
            alerts.append(
                {
                    "level": "Alta" if item["total"] >= 5 or (main_failure and main_failure["count"] >= 5) else "Media",
                    "equipment": item["equipment"],
                    "failure": main_failure["label"] if main_failure else "Falla recurrente",
                    "count": main_failure["count"] if main_failure else item["total"],
                    "message": "Equipo con consultas repetidas. Revisar intervención preventiva o capacitación focalizada.",
                }
            )
        return alerts[:6]

    def failure_map(self, rows: list[sqlite3.Row] | None = None) -> list[dict[str, Any]]:
        rows = rows or self._all_consultations()
        grouped: dict[str, Counter[str]] = {}
        for row in rows:
            equipment = row["equipment_name"]
            grouped.setdefault(equipment, Counter())
            grouped[equipment][self.failure_label(row["question"], row["category"])] += 1

        result = []
        for equipment, counter in grouped.items():
            failures = self._counter_items(counter)
            result.append(
                {
                    "equipment": equipment,
                    "total": sum(counter.values()),
                    "failures": failures[:6],
                }
            )
        return sorted(result, key=lambda item: item["total"], reverse=True)

    def timeline(self, rows: list[sqlite3.Row] | None = None, limit: int = 24) -> list[dict[str, Any]]:
        rows = rows or self._all_consultations()
        sorted_rows = sorted(rows, key=lambda row: (row["date"], row["time"], row["id"]), reverse=True)
        return [
            {
                "date": row["date"],
                "time": row["time"],
                "equipment": row["equipment_name"],
                "category": row["category"],
                "label": self.failure_label(row["question"], row["category"]),
                "question": row["question"],
            }
            for row in sorted_rows[:limit]
        ]

    def classify_category(self, question: str) -> str:
        normalized = self._normalize(question)
        category_terms = (
            ("Alarmas", ("alarma", "alerta", "peep", "presion alta", "presion baja", "fio2")),
            ("Calibracion", ("calibr", "ajuste", "sensor de flujo", "flujo", "test")),
            ("Mantenimiento", ("mantenimiento", "limpieza", "cambio", "reemplazo", "filtro", "bateria")),
            ("Pantalla", ("pantalla", "display", "touch", "tactil", "bloque", "congelada")),
            ("Sensores", ("sensor", "celda", "transductor", "sonda")),
            ("Energia", ("enciende", "energia", "alimentacion", "carga", "bateria", "fusible")),
            ("Uso operativo", ("como", "donde", "que significa", "modo", "configur")),
        )
        for category, terms in category_terms:
            if any(term in normalized for term in terms):
                return category
        return "Consulta tecnica"

    def looks_like_incident(self, question: str) -> bool:
        normalized = self._normalize(question)
        incident_terms = (
            "no enciende",
            "no funciona",
            "no carga",
            "pantalla congelada",
            "alarma constante",
            "alarma permanente",
            "falla",
            "fallo",
            "error",
            "bloqueado",
            "perdida",
            "no calibra",
            "no puedo calibrar",
            "sensor",
            "presion alta",
            "presion baja",
        )
        return any(term in normalized for term in incident_terms)

    def failure_label(self, question: str, category: str) -> str:
        normalized = self._normalize(question)
        labels = (
            ("Alarmas PEEP", ("peep",)),
            ("Pantalla tactil", ("pantalla tactil", "touch", "display", "pantalla")),
            ("Sensor flujo", ("sensor de flujo", "flujo")),
            ("No enciende", ("no enciende", "energia", "alimentacion")),
            ("Bateria / carga", ("bateria", "carga")),
            ("Calibracion", ("calibr",)),
            ("Presion", ("presion",)),
        )
        for label, terms in labels:
            if any(term in normalized for term in terms):
                return label
        return category

    def profile_label(self, profile: str) -> str:
        normalized = self._normalize(profile)
        if normalized == "operador":
            return "Operadores"
        if normalized == "tecnico":
            return "Técnicos"
        return "Sin perfil"

    def _all_consultations(self) -> list[sqlite3.Row]:
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT *
                FROM consultations
                WHERE date >= ?
                ORDER BY date DESC, time DESC, id DESC
                """,
                (self._retention_cutoff(365),),
            ).fetchall()

    def _counter_items(self, counter: Counter[str]) -> list[dict[str, Any]]:
        return [
            {"label": label or "Sin dato", "count": count}
            for label, count in counter.most_common()
        ]

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS consultations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    chat_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    profile TEXT NOT NULL,
                    user_service TEXT NOT NULL,
                    equipment_id TEXT NOT NULL,
                    equipment_name TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    category TEXT NOT NULL,
                    es_incidente INTEGER NOT NULL DEFAULT 0,
                    incident_candidate INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            self._ensure_column(connection, "consultations", "chat_id", "TEXT NOT NULL DEFAULT ''")
            connection.execute(
                """
                UPDATE consultations
                SET chat_id = session_id
                WHERE chat_id = ''
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    consultation_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    user_service TEXT NOT NULL,
                    equipment_id TEXT NOT NULL,
                    equipment_name TEXT NOT NULL,
                    question TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (consultation_id) REFERENCES consultations(id)
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_consultations_dashboard
                ON consultations (date, equipment_name, username, category)
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_consultations_user
                ON consultations (username, date, time)
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_consultations_user_chat
                ON consultations (username, chat_id, id)
                """
            )

    def _ensure_column(
        self,
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
        definition: str,
    ) -> None:
        columns = {
            row["name"]
            for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in columns:
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _normalize(self, value: str) -> str:
        without_accents = unicodedata.normalize("NFKD", value or "")
        ascii_text = without_accents.encode("ascii", "ignore").decode("ascii")
        compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_text).strip().lower()
        return re.sub(r"\s+", " ", compact)

    def _retention_cutoff(self, days: int) -> str:
        return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
