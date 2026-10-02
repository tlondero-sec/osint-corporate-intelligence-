# OSINT & Corporate Link Analysis: Auditoría Societaria y Extracción de Datos Gubernamentales

Este proyecto documenta una investigación integral de Inteligencia Corporativa y Debida Diligencia Forense (*Financial Forensics & Asset Tracing*). El objetivo principal del proyecto es la desarticulación de estructuras societarias complejas para identificar a los beneficiarios finales (*Beneficial Ownership*) y el control real detrás de figuras interpuestas, fideicomisos y sociedades (SAS, SRL, SA).

El flujo de trabajo abarca desde el análisis de fuentes abiertas (OSINT/SOCMINT) y el modelado topológico en Maltego, hasta el desarrollo de herramientas personalizadas (Scraping) para la obtención masiva de documentos gubernamentales ocultos en interfaces públicas.

---

## 1. Metodología y Análisis de Enlaces (Link Analysis)

La investigación se originó a partir de auditorías sobre reportes de riesgo crediticio (mi.nosis.com). Al comparar informes actuales con análisis históricos (de hace un año), se detectó la desaparición de información crítica y discrepancias temporales. Por ejemplo, empresas que figuraban como recién inscriptas en ARCA/AFIP poseían un historial documentado mucho más antiguo en boletines oficiales provinciales.

Ante estas inconsistencias (y confirmando que los agregadores comerciales omiten o indexan mal la información), se procedió a un rastreo manual avanzado:

* **Correlación Multi-Fuente:** Cruce de bases estructuradas (registros comerciales, deudas bancarias, BCRA, domicilios fiscales) con información no estructurada de fuentes abiertas (publicaciones judiciales, edictos, prensa local).


* **Google Dorking:** Análisis de domicilios fiscales y alternativos compartidos por múltiples CUITs. Esto permitió descubrir vínculos informales y operativos entre abogados, escribanos, testaferros y empleados mediante artículos periodísticos y SOCMINT (LinkedIn, Instagram, Facebook).


* **Modelado en Maltego:** Todos los datos dispares se transformaron en una red visual interactiva para identificar nodos críticos, patrones de aislamiento patrimonial (como UTEs de obra pública o quiebras estratégicas) y flujos de capital.



### Visualización del Grafo (Mockup / BMP)

> 🖼️ **Insertar imagen aquí:**
> `![Grafo de Relaciones Societarias en Maltego](./assets/maltego_graph_mockup.bmp)`
> *Descripción: Diagramación topológica correlacionando personas físicas, CUITs, SAS/SRL, escribanías y alertas de riesgo patrimonial.*
> 

---

### 2. Desarrollo del Scraper de Boletines Oficiales (Bypass de Interfaz)

El modelado en Maltego dejó en evidencia que la fuente de datos más crítica y fiable era el Boletín Oficial de la Provincia de Entre Ríos. Sin embargo, la interfaz web oficial presenta una limitación severa de diseño: **solo permite visualizar y buscar boletines hasta el año 2020**.

Para sortear este bloqueo de la UI y realizar una recolección exhaustiva, se desarrolló un **Scraper en Python** explotando fallas en la configuración del servidor.

#### Análisis de Tráfico y Descubrimiento (Reconnaissance)

Mediante técnicas de *Web Scraping* y el uso de las herramientas de desarrollador del navegador (Inspeccionar Elemento / Pestaña Red), se analizó el comportamiento del buscador oficial. Se descubrió lo siguiente:

* **Endpoint Interno e IP Expuesta:** El buscador consume datos de un endpoint alojado en `[https://testing54.entrerios.gov.ar/boletin/factura/inicio/get_buscador](https://testing54.entrerios.gov.ar/boletin/factura/inicio/get_buscador)`, resolviendo a la IP pública visible `[https://190.122.147.21:443](https://190.122.147.21:443)`.
* **Respuesta Limitada:** Este endpoint devuelve un array en formato JSON con los números de boletín y fechas, pero el desarrollador limitó los resultados para que el registro más antiguo que devuelva sea de marzo de 2020 (ej. `[{"nro":"26848","fecha":"2020-03-11","nro_anual":"47"}]`).



#### Vulnerabilidades Explotadas

* **Ausencia total de seguridad perimetral:** El servidor **carece de protección Anti-DDoS, limitación de tasa de peticiones (Rate Limiting), bloqueos contra fuerza bruta o validación por CAPTCHA**. Esto permitió enviar miles de *queries* automatizadas consecutivas sin sufrir bloqueos temporales ni baneos de IP.
* **Inseguridad por Oscuridad (Security through Obscurity):** El servidor gubernamental no elimina los archivos PDF anteriores a 2020, simplemente deja de indexarlos en el endpoint de búsqueda JSON.



#### Ejecución y Formato de la Query

Aprovechando la falta de bloqueos por IP, el script ignora el buscador oficial y genera ataques de fuerza bruta iterando sobre un calendario de días hábiles. Envía peticiones HTTP GET directas reconstruyendo la estructura de carpetas del servidor con el siguiente formato exacto:

```text
GET https://www.entrerios.gov.ar/boletin/calendario/Boletin/{YYYY}/{Mes_Texto}/{DD}-{MM}-{YY}.pdf

```

*(Ejemplo de query exitosa: `.../Boletin/2019/Diciembre/23-12-19.pdf`)*

**Resultado:** Esta técnica de fuerza bruta permitió saltar la barrera visual de 2020 y descargar de forma ininterrumpida y automatizada todo el archivo histórico oculto de boletines oficiales **hasta el año 2015**, rescatando miles de documentos inaccesibles de forma convencional para su posterior análisis forense.



---

## 3. Próximos Pasos: Extracción e Indexación OCR/NLP

Con el archivo histórico completo (2015-2026) descargado localmente, la siguiente fase del proyecto consiste en:

1. Extraer el texto de los PDFs de forma masiva.
2. Indexar la información en una base de datos propia.
3. Crear un motor de búsqueda interno para cruzar CUITs y nombres de manera instantánea, superando las limitaciones de plataformas pagas como Nosis.

---

## 4. Fuentes, Herramientas y Habilidades Demostradas

### Fuentes de Datos Relevadas

* **Registrales y Societarias:** Boletines Oficiales (Entre Ríos, Santa Fe, CABA), Inspección General de Justicia (IGJ) / Registros Públicos de Comercio.


* **Financieras y Tributarias:** Central de Deudores del BCRA, ATER, ARCA/AFIP, BCP (Paraguay), y plataformas de riesgo crediticio.


* **Judiciales y Notariales:** Escribanías, edictos, expedientes de fueros penales/comerciales, registros de embargo.



### Habilidades Clave (Hard Skills)

* **Link Analysis & Graph Theory:** Capacidad de conectar entidades heterogéneas (Personas, Direcciones, Empresas, Timelines).


* **Corporate OSINT & SOCMINT:** Investigación avanzada en fuentes abiertas orientada a litigios corporativos.


* **Corporate & Financial Forensics:** Análisis de balances, emisión de cheques rechazados, reestructuración maliciosa de sociedades y reportes analíticos societarios.


* **AML / KYC Investigation:** Detección de *Red Flags* (banderas rojas) como domiciliaciones de pantalla, picos inusuales de crédito y sustitución de administradores.
