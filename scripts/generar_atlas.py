import pandas as pd
import json
import os

# --- CONFIGURACIÓN ---
CSV_METADATOS = "metadata_haroldo.csv"  # El archivo que te pasa Haroldo
CSV_ZONAS = "zonas.csv"                # Tu base de datos de coordenadas
JSON_SALIDA = "data/puntos_mapa.json"
CARPETA_FOTOS = "fotos/"               # Donde están las subcarpetas (managua, leon, etc)

def generar_json():
    print("🚀 Iniciando construcción automática del Atlas...")
    
    # 1. Cargar base de datos de coordenadas
    df_zonas = pd.read_csv(CSV_ZONAS).set_index('zona')
    
    # 2. Cargar metadatos de Haroldo
    try:
        df_fotos = pd.read_csv(CSV_METADATOS)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {CSV_METADATOS}")
        return

    lista_puntos = []

    for _, row in df_fotos.iterrows():
        zona_id = str(row['zona']).lower().strip()
        
        # Buscar coordenadas en la base de datos de zonas
        if zona_id in df_zonas.index:
            lat = df_zonas.loc[zona_id, 'lat']
            lon = df_zonas.loc[zona_id, 'lon']
        else:
            print(f"⚠️ Advertencia: Zona '{zona_id}' no encontrada en zonas.csv. Saltando...")
            continue

        # Construir la ruta del archivo (asumiendo que están en carpetas por zona)
        # Ejemplo: fotos/managua/NIC_001.webp
        nombre_archivo = f"{row['id']}.webp"
        ruta_foto = f"fotos/{zona_id}/{nombre_archivo}"

        # Crear el objeto para el JSON
        punto = {
            "id": row['id'],
            "lat": float(lat),
            "lon": float(lon),
            "zona": zona_id,
            "capa": row['capa'],
            "titulo": row['titulo'],
            "thumb": ruta_foto,
            "full": ruta_foto,
            "rating": int(row['rating']),
            "descripcion": row.get('descripcion', ''), # Opcional
            "relato": row['relato']
        }
        lista_puntos.append(punto)

    # 3. Guardar el JSON final
    with open(JSON_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(lista_puntos, f, indent=2, ensure_ascii=False)

    print(f"✅ ¡Atlas actualizado! Se procesaron {len(lista_puntos)} fotos.")
    print(f"📂 Archivo generado: {JSON_SALIDA}")

if __name__ == "__main__":
    generar_json()