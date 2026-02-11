import os
import pandas as pd
import json

# ================= CONFIGURACIÓN =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FOTOS = os.path.join(BASE_DIR, "fotos")
RUTA_CSV = os.path.join(BASE_DIR, "data", "zonas.csv")
ARCHIVO_SALIDA = os.path.join(BASE_DIR, "data", "puntos_mapa.json")

# Diccionario de categorías
CATEGORIAS = {
    "pub_": "Crónica & Etnografía",
    "nomad_": "Bitácora Nómada",
    "fly_": "Registro Aéreo",
    "nav_": "Registro Naval"
}

# Extensiones válidas (Ignoramos archivos basura)
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')

def escanear_todo():
    print("🚀 Iniciando Protocolo de Rescate y Sincronización...")

    if not os.path.exists(RUTA_CSV):
        print("❌ ERROR: No encuentro data/zonas.csv")
        return

    # Cargar CSV
    df_zonas = pd.read_csv(RUTA_CSV)
    # Convertimos a string y quitamos espacios para evitar errores tontos
    df_zonas['zona'] = df_zonas['zona'].astype(str).str.strip().lower()
    
    # Mapa de coordenadas en memoria
    info_zonas = {}
    for _, row in df_zonas.iterrows():
        info_zonas[row['zona']] = {
            'lat': float(row['lat']), 
            'lon': float(row['lon']), 
            'desc': row['descripcion']
        }

    todos_los_puntos = []

    # Recorrer el disco
    for root, dirs, files in os.walk(RUTA_FOTOS):
        # Nombre real de la carpeta en el disco (puede tener mayúsculas)
        carpeta_real = os.path.basename(root)
        nombre_lower = carpeta_real.lower()
        
        # Detectar Zona
        zona_detectada = nombre_lower
        categoria_detectada = "Archivo General"
        
        for pre, cat in CATEGORIAS.items():
            if nombre_lower.startswith(pre):
                categoria_detectada = cat
                zona_detectada = nombre_lower.replace(pre, "")
                break
        
        # ¿Esta carpeta es una zona válida del CSV?
        if zona_detectada in info_zonas:
            datos = info_zonas[zona_detectada]
            
            # Filtrar fotos válidas (ignorando basura)
            fotos_validas = [f for f in files if f.lower().endswith(EXTS)]
            
            if fotos_validas:
                print(f"  ✅ Zona Detectada: {zona_detectada.upper()} ({len(fotos_validas)} fotos)")
            
            for foto in fotos_validas:
                # TRUCO: Construimos la ruta RELATIVA exacta tal cual está en el disco
                # Esto arregla el problema de Linux vs Windows
                ruta_completa = os.path.join(root, foto)
                ruta_relativa = os.path.relpath(ruta_completa, BASE_DIR).replace("\\", "/")
                
                # Excluir archivos que empiecen con punto (ocultos) o '._' (mac/linux trash)
                if foto.startswith(".") or foto.startswith("._"):
                    continue

                todos_los_puntos.append({
                    "id": foto,
                    "zona": zona_detectada,
                    "capa": categoria_detectada,
                    "lat": datos['lat'],
                    "lon": datos['lon'],
                    "thumb": ruta_relativa, # Ruta exacta para GitHub
                    "descripcion": datos['desc']
                })

    # Guardar JSON
    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(todos_los_puntos, f, indent=4, ensure_ascii=False)

    print(f"\n✨ BASE DE DATOS REPARADA: {len(todos_los_puntos)} imágenes listas para despegue.")

if __name__ == "__main__":
    escanear_todo()