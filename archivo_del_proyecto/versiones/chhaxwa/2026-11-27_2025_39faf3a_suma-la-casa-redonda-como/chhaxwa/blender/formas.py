"""Las quince maquetas de forma de Chhaxwa: tres por prueba.

Cada función arma una maqueta sobre la mesa del estudio (z = zc) y devuelve (escala, descripción). Las medidas se
escriben en metros reales y se multiplican por la escala de la maqueta. Las que no vienen de una fuente son
decisiones del proyecto (exploracion_formal.md).
"""

import math
import random
from mathutils import Vector

import comun as C


class Ctx:
    def __init__(self, mats, zc, semilla):
        self.m, self.zc, self.r = mats, zc, random.Random(semilla)
        self._ped = {}

    def pedrera(self, clave="piedra", n=36):
        if clave not in self._ped:
            mat = self.m.piedra if clave == "piedra" else self.m.piedra_fina
            self._ped[clave] = C.Pedrera(mat, n=n, semilla=len(self._ped) + 3)
        return self._ped[clave]


def sobre(ctx, x, y, z=0.0):
    return (x, y, ctx.zc + z)


# ----------------------------------------------------------------------------------------------------------------
# Prueba 1. La cosecha
# ----------------------------------------------------------------------------------------------------------------

def forma_1A(ctx):
    """Cuatro montones y un techo: la piedra de una parcela de 2 × 2 m sostiene dos fajas de p'ira."""
    k = 1 / 10
    ped = ctx.pedrera()
    for (x, y) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        C.monton(ped, sobre(ctx, x * k, y * k), 0.5 * k, 0.42 * k, 0.11 * k, ctx.r, z0=ctx.zc)
        ped.poner(sobre(ctx, x * k, y * k, 0.52 * k), 0.36 * k, rot=(math.pi / 2 + ctx.r.uniform(-0.1, 0.1), 0, ctx.r.uniform(0, 3)),
                  aplanar=0.35)
    zp = 0.66 * k
    for x in (-1, 1):
        C.palo(sobre(ctx, x * k, -1.25 * k, zp), sobre(ctx, x * k, 1.25 * k, zp), 0.03 * k, ctx.m.palo)
    for x0 in (-0.72, 0.02):
        C.caja(sobre(ctx, (x0 + 0.35) * k, 0, zp + 0.055 * k), (0.7 * k, 2.5 * k, 0.05 * k), ctx.m.barro, "faja",
               rot=(0, 0, ctx.r.uniform(-0.02, 0.02)), bisel=0.01 * k)
    C.figura_madera(sobre(ctx, 1.9 * k, -0.6 * k), ctx.m.figura, alto=1.65 * k, giro=2.4)
    return k, "Cuatro montones y un techo"


def forma_1B(ctx):
    """La montaña de piedras: toda la cosecha en un cono de piedra seca, hueco, con una boca baja y un óculo."""
    k = 1 / 20
    ped = ctx.pedrera()
    R0, R1, H = 3.0, 0.45, 4.0
    capas = int(H / 0.24)
    for i in range(capas):
        z = i * H / capas
        rr = R0 + (R1 - R0) * z / H
        m = int(2 * math.pi * rr / 0.34)
        fase = ctx.r.uniform(0, 6.28)
        for j in range(m):
            a = fase + 2 * math.pi * j / m
            if abs(((a - math.radians(250)) + math.pi) % (2 * math.pi) - math.pi) < 0.17 and z < 0.95:
                continue
            ped.poner(sobre(ctx, rr * math.cos(a) * k, rr * math.sin(a) * k, (z + 0.1) * k), 0.36 * k,
                      rot=(ctx.r.uniform(-0.15, 0.15), -math.radians(25), a), aplanar=0.6)
    C.tronco(sobre(ctx, 0, 0), (R0 - 0.35) * k, (R1 - 0.1) * k, H * 0.98 * k, C.mat_liso("sombra", (0.04, 0.035, 0.03)),
             lados=32, abierto_arriba=True)
    C.figura_madera(sobre(ctx, -1.2 * k, -3.9 * k), ctx.m.figura, giro=0.4)
    return k, "La montaña de piedras"


def forma_1C(ctx):
    """El montón habitado: un montón de piedra suelta sobre una caja de madera de queñua, con una boca baja."""
    k = 1 / 20
    ped = ctx.pedrera()
    C.monton(ped, sobre(ctx, 0, 0), 2.5 * k, 2.2 * k, 0.32 * k, ctx.r, hueco=(math.radians(270), 0.75, 1.1 * k), z0=ctx.zc)
    # la caja de madera, que queda como forro de la cámara y asoma por la boca
    for (c, d) in (((0, -1.0, 0.55), (1.0, 0.08, 1.1)), ((0, -1.0, 1.12), (1.0, 0.9, 0.06)),
                   ((-0.5, -1.0, 0.55), (0.06, 0.9, 1.1)), ((0.5, -1.0, 0.55), (0.06, 0.9, 1.1))):
        pass
    for x in (-0.42, 0.42):
        C.caja(sobre(ctx, x * k, -2.0 * k, 0.45 * k), (0.06 * k, 1.4 * k, 0.9 * k), ctx.m.palo, "forro")
    C.caja(sobre(ctx, 0, -2.0 * k, 0.93 * k), (0.9 * k, 1.4 * k, 0.06 * k), ctx.m.palo, "dintel")
    C.caja(sobre(ctx, 0, -1.4 * k, 0.45 * k), (0.8 * k, 0.05 * k, 0.9 * k), C.mat_liso("oscuro", (0.02, 0.018, 0.015)), "fondo")
    C.figura_madera(sobre(ctx, 1.4 * k, -3.2 * k), ctx.m.figura, giro=0.9, pose="cuclillas")
    return k, "El montón habitado"


# ----------------------------------------------------------------------------------------------------------------
# Prueba 2. El relleno
# ----------------------------------------------------------------------------------------------------------------

def pirca_tramo(ctx, x0, largo, alto, base, cima, cara, relleno, k, ped, ped_fina, cortada=True):
    """Un tramo de pirca de doble cara a lo largo de x, con el extremo (+x) cortado para ver el relleno."""
    z = 0.0
    while z < alto - 0.05:
        hz = ctx.r.uniform(0.17, 0.26)
        tal = (base - cima) / 2 * (z + hz / 2) / alto
        for lado in (-1, 1):
            y = lado * (base / 2 - tal - cara / 2)
            C.hilada_recta(ped, sobre(ctx, x0 * k, y * k)[:2], sobre(ctx, (x0 + largo) * k, y * k)[:2], ctx.zc + z * k,
                           hz * k, cara * k * 1.1, ctx.r, largo=(1.1, 2.2))
        ancho = base - 2 * tal - 2 * cara
        if relleno == "piedra":
            for _ in range(int(largo / 0.07)):
                s = ctx.r.uniform(0.04, 0.075)
                ped_fina.poner(sobre(ctx, (x0 + ctx.r.uniform(0, largo)) * k, ctx.r.uniform(-ancho / 2, ancho / 2) * k,
                                     (z + ctx.r.uniform(0.02, hz)) * k), s * k)
        elif relleno == "tierra":
            C.caja(sobre(ctx, (x0 + largo / 2) * k, 0, (z + hz / 2) * k), (largo * k, ancho * k, hz * k), ctx.m.tierra,
                   "relleno")
        z += hz


def forma_2A(ctx):
    """El tramo de prueba: las tres variantes de la maqueta 1:5, con el extremo abierto."""
    k = 1 / 5
    ped, fina = ctx.pedrera(), ctx.pedrera("fina")
    for i, rel in enumerate(("piedra", "tierra", None)):
        y0 = (i - 1) * 1.9
        ctx_y = y0
        z = 0.0
        alto, base, cima, cara = 1.2, 0.6, 0.5, 0.15
        while z < alto - 0.05:
            hz = ctx.r.uniform(0.17, 0.26)
            tal = (base - cima) / 2 * (z + hz / 2) / alto
            for lado in (-1, 1):
                y = y0 + lado * (base / 2 - tal - cara / 2)
                C.hilada_recta(ped, ((-1.0) * k, y * k), (1.0 * k, y * k), ctx.zc + z * k, hz * k, cara * k * 1.1, ctx.r,
                               largo=(1.1, 2.2))
            ancho = base - 2 * tal - 2 * cara
            if rel == "piedra":
                for _ in range(26):
                    s = ctx.r.uniform(0.04, 0.075)
                    fina.poner(((ctx.r.uniform(-1, 1)) * k, (y0 + ctx.r.uniform(-ancho / 2, ancho / 2)) * k,
                                ctx.zc + (z + ctx.r.uniform(0.02, hz)) * k), s * k)
            elif rel == "tierra":
                C.caja((0, y0 * k, ctx.zc + (z + hz / 2) * k), (2.0 * k, ancho * k, hz * k), ctx.m.tierra, "relleno")
            z += hz
    C.figura_madera(sobre(ctx, 1.5 * k, -2.6 * k), ctx.m.figura, alto=1.65 * k, giro=2.6)
    return k, "El tramo de prueba", dict(elevacion=42, acimut=-55, aire=1.3)


