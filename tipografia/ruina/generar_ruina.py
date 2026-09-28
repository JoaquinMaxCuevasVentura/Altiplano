"""Genera la fuente variable Ruina.

Ruina sale del marco de cuatro ejes que siguió a Vasijas: una fuente como
aparato de traslación, que registra cómo un signo pierde piedra, se vuelve
metal, pasa por el agua y se suelta de la retícula. Usa la misma retícula
que Contenedor (../fuente/glifos.py), con otras reglas:

1. El azulejo es 1,4 veces más ancho que alto. Las mayúsculas (cinco por
   siete azulejos) quedan cuadradas y el ancho de cada letra es amplio.
2. En reposo, las placas encajan con una junta mínima, como sillares: la
   letra es una masa de piedra. Donde un trazo termina hay un corte a 45°;
   en el rincón donde dos trazos se unen, una trampa que retiene la tinta.
3. Cada placa sabe con quién se toca. Por eso la incisión corre por el
   esqueleto de la letra de placa en placa, y al repujarse se desdobla en
   dos líneas: una fina del lado de la luz y una gruesa del lado de la sombra.
4. Cada placa tiene una resistencia. Con la erosión, las juntas se abren,
   las esquinas se desprenden, las placas débiles desaparecen y las fuertes
   quedan como incisiones sueltas en la dirección del trazo.
5. La onda y la deriva solo trasladan placas: el agua mueve, no deforma.
6. Cada letra tiene cuatro vueltas. En reposo son iguales; cuando un eje
   se mueve, ninguna se erosiona, ondula ni flota igual que otra.

Ejes:

    EROD  Erosión    0 piedra ................ 100 polvo
    REFL  Repujado   0 piedra lisa ... 50 incisión ... 100 aluminio repujado
    ONDA  Onda       0 quieta ................ 100 el agua desplaza cada placa
    GRID  Retícula   0 monoespaciada, en la línea ... 100 proporcional, flota

Funciones OpenType:

    calt  las cuatro vueltas; en «boca», la o es el glifo-boca
    kern  quiebres de palabra: agua, piedra, ruina, voz
    liga  () vasija con un pez, [] azulejo, || nivel del agua

El asterisco es el glifo-boca: un signo sellado que enmarca un pez.

Uso:  python3 generar_ruina.py
Salida: Ruina-Variable.ttf y .woff2, y las instancias estáticas en estaticas/.
"""

import math
import os
import random
import sys

import pathops
from fontTools import varLib
from fontTools.agl import UV2AGL
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      InstanceDescriptor, SourceDescriptor)
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.varLib import instancer

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "fuente"))
import glifos  # noqa: E402

FAMILIA = "Ruina"
VERSION = "0.100"
DISENO = "Joaquin Max Cuevas Ventura"
DESCRIPCION = ("Fuente variable de cuatro ejes (erosión, repujado, onda, retícula) "
               "derivada de «Contener una ruina: acciones para desenterrar una voz», "
               "de Rebeca Paz con CreaciónxAcuerpamiento (La Paz, 22 de agosto de 2026), "
               "y del poema que la acompaña. Prototipo generado por reglas.")

# --- Retícula ---------------------------------------------------------------
UPM = 1000
ANCHO = 140            # el azulejo es 1,4 veces más ancho que alto
ALTO = 100
CELDA = 6              # seis azulejos por letra: cinco de letra y uno de aire
VUELTAS = 4

# --- Piedra (EROD 0) ----------------------------------------------------------
JUNTA = {0: 3, 50: 18, 100: 18}   # separación entre placas según la erosión
CINCEL = 0.62          # corte a 45° en el extremo de un trazo (relativo a la semiplaca menor)
TRAMPA = 0.50          # corte en el rincón donde dos trazos se unen
PEZ = 1.15             # semidiagonal del pez, relativa a la semiplaca
PUNTA_PEZ = 0.10       # las puntas del pez vienen apenas cortadas

# --- Repujado (REFL) ----------------------------------------------------------
SURCO = 8              # semiancho de la incisión (REFL 50)
SURCO_DOBLE = 17       # semiancho del surco del repujado (REFL 100)
LOMO = 8               # semiancho del lomo que queda entre las dos líneas
LUZ = 3                # el lomo se corre hacia la luz, arriba a la izquierda
FACETA = (0.10, 0.24)  # el prensado achaflana cada esquina (relativo a la semiplaca menor)
TOPE = 0.28            # la incisión termina antes del extremo del trazo
PUNZON = (0.34, 0.14)  # placa suelta: marca de punzón (surco y lomo, relativos a la semiplaca)

# --- Erosión ------------------------------------------------------------------
EROSION = (0.70, 0.92)  # tamaño de la placa con EROD 50, según su resistencia
ASTILLA = 0.22          # cuánto se desprende cada esquina con EROD 50
POLVO = 0.38            # con EROD 100 desaparecen las placas menos resistentes que esto
FRAGIL = 0.60           # los terminales resisten menos
SURCO_GASTADO = 0.60    # la erosión gasta la incisión antes que la placa
BRAZO_GASTADO = 0.62

# --- Onda ---------------------------------------------------------------------
ONDA_X = 0.30          # desplazamiento horizontal de cada fila (en azulejos)
FILAS_ONDA = 4.2       # longitud de la onda, en filas
ONDA_Y = 0.22          # desplazamiento vertical de cada columna
COLUMNAS_ONDA = 3.4

# --- Retícula / deriva (GRID) -------------------------------------------------
FLOTA_Y = 0.55         # cuánto sube o baja cada letra (en altos de azulejo)
FLOTA_X = 0.12
SUELTA = {"terminal": 0.50, "placa": 0.12, "pez": 0.60}   # probabilidad de soltarse
ESPACIO_LIBRE = 3      # el espacio proporcional mide tres azulejos

