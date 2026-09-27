"""Genera la fuente variable Contenedor a partir de sus reglas.

La fuente no se dibuja letra por letra: se deduce. Cada glifo es una
distribución de placas sobre la retícula de azulejos (glifos.py) y este
programa aplica las reglas del sistema a esa distribución:

1. La celda es el contenedor. Todas las letras miden lo mismo (monoespaciada):
   la i deja vacía casi toda su celda, como la piscina.
2. Entre placa y placa queda piel. Por eso ninguna contraforma se cierra:
   ningún contenedor aguanta lo que contiene.
3. La topología decide la forma. Una placa con un solo vecino es un terminal
   y se desprende primero cuando la letra tiembla; una placa donde se
   cruzan tres trazos es una articulación y se achica, como una trampa de
   tinta (la tierra se da de beber a sí misma).
4. Todo punto es un pez: los puntos, las tildes y la diéresis son azulejos
   desprendidos, girados 45°.
5. Cada letra tiene cuatro vueltas (alternativas). La función calt las
   encadena para que la misma letra dos veces no salga igual.
6. Las bandas (ss01 boca, ss02 ojos) y el agua devuelta (ss03) son marcas
   de ancho cero que se dibujan sobre la celda de la letra. El agua de cada
   letra se calcula en vasos.py y se pinta en verde (COLR) donde el programa
   sabe de color.

Ejes:

    wdth  Ancho    60 Monolito ... 100 ... 150 Piscina
    wght  Peso    100 Piel     ... 400 ... 900 Piedra
    AGUA  Agua      0 seca     ...         100 el agua deforma la imagen
    VASO  Vaso      0 placa llena ...      100 cada placa es un contenedor
    TEMB  Temblor   0 quieta   ...         100 se mueve como la piedra

Uso:  python3 generar_fuente.py
Salida: Contenedor-Variable.ttf y .woff2, y las instancias estáticas en
estaticas/.
"""

import math
import os
import random
import sys

from fontTools import varLib
from fontTools.agl import UV2AGL
from fontTools.colorLib.builder import buildCOLR, buildCPAL
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      InstanceDescriptor, SourceDescriptor)
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.otlLib.builder import buildStatTable
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.varLib import instancer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glifos  # noqa: E402
import vasos  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))

FAMILIA = "Contenedor"
VERSION = "0.100"
DISENO = "Joaquin Max Cuevas Ventura"
DESCRIPCION = ("Tipografía estructural derivada de «Contener una ruina: acciones "
               "para desenterrar una voz», de Rebeca Paz con CreaciónxAcuerpamiento "
               "(La Paz, 22 de agosto de 2026), y del poema que la acompaña. "
               "Prototipo generado por reglas.")

# --- Retícula ---------------------------------------------------------------
UPM = 1000
AZULEJO = 100          # alto del azulejo; también el ancho con wdth = 100
CELDA = 6              # la celda mide seis azulejos: cinco de letra y uno de aire
VUELTAS = 4            # alternativas por glifo: termina y empieza

# --- Reglas de las placas ---------------------------------------------------
PIEL = [(100, 46), (400, 20), (900, 3)]   # separación entre placas según el peso
ARTICULACION = 0.80    # tamaño relativo de la placa donde se cruzan tres trazos
PEZ = 1.20             # semidiagonal del pez, relativa a la semiplaca
VASO = 0.52            # tamaño del hueco de la placa con VASO = 100
MANO = 0.20            # irregularidad de cada esquina, relativa a la semiplaca: el repujado
GIRO_MANO = 3.2        # giro de cada placa hecho a mano (grados)
COLOCACION = 3         # la placa no cae justo en su azulejo (unidades)
ONDA = 0.30            # amplitud del agua, en azulejos
LONGITUD_ONDA = 4.2    # longitud de la onda, en azulejos
TEMBLOR = 0.09         # desplazamiento máximo de una placa (azulejos)
GIRO_TEMBLOR = 6       # giro máximo de una placa al temblar (grados)
DESPRENDE = 0.28       # cuánto se aleja un terminal (azulejos)
GIRO_DESPRENDE = (12, 24)

# Bandas del mismo material sobre la boca y los ojos (ss01, ss02)
BANDA_BOCA = (-25, 215)
BANDA_OJOS = (285, 525)

