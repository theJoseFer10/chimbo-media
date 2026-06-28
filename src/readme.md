# Chimbo Media
En este documento se redacta como descargar e implementar el script de chimbo media en su sistema.
## Que es Chimbo Media?
Chimbo Media es un script que permite descargar contenido multimedia en su sistema.
## Requisitos.
- Python 3.x
- Ffmpeg instalado en su sistema
- Una terminal o emulador de terminal
# Instalación
- Clone el repositorio de Chimbo Media en su sistema.
```bash
git clone https://github.com/theJoseFer10/chimbo-media.git
```
- Navegue al directorio del repositorio clonado.
```bash
cd chimbo-media
```
- Cree un entorno virtual para el proyecto.
```bash
python -m venv venv
```
- Instale las dependencias del proyecto.
```bash
pip install -r requirements.txt
```

# Creación de alias en bashrc
- Abra su archivo `~/.bashrc` en un editor de texto.
```bash
nano ~/.bashrc
```
- Agregue el siguiente alias al final del archivo.
```bash
alias chimbomedia="cd ruta/chimbomedia && source venv/bin/activate && python src/main.py"
```
- Guarde y cierre el archivo.
```bash
exit
```
Si despues de usar el programa el entorno virtual sigue activo, ejecute el siguiente comando para desactivarlo.
```bash
deactivate
```

# Ejecución
- Para ejecutar Chimbo Media, simplemente ejecute el siguiente comando en su terminal.
```bash
chimbomedia
```

## Creditos
- Makima
- David Gallegos
