# 🔍 Pipeline de Inteligencia OSINT & Auditoría Registral (Boletines Oficiales)

Framework automatizado y soberano para la recolección masiva, normalización y análisis de texto completo sobre más de 1.200 ediciones históricas del Boletín Oficial de la Provincia de Entre Ríos (2021-Presente).

## 🚀 Arquitectura del Proceso
[ Web Oficial Entre Ríos ] ──( curl + Patrón de Fechas )──> [ PDFs Locales ]
│
▼
[ Matriz de Hallazgos (CSV) ] <──( Regex / AWK / pdftotext ) <──────┘



## 🔎 Hallazgo de Auditoría: Acceso a Activos Ocultos (Security Through Obscurity)

Durante la fase de reconocimiento e ingeniería del pipeline de descarga, se identificó una discrepancia crítica en la exposición de datos del servidor oficial (`entrerios.gov.ar`):

1. **Restricción Visual de la Interfaz:** El calendario web de la administración pública limita la visualización y navegación de boletines públicos únicamente hasta el año 2021.
2. **Exposición Real de Archivos (Falta de Control de Acceso):** Al implementar una iteración determinista por rangos de fechas (permutación de URLs en el script Bash), se constató que el servidor web almacena y entrega de forma pública edictos y boletines históricos de años anteriores (ej. 2019 en adelante) que no poseen referencias indexadas en el frontend.
3. **Implicancia Forense:** Esto permitió rescatar documentación oficial no listada oficialmente, ampliando de forma masiva el espectro temporal de la auditoría corporativa y societaria sin requerir técnicas de explotación complejas, meramente explotando la previsibilidad de las rutas estáticas de los archivos PDF.






## 🛠️ Stack Tecnológico
* **Lenguaje / Shell:** Bash Scripting, AWK, Sed.
* **Procesamiento de Documentos:** Poppler-utils (`pdftotext` con layout preservado).
* **Control de Red:** `curl` con reintentos automáticos y validación de cabeceras PDF.

---

## 🧗 Desafíos Técnicos y Dificultades Superadas

### 1. El Reto del Volumen Masivo
* **Contexto:** Procesar más de 1.200 boletines (promedio de 80-90 páginas por edición) de forma manual o mediante herramientas web era inviable por limitaciones de tiempo y cortes de procesamiento.
* **Solución:** Desarrollo de un script iterativo por días hábiles que calcula dinámicamente las rutas de los archivos, valida la existencia del recurso en el servidor gubernamental y almacena localmente de manera incremental (evitando re descargas si el proceso se interrumpe).

### 2. Normalización y Extracción de Texto (OCR / Layout)
* **Dificultad:** Los boletines oficiales presentan variaciones tipográficas, saltos de página y tablas complejas de edictos societarios.
* **Solución:** Uso de `pdftotext -layout` para mantener la fidelidad espacial de las columnas, combinado con normalización de acentos y mayúsculas/minúsculas mediante `sed` y filtrado algorítmico con `awk`.

### 3. Reducción de Ruido y Falsos Positivos
* **Problema:** Términos geográficos o nombres comunes (ej. nombres de calles, apellidos extendidos) generan un alto volumen de coincidencias irrelevantes (*ruido*).
* **Mitigación:** Implementación de expresiones regulares modulares (`TERMINOS="termino1|termino2"`) y generación automática de un archivo CSV estructurado (`fecha, pagina, linea, texto`) para realizar filtros posteriores por línea de interés.

---

## 🕸️ Mapeo Topológico y Análisis Relacional (Maltego)

Para estructurar la complejidad hallada a través de las fuentes abiertas:
* **Integración:** Los hallazgos extraídos de los boletines oficiales se correlacionaron con variaciones en reportes de buroes de crédito (Nosis) y registros públicos.
* **Visualización:** Se diseñó un grafo relacional en Maltego anonimizando todas las entidades personales y comerciales (`[Persona_A]`, `[Sociedad_X]`), priorizando la exposición estricta de las **aristas de vinculación** (nombramientos, domicilios fiscales compartidos, fechas de desprendimiento accionario y modificaciones estatutarias)