# Agua devuelta (ss03): dos líneas por azulejo, en el verde del dibujo
LINEAS_DE_AGUA = (0.25, 0.75)
GROSOR_DE_AGUA = 8
VERDE = (0x4C / 255, 0x8C / 255, 0x3A / 255, 1.0)

EJES = [
    # etiqueta, nombre, nombre en castellano, mínimo, defecto, máximo
    ("wdth", "Width", "Ancho", 60, 100, 150),
    ("wght", "Weight", "Peso", 100, 400, 900),
    ("AGUA", "Water", "Agua", 0, 0, 100),
    ("VASO", "Vessel", "Vaso", 0, 0, 100),
    ("TEMB", "Tremor", "Temblor", 0, 0, 100),
]

DEFECTO = {e[0]: e[4] for e in EJES}

# Maestros: el de defecto, los extremos de cada eje y las esquinas donde dos
# ejes se multiplican (el hueco del vaso depende del tamaño de la placa; la
# onda, del ancho del azulejo).
MAESTROS = [
    {},
    {"wdth": 60}, {"wdth": 150},
    {"wght": 100}, {"wght": 900},
    {"VASO": 100}, {"VASO": 100, "wdth": 60}, {"VASO": 100, "wdth": 150},
    {"VASO": 100, "wght": 100}, {"VASO": 100, "wght": 900},
    {"AGUA": 100}, {"AGUA": 100, "wdth": 60}, {"AGUA": 100, "wdth": 150},
    {"TEMB": 100}, {"TEMB": 100, "VASO": 100},
]

INSTANCIAS = [
    ("Seca", {}),
    ("Piel", {"wght": 100}),
    ("Piedra", {"wght": 900}),
    ("Monolito", {"wdth": 60}),
    ("Piscina", {"wdth": 150}),
    ("Agua", {"AGUA": 100}),
    ("Vaso", {"VASO": 100}),
    ("Temblor", {"TEMB": 100}),
    ("Presente continuo", {"TEMB": 55, "AGUA": 35}),
    ("Ruina", {"wght": 900, "VASO": 60, "TEMB": 100}),
]


# --- Utilidades ---------------------------------------------------------------

def tramo(x, puntos):
    """Interpolación lineal por tramos."""
    for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
        if x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return puntos[-1][1]


def nombre_glifo(ch):
    cp = ord(ch)
    if cp == 0x20:
        return "space"
    return UV2AGL.get(cp, "uni%04X" % cp)


def parametros(loc):
    loc = {**DEFECTO, **loc}
    return {
        "tw": AZULEJO * loc["wdth"] / 100.0,
        "th": float(AZULEJO),
        "piel": tramo(loc["wght"], PIEL),
        "agua": loc["AGUA"] / 100.0,
        "vaso": loc["VASO"] / 100.0,
        "temb": loc["TEMB"] / 100.0,
    }


# --- Topología: de la retícula a los elementos ----------------------------------

