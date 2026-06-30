# Guía Técnica de Instalación, Configuración y Puesta en Marcha

- Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial
- Práctica Profesionalizante II
- Documento técnico para implementación y soporte del sistema
- Asistente IA para Ingeniería Clínica – HRRG
**Institución destinataria:** Hospital Regional Río Grande
**Área destinataria:** Sistemas / soporte técnico / administración técnica del sistema
- Equipo N.º 1:
  - Ana María Ramos Orcko
  - Darío Agustín García Barquet
  - Marisa Mercedes Velásquez
  - Nancy Julieta Cassano  

**Versión 1.0**
**Junio 2026**
**Tierra del Fuego, Antártida e Islas del Atlántico Sur**

## 1. Propósito del documento

Esta guía tiene como finalidad orientar al personal técnico responsable en la instalación,
configuración inicial, puesta en marcha y verificación operativa del Asistente IA para
Ingeniería Clínica – HRRG.
El documento describe los requisitos del entorno, los componentes principales del sistema,
los pasos necesarios para ejecutar la aplicación, la validación de servicios asociados, el
acceso desde red local, la verificación de la base documental y las acciones básicas de
diagnóstico ante problemas frecuentes.
Está destinada al personal de Sistemas, soporte técnico o responsables técnicos designados
para administrar el entorno donde se ejecuta el asistente.
## 2. Alcance

La guía incluye:
- requisitos básicos de hardware y software;
- obtención del proyecto desde el repositorio GitHub oficial;
- preparación del entorno virtual de Python;
- instalación de dependencias;
- verificación de Python, Git y entorno virtual;
- verificación de Ollama y modelos locales requeridos;
- revisión de la configuración inicial del entorno;
- verificación de la base documental procesada;
- disponibilidad y control de la base vectorial ChromaDB;
- ejecución de la aplicación Flask;
- acceso desde la computadora local;
- acceso desde otros dispositivos de la red;
- verificación de manuales cargados;
- validación de funcionamiento del chat;
- regeneración o verificación de códigos QR;
- pruebas mínimas posteriores a la puesta en marcha;
- problemas frecuentes y acciones de diagnóstico;
- consideraciones básicas de seguridad operativa.
No incluye instrucciones de uso cotidiano para operadores o técnicos usuarios finales. Esas
indicaciones forman parte del Manual de Usuario.

<!-- Pagina 4 -->

## 3. Componentes principales del sistema

El Asistente IA para Ingeniería Clínica – HRRG está compuesto por los siguientes
componentes técnicos:
| Componente           | Función                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| Aplicación web Flask | Permite el acceso a la interfaz del asistente, perfiles de usuario, selección de equipos y chat.             |
| Backend Python       | Gestiona la lógica de consulta, recuperación documental, generación de respuestas y guardrails de seguridad. |
| Ollama               | Ejecuta localmente el modelo de lenguaje utilizado por el asistente.                                         |
| ChromaDB             | Almacena los embeddings de los documentos procesados y permite la búsqueda vectorial.                        |
| Corpus documental    | Conjunto de manuales técnicos procesados e indexados para consulta.                                          |
| Módulo de ingesta    | Procesa documentos, genera chunks, metadatos e indexación vectorial.                                         |
| Módulo QR            | Genera códigos QR asociados a equipos para acceso directo.                                                   |
| Interfaz web         | Permite el uso del sistema desde navegador en computadora o dispositivo móvil conectado a la red.            |

flowchart TD
    A[Manuales técnicos / documentación procesada]
    B[Procesamiento documental]
    C[Chunks + metadatos + páginas + fuentes]
    D[ChromaDB]
    E[Recuperación documental por equipo]
    F[Ollama / modelo local]
    G[Respuesta del asistente con fuentes y guardrails]
    H[Interfaz web Flask]

    A --> B --> C --> D --> E --> F --> G --> H

    classDef proceso fill:#9bd4df,stroke:#5aa7b2,color:#000,font-weight:bold;
    class A,B,C,D,E,F,G,H proceso;


