# Validación de recuperación documental – 22 equipos indexados

**Fecha:** 30/05/2026  
**Rama:** `prueba-markdown-dario`  
**Proyecto:** Asistente IA para Ingeniería Clínica HRRG  
**Base vectorial:** ChromaDB – colección `manuales_hrrg`

## 1. Objetivo

Validar la calidad de recuperación documental del sistema RAG sobre los 22 equipos actualmente indexados, utilizando consultas libres similares a las que podría realizar un usuario técnico u operador ante fallas reales.

La validación buscó clasificar cada equipo según:

- recuperación buena / validada;
- recuperación útil pero mejorable mediante expansión o ranking;
- limitación documental o consulta no respaldada claramente;
- necesidad de reprocesamiento documental;
- riesgo de mezcla de modelos o fuentes.

No se realizaron nuevos cambios de código durante esta validación. El objetivo fue diagnosticar el estado del corpus y de la recuperación ya disponible.

---

## 2. Estado general del corpus

Se verificó que la curaduría activa y ChromaDB se encuentran alineados:

- `curaduria_activa.csv`: 59 fuentes activas.
- ChromaDB: 59 fuentes únicas.
- Diferencias entre CSV y Chroma: 0.
- Equipos únicos indexados: 22.
- Chunks totales: 8650.

También se verificó que no persisten fuentes con equipo vacío, “sin equipo asociado”, “unknown” o error en metadatos.

---

## 3. Equipos indexados

| N.º | Equipo | Chunks |
|---:|---|---:|
| 01 | Agitador Presvac AE500 | 59 |
| 02 | Bilirrubinómetro Draeger JM-105 | 214 |
| 03 | Cabina de bioseguridad | 8 |
| 04 | Cama electrónica | 147 |
| 05 | Desfibrilador Mindray BeneHeart | 189 |
| 06 | Dinan AF500 | 137 |
| 07 | Electrobisturí | 785 |
| 08 | Equipo TP 100 | 65 |
| 09 | Esterilizadora Sterrad 100 | 516 |
| 10 | Incubadora Medix TR306 | 697 |
| 11 | Micrótomo Leica RM2125 | 114 |
| 12 | Monitor multiparamétrico | 648 |
| 13 | Máquina de diálisis Fresenius 4008 | 228 |
| 14 | Procesador de tejidos Leica TP1020 | 475 |
| 15 | Respirador Draeger - VN500 | 349 |
| 16 | Rodantes MAC GMM | 19 |
| 17 | Ventilador Crossvent | 490 |
| 18 | Ventilador Engström | 1513 |
| 19 | Ventilador Leistung LUFT3 | 236 |
| 20 | Ventilador Maquet Servo-i | 189 |
| 21 | Ventilador Neumovent GraphNet | 1378 |
| 22 | Ventilador Newport HT70 | 194 |

---

## 4. Clasificación general

### 4.1 Equipos validados / recuperación buena

Estos equipos recuperaron contenido documental útil, específico y defendible para las consultas probadas:

- Agitador Presvac AE500.
- Desfibrilador Mindray BeneHeart.
- Esterilizadora Sterrad 100.
- Incubadora Medix TR306.
- Máquina de diálisis Fresenius 4008.
- Procesador de tejidos Leica TP1020.
- Ventilador Engström.
- Ventilador Leistung LUFT3.
- Ventilador Maquet Servo-i.
- Ventilador Newport HT70.

### 4.2 Recuperación útil, pero mejorable por expansión o ranking

Estos equipos tienen contenido útil, pero algunas consultas cortas o abiertas requieren mejor expansión semántica, ranking o mayor precisión de modelo/fuente:

- Bilirrubinómetro Draeger JM-105.
- Cama electrónica.
- Dinan AF500.
- Electrobisturí.
- Micrótomo Leica RM2125.
- Monitor multiparamétrico.
- Rodantes MAC GMM.
- Ventilador Crossvent.
- Ventilador Neumovent GraphNet.

### 4.3 Limitación documental o consulta no respaldada claramente

Estos casos no parecen fallar por backend, sino por escasez documental o porque la consulta no está claramente respaldada en el corpus actual:

- Cabina de bioseguridad.
- Equipo TP 100.

### 4.4 Reprocesamiento documental prioritario

- Respirador Draeger - VN500.

