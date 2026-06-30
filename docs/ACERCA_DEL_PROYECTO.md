-------------------------------------------------------------------------------------------
**Propuesta de documento público**, redactado con un tono institucional, claro y directo. Está diseñado para que cualquier persona del hospital entienda qué es el sistema, cómo le sirve y cómo usarlo, sin abrumarse con los detalles de la arquitectura de software.
--------------------------------------------------------------------------------------------
---

# 🏥 Conoce el Nuevo Asistente de IA para Ingeniería Clínica del HRRG

Bienvenido al nuevo **Asistente IA para Ingeniería Clínica**, una plataforma inteligente diseñada para el Hospital Regional Río Grande. Este sistema te permite consultar de forma instantánea los manuales oficiales de los equipos médicos del hospital, brindándote la información exacta que necesitas en el momento que la necesitas.

El sistema funciona de manera 100% local y segura: ninguna consulta sale a internet, garantizando la privacidad absoluta de los datos del hospital.

Para asegurar que cada usuario reciba la información adecuada, el sistema cuenta con dos perfiles de acceso adaptados a diferentes necesidades.

---

## 🛡️ Seguridad y Uso Responsable

Es importante recordar las capacidades y los límites de esta nueva herramienta:

* **Confiabilidad:** El Asistente IA solo responde basándose en los manuales oficiales cargados en el sistema. Tiene un mecanismo de seguridad que le impide inventar respuestas o hablar de temas fuera de esa documentación.


* **Límites de uso:** El sistema está diseñado exclusivamente para el soporte técnico del equipamiento. **Nunca debe utilizarse para tomar decisiones clínicas directas sobre los pacientes ni para emitir diagnósticos médicos**.


* **Auditoría:** Cada consulta realizada, junto con su respuesta y las fuentes utilizadas, queda registrada de forma segura para mantener la trazabilidad y mejorar el mantenimiento preventivo del hospital.

---

* * **Este tipo de implementaciones muestra claramente cómo la ciencia de datos y la inteligencia artificial pueden sumar un valor enorme y tangible al trabajo de las instituciones públicas en Tierra del Fuego, un enfoque que refleja muy bien la visión formativa del Centro Politécnico Superior Malvinas Argentinas.** 


-------------------------------------------------------------------------------------------

**Propuesta de documento privado**
--------------------------------------------------------------------------------------------


# 📋 Acerca del Proyecto

## Visión General

**Asistente IA para Ingeniería Clínica HRRG** es un sistema web diseñado para asistir al área de Ingeniería Clínica del Hospital Regional Río Grande. Proporciona un acceso rápido, seguro y trazable a la información técnica de los equipos médicos del hospital mediante una interfaz inteligente basada en inteligencia artificial.

El sistema utiliza **Retrieval-Augmented Generation (RAG)** para consultar manuales oficiales de equipamiento médico de forma local, garantizando privacidad, seguridad y respuestas fundamentadas únicamente en documentación verificada.

---

## Objetivos del Sistema

✅ **Acceso rápido a documentación técnica**  
Consultar manuales de equipos médicos de forma instantánea desde cualquier dispositivo conectado a la red del hospital.

✅ **Seguridad y privacidad**  
Sistema completamente local sin envío de datos a servidores externos.

✅ **Trazabilidad total**  
Cada respuesta genera un registro auditable que permite rastrear:
- Quién consultó
- Qué equipo
- Cuándo fue consultado
- Qué fuentes documentales respaldan la respuesta

✅ **Diferenciación de perfiles**  
Interfaces específicas para operadores (respuestas concisas) y técnicos (respuestas detalladas con fuentes).

✅ **Prevención de alucinaciones**  
Sistema con guardrails que rechaza responder fuera del alcance de los manuales indexados.

---

## Principios Fundamentales

### 1. **Aislamiento Estricto por Equipo**
- Cada equipo tiene su propio espacio de información
- Los manuales de un ventilador nunca se mezclan con los de un monitor
- Previene confusión y errores críticos en equipamiento médico

### 2. **Fallback Documental**
- Si el modelo IA no responde, el sistema devuelve extractos directos de los manuales
- Garantiza información válida incluso si el LLM falla

### 3. **Respuestas en Español y Contextorizadas**
- Todo en español (matching con la documentación hospitalaria)
- Respuestas adaptadas al rol del usuario

### 4. **Memoria Conversacional**
- El sistema recuerda la conversación anterior
- Permite referencias como "¿Cómo resuelvo lo anterior?" o "¿Y para esta alarma?"

---

## Arquitectura Técnica

```
┌─────────────────────────────────────────────────────────────┐
│                  FRONTEND (HTML/CSS/JS)                      │
│              Operador / Técnico / Landing                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP REST
┌──────────────────────▼──────────────────────────────────────┐
│                  BACKEND (Flask)                             │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │
│  │  Auth API  │  │ Chat API   │  │  Equipment/QR API    │   │
│  └────────────┘  └────────────┘  └──────────────────────┘   │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │
│  │ Monit. API │  │ Ingest API │  │  System Health API   │   │
│  └────────────┘  └────────────┘  └──────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    ┌───▼───┐    ┌────▼──────┐  ┌───▼──────┐
    │ChromaDB│    │  SQLite   │  │  Ollama  │
    │(Vectores)   │ (Memoria) │  │   (LLM)  │
    └────────┘    └───────────┘  └──────────┘
```