def forma_2B(ctx):
    """Pilares de mitad y mitad: capas de piedra y de tierra apisonada que cargan un techo pesado de ichu."""
    k = 1 / 20
    ped = ctx.pedrera()
    lado, alto_p, P = 4.0, 2.4, 0.8
    for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        cx, cy = sx * lado / 2, sy * lado / 2
        z = 0.0
        capa = 0
        while z < alto_p - 0.01:
            h = 0.22
            if capa % 2 == 0:
                C.caja(sobre(ctx, cx * k, cy * k, (z + h / 2) * k), (P * k, P * k, h * k), ctx.m.tierra, "tierra")
            else:
                for i in range(3):
                    for j in range(3):
                        ped.poner(sobre(ctx, (cx + (i - 1) * 0.26) * k, (cy + (j - 1) * 0.26) * k, (z + 0.07) * k),
                                  0.3 * k, aplanar=0.55)
            z += h
            capa += 1
    zt = alto_p
    techo = C.tronco(sobre(ctx, 0, 0, zt * k), (lado / 2 + 0.9) * k, 0.35 * k, 2.6 * k, ctx.m.adobe, lados=4,
                     abierto_arriba=True)
    C.paja_sobre(techo, ctx.m.paja, densidad=900000, largo=(0.022, 0.034), ancho=0.0007, semilla=5, capa=0.2 * k)
    C.figura_madera(sobre(ctx, 0.4 * k, -3.3 * k), ctx.m.figura, giro=0.2)
    return k, "Pilares de mitad y mitad"


def forma_2C(ctx):
    """El corral cortado: un corral redondo de pirca de doble cara, cortado para que el relleno sea fachada."""
    k = 1 / 20
    ped, fina = ctx.pedrera(), ctx.pedrera("fina")
    R, base, alto, cara = 3.0, 0.7, 1.4, 0.2
    a_corte = (math.radians(200), math.radians(320))
    z = 0.0
    while z < alto - 0.05:
        hz = ctx.r.uniform(0.18, 0.26)
        for radio in (R - cara / 2, R - base + cara / 2):
            n = int(2 * math.pi * radio / 0.36)
            for i in range(n):
                a = 2 * math.pi * i / n + (0.5 / n if int(z * 10) % 2 else 0)
                if a_corte[0] < a < a_corte[1]:
                    continue
                ped.poner(sobre(ctx, radio * math.cos(a) * k, radio * math.sin(a) * k, (z + hz / 2) * k), 0.36 * k,
                          rot=(0, 0, a + math.pi / 2), aplanar=hz / 0.3)
        for i in range(140):
            a = ctx.r.uniform(0, 2 * math.pi)
            if a_corte[0] < a < a_corte[1]:
                continue
            rr = ctx.r.uniform(R - base + cara, R - cara)
            fina.poner(sobre(ctx, rr * math.cos(a) * k, rr * math.sin(a) * k, (z + ctx.r.uniform(0, hz)) * k), 0.07 * k)
        z += hz
    # las dos caras del corte, en tierra apisonada que contiene el relleno
    for a in a_corte:
        c = (R - base / 2)
        C.caja(sobre(ctx, c * math.cos(a) * k, c * math.sin(a) * k, alto / 2 * k), (base * k, 0.06 * k, alto * k),
               ctx.m.tierra, "corte", rot=(0, 0, a + math.pi / 2))
    C.figura_madera(sobre(ctx, 0.5 * k, -0.3 * k), ctx.m.figura, giro=1.0)
    return k, "El corral cortado"


# ----------------------------------------------------------------------------------------------------------------
# Prueba 3. El dintel
# ----------------------------------------------------------------------------------------------------------------

BL, BA, BH = 0.40, 0.25, 0.12          # bloque de champa (proyecto)


def bloque_champa(ctx, centro, dims, rot_z=0.0):
    ob = C.caja(centro, dims, ctx.m.champa, "champa", rot=(ctx.r.uniform(-0.03, 0.03), ctx.r.uniform(-0.03, 0.03),
                                                            rot_z + ctx.r.uniform(-0.04, 0.04)), bisel=min(dims) * 0.12)
    return ob


def forma_3A(ctx):
    """El paso: un muro de champa con una abertura de hiladas voladas, a la altura de quien se arrodilla."""
    k = 1 / 10
    ab, jamba, vu, largo_muro, alto_muro = 0.6, 0.6, 0.10, 3.0, 1.44
    n_j = int(jamba / BH)
    for i in range(int(alto_muro / BH)):
        z = i * BH
        v = 0 if i < n_j else min((i - n_j + 1) * vu, ab / 2)
        x = -largo_muro / 2 + (BL / 2 if i % 2 else 0)
        while x < largo_muro / 2 - 0.05:
            x1 = min(x + BL, largo_muro / 2)
            if x1 <= -ab / 2 + v or x >= ab / 2 - v:
                a, b = x, x1
            elif x < -ab / 2 + v:
                a, b = x, -ab / 2 + v
            else:
                a, b = ab / 2 - v, x1
            if b - a > 0.05:
                for y in (-0.25, 0.25):
                    bloque_champa(ctx, sobre(ctx, (a + b) / 2 * k, y * k, (z + BH / 2) * k), ((b - a - 0.01) * k, BA * k, (BH - 0.008) * k))
            x = x1
    C.figura_madera(sobre(ctx, 0.15 * k, -0.9 * k), ctx.m.figura, alto=1.65 * k, giro=math.pi / 2, pose="rodillas")
    return k, "El paso"


def forma_3B(ctx):
    """La celda volada: planta cuadrada de champa, muros inclinados por fuera y hiladas voladas por dentro hasta un óculo."""
    k = 1 / 20
    L0, H = 4.0, 4.4
    hiladas = int(H / BH)
    for i in range(hiladas):
        z = i * BH
        fuera = L0 / 2 - z * math.tan(math.radians(12))          # muro inclinado unos 78°
        dentro = max(0.25, (L0 / 2 - 0.6) - max(0, z - 1.1) * 0.62)
        espesor = fuera - dentro
        if espesor < 0.15:
            break
        for lado in range(4):
            ang = lado * math.pi / 2
            n = max(1, int(2 * fuera / BL))
            for j in range(n):
                t = -fuera + (j + 0.5 + (0.5 if i % 2 else 0)) * 2 * fuera / n
                if t > fuera:
                    continue
                if lado == 3 and abs(t) < 0.35 and z < 0.96:
                    continue
                cx, cy = (fuera - espesor / 2), t
                x = cx * math.cos(ang) - cy * math.sin(ang)
                y = cx * math.sin(ang) + cy * math.cos(ang)
                bloque_champa(ctx, sobre(ctx, x * k, y * k, (z + BH / 2) * k),
                              (espesor * k, (2 * fuera / n - 0.01) * k, (BH - 0.008) * k), rot_z=ang)
    C.figura_madera(sobre(ctx, 0.6 * k, -3.0 * k), ctx.m.figura, giro=0.3)
    return k, "La celda volada"


def forma_3C(ctx):
    """El umbral hundido: un lindero de pirca con un paso volado al fondo de una zanja; la tierra sacada, al lado."""
    k = 1 / 20
    ped = ctx.pedrera()
    base = C.caja(sobre(ctx, 0, 0, 0.3 * k), (9.0 * k, 6.0 * k, 0.6 * k), ctx.m.tierra, "terreno")
    corte = C.caja(sobre(ctx, 0, -1.6 * k, 0.45 * k), (0.9 * k, 3.4 * k, 0.6 * k), ctx.m.tierra, "zanja")
    md = base.modifiers.new("zanja", 'BOOLEAN'); md.object = corte; md.operation = 'DIFFERENCE'
    corte.hide_render = True
    z0 = 0.6
    for lado in (-1, 1):
        x_a, x_b = lado * 0.45, lado * 4.4
        z = 0.0
        while z < 1.3:
            hz = ctx.r.uniform(0.18, 0.25)
            for y in (0.1, -0.1):
                C.hilada_recta(ped, (min(x_a, x_b) * k, y * k), (max(x_a, x_b) * k, y * k), ctx.zc + (z0 + z) * k,
                               hz * k, 0.3 * k, ctx.r)
            z += hz
    # dintel volado sobre la zanja
    for i, v in enumerate((0.0, 0.15, 0.3)):
        for lado in (-1, 1):
            ped.poner(sobre(ctx, lado * (0.45 - v) * k, 0, (z0 + 0.0 + i * 0.2 + 0.1) * k), 0.5 * k, rot=(0, 0, 0),
                      aplanar=0.4)
    C.monton(ped, sobre(ctx, 2.6 * k, -2.0 * k), 1.0 * k, 0.6 * k, 0.25 * k, ctx.r, z0=ctx.zc + z0 * k)
    C.figura_madera(sobre(ctx, 0, -2.4 * k, 0.0), ctx.m.figura, giro=0.0)
    return k, "El umbral hundido"


