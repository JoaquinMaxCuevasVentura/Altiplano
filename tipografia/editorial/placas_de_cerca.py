#!/usr/bin/env python3
"""Las placas de la simulación, de cerca, para el libro: la «a» (celda 8), la «z» (celda 32) y el signo final.

En las láminas de la simulación cada placa mide unos 190 px; acá se hacen a su resolución de trabajo
(600 px para 150 mm, 4 px por milímetro) con el mismo azar, la misma mano y el mismo minuto de la
sesión que anotan sus fichas, para que sean las mismas placas. Siguen siendo la propuesta de la máquina.

Uso (desde la raíz del repositorio; tarda medio minuto):
    python3 tipografia/editorial/placas_de_cerca.py
Escribe tipografia/editorial/imagenes/placa_CC_anverso.png y placa_CC_reverso.png: la hoja de aluminio sola,
con el fondo transparente, para que quede sobre el papel del libro como un objeto.
"""

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SIMULACION = AQUI.parent / "simulacion"
sys.path.insert(0, str(SIMULACION))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from comun import POR_SIGNO, T, azar  # noqa: E402
from contener import foto_placa, repujar_placa, reverso, signo_final  # noqa: E402
from desenterrar import calco, desenterrar, frotado, pared  # noqa: E402
from gramatica import celda  # noqa: E402
from pulso import Mano  # noqa: E402

SALIDA = AQUI / "imagenes"
FICHAS = json.loads((SIMULACION / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))


def objeto(foto, mascara, ruta):
    """La foto de la placa con su recorte: lo que no es aluminio queda transparente, con el borde suavizado."""
    gris = (np.clip(foto, 0, 1) * 255 + 0.5).astype(np.uint8)
    alfa = cv2.GaussianBlur(mascara.astype(np.float32), (0, 0), 0.8)
    alfa = (np.clip(alfa, 0, 1) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(np.dstack([gris, gris, gris, alfa]), "RGBA").save(ruta, optimize=True)


def main(signos=("a", "z", "¶")):
    SALIDA.mkdir(exist_ok=True)
    D = desenterrar()
    e = D["esqueleto"]
    P = pared(7, 8, 300, azar("pared"))                   # como en simular.py: la pared, su frotado y el fondo de cada celda
    F = frotado(P, azar("frotado"))
    j, px = P["junta"], P["px"]
    pauta = dict(celda=celda(e), fondo=e["fondo"], borde=e["borde"])
    for s in signos:
        c = POR_SIGNO[s]
        n = c["celda"]
        f = FICHAS[f"{n:02d}.01"]
        if c["estado"] == "manos":
            p = signo_final(azar("signo", 1))
        else:
            x = j + (c["columna"] - 1) * (px + j)
            y = j + (c["fila"] - 1) * (px + j)
            fondo = cv2.resize(F[y:y + px, x:x + px], (T, T), interpolation=cv2.INTER_LINEAR)
            cuerpo = D["gramatica"][s]
            _, trazos = calco(cuerpo["geo"], c["estado"] == "reconstruida", fondo, pauta, azar("calco", n),
                              Mano("calcar", "derecha", f["calco"]["minuto"]))
            p = repujar_placa(trazos, c["estado"] == "reconstruida", n, 1, minuto=f["pulso"]["minuto"])
        r = reverso(p)
        objeto(foto_placa(p, azar("foto", n, 1)), p["mascara"], SALIDA / f"placa_{n:02d}_anverso.png")
        objeto(foto_placa(r, azar("foto reverso", n)), r["mascara"], SALIDA / f"placa_{n:02d}_reverso.png")
        print("listo:", s, n)


if __name__ == "__main__":
    main()
