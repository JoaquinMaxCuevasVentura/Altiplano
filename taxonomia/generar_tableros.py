"""Genera los tableros de la taxonomía visual a partir de catalogo.json.

Uso (desde la raíz del repositorio):
    python3 taxonomia/generar_tableros.py          # los cuatro tableros y el catálogo legible
    python3 taxonomia/generar_tableros.py 2        # solo el tablero 2

Escribe en taxonomia/:
    tablero_1_arbol.jpg y .pdf   materiales arriba, gestos abajo (a la manera del «Tree Diagram» de Kuma)
    tablero_2_fases.jpg y .pdf   los nueve capítulos de la novela como fases, sobre una línea de horizonte
    tablero_3_fechas.jpg y .pdf  las imágenes por fecha, en una franja por gesto
    tablero_4_relato.jpg y .pdf  el argumento del artículo: hilo rojo para el desarrollo, azul para los hallazgos
    catalogo.md                  la ficha de cada imagen, en una tabla

Las imágenes están en taxonomia/imagenes/. Necesita Chromium (ruta en la variable
CHROME) y Pillow.
"""

import html
import json
import math
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
IMG = BASE / "imagenes"
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

PAPEL = "#f3eee4"
TINTA = "#2b2620"
GRIS = "#7a7166"
CELDA = "#fbf8f1"
SERIF = "'Liberation Serif', 'DejaVu Serif', serif"
SANS = "'DejaVu Sans', 'Liberation Sans', sans-serif"

CAT = json.loads((BASE / "catalogo.json").read_text(encoding="utf8"))
MAT = {m["clave"]: m for m in CAT["materiales"]}
GES = {g["clave"]: g for g in CAT["gestos"]}
IMAGENES = CAT["imagenes"]


def e(t):
    return html.escape(str(t), quote=True)


def lineas(texto, ancho):
    return textwrap.wrap(texto, ancho, break_long_words=False) or [""]


def texto(x, y, cadena, tam, color=TINTA, fuente=SERIF, peso="normal", estilo="normal", ancla="start", alto=1.25,
          halo=False):
    """Una o varias líneas de texto SVG; cadena puede ser lista de líneas. Con halo, un borde del color del
    papel separa el texto de los hilos que pasan por debajo."""
    borde = f' stroke="{PAPEL}" stroke-width="7" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    filas = cadena if isinstance(cadena, list) else [cadena]
    out = []
    for i, f in enumerate(filas):
        # Lo que va entre asteriscos sale en cursiva (o en redonda, si la línea ya es cursiva).
        partes = f.split("*")
        otro = "normal" if estilo == "italic" else "italic"
        cuerpo = "".join(e(p) if j % 2 == 0 else f'<tspan font-style="{otro}">{e(p)}</tspan>' for j, p in enumerate(partes))
        out.append(f'<text x="{x:.1f}" y="{y + i * tam * alto:.1f}" font-size="{tam}" fill="{color}" '
                   f'font-family="{fuente}" font-weight="{peso}" font-style="{estilo}" text-anchor="{ancla}"{borde}>{cuerpo}</text>')
    return "\n".join(out)


def tam_imagen(im):
    with Image.open(IMG / im["archivo"]) as x:
        return x.size


def imagen(im, x, y, w, h):
    """La imagen centrada y entera dentro de la caja (x, y, w, h)."""
    return (f'<image href="{(IMG / im["archivo"]).as_uri()}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" preserveAspectRatio="xMidYMid meet"/>')


def ajustada(im, w, h):
    """Medidas de la imagen dentro de una caja de w por h, sin deformarla."""
    iw, ih = tam_imagen(im)
    k = min(w / iw, h / ih)
    return iw * k, ih * k


def insignia(x, y, n, color, r=15):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" stroke="{PAPEL}" stroke-width="2"/>'
            + texto(x, y + r * 0.36, str(n), int(r * 0.95), "#fff", SANS, "bold", ancla="middle"))


def pie(W, y):
    fuentes = ("Imágenes de dominio público: Det Kgl. Bibliotek (Guaman Poma, 1615), Internet Archive y Getty Research "
               "Institute (Squier, 1877), Public Domain Image Archive y Library of Congress. Fichas, enlaces y derechos: "
               "taxonomia/catalogo.md.")
    return texto(70, y, lineas(fuentes, 210), 17, GRIS, SANS)


