import yt_dlp
import os
from logo import logo
import requests
import subprocess
from ytmusicapi import YTMusic
import questionary
from tqdm import tqdm

print(logo)
print("by - makima and David Gallegos \n")

ytmusic = YTMusic()

def obtener_portada(titulo):
    try:
        r = ytmusic.search(titulo, filter="songs")
        if r:
            url = r[0]['thumbnails'][-1]['url']
            return url.split('=')[0] + '=w1000-h1000'
    except:
        pass
    return None

def descargar_imagen(url, ruta):
    img = requests.get(url)
    with open(ruta, 'wb') as f:
        f.write(img.content)

def insertar_portada(mp3, cover):
    temp = mp3.replace(".mp3", "_tmp.mp3")

    resultado = subprocess.run([
        "ffmpeg", "-y",
        "-i", mp3,
        "-i", cover,
        "-map", "0:0", "-map", "1:0",
        "-c:a", "copy",
        "-c:v", "mjpeg", 
        "-map_metadata", "0",
        "-id3v2_version", "3",
        "-metadata:s:v", "title=Album cover",
        "-metadata:s:v", "comment=Cover (front)",
        temp
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if resultado.returncode == 0 and os.path.exists(temp):
        os.replace(temp, mp3)
    else:
        print("Hubo un error al insertar la portada, pero el audio original se conservó.")
        if os.path.exists(temp):
            os.remove(temp)

# Variable global para mantener viva la animación
barra_progreso = None

# Esta función conecta yt_dlp con la animación de tqdm
def animacion_descarga(d):
    global barra_progreso
    if d['status'] == 'downloading':
        if barra_progreso is None:
            # Obtenemos el tamaño del archivo para calcular el porcentaje
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            barra_progreso = tqdm(
                total=total_bytes, 
                unit='B', 
                unit_scale=True, 
                desc="Descargando", 
                colour="green", # Color de la barra
                leave=True # Mantiene la barra visible hasta que termine la descarga
            )
        
        # Actualizamos el progreso
        descargado = d.get('downloaded_bytes', 0)
        if barra_progreso.total:
            barra_progreso.update(descargado - barra_progreso.n)
            
    elif d['status'] == 'finished':
        if barra_progreso:
            barra_progreso.close()
            barra_progreso = None
        print("\n¡Descarga completada! Convirtiendo y procesando...")


while True:
    enlace = questionary.text("Ingresa el enlace de youtube => ").ask()
    formato = questionary.select("¿Qué formato prefieres?", choices=["MP3", "MP4"]).ask()
    ruta = questionary.text("Pega la ruta de la carpeta (Enter para carpeta actual): ").ask()
    if not ruta or not os.path.exists(ruta):
        ruta = "./Music"
        os.makedirs(ruta, exist_ok=True) 

    # Configuración base con nuestra nueva animación
    opciones_base = {
        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noprogress': True, # Apaga la barra por defecto de yt_dlp
        'progress_hooks': [animacion_descarga], # Enciende nuestra barra personalizada
        'quiet': True, # Mantiene la consola limpia de mensajes innecesarios
        'no_warnings': True
    }

    portada_video = False

    if formato == "MP3":
        portada_video = questionary.confirm("¿Deseas descargar la miniatura original del video? (Si eliges No, se buscará en YT Music)").ask()
        questionary.print("\nIniciando proceso...")
        opciones_base.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320', 
                },
                {
                    # Esto le dice a yt_dlp que incruste Artista, Título, etc. en el archivo
                    'key': 'FFmpegMetadata', 
                    'add_metadata': True,
                }
            ],
        })

    elif formato == "MP4":
        print("\nIniciando proceso...")
        opciones_base.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })
    else:
        print("Opción no válida.")
        continue

    try:
        with yt_dlp.YoutubeDL(opciones_base) as ydl:
            info = ydl.extract_info(enlace, download=True)

            def procesar_audio(item_info):
                titulo = ydl.prepare_filename(item_info)
                mp3 = titulo.rsplit('.', 1)[0] + ".mp3"
                
                if portada_video:
                    print("Usando la miniatura original del video...")
                    cover_url = item_info.get('thumbnail') 
                else:
                    print("Buscando la mejor portada en YT Music...")
                    cover_url = obtener_portada(item_info.get('title', ''))

                if cover_url:
                    cover_path = f"{ruta}/cover.jpg"
                    descargar_imagen(cover_url, cover_path)
                    if os.path.exists(mp3): 
                        insertar_portada(mp3, cover_path)
                        if os.path.exists(cover_path):
                            os.remove(cover_path) 
                        print("✅ Portada insertada con éxito.")
                else:
                    print("No se encontró ninguna portada.")

            # playlist
            if 'entries' in info:
                for video in info['entries']:
                    if video is None:
                        continue
                    
                    if formato == "MP3":
                        procesar_audio(video)

            # video individual
            else:
                if formato == "MP3":
                    procesar_audio(info)

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    volver_a_descargar = questionary.confirm("\n¿Realizar otra descarga?").ask()
    if not volver_a_descargar:
        print("¡Hasta luego!")
        break
    else:
        print("\n" + "=" * 30 + "\n")