"""Piezas en diagrama para recomponer las pruebas 3, 4 y 5 de Chhaxwa.

El 27 de noviembre el autor eligió dos formas (E1 y E2) recomponiendo las maquetas de forma, y pidió más opciones en
diagrama para recomponer las otras tres pruebas. Cada pieza es un modelo de masas, blanco y con contornos
(Freestyle), en metros reales, con una figura de 1,65 m. Se corre desde la raíz del repositorio:
    venv_bpy/bin/python chhaxwa/blender/piezas.py            # todas, en chhaxwa/renders/piezas/
    venv_bpy/bin/python chhaxwa/blender/piezas.py 3a 4c      # algunas
Son diagramas, no proyectos: las medidas son del proyecto y se ajustan al recomponer. Después, con el Python del
sistema, aligerar_piezas.py pasa los PNG a una paleta de 64 colores.
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import bpy                       # noqa: E402  (bpy primero: registra bmesh)
import bmesh                     # noqa: E402
from mathutils import Vector     # noqa: E402

import comun as C                # noqa: E402

D = {}


def mats():
    D["piedra"] = C.mat_liso("d_piedra", (0.50, 0.50, 0.49), 0.9)
    D["tierra"] = C.mat_liso("d_tierra", (0.70, 0.64, 0.56), 0.9)
    D["paja"] = C.mat_liso("d_paja", (0.80, 0.74, 0.55), 0.9)
    D["madera"] = C.mat_liso("d_madera", (0.45, 0.34, 0.24), 0.8)
    D["blanco"] = C.mat_liso("d_blanco", (0.86, 0.86, 0.85), 0.9)
    D["sol"] = C.mat_liso("d_sol", (0.75, 0.22, 0.12), 0.6)
    D["humo"] = C.mat_liso("d_humo", (0.62, 0.62, 0.64), 0.9)


def figura(pos, giro=0.0, pose="pie"):
    C.figura_madera(pos, D["blanco"], alto=1.65, giro=giro, pose=pose)


def restar(base, cortador):
    md = base.modifiers.new("resta", 'BOOLEAN')
    md.object = cortador
    md.operation = 'DIFFERENCE'
    cortador.hide_render = True


def palos(radio, n, z0, z1, fase=0.0):
    for i in range(n):
        a = 2 * math.pi * i / n + fase
        C.palo((radio * math.cos(a), radio * math.sin(a), z0), (radio * math.cos(a), radio * math.sin(a), z1), 0.06,
               D["madera"])


def prisma(p0, p1, ancho, alto, z, mat, nombre="prisma"):
    """Un prisma triangular (techo a dos aguas) entre dos puntos de la cumbrera, en planta."""
    bm = bmesh.new()
    (x0, y0), (x1, y1) = p0, p1
    vs = []
    for (x, y) in ((x0, y0), (x1, y1)):
        vs.append([bm.verts.new((x - ancho / 2, y, z)), bm.verts.new((x + ancho / 2, y, z)), bm.verts.new((x, y, z + alto))])
    a, b = vs
    for i in range(3):
        j = (i + 1) % 3
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new((a[0], a[2], a[1])); bm.faces.new((b[0], b[1], b[2]))
    bm.normal_update()
    return C.objeto(nombre, C.malla_de_bm(bm, nombre, mat, suave=False))


def hiladas_voladas(cx, y0, y1, z0, abertura, n, alto=0.12, vuelo=0.1, mat=None):
    """Las hiladas que vuelan hacia el centro de una abertura, entre y0 e y1 (espesor del muro)."""
    for i in range(n):
        v = (i + 1) * vuelo
        for lado in (-1, 1):
            x = cx + lado * (abertura / 2 - v / 2)
            C.caja((x, (y0 + y1) / 2, z0 + i * alto + alto / 2), (v, y1 - y0, alto), mat or D["piedra"], "volada")


# ----------------------------------------------------------------------------------------------------------------
# Prueba 3. Pasos y celdas voladas
# ----------------------------------------------------------------------------------------------------------------

def p3a():
    """Paso volado en un muro."""
    for x0, x1 in ((-2.2, -0.3), (0.3, 2.2)):
        C.caja(((x0 + x1) / 2, 0, 0.8), (x1 - x0, 0.6, 1.6), D["piedra"], "muro")
    hiladas_voladas(0, -0.3, 0.3, 0.6, 0.6, 3)
    C.caja((0, 0, 1.28), (0.6, 0.6, 0.64), D["piedra"], "muro")
    figura((0.9, -1.0, 0), giro=1.6, pose="rodillas")


def p3b():
    """Corredor volado: el paso se alarga y se recorre de rodillas."""
    for x in (-0.6, 0.6):
        C.caja((x, 0, 0.6), (0.6, 4.0, 1.2), D["piedra"], "muro")
    for i in range(3):
        for lado in (-1, 1):
            C.caja((lado * (0.3 - 0.05 - i * 0.1) + lado * 0.0, 0, 0.6 + i * 0.12 + 0.06), (0.1 * (i + 1) + 0.6 * 0, 4.0, 0.12),
                   D["piedra"], "volada")
    C.caja((0, 0, 1.0), (1.8, 4.0, 0.12), D["piedra"], "cierre")
    figura((0.0, -2.8, 0), giro=math.pi / 2, pose="rodillas")


def p3c():
    """Paso hundido: se baja por una zanja hasta un paso volado."""
    suelo = C.caja((0, 0, -0.3), (6.0, 6.0, 0.6), D["tierra"], "suelo")
    zanja = C.caja((0, -1.5, -0.3), (0.8, 3.2, 0.8), D["tierra"], "zanja")
    restar(suelo, zanja)
    for x0, x1 in ((-3.0, -0.4), (0.4, 3.0)):
        C.caja(((x0 + x1) / 2, 0.3, 0.6), (x1 - x0, 0.6, 1.2), D["piedra"], "lindero")
    C.caja((0, 0.3, -0.2), (0.8, 0.6, 0.2), D["piedra"], "umbral")
    hiladas_voladas(0, 0.0, 0.6, 0.2, 0.8, 3)
    C.caja((0, 0.3, 0.9), (0.8, 0.6, 0.6), D["piedra"], "lindero")
    figura((0, -2.3, -0.6), giro=0.0)


def p3d():
    """Celda volada de planta cuadrada, con óculo."""
    h = 0.24
    for i in range(16):
        z = i * h
        fuera = 2.0 - z * 0.2
        dentro = max(0.2, 1.4 - max(0, z - 1.1) * 0.6)
        if fuera - dentro < 0.15:
            break
        e = fuera - dentro
        for (cx, cy, dx, dy) in ((0, fuera - e / 2, 2 * fuera, e), (0, -(fuera - e / 2), 2 * fuera, e),
                                 (fuera - e / 2, 0, e, 2 * dentro), (-(fuera - e / 2), 0, e, 2 * dentro)):
            if cy < 0 and dy == e and z < 0.96:
                for sx in (-1, 1):
                    C.caja((sx * (fuera + 0.35) / 2, cy, z + h / 2), (fuera - 0.35, dy, h), D["tierra"], "hilada")
                continue
            C.caja((cx, cy, z + h / 2), (dx, dy, h), D["tierra"], "hilada")
    figura((1.2, -2.8, 0), giro=0.4)


def p3e():
    """Celda volada redonda, con óculo."""
    h = 0.24
    for i in range(16):
        z = i * h
        fuera = 2.0 - z * 0.18
        dentro = max(0.2, 1.45 - max(0, z - 1.1) * 0.55)
        if fuera - dentro < 0.15:
            break
        n = 28
        for j in range(n):
            a = 2 * math.pi * j / n
            if abs(((a - 1.5 * math.pi) + math.pi) % (2 * math.pi) - math.pi) < 0.22 and z < 0.96:
                continue
            r = (fuera + dentro) / 2
            C.caja((r * math.cos(a), r * math.sin(a), z + h / 2), (fuera - dentro, 2 * math.pi * r / n * 1.02, h),
                   D["tierra"], "hilada", rot=(0, 0, a))
    figura((1.2, -2.9, 0), giro=0.4)


def p3f():
    """Paso a través de un montón."""
    m = C.tronco((0, 0, 0), 3.0, 0.3, 2.2, D["piedra"], lados=48)
    t = C.caja((0, 0, 0.48), (0.7, 7.0, 0.96), D["piedra"], "tunel")
    restar(m, t)
    figura((0.4, -3.6, 0), giro=0.0, pose="rodillas")


# ----------------------------------------------------------------------------------------------------------------
# Prueba 4. Techos de p'ira e ichu
# ----------------------------------------------------------------------------------------------------------------

def p4a():
    """Dos aguas de fajas sobre pares, sin muros."""
    for (x, y) in ((-1.5, -2.5), (1.5, -2.5), (1.5, 2.5), (-1.5, 2.5)):
        C.palo((x, y, 0), (x, y, 1.8), 0.07, D["madera"])
    prisma((0, -2.9), (0, 2.9), 3.8, 1.8, 1.8, D["paja"])
    figura((2.6, -2.0, 0), giro=2.4)


def p4b():
    """Mesa de fajas: un techo plano de p'ira sobre palos bajos."""
    for (x, y) in ((-2.2, -1.2), (0, -1.2), (2.2, -1.2), (-2.2, 1.2), (0, 1.2), (2.2, 1.2)):
        C.palo((x, y, 0), (x, y, 1.2), 0.06, D["madera"])
    for i in range(7):
        C.caja((-2.45 + 0.7 * i + 0.35, 0, 1.25), (0.68, 3.2, 0.08), D["tierra"], "faja")
    figura((3.4, -1.5, 0), giro=2.4, pose="cuclillas")


