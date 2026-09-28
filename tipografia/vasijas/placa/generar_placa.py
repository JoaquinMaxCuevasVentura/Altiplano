"""Genera Placa, una escritura que se oye pero no se lee.

Cada letra es la figura que la arena dibuja sobre una placa cuadrada cuando
la placa suena en el modo de esa letra (modos.py). La figura no se dibuja: se
calcula. La arena queda donde la placa casi no se mueve, en la franja
|f(x, y)| < t, y esa franja se convierte en el contorno del glifo.

- La franja se ensancha donde la placa vibra poco y se afina donde vibra
  mucho, como la arena de verdad.
- Mayúsculas y minúsculas comparten figura: la voz no tiene caja.
- Una vocal con tilde suena más fuerte: su placa lleva doble borde.
- El espacio es una placa sin arena. El punto es un montoncito en el centro.
- Las filas y las columnas quedan a la misma distancia: un texto en Placa es
  una pared de azulejos, o un cuerpo cubierto de relieves.

Uso:  python3 generar_placa.py
Salida: Placa.ttf, Placa.woff2 y modos.json
"""

import math
import os
import sys
import unicodedata

import numpy as np
import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import modos as M  # noqa: E402

UPM = 1000
LADO = 680            # lado de la placa
MARGEN = 30           # aire a cada lado de la placa
AVANCE = LADO + 2 * MARGEN
BORDE = 8             # grosor del borde de la placa
MUESTRAS = 280        # resolución con que se calcula la vibración
ARENA = 0.045         # ancho de la franja de arena, relativo al número de onda


# --- Marching squares: el borde de la región donde queda arena ---------------

def anillos(g):
    """Contornos cerrados de la región g < 0, en coordenadas de muestra."""
    g = np.pad(g, 1, constant_values=1.0)
    alto, ancho = g.shape
    adentro = g < 0

    def punto(arista):
        tipo, i, j = arista
        if tipo == "h":
            a, b = g[j, i], g[j, i + 1]
            t = a / (a - b)
            return (i + t, j)
        a, b = g[j, i], g[j + 1, i]
        t = a / (a - b)
        return (i, j + t)

    segmentos = []
    for j in range(alto - 1):
        for i in range(ancho - 1):
            c0, c1 = adentro[j, i], adentro[j, i + 1]
            c2, c3 = adentro[j + 1, i + 1], adentro[j + 1, i]
            caso = c0 | (c1 << 1) | (c2 << 2) | (c3 << 3)
            if caso in (0, 15):
                continue
            e0, e1, e2, e3 = ("h", i, j), ("v", i + 1, j), ("h", i, j + 1), ("v", i, j)
            centro = (g[j, i] + g[j, i + 1] + g[j + 1, i + 1] + g[j + 1, i]) < 0
            tabla = {
                1: [(e3, e0)], 2: [(e0, e1)], 3: [(e3, e1)], 4: [(e1, e2)],
                5: [(e0, e1), (e2, e3)] if centro else [(e3, e0), (e1, e2)],
                6: [(e0, e2)], 7: [(e3, e2)], 8: [(e2, e3)], 9: [(e0, e2)],
                10: [(e3, e0), (e1, e2)] if centro else [(e0, e1), (e2, e3)],
                11: [(e1, e2)], 12: [(e1, e3)], 13: [(e0, e1)], 14: [(e0, e3)],
            }
            segmentos.extend(tabla[caso])

    vecinos = {}
    for k, (a, b) in enumerate(segmentos):
        vecinos.setdefault(a, []).append(k)
        vecinos.setdefault(b, []).append(k)
    usados = [False] * len(segmentos)
    resultado = []
    for k in range(len(segmentos)):
        if usados[k]:
            continue
        usados[k] = True
        inicio, actual = segmentos[k]
        anillo = [inicio]
        while actual != inicio:
            anillo.append(actual)
            siguiente = next((s for s in vecinos[actual] if not usados[s]), None)
            if siguiente is None:
                break
            usados[siguiente] = True
            a, b = segmentos[siguiente]
            actual = b if a == actual else a
        # Se descuenta el relleno de una muestra agregado alrededor.
        resultado.append([(x - 1, y - 1) for x, y in (punto(e) for e in anillo)])
    return resultado


def simplificar(puntos, tolerancia):
    """Douglas-Peucker para un anillo cerrado."""
    if len(puntos) < 8:
        return puntos

    def dp(pts):
        if len(pts) < 3:
            return pts
        (x0, y0), (x1, y1) = pts[0], pts[-1]
        dx, dy = x1 - x0, y1 - y0
        largo = math.hypot(dx, dy) or 1e-9
        peor, indice = 0.0, 0
        for k in range(1, len(pts) - 1):
            x, y = pts[k]
            d = abs(dy * (x - x0) - dx * (y - y0)) / largo
            if d > peor:
                peor, indice = d, k
        if peor <= tolerancia:
            return [pts[0], pts[-1]]
        return dp(pts[:indice + 1])[:-1] + dp(pts[indice:])

    mitad = len(puntos) // 2
    return dp(puntos[:mitad + 1])[:-1] + dp(puntos[mitad:] + [puntos[0]])[:-1]


# --- De la figura al glifo --------------------------------------------------------

def cuadrado(x0, y0, x1, y1):
    p = pathops.Path()
    p.moveTo(x0, y0)
    p.lineTo(x1, y0)
    p.lineTo(x1, y1)
    p.lineTo(x0, y1)
    p.close()
    return p


