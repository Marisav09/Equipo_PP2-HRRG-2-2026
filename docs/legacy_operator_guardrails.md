# Guardrails anteriores del modo operador

Referencia no ejecutable conservada para una posible reimplementacion.

El flujo anterior bloqueaba una consulta antes de recuperar documentos cuando la pregunta
contenia alguna de estas frases normalizadas:

```python
(
    "paciente conectado",
    "paciente conectada",
    "bebe dentro",
    "tratamiento en curso",
    "dialisis activa",
    "ventilacion activa",
    "ventilando al paciente",
)
```

Tambien eliminaba lineas de la respuesta cuando contenian terminos fijos relacionados con
apertura, desarme, calibracion, reemplazo de piezas, menus de servicio o mediciones internas.

Estos mecanismos fueron retirados del flujo porque dependian de coincidencias literales, no
comprendian escenarios equivalentes expresados de otra forma y podian eliminar una linea sin
evaluar el riesgo de la accion completa.

## Implementacion retirada

```python
def _mentions_patient_connected(self, question: str) -> bool:
    normalized = self._normalize_for_match(question)
    return any(
        phrase in normalized
        for phrase in (
            "paciente conectado",
            "paciente conectada",
            "bebe dentro",
            "tratamiento en curso",
            "dialisis activa",
            "ventilacion activa",
            "ventilando al paciente",
        )
    )


def _strip_prohibited_operator_instructions(self, answer: str) -> str:
    prohibited = (
        "abra la tapa",
        "abra el gabinete",
        "abra la carcasa",
        "abrir la tapa",
        "abrir el gabinete",
        "abrir la carcasa",
        "desarm",
        "retirar la tapa",
        "extraer el modulo",
        "extraer la placa",
        "menu de servicio",
        "menu tecnico",
        "modo servicio",
        "calibr",
        "reemplaz",
        "cambiar el fusible",
        "medir tension",
        "medir voltaje",
        "medir corriente",
        "mida tension",
        "mida voltaje",
        "mida corriente",
        "placa electronica",
        "circuito interno",
        "cable interno",
    )
    safe_lines = [
        line
        for line in answer.splitlines()
        if not any(term in self._normalize_for_match(line) for term in prohibited)
    ]
    return "\n".join(safe_lines).strip()
```
