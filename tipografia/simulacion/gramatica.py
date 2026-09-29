"""Gramática de Contenida: la anatomía base en vectores, antes de los estados.

Uso (desde la raíz del repositorio):
    pip install shapely
    python3 tipografia/simulacion/gramatica.py

El orden es: anatomía base → estados. Del pie se toman solo medidas: dónde
van las astas, cuánto miden los ojos, los hombros y las líneas (el esqueleto
de referencia de cada testigo). Cómo es la forma lo deciden parámetros que
salen de la obra (03c_gramatica.md): el punzón sobre el aluminio, la vasija
abierta, la chapa sobre el cuerpo, la intemperie y la gravedad.

Cuatro glifos generadores (o, l, n, a) dan las partes: la cuenca, el fuste,
el hombro, el gancho con su gota. Con esas partes, más el punto (un trozo de
cinta), la tilde, la onda, la recta y el alivio, se arman los 55 signos. Como
en la iconografía que Agüero, Uribe y Berenguer (2003) analizan en la
litoescultura de Tiwanaku, los elementos se combinan en motivos y los motivos
en figuras; y los dobles opuestos no son idénticos: varían.

simular.py usa construir_todo(). Corrido solo, este archivo escribe en
simulacion/salida/:
  20_gramatica.png          los cuatro generadores: testigo, curvas, cuerpo, calco y cinta,
  21_gramatica_caja.png     los 55 cuerpos base en la caja de 8 × 7,
  gramatica/<signo>.svg     el cuerpo base de cada generador,
  gramatica/gramatica.json  los parámetros, con su valor y de dónde salen.

Como el resto de la simulación, es la propuesta de la máquina: no entra en la
caja ni en la fuente. Mientras no llegue el libro, el testigo es el sustituto.
"""

import json

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes
from shapely import affinity
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

from comun import CELDAS, SALIDA, T, a8, azar, caja_tinta, componentes, guardar, lamina as lamina_8x7, rotulo

GRAM = SALIDA / "gramatica"
GENERADORES = "olna"
VIOLETA = (74, 36, 112)
PAPEL = np.array([0.955, 0.948, 0.925])
CINTA = np.array([0.935, 0.912, 0.852])       # masking blanca, tirando a hueso claro
PLASTICO = np.array([0.07, 0.07, 0.075])      # el plástico negro de la plataforma, donde se pone la cinta
HALLADAS = [c["signo"] for c in CELDAS if c["estado"] == "hallada"]
RECONSTRUIDAS = [c["signo"] for c in CELDAS if c["estado"] == "reconstruida"]


# ---------------------------------------------------------------- el esqueleto: medidas del testigo

def _corridas(v):
    d = np.diff(np.concatenate([[0], v.astype(int), [0]]))
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]))


def _astas(m, y):
    """Centros de las corridas de tinta de una fila: dónde están las astas."""
    return [(a + b) / 2 for a, b in _corridas(m[int(y)]) if b - a > 6]


def esqueleto(A, med):
    """Lo que se toma del pie: medidas, no formas."""
    fondo, xh = float(med["base"]), float(med["xh"])
    canal = float(np.sqrt(med["grueso"] * med["fino"]))   # entre el grueso y el fino del pie: sin modular
    e = dict(fondo=fondo, borde=fondo - xh, afuera=fondo - float(med["asc"]), desague=fondo + float(med["desc"]),
             xh=xh, canal=canal, cajas={s: [float(v) for v in caja_tinta(A[s])] for s in HALLADAS})
    a = A["a"]
    hueco = binary_fill_holes(a) & ~a
    ojo = max(componentes(hueco), key=lambda c: c[1][4])[0]
    e["ojo_a"] = [float(v) for v in caja_tinta(ojo)]
    e["gancho_a"] = float(caja_tinta(a[: int(e["ojo_a"][1]) - 4])[0])
    return e


# ---------------------------------------------------------------- los parámetros: de la obra

def parametros(e):
    c = e["canal"]
    P = {
        "canal": (round(c, 1), "px", "Grosor único del trazo: la media entre el grueso y el fino de la o del pie.",
                  "El punzón y la cinta no modulan: no hay contraste de pluma (D2, D12)"),
        "radio_chapa": (round(0.6 * c, 1), "px", "Radio mínimo de toda curva del eje. Mayor que medio canal: "
                        "así el contorno interior nunca se cruza.", "El aluminio se rasga en un ángulo agudo (D2)"),
        "trapecio": (0.70, "", "Ancho del fondo plano de cada cuenca, sobre su ancho mayor.",
                     "La proyección llega en trapecio; la bandeja con un dedo de agua (D8)"),
        "pared": (0.55, "", "Cuánto se abomba la pared de la cuenca al bajar: 0 es la pared recta del trapecio, "
                  "1 una vasija redonda.", "El vaso: una ficha llama «vaso» al monolito (a verificar)"),
        "desague": (12.0, "px", "Abertura en el fondo de cada cuenca: 3 mm, el surco del punzón con sus lomas.",
                    "«Ningún contenedor aguanta lo que contiene» (D16)"),
        "hombro": (3.0, "", "Exponente de la superelipse de los arcos altos (2 sería una elipse).",
                   "La chapa curvada a la fuerza sobre un hombro o una clavícula (D3)"),
        "hombro_caida": (0.40, "", "Dónde el arco se vuelve vertical, del borde al fondo.",
                         "Del testigo de la n, a ojo: falta medirlo en el libro"),
        "facetas": (3, "", "Planos de cada fuste.", "La placa cambia de plano al apoyarse en el cuerpo (D3, D11)"),
        "quiebre": (1.6, "°", "Ángulo entre plano y plano: apenas.", "«Moverse como se mueve la piedra, es decir, "
                    "apenas» (D11)"),
        "asiento_ancho": (round(2.0 * c, 1), "px", "Ancho del pie de cada fuste sobre el fondo.",
                          "El peso se asienta en la tierra; la piedra en pie"),
        "asiento_alto": (round(0.9 * c, 1), "px", "Altura de la curva cóncava con que el fuste se ensancha.", "Ídem"),
        "intemperie": (round(0.12 * c, 1), "px", "Radio con que se gastan todas las esquinas. Arriba no hay remates: "
                       "el fuste termina en un corte.", "«Hoy está muy erosionado y casi no se ven esos detalles» "
                       "(el pie)"),
        "alivio": (round(0.28 * c, 1), "px", "Radio del rebaje en cada encuentro interior en ángulo agudo "
                   "(k, v, w, x, y, z, 1, 2, 4, 7, « »). Donde el encuentro es tangente no hace falta.",
                   "Para que el aluminio no se desgarre bajo el punzón (D2)"),
        "gancho_fin": (105, "°", "Dónde termina el gancho alto antes de dejar caer la gota.",
                       "Que la gota cuelgue libre, sin tocar la cuenca"),
        "gota_masa": (round(1.25 * c, 1), "px", "Diámetro de la gota que cuelga de un terminal que mira abajo. "
                      "Un terminal que mira arriba termina en un corte: la gravedad no se da vuelta.",
                      "El líquido que chorrea de la boca (D16)"),
        "gota_caida": (round(0.3 * c, 1), "px", "Cuánto baja la gota antes de juntar peso.", "Ídem: la gravedad"),
        "gota_cuello": (round(0.55 * c, 1), "px", "Ancho del cuello de la gota.", "Ídem"),
        "sifon": (0.6, "", "Ancho del cuello que une dos cuencas (g, 8), sobre el canal: el único trazo más fino.",
                  "Vasos comunicantes: el agua que pasa de una cuenca a otra"),
        "cinta": (round(c, 1), "px", "Ancho de la cinta, a la escala en que iguala al canal. Masking blanca, "
                  "tirando a hueso claro.", "La cinta que tapó ojos y boca (D12)"),
        "punto": (round(c, 1), "px", "Lado del punto: un trozo cuadrado de cinta, tan ancho como la cinta.",
                  "La cinta sobre ojos y boca (D12): un parche, no una gota de tinta"),
    }
    return {k: dict(valor=v, unidad=u, que=q, de_donde=f) for k, (v, u, q, f) in P.items()}


def V(P, k):
    return float(P[k]["valor"])


# ---------------------------------------------------------------- geometría

def superelipse(cx, cy, rx, ry, n, a0, a1, pasos=120):
    t = np.radians(np.linspace(a0, a1, pasos))
    co, si = np.cos(t), np.sin(t)
    return np.column_stack([cx + rx * np.sign(co) * np.abs(co) ** (2 / n),
                            cy - ry * np.sign(si) * np.abs(si) ** (2 / n)])