def elementos_de_reticula(filas):
    """Convierte la retícula en elementos con su papel en la letra."""
    placas = {}
    peces = []
    for fila, texto in filas.items():
        seis = len(texto) == 6
        for col, c in enumerate(texto):
            x = col + (0.5 if seis else 1.0)
            if c == "#":
                placas[(col, fila)] = x
            elif c == "*":
                peces.append({"tipo": "pez", "x": x, "y": fila + 0.5, "escala": 1.0})

    elementos = []
    for (col, fila), x in sorted(placas.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
        vecinos8 = [(dc, df) for dc in (-1, 0, 1) for df in (-1, 0, 1)
                    if (dc or df) and (col + dc, fila + df) in placas]
        vecinos4 = [v for v in vecinos8 if 0 in v]
        e = {"tipo": "placa", "x": x, "y": fila + 0.5, "escala": 1.0,
             "terminal": None, "articulacion": len(vecinos4) >= 3}
        if len(vecinos8) == 1:
            dc, df = vecinos8[0]
            n = math.hypot(dc, df)
            e["terminal"] = (-dc / n, -df / n)   # se aleja de su vecino
        elif not vecinos8:
            e["terminal"] = (0.0, 1.0)
        elementos.append(e)
    return elementos + peces


def elementos_de_acento(nombre, mayuscula):
    sube = 2.0 if mayuscula else 0.0
    return [{"tipo": "pez", "x": x + 1.0, "y": f + sube + 0.5, "escala": s}
            for x, f, s in glifos.ACENTOS[nombre]]


def elementos_de_ornamento(nombre):
    cx, cy = 3.0, 3.5
    if nombre == "pez":
        return [{"tipo": "pez", "x": cx, "y": cy, "escala": 5.6}]
    if nombre == "placa":
        return [{"tipo": "marco", "x": cx, "y": cy, "escala": 6.0, "hueco": 0.72},
                {"tipo": "pez", "x": cx, "y": cy, "escala": 2.4}]
    if nombre == "disco":
        anillo = []
        for k in range(12):
            a = 2 * math.pi * k / 12
            anillo.append({"tipo": "placa", "x": cx + 2.55 * math.cos(a),
                           "y": cy + 2.55 * math.sin(a), "escala": 0.7,
                           "giro": math.degrees(a), "terminal": None,
                           "articulacion": False})
        return anillo + [{"tipo": "pez", "x": cx, "y": cy, "escala": 1.5}]
    raise KeyError(nombre)


def elementos_notdef():
    """El glifo de lo que falta: una piscina vacía, con las esquinas rectas."""
    filas = {6: "#####", 0: "#####"}
    for f in range(1, 6):
        filas[f] = "#...#"
    elementos = elementos_de_reticula(filas)
    for e in elementos:
        e["terminal"] = None
        e["articulacion"] = False
    return elementos


# --- Azar reproducible: la mano y el temblor de cada vuelta ---------------------

def sembrar(elementos, semilla):
    rng = random.Random(semilla)
    fase = rng.uniform(0, 2 * math.pi)
    sembrados = []
    for e in elementos:
        e = dict(e)
        e["mano"] = [(rng.uniform(-MANO, MANO), rng.uniform(-MANO, MANO)) for _ in range(4)]
        e["giro_mano"] = rng.uniform(-GIRO_MANO, GIRO_MANO)
        e["colocacion"] = (rng.uniform(-COLOCACION, COLOCACION),
                           rng.uniform(-COLOCACION, COLOCACION))
        if e.get("terminal"):
            ux, uy = e["terminal"]
            lado = rng.uniform(-0.05, 0.05)
            e["temblor"] = (DESPRENDE * ux - lado * uy, DESPRENDE * uy + lado * ux)
            e["giro_temblor"] = rng.choice((-1, 1)) * rng.uniform(*GIRO_DESPRENDE)
        else:
            e["temblor"] = (rng.uniform(-TEMBLOR, TEMBLOR), rng.uniform(-TEMBLOR, TEMBLOR))
            e["giro_temblor"] = rng.uniform(-GIRO_TEMBLOR, GIRO_TEMBLOR)
        e["fase"] = fase
        sembrados.append(e)
    return sembrados


# --- Geometría: de los elementos a los contornos, en un maestro ----------------

def girar(pts, grados):
    a = math.radians(grados)
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c) for x, y in pts]


def contornos(elementos, p):
    tw, th, piel = p["tw"], p["th"], p["piel"]
    salida = []
    for e in elementos:
        cx = e["x"] * tw + e["colocacion"][0]
        cy = e["y"] * th + e["colocacion"][1]
        cx += p["agua"] * ONDA * tw * math.sin(2 * math.pi * e["y"] / LONGITUD_ONDA + e["fase"])
        cx += p["temb"] * e["temblor"][0] * AZULEJO
        cy += p["temb"] * e["temblor"][1] * AZULEJO

        k = e["escala"] * (ARTICULACION if e.get("articulacion") else 1.0)
        hx = k * (tw - piel) / 2
        hy = k * (th - piel) / 2
        if e["tipo"] == "pez":
            hx, hy = PEZ * hx, PEZ * hy
            local = [(0, hy), (hx, 0), (0, -hy), (-hx, 0)]
        else:
            local = [(-hx, hy), (hx, hy), (hx, -hy), (-hx, -hy)]
        local = [(x + jx * hx, y + jy * hy) for (x, y), (jx, jy) in zip(local, e["mano"])]
        local = girar(local, e.get("giro", 0.0) + e["giro_mano"] + p["temb"] * e["giro_temblor"])

        exterior = [(cx + x, cy + y) for x, y in local]
        if e["tipo"] == "marco":
            r = e["hueco"]
        else:
            r = p["vaso"] * VASO
        interior = [(cx + r * x, cy + r * y) for x, y in reversed(local)]
        salida.append(exterior)
        salida.append(interior)
    return salida


