# 📊 Resumen de Cambios No Committeados

**Rama:** `prueba-markdown-dario`  
**Última sincronización con origen:** `fa79673 - Ignorar conversation.sqlite3 en el repo`  
**Fecha de reporte:** 1 de junio de 2026  

---

## 📈 Estadísticas Generales

- **Total de archivos modificados:** 32
- **Total de líneas agregadas:** 250 (+)
- **Total de líneas eliminadas:** 54 (-)
- **Cambios de codificación:** LF → CRLF (avisos en archivos de código)

---

## 🔧 Cambios en Servicios Python

### 1. `app/services/knowledge_audit_service.py` (+14 líneas, -14 líneas)

**Cambios de acentuación en categorías de consultas técnicas:**
- Corregidas tildes en nombres de categorías para mejor presentación
  - `"Calibracion"` → `"Calibración"`
  - `"Energia"` → `"Energía"`
  - `"Consulta tecnica"` → `"Consulta técnica"`
  - `"Pantalla tactil"` → `"Pantalla táctil"`
  - `"Bateria / carga"` → `"Batería / carga"`
  - `"Presion"` → `"Presión"`

**Impacto:** Mejora la presentación visual y legibilidad de categorías en reportes de auditoría

---

### 2. `app/services/vectorstore_service.py` (+13 líneas, -1 línea)

**Nuevas funcionalidades:**
- ✅ Importación de `IngestionAuditService`
- ✅ Integración de información de auditoría de ingesta con timestamps
  - Nueva estructura: `audits_by_source` para mapear archivos fuente con su información de creación
  - Campo `created_at`: Ahora obtiene el timestamp real de cuando se ingirió el documento
  - Campo `source_url`: Nuevo campo que preserva URLs de fuentes en metadatos
- ✅ Mejora en la trazabilidad de documentos con timestamps de ingesta reales
- ✅ Salto de línea final corregido (cambio de formato)

**Impacto:** Mejor rastreo de documentos, timestamps más precisos en búsquedas RAG

---

## 🎨 Cambios en Estilos (CSS)

### `static/css/base.css` (+25 líneas)
- Mejoras generales en estilos base
- Ajustes de responsive design

### `static/css/chat.css` (+159 líneas, -1 línea)

**Nuevos componentes de interfaz:**

1. **Botón QR de Equipo** (`.equipment-qr-button`)
   - Botón cuadrado de 30x30px con borde redondeado
   - Ícono QR de 17x17px
   - Efectos hover: cambio de borde a naranja y mayor opacidad de fondo
   - Ubicación: Junto al nombre del equipo activo

2. **Botón PDF de Manual** (`.manual-pdf-button`)
   - Botón inline-flex con borde verde oscuro (#0f766e)
   - Fondo verde claro (#ecfdf5)
   - Font weight: 950 (muy bold)
   - Hover: cambio a verde más oscuro (#ccfbf1)
   - Posicionamiento: En filas de manuales de equipos

3. **Mejoras en Grid de Manuales**
   - Redefinición de `grid-template-columns`: ahora `auto minmax(220px, 1.4fr) auto`
   - Mejor distribución de botones PDF y QR

4. **Cambios en estructura de paneles**
   - `.manual-equipment` → renombrado a `.manual-status-group`
   - Cambio de layout: `gap: 5px` → `gap: 6px`
   - Alineación: `justify-items: end` para alineación derecha
   - Eliminación de estilos redundantes para `strong` en `.manual-equipment`

5. **Ajustes de diálogos de monitoreo**
   - Nueva clase `.monitoring-dialog` con `overflow: hidden`
   - División de paneles:
     - `.audit-panel`: `overflow-y: auto`
     - `.monitoring-panel`: `overflow-y: hidden` → `overflow: auto` con scroll horizontal oculto
   - Nueva sección `.monitoring-consultation-list`: max-height 320px con scroll

6. **Responsividad móvil (max-width: 760px)**
   - Ajustes en la barra superior compacta (`.chat-compact-topbar`)
   - Redimensionamiento del botón QR en móvil (30x30px)
   - Mejora de espaciado en equipos activos

7. **Otros ajustes**
   - Reducción de `stroke-width` en iconos de habla: 2 → 1.5
   - Nuevas reglas al final para asegurar colocación correcta de QR

**Impacto:** Interfaz más completa con funcionalidad QR y PDF directamente accesible

---

## 💻 Cambios en JavaScript

### `static/js/chat.js` (+66 líneas, -66 líneas)

- Refactorización significativa (66 líneas reescritas)
- Probablemente mejoras en:
  - Manejadores de eventos del botón QR
  - Lógica del botón PDF de manuales
  - Interactividad de diálogos de monitoreo
  - Gestión de scroll en paneles

**Impacto:** Mejora en interactividad y funcionalidad del chat

---

## 📄 Cambios en Templates HTML

### `templates/base.html` (+10 líneas, -1 línea)
- Posibles actualizaciones en estructura base o head

### `templates/operator.html` (+6 líneas, -1 línea)
- Mejoras en layout del panel operador

### `templates/operator_select.html` (+2 líneas, -1 línea)
- Pequeños ajustes en selección de operador

### `templates/partials/chat_panel.html` (+2 líneas, -1 línea)
- Actualización del panel de chat (probablemente: nuevo botón QR)

### `templates/technician.html` (+7 líneas, -1 línea)
- Mejoras en layout del panel técnico

**Impacto:** Integración de nuevos elementos QR y PDF en la interfaz

---

## 🖼️ Cambios en Archivos QR (Imágenes)

**24 archivos QR regenerados** con pequeños ajustes binarios:
- Los cambios de tamaño son mínimos (típicamente 10-100 bytes)
- Probablemente resultado de reoptimización o cambios menores en color/metadata
- **Archivos afectados:**
  - Todos los QR de equipos (21 imágenes .png)
  - PDF de equipos HRRG (1 archivo .pdf)

**Hipótesis:** Los códigos QR fueron regenerados como parte de mejoras visuales o actualizaciones de URLs

---

## 📋 Resumen de Funcionalidades Agregadas

### ✅ Integración QR en Chat
- Botón QR accesible directamente desde el nombre del equipo activo
- Estilos hover interactivos
- Responsive en móvil

### ✅ Botones de Descarga PDF de Manuales
- Botón directo en cada fila de manual
- Diseño verde Tailwind (#0f766e)
- Accesible y con feedback visual

### ✅ Mejora de Auditoría
- Timestamps reales de ingesta de documentos
- URLs de fuentes preservadas
- Mejor rastrabilidad en sistema RAG

### ✅ Mejoras UI/UX
- Paneles de monitoreo mejor organizados
- Mejor responsividad móvil
- Mejor distribución de botones en grid

---

## 🔍 Próximos Pasos Sugeridos

1. **Commit estos cambios:**
   ```bash
   git add -A
   git commit -m "feat(ui,services): integración QR, botones PDF y mejora de auditoría"
   ```

2. **Verificar funcionamiento:**
   - Probar botones QR en equipos
   - Probar descarga de PDFs de manuales
   - Validar responsividad en móvil

3. **Consideración de codificación:**
   - Los archivos Python/CSS/JS tienen LF que se convertirán a CRLF
   - Posiblemente agregar configuración `.gitattributes` para normalizar finales de línea

---

**Generado:** 2026-06-01 | **Estado:** 32 archivos en cambios no staged
