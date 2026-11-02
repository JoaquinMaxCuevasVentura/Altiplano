"""Gramática de Contenida: la anatomía base en vectores, antes de los estados.

Uso (desde la raíz del repositorio):
    pip install shapely
    python3 tipografia/simulacion/gramatica.py

El orden es: anatomía base → estados. Del pie se toman solo medidas: dónde
van las astas, cuánto miden el ojo, el hombro y las líneas (el esqueleto de
referencia de cada testigo). Cómo es la forma lo deciden parámetros que salen
de la obra (03c_gramatica.md): el punzón sobre el aluminio, la vasija abierta,
la chapa sobre el cuerpo, la intemperie y la gravedad.

Construye las curvas maestras de los cuatro glifos generadores (o, l, n, a),
su cuerpo en vectores (SVG), el calco que haría la mano y la cinta: la letra
puesta con la cinta que tapó ojos y boca. Escribe en simulacion/salida/:
  20_gramatica.png          la lámina: testigo, curvas, cuerpo, calco y cinta,
  gramatica/<letra>.svg     el cuerpo base de cada generador,
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

from comun import SALIDA, T, a8, azar, caja_tinta, componentes, guardar, rotulo
from desenterrar import contornos_temblorosos, desenterrar, dibujar_trazos

GRAM = SALIDA / "gramatica"
GENERADORES = "olna"
VIOLETA = (74, 36, 112)
PAPEL = np.array([0.955, 0.948, 0.925])
PIEL_CINTA = np.array([0.90, 0.77, 0.66])     # cinta color piel de farmacia (¿o masking? a confirmar)


# ---------------------------------------------------------------- el esqueleto: medidas del testigo

def _corridas(v):
    d = np.diff(np.concatenate([[0], v.astype(int), [0]]))
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]))


def _astas(m, y):
    """Centros de las corridas de tinta de una fila: dónde están las astas."""
    return [(a + b) / 2 for a, b in _corridas(m[int(y)]) if b - a > 6]


def esqueleto(D):
    """Lo que se toma del pie: medidas, no formas."""
    med, A = D["med"], D["antes"]
    fondo, xh = float(med["base"]), float(med["xh"])
    o = A["o"]
    canal = float(np.sqrt(med["grueso"] * med["fino"]))   # entre el grueso y el fino del pie: sin modular
    e = dict(fondo=fondo, borde=fondo - xh, afuera=fondo - float(med["asc"]), desague=fondo + float(med["desc"]),
             xh=xh, canal=canal)
    x0, y0, x1, y1 = caja_tinta(o)
    e["o"] = dict(x0=float(x0), x1=float(x1), y0=float(y0))
    x0, y0, x1, y1 = caja_tinta(A["l"])
    e["l"] = dict(asta=max(_astas(A["l"], (y0 + fondo) / 2)), y0=float(y0))
    x0, y0, x1, y1 = caja_tinta(A["n"])
    astas = _astas(A["n"], fondo - 0.3 * xh)
    e["n"] = dict(izq=astas[0], der=astas[-1], y0=float(y0))
    a = A["a"]
    x0, y0, x1, y1 = caja_tinta(a)
    hueco = binary_fill_holes(a) & ~a
    ojo = max(componentes(hueco), key=lambda c: c[1][4])[0]
    hx0, hy0, hx1, hy1 = caja_tinta(ojo)
    arriba = a[: int(hy0) - 4]
    e["a"] = dict(asta=_astas(a, fondo - 0.25 * xh)[-1], y0=float(y0), ojo=[float(hx0), float(hy0), float(hx1),
                                                                              float(hy1)],
                  gancho_x=float(caja_tinta(arriba)[0]))
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
        "alivio": (round(0.28 * c, 1), "px", "Radio del rebaje en cada encuentro interior en ángulo (v, w, k, x, "
                   "y). En los generadores no hace falta: todo encuentro es tangente.",
                   "Para que el aluminio no se desgarre bajo el punzón (D2)"),
        "gancho_fin": (125, "°", "Dónde termina el gancho alto antes de dejar caer la gota.",
                       "Que la gota cuelgue libre, sin tocar la cuenca"),
        "gota_masa": (round(1.25 * c, 1), "px", "Diámetro de la gota que cuelga de un terminal que mira abajo.",
                      "El líquido que chorrea de la boca (D16)"),
        "gota_caida": (round(0.5 * c, 1), "px", "Cuánto baja la gota antes de juntar peso.", "Ídem: la gravedad"),
        "gota_cuello": (round(0.55 * c, 1), "px", "Ancho del cuello de la gota.", "Ídem"),
        "cinta": (round(c, 1), "px", "Ancho de la cinta, a la escala en que iguala al canal (12,5 mm en la "
                  "de farmacia, a confirmar).", "La cinta que tapó ojos y boca (D12)"),
    }
    return {k: dict(valor=v, unidad=u, que=q, de_donde=f) for k, (v, u, q, f) in P.items()}


def V(P, k):
    return float(P[k]["valor"])


# ---------------------------------------------------------------- geometría de las curvas maestras

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

def glifo_o(e, P, rng):
    c, o = e["canal"], e["o"]
    cx, rx = (o["x0"] + o["x1"]) / 2, (o["x1"] - o["x0"]) / 2 - c / 2
    ytop, ybot = o["y0"] + c / 2, e["fondo"] - c / 2          # la cuenca se asienta plana sobre el fondo
    cy = (ytop + ybot) / 2
    ry = cy - ytop
    k, d, pared = V(P, "trapecio"), V(P, "desague"), V(P, "pared")
    arriba = superelipse(cx, cy, rx, ry, 2, 0, 180)          # la mitad de arriba es la del pie
    der = cuenca_lado(cx + rx, cy, cx + k * rx, ybot, pared)[::-1]
    izq = cuenca_lado(cx - rx, cy, cx - k * rx, ybot, pared)
    eje = np.vstack([[(cx + d / 2, ybot)], der, arriba[1:-1], izq, [(cx - d / 2, ybot)]])
    marcas = [("hombro del pie", arriba[45]), ("trapecio 0,70", (cx - k * rx, ybot)),
              ("desagüe", (cx, ybot + c / 2))]
    return dict(trazos=[eje], mas=[], menos=[], marcas=marcas, nodos=[(cx + k * rx, ybot), (cx - k * rx, ybot),
                                                                        (cx + rx, cy), (cx - rx, cy)])


def fuste(x, arriba, e, P, rng):
    c = e["canal"]
    alto = V(P, "asiento_alto")
    eje = facetar((x, arriba), (x, e["fondo"] - alto + 2), int(V(P, "facetas")), V(P, "quiebre"), rng)
    pie = asiento(x, e["fondo"], c, V(P, "asiento_ancho"), alto)
    return eje, pie


def glifo_l(e, P, rng):
    x = e["l"]["asta"]
    eje, pie = fuste(x, e["l"]["y0"], e, P, rng)
    marcas = [("corte: sin remate", (x, e["l"]["y0"])), ("facetas", tuple(eje[1])), ("asiento", (x, e["fondo"]))]
    return dict(trazos=[eje], mas=[pie], menos=[], marcas=marcas, nodos=list(map(tuple, eje)))


def glifo_n(e, P, rng):
    c, n = e["canal"], e["n"]
    xi, xd = n["izq"], n["der"]
    yt = n["y0"] + c / 2
    ya = yt + V(P, "hombro_caida") * (e["fondo"] - yt)
    arco = superelipse((xi + xd) / 2, ya, (xd - xi) / 2, ya - yt, V(P, "hombro"), 180, 0)
    izq, pie_i = fuste(xi, e["borde"], e, P, rng)
    der_eje, pie_d = fuste(xd, ya, e, P, rng)
    hombro = np.vstack([arco, der_eje[1:]])
    marcas = [("hombro n=3", tuple(arco[60])), ("encuentro tangente", tuple(arco[8])), ("asiento", (xd, e["fondo"]))]
    return dict(trazos=[izq, hombro], mas=[pie_i, pie_d], menos=[], marcas=marcas,
                nodos=[(xi, ya), (xd, ya), tuple(arco[60])])


def glifo_a(e, P, rng):
    c, a = e["canal"], e["a"]
    xs = a["asta"]
    k, d, pared = V(P, "trapecio"), V(P, "desague"), V(P, "pared")
    # el gancho: un hombro que baja por el fuste; su terminal mira abajo y gotea
    xg = a["gancho_x"] + c / 2
    yt = a["y0"] + c / 2
    yh = yt + V(P, "hombro_caida") * (e["fondo"] - yt)
    gancho = superelipse((xg + xs) / 2, yh, (xs - xg) / 2, yh - yt, V(P, "hombro"), V(P, "gancho_fin"), 0)
    eje_f, pie = fuste(xs, yh, e, P, rng)
    gancho_y_fuste = np.vstack([gancho, eje_f[1:]])
    g, g_fin = gota(gancho[0], c, P)
    # la cuenca: el ojo del pie, arriba como en el pie; abajo, pared, fondo plano y desagüe
    hx0, hy0, hx1, hy1 = a["ojo"]
    izq = hx0 - c / 2
    cxb, rxb = (izq + xs) / 2, (xs - izq) / 2
    ytb, ybb = hy0 - c / 2, e["fondo"] - c / 2
    cyb = (ytb + ybb) / 2
    arriba = superelipse(cxb, cyb, rxb, cyb - ytb, 2, 0, 180)
    x_bi = cxb - k * rxb
    x_d = (x_bi + xs - c / 2) / 2                          # el punto más bajo del ojo
    cuenca = np.vstack([arriba, cuenca_lado(cxb - rxb, cyb, x_bi, ybb, pared)[1:], [(x_d - d / 2, ybb)]])
    fondo_der = np.array([(x_d + d / 2, ybb), (xs, ybb)])
    marcas = [("gota", g_fin), ("hombro n=3", tuple(gancho[70])), ("cuenca", (cxb - rxb, cyb)),
              ("desagüe", (x_d, ybb + c / 2)), ("asiento", (xs, e["fondo"]))]
    return dict(trazos=[gancho_y_fuste, cuenca, fondo_der], mas=[g, pie], menos=[], marcas=marcas,
                nodos=[tuple(gancho[0]), (x_bi, ybb), (cxb - rxb, cyb), (xs, yh)])


CONSTRUIR = dict(o=glifo_o, l=glifo_l, n=glifo_n, a=glifo_a)


def cuerpo(g, P, c):
    """El cuerpo base en vectores: trazos del ancho del canal, más asientos y gotas, menos alivios; gastado."""
    partes = [LineString(t).buffer(c / 2, cap_style="flat", join_style="round", quad_segs=24) for t in g["trazos"]]
    geo = unary_union(partes + g["mas"])
    for m in g["menos"]:
        geo = geo.difference(m)
    r = V(P, "intemperie")
    return geo.buffer(-r, quad_segs=16).buffer(r, quad_segs=16)


def centrar(g, geo):
    """Monoespaciada: cada letra, centrada en su celda."""
    x0, _, x1, _ = geo.bounds
    dx = T / 2 - (x0 + x1) / 2
    g["trazos"] = [t + [dx, 0] for t in g["trazos"]]
    g["marcas"] = [(n, (p[0] + dx, p[1])) for n, p in g["marcas"]]
    g["nodos"] = [(p[0] + dx, p[1]) for p in g["nodos"]]
    g["mas"] = [affinity.translate(m, dx, 0) for m in g["mas"]]
    return affinity.translate(geo, dx, 0), dx


# ---------------------------------------------------------------- salida: raster, SVG, calco, cinta

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


def a_svg(geo, e, letra):
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
            f'<!-- Contenida · {letra} · cuerpo base (propuesta de la máquina) -->\n</svg>\n')


def encintar(trazos, ancho, rng, arrancada=False):
    """La letra puesta con cinta: banda de ancho constante, que no curva en su plano.

    La cinta solo puede ir recta; para girar se pliega (el pliegue sigue la bisectriz)
    o se superpone otro tramo. Donde se superpone, la luz pasa por dos capas. Se corta
    con la mano: los extremos quedan dentados. Sobre el volumen guarda arrugas cerca de
    cada pliegue. Arrancada, deja el rastro del adhesivo, más oscuro donde hubo dos capas.
    """
    S = 2
    capas = np.zeros((T * S, T * S), np.float32)
    pliegues = np.zeros_like(capas)
    for tr in trazos:
        simple = np.array(LineString(tr).simplify(0.3 * ancho).coords)
        n = len(simple)
        for i in range(n - 1):
            p0, p1 = simple[i], simple[i + 1]
            u = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-9)
            w = np.array([-u[1], u[0]]) * ancho / 2
            ext0 = 0 if i == 0 else ancho / 2
            ext1 = 0 if i == n - 2 else ancho / 2
            a, b = p0 - u * ext0, p1 + u * ext1
            quad = np.array([a + w, b + w, b - w, a - w])
            banda = np.zeros_like(capas, np.uint8)
            cv2.fillPoly(banda, [np.round(quad * S * 16).astype(np.int32)], 1, cv2.LINE_AA, shift=4)
            for extremo, hacia in ((i == 0, -u), (i == n - 2, u)):     # cortada a mano: dientes
                if not extremo:
                    continue
                q = p0 if hacia @ u < 0 else p1
                for k in np.linspace(-0.5, 0.5, 7):
                    base = q + np.array([-hacia[1], hacia[0]]) * ancho * k
                    diente = base - hacia * rng.uniform(1.5, 5.0)
                    cv2.circle(banda, tuple(np.round(diente * S).astype(int)), int(rng.uniform(2, 4) * S), 0, -1)
            capas += banda
        for i in range(1, n - 1):                                    # pliegues y arrugas
            p, a, b = simple[i], simple[i - 1], simple[i + 1]
            u = (a - p) / np.linalg.norm(a - p)
            v = (b - p) / np.linalg.norm(b - p)
            giro = np.degrees(np.arccos(np.clip(u @ v, -1, 1)))
            bis = (u + v) / (np.linalg.norm(u + v) + 1e-9)
            L = ancho / 2 / max(np.sin(np.radians(giro) / 2), 0.35)
            cv2.line(pliegues, tuple(np.round((p - bis * L) * S).astype(int)), tuple(np.round((p + bis * L) * S)
                                                                                     .astype(int)), 1.0, S)
            if giro < 160:
                for _ in range(int(rng.integers(3, 6))):
                    t = rng.uniform(0.2, 0.9)
                    q = p + bis * L * t + rng.normal(0, 2, 2)
                    ang = np.arctan2(bis[1], bis[0]) + rng.normal(np.pi / 2, 0.35)
                    dq = np.array([np.cos(ang), np.sin(ang)]) * rng.uniform(4, 9)
                    cv2.line(pliegues, tuple(np.round((q - dq) * S).astype(int)), tuple(np.round((q + dq) * S)
                                                                                        .astype(int)), 0.6, 1)
    capas = cv2.resize(capas, (T, T), interpolation=cv2.INTER_AREA)
    pliegues = cv2.GaussianBlur(cv2.resize(pliegues, (T, T), interpolation=cv2.INTER_AREA), (0, 0), 0.6)
    hay = np.clip(capas, 0, 1)
    img = np.ones((T, T, 3), np.float32) * PAPEL
    if arrancada:
        rastro = cv2.GaussianBlur(np.clip(capas, 0, 2), (0, 0), 1.2) * 0.07
        grano = 0.02 * rng.standard_normal((T, T)) * hay
        return np.clip(img * (1 - rastro - grano)[..., None], 0, 1)
    borde = np.clip(cv2.Laplacian(cv2.GaussianBlur(hay, (0, 0), 0.8), cv2.CV_32F) * 3, 0, 1)
    for k in range(int(np.ceil(capas.max()))):                      # cada capa filtra la luz
        capa = np.clip(capas - k, 0, 1)[..., None]
        img = img * (1 - 0.55 * capa * (1 - PIEL_CINTA / 1.02))
    img = img * (1 - 0.18 * np.clip(pliegues, 0, 1))[..., None] * (1 - 0.35 * borde)[..., None]
    fibra = 0.015 * cv2.GaussianBlur(rng.standard_normal((T, T)).astype(np.float32), (0, 0), 0.7) * hay
    return np.clip(img + fibra[..., None], 0, 1)


# ---------------------------------------------------------------- la lámina

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


def panel_testigo(m, e, s, dx):
    k = LADO / T
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[m] = (0.62, 0.61, 0.59)
    im = Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k)
    x0, y0, x1, y1 = caja_tinta(m)
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=VIOLETA, width=1)
    xs = {"o": [], "l": [e["l"]["asta"]], "n": [e["n"]["izq"], e["n"]["der"]], "a": [e["a"]["asta"]]}[s]
    for x in xs:
        for y in range(int(y0 * k), int(e["fondo"] * k), 8):
            d.line([(x * k, y), (x * k, y + 4)], fill=VIOLETA, width=2)
    d.text((x1 * k + 6, y0 * k), f"{x1 - x0} × {y1 - y0} px", font=rotulo(13), fill=VIOLETA)
    return im


def panel_curvas(m, g, e, P):
    k = LADO / T
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[m] = (0.88, 0.87, 0.85)
    im = Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k, rot=False)
    _celda(d, e, k)
    for geo in g["mas"]:                                     # asientos y gotas: formas, no trazos
        for p in poligonos(geo):
            d.line([(x * k, y * k) for x, y in p.exterior.coords], fill=(110, 106, 98), width=1)
    for t in g["trazos"]:
        d.line([tuple(p * k) for p in t], fill=VIOLETA, width=3, joint="curve")
    for p in g["nodos"]:
        x, y = p[0] * k, p[1] * k
        d.rectangle([x - 4, y - 4, x + 4, y + 4], outline=(30, 30, 30), width=1, fill=(243, 241, 234))
    for c in g["menos"]:
        x, y = c.centroid.coords[0]
        rr = V(P, "alivio") * k
        d.ellipse([x * k - rr, y * k - rr, x * k + rr, y * k + rr], outline=(30, 30, 30), width=1)
    ocupados = []
    for nombre, p in g["marcas"]:
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


def panel_cuerpo(mb, e):
    k = LADO / T
    img = np.ones((T, T, 3), np.float32) * PAPEL
    img[mb] = (0.11, 0.105, 0.10)
    im = Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    _lineas(d, e, k, rot=False)
    _celda(d, e, k)
    return im


def panel_calco(mb, letra):
    tr = contornos_temblorosos(mb, azar("gramatica calco", letra))
    linea = dibujar_trazos((T, T), tr, False, azar("gramatica linea", letra), grosor=3)
    img = np.ones((T, T, 3), np.float32) * PAPEL * (1 - 0.85 * linea)[..., None]
    return Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)


def panel(img):
    return Image.fromarray(a8(img)).resize((LADO, LADO), Image.LANCZOS)


def lamina(filas):
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
                     "desagüe, hombro tenso, fuste en planos, asiento, alivio, gota.", font=rotulo(18),
           fill=(90, 90, 90))
    for i, c in enumerate(columnas):
        d.text((mx + i * (LADO + j), arriba - 30), c, font=rotulo(17), fill=(60, 60, 60))
    for fi, ims in enumerate(filas):
        for ci, im in enumerate(ims):
            lienzo.paste(im, (mx + ci * (LADO + j), arriba + fi * (LADO + j)))
    guardar(SALIDA / "20_gramatica.png", lienzo)


def main():
    GRAM.mkdir(parents=True, exist_ok=True)
    D = desenterrar()
    e = esqueleto(D)
    P = parametros(e)
    c = e["canal"]
    filas, salida = [], {}
    for s in GENERADORES:
        rng = azar("gramatica", s)
        g = CONSTRUIR[s](e, P, rng)
        geo, dx = centrar(g, cuerpo(g, P, c))
        mb = rasterizar(geo)
        testigo = np.roll(D["antes"][s], int(round(dx)), axis=1)
        (GRAM / f"{s}.svg").write_text(a_svg(geo, e, s), encoding="utf8")
        filas.append([panel_testigo(testigo, e, s, dx), panel_curvas(testigo, g, e, P), panel_cuerpo(mb, e),
                      panel_calco(mb, s), panel(encintar(g["trazos"], V(P, "cinta"), azar("cinta", s))),
                      panel(encintar(g["trazos"], V(P, "cinta"), azar("cinta", s), arrancada=True))])
        salida[s] = dict(area_px=int(mb.sum()), trazos=len(g["trazos"]), alivios=len(g["menos"]))
    lamina(filas)
    datos = dict(esqueleto={k: v for k, v in e.items()}, parametros=P, generadores=salida)
    (GRAM / "gramatica.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1, default=float),
                                         encoding="utf8")
    print("canal:", round(c, 1), "px ·", {k: v["area_px"] for k, v in salida.items()})


if __name__ == "__main__":
    main()