def p4c():
    """Pirámide de ichu sobre palos, con óculo."""
    palos(2.2, 8, 0, 1.4)
    C.tronco((0, 0, 1.4), 3.0, 0.3, 3.0, D["paja"], lados=4, abierto_arriba=True, espesor=0.25)
    figura((0.6, -3.6, 0), giro=0.2)


def p4d():
    """Cono de ichu sobre palos, con óculo."""
    palos(2.2, 8, 0, 1.4)
    C.tronco((0, 0, 1.4), 3.0, 0.25, 3.2, D["paja"], lados=48, abierto_arriba=True, espesor=0.25)
    figura((0.6, -3.6, 0), giro=0.2)


def p4e():
    """Un agua: el techo se apoya en una pirca y en palos."""
    C.caja((0, 1.8, 1.1), (5.0, 0.6, 2.2), D["piedra"], "pirca")
    for x in (-2.2, 0, 2.2):
        C.palo((x, -1.8, 0), (x, -1.8, 1.3), 0.06, D["madera"])
    bm = bmesh.new()
    v = [bm.verts.new(p) for p in ((-2.6, -2.2, 1.25), (2.6, -2.2, 1.25), (2.6, 2.1, 2.3), (-2.6, 2.1, 2.3))]
    bm.faces.new(v)
    ob = C.objeto("agua", C.malla_de_bm(bm, "agua", D["paja"], suave=False))
    md = ob.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = 0.25
    figura((3.3, -2.4, 0), giro=2.4)