# ----------------------------------------------------------------------------------------------------------------
# Prueba 4. La p'ira
# ----------------------------------------------------------------------------------------------------------------

def pares(ctx, y_lista, ancho, z_muro, pend, k, r=0.04):
    xr = ancho / 2
    for y in y_lista:
        for lado in (0, 1):
            xa = -xr if lado == 0 else xr
            xb = 0.22 if lado == 0 else -0.22
            C.palo(sobre(ctx, xa * k, y * k, z_muro * k), sobre(ctx, xb * k, y * k, (z_muro + (xr + 0.22) * math.tan(pend)) * k),
                   r * k, ctx.m.palo)


def forma_4A(ctx):
    """La faja sobre los pares: una faja de 2,5 × 0,7 m sobre dos pares de cabrios, y tres muestras de huella."""
    k = 1 / 5
    pend = math.radians(44)
    for y in (-0.55, 0.55):
        pass
    for x in (-0.95, 0.95):
        C.caja(sobre(ctx, x * k, 0, 0.06 * k), (0.25 * k, 1.1 * k, 0.12 * k), ctx.m.adobe, "adobe")
    pares(ctx, (-0.35, 0.35), 1.9, 0.12, pend, k, r=0.035)
    xr = 0.95
    zr = 0.12 + xr * math.tan(pend)
    largo = (xr / math.cos(pend))
    ob = C.caja(sobre(ctx, -xr / 2 * k, 0, (0.12 + zr) / 2 * k + 0.05 * k), (largo * k, 0.7 * k, 0.05 * k), ctx.m.barro, "faja",
                rot=(0, -pend, 0), bisel=0.01 * k)
    for i, x in enumerate((-0.2, 0.7, 1.6)):
        C.caja(sobre(ctx, (x - 0.3) * k, -1.25 * k, 0.025 * k), (0.7 * k, 0.7 * k, 0.05 * k), ctx.m.barro, "muestra",
               rot=(0, 0, ctx.r.uniform(-0.1, 0.1)), bisel=0.01 * k)
    C.figura_madera(sobre(ctx, 1.7 * k, 0.6 * k), ctx.m.figura, alto=1.65 * k, giro=3.6)
    return k, "La faja sobre los pares"


def forma_4B(ctx):
    """El techo a medio subir: una mitad de las veinte fajas ya en la armadura, la otra todavía en el suelo."""
    k = 1 / 20
    W, Lg, Hm = 3.3, 5.75, 2.0
    pend = math.radians(44)
    for (cx, cy, dx, dy) in ((0, -Lg / 2 + 0.2, W, 0.4), (0, Lg / 2 - 0.2, W, 0.4), (-W / 2 + 0.2, 0, 0.4, Lg),
                             (W / 2 - 0.2, 0, 0.4, Lg)):
        C.caja(sobre(ctx, cx * k, cy * k, Hm / 2 * k), (dx * k, dy * k, Hm * k), ctx.m.adobe, "muro")
    ys = [-Lg / 2 + 0.15 + i * (Lg - 0.3) / 8 for i in range(9)]
    pares(ctx, ys, W, Hm, pend, k)
    xr = W / 2
    largo = 2.5
    for i in range(10):                              # fajas ya subidas, del lado oeste
        y = -3.5 + 0.7 * i + 0.35
        if abs(y) > Lg / 2 + 0.6:
            continue
        C.caja(sobre(ctx, -xr / 2 * k - 0.02 * k, y * k, (Hm + xr * math.tan(pend) / 2 + 0.08) * k),
               (largo * k, 0.72 * k, 0.05 * k), ctx.m.barro, "faja", rot=(0, -pend, 0))
    for i in range(10):                              # las demás, en el suelo, donde se hizo la p'ira
        C.caja(sobre(ctx, (4.4 + 1.25) * k, (-3.5 + 0.7 * i + 0.35) * k, 0.025 * k), (2.5 * k, 0.68 * k, 0.05 * k),
               ctx.m.barro, "faja_suelo", rot=(0, 0, ctx.r.uniform(-0.015, 0.015)))
    C.figura_madera(sobre(ctx, 3.6 * k, -4.4 * k), ctx.m.figura, giro=0.6)
    return k, "El techo a medio subir"


def forma_4C(ctx):
    """El pajar levantado: un techo pesado de ichu, de planta cuadrada, sobre palos finos y un piso excavado."""
    k = 1 / 20
    base = C.caja(sobre(ctx, 0, 0, 0.4 * k), (10.0 * k, 10.0 * k, 0.8 * k), ctx.m.yeso, "base")
    pozo = C.caja(sobre(ctx, 0, 0, 0.5 * k), (5.0 * k, 5.0 * k, 0.8 * k), ctx.m.yeso, "pozo")
    zanja = C.caja(sobre(ctx, 0, -4.0 * k, 0.5 * k), (0.9 * k, 4.0 * k, 0.8 * k), ctx.m.yeso, "zanja")
    for c in (pozo, zanja):
        md = base.modifiers.new("hueco", 'BOOLEAN'); md.object = c; md.operation = 'DIFFERENCE'; c.hide_render = True
    zb = 0.8
    h_palo = 1.2
    for i in range(12):
        a = 2 * math.pi * i / 12
        x, y = 2.7 * math.cos(a), 2.7 * math.sin(a)
        C.palo(sobre(ctx, x * k, y * k, zb * k), sobre(ctx, x * k, y * k, (zb + h_palo) * k), 0.05 * k, ctx.m.palo)
    techo = C.tronco(sobre(ctx, 0, 0, (zb + h_palo) * k), 3.3 * k, 0.4 * k, 4.2 * k, ctx.m.adobe, lados=4,
                     abierto_arriba=True)
    C.paja_sobre(techo, ctx.m.paja, densidad=900000, largo=(0.022, 0.034), ancho=0.0007, semilla=9, capa=0.2 * k)
    C.figura_madera(sobre(ctx, 0.3 * k, -4.8 * k, 0.3 * k), ctx.m.figura, giro=0.1)
    return k, "El pajar levantado"


# ----------------------------------------------------------------------------------------------------------------
# Prueba 5. El fogón
# ----------------------------------------------------------------------------------------------------------------

def forma_5A(ctx):
    """La chujlla de Enquelga a 1:10: muros de adobe sobre cimiento de piedra, techo de paja, puerta al este."""
    k = 1 / 10
    W, Lg, Hm, e = 3.3, 5.75, 2.0, 0.4
    ped = ctx.pedrera()
    for (p0, p1) in (((-W / 2, -Lg / 2), (W / 2, -Lg / 2)), ((-W / 2, Lg / 2), (W / 2, Lg / 2)),
                     ((-W / 2, -Lg / 2), (-W / 2, Lg / 2)), ((W / 2, -Lg / 2), (W / 2, Lg / 2))):
        C.hilada_recta(ped, (p0[0] * k, p0[1] * k), (p1[0] * k, p1[1] * k), ctx.zc, 0.3 * k, e * k, ctx.r, largo=(1.0, 1.8))
    zc = 0.3
    puerta = (-0.35, 0.35, 1.5)
    for (cx, cy, dx, dy, lado) in ((0, -Lg / 2 + e / 2, W, e, "s"), (0, Lg / 2 - e / 2, W, e, "n"),
                                   (-W / 2 + e / 2, 0, e, Lg, "o")):
        C.caja(sobre(ctx, cx * k, cy * k, (zc + (Hm - zc) / 2) * k), (dx * k, dy * k, (Hm - zc) * k), ctx.m.adobe, "muro")
    for (y0, y1) in ((-Lg / 2, puerta[0]), (puerta[1], Lg / 2)):      # muro este con la puerta
        C.caja(sobre(ctx, (W / 2 - e / 2) * k, (y0 + y1) / 2 * k, (zc + (Hm - zc) / 2) * k), (e * k, (y1 - y0) * k, (Hm - zc) * k),
               ctx.m.adobe, "muro_e")
    C.caja(sobre(ctx, (W / 2 - e / 2) * k, 0, (puerta[2] + (Hm - puerta[2]) / 2) * k), (e * k, 0.7 * k, (Hm - puerta[2]) * k),
           ctx.m.adobe, "dintel")
    pend = math.radians(44)
    techo = C.tronco(sobre(ctx, 0, 0, Hm * k), 1.0, 1.0, 1.0, ctx.m.adobe, lados=4)   # se reemplaza abajo
    import bpy
    bpy.data.objects.remove(techo)
    import bmesh
    bm = bmesh.new()
    a, xr, zr = 0.3, W / 2, Hm + (W / 2) * math.tan(pend)
    pts = [(-xr - a, -Lg / 2 - 0.3, Hm - a * math.tan(pend)), (0, -Lg / 2 - 0.3, zr), (xr + a, -Lg / 2 - 0.3, Hm - a * math.tan(pend)),
           (xr + a, Lg / 2 + 0.3, Hm - a * math.tan(pend)), (0, Lg / 2 + 0.3, zr), (-xr - a, Lg / 2 + 0.3, Hm - a * math.tan(pend))]
    vs = [bm.verts.new((p[0] * k, p[1] * k, ctx.zc + p[2] * k)) for p in pts]
    bm.faces.new((vs[0], vs[1], vs[4], vs[5])); bm.faces.new((vs[1], vs[2], vs[3], vs[4]))
    techo = C.objeto("techo", C.malla_de_bm(bm, "techo", ctx.m.adobe))
    md = techo.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = 0.25 * k
    C.paja_sobre(techo, ctx.m.paja, densidad=500000, largo=(0.04, 0.06), ancho=0.0011, semilla=11, capa=0.2 * k)
    C.figura_madera(sobre(ctx, (W / 2 + 1.2) * k, -1.6 * k), ctx.m.figura, alto=1.65 * k, giro=2.2, pose="cuclillas")
    return k, "La chujlla de Enquelga"


