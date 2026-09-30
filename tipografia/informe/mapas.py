"""Los mapas del informe de decisiones de Contenida.

Uso (desde la raíz del repositorio):
    python3 tipografia/informe/mapas.py

Escribe en tipografia/informe/mapas/ seis mapas en SVG y en PNG (con Chromium,
como las láminas). Toman de las referencias (planos de dibujo, análisis de
borde, haces de líneas con rótulos, redes sobre un plano) el modo de dibujar,
y de Contenida todo lo demás:
  - la tinta es el violeta del esténcil y el gris del grafito; el verde, que es
    solo luz, no aparece;
  - los nodos son celdas de la cabeza del ídolo, un rectángulo dentro de otro,
    abiertos abajo en su desagüe; o círculos, cuando son fuentes;
  - las vasijas son los cuatro generadores (o, l, n, a), rayados en violeta y
    acotados en milímetros;
  - los rótulos van en Courier Prime; los versos, en Newsreader cursiva;
  - cada mapa lleva su ficha, como las placas, y su folio.
"""

import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
SALIDA = AQUI / "mapas"
FUENTES = TIPO / "laminas" / "fuentes"
sys.path.insert(0, str(TIPO / "laminas"))

PAPEL, TINTA, VIOLETA, LILA = "#f6f4ee", "#1d1c1a", "#4a2470", "#b9a6d6"
GRIS, GRIS2, FILETE, OBRA = "#6d6a63", "#9a968d", "#cfcac0", "#d9d4c8"
MONO, SERIF = "Courier Prime", "Newsreader"
FECHA = "30.09.2026"
TOTAL = 6


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def partir(texto, ancho):
    """Corta un texto en líneas de a lo sumo `ancho` caracteres, por palabras."""
    lineas, linea = [], ""
    for p in texto.split():
        if linea and len(linea) + 1 + len(p) > ancho:
            lineas.append(linea)
            linea = p
        else:
            linea = f"{linea} {p}".strip()
    if linea:
        lineas.append(linea)
    return lineas


