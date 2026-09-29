"""Imágenes de las láminas de exposición.

Uso (desde la raíz del repositorio, después de simular.py):
    python3 tipografia/laminas/imagenes.py

Rehace con la misma semilla de la simulación, y a más resolución, las pocas
imágenes que las láminas muestran grandes: la palabra «contenida» pasando por
el agua (portada) y la «a» en el agua quieta, tocada y con voz. El resto son
recortes de las láminas de simulacion/salida/ y esquemas/.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
sys.path.insert(0, str(TIPO / "simulacion"))

from comun import CELDAS, SALIDA, T, a8, a_rgb, azar, poliza  # noqa: E402
from contener import repujar_placa, sesiones_de_vestir, vestir  # noqa: E402
from desenterrar import calco, desenterrar, frotado, pared  # noqa: E402
from devolver import agua, foto_agua, voz_del_verso  # noqa: E402

IMG = AQUI / "img"
ESQ = TIPO / "esquemas"


def guardar(nombre, img, calidad=90):
    im = Image.fromarray(a8(a_rgb(img)) if img.dtype != np.uint8 else img)
    ruta = IMG / nombre
    if ruta.suffix == ".jpg":
        im.convert("RGB").save(ruta, quality=calidad)
    else:
        im.save(ruta)


def celda_de(signo):
    return next(c for c in CELDAS if c["signo"] == signo)


def placas_vestidas(D, signos):
    """Repite la simulación (misma semilla) solo para las placas que se piden: [(signo, variante)]."""
    pol = poliza()
    P = pared(7, 8, 300, azar("pared"))
    F = frotado(P, azar("frotado"))
    j, px = P["junta"], P["px"]
    claves = [(c["celda"], v) for c in CELDAS for v in range(1, pol[c["signo"]] + 1)]
    sesiones = sesiones_de_vestir(claves)
    salida = {}
    for s, v in signos:
        c = celda_de(s)
        celda = c["celda"]
        x = j + (c["columna"] - 1) * (px + j)
        y = j + (c["fila"] - 1) * (px + j)
        fondo = cv2.resize(F[y:y + px, x:x + px], (T, T), interpolation=cv2.INTER_LINEAR)
        m = D["M"][s] if c["estado"] == "hallada" else D["R"][s]
        _, trazos = calco(m, c["estado"] == "reconstruida", fondo, D["med"], azar("calco", celda))
        p = repujar_placa(trazos, c["estado"] == "reconstruida", celda, v)
        parte, ang, minutos, _ = sesiones[(celda, v)]
        vs = vestir(p, parte, ang, minutos, azar("vestir", celda, v))
        salida[(s, v)] = dict(vs, relieve=vs["relieve"].astype(np.float32), pliegues=vs["pliegues"].astype(np.float32))
    return salida


def portada(vs, palabra="contenida", ancho=560, alto=448):
    """El nombre pasando por el agua quieta: cada letra es otra placa, llega al revés y en trapecio."""
    fotos, vistas = [], {}
    for ch in palabra:
        vistas[ch] = vistas.get(ch, 0) + 1
        celda = celda_de(ch)["celda"]
        v = vistas[ch]
        clave = (celda,) if v == 1 else (celda, v)   # la primera placa, con el azar de simular.py
        lq, _ = agua(vs[(ch, v)], azar("agua", *clave))
        fotos.append(foto_agua(lq, azar("foto agua", *clave), ancho=ancho, alto=alto))
    junta = np.full((alto, 10, 3), 0.02, np.float32)
    fila = []
    for f in fotos:
        fila += [f, junta]
    guardar("portada_contenida.jpg", np.hstack(fila[:-1]))


def la_a_en_el_agua(vs):
    """La «a» (celda 8) en el agua quieta, tocada y con voz, a 700 × 560 px."""
    c = celda_de("a")
    celda, v = c["celda"], vs[("a", 1)]
    lq, _ = agua(v, azar("agua", celda))
    guardar("a_quieta.jpg", foto_agua(lq, azar("foto agua", celda)))
    fase = 1.5 + (celda % 5) * 0.5
    lt, _ = agua(v, azar("tocada", celda), fase=fase)
    guardar("a_tocada.jpg", foto_agua(lt, azar("foto tocada", celda)))
    from comun import VERSOS
    verso = VERSOS[(celda - 1) * len(VERSOS) // len(CELDAS)]
    hz, vol, _, _ = voz_del_verso(verso, azar("voz", celda))
    lv, _ = agua(v, azar("agua voz", celda), voz=(hz, vol))
    guardar("a_voz.jpg", foto_agua(lv, azar("foto voz", celda)))


def signo_final_grande():
    """La celda 56 a 600 × 600 px: la presión de pulgar, con el mismo azar que simular.py."""
    from contener import foto_placa, signo_final
    p = signo_final(azar("signo", 1))
    guardar("celda_56.jpg", foto_placa(p, azar("foto", 56, 1)))


# ---------------------------------------------------------------- recortes

def abrir(ruta):
    return Image.open(ruta).convert("RGB")


def reticula_de_lamina(im, lado=190, j=6, mx=48, arriba=118):
    """La retícula entera de una lámina de 8 × 7, sin el título, con su junta."""
    return im.crop((mx - j, arriba - j, mx + 8 * lado + 7 * j + j, arriba + 7 * lado + 6 * j + j))


def sin_titulo(im, arriba):
    return im.crop((0, arriba, im.width, im.height))


def recortes():
    S = SALIDA
    for nombre in ("03_calco.png", "04_placa.jpg", "06_piel.jpg", "07_cinta.jpg", "11_azulejo.png",
                   "21_gramatica_caja.png"):
        im = abrir(S / nombre)
        base = Path(nombre).stem
        reticula_de_lamina(im).save(IMG / f"{base}_reticula.jpg", quality=90)
    for nombre in ("01_frotado_de_la_pared.jpg", "05_caja_abierta.jpg", "11b_estrofa_en_la_pared.jpg", "03b_notdef.png"):
        abrir(S / nombre).save(IMG / (Path(nombre).stem + ".jpg"), quality=90)
    # las láminas con título de la simulación, sin el título (el título lo pone la lámina de exposición)
    sin_titulo(abrir(S / "08_hectografo_copias.jpg"), 58).save(IMG / "08_hectografo_copias.jpg", quality=90)
    sin_titulo(abrir(S / "04b_placas_rotas.jpg"), 58).save(IMG / "04b_placas_rotas.jpg", quality=90)
    for n in ("08", "32"):
        sin_titulo(abrir(S / f"12_cadena_{n}.jpg"), 58).save(IMG / f"12_cadena_{n}.jpg", quality=90)
    # los cuatro generadores: testigo, curvas, cuerpo y calco (sin la cinta, que tiene su lámina)
    g = abrir(S / "20_gramatica.png")
    g.crop((0, 110, 40 + 4 * 440 + 3 * 16 + 10, g.height)).save(IMG / "20_gramatica_generadores.jpg", quality=90)
    # los esquemas, sin el título (lo pone la lámina)
    caja = abrir(ESQ / "caja_8x7.png")
    caja.crop((80, 235, caja.width - 80, caja.height)).save(IMG / "caja_8x7.png")
    cadena = abrir(ESQ / "cadena_de_estados.png")
    cadena.crop((0, 165, cadena.width, cadena.height)).save(IMG / "cadena_de_estados.png")
    abrir(ESQ / "pauta_azulejo.png").save(IMG / "pauta_azulejo.png")
    ad = abrir(S / "03d_antes_y_despues.png")
    ad.crop((0, 80, ad.width, ad.height)).save(IMG / "03d_antes_y_despues.jpg", quality=90)
    cerrada = abrir(S / "05b_caja_cerrada.jpg")
    cerrada.crop((0, 0, 560, 490)).save(IMG / "05b_puerta.jpg", quality=90)


if __name__ == "__main__":
    IMG.mkdir(exist_ok=True)
    recortes()
    D = desenterrar()
    datos = {k: round(float(D["med"][k]), 1) for k in ("canal", "asc", "xh", "desc")}
    (IMG / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf8")
    signo_final_grande()
    vs = placas_vestidas(D, [("c", 1), ("o", 1), ("n", 1), ("t", 1), ("e", 1), ("n", 2), ("i", 1), ("d", 1), ("a", 1)])
    portada(vs)
    la_a_en_el_agua(vs)
    print("listo:", len(list(IMG.iterdir())), "imágenes en", IMG)
