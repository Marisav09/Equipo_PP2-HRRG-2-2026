import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# ------- Almacenamiento y Gestión de Sesiones (La RAM del Servidor) -------

# Diccionario global para guardar las conversaciones en la memoria RAM
almacenamiento_historias = {}

# Función para obtener o crear el historial de mensajes de una sesión específica
def obtener_historial_sesion(session_id: str) -> ChatMessageHistory:
    if session_id not in almacenamiento_historias:
        almacenamiento_historias[session_id] = ChatMessageHistory()
    return almacenamiento_historias[session_id]

# ---- Configuración del Motor RAG Base (Conectando ChromaDB y Ollama) ----

def get_response_con_memoria_nativa(query: str, session_id: str = "usuario_hospital_default") -> str:
    try:
        BASE_DIR = Path(__file__).resolve().parent
        VECTORSTORE_DIR = BASE_DIR / "chroma_db"
        
        # 1. Configurar embeddings locales originales (768 dimensiones)
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://127.0.0.1:11434"
        )
        
        if not os.path.exists(VECTORSTORE_DIR):
            return f"La base de datos local en {VECTORSTORE_DIR} no existe."
            
        vectorstore = Chroma(
            persist_directory=str(VECTORSTORE_DIR),
            embedding_function=embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # retriever: Conecta LangChain y la base de datos ChromaDB física y pide q traiga los 3 fragmentos más parecidos (k:3)
        
        # 2. Configurar el LLM local
        llm = ChatOllama(
            model="llama3.2:3b",
            base_url="http://127.0.0.1:11434",
            temperature=0.0  # Temperatura en 0 para evitar que invente o desvíe la reformulación
        )
        
        # =====================================================================
        # PASO A: PROMPT TEXTUAL PARA REFORMULAR LA PREGUNTA
        # =====================================================================
        # Usamos un formato de texto plano directo para asegurar que Llama entienda el contexto anterior
        prompt_reformular = ChatPromptTemplate.from_template(
            """Dada la siguiente conversación previa entre un Usuario y un Asistente Técnico, 
y una nueva pregunta del usuario que puede contener elipses o referencias al pasado, 
reescribe la pregunta para que sea independiente, clara y mencione explícitamente el equipo o procedimiento del que se habla.
NO respondas la pregunta, solo devuelve la pregunta reformulada.

CONVERSACIÓN PREVIA:
{historial_texto}

NUEVA PREGUNTA DEL USUARIO: {pregunta_original}

Pregunta reformulada independiente:"""
        )
        
        cadena_reformuladora = prompt_reformular | llm | StrOutputParser()
        
        # =====================================================================
        # PASO B: PROMPT INSTITUCIONAL RAG (Respuesta final con contexto)
        # =====================================================================
        qa_system_prompt = """Eres un asistente técnico experto en equipamiento médico para el Hospital Regional Río Grande.
Usa los siguientes fragmentos del manual técnico para responder la pregunta de forma concisa y profesional.
Si no sabes la respuesta o no se encuentra en los fragmentos, di estrictamente que "La información no se encuentra en el manual", no inventes datos.

Fragmentos del manual:
{context}"""
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
        
        # =====================================================================
        # PASO C: FLUJO LOGÍCO INTERNO (Procesamiento y Extracción)
        # =====================================================================
        def flujo_orquestado(input_data):
            pregunta_original = input_data["question"]
            historial_mensajes = input_data.get("chat_history", [])
            
            # Convertimos la lista de objetos de mensaje a un bloque de texto limpio
            texto_historial = ""                #   recorre los mensajes y los une en un string
            if hasattr(historial_mensajes, "messages"):
                lista_msg = historial_mensajes.messages
            else:
                lista_msg = historial_mensajes

            for msg in lista_msg[-4:]:  # Analizamos los últimos 4 mensajes para mantener velocidad
                rol = "Usuario" if msg.type == "human" else "Asistente"
                texto_historial += f"{rol}: {msg.content}\n"
            
            # Si el historial de texto no está vacío, obligamos a Llama a reformular la duda
            if texto_historial.strip():
                pregunta_inteligente = chain_reformuladora_texto(texto_historial, pregunta_original)
            else:
                pregunta_inteligente = pregunta_original
                
            # Buscamos en ChromaDB usando la pregunta contextualizada
            docs = retriever.invoke(pregunta_inteligente)
            
            # Devolvemos el prompt final estructurado con todo lo necesario
            return qa_prompt.invoke({
                "context": docs,
                "chat_history": lista_msg,
                "question": pregunta_original
            })
            
        def chain_reformuladora_texto(historial, pregunta):
            return chain_reformuladora_ejecutar.invoke({"historial_texto": historial, "pregunta_original": pregunta})

        chain_reformuladora_ejecutar = prompt_reformular | llm | StrOutputParser()
        
        # Unimos la tubería final
        base_chain = RunnableLambda(flujo_orquestado) | llm | StrOutputParser()
        
        # =====================================================================
        # PASO D: ENVOLTORIO NATIVO DE MEMORIA DE LANGCHAIN
        # =====================================================================
        cadena_con_memoria = RunnableWithMessageHistory(
            base_chain,
            get_session_history=obtener_historial_sesion,
            input_messages_key="question",
            history_messages_key="chat_history"
        )
        
        configuracion = {"configurable": {"session_id": session_id}}
        return cadena_con_memoria.invoke({"question": query}, config=configuracion)
        
    except Exception as e:
        return f"Error en el motor conversacional robusto: {str(e)}"