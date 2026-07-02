# Asistente IA para Ingenieria Clinica HRRG

![Pantalla principal del Asistente IA para Ingenieria Clinica HRRG](static/img/pantalla%20principal.png)

Sistema web local basado en arquitectura RAG para asistir al area de Ingenieria Clinica del Hospital Regional Rio Grande. El prototipo consulta manuales oficiales de equipamiento medico con trazabilidad de fuentes, aislamiento estricto por equipo y fallback documental cuando el modelo local no responde.

## Indice

- [Stack principal](#stack-principal)
- [Arquitectura](#arquitectura)
- [Guardrails](#guardrails)
- [Ingesta](#ingesta)
- [Flujo RAG](#flujo-rag)
- [Reconstruccion parent-child](#reconstruccion-parent-child)
- [Endpoints](#endpoints)
- [Pruebas de preguntas RAG](#pruebas-de-preguntas-rag)
- [Requisitos minimos de la computadora servidor](#requisitos-minimos-de-la-computadora-servidor)
- [Puesta en marcha](#puesta-en-marcha)
- [Estado actual](#estado-actual)

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

Por defecto, este comando reconstruye el indice con arquitectura parent-child:
chunks hijos para busqueda y paginas padre completas para expansion de contexto.
Si se quiere conservar el comportamiento incremental y omitir Markdown sin cambios,
usar:

```powershell
python scripts/ingest_documents.py --incremental
```

## Flujo RAG

1. El usuario selecciona un equipo o ingresa desde un QR con `?equipo=...&rol=operador`.
2. El backend normaliza el nombre del equipo con `equipment_catalog.py`.
3. ChromaDB recupera candidatos semanticos usando aislamiento estricto por equipo.
4. BM25 agrega candidatos y peso por similitud lexica.
5. Un cross-encoder local rerankea los candidatos combinando peso semantico, lexico y reranker.
6. Para operador se entregan fragmentos breves y se evalua el resto de la pagina y paginas adyacentes.
7. Para tecnico se entrega la pagina completa mas relevante, truncada alrededor de la coincidencia solo si supera el presupuesto.
8. El LLM local redacta una respuesta usando solo el contexto recuperado.
9. Si el LLM no responde, se devuelve fallback documental.
10. La memoria conversacional se guarda por sesion para resolver referencias como "eso" o "la alarma anterior".

## Reconstruccion parent-child

La arquitectura de recuperacion usa dos colecciones sincronizadas:

- `manuales_hrrg`: chunks hijos breves usados para busqueda.
- `manuales_hrrg_pages`: paginas padre completas usadas para ampliar contexto.

Despues de instalar las dependencias, reconstruir el indice:

```powershell
pip install -r requirements.txt
python scripts/ingest_documents.py
```

El primer uso del reranker puede descargar el modelo configurado en `RERANKER_MODEL`.
Por defecto `RERANKER_DEVICE=auto`: utiliza CUDA si esta disponible y, en caso contrario,
utiliza CPU. Tambien puede forzarse `cuda` o `cpu` desde `.env`.

Los pesos y cantidades de candidatos pueden ajustarse desde `.env`:

```text
SEMANTIC_WEIGHT=0.30
LEXICAL_WEIGHT=0.20
RERANKER_WEIGHT=0.50
SEMANTIC_CANDIDATE_K=40
LEXICAL_CANDIDATE_K=40
RERANKER_CANDIDATE_K=60
```

## Endpoints

```text
GET  /
POST /ask
POST /requests/cancel
POST /memory/clear
POST /ingest
GET  /manuals/<archivo.pdf>
```

## Pruebas de preguntas RAG

Las preguntas base se editan en:

```text
scripts/rag_test_questions.json
```

Cada pregunta puede habilitarse o deshabilitarse con `enabled`. Para seleccionar
equipo y rol de forma interactiva:

```powershell
python scripts/run_rag_question_tests.py
```

Tambien puede ejecutarse sin interaccion:

```powershell
python scripts/run_rag_question_tests.py --equipment ventilador-engstrom --role operador
```

Opciones utiles:

```powershell
python scripts/run_rag_question_tests.py --list-equipment
python scripts/run_rag_question_tests.py --equipment ventilador-engstrom --role tecnico --questions scripts/rag_test_questions.json --output reports/prueba.csv
python scripts/run_rag_question_tests.py --equipment ventilador-engstrom --role tecnico --conversation
python scripts/run_rag_question_tests.py --equipment ventilador-engstrom --role tecnico --force-fallback
```

Para que los extractos en ingles se traduzcan al espanol cuando se activa un fallback,
descargue una vez el modelo traductor local:

```bash
python scripts/download_fallback_translation_model.py
```

La traduccion se ejecuta unicamente en respuestas fallback y nunca modifica los chunks
almacenados ni el contexto enviado al modelo principal.

Por defecto cada pregunta usa una sesion independiente. `--conversation` conserva
la memoria entre preguntas. El CSV incluye respuestas completas, modo de respuesta,
duracion, fuentes, paginas y errores. El script usa directamente el flujo RAG, por
lo que no requiere iniciar Flask; Ollama y los modelos locales si deben estar disponibles.

## Requisitos minimos de la computadora servidor

Estos requisitos corresponden a la computadora donde se instalaran y ejecutaran
Flask, ChromaDB, Ollama, el modelo `llama3.2:3b`, el modelo de embeddings y el
reranker local.

| Componente | Minimo operativo | Recomendado |
|---|---:|---:|
| Procesador | CPU de 64 bits, 4 nucleos | 6 a 8 nucleos modernos |
| Memoria RAM | 16 GB | 32 GB |
| Almacenamiento libre | 20 GB en SSD | 40 GB o mas en SSD/NVMe |
| Placa de video | GPU NVIDIA compatible con CUDA y 6 GB de VRAM | GPU NVIDIA compatible con CUDA y 8 GB o mas de VRAM |
| Sistema operativo | Windows 10/11 de 64 bits o Linux de 64 bits compatible con Ollama | Version estable y actualizada |
| Red | Conexion a la red local del hospital | Ethernet Gigabit |
| Internet | Necesaria durante la instalacion para descargar dependencias y modelos | No es necesaria para el uso local una vez instalado todo |

Tambien se requiere Python 3.10 o superior, Ollama y un navegador web actualizado.
La instalacion en un disco mecanico es posible, pero aumenta considerablemente los
tiempos de carga e indexacion, por lo que se considera necesario utilizar un SSD.

Una computadora con 8 GB de RAM puede no disponer de memoria suficiente para cargar
al mismo tiempo el modelo de lenguaje, el reranker y los servicios de la aplicacion.
Por ese motivo, 16 GB se establece como minimo para una operacion estable.

Para que el asistente sea funcional y mantenga tiempos de respuesta adecuados, se
requiere una GPU NVIDIA compatible con CUDA. Aunque tecnicamente los modelos pueden
ejecutarse mediante el procesador, el uso exclusivo de CPU provoca respuestas e
indexaciones considerablemente mas lentas y solo se considera apropiado para pruebas
o contingencias, no para la operacion habitual del sistema.

Las computadoras que accedan al asistente como clientes no necesitan ejecutar los
modelos. Solo requieren un navegador actualizado y acceso por red a la direccion del
servidor.

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
