from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
COLLECTION_NAME = "manuales_hrrg"

DISTANCE_THRESHOLD = 1.0
DEFAULT_N_RESULTS = 3


def load_collection():
    """
    Conecta con la base vectorial local de ChromaDB
    y devuelve la colección de manuales.
    """
    client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def retrieve_relevant_chunks(
    question,
    n_results=DEFAULT_N_RESULTS,
    distance_threshold=DISTANCE_THRESHOLD
):
    """
    Recupera chunks relevantes desde ChromaDB a partir de una pregunta.

    La función:
    1. Convierte la pregunta en embedding.
    2. Consulta la colección de ChromaDB.
    3. Recupera documentos, metadatos y distancias.
    4. Filtra los resultados por distancia semántica.
    5. Devuelve solo los chunks suficientemente relevantes.
    """
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = load_collection()

    question_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    relevant_chunks = []

    for index, document in enumerate(documents):
        distance = distances[index]
        metadata = metadatas[index]

        if distance <= distance_threshold:
            relevant_chunks.append({
                "text": document,
                "source_file": metadata.get("source_file", "sin_fuente"),
                "page": metadata.get("page", "sin_página"),
                "document_type": metadata.get("document_type", "sin_tipo"),
                "chunk_id": metadata.get("chunk_id", "sin_chunk"),
                "distance": distance
            })

    return relevant_chunks


def build_llm_context(chunks):
    """
    Construye un bloque de contexto documental a partir de los chunks recuperados.

    En una etapa posterior, este contexto podrá enviarse a un LLM
    para generar una respuesta final basada exclusivamente en documentación.
    """
    if not chunks:
        return ""

    context = "CONTEXTO DOCUMENTAL RECUPERADO\n"
    context += "=" * 100 + "\n"

    for index, chunk in enumerate(chunks, start=1):
        context += f"\nFRAGMENTO {index}\n"
        context += "-" * 100 + "\n"
        context += f"Fuente: {chunk['source_file']}\n"
        context += f"Página: {chunk['page']}\n"
        context += f"Tipo de documento: {chunk['document_type']}\n"
        context += f"Chunk: {chunk['chunk_id']}\n"
        context += f"Distancia: {chunk['distance']:.4f}\n"
        context += "\nTexto recuperado:\n"
        context += chunk["text"].strip()
        context += "\n"
        context += "-" * 100 + "\n"

    return context


def answer_question(question):
    """
    Responde usando recuperación semántica desde ChromaDB.

    En esta etapa todavía no genera una respuesta final con LLM:
    muestra los fragmentos documentales recuperados y deja preparado
    el contexto que luego podrá enviarse al modelo de lenguaje.
    """
    relevant_chunks = retrieve_relevant_chunks(question)

    if not relevant_chunks:
        return (
            "La información solicitada no se encuentra suficientemente relacionada "
            "con la base vectorial ChromaDB. "
            "El asistente no generará una respuesta sin respaldo documental."
        )

    response = "Se recuperaron fragmentos relevantes desde ChromaDB:\n\n"

    for index, chunk in enumerate(relevant_chunks, start=1):
        response += f"Resultado {index}\n"
        response += f"Fuente: {chunk['source_file']}\n"
        response += f"Página: {chunk['page']}\n"
        response += f"Tipo de documento: {chunk['document_type']}\n"
        response += f"Chunk: {chunk['chunk_id']}\n"
        response += f"Distancia semántica: {chunk['distance']:.4f}\n"
        response += "Fragmento recuperado:\n"
        response += chunk["text"][:700].strip()        
        response += "\n\n---\n\n"
        response += (
        "Nota: esta respuesta utiliza recuperación semántica con embeddings "
        "y ChromaDB. En una etapa posterior, los fragmentos recuperados podrán "
        "ser enviados como contexto a un modelo de lenguaje para generar una "
        "respuesta final."
    )
        
        return response