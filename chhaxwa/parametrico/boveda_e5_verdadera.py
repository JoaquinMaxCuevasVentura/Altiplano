"""La bóveda verdadera de E5: medio punto, catenaria o rebajada, en lugar de la de hiladas voladas.

El autor preguntó si E5 podía tener una bóveda convencional. Una bóveda verdadera no vuela hiladas: sus piezas se
apoyan unas en otras y empujan hacia los lados, así que la pregunta deja de ser cuánto vuela el adobe y pasa a ser si la
bóveda se sostiene en equilibrio. Para eso se busca una línea de presiones, el camino de los empujes, que quepa dentro
del espesor del anillo; si cabe, la fábrica puede sostenerse solo por su forma. La cuenta es plana, por metro de bóveda,
con el relleno de tierra cargando los riñones. Mide solo el equilibrio, no la resistencia del adobe ni el deslizamiento
de las juntas, y usa pesos supuestos (abajo), que habría que medir.

Se usa desde boveda_e5.py, que lo llama al final. Escribe e5_variantes_verdaderas.csv y la lámina e5_verdaderas (DXF y
PNG), que compara la E5 actual con la mejor de cada tipo.
"""

import csv
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import boveda_e5 as B                                     # noqa: E402

G_ADOBE, G_TIERRA, G_PIEDRA = 18.0, 16.0, 20.0            # pesos en kN/m³: supuestos del proyecto, sin medir
TERCIO = 1 / 3                                            # para la holgura: la línea en el tercio central de cada junta
N_JUNTAS = 60
EMPUJES = [0.25 * 1.12 ** i for i in range(70)]           # de 0,25 a unos 700 kN por metro
# el espesor del anillo sale de cómo se pone el adobe de 40 × 20 × 10 cm en cada dovela
ANILLOS = {0.10: "adobe echado, 10 cm", 0.20: "adobe de canto, 20 cm", 0.40: "adobe a tizón, 40 cm"}
PASO_DOVELA = 0.11                                         # una dovela de 10 cm y su junta, medidas por el intradós


def intrados(tipo, zr, f):
    """El borde de adentro de media bóveda, de la clave (x = 0) al arranque (x = WI/2)."""
    S = B.WI / 2
    if tipo == "medio punto":
        return [(S * math.sin(math.pi / 2 * k / N_JUNTAS), zr + S * math.cos(math.pi / 2 * k / N_JUNTAS))
                for k in range(N_JUNTAS + 1)]
    if tipo == "rebajada":
        R = (S * S + f * f) / (2 * f)
        al = math.asin(S / R)
        zc = zr + f - R
        return [(R * math.sin(al * k / N_JUNTAS), zc + R * math.cos(al * k / N_JUNTAS)) for k in range(N_JUNTAS + 1)]
    lo, hi = 0.05, 80.0                                   # catenaria: la cadena colgada, invertida
    for _ in range(200):
        a = (lo + hi) / 2
        lo, hi = (a, hi) if a * (math.cosh(S / a) - 1) > f else (lo, a)
    return [(S * k / N_JUNTAS, zr + f - a * (math.cosh(S * k / N_JUNTAS / a) - 1)) for k in range(N_JUNTAS + 1)]


def anillo(P, t):
    """El extradós: el intradós corrido t hacia afuera, por la normal."""
    E = []
    for i, (x, z) in enumerate(P):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        tx, tz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(tx, tz)
        E.append((x - tz / n * t, z + tx / n * t))
    return E