def filetear(pts, r, pasos=14):
    """Reemplaza cada vértice de una poligonal por un arco de radio r (o el mayor que quepa)."""
    pts = np.asarray(pts, float)
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        p = pts[i]
        u, v = pts[i - 1] - p, pts[i + 1] - p
        lu, lv = np.linalg.norm(u), np.linalg.norm(v)
        u, v = u / lu, v / lv
        ang = np.arccos(np.clip(u @ v, -1, 1))
        if ang > np.pi - 1e-3:
            out.append(p)
            continue
        d = min(r / np.tan(ang / 2), 0.5 * lu, 0.5 * lv)
        rr = d * np.tan(ang / 2)
        b = (u + v) / np.linalg.norm(u + v)
        centro = p + b * rr / np.sin(ang / 2)
        p1, p2 = p + u * d, p + v * d
        a1 = np.arctan2(*(p1 - centro)[::-1])
        a2 = np.arctan2(*(p2 - centro)[::-1])
        da = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi
        t = a1 + da * np.linspace(0, 1, pasos)
        out.extend(np.column_stack([centro[0] + rr * np.cos(t), centro[1] + rr * np.sin(t)]))
    out.append(pts[-1])
    return np.array(out)


def facetar(p0, p1, n, quiebre, rng):
    """Un fuste en n planos: cada quiebre, apenas; el último vuelve al eje."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    L = np.linalg.norm(p1 - p0)
    d = (p1 - p0) / L
    nrm = np.array([-d[1], d[0]])
    s = rng.choice([-1, 1])
    pts, off = [p0], 0.0
    for k in range(1, n):
        off += s * (-1) ** k * (L / n) * np.tan(np.radians(quiebre))
        pts.append(p0 + d * L * k / n + nrm * off)
    pts.append(p1)
    return np.array(pts)


def asiento(x, fondo, c, ancho, alto, pasos=18):
    """El pie del fuste: se ensancha hacia el fondo en una curva cóncava."""
    t = np.linspace(0, 1, pasos)[:, None]
    P0, P1, P2 = np.array([x - c / 2, fondo - alto]), np.array([x - c / 2, fondo]), np.array([x - ancho / 2, fondo])
    izq = (1 - t) ** 2 * P0 + 2 * (1 - t) * t * P1 + t ** 2 * P2
    der = izq.copy()
    der[:, 0] = 2 * x - der[:, 0]
    return Polygon(np.vstack([izq, der[::-1]]))


def gota(p, c, P):
    """La gota que cuelga: un cuello y una masa que cae por su peso."""
    masa, caida, cuello = V(P, "gota_masa"), V(P, "gota_caida"), V(P, "gota_cuello")
    centro = (p[0], p[1] + caida + masa / 2)
    cuerpo = affinity.scale(Point(centro).buffer(masa / 2, 48), 1.0, 1.15, origin=(centro[0], centro[1] - masa / 2))
    cuello_p = Polygon([(p[0] - c / 2, p[1]), (p[0] + c / 2, p[1]), (centro[0] + cuello / 2, centro[1]),
                        (centro[0] - cuello / 2, centro[1])])
    return unary_union([cuerpo, cuello_p]), (centro[0], centro[1] + masa / 2)


def cuenca_lado(x_medio, cy, x_fondo, ybot, pared, pasos=60):
    """La pared de la cuenca: baja desde su ancho mayor hasta el fondo plano, que toca de plano."""
    t = np.linspace(0, 1, pasos)[:, None]
    P0, P3 = np.array([x_medio, cy]), np.array([x_fondo, ybot])
    P1 = np.array([x_medio, cy + pared * (ybot - cy)])
    P2 = np.array([x_fondo + pared * (x_medio - x_fondo), ybot])
    return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3


# ---------------------------------------------------------------- los cuatro generadores


def remuestrear(pts, paso=1.0):
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] == 0:
        return pts
    t = np.arange(0, s[-1] + 1e-9, paso)
    return np.column_stack([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])])


def cortar(pts, huecos, cerrado=False):
    """Abre una poligonal en cada hueco (x, y, ancho): quedan tramos con el corte recto."""
    pts = remuestrear(np.vstack([pts, pts[:1]]) if cerrado else pts)
    fuera = np.ones(len(pts), bool)
    for x, y, d in huecos:
        cerca = np.hypot(pts[:, 0] - x, pts[:, 1] - y) < 3 * d
        fuera &= ~(cerca & (np.abs(pts[:, 0] - x) < d / 2))
    tramos, actual = [], []
    for p, ok in zip(pts, fuera):
        if ok:
            actual.append(p)
        elif actual:
            tramos.append(actual)
            actual = []
    if actual:
        tramos.append(actual)
    if cerrado and len(tramos) > 1 and fuera[0] and fuera[-1]:
        tramos[0] = tramos.pop() + tramos[0]
    return [np.array(t) for t in tramos if len(t) > 1]


class Glifo:
    """Un signo: trazos (eje y ancho), formas que se suman y alivios que se restan."""

    def __init__(self, signo):
        self.signo = signo
        self.trazos, self.mas, self.menos, self.marcas, self.nodos = [], [], [], [], []

    def trazo(self, pts, ancho=None):
        self.trazos.append((np.asarray(pts, float), ancho))

    def marca(self, nombre, p):
        self.marcas.append((nombre, (float(p[0]), float(p[1]))))

    def mover(self, dx):
        self.trazos = [(t + [dx, 0], w) for t, w in self.trazos]
        self.mas = [affinity.translate(m, dx, 0) for m in self.mas]
        self.menos = [affinity.translate(m, dx, 0) for m in self.menos]
        self.marcas = [(n, (p[0] + dx, p[1])) for n, p in self.marcas]
        self.nodos = [(p[0] + dx, p[1]) for p in self.nodos]


class Taller:
    """Las partes, medidas sobre el pie y formadas por los parámetros."""

    def __init__(self, e, P, A):
        self.e, self.P, self.A = e, P, A
        self.c = e["canal"]
        self.F, self.B, self.Af, self.D, self.xh = e["fondo"], e["borde"], e["afuera"], e["desague"], e["xh"]

    def v(self, k):
        return V(self.P, k)

    def caja(self, s):
        return self.e["cajas"][s]

    def astas(self, s, y):
        return _astas(self.A[s], y)

    # -- el fuste: tres planos; si llega al fondo, se asienta; si no, termina en un corte
    def fuste(self, G, rng, x, arriba, abajo=None):
        abajo = self.F if abajo is None else abajo
        asienta = abs(abajo - self.F) < 1
        fin = abajo - self.v("asiento_alto") + 2 if asienta else abajo
        eje = facetar((x, arriba), (x, fin), int(self.v("facetas")), self.v("quiebre"), rng)
        G.trazo(eje)
        G.nodos += [tuple(p) for p in eje]
        if asienta:
            G.mas.append(asiento(x, self.F, self.c, self.v("asiento_ancho"), self.v("asiento_alto")))
            G.marca("asiento", (x, self.F))
        return eje

    # -- la cuenca: arriba, el ojo del pie; abajo, pared, fondo plano y desagüe
    def cuenca(self, G, x_izq, x_der, y_arriba, y_abajo, fuste=None, huecos_arriba=(), ancho_arriba=None,
               exp=2.0):
        c, k, d, pared = self.c, self.v("trapecio"), self.v("desague"), self.v("pared")
        cx, rx = (x_izq + x_der) / 2, (x_der - x_izq) / 2
        cy = (y_arriba + y_abajo) / 2
        arriba = superelipse(cx, cy, rx, cy - y_arriba, exp, 0, 180)
        izq = cuenca_lado(cx - rx, cy, cx - k * rx, y_abajo, pared)
        der = cuenca_lado(cx + rx, cy, cx + k * rx, y_abajo, pared)
        if fuste == "der":
            xd = (cx - k * rx + x_der - c / 2) / 2
            poli = np.vstack([arriba, izq[1:], [(x_der, y_abajo)]])
        elif fuste == "izq":
            xd = (x_izq + c / 2 + cx + k * rx) / 2
            poli = np.vstack([arriba[::-1], der[1:], [(x_izq, y_abajo)]])
        else:
            xd = cx
            poli = np.vstack([der[::-1], arriba[1:-1], izq])
        huecos = [(xd, y_abajo, d)] + [(x, y_arriba, d) for x in huecos_arriba]
        for t in cortar(poli, huecos, cerrado=fuste is None):
            G.trazo(t, ancho_arriba)
        G.marca("desagüe", (xd, y_abajo + c / 2))
        G.nodos += [(cx - k * rx, y_abajo), (cx + k * rx, y_abajo), (cx - rx, cy), (cx + rx, cy)]
        return dict(cx=cx, cy=cy, rx=rx, ry=cy - y_arriba, xd=xd)

    # -- el hombro: un arco tenso que sale del fuste en su misma dirección y baja como otro fuste
    def hombro(self, G, rng, x_izq, x_der, y_tope, pie=True):
        yt = y_tope + self.c / 2
        ya = yt + self.v("hombro_caida") * (self.F - yt)
        arco = superelipse((x_izq + x_der) / 2, ya, (x_der - x_izq) / 2, ya - yt, self.v("hombro"), 180, 0)
        fin = self.F - self.v("asiento_alto") + 2 if pie else self.F
        bajada = facetar((x_der, ya), (x_der, fin), int(self.v("facetas")), self.v("quiebre"), rng)
        G.trazo(np.vstack([arco, bajada[1:]]))
        if pie:
            G.mas.append(asiento(x_der, self.F, self.c, self.v("asiento_ancho"), self.v("asiento_alto")))
        G.marca("hombro", arco[60])
        return ya

    # -- el gancho: un arco alto que termina mirando abajo; de ahí cuelga la gota
    def gota(self, G, p):
        g, fin = gota(p, self.c, self.P)
        G.mas.append(g)
        G.marca("gota", fin)
        return fin

    def arco(self, cx, cy, rx, ry, a0, a1, exp=None):
        return superelipse(cx, cy, rx, ry, self.v("hombro") if exp is None else exp, a0, a1)

    # -- lo que no es trazo corrido
    def punto(self, G, x, y):
        """Un trozo cuadrado de cinta: tan ancho como la cinta."""
        lado = self.v("punto")
        G.trazo([(x, y - lado / 2), (x, y + lado / 2)], lado)
        G.marca("punto", (x + lado / 2, y))

    def tilde(self, G, x, y):
        """Una gota: la punta arriba, el peso abajo."""
        c = self.c
        cuerpo = Point(x, y + 0.35 * c).buffer(0.5 * c, 32)
        punta = Polygon([(x - 0.42 * c, y + 0.2 * c), (x + 0.42 * c, y + 0.5 * c), (x + 0.7 * c, y - 1.2 * c)])
        G.mas.append(unary_union([cuerpo, punta]))
        G.trazo([(x, y + 0.35 * c), (x + 0.6 * c, y - 1.0 * c)], 0.001)    # para la cinta: un tramo corto
        G.marca("tilde", (x + 0.7 * c, y - 1.2 * c))

    def onda(self, G, x0, x1, y):
        """La virgulilla: la onda del agua tocada."""
        t = np.linspace(0, 1, 80)
        G.trazo(np.column_stack([x0 + (x1 - x0) * t, y - 0.35 * self.c * np.sin(2 * np.pi * t)]))
        G.marca("onda", (x1, y))

    def recta(self, G, rng, p0, p1, planos=2):
        eje = facetar(p0, p1, planos, self.v("quiebre"), rng)
        G.trazo(eje)
        return eje

    def quebrada(self, G, pts):
        """Una poligonal con cada vértice redondeado al radio de la chapa."""
        eje = filetear(pts, self.v("radio_chapa"))
        G.trazo(eje)
        return eje

    def alivio(self, G, v, d1, d2, r=0.0):
        """El rebaje en un rincón agudo: en la bisectriz, donde se encuentran los bordes.

        Si el eje se redondeó con radio r en ese vértice, el rincón queda más lejos.
        """
        d1, d2 = np.asarray(d1, float), np.asarray(d2, float)
        d1, d2 = d1 / np.linalg.norm(d1), d2 / np.linalg.norm(d2)
        ang = np.arccos(np.clip(d1 @ d2, -1, 1))
        b = (d1 + d2) / np.linalg.norm(d1 + d2)
        sen = max(np.sin(ang / 2), 0.2)
        lejos = r / sen - (r - self.c / 2) if r > self.c / 2 else (self.c / 2) / sen
        esquina = np.asarray(v, float) + b * lejos
        G.menos.append(Point(*esquina).buffer(self.v("alivio"), 32))
        G.marca("alivio", esquina)

    def celda_cifra(self, G):
        """Cada cifra vive en una celda de la cabeza del ídolo: un rectángulo dentro de otro, con desagüe."""
        x0, y0, x1, y1 = celda(self.e)
        c = self.c
        for m in (0.3 * c, 1.3 * c):
            anillo = np.array([(x0 + m, y1 - m), (x0 + m, y0 + m), (x1 - m, y0 + m), (x1 - m, y1 - m)])
            anillo = np.vstack([[((x0 + x1) / 2, y1 - m)], anillo, [((x0 + x1) / 2, y1 - m)]])
            for t in cortar(anillo, [((x0 + x1) / 2, y1 - m, self.v("desague"))]):
                G.trazo(t, 0.35 * c)
        G.marca("celda", (x1 - 0.3 * c, (y0 + y1) / 2))
        return (x0 + 1.3 * c, y0 + 1.3 * c, x1 - 1.3 * c, y1 - 1.3 * c)


def u(a, b):
    v = np.asarray(b, float) - np.asarray(a, float)
    return v / np.linalg.norm(v)


# ---------------------------------------------------------------- las recetas: de las partes, los signos

def _alivios(t, G, pts, indices):
    """Alivio en los vértices de una quebrada, que ya están redondeados al radio de la chapa."""
    for i in indices:
        t.alivio(G, pts[i], u(pts[i], pts[i - 1]), u(pts[i], pts[i + 1]), r=t.v("radio_chapa"))


def _cx(caja):
    return (caja[0] + caja[2]) / 2


def r_o(t, G, rng):
    x0, y0, x1, y1 = t.caja("o")
    c = t.c
    return t.cuenca(G, x0 + c / 2, x1 - c / 2, y0 + c / 2, t.F - c / 2)


def r_l(t, G, rng):
    x0, y0, x1, y1 = t.caja("l")
    xs = max(t.astas("l", (y0 + t.F) / 2))
    t.fuste(G, rng, xs, y0)
    G.marca("corte", (xs, y0))


def r_n(t, G, rng, s="n"):
    x0, y0, x1, y1 = t.caja(s)
    a = t.astas(s, t.F - 0.3 * t.xh)
    t.fuste(G, rng, a[0], t.B)
    t.hombro(G, rng, a[0], a[-1], y0)
    return a[0], a[-1]


def r_h(t, G, rng):
    x0, y0, x1, y1 = t.caja("h")
    a = t.astas("h", t.F - 0.3 * t.xh)
    t.fuste(G, rng, a[0], y0)
    t.hombro(G, rng, a[0], a[-1], t.B - 3)


def r_m(t, G, rng):
    x0, y0, x1, y1 = t.caja("m")
    a = t.astas("m", t.F - 0.3 * t.xh)
    xi, xd = a[0], a[-1]
    xm = a[len(a) // 2] if len(a) >= 3 else (xi + xd) / 2
    t.fuste(G, rng, xi, t.B)
    t.hombro(G, rng, xi, xm, y0)
    t.hombro(G, rng, xm, xd, y0)


def r_a(t, G, rng):
    c, e = t.c, t.e
    x0, y0, x1, y1 = t.caja("a")
    xs = t.astas("a", t.F - 0.25 * t.xh)[-1]
    xg = e["gancho_a"] + c / 2
    yt = y0 + c / 2
    yh = yt + t.v("hombro_caida") * (t.F - yt)
    gancho = t.arco((xg + xs) / 2, yh, (xs - xg) / 2, yh - yt, t.v("gancho_fin"), 0)
    G.trazo(gancho)
    fin = t.gota(G, gancho[0])
    t.fuste(G, rng, xs, yh)
    hx0, hy0, hx1, hy1 = e["ojo_a"]
    arriba = max(hy0 - c / 2, fin[1] + 0.4 * c + c / 2)      # la gota cae libre: la cuenca le deja lugar
    t.cuenca(G, hx0 - c / 2, xs, arriba, t.F - c / 2, fuste="der")
    return (xg + xs) / 2


def _u(t, G, rng, s="u"):
    c, k, pared = t.c, t.v("trapecio"), t.v("pared")
    x0, y0, x1, y1 = t.caja(s)
    a = t.astas(s, t.B + 0.3 * t.xh)
    xi, xd = a[0], a[-1]
    ym, yb = t.B + 0.5 * t.xh, t.F - c / 2
    cx, rx = (xi + xd) / 2, (xd - xi) / 2
    izq = cuenca_lado(xi, ym, cx - k * rx, yb, pared)
    der = cuenca_lado(xd, ym, cx + k * rx, yb, pared)
    G.trazo(np.vstack([[(xi, t.B)], izq, der[::-1]]))
    G.marca("cuenca abierta", (cx, yb + c / 2))
    t.fuste(G, rng, xd, t.B)
    return cx, xd - xi


def r_u(t, G, rng):
    _u(t, G, rng)


def r_ú(t, G, rng):
    cx, w = _u(t, G, rng, "ú")
    t.tilde(G, cx + 0.1 * t.c, t.B - 1.9 * t.c)


def r_ü(t, G, rng):
    cx, w = _u(t, G, rng)
    for dx in (-0.3 * w, 0.3 * w):
        t.punto(G, cx + dx, t.B - 1.5 * t.c)


def r_i(t, G, rng):
    x0, y0, x1, y1 = t.caja("i")
    xs = t.astas("i", t.F - 0.3 * t.xh)[0]
    t.fuste(G, rng, xs, t.B)
    t.punto(G, xs, y0 + t.v("punto") / 2)


def r_í(t, G, rng):
    xs = t.astas("í", t.F - 0.3 * t.xh)[0]
    t.fuste(G, rng, xs, t.B)
    t.tilde(G, xs + 0.1 * t.c, t.B - 1.9 * t.c)


def r_j(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("j")
    xs = t.astas("j", t.B + 0.4 * t.xh)[-1]
    yj = t.F + 0.25 * (t.D - t.F)
    lado = cuenca_lado(xs, yj, xs - 0.5 * (xs - x0), y1 - c / 2, t.v("pared"))
    G.trazo(np.vstack([[(xs, t.B)], lado, [(x0 + c / 2, y1 - c / 2)]]))
    G.marca("corte: mira arriba", (x0 + c / 2, y1 - c / 2))
    t.punto(G, xs, y0 + t.v("punto") / 2)


def r_f(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("f")
    xs = t.astas("f", t.F - 0.3 * t.xh)[0]
    yt = y0 + c / 2
    ya = yt + 0.85 * (t.B - yt)
    rx = (x1 - c / 2 - xs) / 2
    gancho = t.arco(xs + rx, ya, rx, ya - yt, 180, 40)
    G.trazo(gancho)
    t.gota(G, gancho[-1])
    t.fuste(G, rng, xs, ya)
    t.recta(G, rng, (x0 + c / 2, t.B + c / 2), (xs + 0.55 * (x1 - xs), t.B + c / 2))


def r_t(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("t")
    xs = t.astas("t", t.B + 0.5 * t.xh)[0]
    ym, yb = t.F - 0.3 * t.xh, t.F - c / 2
    lado = cuenca_lado(xs, ym, xs + 0.45 * (x1 - c / 2 - xs), yb, t.v("pared"))
    G.trazo(np.vstack([[(xs, y0)], lado, [(x1 - c / 2, yb)]]))
    G.marca("corte", (xs, y0))
    t.recta(G, rng, (x0 + c / 2, t.B + c / 2), (x1 - c / 2 - 6, t.B + c / 2))


def r_r(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("r")
    xs = t.astas("r", t.F - 0.3 * t.xh)[0]
    t.fuste(G, rng, xs, t.B)
    yt = y0 + c / 2
    ya = yt + 0.3 * (t.F - yt)
    rx = (x1 - c / 2 - xs) / 2
    brazo = t.arco(xs + rx, ya, rx, ya - yt, 180, 55)
    G.trazo(brazo)
    t.gota(G, brazo[-1])


def r_k(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("k")
    xs = t.astas("k", (t.Af + t.B) / 2)[0]
    t.fuste(G, rng, xs, y0)
    J = np.array([xs, t.F - 0.45 * t.xh])
    E1 = np.array([x1 - c / 2 - 4, t.B + c / 2])
    Q = J + 0.42 * (E1 - J)
    E2 = np.array([x1 - c / 2, t.F - 0.3 * c])
    t.recta(G, rng, J, E1, 1)
    t.recta(G, rng, Q, E2, 1)
    t.alivio(G, J, (0, -1), u(J, E1))
    t.alivio(G, Q, u(Q, E1), u(Q, E2))


def _v(t, G, x0, x1):
    c = t.c
    cx = (x0 + x1) / 2
    pts = np.array([(x0 + c / 2 + 2, t.B + 0.1 * c), (cx, t.F - c / 2), (x1 - c / 2 - 2, t.B + 0.1 * c)])
    t.quebrada(G, pts)
    _alivios(t, G, pts, [1])


def r_v(t, G, rng):
    x0, y0, x1, y1 = t.caja("v")
    _v(t, G, x0, x1)


def r_y(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("y")
    cx = (x0 + x1) / 2
    P0 = np.array([x0 + c / 2 + 2, t.B + 0.1 * c])
    V = np.array([cx, t.F - c / 2])
    P2 = np.array([x1 - c / 2 - 2, t.B + 0.1 * c])
    d = u(P2, V)
    cola = V + d * ((y1 - 2.2 * c - V[1]) / d[1])
    t.recta(G, rng, P0, V, 1)
    t.recta(G, rng, P2, cola, 2)
    t.gota(G, cola)
    t.alivio(G, V, u(V, P0), u(V, P2))


def r_p(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("p")
    xs = t.astas("p", (t.F + t.D) / 2)[0]
    t.fuste(G, rng, xs, t.B, abajo=y1)
    t.cuenca(G, xs, x1 - c / 2, y0 + c / 2, t.F - c / 2, fuste="izq")


def r_q(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("q")
    xs = t.astas("q", (t.F + t.D) / 2)[-1]
    t.fuste(G, rng, xs, t.B, abajo=y1)
    t.cuenca(G, x0 + c / 2, xs, y0 + c / 2, t.F - c / 2, fuste="der")


def r_b(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("b")
    xs = t.astas("b", (t.Af + t.B) / 2)[0]
    t.fuste(G, rng, xs, y0)
    t.cuenca(G, xs, x1 - c / 2, t.B + c / 2 - 3, t.F - c / 2, fuste="izq")


def r_d(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("d")
    xs = t.astas("d", (t.Af + t.B) / 2)[-1]
    t.fuste(G, rng, xs, y0)
    t.cuenca(G, x0 + c / 2, xs, t.B + c / 2 - 3, t.F - c / 2, fuste="der")


def _e(t, G, s="e"):
    c, k, pared, d = t.c, t.v("trapecio"), t.v("pared"), t.v("desague")
    x0, y0, x1, y1 = t.caja(s)
    cx, rx = (x0 + x1) / 2, (x1 - x0) / 2 - c / 2
    yt, yb = y0 + c / 2, t.F - c / 2
    yb_ = yt + 0.47 * (yb - yt)
    arriba = t.arco(cx, yb_, rx, yb_ - yt, 0, 180, exp=2)
    izq = cuenca_lado(cx - rx, yb_, cx - k * rx, yb, pared)
    der = cuenca_lado(cx + rx, yb_, cx + k * rx, yb, pared)[::-1]
    remate = der[: int(0.45 * len(der))]
    G.trazo(np.vstack([arriba, izq[1:], remate]))
    G.trazo([(cx - rx, yb_), (cx - d / 2, yb_)])
    G.trazo([(cx + d / 2, yb_), (cx + rx, yb_)])
    G.marca("desagüe del ojo", (cx, yb_ + c / 2))
    G.marca("corte: mira arriba", remate[-1])
    return cx


def r_e(t, G, rng):
    _e(t, G)


def r_c(t, G, rng):
    c, k, pared = t.c, t.v("trapecio"), t.v("pared")
    x0, y0, x1, y1 = t.caja("c")
    cx, rx = (x0 + x1) / 2, (x1 - x0) / 2 - c / 2
    yt, yb = y0 + c / 2, t.F - c / 2
    cy = (yt + yb) / 2
    arriba = t.arco(cx, cy, rx, cy - yt, 40, 180, exp=2)
    izq = cuenca_lado(cx - rx, cy, cx - k * rx, yb, pared)
    der = cuenca_lado(cx + rx, cy, cx + k * rx, yb, pared)[::-1]
    G.trazo(np.vstack([arriba, izq[1:], der[: int(0.4 * len(der))]]))
    t.gota(G, arriba[0])


def r_s(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("s")
    cx, w = (x0 + x1) / 2, x1 - x0
    yt, yb = y0 + c / 2, t.F - c / 2
    ym = (yt + yb) / 2
    arriba = t.arco(cx, (yt + ym) / 2, 0.86 * (w / 2 - c / 2), (ym - yt) / 2, 25, 270, exp=2.2)
    abajo = t.arco(cx, (ym + yb) / 2, w / 2 - c / 2, (yb - ym) / 2, 90, -160, exp=2.2)
    G.trazo(np.vstack([arriba, abajo[1:]]))
    t.gota(G, arriba[0])
    G.marca("corte: mira arriba", abajo[-1])


def r_g(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("g")
    w = x1 - x0
    arriba = t.cuenca(G, x0 + c / 2 + 0.06 * w, x1 - c / 2 - 0.2 * w, y0 + c / 2 + 6, t.F - 0.22 * t.xh)
    yl = t.F + 0.12 * (y1 - t.F)
    abajo = t.cuenca(G, x0 + c / 2, x1 - c / 2 - 0.05 * w, yl, y1 - c / 2)
    ybu = arriba["cy"] + arriba["ry"]
    G.trazo([(arriba["cx"] - 0.35 * arriba["rx"], ybu), (abajo["cx"] - 0.45 * abajo["rx"], yl + 2)],
            t.v("sifon") * c)
    G.marca("sifón", (arriba["cx"] - 0.4 * arriba["rx"], (ybu + yl) / 2))
    yo = y0 + c / 2 + 4
    t.recta(G, rng, (arriba["cx"] + 0.55 * arriba["rx"], yo), (x1 - c / 2, yo), 1)


def r_coma(t, G, rng, cx=None):
    """Un punto de cinta del que cae una gota."""
    if cx is None:
        cx = _cx(t.caja(","))
    t.punto(G, cx, t.F - t.v("punto") / 2)
    t.gota(G, (cx, t.F))


def r_punto(t, G, rng):
    t.punto(G, _cx(t.caja(".")), t.F - t.v("punto") / 2)


def _parentesis(t, G, s, izq):
    c = t.c
    x0, y0, x1, y1 = t.caja(s)
    rx = (x1 - x0) - c
    cy, ry = (y0 + y1) / 2, (y1 - y0) / 2 - c / 2
    if izq:
        arco = t.arco(x0 + c / 2 + rx, cy, rx, ry, 118, 242, exp=2.4)
    else:
        arco = t.arco(x1 - c / 2 - rx, cy, rx, ry, 62, -62, exp=2.4)
    G.trazo(arco)


def r_abre(t, G, rng):
    _parentesis(t, G, "(", True)


def r_cierra(t, G, rng):
    _parentesis(t, G, ")", False)


def r_á(t, G, rng):
    cx = r_a(t, G, rng)
    t.tilde(G, cx + 0.2 * t.c, t.B - 1.9 * t.c)


# ---- reconstruidos: las mismas partes; lo que falta, por analogía

def r_ó(t, G, rng):
    m = r_o(t, G, rng)
    t.tilde(G, m["cx"] + 0.1 * t.c, t.B - 1.9 * t.c)


def r_é(t, G, rng):
    cx = _e(t, G)
    t.tilde(G, cx + 0.1 * t.c, t.B - 1.9 * t.c)


def r_ñ(t, G, rng):
    xi, xd = r_n(t, G, rng)
    t.onda(G, xi - 0.1 * t.c, xd + 0.1 * t.c, t.B - 1.6 * t.c)


def r_z(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("v")
    pts = np.array([(x0 + c / 2 + 6, t.B + c / 2), (x1 - c / 2 - 6, t.B + c / 2), (x0 + c / 2 + 6, t.F - c / 2),
                    (x1 - c / 2 - 6, t.F - c / 2)])
    t.quebrada(G, pts)
    _alivios(t, G, pts, [1, 2])


def r_w(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("m")
    W, cx = x1 - x0, (x0 + x1) / 2
    pts = np.array([(x0 + c / 2, t.B + 0.1 * c), (x0 + 0.27 * W, t.F - c / 2), (cx, t.B + 0.32 * t.xh),
                    (x1 - 0.27 * W, t.F - c / 2), (x1 - c / 2, t.B + 0.1 * c)])
    t.quebrada(G, pts)
    _alivios(t, G, pts, [1, 2, 3])


def r_x(t, G, rng):
    c = t.c
    x0, y0, x1, y1 = t.caja("v")
    a, b = np.array([x0 + c / 2, t.B + 0.1 * c]), np.array([x1 - c / 2, t.F - 0.1 * c])
    a2, b2 = np.array([x1 - c / 2, t.B + 0.1 * c]), np.array([x0 + c / 2, t.F - 0.1 * c])
    t.recta(G, rng, a, b, 2)
    t.recta(G, rng, a2, b2, 2)
    C = (a + b) / 2
    t.alivio(G, C, u(C, a), u(C, a2))
    t.alivio(G, C, u(C, b), u(C, b2))


def _ancho_o(t):
    x0, y0, x1, y1 = t.caja("o")
    return x1 - x0


def r_pregunta(t, G, rng):
    c = t.c
    cx = T / 2
    rx = 0.8 * (_ancho_o(t) / 2 - c / 2)
    yt = t.Af + 0.3 * (t.B - t.Af) + c / 2
    ry = 0.27 * (t.F - yt)
    yc = yt + ry
    arco = t.arco(cx, yc, rx, ry, 165, -90, exp=2.2)
    G.trazo(arco)
    t.gota(G, arco[0])
    t.recta(G, rng, (cx, yc + ry), (cx, t.F - 1.9 * c), 1)
    t.punto(G, cx, t.F - t.v("punto") / 2)


def r_abre_pregunta(t, G, rng):
    c = t.c
    cx = T / 2
    rx = 0.8 * (_ancho_o(t) / 2 - c / 2)
    yt = t.Af + 0.3 * (t.B - t.Af) + c / 2
    ry = 0.27 * (t.F - yt)
    abajo = t.D - 0.2 * (t.D - t.F)
    ys = abajo - c / 2 - 2 * ry
    t.punto(G, cx, t.B + t.v("punto") / 2)
    t.recta(G, rng, (cx, t.B + 1.9 * c), (cx, ys), 1)
    arco = t.arco(cx, ys + ry, rx, ry, 90, 345, exp=2.2)
    G.trazo(arco)
    G.marca("sin gota: la gravedad no se da vuelta", arco[-1])


def r_punto_y_coma(t, G, rng):
    t.punto(G, T / 2, t.B + 0.9 * t.c)
    r_coma(t, G, rng, T / 2)


def r_dos_puntos(t, G, rng):
    t.punto(G, T / 2, t.B + 0.9 * t.c)
    t.punto(G, T / 2, t.F - t.v("punto") / 2)


def _comillas(t, G, rng, abre):
    c = t.c
    ym, h = t.B + 0.5 * t.xh, 0.26 * t.xh
    wc = 0.28 * _ancho_o(t)
    for i in (-1, 1):
        xa = T / 2 + i * (wc / 2 + 0.4 * c) + rng.normal(0, 1.5)
        tip = (xa - wc / 2, ym + rng.normal(0, 1.5)) if abre else (xa + wc / 2, ym + rng.normal(0, 1.5))
        lado = xa + wc / 2 if abre else xa - wc / 2
        pts = np.array([(lado, ym - h + rng.normal(0, 1.5)), tip, (lado, ym + h + rng.normal(0, 1.5))])
        t.quebrada(G, pts)
        _alivios(t, G, pts, [1])


def r_abre_comillas(t, G, rng):
    _comillas(t, G, rng, True)


def r_cierra_comillas(t, G, rng):
    _comillas(t, G, rng, False)


def r_raya(t, G, rng):
    w = 0.62 * _ancho_o(t) * 2
    t.recta(G, rng, (T / 2 - w / 2, t.B + 0.5 * t.xh), (T / 2 + w / 2, t.B + 0.5 * t.xh), 3)


def r_suspensivos(t, G, rng):
    for dx in (-1.9, 0, 1.9):
        t.punto(G, T / 2 + dx * t.c, t.F - t.v("punto") / 2)


# ---- las cifras: todas reconstruidas, cada una en su celda; elzevirianas

def _cifra(t, G):
    ix0, iy0, ix1, iy1 = t.celda_cifra(G)
    c = t.c
    w = 0.78 * _ancho_o(t)
    return dict(cx=T / 2, rx=w / 2 - c / 2, w=w, sube=iy0 + 1.1 * c, baja=iy1 - 1.1 * c)


def r_0(t, G, rng):
    k = _cifra(t, G)
    t.cuenca(G, k["cx"] - 0.85 * k["rx"], k["cx"] + 0.85 * k["rx"], t.B + t.c / 2, t.F - t.c / 2)


def r_1(t, G, rng):
    k = _cifra(t, G)
    c = t.c
    xs = k["cx"] + 0.05 * k["w"]
    t.fuste(G, rng, xs, t.B)
    top, fin = np.array([xs, t.B + c / 2]), np.array([xs - 0.34 * k["w"], t.B + 0.32 * t.xh])
    t.recta(G, rng, top, fin, 1)
    t.alivio(G, top, u(top, fin), (0, 1))


def r_2(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    yt = t.B + c / 2
    ry = 0.3 * t.xh
    arco = t.arco(cx, yt + ry, rx, ry, 160, -25, exp=2.2)
    esquina = np.array([cx - rx, t.F - c / 2])
    base = filetear([arco[-1], esquina, (cx + rx, t.F - c / 2)], t.v("radio_chapa"))
    G.trazo(np.vstack([arco, base[1:]]))
    t.gota(G, arco[0])
    t.alivio(G, esquina, u(esquina, arco[-1]), (1, 0), r=t.v("radio_chapa"))


def r_3(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    yt, yb = t.B + c / 2, k["baja"] - c / 2
    ym = yt + 0.42 * (yb - yt)
    arriba = t.arco(cx, (yt + ym) / 2, 0.85 * rx, (ym - yt) / 2, 150, -90, exp=2.2)
    abajo = t.arco(cx, (ym + yb) / 2, rx, (yb - ym) / 2, 90, -150, exp=2.2)
    G.trazo(np.vstack([arriba, abajo[1:]]))
    t.gota(G, arriba[0])
    G.marca("corte: mira arriba", abajo[-1])


def r_4(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    xs = cx + 0.22 * k["w"]
    yb = t.F - 0.2 * t.xh
    t.fuste(G, rng, xs, t.B, abajo=k["baja"])
    top, esq = np.array([xs, t.B + c / 2]), np.array([cx - rx - 0.1 * c, yb])
    t.recta(G, rng, top, esq, 1)
    t.recta(G, rng, esq, (cx + rx + 0.1 * c, yb), 1)
    t.alivio(G, top, u(top, esq), (0, 1))
    t.alivio(G, esq, u(esq, top), (1, 0))


def r_5(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    yt, yb = t.B + c / 2, k["baja"] - c / 2
    ym = yt + 0.36 * (yb - yt)
    panza = t.arco(cx, (ym + yb) / 2, rx, (yb - ym) / 2, 145, -150, exp=2.2)
    xs = panza[0][0]
    t.recta(G, rng, (xs, yt), (cx + rx, yt), 1)
    t.recta(G, rng, (xs, yt), panza[0], 1)
    G.trazo(panza)
    G.marca("corte: mira arriba", panza[-1])


def r_6(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    m = t.cuenca(G, cx - rx, cx + rx, t.B + c / 2, t.F - c / 2)
    sube = t.arco(cx, m["cy"], rx, m["cy"] - (k["sube"] + c / 2), 180, 55, exp=2.2)
    G.trazo(sube)
    t.gota(G, sube[-1])


def r_7(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    yt = t.B + c / 2
    pts = np.array([(cx - rx, yt), (cx + rx, yt), (cx - 0.2 * rx, k["baja"])])
    t.quebrada(G, pts)
    _alivios(t, G, pts, [1])


def r_8(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    yt, yb = k["sube"] + c / 2, t.F - c / 2
    ym = yt + 0.44 * (yb - yt)
    t.cuenca(G, cx - 0.78 * rx, cx + 0.78 * rx, yt, ym)
    t.cuenca(G, cx - rx, cx + rx, ym, yb, huecos_arriba=[cx])
    G.marca("sifón", (cx, ym))


def r_9(t, G, rng):
    k = _cifra(t, G)
    c, cx, rx = t.c, k["cx"], k["rx"]
    m = t.cuenca(G, cx - rx, cx + rx, t.B + c / 2, t.F - c / 2)
    baja = t.arco(cx, m["cy"], rx, k["baja"] - c / 2 - m["cy"], 0, -140, exp=2.2)
    G.trazo(baja)
    G.marca("sin gota: la gravedad no se da vuelta", baja[-1])


RECETAS = {
    "o": (r_o, "la cuenca: arriba, el ojo del pie; abajo, pared, fondo plano y desagüe"),
    "l": (r_l, "un fuste en tres planos, con asiento"),
    "n": (r_n, "un fuste y un hombro que baja como otro fuste"),
    "a": (r_a, "un gancho que gotea, un fuste y una cuenca"),
    "h": (r_h, "el fuste de la l y el hombro de la n"),
    "m": (r_m, "un fuste y dos hombros"),
    "u": (r_u, "una cuenca abierta arriba y un fuste"),
    "ú": (r_ú, "la u y una tilde en gota"),
    "i": (r_i, "un fuste y un punto de cinta"),
    "í": (r_í, "un fuste y una tilde en gota"),
    "j": (r_j, "un fuste que baja y dobla en una pared de cuenca; un punto de cinta"),
    "f": (r_f, "un fuste, un gancho que gotea y una barra"),
    "t": (r_t, "un fuste que dobla en una pared de cuenca, y una barra"),
    "r": (r_r, "un fuste y un brazo que gotea"),
    "k": (r_k, "un fuste, un brazo y una pierna, con dos alivios"),
    "v": (r_v, "dos rectas que se juntan en el fondo, redondeadas al radio de la chapa, con alivio"),
    "y": (r_y, "la v con la cola larga, que gotea"),
    "p": (r_p, "un fuste que baja del fondo y una cuenca a su derecha"),
    "q": (r_q, "una cuenca y un fuste que baja del fondo"),
    "b": (r_b, "un fuste alto y una cuenca a su derecha"),
    "d": (r_d, "una cuenca y un fuste alto"),
    "e": (r_e, "una cuenca abierta a la derecha, con barra; el ojo se abre en su desagüe, en la barra"),
    "c": (r_c, "una cuenca abierta a la derecha; arriba gotea"),
    "s": (r_s, "dos hombros encontrados; arriba gotea"),
    "g": (r_g, "dos cuencas unidas por un cuello angosto: un sifón; y una oreja"),
    ",": (r_coma, "un punto de cinta del que cae una gota"),
    ".": (r_punto, "un punto de cinta"),
    "(": (r_abre, "un arco alto"),
    ")": (r_cierra, "el arco alto, medido en su propio testigo"),
    "á": (r_á, "la a y una tilde en gota"),
    "ó": (r_ó, "la cuenca de la o y una tilde en gota"),
    "é": (r_é, "la e y una tilde en gota"),
    "ñ": (r_ñ, "la n y la onda del agua tocada"),
    "z": (r_z, "dos barras y una diagonal, redondeadas al radio de la chapa, con alivio en los dos rincones"),
    "w": (r_w, "dos v: cuatro rectas y tres alivios"),
    "x": (r_x, "dos rectas que se cruzan, con alivio arriba y abajo del cruce"),
    "ü": (r_ü, "la u y dos puntos de cinta"),
    "?": (r_pregunta, "un gancho que gotea, un fuste corto y un punto de cinta"),
    "¿": (r_abre_pregunta, "el doble opuesto de la ?, con variación: el punto arriba y el gancho abajo, "
                           "que no gotea porque la gravedad no se da vuelta"),
    ";": (r_punto_y_coma, "un punto de cinta sobre la coma: un punto del que cae una gota"),
    ":": (r_dos_puntos, "dos puntos de cinta"),
    "«": (r_abre_comillas, "dos ángulos redondeados al radio de la chapa, con alivio"),
    "»": (r_cierra_comillas, "el doble opuesto de «, con variación: armado con su propio azar"),
    "—": (r_raya, "una recta en tres planos"),
    "…": (r_suspensivos, "tres puntos de cinta"),
    "0": (r_0, "una cuenca más angosta que la o"),
    "1": (r_1, "un fuste con asiento y una bandera, con alivio"),
    "2": (r_2, "un gancho que gotea, una diagonal y una barra de fondo, con alivio"),
    "3": (r_3, "dos hombros apilados que bajan del fondo; el de arriba gotea, el de abajo mira arriba y no"),
    "4": (r_4, "una diagonal, una barra y un fuste que baja del fondo, con dos alivios"),
    "5": (r_5, "una barra, un fuste corto y un hombro que baja del fondo"),
    "6": (r_6, "una cuenca y un hombro que sube y gotea"),
    "7": (r_7, "una barra y una diagonal que baja del fondo, con alivio"),
    "8": (r_8, "dos cuencas apiladas y comunicadas: un sifón"),
    "9": (r_9, "el doble opuesto del 6, con variación: la cuenca y un trazo que baja; no gotea, porque "
               "la gravedad no se da vuelta"),
}


def construir(t, s):
    G = Glifo(s)
    RECETAS[s][0](t, G, azar("gramatica", s))
    geo = cuerpo(G, t.P, t.c)
    x0, _, x1, _ = geo.bounds
    dx = T / 2 - (x0 + x1) / 2
    G.mover(dx)
    return G, affinity.translate(geo, dx, 0)


def construir_todo(A, med):
    """Los 55 signos: {signo: dict(glifo, geo, mascara, receta)}; más el esqueleto y los parámetros."""
    e = esqueleto(A, med)
    P = parametros(e)
    t = Taller(e, P, A)
    salida = {}
    for s in HALLADAS + RECONSTRUIDAS:
        G, geo = construir(t, s)
        receta = RECETAS[s][1] + ("; en su celda" if s.isdigit() else "")
        salida[s] = dict(glifo=G, geo=geo, mascara=rasterizar(geo), receta=receta)
    return salida, e, P



# ---------------------------------------------------------------- el cuerpo, en vectores y en píxeles

def cuerpo(G, P, c):
    """Trazos del ancho del canal (o del suyo), más asientos, gotas y tildes, menos alivios; gastado."""
    partes = [LineString(t).buffer((c if w is None else w) / 2, cap_style="flat", join_style="round", quad_segs=24)
              for t, w in G.trazos if len(t) > 1]
    geo = unary_union(partes + G.mas)
    for m in G.menos:
        geo = geo.difference(m)
    r = V(P, "intemperie")
    return geo.buffer(-r, quad_segs=16).buffer(r, quad_segs=16)


def poligonos(geo):
    return list(geo.geoms) if hasattr(geo, "geoms") else [geo]


def rasterizar(geo):
    m = np.zeros((T, T), np.uint8)
    for p in poligonos(geo):
        cv2.fillPoly(m, [np.round(np.array(p.exterior.coords) * 16).astype(np.int32)], 1, cv2.LINE_8, shift=4)
    for p in poligonos(geo):
        for h in p.interiors:
            cv2.fillPoly(m, [np.round(np.array(h.coords) * 16).astype(np.int32)], 0, cv2.LINE_8, shift=4)
    return m.astype(bool)


def celda(e):
    """La celda de la cabeza del ídolo: 0,84 de ancho por alto, como el .notdef."""
    alto = (e["desague"] - e["afuera"]) * 1.1
    cy = (e["afuera"] + e["desague"]) / 2
    return (T / 2 - 0.42 * alto, cy - alto / 2, T / 2 + 0.42 * alto, cy + alto / 2)


def a_svg(geo, e, signo):
    d = ""
    for p in poligonos(geo):
        for anillo in [p.exterior, *p.interiors]:
            xy = list(anillo.coords)[:-1]
            d += "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in xy) + " Z "
    x0, y0, x1, y1 = celda(e)
    lineas = "".join(f'<line x1="0" y1="{y:.1f}" x2="{T}" y2="{y:.1f}" stroke="#9a968d" stroke-dasharray="6 5"/>'
                     f'<text x="6" y="{y - 6:.1f}" font-family="monospace" font-size="14" fill="#6d6a63">{n}</text>'
                     for n, y in (("afuera", e["afuera"]), ("borde", e["borde"]), ("fondo", e["fondo"]),
                                  ("desagüe", e["desague"])))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" width="{T}" height="{T}">\n'
            f'<rect width="{T}" height="{T}" fill="#f3f1ea"/>\n'
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="none" '
            f'stroke="#cfcac0" stroke-width="2"/>\n{lineas}\n'
            f'<path d="{d}" fill="#1d1c1a" fill-rule="evenodd"/>\n'
            f'<!-- Contenida · {signo} · cuerpo base (propuesta de la máquina) -->\n</svg>\n')


# ---------------------------------------------------------------- el estado Cinta

def encintar(G, ancho, rng, arrancada=False):
    """La letra puesta con masking sobre el plástico negro de la plataforma.

    La cinta es una banda de ancho constante que no curva en su plano: solo va recta.
    Para girar se pliega (el pliegue sigue la bisectriz) o se superpone otro tramo;
    donde hay dos capas pasa menos luz. Es papel crepé: tiene arrugas finas a lo ancho.
    Se corta con la mano: los extremos quedan dentados. Sobre el volumen guarda arrugas
    cerca de cada pliegue. No hace gotas ni asientos: solo sigue los trazos. Arrancada,
    deja el rastro del adhesivo, que el polvo vuelve visible.
    Devuelve la imagen y cuántos tramos y pliegues llevó.
    """
    S = 2
    capas = np.zeros((T * S, T * S), np.float32)
    crepe = np.zeros_like(capas)
    pliegues = np.zeros_like(capas)
    yy, xx = np.mgrid[0:T * S, 0:T * S].astype(np.float32) / S
    n_tramos = n_pliegues = 0
    for tr, w in G.trazos:
        if len(tr) < 2:
            continue
        simple = np.array(LineString(tr).simplify(0.3 * ancho).coords)
        n = len(simple)
        for i in range(n - 1):
            p0, p1 = simple[i], simple[i + 1]
            L = np.linalg.norm(p1 - p0)
            if L < 1:
                continue
            uu = (p1 - p0) / L
            ww = np.array([-uu[1], uu[0]]) * ancho / 2
            ext0 = 0 if i == 0 else ancho / 2
            ext1 = 0 if i == n - 2 else ancho / 2
            a, b = p0 - uu * ext0, p1 + uu * ext1
            quad = np.array([a + ww, b + ww, b - ww, a - ww])
            banda = np.zeros_like(capas, np.uint8)
            cv2.fillPoly(banda, [np.round(quad * S * 16).astype(np.int32)], 1, cv2.LINE_AA, shift=4)
            for extremo, hacia in ((i == 0, -uu), (i == n - 2, uu)):     # cortada a mano: dientes
                if not extremo:
                    continue
                q = p0 if hacia @ uu < 0 else p1
                for k in np.linspace(-0.5, 0.5, 7):
                    base = q + np.array([-hacia[1], hacia[0]]) * ancho * k
                    diente = base - hacia * rng.uniform(1.5, 5.0)
                    cv2.circle(banda, tuple(np.round(diente * S).astype(int)), int(rng.uniform(2, 4) * S), 0, -1)
            s = (xx - p0[0]) * uu[0] + (yy - p0[1]) * uu[1]            # a lo largo del tramo
            crepe += banda * (0.5 + 0.5 * np.sin(2 * np.pi * s / rng.uniform(2.0, 2.6)))
            capas += banda
            n_tramos += 1
        for i in range(1, n - 1):                                    # pliegues y arrugas
            p, a, b = simple[i], simple[i - 1], simple[i + 1]
            ua = (a - p) / np.linalg.norm(a - p)
            ub = (b - p) / np.linalg.norm(b - p)
            giro = np.degrees(np.arccos(np.clip(ua @ ub, -1, 1)))
            bis = (ua + ub) / (np.linalg.norm(ua + ub) + 1e-9)
            L = ancho / 2 / max(np.sin(np.radians(giro) / 2), 0.35)
            cv2.line(pliegues, tuple(np.round((p - bis * L) * S).astype(int)),
                     tuple(np.round((p + bis * L) * S).astype(int)), 1.0, S)
            n_pliegues += 1
            if giro < 160:
                for _ in range(int(rng.integers(3, 6))):
                    t = rng.uniform(0.2, 0.9)
                    q = p + bis * L * t + rng.normal(0, 2, 2)
                    ang = np.arctan2(bis[1], bis[0]) + rng.normal(np.pi / 2, 0.35)
                    dq = np.array([np.cos(ang), np.sin(ang)]) * rng.uniform(4, 9)
                    cv2.line(pliegues, tuple(np.round((q - dq) * S).astype(int)),
                             tuple(np.round((q + dq) * S).astype(int)), 0.6, 1)
    capas = cv2.resize(capas, (T, T), interpolation=cv2.INTER_AREA)
    crepe = cv2.resize(crepe, (T, T), interpolation=cv2.INTER_AREA)
    pliegues = cv2.GaussianBlur(cv2.resize(pliegues, (T, T), interpolation=cv2.INTER_AREA), (0, 0), 0.6)
    hay = np.clip(capas, 0, 1)
    fondo = PLASTICO * (1 + 0.25 * cv2.GaussianBlur(rng.standard_normal((T, T)).astype(np.float32), (0, 0), 30)
                        [..., None])
    img = np.ones((T, T, 3), np.float32) * fondo
    if arrancada:
        rastro = cv2.GaussianBlur(np.clip(capas, 0, 2), (0, 0), 1.0) * 0.09
        polvo = 0.05 * np.clip(rng.standard_normal((T, T)), 0, None) * hay
        return np.clip(img + (rastro + polvo)[..., None] * np.array([0.9, 0.88, 0.8]), 0, 1), n_tramos, n_pliegues
    opaca = 1 - 0.18 ** np.clip(capas, 0, 3)                         # cada capa deja pasar menos plástico
    tono = CINTA * (1 - 0.06 * np.clip(capas - 1, 0, 2))[..., None] * (1 - 0.05 * (crepe / np.maximum(capas, 1))
                                                                        [..., None])
    img = img * (1 - opaca[..., None]) + tono * opaca[..., None]
    borde = np.clip(cv2.Laplacian(cv2.GaussianBlur(hay, (0, 0), 0.8), cv2.CV_32F) * 3, 0, 1)
    img = img * (1 - 0.22 * np.clip(pliegues, 0, 1))[..., None] * (1 - 0.3 * borde)[..., None]
    fibra = 0.02 * cv2.GaussianBlur(rng.standard_normal((T, T)).astype(np.float32), (0, 0), 0.7) * hay
    return np.clip(img + fibra[..., None], 0, 1), n_tramos, n_pliegues


# ---------------------------------------------------------------- las láminas de la gramática

LADO = 440


def _lineas(d, e, k, rot=True):
    for n, y in (("afuera", e["afuera"]), ("borde", e["borde"]), ("fondo", e["fondo"]), ("desagüe", e["desague"])):
        yy = y * k
        for x in range(0, LADO, 12):
            d.line([(x, yy), (x + 6, yy)], fill=(150, 146, 138), width=1)
        if rot:
            d.text((4, yy - 16), n, font=rotulo(12), fill=(120, 116, 108))


def _celda(d, e, k):
    x0, y0, x1, y1 = celda(e)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=(200, 195, 184), width=1)


def panel_testigo(m, e):
    k = LADO / T
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[m] = (0.62, 0.61, 0.59)
    im = Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k)
    x0, y0, x1, y1 = caja_tinta(m)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=VIOLETA, width=1)
    d.text((x1 * k + 6, y0 * k), f"{x1 - x0} × {y1 - y0} px", font=rotulo(13), fill=VIOLETA)
    return im


def panel_curvas(m, G, e, P):
    k = LADO / T
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[m] = (0.88, 0.87, 0.85)
    im = Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k, rot=False)
    _celda(d, e, k)
    for geo in G.mas:                                        # asientos, gotas y tildes: formas, no trazos
        for p in poligonos(geo):
            d.line([(x * k, y * k) for x, y in p.exterior.coords], fill=(110, 106, 98), width=1)
    for t, w in G.trazos:
        d.line([tuple(p * k) for p in t], fill=VIOLETA, width=3, joint="curve")
    for p in G.nodos:
        x, y = p[0] * k, p[1] * k
        d.rectangle([x - 4, y - 4, x + 4, y + 4], outline=(30, 30, 30), width=1, fill=(243, 241, 234))
    for c in G.menos:
        x, y = c.centroid.coords[0]
        rr = V(P, "alivio") * k
        d.ellipse([x * k - rr, y * k - rr, x * k + rr, y * k + rr], outline=(30, 30, 30), width=1)
    ocupados = []
    for nombre, p in G.marcas:
        x, y = p[0] * k, p[1] * k
        derecha = x > LADO / 2
        ty = y
        while any(abs(ty - o) < 18 for o in ocupados):
            ty += 18
        ocupados.append(ty)
        f = rotulo(13)
        ancho = d.textlength(nombre, font=f)
        tx = LADO - 8 - ancho if derecha else 8
        d.line([(x, y), (tx + (-4 if derecha else ancho + 4), ty)], fill=(120, 116, 108), width=1)
        d.text((tx, ty - 8), nombre, font=f, fill=(40, 40, 40))
    return im


def imagen_cuerpo(mb, gris=(0.11, 0.105, 0.10)):
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[mb] = gris
    return img


def panel_cuerpo(mb, e):
    k = LADO / T
    im = Image.fromarray(a8(imagen_cuerpo(mb))).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k, rot=False)
    _celda(d, e, k)
    return im


def panel_calco(mb, signo, punteado=False):
    from desenterrar import contornos_temblorosos, dibujar_trazos
    tr = contornos_temblorosos(mb, azar("gramatica calco", signo))
    linea = dibujar_trazos((T, T), tr, punteado, azar("gramatica linea", signo), grosor=3)
    img = np.ones((T, T, 3), np.float32) * PAPEL * (1 - 0.85 * linea)[..., None]
    return Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)


def panel(img):
    return Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)


def lamina_generadores(filas, ruta):
    columnas = ["el testigo del pie: medidas", "curvas maestras", "cuerpo base, en vectores",
                "calco: el canal y su desagüe", "cinta puesta", "cinta arrancada"]
    j, mx, arriba = 16, 40, 150
    W = 2 * mx + 6 * LADO + 5 * j
    H = arriba + len(filas) * (LADO + j) + 40
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    d.text((mx, 26), "Gramática de Contenida · los cuatro generadores · simulación", font=rotulo(32),
           fill=(30, 30, 30))
    d.text((mx, 70), "Del pie, las medidas. De la obra, la forma: canal sin contraste, cuenca con fondo plano y "
                     "desagüe, hombro tenso, fuste en planos, asiento, gota. La cinta, sobre el plástico negro.",
           font=rotulo(18), fill=(90, 90, 90))
    for i, c in enumerate(columnas):
        d.text((mx + i * (LADO + j), arriba - 30), c, font=rotulo(17), fill=(60, 60, 60))
    for fi, ims in enumerate(filas):
        for ci, im in enumerate(ims):
            lienzo.paste(im, (mx + ci * (LADO + j), arriba + fi * (LADO + j)))
    guardar(ruta, lienzo)


def lamina_caja(todo, ruta):
    """Los 55 cuerpos base en la caja de 8 × 7: continuo lo hallado, violeta lo reconstruido."""
    celdas = {}
    for c in CELDAS:
        s = c["signo"]
        if s in todo:
            gris = (0.11, 0.105, 0.10) if c["estado"] == "hallada" else (0.29, 0.14, 0.44)
            celdas[c["celda"]] = imagen_cuerpo(todo[s]["mascara"], gris)
    lamina_8x7(celdas, "Gramática · los 55 cuerpos base · simulación",
               "Del pie, las medidas; de la obra, la forma. En violeta, lo reconstruido: las mismas partes, por "
               "analogía.\nLa celda 56 no se dibuja: se hace con los dedos.", ruta)


def main():
    from desenterrar import desenterrar
    GRAM.mkdir(parents=True, exist_ok=True)
    D = desenterrar()
    todo, e, P = D["gramatica"], D["esqueleto"], D["parametros"]
    filas = []
    for s in GENERADORES:
        G, mb = todo[s]["glifo"], todo[s]["mascara"]
        testigo = D["antes"][s]
        (GRAM / f"{s}.svg").write_text(a_svg(todo[s]["geo"], e, s), encoding="utf8")
        puesta, _, _ = encintar(G, V(P, "cinta"), azar("cinta", s))
        arrancada, _, _ = encintar(G, V(P, "cinta"), azar("cinta", s), arrancada=True)
        filas.append([panel_testigo(testigo, e), panel_curvas(testigo, G, e, P), panel_cuerpo(mb, e),
                      panel_calco(mb, s), panel(puesta), panel(arrancada)])
    lamina_generadores(filas, SALIDA / "20_gramatica.png")
    lamina_caja(todo, SALIDA / "21_gramatica_caja.png")
    datos = dict(esqueleto=e, parametros=P,
                 signos={s: dict(receta=v["receta"], partes=sorted({n for n, _ in v["glifo"].marcas}),
                                 area_px=int(v["mascara"].sum()), alivios=len(v["glifo"].menos))
                         for s, v in todo.items()})
    (GRAM / "gramatica.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1, default=float),
                                         encoding="utf8")
    print("canal:", round(e["canal"], 1), "px · signos:", len(todo))


if __name__ == "__main__":
    main()