class Lienzo:
    def __init__(self, ancho, alto, semilla):
        self.W, self.H = ancho, alto
        self.capas = {"fondo": [], "construccion": [], "rayado": [], "haces": [], "nodos": [], "textos": []}
        self.defs = []
        self.rng = random.Random(semilla)
        self.n_clip = 0

    def add(self, capa, s):
        self.capas[capa].append(s)

    # -------------------------------------------------------------- texto
    def texto(self, x, y, t, tam=14, color=TINTA, fuente=MONO, ancla="start", estilo="", peso=400, esp=0.0,
              capa="textos", rot=0.0):
        tr = f' transform="rotate({rot:.2f} {x:.1f} {y:.1f})"' if rot else ""
        st = f' font-style="{estilo}"' if estilo else ""
        ls = f' letter-spacing="{esp}"' if esp else ""
        self.add(capa, f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fuente}" font-size="{tam}" fill="{color}" '
                       f'text-anchor="{ancla}" font-weight="{peso}"{st}{ls}{tr}>{esc(t)}</text>')

    def bloque(self, x, y, lineas, tam=14, color=TINTA, fuente=MONO, ancla="start", estilo="", inter=1.25, fondo=True):
        """Varias líneas; con fondo de papel para que los haces no las crucen."""
        if fondo:
            ancho = max(len(l) for l in lineas) * tam * (0.6 if fuente == MONO else 0.47)
            x0 = x if ancla == "start" else x - ancho if ancla == "end" else x - ancho / 2
            self.add("textos", f'<rect x="{x0 - 3:.1f}" y="{y - tam * 0.95:.1f}" width="{ancho + 6:.1f}" '
                               f'height="{tam * inter * (len(lineas) - 1) + tam * 1.3:.1f}" fill="{PAPEL}" opacity=".86"/>')
        for i, l in enumerate(lineas):
            self.texto(x, y + i * tam * inter, l, tam, color, fuente, ancla, estilo)
        return y + (len(lineas) - 1) * tam * inter

    # -------------------------------------------------------------- líneas
    def linea(self, x0, y0, x1, y1, color=TINTA, grosor=0.6, opacidad=1.0, guiones="", capa="haces"):
        g = f' stroke-dasharray="{guiones}"' if guiones else ""
        self.add(capa, f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{color}" '
                       f'stroke-width="{grosor}" opacity="{opacidad}"{g}/>')

    def curva(self, p0, p1, p2, p3, color=TINTA, grosor=0.55, opacidad=0.8, guiones="", capa="haces"):
        g = f' stroke-dasharray="{guiones}"' if guiones else ""
        self.add(capa, f'<path d="M{p0[0]:.1f},{p0[1]:.1f} C{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} '
                       f'{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="{color}" stroke-width="{grosor}" '
                       f'opacity="{opacidad}"{g}/>')

    def haz(self, origen, nudo, destino, hebras=5, color=TINTA, abre=10.0, opacidad=0.55, llegada=None, grosor=0.5,
            guiones=""):
        """Un haz de hebras finas: sale junto del origen, se aprieta en el nudo y se abre hacia el destino."""
        r = self.rng
        llegada = llegada if llegada is not None else (destino[0] - nudo[0], destino[1] - nudo[1])
        L = math.hypot(*llegada) or 1
        ux, uy = llegada[0] / L, llegada[1] / L
        for _ in range(hebras):
            j = lambda s: r.uniform(-s, s)                                            # noqa: E731
            p0 = (origen[0] + j(3), origen[1] + j(3))
            p1 = (nudo[0] + j(2.5), nudo[1] + j(2.5))
            d = math.hypot(destino[0] - nudo[0], destino[1] - nudo[1]) * r.uniform(0.35, 0.55)
            p2 = (destino[0] - ux * d + j(abre), destino[1] - uy * d + j(abre))
            p3 = (destino[0] + j(abre * 0.25), destino[1] + j(abre * 0.25))
            self.curva(p0, p1, p2, p3, color, grosor, opacidad * r.uniform(0.6, 1.0), guiones)

    # -------------------------------------------------------------- nodos
    def celda(self, cx, cy, w, color=TINTA, grosor=1.3, relleno=PAPEL, desague=True, doble=True):
        """La celda de la cabeza del ídolo: 0,84 de ancho por alto, un rectángulo dentro de otro, con desagüe."""
        h = w / 0.84
        x0, y0 = cx - w / 2, cy - h / 2
        self.add("nodos", f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{relleno}" stroke="none"/>')
        rects = [(x0, y0, w, h)]
        if doble:
            rects.append((x0 + 0.18 * w, y0 + 0.13 * h, w * 0.64, h * 0.74))
        for (a, b, ww, hh) in rects:
            m, g = a + ww / 2, min(6.0, ww * 0.08) if desague else 0
            self.add("nodos", f'<path d="M{m + g:.1f},{b + hh:.1f} H{a + ww:.1f} V{b:.1f} H{a:.1f} V{b + hh:.1f} H{m - g:.1f}" '
                              f'fill="none" stroke="{color}" stroke-width="{grosor}"/>')
        return (x0, y0, w, h)

    def circulo(self, cx, cy, r, color=TINTA, grosor=0.9, relleno="none", opacidad=1.0, capa="nodos", guiones=""):
        g = f' stroke-dasharray="{guiones}"' if guiones else ""
        self.add(capa, f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{relleno}" stroke="{color}" '
                       f'stroke-width="{grosor}" opacity="{opacidad}"{g}/>')

    def punto(self, cx, cy, r=2.6, color=TINTA):
        self.add("nodos", f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/>')

    # -------------------------------------------------------------- rayado y vasijas
    def rayado(self, d, caja, paso=3.2, color=VIOLETA, grosor=0.9, transform=""):
        """Rayado vertical recortado a una forma (el rojo de las referencias, aquí violeta)."""
        self.n_clip += 1
        cid = f"clip{self.n_clip}"
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}" transform="{transform}" clip-rule="evenodd"/></clipPath>')
        x0, y0, x1, y1 = caja
        lineas = []
        x = x0
        while x <= x1:
            ya = y0 + self.rng.uniform(-2, 2)
            yb = y1 + self.rng.uniform(-2, 2)
            lineas.append(f'<line x1="{x:.1f}" y1="{ya:.1f}" x2="{x:.1f}" y2="{yb:.1f}"/>')
            x += paso * self.rng.uniform(0.75, 1.25)
        self.add("rayado", f'<g clip-path="url(#{cid})" stroke="{color}" stroke-width="{grosor}">{"".join(lineas)}</g>')

    def cortina(self, x0, x1, base, alturas, colores, grosor=1.0, arriba=True):
        """Líneas verticales que cuelgan (o suben) de una base, una por dato: el análisis de borde."""
        n = len(alturas)
        for i, (a, c) in enumerate(zip(alturas, colores)):
            x = x0 + (x1 - x0) * (i + 0.5) / n
            y1 = base - a if arriba else base + a
            self.linea(x, base, x, y1, c, grosor, 1.0, capa="rayado")

    def cota(self, x0, x1, y, texto, color=GRIS, tam=11):
        """Una cota horizontal, con topes y flechas, como en los planos."""
        self.linea(x0, y - 5, x0, y + 5, color, 0.8, capa="textos")
        self.linea(x1, y - 5, x1, y + 5, color, 0.8, capa="textos")
        self.linea(x0, y, x1, y, color, 0.6, capa="textos")
        for x, s in ((x0, 1), (x1, -1)):
            self.add("textos", f'<path d="M{x:.1f},{y:.1f} l{6 * s},-2.5 v5 z" fill="{color}"/>')
        self.texto((x0 + x1) / 2, y + tam + 4, texto, tam, color, ancla="middle")

    def corchetes(self, x0, y0, x1, y1, color=GRIS):
        for x, s in ((x0, 1), (x1, -1)):
            self.add("textos", f'<path d="M{x + 7 * s:.1f},{y0:.1f} H{x:.1f} V{y1:.1f} H{x + 7 * s:.1f}" fill="none" '
                               f'stroke="{color}" stroke-width="0.9"/>')

    # -------------------------------------------------------------- marco, ficha y folio
    def marco(self, numero, titulo, ficha, fw=380):
        W, H = self.W, self.H
        self.add("fondo", f'<rect width="{W}" height="{H}" fill="{PAPEL}"/>')
        self.add("fondo", f'<rect x="18" y="18" width="{W - 36}" height="{H - 36}" fill="none" stroke="{FILETE}" stroke-width="1"/>')
        self.texto(W - 36, 46, f"contenida · informe de decisiones · mapa {numero} / {TOTAL}", 12, GRIS, ancla="end")
        self.texto(36, 46, "(" + str(numero) + ")", 12, GRIS)
        self.texto(W - 36, H - 34, f"MAPA {numero} · {titulo.upper()}", 13, TINTA, ancla="end", esp=1.6)
        # la ficha, abajo a la derecha, como la de las placas
        fh = 22 * (len(ficha) + 1)
        fx, fy = W - 36 - fw, H - 62 - fh
        self.add("textos", f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{PAPEL}" stroke="{GRIS2}" stroke-width="0.8"/>')
        self.texto(fx + 10, fy + 16, "ficha", 12, TINTA, peso=700)
        for i, (k, v) in enumerate(ficha, 1):
            y = fy + 22 * i
            self.linea(fx, y, fx + fw, y, FILETE, 0.8, capa="textos")
            self.linea(fx + 120, y, fx + 120, y + 22, FILETE, 0.8, capa="textos")
            self.texto(fx + 10, y + 15, k, 11.5, GRIS)
            self.texto(fx + 130, y + 15, v, 11.5, TINTA)
        return fx, fy

    def svg(self):
        orden = ["fondo", "construccion", "rayado", "haces", "nodos", "textos"]
        cuerpo = "\n".join("\n".join(self.capas[c]) for c in orden)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" '
                f'height="{self.H}"><defs>{"".join(self.defs)}</defs>\n{cuerpo}\n</svg>\n')


# ------------------------------------------------------------------ datos del proyecto

def generadores():
    """El cuerpo base de o, l, n y a, en el lienzo de la placa (600 px = 150 mm)."""
    out = {}
    for s in "olna":
        t = (TIPO / "simulacion" / "salida" / "gramatica" / f"{s}.svg").read_text(encoding="utf8")
        d = re.search(r'<path d="([^"]+)"', t).group(1)
        nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
        xs, ys = nums[0::2], nums[1::2]
        out[s] = dict(d=d, caja=(min(xs), min(ys), max(xs), max(ys)))
    return out


def vasija(L, s, g, x, y, escala, rotulo=True):
    """Un generador rayado en violeta, entre corchetes y acotado en milímetros."""
    x0, y0, x1, y1 = g["caja"]
    tr = f"translate({x - x0 * escala:.2f} {y - y0 * escala:.2f}) scale({escala})"
    ancho, alto = (x1 - x0) * escala, (y1 - y0) * escala
    L.rayado(g["d"], (x - 4, y - 4, x + ancho + 4, y + alto + 4), paso=3.0, transform=tr)
    L.add("nodos", f'<path d="{g["d"]}" transform="{tr}" fill="none" stroke="{VIOLETA}" stroke-width="{0.7 / escala:.2f}" '
                   f'fill-rule="evenodd"/>')
    L.corchetes(x - 12, y - 6, x + ancho + 12, y + alto + 6)
    if rotulo:
        L.cota(x - 12, x + ancho + 12, y + alto + 20, f"{s} · {(x1 - x0) / 4:.0f} × {(y1 - y0) / 4:.0f} mm".replace(".", ","))
    return ancho, alto


def fichas_simuladas():
    return json.loads((TIPO / "simulacion" / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))


def construccion(L, cx, cy, radios, rayos=(), color=OBRA):
    for r in radios:
        L.circulo(cx, cy, r, color, 0.8, capa="construccion")
    for ang in rayos:
        a = math.radians(ang)
        R = max(radios) * 1.08
        L.linea(cx - R * math.cos(a), cy - R * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a), color, 0.7,
                capa="construccion")


# ------------------------------------------------------------------ rótulos por tipo

TIPOS = {
    "concepto": dict(color=TINTA, fuente=MONO, estilo="", tam=13.5, ancho=34),
    "teoría": dict(color=TINTA, fuente=MONO, estilo="", tam=13.5, ancho=34),
    "retórica": dict(color=VIOLETA, fuente=MONO, estilo="", tam=13.5, ancho=34),
    "poética": dict(color=VIOLETA, fuente=SERIF, estilo="italic", tam=16.5, ancho=38),
}


