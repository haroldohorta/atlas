import os
import json
import pandas as pd

# --- CONFIGURACIÓN CON RUTAS RELATIVAS (Para F:\ATLAS) ---
DIR_FOTOS = r"fotos"              # Carpeta de fotos al lado del script
CSV_ZONAS = r"data\zonas.csv"     # CSV dentro de la carpeta data
JSON_OUT = r"data\puntos_mapa.json" # El JSON de salida ahora va a la carpeta data

def limpiar_nombre_archivo(ruta_carpeta, nombre_original):
    """Limpia nombres con espacios, tildes o símbolos para evitar errores web."""
    # Quitamos espacios y símbolos raros, todo a minúsculas
    nuevo_nombre = nombre_original.replace(" ", "_").replace("+", "_").replace("__", "_").lower()
    if nuevo_nombre != nombre_original:
        try:
            # Intentamos el renombramiento físico en el disco
            os.rename(os.path.join(ruta_carpeta, nombre_original), os.path.join(ruta_carpeta, nuevo_nombre))
            return nuevo_nombre
        except Exception as e:
            print(f"⚠️ No se pudo renombrar {nombre_original}: {e}")
            return nombre_original
    return nombre_original

def limpiar_titulo(n):
    # Convierte 'miliciano_herido.webp' -> 'Miliciano herido'
    base = n.replace(".webp","").replace(".jpg","").replace(".jpeg","").replace("_", " ").split('(')[0].strip()
    return base.capitalize()

def generar_atlas():
    # 1. Intentar cargar relatos existentes (para no perder lo que ya escribiste)
    puntos_existentes = {}
    if os.path.exists(JSON_OUT):
        try:
            with open(JSON_OUT, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                # Creamos un mapa por ID para buscar rápido
                puntos_existentes = {p['id']: p for p in datos}
        except:
            print("⚠️ Creando nuevo JSON de datos.")

    # 2. Cargar coordenadas del CSV
    try:
        df_zonas = pd.read_csv(CSV_ZONAS)
        # Convertimos el CSV en un diccionario para buscar por 'zona'
        zonas_dict = df_zonas.set_index('zona').to_dict('index')
    except Exception as e:
        print(f"❌ Error crítico: No se encontró el CSV en {os.path.abspath(CSV_ZONAS)}\n{e}")
        return

    puntos_finales = []
    conteo_zonas = {}

    # 3. Escaneo de carpetas físicas
    print(f"🛰️  Iniciando escaneo en: {os.path.abspath(DIR_FOTOS)}")
    
    if not os.path.exists(DIR_FOTOS):
        print(f"❌ Error: La carpeta '{DIR_FOTOS}' no existe en esta ubicación.")
        return

    for carpeta in os.listdir(DIR_FOTOS):
        ruta_completa = os.path.join(DIR_FOTOS, carpeta)
        if not os.path.isdir(ruta_completa): continue

        # Lógica de prefijos: pub_medellin -> prefijo: pub, zona: medellin
        if "_" in carpeta:
            partes = carpeta.split("_", 1)
            prefijo = partes[0]
            zona_key = partes[1]
        else:
            # Si no tiene guion bajo, usamos el nombre tal cual
            prefijo = ""
            zona_key = carpeta

        if zona_key in zonas_dict:
            info_gps = zonas_dict[zona_key]
            
            # Asignación de Capas (puedes añadir más aquí)
            capa_nombre = "Archivo Histórico"
            if prefijo == "nomad": capa_nombre = "Bitácora Nómada"
            elif prefijo == "fly": capa_nombre = "Vuelo Aéreo"
            elif prefijo == "pub": capa_nombre = "Publicaciones"
            elif prefijo == "narrativa": capa_nombre = "Narrativa Sonora"

            for archivo in os.listdir(ruta_completa):
                if archivo.lower().endswith((".webp", ".jpg", ".jpeg")):
                    # Limpiamos el nombre del archivo para la web
                    archivo_limpio = limpiar_nombre_archivo(ruta_completa, archivo)
                    
                    # ID único para cada foto
                    foto_id = f"{zona_key}_{archivo_limpio.replace('.', '_')}"
                    
                    # Si la foto ya existía, conservamos su relato y descripción
                    if foto_id in puntos_existentes:
                        punto = puntos_existentes[foto_id].copy()
                        punto["lat"] = info_gps['lat']
                        punto["lon"] = info_gps['lon']
                        punto["capa"] = capa_nombre
                        punto["thumb"] = f"fotos/{carpeta}/{archivo_limpio}"
                        punto["full"] = f"fotos/{carpeta}/{archivo_limpio}"
                        puntos_finales.append(punto)
                    else:
                        # Si es nueva, creamos el registro desde cero
                        puntos_finales.append({
                            "id": foto_id,
                            "lat": info_gps['lat'],
                            "lon": info_gps['lon'],
                            "zona": zona_key,
                            "capa": capa_nombre,
                            "titulo": limpiar_titulo(archivo_limpio),
                            "thumb": f"fotos/{carpeta}/{archivo_limpio}",
                            "full": f"fotos/{carpeta}/{archivo_limpio}",
                            "rating": 5,
                            "descripcion": info_gps.get('descripcion', f"Registro fotográfico en {zona_key.capitalize()}."),
                            "relato": "Pendiente de relato..."
                        })
                    conteo_zonas[zona_key] = conteo_zonas.get(zona_key, 0) + 1

    # 4. Guardar el resultado
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(puntos_finales, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*40)
    for z, c in sorted(conteo_zonas.items()):
        print(f"✅ Zona '{z}': {c} fotos sincronizadas.")
    print("="*40)
    print(f"🚀 ¡Misión cumplida! {len(puntos_finales)} puntos totales en el Atlas.")

if __name__ == "__main__":
    generar_atlas()