def p4f():
    """Tienda de fajas: el techo llega al suelo y no hay muros."""
    prisma((0, -3.0), (0, 3.0), 4.2, 2.4, 0.0, D["paja"])
    for i in range(9):
        y = -2.8 + 0.7 * i
        for lado in (-1, 1):
            pass
    C.caja((0, -3.0, 0.45), (0.8, 0.3, 0.9), D["blanco"], "boca").hide_render = True
    figura((2.8, -3.4, 0), giro=2.2)


# ----------------------------------------------------------------------------------------------------------------
# Prueba 5. El fogón: suelos, plataformas y aberturas
# ----------------------------------------------------------------------------------------------------------------

def fogon(x, y, z=0.0):
    for dx in (-0.16, 0.16):
        C.caja((x + dx, y, z + 0.08), (0.12, 0.6, 0.16), D["piedra"], "fogon")


def p5a():
    """Fogón al centro, en un piso plano."""
    C.caja((0, 0, -0.03), (3.3, 5.75, 0.06), D["tierra"], "piso")
    fogon(0, 0)
    figura((-0.7, -0.4, 0), giro=0.0, pose="cuclillas")


def p5b():
    """Fogón hundido, con una zanja para bajar."""
    suelo = C.caja((0, 0, -0.35), (6.0, 6.0, 0.7), D["tierra"], "suelo")
    pozo = C.tronco((0, 0, -0.65), 1.6, 1.6, 0.8, D["tierra"], lados=48)
    zanja = C.caja((0, -2.2, -0.25), (0.8, 2.6, 0.7), D["tierra"], "zanja")
    restar(suelo, pozo); restar(suelo, zanja)
    fogon(0, 0, -0.6)
    figura((-0.8, 0.3, -0.6), giro=0.0, pose="cuclillas")


