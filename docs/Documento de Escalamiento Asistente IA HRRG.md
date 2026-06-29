# Documento de Escalamiento Asistente_IA_HRRG

<!-- Pagina 1 -->

Tecnicatura Superior en Ciencia de Datos e Inteligencia
Artificial
Práctica Profesionalizante II
Documento de continuidad, escalamiento y hoja de ruta de
mejoras futuras
Asistente IA para Ingeniería Clínica – HRRG
Equipo N.º 1:
Ana María Ramos Orcko
Darío Agustín García Barquet
Marisa Mercedes Velásquez
Nancy Julieta Cassano
Junio 2026

<!-- Pagina 2 -->

Documento de continuidad, escalamiento y hoja de ruta de mejoras futuras
Asistente IA para Ingeniería Clínica – HRRG
Proyecto: Asistente IA para Ingeniería Clínica – HRRG
Institución destinataria: Hospital Regional Río Grande – Ingeniería Clínica
Entrega: Sprint final – Junio 2026
Tipo de documento: Documento académico de transferencia, continuidad y
escalamiento del proyecto
Alcance: Documentación de oportunidades de evolución, correcciones técnicas,
criterios de continuidad y funcionalidades candidatas para futuras cohortes de Práctica
Profesionalizante II
## 1. Objetivo del documento

El presente documento tiene como objetivo ordenar las oportunidades de mejora
detectadas durante el desarrollo y la validación del Asistente IA para Ingeniería Clínica
– HRRG.
Su finalidad es facilitar la continuidad del proyecto en futuras versiones, especialmente
considerando que el sistema podrá ser retomado por otros desarrolladores.
Por ese motivo, este documento no solo enumera posibles mejoras, sino que también
busca orientar el traspaso del trabajo realizado, señalando qué aspectos deben
preservarse, qué componentes requieren revisión cuidadosa y qué líneas de desarrollo
podrían abordarse.
Las mejoras aquí descriptas no deben interpretarse como compromisos incluidos en la
versión final del sprint, sino como funcionalidades candidatas, recomendaciones
técnicas y criterios de continuidad para quienes retomen el proyecto.
## 2. Criterio general de escalamiento

El prototipo desarrollado permitió validar una arquitectura funcional basada en
recuperación documental aumentada por inteligencia artificial, con selección de equipo,
perfiles diferenciados, trazabilidad de fuentes, respuesta en lenguaje natural y criterios
de seguridad.
Sin embargo, durante la validación se identificó que la calidad del asistente depende de
una combinación de factores:
- calidad del corpus documental;
- correcta asociación entre equipo, modelo y manual;
- curaduría de documentos principales y secundarios;
- segmentación adecuada de los textos;

<!-- Pagina 3 -->

- confiabilidad de la recuperación;
- control de respuestas sin evidencia suficiente;
- seguridad del perfil Operador;
- trazabilidad entre respuesta, documento fuente y página;
- mantenimiento de la base vectorial;
- validación continua con consultas reales.
Por ese motivo, el escalamiento del sistema debe priorizar mejoras que aumenten la
confiabilidad, la seguridad y la utilidad operativa antes que agregar funcionalidades
accesorias.
## 3. Sentido de continuidad

