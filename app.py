from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pathlib import Path
import os
import time
import json
import re
import unicodedata


# ============================================================
# 1. Carga explícita de configuración
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Carga el .env de la carpeta del proyecto y pisa variables previas si existen
load_dotenv(dotenv_path=ENV_PATH, override=True)

app = Flask(__name__)


# ============================================================
# 2. Configuración general desde variables de entorno
# ============================================================

USE_LLM_RAW = os.getenv("USE_LLM", "true")
USE_LLM = USE_LLM_RAW.strip().lower() == "true"

LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "8"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Por compatibilidad, se mantiene MANUAL_PATH para pruebas con un único PDF.
MANUAL_PATH = os.getenv("MANUAL_PATH", "manual.pdf")

# Carpeta para ingesta de múltiples manuales.
MANUALS_DIR = os.getenv("MANUALS_DIR", "./data/manuales")

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))

# Archivo textual usado para fallback 2 cuando falla Ollama/embeddings/Chroma
CHUNKS_JSON_PATH = os.getenv(
    "CHUNKS_JSON_PATH",
    "./data/processed/chunks_manual.json"
)


print("CONFIGURACION CARGADA:")
print(f"ENV_PATH = {ENV_PATH}")
print(f"USE_LLM_RAW = {USE_LLM_RAW}")
print(f"USE_LLM = {USE_LLM}")
print(f"OLLAMA_MODEL = {OLLAMA_MODEL}")
print(f"EMBEDDING_MODEL = {EMBEDDING_MODEL}")
print(f"MANUAL_PATH = {MANUAL_PATH}")
print(f"MANUALS_DIR = {MANUALS_DIR}")
print(f"CHROMA_DIR = {CHROMA_DIR}")
print(f"RETRIEVER_K = {RETRIEVER_K}")
print(f"CHUNKS_JSON_PATH = {CHUNKS_JSON_PATH}")


# ============================================================
# 3. Configuración de modelos
# ============================================================

llm = OllamaLLM(model=OLLAMA_MODEL)
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)


# ============================================================
# 4. Ruta para mostrar la interfaz web
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# 5. Funciones auxiliares generales
# ============================================================

