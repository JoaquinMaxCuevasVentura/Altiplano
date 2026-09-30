"""Genera las láminas de Contenida: esquemas SVG, vistas PNG y un PDF de plantillas imprimibles.

Uso (desde la raíz del repositorio, después de tipografia/inventario.py):
    python3 tipografia/esquemas/generar_esquemas.py [--azulejo 150] [--teselas 6] [--junta 3]

Mide el azulejo de la pared de la piscina, las teselas del piso y la junta, y
vuelve a correr el script con esas medidas (en milímetros): la pauta de calco
se imprime a escala 1:1.

Escribe en tipografia/esquemas/:
  caja_8x7.svg          la caja: qué signo va en cada celda
  pauta_azulejo.svg     la pauta de calco, un azulejo a escala 1:1 (A4)
  ficha_de_hallazgo.svg dos fichas por hoja (A4)
  cadena_de_estados.svg la familia como cadena de estados
  montajes_con_agua.svg agua, voz, pliego de agua y frotado
  *.png                 vistas de los esquemas
  plantillas_imprimibles.pdf  pauta, fichas y caja, para imprimir al 100 %

Ninguna lámina dibuja letras: las letras las hace la mano (véase 03_sistema_contenida.md).
Necesita Chromium (ruta en la variable CHROME) y Pillow para las vistas y el PDF.
"""

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
MONO = "'Courier New', Courier, 'Liberation Mono', monospace"

# Paleta de la obra: el aluminio, la piel, la luz verde (solo luz, nunca tinta),
# el líquido negro, el azulejo, la junta y la tinta hectográfica.
PLATA, PLATA_OSC = "#b8bcc0", "#7d8388"
PIEL = "#c89f82"
VERDE = "#39c97e"
NEGRO = "#161616"
AZULEJO, JUNTA = "#f3f2ec", "#a4a39b"
VIOLETA = "#4a2470"
TEXTO, GRIS = "#1f1f1f", "#6d6d6d"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, tam, color=TEXTO, anchor="start", peso="normal", extra=""):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{tam}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{peso}" {extra}>{esc(s)}</text>')


# ---------------------------------------------------------------- la caja

