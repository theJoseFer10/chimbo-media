# Chimbo Media

YouTube / YouTube Music downloader interactivo por CLI.  
Descarga videos y música en **MP3** (320 kbps) o **MP4**, con portada, metadatos y letras incrustadas.

## Requisitos

- Python 3.12+
- `ffmpeg` instalado en el sistema (para conversión de audio e inserción de portada)

## Instalación

Clona el repositorio y prepara el entorno virtual:

```bash
git clone <repo-url>
cd chimbo-media
python -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

## Uso

Activa el entorno virtual y ejecuta:

```bash
source venv/bin/activate
python src/main.py
```

El asistente te guiará para pegar un enlace de YouTube, elegir formato (MP3/MP4), carpeta de salida, y más.

### Alias rápido (`.bashrc`)

Para ejecutar desde cualquier terminal sin escribir los pasos manuales, agrega esto a tu `~/.bashrc`:

```bash
alias chimbo='cd /ruta/completa/a/chimbo-media && source venv/bin/activate && python src/main.py'
```

Reemplaza `/ruta/completa/a/chimbo-media` con la ruta absoluta del proyecto.  
Después de guardar, recarga con `source ~/.bashrc` y ejecuta `chimbo` en cualquier directorio.

## Variables de entorno

| Variable                | Obligatoria | Descripción                                        |
|-------------------------|-------------|----------------------------------------------------|
| `GENIUS_ACCESS_TOKEN`   | No          | Token de la API de Genius para obtener letras. Si no se provee, se usa un token interno por defecto. |

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

## Autoría

- **makima**
- **David Gallegos**