EJES = [
    # etiqueta, nombre, nombre en castellano, mínimo, defecto, máximo
    ("EROD", "Erosion", "Erosión", 0, 0, 100),
    ("REFL", "Emboss", "Repujado", 0, 0, 100),
    ("ONDA", "Wave", "Onda", 0, 0, 100),
    ("GRID", "Grid", "Retícula", 0, 0, 100),
]
DEFECTO = {e[0]: e[4] for e in EJES}

# Erosión y repujado se multiplican (el surco depende del tamaño de la placa):
# por eso hay un maestro en cada cruce. Onda y retícula solo trasladan.
MAESTROS = ([{"EROD": e, "REFL": r} for e in (0, 50, 100) for r in (0, 50, 100)]
            + [{"ONDA": 100}, {"GRID": 100}])

INSTANCIAS = [
    ("Piedra", {}),
    ("Intemperie", {"EROD": 50}),
    ("Polvo", {"EROD": 100}),
    ("Incisión", {"REFL": 50}),
    ("Repujado", {"REFL": 100}),
    ("Refracción", {"ONDA": 100}),
    ("Deriva", {"GRID": 100}),
    ("Vuelve escrito", {"EROD": 30, "REFL": 100, "ONDA": 40, "GRID": 50}),
]

# Ligaduras hechas de puntuación (liga)
LIGADURAS = {
    "vasija": "()",    # dos paréntesis enfrentados cierran una vasija con un pez
    "azulejo": "[]",   # dos corchetes cierran un azulejo vacío
    "nivel": "||",     # dos plecas se acuestan: el nivel del agua
}

# Quiebres de palabra (kern): desplazamientos (x, y, avance) por letra
QUIEBRES = {
    "agua": [(0, 36, 44), (0, -26, 44), (0, 36, 44), (0, -26, 44)],
    "piedra": [(0, 0, 0), (0, 0, 0), (0, 0, 90), (0, -40, 0), (0, -40, 0), (0, -40, 0)],
    "ruina": [(0, 0, 24), (0, -14, 24), (0, -32, 24), (0, -56, 24), (0, -86, 24)],
    "ruinas": [(0, 0, 24), (0, -14, 24), (0, -32, 24), (0, -56, 24), (0, -86, 24), (0, -120, 24)],
    "voz": [(0, -60, 0), (0, -36, 0), (0, -12, 0)],
}


# --- Utilidades ---------------------------------------------------------------

def nombre_glifo(ch):
    cp = ord(ch)
    if cp == 0x20:
        return "space"
    return UV2AGL.get(cp, "uni%04X" % cp)


def area(pts):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) / 2


def girar_indices(origen, destino):
    """Rota la lista destino para que cada vértice caiga cerca del de origen."""
    n = len(origen)
    mejor, k_mejor = None, 0
    for k in range(n):
        d = sum((ox - destino[(i + k) % n][0]) ** 2 + (oy - destino[(i + k) % n][1]) ** 2
                for i, (ox, oy) in enumerate(origen))
        if mejor is None or d < mejor:
            mejor, k_mejor = d, k
    return [destino[(i + k_mejor) % n] for i in range(n)]


# --- Topología: de la retícula a los elementos ----------------------------------

VECINOS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0),
           "NE": (1, 1), "NW": (-1, 1), "SE": (1, -1), "SW": (-1, -1)}
ESQUINAS = {"NE": ("N", "E"), "NW": ("N", "W"), "SE": ("S", "E"), "SW": ("S", "W")}