def marco(inset=0, grosor=BORDE):
    x0, y0 = MARGEN + inset, inset
    x1, y1 = MARGEN + LADO - inset, LADO - inset
    return pathops.op(cuadrado(x0, y0, x1, y1),
                      cuadrado(x0 + grosor, y0 + grosor, x1 - grosor, y1 - grosor),
                      pathops.PathOp.DIFFERENCE)


def arena(modo):
    n, m, s = modo["n"], modo["m"], modo["s"]
    u = np.linspace(0.0, 1.0, MUESTRAS)
    x, y = np.meshgrid(u, u)
    k = math.hypot(n, m)
    g = np.abs(M.f(x, y, n, m, s)) - ARENA * k
    escala = LADO / (MUESTRAS - 1)
    p = pathops.Path(fillType=pathops.FillType.EVEN_ODD)
    for anillo in anillos(g):
        pts = simplificar([(MARGEN + a * escala, b * escala) for a, b in anillo], 0.6)
        if len(pts) < 3:
            continue
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        p.close()
    p.simplify()
    return pathops.op(p, cuadrado(MARGEN, 0, MARGEN + LADO, LADO), pathops.PathOp.INTERSECTION)


def monton(cx, cy, r):
    """Un montoncito de arena: un octógono."""
    p = pathops.Path()
    for k in range(8):
        a = math.pi / 8 + k * math.pi / 4
        (p.moveTo if k == 0 else p.lineTo)(cx + r * math.cos(a), cy + r * math.sin(a))
    p.close()
    return p


def union(*caminos):
    total = pathops.Path()
    for c in caminos:
        total = pathops.op(total, c, pathops.PathOp.UNION)
    return total


def a_glifo(camino):
    pen = TTGlyphPen(None)
    area = 0.0
    for contorno in camino.contours:
        pts = [pt for pt in contorno.points]
        area += sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
    # TrueType dibuja los contornos exteriores en sentido horario.
    destino = ReverseContourPen(pen) if area > 0 else pen
    camino.draw(destino)
    return pen.glyph()


# --- La fuente -------------------------------------------------------------------

def figuras():
    tabla = M.modos()
    base = {ch: union(marco(), arena(mo)) for ch, mo in tabla.items()}
    glifos, cmap = {}, {}

    def nombre(ch):
        return "uni%04X" % ord(ch)

    for ch, camino in base.items():
        glifos[nombre(ch)] = camino
        cmap[ord(ch)] = nombre(ch)
        if ch.upper() != ch:
            cmap[ord(ch.upper())] = nombre(ch)

    # Las vocales con tilde suenan más fuerte: doble borde.
    for ch in "áéíóúü":
        vocal = unicodedata.normalize("NFD", ch)[0]
        camino = union(base[vocal], marco(inset=24, grosor=6))
        glifos[nombre(ch)] = camino
        cmap[ord(ch)] = nombre(ch)
        cmap[ord(ch.upper())] = nombre(ch)

    silencio = marco()
    glifos["space"] = silencio
    cmap[0x20] = "space"
    cmap[0xA0] = "space"
    c = MARGEN + LADO / 2
    glifos["period"] = union(marco(), monton(c, LADO / 2, 34))
    cmap[ord(".")] = "period"
    glifos["comma"] = union(marco(), monton(c, LADO * 0.22, 26))
    cmap[ord(",")] = "comma"
    for ch in ";:¿?¡!-–—…«»“”‘’'\"()":
        cmap[ord(ch)] = "space"
    glifos[".notdef"] = silencio
    return glifos, cmap


def construir():
    glifos, cmap = figuras()
    orden = [".notdef"] + sorted(n for n in glifos if n != ".notdef")
    tabla = {n: a_glifo(glifos[n]) for n in orden}
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(orden)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(tabla)
    metricas = {}
    for n, g in tabla.items():
        g.recalcBounds(fb.font["glyf"])
        metricas[n] = (AVANCE, g.xMin if g.numberOfContours else 0)
    fb.setupHorizontalMetrics(metricas)
    # Filas y columnas a la misma distancia: 740 de avance, 740 de interlínea.
    fb.setupHorizontalHeader(ascent=LADO + 30, descent=-30, lineGap=0)
    fb.setupNameTable({
        "familyName": "Placa",
        "styleName": "Regular",
        "uniqueFontIdentifier": "Placa-0.100",
        "fullName": "Placa",
        "version": "Version 0.100",
        "psName": "Placa-Regular",
        "designer": "Joaquin Max Cuevas Ventura",
        "description": ("Escritura de Chladni: cada letra es la figura que la arena dibuja "
                        "sobre una placa de aluminio cuando suena en el modo de esa letra. "
                        "A partir de «Contener una ruina», de Rebeca Paz."),
        "copyright": "Prototipo 2026. Licencia por definir.",
    })
    fb.setupOS2(sTypoAscender=LADO + 30, sTypoDescender=-30, sTypoLineGap=0,
                usWinAscent=LADO + 40, usWinDescent=40, sxHeight=LADO, sCapHeight=LADO,
                fsSelection=0x40 | 0x80, version=4, achVendID="NONE")
    fb.setupPost(isFixedPitch=1)
    fb.setupMaxp()
    return fb.font


def main():
    font = construir()
    ttf = os.path.join(AQUI, "Placa.ttf")
    font.save(ttf)
    f = TTFont(ttf)
    f.flavor = "woff2"
    f.save(os.path.join(AQUI, "Placa.woff2"))
    M.exportar_json(os.path.join(AQUI, "modos.json"))
    print("Placa: %d glifos, %.0f KB (woff2)" % (
        len(font.getGlyphOrder()), os.path.getsize(os.path.join(AQUI, "Placa.woff2")) / 1024))


if __name__ == "__main__":
    main()
