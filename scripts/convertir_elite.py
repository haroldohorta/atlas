from PIL import Image
import os

# --- LA LISTA DE ÉLITE ---
archivos_a_convertir = [
    r"F:\fotos\uyuni_espejo_pano.jpg",
    r"F:\fotos\aerea_san_pedro (4).jpg",
    r"F:\fotos\aerea_san_pedro (5).jpg",
    r"F:\fotos\aerea_san_pedro (1).jpg",
    r"F:\fotos\aerea_san_pedro (2).jpg",
    r"F:\fotos\aerea_san_pedro (3).jpg",
    r"F:\fotos\reagan_nuclear.jpg"
]

print("🚀 Iniciando operación 'Dieta WebP' para las 7 elegidas...")
print("-" * 50)

contador = 0
for ruta_jpg in archivos_a_convertir:
    # Crear la ruta de salida con extensión .webp
    # (Manejamos .jpg y .JPG por si acaso)
    ruta_webp = ruta_jpg.replace(".jpg", ".webp").replace(".JPG", ".webp")

    try:
        if not os.path.exists(ruta_jpg):
             print(f"⚠️ ADVERTENCIA: No se encontró el archivo: {ruta_jpg}")
             continue

        # 1. Abrir la imagen
        img = Image.open(ruta_jpg)
        
        # 2. Guardar como WebP (Calidad 85 es excelente para web)
        img.save(ruta_webp, "WEBP", quality=85)
        
        # Cerrar el archivo para poder borrarlo
        img.close()
        
        nombre_archivo = os.path.basename(ruta_webp)
        print(f"✅ [{contador+1}/7] Convertida: {nombre_archivo}")

        # 3. Borrar el JPG original para no dejar basura
        os.remove(ruta_jpg)
        print(f"   🗑️ JPG original eliminado.")
        
        contador += 1

    except Exception as e:
        print(f"❌ Error crítico con {os.path.basename(ruta_jpg)}: {e}")

print("-" * 50)
print(f"\n✨ Operación terminada. {contador} fotos pasaron a mejor vida (WebP).")