"""Los diagramas de las cinco exploraciones de Chhaxwa: un corte de cada una y las cinco a la misma escala.

Cada corte parte la exploración por la mitad para mostrar cómo se construye: qué es piedra, qué es tierra, qué es
adobe, qué es paja y qué es madera. Son modelos de masas con contornos (Freestyle), en metros reales, con una figura de
1,65 m, como las piezas de piezas.py. Las medidas son las de formas.py. Se corre desde la raíz del repositorio:
    venv_bpy/bin/python chhaxwa/blender/diagramas.py              # los seis, en chhaxwa/renders/diagramas/
    venv_bpy/bin/python chhaxwa/blender/diagramas.py x3 serie     # algunos
Después, con el Python del sistema, aligerar_piezas.py pasa los PNG a una paleta de 64 colores.
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
import piezas as P               # noqa: E402

D = P.D
FIGURAS = True


def colores():
    P.mats()
    D["menuda"] = C.mat_liso("d_menuda", (0.68, 0.67, 0.65), 0.9)
    D["laja"] = C.mat_liso("d_laja", (0.38, 0.38, 0.37), 0.9)
    D["adobe"] = C.mat_liso("d_adobe", (0.62, 0.50, 0.39), 0.9)
    D["champa"] = C.mat_liso("d_champa", (0.36, 0.30, 0.24), 0.9)
    D["pira"] = C.mat_liso("d_pira", (0.56, 0.49, 0.40), 0.9)
    D["vacio"] = C.mat_liso("d_vacio", (0.16, 0.15, 0.14), 0.9)


def figura(pos, giro=0.0, pose="pie"):
    if FIGURAS:
        P.figura(pos, giro, pose)


# ----------------------------------------------------------------------------------------------------------------
# Ayudas de geometría
# ----------------------------------------------------------------------------------------------------------------

def sector(r_o0, r_o1, r_i0, r_i1, z0, h, a0, a1, mat, n=96, nombre="sector"):
    """Un sector de anillo con forma de tronco de cono: radio de afuera r_o0 abajo y r_o1 arriba, de adentro r_i0 y r_i1.
    Entre los ángulos a0 y a1; si da la vuelta entera no lleva tapas."""
    entero = abs((a1 - a0) - 2 * math.pi) < 1e-6
    seg = max(2, int(n * (a1 - a0) / (2 * math.pi)))
    bm = bmesh.new()

    def anillo(r, z):
        r = max(r, 0.002)
        return [bm.verts.new((r * math.cos(a0 + (a1 - a0) * j / seg), r * math.sin(a0 + (a1 - a0) * j / seg), z))
                for j in range(seg + (0 if entero else 1))]
    ob, ot, ib, it = anillo(r_o0, z0), anillo(r_o1, z0 + h), anillo(r_i0, z0), anillo(r_i1, z0 + h)
    m = len(ob)
    rango = range(m) if entero else range(m - 1)
    for j in rango:
        k = (j + 1) % m
        bm.faces.new((ob[j], ob[k], ot[k], ot[j]))
        bm.faces.new((ib[k], ib[j], it[j], it[k]))
        bm.faces.new((ot[j], ot[k], it[k], it[j]))
        bm.faces.new((ob[k], ob[j], ib[j], ib[k]))
    if not entero:
        bm.faces.new((ob[0], ot[0], it[0], ib[0]))
        bm.faces.new((ob[-1], ib[-1], it[-1], ot[-1]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return C.objeto(nombre, C.malla_de_bm(bm, nombre, mat, suave=False))


def extruir(perfil, eje, d0, d1, mat, nombre="perfil"):
    """Extruye un polígono [(u, z), ...] a lo largo de x («x», con u = y) o de y («y», con u = x), entre d0 y d1."""
    bm = bmesh.new()

    def punto(u, z, d):
        return (d, u, z) if eje == "x" else (u, d, z)
    a = [bm.verts.new(punto(u, z, d0)) for (u, z) in perfil]
    b = [bm.verts.new(punto(u, z, d1)) for (u, z) in perfil]
    n = len(perfil)
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return C.objeto(nombre, C.malla_de_bm(bm, nombre, mat, suave=False))


def caja(x0, x1, y0, y1, z0, z1, mat, nombre="caja"):
    return C.caja(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), (x1 - x0, y1 - y0, z1 - z0), mat, nombre)


# ----------------------------------------------------------------------------------------------------------------
# E1. La montaña habitada: medio cono de piedra, cortado por la boca
# ----------------------------------------------------------------------------------------------------------------

def x1(corte=True):
    R0, R1, H, hz = 3.6, 0.32, 2.6, 0.2
    a0, a1 = (-math.pi / 2, math.pi / 2) if corte else (-math.pi / 2, 1.5 * math.pi)
    for i in range(13):
        z = i * hz
        ro0, ro1 = R0 - (R0 - R1) * z / H, R0 - (R0 - R1) * (z + hz) / H
        ri = 1.4 if z < 0.99 else max(R1, 1.4 - 0.135 * (i - 4))      # la cámara: vertical hasta 1 m y después volada
        s = sector(ro0, ro1, ri, ri, z, hz, a0, a1, D["piedra"])
        if z < 0.99:                                                   # la boca, al sur, de 0,9 × 1,0 m
            P.restar(s, caja(-0.45, 0.45, -4.5, -1.0, -0.1, 1.0, D["piedra"]))
    for x in ((0.48,) if corte else (-0.48, 0.48)):                     # la caja de queñua de la entrada
        caja(x - 0.035, x + 0.035, -4.15, -2.65, 0, 1.0, D["madera"])
    caja(0 if corte else -0.52, 0.52, -4.15, -2.65, 1.0, 1.07, D["madera"])
    figura((0.3, -4.6, 0), giro=math.pi / 2, pose="cuclillas")
    figura((0.6, 0.3, 0), giro=2.6)


# ----------------------------------------------------------------------------------------------------------------
# E2. El corral techado: medio corral de pirca de doble cara y medio cono de ichu sobre palos
# ----------------------------------------------------------------------------------------------------------------

def x2(corte=True):
    R, alto = 3.0, 1.4
    e0, e1 = math.radians(-135), math.radians(-45)                     # la entrada, al sur
    tramos = [(e1, math.pi / 2)] if corte else [(e1, 2 * math.pi + e0)]
    for (a0, a1) in tramos:
        sector(R, R, R - 0.2, R - 0.2, 0, alto, a0, a1, D["piedra"])
        sector(R - 0.5, R - 0.5, R - 0.7, R - 0.7, 0, alto, a0, a1, D["piedra"])
        sector(R - 0.2, R - 0.2, R - 0.5, R - 0.5, 0, alto * 0.98, a0, a1, D["menuda"])
    z_al = 2.3
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        if corte and math.cos(a) < 0:
            continue
        C.palo((2.0 * math.cos(a), 2.0 * math.sin(a), 0), (2.0 * math.cos(a), 2.0 * math.sin(a), z_al - 0.06), 0.06,
               D["madera"])
    a0, a1 = (-math.pi / 2, math.pi / 2) if corte else (0, 2 * math.pi)
    sector(2.07, 2.07, 1.93, 1.93, z_al - 0.12, 0.12, a0, a1, D["madera"])              # el anillo sobre los palos
    for i in range(12):                                                                 # los pares, bajo la paja
        a = 2 * math.pi * i / 12
        if corte and math.cos(a) < -1e-6:
            continue
        C.palo((3.05 * math.cos(a), 3.05 * math.sin(a), z_al + 0.02), (0.12 * math.cos(a), 0.12 * math.sin(a), z_al + 3.15),
               0.045, D["madera"])
    sector(3.4, 0.3, 3.05, 0.05, z_al, 3.4, a0, a1, D["paja"])                          # el cono de ichu
    figura((0.8, -0.6, 0), giro=2.2)


# ----------------------------------------------------------------------------------------------------------------
# E3. La torre de champa: media torre, cortada a lo largo; el corte atraviesa la V
# ----------------------------------------------------------------------------------------------------------------

def x3(corte=True):
    X, Y, Hp, g, Hl, Hh, BH, BA = 1.5, 0.8, 0.9, 0.5, 4.2, 5.4, 0.12, 0.25
    m = 0 if corte else 1

    def tope(x):
        return Hl + (x + X) / (2 * X) * (Hh - Hl)
    caja(-X - 0.1, -g, -0.9 * m, 0.9, 0, Hp, D["piedra"], "pirca")
    pila = sector(1.0, 0.55, 0.0, 0.0, 0, Hp, 0, math.pi if corte else 2 * math.pi, D["piedra"], nombre="monton")
    pila.location.x = (g + X) / 2
    pila.scale.y = 1.55
    for (x0, x1_) in ((-X - 0.1, -g), (g, X + 0.1)):
        caja(x0, x1_, -0.9 * m, 0.9, Hp - 0.02, Hp + 0.05, D["laja"], "lajas")
    z0 = Hp + 0.05
    i = 0
    while True:                                                        # las patas y la V de hiladas voladas
        w = g - 0.06 * (i + 1)
        z = z0 + i * BH
        if w <= 0.03:
            break
        for (xa, xb) in ((-X, -w), (w, X)):
            caja(xa, xb, -Y * m, Y, z, z + BH, D["champa"], "hilada")
        i += 1
    zc = z0 + i * BH
    caja(-X, X, -Y * m, Y, zc, zc + BH, D["champa"], "cierre")
    zc += BH
    perfil = [(-X, zc), (X, zc), (X, tope(X)), (-X, tope(-X))]
    extruir(perfil, "y", Y - BA, Y, D["champa"], "muro_n")
    if not corte:
        extruir(perfil, "y", -Y, -Y + BA, D["champa"], "muro_s")
    for (xa, xb) in ((-X, -X + BA), (X - BA, X)):
        extruir([(xa, zc), (xb, zc), (xb, tope(xb)), (xa, tope(xa))], "y", -(Y - BA) * m, Y - BA, D["champa"], "testero")
    for j in range(6):                                                 # palos de queñua y las piedras hincadas
        x = -X + 0.25 + j * 0.5
        zt = tope(x) + 0.06
        C.palo((x, -(Y + 0.28) * m, zt), (x, Y + 0.28, zt), 0.06, D["madera"])
        for yy in ((Y,) if corte else (-Y, Y)):
            s = 1 if yy > 0 else -1
            caja(x - 0.12, x + 0.12, yy - s * 0.1 if s > 0 else yy - 0.22, yy + 0.22 if s > 0 else yy + 0.1,
                 zt - 0.5, zt - 0.36, D["laja"], "chhaxwa")
    th = math.atan((Hh - Hl) / (2 * X))

    xa, xb = -X - 0.25, X + 0.25
    za, zb = tope(-X) + 0.12 - 0.25 * math.tan(th), tope(X) + 0.12 + 0.25 * math.tan(th)
    extruir([(xa, za), (xb, zb), (xb, zb + 0.06), (xa, za + 0.06)], "y", -(Y + 0.28) * m, Y + 0.28, D["pira"], "fajas")
    for (xl, zl) in ((-0.9, 2.7), (0.4, 3.3), (1.0, 2.4), (-0.3, 3.9), (0.8, 4.3)):      # lajas pasantes
        caja(xl - 0.2, xl + 0.2, Y - 0.15, Y + 0.25, zl, zl + 0.06, D["laja"], "laja")
    figura((-0.1, 0.25, 0), giro=math.pi / 2)


# ----------------------------------------------------------------------------------------------------------------
# E4. La chullpa: media chullpa, cortada por la boca del este
# ----------------------------------------------------------------------------------------------------------------

def x4(corte=True):
    m = 0 if corte else 1
    c, Pp = 1.05, 1.2
    for sx in (-1, 1):                                                  # las pilas, con sus dos hiladas voladas
        for sy in ((1,) if corte else (-1, 1)):
            for i in range(6):
                v = 0.1 * max(0, i - 3)
                xs = sorted((sx * (c - Pp / 2 - v), sx * (c + Pp / 2)))
                ys = sorted((sy * (c - Pp / 2 - v), sy * (c + Pp / 2)))
                caja(xs[0], xs[1], ys[0], ys[1], i * 0.2, (i + 1) * 0.2, D["piedra"], "pila")
    S = 2 * c + Pp
    caja(-S / 2, S / 2, -S / 2 * m, S / 2, 1.2, 1.3, D["laja"], "lajas")
    caja(-1.55, 1.55, -1.55 * m, 1.55, 1.3, 1.48, D["piedra"], "cama")
    z = 1.48
    for i in range(15):                                                 # la pirámide de adobitos, con la cámara volada
        s = 3.0 - 2 * i * 0.062
        h = 0.21
        cam = 0.5 if i < 3 else 0.5 - 0.1 * (i - 2)
        mat = D["adobe"]
        if cam > 0.05 and corte:
            caja(-s / 2, -cam, 0, s / 2, z, z + h, mat, "hilada")
            caja(-cam, cam, cam, s / 2, z, z + h, mat, "hilada")
            y0 = 0.24 if i < 2 else (0.36 if i == 2 else 0.0)
            caja(cam, s / 2, y0, s / 2, z, z + h, mat, "hilada")
            if i == 2:
                caja(cam, s / 2, 0, 0.36, z, z + h, D["laja"], "dintel")
        else:
            if i < 3 and not corte:
                y0 = 0.24 if i < 2 else 0.36
                caja(-s / 2, s / 2 - 0.14, -s / 2, s / 2, z, z + h, mat, "hilada")
                for sg in (-1, 1):
                    caja(s / 2 - 0.14, s / 2, *sorted((sg * y0, sg * s / 2)), z, z + h, mat, "hilada")
                if i == 2:
                    caja(s / 2 - 0.14, s / 2, -0.36, 0.36, z, z + h, D["laja"], "dintel")
            else:
                caja(-s / 2, s / 2, -s / 2 * m, s / 2, z, z + h, mat, "hilada")
        z += h
        if i == 12:                                                     # la cornisa de ichu prensado
            caja(-s / 2 - 0.1, s / 2 + 0.1, -(s / 2 + 0.1) * m, s / 2 + 0.1, z, z + 0.15, D["paja"], "cornisa")
            z += 0.15
    s = 3.0 - 30 * 0.062
    caja(-s / 2 - 0.02, s / 2 + 0.02, -(s / 2 + 0.02) * m, s / 2 + 0.02, z, z + 0.08, D["adobe"], "tapa")
    figura((0.0, 0.35 if corte else -0.2, 0), giro=math.pi / 2, pose="cuclillas")
    figura((-2.6, 0.6, 0), giro=0.4)


# ----------------------------------------------------------------------------------------------------------------
# E5. La casa de la bóveda: media casa, cortada de través por el fogón; se ve la bóveda volada
# ----------------------------------------------------------------------------------------------------------------

def x5(corte=True):
    Li, Wi, E0, Hw, zr, cara = 5.75, 3.30, 0.9, 2.6, 0.8, 0.32
    Lo, Wo = Li + 2 * E0, Wi + 2 * E0
    tal = math.tan(math.radians(10))
    hh, b = 0.11, 0.07 / 0.11
    a2H = (0.13 / 0.11 - b) / 2
    H = (Wi / 2 - 0.15) / (b + a2H)
    a2 = a2H / H
    n = int(round(H / hh)) + 1

    def r(h):
        return max(0.15, Wi / 2 - b * h - a2 * h * h)
    x0 = 0 if corte else -Lo / 2 + tal * Hw / 2
    xi0 = 0 if corte else -Li / 2
    zf = 2.1
    for sg in (-1, 1):                                                  # los muros largos: dos caras y el relleno
        def esp(u):
            return sg * u
        hoja = [(esp(Wo / 2 - cara), 0), (esp(Wo / 2), 0), (esp(Wo / 2 - tal * Hw), Hw), (esp(Wo / 2 - tal * Hw - cara), Hw)]
        extruir(hoja, "x", x0, Lo / 2 - tal * Hw / 2, D["piedra"], "hoja")
        caja(xi0, Li / 2, *sorted((esp(Wi / 2), esp(Wi / 2 + cara))), 0, zr, D["piedra"], "hoja_dentro")
        borde = [(esp(r(h) + 0.40), zr + h) for h in [j * hh for j in range(int((zf - zr) / hh), -1, -1)]]
        relleno = [(esp(Wi / 2 + cara), 0), (esp(Wo / 2 - cara), 0), (esp(Wo / 2 - cara - tal * zf), zf)] + borde + \
                  [(esp(Wi / 2 + cara), zr)]
        if sg < 0:
            relleno = list(reversed(relleno))
        extruir(relleno, "x", x0 + 0.001, Li / 2, D["tierra"], "relleno")
    for (xa, xb, sg) in (((Li / 2, Lo / 2, 1),) if corte else ((Li / 2, Lo / 2, 1), (-Lo / 2, -Li / 2, -1))):
        h_ = Hw - 0.004                                                # un poco más bajo, para no coincidir con el muro largo
        perfil = [(xa, 0), (xb, 0), (xb - tal * h_, h_), (xa, h_)] if sg > 0 else [(xa, 0), (xb, 0), (xb, h_), (xa + tal * h_, h_)]
        tramos = ((0.25, Wo / 2 - 0.1), (-Wo / 2 + 0.1, -0.25)) if sg > 0 else ((-Wo / 2 + 0.1, Wo / 2 - 0.1),)
        for (y0, y1) in tramos:
            extruir(perfil, "y", y0, y1, D["piedra"], "testero")
    caja(Li / 2, Li / 2 + 0.24, -0.28, 0.28, 1.3, Hw - 0.1, D["adobe"], "timpano")
    for i in range(n):                                                  # la bóveda volada
        h = i * hh
        for sg in (-1, 1):
            caja(xi0, Li / 2, *sorted((sg * r(h), sg * (r(h) + 0.40))), zr + h, zr + h + hh - 0.01, D["adobe"], "hilada")
    zc = zr + n * hh
    for xa in [x / 100 for x in range(-int(Li * 50), int(Li * 50), 48)]:   # las lajas de la clave; falta la del fogón
        if (corte and xa < 0) or abs(xa + 0.22) < 0.4:
            continue
        caja(xa, min(xa + 0.44, Li / 2), -0.37, 0.37, zc, zc + 0.08, D["laja"], "laja")
    for dx in (-0.16, 0.16):                                            # el fogón
        caja(0 if corte else -0.3, 0.3, dx - 0.07, dx + 0.07, 0, 0.16, D["piedra"], "fogon")
    if FIGURAS:
        C.palo((0.1, 0, 0.2), (0.1, 0, zc + 1.0), 0.07, D["humo"], lados=10)
        s = C.vector_sol()                                              # el t'uju y el sol del 21 de junio a las 10
        p_in = Vector((Li / 2 - 0.3, Wi / 2 - 0.02, 0.55))
        t = 0.0
        while t < 5.0:
            q = p_in + s * t
            if abs(q.x) > Lo / 2 - tal * q.z or abs(q.y) > Wo / 2 - tal * q.z:
                break
            t += 0.02
        C.palo(p_in - s * 0.05, p_in + s * (t + 0.05), 0.09, D["vacio"], lados=12)
        C.palo(p_in - s * (p_in.z / s.z), p_in + s * (t + 1.6), 0.03, D["sol"], lados=8)
    figura((0.9, -0.6, 0), giro=2.8, pose="cuclillas")


# ----------------------------------------------------------------------------------------------------------------
# Las cinco a la misma escala, de izquierda a derecha
# ----------------------------------------------------------------------------------------------------------------

def serie():
    global FIGURAS
    lugares = ((x1, 0.0), (x2, 8.6), (x3, 15.4), (x4, 21.0), (x5, 28.4))
    for (f, ox) in lugares:
        antes = set(bpy.data.objects)
        FIGURAS = False
        f(corte=False)
        FIGURAS = True
        for ob in bpy.data.objects:
            if ob not in antes:
                ob.location.x += ox
        y_fig = {x1: -4.4, x2: -3.6, x3: -1.6, x4: -2.3, x5: -3.4}[f]
        P.figura((ox + (0.9 if f is not x3 else -2.2), y_fig, 0), giro=0.1)


DIAGRAMAS = {"x1": x1, "x2": x2, "x3": x3, "x4": x4, "x5": x5, "serie": serie}
VISTAS = {"serie": dict(acimut=0, elevacion=0, ancho=2400, alto=560, aire=1.03, suelo=-0.005)}


# ----------------------------------------------------------------------------------------------------------------
# La candidata: la casa redonda, cortada por la puerta del este
# ----------------------------------------------------------------------------------------------------------------

def x6(corte=True):
    import formas as F
    Ri, e, Hb, hh, tal = 2.0, 0.6, 1.2, 0.12, math.tan(math.radians(5))
    R = Ri + e
    radios = F.cupula_perfil(Ri, hh, v0=0.10)
    full = 2 * math.pi
    for (z0, z1, medio) in ((0, 1.0, 0.3), (1.0, 1.2, 0.55)):          # la pirca: dos caras y el relleno, con la puerta
        for (ro0, ro1, ri, mat) in ((R - tal * z0, R - tal * z1, R - 0.2, D["piedra"]), (R - 0.2, R - 0.2, Ri + 0.2, D["menuda"]),
                                    (Ri + 0.2, Ri + 0.2, Ri, D["piedra"])):
            d = math.asin(min(1.0, medio / ri))
            a0, a1 = (d, math.pi) if corte else (d, full - d)
            sector(ro0, ro1, ri, ri, z0, z1 - z0, a0, a1, mat)
    caja(Ri, R, 0 if corte else -0.55, 0.55, 1.0, 1.18, D["laja"], "dintel")
    a0, a1 = (0, math.pi) if corte else (0, full)
    for i, r in enumerate(radios):                                     # la cúpula de champa, volada
        sector(r + 0.4, r + 0.4, r, r, Hb + i * hh, hh - 0.005, a0, a1, D["champa"])
    z_top = Hb + len(radios) * hh
    Hd, r_ocu, dd = z_top - Hb + 0.1, radios[-1] + 0.15, 0.16
    A = R - tal * Hb + 0.02 - r_ocu
    for kb in range(5):                                                # el relleno de tierra en cinco anillos
        t0, t1 = math.pi / 2 * kb / 5, math.pi / 2 * (kb + 1) / 5
        pasos = 6
        for q in range(pasos):
            ta, tb = t0 + (t1 - t0) * q / pasos, t0 + (t1 - t0) * (q + 1) / pasos
            za, zb = Hb + Hd * math.sin(ta), Hb + Hd * math.sin(tb)
            ra, rb = r_ocu + (A - dd * kb) * math.cos(ta), r_ocu + (A - dd * kb) * math.cos(tb)
            h_ = zb - za
            ri_a = max(radios[min(len(radios) - 1, int((za - Hb) / hh))] + 0.4, r_ocu - 0.15)
            sector(ra, rb, ri_a, ri_a, za, h_, a0, a1, D["tierra"])
    for j in range(3):                                                 # el sombrero de ichu
        a = 2 * math.pi * j / 3 + 0.4
        if corte and math.sin(a) < 0:
            continue
        C.palo((0.42 * math.cos(a), 0.42 * math.sin(a), z_top), (0.36 * math.cos(a), 0.36 * math.sin(a), z_top + 0.36), 0.035,
               D["madera"])
    sector(0.62, 0.04, 0.5, 0.02, z_top + 0.3, 0.4, a0, a1, D["paja"])
    for dx in (-0.16, 0.16):                                           # el fogón
        caja(-0.3, 0.3, dx - 0.07 if not corte or dx > 0 else 0, dx + 0.07, 0, 0.16, D["piedra"], "fogon")
    if FIGURAS:
        C.palo((0, 0.1, 0.2), (0, 0.1, z_top + 0.5), 0.07, D["humo"], lados=10)
        s = C.vector_sol()                                              # el t'uju y el sol del 21 de junio a las 10
        p_in = Vector((Ri * math.cos(math.radians(45)), Ri * math.sin(math.radians(45)), 0.65))
        t = 0.0
        while t < 3.0 and (p_in + s * t).xy.length < R - tal * (p_in + s * t).z:
            t += 0.02
        C.palo(p_in - s * 0.05, p_in + s * (t + 0.05), 0.09, D["vacio"], lados=12)
        C.palo(p_in - s * (p_in.z / s.z), p_in + s * (t + 1.4), 0.03, D["sol"], lados=8)
    figura((-0.9, 0.6, 0), giro=0.4, pose="cuclillas")
    figura((R + 0.8, 0.4, 0), giro=2.8)


DIAGRAMAS["x6"] = x6


def renderizar(clave, salida, muestras=16):
    C.escena_nueva()
    colores()
    sc = bpy.context.scene
    suelo = VISTAS.get(clave, {}).get("suelo", -0.705)
    C.caja((0, 0, suelo), (120, 120, 0.01), C.mat_liso("fondo_blanco", (0.93, 0.93, 0.92), 1.0), "fondo")
    antes = set(bpy.data.objects)
    DIAGRAMAS[clave]()
    bpy.context.view_layer.update()
    pts = []
    for ob in bpy.data.objects:
        if ob in antes or ob.hide_render or ob.type != 'MESH':
            continue
        pts += [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    centro, radio = (lo + hi) / 2, (hi - lo).length / 2
    v = VISTAS.get(clave, {})
    cam = C.camara(centro, 80, v.get("acimut", -35), v.get("elevacion", 30), lente=50)
    cam.data.type = 'ORTHO'
    ancho, alto = v.get("ancho", 1000), v.get("alto", 1000)
    if clave == "serie":
        cam.data.ortho_scale = (hi.x - lo.x) * v["aire"]
    else:
        cam.data.ortho_scale = radio * 2.1
    w = bpy.data.worlds.new("blanco"); sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    sol = bpy.data.lights.new("sol", 'SUN'); sol.energy = 2.2; sol.angle = math.radians(8)
    so = C.ligar(bpy.data.objects.new("sol", sol)); so.rotation_euler = (math.radians(40), 0, math.radians(-50))
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = 1.2
    fs = sc.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("lineas")
    ls.linestyle = bpy.data.linestyles.new("tinta")
    ls.linestyle.color = (0.08, 0.075, 0.07)
    ls.select_by_visibility = True
    for k in ("select_silhouette", "select_border", "select_crease", "select_external_contour"):
        setattr(ls, k, True)
    C.ajustes_render(ancho, alto, muestras, str(Path(salida) / f"diagrama_{clave}.png"), exposicion=0.0)
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Standard'
    bpy.ops.render.render(write_still=True)
    print(f"diagrama {clave} listo")


def main():
    args = [a for a in sys.argv[1:] if a != "--"]
    salida = AQUI.parent / "renders" / "diagramas"
    if "--salida" in args:
        salida = Path(args[args.index("--salida") + 1])
    salida.mkdir(parents=True, exist_ok=True)
    for c in [a for a in args if a in DIAGRAMAS] or list(DIAGRAMAS):
        renderizar(c, salida)


if __name__ == "__main__":
    main()
