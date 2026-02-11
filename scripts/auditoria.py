import os
import pandas as pd

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_FOTOS = os.path.join(BASE_DIR, "fotos")
RUTA_CSV = os.path.join(BASE_DIR, "data", "zonas.csv")

def auditar():
    print("🔍 --- INICIANDO AUDITORÍA DE RUTAS ---")
    
    if not os.path.exists(RUTA_CSV):
        print("❌ Error: No se encuentra data/zonas.csv")
        return

    # 1. Leer el CSV y normalizar los nombres de las zonas
    df = pd.read_csv(RUTA_CSV)
    # Creamos un set de zonas normalizadas (minúsculas, sin espacios, sin tildes básicas)
    zonas_csv = set(df['zona'].str.strip().str.lower().str.replace(" ", "_").tolist())

    print(f"📊 Zonas registradas en CSV: {len(zonas_csv)}")
    print("-" * 40)

    carpetas_en_disco = [d for d in os.listdir(RUTA_FOTOS) if os.path.isdir(os.path.join(RUTA_FOTOS, d))]
    
    errores = 0
    encontrados = 0

    for carpeta in carpetas_en_disco:
        nombre_original = carpeta
        nombre_limpio = carpeta.lower()
        
        # Quitamos los prefijos para comparar con el CSV
        zona_carpeta = nombre_limpio.replace("pub_", "").replace("nomad_", "").replace("fly_", "").replace("nav_", "")
        
        if zona_carpeta in zonas_csv:
            print(f"✅ OK: '{nombre_original}' coincide con el CSV.")
            encontrados += 1
        else:
            print(f"⚠️  ERROR: La carpeta '{nombre_original}' NO existe en el CSV.")
            print(f"    (Buscando la palabra '{zona_carpeta}' en la columna 'zona')")
            errores += 1

    print("-" * 40)
    print(f"📈 RESULTADO FINAL:")
    print(f"   - Carpetas vinculadas: {encontrados}")
    print(f"   - Carpetas huérfanas: {errores}")
    
    if errores > 0:
        print("\n💡 CONSEJO: Agrega los nombres de las carpetas huérfanas al archivo 'data/zonas.csv'")
        print("   con sus coordenadas para que el mapa las pueda mostrar.")

if __name__ == "__main__":
    auditar()