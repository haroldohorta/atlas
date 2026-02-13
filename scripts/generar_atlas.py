import os
import json
import pandas as pd

# --- RUTAS ---
DIRECTORIO_FOTOS = r"F:\fotos"
ARCHIVO_ZONAS = r"F:\data\zonas.csv"
ARCHIVO_SALIDA = r"F:\data\puntos_mapa.json"

def generar_json():
    # 1. Cargar las coordenadas de las zonas
    df_zonas = pd.read_csv(ARCHIVO_ZONAS)
    zonas_dict = df_zonas.set_index('zona').to_dict('index')
    
    puntos_mapa = []

    print("🛰️ Escaneando carpetas de fotos...")

    # 2. Recorrer las subcarpetas en F:\fotos
    for carpeta in os.listdir(DIRECTORIO_FOTOS):
        ruta_carpeta = os.path.join(DIRECTORIO_FOTOS, carpeta)
        
        if os.path.isdir(ruta_carpeta) and carpeta.startswith("pub_") or carpeta.startswith("fly_"):
            # Identificar la zona (quitando el prefijo pub_ o fly_)
            zona_key = carpeta.replace("pub_", "").replace("fly_", "")
            
            if zona_key in zonas_dict:
                info_zona = zonas_dict[zona_key]
                
                # Buscar archivos .webp en la carpeta
                for archivo in os.listdir(ruta_carpeta):
                    if archivo.lower().endswith(".webp"):
                        nombre_base = os.path.splitext(archivo)[0]
                        
                        punto = {
                            "id": nombre_base,
                            "lat": info_zona['lat'],
                            "lon": info_zona['lon'],
                            "zona": zona_key,
                            "capa": "Narrativa" if "pub" in carpeta else "Aéreo",
                            "titulo": nombre_base.replace("_", " ").capitalize(),
                            "thumb": f"fotos/{carpeta}/{archivo}",
                            "full": f"fotos/{carpeta}/{archivo}",
                            "rating": 5,
                            "descripcion": f"Registro en {info_zona['descripcion']}",
                            "relato": "Pendiente de relato..."
                        }
                        puntos_mapa.append(punto)
                        print(f"📍 Agregado: {archivo}")
            else:
                print(f"⚠️ Advertencia: La zona '{zona_key}' no está en zonas.csv")

    # 3. Guardar el archivo JSON final
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(puntos_mapa, f, indent=2, ensure_ascii=False)
    
    print(f"\n✨ ¡ÉXITO! Se generaron {len(puntos_mapa)} puntos en {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    generar_json()