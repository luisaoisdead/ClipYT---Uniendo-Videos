import os
import sys
import subprocess

def extraer_cuadros(video_path):
    # 1. Validar que el archivo exista
    if not os.path.isfile(video_path):
        print(f"❌ Error: No se encontró el archivo '{video_path}'")
        return

    # 2. Obtener rutas y nombres limpios
    directorio = os.path.dirname(os.path.abspath(video_path))
    nombre_base = os.path.splitext(os.path.basename(video_path))[0]

    out_inicial = os.path.join(directorio, f"{nombre_base}_inicial.png")
    out_final = os.path.join(directorio, f"{nombre_base}_final.png")

    print(f"🎬 Procesando video: {os.path.basename(video_path)}")

    try:
        # --- EXTRACCIÓN DEL PRIMER CUADRO ---
        print("📸 Extrayendo el 1er cuadro...")
        comando_inicial = [
            'ffmpeg', '-y', 
            '-i', video_path, 
            '-vframes', '1',     # Le pedimos que frene al leer exactamente 1 cuadro
            out_inicial
        ]
        # Ejecutamos ocultando los textos largos de FFmpeg
        subprocess.run(comando_inicial, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"   ✅ Guardado: {os.path.basename(out_inicial)}")

        # --- EXTRACCIÓN DEL ÚLTIMO CUADRO ---
        print("📸 Extrayendo el último cuadro...")
        # TRUCO PRO: '-sseof -2' lee solo los últimos 2 segundos del video.
        # '-update 1' hace que FFmpeg sobreescriba el mismo archivo PNG constantemente.
        # El resultado final es que el archivo guardado será tu cuadro final absoluto.
        comando_final = [
            'ffmpeg', '-y', 
            '-sseof', '-2', 
            '-i', video_path, 
            '-update', '1', 
            out_final
        ]
        subprocess.run(comando_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"   ✅ Guardado: {os.path.basename(out_final)}")

        print("\n🎉 ¡Extracción completada con éxito!")

    except subprocess.CalledProcessError:
        print("❌ Error fatal: FFmpeg no pudo procesar el video.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {str(e)}")

if __name__ == "__main__":
    # Asegurarnos de que el usuario mandó el nombre del video por consola
    if len(sys.argv) < 2:
        print("⚠️ Uso incorrecto. El formato debe ser:")
        print("   python recorte.py \"Nombre del Video.mp4\"")
    else:
        # sys.argv[1] contiene la ruta/nombre del video que le pases
        extraer_cuadros(sys.argv[1])