# Asistente IA para Ingenieria Clinica HRRG

Sistema web local basado en arquitectura RAG para asistir al area de Ingenieria Clinica del Hospital Regional Rio Grande. El prototipo consulta manuales oficiales de equipamiento medico con trazabilidad de fuentes, aislamiento estricto por equipo y fallback documental cuando el modelo local no responde.

## Stack principal

- Backend Flask organizado por capas.
- ChromaDB como base vectorial local.
- SQLite para memoria conversacional.
- LangChain, PyMuPDF y Ollama.
- Modelo LLM local: `llama3.2:3b`.
- Modelo de embeddings local: `nomic-embed-text`.
- Frontend HTML, CSS y Vanilla JavaScript.
- Entrada y salida por voz con APIs del navegador.

## Arquitectura

```text
Equipo_PP2-HRRG-2-2026/
  app/
    api/
      routes.py
    core/
      config.py
      equipment_catalog.py
      exceptions.py
      logging_config.py
    models/
      schemas.py
    services/
      ingestion_service.py
      memory_service.py
      rag_service.py
      vectorstore_service.py
  data/
    raw/
    chroma/
    memory/
  scripts/
    ingest_documents.py
    build_vectorstore.py
    legacy/
  static/
    css/styles.css
    js/chat.js
  templates/
    index.html
  app.py
  run.py
  requirements.txt
  .env.example
```

## Guardrails

- El RAG recupera documentos usando filtro duro por metadatos: `equipo`.
- Si no hay chunks para el equipo seleccionado, el sistema no inventa respuestas.
- Si Ollama falla o excede el timeout, se activa fallback documental con extractos recuperados desde ChromaDB.
- Las respuestas deben estar en español y basarse únicamente en los manuales indexados.
- El rol operador recibe instrucciones concisas, sin fuentes visibles.
- El rol técnico recibe respuestas detalladas con sección de fuentes.

## Ingesta

Los PDFs se colocan en:

```text
data/raw
```

La ingesta:

- extrae texto por pagina;
- detecta imagenes o esquemas;
- divide el contenido en chunks;
- infiere el equipo desde ruta, nombre de archivo o primeras paginas;
- guarda cada chunk con metadatos de trazabilidad, incluyendo `equipo`;
- omite documentos que no pueda asociar a un equipo para evitar contaminacion entre manuales;
- reemplaza versiones anteriores del mismo PDF antes de reindexar.

Ejecutar:

```powershell
python scripts/ingest_documents.py
```

## Flujo RAG

1. El usuario selecciona un equipo o ingresa desde un QR con `?equipo=...&rol=operador`.
2. El backend normaliza el nombre del equipo con `equipment_catalog.py`.
3. ChromaDB recupera fragmentos usando `filter={"equipo": equipo}`.
4. El LLM local redacta una respuesta usando solo el contexto recuperado.
5. Si el LLM no responde, se devuelve fallback documental.
6. La memoria conversacional se guarda por sesion para resolver referencias como "eso" o "la alarma anterior".

## Endpoints

```text
GET  /
POST /ask
POST /requests/cancel
POST /memory/clear
POST /ingest
GET  /manuals/<archivo.pdf>
```

## Puesta en marcha

Crear entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

Preparar Ollama:

```powershell
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Indexar documentos:

```powershell
python scripts/ingest_documents.py
```

Ejecutar la aplicacion:

```powershell
python run.py
```

Abrir:

```text
http://127.0.0.1:5000
```

## Estado actual

La interfaz muestra solo equipos realmente indexados en ChromaDB, por lo que no aparecen modelos ficticios que no existan en `data/raw`.
