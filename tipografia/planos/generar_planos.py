"""Planos de Contenida: la anatomía base de la tipografía en láminas técnicas A3.

Uso (desde la raíz del repositorio):
    pip install ezdxf pymupdf
    python3 tipografia/planos/generar_planos.py [--cache RUTA.json]

Escribe en tipografia/planos/:
  svg/P-00_… P-10_….svg      once láminas A3 apaisadas, a escala, en milímetros,
  dxf/P-0n_….dxf             la vista principal de las láminas a 1:1 y la caja, en mm reales,
  png/P-00_… P-10_….png      vistas previas,
  contenida_planos.pdf       las once, una por página, en A3.

Como un plano de arquitectura: cotas con trazo oblicuo, ejes de trazo y
punto, niveles con el fondo en ±0, llamadas de vista y de detalle, escala
gráfica, cajetín; en lugar del norte, la gravedad. A la derecha de cada
lámina, el porqué: concepto (las decisiones D1 … D16), retórica y poética.

Las medidas salen de la gramática (simulacion/gramatica.py): no se dibuja
nada que la gramática no haga. Es la propuesta de la máquina; la letra de la
caja la calca la mano desde el pie (04, acciones 3 y 4).
Necesita Chromium (o Chrome) para el PDF.
"""

import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(TIPO / "simulacion"))
sys.path.insert(0, str(TIPO / "laminas"))

from dibujo import (COLUMNA, DIBUJO, GRIS, GRIS2, MONO, PAPEL, SERIF, TINTA, VIOLETA, Hoja, Vista,  # noqa: E402
                    coma, estilo, f)
from geometria import leer  # noqa: E402
from por_que import bloques  # noqa: E402

FAMILIA = {"o": "oecdbpqóéá0689", "l": "litjfkí()147", "n": "nmhuúürvwxyzñ235", "a": "a,sg.?;:¿«»—…"}
NOMBRE_GEN = {"o": "cuenca", "l": "fuste", "n": "hombro", "a": "gancho y gota"}
LAMINAS = [
    ("P-00", "Índice y convenciones", "cómo se leen estos planos", "—"),
    ("P-01", "La celda y las cuatro líneas", "la unidad de la letra: la celda de la cabeza", "1:1 · 1:3"),
    ("P-02", "El canal y la chapa", "el trazo, su radio mínimo y su corte", "2:1 · 5:1"),
    ("P-03", "o · la cuenca", "primer generador", "1:1 · 2:1 · 4:1 · 1:2"),
    ("P-04", "l · el fuste", "segundo generador", "1:1 · 2:1 · 1:2"),
    ("P-05", "n · el hombro", "tercer generador", "1:1 · 2:1 · 1:2"),
    ("P-06", "a · el gancho y la gota", "cuarto generador: la suma", "1:1 · 5:1 · 1:2"),
    ("P-07", "Las partes", "cuadro de partes y reglas de derivación", "1:4"),
    ("P-08", "Detalles", "punto, tilde, onda, sifón, alivio y celda", "2:1 · 1:2"),
    ("P-09", "Los dobles opuestos", "? ¿ · 6 9 · « »", "1:2"),
    ("P-10", "La caja", "plan general: 8 × 7", "1:5"),
]
NOMBRES_ARCHIVO = ["indice", "celda", "canal", "o_cuenca", "l_fuste", "n_hombro", "a_gancho_y_gota", "partes",
                   "detalles", "dobles_opuestos", "caja"]


def familia(s):
    for g, signos in FAMILIA.items():
        if s in signos:
            return g
    return "a"


# ---------------------------------------------------------------- medidas

class Medidas:
    """Conversión del lienzo (px) a mm de la placa y a unidades de la fuente."""

    def __init__(self, D):
        self.D, self.E, self.P = D, D["esqueleto"], D["parametros"]
        x0, y0, x1, y1 = self.E["celda"]
        self.alto = y1 - y0
        self.U = 1000 / self.alto
        self.c = self.E["canal"]
        self.F = self.E["fondo"]

    def v(self, k):
        return self.P[k]["valor"]

    def mm(self, px, d=1):
        return coma(px / 4, d)

    def upm(self, px):
        return str(int(round(px * self.U)))

    def cota(self, px, d=1):
        return f"{coma(px / 4, d)} ({int(round(px * self.U))})"

    def nivel(self, y):
        u = int(round((self.F - y) * self.U))
        return "±0" if u == 0 else f"{u:+d}".replace("-", "−")

    def libre_gota(self):
        """Lo que queda de verdad entre la gota de la a y su cuenca, medido sobre el cuerpo."""
        from shapely.geometry import LineString
        geo = cuerpo_base(self.D, "a")
        x = self.D["generadores"]["a"]["gota_centro"][0]
        corte = geo.intersection(LineString([(x, 0), (x, 600)]))
        tramos = sorted((min(p[1] for p in g.coords), max(p[1] for p in g.coords))
                        for g in (corte.geoms if hasattr(corte, "geoms") else [corte]))
        return tramos[1][0] - tramos[0][1]

    def tabla(self):
        E, c, U = self.E, self.c, self.U
        G = self.D["generadores"]
        x0, y0, x1, y1 = E["celda"]
        o, l, n, a = G["o"], G["l"], G["n"], G["a"]
        M = {}

        def par(clave, px, d=1):
            M[clave] = coma(px / 4, d) if px >= 0 else "−" + coma(-px / 4, d)
            M[clave + "_upm"] = str(int(round(px * U))).replace("-", "−")

        par("canal_mm", c)
        M["canal_upm"] = str(int(round(c * U)))
        M["celda_alto"] = coma(self.alto / 4)
        M["celda_ancho"] = coma((x1 - x0) / 4)
        M["upm_mm"] = coma(self.alto / 4 / 1000, 3)
        for k, y in (("cabeza", y0), ("afuera", E["afuera"]), ("borde", E["borde"]), ("desague", E["desague"]),
                     ("pie", y1)):
            M[k + "_mm"] = (coma((self.F - y) / 4) if self.F >= y else "−" + coma((y - self.F) / 4))
            M[k + "_upm"] = self.nivel(y).replace("+", "")
        M["razon"] = coma(E["razon_x"], 2)
        r = self.v("radio_chapa")
        M["radio_mm"], M["radio_upm"] = coma(r / 4), str(round(r * U))
        M["interior_mm"], M["interior_upm"] = coma((r - c / 2) / 4), str(round((r - c / 2) * U))
        d = self.v("desague")
        M["desague_corte_mm"], M["desague_corte_upm"] = coma(d / 4), str(round(d * U))
        for k in ("intemperie", "alivio", "asiento_ancho", "asiento_alto", "gota_masa", "gota_caida", "gota_cuello",
                  "punto"):
            M[k + "_mm"], M[k + "_upm"] = coma(self.v(k) / 4), str(round(self.v(k) * U))
        M["sifon_mm"] = coma(self.v("sifon") * c / 4)
        par("o_ancho", 2 * o["rx"])
        par("o_fondo", o["fondo_der"] - o["fondo_izq"])
        par("o_alto", o["yb"] - o["ya"])
        par("o_cy", o["yb"] - o["cy"])
        par("l_alto", self.F - l["arriba"])
        plano = (l["fin"] - l["arriba"]) / 3
        par("l_plano", plano)
        par("l_desvio", plano * math.tan(math.radians(self.v("quiebre"))), 2)
        par("n_astas", n["xd"] - n["xi"])
        par("n_caida", n["yh"] - n["yt"])
        par("n_resto", self.F - n["yh"])
        par("a_libre", self.libre_gota())
        par("a_libre_regla", a["libre"])
        par("o_sobre", E["borde"] - self.D["signos"]["o"]["caja"][1])
        M["caja_m"] = "1,22 × 1,07 m"
        return M


# ---------------------------------------------------------------- piezas comunes

def nivel(h, x, y, texto, tam=2.3):
    """El símbolo de nivel de un plano: un triángulo sobre la línea, con la cota en UPM."""
    h.linea((x - 2, y), (x + 15, y), "cota")
    h.add("cotas", f'<path d="M{f(x)},{f(y)} L{f(x - 1.5)},{f(y - 2.5)} L{f(x + 1.5)},{f(y - 2.5)} Z" '
                   f'fill="{PAPEL}" stroke="{TINTA}" stroke-width="0.2"/>')
    h.add("cotas", f'<path d="M{f(x)},{f(y)} L{f(x)},{f(y - 2.5)} L{f(x + 1.5)},{f(y - 2.5)} Z" fill="{TINTA}"/>')
    h.texto(x + 2.6, y - 0.8, texto, tam)


def cortar_linea(h, a, b, letra, flechas=-1):
    """La línea de corte: trazo y punto grueso en las puntas, con la letra y el sentido de la vista."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    nx, ny = -uy * flechas, ux * flechas
    h.linea(a, b, "eje", "cotas", w=0.18)
    for p, s in ((a, 1), (b, -1)):
        q = (p[0] + ux * s * 5, p[1] + uy * s * 5)
        h.linea(p, q, "cota", "cotas", w=0.7)
        h.linea(p, (p[0] + nx * 4, p[1] + ny * 4), "cota", "cotas", w=0.25)
        h.flecha((p[0] + nx * 4.6, p[1] + ny * 4.6), p, capa="cotas")
        h.texto(p[0] - ux * s * 2.4, p[1] - uy * s * 2.4 + 1.0, letra, 3.2, "middle", peso=700)


def marco_vista(h, x0, y0, x1, y1):
    h.add("fondo", f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" {estilo("fina")}/>')


def recorte_signo(v, S, ventana, **kw):
    """Dibuja el signo recortado a una ventana del lienzo (px): para los detalles."""
    a, b = v.p(ventana[0], ventana[1]), v.p(ventana[2], ventana[3])
    v.h.recorte(a[0], a[1], b[0], b[1])
    v.signo(S, **kw)
    v.h.fin_recorte()
    marco_vista(v.h, a[0], a[1], b[0], b[1])
    return a, b


def superelipse(cx, cy, rx, ry, n, a0, a1, pasos=120):
    t = np.radians(np.linspace(a0, a1, pasos))
    co, si = np.cos(t), np.sin(t)
    return np.column_stack([cx + rx * np.sign(co) * np.abs(co) ** (2 / n),
                            cy - ry * np.sign(si) * np.abs(si) ** (2 / n)])


def bezier(P0, P1, P2, P3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    P0, P1, P2, P3 = (np.asarray(p, float) for p in (P0, P1, P2, P3))
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3


def testigo(v, T, tipo="fina"):
    d = v.d(T["contorno"])
    v.h.relleno(d, "#e9e6de", "aux")
    v.h.add("aux", f'<path d="{d}" {estilo(tipo)}/>')


def lineas_cortas(v, E, x0, x1, rotulos=False):
    v.lineas(E, x0, x1, rotulos=rotulos, tam=1.9)


def cuerpo_base(D, s):
    """El cuerpo del signo en shapely (para medir y para el DXF)."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    anillos = D["signos"][s]["contorno"]
    polis = [Polygon(r) for r in anillos]
    # el par exterior/interior se resuelve por paridad
    geo = None
    for p in sorted(polis, key=lambda p: -p.area):
        geo = p if geo is None else geo.symmetric_difference(p)
    return unary_union(geo)


# ---------------------------------------------------------------- P-00