def poligono_area(pts):
    a = cx = cz = 0.0
    for (x0, z0), (x1, z1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * z1 - x1 * z0
        a += c
        cx += (x0 + x1) * c
        cz += (z0 + z1) * c
    a /= 2
    return abs(a), (cx / (6 * a), cz / (6 * a)) if a else (0.0, 0.0)


def verdadera(tipo, zr, f, t):
    from shapely.geometry import Polygon, box
    P = intrados(tipo, zr, f)
    E = anillo(P, t)
    techo = E[0][1]
    zf = min(B.HW - B.PARAPETO, techo)
    # las cargas sobre el anillo, acumuladas de la clave a cada junta: cada dovela y la tierra que tiene encima
    W, M, acum = 0.0, 0.0, []
    for k in range(1, len(P)):
        a, c = poligono_area([P[k - 1], P[k], E[k], E[k - 1]])
        W += G_ADOBE * a
        M += G_ADOBE * a * c[0]
        x0, x1 = E[k - 1][0], E[k][0]
        h0, h1 = max(0.0, zf - E[k - 1][1]), max(0.0, zf - E[k][1])
        if x1 > x0 and h0 + h1 > 0:
            area = (h0 + h1) / 2 * (x1 - x0)
            W += G_TIERRA * area
            M += G_TIERRA * area * (x0 + x1) / 2
        acum.append((W, M))
    z_int, z_ext = P[0][1], E[0][1]

    def ventana(H, lim):
        """El tramo de alturas de la clave por donde puede pasar el empuje H para que la línea quepa en cada junta."""
        lo, hi = z_int + lim[0] * (z_ext - z_int), z_int + lim[1] * (z_ext - z_int)
        for k in range(1, len(P)):
            Wk, Mk = acum[k - 1]
            (ax, az), (bx, bz) = P[k], E[k]
            dx, dz = bx - ax, bz - az
            den = H * dz + Wk * dx
            if den <= 1e-12:
                return None
            # s = (H (z0 - az) - (ax Wk - Mk)) / den, con lim0 <= s <= lim1
            base = az + (ax * Wk - Mk) / H
            lo, hi = max(lo, base + lim[0] * den / H), min(hi, base + lim[1] * den / H)
            if lo > hi:
                return None
        return lo, hi

    resultado = {}
    for nombre, lim in (("cabe", (0.0, 1.0)), ("tercio", (TERCIO, 1 - TERCIO))):
        sol = None
        for H in EMPUJES:
            v = ventana(H, lim)
            if v:
                sol = (H, (v[0] + v[1]) / 2)
                break
        resultado[nombre] = sol

    def linea(H, z0):
        pts = [(0.0, z0)]
        for k in range(1, len(P)):
            Wk, Mk = acum[k - 1]
            (ax, az), (bx, bz) = P[k], E[k]
            s = (H * (z0 - az) - (ax * Wk - Mk)) / (H * (bz - az) + Wk * (bx - ax))
            pts.append((ax + s * (bx - ax), az + s * (bz - az)))
        return pts
    # el suelo: con el empuje mínimo, dónde cae la resultante de media casa (anillo, relleno y muros)
    S = B.WI / 2
    vacio = Polygon([(0, 0), (S, 0)] + P[::-1] + [(0, P[0][1])])
    aro = Polygon(P + E[::-1])
    cara_in = box(S, 0, S + B.CARA, zr) if zr > 0 else Polygon()
    cara_out = Polygon([(B.WO / 2 - B.CARA, 0), (B.WO / 2, 0), (B.WO / 2 - B.TALUD * B.HW, B.HW),
                        (B.WO / 2 - B.CARA - B.TALUD * B.HW, B.HW)])
    afuera = Polygon([(B.WO / 2, 0), (B.WO / 2 + 1, 0), (B.WO / 2 + 1, B.HW), (B.WO / 2 - B.TALUD * B.HW, B.HW)])
    tierra = box(0, 0, B.WO / 2, zf).difference(vacio).difference(aro).difference(cara_in).difference(cara_out).difference(afuera)
    piezas = [(G_ADOBE, aro), (G_TIERRA, tierra), (G_PIEDRA, cara_out)] + ([(G_PIEDRA, cara_in)] if zr > 0 else [])
    Wt = sum(g * p.area for g, p in piezas)
    Mt = sum(g * p.area * p.centroid.x for g, p in piezas)
    suelo = None
    if resultado["cabe"]:
        H, z0 = resultado["cabe"]
        suelo = (H * z0 + Mt) / Wt                       # donde la resultante corta el suelo
    def ancho(z):
        if z < zr:
            return B.WI
        xs = [x for (x, zz) in P if zz >= z - 1e-9]
        return 2 * max(xs) if xs else 0.0
    v = dict(tipo=tipo, arranque=zr, flecha=f, espesor=t, P=P, E=E, techo=techo, relleno_alto=zf,
             ancho_de_pie=ancho(B.CABEZA), ancho_sentado=ancho(B.SENTADO),
             adobes=round(2 * aro.area * B.LI / (0.40 * 0.20 * 0.10 * 1.1)),
             relleno=2 * tierra.area * B.LI, cabe=resultado["cabe"], tercio=resultado["tercio"], suelo=suelo,
             empuje=resultado["cabe"][0] if resultado["cabe"] else None,
             cimbra=tipo != "catenaria")                   # solo la catenaria se arma a la nubia, sin cimbra
    v["linea"] = linea(*resultado["cabe"]) if resultado["cabe"] else None
    falla = ""
    if techo > B.HW + 1e-9:
        falla += "A"
    if not resultado["cabe"]:
        falla += "E"
    if suelo is not None and not (S <= suelo <= B.WO / 2):
        falla += "S"
    v["falla"] = falla
    v["cumple"] = not falla
    return v


def barrer():
    vs = []
    for t in ANILLOS:
        for zr in (0.0, 0.05, 0.10, 0.15, 0.20):
            vs.append(verdadera("medio punto", zr, B.WI / 2, t))
        for zr in (0.0, 0.10, 0.20, 0.30, 0.40):
            for f in (1.40, 1.50, 1.60, 1.70, 1.80):
                vs.append(verdadera("catenaria", zr, f, t))
        for zr in (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80):
            for f in (0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50):
                vs.append(verdadera("rebajada", zr, f, t))
    return vs


def mejor(vs, tipo, clave, anillo=0.20):
    """La mejor de un tipo con dovelas de canto, de 20 cm, como el arco de adobe de la foto que mandó el autor."""
    return max([v for v in vs if v["tipo"] == tipo and v["cumple"] and abs(v["espesor"] - anillo) < 1e-9], key=clave)


def elegir(vs):
    por_pie = lambda v: (round(v["ancho_de_pie"], 2), round(v["ancho_sentado"], 2), v["tercio"] is not None, -v["adobes"])
    por_sentado = lambda v: (v["tercio"] is not None, round(v["ancho_sentado"], 2), -v["adobes"], -v["relleno"])
    return [("De medio punto", mejor(vs, "medio punto", por_pie)), ("Catenaria", mejor(vs, "catenaria", por_pie)),
            ("Rebajada", mejor(vs, "rebajada", por_sentado))]


def escribir_csv(vs):
    with open(B.AQUI / "e5_variantes_verdaderas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["tipo", "arranque_m", "flecha_m", "anillo_m", "techo_m", "ancho_de_pie_m", "ancho_sentado_m",
                    "adobes", "relleno_m3", "empuje_min_kN_por_m", "linea_en_el_tercio_central", "resultante_en_el_suelo_m",
                    "pide_cimbra", "cumple", "falla"])
        for v in vs:
            w.writerow([v["tipo"], f"{v['arranque']:.2f}", f"{v['flecha']:.2f}", f"{v['espesor']:.2f}", f"{v['techo']:.3f}",
                        f"{v['ancho_de_pie']:.3f}", f"{v['ancho_sentado']:.3f}", v["adobes"], f"{v['relleno']:.2f}",
                        f"{v['empuje']:.1f}" if v["empuje"] else "", "sí" if v["tercio"] else "no",
                        f"{v['suelo']:.3f}" if v["suelo"] is not None else "", "sí" if v["cimbra"] else "no",
                        "sí" if v["cumple"] else "no", v["falla"]])


