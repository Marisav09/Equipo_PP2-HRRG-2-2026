-------------------------------------------------------------------------------------------
**Propuesta de documento público**, redactado con un tono institucional, claro y directo. Está diseñado para que cualquier persona del hospital entienda qué es el sistema, cómo le sirve y cómo usarlo, sin abrumarse con los detalles de la arquitectura de software.
--------------------------------------------------------------------------------------------
---
## 👩‍⚕️ Guía Rápida para el Perfil Operador

Este acceso está pensado para el personal de las unidades clínicas, como enfermeros y técnicos operativos, que necesitan respuestas rápidas y directas en su día a día.

* **Acceso inmediato:** Solo debes escanear con tu celular el código QR que se encuentra pegado en el equipo médico. Esto abrirá el sistema con el equipo ya seleccionado.


* **Respuestas claras:** El sistema te dará instrucciones concisas y fáciles de entender, sin abrumarte con lenguaje técnico.


* **Consultas por voz:** Si tienes las manos ocupadas, puedes tocar el ícono del micrófono (🎤) y hacer tu pregunta hablando.


* **Lectura en voz alta:** Puedes presionar el botón "🔊 Escuchar" y el sistema te leerá la respuesta.


* **Historial a mano:** En la pantalla podrás ver un recordatorio de tus últimas 5 consultas.



**Ejemplos de preguntas ideales:**

* *"¿Cómo se enciende el monitor?"*

* *"¿Qué significa el código de alarma 705?"*

* *"¿Cómo se silencia esta alarma?"*


---

## 👨‍🔧 Guía Rápida para el Perfil Técnico

Este acceso está diseñado exclusivamente para los ingenieros clínicos y técnicos de mantenimiento del HRRG que requieren información profunda y detallada.

* **Acceso seguro:** Se ingresa desde una computadora a través del enlace web del sistema, seleccionando "Acceso Técnico" e ingresando la contraseña correspondiente.


* **Respuestas fundamentadas:** El sistema proporciona guías paso a paso e incluye obligatoriamente las fuentes documentales exactas (ej. Manual Técnico, Página 47) para que puedas validar la información.


* **Trazabilidad total:** Cuenta con un Centro de Monitoreo que permite ver en tiempo real todas las consultas realizadas en el hospital, qué equipos tienen más alarmas y si se han reportado incidentes.


* **Red de seguridad (Fallback):** Si por algún motivo el motor de inteligencia artificial se demora o satura, el sistema nunca te dejará sin respuesta; automáticamente te mostrará los extractos originales y directos del manual.


* **Acceso a manuales:** Permite ver el catálogo completo de manuales cargados en el sistema y descargar los archivos PDF originales.



**Ejemplos de preguntas ideales:**

* *"¿Cuál es el procedimiento de calibración del sensor de flujo?"*

* *"¿Cuáles son los códigos de error 0x701, 0x702, 0x703?"*





-------------------------------------------------------------------------------------------

**Propuesta de documento privado**
--------------------------------------------------------------------------------------------

# 📖 Guía de Uso - Asistente IA para Ingeniería Clínica

