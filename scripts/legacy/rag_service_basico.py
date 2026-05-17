from pathlib import Path
import json
import re


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = BASE_DIR / "data" / "processed" / "chunks_ambito_desarrollo.json"


def load_chunks():
    """
    Carga los chunks procesados desde el archivo JSON.
    """
    if not CHUNKS_PATH.exists():
        return []

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text):
    """
    Normaliza texto para comparar palabras.
    Convierte a minúsculas y elimina signos básicos.
    """
    text = text.lower()
    text = re.sub(r"[^\wáéíóúñü]+", " ", text)
    return text


def search_relevant_chunks(question, chunks, max_results=2):
    """
    Busca chunks relevantes contando coincidencias simples
    entre palabras de la pregunta y el texto de cada chunk.
    """
    question_normalized = normalize_text(question)
    question_words = set(question_normalized.split())

    # Palabras demasiado generales que no ayudan a buscar
    stopwords = {
        "que", "qué", "como", "cómo", "cuando", "cuándo", "donde", "dónde",
        "el", "la", "los", "las", "un", "una", "unos", "unas",
        "de", "del", "en", "a", "por", "para", "con", "sobre",
        "se", "es", "son", "al", "lo", "y", "o"
    }

    question_words = question_words - stopwords

    results = []

    for chunk in chunks:
        chunk_text = chunk.get("text", "")
        chunk_normalized = normalize_text(chunk_text)
        chunk_words = set(chunk_normalized.split())

        score = len(question_words.intersection(chunk_words))

        if score > 0:
            results.append({
                "score": score,
                "chunk_id": chunk.get("chunk_id"),
                "source_file": chunk.get("source_file"),
                "text": chunk_text
            })

    results = sorted(results, key=lambda item: item["score"], reverse=True)

    return results[:max_results]


def answer_question(question):
    """
    Responde buscando fragmentos relevantes en los chunks procesados.
    """
    chunks = load_chunks()

    if not chunks:
        return (
            "No se encontraron chunks procesados. "
            "Primero debe ejecutarse el script de ingesta documental."
        )

    relevant_chunks = search_relevant_chunks(question, chunks)

    if not relevant_chunks:
        return (
            "La información solicitada no se encuentra identificada en la base documental procesada. "
            "El asistente no generará una respuesta sin respaldo documental."
        )

    response = "Se encontraron fragmentos relevantes en la base documental procesada:\n\n"

    for result in relevant_chunks:
        response += f"Fuente: {result['source_file']} | Chunk: {result['chunk_id']}\n"
        response += result["text"][:700]
        response += "\n\n---\n\n"

    response += (
        "Nota: esta respuesta corresponde a una recuperación documental básica. "
        "En una etapa posterior se reemplazará por búsqueda semántica con embeddings y ChromaDB."
    )

    return response