"""P-11A · Las proporciones, sobre la lámina: el anexo de P-11, con capturas de las imágenes.

Uso (desde la raíz del repositorio):
    python3 tipografia/planos/proporciones_sobre_la_lamina.py RUTA/LAMINA_ENDEREZADA RUTA/PIE

LAMINA_ENDEREZADA es la lámina entera, enderezada: la imagen en la que se midió la retícula
(esquemas/celda_medida.json, 940 × 2000 px). PIE es el pie aparte, la imagen en la que se midió
la altura de x (esquemas/razon_medida.json).

Escribe en tipografia/planos/privado/ (SVG, PDF y PNG), que no entra en el repositorio: la foto
de la lámina no se sube, solo letras sueltas y medidas (07_posnansky.md, §3). Las capturas van en
gris; encima, en violeta, lo que midió la máquina. La lámina técnica, sin capturas, es P-11.
Necesita Chromium (ruta en la variable CHROME) para el PDF y el PNG.
"""

import base64
import io
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
PRIVADO = AQUI / "privado"
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(TIPO / "laminas"))

from dibujo import GRIS, GRIS2, PAPEL, SERIF, TINTA, VIOLETA, Hoja, coma, estilo, f  # noqa: E402

R = json.loads((TIPO / "esquemas" / "celda_medida.json").read_text(encoding="utf8"))
P = json.loads((TIPO / "esquemas" / "razon_medida.json").read_text(encoding="utf8"))

CABEZA = (60, 100, 480, 480)          # la cabeza de frente, en px de la lámina enderezada (donde se midió)
COSTADO = (560, 40, 940, 500)         # la cabeza de costado
PIE_LAMINA = (20, 1900, 925, 2000)    # el pie, en la lámina
ZOOM = (106, 58, 330, 100)            # «muy erosionado», en el pie aparte: astas de m, u, r, n y de la d


def incrustar(im, h, x, y, w, alto, capa="fondo", opacidad=1.0):
    """Una captura en la hoja: PNG en gris, incrustado en el SVG."""
    b = io.BytesIO()
    im.convert("L").save(b, "PNG", optimize=True)
    datos = base64.b64encode(b.getvalue()).decode("ascii")
    h.add(capa, f'<image x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(alto)}" preserveAspectRatio="none" '
                f'opacity="{f(opacidad)}" href="data:image/png;base64,{datos}"/>')


def rect(h, x, y, ancho, alto, tipo, capa="cotas", **extra):
    h.add(capa, f'<rect x="{f(x)}" y="{f(y)}" width="{f(ancho)}" height="{f(alto)}" {estilo(tipo, **extra)}/>')