def p5c():
    """Plataformas en U alrededor del fogón."""
    C.caja((0, 0, -0.03), (3.3, 5.75, 0.06), D["tierra"], "piso")
    for (cx, cy, dx, dy) in ((0, 2.4, 3.3, 0.9), (0, -2.4, 3.3, 0.9), (-1.2, 0, 0.9, 3.9)):
        C.caja((cx, cy, 0.15), (dx, dy, 0.3), D["tierra"], "plataforma")
    fogon(0.4, 0)
    figura((-1.2, 0.6, 0.3), giro=0.0, pose="cuclillas")


def p5d():
    """T'uju en la esquina noreste, apuntado al sol del 21 de junio a las 10."""
    C.caja((0, 0, -0.03), (3.3, 3.3, 0.06), D["tierra"], "piso")
    C.caja((1.45, 0, 1.0), (0.4, 3.3, 2.0), D["tierra"], "muro_e")
    C.caja((0, 1.45, 1.0), (3.3, 0.4, 2.0), D["tierra"], "muro_n")
    s = C.vector_sol()
    esquina = Vector((1.45, 1.45, 1.55))
    agujero = C.palo(esquina - s * 0.5, esquina + s * 0.5, 0.09, D["blanco"], lados=12)
    for m in (bpy.data.objects["muro_e"], bpy.data.objects["muro_n"]):
        restar(m, agujero)
    t = esquina.z / s.z
    piso = esquina - s * t
    C.palo(esquina + s * 0.6, Vector((piso.x, piso.y, 0.01)), 0.035, D["sol"], lados=8)
    C.caja((piso.x, piso.y, 0.005), (0.3, 0.3, 0.01), D["sol"], "mancha")
    figura((-0.6, -0.6, 0), giro=0.8, pose="cuclillas")


def p5e():
    """Óculo de humo en la cumbre de un techo de ichu."""
    C.caja((0, 0, -0.03), (5.0, 5.0, 0.06), D["tierra"], "piso")
    palos(2.0, 6, 0, 1.6)
    C.tronco((0, 0, 1.6), 2.7, 0.3, 2.9, D["paja"], lados=48, abierto_arriba=True, espesor=0.22)
    fogon(0, 0)
    C.palo((0, 0, 0.2), (0.15, -0.1, 5.4), 0.08, D["humo"], lados=10)
    figura((0.7, -3.2, 0), giro=0.2)


def p5f():
    """Casa en cuclillas: un bloque macizo con un hueco de 1,25 m, abierto en corte."""
    blq = C.caja((0, 0, 1.0), (3.3, 5.75, 2.0), D["tierra"], "bloque")
    hueco = C.caja((0, -0.4, 0.15 + 0.625), (2.5, 5.75, 1.25), D["tierra"], "hueco")
    restar(blq, hueco)
    fogon(0, 0.4, 0.15)
    figura((-0.6, -0.4, 0.15), giro=0.0, pose="cuclillas")


PIEZAS = {f.__name__[1:]: f for f in (p3a, p3b, p3c, p3d, p3e, p3f, p4a, p4b, p4c, p4d, p4e, p4f, p5a, p5b, p5c,
                                      p5d, p5e, p5f)}