## 4. Requisitos previos

Antes de poner en marcha el sistema, se debe contar con:
- equipo o servidor definido para ejecutar la aplicación;
- sistema operativo compatible;
- Git instalado o herramienta equivalente para descargar el repositorio;
- acceso autorizado al repositorio GitHub del proyecto;
- conexión a internet para descargar el repositorio, dependencias y modelos locales cuando corresponda;
- Python instalado;
- entorno virtual del proyecto;
- dependencias instaladas;
- Ollama instalado y operativo;
- modelo de lenguaje descargado localmente;
- carpeta del proyecto disponible;
- base documental procesada;
- base vectorial ChromaDB disponible o reconstruible únicamente por personal técnico autorizado;
- navegador web actualizado;
- conexión a la red local donde se utilizará el asistente.
## 5. Obtención del proyecto desde GitHub

La versión final del Asistente IA para Ingeniería Clínica – HRRG se entrega mediante el
repositorio GitHub oficial del proyecto.
El personal técnico responsable de la instalación deberá descargar o clonar el repositorio en
el equipo o servidor donde se ejecutará la aplicación.
Para la instalación operativa se utilizará la rama principal del repositorio: main
No se requiere utilizar ramas de desarrollo, ramas experimentales ni versiones intermedias
del proyecto.
Procedimiento general:
`git clone https://github.com/Marisav09/Equipo_PP2-HRRG-2-2026`
`cd Equipo_PP2-HRRG-2-2026`
`git checkout main`
Una vez clonado el repositorio, se recomienda registrar la fecha de instalación y el commit
utilizado, para conservar trazabilidad técnica de la versión instalada.

Registro sugerido para instalación:
- Repositorio utilizado: https://github.com/Marisav09/Equipo_PP2-HRRG-2-2026
- Rama utilizada: main
- Commit utilizado: v1.0-hrrg
- Fecha de instalación: ___________________________
- Responsable técnico: ___________________________   
  
Estructura general del repositorio Proyecto Asistente IA HRRG  
│  
├── app  
│ └── Lógica principal del backend, servicios, rutas y configuración interna.
│
├── data
│ └── Datos del sistema, base documental procesada, memoria local y
recursos asociados.
│
├── scripts
│ └── Scripts auxiliares para ingesta, procesamiento, validación y tareas
técnicas.
│
├── static
│ └── Archivos estáticos de la interfaz: estilos CSS, JavaScript, imágenes
y recursos visuales.
│
├── templates
│ └── Plantillas HTML utilizadas por la aplicación web Flask.
│
├── tests
│ └── Archivos de prueba y validación técnica del sistema.
│
├── requirements.txt
│ └── Dependencias necesarias para instalar y ejecutar el proyecto.
│
├── .env.example
│ └── Archivo de referencia para configurar variables de entorno.
│
├── README.md
│ └── Descripción general del proyecto y orientación técnica inicial.
│
└── run.py
└── Archivo principal para iniciar la aplicación.

## 6. Preparación del entorno virtual

Una vez descargado o clonado el repositorio, el personal técnico debe preparar el entorno
virtual de Python dentro de la carpeta raíz del proyecto.
El entorno virtual permite instalar las dependencias necesarias del sistema sin afectar otras
configuraciones de Python existentes en el equipo o servidor.
Desde la carpeta raíz del proyecto, ejecutar:
`python -m venv venv`
Luego activar el entorno virtual:
`.\venv\Scripts\activate`
Cuando el entorno virtual se encuentra activo, la terminal debe mostrar el prefijo:
(venv)
Ejemplo:
(venv) PS C:\Ruta\Del\Proyecto>
A partir de ese momento, todos los comandos de instalación y ejecución deben realizarse
con el entorno virtual activo.
Si el entorno virtual ya fue creado previamente, no es necesario volver a crearlo. En ese
caso, solo se debe activar antes de ejecutar el sistema.
## 7. Instalación de dependencias