def caja(datos):
    col, fil = datos["columnas"], datos["filas"]
    lado, junta, mx, arriba = 92, 6, 60, 132
    ancho = mx * 2 + col * lado + (col - 1) * junta
    alto_grilla = fil * lado + (fil - 1) * junta
    alto = arriba + alto_grilla + 300
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" font-family="{MONO}">',
         f'<rect width="{ancho}" height="{alto}" fill="#ffffff"/>',
         t(mx, 42, "La caja · 8 × 7 = 56 celdas", 24, peso="bold"),
         t(mx, 68, "La retícula de la cabeza en la lámina: 8 columnas × 7 filas visibles.", 13, GRIS),
         t(mx, 86, "Orden: hallados por orden de aparición en el pie; reconstruidos por orden", 13, GRIS),
         t(mx, 104, "de necesidad en el poema; al final, el signo hecho con las manos.", 13, GRIS),
         f'<rect x="{mx - junta}" y="{arriba - junta}" width="{ancho - 2 * mx + 2 * junta}" '
         f'height="{alto_grilla + 2 * junta}" fill="{JUNTA}"/>']
    for c in datos["celdas"]:
        x = mx + (c["columna"] - 1) * (lado + junta)
        y = arriba + (c["fila"] - 1) * (lado + junta)
        o.append(f'<rect x="{x}" y="{y}" width="{lado}" height="{lado}" fill="{AZULEJO}"/>')
        m = 9
        if c["estado"] == "hallada":
            trazo, color = f'stroke="{TEXTO}" stroke-width="1.4"', TEXTO
        elif c["estado"] == "reconstruida":
            trazo, color = f'stroke="{GRIS}" stroke-width="1.4" stroke-dasharray="4 3"', GRIS
        else:
            trazo, color = f'stroke="{PIEL}" stroke-width="2.2"', PIEL
        o.append(f'<rect x="{x + m}" y="{y + m}" width="{lado - 2 * m}" height="{lado - 2 * m}" fill="none" {trazo}/>')
        o.append(t(x + lado / 2, y + lado / 2 + 13, c["signo"], 36, color, "middle"))
        o.append(t(x + 13, y + 22, str(c["celda"]), 9, GRIS))
        nota = {"hallada": f'×{c.get("testigos", "")}', "reconstruida": "rec.", "manos": "manos"}[c["estado"]]
        o.append(t(x + lado - 13, y + lado - 14, nota, 9, GRIS, "end"))
    y0 = arriba + alto_grilla + 44
    # leyenda
    ley = [("hallada", f'stroke="{TEXTO}" stroke-width="1.4"', "hallado en el pie (×n: testigos)"),
           ("reconstruida", f'stroke="{GRIS}" stroke-width="1.4" stroke-dasharray="4 3"', "reconstruido: hipótesis, siempre punteado"),
           ("manos", f'stroke="{PIEL}" stroke-width="2.2"', "¶ signo final, hecho con los dedos")]
    for i, (_, trazo, texto) in enumerate(ley):
        yy = y0 + i * 26
        o.append(f'<rect x="{mx}" y="{yy - 14}" width="18" height="18" fill="{AZULEJO}" {trazo}/>')
        o.append(t(mx + 30, yy, texto, 13))
    # fuera de la caja: la celda vacía de la lámina es el .notdef
    fx, fy = mx, y0 + 96
    o.append(t(fx, fy, "Fuera de la caja", 15, peso="bold"))
    cw, ch = 44, 56  # la celda de la lámina es algo más alta que ancha
    cx, cy = fx, fy + 16
    o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="none" stroke="{TEXTO}" stroke-width="1.4"/>')
    o.append(f'<rect x="{cx + 8}" y="{cy + 9}" width="{cw - 16}" height="{ch - 18}" fill="none" stroke="{TEXTO}" stroke-width="1.4"/>')
    o.append(t(cx + cw + 18, cy + 18, ".notdef = la celda vacía de la lámina, calcada a mano.", 13))
    o.append(t(cx + cw + 18, cy + 38, "Lo que no cabe en la caja se ve así:", 13))
    for i, linea in enumerate(datos["celda_vacia"].split(" · ")):
        o.append(t(cx + cw + 18, cy + 60 + i * 19, "· " + linea, 12, GRIS))
    o.append(t(cx + cw + 18, cy + 128, datos["sin_celda"], 13))
    o.append("</svg>")
    return "\n".join(o), ancho, alto


# ---------------------------------------------------------------- pauta de calco (mm, A4)