def glifo_tt(lista_contornos):
    g = Glyph()
    if not lista_contornos:
        g.numberOfContours = 0
        return g
    puntos, fines = [], []
    for c in lista_contornos:
        puntos.extend((round(x), round(y)) for x, y in c)
        fines.append(len(puntos) - 1)
    g.numberOfContours = len(lista_contornos)
    g.coordinates = GlyphCoordinates(puntos)
    g.endPtsOfContours = fines
    g.flags = bytearray([1] * len(puntos))
    g.flags[0] |= 0x40   # OVERLAP_SIMPLE: las placas pueden superponerse
    g.program = ttProgram.Program()
    g.program.fromBytecode(b"")
    return g


# --- El repertorio -----------------------------------------------------------

def repertorio():
    """Lista de (nombre, código, elementos) y, aparte, el agua de cada glifo.

    El agua es la del glifo base: la tilde de la ú no cambia lo que la u
    retiene.
    """
    reticula = glifos.todos()
    items, agua = [], {}
    for ch, filas in reticula.items():
        items.append((nombre_glifo(ch), ord(ch), elementos_de_reticula(filas)))
        if vasos.celdas_con_agua(filas):
            agua[nombre_glifo(ch)] = nombre_glifo(ch)
    for ch, (base, acento) in glifos.COMPUESTOS.items():
        mayuscula = base.isupper()
        elementos = elementos_de_reticula(reticula[base]) + elementos_de_acento(acento, mayuscula)
        items.append((nombre_glifo(ch), ord(ch), elementos))
        if nombre_glifo(base) in agua:
            agua[nombre_glifo(ch)] = nombre_glifo(base)
    for ch, orn in glifos.ORNAMENTOS.items():
        items.append((nombre_glifo(ch), ord(ch), elementos_de_ornamento(orn)))
    return items, agua


# --- El agua devuelta (ss03) ----------------------------------------------------

def tramos_de_agua(filas):
    """Tramos horizontales de agua: (fila, primera columna, última columna, seis)."""
    celdas = vasos.celdas_con_agua(filas)
    seis = max(len(t) for t in filas.values()) == 6
    tramos = []
    for f in sorted({f for c, f in celdas}, reverse=True):
        cols = sorted(c for c, ff in celdas if ff == f)
        inicio = previo = cols[0]
        for c in cols[1:] + [None]:
            if c is None or c != previo + 1:
                tramos.append((f, inicio, previo, seis))
                if c is not None:
                    inicio = c
            if c is not None:
                previo = c
    return tramos


def contornos_agua(tramos, p):
    """El agua se dibuja como en un corte de arquitectura: líneas horizontales.

    Cada línea toca las placas de los dos lados (el acento toca su borde).
    """
    tw, th, piel = p["tw"], p["th"], p["piel"]
    salida = []
    for f, c0, c1, seis in tramos:
        corrimiento = 0.5 if seis else 1.0
        x0 = (c0 + corrimiento - 0.5) * tw - piel / 2
        x1 = (c1 + corrimiento + 0.5) * tw + piel / 2
        for fr in LINEAS_DE_AGUA:
            y = (f + fr) * th
            dx = p["agua"] * ONDA * tw * math.sin(2 * math.pi * (f + fr) / LONGITUD_ONDA)
            g = GROSOR_DE_AGUA / 2
            salida.append([(x0 + dx, y + g), (x1 + dx, y + g), (x1 + dx, y - g), (x0 + dx, y - g)])
    return salida


def construir_glifos(items):
    """Siembra las cuatro vueltas de cada glifo."""
    glifos_sembrados = {".notdef": sembrar(elementos_notdef(), ".notdef")}
    for nombre, cp, elementos in items:
        for v in range(VUELTAS):
            n = nombre if v == 0 else "%s.v%d" % (nombre, v)
            glifos_sembrados[n] = sembrar(elementos, "%s|%d" % (nombre, v))
    return glifos_sembrados


# --- Funciones OpenType -------------------------------------------------------