def forma_5B(ctx):
    """La casa partida: un bloque de tierra apisonada ahuecado a la medida del cuerpo en cuclillas, abierto en dos."""
    k = 1 / 20
    W, Lg, H = 3.3, 5.75, 2.0
    hueco_h = 1.25
    for lado in (-1, 1):                             # se parte a lo largo; la mitad este se corre al sur, como la piedra partida
        x = lado * (W / 4 + 0.9)
        y = -3.4 if lado == 1 else 0.0
        blq = C.caja(sobre(ctx, x * k, y * k, H / 2 * k), (W / 2 * k, Lg * k, H * k), ctx.m.tierra, "mitad")
        hc = C.caja(sobre(ctx, (x - lado * W / 4) * k, y * k, (0.15 + hueco_h / 2) * k), ((W / 2 - 0.4) * 2 * k, (Lg - 0.9) * k,
                                                                                       hueco_h * k), ctx.m.tierra, "hueco")
        md = blq.modifiers.new("hueco", 'BOOLEAN'); md.object = hc; md.operation = 'DIFFERENCE'; hc.hide_render = True
    ped = ctx.pedrera()                              # el fogón, en la mitad oeste
    for dy in (-0.16, 0.16):
        for j in range(3):
            ped.poner(sobre(ctx, (-W / 4 - 0.9 + 0.55 + dy) * k, (j - 1) * 0.2 * k, 0.2 * k), 0.18 * k, aplanar=0.8)
    C.figura_madera(sobre(ctx, (-W / 4 - 0.5) * k, 1.0 * k, 0.15 * k), ctx.m.figura, giro=-0.6, pose="cuclillas")
    return k, "La casa partida", dict(acimut=62, elevacion=20)


def forma_5C(ctx):
    """El cono del fogón: un fogón hundido bajo un cono de ichu sobre palos, con el t'uju al noreste y el humo arriba."""
    k = 1 / 20
    base = C.caja(sobre(ctx, 0, 0, 0.35 * k), (9.0 * k, 9.0 * k, 0.7 * k), ctx.m.yeso, "base")
    import bmesh
    import bpy
    pozo = C.tronco(sobre(ctx, 0, 0, 0.05 * k), 1.6 * k, 1.6 * k, 0.9 * k, ctx.m.yeso, lados=40)
    zanja = C.caja(sobre(ctx, 0, -3.1 * k, 0.45 * k), (0.8 * k, 3.2 * k, 0.7 * k), ctx.m.yeso, "zanja")
    for c in (pozo, zanja):
        md = base.modifiers.new("hueco", 'BOOLEAN'); md.object = c; md.operation = 'DIFFERENCE'; c.hide_render = True
    ped = ctx.pedrera()
    for dx in (-0.16, 0.16):
        for j in range(3):
            ped.poner(sobre(ctx, dx * k, (j - 1) * 0.2 * k, 0.12 * k), 0.17 * k, aplanar=0.8)
    zb = 0.7
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.2
        x, y = 2.1 * math.cos(a), 2.1 * math.sin(a)
        C.palo(sobre(ctx, x * k, y * k, zb * k), sobre(ctx, x * k, y * k, (zb + 1.3) * k), 0.05 * k, ctx.m.palo)
    cono = C.tronco(sobre(ctx, 0, 0, (zb + 1.3) * k), 2.6 * k, 0.3 * k, 3.8 * k, ctx.m.adobe, lados=40, abierto_arriba=True)
    C.paja_sobre(cono, ctx.m.paja, densidad=900000, largo=(0.022, 0.034), ancho=0.0007, semilla=13, capa=0.2 * k)
    # el t'uju: un tubo de barro que atraviesa el flanco noreste, apuntado al sol del 21 de junio a las 10
    s = C.vector_sol()
    centro = Vector((1.2 * 0.7071, 1.2 * 0.7071, zb + 1.3 + 1.6))
    C.palo(sobre(ctx, *(centro - s * 0.6) * k) if False else ((centro - s * 0.6) * k + Vector((0, 0, ctx.zc))),
           (centro + s * 0.9) * k + Vector((0, 0, ctx.zc)), 0.16 * k, ctx.m.adobe, lados=12, nombre="tuju")
    C.figura_madera(sobre(ctx, 0.2 * k, -3.6 * k, 0.15 * k), ctx.m.figura, giro=0.0)
    return k, "El cono del fogón"



# ----------------------------------------------------------------------------------------------------------------
# Las formas elegidas por el autor (27 de noviembre): recomposiciones de las anteriores
# ----------------------------------------------------------------------------------------------------------------

def forma_E1(ctx):
    """La montaña habitada: el cono de piedra de 1B, más chato, con la entrada forrada de queñua de 1C."""
    k = 1 / 20
    ped = ctx.pedrera()
    R0, R1, H = 3.6, 0.32, 2.6
    boca = math.radians(270)                       # la boca mira al sur
    capas = int(H / 0.2)
    for i in range(capas):
        z = i * H / capas
        rr = R0 + (R1 - R0) * z / H
        m = int(2 * math.pi * rr / 0.33)
        fase = ctx.r.uniform(0, 6.28)
        for j in range(m):
            a = fase + 2 * math.pi * j / m
            da = abs(((a - boca) + math.pi) % (2 * math.pi) - math.pi)
            if z < 1.05 and da * rr < 0.62:
                continue
            ped.poner(sobre(ctx, rr * math.cos(a) * k, rr * math.sin(a) * k, (z + 0.09) * k), 0.35 * k,
                      rot=(ctx.r.uniform(-0.12, 0.12), -math.radians(16), a), aplanar=0.55)
    C.tronco(sobre(ctx, 0, 0), (R0 - 0.4) * k, (R1 - 0.08) * k, H * 0.98 * k, C.mat_liso("sombra", (0.04, 0.035, 0.03)),
             lados=32, abierto_arriba=True)
    # la entrada de 1C: una caja de queñua que atraviesa el muro y asoma
    y0 = -(R0 - 0.2)
    for x in (-0.48, 0.48):
        C.caja(sobre(ctx, x * k, y0 * k, 0.5 * k), (0.07 * k, 1.5 * k, 1.0 * k), ctx.m.palo, "forro")
    C.caja(sobre(ctx, 0, y0 * k, 1.03 * k), (1.03 * k, 1.5 * k, 0.07 * k), ctx.m.palo, "dintel")
    C.caja(sobre(ctx, 0, (y0 + 0.9) * k, 0.5 * k), (0.9 * k, 0.05 * k, 1.0 * k), C.mat_liso("oscuro", (0.02, 0.018, 0.015)), "fondo")
    C.figura_madera(sobre(ctx, 1.3 * k, (y0 - 1.6) * k), ctx.m.figura, giro=0.9, pose="cuclillas")
    return k, "La montaña habitada"