def pauta(azulejo, teselas, junta):
    """La pauta de calco: la placa, la celda de la cabeza del ídolo (0,84) y las cuatro líneas del pie.

    Las líneas salen de la gramática (simulacion/salida/gramatica/gramatica.json) si existe;
    si no, de la pauta provisional. La placa mide lo que el azulejo: 150 mm hasta medir.
    """
    W, H = 210, 297
    x0, y0 = (W - azulejo) / 2, 34
    k = azulejo / 600                                   # la simulación trabaja en 600 px por placa
    ruta = Path(__file__).resolve().parent.parent / "simulacion" / "salida" / "gramatica" / "gramatica.json"
    if ruta.exists():
        e = json.loads(ruta.read_text(encoding="utf8"))["esqueleto"]
        lineas = [(e["desague"] * k, "desagüe"), (e["fondo"] * k, "fondo"), (e["borde"] * k, "borde"),
                  (e["afuera"] * k, "afuera")]
        alto = (e["desague"] - e["afuera"]) * 1.1 * k
        cy = (e["desague"] + e["afuera"]) / 2 * k
        origen = "del pie (testigo sustituto)"
    else:
        tes = azulejo / 6
        lineas = [(azulejo - v * tes, n) for v, n in ((0.5, "desagüe"), (1.5, "fondo"), (4.0, "borde"), (5.5, "afuera"))]
        alto, cy = azulejo * 0.92, azulejo / 2
        origen = "provisional"
    ancho = 0.84 * alto
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" font-family="{MONO}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         t(x0, 14, "Contenida · pauta de calco", 5.2, peso="bold"),
         t(x0, 21, f"1 placa = {azulejo:g} mm = 1 letra · la celda: 0,84 de ancho por alto · líneas: {origen}", 3.1, GRIS),
         t(x0, 26.5, "Imprimir al 100 %. Comprobar la barra de 100 mm.", 3.1, GRIS),
         f'<rect x="{x0}" y="{y0}" width="{azulejo}" height="{azulejo}" fill="#ffffff" stroke="{JUNTA}" stroke-width="0.3"/>',
         f'<rect x="{x0 + (azulejo - ancho) / 2:.2f}" y="{y0 + cy - alto / 2:.2f}" width="{ancho:.2f}" height="{alto:.2f}" '
         f'fill="none" stroke="{JUNTA}" stroke-width="0.6"/>']
    for y, nombre in lineas:
        yy = y0 + y
        grosor = "0.5" if nombre.startswith(("fondo", "borde")) else "0.3"
        o.append(f'<line x1="{x0}" y1="{yy:.2f}" x2="{x0 + azulejo}" y2="{yy:.2f}" stroke="{TEXTO}" stroke-width="{grosor}" stroke-dasharray="2 1.2"/>')
        o.append(t(x0 + azulejo + 2, yy + 1.1, nombre, 2.8, GRIS))
    o.append(t(x0 + azulejo + 2, y0 + cy - alto / 2 - 1, "celda", 2.6, GRIS))
    # campos
    yc = y0 + azulejo + 11
    campos = ["Celda nº ______   Signo ______   [ ] hallado   [ ] reconstruido",
              "Hallado en (palabra y línea del pie): ______________________________",
              "Reconstruido con las partes de: ____________________________________",
              "Generación de ampliación: ______   Mano: ___________________________",
              "Fecha: ____________   Intentos: ______   Roturas: ______",
              "Notas: _____________________________________________________________",
              "____________________________________________________________________"]
    for i, c in enumerate(campos):
        o.append(t(x0, yc + i * 8.2, c, 3.2))
    # barra de control de escala
    yb = H - 26
    o.append(f'<line x1="{x0}" y1="{yb}" x2="{x0 + 100}" y2="{yb}" stroke="{TEXTO}" stroke-width="0.5"/>')
    for i in range(11):
        alto = 3 if i % 5 == 0 else 1.6
        o.append(f'<line x1="{x0 + i * 10}" y1="{yb}" x2="{x0 + i * 10}" y2="{yb - alto}" stroke="{TEXTO}" stroke-width="0.35"/>')
    o.append(t(x0 + 104, yb, "100 mm", 3, GRIS))
    o.append(t(x0, H - 21, "desagüe = descendentes · fondo = base · borde = altura de x · afuera = ascendentes", 3, GRIS))
    o.append(t(x0, H - 16, "Dibujar al derecho, con línea continua lo hallado y punteada lo reconstruido.", 3, GRIS))
    o.append(t(x0, H - 11, "Para repujar: dar vuelta el calco (espejo) y repasarlo por el reverso de la placa.", 3, GRIS))
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- ficha de hallazgo (mm, A4, dos por hoja)

