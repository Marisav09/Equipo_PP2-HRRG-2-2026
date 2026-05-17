from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os

print("--- Iniciando proceso de ingesta técnica ---")

ruta_pdf = "manual.pdf"
if not os.path.exists(ruta_pdf):
    print(f"Error: No se encontró el archivo {ruta_pdf} en la carpeta.")
    exit()

print("1. Cargando el documento PDF...")
loader = PyPDFLoader(ruta_pdf)
documentos = loader.load()

print("2. Fragmentando el texto...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
fragmentos = text_splitter.split_documents(documentos)

print("3. Creando la base de datos vectorial (Usando embeddings locales)...")
# Usamos un embedding gratuito que corre directo en tu CPU sin necesidad de Ollama
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

Chroma.from_documents(
    documents=fragmentos, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

print(f"¡Éxito! PDF procesado. Se crearon {len(fragmentos)} fragmentos y se guardaron en la carpeta './chroma_db'.")