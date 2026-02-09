import sqlite3
import json
import pandas as pd
import os

# CONFIGURACIÓN SUR DAO
DB_PATH = r'F:\haroldo_archivo.db'
ZONA_CSV = r'F:\Scripts\zonas.csv' # Asegúrate que el nombre coincida (zona o zonas)
OUTPUT_JSON = r'F:\puntos_mapa.json'

def unificador_pum_final():
    print("🚀 Iniciando UNIFICADOR PUM v26.0...")
    
    # 1. Cargar el GPS y las descripciones del CSV
    if not os.path.exists(ZONA_CSV):
        print(f"❌ Error: No se encuentra {ZONA_CSV}")
        return
    
    # Cargamos el CSV como diccionario para búsqueda rápida
    df_zonas = pd.read_csv(ZONA_CSV)
    zonas_dict = df_zonas.set_index('zona').to_dict('index')
    
    # 2. Conectar al Búnker SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Traemos todas las fotos procesadas
    cursor.execute("SELECT filename, ruta_relativa, lat, lon, capa, titulo FROM fotos")
    rows = cursor.fetchall()
    
    puntos_finales = []
    
    for r in rows:
        filename, ruta, lat, lon, capa, titulo = r
        
        # Buscamos si hay una descripción especial en el CSV para esta zona
        descripcion_extra = "Archivo Histórico Haroldo Horta"
        for zona_clave, data in zonas_dict.items():
            if zona_clave.lower() in ruta.lower():
                # Si el CSV tiene columna 'descripcion', la usamos
                descripcion_extra = data.get('descripcion', descripcion_extra)
                break
        
        # Formateamos para el mapa y la galería
        thumb_path = f"./fotos/{ruta}/{os.path.splitext(filename)[0]}.webp"
        
        puntos_finales.append({
            "id": filename,
            "capa": capa,
            "lat": lat,
            "lon": lon,
            "thumb": thumb_path.replace("//", "/"),
            "titulo": f"{titulo}",
            "relato": descripcion_extra # Esto aparecerá en el popup
        })

    # 3. Guardar el JSON Maestro
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(puntos_finales, f, indent=4, ensure_ascii=False)
    
    conn.close()
    print(f"✨ ¡PUM! Sistema sincronizado con {len(puntos_finales)} puntos.")
    print(f"📂 Archivo generado en: {OUTPUT_JSON}")

if __name__ == "__main__":
    unificador_pum_final()
