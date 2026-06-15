from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.equipment_catalog import EQUIPMENT_CATALOG, Equipment, find_equipment_by_id
from app.core.logging_config import configure_logging
from app.services.rag_test_service import RagTestService, load_questions


DEFAULT_QUESTIONS = ROOT_DIR / "scripts" / "rag_test_questions.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ejecuta preguntas configurables contra el RAG y guarda las respuestas en CSV."
    )
    parser.add_argument("--equipment", help="ID del equipo. Use --list-equipment para ver opciones.")
    parser.add_argument("--role", choices=("operador", "tecnico"), help="Rol usado para las consultas.")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS, help="Archivo JSON de preguntas.")
    parser.add_argument("--output", type=Path, help="Ruta del CSV de salida.")
    parser.add_argument(
        "--conversation",
        action="store_true",
        help="Usa una sola sesion para todas las preguntas y conserva memoria entre ellas.",
    )
    parser.add_argument(
        "--force-fallback",
        action="store_true",
        help="Evalua solo recuperacion documental, sin pedir una respuesta al LLM.",
    )
    parser.add_argument("--list-equipment", action="store_true", help="Lista los IDs de equipos y termina.")
    return parser.parse_args()


def select_equipment(equipment_id: str | None) -> Equipment:
    if equipment_id:
        equipment = find_equipment_by_id(equipment_id)
        if equipment:
            return equipment
        raise ValueError(f"Equipo desconocido: {equipment_id}. Use --list-equipment.")

    print("Seleccione el equipo:")
    for index, equipment in enumerate(EQUIPMENT_CATALOG, start=1):
        print(f"{index:>2}. {equipment.name} [{equipment.id}]")
    selected = input("Numero de equipo: ").strip()
    try:
        return EQUIPMENT_CATALOG[int(selected) - 1]
    except (ValueError, IndexError) as exc:
        raise ValueError("Seleccion de equipo invalida.") from exc


def select_role(role: str | None) -> str:
    if role:
        return role
    selected = input("Rol (operador/tecnico): ").strip().lower()
    if selected not in {"operador", "tecnico"}:
        raise ValueError("El rol debe ser 'operador' o 'tecnico'.")
    return selected


def default_output_path(equipment_id: str, role: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return ROOT_DIR / "reports" / f"rag_test_{equipment_id}_{role}_{timestamp}.csv"


def main() -> int:
    args = parse_args()
    if args.list_equipment:
        for equipment in EQUIPMENT_CATALOG:
            print(f"{equipment.id}: {equipment.name}")
        return 0

    try:
        equipment = select_equipment(args.equipment)
        role = select_role(args.role)
        questions_path = args.questions if args.questions.is_absolute() else ROOT_DIR / args.questions
        questions = load_questions(questions_path)
    except (OSError, ValueError) as exc:
        print(f"Error de configuracion: {exc}", file=sys.stderr)
        return 2

    output_path = args.output or default_output_path(equipment.id, role)
    if not output_path.is_absolute():
        output_path = ROOT_DIR / output_path

    configure_logging()
    runner = RagTestService()
    print(f"Ejecutando {len(questions)} preguntas para {equipment.name} como {role}.")

    def report_progress(row: dict) -> None:
        status = "ERROR" if row["error"] else row["mode"]
        print(
            f"[{row['question_number']}/{len(questions)}] "
            f"{status} ({row['elapsed_seconds']} s): {row['question']}"
        )

    rows = runner.run(
        questions=questions,
        equipment_id=equipment.id,
        equipment_name=equipment.name,
        role=role,
        shared_session=args.conversation,
        force_fallback=args.force_fallback,
        on_result=report_progress,
    )
    runner.write_csv(rows, output_path)
    errors = sum(bool(row["error"]) for row in rows)
    print(f"Reporte generado: {output_path}")
    print(f"Resultados: {len(rows) - errors} correctos, {errors} con error.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
