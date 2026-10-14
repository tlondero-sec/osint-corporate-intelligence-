import os
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE RASTREO HISTÓRICO ---
ANIO_INICIO = 2026
ANIO_FIN = 2020

START_DATE = datetime(ANIO_INICIO, 10, 14)
STOP_DATE = datetime(ANIO_FIN, 1, 1)

OUTPUT_DIR = "documentos_historicos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

meses_espanol = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

print(f"=== Iniciando recolección histórica ({ANIO_INICIO} a {ANIO_FIN}) ===")
print(f"Directorio de destino: ./{OUTPUT_DIR}/\n")

current_date = START_DATE
descargados = 0
omitidos = 0
consecutivos_404 = 0

# Plantilla genérica para estructurar las peticiones al repositorio objetivo
BASE_URL_TEMPLATE = "https://www.ejemplo-gobierno.gov.ar/repositorio/calendario/Documento/{anio}/{mes_nombre}/{fecha_str}.pdf"

while current_date >= STOP_DATE:
    # Omitir fines de semana (Sábados=5, Domingos=6)
    if current_date.weekday() < 5:
        anio = current_date.strftime("%Y")
        mes_nombre = meses_espanol[current_date.month]
        fecha_str = current_date.strftime("%d-%m-%y")

        url = BASE_URL_TEMPLATE.format(anio=anio, mes_nombre=mes_nombre, fecha_str=fecha_str)
        pdf_path = os.path.join(OUTPUT_DIR, f"{current_date.strftime('%Y-%m-%d')}.pdf")

        if os.path.exists(pdf_path):
            omitidos += 1
            consecutivos_404 = 0
        else:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ResearchBot/1.0'}
                response = requests.get(url, headers=headers, timeout=8)
                
                if response.status_code == 200 and len(response.content) > 1000:
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[OK] Descargado: {current_date.strftime('%Y-%m-%d')}")
                    descargados += 1
                    consecutivos_404 = 0
                else:
                    consecutivos_404 += 1
            except Exception as e:
                consecutivos_404 += 1

    current_date -= timedelta(days=1)

print(f"\n=== Proceso Finalizado ===")
print(f"Archivos nuevos descargados: {descargados}")
print(f"Archivos omitidos (existentes): {omitidos}")
