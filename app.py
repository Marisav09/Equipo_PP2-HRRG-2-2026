from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import time


# Cargar variables desde .env si existe
load_dotenv()

app = Flask(__name__)


# 1. Configuración general desde variables de entorno
USE_LLM = os.getenv("USE_LLM", "true").lower() == "true"
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "8"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
MANUAL_PATH = os.getenv("MANUAL_PATH", "manual.pdf")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))


# 2. Configuración de modelos
llm = OllamaLLM(model=OLLAMA_MODEL)
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)


# 3. Ruta para mostrar la interfaz web
@app.route("/")
def home():
    return render_template("index.html")


# 4. Funciones auxiliares
def format_docs(docs):
    """
    Une el contenido de los documentos recuperados para enviarlo como contexto al LLM.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def format_fallback_response(docs):
    """
    Construye una respuesta útil cuando el LLM está desactivado o falla.
    Devuelve fragmentos recuperados directamente desde ChromaDB.
    """
    if not docs:
        return (
            "No se encontraron fragmentos relevantes en la base documental. "
            "Probá reformular la consulta o verificar que el manual haya sido ingerido correctamente."
        )

    bloques = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata or {}
        pagina = metadata.get("page", None)
        fuente = metadata.get("source", "manual")

        encabezado = f"Fragmento {i}"
        if pagina is not None:
            encabezado += f" | página {pagina + 1}"
        if fuente:
            encabezado += f" | fuente: {fuente}"

        bloques.append(
            f"{encabezado}\n"
            f"{doc.page_content.strip()}"
        )

    return (
        "No se pudo generar una respuesta con el modelo de lenguaje. "
        "Se muestran los fragmentos más relevantes recuperados del manual:\n\n"
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


# 5. Ruta para procesar y guardar el PDF en ChromaDB
@app.route("/ingestar", methods=["POST"])
def ingestar_pdf():
    inicio = time.perf_counter()
    ruta_pdf = MANUAL_PATH

    if not os.path.exists(ruta_pdf):
        return jsonify({
            "error": f"No se encontró el archivo {ruta_pdf} en la carpeta."
        }), 400

    loader = PyPDFLoader(ruta_pdf)
    documentos = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    fragmentos = text_splitter.split_documents(documentos)

    Chroma.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    tiempo_total = round(time.perf_counter() - inicio, 2)

    return jsonify({
        "mensaje": (
            f"PDF procesado exitosamente. "
            f"Se crearon {len(fragmentos)} fragmentos "
            f"y se guardaron en ChromaDB."
        ),
        "manual_path": MANUAL_PATH,
        "chroma_dir": CHROMA_DIR,
        "fragmentos": len(fragmentos),
        "tiempo_segundos": tiempo_total
    })


# 6. Ruta para hacerle preguntas al manual
@app.route("/consultar", methods=["POST"])
def consultar_manual():
    inicio_total = time.perf_counter()

    data = request.json or {}
    pregunta = data.get("pregunta", "").strip()

    if not pregunta:
        return jsonify({
            "respuesta": "No se recibió ninguna pregunta para consultar."
        }), 400

    if not os.path.exists(CHROMA_DIR):
        return jsonify({
            "respuesta": (
                "La base de datos está vacía. "
                "Por favor, ejecuta la ingesta del manual primero."
            )
        }), 400

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )

    # 1) Recuperación documental
    inicio_retrieval = time.perf_counter()
    docs = retriever.invoke(pregunta)
    tiempo_retrieval = round(time.perf_counter() - inicio_retrieval, 2)

    modo_respuesta = "fallback"
    error_llm = None

    # 2) Intento de respuesta con LLM
    if USE_LLM:
        try:
            inicio_llm = time.perf_counter()
            respuesta = generar_respuesta_llm(pregunta, docs)
            tiempo_llm = round(time.perf_counter() - inicio_llm, 2)
            modo_respuesta = "llm"

        except Exception as error:
            error_llm = str(error)
            tiempo_llm = None
            respuesta = format_fallback_response(docs)
            modo_respuesta = "fallback"
    else:
        tiempo_llm = None
        respuesta = format_fallback_response(docs)
        modo_respuesta = "fallback"

    tiempo_total = round(time.perf_counter() - inicio_total, 2)

    return jsonify({
        "pregunta": pregunta,
        "respuesta": respuesta,
        "modo": modo_respuesta,
        "modelo": OLLAMA_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "use_llm": USE_LLM,
        "retriever_k": RETRIEVER_K,
        "chunks_recuperados": len(docs),
        "tiempo_retrieval_segundos": tiempo_retrieval,
        "tiempo_llm_segundos": tiempo_llm,
        "tiempo_total_segundos": tiempo_total,
        "error_llm": error_llm
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)