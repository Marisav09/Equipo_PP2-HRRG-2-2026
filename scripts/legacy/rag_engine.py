import time


def get_response(query: str) -> str:
    """Placeholder del motor RAG.

    Aqui se integraran LangChain, Ollama y ChromaDB para recuperar contexto,
    construir el prompt y generar la respuesta final.
    """
    time.sleep(2)
    return (
        "Respuesta de prueba del asistente RAG: se recibio la consulta "
        f"'{query}'. En la version final, esta respuesta usara documentos "
        "tecnicos y contexto clinico recuperado desde la base vectorial."
    )