Con el entorno virtual activo, se deben instalar las dependencias del proyecto desde el archivo
requirements.txt.
Desde la carpeta raíz del proyecto, ejecutar:
`pip install -r requirements.txt`
Este comando instala las librerías necesarias para ejecutar la aplicación, incluyendo los
componentes utilizados por el backend, la interfaz web, la recuperación documental, la base
vectorial, el procesamiento de documentos y los servicios asociados.
Una vez finalizada la instalación, se recomienda verificar que no se hayan producido errores
en la terminal.

Si alguna dependencia no se instala correctamente, el personal técnico deberá revisar:
- conexión a internet disponible durante la instalación;
- versión de Python utilizada;
- entorno virtual activo;
- permisos del sistema;
- mensaje de error informado por pip;
- compatibilidad de paquetes en el equipo o servidor.
La instalación de dependencias debe realizarse antes de ejecutar la aplicación por primera
vez.
## 8. Verificación de Ollama y modelos

locales
El asistente utiliza Ollama para ejecutar localmente los modelos necesarios para la
generación de respuestas y/o procesamiento semántico.
Antes de iniciar la aplicación, el personal técnico debe verificar que Ollama se encuentre
instalado y operativo en el equipo o servidor.
Desde la terminal, ejecutar:
`ollama --version`
Luego verificar los modelos disponibles:
`ollama list`
Para esta versión del sistema, se deben encontrar disponibles los modelos definidos por la
configuración del proyecto. En la versión actual se prevé el uso de:
llama3.2:3b
nomic-embed-text
Si los modelos no se encuentran descargados, pueden instalarse mediante:
`ollama pull llama3.2:3b`
`ollama pull nomic-embed-text`
Una vez descargados, volver a verificar con:
`ollama list`

Si Ollama no responde, el asistente puede presentar errores al generar respuestas o al
recuperar información semántica. En ese caso, se recomienda revisar:
- instalación de Ollama;
- disponibilidad del servicio local;
- modelos descargados;
- conectividad local con el servicio de Ollama;
- recursos disponibles del equipo o servidor;
- mensajes de error mostrados en terminal.
No se recomienda modificar los modelos configurados sin validación técnica previa, ya que
esto puede afectar la calidad, velocidad o estabilidad de las respuestas.
## 9. Configuración inicial del entorno

Antes de ejecutar la aplicación, el personal técnico debe verificar la configuración inicial del
proyecto.
Si el repositorio incluye un archivo de ejemplo de variables de entorno, como:
.env.example
se debe utilizar como referencia para crear o revisar el archivo de configuración local:
.env
El archivo .env permite definir parámetros de ejecución del sistema sin modificar
directamente el código fuente.
Entre las configuraciones que pueden definirse se encuentran:
- modelo de lenguaje local;
- modelo de embeddings;
- ruta de la base vectorial;
- cantidad de documentos recuperados por consulta;
- configuración de red;
- parámetros de ejecución;
- comportamiento del sistema ante recuperación documental o generación de respuestas.
El personal técnico debe revisar que los valores configurados coincidan con el entorno donde
se instalará el asistente.
Ejemplo general:
OLLAMA_MODEL=llama3.2:3b
EMBEDDING_MODEL=nomic-embed-text
CHROMA_DIR=./data/chroma
RETRIEVAL_K=4

No se recomienda modificar estos valores sin validación previa, ya que pueden afectar el
rendimiento, la recuperación documental, la estabilidad del sistema o la calidad de las
respuestas.
Si el sistema ya se entrega con una configuración validada, se recomienda conservarla y
realizar cambios solo cuando exista una necesidad técnica justificada.
## 10. Estado de la base documental y

ChromaDB
El asistente utiliza una base vectorial ChromaDB para recuperar información desde los
documentos técnicos procesados.
Antes de ejecutar el sistema en un entorno operativo, el personal técnico debe verificar si la
entrega incluye la base documental ya procesada y la base ChromaDB preconstruida.
Si la base ChromaDB se entrega ya construida y validada, no se recomienda reconstruirla sin
indicación técnica, ya que una reingesta incorrecta puede alterar la trazabilidad documental,
modificar la cantidad de chunks disponibles o incorporar documentos no validados.
La carpeta esperada para la base vectorial es:

```text
data/chroma
```

La arquitectura actual utiliza dos colecciones sincronizadas:

- `manuales_hrrg`: chunks hijos usados para busqueda semantica, busqueda lexical y reranking.
- `manuales_hrrg_pages`: paginas padre completas usadas para ampliar contexto y mejorar trazabilidad.

Tambien debe verificarse la disponibilidad del corpus documental procesado utilizado por el sistema.

Si por algún motivo fuera necesario reconstruir la base vectorial, debe realizarse únicamente
por personal técnico autorizado y siguiendo el procedimiento definido por el equipo
responsable.
El comando de ingesta debe ejecutarse solo cuando corresponda reconstruir o actualizar la
base documental. En la version actual, la ingesta normal reconstruye el indice con arquitectura
parent-child: chunks hijos para busqueda y paginas padre completas para expansion de contexto.

```powershell
python scripts/ingest_documents.py
```

Antes de ejecutar una reingesta, se recomienda confirmar:
- que el corpus documental activo sea el correcto;
- que no existan documentos duplicados, de prueba o no validados;
- que los documentos estén asociados al equipo correspondiente;
- que la configuración de ChromaDB sea la adecuada;
- que Ollama y los modelos requeridos estén disponibles;
- que exista una copia de respaldo de la base anterior, si corresponde.
Luego de una reingesta, se debe validar desde la interfaz técnica la sección “Manuales
cargados”, verificando cantidad de documentos activos, errores, documentos omitidos y
cantidad de chunks generados.

No se debe solicitar a los usuarios finales que reconstruyan ChromaDB ni que ejecuten
procesos de ingesta documental.
## 11. Puesta en marcha general

El flujo general de puesta en marcha es el siguiente:
1. Descargar o clonar la versión final del repositorio desde GitHub.

2. Verificar que se esté trabajando sobre la rama main.

3. Abrir una terminal en la carpeta raíz del proyecto.

4. Crear o activar el entorno virtual de Python.

5. Instalar las dependencias desde requirements.txt, si aún no fueron instaladas.

6. Verificar que Ollama esté instalado y que los modelos locales requeridos estén disponibles.
7. Revisar la configuración inicial del entorno y, si corresponde, el archivo .env.

8. Confirmar la disponibilidad de la base documental procesada y de la base vectorial ChromaDB.
9. Evitar reconstruir ChromaDB salvo indicación técnica o necesidad justificada.

10. Ejecutar la aplicación Flask.

11. Acceder al sistema desde el navegador local.

12. Validar el acceso desde otro dispositivo conectado a la misma red.

13. Realizar una consulta de prueba desde el perfil Técnico.

14. Realizar una consulta de prueba desde el perfil Operador.

15. Verificar Manuales cargados, QR y funcionamiento general de la interfaz.

## 12. Ejecución de la aplicación

Desde la carpeta raíz del proyecto, con el entorno virtual activo, ejecutar:
`python .\run.py`
Si la aplicación inicia correctamente, la terminal debe mostrar una salida similar a:
Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:5000
Running on http://<IP_LOCAL_DEL_EQUIPO>:5000
La dirección 127.0.0.1 permite acceder únicamente desde la computadora donde se ejecuta
el sistema.
La dirección con IP local permite acceder desde otros dispositivos conectados a la misma
red. La IP puede variar según la red utilizada.
Ejemplo de acceso local por red: http://192.168.1.14:5000
 
Nota técnica
El mensaje de advertencia mostrado por Flask indica que el servidor integrado corresponde a un entorno de desarrollo. Para pruebas locales, validación funcional o uso controlado en red interna puede utilizarse de acuerdo con la configuración definida por el equipo técnico. Si la institución decide implementar el sistema en un entorno productivo permanente, se recomienda evaluar una configuración de despliegue más robusta, con servidor WSGI, control de acceso, políticas de red y medidas de seguridad institucionales.