# ----------------------------------------------------------------------------------------------------------------
# Piezas de la segunda tanda de referencias (27 de noviembre): anillo de tierra con rendijas, torre de hiladas
# sobre dos pircas, planos inclinados con paja y masa de paja sobre zancos atravesada por una caja
# ----------------------------------------------------------------------------------------------------------------

def anillo_tierra(r_fuera, r_fuera_arriba, r_dentro, alto, mat):
    a = C.tronco((0, 0, 0), r_fuera, r_fuera_arriba, alto, mat, lados=72)
    b = C.tronco((0, 0, -0.1), r_dentro, r_dentro, alto + 0.2, mat, lados=72)
    restar(a, b)
    return a


def rendija_volada(anillo, az, ancho=0.9, alto=1.5, pasos=5, largo=4.0):
    """Corta una rendija escalonada (hiladas voladas) a través del anillo, en el acimut dado (grados desde el norte)."""
    a = math.radians(az)
    d = Vector((math.sin(a), math.cos(a), 0))
    for i in range(pasos):
        w = ancho * (1 - i / pasos)
        h = alto / pasos
        c = d * 4.2 + Vector((0, 0, i * h + h / 2))
        cort = C.caja(tuple(c), (w, largo, h * 1.01), D["tierra"], "rendija", rot=(0, 0, -a))
        restar(anillo, cort)


def p3g():
    """Anillo de tierra con pasos volados: la rendija escalonada obliga a agacharse."""
    an = anillo_tierra(5.0, 4.4, 3.7, 2.0, D["tierra"])
    for az in (200, 20):
        rendija_volada(an, az, ancho=1.0, alto=1.4)
    figura((1.2, -6.0, 0), giro=0.3)


def p3h():
    """Torre de hiladas voladas sobre dos pircas: la V invertida de abajo es un paso volado."""
    for x in (-1.25, 1.25):
        C.tronco((x, 0, 0), 0.75, 0.55, 1.4, D["piedra"], lados=4)
    h = 0.15
    hueco = 1.4
    z = 1.4
    i = 0
    while z < 7.0:
        g = max(0.0, hueco - 2 * 0.1 * i)
        if g > 0.01:
            for lado in (-1, 1):
                x0 = lado * (g / 2)
                x1 = lado * 1.3
                C.caja(((x0 + x1) / 2, 0, z + h / 2), (abs(x1 - x0), 1.6, h * 0.92), D["madera"], "hilada")
        else:
            C.caja((0, 0, z + h / 2), (2.6, 1.6, h * 0.92), D["madera"], "hilada")
        z += h
        i += 1
    bm = bmesh.new()
    v = [bm.verts.new(p) for p in ((-1.7, -1.1, 7.0), (1.7, -1.1, 7.0), (1.7, 1.1, 7.9), (-1.7, 1.1, 7.9))]
    bm.faces.new(v)
    ob = C.objeto("techo", C.malla_de_bm(bm, "techo", D["blanco"], suave=False))
    md = ob.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = 0.12
    figura((0, -1.6, 0), giro=0.0)


def p4g():
    """Dos planos inclinados con ichu entre ellos, sobre zancos, con una escalera."""
    for i in range(6):
        for y in (-1.6, 1.6):
            C.palo((-2.0 + i * 0.8, y, 0), (-2.0 + i * 0.8, y, 0.6), 0.05, D["madera"])
    C.caja((0, 0, 0.65), (4.4, 3.6, 0.1), D["madera"], "plataforma")
    for (x0, x1, z1) in ((-2.1, 0.5, 4.2), (2.1, -0.6, 3.6)):
        bm = bmesh.new()
        v = [bm.verts.new(p) for p in ((x0, -1.8, 0.7), (x0, 1.8, 0.7), (x1, 1.8, z1), (x1, -1.8, z1))]
        bm.faces.new(v)
        ob = C.objeto("plano", C.malla_de_bm(bm, "plano", D["madera"], suave=False))
        md = ob.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = 0.1
    prisma((0, -1.5), (0, 1.5), 3.4, 2.6, 0.7, D["paja"], "ichu")
    for x in (-1.4, -1.0):
        C.palo((x, -1.75, 0.7), (x + 0.9, -1.75, 3.0), 0.04, D["madera"])
    for j in range(7):
        t = j / 7
        C.palo((-1.4 + 0.9 * t, -1.75, 0.7 + 2.3 * t), (-1.0 + 0.9 * t, -1.75, 0.7 + 2.3 * t), 0.025, D["madera"])
    figura((2.9, -2.4, 0), giro=2.4)