### Componentes Principales

| Componente | Función |
|-----------|---------|
| **ChromaDB** | Base de datos vectorial que almacena embeddings de fragmentos de manuales |
| **SQLite** | Almacenamiento de historial conversacional y auditoría |
| **Ollama** | Motor LLM local que ejecuta `llama3.2:3b` |
| **LangChain** | Framework para orquestar RAG |
| **Flask** | Servidor web backend |
| **PyMuPDF** | Extracción de texto e imágenes de PDFs |

---

## Stack Tecnológico

### Backend
- **Framework:** Flask
- **LLM Local:** Ollama + llama3.2:3b
- **Embeddings:** nomic-embed-text
- **Vector Database:** ChromaDB
- **Conversational Memory:** SQLite
- **PDF Processing:** PyMuPDF (fitz)
- **Procesamiento:** LangChain, LangChain-Community

### Frontend
- **HTML5** - Markup semántico
- **CSS3** - Diseño responsive (Mobile-First)
- **Vanilla JavaScript** - Sin frameworks (máxima compatibilidad)
- **Web APIs:** Speech Recognition, Speech Synthesis

### Infraestructura
- **Servidor Local:** Windows/Linux compatible
- **Configuración:** Variables de entorno (.env)
- **Logging:** Structured logging con rotación
- **Port:** 5000 (predeterminado, configurable)

---

## Flujo de Funcionamiento

### 1. **Ingesta de Documentos**

```
PDFs en data/raw/
        ↓
┌──────────────────────────────┐
│  Procesar PDF:               │
│  • Extraer texto por página  │
│  • Detectar imágenes/gráficos│
│  • Inferir equipo desde:     │
│    - Ruta del archivo        │
│    - Nombre de archivo       │
│    - Primeras páginas        │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Dividir en chunks:          │
│  • Tamaño: ~1000 caracteres  │
│  • Overlap: ~180 caracteres  │
│  • Preservar contexto        │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Agregar metadatos:          │
│  • equipment: "Ventilador XYZ"│
│  • page: 12                  │
│  • source_file: "venti.pdf"  │
│  • chunk_index: 3            │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Indexar en ChromaDB:        │
│  • Generar embeddings        │
│  • Almacenar con filtros     │
│  • Permitir búsqueda scoped  │
└──────────────────────────────┘
```

### 2. **Consulta RAG**

```
Usuario selecciona equipo + pregunta
        ↓
┌──────────────────────────────┐
│  Normalizar equipo           │
│  ej: "venti" → "Ventilador.."│
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Guardrails: ¿Equipo válido? │
│  Si no: rechazar             │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Recuperar histórico          │
│  (memoria conversacional)     │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  ChromaDB.search({            │
│    query: pregunta,           │
│    filter: {equipo: XYZ},     │
│    k: 4                       │
│  })                           │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Construir prompt:           │
│  • Rol del usuario           │
│  • Contexto recuperado       │
│  • Histórico conversa        │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  LLM genera respuesta        │
│  (con timeout de seguridad)  │
│  Si falla → fallback texto   │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│  Registrar en auditoría:     │
│  • Usuario / sesión          │
│  • Pregunta / respuesta      │
│  • Fuentes usadas            │
│  • Timestamp                 │
└──────────────────────────────┘
        ↓
Respuesta al usuario + Fuentes
```

---

## Modelos IA Utilizados

### LLM Principal: llama3.2:3b
- **Tamaño:** 3 billones de parámetros (ligero)
- **Lenguaje:** Soporte multiidioma (optimizado para inglés, pero funciona bien en español)
- **Velocidad:** Respuestas en 5-30 segundos (según complejidad)
- **Contexto:** 8k tokens (~6000 palabras)

### Modelo de Embeddings: nomic-embed-text
- **Dimensión:** 768 características vectoriales
- **Entrenamiento:** Optimizado para búsqueda semántica
- **Velocidad:** ~100ms por documento

---

## Perfiles de Usuario

### 👤 Operador
**Rol:** Personal hospitalario que opera equipos (enfermeras, técnicos operativos)

**Acceso:** 
- Interfaz simplificada
- Respuestas concisas y directas
- Sin fuentes visibles (solo la respuesta)
- Acceso por QR desde equipos

**Funcionalidades:**
- Consultar procedimientos rápidos
- Resolver alarmas comunes
- Historial de últimas 5 consultas
- Lectura en voz alta de respuestas

### 👨‍💼 Técnico
**Rol:** Ingenieros clínicos, técnicos de mantenimiento, especialistas

**Acceso:**
- Interfaz completa
- Respuestas detalladas con argumentación
- Sección visible de fuentes documentales
- Centro de monitoreo con auditoría en tiempo real

**Funcionalidades:**
- Consultas técnicas avanzadas
- Ver todos los manuales cargados (con metadata)
- Centro de monitoreo: seguimiento de consultas del hospital
- Auditoría de ingesta de documentos
- Historial completo de sesiones

