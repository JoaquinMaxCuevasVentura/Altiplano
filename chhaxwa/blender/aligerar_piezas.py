"""Aligera los PNG de las piezas y de los diagramas: los pasa a una paleta de 64 colores, sin tramado.

Los diagramas son blancos con contornos y pocos tonos, así que no pierden nada visible. Se corre con el Python del
sistema (necesita Pillow), después de piezas.py o de diagramas.py:
    python3 chhaxwa/blender/aligerar_piezas.py
"""
import sys
from pathlib import Path

from PIL import Image

sys.dont_write_bytecode = True
RENDERS = Path(__file__).resolve().parent.parent / "renders"

antes = despues = 0
for p in sorted(list(RENDERS.glob("piezas/pieza_*.png")) + list(RENDERS.glob("diagramas/diagrama_*.png"))):
    im = Image.open(p)
    if im.mode == "P":
        continue
    antes += p.stat().st_size
    im.convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(p, optimize=True)
    despues += p.stat().st_size
print(f"{antes / 1e6:.1f} MB -> {despues / 1e6:.1f} MB")
