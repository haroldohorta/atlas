import os
import json
import pandas as pd

# --- RUTAS ---
DIR_FOTOS = r"F:\fotos"
CSV_ZONAS = r"F:\data\zonas.csv"
JSON_OUT = r"F:\data\puntos_mapa.json"

def limpiar_titulo(n):
    return n.replace(".webp","").replace("_", " ").split('(')[0].split('_copy')[0].strip().capitalize()

def generar_atlas_perfecto():
    # 1. Cargamos lo existente para NO borrar tus relatos
    puntos_existentes = {}
    if os.path.exists(JSON_OUT):
        with open(JSON_OUT, 'r', encoding='utf-8') as f:
            puntos_existentes = {p['id']: p for p in json.load(f)}

    # 2. Cargamos zonas
    df = pd.read_csv(CSV_ZONAS)
    zonas = df.set_index('zona').to_dict('index')

    puntos_nuevos = []
    prefijos = ("pub_", "fly_", "nomad_")

    print("🚀 Reconstruyendo el Atlas para activar espirales...")

    for carpeta in os.listdir(DIR_FOTOS):
        ruta_c = os.path.join(DIR_FOTOS, carpeta)
        if not os.path.isdir(ruta_c) or not carpeta.startswith(prefijos):
            continue
            
        zona_key = carpeta.split('_', 1)[-1]
        
        if zona_key in zonas:
            info = zonas[zona_key]
            for f in os.listdir(ruta_c):
                if f.lower().endswith(".webp"):
                    # SI YA EXISTE: Mantenemos el punto pero reseteamos la coordenada a la exacta
                    if f in puntos_existentes:
                        punto = puntos_existentes[f]
                        punto["lat"] = info['lat'] # Volvemos al origen
                        punto["lon"] = info['lon'] # Volvemos al origen
                        puntos_nuevos.append(punto)
                    else:
                        # SI ES NUEVO: Creamos con coordenada exacta
                        puntos_nuevos.append({
                            "id": f,
                            "lat": info['lat'],
                            "lon": info['lon'],
                            "zona": zona_key,
                            "capa": "Vuelo" if "fly_" in carpeta else "Narrativa",
                            "titulo": limpiar_titulo(f),
                            "thumb": f"fotos/{carpeta}/{f}",
                            "full": f"fotos/{carpeta}/{f}",
                            "descripcion": info['descripcion'],
                            "relato": "Pendiente de relato..."
                        })

    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(puntos_nuevos, f, indent=2, ensure_ascii=False)
    
    print(f"✨ ¡Listo! {len(puntos_nuevos)} puntos listos para el efecto espiral.")

if __name__ == "__main__":
    generar_atlas_perfecto()
