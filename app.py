from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os


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


# 4. Ruta para procesar y guardar el PDF en ChromaDB
@app.route("/ingestar", methods=["POST"])
def ingestar_pdf():
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

    return jsonify({
        "mensaje": (
            f"PDF procesado exitosamente. "
            f"Se crearon {len(fragmentos)} fragmentos "
            f"y se guardaron en ChromaDB."
        )
    })


# 5. Ruta para hacerle preguntas al manual
@app.route("/consultar", methods=["POST"])
def consultar_manual():
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

    system_prompt = (
        "Eres un asistente técnico para Ingeniería Clínica. "
        "Usa ÚNICAMENTE los siguientes fragmentos de contexto recuperado "
        "para responder la pregunta. "
        "Si la respuesta no está en el contexto, di exactamente: "
        "'La información no se encuentra en el manual'. "
        "Responde en español, de forma clara, breve y útil para personal técnico. "
        "\n\n"
        "Contexto: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Arquitectura RAG con LCEL:
    # pregunta -> retriever -> contexto -> prompt -> LLM -> respuesta
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Por ahora USE_LLM queda preparado para el modo híbrido.
    # En el próximo paso vamos a implementar el fallback cuando USE_LLM=false
    # o cuando Ollama falle/tarde demasiado.
    if USE_LLM:
        respuesta = rag_chain.invoke(pregunta)
    else:
        docs = retriever.invoke(pregunta)
        respuesta = (
            "Modo LLM desactivado. Se muestran los fragmentos recuperados:\n\n"
            + format_docs(docs)
        )

    return jsonify({
        "pregunta": pregunta,
        "respuesta": respuesta,
        "modelo": OLLAMA_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "use_llm": USE_LLM,
        "retriever_k": RETRIEVER_K
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)