from PIL import Image, ImageOps
import os

CARPETA_ENTRADA = r"F:\fotos\recortes"
CARPETA_SALIDA = r"F:\fotos\recortes\assets_web"

# --- ROTACIONES MANUALES (Si el auto-giro falla) ---
# Pon aquí el nombre original y cuántos grados quieres girar (sentido anti-horario)
ROTACIONES_MANUALES = {
    "El_comercio_verano_sangriento_1997.jpeg": 270, # Prueba con 90, -90 o 180
}

MAPEO_NOMBRES = {
    "new_york_times_1987.jpeg": "horta-new-york-times-nicaragua-1987",
    "spiegel_das_war_1991.jpeg": "horta-stern-jahrbuch-portada-1991",
    "das_war_1991_colera.jpeg": "horta-stern-anuario-colera-peru-1991",
    "spiegel_pampa_1991.jpeg": "horta-der-spiegel-argentina-pampa-1991",
    "spiegel_pampa_1991_tex.jpeg": "horta-der-spiegel-argentina-pampa-texto",
    "pub_francia_colera.jpeg": "horta-francia-reportaje-colera-peru",
    "consulado_managua.jpeg": "horta-documento-consulado-managua-1979",
    "dossier_pub.jpeg": "horta-dossier-derechos-humanos-chile",
    "sueca_estadio_nacional.jpeg": "horta-frankfurter-allgemeine-estadio-nacional",
    "sueca_estadio_texto_1.jpeg": "horta-frankfurter-allgemeine-estadio-texto-1",
    "sueca_estadio_texto_2.jpeg": "horta-frankfurter-allgemeine-estadio-texto-2",
    "miembros_ zeitenspiegel.jpeg": "horta-agencia-zeitenspiegel-alemania-equipo",
    "bilder_portada_.jpeg": "horta-folket-i-bild-portada-nicaragua",
    "bilder_texto_1.jpeg": "horta-folket-i-bild-perfil-autor",
    "bilder_doble_pag1.jpeg": "horta-folket-i-bild-nicaragua-doble-1",
    "bilder_doble_pag_2.jpeg": "horta-folket-i-bild-nicaragua-doble-2",
    "revista_sueca_1995.jpeg": "horta-revista-sueca-especial-1995",
    "sueca_sondag_.jpeg": "horta-dn-sondag-suecia-cronica",
    "sueca_sondag_portada_1.jpeg": "horta-dn-sondag-suecia-portada-1",
    "sueca_sondag_portada_2.jpeg": "horta-dn-sondag-suecia-portada-2",
    "El_comercio_verano_sangriento_1997.jpeg": "horta-el-comercio-peru-embajada-1997",
    "el_comercio_1_enero_1999.jpeg": "horta-el-comercio-peru-archivo-1999",
    "colera_sueca_2.jpeg": "horta-suecia-reportaje-colera-peru-2",
    "sueca_colera_portada.jpeg": "horta-suecia-reportaje-colera-portada",
    "sueca_colera_texto.jpeg": "horta-suecia-reportaje-colera-texto",
    "exposicion_europa_rev_sandinista_1.jpeg": "horta-exposicion-suecia-fotograficentrum-1",
    "exposicion_europa_rev_sandinista_2.jpeg": "horta-exposicion-suecia-fotograficentrum-2",
    "exposicion_europa_rev_sandinista_3.jpeg": "horta-exposicion-suecia-fotograficentrum-3",
    "exposicion_europa_rev_sandinista_4.jpeg": "horta-exposicion-suecia-fotograficentrum-4"
}

if not os.path.exists(CARPETA_SALIDA):
    os.makedirs(CARPETA_SALIDA)

print("🔄 Aplicando corrección manual de ángulos...")

for archivo in os.listdir(CARPETA_ENTRADA):
    if archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.tif')):
        nombre_seo = MAPEO_NOMBRES.get(archivo, archivo.lower().replace("_", "-").replace(" ", "-"))
        
        ruta_entrada = os.path.join(CARPETA_ENTRADA, archivo)
        ruta_salida = os.path.join(CARPETA_SALIDA, f"{nombre_seo}.webp")

        try:
            with Image.open(ruta_entrada) as img:
                # 1. Corrección automática por EXIF
                img = ImageOps.exif_transpose(img)
                
                # 2. Corrección MANUAL si está en la lista
                if archivo in ROTACIONES_MANUALES:
                    angulo = ROTACIONES_MANUALES[archivo]
                    img = img.rotate(angulo, expand=True)
                    print(f"🔄 Giro manual de {angulo}° aplicado a: {archivo}")

                img = img.convert("RGB")
                img.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
                img.save(ruta_salida, "WEBP", quality=82)
                print(f"✅ Procesado: {nombre_seo}.webp")
        except Exception as e:
            print(f"❌ Error en {archivo}: {e}")

print(f"\n✨ ¡Check out en '{CARPETA_SALIDA}'! Si la embajada sigue torcida, cambia el número en el script.")