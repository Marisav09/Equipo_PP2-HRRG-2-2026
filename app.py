from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

app = Flask(__name__)

# 1. Configuración de Modelos
llm = OllamaLLM(model="llama3.2:3b")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Ruta para mostrar la interfaz web
@app.route('/')
def home():
    return render_template('index.html')

# 3. Ruta para procesar y guardar el PDF en ChromaDB
@app.route('/ingestar', methods=['POST'])
def ingestar_pdf():
    ruta_pdf = "manual.pdf"
    
    if not os.path.exists(ruta_pdf):
        return jsonify({"error": f"No se encontró el archivo {ruta_pdf} en la carpeta."}), 400
    
    loader = PyPDFLoader(ruta_pdf)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    fragmentos = text_splitter.split_documents(documentos)
    
    Chroma.from_documents(
        documents=fragmentos, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    
    return jsonify({"mensaje": f"PDF procesado exitosamente. Se crearon {len(fragmentos)} fragmentos y se guardaron en ChromaDB."})

# 4. Ruta para hacerle preguntas al manual
@app.route('/consultar', methods=['POST'])
def consultar_manual():
    data = request.json
    pregunta = data.get("pregunta")
    
    if not os.path.exists("./chroma_db"):
        return jsonify({"respuesta": "La base de datos está vacía. Por favor, ejecuta la ingesta del manual primero."}), 400
        
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vector_store.as_retriever()
    
    system_prompt = (
        "Eres un asistente técnico para Ingeniería Clínica. "
        "Usa ÚNICAMENTE los siguientes fragmentos de contexto recuperado para responder la pregunta. "
        "Si la respuesta no está en el contexto, di 'La información no se encuentra en el manual'. "
        "\n\n"
        "Contexto: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Arquitectura RAG moderna usando puramente LCEL
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    respuesta = rag_chain.invoke(pregunta)
    
    return jsonify({"pregunta": pregunta, "respuesta": respuesta})

if __name__ == '__main__':
    app.run(debug=True, port=5000)