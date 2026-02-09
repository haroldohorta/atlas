#  Haroldo Horta: Atlas Digital y Soberanía Visual
> *"Desde el corazon de la revolución Sandinista en Nicaragua al silencio infinito de Atacama. Un archivo rescatado para no olvidar el vuelo ni la dignidad humana."*

## 📜 El Manifiesto: Una Vida en Tres Actos

Este repositorio constituye la columna vertebral de la trayectoria y legado fotográfico de Haroldo Horta. No es solo un almacenamiento de archivos; es un acto de resistencia técnica y una reconexión con el valor de lo humano a través del lente, tando desde la tierra como desde el aire.

---

## 🏛️ Estructura de Capas (Indexación Activa)

El archivo ha sido reorganizado en la unidad maestra `F:` bajo una lógica de **Capas de Intención**, permitiendo una navegación que cruza la geografía con el peso ético de la imagen.

### 🔴 CAPA 01: EL TESTIGO (Corresponsalía 1979 - 1998)
*El registro del grano de la historia donde el mundo tembló.*

| Región | Hitos Visuales y Conflictos | Archivos de Referencia |
| :--- | :--- | :--- |
| **🇳🇮 Nicaragua** | Brigadas Telcor, Hospital de Managua, La Montaña. | `soldado_herido.JPG`, `ortega.JPG`, `historica.JPG` |
| **🇵🇪 Perú** | Captura de Abimael Guzmán, Coche Bomba, Epidemia de Cólera. | `Verano_Sangriento_1997.jpg`, `Fujimori_1991.jpg` |
| **🇨🇴 Colombia** | Pulso urbano y dinámicas sociales en Medellín. | `pub_medellin_root` |
| **🇨🇱 Chile (Lota)** | El fin de la era del carbón y la resistencia minera. | `seleccion_lota_01.jpg` |

### 🟡 CAPA 02: EL AUTOR (Editorial y Patrimonio)
*La construcción del relato nacional y la arqueología industrial.*

- **Brasil (Fordlandia):** Registro del sueño fallido de Henry Ford en el Amazonas (`fordlandia_01-18.JPG`).
- **Chile Industrial:** La planta de Litio, el Estrecho de Magallanes y la Antártica.
- **Obra Publicada:** Portadas de revistas *Caretas*, *Paula*, *AfoCo* y Libros (*Faros de Chile*, *Chiloé*, *Esmeralda*).

### 🔵 CAPA 03: EL NÓMADE (Libre Vuelo y Síntesis)
*Habitar el territorio desde el aire: La perspectiva del Paratrike y el Dron.*

- **Bolivia (Salar de Uyuni):** Panorámicas, reflejos y la abstracción del salar.
- **Chile (Atacama):** San Pedro, Valle de la Luna, Tebenquinche y Lagunas Altiplánicas.
- **Tecnología:** Integración de Dron como compañero de vuelo y explorador de formas de vida alternativas.

---

## 🧭 Infraestructura Técnica

### 📍 El Mapa Maestro (SIG)
El corazón del proyecto es un visualizador geográfico basado en **Leaflet** que vincula cada archivo de la unidad `F:` con su coordenada exacta. 
- **Inyección GPS:** Datos extraídos vía Adobe Bridge para situar al usuario en el lugar del evento.
- **Capas Dinámicas:** Opción de visualizar por intención (Corresponsal, Editorial o Vuelo).

### 🗄️ El Cerebro: `haroldo_indice.db`
Base de datos SQLite que indexa los 28TB de archivo maestro, permitiendo búsquedas por:
- **Metadatos:** Fecha, cámara, ISO y locación.
- **Etiquetas Éticas:** Clasificación por hito histórico o valor documental.

---

## 🏛️ Validación Internacional
La mirada de Haroldo ha sido el lente de medios globales, validando una vida dedicada al registro de calidad:

| Bloque Editorial | Medios Destacados |
| :--- | :--- |
| **Prensa Europea** | *Stern*, *Folket i Bild*, *Zeitenspiegel* (Suecia/Alemania). |
| **Prensa Latinoamérica** | *Caretas*, *Paula*, *Página/12*, *La Tercera*. |
| **Patrimonio** | *Kactus*, *UNESCO*, *Armada de Chile*. |

---

## 🚀 Próximos Pasos
- [ ] **Build v1.0:** Implementar el selector de capas en el mapa interactivo.
- [ ] **Inyección de Relatos:** Vincular audios/textos de Haroldo a las fotos de Nicaragua y Perú.
- [ ] **Galería Liviana:** Generación de miniaturas `.webp` para navegación fluida.

---
*Este proyecto es custodiado por la comunidad SUR DAO en Ituzaingó, 2026.*