def corral_techado(ctx, techo):
    """El corral de 2C y, encima, flotando sobre palos de queñua, el techo de ichu de 4C (pirámide) o de 5C (cono)."""
    k = 1 / 20
    ped, fina = ctx.pedrera(), ctx.pedrera("fina")
    R, base, alto, cara = 3.0, 0.7, 1.4, 0.2
    a_corte = (math.radians(225), math.radians(315))
    z = 0.0
    while z < alto - 0.05:
        hz = ctx.r.uniform(0.18, 0.26)
        for radio in (R - cara / 2, R - base + cara / 2):
            n = int(2 * math.pi * radio / 0.36)
            for i in range(n):
                a = 2 * math.pi * i / n + (0.5 / n if int(z * 10) % 2 else 0)
                if a_corte[0] < a < a_corte[1]:
                    continue
                ped.poner(sobre(ctx, radio * math.cos(a) * k, radio * math.sin(a) * k, (z + hz / 2) * k), 0.36 * k,
                          rot=(0, 0, a + math.pi / 2), aplanar=hz / 0.3)
        for i in range(120):
            a = ctx.r.uniform(0, 2 * math.pi)
            if a_corte[0] < a < a_corte[1]:
                continue
            rr = ctx.r.uniform(R - base + cara, R - cara)
            fina.poner(sobre(ctx, rr * math.cos(a) * k, rr * math.sin(a) * k, (z + ctx.r.uniform(0, hz)) * k), 0.07 * k)
        z += hz
    for a in a_corte:
        c = (R - base / 2)
        C.caja(sobre(ctx, c * math.cos(a) * k, c * math.sin(a) * k, alto / 2 * k), (base * k, 0.06 * k, alto * k),
               ctx.m.tierra, "corte", rot=(0, 0, a + math.pi / 2))
    z_alero = 2.3                                  # el techo flota 90 cm sobre la pirca
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        x, y = 2.0 * math.cos(a), 2.0 * math.sin(a)
        C.palo(sobre(ctx, x * k, y * k), sobre(ctx, x * k, y * k, z_alero * k), 0.06 * k, ctx.m.palo)
    if techo == "piramide":
        t = C.tronco(sobre(ctx, 0, 0, z_alero * k), 3.3 * k, 0.35 * k, 3.2 * k, ctx.m.adobe, lados=4, abierto_arriba=True)
    else:
        t = C.tronco(sobre(ctx, 0, 0, z_alero * k), 3.4 * k, 0.3 * k, 3.4 * k, ctx.m.adobe, lados=40, abierto_arriba=True)
    C.paja_sobre(t, ctx.m.paja, densidad=900000, largo=(0.022, 0.034), ancho=0.0007, semilla=17, capa=0.2 * k)
    C.figura_madera(sobre(ctx, 0.2 * k, -3.6 * k), ctx.m.figura, giro=0.1)
    return k


def forma_E2P(ctx):
    """El corral techado, con el techo de pirámide de 4C."""
    return corral_techado(ctx, "piramide"), "El corral techado (pirámide)", dict(elevacion=11, acimut=-28)


def forma_E2C(ctx):
    """El corral techado, con el techo de cono de 5C."""
    return corral_techado(ctx, "cono"), "El corral techado (cono)", dict(elevacion=11, acimut=-28)


# ----------------------------------------------------------------------------------------------------------------
# Las otras tres exploraciones (27 de noviembre): E3, la torre de champa; E4, la chullpa; E5, la casa de la bóveda
# ----------------------------------------------------------------------------------------------------------------

def caras_de_piedra(ctx, ped, x0, x1, y0, y1, z, hz, cara, k, sin=(), largo=(1.1, 2.2)):
    """Una hilada de piedra en las cuatro caras de un rectángulo en planta [x0, x1] × [y0, y1], en metros reales.
    sin: tramos sin piedra, como (lado, t0, t1), con lado en «s», «n», «o» o «e» y t medido a lo largo de esa cara."""
    lados = {"s": ((x0, y0 + cara / 2), (x1, y0 + cara / 2)), "n": ((x0, y1 - cara / 2), (x1, y1 - cara / 2)),
             "o": ((x0 + cara / 2, y0 + cara), (x0 + cara / 2, y1 - cara)),
             "e": ((x1 - cara / 2, y0 + cara), (x1 - cara / 2, y1 - cara))}
    for lado, (p0, p1) in lados.items():
        horizontal = lado in "sn"
        a, b = (p0[0], p1[0]) if horizontal else (p0[1], p1[1])
        tramos, cur = [], a
        for (t0, t1) in sorted((t0, t1) for (l, t0, t1) in sin if l == lado):
            if t0 > cur:
                tramos.append((cur, min(t0, b)))
            cur = max(cur, t1)
        if cur < b:
            tramos.append((cur, b))
        for (ta, tb) in tramos:
            if tb - ta < 0.1:
                continue
            q0, q1 = ((ta, p0[1]), (tb, p0[1])) if horizontal else ((p0[0], ta), (p0[0], tb))
            C.hilada_recta(ped, (q0[0] * k, q0[1] * k), (q1[0] * k, q1[1] * k), ctx.zc + z * k, hz * k, cara * k * 1.05,
                           ctx.r, largo=largo, exacto=True)


def nucleo(ctx, x0, x1, y0, y1, z0, z1, k, mat=None):
    """El relleno oculto de un muro o una pila, para que no se vea a través de las juntas."""
    return C.caja(sobre(ctx, (x0 + x1) / 2 * k, (y0 + y1) / 2 * k, (z0 + z1) / 2 * k),
                  ((x1 - x0) * k, (y1 - y0) * k, (z1 - z0) * k), mat or ctx.sombra, "nucleo")


def hilera_champa(ctx, a, b, fijo, z, eje, k, fase, sin=()):
    """Una hilera de bloques de champa a soga entre a y b, a lo largo de x (eje «x», con y = fijo) o de y (eje «y»).
    Los bloques se cortan en los extremos; sin: lista de valores de la coordenada donde falta un bloque."""
    t = a - fase * (BL + 0.012) / 2
    while t < b - 0.03:
        paso = ctx.r.uniform(0.3, 0.5) + 0.012          # la champa se corta a pala: ningún bloque es igual
        t0, t1 = max(t, a), min(t + paso, b)
        c = (t0 + t1) / 2
        if t1 - t0 > 0.06 and not any(abs(c - u) < paso / 2 for u in sin):
            dims = ((t1 - t0 - 0.012) * k, BA * k, (BH * ctx.r.uniform(0.85, 1.0) - 0.008) * k)
            f = fijo + ctx.r.uniform(-0.015, 0.015)
            if eje == "x":
                bloque_champa(ctx, (c * k, f * k, ctx.zc + (z + BH / 2) * k), dims)
            else:
                bloque_champa(ctx, (f * k, c * k, ctx.zc + (z + BH / 2) * k), dims, rot_z=math.pi / 2)
        t += paso


