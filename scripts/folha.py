"""Folha de contato de um vídeo, para revisar sem assistir inteiro.

Uso:
  python folha.py videos/03-minha-aula.mp4          -> 03-minha-aula.folha.png (um quadro a cada 4 s)
  python folha.py videos/03-minha-aula.mp4 37.5     -> 03-minha-aula.t37.5.png (um quadro em tamanho real)
"""
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
video = sys.argv[1]
base = re.sub(r"\.mp4$", "", video)
info = subprocess.run([FF, "-i", video], capture_output=True, text=True).stderr
print(re.search(r"Duration: [^,]+", info).group(0))
if len(sys.argv) > 2:
    saida = f"{base}.t{sys.argv[2]}.png"
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", sys.argv[2], "-i", video, "-frames:v", "1", saida], check=True)
else:
    saida = f"{base}.folha.png"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", video, "-vf", "fps=1/4,scale=400:-1,tile=6x5",
                    "-frames:v", "1", saida], check=True)
print(saida)
