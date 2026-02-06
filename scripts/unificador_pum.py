import sqlite3
import json
import pandas as pd
import os

# Configuración de rutas
DB_PATH = 'data/haroldo_indice.db'
ZONA_CSV = 'data/zona.csv'
OUTPUT_GEOJSON = 'data/mapa_maestro.geojson'

def generar_mapa():
    # 1. Cargar el diccionario de zonas para el "chantaje" de GPS
    if not os.path.exists(ZONA_CSV):
        print(f"❌ Error: No se encuentra {ZONA_CSV}")
        return
    
    zonas = pd.read_csv(ZONA_CSV).set_index('zona').to_dict('index')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 2. Query con filtros de seguridad y origen
    # Excluimos carpetas de recuperación y priorizamos el Drive
    query = """
    SELECT Nombre, RutaFull, Año, Descripcion 
    FROM inventario 
    WHERE RutaFull NOT LIKE '%recup_dir%' 
    AND RutaFull LIKE '%Haroldo_Live%'
    """
    cursor.execute(query)
    
    features = []
    print("🛰️ Procesando trayectoria de Haroldo...")

    for row in cursor.fetchall():
        nombre, ruta, anio, desc = row
        lat, lon = None, None
        
        # Lógica de match por carpeta
        ruta_min = ruta.lower().replace('\\', '/')
        for ciudad_clave, gps in zonas.items():
            if ciudad_clave.lower() in ruta_min:
                lat, lon = gps['gps_lat'], gps['gps_lon']
                break
        
        if lat and lon:
            # Clasificación de Etapa para el color del pin
            etapa = "Nómade"
            if any(x in ruta_min for x in ['nicaragua', 'lota', 'embajada', 'peru', 'colombia']):
                etapa = "Corresponsal"
            elif any(x in ruta_min for x in ['chiloe', 'faros', 'kactus']):
                etapa = "Patrimonio"

            feature = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]},
                "properties": {
                    "titulo": nombre,
                    "etapa": etapa,
                    "anio": anio,
                    "relato": desc or "Sin descripción",
                    "ruta": ruta.replace('\\', '/')
                }
            }
            features.append(feature)

    # 3. Guardar el GeoJSON
    os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)
    with open(OUTPUT_GEOJSON, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False)
    
    conn.close()
    print(f"✨ ¡PUM! Mapa generado con {len(features)} puntos.")

if __name__ == "__main__":
    generar_mapa()
