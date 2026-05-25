from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


INPUT_CSV = Path("reports/auditoria_calidad_texto_pdfs.csv")
OUTPUT_MD = Path("reports/informe_auditoria_calidad_texto_pdfs.md")


def read_rows() -> list[dict]:
    with INPUT_CSV.open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def md_table(rows: list[dict]) -> str:
    if not rows:
        return "_Sin registros._\n"

    lines = [
        "| Archivo | Páginas | Caracteres extraídos | Promedio caracteres/página | Estado | Observación |",
        "|---|---:|---:|---:|---|---|",
    ]

    for row in rows:
        archivo = row.get("archivo", "")
        paginas = row.get("paginas", "")
        caracteres = row.get("caracteres_extraidos", "")
        promedio = row.get("promedio_caracteres_por_pagina", "")
        estado = row.get("estado", "")
        observacion = row.get("observacion", "")

        lines.append(
            f"| `{archivo}` | {paginas} | {caracteres} | {promedio} | {estado} | {observacion} |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    rows = read_rows()
    total = len(rows)

    counter = Counter(row.get("estado", "SIN_ESTADO") for row in rows)

    ok_rows = [row for row in rows if row.get("estado") == "OK"]
    revisar_rows = [row for row in rows if row.get("estado") == "REVISAR"]
    ocr_rows = [row for row in rows if row.get("estado") == "REQUIERE_OCR"]
    error_rows = [row for row in rows if row.get("estado") == "ERROR"]

    content = f"""# Informe de auditoría de calidad textual de PDFs

## Proyecto

Asistente IA para Ingeniería Clínica - HRRG  
Rama de trabajo: `curaduria-corpus-completo-julieta`

## Objetivo

Evaluar la calidad del texto extraíble de los PDFs cargados en `data/raw`, con el fin de identificar qué documentos pueden utilizarse directamente en el flujo RAG y cuáles requieren revisión u OCR previo.

La auditoría no modifica los archivos originales. Solo analiza el texto extraíble de cada PDF y genera una clasificación preliminar.

## Resumen general

| Indicador | Cantidad |
|---|---:|
| Total de PDFs auditados | {total} |
| OK | {counter.get("OK", 0)} |
| REVISAR | {counter.get("REVISAR", 0)} |
| REQUIERE_OCR | {counter.get("REQUIERE_OCR", 0)} |
| ERROR | {counter.get("ERROR", 0)} |

## Criterios utilizados

La clasificación se realizó a partir de la cantidad total de caracteres extraídos y del promedio de caracteres por página.

| Estado | Interpretación |
|---|---|
| OK | El PDF tiene texto extraíble suficiente para ingesta textual directa. |
| REVISAR | El PDF tiene texto extraíble parcial o bajo. Puede ser útil, pero conviene revisarlo manualmente. |
| REQUIERE_OCR | El PDF tiene texto insuficiente o nulo. Probablemente requiere OCR o tratamiento especial. |
| ERROR | El PDF no pudo abrirse o falló la extracción. |

## PDFs que requieren OCR

{md_table(ocr_rows)}

## PDFs a revisar manualmente

{md_table(revisar_rows)}

## PDFs con texto extraíble suficiente

{md_table(ok_rows)}

## PDFs con error de lectura

{md_table(error_rows)}

## Conclusión preliminar

La auditoría muestra que la mayoría de los PDFs del corpus tienen texto extraíble suficiente para funcionar dentro del flujo RAG. Sin embargo, se identificaron documentos con bajo o nulo texto extraíble que deberían tratarse con OCR o revisión manual antes de considerarlos plenamente válidos para recuperación semántica.

El OCR no debería aplicarse de forma masiva sobre los 72 PDFs, sino únicamente sobre los documentos marcados como `REQUIERE_OCR` y, si corresponde, sobre algunos casos `REVISAR` luego de evaluación manual.

## Próximos pasos sugeridos

1. Revisar manualmente los PDFs marcados como `REQUIERE_OCR`.
2. Confirmar si son documentos relevantes para el alcance del MVP.
3. Aplicar OCR solo a los PDFs necesarios.
4. Reingestar el corpus corregido.
5. Repetir la validación de recuperación por equipo.
6. Repetir la validación de calidad de respuestas LLM.
"""

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(content, encoding="utf-8")

    print(f"Informe generado: {OUTPUT_MD}")


if __name__ == "__main__":
    main()