def ficha():
    W, H = 210, 297
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" font-family="{MONO}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    filas = [("Pie", "palabra _______ línea __ testigo __ de __"),
             ("Reconstrucción", "por analogía con ______________________"),
             ("Calco", "mano ______________ fecha ________"),
             ("Placa", "mano ______ fecha ______ intentos __ roturas __"),
             ("Cinta", "tramos __ pliegues __   foto nº ______"),
             ("Frotado", "papel ______ frotadas legibles __ última __"),
             ("Agua", "[ ] quieta  [ ] tocada   foto nº ______"),
             ("Voz", "verso leído ____________   foto nº ______"),
             ("Notas", "_______________________________________")]
    for k in range(2):
        oy = k * H / 2
        o.append(f'<rect x="8" y="{oy + 8}" width="{W - 16}" height="{H / 2 - 16}" fill="none" stroke="{JUNTA}" stroke-width="0.4"/>')
        o.append(t(16, oy + 19, "Ficha de hallazgo · Contenida", 4.4, peso="bold"))
        o.append(t(16, oy + 25, "Una por signo. Acompaña a la placa en su celda.", 2.9, GRIS))
        # recuadro para el signo y la celda
        o.append(f'<rect x="{W - 62}" y="{oy + 14}" width="46" height="46" fill="{AZULEJO}" stroke="{JUNTA}" stroke-width="0.4"/>')
        o.append(t(W - 39, oy + 65, "signo (dibujo)", 2.6, GRIS, "middle"))
        o.append(t(W - 62, oy + 72, "celda nº ____", 3.1))
        o.append(t(16, oy + 34, "[ ] hallado   [ ] reconstruido   [ ] signo final", 3.2))
        for i, (a, b) in enumerate(filas):
            y = oy + 44 + i * 8.8
            o.append(t(16, y, a, 3.3, peso="bold"))
            o.append(t(46, y, b, 3.1))
            o.append(f'<line x1="16" y1="{y + 2.6}" x2="{W - 70 if i < 3 else W - 16}" y2="{y + 2.6}" stroke="{AZULEJO}" stroke-width="0.3"/>')
    o.append(f'<line x1="0" y1="{H / 2}" x2="{W}" y2="{H / 2}" stroke="{JUNTA}" stroke-width="0.3" stroke-dasharray="2 2"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- cadena de estados

ESTADOS = [
    # nombre, verbo, material (| corta la línea), verso, pierde, gana
    ("Pie", "hallar y|medir", "el libro", "«le pusieron nombre»", "—", "las medidas del archivo"),
    ("Calco", "calcar la|gramática", "calco|lápiz", "«solo la opinión sobre ella»", "la tinta del libro", "el cuerpo base"),
    ("Placa", "repujar", "aluminio|punzón", "«un signo hecho con las manos»", "la línea", "relieve y reflejo"),
    ("Cinta", "tapar", "masking|hueso claro", "«a la boca la taparon»", "la curva y la gota", "el pliegue"),
    ("Frotado", "frotar la|placa", "papel|grafito", "«todos los archivos funcionan así»", "relieve en cada frotada",
     "la vuelta al papel"),
    ("Agua", "reflejar", "bandeja|un dedo de agua", "«tocas el agua»", "el papel", "temblor y luz"),
    ("Voz", "hacer vibrar", "parlante|bajo la bandeja", "«pocas veces vuelve hablado»", "la palabra", "la vibración"),
    ("Digital", "si cierra", "escáner|software libre", "«termina y empieza»", "el cuerpo", "circulación"),
]


def cadena():
    n = len(ESTADOS)
    lado, paso, x0, y0 = 140, 172, 40, 150
    W, H = x0 * 2 + (n - 1) * paso + lado, 580
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{MONO}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<defs><linearGradient id="ml" x1="0" x2="1"><stop offset="0" stop-color="#4b4b4b"/>'
         f'<stop offset="0.55" stop-color="{PLATA}"/><stop offset="1" stop-color="{VERDE}"/></linearGradient>'
         '<marker id="fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{GRIS}"/></marker>'
         '<marker id="fv" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{VERDE}"/></marker></defs>',
         t(x0, 40, "La familia es una cadena de estados", 24, peso="bold"),
         t(x0, 66, "Cada estado sale del anterior por una operación física. No hay Regular: ninguno es la cara neutra.", 13, GRIS),
         f'<rect x="{x0}" y="92" width="{(n - 2) * paso + lado}" height="12" fill="url(#ml)"/>',
         t(x0, 124, "materia", 12, GRIS),
         t(x0 + (n - 2) * paso + lado, 124, "luz", 12, GRIS, "end")]
    for i, (nombre, verbo, material, verso, pierde, gana) in enumerate(ESTADOS):
        x = x0 + i * paso
        digital = nombre == "Digital"
        fondo = "#ffffff" if i == 0 or digital else AZULEJO
        borde = (f'stroke="{GRIS}" stroke-width="2" stroke-dasharray="6 4"' if digital
                 else f'stroke="{JUNTA}" stroke-width="3"')
        o.append(f'<rect x="{x}" y="{y0}" width="{lado}" height="{lado}" fill="{fondo}" {borde}/>')
        o.append(t(x + lado / 2, y0 + 40, nombre, 20, peso="bold", anchor="middle"))
        for j, parte in enumerate(verbo.split("|")):
            o.append(t(x + lado / 2, y0 + 62 + j * 14, parte, 11, GRIS, "middle"))
        for j, parte in enumerate(material.split("|")):
            o.append(t(x + lado / 2, y0 + 100 + j * 15, parte, 11, TEXTO, "middle"))
        if i < n - 1:
            raya = ' stroke-dasharray="5 4"' if ESTADOS[i + 1][0] == "Digital" else ""
            o.append(f'<line x1="{x + lado + 4}" y1="{y0 + lado / 2}" x2="{x + paso - 4}" y2="{y0 + lado / 2}" '
                     f'stroke="{GRIS}" stroke-width="1.5"{raya} marker-end="url(#fl)"/>')
        yv = y0 + lado + 30
        palabras = verso.split(" ")
        mitad = (len(palabras) + 1) // 2
        o.append(t(x, yv, " ".join(palabras[:mitad]), 11, VIOLETA))
        o.append(t(x, yv + 15, " ".join(palabras[mitad:]), 11, VIOLETA))
        o.append(t(x, yv + 44, "pierde:", 10, GRIS))
        o.append(t(x, yv + 58, pierde, 10))
        o.append(t(x, yv + 80, "gana:", 10, GRIS))
        o.append(t(x, yv + 94, gana, 10))
    # la vuelta: de lo digital a la placa
    xd = x0 + (n - 1) * paso + lado / 2
    xp = x0 + 2 * paso + lado / 2
    yb = y0 + lado + 140
    o.append(f'<path d="M{xd},{yb} C{xd},{yb + 110} {xp},{yb + 110} {xp},{yb}" '
             f'fill="none" stroke="{VERDE}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#fv)"/>')
    o.append(t((xd + xp) / 2, yb + 104, "vuelve: se proyecta a través del agua y se imprime como esténcil para placas nuevas", 12, TEXTO, "middle"))
    o.append("</svg>")
    return "\n".join(o), W, H


