from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
COLLECTION_NAME = "manuales_hrrg"
REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_REPORT = REPORTS_DIR / "resultados_busqueda_chromadb.txt"


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


def search_vectorstore(question, n_results=3):
    """
    Realiza una búsqueda semántica en ChromaDB.
    Convierte la pregunta en embedding y recupera los chunks más cercanos.
    """
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = load_collection()

    question_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    return results


def format_results(question, results):
    """
    Arma un texto ordenado con los resultados de búsqueda.
    Sirve para imprimir en terminal y también para guardar en un archivo.
    """
    output = ""

    output += "\n" + "=" * 100 + "\n"
    output += f"PREGUNTA: {question}\n"
    output += "=" * 100 + "\n"

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        output += "No se encontraron resultados.\n"
        return output

    for index, document in enumerate(documents, start=1):
        metadata = metadatas[index - 1]
        distance = distances[index - 1]

        output += f"\nRESULTADO {index}\n"
        output += "-" * 100 + "\n"
        output += f"Fuente: {metadata.get('source_file', 'sin_fuente')}\n"
        output += f"Página aproximada: {metadata.get('page', 'sin_página')}\n"
        output += f"Tipo de documento: {metadata.get('document_type', 'sin_tipo')}\n"
        output += f"Chunk: {metadata.get('chunk_id', 'sin_chunk')}\n"
        output += f"Distancia: {distance:.4f}\n"
        output += "-" * 100 + "\n"
        output += document[:900] + "\n"
        output += "-" * 100 + "\n"

    return output


def print_results(question, results):
    """
    Imprime en terminal los resultados ya formateados.
    """
    print(format_results(question, results))


if __name__ == "__main__":
    test_questions = [
        # Preguntas muy relacionadas con el documento
        "¿Qué herramientas tecnológicas se utilizarán en el proyecto?",
        "¿Cuál es el objetivo general del proyecto?",
        "¿Qué dice el documento sobre la arquitectura RAG?",

        # Preguntas medianamente relacionadas
        "¿Cómo se organizará la base de conocimiento documental?",
        "¿Qué limitaciones tiene el prototipo académico?",
        "¿Por qué es importante la trazabilidad de las respuestas?",

        # Preguntas poco relacionadas
        "¿El sistema permite identificar equipos mediante QR?",
        "¿El asistente puede reemplazar al criterio profesional del técnico?",

        # Preguntas no relacionadas con este documento
        "¿Qué dice sobre sensores de oxígeno?",
        "¿Cuál es el protocolo de calibración de un respirador neonatal?",
        "¿Qué repuestos necesita una bomba de infusión?"
    ]

    collection = load_collection()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report_text = ""
    report_text += "REPORTE DE BÚSQUEDA SEMÁNTICA CON CHROMADB\n"
    report_text += "=" * 100 + "\n"
    report_text += f"Ubicación de la base vectorial: {VECTORSTORE_DIR}\n"
    report_text += f"Colección: {COLLECTION_NAME}\n"
    report_text += f"Cantidad de chunks almacenados: {collection.count()}\n"
    report_text += "=" * 100 + "\n"

    print("\nBASE VECTORIAL CHROMADB")
    print("=" * 100)
    print(f"Ubicación: {VECTORSTORE_DIR}")
    print(f"Colección: {COLLECTION_NAME}")
    print(f"Cantidad de chunks almacenados: {collection.count()}")

    n_results_options = [1, 2, 3, 5]

    for n_results in n_results_options:
        section_title = f"\n\nCOMPARACIÓN CON n_results = {n_results}\n"
        section_title += "=" * 100 + "\n"

        print(section_title)
        report_text += section_title

        for question in test_questions:
            results = search_vectorstore(question, n_results=n_results)
            formatted = format_results(question, results)

            print(formatted)
            report_text += formatted

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as file:
        file.write(report_text)

    print("\nReporte guardado correctamente en:")
    print(OUTPUT_REPORT)