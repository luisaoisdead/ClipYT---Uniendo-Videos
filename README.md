# ClipYT - Estudio de Mezcla y Edición Avanzada

Para que este programa funcione correctamente, necesitas los binarios de **FFmpeg**, que es el motor encargado de procesar, unir y reproducir los videos y audios en segundo plano.

## Requisitos Previos: Archivos "FF"

El programa utiliza tres archivos ejecutables:
1. `ffmpeg.exe` (Se encarga de procesar y renderizar el archivo final)
2. `ffplay.exe` (Se utiliza para el reproductor de previsualización en vivo)
3. `ffprobe.exe` (Se usa para leer las duraciones y metadatos de los videos)

---

## ¿De dónde descargarlos? (Instrucciones para Windows)

1. Ingresa a la página oficial de descargas de FFmpeg para Windows: [gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
2. Busca la sección llamada **"release builds"**.
3. Descarga el archivo que termina en **-essentials_build.zip** (por ejemplo: `ffmpeg-release-essentials.zip`).
4. Extrae/Descomprime el archivo `.zip` que descargaste.
5. Abre la carpeta que extrajiste y entra en la subcarpeta llamada `bin`.
6. Ahí adentro encontrarás los tres archivos que necesitamos: `ffmpeg.exe`, `ffplay.exe` y `ffprobe.exe`.

---

## ¿Dónde colocarlos?

Tienes dos opciones para que la aplicación los detecte:

- **Opción A (La más fácil):** Copia esos tres archivos (`ffmpeg.exe`, `ffplay.exe`, `ffprobe.exe`) y pégalos **exactamente en la misma carpeta** donde tienes el script de Python (`unir_videos_gui v2.py`). 
- **Opción B (Usuarios avanzados):** Agrega la carpeta `bin` a la variable de entorno `PATH` de tu sistema operativo Windows.

¡Eso es todo! Con esos tres ejecutables listos, la aplicación funcionará perfectamente.