# ---------------------------------------------------------------- montajes con agua

def pared(x, y, w, h, lado=26):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{AZULEJO}" stroke="{JUNTA}" stroke-width="1.2"/>']
    for i in range(1, int(h // lado) + 1):
        o.append(f'<line x1="{x}" y1="{y + i * lado}" x2="{x + w}" y2="{y + i * lado}" stroke="{JUNTA}" stroke-width="0.8"/>')
    return o


def bandeja(x, y, w, agua=True):
    o = [f'<path d="M{x},{y} L{x + 8},{y + 26} L{x + w - 8},{y + 26} L{x + w},{y}" fill="none" stroke="{NEGRO}" stroke-width="2"/>']
    if agua:
        o.append(f'<path d="M{x + 3},{y + 8} L{x + 8},{y + 25} L{x + w - 8},{y + 25} L{x + w - 3},{y + 8} Z" fill="#cfe9ef" opacity="0.9"/>')
    return o


def montajes():
    W, H = 1200, 860
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{MONO}">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<defs><marker id="fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{VERDE}"/></marker></defs>',
         t(40, 40, "Montajes con agua", 24, peso="bold"),
         t(40, 64, "Nada con enchufe sobre el agua ni al lado de la bandeja: lámpara y parlante a pilas.", 13, GRIS)]
    paneles = [(40, 90), (620, 90), (40, 470), (620, 470)]
    pw, ph = 540, 350
    for (px, py) in paneles:
        o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="{AZULEJO}" stroke-width="2"/>')

    # A · Agua
    px, py = paneles[0]
    o.append(t(px + 16, py + 28, "A · Agua", 16, peso="bold"))
    o += pared(px + 440, py + 60, 70, 240)
    o += bandeja(px + 180, py + 250, 170)
    o.append(f'<line x1="{px + 200}" y1="{py + 272}" x2="{px + 330}" y2="{py + 272}" stroke="{PLATA_OSC}" stroke-width="4"/>')
    o.append(f'<rect x="{px + 40}" y="{py + 120}" width="46" height="26" rx="4" fill="{NEGRO}"/>')
    o.append(f'<line x1="{px + 86}" y1="{py + 136}" x2="{px + 262}" y2="{py + 268}" stroke="{VERDE}" stroke-width="2.5" marker-end="url(#fa)"/>')
    o.append(f'<line x1="{px + 264}" y1="{py + 266}" x2="{px + 438}" y2="{py + 118}" stroke="{VERDE}" stroke-width="2.5" marker-end="url(#fa)"/>')
    o.append(f'<rect x="{px + 440}" y="{py + 86}" width="70" height="70" fill="{VERDE}" opacity="0.35"/>')
    o.append(t(px + 30, py + 110, "lámpara a pilas", 11, GRIS))
    o.append(t(px + 180, py + 318, "un dedo de agua; la placa en el fondo", 11, GRIS))
    o.append(t(px + 425, py + 76, "llega a la pared temblando", 11, GRIS, "end"))
    o.append(t(px + 425, py + 91, "y al revés", 11, GRIS, "end"))

    # B · Voz
    px, py = paneles[1]
    o.append(t(px + 16, py + 28, "B · Voz", 16, peso="bold"))
    o += bandeja(px + 170, py + 190, 200)
    o.append(f'<rect x="{px + 225}" y="{py + 218}" width="90" height="60" rx="6" fill="{NEGRO}"/>')
    o.append(f'<circle cx="{px + 270}" cy="{py + 248}" r="18" fill="none" stroke="{PLATA}" stroke-width="3"/>')
    o.append(f'<path d="M{px + 214},{py + 212} L{px + 214},{py + 286} L{px + 326},{py + 286} L{px + 326},{py + 212}" fill="none" stroke="{GRIS}" stroke-dasharray="3 3"/>')
    for r in (14, 28, 42):
        o.append(f'<path d="M{px + 270 - r * 2},{py + 200} q{r},-{r / 3} {r * 2},0 q{r},{r / 3} {r * 2},0" fill="none" stroke="{VERDE}" stroke-width="1.5"/>')
    o.append(t(px + 30, py + 318, "parlante a pilas, dentro de una bolsa, bajo la bandeja", 11, GRIS))
    o.append(t(px + 30, py + 334, "tu voz leyendo el poema: se guarda lo que hace en el agua, no la grabación", 11, GRIS))

    # C · Pliego de agua (el ángulo de ida y el de vuelta son iguales)
    px, py = paneles[2]
    o.append(t(px + 16, py + 28, "C · Pliego de agua", 16, peso="bold"))
    o.append(f'<line x1="{px + 220}" y1="{py + 60}" x2="{px + 490}" y2="{py + 60}" stroke="{GRIS}" stroke-width="1"/>')
    o.append(f'<line x1="{px + 240}" y1="{py + 60}" x2="{px + 240}" y2="{py + 90}" stroke="{GRIS}"/>')
    o.append(f'<line x1="{px + 470}" y1="{py + 60}" x2="{px + 470}" y2="{py + 90}" stroke="{GRIS}"/>')
    o.append(f'<rect x="{px + 230}" y="{py + 90}" width="250" height="6" fill="{TEXTO}"/>')
    o.append(t(px + 215, py + 92, "pliego en espejo,", 11, GRIS, "end"))
    o.append(t(px + 215, py + 107, "boca abajo", 11, GRIS, "end"))
    o += bandeja(px + 220, py + 250, 270)
    o.append(f'<circle cx="{px + 200}" cy="{py + 198}" r="11" fill="none" stroke="{TEXTO}" stroke-width="2"/>')
    o.append(t(px + 182, py + 202, "quien lee se asoma", 11, GRIS, "end"))
    o.append(f'<line x1="{px + 208}" y1="{py + 206}" x2="{px + 250}" y2="{py + 258}" stroke="{VERDE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    o.append(f'<line x1="{px + 250}" y1="{py + 258}" x2="{px + 385}" y2="{py + 96}" stroke="{VERDE}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    o.append(t(px + 30, py + 318, "el texto solo se lee en el agua; si alguien la toca, se deforma", 11, GRIS))

    # D · Frotado
    px, py = paneles[3]
    o.append(t(px + 16, py + 28, "D · Frotado", 16, peso="bold"))
    o.append(f'<rect x="{px + 60}" y="{py + 150}" width="150" height="10" fill="{PLATA}" stroke="{PLATA_OSC}"/>')
    o.append(f'<path d="M{px + 95},{py + 150} q8,-9 16,0 M{px + 140},{py + 150} q8,-9 16,0" fill="none" stroke="{PLATA_OSC}" stroke-width="2"/>')
    o.append(f'<path d="M{px + 50},{py + 136} L{px + 220},{py + 136}" stroke="{JUNTA}" stroke-width="2"/>')
    o.append(f'<path d="M{px + 80},{py + 110} l70,-50" stroke="{NEGRO}" stroke-width="10" stroke-linecap="round"/>')
    for i in range(5):
        o.append(f'<line x1="{px + 70 + i * 26}" y1="{py + 130}" x2="{px + 88 + i * 26}" y2="{py + 118}" stroke="{GRIS}" stroke-width="1.5"/>')
    o.append(t(px + 135, py + 190, "papel sobre la placa; grafito", 11, GRIS, "middle"))
    for i in range(6):
        x = px + 300 + (i % 3) * 72
        y = py + 60 + (i // 3) * 104
        op = max(0.06, 0.9 - i * 0.16)
        o.append(f'<rect x="{x}" y="{y}" width="60" height="78" fill="#ffffff" stroke="{JUNTA}"/>')
        o.append(f'<rect x="{x + 15}" y="{y + 17}" width="30" height="42" fill="none" stroke="{GRIS}" stroke-width="3" opacity="{op:.2f}"/>')
        o.append(t(x + 30, y + 94, ["1", "5", "10", "15", "20", "…"][i], 10, GRIS, "middle"))
    o.append(t(px + 30, py + 318, "cada frotada aplasta un poco el relieve: se frota hasta que no se lee", 11, GRIS))
    o.append(t(px + 30, py + 334, "el peso de una letra se mide en frotadas", 11, GRIS))
    o.append("</svg>")
    return "\n".join(o), W, H


# ---------------------------------------------------------------- salida

def a_png(svg, w, h, destino, escala=2):
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "v.html"
        html.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}"
                        f"svg{{display:block;width:{w}px;height:{h}px}}</style>{svg}", encoding="utf8")
        captura = Path(tmp) / "v.png"
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--force-device-scale-factor={escala}", f"--window-size={w},{h + 120}",
                        f"--screenshot={captura}", html.as_uri()], check=True, capture_output=True)
        Image.open(captura).convert("RGB").crop((0, 0, w * escala, h * escala)).save(destino)


