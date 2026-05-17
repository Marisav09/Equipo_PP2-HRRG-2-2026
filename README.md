# Asistente IA para Ingenieria Clinica HRRG

Sistema web local basado en arquitectura RAG para asistir al area de Ingenieria Clinica del Hospital Regional Rio Grande. El objetivo del prototipo es permitir que el personal tecnico consulte manuales oficiales de equipamiento medico y reciba respuestas con respaldo documental, trazabilidad de fuentes y mecanismos de contingencia cuando el modelo local no se encuentre disponible o demore demasiado.

## Estado del prototipo

Habiendo decidido implementar un sistema híbrido (combinación de ChromaDB con LLM mediante RAG) y sumar la memoria conversacional, el prototipo inicial evolucionó hacia una solución más robusta.  
Se procedió a transformar la estructura centralizada en una arquitectura modular, mantenible y escalable, y se enriqueciò con nuevas funcionalidades que amplían significativamente el alcance del sistema.  

Actualmente, incluye:

- Backend Flask organizado por capas.  
- Servicios separados para ingesta documental, búsqueda vectorial, generación RAG, memoria, auditoría y tickets.  
- Base vectorial local con ChromaDB.  
- Modelos locales mediante Ollama.  
- Interfaz web premium en HTML, CSS y Vanilla JavaScript, con tarjetas dinámicas y selección de equipo.  
- Fallback documental para garantizar que el técnico siempre reciba respuesta, incluso si el LLM falla o demora.  
- Detección de imágenes en manuales y redirección al PDF original para complementar la explicación textual.  
- OCR opcional para integrar manuales escaneados.  
- Entrada y salida por voz desde el navegador.  
- Sistema de tickets automático y manual para escalar consultas sin respuesta.  
- Auditoría técnica completa con registro de consultas, respuestas, fuentes y equipos.  
- Memoria conversacional por sesión para interpretar referencias contextuales.  

## Tecnologias principales

- Python
- Flask
- LangChain
- ChromaDB
- Ollama
- Modelo LLM local: `llama3.2:3b`
- Modelo de embeddings local: `nomic-embed-text`
- PyMuPDF
- SQLite
- HTML, CSS moderno y Vanilla JavaScript
- APIs del navegador para entrada y salida por voz

## Arquitectura

