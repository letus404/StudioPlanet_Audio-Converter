#AQUI CONFIGURAMOS EL PATH para que ejecute ffmpeg portable.

import os

def configure_ffmpeg():
    FFMPEG_PATH = os.path.join(os.getcwd(), 'ffmpeg', 'bin')  # Ruta a la carpeta donde está ffmpeg
    os.environ["PATH"] += os.pathsep + FFMPEG_PATH  