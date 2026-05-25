from __future__ import annotations

import csv
import json
import urllib.request
from pathlib import Path


API_URL = "http://127.0.0.1:5000/ask"
OUTPUT_PATH = Path("reports/validacion_recuperacion_por_equipo.csv")


TEST_CASES = [
    {
        "equipo": "Respirador Drager VN500",
        "query": "Que informacion contiene el manual del VN500?",
        "expected_terms": ["drager", "vn500", "babyflow", "ps500", "gs500"],
    },
    {
        "equipo": "Esterilizadora Sterrad 100",
        "query": "Que informacion contiene el manual del Sterrad 100?",
        "expected_terms": ["sterrad"],
    },
    {
        "equipo": "Maquina de dialisis Fresenius 4008",
        "query": "Que informacion contiene el manual de la Fresenius 4008?",
        "expected_terms": ["fresenius", "4008"],
    },
    {
        "equipo": "Procesador Leica TP1020",
        "query": "Que informacion contiene el manual del Leica TP1020?",
        "expected_terms": ["leica", "tp1020", "tp_1020"],
    },
    {
        "equipo": "Desfibrilador Mindray BeneHeart D3",
        "query": "Que informacion contiene el manual del desfibrilador BeneHeart D3?",
        "expected_terms": ["desfibrilador", "beneheart", "d3", "mindray"],
    },
    {
        "equipo": "Bilirrubinometro Drager JM-105",
        "query": "Que informacion contiene el manual del bilirrubinometro JM-105?",
        "expected_terms": ["bilirrubinometro", "jm105", "jm_105", "drager"],
    },
    {
        "equipo": "Incubadora Medix",
        "query": "Que informacion contiene el manual de la incubadora Medix?",
        "expected_terms": ["incubadora", "medix", "tr200", "tr306", "natal"],
    },
    {
        "equipo": "Ventilador Neumovent GraphNet",
        "query": "Que informacion contiene el manual del Neumovent GraphNet?",
        "expected_terms": ["neumovent", "graphnet", "neo"],
    },
    {
        "equipo": "Ventilador Maquet Servo-i",
        "query": "Que informacion contiene el manual del Maquet Servo-i?",
        "expected_terms": ["maquet", "servo"],
    },
    {
        "equipo": "Ventilador Engstrom",
        "query": "Que informacion contiene el manual del ventilador Engstrom?",
        "expected_terms": ["engstrom", "carestation"],
    },
]


def post_ask(query: str, equipment: str) -> dict:
    payload = {
        "query": query,
        "equipment": equipment,
        "force_fallback": True,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def extract_sources(response: dict) -> list[dict]:
    sources = response.get("sources") or []

    if isinstance(sources, dict):
        sources = [sources]

    if not isinstance(sources, list):
        return []

    return sources


def source_matches_expected(source_file: str, expected_terms: list[str]) -> bool:
    normalized = source_file.lower()
    return any(term.lower() in normalized for term in expected_terms)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for case in TEST_CASES:
        equipo = case["equipo"]
        query = case["query"]
        expected_terms = case["expected_terms"]

        print(f"Probando: {equipo}")

        try:
            response = post_ask(query=query, equipment=equipo)
            sources = extract_sources(response)

            if not sources:
                rows.append(
                    {
                        "equipo": equipo,
                        "query": query,
                        "source_file": "",
                        "page": "",
                        "match": "NO",
                        "observacion": "No devolvio fuentes",
                    }
                )
                continue

            for source in sources:
                source_file = str(source.get("source_file", ""))
                page = source.get("page", "")
                match = source_matches_expected(source_file, expected_terms)

                rows.append(
                    {
                        "equipo": equipo,
                        "query": query,
                        "source_file": source_file,
                        "page": page,
                        "match": "SI" if match else "NO",
                        "observacion": "" if match else "Fuente potencialmente mezclada o clasificacion a revisar",
                    }
                )

        except Exception as exc:
            rows.append(
                {
                    "equipo": equipo,
                    "query": query,
                    "source_file": "",
                    "page": "",
                    "match": "ERROR",
                    "observacion": str(exc),
                }
            )

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "equipo",
                "query",
                "source_file",
                "page",
                "match",
                "observacion",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Reporte generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()