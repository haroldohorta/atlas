import os

def mapear_bunker(ruta_raiz, nivel_max_fotos=1):
    print(f"\n🔍 ESCANEO DE ESTRUCTURA: {ruta_raiz}")
    print("=" * 50)

    for raiz, carpetas, archivos in os.walk(ruta_raiz):
        # Filtros de exclusión: Git y la carpeta del legado
        if '.git' in carpetas:
            carpetas.remove('.git')
        if 'legado_haroldo' in carpetas:
            carpetas.remove('legado_haroldo')

        # Calcular nivel de profundidad
        nivel = raiz.replace(ruta_raiz, '').count(os.sep)
        separador = '  ' * nivel
        nombre_carpeta = os.path.basename(raiz) or raiz

        # Imprimir la carpeta actual
        print(f"{separador}📁 {nombre_carpeta}/")

        # Imprimir archivos (resumen para carpetas de fotos)
        sub_separador = '  ' * (nivel + 1)
        
        if "fotos" in raiz and nivel >= nivel_max_fotos:
            if archivos:
                print(f"{sub_separador}📸 [{len(archivos)} archivos fotográficos...]")
        else:
            for f in archivos:
                if f != "revisar_atlas.py":
                    print(f"{sub_separador}📄 {f}")

if __name__ == "__main__":
    ruta_actual = os.getcwd()
    mapear_bunker(ruta_actual)