def forma_E3(ctx):
    """La torre de champa: un cuerpo de champa en hiladas delgadas sobre dos apoyos, una pirca y un montón; entre los dos,
    una V invertida de hiladas voladas por la que se pasa; lajas pasantes que asoman, y un techo de un agua de fajas de
    p'ira sobre palos de queñua atados a piedras hincadas en el muro (la chhaxwa de Bertonio)."""
    k = 1 / 20
    ped = ctx.pedrera()
    ctx.sombra = C.mat_liso("sombra", (0.035, 0.03, 0.026))
    X, Y = 1.5, 0.8                                  # medio largo y medio ancho de la torre (proyecto)
    ctx.m.champa = C.mat_tierra("champa_oscura", capas=False, escala_obj=14, claro=(0.10, 0.083, 0.06),
                                oscuro=(0.035, 0.03, 0.022), paja=True)
    Hp, g = 0.9, 0.5                                 # alto de los apoyos y medio paso entre ellos, arriba
    Hl, Hh = 4.2, 5.4                                # alto de la torre en el lado bajo y en el alto
    def tope(x):
        return Hl + (x + X) / (2 * X) * (Hh - Hl)
    # el apoyo oeste: una pirca de cuatro caras, con una cama de lajas
    for i in range(5):
        z = i * 0.18
        caras_de_piedra(ctx, ped, -X - 0.1, -g, -Y - 0.1, Y + 0.1, z, 0.18, 0.3, k, largo=(1.2, 2.4))
        nucleo(ctx, -X + 0.2, -g - 0.3, -Y + 0.2, Y - 0.2, z, z + 0.18, k)
    # el apoyo este: un montón de piedra suelta, ancho al pie, con la cima aplanada
    cx = (g + X) / 2
    for i in range(6):
        z = i * 0.15
        f = 1 - z / Hp
        rx, ry = (X - g) / 2 + 0.05 + 0.45 * f, Y + 0.1 + 0.45 * f
        m = int(2 * math.pi * math.sqrt((rx * rx + ry * ry) / 2) / 0.3)
        for j in range(m):
            a = 2 * math.pi * (j + ctx.r.uniform(-0.25, 0.25)) / m
            ped.poner(sobre(ctx, (cx + rx * math.cos(a)) * k, ry * math.sin(a) * k, (z + 0.08) * k), ctx.r.uniform(0.24, 0.36) * k,
                      rot=(ctx.r.uniform(-0.5, 0.5), ctx.r.uniform(-0.5, 0.5), ctx.r.uniform(0, 6.3)), aplanar=0.7)
    C.tronco(sobre(ctx, cx * k, 0), (X - g) / 2 * k * 1.25, (X - g) / 2 * k, Hp * 0.95 * k, ctx.sombra, lados=24).scale.y = 1.6
    for (x0, x1) in ((-X - 0.1, -g), (g, X + 0.1)):          # las camas de lajas
        for yy in (-0.6, 0.0, 0.6):
            C.hilada_recta(ped, (x0 * k, yy * k), (x1 * k, yy * k), ctx.zc + (Hp - 0.02) * k, 0.07 * k, 0.6 * k, ctx.r,
                           largo=(6.0, 9.0), exacto=True)
    # el cuerpo de champa: bloques de 40 × 25 × 12 cm a soga; abajo, dos patas con la V de hiladas voladas
    z0 = Hp + 0.05
    i = 0
    huecos_r = random.Random(41)
    while True:
        z = z0 + i * BH
        if z > Hh - 0.02:
            break
        w = g - 0.06 * (i + 1)
        fase = i % 2
        tramos = [(-X, -w), (w, X)] if w > 0.03 else [(-X, X)]
        sin = [huecos_r.uniform(-X, X) for _ in range(2)] if i > 12 and huecos_r.random() < 0.6 else []
        for (xa, xb) in tramos:
            xb_t = xb
            # los muros largos se acaban donde los corta el techo
            xs_ok = [x for x in (xa, xb) if tope(x) > z + BH * 0.5]
            if not xs_ok:
                continue
            x_ini = xa if tope(xa) > z + BH * 0.5 else -X + (z + BH * 0.5 - Hl) / (Hh - Hl) * 2 * X
            for yy in (-Y + BA / 2, Y - BA / 2):
                hilera_champa(ctx, max(xa, x_ini), xb_t, yy, z, "x", k, fase, sin=sin if yy < 0 else [])
            for xx in (xa + BA / 2, xb - BA / 2):
                if tope(xx) > z + BH * 0.5 and (xx < -X + 0.3 or xx > X - 0.3 or w > 0.03):
                    hilera_champa(ctx, -Y + BA, Y - BA, xx, z, "y", k, fase)
        i += 1
    nucleo(ctx, -X + BA, X - BA, -Y + BA, Y - BA, z0 + 8 * BH, Hl - 0.1, k)
    # lajas pasantes que asoman de la cara sur y de la norte
    for _ in range(26):
        xl = ctx.r.uniform(-X + 0.25, X - 0.25)
        zl = ctx.r.uniform(z0 + 1.4, tope(xl) - 0.5)
        zl = z0 + round((zl - z0) / BH) * BH
        for yy in ((-Y - 0.12,) if ctx.r.random() < 0.6 else (Y + 0.12,)):
            ped.poner(sobre(ctx, xl * k, yy * k, zl * k), ctx.r.uniform(0.4, 0.55) * k, rot=(0, 0, math.pi / 2 + ctx.r.uniform(-0.15, 0.15)),
                      aplanar=0.17)
    # el techo: palos de queñua de lado a lado, atados a piedras hincadas bajo cada extremo, y dos hileras de fajas
    th = math.atan((Hh - Hl) / (2 * X))
    for j in range(6):
        x = -X + 0.25 + j * 0.5
        zt = tope(x) + 0.06
        C.palo(sobre(ctx, x * k, -(Y + 0.28) * k, zt * k), sobre(ctx, x * k, (Y + 0.28) * k, zt * k), 0.06 * k, ctx.m.palo)
        for yy in (-Y - 0.1, Y + 0.1):
            ped.poner(sobre(ctx, x * k, yy * k, (zt - 0.42) * k), 0.34 * k, rot=(0, 0, math.pi / 2), aplanar=0.4)
    largo_t = (2 * X + 0.5) / math.cos(th)
    for fila, (s0, alza) in enumerate(((0.0, 0.0), (largo_t - 2.5, 0.05))):
        for yy in (-0.7, 0.0, 0.7):
            sm = s0 + 1.25
            xm = -X - 0.25 + sm * math.cos(th)
            zm = tope(-X - 0.25) + 0.12 + 0.03 + alza + sm * math.sin(th)
            C.caja(sobre(ctx, xm * k, yy * k, zm * k), (2.5 * k, 0.72 * k, 0.05 * k), ctx.m.barro, "faja",
                   rot=(ctx.r.uniform(-0.01, 0.01), -th, ctx.r.uniform(-0.012, 0.012)), bisel=0.01 * k)
    C.figura_madera(sobre(ctx, -0.15 * k, -0.2 * k), ctx.m.figura, alto=1.65 * k, giro=math.pi / 2)
    C.figura_madera(sobre(ctx, -(X + 0.9) * k, 0.3 * k), ctx.m.figura, alto=1.65 * k, giro=0.4)
    return k, "La torre de champa", dict(acimut=-24, elevacion=9, aire=1.06)


def forma_E4(ctx):
    """La chullpa: cuatro pilas de pirca que vuelan hacia los pasos, una cama de lajas, una hilada de piedra y una pirámide
    de adobitos de pie, en aparejo de librero, con una cornisa de ichu prensado y una boca baja al este."""
    k = 1 / 20
    ped = ctx.pedrera()
    ado = C.Adobera(ctx.m.adobe, n=12, semilla=21)
    ctx.sombra = C.mat_liso("sombra", (0.035, 0.03, 0.026))
    c, P, Hp, cara = 1.05, 1.2, 1.2, 0.3
    hz = 0.2
    for sx in (-1, 1):
        for sy in (-1, 1):
            for i in range(int(Hp / hz)):
                vuelo = 0.1 * max(0, i - 3)        # las dos últimas hiladas vuelan 10 cm hacia los pasos
                xs = sorted((sx * c - sx * (P / 2 + vuelo), sx * c + sx * P / 2))
                ys = sorted((sy * c - sy * (P / 2 + vuelo), sy * c + sy * P / 2))
                caras_de_piedra(ctx, ped, xs[0], xs[1], ys[0], ys[1], i * hz, hz, cara, k, largo=(1.0, 2.0))
                nucleo(ctx, xs[0] + cara, xs[1] - cara, ys[0] + cara, ys[1] - cara, i * hz, (i + 1) * hz, k)
    S = 2 * c + P
    z = Hp
    for j in range(6):                               # la cama de lajas, que cruza los pasos
        y = -S / 2 + (j + 0.5) * S / 6
        C.hilada_recta(ped, (-S / 2 * k, y * k), (S / 2 * k, y * k), ctx.zc + z * k, 0.1 * k, S / 6 * k * 0.98, ctx.r,
                       largo=(5.0, 8.0), exacto=True)
    z += 0.1
    caras_de_piedra(ctx, ped, -1.55, 1.55, -1.55, 1.55, z, 0.18, 0.3, k)   # la hilada de piedra bajo el adobe
    nucleo(ctx, -1.25, 1.25, -1.25, 1.25, z, z + 0.18, k)
    z += 0.18
    # la pirámide de adobitos de pie (Agüero Benites et al., 2015: 3 y 6); medidas del adobito: proyecto
    ha, mj, t, pr, g = 0.19, 0.02, 0.06, 0.14, 0.015
    S0, ret = 3.0, 0.062
    mortero = C.mat_tierra("mortero", capas=False, escala_obj=14, claro=(0.33, 0.27, 0.19), oscuro=(0.2, 0.16, 0.11))
    ichu = C.mat_tierra("ichu_prensado", capas=True, escala_obj=90, claro=(0.64, 0.55, 0.34), oscuro=(0.34, 0.27, 0.15))
    hiladas = 15
    for i in range(hiladas):
        s = S0 - 2 * i * ret
        C.caja(sobre(ctx, 0, 0, (z + mj / 2) * k), ((s + 0.01) * k, (s + 0.01) * k, mj * k), mortero, "mortero")
        z += mj
        zc = z + ha / 2
        nucleo(ctx, -s / 2 + pr * 0.9, s / 2 - pr * 0.9, -s / 2 + pr * 0.9, s / 2 - pr * 0.9, z, z + ha, k)
        for lado in ("s", "n", "o", "e"):
            largo_cara = s if lado in "sn" else s - 2 * pr
            m = int((largo_cara + g) / (t + g))
            paso = largo_cara / m
            for j in range(m):
                u = -largo_cara / 2 + (j + 0.5) * paso
                if lado == "e" and i < 2 and abs(u) < 0.24:
                    continue                         # la boca, al este y al nivel de la cama (Squier, 1877: 244)
                if lado == "e" and i == 2 and abs(u) < 0.36:
                    continue                         # aquí va el dintel
                if lado in "sn":
                    y = (-1 if lado == "s" else 1) * (s / 2 - pr / 2)
                    ado.poner(sobre(ctx, u * k, y * k, zc * k), (t * k, pr * k, ha * k))
                else:
                    x = (-1 if lado == "o" else 1) * (s / 2 - pr / 2)
                    ado.poner(sobre(ctx, x * k, u * k, zc * k), (pr * k, t * k, ha * k))
        if i == 2:                                   # el dintel de la boca, una laja
            C.caja(sobre(ctx, (s / 2 - pr / 2) * k, 0, zc * k), ((pr + 0.02) * k, 0.72 * k, ha * k), ctx.m.piedra,
                   "dintel", bisel=0.008 * k)
        z += ha
        if i == hiladas - 3:                         # la cornisa de ichu prensado (Squier, 1877: 243)
            C.caja(sobre(ctx, 0, 0, (z + 0.075) * k), ((s + 0.2) * k, (s + 0.2) * k, 0.15 * k), ichu, "cornisa",
                   bisel=0.01 * k)
            z += 0.15
    s = S0 - 2 * hiladas * ret
    C.caja(sobre(ctx, 0, 0, (z + 0.04) * k), ((s + 0.04) * k, (s + 0.04) * k, 0.08 * k), mortero, "tapa", bisel=0.01 * k)
    C.figura_madera(sobre(ctx, -2.3 * k, -2.2 * k), ctx.m.figura, alto=1.65 * k, giro=-0.3)
    C.figura_madera(sobre(ctx, 0.0, -1.2 * k), ctx.m.figura, alto=1.65 * k, giro=math.pi / 2, pose="cuclillas")
    return k, "La chullpa", dict(acimut=48, elevacion=12, aire=1.08)