def p4h():
    """Una masa de ichu sobre zancos de queñua, atravesada por una caja de madera."""
    for (x, y) in ((-1.4, -1.0), (1.4, -1.0), (1.4, 1.0), (-1.4, 1.0), (0, -1.0), (0, 1.0)):
        C.palo((x, y, 0), (x, y, 1.5), 0.06, D["madera"])
    C.palo((-1.4, -1.0, 0.3), (1.4, -1.0, 1.3), 0.04, D["madera"])
    C.palo((1.4, 1.0, 0.3), (-1.4, 1.0, 1.3), 0.04, D["madera"])
    m = C.tronco((0, 0, 1.5), 1.9, 0.35, 5.0, D["paja"], lados=24, ruido=0.12, semilla=3)
    caja = C.caja((-1.9, 0, 2.6), (1.4, 0.9, 1.3), D["madera"], "caja")
    hueco = C.caja((-2.0, 0, 2.6), (1.6, 0.75, 1.15), D["madera"], "hueco_caja")
    restar(caja, hueco)
    restar(m, C.caja((-1.5, 0, 2.6), (1.4, 0.9, 1.3), D["paja"], "hueco_paja"))
    figura((1.0, -2.6, 0), giro=0.5)


def p5g():
    """El anillo del sol: un fogón dentro de un anillo de tierra cortado por rendijas que miran a la salida del sol el
    21 de junio, en los equinoccios y el 21 de diciembre, y al sol de junio a las 10 (tabla de la prueba 5)."""
    an = anillo_tierra(5.0, 4.5, 3.8, 1.9, D["tierra"])
    for az in (44.3, 65.5, 90.6, 114.5):
        rendija_volada(an, az, ancho=0.55, alto=1.5, pasos=4)
    fogon(0, 0)
    a = math.radians(65.5)
    d = Vector((math.sin(a), math.cos(a), 0))
    C.palo(tuple(d * 7.5 + Vector((0, 0, 0.35))), (0, 0, 0.3), 0.035, D["sol"], lados=8)
    figura((-0.8, -0.5, 0), giro=0.3, pose="cuclillas")


PIEZAS.update({f.__name__[1:]: f for f in (p3g, p3h, p4g, p4h, p5g)})


# ----------------------------------------------------------------------------------------------------------------
# Tercera tanda de referencias (27 de noviembre): la torre de tejuelas, la pirámide sobre patas en V delante de una
# masa en estratos, la torre de lamas sobre una base escalonada y la serie de una obra en el tiempo
# ----------------------------------------------------------------------------------------------------------------

def p4i():
    """Torre de fajas de p'ira: las fajas se traslapan como tejuelas y el muro, en espiral, deja la entrada."""
    C.tronco((0, 0, 0), 2.6, 2.6, 0.3, D["madera"], lados=48)
    filas, alto_fila = 5, 1.0
    for f in range(filas):
        z = 0.3 + f * alto_fila * 0.92
        n = 26
        for j in range(n + 4):
            th = 2 * math.pi * j / n
            r = 1.75 - 0.08 * f + 0.45 * th / (2 * math.pi)
            if th > 2 * math.pi + 0.5:
                break
            x, y = r * math.cos(th), r * math.sin(th)
            C.caja((x, y, z + alto_fila / 2), (0.06, 0.5, alto_fila), D["tierra"], "faja",
                   rot=(0, -0.08, th + 0.12))
    figura((1.5, -3.0, 0.3), giro=0.4)