def a_pdf(paginas, destino):
    cuerpo = "".join(f'<div class="p">{s}</div>' for s in paginas)
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "p.html"
        html.write_text("<!doctype html><meta charset='utf-8'><style>@page{size:A4;margin:0}"
                        "html,body{margin:0}.p{width:210mm;height:297mm;page-break-after:always;overflow:hidden}"
                        ".p>svg{display:block;width:210mm;height:297mm}</style>" + cuerpo, encoding="utf8")
        subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={destino}", html.as_uri()], check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--azulejo", type=float, default=150, help="lado del azulejo de pared, en mm")
    ap.add_argument("--teselas", type=int, default=6, help="teselas del piso por lado de azulejo")
    ap.add_argument("--junta", type=float, default=3, help="ancho de la junta, en mm")
    a = ap.parse_args()
    datos = json.loads((AQUI / "caja.json").read_text(encoding="utf8"))

    svg_caja, cw, chh = caja(datos)
    svg_pauta = pauta(a.azulejo, a.teselas, a.junta)
    svg_ficha = ficha()
    svg_cadena, dw, dh = cadena()
    svg_montajes, mw, mh = montajes()
    for nombre, svg in [("caja_8x7", svg_caja), ("pauta_azulejo", svg_pauta), ("ficha_de_hallazgo", svg_ficha),
                        ("cadena_de_estados", svg_cadena), ("montajes_con_agua", svg_montajes)]:
        (AQUI / f"{nombre}.svg").write_text(svg + "\n", encoding="utf8")
        print(f"{nombre}.svg")

    if not Path(CHROME).exists():
        print("Sin Chromium: no genero vistas ni PDF (define la variable CHROME).")
        return
    for nombre, svg, w, h in [("caja_8x7", svg_caja, cw, chh), ("cadena_de_estados", svg_cadena, dw, dh),
                              ("montajes_con_agua", svg_montajes, mw, mh)]:
        a_png(svg, w, h, AQUI / f"{nombre}.png")
        print(f"{nombre}.png")
    a_png(svg_pauta.replace('width="210mm" height="297mm" ', ""), 794, 1123, AQUI / "pauta_azulejo.png", 1)
    a_png(svg_ficha.replace('width="210mm" height="297mm" ', ""), 794, 1123, AQUI / "ficha_de_hallazgo.png", 1)
    print("pauta_azulejo.png · ficha_de_hallazgo.png")
    caja_a4 = svg_caja.replace("<svg ", '<svg width="210mm" height="297mm" preserveAspectRatio="xMidYMin meet" ', 1)
    a_pdf([svg_pauta, svg_ficha, caja_a4], AQUI / "plantillas_imprimibles.pdf")
    print("plantillas_imprimibles.pdf")


if __name__ == "__main__":
    main()