def seccion_verdadera(L, v, o):
    """El corte de través de una bóveda verdadera, con su línea de presiones, centrado en o."""
    from dibujar_detalles import rect
    ox, oz = o
    P, E, zr, zf = v["P"], v["E"], v["arranque"], v["relleno_alto"]

    def t(pts, s=1):
        return [(ox + s * x, oz + z) for (x, z) in pts]
    S = B.WI / 2
    for s in (-1, 1):
        L.cortado(t([(B.WO / 2 - B.CARA, 0), (B.WO / 2, 0), (B.WO / 2 - B.TALUD * B.HW, B.HW),
                     (B.WO / 2 - B.CARA - B.TALUD * B.HW, B.HW)], s), "PIEDRA")
        if zr > 0:
            L.cortado(t(rect(S, 0, S + B.CARA, zr), s), "PIEDRA")
        # el relleno: del muro de afuera al extradós, hasta zf, sobre la cara de adentro
        cola = [p for p in E if p[1] <= zf]
        if cola:
            pie = [(S + B.CARA, zr), (S + B.CARA, 0)] if zr > 0 else [(cola[-1][0], 0)]
            relleno = [(B.WO / 2 - B.CARA, 0), (B.WO / 2 - B.CARA - B.TALUD * zf, zf)] + cola + pie
            L.cortado(t(relleno, s), "TIERRA", juntas=False)
        L.cortado(t(P + E[::-1], s), "ADOBE", angulo=0)
        if v["linea"]:
            L.linea(t(v["linea"], s), "PRESIONES")
    largo, juntas = 0.0, []                                                 # las juntas de las dovelas, cada 11 cm
    for k in range(1, len(P)):
        d = math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1])
        while largo + d >= PASO_DOVELA * (len(juntas) + 0.5):
            u = (PASO_DOVELA * (len(juntas) + 0.5) - largo) / d
            juntas.append(((P[k - 1][0] + u * (P[k][0] - P[k - 1][0]), P[k - 1][1] + u * (P[k][1] - P[k - 1][1])),
                           (E[k - 1][0] + u * (E[k][0] - E[k - 1][0]), E[k - 1][1] + u * (E[k][1] - E[k - 1][1]))))
        largo += d
    for (a, b) in juntas:
        for s in (-1, 1):
            L.linea(t([a, b], s), "JUNTAS")
    L.linea(t([(-B.WO / 2 - 0.3, 0), (B.WO / 2 + 0.3, 0)]), "TERRENO")
    L.linea(t([(-B.WO / 2 - 0.15, B.HW), (B.WO / 2 + 0.15, B.HW)]), "OCULTO")
    if v["ancho_de_pie"] > 0:
        a = v["ancho_de_pie"] / 2
        L.linea(t([(-a, B.CABEZA), (a, B.CABEZA)]), "JUNTAS")