def format_docs(docs):
    """
    Une el contenido de los documentos recuperados para enviarlo como contexto al LLM.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def normalizar_texto(texto):
    """
    Normaliza texto para búsquedas simples:
    - pasa a minúsculas
    - quita tildes
    - deja solo letras, números y espacios
    """
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def extraer_terminos_busqueda(pregunta):
    """
    Extrae términos útiles de la consulta para fallback textual.
    Evita palabras muy cortas y conectores comunes.
    """
    stopwords = {
        "que", "como", "para", "con", "del", "los", "las", "una", "uno",
        "unos", "unas", "por", "sin", "sobre", "cual", "cuales", "son",
        "hacer", "realizar", "indica", "dice", "manual", "service",
        "servicio", "equipo", "necesarias", "necesarios", "necesario",
        "necesaria", "el", "la", "de", "y", "o", "a", "en", "un"
    }

    texto = normalizar_texto(pregunta)
    terminos = [
        termino for termino in texto.split()
        if len(termino) >= 3 and termino not in stopwords
    ]

    return terminos


def generar_manual_id(ruta_pdf):
    """
    Genera un identificador simple a partir del nombre del archivo PDF.
    Ejemplo: monitor_hr1000.pdf -> monitor_hr1000
    """
    nombre = Path(ruta_pdf).stem
    nombre = normalizar_texto(nombre)
    nombre = nombre.replace(" ", "_")
    return nombre


def obtener_pdfs_a_ingestar():
    """
    Busca PDFs dentro de MANUALS_DIR.
    Si no encuentra ninguno, usa MANUAL_PATH como compatibilidad con el modo anterior.
    """
    ruta_manuales = BASE_DIR / MANUALS_DIR
    pdfs = []

    if ruta_manuales.exists():
        pdfs = sorted(ruta_manuales.glob("*.pdf"))

    if pdfs:
        return pdfs, "multiple"

    ruta_manual_unico = BASE_DIR / MANUAL_PATH

    if ruta_manual_unico.exists():
        return [ruta_manual_unico], "unico"

    return [], "ninguno"


def guardar_chunks_json(fragmentos):
    """
    Guarda una copia textual simple de los chunks.
    Sirve para fallback 2 si Ollama, embeddings o ChromaDB fallan.
    Incluye metadata para distinguir manuales distintos.
    """
    ruta_json = BASE_DIR / CHUNKS_JSON_PATH
    ruta_json.parent.mkdir(parents=True, exist_ok=True)

    chunks = []

    for i, doc in enumerate(fragmentos, start=1):
        metadata = doc.metadata or {}

        chunks.append({
            "id": i,
            "texto": doc.page_content,
            "metadata": {
                "manual_id": metadata.get("manual_id", "manual_unico"),
                "archivo_origen": metadata.get("archivo_origen", MANUAL_PATH),
                "source": metadata.get("source", MANUAL_PATH),
                "page": metadata.get("page", None)
            }
        })

    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(chunks, archivo, ensure_ascii=False, indent=2)

    return ruta_json, len(chunks)


def cargar_chunks_json():
    """
    Carga los chunks textuales guardados durante la ingesta.
    """
    ruta_json = BASE_DIR / CHUNKS_JSON_PATH

    if not ruta_json.exists():
        return []

    with open(ruta_json, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def busqueda_textual_simple(pregunta, limite=5, manual_id=None):
    """
    Fallback 2:
    Busca coincidencias simples por palabras clave dentro de chunks_manual.json.
    No depende de Ollama, embeddings ni ChromaDB.
    Si recibe manual_id, limita la búsqueda a ese manual.
    """
    chunks = cargar_chunks_json()

    if not chunks:
        return []

    terminos = extraer_terminos_busqueda(pregunta)
    pregunta_normalizada = normalizar_texto(pregunta)
    manual_id_normalizado = manual_id.strip() if manual_id else ""

    resultados = []

    for chunk in chunks:
        metadata = chunk.get("metadata", {}) or {}

        if manual_id_normalizado:
            if metadata.get("manual_id") != manual_id_normalizado:
                continue

        texto_original = chunk.get("texto", "")
        texto_normalizado = normalizar_texto(texto_original)

        score = 0

        # Coincidencia por términos individuales
        for termino in terminos:
            score += texto_normalizado.count(termino)

        # Pequeño refuerzo si aparece una frase relevante completa
        if pregunta_normalizada and pregunta_normalizada in texto_normalizado:
            score += 5

        if score > 0:
            resultados.append({
                "score": score,
                "id": chunk.get("id"),
                "texto": texto_original,
                "metadata": metadata
            })

    resultados.sort(key=lambda item: item["score"], reverse=True)

    return resultados[:limite]


def format_fallback_response(docs):
    """
    Construye una respuesta útil cuando el LLM está desactivado o falla,
    pero ChromaDB sí pudo recuperar documentos.
    """
    if not docs:
        return (
            "[MODO FALLBACK DOCUMENTAL]\n\n"
            "No se encontraron fragmentos relevantes en la base documental. "
            "Probá reformular la consulta, verificar el manual seleccionado "
            "o confirmar que los manuales hayan sido ingeridos correctamente."
        )

    bloques = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata or {}
        pagina = metadata.get("page", None)
        fuente = metadata.get("archivo_origen") or metadata.get("source", "manual")
        manual_id = metadata.get("manual_id", "manual")

        encabezado = f"Fragmento {i}"
        encabezado += f" | manual_id: {manual_id}"
        if pagina is not None:
            encabezado += f" | página {pagina + 1}"
        if fuente:
            encabezado += f" | fuente: {fuente}"

        bloques.append(
            f"{encabezado}\n"
            f"{doc.page_content.strip()}"
        )

    return (
        "[MODO FALLBACK DOCUMENTAL]\n\n"
        "El modelo de lenguaje está desactivado o no pudo generar una respuesta. "
        "Se muestran los fragmentos más relevantes recuperados directamente del manual:\n\n"
        + "\n\n---\n\n".join(bloques)
    )


def format_fallback_textual_response(resultados):
    """
    Construye la respuesta del fallback 2.
    Este modo no depende de Ollama ni de ChromaDB.
    """
    if not resultados:
        return (
            "[MODO FALLBACK TEXTUAL]\n\n"
            "No se pudo usar la búsqueda vectorial y tampoco se encontraron "
            "coincidencias textuales suficientes en los chunks guardados. "
            "Probá reformular la consulta, verificar el manual seleccionado "
            "o confirmar que los manuales hayan sido ingeridos."
        )

    bloques = []

    for i, item in enumerate(resultados, start=1):
        metadata = item.get("metadata", {})
        pagina = metadata.get("page", None)
        fuente = metadata.get("archivo_origen") or metadata.get("source", "manual")
        manual_id = metadata.get("manual_id", "manual")
        score = item.get("score", 0)

        encabezado = f"Coincidencia textual {i}"
        encabezado += f" | manual_id: {manual_id}"
        if pagina is not None:
            encabezado += f" | página {pagina + 1}"
        if fuente:
            encabezado += f" | fuente: {fuente}"
        encabezado += f" | score: {score}"

        bloques.append(
            f"{encabezado}\n"
            f"{item.get('texto', '').strip()}"
        )

    return (
        "[MODO FALLBACK TEXTUAL]\n\n"
        "No se pudo utilizar la búsqueda vectorial con embeddings. "
        "Se realizó una búsqueda textual simple sobre los chunks guardados del manual:\n\n"
        + "\n\n---\n\n".join(bloques)
    )


def build_rag_prompt():
    """
    Define el prompt del asistente técnico.
    """
    system_prompt = (
        "Eres un asistente técnico para Ingeniería Clínica. "
        "Usa ÚNICAMENTE los siguientes fragmentos de contexto recuperado "
        "para responder la pregunta. "
        "Si la respuesta no está en el contexto, di exactamente: "
        "'La información no se encuentra en el manual'. "
        "No inventes datos, valores, procedimientos ni recomendaciones. "
        "Responde en español, de forma clara, breve y útil para personal técnico. "
        "\n\n"
        "Contexto: {context}"
    )

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])


def generar_respuesta_llm(pregunta, docs):
    """
    Genera una respuesta con el LLM usando únicamente los documentos ya recuperados.
    Esta función NO vuelve a consultar ChromaDB. Usa el contexto recibido.
    """
    prompt = build_rag_prompt()
    contexto = format_docs(docs)

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "context": contexto,
        "input": pregunta
    })


# ============================================================
# 6. Ruta para procesar y guardar PDF(s)
# ============================================================

@app.route("/ingestar", methods=["POST"])
def ingestar_pdf():
    inicio = time.perf_counter()

    rutas_pdf, modo_ingesta = obtener_pdfs_a_ingestar()

    if not rutas_pdf:
        return jsonify({
            "error": (
                "No se encontraron manuales PDF para ingerir. "
                f"Verificá la carpeta {MANUALS_DIR} o el archivo {MANUAL_PATH}."
            )
        }), 400

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    todos_los_fragmentos = []
    manuales_procesados = []

    for ruta_pdf in rutas_pdf:
        manual_id = generar_manual_id(ruta_pdf)

        loader = PyPDFLoader(str(ruta_pdf))
        documentos = loader.load()

        # Agregar metadata del manual antes de fragmentar
        for doc in documentos:
            doc.metadata = doc.metadata or {}
            doc.metadata["manual_id"] = manual_id
            doc.metadata["archivo_origen"] = ruta_pdf.name
            doc.metadata["source"] = str(ruta_pdf)

        fragmentos = text_splitter.split_documents(documentos)

        todos_los_fragmentos.extend(fragmentos)

        manuales_procesados.append({
            "manual_id": manual_id,
            "archivo": ruta_pdf.name,
            "paginas": len(documentos),
            "fragmentos": len(fragmentos)
        })

    # 1) Guardar en ChromaDB para búsqueda vectorial
    Chroma.from_documents(
        documents=todos_los_fragmentos,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    # 2) Guardar copia textual simple para fallback 2
    ruta_chunks_json, cantidad_chunks_json = guardar_chunks_json(todos_los_fragmentos)

    tiempo_total = round(time.perf_counter() - inicio, 2)

    return jsonify({
        "mensaje": (
            f"Ingesta completada en modo {modo_ingesta}. "
            f"Se procesaron {len(manuales_procesados)} manual(es), "
            f"se crearon {len(todos_los_fragmentos)} fragmentos, "
            f"se guardaron en ChromaDB y también en JSON textual."
        ),
        "modo_ingesta": modo_ingesta,
        "manual_path": MANUAL_PATH,
        "manuals_dir": MANUALS_DIR,
        "chroma_dir": CHROMA_DIR,
        "chunks_json_path": str(ruta_chunks_json),
        "manuales_procesados": manuales_procesados,
        "fragmentos": len(todos_los_fragmentos),
        "fragmentos_json": cantidad_chunks_json,
        "tiempo_segundos": tiempo_total
    })


# ============================================================
# 7. Ruta para hacerle preguntas al manual
# ============================================================

@app.route("/consultar", methods=["POST"])
def consultar_manual():
    inicio_total = time.perf_counter()

    data = request.json or {}
    pregunta = data.get("pregunta", "").strip()
    manual_id = data.get("manual_id", "").strip()

    if not pregunta:
        return jsonify({
            "respuesta": "No se recibió ninguna pregunta para consultar."
        }), 400

    docs = []
    error_retrieval = None
    error_llm = None
    tiempo_retrieval = None
    tiempo_llm = None
    modo_respuesta = "fallback_textual"

    # ========================================================
    # 1) Intentar búsqueda vectorial con ChromaDB + embeddings
    # ========================================================

    try:
        if not os.path.exists(CHROMA_DIR):
            raise FileNotFoundError(
                "La base ChromaDB no existe. Se intentará fallback textual."
            )

        vector_store = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )

        search_kwargs = {"k": RETRIEVER_K}

        if manual_id:
            search_kwargs["filter"] = {"manual_id": manual_id}

        retriever = vector_store.as_retriever(
            search_kwargs=search_kwargs
        )

        inicio_retrieval = time.perf_counter()
        docs = retriever.invoke(pregunta)
        tiempo_retrieval = round(time.perf_counter() - inicio_retrieval, 2)

        # ====================================================
        # 2) Si ChromaDB funcionó, intentar LLM o fallback 1
        # ====================================================

        if USE_LLM:
            try:
                inicio_llm = time.perf_counter()
                respuesta = generar_respuesta_llm(pregunta, docs)
                tiempo_llm = round(time.perf_counter() - inicio_llm, 2)
                modo_respuesta = "llm"

            except Exception as error:
                error_llm = str(error)
                respuesta = format_fallback_response(docs)
                modo_respuesta = "fallback_documental"

        else:
            respuesta = format_fallback_response(docs)
            modo_respuesta = "fallback_documental"

    except Exception as error:
        # ====================================================
        # 3) Si falla ChromaDB / embeddings / Ollama completo:
        #    fallback 2 textual sobre chunks_manual.json
        # ====================================================

        error_retrieval = str(error)

        inicio_retrieval = time.perf_counter()
        resultados_textuales = busqueda_textual_simple(
            pregunta,
            limite=RETRIEVER_K,
            manual_id=manual_id if manual_id else None
        )
        tiempo_retrieval = round(time.perf_counter() - inicio_retrieval, 2)

        respuesta = format_fallback_textual_response(resultados_textuales)
        modo_respuesta = "fallback_textual"

    tiempo_total = round(time.perf_counter() - inicio_total, 2)

    return jsonify({
        "pregunta": pregunta,
        "manual_id_solicitado": manual_id or None,
        "respuesta": respuesta,
        "modo": modo_respuesta,
        "modelo": OLLAMA_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "use_llm": USE_LLM,
        "use_llm_raw": USE_LLM_RAW,
        "env_path": str(ENV_PATH),
        "manual_path": MANUAL_PATH,
        "manuals_dir": MANUALS_DIR,
        "retriever_k": RETRIEVER_K,
        "chunks_recuperados": len(docs),
        "tiempo_retrieval_segundos": tiempo_retrieval,
        "tiempo_llm_segundos": tiempo_llm,
        "tiempo_total_segundos": tiempo_total,
        "error_retrieval": error_retrieval,
        "error_llm": error_llm,
        "chunks_json_path": str(BASE_DIR / CHUNKS_JSON_PATH)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)