CUADRO = [
    ("cuerpo", "la celda de la cabeza, 0,84 : 1", "P-01"),
    ("ancho", "monoespaciada: una letra, una celda", "P-01"),
    ("líneas", "fondo, borde, afuera, desagüe", "P-01"),
    ("altura de x", "1,71 de las ascendentes", "P-01"),
    ("contraste", "ninguno: un canal de 8,9 mm", "P-02"),
    ("curvas", "radio mínimo de 0,6 canal", "P-02"),
    ("remates", "ninguno: un corte, gastado", "P-02 · P-04"),
    ("contornos", "abiertos: un desagüe de 3 mm", "P-02 · P-03"),
    ("ojo", "arriba, el del pie; abajo, una vasija", "P-03"),
    ("sobrepaso", "arriba sí; abajo no", "P-03"),
    ("eje", "vertical: sin pluma", "P-03"),
    ("asta", "un fuste en tres planos", "P-04"),
    ("pie del asta", "un asiento cóncavo, sin serifa", "P-04"),
    ("hombro", "superelipse n = 3, arranque tangente", "P-05"),
    ("terminales", "gota si mira abajo; corte si mira arriba", "P-06"),
    ("a", "de dos pisos: la suma de las partes", "P-06"),
    ("punto", "un cuadrado de cinta", "P-08"),
    ("tilde", "una gota", "P-08"),
    ("virgulilla", "una onda", "P-08"),
    ("enlace de la g", "un sifón", "P-08"),
    ("rincones agudos", "un alivio", "P-08"),
    ("cifras", "elzevirianas, cada una en su celda", "P-08"),
    ("dobles opuestos", "varían: ? ¿ · 6 9 · « »", "P-09"),
    ("mayúsculas", "ninguna: solo caja baja", "P-10"),
]


def p00(h, D, M):
    x, y = DIBUJO[0] + 5, DIBUJO[1] + 14
    h.texto(x, y, "Contenida", 13, familia=SERIF, peso=300)
    h.texto(x + 58, y, "planos de la anatomía base", 5.0, familia=SERIF, cursiva=True, peso=300, color=GRIS)
    h.texto(x, y + 8, "La gramática de la letra dibujada como un proyecto de arquitectura: la forma, antes de "
                      "los estados.", 3.0, familia=SERIF, peso=300)
    # el índice
    y0 = y + 20
    h.texto(x, y0, "ÍNDICE", 2.6, peso=700, espaciado=0.35)
    h.linea((x, y0 + 1.4), (x + 118, y0 + 1.4), "filete", "textos")
    for i, (cod, tit, sub, esc) in enumerate(LAMINAS):
        yy = y0 + 6.6 + i * 7.0
        h.texto(x, yy, cod, 2.8, peso=700)
        h.texto(x + 15, yy, tit, 3.3, familia=SERIF, peso=400)
        h.texto(x + 15, yy + 3.0, sub, 2.0, color=GRIS)
        h.texto(x + 118, yy, esc, 2.0, "end", color=GRIS)
        h.linea((x, yy + 4.2), (x + 118, yy + 4.2), "fina", "textos")
    # dónde están en la cadena
    yc = y0 + 6.6 + len(LAMINAS) * 7.0 + 6
    h.texto(x, yc, "DÓNDE ESTÁN EN LA CADENA", 2.6, peso=700, espaciado=0.35)
    h.linea((x, yc + 1.4), (x + 118, yc + 1.4), "filete", "textos")
    pasos_ = ["pie", "planos", "calco", "placa", "cinta", "frotado", "agua", "voz"]
    xs = [x + 2 + i * 16.4 for i in range(len(pasos_))]
    for i, (p, xx) in enumerate(zip(pasos_, xs)):
        aqui = p == "planos"
        h.circulo((xx + 2, yc + 9), 2.1 if aqui else 1.4, "filete", "textos", relleno=VIOLETA if aqui else PAPEL)
        h.texto(xx + 2, yc + 15.2, p, 2.4, "middle", color=VIOLETA if aqui else TINTA, peso=700 if aqui else 400)
        if i:
            h.linea((xs[i - 1] + 4.2, yc + 9), (xx - 0.4, yc + 9), "cota", "textos")
            h.flecha((xx - 0.2, yc + 9), (xx - 3, yc + 9), largo=1.6, ancho=0.6, capa="textos")
    h.parrafo(x, yc + 22, 118, "Del **pie** se toman medidas. Los **planos** fijan cómo se comporta la forma: la "
                                "anatomía base. La mano **calca** el esqueleto del pie aplicando estas reglas, y "
                                "después vienen los estados, en orden. Los planos no son un estado: no entran en "
                                "la caja.", 2.7)
    # las convenciones
    cx = x + 132
    h.texto(cx, y0, "CONVENCIONES", 2.6, peso=700, espaciado=0.35)
    h.linea((cx, y0 + 1.4), (cx + 112, y0 + 1.4), "filete", "textos")
    muestras = [
        ("contorno", "contorno del cuerpo: lo hallado en el pie"),
        ("contorno_r", "contorno a puntos, en violeta: lo reconstruido"),
        ("eje", "eje del trazo: la curva maestra"),
        ("linea", "líneas de la gramática: afuera, borde, fondo, desagüe"),
        ("celda", "celda de la cabeza (0,84 : 1)"),
        ("placa", "placa de aluminio, 150 × 150 mm"),
        ("aux", "construcción: polígonos de control, cajas, medidas"),
        ("comparar", "comparación: la forma que no se eligió"),
        ("rotura", "lo que no se hace: donde el aluminio se rasga"),
    ]
    yy = y0 + 6.4
    for tipo, txt in muestras:
        h.linea((cx, yy - 0.8), (cx + 22, yy - 0.8), tipo, "textos")
        h.texto(cx + 26, yy, txt, 2.3)
        yy += 5.4
    for pat, txt in (("url(#metal)", "el cuerpo de la letra: metal (rayado a 45°)"),
                     ("url(#metal_r)", "el cuerpo de lo reconstruido"),
                     ("url(#blanda)", "la base blanda del repujado (en los cortes)")):
        h.add("textos", f'<rect x="{f(cx)}" y="{f(yy - 3.2)}" width="22" height="3.6" fill="{pat}" '
                        f'stroke="{TINTA}" stroke-width="0.25"/>')
        h.texto(cx + 26, yy, txt, 2.3)
        yy += 5.4
    yy += 1.5
    h.nodo((cx + 11, yy - 0.8), "textos")
    h.texto(cx + 26, yy, "nodo de la curva maestra", 2.3)
    yy += 5.6
    h.cota((cx, yy + 1), (cx + 22, yy + 1), 0, "8,9 (65)", tam=2.1, ext=False)
    h.texto(cx + 26, yy, "cota: mm de la placa (UPM)", 2.3)
    yy += 6.6
    nivel(h, cx + 4, yy, "+401", 2.1)
    h.texto(cx + 26, yy, "nivel, en UPM: el fondo es ±0", 2.3)
    yy += 7.6
    h.rombo((cx + 11, yy - 0.8), 3, capa="textos")
    h.texto(cx + 26, yy, "decisión 3 de la lámina: su porqué, en la columna", 2.3)
    yy += 8.6
    h.llamada(cx + 7, yy, 2, "P-03")
    h.texto(cx + 26, yy - 1.0, "llamada: vista o detalle 2 de la lámina P-03", 2.3)
    yy += 14
    h.gravedad(cx + 7, yy, 4.0)
    h.clave((cx + 2.8, yy), (cx - 6, yy), 2)
    h.texto(cx + 26, yy - 1.0, "en lugar del norte, la gravedad:", 2.3)
    h.texto(cx + 26, yy + 2.4, "solo gotea lo que mira abajo", 2.0, color=GRIS)
    yy += 11
    h.escala_grafica(cx, yy, 1.0, 50, 10)
    h.texto(cx + 63, yy + 1.4, "escala gráfica, a 1:1", 2.3)
    yy += 9
    h.texto(cx, yy, "Decimales con coma. Las cotas a 1:1 se miden con regla sobre la hoja", 2.1, color=GRIS)
    h.texto(cx, yy + 3.0, "impresa en A3 al 100 %.", 2.1, color=GRIS)
    # el cuadro de las decisiones anatómicas
    yq = 206
    h.texto(x, yq, "CUADRO DE LAS DECISIONES ANATÓMICAS", 2.6, peso=700, espaciado=0.35)
    h.linea((x, yq + 1.4), (x + 244, yq + 1.4), "filete", "textos")
    mitad = (len(CUADRO) + 1) // 2
    for i, (parte, decision, lamina) in enumerate(CUADRO):
        col, fila = divmod(i, mitad)
        xx = x + col * 126
        yy = yq + 6.2 + fila * 5.75
        h.texto(xx, yy, parte, 2.5, familia=SERIF, peso=500)
        h.texto(xx + 27, yy, decision, 2.2)
        h.texto(xx + 118, yy, lamina, 2.0, "end", color=VIOLETA)
        h.linea((xx, yy + 1.7), (xx + 118, yy + 1.7), "fina", "textos")
    h.clave((cx, y0 + 6.4 + 5.4 - 0.8), (cx - 6, y0 + 6.4 + 5.4 - 0.8), 1)
    h.columna(bloques("P-00", M))


# ---------------------------------------------------------------- P-01

def p01(h, D, M):
    E, Me = D["esqueleto"], M["_"]
    ox, oy = 76, 30
    v = Vista(h, ox, oy, 1.0)
    h.llamada(32, 22, 1, titulo="LA CELDA EN LA PLACA", escala="1:1")
    v.placa()
    v.celda(E)
    for nombre, k in (("afuera", "afuera"), ("borde", "borde"), ("fondo", "fondo"), ("desagüe", "desague")):
        y = E[k]
        h.linea(v.p(0, y), v.p(600, y), "linea", "fondo")
        a = v.p(0, y)
        h.texto(a[0] + 1.6, a[1] - 1.0, nombre, 2.3, color=GRIS)
    x0, y0, x1, y1 = E["celda"]
    h.texto(v.p(x0, y0)[0] + 1.5, v.p(x0, y0)[1] + 3.6, "celda 0,84 : 1", 2.3)
    h.linea(v.p(300, -24), v.p(300, 624), "eje", "ejes")
    h.texto(v.p(300, -24)[0], v.p(300, -24)[1] - 1.5, "eje de la celda", 2.2, "middle")
    # a la izquierda, la cadena de cotas
    niveles = [y1, E["desague"], E["fondo"], E["borde"], E["afuera"], y0]
    for a, b in zip(niveles[:-1], niveles[1:]):
        h.cota((ox, oy + a / 4), (ox, oy + b / 4), 7, Me.mm(a - b), tam=2.2)
    h.cota((ox, oy + y1 / 4), (ox, oy + y0 / 4), 15, f"celda {Me.cota(y1 - y0)}", tam=2.3)
    h.cota((ox, oy + 150), (ox, oy), 23, "placa 150", tam=2.3)
    # a la derecha, los niveles en UPM
    xr = ox + 150 + 5
    h.texto(xr + 2, oy - 2, "NIVELES (UPM)", 2.0, espaciado=0.2, color=GRIS)
    for nombre, y in (("cabeza de la celda", y0), ("afuera", E["afuera"]), ("borde", E["borde"]),
                      ("fondo", E["fondo"]), ("desagüe", E["desague"]), ("pie de la celda", y1)):
        yy = oy + y / 4
        h.linea((ox + 150, yy), (xr - 2, yy), "fina", "cotas")
        nivel(h, xr + 1, yy, Me.nivel(y))
        h.texto(xr + 17, yy - 0.8, nombre, 2.0, color=GRIS)
    asc, xh = E["fondo"] - E["afuera"], E["fondo"] - E["borde"]
    for i, r in enumerate(["ascendente / x", f"{coma(asc / 4)} / {coma(xh / 4)} ≈ {coma(E['razon_x'], 2)}",
                           "(de la foto del pie)"]):
        h.texto(xr + 2, oy + 72 + i * 3.2, r, 2.2, color=TINTA if i < 2 else GRIS)
    h.gravedad(xr + 34, oy + 36)
    # abajo, los anchos
    yb = oy + y1 / 4
    s_ = -(150 - y1 / 4) - 7
    h.cota((ox, yb), (ox + x0 / 4, yb), s_, Me.mm(x0), tam=2.2)
    h.cota((ox + x0 / 4, yb), (ox + x1 / 4, yb), s_, f"{Me.cota(x1 - x0)} · avance", tam=2.2)
    h.cota((ox + x1 / 4, yb), (ox + 150, yb), s_, Me.mm(600 - x1), tam=2.2)
    h.cota((ox, oy + 150), (ox + 150, oy + 150), -15, "placa 150", tam=2.3)
    h.escala_grafica(ox, oy + 150 + 22, 1.0, 50, 10)
    # las decisiones, en el dibujo
    h.clave((ox + 100, oy + y0 / 4), (ox + 108, oy - 6), 1)
    h.clave((ox + x1 / 4, oy + y1 / 4 - 4), (ox + x1 / 4 + 9, oy + y1 / 4 - 10), 2)
    h.clave((ox + 40, oy + E["fondo"] / 4), (ox + 48, oy + E["fondo"] / 4 + 9), 3)
    h.clave((ox + 60, oy + E["borde"] / 4), (ox + 68, oy + E["borde"] / 4 + 9), 4)
    # abajo, a 1:3: tres signos y la celda vacía
    yv = 220
    h.llamada(32, yv - 7, 2, titulo="TRES SIGNOS Y LA CELDA VACÍA", escala="1:3")
    ejemplos = [("o", "o · altura de x"), ("l", "l · ascendente"), ("p", "p · descendente"), (None, "la celda vacía")]
    for i, (s, rot) in enumerate(ejemplos):
        vx = 34 + i * 62
        w = Vista(h, vx, yv, 1 / 3)
        w.placa()
        w.celda(E)
        for k in ("afuera", "borde", "fondo", "desague"):
            h.linea(w.p(0, E[k]), w.p(600, E[k]), "linea", "fondo", w=0.18)
        if s:
            w.signo(D["signos"][s], nodos=False)
        else:
            h.texto(w.p(300, 330)[0], w.p(300, 330)[1], "la piel", 2.6, "middle", familia=SERIF, cursiva=True,
                    color=GRIS)
            h.clave(w.p(300, 345), (w.p(300, 345)[0] + 9, w.p(300, 345)[1] + 9), 2)
        h.texto(vx, yv + 50 + 4.5, rot, 2.4, familia=SERIF if s is None else MONO, cursiva=s is None)
    h.columna(bloques("P-01", M))