def lineas_del_pie(g):
    """La banda de x en el recorte del pie: las filas donde la tinta pasa la mitad de su máximo."""
    k = 1 - np.asarray(g, np.float32) / 255
    perfil = k.mean(axis=1)
    alto = perfil > perfil.max() / 2
    runs, i = [], 0
    while i < len(alto):
        if alto[i]:
            j = i
            while j + 1 < len(alto) and alto[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    a, z = max(runs, key=lambda r: r[1] - r[0])
    return a - 0.5, z + 0.5                           # el borde y el fondo, a media oscuridad


def hoja(lamina, pie):
    h = Hoja("P-11A", "Las proporciones, sobre la lámina", "anexo de P-11: con capturas de las imágenes", "S/E",
             "A", "P-11", fecha="08.11.2026", unidades="px de cada imagen",
             pie=(("MIDIÓ", "la máquina, en dos imágenes de la lámina (esquemas/*_medida.json)"),
                  ("MUESTRA", "capturas de la lámina, en gris; las medidas, en violeta"),
                  ("NOTA", "no se sube al repositorio: la foto de la lámina no se sube (07, §3)")))
    W, H = lamina.size
    if (W, H) != (940, 2000):
        print(f"  ! la lámina mide {W} × {H} px y las medidas son de una de 940 × 2000: no van a caer en su lugar")

    # ---- 1. la cabeza de frente, con la retícula medida encima
    h.llamada(32, 22, 1, titulo="LA CABEZA DE FRENTE, MEDIDA", escala="la lámina enderezada · 1 px = 0,28 mm")
    k1, ox, oy = 0.28, 34.0, 36.0
    x0, y0, x1, y1 = CABEZA
    incrustar(lamina.crop(CABEZA), h, ox, oy, (x1 - x0) * k1, (y1 - y0) * k1)

    def C1(x, y):
        return (ox + (x - x0) * k1, oy + (y - y0) * k1)

    for x in R["centros_x"]:
        h.linea(C1(x, y0 + 8), C1(x, y1 - 8), "eje", "ejes", color=VIOLETA, w=0.15)
    for y in R["centros_y"]:
        h.linea(C1(x0 + 8, y), C1(x1 - 8, y), "eje", "ejes", color=VIOLETA, w=0.15)
    for q in R["huecos"]:
        a = C1(q["x"] - q["ancho"] / 2, q["y"] - q["alto"] / 2)
        rect(h, a[0], a[1], q["ancho"] * k1, q["alto"] * k1, "contorno", color=VIOLETA, w=0.25)
        h.punto(C1(q["x"], q["y"]), 0.32, VIOLETA)
    hw = R["hueco"]["ancho_sobre_paso"] * float(np.median(R["paso_x"]))
    hh = R["hueco"]["alto_sobre_paso"] * R["paso_y_mediana"]
    for q in R["sin_medir"]:
        x, y = R["centros_x"][q["columna"] - 1], R["centros_y"][q["fila"] - 1]
        a = C1(x - hw / 2, y - hh / 2)
        rect(h, a[0], a[1], hw * k1, hh * k1, "contorno_r", w=0.35)
    for j, x in enumerate(R["centros_x"]):
        p = C1(x, y0)
        h.circulo((p[0], oy - 4.2), 2.0, "filete", "textos")
        h.texto(p[0], oy - 3.5, str(j + 1), 2.0, "middle", peso=700)
    for j, r in enumerate(R["ancho_por_alto"]):
        xm = (C1(R["centros_x"][j], 0)[0] + C1(R["centros_x"][j + 1], 0)[0]) / 2
        h.texto(xm, oy + (y1 - y0) * k1 + 4.6, coma(r, 2), 2.1, "middle", peso=700 if j in (0, 3, 6) else 400,
                color=VIOLETA)
    yb = oy + (y1 - y0) * k1
    h.texto(ox, yb + 10.2, f"arriba, el ancho por alto de cada paso; la retícula entera: {coma(R['global'], 3)} ≈ "
                           f"{coma(R['celda'], 2)} (en la foto de cámara, {coma(R['antes']['global'], 3)})", 2.2)
    h.texto(ox, yb + 14.4, "en violeta, lo medido: los centros, los huecos y los ejes; a puntos, los dos sin medir",
            1.9, color=GRIS)

    # ---- 2. la lámina entera, y dónde está cada captura
    h.llamada(176, 22, 2, titulo="LA LÁMINA ENTERA", escala="enderezada · 1 px = 0,06 mm")
    k2, ox2, oy2 = 0.06, 178.0, 33.0
    incrustar(lamina, h, ox2, oy2, W * k2, H * k2)

    def C2(x, y):
        return (ox2 + x * k2, oy2 + y * k2)

    for (a, b, c, d), n in ((CABEZA, 1), (COSTADO, 3), (PIE_LAMINA, 4)):
        p, q = C2(a, b), C2(c, d)
        rect(h, p[0], p[1], q[0] - p[0], q[1] - p[1], "contorno", color=VIOLETA, w=0.3)
        h.circulo((q[0] + 3.2, p[1] + 2.4), 2.0, "filete", "textos", color=VIOLETA)
        h.texto(q[0] + 3.2, p[1] + 3.1, str(n), 2.0, "middle", peso=700, color=VIOLETA)
    xt = ox2 + W * k2 + 9
    for i, t in enumerate(("Posnansky, según el pie:", "de frente (izquierda)", "y de costado (derecha);",
                           "abajo, el pie.", "", "La lámina se enderezó", "para quitar la perspectiva",
                           "de la cámara: es la misma", "imagen, recta.")):
        h.texto(xt, oy2 + 4 + i * 3.6, t, 2.2, familia=SERIF, color=TINTA if i < 4 else GRIS)

    # ---- 3. la cabeza de costado
    h.llamada(176, 168, 3, titulo="LA CABEZA DE COSTADO", escala="1 px = 0,16 mm")
    k3, ox3, oy3 = 0.16, 178.0, 180.0
    a, b, c, d = COSTADO
    incrustar(lamina.crop(COSTADO), h, ox3, oy3, (c - a) * k3, (d - b) * k3)
    xt3 = ox3 + (c - a) * k3 + 4
    for i, t in enumerate(("De costado, la retícula", "no sigue: está solo en el", "frente. Ahí las columnas",
                           "se angostan hacia los", "bordes, como sobre un", "cilindro (P-11, vista 2).",
                           "La letra toma el dibujo", "de frente.")):
        h.texto(xt3, oy3 + 4 + i * 3.6, t, 2.2, familia=SERIF)

    # ---- 4. el pie, y una palabra ampliada con sus líneas
    h.llamada(32, 168, 4, titulo="EL PIE", escala="el pie aparte · 1 px = 0,07 mm; abajo, 1 px = 0,5 mm")
    k4, ox4, oy4 = 0.07, 34.0, 180.0
    incrustar(pie, h, ox4, oy4, pie.width * k4, pie.height * k4)
    a, b, c, d = ZOOM
    rect(h, ox4 + a * k4, oy4 + b * k4, (c - a) * k4, (d - b) * k4, "contorno", color=VIOLETA, w=0.3)
    k5, ox5, oy5 = 0.5, 46.0, 206.0
    recorte = pie.crop(ZOOM)
    incrustar(recorte, h, ox5, oy5, (c - a) * k5, (d - b) * k5)
    h.linea((ox4 + (a + c) / 2 * k4, oy4 + d * k4), (ox5 + (c - a) * k5 / 2, oy5), "aux", "cotas", color=VIOLETA)
    borde, fondo = lineas_del_pie(recorte)
    la = P["lamina_enderezada"]
    yf = oy5 + fondo * k5
    niveles = (("afuera", yf - la["ascendente"] * k5), ("borde", yf - la["alto_x"] * k5), ("fondo", yf),
               ("desagüe", yf + la["descendente"] * k5))
    xa, xb = ox5 - 2, ox5 + (c - a) * k5 + 2
    for nombre, y in niveles:
        h.linea((xa, y), (xb, y), "linea", "cotas", color=VIOLETA, w=0.3)
        h.texto(xa - 1.2, y + 0.8, nombre, 2.0, "end", color=VIOLETA)
    xc = xb + 3
    h.cota((xc, yf), (xc, niveles[1][1]), -3, coma(la["alto_x"]), tam=1.9, color=VIOLETA)
    h.cota((xc, yf), (xc, niveles[0][1]), -8, coma(la["ascendente"]), tam=1.9, color=VIOLETA)
    h.cota((xc, niveles[3][1]), (xc, yf), -3, coma(la["descendente"]), tam=1.9, color=VIOLETA)
    yl = oy5 + (d - b) * k5 + 8
    h.texto(ox5, yl, "«muy erosionado»: las astas de m, u, r y n dan la x; la de la d, la ascendente.", 1.9, color=GRIS)
    h.texto(ox5, yl + 3.4, f"Las líneas son las medianas de {la['astas']['x']} astas de x y "
                           f"{la['astas']['ascendentes']} ascendentes de todo el pie.", 1.9, color=GRIS)
    h.texto(ox5, yl + 8.6, f"ascendentes / x: {coma(la['razon'], 2)} en esta imagen · "
                           f"{coma(P['foto_de_camara']['razon'], 2)} en la foto de cámara · la razón queda en "
                           f"{coma(P['razon'], 2)}", 2.2)
    h.gravedad(40, 262, 3.6)

    # ---- la columna
    h.columna([
        ("titulo", "Qué se ve"),
        ("p", "**Las imágenes en que se midieron las proporciones de _Contenida_**, con las medidas encima. Es el "
              "anexo de P-11: allí las mismas medidas están redibujadas, sin las imágenes."),
        ("titulo", "Cómo se lee"),
        ("p", "En gris, las capturas de las dos imágenes, sin retocar. En violeta, lo que midió la máquina: los centros "
              "y los huecos de la retícula, sus ejes, las cuatro líneas del pie y sus cotas, en píxeles de cada imagen. "
              "Los números en círculo dicen dónde está cada vista en la lámina entera."),
        ("titulo", "La celda"),
        ("p", "En la cabeza de frente, cada hueco de la retícula (el rectángulo de adentro) da su centro. Los "
              "centros se agrupan en ocho columnas y siete filas. El paso de cada columna, sobre el de las filas, "
              f"da su ancho por alto: {coma(min(R['ancho_por_alto']), 2)} en los bordes y "
              f"{coma(max(R['ancho_por_alto']), 2)} al centro. La retícula entera mide {coma(R['celda'], 2)}: es la "
              "celda de la letra."),
        ("titulo", "La altura de x"),
        ("p", "En el pie, cada asta se corta a la mitad de su oscuridad. Las de n, m, u y r dan la altura de x; las "
              "de l, d, b, h y k, la de las ascendentes. En esta imagen las ascendentes miden "
              f"{coma(P['lamina_enderezada']['razon'], 2)} veces la x; en la foto de cámara, "
              f"{coma(P['foto_de_camara']['razon'], 2)}. La diferencia es menor que el paso de la medida: la razón "
              f"queda en {coma(P['razon'], 2)}."),
        ("titulo", "Lo que no se sube"),
        ("p", "La foto de la lámina no entra en el repositorio, que es público: solo las letras sueltas y las medidas "
              "(07, §3). Esta lámina se arma con proporciones_sobre_la_lamina.py, desde las imágenes, y queda en "
              "planos/privado/, fuera del repositorio. La lámina es de Posnansky, según el pie; el libro del que sale "
              "no está identificado."),
    ])
    h.marco()
    return h


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lamina = Image.open(sys.argv[1]).convert("L")
    pie = Image.open(sys.argv[2]).convert("L")
    PRIVADO.mkdir(exist_ok=True)
    h = hoja(lamina, pie)
    svg = h.svg("../../laminas/fuentes")
    (PRIVADO / "P-11A_proporciones_sobre_la_lamina.svg").write_text(svg, encoding="utf8")
    from generar_planos import imprimir
    pdf = PRIVADO / "P-11A_proporciones_sobre_la_lamina.pdf"
    imprimir([h.svg("../laminas/fuentes")], pdf)
    import fitz
    doc = fitz.open(pdf)
    doc[0].get_pixmap(dpi=150).save(PRIVADO / "P-11A_proporciones_sobre_la_lamina.png")
    doc.close()
    print("listo:", pdf, "(fuera del repositorio)")


if __name__ == "__main__":
    main()