El manual principal figura indexado con 311 chunks, pero todos los chunks inspeccionados contienen únicamente el encabezado:

```text
**Equipo:** Respirador Draeger - VN500

````

Esto confirma que el problema de VN500 no está en el prompt, ni en el valor de `k`, ni en la expansión semántica. El manual principal debe reprocesarse desde el PDF original, aplicar OCR si corresponde o reconstruir el Markdown antes de reingestar.

---

## 5. Hallazgos principales

### 5.1 Equipos con recuperación sólida

Se consideran sólidos para validación técnica inicial los siguientes equipos:

- Agitador Presvac AE500: recupera correctamente fallas como “no agita” y “batería baja”.
- Desfibrilador Mindray BeneHeart: recupera correctamente información sobre falla de carga, batería, fuente, capacitor y errores de energía.
- Esterilizadora Sterrad 100: recupera cancelación de ciclo, presión fuera de rango, potencia RF, plasma no encendido y baja potencia de plasma.
- Incubadora Medix TR306: recupera baja temperatura, alarma de temperatura de aire, calefactor, sensor y condiciones ambientales.
- Fresenius 4008: recupera T1 test, test unsuccessful, error display, incorrect test step y subtests.
- Leica TP1020: recupera modo automático, inicio de programa, estaciones, canastos, tiempo de infiltración y recuperación luego de proceso abortado.
- Engström: recupera apnea, desconexión, fugas, VMesp bajo, PEEPe baja y ventilación de respaldo.
- Leistung LUFT3: recupera presión inspiratoria máxima, alta presión inspiratoria, causas y acciones correctivas.
- Servo-i: recupera alarma de oxígeno, celda O2, concentración medida, degradación de celda, Pre-use check y módulos de gas.
- Newport HT70: recupera batería, Power Pac, alimentación externa, conmutación a batería y chequeo integrado de batería.

### 5.2 Equipos con recuperación útil pero mejorable

Estos equipos tienen contenido documental útil, pero podrían beneficiarse de expansiones semánticas o ajustes de ranking:

- Bilirrubinómetro Draeger JM-105: el contenido útil existe, especialmente Light Checker, rango aceptable, fuera de rango, limpieza de sonda/comprobador y contacto con DrägerService. La consulta “no mide bilirrubina” no siempre prioriza ese contenido.
- Cama electrónica: recupera control de mano, botón GO, botón STOP, batería, fusibles, ajustes y movimiento, pero la consulta corta “no sube” requiere expansión.
- Dinan AF500: recupera fuente switching, 12VDC, 220VAC, contactor de línea, precauciones eléctricas y LED de placa driver si la consulta se formula con términos técnicos.
- Electrobisturí: recupera contenido útil sobre placa paciente, electrodo activo, potencia, CUT/COAG, salida y pruebas, pero mezcla modelos Valleylab, Kairos y LEEP.
- Micrótomo Leica RM2125: recupera cuchilla, portacuchillas, espesor de corte, ángulo libre, vibración y mantenimiento, aunque no se detectó una tabla explícita de troubleshooting.
- Monitor multiparamétrico: recupera ECG Lead Off, electrodos, lead wire, adapter cable, ECG Amplitude Too Small, signal noise y movimiento del paciente, pero puede mezclar modelos ePM, iMEC y PM-9000.
- Rodantes MAC GMM: recupera PREP+RAD, filamento, autocalibración, fusibles y cableado, pero el corpus es pequeño.
- Ventilador Crossvent: recupera presión baja, desconexión, PEEP/CPAP, volumen tidal bajo, tubo proximal y transductor, pero requiere expansión/ranking.
- Neumovent GraphNet: recupera apnea, fugas, circuito paciente, presión continuada alta, obstrucción y sensores de presión, pero la consulta “no ventila” es muy amplia y puede dispersarse.

### 5.3 Equipos con limitación documental

- Cabina de bioseguridad: solo tiene 8 chunks y páginas 1 a 3. Recupera low air flow alarm, posición de ventana frontal, HEPA, motor blower, sensor volumétrico y alarmas, pero no alcanza para troubleshooting profundo.
- Equipo TP 100: ante “error de temperatura” no se encontró respaldo claro. El corpus recupera más presión, caudal, conductividad, filtros, bomba, alimentación de agua y sanitización.

### 5.4 Reprocesamiento prioritario

- Respirador Draeger - VN500: el manual principal está indexado vacío. Debe reprocesarse antes de volver a validar preguntas sobre presión, alarma, PEEP, Paw, ventilación o troubleshooting.

---

## 6. Observaciones transversales

### 6.1 Fuentes visibles

Se verificó que las respuestas ya muestran fuentes visibles como PDF y página, evitando exponer archivos `.md` internos. Esto mejora la trazabilidad para el usuario técnico.

Ejemplo esperado:

```text
Fuente: fresenius_4008_service_manual.pdf, pag. 3
````