def filas_a_elementos(filas):
    """Convierte una retícula (fila -> texto) en elementos con su topología."""
    placas, peces = {}, []
    for fila, texto in filas.items():
        corrimiento = 1.0 if len(texto) == 5 else 0.5 if len(texto) == 6 else 0.5
        for col, c in enumerate(texto):
            x = col + corrimiento
            if c == "#":
                placas[(col, fila)] = x
            elif c == "*":
                peces.append({"tipo": "pez", "x": x, "y": fila + 0.5, "escala": 1.0})
    elementos = []
    for (col, fila), x in sorted(placas.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
        v = {k for k, (dc, df) in VECINOS.items() if (col + dc, fila + df) in placas}
        elementos.append({"tipo": "placa", "x": x, "y": fila + 0.5, "escala": 1.0,
                          "vecinos": v, "col": col})
    return elementos + peces


def topologia(e):
    """Deduce de los vecinos el papel de la placa: terminal, uniones, brazos."""
    v = e["vecinos"]
    e["terminal"] = None
    e["cincel"] = None
    if len(v) == 1:
        dc, df = VECINOS[next(iter(v))]
        e["terminal"] = (-dc, -df)            # se aleja de su único vecino
        afuera = (-dc, -df)
        if afuera[0] and afuera[1]:            # trazo diagonal: se corta la esquina de afuera
            e["cincel"] = ("N" if afuera[1] > 0 else "S") + ("E" if afuera[0] > 0 else "W")
        else:                                  # trazo recto: corte a 45°, siempre del mismo lado
            e["cincel"] = {(0, 1): "NW", (1, 0): "NE", (0, -1): "SE", (-1, 0): "SW"}[afuera]
    # Trampa de tinta: la placa es el rincón de una unión cuando sus dos
    # vecinos ortogonales de una esquina están y el diagonal no.
    e["trampas"] = {k for k, (a, b) in ESQUINAS.items() if a in v and b in v and k not in v}
    brazos = {k for k in "NESW" if k in v}
    e["brazos"] = {k: "borde" for k in brazos}
    if len(brazos) == 1 and not (v - brazos):
        opuesto = {"N": "S", "S": "N", "E": "W", "W": "E"}[next(iter(brazos))]
        e["brazos"][opuesto] = "tope"          # la incisión se detiene antes del extremo
    diagonales = [k for k in ("NE", "NW", "SE", "SW") if k in v]
    e["diagonal"] = None
    if not brazos and diagonales:
        dc, df = VECINOS[diagonales[0]]
        n = math.hypot(dc * ANCHO, df * ALTO)
        e["diagonal"] = (dc * ANCHO / n, df * ALTO / n)
    # Dirección del trazo, para la incisión que queda con EROD 100
    vert = len(v & {"N", "S"})
    hori = len(v & {"E", "W"})
    if e["diagonal"]:
        e["direccion"] = e["diagonal"]
    elif vert > hori:
        e["direccion"] = (0.0, 1.0)
    elif hori > vert:
        e["direccion"] = (1.0, 0.0)
    else:
        e["direccion"] = None
    return e


def elementos_de_acento(nombre, mayuscula):
    sube = 2.0 if mayuscula else 0.0
    return [{"tipo": "pez", "x": x + 1.0, "y": f + sube + 0.5, "escala": s}
            for x, f, s in glifos.ACENTOS[nombre]]


# Glifos propios de Ruina (filas de seis ocupan la celda entera)
PROPIOS = {
    # El glifo-boca: un signo sellado que enmarca un pez.
    "*": glifos.G(4, "#####", "#...#", "#.*.#", "#...#", "#####"),
    "vasija": glifos.G(5, "..##..", ".#..#.", "#....#", "#....#", "#....#", ".#..#.", "..##.."),
    "azulejo": glifos.G(6, "######", "#....#", "#....#", "#....#", "#....#", "#....#",
                        "#....#", "######"),
    # En Contenedor el calderón es el signo escalonado. Ruina no lleva motivos
    # de Tiwanaku: su calderón es el de la imprenta, dibujado en la retícula.
    "¶": glifos.G(6, ".####", "###.#", "###.#", ".##.#", "..#.#", "..#.#", "..#.#"),
}


def elementos_propios(nombre):
    if nombre == "vasija":
        return filas_a_elementos(PROPIOS["vasija"]) + [
            {"tipo": "pez", "x": 3.0, "y": 2.5, "escala": 1.0}]
    if nombre == "nivel":
        # dos líneas de agua que cruzan la celda; cada tramo es un azulejo
        return [{"tipo": "linea", "x": c + 0.5, "y": y, "escala": 1.0}
                for y in (1.9, 2.8) for c in range(CELDA)]
    return filas_a_elementos(PROPIOS[nombre])


def elementos_ornamento(nombre):
    cx, cy = 3.0, 3.5
    if nombre == "pez":
        return [{"tipo": "pez", "x": cx, "y": cy, "escala": 4.2}]
    if nombre == "placa":
        return filas_a_elementos(PROPIOS["*"])
    if nombre == "disco":
        anillo = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            anillo.append({"tipo": "pez", "x": cx + 2.2 * math.cos(a),
                           "y": cy + 3.0 * math.sin(a), "escala": 0.55})
        return anillo + [{"tipo": "pez", "x": cx, "y": cy, "escala": 1.2}]
    raise KeyError(nombre)


def elementos_notdef():
    filas = {6: "#####", 0: "#####"}
    for f in range(1, 6):
        filas[f] = "#...#"
    return filas_a_elementos(filas)


# --- Azar reproducible por vuelta ----------------------------------------------

def sembrar(elementos, semilla):
    rng = random.Random(semilla)
    glifo = {
        "fase_x": rng.uniform(0, 2 * math.pi),
        "fase_y": rng.uniform(0, 2 * math.pi),
        "flota": (rng.uniform(-FLOTA_X, FLOTA_X) * ANCHO, rng.uniform(-FLOTA_Y, FLOTA_Y) * ALTO),
    }
    sembrados = []
    for e in elementos:
        e = dict(e)
        if e["tipo"] == "placa":
            topologia(e)
        r = rng.random()
        if e.get("terminal"):
            r *= FRAGIL
        e["resistencia"] = r
        e["astillas"] = [rng.uniform(0, ASTILLA * (1 - 0.5 * r)) for _ in range(8)]
        e["astillas_polvo"] = [rng.uniform(0, 0.25) for _ in range(8)]
        e["facetas"] = {k: rng.uniform(*FACETA) for k in ESQUINAS}
        e["corrida"] = rng.uniform(-0.2, 0.2)
        tipo = "terminal" if e.get("terminal") else e["tipo"]
        if e["tipo"] != "linea" and rng.random() < SUELTA.get(tipo, 0):
            e["suelta"] = (rng.uniform(-0.45, 0.45) * ANCHO, rng.uniform(-1.0, 0.4) * ALTO)
        else:
            e["suelta"] = (0.0, 0.0)
        sembrados.append(e)
    return glifo, sembrados


# --- Geometría de un elemento en un maestro --------------------------------------

def octogono(hx, hy, c):
    """Placa con sus esquinas cortadas a 45°, en sentido horario."""
    return [(-hx + c["NW"], hy), (hx - c["NE"], hy), (hx, hy - c["NE"]), (hx, -hy + c["SE"]),
            (hx - c["SE"], -hy), (-hx + c["SW"], -hy), (-hx, -hy + c["SW"]), (-hx, hy - c["NW"])]


def rombo(a, b, k):
    """El pez: un azulejo girado 45°, con las puntas cortadas (horario)."""
    return [(-k * a, (1 - k) * b), (k * a, (1 - k) * b), ((1 - k) * a, k * b), ((1 - k) * a, -k * b),
            (k * a, -(1 - k) * b), (-k * a, -(1 - k) * b), (-(1 - k) * a, -k * b), (-(1 - k) * a, k * b)]


def cruz(brazos, g, ox=0.0, oy=0.0):
    """Surco: un cuadrado central de semiancho g y un brazo por dirección.

    brazos: {dirección: coordenada del extremo}; sentido antihorario (hueco).
    (ox, oy) corre el centro y el ancho de los brazos, no sus extremos.
    """
    pts = []
    if "E" in brazos:
        pts += [(ox + g, oy - g), (brazos["E"], oy - g), (brazos["E"], oy + g)]
    else:
        pts += [(ox + g, oy - g)]
    if "N" in brazos:
        pts += [(ox + g, oy + g), (ox + g, brazos["N"]), (ox - g, brazos["N"])]
    else:
        pts += [(ox + g, oy + g)]
    if "W" in brazos:
        pts += [(ox - g, oy + g), (brazos["W"], oy + g), (brazos["W"], oy - g)]
    else:
        pts += [(ox - g, oy + g)]
    if "S" in brazos:
        pts += [(ox - g, oy - g), (ox - g, brazos["S"]), (ox + g, brazos["S"])]
    else:
        pts += [(ox - g, oy - g)]
    return pts


def raya(u, largo, g, ox=0.0, oy=0.0):
    """Surco recto en la dirección u (antihorario)."""
    ux, uy = u
    nx, ny = -uy, ux
    return [(ox + ux * largo - nx * g, oy + uy * largo - ny * g),
            (ox + ux * largo + nx * g, oy + uy * largo + ny * g),
            (ox - ux * largo + nx * g, oy - uy * largo + ny * g),
            (ox - ux * largo - nx * g, oy - uy * largo - ny * g)]


def cuadro(p, ox=0.0, oy=0.0):
    return [(ox + p, oy - p), (ox + p, oy + p), (ox - p, oy + p), (ox - p, oy - p)]


def rombo_hueco(a, b, ox=0.0, oy=0.0):
    return [(ox + a, oy), (ox, oy + b), (ox - a, oy), (ox, oy - b)]


def anchos_de_surco(E, R):
    """Semiancho del surco y del lomo según la erosión y el repujado."""
    gasto = {0: 1.0, 50: SURCO_GASTADO, 100: 0.0}[E]
    surco = {0: 0.0, 50: SURCO, 100: SURCO_DOBLE}[R] * gasto
    lomo = {0: 0.0, 50: 0.0, 100: LOMO}[R] * gasto
    luz = LUZ * gasto if R == 100 else 0.0
    return surco, lomo, luz


def geometria_placa(e, E, R):
    """Cuerpo, surco y lomo de una placa, en coordenadas locales."""
    junta = JUNTA[E]
    hx0 = (ANCHO - junta) / 2 * e["escala"]
    hy0 = (ALTO - junta) / 2 * e["escala"]
    menor = min(hx0, hy0)
    s = 1.0 if E == 0 else EROSION[0] + (EROSION[1] - EROSION[0]) * e["resistencia"]
    hx, hy = hx0 * s, hy0 * s
    surco, lomo, luz = anchos_de_surco(E, R)

    c = {k: 0.0 for k in ESQUINAS}
    for k in e["trampas"]:
        c[k] += TRAMPA * menor * s
    if e["cincel"]:
        c[e["cincel"]] += CINCEL * menor * s
    if R == 100:
        for k in ESQUINAS:
            c[k] += e["facetas"][k] * menor * s
    # El surco tiene que salir por el borde recto de la placa: los cortes no
    # pueden comerse ese tramo. Tampoco dos cortes pueden cruzarse.
    for k, (a, b) in ESQUINAS.items():
        limite = min(hx, hy) - 2
        if a in e["brazos"]:
            limite = min(limite, hx - surco - 2)
        if b in e["brazos"]:
            limite = min(limite, hy - surco - 2)
        c[k] = max(0.0, min(c[k], limite))

    cuerpo = octogono(hx, hy, c)
    if E == 50:
        cuerpo = [(x * (1 - a), y * (1 - a)) for (x, y), a in zip(cuerpo, e["astillas"])]
    if E == 100:
        cuerpo_50 = [(x * (1 - a), y * (1 - a)) for (x, y), a in
                     zip(octogono(hx0 * s, hy0 * s, {k: 0.0 for k in ESQUINAS}), e["astillas"])]
        cuerpo = polvo(e, hx0, hy0, cuerpo_50)

    # El surco
    if surco <= 0 or E == 100:
        return cuerpo, [(0.0, 0.0)] * len(forma_surco(e, 1, 1, hx, hy, E)), \
            [(0.0, 0.0)] * len(forma_surco(e, 1, 1, hx, hy, E))
    hueco = forma_surco(e, surco, 0.0, hx, hy, E)
    if lomo > 0:
        isla = forma_surco(e, lomo, surco - lomo, hx, hy, E, luz=luz, isla=True)
        isla = list(reversed(isla))
    else:
        isla = [(0.0, 0.0)] * len(hueco)
    return cuerpo, hueco, isla


def forma_surco(e, g, retiro, hx, hy, E, luz=0.0, isla=False):
    """Polígono del surco de semiancho g. retiro acorta los brazos que terminan
    adentro de la placa (para que el surco envuelva al lomo)."""
    gasto = 1.0 if E == 0 else BRAZO_GASTADO
    ox, oy = -luz, luz
    if e["brazos"]:
        brazos = {}
        for k, modo in e["brazos"].items():
            medio = hx if k in "EW" else hy
            signo = 1 if k in "NE" else -1
            if modo == "borde" and E == 0:
                largo = medio
            elif modo == "borde":
                largo = medio * gasto - retiro
            else:
                largo = max(TOPE * medio - retiro, g)
            brazos[k] = signo * largo
        return cruz(brazos, g, ox if "N" in brazos or "S" in brazos else 0.0,
                    oy if "E" in brazos or "W" in brazos else 0.0)
    if e["diagonal"]:
        largo = 0.55 * min(hx, hy) * math.sqrt(2) * (1.0 if E == 0 else gasto)
        return raya(e["diagonal"], max(largo - retiro, g), g, ox, oy)
    # placa suelta: una marca de punzón
    menor = min(hx, hy)
    if isla:
        return cuadro(g / LOMO * PUNZON[1] * menor, ox, oy)
    return cuadro(g / SURCO_DOBLE * PUNZON[0] * menor, ox, oy)


def polvo(e, hx0, hy0, cuerpo_50):
    """Con EROD 100 la placa desaparece o queda como incisión suelta."""
    r = e["resistencia"]
    if r < POLVO:
        return [(0.0, 0.0)] * 8
    t = (r - POLVO) / (1 - POLVO)
    d = e.get("direccion")
    if d:
        # una astilla angosta en la dirección del trazo
        ux, uy = d
        nx, ny = -uy, ux
        largo = (0.45 + 0.40 * t) * (abs(ux) * hx0 + abs(uy) * hy0)
        ancho = 6 + 5 * t
        corre = e["corrida"] * largo
        astilla = octogono(largo, ancho, {q: 0.45 * ancho for q in ESQUINAS})
        contorno = [(ux * (a + corre) + nx * b, uy * (a + corre) + ny * b) for a, b in astilla]
        return girar_indices(cuerpo_50, contorno)
    k = 0.30 * (0.6 + 0.8 * t)
    trozo = octogono(hx0 * k, hy0 * k, {q: 0.25 * min(hx0, hy0) * k for q in ESQUINAS})
    return [(x * (1 - a), y * (1 - a)) for (x, y), a in zip(trozo, e["astillas_polvo"])]


def geometria_pez(e, E, R):
    junta = JUNTA[E]
    a0 = PEZ * (ANCHO - junta) / 2 * e["escala"]
    b0 = PEZ * (ALTO - junta) / 2 * e["escala"]
    r = e["resistencia"]
    if E == 0:
        s = 1.0
    elif E == 50:
        s = 0.80 + 0.12 * r
    else:
        s = 0.0 if r < POLVO else 0.45
    a, b = a0 * s, b0 * s
    k = PUNTA_PEZ + (0.08 if R == 100 else 0.0)
    cuerpo = rombo(a, b, k)
    if E == 50:
        cuerpo = [(x * (1 - q), y * (1 - q)) for (x, y), q in zip(cuerpo, e["astillas"])]
    surco, lomo, luz = anchos_de_surco(E, R)
    if surco <= 0 or s == 0 or E == 100:
        return cuerpo, [(0.0, 0.0)] * 4, [(0.0, 0.0)] * 4
    f = surco / SURCO_DOBLE if R == 100 else surco / SURCO
    hueco = rombo_hueco(a * (0.22 if R == 50 else 0.36) * f, b * (0.22 if R == 50 else 0.36) * f)
    if lomo > 0:
        isla = list(reversed(rombo_hueco(a * 0.17 * f, b * 0.17 * f, -luz * 0.5, luz * 0.5)))
    else:
        isla = [(0.0, 0.0)] * 4
    return cuerpo, hueco, isla


def geometria_linea(e):
    hx = ANCHO / 2 + 1   # los tramos se tocan de una celda a otra
    hy = 7
    return [[(-hx, hy), (hx, hy), (hx, -hy), (-hx, -hy)]]


def contornos_elemento(e, loc, glifo):
    """Los contornos (en unidades de la fuente) de un elemento en un maestro."""
    E, R = loc.get("EROD", 0), loc.get("REFL", 0)
    O, G = loc.get("ONDA", 0), loc.get("GRID", 0)
    cx, cy = e["x"] * ANCHO, e["y"] * ALTO
    if O:
        cx += ONDA_X * ANCHO * math.sin(2 * math.pi * e["y"] / FILAS_ONDA + glifo["fase_x"])
        cy += ONDA_Y * ALTO * math.sin(2 * math.pi * e["x"] / COLUMNAS_ONDA + glifo["fase_y"])
    if G:
        cx += glifo["corrimiento"] + glifo["flota"][0] + e["suelta"][0]
        cy += glifo["flota"][1] + e["suelta"][1]
    if e["tipo"] == "linea":
        partes = geometria_linea(e)
    elif e["tipo"] == "pez":
        partes = geometria_pez(e, E, R)
    else:
        partes = geometria_placa(e, E, R)
    return [[(cx + x, cy + y) for x, y in c] for c in partes]


# --- El repertorio -----------------------------------------------------------

def columnas_ocupadas(filas):
    cols = [c for texto in filas.values() if len(texto) == 5
            for c, ch in enumerate(texto) if ch != "."]
    anchas = any(len(t) == 6 for t in filas.values())
    if anchas or not cols:
        return None
    return min(cols), max(cols)


def repertorio():
    """Lista de (nombre, código o None, elementos, columnas ocupadas)."""
    glifos.validar()
    reticula = glifos.todos()
    reticula["*"] = PROPIOS["*"]
    reticula["¶"] = PROPIOS["¶"]
    items = []
    for ch, filas in reticula.items():
        items.append((nombre_glifo(ch), ord(ch), filas_a_elementos(filas), columnas_ocupadas(filas)))
    for ch, (base, acento) in glifos.COMPUESTOS.items():
        elementos = filas_a_elementos(reticula[base]) + elementos_de_acento(acento, base.isupper())
        items.append((nombre_glifo(ch), ord(ch), elementos, columnas_ocupadas(reticula[base])))
    for ch, orn in glifos.ORNAMENTOS.items():
        items.append((nombre_glifo(ch), ord(ch), elementos_ornamento(orn), None))
    for nombre in LIGADURAS:
        items.append((nombre, None, elementos_propios(nombre), None))
    return items


def avance_libre(nombre, columnas):
    """Avance con GRID 100: proporcional a lo que la letra ocupa."""
    if nombre == "space" or nombre == "uni00A0":
        return ESPACIO_LIBRE * ANCHO, 0.0
    if columnas is None:
        return CELDA * ANCHO, 0.0
    c0, c1 = columnas
    return (c1 - c0 + 2) * ANCHO, -c0 * ANCHO


def construir_glifos(items):
    """Siembra las cuatro vueltas de cada glifo."""
    sembrados = {}
    g, el = sembrar(elementos_notdef(), ".notdef")
    g["corrimiento"] = 0.0
    sembrados[".notdef"] = (g, el, CELDA * ANCHO)
    for nombre, cp, elementos, columnas in items:
        libre, corrimiento = avance_libre(nombre, columnas)
        for v in range(VUELTAS):
            n = nombre if v == 0 else "%s.v%d" % (nombre, v)
            g, el = sembrar(elementos, "%s|%d" % (nombre, v))
            g["corrimiento"] = corrimiento
            sembrados[n] = (g, el, libre)
    return sembrados


def glifo_tt(lista):
    g = Glyph()
    if not lista:
        g.numberOfContours = 0
        return g
    puntos, fines = [], []
    for c in lista:
        puntos.extend((round(x), round(y)) for x, y in c)
        fines.append(len(puntos) - 1)
    g.numberOfContours = len(lista)
    g.coordinates = GlyphCoordinates(puntos)
    g.endPtsOfContours = fines
    g.flags = bytearray([1] * len(puntos))
    g.flags[0] |= 0x40   # OVERLAP_SIMPLE
    g.program = ttProgram.Program()
    g.program.fromBytecode(b"")
    return g


# --- Funciones OpenType -------------------------------------------------------

def clase_de(ch, base):
    n = nombre_glifo(ch)
    if n not in base:
        return None
    return [n] + ["%s.v%d" % (n, v) for v in range(1, VUELTAS)]


def codigo_fea(items):
    base = [n for n, cp, e, c in items]
    conjunto = set(base)
    clases = ["@V0 = [%s];" % " ".join(base)]
    for v in range(1, VUELTAS):
        clases.append("@V%d = [%s];" % (v, " ".join("%s.v%d" % (n, v) for n in base)))
    salto = {n: ((cp or sum(map(ord, n))) % 3) + 1 for n, cp, e, c in items}
    grupos = {}
    for n in base:
        for v in range(VUELTAS):
            nv = n if v == 0 else "%s.v%d" % (n, v)
            grupos.setdefault((v, salto[n]), []).append(nv)
    ciclo = []
    for (v, h), miembros in sorted(grupos.items()):
        clases.append("@P%d_%d = [%s];" % (v, h, " ".join(miembros)))
        destino = (v + h) % VUELTAS
        if destino:
            ciclo.append("        sub @P%d_%d @V0' by @V%d;" % (v, h, destino))

    # Letras de las palabras que se quiebran
    letras = sorted({ch for palabra in list(QUIEBRES) + ["boca"] for ch in palabra})
    for ch in letras:
        miembros = clase_de(ch, conjunto)
        mayus = clase_de(ch.upper(), conjunto)
        clases.append("@l_%s = [%s];" % (ch, " ".join(miembros)))
        clases.append("@i_%s = [%s];" % (ch, " ".join(miembros + (mayus or []))))
    todas = [ch for ch in glifos.todos() if ch.isalpha()] + [ch for ch in glifos.COMPUESTOS if ch.isalpha()]
    letra = sorted({g for ch in todas for g in clase_de(ch, conjunto) or []})
    sin_s = [g for g in letra if g.split(".")[0] not in ("s", "S")]
    clases.append("@letra = [%s];" % " ".join(letra))
    clases.append("@letra_sin_s = [%s];" % " ".join(sin_s))

    def secuencia(palabra):
        return ["@i_%s" % palabra[0]] + ["@l_%s" % ch for ch in palabra[1:]]

    quiebres = []
    for palabra in sorted(QUIEBRES, key=len, reverse=True):
        seq = secuencia(palabra)
        valores = QUIEBRES[palabra]
        # la entrada empieza en la primera letra que se mueve
        primero = next(i for i, (dx, dy, av) in enumerate(valores) if dx or dy or av)
        atras, entrada = seq[:primero], seq[primero:]
        vr = valores[primero:]
        marcada = " ".join("%s'" % s for s in entrada)
        despues = "@letra_sin_s" if not palabra.endswith("s") else "@letra"
        quiebres.append("        ignore pos @letra %s %s;" % (" ".join(atras), marcada))
        quiebres.append("        ignore pos %s %s %s;" % (" ".join(atras), marcada, despues))
        cuerpo = " ".join("%s' <%d %d %d 0>" % (s, dx, dy, av) for s, (dx, dy, av) in zip(entrada, vr))
        quiebres.append("        pos %s %s;" % (" ".join(atras), cuerpo))

    boca = secuencia("boca")
    boca_rules = [
        "        ignore sub @letra %s %s' %s;" % (boca[0], boca[1], " ".join(boca[2:])),
        "        ignore sub %s %s' %s @letra_sin_s;" % (boca[0], boca[1], " ".join(boca[2:])),
        "        sub %s %s' %s by asterisk;" % (boca[0], boca[1], " ".join(boca[2:])),
    ]

    ligaduras = []
    for nombre, texto in LIGADURAS.items():
        ligaduras.append("    sub %s by %s;" % (" ".join(nombre_glifo(ch) for ch in texto), nombre))

    return """languagesystem DFLT dflt;
languagesystem latn dflt;

%s

# La puntuación se vuelve ornamento: vasija, azulejo, nivel del agua.
feature liga {
%s
} liga;

feature calt {
    # Termina y empieza: cada vuelta pasa por el agua y el agua no repite.
    lookup ciclo {
%s
    } ciclo;
    # A la boca la taparon: en «boca», la o es el glifo-boca.
    lookup boca {
%s
    } boca;
} calt;

# Quiebres: algunas palabras no se dejan componer en la línea.
feature kern {
    lookup quiebres {
%s
    } quiebres;
} kern;
""" % ("\n".join(clases), "\n".join(ligaduras), "\n".join(ciclo), "\n".join(boca_rules),
       "\n".join(quiebres))


# --- Maestros y fuente variable ------------------------------------------------

def construir_maestro(loc, sembrados, items, fea):
    tabla, metricas, estructura = {}, {}, {}
    for nombre, (glifo, elementos, libre) in sembrados.items():
        contornos, partes = [], []
        for e in elementos:
            cs = contornos_elemento(e, loc, glifo)
            contornos.extend(cs)
            partes.append(len(cs))
        tabla[nombre] = glifo_tt(contornos)
        avance = libre if loc.get("GRID") else CELDA * ANCHO
        metricas[nombre] = [round(avance), 0]
        estructura[nombre] = partes

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(list(sembrados))
    fb.setupCharacterMap({cp: n for n, cp, e, c in items if cp is not None})
    fb.setupGlyf(tabla)
    for n, g in tabla.items():
        g.recalcBounds(fb.font["glyf"])
        metricas[n][1] = g.xMin if g.numberOfContours else 0
    fb.setupHorizontalMetrics({n: tuple(m) for n, m in metricas.items()})
    fb.setupHorizontalHeader(ascent=1000, descent=-380, lineGap=0)
    fb.setupNameTable({
        "copyright": "Prototipo 2026. Licencia por definir.",
        "familyName": FAMILIA,
        "styleName": "Regular",
        "uniqueFontIdentifier": "%s-%s" % (FAMILIA, VERSION),
        "fullName": FAMILIA,
        "version": "Version %s" % VERSION,
        "psName": FAMILIA + "-Regular",
        "designer": DISENO,
        "description": DESCRIPCION,
        "typographicFamily": FAMILIA,
        "typographicSubfamily": "Piedra",
    })
    fb.setupOS2(
        sTypoAscender=1000, sTypoDescender=-380, sTypoLineGap=0,
        usWinAscent=1100, usWinDescent=460,
        sxHeight=500, sCapHeight=700, usWeightClass=400, usWidthClass=7,
        fsSelection=0x40 | 0x80, achVendID="NONE", version=4,
        panose={"bFamilyType": 2, "bSerifStyle": 0, "bWeight": 6, "bProportion": 9,
                "bContrast": 0, "bStrokeVariation": 0, "bArmStyle": 0,
                "bLetterForm": 0, "bMidline": 0, "bXHeight": 0},
    )
    fb.setupPost(isFixedPitch=1, underlinePosition=-160, underlineThickness=60)
    fb.setupMaxp()
    addOpenTypeFeaturesFromString(fb.font, fea)
    return fb.font, estructura


def tag_a_nombre(tag):
    for t, en, es, mn, df, mx in EJES:
        if t == tag:
            return en
    raise KeyError(tag)


def construir_variable():
    items = repertorio()
    sembrados = construir_glifos(items)
    fea = codigo_fea(items)

    ds = DesignSpaceDocument()
    for tag, en, es, mn, df, mx in EJES:
        a = AxisDescriptor()
        a.tag, a.name, a.minimum, a.default, a.maximum = tag, en, mn, df, mx
        a.labelNames = {"en": en, "es": es}
        ds.addAxis(a)
    maestros = {}
    for i, loc in enumerate(MAESTROS):
        completo = {**DEFECTO, **loc}
        s = SourceDescriptor()
        s.name = "maestro%02d" % i
        s.location = {tag_a_nombre(t): v for t, v in completo.items()}
        s.font, estructura = construir_maestro(loc, sembrados, items, fea)
        maestros[tuple(sorted(completo.items()))] = s.font
        ds.addSource(s)
    for estilo, loc in INSTANCIAS:
        inst = InstanceDescriptor()
        inst.familyName = FAMILIA
        inst.styleName = estilo
        inst.location = {tag_a_nombre(t): v for t, v in {**DEFECTO, **loc}.items()}
        ds.addInstance(inst)

    vf, _, _ = varLib.build(ds, exclude=["MVAR"])
    buildStatTable(vf, [
        {"tag": tag, "name": en, "values": [
            {"value": df, "name": "Piedra", "flags": 0x2}]}
        for tag, en, es, mn, df, mx in EJES
    ])
    return vf, items, estructura


# --- Comprobaciones -------------------------------------------------------------

def a_path(pts):
    p = pathops.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    return p


def fuera(interior, exterior):
    """Área de interior que queda fuera de exterior."""
    if abs(area(interior)) < 1:
        return 0.0
    a = a_path(interior)
    b = a_path(exterior)
    try:
        d = pathops.op(a, b, pathops.PathOp.DIFFERENCE, fix_winding=True)
    except pathops.PathOpsError:
        return float("inf")
    return abs(d.area)


def comprobar(font, estructura, etiqueta):
    """Revisa cada elemento: sentido de los contornos, surco dentro de la placa,
    lomo dentro del surco. Devuelve la lista de problemas."""
    glyf = font["glyf"]
    problemas = []
    for nombre, partes in estructura.items():
        g = glyf[nombre]
        if g.numberOfContours <= 0:
            continue
        coords = list(g.coordinates)
        contornos, inicio = [], 0
        for fin in g.endPtsOfContours:
            contornos.append(coords[inicio:fin + 1])
            inicio = fin + 1
        i = 0
        for n in partes:
            grupo = contornos[i:i + n]
            i += n
            cuerpo = grupo[0]
            # Un elemento que ya desapareció puede quedar con un par de
            # unidades de área por el redondeo de los maestros: no se ve.
            if area(cuerpo) > 30:
                problemas.append((etiqueta, nombre, "cuerpo invertido"))
            if n == 3:
                hueco, isla = grupo[1], grupo[2]
                if area(hueco) < -1:
                    problemas.append((etiqueta, nombre, "surco invertido"))
                if area(isla) > 1:
                    problemas.append((etiqueta, nombre, "lomo invertido"))
                if fuera(hueco, cuerpo) > 4:
                    problemas.append((etiqueta, nombre, "surco fuera de la placa"))
                if abs(area(isla)) >= 1 and fuera(isla, hueco) > 4:
                    problemas.append((etiqueta, nombre, "lomo fuera del surco"))
    return problemas


def limpiar_degenerados(font):
    """En una instancia estática, borra los contornos sin área."""
    glyf = font["glyf"]
    for nombre in font.getGlyphOrder():
        g = glyf[nombre]
        if g.numberOfContours <= 0:
            continue
        coords = list(g.coordinates)
        inicio, nuevos, fines, flags = 0, [], [], []
        for fin in g.endPtsOfContours:
            c = coords[inicio:fin + 1]
            if abs(area(c)) > 2:
                nuevos.extend(c)
                flags.extend(g.flags[inicio:fin + 1])
                fines.append(len(nuevos) - 1)
            inicio = fin + 1
        g.coordinates = GlyphCoordinates(nuevos)
        g.endPtsOfContours = fines
        g.flags = bytearray(flags)
        g.numberOfContours = len(fines)
        if fines:
            g.flags[0] |= 0x40
        g.recalcBounds(glyf)


def exportar_estaticas(vf):
    carpeta = os.path.join(AQUI, "estaticas")
    os.makedirs(carpeta, exist_ok=True)
    for estilo, loc in INSTANCIAS:
        f = instancer.instantiateVariableFont(vf, {**DEFECTO, **loc}, inplace=False)
        limpiar_degenerados(f)
        sufijo = "".join(p[:1].upper() + p[1:] for p in estilo.split())
        sufijo = sufijo.replace("ó", "o").replace("í", "i")
        nombre = f["name"]
        for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
            nombre.setName("%s %s" % (FAMILIA, estilo), 1, pid, eid, lid)
            nombre.setName("Regular", 2, pid, eid, lid)
            nombre.setName("%s %s" % (FAMILIA, estilo), 4, pid, eid, lid)
            nombre.setName("%s-%s" % (FAMILIA, sufijo), 6, pid, eid, lid)
            nombre.setName(FAMILIA, 16, pid, eid, lid)
            nombre.setName(estilo, 17, pid, eid, lid)
        f.save(os.path.join(carpeta, "%s-%s.ttf" % (FAMILIA, sufijo)))


def main(argv):
    vf, items, estructura = construir_variable()
    ruta = os.path.join(AQUI, FAMILIA + "-Variable.ttf")
    vf.save(ruta)
    vf = TTFont(ruta)
    vf.flavor = "woff2"
    vf.save(os.path.join(AQUI, FAMILIA + "-Variable.woff2"))
    exportar_estaticas(TTFont(ruta))
    print("%d caracteres y %d ligaduras, %d glifos, %d maestros" % (
        sum(1 for n, cp, e, c in items if cp is not None), len(LIGADURAS),
        len(TTFont(ruta).getGlyphOrder()), len(MAESTROS)))
    for archivo in sorted(os.listdir(AQUI)):
        if archivo.startswith(FAMILIA):
            print("  %-28s %7.1f KB" % (archivo, os.path.getsize(os.path.join(AQUI, archivo)) / 1024))
    if "--comprobar" in argv:
        muestras = []
        for e in (0, 25, 50, 75, 100):
            for r in (0, 25, 50, 75, 100):
                for o in (0, 100):
                    for g in (0, 100):
                        muestras.append({"EROD": e, "REFL": r, "ONDA": o, "GRID": g})
        total = []
        fuente = TTFont(ruta)
        for loc in muestras:
            inst = instancer.instantiateVariableFont(fuente, loc, inplace=False)
            total += comprobar(inst, estructura, "E%(EROD)d R%(REFL)d O%(ONDA)d G%(GRID)d" % loc)
        print("%d combinaciones revisadas, %d problemas" % (len(muestras), len(total)))
        for p in total[:40]:
            print("  ", p)


if __name__ == "__main__":
    main(sys.argv[1:])
