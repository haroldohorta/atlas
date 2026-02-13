import os
import json
import pandas as pd
import random

# --- CONFIGURACIÓN ---
DIRECTORIO_FOTOS = r"F:\fotos"
ARCHIVO_ZONAS = r"F:\data\zonas.csv"
ARCHIVO_SALIDA = r"F:\data\puntos_mapa.json"

def limpiar_titulo(nombre_archivo):
    base = os.path.splitext(nombre_archivo)[0]
    # Limpieza: quita (1), _copy, _, y capitaliza
    base = base.split('(')[0].split('_copy')[0].replace("_", " ").strip()
    return base.capitalize()

def generar_atlas_final_final():
    puntos_existentes = {}
    if os.path.exists(ARCHIVO_SALIDA):
        try:
            with open(ARCHIVO_SALIDA, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                puntos_existentes = {p['id']: p for p in datos}
            print(f"📖 Base de datos cargada: {len(puntos_existentes)} puntos previos.")
        except Exception:
            print("⚠️ Iniciando base de datos limpia.")

    try:
        df_zonas = pd.read_csv(ARCHIVO_ZONAS)
        zonas_dict = df_zonas.set_index('zona').to_dict('index')
    except Exception as e:
        print(f"❌ Error en zonas.csv: {e}")
        return

    lista_final = []
    print("🛰️ Escaneando carpetas: Publicaciones, Vuelos, Nómades y Panos...")

    for carpeta in os.listdir(DIRECTORIO_FOTOS):
        ruta_carpeta = os.path.join(DIRECTORIO_FOTOS, carpeta)
        if not os.path.isdir(ruta_carpeta): continue
        
        # Identificación inteligente de Zona y Capa
        zona_key = None
        capa_nombre = "Crónica & Etnografía" # Default

        if carpeta.startswith("pub_"):
            zona_key = carpeta.replace("pub_", "")
        elif carpeta.startswith("fly_"):
            zona_key = carpeta.replace("fly_", "")
            capa_nombre = "Vuelo Aéreo"
        elif carpeta.startswith("nomad_"):
            zona_key = carpeta.replace("nomad_", "")
            capa_nombre = "Expedición Nómade"
        elif carpeta == "panos":
            zona_key = "latinoamerica" # Anclamos las panos al centro del mapa
            capa_nombre = "Panorámicas"

        # Si encontramos una zona válida, procesamos las fotos
        if zona_key and zona_key in zonas_dict:
            info_zona = zonas_dict[zona_key]
            
            for archivo in os.listdir(ruta_carpeta):
                if archivo.lower().endswith(".webp"):
                    foto_id = archivo 
                    
                    # Si ya existe, respetamos el trabajo manual previo
                    if foto_id in puntos_existentes:
                        lista_final.append(puntos_existentes[foto_id])
                        continue
                    
                    # Dispersión (Jitter) para que no se amontonen
                    lat_final = info_zona['lat'] + random.uniform(-0.007, 0.007)
                    lon_final = info_zona['lon'] + random.uniform(-0.007, 0.007)

                    nuevo_punto = {
                        "id": foto_id,
                        "lat": round(lat_final, 6),
                        "lon": round(lon_final, 6),
                        "zona": zona_key,
                        "capa": capa_nombre,
                        "titulo": limpiar_titulo(archivo),
                        "thumb": f"fotos/{carpeta}/{archivo}",
                        "full": f"fotos/{carpeta}/{archivo}",
                        "rating": 5,
                        "descripcion": info_zona['descripcion'],
                        "relato": "Pendiente de relato de Haroldo..."
                    }
                    lista_final.append(nuevo_punto)
                    print(f"📍 Rescatado: {archivo} ({zona_key})")
        elif zona_key:
            print(f"⚠️ Alerta: La zona '{zona_key}' no está en tu zonas.csv")

    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(lista_final, f, indent=2, ensure_ascii=False)
    
    print(f"\n🚀 ¡TRABAJO TERMINADO! El Atlas tiene {len(lista_final)} puntos operativos.")

if __name__ == "__main__":
    generar_atlas_final_final()