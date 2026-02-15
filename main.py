import yt_dlp
import os
from logo import logo

print(logo)
print("by - makima\n")

while True:
    enlace = input("Ingresa el enlace de youtube => ")
    print("¿Qué formato prefieres?\n1. MP3 (Audio)\n2. MP4 (Video)")
    formato = input("==> ")

    # Pedimos la ruta y la limpiamos
    ruta = input("Pega la ruta de la carpeta donde quieres guardar el archivo: ").strip()

    # Validar que la ruta existe, si no, usar la carpeta actual
    if not os.path.exists(ruta):
        print("La ruta no existe. Se guardará en la carpeta actual.")
        ruta = "."

    # Configuración base con la ruta de destino
    # El '%(title)s.%(ext)s' sirve para que el nombre sea el título del video
    opciones_base = {
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
    }

    if formato == "1":
        print("Descargando MP3...")
        # Actualizamos los datos de configuracion.
        opciones_base.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        with yt_dlp.YoutubeDL(opciones_base) as ydl:
            ydl.download([enlace])

        print("---Descarga completa---")

    elif formato == "2":
        print("Descargando MP4...")
        opciones_base.update({
            'format': 'bestvideo+bestaudio/best',
        })
        with yt_dlp.YoutubeDL(opciones_base) as ydl:
            ydl.download([enlace])

        print("---Descarga completa---")
    else:
        print("Opción no válida.")

    volver_a_descargar = input("Realizar otra descarga? Si/No => ").strip().lower()
    if volver_a_descargar in ["no", "n"]:
        print("Hasta luego")
        break
    else:
        print("\n" + "="*30 + "\n")