def rotulo(L, x, y, tipo, texto, ancla="start", ancho=None):
    """Un rótulo de mapa: el tipo en versalitas grises y el texto. Devuelve el alto que ocupa."""
    t = TIPOS[tipo]
    L.texto(x, y, tipo.upper(), 9.5, GRIS2, ancla=ancla, esp=1.2)
    lineas = partir(texto, ancho or t["ancho"])
    fin = L.bloque(x, y + t["tam"] + 3, lineas, t["tam"], t["color"], t["fuente"], ancla, t["estilo"])
    return fin - y + 10


# ------------------------------------------------------------------ mapa 1: el proyecto entero

ETAPAS = [
    ("La obra", "Contener una ruina, 2026", [
        ("concepto", "Partir del registro, no de la piedra: la lámina del ídolo y su pie"),
        ("concepto", "Todo es un continente, y ninguno retiene lo que le ponen adentro"),
        ("teoría", "La cadena de desplazamientos: cada paso pierde materia y gana luz"),
        ("retórica", "Confesión: el pie admite un dibujo reconstructivo, un calendario sin leer y otro lugar"),
        ("poética", "«Quedó el contenedor / de lo que ya no está.»"),
    ]),
    ("Desenterrar", "acciones 0 a 3", [
        ("concepto", "Del pie, las medidas: 30 signos hallados y 25 por reconstruir"),
        ("teoría", "Nedmural (Tshuma): letras sacadas de un muro, tal como están"),
        ("teoría", "Sankofa: ¿de quién es esta historia?, ¿quién la escribió?"),
        ("retórica", "Sinécdoque: el pie por la lámina. Antítesis: continuo lo hallado, punteado lo reconstruido"),
        ("poética", "«No se salvó la piedra, / solo la opinión sobre ella.»"),
    ]),
    ("Contener", "acciones 4 a 7", [
        ("concepto", "Cada letra es una placa suelta: un tipo móvil de aluminio"),
        ("concepto", "La caja de 8 × 7; lo que no cabe se ve como celda vacía"),
        ("teoría", "La escritura como vasija (Mahendran), pero una que no retiene"),
        ("retórica", "Paradoja hecha forma: toda cuenca se abre abajo, en un desagüe"),
        ("poética", "«ningún contenedor aguanta lo que contiene»"),
    ]),
    ("Devolver", "acciones 8 a 12", [
        ("concepto", "Estados, no pesos: el peso se mide en frotadas"),
        ("teoría", "Transmodalidad y cimática (Mahendran): la voz mueve el agua"),
        ("retórica", "La voz como deformación, no como palabra"),
        ("poética", "«Tocas el agua y la diosa se deforma.»"),
        ("poética", "«la misma diosa dos veces / y ninguna igual»"),
    ]),
    ("Digital", "si cierra", [
        ("concepto", "Un estado más, no el final limpio: vuelve al agua y a la placa"),
        ("teoría", "Objeto, signo y objeto otra vez: la mesa serif (Tshuma)"),
        ("retórica", "El colofón como cadena de custodia: «sin nombre registrado»"),
        ("poética", "«Termina y empieza, / termina y empieza.»"),
    ]),
]


