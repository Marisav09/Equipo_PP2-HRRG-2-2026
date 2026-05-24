# Asistente IA HRRG

Sistema web local para asistencia en Ingenieria Clinica del Hospital Regional Rio Grande.

## Primera etapa

Esta base contiene:

- Aplicacion Flask modular.
- Rutas separadas para operador, tecnico, autenticacion, chat, equipos e ingesta.
- Catalogo inicial de equipos.
- Prompts por rol.
- Guardrail inicial que exige equipo exacto antes de responder.
- Frontend inicial separado por perfil.

## Ejecucion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Luego abrir:

- Tecnico: `http://localhost:5000/login`
- Operador: `http://localhost:5000/equipo/sterrad-100`

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Ingesta

Copiar manuales PDF a `data/raw` y ejecutar:

```powershell
.\.venv\Scripts\python.exe scripts\ingest_documents.py
```

## Codigos QR

Generar QR para todos los equipos:

```powershell
.\.venv\Scripts\python.exe scripts\generate_qr.py --base-url http://127.0.0.1:5000
```

Generar QR para un equipo:

```powershell
.\.venv\Scripts\python.exe scripts\generate_qr.py --equipment-id sterrad-100 --base-url http://127.0.0.1:5000
```

## Diagnostico

```powershell
.\.venv\Scripts\python.exe scripts\check_system.py
```

Endpoint:

```text
GET /api/system/health
```
