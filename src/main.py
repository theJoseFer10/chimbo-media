import os
import re

import questionary
import yt_dlp
from ytmusicapi import YTMusic

from lib.utils import (
    animacion_descarga,
    descargar_imagen,
    insertar_letra_en_mp3,
    insertar_portada,
    obtener_letra,
    obtener_portada,
)
from logo import logo

print(logo)
print("by - makima and David Gallegos \n")

ytmusic = YTMusic()


while True:
    enlace = questionary.text("Ingresa el enlace de youtube => ").ask()
    formato = questionary.select(
        "¿Qué formato prefieres?", choices=["MP3", "MP4"]
    ).ask()
    ruta = questionary.text(
        "Pega la ruta de la carpeta (Enter para carpeta actual): "
    ).ask()
    if not ruta or not os.path.exists(ruta):
        ruta = "./Music"
        os.makedirs(ruta, exist_ok=True)

    # Configuración base con nuestra nueva animación
    opciones_base = {
        "outtmpl": f"{ruta}/%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noprogress": True,  # Apaga la barra por defecto de yt_dlp
        "progress_hooks": [animacion_descarga],  # Enciende nuestra barra personalizada
        "quiet": True,  # Mantiene la consola limpia de mensajes innecesarios
        "no_warnings": True,
    }

    portada_video = False

    if formato == "MP3":
        portada_video = questionary.confirm(
            "¿Deseas descargar la miniatura original del video? (Si eliges No, se buscará en YT Music)"
        ).ask()
        questionary.print("\nIniciando proceso...")
        opciones_base.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    },
                    {
                        # Esto le dice a yt_dlp que incruste Artista, Título, etc. en el archivo
                        "key": "FFmpegMetadata",
                        "add_metadata": True,
                    },
                ],
            }
        )

    elif formato == "MP4":
        print("\nIniciando proceso...")
        opciones_base.update(
            {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            }
        )
    else:
        print("Opción no válida.")
        continue

    try:
        with yt_dlp.YoutubeDL(opciones_base) as ydl:
            info = ydl.extract_info(enlace, download=True)

            def procesar_audio(item_info):
                titulo_archivo = ydl.prepare_filename(item_info)
                mp3 = titulo_archivo.rsplit(".", 1)[0] + ".mp3"

                # 1. Extracción inteligente: Preferimos los campos 'artist' y 'track' que yt-dlp
                # ya extrajo de YouTube Music, si no existen, usamos el title y limpiamos.
                artista = (
                    item_info.get("artist")
                    or item_info.get("uploader", "")
                    .replace(" - Topic", "")
                    .split(",")[0]
                    .strip()
                )

                if len(artista) > 20:
                    artista = None

                raw_title = item_info.get("track") or item_info.get("title", "")

                # 2. Limpieza de texto: quitamos paréntesis/corchetes, texto tipo (Official Video), etc.
                titulo_limpio = re.sub(r"\(.*?\)|\[.*?\]", "", raw_title).strip()

                print(f"Buscando letra para: {artista} - {titulo_limpio}")

                # 3. Llamada a la función (asegúrate de que obtener_letra en lib/utils.py
                # acepte estos dos argumentos ahora)
                letra = obtener_letra(artista, titulo_limpio)

                if letra:
                    ruta_txt = mp3.rsplit(".", 1)[0] + ".txt"
                    with open(ruta_txt, "w", encoding="utf-8") as f:
                        f.write("\n".join(letra))
                        print(f"✅ Letra guardada en {ruta_txt}.")
                    try:
                        insertar_letra_en_mp3(mp3, letra)
                        print("✅ Letra incrustada en el ID3 del MP3.")
                    except Exception as e:
                        print(f"⚠️  No se pudo incrustar la letra en ID3: {e}")
                else:
                    print("No se encontró la letra.")

                if portada_video:
                    print("Usando la miniatura original del video...")
                    cover_url = item_info.get("thumbnail")
                else:
                    print("Buscando la mejor portada en YT Music...")
                    cover_url = obtener_portada(item_info.get("title", ""))

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
            if "entries" in info:
                for video in info["entries"]:
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