# ---------------------------------------------------------------- P-02

def _eje_codo(r, largo=150.0):
    """Un eje en L, de ancho de canal, con el codo redondeado a radio r (px)."""
    from gramatica import filetear
    pts = np.array([(0.0, 0.0), (largo, 0.0), (largo, largo)])
    return filetear(pts, r, pasos=40)


def _offset_crudo(pts, d):
    """La paralela a distancia d de una poligonal, sin resolver: si el radio es chico, se cruza."""
    pts = np.asarray(pts, float)
    tg = np.gradient(pts, axis=0)
    tg /= np.linalg.norm(tg, axis=1)[:, None]
    nrm = np.column_stack([-tg[:, 1], tg[:, 0]])
    return pts + nrm * d


def _perfil(h, perfil, espesor, abajo):
    """Una hoja de aluminio en corte (con el espesor exagerado) sobre la base blanda."""
    x0, x1 = perfil[0][0], perfil[-1][0]
    y0 = perfil[0][1]
    blanda = [(x0, y0 + espesor), *[(p[0], p[1] + espesor) for p in perfil], (x1, y0 + espesor), (x1, abajo),
              (x0, abajo)]
    h.add("cuerpo", f'<path d="M{" L".join(f"{f(a)},{f(b)}" for a, b in blanda)} Z" fill="url(#blanda)" '
                    f'stroke="{GRIS}" stroke-width="0.2"/>')
    hoja = np.vstack([perfil, perfil[::-1] + [0, espesor]])
    h.add("cuerpo", f'<path d="M{" L".join(f"{f(a)},{f(b)}" for a, b in hoja)} Z" fill="url(#metal)" '
                    f'stroke="{TINTA}" stroke-width="0.35"/>')


