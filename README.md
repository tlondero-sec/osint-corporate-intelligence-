# OSINT & Corporate Link Analysis: Auditoría Societaria y Extracción de Datos Gubernamentales

Este proyecto documenta una investigación integral de Inteligencia Corporativa y Debida Diligencia Forense (*Financial Forensics & Asset Tracing*). El objetivo principal del proyecto es la desarticulación de estructuras societarias complejas para identificar a los beneficiarios finales (*Beneficial Ownership*) y el control real detrás de figuras interpuestas, fideicomisos y sociedades (SAS, SRL, SA).

El flujo de trabajo abarca desde el análisis de fuentes abiertas (OSINT/SOCMINT) y el modelado topológico en Maltego, hasta el desarrollo de herramientas personalizadas de extracción automatizada para la recuperación de archivos históricos en portales públicos.

---

## 1. Metodología y Análisis de Enlaces (Link Analysis)

La investigación se originó a partir de auditorías sobre reportes de riesgo crediticio. Al comparar informes actuales con análisis históricos, se detectaron discrepancias temporales y vacíos de información crítica. Ante estas limitaciones en los agregadores comerciales, se procedió a un rastreo manual avanzado:

- **Correlación Multi-Fuente:** Cruce de registros comerciales, bases tributarias y deudas financieras con información no estructurada de fuentes abiertas (edictos, gacetillas y registros públicos).
- **Google Dorking & SOCMINT:** Análisis de domicilios fiscales compartidos y correlación de metadatos de redes profesionales para identificar vínculos operativos entre administradores y sociedades.
- **Modelado en Maltego:** Transformación de datos dispersos en una red interactiva para aislar nodos críticos, esquemas de aislamiento patrimonial y patrones societarios complejos.

> 🖼️ **Ejemplo de correlación topológica:**
> ![Grafo de Relaciones Societarias](./graph%20para%20github.bmp)
> *Nota: Datos ofuscados por motivos de OPSEC y confidencialidad. La muestra representa una fracción de la red total relevada.*

---

## 2. Automatización de Extracción de Datos (Scraper de Fuentes Públicas)

Para superar las restricciones de indexación temporal en interfaces web tradicionales, se desarrolló un **Scraper modular en Python** enfocado en el consumo estructurado de metadatos desde los flujos de datos subyacentes del servidor.

### Arquitectura y Funcionamiento del Script
- **Consumo de Endpoints / JSON:** Automatización de peticiones orientadas a la capa de datos del servidor para evitar la navegación visual repetitiva.
- **Rastreo Cronológico Inverso (*Backward Crawling*):** Implementación de un bucle de fecha descendente que valida la existencia de documentos estructurados por días hábiles.
- **Manejo de Errores y Excepciones:** Control de flujos HTTP (respuestas 200/404) y omisión automática de fines de semana para optimizar el rendimiento de descarga local.

---

## 3. Roadmap: Pipeline de Procesamiento e Inteligencia (Próximas Fases)

- **Fase 1: Normalización Textual:** Conversión masiva de documentos descargados a texto plano (*plaintext*) y limpieza de ruido tipográfico.
- **Fase 2: Base de Datos Local (SQLite/DuckDB):** Indexación de entidades clave (CUITs, razones sociales, tipos de actos jurídicos) para consultas de baja latencia.
- **Fase 3: Motor CLI & Alertas:** Desarrollo de una interfaz de comandos para realizar búsquedas rápidas y seguimiento automatizado de entidades corporativas.

---

## 🛠️ Habilidades Técnicas Demostradas
- **Link Analysis & Graph Theory:** Modelado topológico de entidades complejas.
- **Corporate OSINT & AML/KYS:** Investigación defensiva y detección de *Red Flags* societarias.
- **Automation & Scripting:** Desarrollo en Python (Requests, manejo de fechas, gestión de I/O de archivos).
