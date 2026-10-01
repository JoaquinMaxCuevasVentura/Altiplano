"""Genera las figuras del artículo a partir de las notaciones SVG.

Uso (desde la raíz del repositorio):
    python3 articulo/generar_figuras.py            # las ocho
    python3 articulo/generar_figuras.py 2 5        # solo las figuras 2 y 5

Las ocho figuras salen de analisis/esquemas/diagramas/, que escribe
generar_diagramas.js (córrelo antes): los esquemas de encaje de las figuras 1
a 6 y los diagramas de las figuras 7 y 8, todos como notaciones
(analisis/21 y analisis/23). Escribe articulo/figuras/figura_1.png …
figura_8.png con la numeración del artículo. Necesita Chromium (ruta en la
variable CHROME) y Pillow.

Los esquemas anteriores de las figuras 1 a 6 (analisis/esquemas/fig*.svg, con
la numeración de la serie original) se conservan, pero ya no se publican.

Si sustituyes una figura por la fotografía de su pastel, no vuelvas a correr
este script sobre ese número o sobrescribirá la fotografía (véase
figuras/LEEME.md).
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
ESQ = BASE.parent / "analisis" / "esquemas"
DIAG = ESQ / "diagramas"
OUT = BASE / "figuras"
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
# Escala de la captura. Las Figuras 7 y 8 salen a 3 (unos 380 ppp a su tamaño de impresión); las
# Figuras 1 a 6, con más masa y grano, a 2,5: de 1.400 a 2.100 px, más de 300 ppp, y pesan menos.
ESCALA = {7: 3, 8: 3}
# Notación (en analisis/esquemas/diagramas/) -> número de figura en el artículo.
DIAGRAMAS = [("fig1_craneo_nido.svg", 1), ("fig2_signo_mapa.svg", 2), ("fig3_apacheta.svg", 3),
             ("fig4_castillete.svg", 4), ("fig5_pelvis.svg", 5), ("fig6_centinela.svg", 6),
             ("fig7_memoria_retorno.svg", 7), ("fig8_tres_montones.svg", 8)]
# Las figuras 1 a 6 tienen masas de materia con grano (hollín, casiterita, noche): necesitan más tonos.
COLORES = {7: 64, 8: 64}


def main():
    OUT.mkdir(exist_ok=True)
    pedidas = {int(a) for a in sys.argv[1:]}
    with tempfile.TemporaryDirectory() as tmp:
        for origen, n in DIAGRAMAS:
            if pedidas and n not in pedidas:
                continue
            svg = (DIAG / origen).read_text(encoding="utf8")
            w, h = (int(float(v)) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()[2:])
            svg = svg.replace("<svg ", f'<svg width="{w}" height="{h}" ', 1)
            html = Path(tmp) / f"f{n}.html"
            html.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                            f"svg{{display:block}}</style>{svg}", encoding="utf8")
            captura = Path(tmp) / f"f{n}.png"
            escala = ESCALA.get(n, 2.5)
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            f"--force-device-scale-factor={escala}", f"--window-size={w + 40},{h + 200}",
                            "--virtual-time-budget=3000",
                            f"--screenshot={captura}", html.as_uri()], check=True, capture_output=True)
            im = Image.open(captura).convert("RGB").crop((0, 0, round(w * escala), round(h * escala)))
            destino = OUT / f"figura_{n}.png"
            # Dibujo de línea con pocos tonos: una paleta reducida basta y pesa mucho menos.
            im.quantize(colors=COLORES.get(n, 128), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
                destino, dpi=(300, 300), optimize=True)
            print(f"{origen} -> {destino.name}")


if __name__ == "__main__":
    main()