def p02(h, D, M):
    from shapely.geometry import LineString
    Me = M["_"]
    c = Me.c
    rch = Me.v("radio_chapa")
    ri = Me.v("intemperie")

    def cuerpo_codo(r):
        eje = _eje_codo(r)
        g = LineString(eje).buffer(c / 2, cap_style="flat", join_style="round", quad_segs=24)
        return eje, g.buffer(-ri, quad_segs=12).buffer(ri, quad_segs=12)

    def anillos(g):
        polis = list(g.geoms) if hasattr(g, "geoms") else [g]
        return [list(p.exterior.coords)[:-1] for p in polis] + [list(i.coords)[:-1] for p in polis for i in p.interiors]

    # 1 · el canal y el radio de la chapa, 2:1
    h.llamada(32, 22, 1, titulo="EL CANAL Y EL RADIO DE LA CHAPA", escala="2:1")
    v = Vista(h, 44, 42, 2.0, px0=-30, py0=-30)
    eje, g = cuerpo_codo(rch)
    d = v.d(anillos(g))
    h.relleno(d, "url(#metal)")
    h.add("cuerpo", f'<path d="{d}" {estilo("contorno")}/>')
    h.poli([v.p(*p) for p in eje], "eje", "ejes")
    h.cota(v.p(0, c / 2), v.p(0, -c / 2), 6, f"canal {Me.cota(c)}", tam=2.2)
    cen = v.p(150 - rch, rch)
    h.punto(cen, 0.5)
    h.cota_radio(cen, v.mm(rch), 50, f"{Me.cota(rch)} eje", largo=16)
    h.cota_radio(cen, v.mm(rch + c / 2), 18, f"{Me.mm(rch + c / 2)} exterior", largo=8)
    h.cota_radio(cen, v.mm(rch - c / 2), 205, f"{Me.mm(rch - c / 2)} interior", largo=22)
    cortar_linea(h, v.p(40, -c / 2 - 22), v.p(40, c / 2 + 22), "A")
    h.texto(v.p(-28, 100)[0], v.p(-28, 100)[1], "r ≥ 0,6 c: el contorno interior", 2.3)
    h.texto(v.p(-28, 100)[0], v.p(-28, 100)[1] + 3.1, "no se cruza; la chapa se dobla", 2.3)
    h.clave(v.p(30, -c / 2), (v.p(30, -c / 2)[0] - 2, v.p(30, -c / 2)[1] - 10), 1)
    h.clave(v.p(*eje[len(eje) // 2]), (cen[0] - 14, cen[1] + 14), 2)

    # 2 · lo que no se hace, 2:1
    h.llamada(162, 22, 2, titulo="LO QUE NO SE HACE", escala="2:1")
    w = Vista(h, 166, 42, 2.0, px0=-30, py0=-30)
    r_mal = 0.18 * c
    eje2, g2 = cuerpo_codo(r_mal)
    ext = _offset_crudo(eje2, -c / 2)
    inn = _offset_crudo(eje2, c / 2)
    h.relleno(w.d(anillos(g2)), "#efece4")
    h.poli([w.p(*p) for p in ext], "contorno", "cuerpo")
    h.poli([w.p(*p) for p in inn], "rotura", "cuerpo")
    h.poli([w.p(*p) for p in eje2], "eje", "ejes")
    h.poli([w.p(0, -c / 2), w.p(0, c / 2)], "contorno", "cuerpo")
    h.poli([w.p(150 - c / 2, 150), w.p(150 + c / 2, 150)], "contorno", "cuerpo")
    cen2 = w.p(150 - r_mal, r_mal)
    h.cota_radio(cen2, w.mm(r_mal), 140, f"{Me.mm(r_mal)} < c/2", largo=12)
    h.nota(w.p(150 - c / 2 + 3, c / 2 - 3), w.p(40, 95), "", lineas=["el contorno interior", "se cruza consigo mismo:",
                                                                    "ahí el aluminio se rasga"], tam=2.2)

    # 3 · corte A–A, 5:1
    h.llamada(32, 124, 3, titulo="CORTE A–A · EL CANAL EN LA PLACA", escala="5:1 · espesor exagerado")
    k = 5.0
    x0, y0 = 90, 158
    cw = c / 4 * k
    prof = 0.22 * c / 4 * k
    hoja_e = 0.7
    xs = np.linspace(-1.85 * cw / 2, 1.85 * cw / 2, 200)
    perfil = np.array([(x0 + xx, y0 + (prof * (1 - (abs(xx) / (cw / 2)) ** 2) ** 0.6 if abs(xx) < cw / 2 else 0.0))
                       for xx in xs])
    _perfil(h, perfil, hoja_e, y0 + 13)
    pb = (x0 + cw / 2 - 2.2, y0 + prof * 0.45 - 2.4)
    h.circulo(pb, 2.4, "contorno", "cuerpo", relleno="#d9d6cf")
    h.add("cuerpo", f'<path d="M{f(pb[0] + 1.2)},{f(pb[1] - 2.1)} L{f(pb[0] + 9)},{f(pb[1] - 20)} '
                    f'L{f(pb[0] + 13)},{f(pb[1] - 18.5)} L{f(pb[0] + 2.4)},{f(pb[1] - 0.9)}" fill="#d9d6cf" '
                    f'stroke="{TINTA}" stroke-width="0.35"/>')
    h.cota((x0 - cw / 2, y0), (x0 + cw / 2, y0), 9, f"canal {Me.cota(c)}", tam=2.2)
    h.texto(x0 - 1.85 * cw / 2, y0 - 3.0, "reverso: se trabaja", 2.2, color=GRIS)
    h.texto(x0 - 1.85 * cw / 2, y0 + 23.5, "anverso (abajo): la letra sale en relieve", 2.2, color=GRIS)
    h.nota((x0 - 8, y0 + prof * 0.75), (x0 - 30, y0 + 16), "h: la decide la mano", ancla="end", tam=2.1)
    h.nota((x0 + 1.85 * cw / 2 - 5, y0 + 8), (x0 + 1.85 * cw / 2 + 3, y0 + 12), "base blanda", tam=2.1)
    h.nota((pb[0] + 6, pb[1] - 11), (pb[0] + 18, pb[1] - 15), "punzón de bola", tam=2.1)
    h.clave((x0, y0 + prof + hoja_e), (x0 + 9, y0 + prof + 9), 5)

    # 4 · corte B–B: el desagüe, 5:1
    h.llamada(162, 124, 4, titulo="CORTE B–B · EL DESAGÜE", escala="5:1 · espesor exagerado")
    xb, yb0 = 220, 158
    gap = Me.v("desague") / 4 * k
    rampa = 5.0
    xs = np.linspace(-52, 52, 300)

    def dz(a):
        if a <= gap / 2:
            return 0.0
        if a >= gap / 2 + rampa:
            return prof
        t = (a - gap / 2) / rampa
        return prof * (0.5 - 0.5 * math.cos(math.pi * t))

    perfil = np.array([(xb + xx, yb0 + dz(abs(xx))) for xx in xs])
    _perfil(h, perfil, hoja_e, yb0 + 13)
    h.cota((xb - gap / 2, yb0), (xb + gap / 2, yb0), 9, f"desagüe {Me.cota(Me.v('desague'))}", tam=2.2)
    h.texto(xb - 52, yb0 + 17.5, "a lo largo del trazo: el punzón se detiene 3 mm antes de cerrar", 2.2, color=GRIS)
    h.clave((xb, yb0), (xb + 14, yb0 - 8), 4)

    # 5 · la intemperie, 5:1: el corte de arriba de la l y el remate del testigo
    h.llamada(32, 196, 5, titulo="LA INTEMPERIE · ARRIBA, UN CORTE", escala="5:1")
    S = D["signos"]["l"]
    T = D["testigos"]["l"]
    xs_ = D["generadores"]["l"]["xs"]
    vi = Vista(h, 34, 206, 5.0, px0=xs_ - 44, py0=48)
    a, b = vi.p(xs_ - 44, 48), vi.p(xs_ + 22, 68)
    h.recorte(a[0], a[1], b[0], b[1])
    h.add("aux", f'<path d="{vi.d(T["contorno"])}" {estilo("comparar")}/>')
    vi.signo(S, nodos=False)
    h.fin_recorte()
    marco_vista(h, a[0], a[1], b[0], b[1])
    esq = vi.p(xs_ + c / 2 - ri, 55 + ri)
    h.cota_radio(esq, vi.mm(ri), 40, f"{Me.cota(ri)} intemperie", largo=6)
    h.texto(a[0], b[1] + 4.0, "en línea de comparación, el remate del testigo del pie:", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 7.0, "lo que la intemperie se llevó", 2.1, color=GRIS)
    h.clave(vi.p(xs_ - c / 2 + ri, 55), (a[0] + 4, a[1] - 3.5), 3)

    # 6 · de dónde sale el canal, 2:1
    h.llamada(162, 196, 6, titulo="DE DÓNDE SALE EL CANAL", escala="2:1")
    g_, fi_ = D["esqueleto"]["grueso"], D["esqueleto"]["fino"]
    xb2, yb2 = 170, 208
    for i, (nombre, val) in enumerate((("grueso de la o", g_), ("fino de la o", fi_), ("canal", c))):
        x = xb2 + i * 34
        wv = val / 4 * 2
        h.add("cuerpo", f'<rect x="{f(x)}" y="{f(yb2)}" width="{f(wv)}" height="40" '
                        f'fill="{"url(#metal)" if i == 2 else "#e9e6de"}" stroke="{TINTA}" '
                        f'stroke-width="{0.5 if i == 2 else 0.25}"/>')
        h.cota((x, yb2 + 40), (x + wv, yb2 + 40), -4, Me.mm(val), tam=2.1)
        h.texto(x, yb2 + 51, nombre, 2.1)
    h.texto(xb2 + 68, yb2 + 54.2, "= √(grueso × fino)", 2.1)
    h.texto(xb2, yb2 + 60, "del pie, la medida; no el contraste", 2.1, color=GRIS)
    h.columna(bloques("P-02", M))


# ---------------------------------------------------------------- vista de un generador y sus pasos

def vista_generador(h, D, s, ox, oy):
    """La vista principal de un generador, a 1:1: la celda con sus líneas, el cuerpo, los ejes y los nodos."""
    E = D["esqueleto"]
    v = Vista(h, ox, oy, 1.0)
    x0, y0, x1, y1 = E["celda"]
    v.celda(E)
    v.lineas(E, x0 - 30, x1 + 30, rotulos=True, tam=2.2, lado="izq")
    h.linea(v.p(300, y0 - 22), v.p(300, y1 + 22), "eje", "ejes", w=0.13)
    v.signo(D["signos"][s])
    return v


def pasos(h, D, y, titulos, dibujar, ventana, escala=0.5):
    """Una fila de pasos de construcción, a 1:2."""
    for i, tit in enumerate(titulos):
        x = 30 + i * 62
        v = Vista(h, x, y + 4, escala, px0=ventana[0], py0=ventana[1])
        a, b = v.p(ventana[0], ventana[1]), v.p(ventana[2], ventana[3])
        marco_vista(h, a[0], a[1], b[0], b[1])
        h.recorte(a[0], a[1], b[0], b[1])
        for k in ("afuera", "borde", "fondo", "desague"):
            h.linea(v.p(ventana[0], D["esqueleto"][k]), v.p(ventana[2], D["esqueleto"][k]), "linea", "aux", w=0.15)
        dibujar(i, v)
        h.fin_recorte()
        h.texto(x, b[1] + 4.2, f"{i + 1} · {tit}", 2.3)


OX, OY = 28, 25          # la vista principal de los generadores


# ---------------------------------------------------------------- P-03 · o

def p03(h, D, M):
    Me, E = M["_"], D["esqueleto"]
    G = D["generadores"]["o"]
    S = D["signos"]["o"]
    c = Me.c
    F = E["fondo"]
    x0c, y0c, x1c, y1c = E["celda"]
    h.llamada(32, 22, 1, titulo="LA CUENCA · VISTA", escala="1:1")
    v = vista_generador(h, D, "o", OX, OY)
    for lado in ("bezier_izq", "bezier_der"):
        B = G[lado]
        pts = [v.p(*B[k]) for k in ("P0", "P1", "P2", "P3")]
        h.poli(pts, "aux", "aux")
        for p in pts[1:3]:
            h.add("aux", f'<rect x="{f(p[0] - 0.7)}" y="{f(p[1] - 0.7)}" width="1.4" height="1.4" fill="{PAPEL}" '
                         f'stroke="{GRIS}" stroke-width="0.18"/>')
    h.linea(v.p(G["cx"] - G["rx"] - 12, G["cy"]), v.p(G["cx"] + G["rx"] + 12, G["cy"]), "aux", "aux")
    yb = G["yb"]
    h.cota(v.p(G["fondo_izq"], yb), v.p(G["fondo_der"], yb), -9.5,
           f"fondo plano {Me.cota(G['fondo_der'] - G['fondo_izq'])} · 0,70", tam=2.2)
    h.cota(v.p(G["xi"], G["cy"]), v.p(G["xd"], G["cy"]), -(yb - G["cy"]) / 4 - 17,
           f"ancho mayor (eje) {Me.cota(2 * G['rx'])}", tam=2.2)
    h.cota(v.p(G["xi"], yb), v.p(G["xi"], G["cy"]), 9, Me.cota(yb - G["cy"]), tam=2.2)
    h.cota(v.p(G["xi"], G["cy"]), v.p(G["xi"], G["ya"]), 9, Me.cota(G["cy"] - G["ya"]), tam=2.2)
    yc_ = G["cy"] + 45
    h.cota(v.p(G["xd"] + c / 2, yc_), v.p(G["xd"] - c / 2, yc_), -0.01, "", ext=False, tam=2.2)
    h.nota(v.p(G["xd"] + c / 2, yc_), v.p(424, yc_ + 22), f"canal {Me.cota(c)}", tam=2.1)
    h.nota(v.p(*G["bezier_der"]["P1"]), v.p(424, G["cy"] + 4), "pared 0,55", tam=2.1)
    p_el = (G["cx"] - G["rx"] * 0.72, G["cy"] - G["ry"] * 0.70)
    h.nota(v.p(*p_el), v.p(x0c + 100, 150), "", ancla="end", tam=2.1, lineas=["mitad alta:", "el ojo del pie"])
    top = S["caja"][1]
    h.nota(v.p(G["cx"] + 30, top + 1), v.p(G["cx"] + 62, 172), f"sobrepaso {Me.cota(E['borde'] - top)}", tam=2.1)
    h.nota(v.p(G["cx"] - 52, F), v.p(G["cx"] - 92, F + 34), "sin sobrepaso", tam=2.1, ancla="end")
    h.gravedad(OX + 145, OY + 34)
    # las decisiones
    h.clave(v.p(G["cx"] - 12, G["ya"] - c / 2), v.p(G["cx"] - 40, 150), 1)
    h.clave(v.p(G["xd"] + c / 2 - 2, G["cy"] + 60), v.p(452, G["cy"] + 92), 2)
    h.clave(v.p(G["cx"] + 4, top + 0.5), v.p(G["cx"] + 18, 160), 3)
    h.clave(v.p(G["cx"], F - c / 2), v.p(G["cx"], F - c - 34), 4)
    h.clave(v.p(300, 110), v.p(330, 92), 5)

    # 2 · la pared: 0, 0,55, 1 (2:1)
    h.llamada(182, 22, 2, titulo="LA PARED", escala="2:1")
    w = Vista(h, 192, 36, 2.0, px0=G["cx"], py0=G["cy"] - 6)
    h.linea(w.p(G["cx"], G["yb"]), w.p(G["xd"] + 14, G["yb"]), "linea", "aux")
    h.linea(w.p(G["cx"], G["cy"]), w.p(G["xd"] + 14, G["cy"]), "aux", "aux")
    for p, tipo in (("0.0", "comparar"), ("1.0", "comparar"), ("0.55", "eje")):
        h.poli([w.p(*q) for q in G["paredes"][p]], tipo, "ejes", w=0.4 if p == "0.55" else 0.25)
    q0 = w.p(*G["paredes"]["0.0"][30])
    q1 = w.p(*G["paredes"]["1.0"][30])
    q5 = w.p(*G["paredes"]["0.55"][38])
    h.nota(q0, (q0[0] - 10, q0[1] + 14), "0 · trapecio", tam=2.1, ancla="end")
    h.nota(q1, (q1[0] + 7, q1[1] - 9), "1 · cuenco", tam=2.1)
    h.nota(q5, (q5[0] + 9, q5[1] + 10), "0,55", tam=2.1)
    h.cota(w.p(G["cx"], G["yb"]), w.p(G["fondo_der"], G["yb"]), -5, "0,70 × ancho/2", tam=2.1)
    h.clave(q5, (q5[0] - 14, q5[1] + 4), 2)

    # 3 · el desagüe (4:1)
    h.llamada(182, 112, 3, titulo="EL DESAGÜE", escala="4:1")
    z = Vista(h, 192, 124, 4.0, px0=300 - 20, py0=F - 42)
    a, b = z.p(280, F - 42), z.p(320, F + 6)
    h.recorte(a[0], a[1], b[0], b[1])
    z.signo(S, nodos=False)
    h.linea(z.p(280, F), z.p(320, F), "linea", "aux")
    h.fin_recorte()
    marco_vista(h, a[0], a[1], b[0], b[1])
    dd = Me.v("desague")
    h.cota(z.p(300 - dd / 2, F - c / 2), z.p(300 + dd / 2, F - c / 2), 20, Me.cota(dd), tam=2.2)
    h.texto(a[0], b[1] + 4.2, "el trazo termina en un corte,", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 7.2, "gastado por la intemperie", 2.1, color=GRIS)
    h.clave(z.p(300, F - c / 2), (z.p(300, F)[0] + 13, z.p(300, F)[1] + 3), 4)

    # 4 · pasos de construcción, 1:2
    T = D["testigos"]["o"]
    sup = superelipse(G["cx"], G["cy"], G["rx"], G["ry"], 2.0, 0, 180)

    def dibujar(i, w):
        if i == 0:
            testigo(w, T)
            x0, y0, x1, y1 = T["caja"]
            w.h.add("aux", f'<rect x="{f(w.p(x0, y0)[0])}" y="{f(w.p(x0, y0)[1])}" width="{f(w.mm(x1 - x0))}" '
                           f'height="{f(w.mm(y1 - y0))}" {estilo("aux")}/>')
        if i >= 1:
            w.h.poli([w.p(*p) for p in sup], "eje", "ejes")
            w.h.linea(w.p(G["xi"] - 6, G["cy"]), w.p(G["xd"] + 6, G["cy"]), "aux", "aux")
        if i >= 2:
            for lado in ("bezier_izq", "bezier_der"):
                B = G[lado]
                w.h.poli([w.p(*q) for q in bezier(B["P0"], B["P1"], B["P2"], B["P3"])], "eje", "ejes")
                if i == 2:
                    w.h.poli([w.p(*B[k]) for k in ("P0", "P1", "P2", "P3")], "aux", "aux")
            w.h.linea(w.p(G["fondo_izq"], G["yb"]), w.p(G["fondo_der"], G["yb"]), "eje", "ejes")
        if i == 3:
            w.signo(S, nodos=False, ejes=False)

    y = 204
    h.llamada(32, y - 8, 4, titulo="CÓMO SE CONSTRUYE", escala="1:2")
    pasos(h, D, y, ["del pie: la caja del ojo", "arriba: la elipse", "las paredes y el fondo",
                    "el canal y el desagüe"], dibujar, (170, 180, 430, 450))
    h.columna(bloques("P-03", M))


# ---------------------------------------------------------------- P-04 · l

def p04(h, D, M):
    Me, E = M["_"], D["esqueleto"]
    G = D["generadores"]["l"]
    S = D["signos"]["l"]
    c = Me.c
    F = E["fondo"]
    h.llamada(32, 22, 1, titulo="EL FUSTE · VISTA", escala="1:1")
    v = vista_generador(h, D, "l", OX, OY)
    eje = G["eje"]
    xs = G["xs"]
    h.cota(v.p(xs - c / 2, F), v.p(xs - c / 2, G["arriba"]), 26, f"alto {Me.cota(F - G['arriba'])}", tam=2.2)
    for p, q in zip(eje[:-1], eje[1:]):
        h.cota(v.p(xs + c / 2, q[1]), v.p(xs + c / 2, p[1]), -9, Me.mm(q[1] - p[1]), tam=2.1)
    for p in eje[1:-1]:
        h.nota(v.p(*p), v.p(xs + 70, p[1] - 14), "quiebre", tam=2.1)
    h.nota(v.p(xs - c / 2 + 1, G["arriba"] + 2), v.p(xs - 64, G["arriba"] + 22), "corte: sin remate", tam=2.1,
           ancla="end")
    h.nota(v.p(xs - G["asiento_ancho"] / 2 + 3, F - 2), v.p(xs - 64, F - 34), "asiento", tam=2.1, ancla="end")
    h.gravedad(OX + 145, OY + 34)
    h.clave(v.p(*eje[1]), v.p(xs - 42, eje[1][1] + 24), 1)
    h.clave(v.p(xs + c / 2 - 2, G["arriba"] + 1), v.p(xs + 40, 36), 2)
    h.clave(v.p(xs + G["asiento_ancho"] / 2 - 3, F - 2), v.p(xs + 52, F + 32), 3)

    # 2 · el quiebre, con los desvíos ×10
    h.llamada(182, 22, 2, titulo="EL QUIEBRE", escala="1:1 en alto · desvíos × 10")
    w = Vista(h, 204, 34, 1.0, px0=xs - 40, py0=G["arriba"] - 8)
    exag = [(xs + (p[0] - xs) * 10, p[1]) for p in eje]
    h.linea(w.p(xs, G["arriba"] - 4), w.p(xs, G["fin"] + 14), "aux", "aux")
    h.poli([w.p(*p) for p in exag], "eje", "ejes", w=0.35)
    for p in exag:
        h.nodo(w.p(*p))
    p0, p1 = exag[0], exag[1]
    ang_eje = -90.0
    ang_pl = math.degrees(math.atan2(-(p1[1] - p0[1]), p1[0] - p0[0]))
    a0_, a1_ = sorted((ang_eje, ang_pl))
    h.cota_angular(w.p(*p0), 22, a0_, a1_, "1,6°", tam=2.1)
    desvio = abs(eje[1][0] - eje[0][0])
    h.nota(w.p(*exag[1]), w.p(xs + 60, exag[1][1] + 24), "", tam=2.1,
           lineas=[f"desvío real {Me.mm(desvio, 2)} mm,", "dibujado × 10"])
    h.texto(w.p(xs - 40, 0)[0], w.p(0, G["fin"] + 30)[1], "cada plano se aparta 1,6° del eje: entre", 2.1, color=GRIS)
    h.texto(w.p(xs - 40, 0)[0], w.p(0, G["fin"] + 30)[1] + 3.0, "el primero y el segundo hay 3,2°; entre el", 2.1,
            color=GRIS)
    h.texto(w.p(xs - 40, 0)[0], w.p(0, G["fin"] + 30)[1] + 6.0, "segundo y el tercero, 1,6°", 2.1, color=GRIS)
    h.clave(w.p(*exag[1]), (w.p(*exag[1])[0] - 14, w.p(*exag[1])[1] - 8), 1)

    # 3 · el asiento, 2:1
    h.llamada(182, 146, 3, titulo="EL ASIENTO", escala="2:1")
    z = Vista(h, 192, 158, 2.0, px0=xs - 46, py0=F - 52)
    a, b = z.p(xs - 46, F - 52), z.p(xs + 46, F + 6)
    h.recorte(a[0], a[1], b[0], b[1])
    z.signo(S, nodos=False)
    h.linea(z.p(xs - 46, F), z.p(xs + 46, F), "linea", "aux")
    aa, al = G["asiento_ancho"], G["asiento_alto"]
    P0, P1, P2 = (xs - c / 2, F - al), (xs - c / 2, F), (xs - aa / 2, F)
    h.poli([z.p(*P0), z.p(*P1), z.p(*P2)], "aux", "aux")
    for p in (P0, P1, P2):
        h.add("aux", f'<rect x="{f(z.p(*p)[0] - 0.7)}" y="{f(z.p(*p)[1] - 0.7)}" width="1.4" height="1.4" '
                     f'fill="{PAPEL}" stroke="{GRIS}" stroke-width="0.18"/>')
    h.fin_recorte()
    marco_vista(h, a[0], a[1], b[0], b[1])
    h.cota(z.p(xs - aa / 2, F), z.p(xs + aa / 2, F), -6, f"2 c = {Me.cota(aa)}", tam=2.1)
    h.cota(z.p(xs + aa / 2, F), z.p(xs + aa / 2, F - al), -6, f"0,9 c = {Me.mm(al)}", tam=2.1)
    h.texto(a[0], b[1] + 13, "una curva cuadrática, cóncava: de un canal a dos", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 16, "(la apófige, sin remate)", 2.1, color=GRIS)
    h.clave(z.p(xs - aa / 2 + 6, F - 3), (a[0] + 5, a[1] + 6), 3)

    # 4 · pasos
    T = D["testigos"]["l"]

    def dibujar(i, w):
        if i == 0:
            testigo(w, T)
            w.h.linea(w.p(xs, G["arriba"]), w.p(xs, F), "aux", "aux")
        if i == 1:
            w.h.poli([w.p(*p) for p in exag], "eje", "ejes")
            for p in exag:
                w.h.nodo(w.p(*p))
        if i == 2:
            w.h.poli([w.p(*p) for p in eje], "eje", "ejes")
            for anillo in S["mas"]:
                w.h.add("cuerpo", f'<path d="{w.d(anillo)}" fill="url(#metal)" stroke="{TINTA}" stroke-width="0.25"/>')
        if i == 3:
            w.signo(S, nodos=False, ejes=False)

    y = 204
    h.llamada(32, y - 8, 4, titulo="CÓMO SE CONSTRUYE", escala="1:2")
    pasos(h, D, y, ["del pie: el asta y su alto", "tres planos (× 10)", "el asiento", "el canal, gastado"],
          dibujar, (180, 40, 420, 450))
    h.columna(bloques("P-04", M))


# ---------------------------------------------------------------- P-05 · n

def p05(h, D, M):
    Me, E = M["_"], D["esqueleto"]
    G = D["generadores"]["n"]
    S = D["signos"]["n"]
    c = Me.c
    F = E["fondo"]
    h.llamada(32, 22, 1, titulo="EL HOMBRO · VISTA", escala="1:1")
    v = vista_generador(h, D, "n", OX, OY)
    h.poli([v.p(*p) for p in G["arcos"]["2.0"]], "comparar", "aux")
    h.cota(v.p(G["xi"], G["yt"]), v.p(G["xd"], G["yt"]), 17, f"entre astas {Me.cota(G['xd'] - G['xi'])}", tam=2.2)
    h.cota(v.p(G["xd"] + c / 2, G["yh"]), v.p(G["xd"] + c / 2, G["yt"]), -9, Me.cota(G["yh"] - G["yt"]), tam=2.1)
    h.cota(v.p(G["xd"] + c / 2, F), v.p(G["xd"] + c / 2, G["yh"]), -9, Me.cota(F - G["yh"]), tam=2.1)
    h.linea(v.p(G["xi"] - 16, G["yh"]), v.p(G["xd"] + 16, G["yh"]), "aux", "aux")
    pl = v.p(G["xi"] - 18, G["yh"])
    h.texto(pl[0], pl[1] + 0.8, "caída 0,40", 2.1, "end")
    h.nota(v.p(*G["arcos"]["2.0"][88]), v.p(G["xd"] + 40, G["yt"] - 40), "", tam=2.1,
           lineas=["n = 2: elipse,", "no se eligió"])
    h.nota(v.p(*G["arcos"]["3.0"][34]), v.p(G["xi"] - 26, G["yt"] - 44), "", tam=2.1, ancla="end",
           lineas=["superelipse", "n = 3"])
    h.gravedad(OX + 145, OY + 34)
    h.clave(v.p(*G["arcos"]["3.0"][70]), v.p(G["xd"] - 20, G["yt"] - 30), 1)
    h.clave(v.p(G["xi"], G["yh"]), v.p(G["xi"] + 40, G["yh"] + 40), 2)
    h.clave(v.p(G["xi"] - 16, G["yh"]), v.p(G["xi"] - 36, G["yh"] + 30), 3)
    h.clave(v.p(G["xd"] - c / 2, (G["yh"] + F) / 2 + 20), v.p(G["xd"] - 48, (G["yh"] + F) / 2 + 40), 4)

    # 2 · la familia de arcos (1:1)
    h.llamada(182, 22, 2, titulo="LA TENSIÓN DEL ARCO", escala="1:1")
    w = Vista(h, 192, 38, 1.0, px0=G["xi"] - 10, py0=G["yt"] - 10)
    for n, tipo in (("2.0", "comparar"), ("4.0", "comparar"), ("3.0", "eje")):
        h.poli([w.p(*p) for p in G["arcos"][n]], tipo, "ejes", w=0.4 if n == "3.0" else 0.25)
    for n, i, dx, dy in (("2.0", 28, -10, 9), ("3.0", 60, 0, -8), ("4.0", 96, 12, -3)):
        p = w.p(*G["arcos"][n][i])
        h.nota(p, (p[0] + dx, p[1] + dy), f"n = {n[0]}", tam=2.1, ancla="end" if dx < 0 else "start")
    h.linea(w.p(G["xi"] - 10, G["yh"]), w.p(G["xd"] + 10, G["yh"]), "aux", "aux")
    h.texto(192, 38 + 31, "|x/a|ⁿ + |y/b|ⁿ = 1", 2.6, familia=SERIF, cursiva=True)
    h.texto(192, 38 + 35, "2: elipse · 3: la chapa · 4: casi un rectángulo", 2.1, color=GRIS)
    h.clave(w.p(*G["arcos"]["3.0"][60]), (w.p(*G["arcos"]["3.0"][60])[0] + 14, w.p(*G["arcos"]["3.0"][60])[1] - 6), 1)

    # 3 · el encuentro tangente, 2:1
    h.llamada(182, 112, 3, titulo="EL ENCUENTRO TANGENTE", escala="2:1")
    z = Vista(h, 192, 124, 2.0, px0=G["xi"] - 40, py0=G["yt"] - 26)
    a, b = z.p(G["xi"] - 40, G["yt"] - 26), z.p(G["xi"] + 60, G["yh"] + 30)
    h.recorte(a[0], a[1], b[0], b[1])
    z.signo(S, nodos=True)
    h.fin_recorte()
    marco_vista(h, a[0], a[1], b[0], b[1])
    pt = z.p(G["xi"], G["yh"])
    h.linea((pt[0], a[1]), (pt[0], b[1]), "aux", "aux")
    h.texto(a[0], b[1] + 4.2, "sale del fuste en su misma dirección:", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 7.2, "no hay rincón, no hace falta alivio", 2.1, color=GRIS)
    h.clave(pt, (pt[0] + 12, pt[1] + 8), 2)

    # 4 · pasos
    T = D["testigos"]["n"]
    arco = G["arcos"]["3.0"]
    fuste = S["trazos"][0][0]

    def dibujar(i, w):
        if i == 0:
            testigo(w, T)
            for x in (G["xi"], G["xd"]):
                w.h.linea(w.p(x, G["tope"]), w.p(x, F), "aux", "aux")
        if 1 <= i < 3:
            w.h.poli([w.p(*p) for p in fuste], "eje", "ejes")
        if i == 2:
            w.h.poli([w.p(*p) for p in S["trazos"][1][0]], "eje", "ejes")
            w.h.poli([w.p(*p) for p in arco], "aux", "aux")
        if i == 3:
            w.signo(S, nodos=False, ejes=False)

    y = 204
    h.llamada(32, y - 8, 4, titulo="CÓMO SE CONSTRUYE", escala="1:2")
    pasos(h, D, y, ["del pie: las astas", "el fuste, desde el borde", "el arco y la bajada", "asientos y canal"],
          dibujar, (180, 180, 420, 450))
    h.columna(bloques("P-05", M))


# ---------------------------------------------------------------- P-06 · a

def p06(h, D, M):
    Me, E = M["_"], D["esqueleto"]
    G = D["generadores"]["a"]
    S = D["signos"]["a"]
    c = Me.c
    F = E["fondo"]
    h.llamada(32, 22, 1, titulo="EL GANCHO Y LA GOTA · VISTA", escala="1:1")
    v = vista_generador(h, D, "a", OX, OY)
    cen = v.p(G["cxg"], G["yh"])
    h.punto(cen, 0.5)
    h.linea(cen, v.p(G["cxg"] + G["rx"] + 10, G["yh"]), "aux", "aux")
    gp = v.p(*G["gota_p"])
    h.linea(cen, gp, "aux", "aux")
    h.cota_angular(cen, 9, 0, G["gancho_fin"], "105°", tam=2.1)
    gc = G["gota_centro"]
    h.linea(v.p(gc[0], G["gota_p"][1] - 34), v.p(gc[0], G["cuenca_arriba"] + 6), "eje", "ejes", w=0.13)
    h.nota(v.p(gc[0], G["gota_p"][1] - 30), v.p(gc[0] - 50, G["gota_p"][1] - 52), "plomada", tam=2.1, ancla="end")
    libre = Me.libre_gota()
    yl0 = gc[1] + 0.65 * Me.v("gota_masa")
    h.cota(v.p(gc[0], yl0 + libre), v.p(gc[0], yl0), 0.01, "", ext=False)
    h.nota(v.p(gc[0], yl0 + libre / 2), v.p(G["cuenca_izq"] - 50, yl0 + 14), "", tam=2.1, ancla="end",
           lineas=[f"libre {Me.cota(libre)}", f"(la regla pide {Me.mm(G['libre'])})"])
    h.nota(v.p(G["xs"] + c / 2, G["yh"] + 40), v.p(G["xs"] + 66, G["yh"] + 22), "fuste (l)", tam=2.1)
    h.nota(v.p(G["xs"] - 6, G["yt"] - c / 2 + 2), v.p(G["xs"] + 50, G["yt"] - 30), "gancho (n)", tam=2.1)
    h.nota(v.p(G["cuenca_izq"] + 3, F - 40), v.p(G["cuenca_izq"] - 50, F + 26), "cuenca (o)", tam=2.1, ancla="end")
    h.gravedad(OX + 145, OY + 34)
    h.clave(v.p(*G["gota_p"]), v.p(G["gota_p"][0] - 40, G["gota_p"][1] - 70), 1)
    h.clave(v.p(gc[0] - Me.v("gota_masa") / 2, gc[1]), v.p(gc[0] - 64, gc[1] - 18), 2)
    h.clave(v.p(G["cuenca_izq"] + c / 2 + 2, F - 34), v.p(G["cuenca_izq"] + 48, F - 52), 3)
    h.clave(v.p(G["xs"] + c / 2, F - 70), v.p(G["xs"] + 48, F - 52), 4)

    # 2 · la gota, 5:1
    h.llamada(182, 22, 2, titulo="LA GOTA", escala="5:1")
    gp_ = G["gota_p"]
    fin = G["gota_fin"]
    ventana = (gc[0] - 24, gp_[1] - 18, gc[0] + 24, gc[1] + 0.65 * Me.v("gota_masa") + 6)
    z = Vista(h, 214, 34, 5.0, px0=ventana[0], py0=ventana[1])
    a, b = z.p(ventana[0], ventana[1]), z.p(ventana[2], ventana[3])
    h.recorte(a[0], a[1], b[0], b[1])
    z.signo(S, nodos=False)
    h.fin_recorte()
    marco_vista(h, a[0], a[1], b[0], b[1])
    masa, caida, cuello = Me.v("gota_masa"), Me.v("gota_caida"), Me.v("gota_cuello")
    yc = gc[1]
    # la construcción: un trapecio del terminal al centro de la masa, y un círculo estirado 1,15 hacia abajo
    trap = [(gp_[0] - c / 2, gp_[1]), (gp_[0] + c / 2, gp_[1]), (gc[0] + cuello / 2, yc), (gc[0] - cuello / 2, yc)]
    h.poli([z.p(*q) for q in trap], "aux", "ejes", cerrado=True)
    h.add("ejes", f'<circle cx="{f(z.p(*gc)[0])}" cy="{f(z.p(*gc)[1])}" r="{f(z.mm(masa / 2))}" {estilo("aux")}/>')
    ye = yc + 0.075 * masa
    h.add("ejes", f'<ellipse cx="{f(z.p(gc[0], ye)[0])}" cy="{f(z.p(gc[0], ye)[1])}" rx="{f(z.mm(masa / 2))}" '
                  f'ry="{f(z.mm(1.15 * masa / 2))}" {estilo("aux")}/>')
    h.linea(z.p(gc[0], ventana[1]), z.p(gc[0], ventana[3]), "eje", "ejes", w=0.13)
    h.cota(z.p(gc[0] - masa / 2, ye), z.p(gc[0] + masa / 2, ye), 0.01, "", ext=False)
    h.nota(z.p(gc[0] - masa / 2 + 1, ye), (a[0] - 3, z.p(0, ye)[1] + 10), f"masa Ø {Me.cota(masa)}", tam=2.1,
           ancla="end")
    h.cota(z.p(gc[0] - cuello / 2, yc), z.p(gc[0] + cuello / 2, yc), 0.01, "", ext=False, ticks=True)
    h.nota(z.p(gc[0] - cuello / 2, yc), (a[0] - 3, z.p(0, yc)[1] - 4), "", tam=2.1, ancla="end",
           lineas=[f"cuello {Me.cota(cuello)}", "(en el centro de la masa)"])
    h.cota(z.p(gc[0] - masa / 2 - 4, gp_[1] + caida), z.p(gc[0] - masa / 2 - 4, gp_[1]), 0.01, "", ext=False)
    h.nota(z.p(gc[0] - masa / 2 - 4, gp_[1] + caida / 2), (a[0] - 3, z.p(0, gp_[1])[1] - 8),
           f"caída {Me.cota(caida)}", tam=2.1, ancla="end")
    h.texto(a[0], b[1] + 4.2, "en línea de construcción: un trapecio de c a 0,55 c,", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 7.2, "del terminal al centro de la masa, y un círculo de", 2.1, color=GRIS)
    h.texto(a[0], b[1] + 10.2, "1,25 c estirado 1,15 hacia abajo, por su peso", 2.1, color=GRIS)
    h.clave(z.p(gc[0] + masa / 2, ye + 8), (b[0] - 6, z.p(0, ye)[1] + 22), 2)

    # 3 · pasos
    T = D["testigos"]["a"]
    gancho = superelipse(G["cxg"], G["yh"], G["rx"], G["ry"], 3.0, G["gancho_fin"], 0)

    def dibujar(i, w):
        if i == 0:
            testigo(w, T)
            x0, y0, x1, y1 = T["ojo"]
            w.h.add("aux", f'<rect x="{f(w.p(x0, y0)[0])}" y="{f(w.p(x0, y0)[1])}" width="{f(w.mm(x1 - x0))}" '
                           f'height="{f(w.mm(y1 - y0))}" {estilo("aux")}/>')
            w.h.linea(w.p(T["gancho"], 200), w.p(T["gancho"], 300), "aux", "aux")
        if i >= 1:
            w.h.poli([w.p(*p) for p in gancho], "eje", "ejes")
            w.h.linea(w.p(G["xs"], G["yh"]), w.p(G["xs"], F - 30), "eje", "ejes")
        if i == 2:
            for anillo in S["mas"]:
                w.h.add("cuerpo", f'<path d="{w.d(anillo)}" fill="url(#metal)" stroke="{TINTA}" stroke-width="0.25"/>')
        if i == 3:
            w.signo(S, nodos=False, ejes=False)

    y = 204
    h.llamada(32, y - 8, 3, titulo="CÓMO SE CONSTRUYE", escala="1:2")
    pasos(h, D, y, ["del pie: ojo y gancho", "el gancho y el fuste", "la gota y el asiento", "la cuenca"],
          dibujar, (180, 180, 420, 450))
    h.columna(bloques("P-06", M))


# ---------------------------------------------------------------- P-07 · las partes

PARTES = [
    ("la cuenca", "o", "desagüe", "la o", "b d p q a e g 0 6 8 9", "trapecio · pared · desagüe", 1),
    ("la cuenca abierta", "u", "cuenca abierta", "la o, sin cerrar", "c e u j t", "trapecio · pared", None),
    ("el fuste", "l", "asiento", "la l", "casi todas", "facetas · quiebre · asiento", None),
    ("el hombro", "n", "hombro", "la n", "h m r f s 2 3 5 6 9 ? ¿", "hombro · caída", None),
    ("el gancho y la gota", "c", "gota", "la a", "a á c f r s y 2 3 6 ? ,", "gancho_fin · gota", 2),
    ("la recta y el alivio", "k", "alivio", "nueva", "k v w x y z 1 2 4 7 « »", "radio_chapa · alivio", None),
    ("el punto", "i", "punto", "la cinta (D12)", "i j ü . , ; : … ? ¿", "punto = cinta = canal", 3),
    ("la tilde", "é", "tilde", "la gota", "á é í ó ú", "canal", 5),
    ("la onda", "ñ", "onda", "el agua tocada (D15)", "ñ", "canal", None),
    ("el sifón", "g", "sifón", "dos cuencas", "g 8", "sifon", None),
    ("la celda de la cifra", "5", "celda", "la cabeza de la ídolo", "0 1 2 3 4 5 6 7 8 9", "0,35 canal · desagüe", 4),
    ("el corte que mira arriba", "e", "corte: mira arriba", "la gravedad", "e j s 3 5 9 ¿", "intemperie", 2),
]


def p07(h, D, M):
    E = D["esqueleto"]
    h.llamada(32, 22, 1, titulo="CUADRO DE PARTES", escala="1:4 · la parte, marcada en un signo")
    filas = len(PARTES) // 2
    alto = 40.5
    for i, (nombre, s, marca, viene, esta, param, regla) in enumerate(PARTES):
        col, fila = divmod(i, filas)
        x = 30 + col * 126
        y = 34 + fila * alto
        S = D["signos"][s]
        w = Vista(h, x, y + 1, 0.25, px0=E["celda"][0], py0=E["celda"][1])
        w.celda(E)
        for k in ("afuera", "borde", "fondo", "desague"):
            h.linea(w.p(E["celda"][0], E[k]), w.p(E["celda"][2], E[k]), "linea", "fondo", w=0.13)
        w.signo(S, nodos=False, ejes=False)
        for n, mx, my in S["marcas"]:
            if n.startswith(marca):
                p = w.p(mx, my)
                h.circulo(p, 3.0, "cota", "cotas", w=0.3, color=VIOLETA)
                break
        tx = x + 34
        h.texto(tx, y + 4, f"{i + 1:02d}", 2.3, peso=700, color=GRIS)
        h.texto(tx + 7, y + 4.2, nombre, 3.6, familia=SERIF)
        if regla:
            h.rombo((x + 118, y + 3), regla)
        filas_txt = (("VIENE DE", viene), ("ESTÁ EN", esta), ("SE MIDE", param))
        for j, (k, val) in enumerate(filas_txt):
            h.texto(tx, y + 10.5 + j * 5, k, 1.7, color=GRIS, espaciado=0.2)
            h.texto(tx + 18, y + 10.5 + j * 5, val, 2.3)
        h.texto(tx, y + 25.5, "RECETA", 1.7, color=GRIS, espaciado=0.2)
        h.parrafo(tx + 18, y + 25.5, 66, f"{s}: {S['receta']}", 2.0, inter=1.3, familia=MONO, peso=400, color=GRIS)
        h.linea((x, y + alto - 3), (x + 120, y + alto - 3), "fina", "textos")
    h.columna(bloques("P-07", M))


# ---------------------------------------------------------------- P-08 · detalles

def p08(h, D, M):
    Me, E = M["_"], D["esqueleto"]
    c = Me.c
    cajas = [(30, 32), (114, 32), (198, 32), (30, 152), (114, 152), (198, 152)]
    W, H = 76, 98

    def marca(s, nombre):
        for n, x, y in D["signos"][s]["marcas"]:
            if n.startswith(nombre):
                return x, y
        raise KeyError(nombre)

    def detalle(i, titulo, s, centro):
        x, y = cajas[i]
        h.llamada(x + 4, y - 8, i + 1, titulo=titulo, escala="2:1")
        cx, cy = centro
        px_w, px_h = W * 4 / 2, (H - 24) * 4 / 2
        v = Vista(h, x, y, 2.0, px0=cx - px_w / 2, py0=cy - px_h / 2)
        recorte_signo(v, D["signos"][s], (cx - px_w / 2, cy - px_h / 2, cx + px_w / 2, cy + px_h / 2))
        return v

    def pie(i, *lineas):
        x, y = cajas[i]
        for j, r in enumerate(lineas):
            h.texto(x, y + H - 20 + j * 3.1, r, 2.1, color=GRIS)

    # 1 · el punto (i)
    xi, yi = marca("i", "punto")
    lado = Me.v("punto")
    cxp = xi - lado / 2
    v = detalle(0, "EL PUNTO · i", "i", (cxp, yi + 28))
    h.cota(v.p(cxp - lado / 2, yi - lado / 2), v.p(cxp + lado / 2, yi - lado / 2), 6, Me.cota(lado), tam=2.1)
    h.cota(v.p(cxp + lado / 2, yi + lado / 2), v.p(cxp + lado / 2, yi - lado / 2), -6, Me.mm(lado), tam=2.1)
    h.clave(v.p(cxp - lado / 2, yi), (v.p(cxp - lado / 2, yi)[0] - 12, v.p(cxp - lado / 2, yi)[1] + 6), 1)
    pie(0, "un trozo cuadrado de cinta, lado = canal")

    # 2 · la tilde (é)
    xt, yt = marca("é", "tilde")
    v = detalle(1, "LA TILDE · é", "é", (xt - 0.35 * c, yt + 1.25 * c))
    cen = v.p(xt - 0.7 * c, yt + 1.2 * c + 0.35 * c)
    h.cota_radio(cen, v.mm(0.5 * c), 215, f"{Me.mm(0.5 * c)} · 0,5 c", largo=7)
    cerca = [(x_, y_) for r in D["signos"]["é"]["contorno"] for x_, y_ in r if abs(x_ - xt) < c and y_ < yt + 0.8 * c]
    punta = min(cerca, key=lambda q: q[1]) if cerca else (xt, yt)
    h.nota(v.p(*punta), (v.p(*punta)[0] + 7, v.p(*punta)[1] - 3), "la punta, arriba", tam=2.1)
    h.clave(cen, (cen[0] + 6, cen[1] + 14), 2)
    pie(1, "una gota: la punta arriba, el peso abajo")

    # 3 · la onda (ñ)
    xo, yo = marca("ñ", "onda")
    Gn = D["generadores"]["n"]
    largo = Gn["xd"] - Gn["xi"] + 0.2 * c
    x0o = xo - largo
    v = detalle(2, "LA ONDA · ñ", "ñ", (xo - largo / 2, yo + 12))
    h.cota(v.p(x0o - 6, yo + 0.35 * c), v.p(x0o - 6, yo - 0.35 * c), 5, "0,7 c", tam=2.0)
    h.cota(v.p(x0o, yo + 0.35 * c + 20), v.p(xo, yo + 0.35 * c + 20), -4, Me.cota(largo), tam=2.1)
    h.clave(v.p(xo - largo * 0.75, yo - 0.35 * c), (v.p(xo - largo * 0.75, yo)[0] + 4, v.p(0, yo)[1] - 12), 3)
    pie(2, "un período de onda: el agua tocada")

    # 4 · el sifón (g)
    xg, yg = marca("g", "sifón")
    v = detalle(3, "EL SIFÓN · g", "g", (xg + 8, yg))
    S = D["signos"]["g"]
    sif = [t for t in S["trazos"] if t[1] is not None and abs(t[1] - Me.v("sifon") * c) < 0.5]
    if sif:
        (pa, pb), w_ = sif[0][0][:2], sif[0][1]
        pm = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
        L = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        nx, ny = -(pb[1] - pa[1]) / L, (pb[0] - pa[0]) / L
        q1 = v.p(pm[0] - nx * w_ / 2, pm[1] - ny * w_ / 2)
        q2 = v.p(pm[0] + nx * w_ / 2, pm[1] + ny * w_ / 2)
        h.cota(q1, q2, 0.01, "", ext=False)
        h.nota(q2, (q2[0] + 12, q2[1] + 4), f"{Me.mm(w_)} · 0,6 c", tam=2.1)
        h.clave(q1, (q1[0] - 12, q1[1] - 6), 4)
    pie(3, "vasos comunicantes: el único trazo más fino")

    # 5 · el alivio (k)
    S = D["signos"]["k"]
    ax, ay, ar = S["alivios"][1]
    v = detalle(4, "EL ALIVIO · k", "k", (ax, ay))
    h.circulo(v.p(ax, ay), v.mm(ar), "aux", "cotas")
    h.cota_radio(v.p(ax, ay), v.mm(ar), 300, f"{Me.cota(ar)} · 0,28 c", largo=12)
    h.clave(v.p(ax - ar, ay), (v.p(ax - ar, ay)[0] - 12, v.p(ax, ay)[1] - 8), 5)
    pie(4, "en el rincón agudo, sobre la bisectriz")

    # 6 · la celda de la cifra (5), 1:2
    x, y = cajas[5]
    h.llamada(x + 4, y - 8, 6, titulo="LA CELDA · 5", escala="1:2")
    cel = E["celda"]
    v = Vista(h, x + 9, y + 1, 0.5, px0=cel[0], py0=cel[1])
    v.celda(E)
    v.signo(D["signos"]["5"], nodos=False)
    h.clave(v.p(cel[0] + 0.3 * c, (cel[1] + cel[3]) / 2), (x + 3, y + 30), 6)
    pie(5, "", "", "", "")
    h.texto(x, y + 73.5, "dos rectángulos, a 0,3 c y a 1,3 c del borde,", 2.1, color=GRIS)
    h.texto(x, y + 76.6, f"con un trazo de 0,35 c ({Me.mm(0.35 * c)} mm) y desagüe abajo", 2.1, color=GRIS)
    h.columna(bloques("P-08", M))


# ---------------------------------------------------------------- P-09 · dobles opuestos

def _transformar(anillos, modo, desde, hacia):
    """Da vuelta (rot180) o espeja (espejo) los anillos sobre el centro de su caja y los lleva al centro de otra."""
    cx0, cy0 = desde
    cx1, cy1 = hacia
    out = []
    for r in anillos:
        q = []
        for x, y in r:
            x2, y2 = (2 * cx0 - x, 2 * cy0 - y) if modo == "rot180" else (2 * cx0 - x, y)
            q.append((x2 - cx0 + cx1, y2 - cy0 + cy1))
        out.append(q)
    return out


def p09(h, D, M):
    E = D["esqueleto"]
    pares = [("?", "¿", "rot180", "dada vuelta"), ("6", "9", "rot180", "dado vuelta"), ("«", "»", "espejo", "en espejo")]
    cel = E["celda"]
    for i, (A, B, modo, como) in enumerate(pares):
        y = 30 + i * 86
        h.llamada(32, y - 8, i + 1, titulo=f"{A}  Y  {B}", escala="1:2")
        for j, s in enumerate((A, B, B)):
            x = 34 + j * 76
            v = Vista(h, x, y + 1, 0.5, px0=cel[0], py0=cel[1])
            v.celda(E)
            for k in ("afuera", "borde", "fondo", "desague"):
                h.linea(v.p(cel[0], E[k]), v.p(cel[2], E[k]), "linea", "fondo", w=0.13)
            S = D["signos"][s]
            v.signo(S, nodos=False, ejes=j < 2)
            if j == 2:
                SA = D["signos"][A]
                ca = ((SA["caja"][0] + SA["caja"][2]) / 2, (SA["caja"][1] + SA["caja"][3]) / 2)
                cb = ((S["caja"][0] + S["caja"][2]) / 2, (S["caja"][1] + S["caja"][3]) / 2)
                h.add("ejes", f'<path d="{v.d(_transformar(SA["contorno"], modo, ca, cb))}" '
                              f'{estilo("comparar", color=TINTA, w=0.3)}/>')
            rot = s if j < 2 else f"{B}, y encima {A} {como}"
            h.texto(x, y + 73, rot, 2.4 if j < 2 else 2.2)
        for j, s in ((0, A), (1, B)):
            S = D["signos"][s]
            x = 34 + j * 76
            v = Vista(h, x, y + 1, 0.5, px0=cel[0], py0=cel[1])
            for n, mx, my in S["marcas"]:
                if n == "gota" or n.startswith("sin gota") or n.startswith("corte"):
                    p = v.p(mx, my)
                    txt = "gotea" if n == "gota" else "no gotea: mira arriba"
                    h.nota(p, (p[0] + 12, p[1] + (-8 if n == "gota" else 8)), txt, tam=2.0)
                    if j == 1:
                        h.clave(p, (p[0] - 10, p[1] + 10), i + 1)
                    break
        if A == "«":
            h.texto(34 + 76, y + 76.5, "armadas con su propio azar", 2.1, color=GRIS)
            h.clave(Vista(h, 34 + 76, y + 1, 0.5, px0=cel[0], py0=cel[1]).p(330, 330), (34 + 76 + 48, y + 30), 3)
    h.columna(bloques("P-09", M))


# ---------------------------------------------------------------- P-10 · la caja

def p10(h, D, M):
    import json
    E = D["esqueleto"]
    caja = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
    k = 0.2                                 # 1:5
    lado, junta = 150 * k, 3 * k
    ox, oy = 27.0, 30.0
    h.llamada(32, 22, 1, titulo="LA CAJA · PLAN GENERAL", escala="1:5")
    for celda in caja["celdas"]:
        s, n = celda["signo"], celda["celda"]
        col, fila = celda["columna"] - 1, celda["fila"] - 1
        x = ox + col * (lado + junta)
        y = oy + fila * (lado + junta)
        h.add("fondo", f'<rect x="{f(x)}" y="{f(y)}" width="{f(lado)}" height="{f(lado)}" {estilo("placa", w=0.25)}/>')
        v = Vista(h, x, y, k)
        if s in D["signos"]:
            S = D["signos"][s]
            v.celda(E, "fina")
            h.linea(v.p(E["celda"][0], E["fondo"]), v.p(E["celda"][2], E["fondo"]), "linea", "fondo", w=0.1)
            v.signo(S, nodos=False, ejes=False)
            h.texto(x + lado - 1.2, y + 2.8, familia(s), 2.0, "end", color=GRIS, familia=SERIF, cursiva=True)
        else:
            h.texto(x + lado / 2, y + lado / 2 + 1, "¶", 7, "middle", familia=SERIF, color=GRIS2)
            h.texto(x + lado / 2, y + lado - 3.5, "con los dedos", 1.9, "middle", color=GRIS)
            h.clave((x + lado / 2, y + lado / 2 + 3), (x + lado - 4, y + 6), 4)
        h.texto(x + 1.2, y + 2.8, str(n), 1.9, color=VIOLETA if celda["estado"] != "hallada" else TINTA)
    h.add("cotas", f'<rect x="{f(ox - 1.2)}" y="{f(oy - 1.2)}" width="{f(lado + 2.4)}" height="{f(lado + 2.4)}" '
                   f'{estilo("comparar", color=VIOLETA, w=0.35)}/>')
    qx, qy = ox + lado + 62, oy - 5
    h.punto((ox + lado + 1.2, oy + 3), 0.45, VIOLETA)
    h.linea((ox + lado + 1.2, oy + 3), (qx, qy), "cota", "cotas", color=VIOLETA)
    h.rombo((qx + 3, qy), 5)
    h.texto(qx + 6.5, qy + 0.8, "la puerta de la tapa, sobre la celda 1 (D4)", 2.1, color=VIOLETA)
    h.clave((ox + 2.5, oy + 2), (ox + 6, oy + 9), 3)
    W = 8 * lado + 7 * junta
    Hh = 7 * lado + 6 * junta
    h.cota((ox, oy + Hh), (ox + lado, oy + Hh), -5, "150", tam=2.1)
    h.cota((ox + lado, oy + Hh), (ox + lado + junta, oy + Hh), -5, "", tam=2.1)
    h.texto(ox + lado + junta / 2, oy + Hh + 9.5, "junta 3", 2.0, "middle")
    h.cota((ox, oy + Hh), (ox + W, oy + Hh), -14, "1221", tam=2.3)
    h.cota((ox + W, oy + Hh), (ox + W, oy), -5, "1068", tam=2.3)
    h.clave((ox + W / 2 + 18, oy + Hh + 14), (ox + W / 2 + 28, oy + Hh + 20), 2)
    h.texto(ox, oy + Hh + 25, "en metal y línea continua: lo hallado · en violeta y a puntos: lo reconstruido · "
                              "arriba: la celda y su generador (o, l, n, a)", 2.2, color=GRIS)
    h.texto(ox + 6, oy + Hh + 29.6, "solo caja baja: las mayúsculas no tienen celda; una mayúscula tecleada se escribe "
                                    "en caja baja", 2.2, color=GRIS)
    h.rombo((ox + 2.5, oy + Hh + 28.8), 1)
    h.escala_grafica(ox, oy + Hh + 34, k, 500, 100, "mm")
    h.columna(bloques("P-10", M))


# ---------------------------------------------------------------- el DXF

def dxf(D, M, ruta, signos, caja=False):
    """La vista a 1:1 en mm reales, con el origen en el fondo y el borde izquierdo de la celda (como la fuente)."""
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
    E = D["esqueleto"]
    cx0, cy0, cx1, cy1 = E["celda"]
    F = E["fondo"]
    doc = ezdxf.new("R2010", setup=True, units=4)          # 4: milímetros
    for nombre, color, tipo in (("CONTORNO", 7, "CONTINUOUS"), ("RECONSTRUIDO", 6, "DOTTED"), ("EJE", 1, "DASHDOT"),
                                ("LINEAS", 8, "DASHED"), ("CELDA", 8, "CONTINUOUS"), ("PLACA", 9, "CONTINUOUS"),
                                ("NODOS", 3, "CONTINUOUS"), ("ALIVIOS", 5, "DASHED"), ("COTAS", 2, "CONTINUOUS"),
                                ("TEXTO", 7, "CONTINUOUS")):
        doc.layers.add(nombre, color=color, linetype=tipo)
    doc.header["$LTSCALE"] = 2.0
    msp = doc.modelspace()

    def P(x, y, dx=0.0, dy=0.0):
        return ((x - cx0) / 4 + dx, (F - y) / 4 + dy)

    def un_signo(s, dx, dy, ejes=True, cotas=False):
        S = D["signos"][s]
        capa = "RECONSTRUIDO" if S["estado"] == "reconstruida" else "CONTORNO"
        for r in S["contorno"]:
            msp.add_lwpolyline([P(x, y, dx, dy) for x, y in r], close=True, dxfattribs={"layer": capa})
        if ejes:
            for pts, ancho in S["trazos"]:
                if ancho is not None and ancho < 1:
                    continue
                msp.add_lwpolyline([P(x, y, dx, dy) for x, y in pts], dxfattribs={"layer": "EJE"})
            for x, y in S["nodos"]:
                msp.add_circle(P(x, y, dx, dy), 0.6, dxfattribs={"layer": "NODOS"})
            for x, y, r in S["alivios"]:
                msp.add_circle(P(x, y, dx, dy), r / 4, dxfattribs={"layer": "ALIVIOS"})

    def marco(dx, dy, rotulos=True):
        msp.add_lwpolyline([P(0, 0, dx, dy), P(600, 0, dx, dy), P(600, 600, dx, dy), P(0, 600, dx, dy)], close=True,
                           dxfattribs={"layer": "PLACA"})
        msp.add_lwpolyline([P(cx0, cy0, dx, dy), P(cx1, cy0, dx, dy), P(cx1, cy1, dx, dy), P(cx0, cy1, dx, dy)],
                           close=True, dxfattribs={"layer": "CELDA"})
        for nombre, k in (("afuera", "afuera"), ("borde", "borde"), ("fondo", "fondo"), ("desagüe", "desague")):
            msp.add_line(P(0, E[k], dx, dy), P(600, E[k], dx, dy), dxfattribs={"layer": "LINEAS"})
            if rotulos:
                msp.add_text(f"{nombre} {M['_'].nivel(E[k])}", height=2.0, dxfattribs={"layer": "TEXTO"}).set_placement(
                    P(4, E[k] - 6, dx, dy), align=TextEntityAlignment.BOTTOM_LEFT)

    if caja:
        import json
        cj = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
        for celda in cj["celdas"]:
            dx = (celda["columna"] - 1) * 153.0
            dy = -(celda["fila"] - 1) * 153.0
            marco(dx, dy, rotulos=False)
            if celda["signo"] in D["signos"]:
                un_signo(celda["signo"], dx, dy, ejes=False)
            msp.add_text(f"{celda['celda']} {celda['signo']}", height=4.0, dxfattribs={"layer": "TEXTO"}).set_placement(
                P(8, 20, dx, dy), align=TextEntityAlignment.BOTTOM_LEFT)
    else:
        marco(0, 0)
        for s in signos:
            un_signo(s, 0, 0)
        # cotas de la celda: alto y ancho
        d = msp.add_linear_dim(base=P(cx0, cy1, 0, -12), p1=P(cx0, cy1), p2=P(cx1, cy1), dimstyle="EZDXF",
                               dxfattribs={"layer": "COTAS"})
        d.render()
        d = msp.add_linear_dim(base=P(cx0, cy0, -12, 0), p1=P(cx0, cy1), p2=P(cx0, cy0), angle=90, dimstyle="EZDXF",
                               dxfattribs={"layer": "COTAS"})
        d.render()
        G = D["generadores"]
        if signos == ["o"]:
            o = G["o"]
            for p1, p2, off in ((P(o["xi"], o["cy"]), P(o["xd"], o["cy"]), -40),
                                (P(o["fondo_izq"], o["yb"]), P(o["fondo_der"], o["yb"]), -12)):
                d = msp.add_linear_dim(base=(p1[0], P(0, o["yb"])[1] + off), p1=p1, p2=p2, dimstyle="EZDXF",
                                       dxfattribs={"layer": "COTAS"})
                d.render()
        if signos == ["a"]:
            a = G["a"]
            c = P(a["cxg"], a["yh"])
            ang = math.radians(a["gancho_fin"])
            d = msp.add_angular_dim_cra(center=c, radius=12, start_angle=0, end_angle=a["gancho_fin"], distance=4,
                                        dimstyle="EZDXF", dxfattribs={"layer": "COTAS"})
            d.render()
            _ = ang
        if signos == ["n"]:
            n = G["n"]
            d = msp.add_linear_dim(base=(0, P(0, n["yt"])[1] + 20), p1=P(n["xi"], n["yt"]), p2=P(n["xd"], n["yt"]),
                                   dimstyle="EZDXF", dxfattribs={"layer": "COTAS"})
            d.render()
        if signos == ["l"]:
            l_ = G["l"]
            d = msp.add_linear_dim(base=P(l_["xs"], 0, 25, 0), p1=P(l_["xs"], F), p2=P(l_["xs"], l_["arriba"]),
                                   angle=90, dimstyle="EZDXF", dxfattribs={"layer": "COTAS"})
            d.render()
    msp.add_text("Contenida · anatomía base · propuesta de la máquina (simulacion/gramatica.py) · mm · origen: fondo "
                 "y borde izquierdo de la celda", height=2.5, dxfattribs={"layer": "TEXTO"}).set_placement(
        P(0, 640), align=TextEntityAlignment.BOTTOM_LEFT)
    doc.saveas(ruta)


# ---------------------------------------------------------------- salida

def chrome():
    from generar_laminas import chrome as ch
    return ch()


def imprimir(hojas, ruta_pdf):
    """Las láminas en un HTML de páginas A3, y Chromium lo pasa a PDF."""
    paginas = "\n".join(f'<div class="hoja">{svg}</div>' for svg in hojas)
    html_ = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Contenida · planos</title><style>'
             f'@page{{size:420mm 297mm;margin:0}}html,body{{margin:0;padding:0;background:{PAPEL}}}'
             f'.hoja{{width:420mm;height:297mm;overflow:hidden;page-break-after:always;break-after:page}}'
             f'.hoja svg{{display:block;width:420mm;height:297mm}}</style></head><body>{paginas}</body></html>')
    tmp = AQUI / "_imprimir.html"
    tmp.write_text(html_, encoding="utf8")
    ejecutable = chrome()
    modo = [] if ejecutable.endswith("headless_shell") else ["--headless=new"]
    subprocess.run([ejecutable, *modo, "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--virtual-time-budget=8000", f"--print-to-pdf={ruta_pdf}", "--no-pdf-header-footer",
                    tmp.as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", help="guarda (o lee) la geometría de la gramática en este JSON")
    ap.add_argument("--solo", help="solo esta lámina (P-03, por ejemplo), sin PDF ni DXF")
    args = ap.parse_args()
    D = leer(args.cache)
    Me = Medidas(D)
    M = Me.tabla()
    M["_"] = Me
    funciones = [p00, p01, p02, p03, p04, p05, p06, p07, p08, p09, p10]
    SVG, PNG, DXF = AQUI / "svg", AQUI / "png", AQUI / "dxf"
    for d in (SVG, PNG, DXF):
        d.mkdir(exist_ok=True)
    hojas = []
    for i, ((cod, tit, sub, esc), fn, nombre) in enumerate(zip(LAMINAS, funciones, NOMBRES_ARCHIVO)):
        if args.solo and cod != args.solo:
            continue
        h = Hoja(cod, tit, sub, esc, i + 1, len(LAMINAS))
        fn(h, D, M)
        h.marco()
        (SVG / f"{cod}_{nombre}.svg").write_text(h.svg("../../laminas/fuentes"), encoding="utf8")
        hojas.append(h.svg("../laminas/fuentes"))
        print(f"{cod}: {tit}")
    ruta_pdf = AQUI / ("contenida_planos.pdf" if not args.solo else f"_{args.solo}.pdf")
    imprimir(hojas, ruta_pdf)
    import fitz
    doc = fitz.open(ruta_pdf)
    nombres = [n for (cod, *_), n in zip(LAMINAS, NOMBRES_ARCHIVO) if not args.solo or cod == args.solo]
    codigos = [cod for cod, *_ in LAMINAS if not args.solo or cod == args.solo]
    for pag, cod, nombre in zip(doc, codigos, nombres):
        pag.get_pixmap(dpi=110).save(PNG / f"{cod}_{nombre}.png")
    doc.close()
    if args.solo:
        ruta_pdf.unlink()
        return
    dxf(D, M, DXF / "P-01_celda.dxf", [])
    for cod, s, nombre in (("P-03", "o", "o_cuenca"), ("P-04", "l", "l_fuste"), ("P-05", "n", "n_hombro"),
                           ("P-06", "a", "a_gancho_y_gota")):
        dxf(D, M, DXF / f"{cod}_{nombre}.dxf", [s])
    dxf(D, M, DXF / "P-10_caja.dxf", [], caja=True)
    print("listo:", ruta_pdf)


if __name__ == "__main__":
    main()