Dado que el proyecto podrá ser continuado por otros desarrolladores, resulta importante
dejar documentadas no solo las funcionalidades pendientes, sino también las decisiones
técnicas ya tomadas y los criterios que no deberían perderse.
El próximo equipo que retome el desarrollo no debería comenzar únicamente desde el
código fuente, sino también desde la experiencia acumulada durante la construcción del
prototipo: problemas encontrados, validaciones realizadas, límites detectados, criterios
de seguridad, decisiones de curaduría documental y mejoras priorizadas.
En particular, se recomienda que cualquier continuidad del proyecto respete los
siguientes principios:
- no modificar el corpus documental sin registrar la decisión de curaduría correspondiente;
- no reconstruir la base vectorial sin verificar previamente qué documentos están activos;
- no agregar funcionalidades nuevas si comprometen la seguridad o la trazabilidad de las respuestas;
- no orientar la validación a preguntas preparadas únicamente para demostración;
- mantener la diferencia entre perfil Técnico y perfil Operador;
- preservar el control semantico de riesgo del perfil Operador y su salida estructurada;
- validar cada mejora con preguntas realistas por equipo;
- documentar cada cambio técnico con pruebas y evidencia;
- evitar que el sistema responda sin respaldo documental suficiente o sin una estrategia segura cuando el riesgo sea medio, alto o desconocido;
- diferenciar claramente entre mejoras de backend, frontend, corpus documental y documentación de usuario;
- no reemplazar documentación validada sin revisar el impacto sobre el producto final.
La continuidad del proyecto debería priorizar la madurez del producto antes que la
incorporación acelerada de nuevas funciones. En este tipo de sistema, una mejora
pequeña pero segura, validada y documentada, tiene más valor que una funcionalidad
llamativa que no pueda sostenerse técnicamente.

<!-- Pagina 4 -->

## 4. Prioridades recomendadas para próximas versiones

Prioridad
Línea de trabajo
Motivo
Alta
Curaduría continua del
corpus documental
La calidad del RAG depende directamente de
los documentos procesados, sus metadatos,
páginas, estructura y estado de curaduría.
Alta
Revisión y
reprocesamiento de
manuales críticos
Algunos manuales extensos o complejos
pueden requerir revisión de OCR, Markdown,
chunks, imágenes o estructura para mejorar la
recuperación.
Alta
Mejora de recuperación
por equipo/modelo
específico
Evita mezcla de fuentes entre equipos de una
misma familia, versiones similares o
documentos complementarios.
Alta
Validacion del control semantico de riesgo
El perfil Operador ya incorpora clasificacion de riesgo (`low`, `medium`, `high`, `unknown`) y estrategias de respuesta. Proximas versiones deberian ampliar pruebas reales, metricas y revision humana sobre estos casos.
Media
Ranking, reranking y
expansión semántica de
consultas
Mejora consultas cortas o coloquiales como “no
prende”, “alarma”, “no calibra”, “no ventila”, “no
corta” o “no pasa test”.
Media
Modo extractivo para
códigos técnicos y tests
Permite responder consultas sobre códigos,
errores o pruebas sin que el modelo interprete
de más o invente significados.
Media
Glosario técnico inglés-
español
Mejora la traducción de términos técnicos y
evita interpretaciones poco naturales en
manuales en inglés.
Media
Exportación formal de
consultas e incidentes
Facilita reportes técnicos para Ingeniería
Clínica y seguimiento institucional.
Baja
Analítica histórica
avanzada
Permite detectar tendencias, equipos más
consultados, fallas recurrentes y necesidades
de capacitación.
Baja
Modo capacitación
Puede servir para entrenamiento interno
mediante preguntas frecuentes, tarjetas de
aprendizaje o simulaciones guiadas.
## 5. Líneas de mejora documental

### 5.1 Curaduría continua del corpus

La curaduría documental debe mantenerse como un proceso permanente. Cada nuevo
manual incorporado deberá ser revisado antes de formar parte de la base activa del
asistente.
Se recomienda conservar un registro de:
- documento original;
- equipo asociado;
- fabricante;
- modelo;
- tipo de manual;

<!-- Pagina 5 -->

- idioma;
- estado de procesamiento;
- estado de OCR;
- decisión de curaduría;
- fecha de incorporación;
- responsable de revisión;
- observaciones técnicas.
Esto permitirá evitar que documentos secundarios, duplicados, incompletos o mal
asociados afecten la calidad de las respuestas.
### 5.2 Reprocesamiento de manuales críticos