def mapa_1(G):
    L = Lienzo(1200, 1600, 1)
    cx, cy, R = 600, 820, 235
    construccion(L, cx, cy, (R, 390, 560), rayos=(90, 18, -54, 54, -18))
    angulos = [-90, -18, 54, 126, 198]
    nodos = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in angulos]
    # el ciclo de las etapas: termina y empieza
    for i in range(5):
        a0, a1 = math.radians(angulos[i] + 9), math.radians(angulos[(i + 1) % 5] - 9)
        if a1 < a0:
            a1 += 2 * math.pi
        L.add("haces", f'<path d="M{cx + R * math.cos(a0):.1f},{cy + R * math.sin(a0):.1f} A{R},{R} 0 0 1 '
                       f'{cx + R * math.cos(a1):.1f},{cy + R * math.sin(a1):.1f}" fill="none" stroke="{VIOLETA}" stroke-width="1.4"/>')
        ax, ay = cx + R * math.cos(a1), cy + R * math.sin(a1)
        t = a1 + math.pi / 2
        L.add("haces", f'<path d="M{ax:.1f},{ay:.1f} l{-8 * math.cos(t) + 4 * math.cos(a1):.1f},{-8 * math.sin(t) + 4 * math.sin(a1):.1f} '
                       f'M{ax:.1f},{ay:.1f} l{-8 * math.cos(t) - 4 * math.cos(a1):.1f},{-8 * math.sin(t) - 4 * math.sin(a1):.1f}" '
                       f'stroke="{VIOLETA}" stroke-width="1.4" fill="none"/>')
    L.texto(cx, cy + R - 20, "termina y empieza", 12, VIOLETA, ancla="middle")
    # el centro
    L.celda(cx, cy, 230, TINTA, 1.6)
    L.texto(cx, cy - 6, "Contenida", 30, TINTA, SERIF, "middle", peso=300)
    L.texto(cx, cy + 20, "acciones para", 12, GRIS, ancla="middle")
    L.texto(cx, cy + 36, "componer una voz", 12, GRIS, ancla="middle")
    # dónde van los rótulos de cada etapa
    zonas = [
        ("arriba", 330, 870, 96, 430),
        ("derecha", 860, 1165, 370, 800),
        ("derecha", 860, 1165, 900, 1330),
        ("izquierda", 35, 340, 900, 1330),
        ("izquierda", 35, 340, 400, 800),
    ]
    for (nombre, sub, items), (nx, ny), (lado, xa, xb, ya, yb) in zip(ETAPAS, nodos, zonas):
        L.celda(nx, ny, 70, VIOLETA, 1.3)
        L.texto(nx, ny + 60, nombre, 17, TINTA, SERIF, "middle", peso=500)
        L.texto(nx, ny + 76, sub, 11, GRIS, ancla="middle")
        # posiciones de los rótulos
        if lado == "arriba":
            cols = [(xa, ya), (xa + 290, ya)]
            pos, fila = [], [0, 0]
            for i, it in enumerate(items):
                c = i % 2
                pos.append((cols[c][0], cols[c][1] + fila[c]))
                fila[c] += 118 if it[0] == "retórica" else 92
        else:
            paso = (yb - ya) / len(items)
            pos = [(xa if lado == "derecha" else xb, ya + i * paso) for i in range(len(items))]
        nudo = (nx + (0 if lado == "arriba" else (70 if lado == "derecha" else -70)),
                ny - (95 if lado == "arriba" else 0))
        for (tipo, texto), (x, y) in zip(items, pos):
            ancla = "end" if lado == "izquierda" else "start"
            alto = rotulo(L, x, y, tipo, texto, ancla, ancho=30 if lado == "arriba" else None)
            destino = (x - 8 if ancla == "start" else x + 8, y + 10)
            if lado == "arriba":
                destino = (x + 40, y + alto - 6)
            L.haz((nx, ny - (0 if lado != "arriba" else 42)), nudo, destino, hebras=7, abre=14,
                  color=VIOLETA if tipo in ("retórica", "poética") else TINTA)
    # las cuatro vasijas: los generadores, abajo, como en el plano de referencia
    x = 70
    for s in "olna":
        a, _ = vasija(L, s, G[s], x, 1395, 0.22)
        x += a + 70
    L.texto(70, 1372, "las cuatro vasijas: los generadores de la gramática", 11.5, GRIS)
    L.marco(1, "El proyecto entero", [("etapas", "5, en ciclo"), ("rótulos", "24"),
                                        ("tipos", "concepto, teoría, retórica, poética"),
                                        ("tinta", "violeta del esténcil"), ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ mapa 2: teoría y fuentes

FUENTES_T = [
    # nombre, año, x, y, radio
    ("EthnoGraphemes", "Mahendran, 2020", 150, 300, 78),
    ("Afrography", "Tshuma, 2025", 150, 880, 78),
    ("Tihuanacu", "Posnansky, 1945", 1450, 290, 62),
    ("La iconografía Tiwanaku", "Agüero, Uribe y Berenguer, 2003", 1455, 880, 54),
    ("Contener una ruina", "Rebeca Paz Prada, 2026", 800, 150, 58),
]
TOMA = [
    # fuente, texto, columna, fila (en la caja de 8 × 7; solo columnas impares: cada rótulo ocupa dos)
    (0, "la escritura como vasija, que aquí no retiene", 1, 1),
    (0, "transmodalidad: la letra se toca, se moja", 1, 2),
    (0, "cimática → el estado Voz", 1, 3),
    (0, "caja baja: la letra de la mano (Brookes)", 1, 4),
    (0, "contra el exotismo: ningún motivo pegado (Morcos)", 3, 1),
    (0, "el diccionario de cartas → la caja de placas", 3, 2),
    (0, "Ellipsis: lo inacabado → el signo …", 3, 3),
    (0, "la ética del que viene de afuera → Acción 0", 3, 4),
    (1, "sankofa: ¿quién lo escribió?", 1, 5),
    (1, "Nedmural: letras sacadas de un muro → el pie", 1, 6),
    (1, "The Great Stone: la restricción de la ruina", 1, 7),
    (1, "la cabeza de Oba → el colofón como custodia", 3, 5),
    (1, "tres cuadernos → Desenterrar, Contener, Devolver", 3, 6),
    (1, "objeto → signo → objeto: la vuelta a la placa", 3, 7),
    (1, "herramientas libres; la economía del trabajo", 5, 6),
    (1, "la transformación: la placa rota no se corrige", 5, 7),
    (2, "La Paz contiene la ruina", 7, 1),
    (2, "la cloaca máxima hecha piso: el desagüe", 7, 2),
    (2, "el agua que se fue: la piscina vacía", 7, 3),
    (2, "el asperón, elegido por blando: el material decide", 5, 1),
    (2, "lo que no está se reconstruye: el punteado", 5, 2),
    (3, "elementos → motivos → figuras: partes → signos", 7, 4),
    (3, "dobles opuestos con variación: la ¿ no es la ? al revés", 7, 5),
    (3, "Personaje Frontal en pecho y espalda (D4)", 7, 6),
    (3, "cabezas de pez de perfil (D7)", 7, 7),
    (4, "partir del registro: el pie de la lámina", 5, 3),
    (4, "el aluminio, la cinta, el agua, la voz", 5, 4),
    (4, "la piscina vacía: escenario y pantalla", 5, 5),
]
NO_TOMA = [
    (0, "revitalizar una lengua", 40, 470, "start"),
    (0, "una frecuencia por letra", 40, 495, "start"),
    (0, "tatuar: se queda en el esténcil", 40, 520, "start"),
    (1, "inventar una escritura", 40, 1010, "start"),
    (1, "el estallido: el agua vuelve", 40, 1035, "start"),
    (1, "letras hechas con módulos", 40, 1060, "start"),
    (2, "su cronología", 1570, 445, "end"),
    (2, "su tesis del título", 1570, 470, "end"),
    (2, "su lectura racial de la historia", 1570, 495, "end"),
    (3, "interpretar la iconografía", 1170, 962, "end"),
    (3, "traducir el «calendario»", 1170, 986, "end"),
    (4, "las lecturas rituales", 735, 120, "end"),
    (4, "las fotos y el cuerpo de Rebeca", 735, 145, "end"),
]


def mapa_2():
    L = Lienzo(1600, 1200, 2)
    # el plano: la caja de 8 × 7 en líneas finas, como las manzanas de un plano
    gx0, gy0, gw, gh = 330, 250, 940, 700
    cw, ch = gw / 8, gh / 7
    for i in range(9):
        L.linea(gx0 + i * cw, gy0 - 30, gx0 + i * cw, gy0 + gh + 30, OBRA, 0.9, capa="construccion")
    for j in range(8):
        L.linea(gx0 - 30, gy0 + j * ch, gx0 + gw + 30, gy0 + j * ch, OBRA, 0.9, capa="construccion")
    for i in range(8):
        for j in range(7):
            L.add("construccion", f'<rect x="{gx0 + i * cw + 0.18 * cw:.1f}" y="{gy0 + j * ch + 0.13 * ch:.1f}" '
                                  f'width="{0.64 * cw:.1f}" height="{0.74 * ch:.1f}" fill="none" stroke="{OBRA}" stroke-width="0.6"/>')
    # el hilo del proyecto: una curva oscura que cruza la caja
    L.add("haces", f'<path d="M{gx0 - 60},{gy0 + gh * 0.55} C{gx0 + 200},{gy0 + gh * 0.2} {gx0 + 420},{gy0 + gh * 0.95} '
                   f'{gx0 + 620},{gy0 + gh * 0.5} S{gx0 + gw - 60},{gy0 + gh * 0.25} {gx0 + gw + 10},{gy0 + gh * 0.45}" '
                   f'fill="none" stroke="{TINTA}" stroke-width="2.2"/>')
    for k in range(4):
        d = (k - 1.5) * 4
        L.add("haces", f'<path d="M{gx0 - 60},{gy0 + gh * 0.55 + d} C{gx0 + 200},{gy0 + gh * 0.2 + d} {gx0 + 420},{gy0 + gh * 0.95 + d} '
                       f'{gx0 + 620},{gy0 + gh * 0.5 + d} S{gx0 + gw - 60},{gy0 + gh * 0.25 + d} {gx0 + gw + 10},{gy0 + gh * 0.45 + d}" '
                       f'fill="none" stroke="{VIOLETA}" stroke-width="0.6" opacity=".7"/>')
    L.bloque(gx0 - 60, gy0 + gh * 0.55 + 24, ["el hilo: obra → pie → gramática", "→ estados → digital"], 12, TINTA)
    # las fuentes: círculos en el borde; lo que se toma, puntos en la caja
    for f, (nombre, autor, x, y, r) in enumerate(FUENTES_T):
        L.circulo(x, y, r, TINTA, 1.1, PAPEL)
        L.circulo(x, y, r * 0.18, VIOLETA, 0, VIOLETA)
        if f == 4:                                   # la obra: el nombre a la derecha del círculo
            L.texto(x + r + 16, y - 4, nombre, 17, TINTA, SERIF, estilo="italic")
            L.texto(x + r + 16, y + 16, autor, 11.5, GRIS)
            continue
        lineas = partir(nombre, 16)
        for k, l in enumerate(lineas):
            L.texto(x, y - r - 14 - (len(lineas) - 1 - k) * 18, l, 16, TINTA, SERIF, "middle", "italic")
        L.texto(x, y + r + 18, autor, 11.5, GRIS, ancla="middle")
    for f, texto, col, fila in TOMA:
        px = gx0 + (col - 1) * cw + 14
        py = gy0 + (fila - 0.5) * ch - 14
        _, _, fx, fy, fr = FUENTES_T[f]
        for _ in range(3):
            a = math.atan2(py - fy, px - fx) + L.rng.uniform(-0.35, 0.35)
            L.linea(fx + fr * math.cos(a), fy + fr * math.sin(a), px, py, VIOLETA, 0.55, 0.6)
        L.punto(px, py, 2.8, VIOLETA)
        lineas = partir(texto, 27)
        L.bloque(px + 7, py + 4, lineas, 11.5, TINTA, fondo=True, inter=1.2)
    for f, texto, x, y, ancla in NO_TOMA:
        _, _, fx, fy, fr = FUENTES_T[f]
        largo = len("no: " + texto) * 6.9
        xl = x + largo + 6 if ancla == "start" else x - largo - 6
        a = math.atan2(y - 4 - fy, xl - fx)
        L.linea(fx + fr * math.cos(a), fy + fr * math.sin(a), xl, y - 4, GRIS2, 0.7, 0.9, "3 4")
        L.texto(x, y, "no: " + texto, 11.5, GRIS, ancla=ancla)
    L.texto(gx0, gy0 - 46, "lo que se toma, sobre la caja de 8 × 7", 12, VIOLETA)
    L.texto(gx0 + gw, gy0 - 46, "- - -  lo que no se toma", 12, GRIS, ancla="end")
    L.marco(2, "Teoría y fuentes", [("fuentes", "5 y el poema"), ("se toma", f"{len(TOMA)} ideas"),
                                      ("no se toma", f"{len(NO_TOMA)}"), ("plano", "la caja de 8 × 7"),
                                      ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ mapa 3: la obra, decisión por decisión

DECISIONES = [
    ("D1", "Partir de la lámina y no de la piedra", "Las letras salen del pie de la lámina"),
    ("D2", "Asperón → papel de aluminio", "Matrices de aluminio repujado; solo caja baja"),
    ("D3", "Placas sueltas, con piel entre ellas", "Cada letra es un tipo móvil; entre palabras, la piel"),
    ("D4", "Puertas en el pecho y la espalda", "La tapa de la caja: una puerta sobre la celda 1"),
    ("D5", "Iconografía interpretada, no copiada", "Del monolito, solo la retícula y la celda vacía"),
    ("D6", "La piscina vacía, en un estudio de tatuajes", "Fondo, borde, desagüe; el violeta del esténcil"),
    ("D7", "Placas en el fondo, como peces", "No se dibujan peces: las letras ya lo parecen"),
    ("D8", "La bandeja con un dedo de agua", "El estado Agua: se lee reflejada"),
    ("D9", "Escenario, pantalla y tema", "La pared frotada es el papel del calco"),
    ("D10", "El bucle", "Frotar hasta que no se lea, y repujar otra"),
    ("D11", "Moverse como la piedra: apenas", "El temblor de la mano; fustes de tres planos a 1,6°"),
    ("D12", "Ojos y boca tapados con cinta", "No hay Regular; el estado Cinta; el punto de cinta"),
    ("D13", "De la boca sale una placa", "El signo final ¶, hecho con los dedos"),
    ("D14", "Un canto que no se entiende", "El estado Voz: la voz deforma, no se graba"),
    ("D15", "Tocar el agua deforma la imagen", "El agua tocada; en lo digital, tocar deforma"),
    ("D16", "El líquido que chorrea de la boca", "Toda cuenca se abre abajo; solo gotea lo que mira abajo"),
]
CADENA = ["piedra borrada", "fotografía vieja", "dibujo reconstructivo", "escaneo", "repujado en aluminio", "cuerpo",
          "video", "charco", "pared de azulejo"]


def mapa_3():
    L = Lienzo(1200, 1600, 3)
    # la espina: la cadena de desplazamientos, una S que baja
    pts = []
    for i in range(200):
        t = i / 199
        pts.append((600 + 210 * math.sin(t * math.pi * 2.1 + 0.3), 150 + t * 1260))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    L.add("haces", f'<path d="{d}" fill="none" stroke="{TINTA}" stroke-width="2"/>')
    for k in range(5):
        dd = (k - 2) * 3.2
        L.add("haces", f'<path d="{"M" + " L".join(f"{x + dd:.1f},{y:.1f}" for x, y in pts)}" fill="none" '
                       f'stroke="{VIOLETA}" stroke-width="0.5" opacity=".7"/>')
    for i, c in enumerate(CADENA):
        x, y = pts[int(i * 199 / (len(CADENA) - 1))]
        L.punto(x, y, 4, VIOLETA)
        adentro = x > 600
        L.bloque(x + (-14 if adentro else 14), y + 22, [c], 12, VIOLETA, ancla="end" if adentro else "start")
    L.texto(600, 118, "la cadena de desplazamientos: cada paso pierde materia y gana luz", 12.5, TINTA, ancla="middle")
    # las decisiones: nodos sobre la espina, haces hacia su traducción
    for i, (n, obra, tipo) in enumerate(DECISIONES):
        t = (i + 0.5) / len(DECISIONES)
        x, y = pts[int(t * 199)]
        L.celda(x, y, 26, TINTA, 1.0)
        izquierda = i % 2 == 0
        tx = 70 if izquierda else 1130
        ty = 175 + i * 76
        L.haz((x, y), (x + (-60 if izquierda else 60), y + 6), (tx + (262 if izquierda else -262), ty + 16), hebras=9,
              color=TINTA, abre=16, opacidad=0.5)
        ancla = "start" if izquierda else "end"
        L.texto(tx, ty, n, 13, VIOLETA, ancla=ancla, peso=700)
        L.bloque(tx + (38 if izquierda else -38), ty, partir(obra, 30), 12, GRIS, ancla=ancla, inter=1.2)
        L.bloque(tx, ty + 20 + (len(partir(obra, 30)) - 1) * 14, partir(tipo, 36), 13.5, TINTA, ancla=ancla, inter=1.2)
    L.texto(70, 150, "la obra · su traducción en Contenida", 12, GRIS)
    L.marco(3, "La obra, decisión por decisión", [("decisiones", "16 (D1 a D16)"), ("espina", "la cadena de la obra"),
                                                    ("gris", "lo que hizo la obra"), ("tinta", "lo que hace la letra"),
                                                    ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ mapa 4: del pie a los 55 signos

PIE = ["EL IDOLO KOCHAMAMA, según Posnansky, presentado en amplio detalle reconstructivo, según",
       "viejas fotografías (hoy está muy erosionado y casi no se ven esos detalles). Su calendario, todavía",
       "no bien interpretado, es distinto del de la Puerta del Sol y muestra motivos mucho más antiguos.",
       "Suponemos que originariamente se encontraba en Pumapuncu, en el lugar en donde luego se puso la Puerta de la Luna."]
MEDIDAS = ["altura de x: ascendentes 1,71 veces la x (la foto)", "grueso 11,2 mm y fino 7,0 mm de la o: canal 8,9 mm",
           "las astas, los ojos y las cajas de cada testigo", "afuera 94,1 · borde 54,8 · fondo 0 · desagüe −30,2 mm"]
OBRA_FORMA = [("el punzón sobre el aluminio", "D2"), ("la vasija abierta", "D16"), ("la chapa sobre el cuerpo", "D3"),
              ("la intemperie", "el pie"), ("la gravedad", "D16"), ("la cinta de ojos y boca", "D12")]
PARAMS = ["canal 8,9 mm", "radio_chapa 0,6 canal", "trapecio 0,70", "pared 0,55", "desagüe 3 mm", "hombro 3",
          "hombro_caida 0,40", "facetas 3 · quiebre 1,6°", "asiento 2 × 0,9 canal", "intemperie 0,12 canal",
          "alivio 0,28 canal", "gancho_fin 105°", "gota 1,25 · 0,3 · 0,55 canal", "sifón 0,6 canal",
          "cinta 1 canal · punto 1 canal"]
PARTES = ["fuste", "cuenca", "hombro", "gancho", "gota", "asiento", "punto", "tilde", "onda", "recta", "alivio", "sifón"]


def mapa_4(G):
    L = Lienzo(1200, 1600, 4)
    construccion(L, 600, 760, (300, 520), rayos=(90, 0, 45, -45))
    # el pie, arriba, en letra chica
    for i, l in enumerate(PIE):
        L.texto(70, 110 + i * 17, l, 11, GRIS)
    L.texto(70, 88, "el pie de la lámina (la foto da medidas, no formas)", 12, TINTA)
    # del pie, las medidas: un nudo a la izquierda
    nudo_m = (300, 420)
    for i, m in enumerate(MEDIDAS):
        y = 250 + i * 32
        L.haz((110 + i * 240, 170), (nudo_m[0] - 20, nudo_m[1] - 60), (nudo_m[0] + 0, nudo_m[1] - 8), hebras=5,
              color=GRIS, opacidad=0.45)
    L.celda(nudo_m[0], nudo_m[1], 54, TINTA, 1.2)
    L.texto(nudo_m[0] - 40, nudo_m[1] + 6, "del pie, las medidas", 14, TINTA, ancla="end", peso=700)
    for i, m in enumerate(MEDIDAS):
        L.bloque(70, 520 + i * 36, partir(m, 34), 12.5, TINTA)
        L.haz(nudo_m, (nudo_m[0] - 30, nudo_m[1] + 60), (330, 516 + i * 36), hebras=3, color=TINTA, opacidad=0.5)
    # de la obra, la forma: un nudo a la derecha
    nudo_o = (900, 420)
    L.celda(nudo_o[0], nudo_o[1], 54, VIOLETA, 1.2)
    L.texto(nudo_o[0] + 40, nudo_o[1] + 6, "de la obra, la forma", 14, VIOLETA, peso=700)
    for i, (f, dd) in enumerate(OBRA_FORMA):
        y = 230 + i * 30
        L.texto(1130, y, f"{f} ({dd})", 12.5, VIOLETA, ancla="end")
        L.haz((1130 - len(f + dd) * 7.8 - 30, y - 4), (nudo_o[0] + 30, nudo_o[1] - 50), nudo_o, hebras=3, color=VIOLETA,
              opacidad=0.5)
    # los parámetros: la columna del centro
    px, py = 600, 330
    L.texto(px, py - 26, "20 parámetros", 15, TINTA, SERIF, "middle", "italic")
    for i, p in enumerate(PARAMS):
        y = py + i * 25
        L.bloque(px, y, [p], 12, TINTA, ancla="middle")
        for (nx, ny), c in ((nudo_m, TINTA), (nudo_o, VIOLETA)):
            if (i % 3 == 0 and c == TINTA) or (i % 2 == 1 and c == VIOLETA) or i == 0:
                L.curva((nx, ny), (nx + (px - nx) * 0.5, ny), (px + (nx - px) * 0.4, y - 4), (px + (95 if nx > px else -95), y - 4),
                        c, 0.5, 0.45)
    # las partes: un abanico hacia abajo
    nudo_p = (600, 760)
    L.punto(*nudo_p, 5, TINTA)
    for i in range(len(PARAMS)):
        L.curva((px, py + i * 25 + 6), (px + (i - 7) * 4, 700), (nudo_p[0], nudo_p[1] - 40), nudo_p, TINTA, 0.45, 0.4)
    L.texto(nudo_p[0] + 14, nudo_p[1] + 5, "las partes", 14, TINTA, peso=700)
    for i, p in enumerate(PARTES):
        a = math.radians(200 + i * (140 / (len(PARTES) - 1)))
        x, y = nudo_p[0] + 250 * math.cos(-a + math.pi), nudo_p[1] + 120 + 110 * math.sin(-a + math.pi) * 0.8
        x = 180 + i * (840 / (len(PARTES) - 1))
        y = 880 + (35 if i % 2 else 0)
        L.haz(nudo_p, (nudo_p[0], nudo_p[1] + 40), (x, y - 14), hebras=4, color=TINTA, opacidad=0.5)
        L.bloque(x, y, [p], 13, TINTA, ancla="middle")
    # los cuatro generadores: vasijas rayadas, acotadas
    L.texto(70, 975, "cuatro generadores dan las partes; con ellas se arman los 55 signos", 12.5, TINTA)
    x, bases = 120, []
    for s_ in "olna":
        a, h = vasija(L, s_, G[s_], x, 1010, 0.36)
        bases.append((x + a / 2, 1010 + h + 44))
        x += a + 150
    # los 55: una caja de 8 × 7 chiquita, abajo
    cx0, cy0, lado = 470, 1262, 30
    nudo = (cx0 + 4 * (lado + 4) - 2, cy0 - 36)
    for bx, by in bases:
        L.haz((bx, by), (bx + (nudo[0] - bx) * 0.5, by + 12), nudo, hebras=5, color=VIOLETA, opacidad=0.45, abre=4)
    L.haz(nudo, (nudo[0], nudo[1] + 12), (nudo[0], cy0 - 2), hebras=6, color=VIOLETA, opacidad=0.45, abre=40)
    for c in json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))["celdas"]:
        x = cx0 + (c["columna"] - 1) * (lado + 4)
        y = cy0 + (c["fila"] - 1) * (lado + 4)
        color = TINTA if c["estado"] == "hallada" else VIOLETA if c["estado"] == "reconstruida" else GRIS2
        L.add("nodos", f'<rect x="{x}" y="{y}" width="{lado}" height="{lado}" fill="{PAPEL}" stroke="{FILETE}" stroke-width="0.8"/>')
        L.texto(x + lado / 2, y + lado * 0.68, c["signo"], 16, color, SERIF, "middle")
    lx = cx0 + 8 * (lado + 4) + 16
    L.texto(lx, cy0 + 16, "30 hallados", 12, TINTA)
    L.texto(lx, cy0 + 34, "25 reconstruidos", 12, VIOLETA)
    L.texto(lx, cy0 + 52, "1 con los dedos", 12, GRIS)
    L.texto(lx, cy0 + 76, "la caja de 8 × 7", 12, GRIS)
    L.marco(4, "Del pie a los 55 signos", [("del pie", "medidas, no formas"), ("de la obra", "la forma"),
                                            ("parámetros", "20 y la altura de x"), ("generadores", "o, l, n, a"),
                                            ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ mapa 5: la cadena de estados

ESTADOS = [
    ("pie", "el registro", ["la foto mide; el sustituto da la forma", "D1"], "«le pusieron nombre, / otra manera de enterrar»"),
    ("calco", "acción 3", ["continuo lo hallado, punteado lo reconstruido", "sobre el frotado de la pared", "D9"],
     "«No se salvó la piedra, / solo la opinión sobre ella.»"),
    ("placa", "acción 4", ["punzón de bola de 1 mm, por el reverso", "119 placas · 12 rotas", "D2 · D3"],
     "«de la boca sale un signo / hecho con las manos»"),
    ("cinta", "acción 6", ["masking sobre plástico negro", "no curva: se pliega", "D12"],
     "«A la boca la taparon, a las manos no,»"),
    ("frotado", "acción 8", ["papel y grafito: cada frotada aplasta", "el peso se mide en frotadas", "D10"],
     "«otra manera de enterrar»"),
    ("agua", "acción 9", ["la placa en una bandeja", "llega al revés y en trapecio", "D8 · D15"],
     "«Tocas el agua y la diosa se deforma.»"),
    ("voz", "acción 10", ["ondas de Faraday, a la mitad de la frecuencia", "no es tu voz", "D14"],
     "«pocas veces vuelve hablado»"),
    ("digital", "si cierra", ["un estado más", "vuelve al agua y a la placa: generación 2", "D10"],
     "«Termina y empieza»"),
]


def mapa_5():
    L = Lienzo(1600, 1200, 5)
    F = fichas_simuladas()
    y0 = 470
    xs = [120 + i * 194 for i in range(len(ESTADOS))]
    # materia arriba (baja), luz abajo (sube): la cadena pierde materia y gana luz
    n = len(xs)
    for i, x in enumerate(xs):
        materia = 100 * (1 - i / (n - 1)) + 18
        luz = 18 + 100 * i / (n - 1)
        for k in range(14):
            xx = x - 40 + k * 6
            L.linea(xx, y0 - 72, xx, y0 - 72 - materia * L.rng.uniform(0.75, 1.0), VIOLETA, 1.0, 0.9, capa="rayado")
            L.linea(xx, y0 + 72, xx, y0 + 72 + luz * L.rng.uniform(0.75, 1.0), GRIS2, 0.8, 0.9, capa="rayado")
    L.texto(40, y0 - 150, "materia", 12, VIOLETA)
    L.texto(40, y0 + 160, "luz", 12, GRIS)
    L.linea(xs[0] - 60, y0, xs[-1] + 60, y0, TINTA, 1.6)
    for i, (nombre, accion, notas, verso) in enumerate(ESTADOS):
        x = xs[i]
        L.celda(x, y0, 56, VIOLETA if nombre not in ("pie", "digital") else TINTA, 1.3)
        L.bloque(x, y0 - 46, [nombre], 18, TINTA, SERIF, "middle")
        L.texto(x, y0 + 50, accion, 11, GRIS, ancla="middle")
        arriba = i % 2 == 0
        ty = 100 if arriba else 740
        yy = ty
        for nt in notas:
            yy = L.bloque(x, yy, partir(nt, 22), 12, TINTA, ancla="middle", inter=1.2) + 18
        fin = L.bloque(x, yy + 6, partir(verso, 24), 14.5, VIOLETA, SERIF, "middle", "italic", inter=1.15)
        if arriba:
            L.haz((x, y0 - 70), (x, y0 - 200), (x, fin + 10), hebras=5, color=TINTA, opacidad=0.4, abre=12)
        else:
            L.haz((x, y0 + 40), (x, y0 + 200), (x, ty - 20), hebras=5, color=TINTA, opacidad=0.4, abre=12)
    # la vuelta: de lo digital a la placa (esténcil → repujado)
    xa, xb = xs[-1], xs[2]
    L.add("haces", f'<path d="M{xa},{y0 + 34} C{xa},{y0 + 250} {xb},{y0 + 250} {xb},{y0 + 34}" fill="none" '
                   f'stroke="{VIOLETA}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    L.bloque((xa + xb) / 2, y0 + 200, ["termina y empieza: esténcil → placa nueva (generación 2)"], 12, VIOLETA, ancla="middle")
    # el frotado, por signo: la cortina de las frotadas legibles
    x0, x1, base = 330, 1180, 1072
    datos = sorted(((v["celda"], v["frotado"]["legibles"], v["estado"]) for v in F.values() if v["variante"] == 1),
                   key=lambda t: t[0])
    L.cortina(x0, x1, base, [f * 4.0 for _, f, _ in datos],
              [TINTA if e == "hallada" else VIOLETA if e == "reconstruida" else GRIS2 for _, _, e in datos], grosor=1.8)
    L.linea(x0, base, x1, base, GRIS, 0.8)
    L.texto(x0, base + 20, "frotadas legibles de cada celda, de la 1 a la 56", 12, TINTA)
    L.texto(x0, base + 38, "en tinta las halladas (22,1 en promedio); en violeta las reconstruidas (9,8)", 11.5, GRIS)
    L.marco(5, "La cadena de estados", [("estados", "6, más el pie y lo digital"), ("arriba", "la materia que se pierde"),
                                         ("abajo", "la luz que se gana"), ("datos", "fichas_simuladas.json"),
                                         ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ mapa 6: retórica y poética

FIGURAS = [
    ("anáfora y gradación", "«es decir, apenas, es decir, temblor»"),
    ("paradoja", "ningún contenedor aguanta lo que contiene"),
    ("derivación", "enterrar, desenterrar, contener, contenida"),
    ("apóstrofe", "«Tocas el agua»: le habla a quien mira"),
    ("prosopopeya", "«La tierra se dio de beber a sí misma»"),
    ("repetición y ciclo", "«termina y empieza, / termina y empieza»"),
    ("antítesis", "vuelve escrito / vuelve hablado; hallado / reconstruido"),
    ("metáfora", "la letra es una vasija; sus líneas tienen nombres de vasija"),
    ("sinécdoque y metonimia", "el pie por la lámina; la cinta por el rostro tapado"),
    ("elipsis", "lo que falta se ve vacío: la celda del .notdef, el …"),
    ("etimología", "portada y puerta; el ojo del tipo; componer; el calderón"),
    ("sentencia", "«Todos los archivos funcionan así»"),
    ("interrogación retórica", "«Es lo que hacemos con todo, no?»"),
]
OPERACIONES = [
    ("el temblor de la mano; tres planos a 1,6°", [0]),
    ("toda cuenca se abre en un desagüe", [1, 4]),
    ("el nombre no es Kochamama", [2, 7]),
    ("el agua tocada; tocar deforma el espécimen", [3]),
    ("la gota: solo gotea lo que mira abajo", [4]),
    ("el bucle; frotar y repujar otra; generación 2", [5]),
    ("continuo y punteado en todos los estados", [6]),
    ("fondo, borde, desagüe, afuera", [7]),
    ("las letras salen del pie; el punto de cinta", [8]),
    ("la celda vacía; lo que no cabe", [9]),
    ("la puerta sobre la celda 1; no hay Regular; ¶", [10]),
    ("el estado Voz: deforma, no se graba", [6]),
    ("de la piscina no se saca nada", [11]),
    ("la ? se arma sin modelo; la ¿ no es su espejo", [12]),
]
VERSO_FIGURA = {
    "moverse como se mueve la piedra,": [0], "es decir, apenas, es decir, temblor,": [0], "es decir, un presente continuo.": [0],
    "y ningún contenedor aguanta lo que contiene.": [1], "quedó el contenedor": [1, 7], "de lo que ya no está.": [1],
    "a la ídolo la desenterraron,": [2], "otra manera de enterrar.": [2], "desenterrar una voz": [2],
    "tocas el agua y la diosa se deforma.": [3], "la tierra se dio de beber a sí misma": [4],
    "termina y empieza,": [5], "termina y empieza.": [5], "vuelve sin que la llames.": [5], "cada vuelta pasa por el agua": [5],
    "y es que lo que vuelve, vuelve escrito;": [6], "pocas veces vuelve hablado.": [6],
    "primero enterramos,": [6], "después nos emocionamos.": [6],
    "una piscina vacía,": [7], "le pusieron nombre,": [7], "a la boca la taparon, a las manos no,": [8, 6],
    "donde una vez aprendí a flotar,": [6], "ahora aprendo a mirar.": [6],
    "todos los archivos funcionan así.": [11], "nos fuimos con las manos secas,": [11],
    "que es como se sale de todas las ruinas.": [11], "es lo que hacemos con todo, no?": [12],
    "es lo más parecido a estar viva": [4], "que puede hacer una imagen.": [4],
    "es desenterrar la mano del que la escribió.": [2],
    "no se salvó la piedra,": [8], "solo la opinión sobre ella.": [8],
    "no tiene lengua pero igual dice.": [9], "ninguna palabra,": [9],
    "de la boca sale un signo": [10], "hecho con las manos,": [10], "al final del ciclo,": [10, 5],
    "la misma diosa dos veces": [5, 6], "y ninguna igual.": [6],
}


def mapa_6():
    L = Lienzo(1200, 1600, 6)
    versos = [v for v in (TIPO / "textos" / "poema.txt").read_text(encoding="utf8").lower().split("\n")]
    construccion(L, 610, 820, (330, 560), rayos=(0, 90))
    # los versos: una columna a la izquierda, con los blancos entre estrofas
    y, pos = 110, {}
    for v in versos:
        if not v.strip():
            y += 12
            continue
        pos[v.strip()] = y
        L.texto(60, y, v.strip(), 13.5, VIOLETA if v.strip() in VERSO_FIGURA else GRIS2, SERIF, estilo="italic")
        y += 29
    L.texto(60, 80, "el poema, verso a verso", 12, GRIS)
    # las figuras: nudos al centro
    fx = 640
    fys = [150 + i * 98 for i in range(len(FIGURAS))]
    for i, (fig, ej) in enumerate(FIGURAS):
        L.punto(fx - 30, fys[i], 4.5, TINTA)
        L.texto(fx - 16, fys[i] + 5, fig, 15, TINTA, peso=700)
        L.bloque(fx - 16, fys[i] + 24, partir(ej, 30), 11.5, GRIS, inter=1.2)
    for v, figs in VERSO_FIGURA.items():
        if v not in pos:
            continue
        largo = len(v) * 6.4
        for f in figs:
            L.haz((60 + largo + 10, pos[v] - 5), (60 + largo + 60, pos[v] - 5), (fx - 36, fys[f]), hebras=4,
                  color=VIOLETA, opacidad=0.45, abre=5)
    # las operaciones: a la derecha
    ox = 1150
    for j, (op, figs) in enumerate(OPERACIONES):
        oy = 170 + j * 88
        L.bloque(ox, oy, partir(op, 26), 13, TINTA, ancla="end", inter=1.2)
        for f in figs:
            L.haz((fx + 175, fys[f]), (fx + 230, fys[f]), (ox - 200, oy - 4), hebras=4, color=TINTA, opacidad=0.45, abre=5)
    L.texto(ox, 130, "lo que hace la letra", 12, GRIS, ancla="end")
    L.texto(fx - 16, 115, "las figuras", 12, GRIS)
    L.marco(6, "Retórica y poética", [("versos", f"{len(pos)} del poema"), ("figuras", f"{len(FIGURAS)}"),
                                       ("operaciones", f"{len(OPERACIONES)}"), ("violeta", "los versos que operan"),
                                       ("fecha", FECHA)])
    return L


# ------------------------------------------------------------------ salida

def html(svg, W, H):
    caras = "".join(
        f'@font-face{{font-family:"{fam}";src:url("{(FUENTES / arch).as_uri()}") format("woff2");'
        f'font-weight:{peso};font-style:{est}}}'
        for fam, arch, peso, est in (
            ("Courier Prime", "courier-prime-latin-400-normal.woff2", 400, "normal"),
            ("Courier Prime", "courier-prime-latin-700-normal.woff2", 700, "normal"),
            ("Courier Prime", "courier-prime-latin-400-italic.woff2", 400, "italic"),
            ("Newsreader", "newsreader-latin-300-normal.woff2", 300, "normal"),
            ("Newsreader", "newsreader-latin-400-normal.woff2", 400, "normal"),
            ("Newsreader", "newsreader-latin-500-normal.woff2", 500, "normal"),
            ("Newsreader", "newsreader-latin-400-italic.woff2", 400, "italic"),
            ("Newsreader", "newsreader-latin-300-italic.woff2", 300, "italic")))
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{caras}html,body{{margin:0;background:{PAPEL}}}'
            f'svg{{display:block;width:{W}px;height:{H}px}}</style></head><body>{svg}</body></html>')


def main():
    from generar_laminas import chrome
    SALIDA.mkdir(exist_ok=True)
    G = generadores()
    mapas = [("el_proyecto_entero", mapa_1(G)), ("teoria_y_fuentes", mapa_2()), ("la_obra_decision_por_decision", mapa_3()),
             ("del_pie_a_los_55", mapa_4(G)), ("la_cadena_de_estados", mapa_5()), ("retorica_y_poetica", mapa_6())]
    ejecutable = chrome()
    modo = [] if ejecutable.endswith("headless_shell") else ["--headless=new"]
    for i, (nombre, L) in enumerate(mapas, 1):
        svg = L.svg()
        base = SALIDA / f"mapa_{i}_{nombre}"
        base.with_suffix(".svg").write_text(svg, encoding="utf8")
        pagina = SALIDA / f".mapa_{i}.html"
        pagina.write_text(html(svg, L.W, L.H), encoding="utf8")
        subprocess.run([ejecutable, *modo, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--allow-file-access-from-files", "--virtual-time-budget=5000",
                        f"--window-size={L.W},{L.H}", f"--screenshot={base.with_suffix('.png')}", pagina.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pagina.unlink()
        print(f"mapa {i}: {nombre}")


if __name__ == "__main__":
    main()