---

## Características Principales

### 🔐 Seguridad

- ✅ Autenticación por contraseña (usuario/rol)
- ✅ Sesiones aisladas por usuario
- ✅ Sin transmisión de datos a internet
- ✅ Encriptación local de información sensible
- ✅ Logs auditables de todas las consultas

### 📊 Auditoría

- ✅ Registro completo de cada consulta
- ✅ Trazabilidad de fuentes documentales
- ✅ Timestamps precisos
- ✅ Información de usuario / rol
- ✅ Categorización automática de preguntas

### 🎤 Accesibilidad

- ✅ Reconocimiento de voz (Speech Recognition API)
- ✅ Síntesis de voz (Text-to-Speech)
- ✅ Interfaz responsive (móvil, tablet, desktop)
- ✅ Soporte para navegadores modernos

### 📱 Códigos QR

- ✅ Generación automática de QR por equipo
- ✅ Acceso operador con un escaneo
- ✅ Descargables, imprimibles
- ✅ URLs encoded con equipo y rol

### 📚 Gestión de Manuales

- ✅ Ingesta automatizada de PDFs
- ✅ Detección automática de equipo
- ✅ Reindexación incremental
- ✅ Visibilidad completa de trazabilidad (para técnico)
- ✅ Búsqueda por equipo

---

## Flujos de Acceso

### Acceso Operador

1. Escanear código QR en el equipo
2. Se abre interfaz operador con equipo preseleccionado
3. Ingresar pregunta (texto o voz)
4. Recibir respuesta concisa
5. Opcionalmente escuchar respuesta en voz

### Acceso Técnico

1. Abrir navegador → `http://localhost:5000`
2. Seleccionar "Acceso Técnico"
3. Ingresar contraseña
4. Seleccionar equipo
5. Acceder a:
   - Chat (consultas)
   - Centro de Monitoreo (auditoría en vivo)
   - Manuales cargados (trazabilidad)

---

## Configuración y Personalización

### Variables de Entorno (.env)

```bash
# Modelos IA
LLM_MODEL=llama3.2:3b
EMBEDDING_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://127.0.0.1:11434

# Rutas de datos
RAW_DOCUMENTS_DIR=data/raw
VECTORSTORE_DIR=data/chroma
MEMORY_DB_PATH=data/memory/conversation.sqlite3

# Parámetros RAG
RETRIEVAL_K=4           # Número de chunks a recuperar
CHUNK_SIZE=1000         # Tamaño de fragmento
CHUNK_OVERLAP=180       # Solapamiento entre chunks

# Autenticación
TECHNICAL_USER_PASSWORD=tecnico-hrrg
OPERATOR_USER_PASSWORD=operador-hrrg

# Otros
LLM_TIMEOUT_SECONDS=300
ENABLE_OCR=false
```

---

## Limitaciones y Consideraciones

⚠️ **Modelo pequeño (3B)**
- Respuestas menos complejas que GPT-4
- Mejor rendimiento local pero menos precision en preguntas ambiguas

⚠️ **Dependencia de ChromaDB**
- Requiere reindexación de manuales nuevos
- No soporta updates dinámicos en tiempo real

⚠️ **Offline only**
- Requiere Ollama corriendo localmente
- Sin acceso a información actual de internet

⚠️ **Tamaño de contexto**
- llama3.2 soporta 8k tokens (~6000 palabras)
- Diálogos muy largos pueden truncar historial

---

## Casos de Uso Recomendados

✅ **Respuestas procedurales:** "¿Cómo se enciende el equipo X?"  
✅ **Resolución de alarmas:** "¿Qué significa alarma 402?"  
✅ **Mantenimiento básico:** "¿Cuándo hacer cambio de filtro?"  
✅ **Especificaciones técnicas:** "¿Cuál es la presión máxima?"  
✅ **Troubleshooting común:** "¿Por qué no enciende?"  

❌ **No recomendado para:**
- Decisiones clínicas directas (usar protocolos hospitalarios)
- Información no en manuales
- Diagnósticos en equipos rotos
- Consultas fuera del alcance técnico

---

## Equipo y Contacto

**Proyecto:** Asistente IA para Ingeniería Clínica  
**Institución:** Hospital Regional Río Grande (HRRG)  
**Área:** Ingeniería Clínica  
**Fecha:** 2026  

**Documentación y Desarrollo:**
- Documentación técnica: Ver `/docs`
- Scripts de ingesta: Ver `/scripts`
- Tests: Ver `/tests`

---

## Licencia y Notas Legales

Este sistema está diseñado exclusivamente para uso interno en HRRG. Los manuales de equipos son propiedad de sus respectivos fabricantes. El sistema no pretende reemplazar manuales oficiales sino facilitar su consulta rápida y segura.

**Responsabilidad:** Todo uso del sistema debe cumplir con protocolos de seguridad hospitalaria. En caso de duda, consultar directamente los manuales originales o contactar a Ingeniería Clínica.

---

*Última actualización: 1 de junio de 2026*
