"""La geometría de los planos, leída de la gramática (simulacion/gramatica.py).

No dibuja nada propio: corre la gramática y anota, en el lienzo de la placa
(600 px = 150 mm, y hacia abajo), lo que cada lámina necesita acotar:
contornos, ejes, nodos, marcas, alivios y los puntos de construcción de los
cuatro generadores (o, l, n, a), con las mismas fórmulas que sus recetas.

Correr la gramática toma unos veinte segundos; con una ruta de caché, la
segunda vez se lee del archivo.
"""

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
sys.path.insert(0, str(TIPO / "simulacion"))

PX_MM = 4                 # el lienzo de la placa: 4 px por mm
T = 600                   # 150 mm


def _anillos(geo, tol=0.15):
    geo = geo.simplify(tol)
    out = []
    for p in (list(geo.geoms) if hasattr(geo, "geoms") else [geo]):
        for a in [p.exterior, *p.interiors]:
            out.append([[round(x, 2), round(y, 2)] for x, y in list(a.coords)[:-1]])
    return out


def _linea(pts, tol=0.08):
    from shapely.geometry import LineString
    if len(pts) < 3:
        return [[round(float(x), 2), round(float(y), 2)] for x, y in pts]
    return [[round(x, 2), round(y, 2)] for x, y in LineString(pts).simplify(tol).coords]


def construcciones(t, todo):
    """Los puntos de construcción de los generadores, ya corridos como el signo (dx)."""
    import numpy as np
    from gramatica import cuenca_lado, superelipse

    c, F, B = t.c, t.F, t.B
    k, pared = t.v("trapecio"), t.v("pared")
    out = {}

    # o: la cuenca
    x0, y0, x1, y1 = t.caja("o")
    dx = todo["o"]["glifo"].dx
    xi, xd, ya, yb = x0 + c / 2 + dx, x1 - c / 2 + dx, y0 + c / 2, F - c / 2
    cx, rx, cy = (xi + xd) / 2, (xd - xi) / 2, (ya + yb) / 2
    lado = lambda x_medio, x_fondo: dict(
        P0=[x_medio, cy], P1=[x_medio, cy + pared * (yb - cy)],
        P2=[x_fondo + pared * (x_medio - x_fondo), yb], P3=[x_fondo, yb])
    out["o"] = dict(cx=cx, cy=cy, rx=rx, ry=cy - ya, ya=ya, yb=yb, xi=xi, xd=xd,
                    fondo_izq=cx - k * rx, fondo_der=cx + k * rx,
                    bezier_izq=lado(cx - rx, cx - k * rx), bezier_der=lado(cx + rx, cx + k * rx),
                    paredes={str(p): cuenca_lado(cx + rx, cy, cx + k * rx, yb, p).tolist() for p in (0.0, 0.55, 1.0)})

    # l: el fuste
    x0, y0, x1, y1 = t.caja("l")
    dx = todo["l"]["glifo"].dx
    G = todo["l"]["glifo"]
    eje = [list(map(float, p)) for p in G.trazos[0][0]]
    out["l"] = dict(xs=eje[0][0], arriba=y0, fin=eje[-1][1], eje=eje, asiento_y=F,
                    asiento_ancho=t.v("asiento_ancho"), asiento_alto=t.v("asiento_alto"))

    # n: el fuste y el hombro
    x0, y0, x1, y1 = t.caja("n")
    dx = todo["n"]["glifo"].dx
    a = t.astas("n", F - 0.3 * t.xh)
    xi, xd = a[0] + dx, a[-1] + dx
    yt = y0 + c / 2
    yh = yt + t.v("hombro_caida") * (F - yt)
    comparar = {str(n): superelipse((xi + xd) / 2, yh, (xd - xi) / 2, yh - yt, n, 180, 0).tolist()
                for n in (2.0, 3.0, 4.0)}
    out["n"] = dict(xi=xi, xd=xd, yt=yt, yh=yh, tope=y0, arcos=comparar)

    # a: el gancho, la gota, el fuste y la cuenca
    x0, y0, x1, y1 = t.caja("a")
    dx = todo["a"]["glifo"].dx
    e = t.e
    xs = t.astas("a", F - 0.25 * t.xh)[-1]
    xg = e["gancho_a"] + c / 2
    yt = y0 + c / 2
    yh = yt + t.v("hombro_caida") * (F - yt)
    gancho = t.arco((xg + xs) / 2, yh, (xs - xg) / 2, yh - yt, t.v("gancho_fin"), 0)
    p = gancho[0]
    masa, caida = t.v("gota_masa"), t.v("gota_caida")
    centro = (p[0], p[1] + caida + masa / 2)
    fin = (centro[0], centro[1] + masa / 2)
    hx0, hy0, hx1, hy1 = e["ojo_a"]
    arriba = max(hy0 - c / 2, fin[1] + 0.4 * c + c / 2)
    out["a"] = dict(xs=xs + dx, xg=xg + dx, cxg=(xg + xs) / 2 + dx, yt=yt, yh=yh, rx=(xs - xg) / 2, ry=yh - yt,
                    gancho_fin=t.v("gancho_fin"), gota_p=[p[0] + dx, p[1]], gota_centro=[centro[0] + dx, centro[1]],
                    gota_fin=[fin[0] + dx, fin[1]], cuenca_arriba=arriba, cuenca_izq=hx0 - c / 2 + dx,
                    libre=arriba - c / 2 - fin[1], ojo_arriba=hy0)
    return out