def codigo_fea(items, agua):
    base = [n for n, cp, e in items]
    clases = ["@V0 = [%s];" % " ".join(base)]
    for v in range(1, VUELTAS):
        clases.append("@V%d = [%s];" % (v, " ".join("%s.v%d" % (n, v) for n in base)))

    # El salto de una vuelta a la siguiente depende de la letra anterior:
    # así una diferencia en el texto se propaga y dos palabras iguales rara
    # vez caen en las mismas vueltas.
    salto = {n: (cp % 3) + 1 for n, cp, e in items}
    grupos = {}
    for n in base:
        for v in range(VUELTAS):
            nv = n if v == 0 else "%s.v%d" % (n, v)
            grupos.setdefault((v, salto[n]), []).append(nv)
    reglas = []
    for (v, h), miembros in sorted(grupos.items()):
        clases.append("@P%d_%d = [%s];" % (v, h, " ".join(miembros)))
        destino = (v + h) % VUELTAS
        if destino:
            reglas.append("    sub @P%d_%d @V0' by @V%d;" % (v, h, destino))

    todos = [n for n in base] + ["%s.v%d" % (n, v) for n in base for v in range(1, VUELTAS)]
    boca = "\n".join("    sub %s by %s banda.boca;" % (n, n) for n in todos)
    ojos = "\n".join("    sub %s by %s banda.ojos;" % (n, n) for n in todos)
    devuelta = "\n".join(
        "    sub %s by %s agua.%s;" % (nv, nv, agua[n])
        for n in base if n in agua
        for nv in [n] + ["%s.v%d" % (n, v) for v in range(1, VUELTAS)])
    marcas = ["banda.boca", "banda.ojos"] + ["agua." + n for n in sorted(set(agua.values()))]
    return """languagesystem DFLT dflt;
languagesystem latn dflt;

%s

table GDEF {
    GlyphClassDef [%s], , [%s], ;
} GDEF;

# Termina y empieza: cada vuelta pasa por el agua y el agua no repite.
feature calt {
    lookup ciclo {
        lookupflag IgnoreMarks;
%s
    } ciclo;
} calt;

# A la boca la taparon.
feature ss01 {
    featureNames { name "Boca tapada"; };
%s
} ss01;

# Y a los ojos.
feature ss02 {
    featureNames { name "Ojos tapados"; };
%s
} ss02;

# A la piscina le devolvieron su agua: cada letra retiene la que puede.
feature ss03 {
    featureNames { name "Agua devuelta"; };
%s
} ss03;
""" % ("\n".join(clases), " ".join(todos), " ".join(marcas), "\n".join(reglas),
       boca, ojos, devuelta)


# --- Maestros y fuente variable ------------------------------------------------

def construir_maestro(loc, glifos_sembrados, items, agua, fea):
    p = parametros(loc)
    ancho = round(CELDA * p["tw"])
    reticula = {nombre_glifo(ch): filas for ch, filas in glifos.todos().items()}
    aguas = sorted(set(agua.values()))
    orden = (list(glifos_sembrados) + ["banda.boca", "banda.ojos"]
             + ["agua." + n for n in aguas] + ["agua.%s.capa" % n for n in aguas])

    tabla_glifos, metricas = {}, {}
    for nombre, elementos in glifos_sembrados.items():
        tabla_glifos[nombre] = glifo_tt(contornos(elementos, p))
        metricas[nombre] = (ancho, 0)
    for nombre, (y0, y1) in (("banda.boca", BANDA_BOCA), ("banda.ojos", BANDA_OJOS)):
        rect = [(-ancho - 2, y1), (2, y1), (2, y0), (-ancho - 2, y0)]
        tabla_glifos[nombre] = glifo_tt([rect])
        metricas[nombre] = (0, 0)
    # El agua es una marca de ancho cero que se dibuja hacia atrás, sobre la
    # celda de la letra que la retiene.
    for n in aguas:
        lineas = [[(x - ancho, y) for x, y in c]
                  for c in contornos_agua(tramos_de_agua(reticula[n]), p)]
        for nombre in ("agua." + n, "agua.%s.capa" % n):
            tabla_glifos[nombre] = glifo_tt(lineas)
            metricas[nombre] = (0, 0)

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(orden)
    fb.setupCharacterMap({cp: n for n, cp, e in items})
    fb.setupGlyf(tabla_glifos)
    for n, g in tabla_glifos.items():
        g.recalcBounds(fb.font["glyf"])
        izquierda = g.xMin if g.numberOfContours else 0
        metricas[n] = (metricas[n][0], izquierda)
    fb.setupHorizontalMetrics(metricas)
    fb.setupHorizontalHeader(ascent=900, descent=-250, lineGap=0)
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
        "typographicSubfamily": "Seca",
    })
    fb.setupOS2(
        sTypoAscender=900, sTypoDescender=-250, sTypoLineGap=0,
        usWinAscent=1000, usWinDescent=330,
        sxHeight=500, sCapHeight=700, usWeightClass=400, usWidthClass=5,
        fsSelection=0x40 | 0x80, achVendID="NONE", version=4,
        panose={"bFamilyType": 2, "bSerifStyle": 0, "bWeight": 5, "bProportion": 9,
                "bContrast": 0, "bStrokeVariation": 0, "bArmStyle": 0,
                "bLetterForm": 0, "bMidline": 0, "bXHeight": 0},
    )
    fb.setupPost(isFixedPitch=1, underlinePosition=-150, underlineThickness=60)
    fb.setupMaxp()
    addOpenTypeFeaturesFromString(fb.font, fea)
    # Donde el programa sabe de color, el agua vuelve verde, como en el dibujo.
    # Donde no, se ve del color del texto.
    fb.font["COLR"] = buildCOLR({"agua." + n: [("agua.%s.capa" % n, 0)] for n in aguas},
                                version=0)
    fb.font["CPAL"] = buildCPAL([[VERDE]])
    return fb.font


