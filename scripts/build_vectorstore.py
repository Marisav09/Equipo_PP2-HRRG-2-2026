from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = BASE_DIR / "data" / "processed" / "chunks_ambito_desarrollo.json"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
COLLECTION_NAME = "manuales_hrrg"


def load_chunks():
    """
    Carga los chunks generados previamente en formato JSON.
    """
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de chunks: {CHUNKS_PATH}"
        )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_vectorstore():
    """
    Genera embeddings para cada chunk y los almacena en ChromaDB,
    incluyendo metadatos ampliados para mejorar la trazabilidad.
    """
    chunks = load_chunks()

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    print("Cargando modelo de embeddings...")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Conectando con ChromaDB local...")
    client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print(f"Procesando {len(chunks)} chunks...")

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        chunk_id = str(chunk["chunk_id"])
        text = chunk["text"]
        source_file = chunk.get("source_file", "sin_fuente")
        page = chunk.get("page", None)
        document_type = chunk.get("document_type", "sin_tipo")

        embedding = embedding_model.encode(text).tolist()

        ids.append(chunk_id)
        documents.append(text)
        embeddings.append(embedding)
        metadatas.append({
            "source_file": source_file,
            "chunk_id": chunk_id,
            "page": page if page is not None else "sin_página",
            "document_type": document_type
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Base vectorial creada/actualizada correctamente.")
    print(f"Ubicación: {VECTORSTORE_DIR}")
    print(f"Colección: {COLLECTION_NAME}")
    print(f"Cantidad de chunks cargados: {collection.count()}")


if __name__ == "__main__":
    build_vectorstore()