def forma_E5(ctx):
    """La casa de la bóveda: la planta de la chujlla de Enquelga (5,75 × 3,30 m) dentro de un bloque de pirca en talud,
    cubierta por una bóveda de adobe por aproximación de hiladas, con una ranura al este y el t'uju al noreste."""
    k = 1 / 20
    ped = ctx.pedrera()
    ado = C.Adobera(ctx.m.adobe, n=12, semilla=31)
    ctx.sombra = C.mat_liso("sombra", (0.035, 0.03, 0.026))
    Li, Wi = 5.75, 3.30                              # el cuarto: la mediana de Šolc (2011 [1975]: 93-94)
    E0, Hw, cara = 0.9, 2.6, 0.32                    # espesor del muro al pie y alto del bloque: proyecto
    Lo, Wo = Li + 2 * E0, Wi + 2 * E0
    tal = math.tan(math.radians(10))
    ranura, puerta = 0.25, 1.3                       # la ranura: 50 cm, lo justo para un cuerpo; la puerta, 1,30 m
    zr, hz = 0.8, 0.2                                # arranque de la bóveda
    for i in range(int(round(Hw / hz))):
        z = i * hz
        d = tal * (z + hz / 2)
        caras_de_piedra(ctx, ped, -Lo / 2 + d, Lo / 2 - d, -Wo / 2 + d, Wo / 2 - d, z, hz, cara, k, sin=[("e", -ranura, ranura)])
        if z < zr:                                   # la cara de adentro, hasta el arranque
            caras_de_piedra(ctx, ped, -Li / 2 - cara, Li / 2 + cara, -Wi / 2 - cara, Wi / 2 + cara, z, hz, cara, k,
                            sin=[("e", -ranura, ranura)])
    # el relleno del muro y de los riñones de la bóveda, que carga las colas de las hiladas
    zf = 2.1
    A_ = (Lo - 2 * tal * Hw - 2 * cara - 0.1, Wo - 2 * tal * Hw - 2 * cara - 0.1)
    relleno = C.caja(sobre(ctx, 0, 0, zf / 2 * k), (A_[0] * k, A_[1] * k, zf * k), ctx.m.tierra, "relleno")
    cuarto = C.caja(sobre(ctx, 0, 0, Hw / 2 * k), ((Li - 0.02) * k, (Wi - 0.02) * k, (Hw + 1) * k), ctx.m.tierra, "cuarto")
    hueco = C.caja(sobre(ctx, Lo / 2 * k, 0, Hw / 2 * k), (Lo * k, 2 * ranura * k, (Hw + 1) * k), ctx.m.tierra, "ranura")
    for cort in (cuarto, hueco):
        md = relleno.modifiers.new("hueco", 'BOOLEAN'); md.object = cort; md.operation = 'DIFFERENCE'; cort.hide_render = True
    # la bóveda volada: cada hilada entra un poco más que la de abajo, de 7 cm al arranque a 13 cm junto a la clave
    hh, b = 0.11, 0.07 / 0.11
    a2H = (0.13 / 0.11 - b) / 2
    H = (Wi / 2 - 0.15) / (b + a2H)
    a2 = a2H / H
    n = int(round(H / hh)) + 1
    for i in range(n):
        h = i * hh
        r = max(0.15, Wi / 2 - b * h - a2 * h * h)
        m = int(Li / 0.205)
        paso = Li / m
        for j in range(m + 1):
            x = -Li / 2 + (j + 0.5 * (i % 2)) * paso
            ancho = paso - 0.012
            if x - paso / 2 < -Li / 2:
                x, ancho = -Li / 2 + paso / 4, paso / 2 - 0.012
            if x + paso / 2 > Li / 2 + 1e-6:
                if i % 2 == 0:
                    continue
                x, ancho = Li / 2 - paso / 4, paso / 2 - 0.012
            for lado in (-1, 1):
                ado.poner(sobre(ctx, x * k, lado * (r + 0.2) * k, (zr + h + hh / 2) * k),
                          (ancho * k, 0.40 * k, (hh - 0.01) * k), inclinar=0.006)
    zc_ = zr + n * hh
    # la clave: lajas que cierran la rendija de arriba; falta una sobre el fogón, por donde sale el humo
    x = -Li / 2 + 0.25
    while x < Li / 2 - 0.2:
        if abs(x) > 0.32:
            C.caja(sobre(ctx, x * k, 0, (zc_ + 0.04) * k), (0.44 * k, 0.75 * k, 0.08 * k), ctx.m.piedra, "laja",
                   rot=(ctx.r.uniform(-0.03, 0.03), ctx.r.uniform(-0.03, 0.03), ctx.r.uniform(-0.06, 0.06)), bisel=0.01 * k)
        x += 0.48
    # el tímpano de adobe que cierra la ranura sobre la puerta
    C.caja(sobre(ctx, (Li / 2 + 0.12) * k, 0, (puerta + (Hw - 0.1 - puerta) / 2) * k), (0.24 * k, (2 * ranura + 0.06) * k,
           (Hw - 0.1 - puerta) * k), ctx.m.adobe, "timpano")
    # el fogón al centro, bajo la laja que falta
    for dx in (-0.16, 0.16):
        for j in range(3):
            ped.poner(sobre(ctx, (j - 1) * 0.2 * k, dx * k, 0.09 * k), 0.17 * k, aplanar=0.8)
    # el t'uju: un tubo de 15 cm por la esquina noreste, apuntado al sol del 21 de junio a las 10
    s = C.vector_sol()
    p_in = Vector((Li / 2 - 0.3, Wi / 2 - 0.02, 0.55))
    t = 0.0
    while t < 5.0:
        q = p_in + s * t
        if abs(q.x) > Lo / 2 - tal * q.z - 0.02 or abs(q.y) > Wo / 2 - tal * q.z - 0.02:
            break
        t += 0.02
    C.palo((p_in - s * 0.1) * k + Vector((0, 0, ctx.zc)), (p_in + s * (t + 0.03)) * k + Vector((0, 0, ctx.zc)), 0.075 * k,
           ctx.sombra, lados=12, nombre="tuju")
    C.figura_madera(sobre(ctx, (Lo / 2 + 0.45) * k, -1.75 * k), ctx.m.figura, alto=1.65 * k, giro=2.6)
    return k, "La casa de la bóveda", dict(acimut=62, elevacion=22)



# ----------------------------------------------------------------------------------------------------------------
# Una candidata (27 de noviembre): la imagen que mandó el autor, con cuatro correcciones
# ----------------------------------------------------------------------------------------------------------------