def construir_variable():
    glifos.validar()
    items, agua = repertorio()
    sembrados = construir_glifos(items)
    fea = codigo_fea(items, agua)

    ds = DesignSpaceDocument()
    for tag, en, es, mn, df, mx in EJES:
        a = AxisDescriptor()
        a.tag, a.name, a.minimum, a.default, a.maximum = tag, en, mn, df, mx
        a.labelNames = {"en": en, "es": es}
        ds.addAxis(a)

    for i, loc in enumerate(MAESTROS):
        completo = {**DEFECTO, **loc}
        s = SourceDescriptor()
        s.name = "maestro%02d" % i
        s.location = {tag_a_nombre(t): v for t, v in completo.items()}
        s.font = construir_maestro(loc, sembrados, items, agua, fea)
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
            {"value": df, "name": "Seca" if tag != "wdth" else "Normal", "flags": 0x2}]}
        for tag, en, es, mn, df, mx in EJES
    ])
    return vf, items


def tag_a_nombre(tag):
    for t, en, es, mn, df, mx in EJES:
        if t == tag:
            return en
    raise KeyError(tag)


def limpiar_degenerados(font):
    """En una instancia estática, borra los huecos que no se abrieron."""
    glyf = font["glyf"]
    for nombre in font.getGlyphOrder():
        g = glyf[nombre]
        if g.numberOfContours <= 0:
            continue
        coords = list(g.coordinates)
        inicio, nuevos, fines, flags = 0, [], [], []
        for fin in g.endPtsOfContours:
            c = coords[inicio:fin + 1]
            area = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(c, c[1:] + c[:1]))
            if abs(area) > 2:
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
        nombre = f["name"]
        for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
            nombre.setName("%s %s" % (FAMILIA, estilo), 1, pid, eid, lid)
            nombre.setName("Regular", 2, pid, eid, lid)
            nombre.setName("%s %s" % (FAMILIA, estilo), 4, pid, eid, lid)
            nombre.setName("%s-%s" % (FAMILIA, sufijo), 6, pid, eid, lid)
            nombre.setName(FAMILIA, 16, pid, eid, lid)
            nombre.setName(estilo, 17, pid, eid, lid)
        f.save(os.path.join(carpeta, "%s-%s.ttf" % (FAMILIA, sufijo)))


def main():
    vf, items = construir_variable()
    ruta = os.path.join(AQUI, FAMILIA + "-Variable.ttf")
    vf.save(ruta)
    vf = TTFont(ruta)
    vf.flavor = "woff2"
    vf.save(os.path.join(AQUI, FAMILIA + "-Variable.woff2"))
    exportar_estaticas(TTFont(ruta))
    print("%d caracteres, %d glifos, %d maestros" % (
        len(items), len(TTFont(ruta).getGlyphOrder()), len(MAESTROS)))
    for archivo in sorted(os.listdir(AQUI)):
        if archivo.startswith(FAMILIA):
            print("  %-32s %7.1f KB" % (archivo, os.path.getsize(os.path.join(AQUI, archivo)) / 1024))


if __name__ == "__main__":
    main()
