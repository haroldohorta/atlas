import sqlite3
import os

# Configuración
db_gps = 'haroldo_indice.db' 
nueva_casa = r'F:\LEGADO_HAROLDO' 

conn = sqlite3.connect(db_gps)
cursor = conn.cursor()

print("1. Mapeando el nuevo orden en F:...")
mapa_f = {}
for raiz, dirs, archivos in os.walk(nueva_casa):
    for f in archivos:
        mapa_f[f] = os.path.join(raiz, f)

print(f"2. Reconectando puntos GPS...")
cursor.execute("SELECT Nombre, RutaFull FROM inventario WHERE Latitud IS NOT NULL")
fotos_gps = cursor.fetchall()

actualizados = 0
for nombre, ruta_vieja in fotos_gps:
    if nombre in mapa_f:
        cursor.execute("UPDATE inventario SET RutaFull = ? WHERE Nombre = ?", (mapa_f[nombre], nombre))
        actualizados += 1

conn.commit()
print(f"¡Listo! {actualizados} fotos con GPS ahora apuntan a F:.")
conn.close()