Algunos manuales requieren atención especial por su extensión, complejidad o
relevancia clínica. En próximas versiones se recomienda revisar manuales con:
- texto extraído de baja calidad;
- OCR incompleto o confuso;
- chunks vacíos o demasiado generales;
- tablas mal interpretadas;
- diagramas sin contexto textual;
- páginas mal asociadas;
- mezcla de documentos principales y complementarios;
- fuentes laterales que dominan consultas generales.
Esta línea es especialmente importante en equipos críticos como ventiladores,
máquinas de diálisis, desfibriladores, esterilizadores e incubadoras.
### 5.3 Mejor trazabilidad entre PDF, Markdown y página visible

El sistema debe conservar internamente la trazabilidad técnica de cada chunk, pero
mostrar al usuario final una referencia comprensible y verificable.
En futuras versiones se recomienda fortalecer el vínculo entre:
- PDF original;
- archivo Markdown procesado;
- número de página real;
- página interna del procesamiento;
- chunk recuperado;
- imagen asociada;
- fuente visible en la interfaz.
El objetivo es que el usuario técnico pueda identificar claramente de qué documento
proviene la información y, cuando sea posible, consultar la página correspondiente en
el PDF original.
### 5.4 Tratamiento de imágenes, tablas y diagramas

Muchos manuales técnicos contienen información relevante en imágenes, tablas,
esquemas eléctricos, diagramas de flujo o capturas de pantalla.

<!-- Pagina 6 -->

En futuras versiones se recomienda avanzar en una estrategia específica para este tipo
de contenido. No alcanza con extraer imágenes de manera automática: también es
necesario determinar si la imagen aporta valor a la consulta y si cuenta con contexto
suficiente para ser interpretada.
Se recomienda trabajar sobre:
- descripción contextual de imágenes relevantes;
- asociación imagen-página-chunk;
- filtrado de imágenes decorativas o poco útiles;
- extracción de tablas técnicas;
- conversión de diagramas críticos a texto estructurado;
- revisión manual de imágenes prioritarias;
- criterio claro para mostrar imágenes en el chat solo cuando aporten a la respuesta.
## 6. Líneas de mejora del RAG

### 6.1 Recuperación por equipo y modelo específico

El sistema debe continuar fortaleciendo la búsqueda restringida al equipo seleccionado.
Esto es especialmente importante en familias de equipos donde existen modelos
similares, manuales de usuario, manuales de servicio, guías rápidas, folletos y
documentos complementarios.
Se recomienda mejorar:
- filtrado por equipo;
- filtrado por modelo;
- aliases controlados;
- diferenciación entre fuente principal y fuente lateral;
- penalización de documentos secundarios cuando la consulta sea general;
- priorización de manuales de servicio o usuario según el perfil y la pregunta.
### 6.2 Ranking y reranking de resultados

La recuperación semántica puede devolver fragmentos relacionados, pero no siempre
los más útiles. Por eso se recomienda avanzar en estrategias de reranking que
consideren:
- coincidencia con el equipo seleccionado;
- tipo de documento;
- fuente principal o complementaria;
- presencia de códigos técnicos exactos;
- presencia de términos críticos de la consulta;
- calidad del chunk;
- cercanía semántica;
- página o sección del manual;
- riesgo de mezclar modelos.
Esto permitiría mejorar la precisión del contexto antes de enviarlo al modelo de lenguaje.

<!-- Pagina 7 -->

### 6.3 Modo extractivo para códigos, errores y tests

Las consultas sobre códigos técnicos, errores, alarmas, tests o abreviaturas requieren
un tratamiento cuidadoso. El modelo no debe expandir siglas, interpretar códigos o
inventar causas si el manual no las define explícitamente.
Se recomienda implementar o profundizar un modo extractivo que:
- detecte códigos técnicos exactos;
- priorice chunks que contengan el código literal;
- extraiga texto directamente del manual;
- indique si la evidencia es parcial;
- evite inferencias no respaldadas;
- diferencie entre código listado, causa, acción correctiva y condición de activación;
- derive o pida aclaración si la documentación no permite responder con seguridad.
### 6.4 Evaluación de evidencia antes de responder