def revolver(ctx, puntos, mat, k, lados=72, espesor=0.04, nombre="revoque"):
    """Una superficie de revolución abierta a partir de un perfil [(radio, z), ...] en metros reales, con espesor."""
    import bmesh
    bm = bmesh.new()
    anillos = []
    for (r, z) in puntos:
        anillos.append([bm.verts.new((r * math.cos(2 * math.pi * j / lados) * k, r * math.sin(2 * math.pi * j / lados) * k,
                                      ctx.zc + z * k)) for j in range(lados)])
    for a, b in zip(anillos, anillos[1:]):
        for j in range(lados):
            j2 = (j + 1) % lados
            bm.faces.new((a[j], a[j2], b[j2], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    ob = C.objeto(nombre, C.malla_de_bm(bm, nombre, mat))
    md = ob.modifiers.new("espesor", 'SOLIDIFY'); md.thickness = espesor * k; md.offset = -1
    return ob


def cupula_perfil(Ri=2.0, hh=0.12, v0=0.08, v1=0.13, r_oculo=0.3):
    """El radio de adentro de cada hilada de una cúpula volada: cada una entra v0 al arranque y v1 junto al óculo."""
    b = v0 / hh
    a2H = (v1 / hh - b) / 2
    H = (Ri - r_oculo) / (b + a2H)
    a2 = a2H / H
    n = int(round(H / hh)) + 1
    return [max(r_oculo, Ri - b * i * hh - a2 * (i * hh) ** 2) for i in range(n)]


def forma_E6(ctx):
    """Candidata: la casa redonda (muruqu uta). Una pirca redonda de piedra de cosecha y, encima, una cúpula de champa
    por aproximación de hiladas, cubierta de tierra en anillos que escurren el agua, con el óculo abierto bajo un sombrero
    de ichu, la puerta al este con un dintel de laja y el t'uju al noreste. Corrige la imagen que mandó el autor."""
    k = 1 / 20
    ped, fina = ctx.pedrera(), ctx.pedrera("fina")
    ctx.sombra = C.mat_liso("sombra", (0.035, 0.03, 0.026))
    ctx.m.champa = C.mat_tierra("champa_oscura", capas=False, escala_obj=14, claro=(0.10, 0.083, 0.06),
                                oscuro=(0.035, 0.03, 0.022), paja=True)
    revoque = C.mat_tierra("revoque", capas=False, escala_obj=10, claro=(0.42, 0.33, 0.22), oscuro=(0.24, 0.18, 0.12),
                           paja=True)
    Ri, e, Hb, cara = 2.0, 0.6, 1.2, 0.2             # cuarto de 4 m, pirca de 60 cm y 1,20 m de alto (proyecto)
    R = Ri + e
    tal = math.tan(math.radians(5))
    medio, h_puerta = 0.3, 1.0                       # la puerta: 60 cm × 1 m, al este
    hz = 0.2
    for i in range(int(round(Hb / hz))):
        z = i * hz
        for radio in (R - cara / 2 - tal * (z + hz / 2), Ri + cara / 2):
            n = int(2 * math.pi * radio / 0.34)
            for j in range(n):
                a = 2 * math.pi * (j + 0.5 * (i % 2)) / n
                if math.cos(a) > 0 and abs(radio * math.sin(a)) < medio + 0.12 and z < h_puerta:
                    continue
                if math.cos(a) > 0 and abs(radio * math.sin(a)) < medio + 0.25 and z >= h_puerta:
                    continue                         # aquí va el dintel
                ped.poner(sobre(ctx, radio * math.cos(a) * k, radio * math.sin(a) * k, (z + hz / 2) * k), 0.34 * k,
                          rot=(0, 0, a + math.pi / 2), aplanar=hz / 0.3)
        for _ in range(110):                         # el relleno de piedra menuda
            a = ctx.r.uniform(0, 2 * math.pi)
            rr = ctx.r.uniform(Ri + cara, R - cara - tal * z)
            if math.cos(a) > 0 and abs(rr * math.sin(a)) < medio + 0.3:
                continue
            fina.poner(sobre(ctx, rr * math.cos(a) * k, rr * math.sin(a) * k, (z + ctx.r.uniform(0, hz)) * k), 0.07 * k)
    C.caja(sobre(ctx, (Ri + e / 2) * k, 0, (h_puerta + 0.09) * k), ((e + 0.1) * k, 1.05 * k, 0.18 * k), ctx.m.piedra,
           "dintel", rot=(0, 0, ctx.r.uniform(-0.03, 0.03)), bisel=0.01 * k)
    # la cúpula de champa, volada hilada sobre hilada
    hh = 0.12
    radios = cupula_perfil(Ri, hh, v0=0.10)
    for i, r in enumerate(radios):
        rc = r + 0.2
        m = max(6, int(2 * math.pi * rc / 0.27))
        for j in range(m):
            a = 2 * math.pi * (j + 0.5 * (i % 2)) / m
            bloque_champa(ctx, sobre(ctx, rc * math.cos(a) * k, rc * math.sin(a) * k, (Hb + i * hh + hh / 2) * k),
                          (0.40 * k, (2 * math.pi * rc / m - 0.012) * k, (hh - 0.01) * k), rot_z=a)
    z_tope = Hb + len(radios) * hh
    # por fuera, un relleno de tierra con forma de cúpula baja, en cinco anillos revocados con barro; cada anillo entra
    # 10 cm respecto del de abajo y su borde sube hacia adentro para que escurra el agua. Carga las colas de las hiladas.
    Hd, r_ocu, d = z_tope - Hb + 0.1, radios[-1] + 0.15, 0.16
    A = R - tal * Hb + 0.02 - r_ocu
    puntos = []
    for kb in range(5):
        for q in range(9):
            t = math.pi / 2 * (kb + q / 8) / 5
            puntos.append((r_ocu + (A - d * kb) * math.cos(t), Hb - 0.02 + Hd * math.sin(t) + (0.05 if q == 0 and kb else 0)))
    z_tope = Hb - 0.02 + Hd
    puntos += [(radios[-1], z_tope), (radios[-1], z_tope - 0.12)]
    revolver(ctx, puntos, revoque, k, espesor=0.05)
    # el sombrero de ichu: un cono de paja sobre tres palos, levantado 30 cm sobre el óculo
    zs = z_tope + 0.3
    for j in range(3):
        a = 2 * math.pi * j / 3 + 0.4
        C.palo(sobre(ctx, 0.42 * math.cos(a) * k, 0.42 * math.sin(a) * k, (z_tope + 0.02) * k),
               sobre(ctx, 0.36 * math.cos(a) * k, 0.36 * math.sin(a) * k, (zs + 0.06) * k), 0.035 * k, ctx.m.palo)
    gorro = C.tronco(sobre(ctx, 0, 0, zs * k), 0.62 * k, 0.04 * k, 0.4 * k, ctx.m.adobe, lados=32, abierto_arriba=True)
    C.paja_sobre(gorro, ctx.m.paja, densidad=900000, largo=(0.02, 0.03), ancho=0.0007, semilla=23, capa=0.1 * k)
    for dx in (-0.16, 0.16):                         # el fogón al centro, bajo el óculo
        for j in range(3):
            ped.poner(sobre(ctx, (j - 1) * 0.2 * k, dx * k, 0.09 * k), 0.17 * k, aplanar=0.8)
    # el t'uju: un tubo de 15 cm por la pirca del noreste, apuntado al sol del 21 de junio a las 10 (Yampara Blanco, 2019: 13)
    s_ = C.vector_sol()
    p_in = Vector((Ri * math.cos(math.radians(45)), Ri * math.sin(math.radians(45)), 0.65))
    t = 0.0
    while t < 3.0 and (p_in + s_ * t).xy.length < R - tal * (p_in + s_ * t).z:
        t += 0.02
    C.palo((p_in - s_ * 0.1) * k + Vector((0, 0, ctx.zc)), (p_in + s_ * (t + 0.03)) * k + Vector((0, 0, ctx.zc)), 0.075 * k,
           ctx.sombra, lados=12, nombre="tuju")
    C.figura_madera(sobre(ctx, 0.9 * k, -(R + 0.7) * k), ctx.m.figura, alto=1.65 * k, giro=2.0)
    return k, "La casa redonda (candidata)", dict(girar=-90, acimut=-14, elevacion=14)


FORMAS = {f.__name__.split("_")[1]: f for f in (forma_1A, forma_1B, forma_1C, forma_2A, forma_2B, forma_2C, forma_3A,
                                                  forma_3B, forma_3C, forma_4A, forma_4B, forma_4C, forma_5A, forma_5B,
                                                  forma_5C, forma_E1, forma_E2P, forma_E2C, forma_E3, forma_E4,
                                                  forma_E5, forma_E6)}