def leer(cache=None):
    """{esqueleto, parametros, signos{s: …}, generadores{o, l, n, a}}; en px del lienzo de la placa."""
    if cache and Path(cache).exists():
        return json.loads(Path(cache).read_text(encoding="utf8"))
    import cv2
    import numpy as np

    import gramatica
    from comun import CELDAS

    mover = gramatica.Glifo.mover

    def mover_anotado(self, dx):           # para saber cuánto corrió cada signo hasta el centro de la celda
        self.dx = getattr(self, "dx", 0.0) + dx
        mover(self, dx)

    gramatica.Glifo.mover = mover_anotado
    from desenterrar import desenterrar
    D = desenterrar()
    todo, e, P = D["gramatica"], D["esqueleto"], D["parametros"]
    t = gramatica.Taller(e, P, D["antes"])
    estado = {c["signo"]: c["estado"] for c in CELDAS}
    signos = {}
    for s, v in todo.items():
        G = v["glifo"]
        signos[s] = dict(
            contorno=_anillos(v["geo"]), receta=v["receta"], estado=estado.get(s, ""),
            trazos=[[_linea(p), w] for p, w in G.trazos if len(p) > 1],
            marcas=[[n, round(p[0], 2), round(p[1], 2)] for n, p in G.marcas],
            nodos=[[round(float(x), 2), round(float(y), 2)] for x, y in G.nodos],
            alivios=[[round(m.centroid.x, 2), round(m.centroid.y, 2), round((m.bounds[2] - m.bounds[0]) / 2, 2)]
                     for m in G.menos],
            mas=[_anillos(m, 0.1) for m in G.mas],
            caja=[round(x, 2) for x in v["geo"].bounds], dx=round(G.dx, 3))
    esq = {k: float(e[k]) for k in ("afuera", "borde", "fondo", "desague", "xh", "canal")}
    esq["celda"] = [float(x) for x in gramatica.celda(e)]
    esq["razon_x"] = float(D["med"].get("razon_x", 0))
    esq["grueso"], esq["fino"] = float(D["med"]["grueso"]), float(D["med"]["fino"])
    testigos = {}
    for s in "olna":                       # el testigo del pie, ya achatado, corrido como su signo
        dx = todo[s]["glifo"].dx
        cs, _ = cv2.findContours(D["antes"][s].astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        anillos = [[[round(float(x) + dx, 2), round(float(y), 2)] for x, y in cv2.approxPolyDP(c, 0.6, True)[:, 0]]
                   for c in cs if len(c) > 8]
        x0, y0, x1, y1 = e["cajas"][s]
        testigos[s] = dict(contorno=anillos, caja=[x0 + dx, y0, x1 + dx, y1])
    dxa = todo["a"]["glifo"].dx
    testigos["a"]["ojo"] = [e["ojo_a"][0] + dxa, e["ojo_a"][1], e["ojo_a"][2] + dxa, e["ojo_a"][3]]
    testigos["a"]["gancho"] = e["gancho_a"] + dxa
    datos = dict(esqueleto=esq, parametros={k: dict(valor=float(v["valor"]), unidad=v["unidad"], que=v["que"],
                                                    de_donde=v["de_donde"]) for k, v in P.items()},
                 signos=signos, generadores=construcciones(t, todo), testigos=testigos)
    if cache:
        Path(cache).write_text(json.dumps(datos, ensure_ascii=False, default=float), encoding="utf8")
    return datos


if __name__ == "__main__":
    d = leer(sys.argv[1] if len(sys.argv) > 1 else None)
    print({k: round(v, 1) for k, v in d["esqueleto"].items() if not isinstance(v, list)}, len(d["signos"]))