El sistema debería continuar avanzando hacia una lógica tipo Self-RAG, en la que no
se genere una respuesta automáticamente solo porque se recuperaron fragmentos.
Antes de responder, el sistema debería evaluar:
- si los fragmentos pertenecen al equipo correcto;
- si la fuente es principal o secundaria;
- si la evidencia recuperada es suficiente, parcial o débil;
- si hay mezcla de documentos;
- si existe riesgo de alucinación;
- si corresponde responder, pedir aclaración, usar modo extractivo o rechazar la respuesta.
Este enfoque mejora la seguridad y la confiabilidad del asistente.
## 7. Mejoras funcionales candidatas

Las siguientes funcionalidades podrían incorporarse en futuras versiones, según
disponibilidad técnica, necesidad institucional y validación con Ingeniería Clínica.
### 7.1 ABM de equipos y modelos

Incorporar una interfaz administrativa para gestionar:
- equipos;
- fabricantes;
- modelos;
- alias;
- servicios hospitalarios;
- ubicaciones físicas;
- documentación asociada;

<!-- Pagina 8 -->

- estado activo o inactivo del equipo.
Esto permitiría mantener actualizado el catálogo sin depender exclusivamente de
cambios en código.
### 7.2 Carga asistida de manuales

Incorporar una funcionalidad para cargar manuales desde la interfaz técnica, con
controles previos antes de indexar.
La carga asistida podría verificar:
- si el archivo es PDF válido;
- si contiene texto extraíble;
- si requiere OCR;
- si ya existe un documento similar;
- a qué equipo o modelo corresponde;
- si debe quedar activo, en revisión o excluido;
- si se generó correctamente el Markdown o representación procesada;
- si ChromaDB debe reconstruirse o actualizarse.
### 7.3 Versionado del corpus

Registrar qué versión del corpus respalda cada respuesta permitiría mejorar la
trazabilidad y auditoría del sistema.
Se recomienda registrar:
- versión del corpus;
- fecha de ingesta;
- documentos incluidos;
- documentos excluidos;
- cantidad de chunks;
- responsable de curaduría;
- parámetros de ingesta;
- estado de ChromaDB.
Esto permitiría saber con qué base documental respondió el asistente en un momento
determinado.
### 7.4 Evaluación automática de calidad de respuestas

Se recomienda construir baterías de preguntas por equipo para validar automáticamente
el comportamiento del RAG.
Estas pruebas deberían incluir:
- preguntas técnicas;
- preguntas de operador;
- consultas cortas;
- consultas mal redactadas;
- códigos técnicos;
- alarmas;

<!-- Pagina 9 -->

- fallas frecuentes;
- consultas fuera de alcance;
- preguntas sin respaldo documental.
La evaluación debería clasificar respuestas como aceptables, parciales, inseguras,
incorrectas o sin evidencia suficiente.
### 7.5 Exportación de consultas e incidentes

En versiones futuras, el sistema podría permitir exportar registros en CSV o PDF, con
filtros por:
- fecha;
- equipo;
- perfil de usuario;
- tipo de consulta;
- incidente registrado;
- servicio hospitalario;
- usuario;
- prioridad;
- estado.
Esta funcionalidad podría apoyar el seguimiento técnico, sin reemplazar los registros
institucionales formales de mantenimiento.
### 7.6 Dashboard de mantenimiento y recurrencia

El Centro de Monitoreo podría evolucionar hacia un tablero más completo para
visualizar:
- equipos más consultados;
- fallas más frecuentes;
- alarmas recurrentes;
- consultas por perfil;
- consultas por servicio;
- incidentes sugeridos;
- tendencias mensuales;
- necesidades de capacitación;
- equipos con mayor demanda de soporte.
Esta información podría servir como insumo para análisis preventivo, capacitación
interna o priorización de mantenimiento.
### 7.7 Integración con sistemas institucionales

En caso de existir disponibilidad institucional, el asistente podría integrarse con:
- inventario hospitalario;
- sistema de mantenimiento;
- sistema de tickets;
- registro de órdenes de trabajo;
- base de activos biomédicos;
- directorio de usuarios institucionales.

<!-- Pagina 10 -->