### 6.2 Traducción automática del fallback

El fallback con traducción automática es útil, pero algunas traducciones técnicas quedan poco naturales.

Ejemplos detectados:

* “nuisance alarm” fue traducido como “alarmón de molestia”.
* “RF Amplifier Failure” fue traducido como “Fallimiento del Amplificador RF”.
* “Low plasma power” fue traducido como “Poder de plasma bajo”.

Esto no bloquea la validación actual, pero queda como mejora futura: normalizar términos técnicos frecuentes o ajustar la traducción técnica.

### 6.3 Agrupación de modelos

Algunos equipos agrupan varios modelos bajo una misma etiqueta general. Esto puede generar mezcla de fuentes en consultas genéricas.

Casos relevantes:

* Electrobisturí: Valleylab, Kairos y LEEP.
* Monitor multiparamétrico: ePM, iMEC y PM-9000.
* Neumovent GraphNet: GraphNet, Advance TS Neo, Neo, manual técnico bebé y manual de calibración.

Para uso real, el QR o selección de modelo específico debería reducir esta ambigüedad.

### 6.4 Expansiones futuras candidatas

No se recomienda seguir agregando expansiones una por una sin priorización. Candidatos futuros:

* Cama electrónica: no sube, no baja, no responde mando.
* Dinan AF500: no enciende, pantalla apagada, fuente, 12VDC, 220VAC.
* Monitor multiparamétrico: sin señal ECG, ECG Lead Off, electrodos, cable, interferencia.
* Bilirrubinómetro JM-105: no mide, fuera de rango, Light Checker, limpiar sonda/comprobador.
* Crossvent: alarma presión baja, desconexión, fuga, PEEP/CPAP baja.
* Neumovent GraphNet: no ventila, apnea, fugas, obstrucción, sensores de presión.
* Electrobisturí: no corta, no coagula, sin potencia, diferenciando modelo.
* Micrótomo Leica RM2125: no corta bien, corte irregular, ángulo libre, espesor, vibración.
* Rodantes MAC GMM: no dispara, PREP+RAD, filamento, fusibles.

---

## 7. Decisiones

1. No realizar nuevos cambios de backend durante esta validación.
2. No hacer microcommits por cada mejora potencial.
3. Mantener los hallazgos clasificados para priorizar después.
4. Reprocesar prioritariamente el manual principal de Draeger VN500.
5. No intentar resolver Draeger VN500 con prompt, expansión o aumento de `k`.
6. Mantener las expansiones futuras como bloque de mejora planificado.
7. Tratar los casos con múltiples modelos mediante QR o modelo específico cuando sea posible.
8. Documentar la limitación de corpus en Cabina de bioseguridad y TP100.
9. Mantener Git limpio después de pruebas que modifican `data/memory/conversation.sqlite3`.

---

## 8. Estado final

```text
Equipos indexados: 22
Fuentes activas: 59
Chunks totales: 8650
Estado Chroma vs curaduría: consistente
Problema crítico único: Draeger VN500 con manual principal vacío
Cambios de código en este bloque: ninguno
```

---

## 9. Próximos pasos recomendados

1. Reprocesar/OCR/reconstruir Markdown de `drager_vn500_manual_usuario_vn500_es.pdf`.
2. Reingestar Draeger VN500 y validar nuevamente consultas de presión, alarma, PEEP, Paw, ventilación y troubleshooting.
3. Priorizar un bloque único de expansiones semánticas para consultas frecuentes, evitando microcambios.
4. Revisar si TP100 posee documentación adicional sobre temperatura o si la consulta “error de temperatura” no corresponde al manual disponible.
5. Ampliar corpus de Cabina de bioseguridad si se espera soporte técnico más profundo.
6. Considerar mejora futura del fallback de traducción técnica.
7. Mantener validación por equipo con consultas libres reales, no preguntas demo cerradas.
