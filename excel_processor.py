import pandas as pd
import re
from datetime import datetime, time

def procesar_excel(file_path):
    # Leer el archivo crudo manteniendo estructura original
    df_raw = pd.read_excel(file_path, header=None)
    
    # Variables para almacenar datos procesados
    data = []
    current_date = None
    headers = ["Estudiantes", "Tutor", "Presidente", "Miembro", "Miembro2", "Oponente", "Fecha", "Hora", "Lugar"]
    
    for index, row in df_raw.iterrows():
        # Detectar filas con fechas (ej: "26 de febrero 2025")
        if re.match(r"\d{1,2} de \w+ \d{4}", str(row[1])):
            try:
                current_date = datetime.strptime(row[1], "%d de %B %Y").date()
            except:
                # Plan B: Mapeo manual de meses en español
                meses = {
                    'enero': '01', 'febrero': '02', 'marzo': '03',
                    'abril': '04', 'mayo': '05', 'junio': '06',
                    'julio': '07', 'agosto': '08', 'septiembre': '09',
                    'octubre': '10', 'noviembre': '11', 'diciembre': '12'
                }
                
                fecha_partes = row[1].split()
                mes = fecha_partes[2].lower()
                fecha_formateada = f"{fecha_partes[0]} {meses[mes]} {fecha_partes[3]}"
                current_date = datetime.strptime(fecha_formateada, "%d %m %Y").date()
            
            continue
        
        # Detectar filas de encabezado
        if list(row[1:10].dropna()) == headers:
            continue
        
        # Capturar filas de datos válidas
        if current_date and len(row[1:9].dropna()) >= 7:
            datos = {
                "fecha": current_date if pd.notnull(current_date) else None,
                "estudiante": row[1],
                "tutores": limpiar_nombres(row[2]),
                "presidente": limpiar_nombres(row[3]),
                "miembro_1": limpiar_nombres(row[4]),
                "miembro_2": limpiar_nombres(row[5]),
                "oponente": limpiar_nombres(row[6]),
                "hora": normalizar_hora(row[8]),  # ← Corregido: Columna H (índice 7)
                "lugar": normalizar_lugar(row[9])  # ← Corregido: Columna I (índice 8)
            }
            try:
                datos['hora'] = pd.to_datetime(datos['hora'], errors='coerce').time()
            except:
                datos['hora'] = None
            data.append(datos)
    
    df = pd.DataFrame(data)
    return df

def limpiar_nombres(texto):
    # Eliminar menciones de Twitter y múltiples espacios
    if pd.isna(texto):
        return None
    return re.sub(r"@\w+", "", texto).strip()

def normalizar_hora(hora):
    # Caso especial "1 pkm"
    if isinstance(hora, str) and "pkm" in hora.lower():
        return "13:00"
    
    # Manejar objetos time existentes
    if isinstance(hora, time):  # <-- Usar 'time' directamente
        return hora.strftime("%H:%M")
    
    try:
        # Convertir cualquier formato a string HH:MM
        hora_parsed = pd.to_datetime(hora, errors='coerce')
        return hora_parsed.strftime("%H:%M") if not pd.isna(hora_parsed) else None
    except:
        return None


def normalizar_lugar(lugar):
    # Estandarizar nombres de lugares
    lugar = str(lugar).split("(")[0].strip()
    return lugar.replace("Francofonia", "Francofonía").replace("Resp ", "")