```text
Equipo_PP2-HRRG-2-2026/
  app/
    api/
      routes.py
    core/
      config.py
      exceptions.py
      logging_config.py
    models/
      schemas.py
    services/
      audit_service.py
      ingestion_service.py
      memory_service.py
      rag_service.py
      ticket_service.py
      vectorstore_service.py
  data/
    raw/
    chroma/
    audit/
    tickets/
  docs/
    archive/
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

## Funcionalidades implementadas

### 1. Refactorizacion modular

Se separo la logica principal en modulos especializados:

- `app/api/routes.py`: rutas HTTP de Flask.
- `app/core/config.py`: configuracion centralizada desde variables de entorno.
- `app/core/logging_config.py`: logging profesional con archivo rotativo.
- `app/core/exceptions.py`: excepciones controladas del dominio.
- `app/services/ingestion_service.py`: procesamiento e ingesta de PDFs.
- `app/services/vectorstore_service.py`: conexion y consultas a ChromaDB.
- `app/services/rag_service.py`: orquestacion RAG, LLM y fallback.
- `app/services/memory_service.py`: memoria conversacional por sesion.
- `app/services/audit_service.py`: auditoria de consultas y respuestas.
- `app/services/ticket_service.py`: gestion de tickets.
- `app/models/schemas.py`: estructuras tipadas para respuestas, fuentes y tickets.

### 2. Configuracion con `.env`

Se agrego `.env.example` para manejar rutas, modelos y parametros del sistema sin dejar valores hardcodeados en el codigo.

Variables principales:

```env
RAW_DOCUMENTS_DIR=data/raw
VECTORSTORE_DIR=data/chroma
AUDIT_DB_PATH=data/audit/queries.sqlite3
TICKETS_DB_PATH=data/tickets/tickets.sqlite3
LOGS_DIR=logs
COLLECTION_NAME=manuales_hrrg
OLLAMA_BASE_URL=http://127.0.0.1:11434
LLM_MODEL=llama3.2:3b
EMBEDDING_MODEL=nomic-embed-text
CHUNK_SIZE=1000
CHUNK_OVERLAP=180
RETRIEVAL_K=4
EMBEDDING_BATCH_SIZE=4
LLM_TIMEOUT_SECONDS=300
MEMORY_WINDOW_MESSAGES=6
OLLAMA_HEALTH_TIMEOUT_SECONDS=3
ENABLE_OCR=false
TECHNICAL_USER_PASSWORD=tecnico-hrrg
ADMIN_USER_PASSWORD=admin-hrrg
```

### 3. Ingesta multi-documento

El sistema procesa multiples archivos PDF desde `data/raw`.

Durante la ingesta:

- Extrae texto pagina por pagina.
- Divide el contenido en chunks.
- Conserva metadatos de trazabilidad:
  - nombre del documento,
  - pagina,
  - identificador de chunk,
  - indicador de presencia de imagenes,
  - cantidad de imagenes detectadas.
- Genera embeddings con Ollama.
- Guarda los fragmentos en ChromaDB.

El script principal es:

```powershell
python scripts/ingest_documents.py
```

### 4. RAG con modelos locales

El flujo RAG implementado es:

1. El usuario realiza una consulta tecnica.
2. El sistema recupera fragmentos relevantes desde ChromaDB.
3. Los fragmentos se incorporan al prompt del LLM.
4. Ollama genera una respuesta usando solo el contexto documental recuperado.
5. La respuesta se devuelve con fuentes.
6. La consulta queda registrada para auditoria.

El modelo configurado por defecto es:

```text
llama3.2:3b
```

El modelo de embeddings es:

```text
nomic-embed-text
```

### 5. Sistema hibrido con fallback documental

Se implemento un mecanismo para que el tecnico no quede sin respuesta.

Si el LLM:

- no esta disponible,
- falla,
- se demora demasiado,
- o el usuario decide no esperar,

el sistema puede devolver una respuesta documental basada directamente en los fragmentos recuperados desde ChromaDB.

El fallback informa la situacion y muestra extractos relevantes con sus fuentes.

Tambien se agrego soporte para que el frontend pueda solicitar explicitamente una respuesta documental sin esperar a la generacion completa del LLM.

### 6. Memoria conversacional

Se agrego memoria por sesion mediante SQLite.

Esto permite resolver preguntas de seguimiento como:

```text
Usuario: Estoy consultando el proyecto del Hospital Regional Rio Grande. Cual es su finalidad?
Usuario: Y que area del hospital participa?
```

El sistema conserva los ultimos mensajes de la sesion y los utiliza para interpretar referencias como:

- "eso",
- "ese equipo",
- "la alarma anterior",
- "lo que te pregunte recien".

La memoria se limpia cuando el usuario inicia un nuevo chat o selecciona otro equipo.

Endpoint relacionado:

```text
POST /memory/clear
```

### 7. Auditoria tecnica

Cada consulta queda registrada en SQLite con:

- fecha y hora,
- pregunta,
- respuesta,
- modo de respuesta (`llm`, `fallback`, `ticket`),
- equipo seleccionado,
- fuentes utilizadas,
- ticket asociado si corresponde.

Endpoint de administrador:

```text
GET /admin/audit?password=admin-hrrg
```

### 8. Gestion de tickets

El sistema permite crear tickets de dos formas:

- automaticamente, cuando no hay base documental o no se recupera evidencia suficiente;
- manualmente, desde la interfaz del tecnico.

Cada ticket registra:

- pregunta o descripcion,
- equipo,
- motivo,
- estado,
- fecha de creacion.

Endpoint de administrador:

```text
GET /admin/tickets?password=admin-hrrg
```

Endpoint para crear ticket:

```text
POST /tickets
```

### 9. Soporte para imagenes en manuales

Durante la ingesta, el sistema detecta si una pagina contiene imagenes o esquemas.

Si una fuente contiene imagenes, la respuesta orienta al tecnico a revisar visualmente la pagina del PDF original.

Tambien se dejo OCR opcional para manuales escaneados:

```env
ENABLE_OCR=true
```

Para usar OCR es necesario instalar Tesseract en el sistema operativo y contar con las dependencias Python correspondientes.

### 10. Fuentes y trazabilidad

Las respuestas incluyen fuentes con:

- documento,
- pagina,
- chunk,
- indicador de imagenes cuando corresponde.

Ademas, se agrego soporte backend para servir manuales PDF desde:

```text
GET /manuals/<archivo.pdf>
```

La idea es que las citas puedan abrir directamente el PDF en la pagina correspondiente usando enlaces con formato:

```text
/manuals/manual.pdf#page=3
```

Esto apunta a una experiencia similar a NotebookLM, donde la respuesta no solo menciona la fuente, sino que permite acceder rapidamente al documento original.

### 11. Interfaz web premium

Se refactorizo la interfaz en:

- `templates/index.html`
- `static/css/styles.css`
- `static/js/chat.js`

Mejoras visuales:

- layout tipo aplicacion de chat;
- panel lateral con historial;
- tarjetas dinamicas con hover;
- sombras suaves;
- bordes redondeados modernos;
- efecto glassmorphism;
- modal de seleccion de equipo;
- botones con iconos SVG;
- diseno responsive.

Mejoras funcionales:

- seleccion dinamica del equipo;
- actualizacion de `#active-equipment`;
- reinicio de memoria al iniciar nuevo chat;
- envio de consultas al endpoint `/ask`;
- creacion manual de tickets;
- ingesta desde interfaz;
- boton de microfono integrado en la caja de input.