Esta integración debería evaluarse cuidadosamente, ya que implica requisitos
adicionales de seguridad, autenticación, permisos, interoperabilidad y protección de
datos.
### 7.8 Modo capacitación

El sistema podría incorporar un modo orientado a capacitación interna, con:
- preguntas frecuentes por equipo;
- tarjetas de aprendizaje;
- simulaciones guiadas;
- recorridos por manuales;
- explicación de alarmas frecuentes;
- material de inducción para nuevos técnicos u operadores.
Este modo debería diferenciarse claramente del modo de asistencia operativa, para no
confundir formación con indicaciones de intervención real.
## 8. Correcciones técnicas recomendadas

Para
próximas
iteraciones
se
recomiendan
las
siguientes
correcciones
y
fortalecimientos técnicos:
- robustecer OCR selectivo para PDFs con bajo texto extraíble;
- revisar manuales críticos con chunks vacíos, pobres o mal segmentados;
- mejorar detección de páginas oficiales cuando existan mapeos dudosos;
- separar equipos agrupados por marca o familia cuando exista riesgo de mezcla documental;
- agregar pruebas de regresión para consultas críticas por equipo;
- mejorar recuperación ante consultas sobre tests, códigos, alarmas y fallas de arranque;
- fortalecer autenticación si el sistema pasa de prototipo local a uso institucional sostenido;
- documentar procedimientos de reconstrucción de ChromaDB;
- normalizar logs, backups de ChromaDB y SQLite;
- definir procedimiento de restauración ante fallas;
- mejorar control de imágenes visibles en respuestas;
- ocultar fuentes duplicadas, internas o poco relevantes;
- asegurar que las fuentes mostradas correspondan al contenido realmente utilizado;
- separar documentación técnica interna de documentación visible para usuario final;
- mantener una matriz de validación por equipo y perfil;
- registrar cada cambio relevante en bitácora técnica.
## 9. Criterios para priorizar próximos sprints

Para decidir qué mejoras abordar primero, se recomienda utilizar los siguientes criterios:

<!-- Pagina 11 -->

Criterio
Pregunta orientadora
Seguridad del usuario y del
paciente
¿La mejora reduce riesgo operativo, clínico o técnico?
Impacto funcional
¿Afecta a muchos equipos o a consultas frecuentes?
Riesgo de mezcla
documental
¿Puede evitar respuestas basadas en manuales
incorrectos?
Calidad de evidencia
¿Mejora la trazabilidad o el respaldo documental?
Esfuerzo técnico
¿Puede implementarse sin romper funcionalidades ya
validadas?
Valor para Ingeniería
Clínica
¿Aporta utilidad concreta al equipo usuario?
Madurez del prototipo
¿Fortalece el sistema como producto real y no solo como
demostración?
Mantenibilidad
¿Facilita futuras actualizaciones del corpus o del código?
Continuidad académica
¿Ayuda a que futuras cohortes puedan continuar el
proyecto sin empezar desde cero?
## 10. Recomendación de orden de implementación

Como hoja de ruta preliminar, se propone el siguiente orden para próximas versiones:
1. Revisar el estado actual del repositorio, rama final y documentación entregada.

## 2. Comprender la arquitectura existente antes de modificar código.

## 3. Consolidar curaduría documental continua y versionado del corpus.

## 4. Mejorar recuperación por equipo, modelo y tipo de fuente.

## 5. Profundizar modo extractivo para códigos, tests y alarmas.

## 6. Reforzar trazabilidad entre PDF original, Markdown, página y chunk.

## 7. Ampliar pruebas automáticas de calidad por equipo.

## 8. Mejorar manejo de imágenes, tablas y diagramas técnicos.

## 9. Incorporar glosario técnico inglés-español.

## 10. Desarrollar carga asistida de manuales desde interfaz técnica.

## 11. Fortalecer Centro de Monitoreo y exportación de consultas.

## 12. Evaluar integración con inventario, tickets o sistemas institucionales.