def p4j():
    """Pirámide invertida de fajas sobre patas en V, delante de una masa de lajas en estratos."""
    for i in range(14):
        z = i * 0.22
        for k in range(3):
            C.caja((-3.0 + k * 2.0 + (i % 3) * 0.3, 3.2, z + 0.11), (2.4 - 0.1 * (i % 4), 1.4 - 0.05 * k, 0.2),
                   D["piedra"], "estrato", rot=(0, 0, 0.04 * ((i + k) % 3 - 1)))
    lado = 3.6
    for s in range(4):
        a = s * math.pi / 2
        for j in range(3):
            t0 = -lado / 2 + j * lado / 3
            p_suelo = Vector((t0 + lado / 6, -lado / 2, 0))
            for dt in (0.0, lado / 3):
                p_viga = Vector((t0 + dt, -lado / 2, 1.3))
                q0 = Vector((p_suelo.x * math.cos(a) - p_suelo.y * math.sin(a), p_suelo.x * math.sin(a) + p_suelo.y * math.cos(a), 0))
                q1 = Vector((p_viga.x * math.cos(a) - p_viga.y * math.sin(a), p_viga.x * math.sin(a) + p_viga.y * math.cos(a), 1.3))
                C.palo(q0, q1, 0.05, D["madera"])
    C.caja((0, 0, 1.33), (lado, lado, 0.06), D["madera"], "anillo")
    C.tronco((0, 0, 1.36), 1.8, 2.3, 2.6, D["tierra"], lados=4)
    figura((2.6, -2.6, 0), giro=2.3)


def p5h():
    """Torre de humo: una corona de lamas de ichu sobre patas, encima de una base escalonada de pirca con el fogón."""
    for i, (l, h) in enumerate(((3.4, 0.6), (2.7, 0.6), (2.0, 0.6))):
        C.caja((0, 0, i * 0.6 + h / 2), (l, l, h), D["piedra"], "escalon")
    for i in range(6):
        a = 2 * math.pi * i / 6
        C.palo((1.0 * math.cos(a), 1.0 * math.sin(a), 1.8), (1.4 * math.cos(a), 1.4 * math.sin(a), 3.2), 0.05, D["madera"])
    for j in range(16):
        a = 2 * math.pi * j / 16
        C.caja((1.4 * math.cos(a), 1.4 * math.sin(a), 5.2), (0.08, 0.5, 4.0), D["paja"], "lama", rot=(0, 0, a + 0.6))
    C.palo((0, 0, 1.8), (0.2, 0.1, 8.6), 0.12, D["humo"], lados=10)
    figura((1.9, -2.4, 0), giro=0.4)


def corral_simple(estado):
    """El corral techado de E2, en masas, en cuatro estados (serie del tiempo)."""
    ring = C.tronco((0, 0, 0), 3.0, 2.95, 1.4 if estado < 4 else 1.4, D["piedra"], lados=64)
    dentro = C.tronco((0, 0, -0.1), 2.3, 2.3, 1.7, D["piedra"], lados=64)
    restar(ring, dentro)
    entrada = C.caja((0, -2.8, 0.7), (1.6, 1.8, 1.6), D["piedra"], "entrada")
    restar(ring, entrada)
    if estado == 4:
        for (az, w) in ((60, 1.8), (150, 1.2)):
            a = math.radians(az)
            c = C.caja((2.65 * math.cos(a), 2.65 * math.sin(a), 1.0), (1.0, w, 1.0), D["piedra"], "caida", rot=(0, 0, a))
            restar(ring, c)
            C.tronco((3.3 * math.cos(a), 3.3 * math.sin(a), 0), 0.9, 0.1, 0.55, D["piedra"], lados=24)
    if estado <= 3:
        palos(2.0, 8, 0, 2.3 if estado < 3 else 2.0, fase=math.pi / 8)
    if estado <= 2:
        techo = C.tronco((0, 0, 2.3), 3.3, 0.35, 3.2, D["paja"], lados=4, abierto_arriba=True, espesor=0.22)
        if estado == 2:
            for (x, y, z) in ((1.2, -0.6, 3.3), (-0.6, 1.3, 3.0)):
                restar(techo, C.caja((x, y, z), (1.4, 1.2, 1.2), D["paja"], "hueco"))
    figura((0.4, -3.8, 0), giro=0.1)


def pt1():
    """El corral techado, recién hecho."""
    corral_simple(1)


def pt2():
    """Los techos «desfondados» (Botelho Gosálvez, 1982 [1945]: 79)."""
    corral_simple(2)


