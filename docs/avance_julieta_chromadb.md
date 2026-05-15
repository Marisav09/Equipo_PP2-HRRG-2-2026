## Avance rama `julieta-chromadb`

En esta rama avancé con una primera implementación manual del flujo RAG, sin LangChain, para entender y validar cada etapa antes de incorporar una capa de orquestación.

Herramientas utilizadas:

- **PyMuPDF**: lectura de PDF y extracción de texto.
- **Python propio**: generación de chunks y metadatos.
- **JSON**: almacenamiento intermedio de chunks procesados.
- **SentenceTransformers**: generación de embeddings.
- **ChromaDB**: base vectorial local y búsqueda semántica.
- **Retriever propio**: filtrado de resultados por distancia semántica.
- **Flask**: interfaz web mínima para consultas.
- **HTML/CSS**: presentación de consulta y respuesta.

LangChain no se incorporó todavía porque primero se priorizó entender el flujo completo “a mano”. Queda como posible mejora posterior para ordenar/orquestar el RAG.