Este orden prioriza primero comprensión, confiabilidad, seguridad y trazabilidad, y deja
para etapas posteriores las funcionalidades de integración, analítica avanzada o
capacitación.
## 11. Recomendaciones para el próximo equipo de desarrollo

Para quienes continúen el proyecto, se recomienda comenzar con una etapa de lectura
y diagnóstico antes de implementar cambios.
Los primeros pasos sugeridos son:

<!-- Pagina 12 -->

1. Revisar el Manual de Usuario, la Guía Técnica de Instalación, el Informe de

Dificultades Encontradas, el Informe de Validación RAG y este Documento de
Continuidad.
## 2. Identificar cuál es la rama final entregada y cuál es el estado estable del

repositorio.
## 3. Levantar el sistema localmente siguiendo la guía técnica.

4. Verificar que los modelos locales, ChromaDB y la base documental estén

disponibles.
5. Probar el sistema sin modificar código, utilizando preguntas reales por equipo.

6. Revisar la matriz de validación existente y detectar qué respuestas siguen siendo

mejorables.
## 7. Definir un objetivo pequeño y verificable para el primer sprint de continuidad.

8. Evitar modificaciones simultáneas sobre frontend, backend, corpus y

documentación.
9. Registrar cada cambio en una bitácora técnica.

10. Validar cada mejora antes de considerarla integrada.

También se recomienda mantener una organización clara de roles:
- una persona o subequipo para backend/RAG;
- una persona o subequipo para frontend/interfaz;
- una persona o subequipo para curaduría documental;
- una persona o subequipo para validación y documentación.
La experiencia del sprint final demostró que el proyecto mejora cuando cada cambio
tiene objetivo concreto, prueba asociada y registro documental.
## 12. Riesgos a evitar en la continuidad

Durante próximas etapas, deberían evitarse algunos riesgos que pueden afectar la
estabilidad del sistema:
- agregar documentos al corpus sin curaduría previa;
- mezclar manuales de equipos similares sin diferenciar modelos;
- reconstruir ChromaDB sin registrar qué corpus se utilizó;
- modificar guardrails de seguridad sin validar respuestas de operador;
- agregar funciones nuevas sin comprobar que no rompan lo existente;
- entrenar o ajustar el sistema solo con preguntas preparadas para demostración;
- mostrar páginas o fuentes no confiables como si fueran verificadas;
- usar el asistente como sistema formal de mantenimiento sin integración institucional adecuada;
- convertir el Centro de Monitoreo en reemplazo de registros oficiales;
- exponer información interna de desarrollo al usuario final;
- confundir documentación académica, documentación técnica y manuales de usuario.
El objetivo de la continuidad no debería ser “hacer más cosas” rápidamente, sino
fortalecer lo que ya funciona y ampliar el sistema de manera gradual, segura y trazable.

<!-- Pagina 13 -->

## 13. Conclusión

El Asistente IA para Ingeniería Clínica – HRRG alcanzó una base funcional que permite
consultar documentación técnica mediante una interfaz orientada a perfiles de usuario,
con recuperación documental, trazabilidad de fuentes, criterios de seguridad y
validación por equipo.
El escalamiento del sistema debe sostener el mismo criterio aplicado durante el
desarrollo: priorizar respuestas confiables, seguras, trazables y respaldadas por
documentación.
Las mejoras futuras no deberían orientarse únicamente a agregar nuevas funciones
visibles, sino a fortalecer la calidad del corpus, la precisión de la recuperación, la
seguridad de las respuestas y la mantenibilidad del sistema.
Este documento deja registrada una hoja de ruta posible para próximas versiones, con
foco en continuidad técnica, madurez del producto y utilidad real para Ingeniería Clínica.
Finalmente, busca servir como puente entre el equipo que desarrolló el prototipo inicial
y quienes puedan continuarlo en próximos ciclos académicos. La intención es que las
futuras cohortes no partan desde cero, sino desde una base técnica documentada, con
decisiones justificadas, problemas identificados y una hoja de ruta orientada a mejorar
el sistema de manera segura, progresiva y trazable.
Sprint final – Junio 2026