def pt3():
    """Quedan los palos."""
    corral_simple(3)


def pt4():
    """La pirca a medio caer, con su piedra en montones."""
    corral_simple(4)


PIEZAS.update({f.__name__[1:]: f for f in (p4i, p4j, p5h, pt1, pt2, pt3, pt4)})


def p5i():
    """Muro que deja pasar: adobitos de pie, con una separación entre uno y otro y una cama de barro entre las
    hiladas, alrededor del fogón (referencia: fotos del autor en la Huaca Pucllana, Lima). Medidas del proyecto."""
    R, hilada, cama, ancho, hueco, prof = 2.0, 0.24, 0.04, 0.10, 0.035, 0.18
    z = 0.0
    for i in range(7):
        a_cama = C.tronco((0, 0, z), R + prof / 2, R + prof / 2, cama, D["tierra"], lados=64)
        restar(a_cama, C.tronco((0, 0, z - 0.05), R - prof / 2, R - prof / 2, cama + 0.1, D["tierra"], lados=64))
        if i < 5:
            restar(a_cama, C.caja((0, -R, z + cama / 2), (0.8, 0.6, cama + 0.1), D["tierra"], "boca"))
        z += cama
        n = int(2 * math.pi * R / (ancho + hueco))
        for j in range(n):
            a = 2 * math.pi * (j + 0.5 * (i % 2)) / n
            if abs(((a - 1.5 * math.pi) + math.pi) % (2 * math.pi) - math.pi) < 0.2 and i < 5:
                continue
            C.caja((R * math.cos(a), R * math.sin(a), z + hilada / 2), (prof, ancho, hilada), D["tierra"], "adobito",
                   rot=(0, 0, a))
        z += hilada
    fogon(0, 0)
    C.palo((0, 0, 0.2), (0.1, 0.1, 3.4), 0.07, D["humo"], lados=10)
    figura((-0.7, -0.3, 0), giro=0.3, pose="cuclillas")


PIEZAS.update({"5i": p5i})


def renderizar(clave, salida, lado=900, muestras=16):
    C.escena_nueva()
    mats()
    sc = bpy.context.scene
    C.caja((0, 0, -0.705), (40, 40, 0.01), C.mat_liso("fondo_blanco", (0.93, 0.93, 0.92), 1.0), "fondo")
    antes = set(bpy.data.objects)
    PIEZAS[clave]()
    bpy.context.view_layer.update()
    pts = []
    for ob in bpy.data.objects:
        if ob in antes or ob.hide_render or ob.type != 'MESH':
            continue
        pts += [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centro, radio = (lo + hi) / 2, (hi - lo).length / 2
    cam = C.camara(centro, 40, -35, 30, lente=50)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = radio * 2.15
    w = bpy.data.worlds.new("blanco"); sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    sol = bpy.data.lights.new("sol", 'SUN'); sol.energy = 2.2; sol.angle = math.radians(8)
    so = C.ligar(bpy.data.objects.new("sol", sol)); so.rotation_euler = (math.radians(40), 0, math.radians(-50))
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = 1.3
    fs = sc.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("lineas")
    ls.linestyle = bpy.data.linestyles.new("tinta")
    ls.linestyle.color = (0.08, 0.075, 0.07)
    ls.select_by_visibility = True
    for k in ("select_silhouette", "select_border", "select_crease", "select_external_contour"):
        setattr(ls, k, True)
    C.ajustes_render(lado, lado, muestras, str(Path(salida) / f"pieza_{clave}.png"), exposicion=0.0)
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Standard'
    bpy.ops.render.render(write_still=True)
    print(f"pieza {clave} lista")


def main():
    args = [a for a in sys.argv[1:] if a != "--"]
    salida = AQUI.parent / "renders" / "piezas"
    if "--salida" in args:
        salida = Path(args[args.index("--salida") + 1])
    salida.mkdir(parents=True, exist_ok=True)
    claves = [a for a in args if a in PIEZAS] or list(PIEZAS)
    for c in claves:
        renderizar(c, salida)


if __name__ == "__main__":
    main()