### 12. Entrada y salida por voz

Se incorporo entrada por voz usando:

```javascript
SpeechRecognition || webkitSpeechRecognition
```

Funcionamiento:

1. El usuario presiona el boton del microfono.
2. El boton cambia visualmente de estado.
3. El navegador escucha la consulta.
4. Al finalizar, el texto reconocido se inserta automaticamente en el input.

Tambien se incorporo salida por voz con:

```javascript
SpeechSynthesisUtterance
```

Esto permite que las respuestas puedan ser leidas en voz alta desde el navegador.

## Endpoints disponibles

```text
GET  /
POST /ask
POST /requests/cancel
POST /memory/clear
POST /ingest
POST /tickets
GET  /manuals/<archivo.pdf>
GET  /admin/audit?password=admin-hrrg
GET  /admin/tickets?password=admin-hrrg
```

## Puesta en marcha

### 1. Crear entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Crear archivo `.env`

```powershell
Copy-Item .env.example .env
```

### 4. Preparar Ollama

En una terminal:

```powershell
ollama serve
```

En otra terminal:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 5. Cargar manuales

Copiar los manuales PDF en:

```text
data/raw
```

### 6. Indexar documentos

```powershell
python scripts/ingest_documents.py
```

### 7. Ejecutar la aplicacion

```powershell
python run.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Pruebas realizadas

Se verifico:

- carga correcta de la aplicacion Flask;
- registro de rutas principales;
- ingesta de PDFs desde `data/raw`;
- creacion de chunks en ChromaDB;
- respuesta con LLM local;
- fallback documental cuando el LLM falla o demora;
- memoria conversacional por sesion;
- creacion de tickets automaticos y manuales;
- renderizado de la interfaz web;
- seleccion dinamica de equipos desde el modal;
- endpoint de limpieza de memoria.

## Limpieza y organizacion del proyecto

Se movieron prototipos y archivos anteriores a:

```text
scripts/legacy
docs/archive
```

Esto permite conservar el historial de desarrollo sin mezclarlo con el codigo principal actual.

Tambien se reorganizaron los PDFs de manuales dentro de:

```text
data/raw
```

## Consideraciones actuales

- Las respuestas con LLM local pueden demorar dependiendo del rendimiento de Ollama y del equipo donde se ejecute.
- El fallback documental permite mantener disponibilidad cuando el LLM no responde.
- El OCR esta preparado como funcionalidad opcional, pero requiere instalacion externa de Tesseract.
- La autenticacion de administrador esta en una version inicial por password en query param; en una version productiva deberia reemplazarse por login seguro con sesiones y roles.
- La UI ya tiene estructura para evolucionar hacia un panel administrativo mas completo.

## Proximas mejoras sugeridas

- Panel administrador visual para estadisticas, auditoria, usuarios, equipos y mantenimiento.
- Login diferenciado para tecnico y administrador.
- Gestion completa de usuarios y roles.
- Visualizador embebido de PDF dentro de la aplicacion.
- Citas interactivas con vista previa del fragmento citado.
- Cancelacion mas robusta de procesos LLM en ejecucion.
- Exportacion de auditoria y tickets.
- Tests automatizados de backend y frontend.
- Dockerizacion del entorno.
- Integracion con inventario de equipos del hospital.

## Resumen para informe de avance

Durante esta etapa se refactorizo el prototipo inicial del Asistente IA para Ingenieria Clinica, transformandolo en una aplicacion modular basada en Flask, LangChain, ChromaDB y Ollama. Se separaron responsabilidades en servicios independientes, se incorporo configuracion mediante variables de entorno, logging, auditoria, memoria conversacional, sistema de tickets y un flujo RAG hibrido con fallback documental.

Ademas, se mejoro la experiencia de usuario mediante una interfaz web moderna, responsive e interactiva, con seleccion dinamica de equipos, entrada por voz, salida por voz, historial visual, tarjetas dinamicas y una caja de consulta similar a aplicaciones de mensajeria. El sistema permite procesar multiples manuales PDF, conservar metadatos de trazabilidad y responder consultas tecnicas basandose en documentos oficiales, manteniendo siempre una alternativa documental cuando el modelo generativo local no se encuentra disponible.