## Índice
1. [Acceso General](#acceso-general)
2. [Guía para Operadores](#guía-para-operadores)
3. [Guía para Técnicos](#guía-para-técnicos)
4. [Preguntas Frecuentes](#preguntas-frecuentes)
5. [Solución de Problemas](#solución-de-problemas)

---

# Acceso General

## 🚀 Primer Acceso

### Requisitos
- Navegador moderno (Chrome, Firefox, Edge, Safari)
- Conexión a red del hospital
- Dirección IP del servidor: `http://localhost:5000` (o la asignada)

### Paso 1: Abrir la Aplicación

1. Abre tu navegador
2. Ingresa la dirección: **`http://localhost:5000`**
3. Verás la página de bienvenida (landing page)

### Paso 2: Seleccionar tu Rol

Tienes dos opciones:

```
┌─────────────────────┬──────────────────────┐
│  OPERADOR           │  ACCESO TÉCNICO      │
├─────────────────────┼──────────────────────┤
│ • Interfaz simple   │ • Interfaz completa  │
│ • Respuestas cortas │ • Respuestas detall. │
│ • Acceso directo    │ • Requiere password  │
│ • Por QR            │ • Monitoreo         │
└─────────────────────┴──────────────────────┘
```

---

## 🔐 Autenticación

### Acceso Operador (Sin Contraseña)
- Haz clic en **"Acceso Operador"**
- Selecciona un equipo (o escanea QR)
- Acceso inmediato al chat

### Acceso Técnico (Requiere Contraseña)
- Haz clic en **"Acceso Técnico"**
- Ingresa contraseña: `tecnico-hrrg`
- Presiona **Enter** o haz clic en "Ingresar"
- Acceso a interfaz técnica completa

**Nota:** Usa las credenciales asignadas por Ingeniería Clínica

---

---

# 📱 GUÍA PARA OPERADORES

## ¿Quién soy?

Eres **operador** si:
- ✓ Trabajas en una unidad clínica (enfermera, técnico operativo)
- ✓ Necesitas respuestas rápidas sobre los equipos que manejas
- ✓ Quieres información sin términos muy técnicos
- ✓ Prefieres interfaz simple y directa

---

## 1️⃣ Inicio Rápido - Acceso por QR

### Paso 1: Localiza el Código QR
En cada equipo del hospital hay un código QR pegado (o disponible en Ingeniería Clínica)

```
┌─────────────────┐
│                 │
│      ██ ██      │
│      ██ ██      │◄─ Código QR del equipo
│       ███       │
│                 │
└─────────────────┘
```

### Paso 2: Escanea con tu Móvil
- Abre la cámara de tu teléfono
- Apunta al código QR
- Haz clic en la notificación que aparece

### Paso 3: Interfaz Operador Automática
La aplicación se abre directamente:
- ✅ Equipo preseleccionado
- ✅ Listo para consultar
- ✅ Sin necesidad de elegir equipo

---

## 2️⃣ Flujo Estándar de Consulta

### Opción A: Por Texto

```
1. Escribe tu pregunta en el cuadro de entrada
   Ejemplo: "¿Cómo se enciende?" o "¿Qué es alarma 402?"

2. Presiona Enter o haz clic en el botón "Enviar"

3. Espera la respuesta (5-30 segundos)

4. Lee la respuesta en la pantalla
```

### Opción B: Por Voz

```
1. Haz clic en el ícono 🎤 de micrófono

2. Habla tu pregunta claramente

3. Cuando termines, suelta el botón (o espera 3 segundos)

4. El sistema procesa tu voz

5. Recibe respuesta en texto

6. (Opcional) Escucha la respuesta en voz alta
```

---

## 3️⃣ Interfaz Operador Explicada

```
┌────────────────────────────────────────────────────┐
│ ◀ Cambiar equipo │ 🖥️ Monitor Multiparamétrico │ 🎤 🚪 │
├────────────────────────────────────────────────────┤
│                                                    │
│  Preguntas anteriores:                             │
│  • ¿Cómo resuelvo alarma?                          │
│  • ¿Cuándo cambiar batería?                        │
│  • Pantalla oscura, ¿qué hago?                     │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│ RESPUESTA:                                         │
│ Para resolver esta alarma, debes...                │
│ [Respuesta clara en español]                       │
│                                                    │
│ 🔊 Escuchar  │                                     │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  ¿Tu pregunta aquí?     [Enviar] 🎤               │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Elementos Principales

| Elemento | Función |
|----------|---------|
| **◀ Cambiar equipo** | Volver a seleccionar otro equipo |
| **Nombre equipo** | Confirma qué equipo consultaste |
| **🎤 Micrófono** | Hacer consulta por voz |
| **🔊 Escuchar** | Reproduce respuesta en audio |
| **Historial lateral** | Últimas 5 consultas (para referencia) |
| **Cuadro entrada** | Escribe tu pregunta |
| **🚪 Salir** | Termina sesión y vuelve a inicio |

---

## 4️⃣ Ejemplos de Preguntas

### ✅ Preguntas Buenas

```
"¿Cómo se enciende el monitor?"
"¿Qué significa alarma 502?"
"¿Cuándo cambiar filtro?"
"¿Cómo se silencia esta alarma?"
"No tiene batería, ¿qué hago?"
"¿Cuántos minutos de autonomía?"
"¿Cómo cambio la pantalla de vista?"
```

### ❌ Preguntas Fuera de Alcance

```
"¿Cuál es el diagnóstico del paciente?"
"¿Debería usar este equipo para X?"
"¿Es mejor este equipo u otro?"
"Información política/general"
```

---

## 5️⃣ Funciones Especiales

### Escuchar Respuesta en Voz Alta

```
1. Después de recibir respuesta
2. Haz clic en botón "🔊 Escuchar"
3. El sistema lee la respuesta automáticamente
4. Presiona Stop para cancelar
```

### Silenciar Respuestas en Voz
- Haz clic en el ícono 🔇 de la barra superior
- Desactiva "Leer respuesta automáticamente"

### Ver Historial Anterior

En el panel izquierdo ves tus últimas 5 consultas:
- Haz clic en cualquiera para revisarla
- Se carga la conversación anterior
- Puedes continuar desde ahí

### Cambiar de Equipo

```
1. Haz clic en "◀ Cambiar equipo" (arriba a la izquierda)
2. Elige nuevo equipo de la lista
3. El chat se reinicia para el nuevo equipo
4. Puedes hacer nuevas consultas
```

---

## 6️⃣ Consejos Prácticos

### 💡 Para Mejores Respuestas

1. **Sé específico**
   - ❌ "¿Cómo funciona?"
   - ✅ "¿Cómo conecto el sensor de presión?"

2. **Usa términos del manual**
   - ❌ "¿Por qué hace ruido?"
   - ✅ "¿Qué significa el código de alarma 705?"

3. **Pregunta una cosa a la vez**
   - ❌ "¿Cómo la enciendo y qué hago si falla?"
   - ✅ "¿Cómo se enciende?"

4. **Si no entiendes, pregunta de nuevo**
   - El sistema recuerda el contexto
   - "¿Puedes explicar eso de forma más simple?"

### ⚡ Atajos Rápidos

| Acción | Atajo |
|--------|-------|
| Enviar pregunta | Enter (o Cmd+Enter) |
| Micrófono | Presiona y mantén (algunos navegadores) |
| Escuchar | Haz clic en 🔊 |
| Cambiar equipo | "◀ Cambiar equipo" botón |
| Salir | Botón "🚪 Salir" arriba derecha |

---

---

# 👨‍💼 GUÍA PARA TÉCNICOS

## ¿Quién soy?

Eres **técnico** si:
- ✓ Eres ingeniero/a clínico/a del hospital
- ✓ Trabajas en mantenimiento o soporte
- ✓ Necesitas respuestas técnicas detalladas
- ✓ Quieres ver fuentes documentales
- ✓ Necesitas auditoría de consultas

---

## 1️⃣ Acceso Técnico

### Paso 1: Abrir la Aplicación

```
http://localhost:5000
```

### Paso 2: Seleccionar "Acceso Técnico"

Haz clic en el botón **"ACCESO TÉCNICO"** en la página de inicio

### Paso 3: Ingresar Contraseña

```
Contraseña: tecnico-hrrg
```

Presiona **Enter** o haz clic en "Ingresar"

### Paso 4: Seleccionar Equipo

Se abre selector de equipos con lista completa:
- Ventiladores
- Monitores
- Esterilizadoras
- Y más...

Haz clic en el equipo que deseas consultar

---

## 2️⃣ Interfaz Técnica - Componentes

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ INGENIERÍA CLÍNICA        ◀ Cambiar eq  🎤   🚪   │  │
│  │                                                   │  │
│  │  🖥️ Centro de Monitoreo     📊 Manuales     ➕ Chat │  │ MENÚ
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Mis últimos chats:                                │  │ HISTORIAL
│  │ • ¿Cómo cambiar sensor? - 2h                      │  │ TÉCNICO
│  │ • Calibración procedimiento - 5h                  │  │
│  │ • Error 0x402 - ayer                              │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ RESPUESTA:                                        │  │ ÁREA DE
│  │ La calibración del sensor XYZ requiere:          │  │ RESPUESTAS
│  │ 1. Conectar al puerto calibration                 │  │
│  │ 2. Ejecutar secuencia de 5 minutos               │  │
│  │ 3. Validar offset (debe estar <0.5mm)            │  │
│  │                                                   │  │
│  │ 📄 FUENTES:                                        │  │
│  │ • Manual Técnico, Página 47                       │  │
│  │ • Guía de Mantenimiento, Sección 3.2              │  │
│  │                                                   │  │
│  │ 🔊 Escuchar                                        │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Tu pregunta: [________] [Enviar] 🎤                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 3️⃣ Opciones del Menú Técnico

### 🎯 Centro de Monitoreo

**Función:** Ver en tiempo real:
- Consultas hechas en el hospital
- Quién consultó, cuándo, qué equipo
- Categoría de la consulta (alarma, mantenimiento, etc.)
- Si fue incidente reportado

**Uso:**
1. Haz clic en **"📊 Centro de Monitoreo"**
2. Se abre panel con:
   - Filtros de búsqueda (usuario, equipo, fecha)
   - Tabla con últimas consultas
   - Detalles de cada consulta
3. Haz clic en cualquier consulta para ver detalles completos

**Información visible:**
- Usuario y rol (operador/técnico)
- Equipo consultado
- Fecha y hora exacta
- Pregunta realizada
- Respuesta generada
- Fuentes utilizadas
- Si se marcó como incidente

---

### 📚 Manuales Cargados

**Función:** Ver trazabilidad completa de documentos

**Uso:**
1. Haz clic en **"📚 Manuales cargados"**
2. Se abre diálogo con:
   - Resumen de manuales indexados
   - Tabla detallada por equipo
   - Estadísticas de chunks y imágenes

**Información por manual:**
- Nombre del archivo PDF
- Equipo asociado
- Cantidad de chunks (fragmentos)
- Cantidad de imágenes detectadas
- Fecha de ingesta (cuándo se agregó)
- URL fuente (si está disponible)
- Botón: **Descargar PDF** para acceso directo

**Filtros:**
- Por equipo
- Por fecha de carga
- Estado (activo/procesado)

---

### ➕ Nuevo Chat

**Función:** Iniciar nueva conversación limpia

**Uso:**
1. Haz clic en **"➕ Nuevo chat"**
2. Se reinicia el área de chat
3. Historiał anterior se guarda automáticamente
4. Comienza conversación nueva

---

## 4️⃣ Flujo Completo de Consulta Técnica

### Ejemplo: Diagnosticar Falla de Monitor

```
PASO 1: Seleccionar equipo
┌─────────────────────────────────────┐
│ Monitor Multiparamétrico            │
│ (Marca: Philips, Modelo: MP-50)     │
└─────────────────────────────────────┘

PASO 2: Hacer pregunta técnica
┌─────────────────────────────────────┐
│ "¿Cómo calibro el módulo de SpO2?   │
│  Tengo offset mayor a 2%"           │
└─────────────────────────────────────┘

PASO 3: Esperar respuesta (sistema busca en manuales)
- ChromaDB busca: "calibración SpO2"
- Filtra por: equipo = "Monitor Multiparamétrico"
- Recupera: 4 fragmentos mejores

PASO 4: LLM genera respuesta técnica
- Argumenta con procedimiento paso a paso
- Incluye especificaciones técnicas
- Menciona rangos aceptables

PASO 5: Ver fuentes documentales
- Se muestran referencias exactas
- Manual página X, sección Y
- Permite validar la información

PASO 6: Guardar en auditoría
- Usuario técnico, equipo, fecha/hora
- Pregunta, respuesta, fuentes
- Categoría automática: "Calibración"
```

---

## 5️⃣ Ver Respuestas Detalladas con Fuentes

### Estructura de Respuesta Técnica

```
┌─────────────────────────────────────┐
│        RESPUESTA LLM                │
├─────────────────────────────────────┤
│ Para calibrar el módulo SpO2:       │
│                                     │
│ 1. Conectar cable calibración       │
│ 2. Acceder a menú SERVICE           │
│ 3. Seleccionar CALIBRATION          │
│ 4. Seguir procedimiento (3 min)     │
│ 5. Verificar offset < 1%            │
│                                     │
│ Si persiste error, reemplazar       │
│ sensor (código: MOD-SPO2-V3)        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│    📄 FUENTES DOCUMENTALES          │
├─────────────────────────────────────┤
│ 1. Manual Técnico Philips MP-50     │
│    Página 142, Sección 5.3          │
│    "Procedimientos de Calibración"  │
│                                     │
│ 2. Guía de Mantenimiento            │
│    Página 67, Sección 3.2           │
│    "Troubleshooting SpO2"           │
│                                     │
│ 3. Especificaciones Técnicas        │
│    Página 12, Sección 2.1.4         │
│    "Rango de Offset Aceptable"      │
│                                     │
│ ✅ Confiabilidad: Alta              │
│ (3 fuentes documentales)            │
└─────────────────────────────────────┘
```

### Cómo Usar las Fuentes

1. **Verificar información crítica**
   - Usa las referencias para validar
   - Consulta manuals originales si necesario

2. **Acceder a manuales completos**
   - Haz clic en **"📚 Manuales cargados"**
   - Descarga el PDF original
   - Navega a página exacta

3. **Registrar en auditoría**
   - Las fuentes se guardan automáticamente
   - Crucial para trazabilidad hospitalaria

---

## 6️⃣ Centro de Monitoreo Detallado

### Acceso y Vista General

```
Centro de Monitoreo
├─ KPIs Generales (arriba)
│  ├─ Total consultas (hoy)
│  ├─ Consultas técnicas vs operador
│  ├─ Incidentes reportados
│  └─ Equipos más consultados
│
└─ Tabla de Consultas
   ├─ Filtros (usuario, equipo, rango fechas)
   ├─ Ordenamiento por columnas
   └─ Detalles al hacer clic
```

### Información en Tabla

| Columna | Contenido |
|---------|-----------|
| **Hora** | Timestamp de consulta |
| **Usuario** | Quién consultó |
| **Rol** | Operador o Técnico |
| **Equipo** | Equipo consultado |
| **Categoría** | Auto-clasificación (alarma, mantenimiento, etc.) |
| **Tipo Consulta** | Pregunta / Fallback documental |
| **Estado** | ¿Se resolvió? ¿Incidente? |
| **Acción** | Ver detalles completos |

### Casos de Uso

**Uso 1: Monitoreo de Equipos Críticos**
```
Filtrar por equipo: "Ventilador Servo-i"
Ver: Todas las consultas en último mes
Buscar: Patrones de fallos
Acción: Planificar mantenimiento preventivo
```

**Uso 2: Auditoría de Incidentes**
```
Filtrar por estado: "Incidente = Sí"
Ver: Consultas marcadas como incidente
Buscar: Equipos problemáticos
Acción: Investigar causa raíz
```

**Uso 3: Evaluación de Operadores**
```
Filtrar por usuario: "Operador X"
Ver: Patrón de preguntas
Buscar: Áreas de capacitación necesarias
Acción: Plan de entrenamiento personalizado
```

---

## 7️⃣ Historial Técnico Completo

### Acceso

En el panel izquierdo, sección **"Mis últimos chats"**:
- Muestra últimas conversaciones
- Haz clic para cargar conversación anterior
- Puedes continuar desde donde dejaste

### Funciones Adicionales

```
Para cada chat anterior:
├─ Timestamp (fecha/hora)
├─ Resumen de pregunta
├─ Estado (completado/incidente)
├─ Acción: Duplicar chat
└─ Acción: Compartir con colega
```

---

## 8️⃣ Preguntas Técnicas - Buenas Prácticas

### ✅ Preguntas Óptimas

```
"¿Cuál es el procedimiento de calibración del sensor de flujo?"
"¿Cómo se realiza mantenimiento preventivo mensual?"
"¿Cuáles son los códigos de error 0x701, 0x702, 0x703?"
"¿Qué especificación de batería necesita este equipo?"
"¿Cuál es la presión máxima recomendada antes de alarma?"
```

### 📋 Estructura Recomendada

```
Pregunta + Contexto:

"El monitor XX está mostrando error 0x402.
He reiniciado 3 veces. ¿Cuál es causa probable?
¿Qué verifica primero?"

Beneficios:
- Sistema entiende mejor
- Respuesta más targeted
- Menos ambigüedad
```

### ❌ Evitar

```
"¿Esto funciona?" (muy vago)
"¿Hay problemas?" (sin contexto)
"Dime todo sobre X" (muy amplio)
Preguntas de diagnóstico clínico (no es función)
```

---

## 9️⃣ Funciones Avanzadas

### Búsqueda Semántica

El sistema entiende significado, no solo palabras clave:

```
Pregunta: "El equipo no responde a comandos"
Sistema busca: "problemas comunicación", "interfaz", "timeouts"

No requiere: "¿Interface no funciona?"
```

### Memoria Conversacional

El sistema recuerda contexto:

```
Tú: "¿Cómo calibro?"
Sistema: [respuesta detallada]

Tú: "¿Y después?"
Sistema entiende: Continuación de calibración
(sin necesidad de repetir contexto)
```

### Fallback Documental

Si el LLM falla:

```
┌─────────────────────────┐
│ Si LLM timeout o error: │
├─────────────────────────┤
│ Sistema devuelve:       │
│ Extractos directos      │
│ del manual              │
│ Válidos pero sin        │
│ procesamiento LLM       │
└─────────────────────────┘
```

---

---

# ❓ PREGUNTAS FRECUENTES

## General

### P: ¿Qué navegador debo usar?
**R:** Cualquier navegador moderno:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### P: ¿Funciona en móvil?
**R:** Sí, interfaz responsive:
- Operador: Muy buena experiencia en móvil
- Técnico: Óptimo en tablet, aceptable en móvil

### P: ¿Qué pasa si no hay respuesta?
**R:** Sistema intenta 3 caminos:
1. Respuesta LLM (primaria)
2. Fallback documental (si LLM falla)
3. "No hay información" (si no hay manuales)

---

## Sobre Operador

### P: ¿Puedo hacer consultas sin QR?
**R:** Sí, desde `http://localhost:5000` > "Acceso Operador" > seleccionar equipo

### P: ¿Se guardan mis consultas?
**R:** Sí, en base de datos local. Siempre con fines de auditoría.

### P: ¿Puedo compartir respuestas con colegas?
**R:** Por ahora no, pero puedes usar "Escuchar en voz alta" para compartir oralmente.

### P: ¿Qué pasa si cambio de equipo a mitad de chat?
**R:** Se inicia conversación nueva. Anterior se guarda en historial.

---

## Sobre Técnico

### P: ¿Cómo agrego nuevos manuales?
**R:** 
1. Coloca PDF en `data/raw/`
2. Ejecuta: `python scripts/ingest_documents.py`
3. Nuevos manuales estarán disponibles en 5-10 minutos

### P: ¿Puedo descargar manuales desde la interfaz?
**R:** Sí, en **"📚 Manuales cargados"** > botón "Descargar PDF"

### P: ¿Cómo exporto auditoría?
**R:** Centro de Monitoreo tiene botones de exportación a CSV/PDF

### P: ¿Qué significan los "KPIs" del monitoreo?
**R:**
- **Consultas (hoy):** Total de preguntas respondidas
- **Técnicas vs Operador:** Distribución por rol
- **Incidentes:** Consultas marcadas como problema crítico
- **Top Equipos:** Más consultados (posibles issues)

### P: ¿Cómo reporto un incidente?
**R:** Al hacer consulta, marca "¿Es incidente?" antes de enviar

---

## Solución de Problemas

### 🔴 "No hay respuesta del servidor"

**Causa:** Servidor no está corriendo

**Solución:**
```bash
# Terminal
python run.py

# Debería ver: "Running on http://127.0.0.1:5000"
```

### 🔴 "No hay manuales para este equipo"

**Causa:** No hay PDFs ingiridos para ese equipo

**Solución:**
1. Ir a `data/raw/`
2. Agregar PDF del equipo
3. Ejecutar: `python scripts/ingest_documents.py`
4. Esperar 5-10 minutos
5. Recargar navegador

### 🔴 "Las respuestas son lentaas (>1 minuto)"

**Causa:** Ollama está lento o sin recuros

**Solución:**
```bash
# Verificar Ollama
curl http://127.0.0.1:11434/api/generate

# Si falla, reiniciar:
# Windows: Ctrl+Shift+Esc > Ollama > Finalizar
# Luego: ollama serve

# O liberar recursos (cerrar otras apps)
```

### 🔴 "Error al descargar QR"

**Causa:** Códigos QR no han sido generados

**Solución:**
```bash
python scripts/generate_qr.py
```

### 🔴 "Base de datos corrupta"

**Causa:** SQLite dañada

**Solución:**
```bash
# Opción 1: Borrar y reconstruir
cd data/memory/
del conversation.sqlite3

# Sistema crea nueva BD automáticamente

# Opción 2: Si persiste, contactar a Ingeniería Clínica
```

### 🔴 "Diccionario de voz no funciona"

**Causa:** Navegador sin permisos de micrófono

**Solución:**
1. Recarga navegador (F5)
2. Haz clic en micrófono
3. Permite acceso cuando navegador pregunta
4. Reintentar

---

---

# 🔧 SOLUCIÓN DE PROBLEMAS

## Checklist de Diagnóstico

```
┌─ ¿Qué no funciona?
│
├─ ACCESO
│  ├─ ¿Navegador muestra página? 
│  ├─ ¿Dirección correcta (localhost:5000)?
│  └─ ¿Puerto 5000 disponible?
│
├─ CONSULTAS
│  ├─ ¿Sistema entiende la pregunta?
│  ├─ ¿Hay manuales del equipo?
│  └─ ¿Ollama está corriendo?
│
├─ RESPUESTAS
│  ├─ ¿Son precisas las respuestas?
│  ├─ ¿Aparecen las fuentes?
│  └─ ¿Se guardan en auditoría?
│
└─ PERFORMANCE
   ├─ ¿Velocidad aceptable?
   └─ ¿Recursos de computadora?
```

## Comandos Útiles de Diagnóstico

```powershell
# Verificar si Ollama está corriendo
curl http://127.0.0.1:11434/api/generate

# Verificar si servidor Flask está corriendo
curl http://127.0.0.1:5000/api/system/health

# Verificar cantidad de documentos indexados
curl http://127.0.0.1:5000/api/equipment/catalog

# Ver logs de la aplicación
type logs/app.log

# Reiniciar sistema
python run.py
```

## Contacto de Soporte

Para problemas no resueltos:
- **Email:** ingenieria.clinica@hrrg.gob.ar
- **Teléfono:** [Extensión]
- **Ubicación:** Ingeniería Clínica, Piso 2

---

---

*Última actualización: 1 de junio de 2026*  
*Versión: 1.0*
