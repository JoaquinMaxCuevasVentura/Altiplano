"""Genera las figuras del artículo a partir de los esquemas SVG.

Uso (desde la raíz del repositorio):
    python3 articulo/generar_figuras.py

Lee analisis/esquemas/fig*.svg, quita el título «Fig. N · …» de cada esquema
y escribe articulo/figuras/figura_1.png … figura_6.png con la numeración del
artículo, que sigue el orden de aparición. Necesita Chromium (ruta en la
variable CHROME) y Pillow.

Si sustituyes una figura por la fotografía de su pastel, no vuelvas a correr
este script sobre ese número o sobrescribirá la fotografía (véase
figuras/LEEME.md).
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
ESQ = BASE.parent / "analisis" / "esquemas"
OUT = BASE / "figuras"
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
SCALE = 4
# Esquema de origen -> número de figura en el artículo.
MAPA = [("fig1_craneo_nido.svg", 1), ("fig2_signo_mapa.svg", 2), ("fig3_apacheta.svg", 3),
        ("fig6_castillete.svg", 4), ("fig4_pelvis.svg", 5), ("fig5_centinela.svg", 6)]


def sin_titulo(svg):
    svg = re.sub(r'\s*<text[^>]*>Fig\. \d[^<]*</text>', "", svg)
    return re.sub(r'\s*<text[^>]*>esquema \([^<]*\)</text>', "", svg)


def recorte_superior(im):
    """Recorta la franja vacía que deja el título."""
    fondo, px = im.getpixel((2, 2)), im.load()
    for y in range(im.height):
        if any(sum(abs(a - b) for a, b in zip(px[x, y], fondo)) > 30 for x in range(0, im.width, 2)):
            return im.crop((0, max(0, y - 8 * SCALE), im.width, im.height))
    return im


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for origen, n in MAPA:
            svg = sin_titulo((ESQ / origen).read_text(encoding="utf8"))
            w, h = (int(float(v)) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()[2:])
            svg = svg.replace("<svg ", f'<svg width="{w}" height="{h}" ', 1)
            html = Path(tmp) / f"f{n}.html"
            html.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                            f"svg{{display:block}}</style>{svg}", encoding="utf8")
            captura = Path(tmp) / f"f{n}.png"
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            f"--force-device-scale-factor={SCALE}", f"--window-size={w + 40},{h + 200}",
                            f"--screenshot={captura}", html.as_uri()], check=True, capture_output=True)
            im = Image.open(captura).convert("RGB").crop((0, 0, w * SCALE, h * SCALE))
            destino = OUT / f"figura_{n}.png"
            recorte_superior(im).save(destino, dpi=(300, 300))
            print(f"{origen} -> {destino.name}")


if __name__ == "__main__":
    main()