## 13. Acceso desde red local

Para acceder desde otro dispositivo, como un teléfono celular o una tablet, se debe utilizar la
IP local del equipo donde está corriendo la aplicación.
`http://<IP_LOCAL_DEL_EQUIPO>:5000`
El dispositivo móvil debe estar conectado a la misma red local que la computadora o servidor
donde se ejecuta el asistente.
No debe utilizarse 127.0.0.1 desde el celular, ya que esa dirección apunta al propio
dispositivo móvil y no a la computadora que ejecuta el sistema.

## 14. Validaciones mínimas posteriores al inicio
Una vez iniciado el sistema, se recomienda realizar las siguientes verificaciones mínimas:
| Verificación                         | Resultado esperado                                                                  | Estado                 |
| ------------------------------------ | ----------------------------------------------------------------------------------- | ---------------------- |
| Abrir la pantalla principal          | La pantalla inicial carga correctamente desde el navegador.                         | Pendiente / OK / Error |
| Acceder como Técnico                 | El sistema permite iniciar sesión con perfil técnico autorizado.                    | Pendiente / OK / Error |
| Acceder como Operador                | El sistema permite iniciar sesión con perfil operador autorizado.                   | Pendiente / OK / Error |
| Visualizar selector de equipos       | Se muestra el listado de equipos disponibles.                                       | Pendiente / OK / Error |
| Abrir chat de un equipo              | El sistema abre el chat correspondiente al equipo seleccionado.                     | Pendiente / OK / Error |
| Realizar consulta técnica de prueba  | El asistente responde y, si corresponde, muestra fuentes documentales.              | Pendiente / OK / Error |
| Realizar consulta como operador      | El asistente responde de forma breve y segura, sin instrucciones técnicas internas. | Pendiente / OK / Error |
| Verificar Manuales cargados          | Se visualizan documentos activos, errores, omitidos y cantidad de chunks.           | Pendiente / OK / Error |
| Verificar Centro de Monitoreo        | El panel carga correctamente desde el perfil técnico.                               | Pendiente / OK / Error |
| Probar acceso desde celular o tablet | El dispositivo accede usando la IP local o dirección institucional correcta.        | Pendiente / OK / Error |
| Probar código QR                     | El QR dirige al flujo de acceso y luego al chat del equipo correspondiente.         | Pendiente / OK / Error |

Estas validaciones permiten confirmar que la aplicación, la interfaz, los perfiles, la base
documental y el acceso por red se encuentran operativos.
#### Registro final de puesta en marcha

Una vez completadas las validaciones mínimas, se recomienda dejar registro de la instalación
realizada.
Fecha de puesta en marcha: __________________________
Equipo o servidor utilizado: ___________________________
Dirección local o institucional de acceso: _________________
Repositorio / commit instalado: _________________________
Responsable técnico de la instalación: ___________________
Observaciones: _____________________________________

## 15. Verificación de manuales cargados

Desde el perfil técnico, ingresar a la sección “Manuales cargados”.
Esta pantalla permite verificar:
- cantidad de documentos disponibles;
- cantidad de documentos activos;
- documentos omitidos;
- errores de procesamiento;
- cantidad total de chunks;
- estado de indexación;
- páginas asociadas;
- imágenes detectadas;
- fecha de procesamiento.

Esta validación permite confirmar que la base documental está disponible para el asistente.
En la versión final validada del sistema, la pantalla “Manuales cargados” debe mostrar como
referencia:
- documentos activos: 59;
- documentos omitidos: 0;
- errores de procesamiento: 0;
- estado de los documentos: Indexado.

La cantidad total de chunks puede variar si se reconstruye la base vectorial, si se modifica el
corpus documental o si se ajustan parámetros de ingesta. Por ese motivo, ante una diferencia
en la cantidad de chunks, se recomienda verificar que la base haya sido generada desde el
corpus correcto y que no existan errores u omisiones.

## 16. Códigos QR

