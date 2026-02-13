import os
import json
import pandas as pd
import random

# --- CONFIGURACIÓN DE RUTAS ---
DIRECTORIO_FOTOS = r"F:\fotos"
ARCHIVO_ZONAS = r"F:\data\zonas.csv"
ARCHIVO_SALIDA = r"F:\data\puntos_mapa.json"

def limpiar_titulo(nombre_archivo):
    """Convierte 'miliciano_herido.webp' en 'Miliciano herido'"""
    # Quitar extensión y limpiar basura de nombres
    base = os.path.splitext(nombre_archivo)[0]
    # Quitar (1), _copy, etc.
    base = base.split('(')[0].split('_copy')[0].replace("_", " ").strip()
    return base.capitalize()

def generar_atlas_inteligente():
    # 1. Intentar cargar el JSON actual para no sobreescribir relatos manuales
    puntos_existentes = {}
    if os.path.exists(ARCHIVO_SALIDA):
        try:
            with open(ARCHIVO_SALIDA, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Mapeamos por ID para encontrarlos rápido
                puntos_existentes = {p['id']: p for p in datos}
            print(f"📖 Se cargaron {len(puntos_existentes)} puntos previos del JSON.")
        except Exception as e:
            print(f"⚠️ No se pudo leer el JSON previo ({e}). Se creará uno nuevo.")

    # 2. Cargar las zonas del CSV
    try:
        df_zonas = pd.read_csv(ARCHIVO_ZONAS)
        zonas_dict = df_zonas.set_index('zona').to_dict('index')
    except Exception as e:
        print(f"❌ Error crítico cargando zonas.csv: {e}")
        return

    lista_final = []
    print("🛰️ Iniciando escaneo inteligente de carpetas...")

    # 3. Recorrer carpetas de fotos
    for carpeta in os.listdir(DIRECTORIO_FOTOS):
        ruta_carpeta = os.path.join(DIRECTORIO_FOTOS, carpeta)
        
        if os.path.isdir(ruta_carpeta) and (carpeta.startswith("pub_") or carpeta.startswith("fly_")):
            zona_key = carpeta.replace("pub_", "").replace("fly_", "")
            
            if zona_key in zonas_dict:
                info_zona = zonas_dict[zona_key]
                
                for archivo in os.listdir(ruta_carpeta):
                    if archivo.lower().endswith(".webp"):
                        # Usamos el nombre del archivo como ID único
                        foto_id = archivo 
                        
                        # SI YA EXISTE EN EL JSON: Lo dejamos como está (preserva tu trabajo)
                        if foto_id in puntos_existentes:
                            lista_final.append(puntos_existentes[foto_id])
                            continue
                        
                        # SI ES NUEVA: Creamos el punto con Jitter (dispersión)
                        # El jitter mueve el punto hasta unos 400-500 metros a la redonda
                        lat_final = info_zona['lat'] + random.uniform(-0.005, 0.005)
                        lon_final = info_zona['lon'] + random.uniform(-0.005, 0.005)

                        nuevo_punto = {
                            "id": foto_id,
                            "lat": round(lat_final, 6),
                            "lon": round(lon_final, 6),
                            "zona": zona_key,
                            "capa": "Crónica & Etnografía" if "pub_" in carpeta else "Vuelo Aéreo",
                            "titulo": limpiar_titulo(archivo),
                            "thumb": f"fotos/{carpeta}/{archivo}",
                            "full": f"fotos/{carpeta}/{archivo}",
                            "rating": 5,
                            "descripcion": info_zona['descripcion'],
                            "relato": "Pendiente de relato de Haroldo..."
                        }
                        lista_final.append(nuevo_punto)
                        print(f"🆕 Nuevo punto detectado: {archivo}")
            else:
                print(f"⚠️ Advertencia: La carpeta '{carpeta}' no tiene zona en el CSV.")

    # 4. Guardar todo el conjunto
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(lista_final, f, indent=2, ensure_ascii=False)
    
    print(f"\n✨ ¡Misión cumplida! El Atlas ahora tiene {len(lista_final)} puntos.")
    print(f"📂 Archivo actualizado: {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    generar_atlas_inteligente()