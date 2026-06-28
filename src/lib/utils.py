import os
import subprocess

import lyricsgenius
from mutagen.id3 import ID3, USLT
import requests
from tqdm import tqdm
from ytmusicapi import YTMusic

ytmusic = YTMusic()
barra_progreso = None
GENIUS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


def obtener_portada(titulo):
    try:
        r = ytmusic.search(titulo, filter="songs")
        if r:
            url = r[0]["thumbnails"][-1]["url"]
            return url.split("=")[0] + "=w1000-h1000"
    except:
        pass
    return None


def descargar_imagen(url, ruta):
    img = requests.get(url)
    with open(ruta, "wb") as f:
        f.write(img.content)


def insertar_portada(mp3, cover):
    temp = mp3.replace(".mp3", "_tmp.mp3")

    resultado = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            mp3,
            "-i",
            cover,
            "-map",
            "0:0",
            "-map",
            "1:0",
            "-c:a",
            "copy",
            "-c:v",
            "mjpeg",
            "-map_metadata",
            "0",
            "-id3v2_version",
            "3",
            "-metadata:s:v",
            "title=Album cover",
            "-metadata:s:v",
            "comment=Cover (front)",
            temp,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if resultado.returncode == 0 and os.path.exists(temp):
        os.replace(temp, mp3)
    else:
        print(
            "Hubo un error al insertar la portada, pero el audio original se conservó."
        )
        if os.path.exists(temp):
            os.remove(temp)


def insertar_letra_en_mp3(mp3_path, letra):
    try:
        tags = ID3(mp3_path)
    except:
        tags = ID3()

    lyrics_text = "\n".join(letra)

    tags.delall("USLT")
    tags["USLT::spa"] = USLT(encoding=3, lang="spa", desc="", text=lyrics_text)
    tags.save(mp3_path)


def animacion_descarga(d):
    global barra_progreso
    if d["status"] == "downloading":
        if barra_progreso is None:
            # Obtenemos el tamaño del archivo para calcular el porcentaje
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            barra_progreso = tqdm(
                total=total_bytes,
                unit="B",
                unit_scale=True,
                desc="Descargando",
                colour="green",  # Color de la barra
                leave=True,  # Mantiene la barra visible hasta que termine la descarga
            )

        # Actualizamos el progreso
        descargado = d.get("downloaded_bytes", 0)
        if barra_progreso.total:
            barra_progreso.update(descargado - barra_progreso.n)

    elif d["status"] == "finished":
        if barra_progreso:
            barra_progreso.close()
            barra_progreso = None
        print("\n¡Descarga completada! Convirtiendo y procesando...")


def obtener_letra(artista, titulo_cancion):
    try:
        genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True)
        genius.verbose = False

        primera = None
        if " - " in titulo_cancion:
            primera = titulo_cancion.split(" - ")[0].strip()

        if artista:
            song = genius.search_song(titulo_cancion, artista)
            if song and song.lyrics:
                return song.lyrics.split("\n")
            if primera:
                song = genius.search_song(primera, artista)
                if song and song.lyrics:
                    return song.lyrics.split("\n")

        if primera:
            song = genius.search_song(primera)
            if song and song.lyrics:
                return song.lyrics.split("\n")

        song = genius.search_song(titulo_cancion)
        if song and song.lyrics:
            return song.lyrics.split("\n")
    except Exception as e:
        print(f"Error con Genius: {e}")
    return None