Los códigos QR permiten vincular un equipo físico con el chat correspondiente dentro del
asistente. Para su uso operativo, deben estar generados con una dirección válida para la red
donde se utilizarán.
Si los QR fueron generados con 127.0.0.1, solo funcionarán desde la computadora local.
Para celulares o tablets, deben generarse o configurarse con la IP local o dirección
institucional correspondiente.
Al validar un QR, se debe comprobar que el flujo sea:
1. Escanear el QR del equipo.
2. Acceder a la pantalla principal.
3. Iniciar sesión con el perfil autorizado.
4. Abrir automáticamente el chat del equipo asociado al QR.
5. Realizar una consulta de prueba.

Para la instalación final, los códigos QR deberán generarse o validarse con la dirección de
acceso correspondiente al entorno donde se utilizará el sistema.
Si el asistente se ejecuta en una computadora local, los QR deberán apuntar a la IP local
accesible desde los dispositivos de la red habilitada. Si el sistema se instala en un servidor
institucional, los QR deberán apuntar a la dirección definida por el área técnica responsable.
Antes de imprimir o distribuir los QR, se recomienda realizar una prueba desde un teléfono
celular conectado a la red correspondiente, verificando que el flujo complete correctamente:
QR, inicio de sesión y apertura del chat del equipo asociado.

## 17. Problemas frecuentes y acciones

| Problema                                     | Posible causa                                                                                | Acción sugerida                                                           |
| -------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| No carga la pantalla principal               | La aplicación no está ejecutándose o el puerto no está disponible.                           | Verificar terminal, reiniciar aplicación y confirmar puerto 5000.         |
| El celular no accede al sistema              | Se usó 127.0.0.1, IP incorrecta o red distinta.                                              | Usar la IP local del equipo y conectar ambos dispositivos a la misma red. |
| El asistente no responde                     | Ollama no está activo, modelo no disponible o error de backend.                              | Verificar servicio de Ollama y revisar salida de terminal.                |
| No aparecen documentos cargados              | ChromaDB no está disponible o la ingesta no fue ejecutada correctamente.                     | Verificar carpeta de ChromaDB y proceso de ingesta.                       |
| Las respuestas no tienen fuentes             | Puede tratarse del perfil operador o de evidencia no verificable.                            | Probar desde perfil técnico y revisar trazabilidad documental.            |
| El QR no abre el equipo esperado             | QR generado con IP incorrecta o ruta desactualizada.                                         | Regenerar QR con la IP local correcta y validar enlace.                   |
| El sistema responde información insuficiente | No hay evidencia documental suficiente para la consulta.                                     | Revisar documentación cargada o reformular la consulta.                   |
| La terminal no reconoce Python               | Python no está instalado, no está agregado al PATH o se está usando una terminal incorrecta. | Verificar instalación de                                                  |

## 18. Consideraciones de seguridad operativa
El sistema debe ejecutarse dentro del entorno autorizado por la institución.
Se recomienda:
- no exponer la aplicación públicamente sin configuración de seguridad adicional;
- evitar publicar credenciales en documentos de usuario final;
- mantener control sobre el equipo o servidor donde se ejecuta;
- revisar permisos de red;
- proteger el acceso a los documentos técnicos;
- validar el funcionamiento antes de su uso operativo;
- registrar cambios relevantes del sistema.

Las credenciales de acceso al sistema no deben incluirse en esta guía ni en documentos
públicos o compartidos sin control de acceso. Los usuarios, contraseñas iniciales o
mecanismos de administración de cuentas deberán ser entregados por el área responsable
mediante un canal seguro y actualizado cuando corresponda.
## 19. Cierre

Esta guía permite poner en marcha el Asistente IA para Ingeniería Clínica – HRRG en un
entorno controlado, verificar su funcionamiento inicial y asegurar que los componentes
principales se encuentren disponibles.
La administración técnica del sistema debe realizarse por personal autorizado, respetando
las condiciones de seguridad, privacidad y uso responsable definidas para el entorno
institucional.
