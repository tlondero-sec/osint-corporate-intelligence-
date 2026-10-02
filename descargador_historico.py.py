import os
import requests
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE RASTREO HISTÓRICO ---
# Arrancamos desde el día de hoy hacia atrás, o configuramos un año específico (ej. 1 de Enero de 2025)
ANIO_INICIO = 2023
ANIO_FIN = 2021

START_DATE = datetime(ANIO_INICIO, 12, 31)
STOP_DATE = datetime(ANIO_FIN, 1, 1)

OUTPUT_DIR = "boletines_oficiales_historicos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

meses_espanol = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

print(f"=== Iniciando descarga histórica hacia atrás ({ANIO_INICIO} a {ANIO_FIN}) ===")
print(f"Carpeta de destino: ./{OUTPUT_DIR}/\n")

current_date = START_DATE
descargados = 0
omitidos = 0
consecutivos_404 = 0

while current_date >= STOP_DATE:
    # Omitir fines de semana (Sábados=5, Domingos=6)
    if current_date.weekday() < 5:
        anio = current_date.strftime("%Y")
        mes_nombre = meses_espanol[current_date.month]
        fecha_str = current_date.strftime("%d-%m-%y")

        url = f"https://www.entrerios.gov.ar/boletin/calendario/Boletin/{anio}/{mes_nombre}/{fecha_str}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, f"{current_date.strftime('%Y-%m-%d')}.pdf")

        if os.path.exists(pdf_path):
            omitidos += 1
            consecutivos_404 = 0 # Reseteamos contador si ya lo tenemos guardado
        else:
            try:
                response = requests.get(url, timeout=8)
                if response.status_code == 200 and len(response.content) > 1000:
                    with open(pdf_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[OK] Descargado: {current_date.strftime('%Y-%m-%d')} -> {url}")
                    descargados += 1
                    consecutivos_404 = 0 # Encontró uno válido, reseteamos racha de 404
                else:
                    # Sumamos contador de fallos (404 o contenido vacío)
                    consecutivos_404 += 1
            except Exception as e:
                consecutivos_404 += 1

    current_date -= timedelta(days=1)

print(f"\n=== Proceso Histórico Finalizado ===")
print(f"PDFs nuevos descargados: {descargados}")
print(f"PDFs ya existentes (omitidos): {omitidos}")