def lamina(actual, elegidas):
    from dibujar_detalles import Lamina, TA
    L = Lamina(50, (0, 0))
    L.doc.layers.add("PRESIONES", color=7, lineweight=35)                  # la línea de presiones, gruesa y negra
    celdas = [("Hiladas voladas: la E5 actual", actual)] + elegidas
    for j, (titulo, v) in enumerate(celdas):
        cx, yg = (70 if j % 2 == 0 else 270), (196 if j < 2 else 96)
        o = L.h(cx, yg)
        if "tipo" in v:
            seccion_verdadera(L, v, o)
        else:
            B.seccion(L, v, o, lleno=False)
        L.texto(cx - 51, yg + 52, titulo, 3.0)
        a = v["ancho_sentado"] / 2
        L.cota((o[0] - a, o[1] + B.SENTADO), (o[0] + a, o[1] + B.SENTADO), (o[0], o[1] + B.SENTADO))
        if "tipo" in v:
            filas = [f"arranque a {B.coma(v['arranque'])} m; flecha de {B.coma(v['flecha'])} m",
                     f"dovelas de {ANILLOS[v['espesor']]}",
                     f"lo más alto, a {B.coma(v['techo'])} m",
                     f"de pie, {B.coma(v['ancho_de_pie'])} m de ancho" if v["ancho_de_pie"] else "no hay alto para estar de pie",
                     f"sentado, {B.coma(v['ancho_sentado'])} m de ancho",
                     f"unos {v['adobes']} adobes; {B.coma(v['relleno'], 1)} m³ de relleno",
                     f"empuje de unos {B.coma(v['empuje'], 1)} kN por metro",
                     "la línea de presiones cabe en el tercio central" if v["tercio"] else
                     "la línea de presiones cabe, sin holgura",
                     "pide cimbra mientras se levanta" if v["cimbra"] else "puede levantarse sin cimbra, a la nubia"]
        else:
            filas = [f"arranque a {B.coma(v['arranque'])} m; {v['hiladas']} hiladas",
                     f"vuelo de {B.cm(v['vuelo_inicial'])} a {B.cm(v['vuelo_final'])} cm por hilada",
                     f"lo más alto, a {B.coma(v['techo'])} m",
                     f"de pie, {B.coma(v['ancho_de_pie'])} m de ancho",
                     f"sentado, {B.coma(v['ancho_sentado'])} m de ancho",
                     f"{v['adobes']} adobes; {B.coma(v['relleno'], 1)} m³ de relleno",
                     "no empuja: cada hilada vuela sobre la de abajo",
                     "el vuelo de 13 cm lo dirá la prueba 3",
                     "no pide cimbra"]
        for i, f_ in enumerate(filas):
            L.texto(cx + 56, yg + 40 - i * 5.0, f_, 2.4)
    L.marco("P4", "E5. Bóveda volada o verdadera", "Exploración paramétrica: la bóveda verdadera", [
        "La línea negra dentro del anillo es la línea de presiones con el menor empuje: si cabe en el espesor, la bóveda se sostiene por su",
        "forma. Las bóvedas verdaderas son de dovelas de adobe, con las juntas hacia el centro. Cuenta plana por metro, con pesos supuestos",
        "(adobe 18, tierra 16 y piedra 20 kN/m³) y el relleno en los riñones; no mide la resistencia del adobe ni el deslizamiento."],
        serie="piloto")
    return L.guardar("e5_verdaderas", B.AQUI)