def pagina(W, H, cuerpo):
    return (f"<!doctype html><meta charset='utf-8'><style>@page{{size:{W}px {H}px;margin:0}}"
            f"html,body{{margin:0;background:{PAPEL}}}svg{{display:block}}</style>"
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{PAPEL}"/>{cuerpo}</svg>')


# ---------------------------------------------------------------- tablero 1: el árbol

def tablero_arbol():
    W, M = 2800, 70
    colW = (W - 2 * M) / len(GES)
    gut, celdaW, imgH, capH, sep = 62, 296, 190, 86, 12
    filaH = imgH + capH + sep
    yMat, top = 300, 660
    s = [texto(M, 92, "Taxonomía visual de «Cosecha de piedras»", 50, peso="bold"),
         texto(M, 140, "Seis materiales arriba y siete gestos abajo. Cada imagen está en la columna de su gesto, "
               "y una línea del color de su material la ata a él.", 24, GRIS, estilo="italic")]
    # Materiales
    claves = list(MAT)
    xs = {k: M + 190 + i * (W - 2 * M - 380) / (len(claves) - 1) for i, k in enumerate(claves)}
    por_gesto = {g: [im for im in IMAGENES if im["gesto"] == g and im["id"] <= 42] for g in GES}
    curvas, cajas = [], []
    for c, g in enumerate(GES):
        x0 = M + c * colW
        for r, im in enumerate(por_gesto[g]):
            col = MAT[im["material"]]["color"]
            y = top + r * filaH
            ix = x0 + gut
            cajas.append(f'<rect x="{ix:.1f}" y="{y:.1f}" width="{celdaW}" height="{imgH}" fill="{CELDA}" '
                         f'stroke="#d8d0c2" stroke-width="1.2"/>')
            cajas.append(imagen(im, ix + 6, y + 6, celdaW - 12, imgH - 12))
            cajas.append(insignia(ix + 4, y + 4, im["id"], col))
            ls = lineas(im["titulo"], 38)
            cajas.append(texto(ix, y + imgH + 21, ls, 16))
            cajas.append(texto(ix, y + imgH + 21 + len(ls) * 20, f'{im["autor_breve"]}, {im["fecha"]}', 14, GRIS, SANS))
            # Raíz: sale del borde izquierdo de la imagen, sube por la calle y se curva hacia su material.
            lane = x0 + gut - 12 - r * 8
            ys = y + imgH / 2
            mx = xs[im["material"]]
            curvas.append(f'<path d="M{ix:.1f},{ys:.1f} H{lane:.1f} V{top - 24:.1f} '
                          f'C{lane:.1f},{top - 200:.1f} {mx:.1f},{yMat + 170:.1f} {mx:.1f},{yMat + 40:.1f}" '
                          f'fill="none" stroke="{col}" stroke-width="2.6" stroke-opacity="0.82"/>')
            curvas.append(f'<circle cx="{ix:.1f}" cy="{ys:.1f}" r="4.5" fill="{col}"/>')
        # Gesto, al pie de su columna
        yb = top + 6 * filaH + 6
        cajas.append(f'<path d="M{x0 + gut:.1f},{yb:.1f} v14 H{x0 + gut + celdaW:.1f} v-14" fill="none" '
                     f'stroke="{TINTA}" stroke-width="2"/>')
        cajas.append(texto(x0 + gut + celdaW / 2, yb + 62, GES[g]["nombre"], 38, peso="bold", ancla="middle"))
        cajas.append(texto(x0 + gut + celdaW / 2, yb + 94, GES[g]["def"], 18, GRIS, estilo="italic", ancla="middle"))
    for k in claves:
        m = MAT[k]
        n = sum(1 for im in IMAGENES if im["material"] == k and im["id"] <= 42)
        cajas.append(texto(xs[k], yMat - 70, m["nombre"], 38, peso="bold", ancla="middle"))
        cajas.append(texto(xs[k], yMat - 40, m["def"], 18, GRIS, estilo="italic", ancla="middle"))
        cajas.append(f'<circle cx="{xs[k]:.1f}" cy="{yMat:.1f}" r="40" fill="{m["color"]}"/>')
        cajas.append(texto(xs[k], yMat + 10, str(n), 30, "#fff", SANS, "bold", ancla="middle"))
    H = top + 6 * filaH + 270
    con_ref = sum(1 for im in IMAGENES if im["id"] <= 42 and im["referencia"])
    nota = (f"Las imágenes no ilustran la novela: son analogías. Todas tienen un material y un gesto; {con_ref} llevan además "
            f"la cita que justifica la analogía, y las otras {42 - con_ref} todavía no (catalogo.md). El número dentro "
            "de cada material es cuántas imágenes llegan a él.")
    cuerpo = "\n".join(s + curvas + cajas) + texto(M, H - 84, lineas(nota, 230), 18, TINTA, SANS) + pie(W, H - 40)
    return W, H, pagina(W, H, cuerpo)


# ---------------------------------------------------------------- tablero 2: las fases

def tablero_fases():
    W, M = 3000, 60
    fases = CAT["fases"]
    colW = (W - 2 * M) / len(fases)
    yHor, maxW, capH, alto_max = 960, colW - 34, 62, 205
    partes = [("Primera parte", 0, 3), ("Segunda parte", 3, 5), ("Tercera parte", 5, 9)]
    s = [texto(M, 84, "Nueve fases: los capítulos de *Altiplano* sobre una línea de horizonte", 46, peso="bold"),
         texto(M, 128, "Arriba, lo que se levanta y queda a la vista: casas, muros, papeles, máquinas. Abajo, lo que va "
               "a la tierra: semillas, muertos, galerías. Las imágenes son analogías, no ilustraciones.", 23, GRIS,
               estilo="italic")]
    for nombre, a, b in partes:
        x1, x2 = M + a * colW + 8, M + b * colW - 8
        s.append(f'<path d="M{x1:.1f},{184} v-10 H{x2:.1f} v10" fill="none" stroke="{GRIS}" stroke-width="1.6"/>')
        s.append(texto((x1 + x2) / 2, 164, nombre.upper(), 16, GRIS, SANS, "bold", ancla="middle"))
    # Horizonte
    s.append(f'<line x1="{M}" y1="{yHor}" x2="{W - M}" y2="{yHor}" stroke="{TINTA}" stroke-width="5"/>')
    fondo = yHor
    for i, f in enumerate(fases):
        x0 = M + i * colW
        cx = x0 + colW / 2
        if i:
            s.append(f'<line x1="{x0:.1f}" y1="200" x2="{x0:.1f}" y2="{yHor + 560}" stroke="#d8d0c2" '
                     f'stroke-width="1.2" stroke-dasharray="4 6"/>')
        s.append(texto(x0 + 16, 226, f'FASE {f["n"]}', 18, GRIS, SANS, "bold"))
        s.append(texto(x0 + 16, 262, f["capitulo"], 31, peso="bold"))
        s.append(texto(x0 + 16, 290, f'pp. {f["paginas"].replace("-", "–")}', 17, GRIS, SANS))
        if f["cita"]:
            ls = lineas(f'«{f["cita"]}» (p. {f["pagina_cita"]})', 31)
            s.append(texto(x0 + 16, 324, ls, 18, TINTA, estilo="italic"))
        else:
            s.append(texto(x0 + 16, 324, lineas("El artículo no cita este capítulo.", 31), 18, GRIS, estilo="italic"))
        s.append(f'<circle cx="{cx:.1f}" cy="{yHor}" r="9" fill="{TINTA}"/>')
        arriba = [im for im in IMAGENES if im["fase"] == f["n"] and im["lado"] == "arriba"]
        abajo = [im for im in IMAGENES if im["fase"] == f["n"] and im["lado"] == "abajo"]
        # Alto de cada imagen: que la pila de arriba quepa entre la cita (hasta y = 420) y el horizonte.
        maxH = min(alto_max, (yHor - 22 - 420 - len(arriba) * (capH + 14)) / max(len(arriba), 1))
        # Arriba: se apilan hacia arriba desde el horizonte.
        y = yHor - 22
        for im in arriba:
            w, h = ajustada(im, maxW, maxH)
            y -= h + capH
            s.append(imagen(im, cx - w / 2, y, w, h))
            s.append(insignia(cx - w / 2 + 2, y + 2, im["id"], MAT[im["material"]]["color"], 14))
            s.append(texto(cx - maxW / 2, y + h + 19, lineas(im["titulo"], 36)[:3], 15))
            y -= 14
        # Abajo: cuelgan del horizonte.
        y = yHor + 26
        for im in abajo:
            w, h = ajustada(im, maxW, maxH)
            s.append(imagen(im, cx - w / 2, y, w, h))
            s.append(insignia(cx - w / 2 + 2, y + 2, im["id"], MAT[im["material"]]["color"], 14))
            s.append(texto(cx - maxW / 2, y + h + 19, lineas(im["titulo"], 36)[:3], 15))
            y += h + capH + 14
        fondo = max(fondo, y)
    s.append(texto(W - M - 6, yHor - 14, "horizonte", 18, GRIS, estilo="italic", ancla="end"))
    H = int(fondo + 130)
    nota = ("Capítulos y páginas: índice de la 7.ª edición (La Paz, Juventud, 1982). Las citas son las del artículo, "
            "comprobadas en entregables/04_fichero_de_pasajes.md. El color de cada número es el de su material.")
    s.append(texto(M, H - 74, lineas(nota, 210), 18, TINTA, SANS))
    s.append(pie(W, H - 28))
    return W, H, pagina(W, H, "\n".join(s))


# ---------------------------------------------------------------- tablero 3: las fechas

def tablero_fechas():
    W, M = 3000, 60
    xL, x0, x1 = M + 300, M + 470, W - M - 40   # carril de rótulos, comienzo y fin del eje 1500-1950
    a0, a1 = 1500, 1950
    laneH, top, th = 200, 250, 80

    def X(anio):
        if anio < a0:   # lo anterior a 1500 (la túnica wari) va a la izquierda del corte
            return xL + 70
        return x0 + (anio - a0) * (x1 - x0) / (a1 - a0)

    s = [texto(M, 84, "Mapa de fechas: cuándo aparece cada gesto en las imágenes reunidas", 46, peso="bold"),
         texto(M, 128, "Una franja por gesto. Cada miniatura está en su año; las líneas verticales unen las imágenes "
               "de una misma obra. Es un mapa de esta selección, no de la historia de la imagen.", 23, GRIS,
               estilo="italic")]
    gestos = list(GES)
    bottom = top + laneH * len(gestos)
    for i, g in enumerate(gestos):
        y = top + i * laneH
        if i % 2 == 0:
            s.append(f'<rect x="{M}" y="{y}" width="{W - 2 * M}" height="{laneH}" fill="#ece5d8"/>')
        s.append(texto(M + 14, y + 62, GES[g]["nombre"], 34, peso="bold"))
        s.append(texto(M + 14, y + 92, lineas(GES[g]["def"], 26), 17, GRIS, estilo="italic"))
    # Eje
    for anio in range(1500, 1951, 50):
        x = X(anio)
        s.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="#d2c9b9" stroke-width="1"/>')
        s.append(texto(x, bottom + 34, str(anio), 20, GRIS, SANS, ancla="middle"))
    s.append(f'<line x1="{xL + 140:.1f}" y1="{top}" x2="{xL + 140:.1f}" y2="{bottom}" stroke="{TINTA}" '
             f'stroke-width="2" stroke-dasharray="3 5"/>')
    s.append(texto(xL + 70, bottom + 34, "hacia 800", 20, GRIS, SANS, ancla="middle"))
    # La novela
    for anio in (1940, 1945):
        x = X(anio)
        s.append(f'<line x1="{x:.1f}" y1="{top - 40}" x2="{x:.1f}" y2="{bottom + 50}" stroke="#9c2a3f" stroke-width="3"/>')
    s.append(texto(X(1945) - 8, top - 52, "*Altiplano*: 1940, escrita para el concurso (nota «Al lector», p. 4); "
                   "1945, primera edición en Buenos Aires", 19, "#9c2a3f", SANS, "bold", ancla="end"))
    # Grupos: misma obra (autor y año) en el mismo gesto.
    grupos = {}
    for im in IMAGENES:
        grupos.setdefault((im["gesto"], im["anio"], im["autor"]), []).append(im)
    pos = {}
    for i, g in enumerate(gestos):
        y = top + i * laneH
        fila = sorted([(k, v) for k, v in grupos.items() if k[0] == g], key=lambda kv: kv[0][1])
        libre = -1e9
        rotulos = []
        for (gg, anio, autor), ims in fila:
            cols = min(len(ims), 3)
            ancho = cols * (th + 4)
            xc = max(X(anio) - ancho / 2, libre + 8)
            libre = xc + ancho
            filas = (len(ims) + 2) // 3
            yc = y + (laneH - filas * (th + 4)) / 2
            # Marca del año exacto sobre el borde de la franja y, si el grupo se corrió, una guía.
            s.append(f'<circle cx="{X(anio):.1f}" cy="{y + laneH - 6:.1f}" r="4" fill="{TINTA}"/>')
            if abs(xc + ancho / 2 - X(anio)) > 4:
                s.append(f'<line x1="{X(anio):.1f}" y1="{y + laneH - 6:.1f}" x2="{xc + ancho / 2:.1f}" '
                         f'y2="{yc + filas * (th + 4):.1f}" stroke="{GRIS}" stroke-width="1"/>')
            for j, im in enumerate(ims):
                xi = xc + (j % 3) * (th + 4)
                yi = yc + (j // 3) * (th + 4)
                col = MAT[im["material"]]["color"]
                s.append(f'<rect x="{xi:.1f}" y="{yi:.1f}" width="{th}" height="{th}" fill="{CELDA}" stroke="{col}" stroke-width="3"/>')
                s.append(f'<image href="{(IMG / im["archivo"]).as_uri()}" x="{xi + 3:.1f}" y="{yi + 3:.1f}" '
                         f'width="{th - 6}" height="{th - 6}" preserveAspectRatio="xMidYMid slice"/>')
                s.append(f'<rect x="{xi + th - 27:.1f}" y="{yi + th - 20:.1f}" width="24" height="17" fill="{TINTA}" fill-opacity="0.75"/>')
                s.append(texto(xi + th - 15, yi + th - 7, str(im["id"]), 13, "#fff", SANS, "bold", ancla="middle"))
            pos.setdefault((anio, autor), []).append((xc + ancho / 2, yc, yc + filas * (th + 4)))
            if autor not in ("Felipe Guaman Poma de Ayala", "E. G. Squier"):
                rot = f'{ims[0]["autor_breve"]}, {ims[0]["fecha"]}'
                xm, media = xc + ancho / 2, len(rot) * 3.9   # media anchura aproximada del rótulo
                fila_r = 0   # si choca con otro rótulo de la franja, baja una línea
                while any(r == fila_r and xm - media < b2 + 6 and xm + media > a2 - 6 for a2, b2, r in rotulos):
                    fila_r += 1
                rotulos.append((xm - media, xm + media, fila_r))
                s.append(texto(xm, yc + filas * (th + 4) + 17 + fila_r * 16, rot, 13, GRIS, SANS, ancla="middle"))
    # Una misma obra en varios gestos: línea vertical entre sus grupos.
    for (anio, autor), ps in pos.items():
        if len(ps) > 1:
            ps.sort(key=lambda p: p[1])
            for a, b in zip(ps, ps[1:]):
                s.append(f'<path d="M{a[0]:.1f},{a[2]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{TINTA}" '
                         f'stroke-width="1.6" stroke-dasharray="6 4" fill="none"/>')
    # Rótulos de las obras que aparecen en varios gestos
    for (anio, autor), ps in pos.items():
        if len(ps) > 2:
            x = min(p[0] for p in ps)
            s.append(texto(x, top - 14, f"{autor.split(',')[0]}, {anio}", 19, TINTA, SANS, "bold", ancla="middle"))
    # Leyenda de materiales
    ly = bottom + 90
    s.append(texto(M, ly, "Borde de cada miniatura: su material", 19, TINTA, SANS, "bold"))
    for i, k in enumerate(MAT):
        x = M + 420 + i * 260
        s.append(f'<rect x="{x}" y="{ly - 20}" width="26" height="26" fill="{CELDA}" stroke="{MAT[k]["color"]}" stroke-width="4"/>')
        s.append(texto(x + 38, ly, MAT[k]["nombre"], 20, TINTA, SANS))
    H = ly + 90
    s.append(pie(W, H - 28))
    return W, H, pagina(W, H, "\n".join(s))


# ---------------------------------------------------------------- tablero 4: el relato

ROJO = "#c0262d"
AZUL = "#1f5fbf"


def tablero_relato():
    """El argumento del artículo como un tablero de collage: hilo rojo para el desarrollo, azul para los hallazgos."""
    W, H = 3000, 2110
    R = CAT["relato"]
    POR_ID = {im["id"]: im for im in IMAGENES}
    # Centro de cada grupo de imágenes: arriba de izquierda a derecha, baja por la derecha y vuelve abajo.
    sitio = {"1": (300, 450), "2": (870, 450), "3": (1450, 450), "4": (2030, 450), "5": (2600, 450),
             "6": (2790, 930), "7": (2260, 1330), "8": (1560, 1330), "9": (880, 1330), "callado": (1960, 900)}
    giro = {"1": -1.5, "2": 1.2, "3": -0.8, "4": 1.5, "5": -1.0, "6": -1.2, "7": 1.0, "8": -1.4, "9": 0.9,
            "callado": 1.8}
    altoMax, anchoMax = 220, 500
    s = [texto(60, 84, "El relato: el argumento de «Cosecha de piedras» sobre las imágenes", 46, peso="bold"),
         texto(60, 128, "Hilo rojo: el desarrollo, en el orden de la novela. Hilo azul: los cuatro hallazgos de las "
               "conclusiones (sección 8). Las imágenes son analogías; las citas, las del artículo.", 23, GRIS,
               estilo="italic")]
    capas_hilo, capas_img, capas_txt = [], [], []
    ancla = {}   # centro de cada grupo, para los hilos
    pie_grupo = {}   # borde inferior del grupo de imágenes

    def grupo(clave, ids):
        cx, cy = sitio[clave]
        ims = [POR_ID[i] for i in ids]
        medidas = [ajustada(im, anchoMax / len(ims) - 16, altoMax) for im in ims]
        total = sum(w for w, h in medidas) + 22 * (len(ims) - 1)
        x = cx - total / 2
        alto = max(h for w, h in medidas)
        partes = []
        for im, (w, h) in zip(ims, medidas):
            y = cy - h / 2
            partes.append(f'<rect x="{x - 7:.1f}" y="{y - 7:.1f}" width="{w + 14:.1f}" height="{h + 14:.1f}" '
                          f'fill="#fffdf8" stroke="#cfc6b6" stroke-width="1"/>')
            partes.append(imagen(im, x, y, w, h))
            partes.append(insignia(x - 2, y - 2, im["id"], MAT[im["material"]]["color"], 14))
            x += w + 22
        capas_img.append(f'<g transform="rotate({giro[clave]} {cx:.1f} {cy:.1f})">{"".join(partes)}</g>')
        ancla[clave] = (cx, cy)
        pie_grupo[clave] = cy + alto / 2 + 7
        return cx, cy, alto, total

    # Nodos del desarrollo
    nodos = R["nodos"]
    for nd in nodos:
        cx, cy, alto, total = grupo(nd["n"], nd["imagenes"])
        y0 = cy + alto / 2 + 44
        x0 = cx - max(total, 300) / 2
        etiqueta = f'{nd["n"]} · {nd["titulo"]}'
        capas_txt.append(f'<rect x="{x0:.1f}" y="{y0 - 27:.1f}" width="{len(etiqueta) * 15 + 26:.1f}" height="38" fill="{ROJO}"/>')
        capas_txt.append(texto(x0 + 13, y0, etiqueta, 25, "#fff", SERIF, "bold"))
        capas_txt.append(texto(x0, y0 + 36, f'{nd["capitulo"]}, p. {nd["pagina"]}', 17, GRIS, SANS, halo=True))
        capas_txt.append(texto(x0, y0 + 64, lineas(f'«{nd["cita"]}»', 44), 21, TINTA, estilo="italic", halo=True))
    # Lo que la novela calla
    cl = R["callado"]
    cx, cy, alto, total = grupo("callado", cl["imagenes"])
    capas_img.append(f'<rect x="{cx - total / 2 - 26:.1f}" y="{cy - alto / 2 - 30:.1f}" width="{total + 52:.1f}" '
                     f'height="{alto + 60:.1f}" fill="none" stroke="{AZUL}" stroke-width="2.5" stroke-dasharray="10 7"/>')
    capas_txt.append(texto(cx, cy + alto / 2 + 64, lineas(cl["rotulo"], 30), 22, AZUL, SERIF, "bold", "italic",
                           ancla="middle", halo=True))
    capas_txt.append(texto(cx, cy + alto / 2 + 120, "Guaman Poma, 1615", 16, GRIS, SANS, ancla="middle", halo=True))

    # Hilo rojo: de un nodo al siguiente, con una flecha a mitad de cada tramo.
    codos = {("5", "6"): [(2945, 450), (2945, 930)]}   # rodeos para no cruzar los rótulos
    for a, b in zip(nodos, nodos[1:]):
        pts = [ancla[a["n"]]] + codos.get((a["n"], b["n"]), []) + [ancla[b["n"]]]
        capas_hilo.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" '
                          f'stroke="{ROJO}" stroke-width="6" stroke-linejoin="round"/>')
        # Flecha a mitad del tramo más largo
        (x1, y1), (x2, y2) = max(zip(pts, pts[1:]), key=lambda s: math.dist(*s))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        capas_txt.append(f'<polygon points="-16,-12 14,0 -16,12" fill="{ROJO}" transform="translate({mx:.1f} {my:.1f}) rotate({ang:.1f})"/>')
    for nd in nodos:
        x, y = ancla[nd["n"]]
        capas_txt.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{ROJO}" stroke="#fff" stroke-width="3"/>')
    # Arco de la profecía: del primer montón al último.
    ar = R["arco"]
    (x1, y1), (x2, y2) = ancla[ar["desde"]], ancla[ar["hasta"]]
    capas_hilo.append(f'<path d="M{x1:.1f},{y1:.1f} C{x1 - 80:.1f},{y1 + 900:.1f} {x2 - 700:.1f},{y2 + 120:.1f} {x2:.1f},{y2:.1f}" '
                      f'fill="none" stroke="{ROJO}" stroke-width="3.5" stroke-dasharray="14 9"/>')
    ls = lineas(f'«{ar["cita"]}» (p. {ar["pagina"]})', 34)
    capas_txt.append(texto(140, 1000, ls, 21, ROJO, estilo="italic", halo=True))
    capas_txt.append(texto(140, 1000 + len(ls) * 26 + 6, lineas(ar["rotulo"], 34), 19, ROJO, SANS, "bold", halo=True))

    # Hallazgos (azul), al pie, con sus hilos hacia los nodos que los sostienen.
    hs = R["hallazgos"]
    yC, hC, mC = 1690, 230, 60
    anchoC = (W - 2 * mC - 3 * 40) / len(hs)
    for i, h in enumerate(hs):
        xC = mC + i * (anchoC + 40)
        n = len(h["nodos"])
        for j, destino in enumerate(h["nodos"]):
            px = xC + anchoC * (j + 1) / (n + 1)
            dx, dy = ancla[destino]
            dy = pie_grupo[destino] - 20
            raya = ' stroke-dasharray="12 8"' if destino == "callado" else ""
            capas_hilo.append(f'<line x1="{px:.1f}" y1="{yC:.1f}" x2="{dx:.1f}" y2="{dy:.1f}" stroke="{AZUL}" '
                              f'stroke-width="3" stroke-opacity="0.85"{raya}/>')
            capas_txt.append(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="7" fill="{AZUL}" stroke="#fff" stroke-width="2"/>')
            capas_txt.append(f'<circle cx="{px:.1f}" cy="{yC:.1f}" r="7" fill="{AZUL}"/>')
        capas_txt.append(f'<rect x="{xC:.1f}" y="{yC:.1f}" width="{anchoC:.1f}" height="{hC}" fill="#f8fbff" '
                         f'stroke="{AZUL}" stroke-width="3"/>')
        capas_txt.append(texto(xC + 24, yC + 48, f'Hallazgo {h["n"]}', 28, AZUL, SERIF, "bold"))
        capas_txt.append(texto(xC + 24, yC + 90, lineas(h["texto"], 52), 23, TINTA))
        capas_txt.append(texto(xC + anchoC - 24, yC + hC - 18, "hilos a: " + ", ".join(
            "lo callado" if d == "callado" else d for d in h["nodos"]), 16, GRIS, SANS, ancla="end"))
    # Leyenda
    ly = 168
    s.append(f'<line x1="1960" y1="{ly}" x2="2040" y2="{ly}" stroke="{ROJO}" stroke-width="6"/>')
    s.append(texto(2055, ly + 7, "desarrollo", 20, TINTA, SANS))
    s.append(f'<line x1="2220" y1="{ly}" x2="2300" y2="{ly}" stroke="{ROJO}" stroke-width="3.5" stroke-dasharray="14 9"/>')
    s.append(texto(2315, ly + 7, "eco", 20, TINTA, SANS))
    s.append(f'<line x1="2420" y1="{ly}" x2="2500" y2="{ly}" stroke="{AZUL}" stroke-width="3"/>')
    s.append(texto(2515, ly + 7, "conclusión", 20, TINTA, SANS))
    s.append(texto(60, H - 76, lineas("Los hallazgos resumen la sección 8 del artículo. Los números de colores son los de "
                                      "las imágenes en catalogo.md; el color es el de su material.", 230), 18, TINTA, SANS))
    s.append(pie(W, H - 34))
    return W, H, pagina(W, H, "\n".join(s + capas_hilo + capas_img + capas_txt))


# ---------------------------------------------------------------- catálogo legible

def catalogo_md():
    filas = ["# Catálogo de la taxonomía visual", "",
             "Generado por `generar_tableros.py` desde `catalogo.json`; no lo edites a mano. "
             "La «referencia» es la cita de la novela o del artículo que justifica la analogía; las citas de la novela "
             "son las del artículo, con su página en la 7.ª edición (1982).", "",
             "| N.º | Imagen | Autor y fecha | Material | Gesto | Fase | Referencia | Fuente y derechos |",
             "|---|---|---|---|---|---|---|---|"]
    fases = {f["n"]: f["capitulo"] for f in CAT["fases"]}
    for im in IMAGENES:
        ubic = f', {im["ubicacion"]}' if im["ubicacion"] else ""
        orig = f' (*{im["titulo_original"]}*)' if im["titulo_original"] else ""
        fase = f'{im["fase"]} {fases[im["fase"]]}, {im["lado"]}' if im["fase"] else "—"
        filas.append(f'| {im["id"]} | [{im["titulo"]}](imagenes/{im["archivo"]}){orig} | {im["autor"]}, {im["fecha"]}{ubic} | '
                     f'{MAT[im["material"]]["nombre"]} | {GES[im["gesto"]]["nombre"]} | {fase} | '
                     f'{im["referencia"] or "—"} | [{im["fuente"]}]({im["pagina"]}). {im["derechos"]} |')
    (BASE / "catalogo.md").write_text("\n".join(filas) + "\n", encoding="utf8")
    print("catalogo.md")


def render(nombre, W, H, doc):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / f"{nombre}.html"
        f.write_text(doc, encoding="utf8")
        png = Path(tmp) / f"{nombre}.png"
        base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                "--allow-file-access-from-files", "--virtual-time-budget=8000"]
        subprocess.run(base + ["--force-device-scale-factor=1", f"--window-size={W},{H + 300}", f"--screenshot={png}",
                               f.as_uri()], check=True, capture_output=True)
        Image.open(png).convert("RGB").crop((0, 0, W, H)).save(BASE / f"{nombre}.jpg", quality=86, optimize=True,
                                                                 progressive=True)
        subprocess.run(base + ["--no-pdf-header-footer", f"--print-to-pdf={BASE / (nombre + '.pdf')}", f.as_uri()],
                       check=True, capture_output=True)
    print(f"{nombre}.jpg y .pdf ({W} x {H})")


def main():
    pedidos = {int(a) for a in sys.argv[1:]}
    tableros = [(1, "tablero_1_arbol", tablero_arbol), (2, "tablero_2_fases", tablero_fases),
                (3, "tablero_3_fechas", tablero_fechas), (4, "tablero_4_relato", tablero_relato)]
    for n, nombre, f in tableros:
        if pedidos and n not in pedidos:
            continue
        render(nombre, *f())
    if not pedidos:
        catalogo_md()


if __name__ == "__main__":
    main()
