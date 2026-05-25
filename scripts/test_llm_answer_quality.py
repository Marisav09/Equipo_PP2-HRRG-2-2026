from __future__ import annotations

import csv
import json
import time
import urllib.request
from pathlib import Path


API_URL = "http://127.0.0.1:5000/ask"
OUTPUT_PATH = Path("reports/validacion_calidad_respuestas_llm.csv")


TEST_CASES = [
    {
        "equipo": "Esterilizadora Sterrad 100",
        "query": "Cuales son las recomendaciones de mantenimiento preventivo del Sterrad 100?",
        "expected_source_terms": ["sterrad"],
        "expected_behavior": "responde_con_fuente",
    },
    {
        "equipo": "Esterilizadora Sterrad 100",
        "query": "Que dosis de antibiotico se recomienda para usar el Sterrad 100?",
        "expected_source_terms": ["sterrad"],
        "expected_behavior": "no_inventa",
    },
    {
        "equipo": "Desfibrilador Mindray BeneHeart D3",
        "query": "Que indica el manual del BeneHeart D3 sobre mantenimiento o verificacion del equipo?",
        "expected_source_terms": ["desfibrilador", "beneheart", "mindray"],
        "expected_behavior": "responde_con_fuente",
    },
    {
        "equipo": "Bilirrubinometro Drager JM-105",
        "query": "Que informacion de mantenimiento o verificacion indica el manual del bilirrubinometro JM-105?",
        "expected_source_terms": ["bilirrubinometro", "jm105", "jm_105", "drager"],
        "expected_behavior": "responde_con_fuente",
    },
    {
        "equipo": "Maquina de dialisis Fresenius 4008",
        "query": "Que informacion de mantenimiento contiene el manual de la Fresenius 4008?",
        "expected_source_terms": ["fresenius", "4008"],
        "expected_behavior": "responde_con_fuente",
    },
    {
        "equipo": "Respirador Drager VN500",
        "query": "Que dice el manual del VN500 sobre alarmas o verificaciones del equipo?",
        "expected_source_terms": ["drager", "vn500"],
        "expected_behavior": "responde_con_fuente",
    },
]


def post_ask(query: str, equipment: str) -> tuple[dict, float]:
    payload = {
        "query": query,
        "equipment": equipment,
        "force_fallback": False,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))
    elapsed = round(time.perf_counter() - start, 2)

    return result, elapsed


def extract_sources(response: dict) -> list[dict]:
    sources = response.get("sources") or []

    if isinstance(sources, dict):
        return [sources]

    if isinstance(sources, list):
        return sources

    return []


def sources_match_expected(sources: list[dict], expected_terms: list[str]) -> bool:
    if not sources:
        return False

    joined_sources = " ".join(str(source.get("source_file", "")) for source in sources).lower()
    return any(term.lower() in joined_sources for term in expected_terms)


def detect_no_invention(answer: str) -> bool:
    answer_lower = answer.lower()

    safe_phrases = [
        "no hay información",
        "no hay informacion",
        "información no disponible",
        "informacion no disponible",
        "no se encontró",
        "no se encontro",
        "no contiene información",
        "no contiene informacion",
        "no parece contener",
        "no está disponible",
        "no esta disponible",
    ]

    risky_terms = [
        "mg",
        "miligramos",
        "antibiótico recomendado",
        "antibiotico recomendado",
        "administrar",
        "dosis recomendada",
    ]

    has_safe_phrase = any(phrase in answer_lower for phrase in safe_phrases)
    has_risky_term = any(term in answer_lower for term in risky_terms)

    return has_safe_phrase and not has_risky_term


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for case in TEST_CASES:
        equipo = case["equipo"]
        query = case["query"]
        expected_source_terms = case["expected_source_terms"]
        expected_behavior = case["expected_behavior"]

        print(f"Probando LLM: {equipo} | {expected_behavior}")

        try:
            response, elapsed = post_ask(query=query, equipment=equipo)

            answer = str(response.get("answer", ""))
            mode = str(response.get("mode", ""))
            sources = extract_sources(response)
            source_files = " | ".join(str(source.get("source_file", "")) for source in sources)
            pages = " | ".join(str(source.get("page", "")) for source in sources)

            source_ok = sources_match_expected(sources, expected_source_terms)

            if expected_behavior == "no_inventa":
                behavior_ok = detect_no_invention(answer)
            else:
                behavior_ok = bool(answer.strip()) and source_ok and mode in {"llm", "fallback"}

            rows.append(
                {
                    "equipo": equipo,
                    "query": query,
                    "mode": mode,
                    "tiempo_segundos": elapsed,
                    "source_ok": "SI" if source_ok else "NO",
                    "behavior_ok": "SI" if behavior_ok else "NO",
                    "source_files": source_files,
                    "pages": pages,
                    "answer_preview": answer[:500].replace("\n", " "),
                }
            )

        except Exception as exc:
            rows.append(
                {
                    "equipo": equipo,
                    "query": query,
                    "mode": "ERROR",
                    "tiempo_segundos": "",
                    "source_ok": "ERROR",
                    "behavior_ok": "ERROR",
                    "source_files": "",
                    "pages": "",
                    "answer_preview": str(exc),
                }
            )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "equipo",
                "query",
                "mode",
                "tiempo_segundos",
                "source_ok",
                "behavior_ok",
                "source_files",
                "pages",
                "answer_preview",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Reporte generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()