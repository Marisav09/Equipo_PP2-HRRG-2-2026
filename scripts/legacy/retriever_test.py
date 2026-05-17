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
    y devuelve la colección configurada.
    """
    client = chromadb.PersistentClient(path=str(VECTORSTORE_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def retrieve_relevant_chunks(question, n_results=DEFAULT_N_RESULTS, distance_threshold=DISTANCE_THRESHOLD):
    """
    Recupera chunks relevantes desde ChromaDB a partir de una pregunta.

    La función:
    1. Convierte la pregunta en embedding.
    2. Consulta la colección de ChromaDB.
    3. Filtra los resultados por distancia semántica.
    4. Devuelve solo los chunks que cumplen con el umbral definido.
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
    Este texto será el que, en una etapa posterior, pueda enviarse a un LLM
    para generar una respuesta basada exclusivamente en la documentación.
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

def print_retrieval_result(question, chunks):
    """
    Imprime el resultado de recuperación de forma simple.
    """
    print("\n" + "=" * 100)
    print(f"PREGUNTA: {question}")
    print("=" * 100)

    if not chunks:
        print("No se encontraron chunks suficientemente relevantes.")
        return

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nRESULTADO ACEPTADO {index}")
        print("-" * 100)
        print(f"Fuente: {chunk['source_file']}")
        print(f"Página: {chunk['page']}")
        print(f"Tipo de documento: {chunk['document_type']}")
        print(f"Chunk: {chunk['chunk_id']}")
        print(f"Distancia: {chunk['distance']:.4f}")
        print("-" * 100)
        print(chunk["text"][:700])
        print("-" * 100)


if __name__ == "__main__":
    test_questions = [
        "¿Cómo se organizará la base de conocimiento documental?",
        "¿El sistema permite identificar equipos mediante QR?",
        "¿Qué dice sobre sensores de oxígeno?"
    ]

    for question in test_questions:
        chunks = retrieve_relevant_chunks(question)
        print_retrieval_result(question, chunks)

        llm_context = build_llm_context(chunks)

        if llm_context:
            print("\nCONTEXTO PREPARADO PARA EL LLM")
            print("=" * 100)
            print(llm_context)
        else:
            print("\nNo se generó contexto para LLM porque no hubo chunks aceptados.")