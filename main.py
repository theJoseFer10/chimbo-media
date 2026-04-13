import yt_dlp
import os
from logo import logo
import requests
import subprocess
from ytmusicapi import YTMusic

print(logo)
print("by - makima (Enhanced Version)\n")

ytmusic = YTMusic()

def obtener_portada(titulo):
    try:
        r = ytmusic.search(titulo, filter="songs")
        if r:
            url = r[0]['thumbnails'][-1]['url']
            return url.split('=')[0] + '=w1000-h1000'  # HD 🔥
    except:
        pass
    return None

def descargar_imagen(url, ruta):
    img = requests.get(url)
    with open(ruta, 'wb') as f:
        f.write(img.content)

def insertar_portada(mp3, cover):
    temp = mp3.replace(".mp3", "_tmp.mp3")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", mp3,
        "-i", cover,
        "-map", "0", "-map", "1",
        "-c", "copy",
        "-id3v2_version", "3",
        "-metadata:s:v", "title=Album cover",
        "-metadata:s:v", "comment=Cover (front)",
        temp
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.replace(temp, mp3)

while True:
    enlace = input("Ingresa el enlace de youtube => ")
    print("¿Qué formato prefieres?\n1. MP3 (Alta Calidad + Portada)\n2. MP4 (Video)")
    formato = input("==> ")

    ruta = input("Pega la ruta de la carpeta (Enter para carpeta actual): ").strip()
    if not ruta or not os.path.exists(ruta):
        ruta = "."

    # Configuración base
    opciones_base = {
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'restrictfilenames': True

    }

    if formato == "1":
        print("Descargando MP3 en alta calidad (320kbps) con metadatos...")
        opciones_base.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', # Máxima calidad de audio
                }
            ],
        })
    
    elif formato == "2":
        print("Descargando MP4...")
        opciones_base.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })
    else:
        print("Opción no válida.")
        continue

    try:
        with yt_dlp.YoutubeDL(opciones_base) as ydl:
            info = ydl.extract_info(enlace, download=False)
            titulo = ydl.prepare_filename(info)
            print("Descargando...")
            ydl.download([enlace])
        
        mp3 = f"{titulo.replace(".webm","")}.mp3"

        print("Buscando portada...")
        cover_url = obtener_portada(titulo)

        if cover_url:
            cover_path = f"{ruta}/cover.jpg"
            descargar_imagen(cover_url, cover_path)

            print("Insertando portada...")
            insertar_portada(mp3, cover_path)

            os.remove(cover_path)
        else:
            print("No se encontró portada")

        print("--- Descarga completa con éxito ---")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    volver_a_descargar = input("\n¿Realizar otra descarga? Si/No => ").strip().lower()
    if volver_a_descargar in ["no", "n"]:
        print("¡Hasta luego!")
        break
    else:
        print("\n" + "="*30 + "\n")