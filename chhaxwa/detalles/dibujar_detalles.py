"""Las láminas de detalle de las seis exploraciones de Chhaxwa, en DXF.

Cada lámina es un A3 apaisado a una sola escala, dibujado en metros reales en el espacio modelo. Se abren y se editan en
QCAD Community Edition, que trabaja sobre DXF, o en cualquier programa de CAD. Las medidas salen de
chhaxwa/blender/formas.py y de chhaxwa/exploraciones.md; donde la lámina resuelve algo que el modelo no dice, el rótulo
lo marca como decisión del proyecto.

Las capas siguen la jerarquía de grosores del dibujo de arquitectura (grosores al imprimir el A3 a su escala):
    CORTE        0,50 mm, negro   el contorno de lo que el plano de corte atraviesa
    TERRENO      0,70 mm, negro   la línea del suelo
    JUNTAS       0,18 mm, negro   las hiladas y piezas dentro de lo cortado
    VISTA        0,18 mm, gris    lo que se ve más allá del corte
    OCULTO       0,18 mm, gris    lo que queda detrás, en trazos
    SOMBREADO_*  0,09 mm, gris    un sombreado por material
    COTAS, GUIAS 0,13 mm, gris    cotas y líneas de rótulo
    TEXTO        0,18 mm, negro
    MARCO        0,50 y 0,13 mm   el marco y el cajetín

Se corre con un Python que tenga ezdxf, shapely y matplotlib (pip install ezdxf shapely matplotlib), desde la raíz:
    python3 chhaxwa/detalles/dibujar_detalles.py            # las seis, en chhaxwa/detalles/
    python3 chhaxwa/detalles/dibujar_detalles.py E5         # una
Escribe detalle_EX.dxf, una vista detalle_EX.png en grises y laminas_de_detalle.pdf, con las seis en A3. Un DXF que no
cambia no se reescribe, y entonces su vista y el PDF tampoco se rehacen; con --todo se rehace todo.
"""

import math
import sys
from pathlib import Path

import ezdxf
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment as TA
from shapely.geometry import Polygon
from shapely.ops import unary_union

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
ezdxf.options.write_fixed_meta_data_for_testing = True   # fechas e identificadores fijos: el mismo dibujo da el mismo DXF
NEGRO = None


def gris(v):
    return colors.rgb2int((v, v, v))


# capa: (color ACI de reserva, gris verdadero o NEGRO, grosor en centésimas de mm, tipo de línea)
CAPAS = {
    "CORTE": (7, NEGRO, 50, "Continuous"),
    "TERRENO": (7, NEGRO, 70, "Continuous"),
    "JUNTAS": (7, NEGRO, 18, "Continuous"),
    "VISTA": (8, 125, 18, "Continuous"),
    "OCULTO": (8, 125, 18, "DASHED"),
    "COTAS": (250, 60, 13, "Continuous"),
    "GUIAS": (250, 60, 13, "Continuous"),
    "TEXTO": (7, NEGRO, 18, "Continuous"),
    "ROTURA": (7, NEGRO, 18, "Continuous"),
    "MARCO": (7, NEGRO, 50, "Continuous"),
    "MARCO_FINO": (7, NEGRO, 13, "Continuous"),
}
# material: (patrón de AutoCAD o SOLID, escala del patrón, gris del sombreado)
MATERIALES = {
    "PIEDRA": ("GRAVEL", 0.5, 95),
    "PIEDRA_MENUDA": ("AR-SAND", 0.15, 95),
    "TIERRA": ("MUDST", 0.4, 105),
    "TERRENO": ("EARTH", 0.9, 175),
    "ADOBE": ("ANSI31", 0.45, 105),
    "CHAMPA": ("ANSI37", 0.5, 110),
    "PIRA": ("SOLID", 1, 135),
    "PAJA": ("DASH", 0.4, 100),
    "MADERA": ("SOLID", 1, 200),
    "LAJA": ("ANSI33", 0.4, 95),
    "GRANO": ("DOTS", 1.4, 130),
}


def rect(x0, z0, x1, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def tramo(xa, xb, z0, z1):
    """Un rectángulo entre dos x dadas en cualquier orden."""
    return rect(min(xa, xb), z0, max(xa, xb), z1)


def espejo(pts):
    return [(-x, z) for (x, z) in pts]


class Lamina:
    """Un A3 a la escala 1:escala; origen = punto del papel (en mm, desde la esquina) donde cae el (0, 0) del modelo."""

    def __init__(self, escala, origen, materiales=None):
        self.e = escala
        self.mm = escala / 1000
        self.x0, self.y0 = -origen[0] * self.mm, -origen[1] * self.mm
        self.doc = ezdxf.new("R2018", setup=True)
        self.doc.units = ezdxf.units.M
        self.doc.header["$LTSCALE"] = 4 * self.mm
        self.doc.header["$LWDISPLAY"] = 1
        self.msp = self.doc.modelspace()
        for capa, (aci, g, lw, lt) in CAPAS.items():
            ly = self.doc.layers.add(capa, color=aci, linetype=lt, lineweight=lw)
            if g is not None:
                ly.rgb = (g, g, g)
        self.materiales = {**MATERIALES, **(materiales or {})}
        for mat, (_, _, g) in self.materiales.items():
            ly = self.doc.layers.add("SOMBREADO_" + mat, color=8, lineweight=9)
            ly.rgb = (g, g, g)
        mm = self.mm
        self.doc.dimstyles.new("CHHAXWA", dxfattribs={
            "dimtxt": 2.2 * mm, "dimtsz": 1.3 * mm, "dimexe": 1.5 * mm, "dimexo": 1.0 * mm, "dimgap": 0.7 * mm,
            "dimdec": 2, "dimdsep": ord(","), "dimtad": 1, "dimzin": 0, "dimclrd": 250, "dimclre": 250, "dimclrt": 7,
            "dimlwd": 13, "dimlwe": 13})
        self.cortes = []

    def h(self, x, y):
        """Un punto del papel, en mm, pasado al modelo."""
        return (self.x0 + x * self.mm, self.y0 + y * self.mm)

    # --- lo cortado y lo visto ---------------------------------------------------------------------------------------
    def sombrear(self, pts, mat, angulo=0.0):
        patron, f, _ = self.materiales[mat]
        hch = self.msp.add_hatch(dxfattribs={"layer": "SOMBREADO_" + mat, "lineweight": 9})
        if patron == "SOLID":
            hch.set_solid_fill(color=8, rgb=(self.materiales[mat][2],) * 3)
        else:
            hch.set_pattern_fill(patron, scale=self.mm * f, angle=angulo)
        hch.paths.add_polyline_path(pts, is_closed=True)

    def cortado(self, pts, mat, juntas=True, angulo=0.0):
        """Una pieza que el plano de corte atraviesa: su sombreado, su junta fina y, al final, el contorno grueso."""
        self.sombrear(pts, mat, angulo)
        if juntas:
            self.msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "JUNTAS"})
        self.cortes.append(Polygon(pts).buffer(0))

    def alzado(self, pts, mat):
        """Una pieza vista de frente: su sombreado y un contorno fino, sin el contorno de lo cortado."""
        self.sombrear(pts, mat)
        self.msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "JUNTAS"})

    def nivel(self, x, z, texto):
        """La cota de nivel: un triángulo sobre la línea y la altura desde el suelo."""
        mm = self.mm
        self.linea([(x, z), (x - 1.4 * mm, z + 2.4 * mm), (x + 1.4 * mm, z + 2.4 * mm)], "COTAS", cerrada=True)
        self.linea([(x - 3 * mm, z), (x + 14 * mm, z)], "COTAS")
        t = self.msp.add_text(texto, height=2.2 * mm, dxfattribs={"layer": "TEXTO"})
        t.set_placement((x + 2.2 * mm, z + 0.9 * mm), align=TA.LEFT)

    def rumbos(self, izq, der, x0, x1, z=0.0):
        """Los rumbos a los dos lados del corte, sobre el suelo."""
        for (x, s, al) in ((x0, izq, TA.LEFT), (x1, der, TA.RIGHT)):
            t = self.msp.add_text(s.upper(), height=2.2 * self.mm, dxfattribs={"layer": "TEXTO"})
            t.set_placement((x, z + 1.5 * self.mm), align=al)

    def linea(self, pts, capa, cerrada=False):
        self.msp.add_lwpolyline(pts, close=cerrada, dxfattribs={"layer": capa})

    def circulo(self, c, r, capa):
        self.msp.add_circle(c, r, dxfattribs={"layer": capa})

    def terreno(self, x0, x1, z=0.0, hondo=None):
        hondo = hondo or 7 * self.mm
        self.sombrear(rect(x0, z - hondo, x1, z), "TERRENO")
        self.linea([(x0, z), (x1, z)], "TERRENO")

    def rotura(self, p0, p1):
        """La línea de rotura: dice que el dibujo sigue más allá."""
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        a = 2.5 * self.mm
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        self.linea([p0, (mx - ux * a, my - uy * a), (mx - ux * a * 0.4 - uy * a * 1.6, my - uy * a * 0.4 + ux * a * 1.6),
                    (mx + ux * a * 0.4 + uy * a * 1.6, my + uy * a * 0.4 - ux * a * 1.6), (mx + ux * a, my + uy * a), p1],
                   "ROTURA")

    # --- cotas, textos y rótulos ---------------------------------------------------------------------------------------
    def cota(self, p1, p2, base, angulo=0, texto=None):
        kw = {"text": texto} if texto else {}
        self.msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=angulo, dimstyle="CHHAXWA",
                                dxfattribs={"layer": "COTAS"}, **kw).render()

    def cota_alineada(self, p1, p2, distancia, texto=None):
        kw = {"text": texto} if texto else {}
        self.msp.add_aligned_dim(p1=p1, p2=p2, distance=distancia, dimstyle="CHHAXWA",
                                 dxfattribs={"layer": "COTAS"}, **kw).render()

    def texto(self, x, y, s, alto=2.5, alinear=TA.LEFT, capa="TEXTO"):
        """Un texto puesto en el papel, en mm."""
        t = self.msp.add_text(s, height=alto * self.mm, dxfattribs={"layer": capa})
        t.set_placement(self.h(x, y), align=alinear)

    def rotulo(self, punto, x, y, s, lado="der", alto=2.4):
        """Un punto en la pieza, una guía hasta (x, y) en el papel y el texto a un lado."""
        mm = self.mm
        codo = self.h(x, y)
        signo = 1 if lado == "der" else -1
        hombro = (codo[0] + signo * 2.5 * mm, codo[1])
        self.linea([punto, codo, hombro], "GUIAS")
        hch = self.msp.add_hatch(dxfattribs={"layer": "GUIAS"})
        hch.set_solid_fill(color=250, rgb=(60, 60, 60))
        hch.paths.add_polyline_path([(punto[0] + 0.55 * mm * math.cos(a * math.pi / 6),
                                      punto[1] + 0.55 * mm * math.sin(a * math.pi / 6)) for a in range(12)], is_closed=True)
        lineas = s.split("\n")
        for i, ln in enumerate(lineas):
            dy = ((len(lineas) - 1) / 2 - i) * alto * 1.55
            self.texto(x + signo * 3.5, y + dy, ln, alto, TA.MIDDLE_LEFT if lado == "der" else TA.MIDDLE_RIGHT)

    def titulo(self, x, y, s, alinear=TA.LEFT):
        self.texto(x, y, s, 3.0, alinear)

    def marco(self, numero, titulo, subtitulo, notas, serie="de 6"):
        """El marco del A3, el cajetín y las notas."""
        W, H = 420, 297
        self.linea([self.h(0, 0), self.h(W, 0), self.h(W, H), self.h(0, H)], "MARCO_FINO", True)
        self.linea([self.h(10, 10), self.h(W - 10, 10), self.h(W - 10, H - 10), self.h(10, H - 10)], "MARCO", True)
        cx, cy = W - 10 - 150, 10
        self.linea([self.h(cx, cy), self.h(cx + 150, cy), self.h(cx + 150, cy + 42), self.h(cx, cy + 42)], "MARCO", True)
        self.linea([self.h(cx, cy + 30), self.h(cx + 150, cy + 30)], "MARCO_FINO")
        self.linea([self.h(cx + 122, cy), self.h(cx + 122, cy + 30)], "MARCO_FINO")
        self.texto(cx + 4, cy + 34, "CHHAXWA. Cinco pruebas de construcción a partir de Altiplano", 2.8)
        self.texto(cx + 4, cy + 21, titulo, 4.5)
        self.texto(cx + 4, cy + 14, subtitulo, 2.8)
        self.texto(cx + 4, cy + 8.5, f"Escala 1:{self.e} en A3. Medidas en metros.", 2.4)
        self.texto(cx + 4, cy + 3.5, "Joaquin Max Cuevas Ventura, noviembre de 2026. Dibujado con código (ezdxf), con asistencia de IA.", 1.8)
        self.texto(cx + 136, cy + 17, numero, 10.0, TA.MIDDLE_CENTER)
        self.texto(cx + 136, cy + 6, serie, 2.4, TA.MIDDLE_CENTER)
        for i, n in enumerate(notas):
            self.texto(16, 16 + (len(notas) - 1 - i) * 4.6, n, 2.3)

    def guardar(self, nombre, carpeta=AQUI):
        """El contorno grueso de lo cortado: la unión de las piezas, con las juntas cerradas."""
        c = 0.006
        union = unary_union(self.cortes).buffer(c, join_style=2).buffer(-c, join_style=2)
        for g in getattr(union, "geoms", [union]):
            if g.is_empty:
                continue
            for anillo in [g.exterior] + list(g.interiors):
                self.linea(list(anillo.coords)[:-1], "CORTE", cerrada=True)
        for lt in self.doc.linetypes:                 # sin espacios al final de las descripciones (git diff --check)
            if lt.dxf.hasattr("description"):
                lt.dxf.description = lt.dxf.description.rstrip()
        import io
        flujo = io.StringIO()
        self.doc.write(flujo)
        ruta = carpeta / f"{nombre}.dxf"
        if ruta.exists() and ruta.read_text(encoding="utf-8") == flujo.getvalue():
            return False                                # sin cambios: no se reescribe
        ruta.write_text(flujo.getvalue(), encoding="utf-8")
        return True


# ------------------------------------------------------------------------------------------------------------------
# E1. La montaña habitada: corte por la boca, 1:25
# ------------------------------------------------------------------------------------------------------------------

def detalle_E1():
    from shapely.geometry import Polygon, box
    L = Lamina(25, (250, 92))
    R0, R1, H, hz, v, collar = 4.2, 0.32, 2.8, 0.2, 0.12, 0.40      # desde el piloto paramétrico (28 de noviembre)
    Rt, norte = R1 + collar, 2.5                                    # al norte, el corte sigue más allá de la rotura

    def ri(i):
        return 1.4 if i < 5 else max(R1, 1.4 - v * (i - 4))

    def u(z):
        return R0 - (R0 - Rt) * z / H
    for i in range(14):                                   # el cono, hilada por hilada; arriba, el collar del óculo
        z0, z1 = i * hz, (i + 1) * hz
        for s in (1, -1):
            zb = z0 if s == 1 else max(z0, 1.08)          # al sur, el paso de la boca hasta 1,08 m
            if zb >= z1:
                continue
            pts = [(ri(i), zb), (u(zb), zb), (u(z1), z1)] + ([(ri(i), z1)] if u(z1) - ri(i) > 1e-6 else [])
            if s == 1:
                pts = list(Polygon(pts).intersection(box(-1, -1, norte, 9)).exterior.coords)[:-1]
            L.cortado([(s * x, z) for (x, z) in pts], "PIEDRA")
    L.cortado(rect(-3.25, 1.0, -1.265, 1.08), "LAJA")
    L.cortado(rect(-4.75, 1.0, -3.25, 1.07), "MADERA")
    L.linea(rect(-4.75, 0.0, -3.25, 1.0), "VISTA", True)              # la pared del fondo de la caja
    L.linea([(-math.sqrt(u(0) ** 2 - 0.48 ** 2), 0.0), (-math.sqrt(u(1.0) ** 2 - 0.48 ** 2), 1.0)], "VISTA")   # el cono, al fondo
    for i in range(1, 14):                                             # las hiladas del fondo de la cámara
        L.linea([(-ri(i), i * hz), (ri(i), i * hz)], "VISTA")
    L.rotura((norte, -0.15), (norte, (R0 - norte) * H / (R0 - Rt) + 0.15))
    L.terreno(-5.5, norte + 0.9)
    L.rumbos("Sur", "Norte", -5.5, norte + 0.9)
    L.cota((-4.2, 0), (0, 0), (0, -0.8))
    L.cota((-4.75, 0), (-3.25, 0), (0, -0.45))
    L.cota((-3.25, 0), (-1.4, 0), (0, -0.45))
    L.cota((-1.4, 0), (1.4, 0), (0, -0.45))
    L.cota((-0.72, 2.8), (-0.32, 2.8), (0, 3.1))
    L.cota((-0.32, 2.8), (0.32, 2.8), (0, 3.1))
    L.cota((-4.2, 0), (-0.72, 2.8), (-5.2, 0), 90)
    L.cota((1.4, 0), (1.4, 1.0), (1.15, 0), 90)
    L.cota((-4.5, 0), (-4.5, 1.0), (-4.5, 0), 90)
    L.rotulo((0.85, 1.9), 300, 262, "Cámara de 2,80 m: vertical hasta 1 m; después,\nnueve hiladas de 20 cm que vuelan 12 cm cada\nuna hasta el óculo (piloto paramétrico).")
    L.rotulo((2.2, 0.5), 300, 238, "Cono de la piedra de la cosecha, unos 52 m³, con\nun talud de 39°. No se trae otra piedra (prueba 1).")
    L.rotulo((0.52, 2.72), 300, 216, "Collar de piedra de 40 cm alrededor del óculo:\ncarga la cola de la última hilada (piloto).")
    L.rotulo((-0.25, 2.78), 150, 262, "Óculo de 64 cm, abierto.", "izq")
    L.rotulo((-2.2, 1.04), 150, 240, "Dintel de lajas sobre el paso (proyecto).", "izq")
    L.rotulo((-4.0, 1.035), 150, 218, "Caja de queñua que atraviesa el pie del cono y asoma:\nla boca, de 0,90 × 1,00 m. Se entra en cuclillas.", "izq")
    L.marco("1", "E1. La montaña habitada", "Corte por la boca, que mira al sur", [
        "Pasaje: «quizá un día la montaña de piedras sobrepase la altura del cerro» (Botelho Gosálvez, 1982 [1945]: 9).",
        "Las medidas son decisiones del proyecto. La prueba 1 dirá cuánta piedra da una parcela y cuántas hacen falta."])
    return L.guardar("detalle_E1")


# ------------------------------------------------------------------------------------------------------------------
# E2. El corral techado: la pirca y el alero, 1:20
# ------------------------------------------------------------------------------------------------------------------

def detalle_E2():
    L = Lamina(20, (50, 64))
    R, base, alto, cara = 3.0, 0.7, 1.4, 0.2
    Rb, Ra, Hc, za = 3.4, 0.3, 3.4, 2.3
    pend = Hc / (Rb - Ra)
    nr, nz = pend / math.hypot(pend, 1), 1 / math.hypot(pend, 1)     # normal del cono, hacia afuera y arriba

    def zc(r):
        return za + (Rb - r) * pend

    def p(r, d):
        return (r + d * nr, zc(r) + d * nz)

    def banda(ra, rb, d0, d1):
        return [p(ra, d0), p(rb, d0), p(rb, d1), p(ra, d1)]
    for (a, b) in ((R - base, R - base + cara), (R - cara, R)):       # las dos caras de la pirca, en hiladas
        for i in range(7):
            L.cortado(rect(a, i * 0.2, b, (i + 1) * 0.2), "PIEDRA")
    L.cortado(rect(R - base + cara, 0, R - cara, alto - 0.04), "PIEDRA_MENUDA")
    rp = R - base / 2
    z_par = zc(rp) - 0.20 / nz                                         # bajo del par sobre el palo; encima, la correa
    r_an = 0.05
    L.cortado(rect(rp - 0.06, alto, rp + 0.06, z_par - 2 * r_an), "MADERA")
    L.cortado([(rp + r_an * math.cos(k * math.pi / 8), z_par - r_an + r_an * math.sin(k * math.pi / 8)) for k in range(16)],
              "MADERA")
    r1 = 2.0
    L.cortado(banda(r1, Rb - 0.03, -0.20, -0.11), "MADERA")           # el par
    faldon = math.hypot(Rb - Ra, Hc)                                   # las correas: anillos sobre los pares, a 70 cm
    nc = math.ceil((faldon - 0.10) / 0.70 - 1e-9)                      # o menos a lo largo del faldón (piloto)
    correas = [Rb - (0.05 + q * (faldon - 0.10) / nc) * (Rb - Ra) / faldon for q in range(nc + 1)]
    for rc in [r for r in correas if r > r1 + 0.05]:
        cx, cz = p(rc, -0.085)
        L.cortado([(cx + 0.025 * math.cos(q * math.pi / 8), cz + 0.025 * math.sin(q * math.pi / 8)) for q in range(16)],
                  "MADERA")
    L.cortado(banda(r1, Rb, -0.06, 0.0), "PIRA")                       # la p'ira
    ang = math.degrees(math.atan(pend))
    L.cortado(banda(r1, Rb + 0.08, 0.0, 0.25), "PAJA", angulo=-ang)    # el ichu
    L.rotura(p(r1 - 0.0, -0.3), p(r1, 0.4))
    L.terreno(1.0, 4.3)
    L.rumbos("Adentro", "Afuera", 1.0, 4.3)
    L.cota((R - base, 0), (R, 0), (R, -0.62))
    L.cota((R - base, 0), (R - base + cara, 0), (R, -0.38))
    L.cota((R - base + cara, 0), (R - cara, 0), (R, -0.38))
    L.cota((R - cara, 0), (R, 0), (R, -0.38))
    L.cota((R, 0), (R, alto), (R + 0.75, 0), 90)
    L.cota((R, alto), (Rb, za), (R + 0.75, 0), 90)
    L.cota((Rb, 0), (Rb, za), (R + 1.05, 0), 90)
    L.cota((rp, alto), (rp, z_par - 2 * r_an), (rp - 0.45, 0), 90)
    L.rotulo(p(3.0, 0.15), 262, 262, "Ichu en capas, de unos 25 cm.")
    L.rotulo(p(2.75, -0.03), 262, 244, "Fajas de p'ira de 0,70 m sobre las correas, como en Enquelga\n(Šolc, 2011 [1975]: 105-107). Pendiente de 48°.")
    paso = (faldon - 0.10) / nc
    L.rotulo(p(correas[1], -0.085), 262, 222, f"Correas de queñua atadas en anillo sobre los pares, cada\n{round(paso * 100)} cm a lo largo del faldón: en ellas se apoyan las fajas.")
    L.rotulo((3.2, 1.85), 262, 196, "Franja de cielo de 0,90 m entre la piedra y la paja.")
    L.rotulo((2.9, 0.9), 262, 150, "Pirca de doble cara: caras de 20 cm\ncon la piedra de la cosecha.")
    L.rotulo((2.65, 0.5), 262, 124, "Relleno de piedra menuda: la mitad del corte (prueba 2).")
    L.rotulo(p(2.35, -0.1), 135, 262, "Par de queñua, del anillo a la punta.", "izq")
    L.rotulo((rp + 0.03, z_par - r_an), 135, 240, "Anillo de palos atados: recibe los pares.", "izq")
    palo = z_par - 2 * r_an - alto
    L.rotulo((rp, 2.1), 135, 205, f"Palo de queñua de {palo:.2f} m, parado sobre la pirca.".replace(".", ",", 1), "izq")
    L.marco("2", "E2. El corral techado", "La pirca y el alero, con la p'ira bajo el ichu", [
        "Corte radial por la pirca, lejos de la entrada. Pasajes: «Las pircas derruidas; desfondados los techos de las casas» (p. 79)",
        "y las pircas «compuestas» (p. 156). Las medidas sin fuente son decisiones del proyecto."])
    return L.guardar("detalle_E2")


# ------------------------------------------------------------------------------------------------------------------
# E3. La casa redonda: corte por el paso de entrada, 1:20
# ------------------------------------------------------------------------------------------------------------------

def cupula_perfil(Ri=2.0, hh=0.12, v0=0.08, v1=0.13, r_oculo=0.3):
    """La misma cuenta de chhaxwa/blender/formas.py: el radio de adentro de cada hilada de la cúpula volada."""
    b = v0 / hh
    a2H = (v1 / hh - b) / 2
    H = (Ri - r_oculo) / (b + a2H)
    a2 = a2H / H
    n = int(round(H / hh)) + 1
    return [max(r_oculo, Ri - b * i * hh - a2 * (i * hh) ** 2) for i in range(n)]


def detalle_E3():
    L = Lamina(20, (185, 74))
    Ri, e, Hb, hh, tal = 2.0, 0.6, 1.2, 0.12, math.tan(math.radians(5))
    R = Ri + e
    paso_y, Xe = 0.72, R + 0.6
    radios = cupula_perfil(Ri, hh, v0=0.08, v1=0.12)         # de 8 a 12 cm (piloto, 28 de noviembre)
    z_c = Hb + len(radios) * hh
    Hd, r_ocu = z_c - Hb + 0.1, radios[-1] + 0.15
    A = R - tal * Hb + 0.02 - r_ocu
    z_t = Hb - 0.02 + Hd

    def elipse(t):
        return (r_ocu + A * math.cos(t), Hb - 0.02 + Hd * math.sin(t))

    def normal(t):
        v = (Hd * math.cos(t), A * math.sin(t))
        n_ = math.hypot(*v)
        return (v[0] / n_, v[1] / n_)
    # el oeste: la pirca de doble cara, en hiladas, con su talud por fuera
    for i in range(6):
        z0, z1 = i * 0.2, (i + 1) * 0.2
        L.cortado([(-(R - 0.2), z0), (-(R - tal * z0), z0), (-(R - tal * z1), z1), (-(R - 0.2), z1)], "PIEDRA")
        L.cortado(rect(-(Ri + 0.2), z0, -Ri, z1), "PIEDRA")
    L.cortado(rect(-(R - 0.2), 0, -(Ri + 0.2), Hb - 0.03), "PIEDRA_MENUDA")
    # el este: el paso, cortado por su eje; abajo queda el hueco y arriba las hiladas que lo cierran
    for j in range(7, 10):
        L.cortado(rect(Ri - 0.05, j * 0.12, Xe, (j + 1) * 0.12), "PIEDRA")
    L.cortado(rect(R - 0.1, Hb, Xe + 0.05, Hb + 0.08), "LAJA")
    L.linea(rect(Ri - 0.05, 0, Xe, 0.84), "VISTA", True)              # la jamba del norte, al fondo del paso
    for z in (0.12, 0.24, 0.36, 0.48, 0.6, 0.72):
        L.linea([(Ri - 0.05, z), (Xe, z)], "VISTA")
    # la cúpula de champa, volada, a los dos lados
    for i, r in enumerate(radios):
        for s in (1, -1):
            L.cortado([(s * x, z) for (x, z) in rect(r, Hb + i * hh, r + 0.4, Hb + (i + 1) * hh)], "CHAMPA")
        if i:
            L.linea([(-r, Hb + i * hh), (r, Hb + i * hh)], "VISTA")
    # el relleno de tierra sobre las colas
    borde = []
    for i in range(len(radios) - 1, -1, -1):
        borde += [(radios[i] + 0.4, Hb + (i + 1) * hh), (radios[i] + 0.4, Hb + i * hh)]
    perfil = [elipse(math.pi / 2 * q / 40) for q in range(41)] + [(radios[-1], z_t), (radios[-1], z_c)] + borde
    for s in (1, -1):
        L.cortado([(s * x, z) for (x, z) in perfil], "TIERRA")
    # las fajas de p'ira, traslapadas como tejuelas
    ts = [math.pi / 2 * q / 400 for q in range(401)]
    arco = [0.0]
    for t0, t1 in zip(ts, ts[1:]):
        p0, p1 = elipse(t0), elipse(t1)
        arco.append(arco[-1] + math.hypot(p1[0] - p0[0], p1[1] - p0[1]))

    def en(sv):
        for q in range(1, len(arco)):
            if arco[q] >= sv:
                return ts[q - 1] + (sv - arco[q - 1]) / (arco[q] - arco[q - 1]) * (ts[q] - ts[q - 1])
        return ts[-1]
    s0, primera = 0.0, True
    while s0 < arco[-1] - 0.05:
        s1 = min(s0 + 0.7, arco[-1])
        fuera, dentro = [], []
        for q in range(13):
            sv = s0 + (s1 - s0) * q / 12
            t = en(sv)
            (x, z), (nx, nz) = elipse(t), normal(t)
            alza = 0.0 if primera else max(0.0, min(1.0, (s0 + 0.25 - sv) / 0.1)) * 0.045
            fuera.append((x + nx * (alza + 0.045), z + nz * (alza + 0.045)))
            dentro.append((x + nx * alza, z + nz * alza))
        for s in (1, -1):
            L.cortado([(s * x, z) for (x, z) in fuera + dentro[::-1]], "PIRA")
        s0 += 0.55
        primera = False
    # el sombrero de ichu
    for s in (1, -1):
        L.cortado([(s * x, z) for (x, z) in [(0.5, z_t + 0.3), (0.62, z_t + 0.3), (0.04, z_t + 0.7), (0.02, z_t + 0.7)]],
                  "PAJA", angulo=-math.degrees(math.atan(0.4 / 0.58)) * s)
    L.linea([(-0.62, z_t + 0.3), (0.62, z_t + 0.3)], "VISTA")
    L.linea(rect(-0.3, 0, 0.3, 0.16), "VISTA", True)                   # el fogón
    L.circulo((Ri * math.cos(math.radians(45)), 0.65), 0.075, "VISTA")  # el t'uju, en el muro del noreste
    L.terreno(-3.05, 3.6)
    L.rumbos("Oeste", "Este", -3.05, 3.6)
    L.cota((-R, 0), (-Ri, 0), (0, -0.42))
    L.cota((-Ri, 0), (Ri, 0), (0, -0.42))
    L.cota((Ri, 0), (R, 0), (0, -0.42))
    L.cota((R, 0), (Xe, 0), (0, -0.42))
    L.cota((-R, 0), (-(R - tal * Hb), Hb), (-2.9, 0), 90)
    L.nivel(-radios[-1], z_t, "+" + f"{z_t:.2f}".replace(".", ","))
    L.cota((Xe, 0), (Xe, 0.84), (3.45, 0), 90)
    L.cota((Xe, 0.84), (Xe, Hb + 0.08), (3.45, 0), 90)
    L.cota((-radios[-1], z_c - 0.3), (radios[-1], z_c - 0.3), (0, z_c - 0.3))
    L.rotulo((-0.35, z_t + 0.48), 108, 272, "Sombrero de ichu sobre tres palos atados\na piedras hincadas, la chhaxwa (Bertonio,\n2011 [1612]: 330). Óculo de 60 cm.", "izq")
    pa = elipse(en(1.6))
    L.rotulo((-pa[0] - 0.02, pa[1] + 0.06), 108, 252, "Fajas de p'ira de 0,70 m traslapadas 15 cm,\ncomo tejuelas (Šolc, 2011 [1975]: 105, el ancho).", "izq")
    L.rotulo((-1.9, 1.75), 108, 233, "Relleno de tierra: carga las colas\nde las hiladas.", "izq")
    L.rotulo((1.25, 2.4), 290, 272, f"Cúpula de champa: {len(radios)} hiladas de 12 cm\nque vuelan de 8 a 12 cm (piloto paramétrico).")
    L.rotulo((2.9, 1.24), 350, 200, "Laja sobre el paso.")
    L.rotulo((2.9, 0.5), 290, 234, "Paso al este: jambas de 60 cm y tres hiladas que\nvuelan 10 cm hasta cerrarse a 96 cm (prueba 3).\nAl centro quedan 84 cm libres: se entra de rodillas.")
    L.rotulo((-2.3, 0.7), 100, 128, "Pirca de doble cara con relleno de piedra\nmenuda (prueba 2) y un talud de 5° por fuera.")
    L.rotulo((Ri * 0.707 - 0.05, 0.62), 238, 118, "T'uju de 15 cm, al noreste (Yampara Blanco, 2019: 13).", "izq")
    L.rotulo((0.0, 0.1), 238, 104, "Fogón al centro.", "izq")
    L.marco("3", "E3. La casa redonda", "Corte por el paso de entrada, de oeste a este", [
        "Pasajes: «Desde el portal de su chujlla el Paulo Huanca [...] miró irse a los desterrados» (p. 34) y el «dintel de Jatun-Kolla» (p. 155).",
        "La casa redonda es el muruqu uta de Yampara Blanco (2019: 13). Las medidas sin fuente son decisiones del proyecto."])
    return L.guardar("detalle_E3")


# ------------------------------------------------------------------------------------------------------------------
# E4. La chullpa: la base, la cámara y la boca; el aparejo de librero y la cornisa, 1:25
# ------------------------------------------------------------------------------------------------------------------

def detalle_E4():
    L = Lamina(25, (118, 74))                           # a 1:25 desde el piloto: la cámara llega a 4 m
    c, Pp = 1.05, 1.2
    for sx in (-1, 1):                                  # las pilas, al fondo del paso de este a oeste
        for i in range(6):
            v = 0.1 * max(0, i - 3)
            xs = sorted((sx * (c - Pp / 2 - v), sx * (c + Pp / 2)))
            L.linea(rect(xs[0], i * 0.2, xs[1], (i + 1) * 0.2), "VISTA", True)
    L.cortado(rect(-1.65, 1.2, 1.65, 1.3), "LAJA")
    L.cortado(rect(-1.55, 1.3, -1.25, 1.48), "PIEDRA")
    L.cortado(rect(1.25, 1.3, 1.55, 1.48), "PIEDRA")
    L.cortado(rect(-1.25, 1.3, 1.25, 1.48), "PIEDRA_MENUDA")
    z, ha, mj, pr, ret = 1.48, 0.19, 0.02, 0.14, 0.062
    vc, cierre = 0.04, 0.15                             # la cámara vuela 4 cm; una laja cierra el hueco de 28 cm

    def camara(i):
        return 0.5 if i < 3 else 0.5 - vc * (i - 2)
    ultima = next(i for i in range(3, 20) if camara(i) <= cierre + 1e-9)
    for i in range(ultima + 2):                         # la pirámide de adobitos, con la cámara y la boca al este
        s = 3.0 - 2 * i * ret
        zz = z + mj
        if i > ultima:                                  # la hilada que cierra: la laja sobre el forro y tierra encima
            c_ = camara(ultima)
            L.cortado(rect(-c_ - 0.06, z, c_ + 0.06, z + 0.08), "LAJA")
            L.cortado(rect(-c_ - 0.06, z + 0.08, c_ + 0.06, zz + ha), "TIERRA")
            for sg in (-1, 1):
                out = sg * s / 2
                a_, b_ = sorted((sg * (c_ + 0.06), out))
                L.cortado(rect(a_, z, b_, zz), "TIERRA")
                L.cortado(tramo(out - sg * pr, out, zz, zz + ha), "ADOBE")
                a_, b_ = sorted((sg * (c_ + 0.06), out - sg * pr))
                L.cortado(rect(a_, zz, b_, zz + ha), "TIERRA")
            z += mj + ha
            continue
        cam = camara(i)
        for sg in (-1, 1):
            if sg == 1 and i < 2:                        # la boca atraviesa la cara del este
                continue
            out = sg * s / 2
            lo, hi = sorted((sg * cam, out))
            L.cortado(rect(lo, z, hi, z + mj), "TIERRA")
            if sg == 1 and i == 2:                       # el dintel de laja, de la cámara a la cara
                L.cortado(rect(cam, zz, s / 2, zz + ha), "LAJA")
                continue
            L.cortado(tramo(out - sg * pr, out, zz, zz + ha), "ADOBE")
            dentro = sg * (cam + pr)                     # el forro de la cámara
            L.cortado(tramo(sg * cam, dentro, zz, zz + ha), "ADOBE")
            a_, b_ = sorted((dentro, out - sg * pr))
            if b_ - a_ > 0.01:
                L.cortado(rect(a_, zz, b_, zz + ha), "TIERRA")
        z += mj + ha
    z_cam = 1.48 + (ultima + 1) * (mj + ha)
    L.rotura((-1.5, z + 0.03), (1.5, z + 0.03))
    L.terreno(-2.1, 2.1)
    L.rumbos("Oeste", "Este", -2.1, 2.1)
    L.cota((-1.65, 0), (1.65, 0), (0, -0.62))
    L.cota((-1.65, 0), (-0.45, 0), (0, -0.38))
    L.cota((-0.45, 0), (0.45, 0), (0, -0.38))
    L.cota((0.45, 0), (1.65, 0), (0, -0.38))
    L.cota((-0.25, 1.0), (0.25, 1.0), (0, 1.08))
    L.cota((-1.65, 0), (-1.65, 1.2), (-2.0, 0), 90)
    L.cota((-1.65, 1.2), (-1.65, 1.48), (-2.0, 0), 90)
    L.cota((-0.5, 1.6), (0.5, 1.6), (0, 1.6))
    L.cota((0.0, 1.48), (0.0, z_cam), (0.0, 0), 90)
    L.cota((-camara(ultima), z_cam - 0.3), (camara(ultima), z_cam - 0.3), (0, z_cam - 0.3))
    L.cota((1.55, 1.48), (1.55, 1.9), (1.85, 0), 90)
    L.nivel(-1.3, z_cam, "+" + f"{z_cam:.2f}".replace(".", ","))
    L.rotulo((0.25, 3.3), 205, 262, f"Cámara de 1,0 × 1,0 m: tres hiladas verticales y\n{ultima - 2} que vuelan 4 cm cada una, hasta que una laja\ncierra el hueco de 28 cm (piloto paramétrico).")
    L.rotulo((1.15, 1.72), 205, 241, "Boca de 48 × 42 cm al este, al nivel de la cama\n(Squier, 1877: 244).")
    L.rotulo((0.9, 2.02), 205, 222, "Dintel de laja, de la cámara a la cara.")
    L.rotulo((1.05, 2.75), 205, 205, "Adobitos de pie, de 19 × 14 × 6 cm, en aparejo de\nlibrero; cada hilada se retira 6,2 cm.")
    L.rotulo((1.4, 1.39), 205, 186, "Hilada de piedra de 18 cm que separa el adobe del suelo.")
    L.rotulo((1.6, 1.25), 205, 172, "Cama de lajas de 10 cm que cruza los pasos.")
    L.rotulo((0.4, 0.9), 205, 148, "Pilas de pirca de 1,2 m, al fondo; las dos últimas\nhiladas vuelan 10 cm cada una hacia el paso.")
    L.rotulo((0.2, 0.4), 205, 124, "Paso de 0,90 m al pie y 0,50 m arriba:\nse pasa agachado.")
    # el aparejo de librero, en alzado
    ox, oz = L.h(308, 212)
    L.titulo(308, 262, "El aparejo de librero, en alzado")
    for fila in range(3):
        z0 = oz + fila * (ha + mj)
        L.linea([(ox, z0), (ox + 1.5, z0)], "VISTA")
        L.linea([(ox, z0 + mj), (ox + 1.5, z0 + mj)], "VISTA")
        x = ox + (0.0375 if fila % 2 else 0.0)
        while x + 0.06 <= ox + 1.5 + 1e-9:
            L.alzado(rect(x, z0 + mj, x + 0.06, z0 + mj + ha), "ADOBE")
            x += 0.075
    zt = oz + 3 * (ha + mj)
    L.cota((ox + 0.15, zt), (ox + 0.21, zt), (ox, zt + 0.12), texto="0,06")
    L.cota((ox + 0.21, zt), (ox + 0.225, zt), (ox, zt + 0.25), texto="0,015")
    L.cota((ox + 1.5, oz + mj), (ox + 1.5, oz + mj + ha), (ox + 1.62, 0), 90)
    L.texto(308, 205, "Los adobitos van de pie, como libros en un estante, a 1,5 cm", 2.3)
    L.texto(308, 200.5, "uno de otro, con mortero solo arriba y abajo (Agüero Benites", 2.3)
    L.texto(308, 196, "et al., 2015: 3 y 6). El mortero, 2 cm; la hilada, 21 cm.", 2.3)
    # la cornisa de ichu prensado, en corte
    ox, oz = L.h(325, 118)
    L.titulo(308, 182, "La cornisa de ichu prensado, en corte")
    for k, (dx, z0) in enumerate(((0.062, 0.0), (0.0, ha + mj))):
        L.cortado(rect(ox - 0.5, oz + z0, ox + dx - pr, oz + z0 + mj), "TIERRA")
        L.cortado(rect(ox + dx - pr, oz + z0, ox + dx, oz + z0 + mj + ha), "ADOBE")
        L.cortado(rect(ox - 0.5, oz + z0 + mj, ox + dx - pr, oz + z0 + mj + ha), "TIERRA")
    zc_ = oz + 2 * (ha + mj)
    L.cortado(rect(ox - 0.5, zc_, ox + 0.1, zc_ + 0.15), "PAJA")
    L.cortado(rect(ox - 0.5, zc_ + 0.15, ox - 0.062 - pr, zc_ + 0.15 + mj + ha), "TIERRA")
    L.cortado(rect(ox - 0.062 - pr, zc_ + 0.15, ox - 0.062, zc_ + 0.15 + mj + ha), "ADOBE")
    L.rotura((ox - 0.5, oz - 0.03), (ox - 0.5, zc_ + 0.15 + mj + ha + 0.03))
    L.cota((ox + 0.1, zc_), (ox + 0.1, zc_ + 0.15), (ox + 0.32, 0), 90)
    L.cota((ox, zc_ + 0.15), (ox + 0.1, zc_ + 0.15), (0, zc_ + 0.5))
    L.texto(352, 150, "Ichu prensado, de 15 cm de alto,", 2.3)
    L.texto(352, 145.5, "que vuela 10 cm: «a cornice or", 2.3)
    L.texto(352, 141, "projection of four inches» (Squier,", 2.3)
    L.texto(352, 136.5, "1877: 243), sobre la hilada 13.", 2.3)
    L.marco("4", "E4. La chullpa", "La base, la cámara y la boca; el aparejo y la cornisa", [
        "Corte de este a oeste por la boca. Pasajes: «amontonó piedras sobre el cadáver» (p. 35) y «un informe montón de rocas, lodo",
        "y maderos astillados» (p. 154). Alto total, 4,9 m, el de la chullpa de Palca (Squier, 1877: 243); lo demás sin fuente es del proyecto."])
    return L.guardar("detalle_E4")


# ------------------------------------------------------------------------------------------------------------------
# E5. La casa de la bóveda: corte de través por el fogón, 1:20
# ------------------------------------------------------------------------------------------------------------------

def detalle_E5():
    L = Lamina(20, (176, 92))
    Wi, E0, Hw, zr, cara = 3.30, 0.9, 2.0, 0.35, 0.32
    Wo = Wi + 2 * E0
    tal = math.tan(math.radians(10))
    hh, b = 0.11, 0.11 / 0.11
    a2H = (0.13 / 0.11 - b) / 2
    H = (Wi / 2 - 0.15) / (b + a2H)
    a2 = a2H / H
    n = int(round(H / hh)) + 1
    zf = 1.7

    def r(i):
        h = i * hh
        return max(0.15, Wi / 2 - b * h - a2 * h * h)
    for sg in (-1, 1):
        def m(pts):
            return [(sg * x, z) for (x, z) in pts]
        for i in range(10):                                            # la cara de afuera, en talud, por hiladas
            z0, z1 = i * 0.2, (i + 1) * 0.2
            L.cortado(m([(Wo / 2 - cara - tal * z0, z0), (Wo / 2 - tal * z0, z0), (Wo / 2 - tal * z1, z1),
                         (Wo / 2 - cara - tal * z1, z1)]), "PIEDRA")
        L.cortado(m(rect(Wi / 2, 0, Wi / 2 + cara, 0.2)), "PIEDRA")    # la cara de adentro, hasta el arranque
        L.cortado(m(rect(Wi / 2, 0.2, Wi / 2 + cara, zr)), "PIEDRA")
        imax = int((zf - zr) / hh)
        cola = []
        for i in range(imax, -1, -1):
            cola += [(r(i) + 0.4, min(zr + (i + 1) * hh, zf)), (r(i) + 0.4, zr + i * hh)]
        L.cortado(m([(Wi / 2 + cara, 0), (Wo / 2 - cara, 0), (Wo / 2 - cara - tal * zf, zf)] + cola + [(Wi / 2 + cara, zr)]),
                  "TIERRA")
        for i in range(n):
            z0 = zr + i * hh
            L.cortado(m(rect(r(i), z0, r(i) + 0.4, z0 + hh)), "ADOBE")
            if i:
                L.linea([(-r(i), z0), (r(i), z0)], "VISTA")
    zc = zr + n * hh
    L.linea(rect(-0.37, zc, 0.37, zc + 0.08), "VISTA", True)          # las lajas de la clave, más allá del fogón
    L.cortado(rect(-Wi / 2, 0, -Wi / 2 + 0.7, zr), "ADOBE")            # el camastro
    for dy in (-0.16, 0.16):
        L.cortado(rect(dy - 0.085, 0, dy + 0.085, 0.16), "PIEDRA")
    L.terreno(-3.25, 3.25)
    L.rumbos("Sur", "Norte", -3.25, 3.25)
    L.cota((-Wo / 2, 0), (Wo / 2, 0), (0, -0.72))
    L.cota((-Wo / 2, 0), (-Wi / 2, 0), (0, -0.42))
    L.cota((-Wi / 2, 0), (Wi / 2, 0), (0, -0.42))
    L.cota((Wi / 2, 0), (Wo / 2, 0), (0, -0.42))
    L.cota((Wo / 2, 0), (Wo / 2 - tal * zr, zr), (2.95, 0), 90)
    L.cota((Wo / 2, 0), (Wo / 2 - tal * zf, zf), (3.2, 0), 90)
    L.cota((Wo / 2, 0), (Wo / 2 - tal * Hw, Hw), (3.45, 0), 90)
    L.cota((-0.37, 0), (-0.37, zc), (-0.62, 0), 90)
    L.cota((-r(n - 1), zc - 0.06), (r(n - 1), zc - 0.06), (0, zc - 0.06))
    L.rotulo((-2.25, 1.2), 158, 218, "Pirca de doble cara, en talud de 10° por fuera,\ncon la piedra de la cosecha. Sube hasta 2 m.", "izq")
    L.rotulo((-1.75, 1.3), 168, 240, "Relleno de tierra y piedra menuda hasta 1,70 m:\ncarga las colas de las hiladas.", "izq")
    L.rotulo((0.1, zc - 0.02), 190, 262, "La clave abierta: falta una laja sobre el fogón\ny por ahí sale el humo. Las demás, a 1,86 m.")
    L.rotulo((1.2, 0.9), 262, 232, "Bóveda de adobe de 40 × 20 × 10 cm a tizón:\nhiladas de 11 cm que vuelan de 11 a 13 cm.\nArranca a 35 cm y se cierra a 1,78 m.")
    L.rotulo((-1.45, 0.3), 178, 262, "Camastro de adobe, «apenas la altura de un adobe»\n(pp. 30-31). La bóveda arranca a su altura.", "izq")
    L.rotulo((0.16, 0.12), 262, 205, "Fogón al centro, bajo la laja que falta.")
    L.marco("5", "E5. La casa de la bóveda", "Corte de través por el fogón", [
        "Pasajes: «Rectangulares y chatas, apenas se alzan dos metros del suelo» (p. 30), y las herramientas colgadas de las vigas (p. 31).",
        "Cuarto de 5,75 × 3,30 m, la mediana de Šolc (2011 [1975]: 93-94). Hay que probar que el adobe vuele 13 cm, un tercio de su largo."])
    return L.guardar("detalle_E5")


# ------------------------------------------------------------------------------------------------------------------
# E6. La pirwa: la V volada con la trampa, y la chhaxwa, 1:20
# ------------------------------------------------------------------------------------------------------------------

def detalle_E6():
    L = Lamina(20, (112, 86))
    X, Y, Hp, g, BH, BA = 1.5, 0.8, 0.9, 0.5, 0.12, 0.25
    Hl, Hh = 3.6, 4.6
    z0 = Hp + 0.05
    for i in range(5):                                                 # el apoyo oeste: pirca
        L.cortado(rect(-X - 0.1, i * 0.18, -g, (i + 1) * 0.18), "PIEDRA")
    L.cortado([(0.0, 0), (2.0, 0), (1.55, Hp), (0.45, Hp)], "PIEDRA")  # el apoyo este: montón
    for (a, b_) in ((-X - 0.1, -g), (g, X + 0.1)):
        L.cortado(rect(a, Hp, b_, z0), "LAJA")
    zt = 2.95
    i = 0
    while z0 + i * BH < zt - 1e-6:                                     # el cuerpo de champa
        z = z0 + i * BH
        z1 = min(z + BH, zt)
        w = g - 0.06 * (i + 1)
        if w > 0.03:                                                   # la V: las cabeceras de cada pata, cortadas
            for (a, b_) in ((-X, -w), (w, X)):
                L.cortado(rect(a, z, a + BA, z1), "CHAMPA")
                L.cortado(rect(b_ - BA, z, b_, z1), "CHAMPA")
                L.linea(rect(a, z, b_, z1), "VISTA", True)              # el muro largo, al fondo
        else:
            L.cortado(rect(-X, z, -X + BA, z1), "CHAMPA")
            L.cortado(rect(X - BA, z, X, z1), "CHAMPA")
            L.linea(rect(-X, z, X, z1), "VISTA", True)
        i += 1
    zc = z0 + 7 * BH
    xs = [x for x in [-X + BA + 0.07 + 0.14 * q for q in range(20)] if x < X - BA - 0.06 and abs(x) > 0.24]
    for x in xs:                                                       # el piso: palos de queñua de muro a muro
        L.cortado([(x + 0.06 * math.cos(k * math.pi / 8), zc + 0.06 + 0.06 * math.sin(k * math.pi / 8)) for k in range(16)],
                  "MADERA")
    L.cortado(rect(-0.2, zc - 0.035, 0.2, zc - 0.005), "MADERA")       # la trampa
    L.cortado(rect(-X + BA, zc + 0.12, X - BA, zt), "GRANO", juntas=False)
    L.rotura((-X - 0.15, zt + 0.02), (X + 0.15, zt + 0.02))
    L.terreno(-2.0, 2.3)
    L.rumbos("Oeste", "Este", -2.0, 2.3)
    L.cota((-X - 0.1, 0), (-g, 0), (0, -0.38))
    L.cota((-g, 0), (0.0, 0), (0, -0.38))
    L.cota((0.0, 0), (2.0, 0), (0, -0.38))
    L.cota((-g, z0), (g, z0), (0, z0 - 0.16))
    L.cota((-X - 0.1, 0), (-X - 0.1, Hp), (-1.9, 0), 90)
    L.cota((-0.44, z0 + 0.12), (-0.38, z0 + 0.12), (0, z0 + 0.06), texto="0,06")
    L.cota((X - BA, zt - 0.3), (X, zt - 0.3), (0, zt - 0.3))
    L.nivel(X + 0.02, zc - 0.035, "+1,79, la clave")
    L.texto(112 - 1.05 / 0.02, 56, "Apoyo de pirca", 2.4, TA.MIDDLE_CENTER)
    L.texto(112 + 1.0 / 0.02, 56, "Apoyo de piedra amontonada", 2.4, TA.MIDDLE_CENTER)
    L.rotulo((0.6, 2.5), 240, 198, "Lo guardado: granos, quinua, papas deshidratadas\n(Yampara Blanco, 2019: 14).")
    L.rotulo((xs[-1] + 0.03, zc + 0.08), 240, 184, "Piso de palos de queñua de muro a muro (proyecto).")
    L.rotulo((0.1, zc - 0.02), 240, 160, "Trampa de queñua en la clave de la V: por aquí\nse saca lo guardado (proyecto).")
    L.rotulo((0.62, z0 + 0.55), 240, 132, "Champa de 40 × 25 × 12 cm. En la V cada hilada\nvuela 6 cm hasta tocarse, «forming a rude kind\nof arch» (Squier, 1877: 313).")
    L.rotulo((0.9, z0 + 0.3), 240, 108, "Muro largo, al fondo: la V vista de frente.")
    # la chhaxwa: corte de través por un palo del techo, con su propio origen en el papel
    tope = Hl + (-0.25 + X) / (2 * X) * (Hh - Hl)
    zp = tope + 0.06
    ox, oz = L.h(300, 248)

    def q(pts):
        return [(ox + y, oz + z - tope) for (y, z) in pts]
    L.titulo(262, 274, "La chhaxwa, en corte de través por un palo del techo")
    zb = tope - 5 * BH
    for sg in (-1, 1):
        for k in range(5):
            L.cortado(q(tramo(sg * (Y - BA), sg * Y, zb + k * BH, zb + (k + 1) * BH)), "CHAMPA")
        L.cortado(q(tramo(sg * (Y - 0.18), sg * (Y + 0.24), zp - 0.44, zp - 0.37)), "PIEDRA")
        L.linea(q([(sg * (Y + 0.22), zp - 0.37), (sg * (Y + 0.25), zp - 0.06)]), "JUNTAS")
        L.linea(q([(sg * (Y + 0.2), zp - 0.37), (sg * (Y + 0.23), zp - 0.06)]), "JUNTAS")
    L.cortado(q(rect(-Y - 0.28, zp - 0.06, Y + 0.28, zp + 0.06)), "MADERA")
    L.cortado(q(rect(-1.06, zp + 0.06, 1.06, zp + 0.11)), "PIRA")
    L.cortado(q(rect(-Y + BA, zb, Y - BA, Hl - 0.1)), "GRANO", juntas=False)
    L.rotura(q([(-Y - 0.1, zb - 0.02)])[0], q([(Y + 0.1, zb - 0.02)])[0])
    L.cota(q([(-Y, zb)])[0], q([(Y, zb)])[0], q([(0, zb - 0.22)])[0])
    L.rotulo(q([(Y + 0.15, zp - 0.4)])[0], 362, 222, "Piedra «hincada en la pared\npara atar en ella los palos\ndel techo»: la chhaxwa\n(Bertonio, 2011 [1612]: 330).")
    L.rotulo(q([(Y + 0.235, zp - 0.2)])[0], 362, 254, "Soga de paja.")
    L.rotulo(q([(-0.55, zp)])[0], 244, 266, "Palo de queñua y fajas de p'ira encima\n(Šolc, 2011 [1975]: 105).", "izq")
    L.marco("6", "E6. La pirwa", "La V volada con la trampa; la chhaxwa", [
        "Corte por el eje largo. Pasajes: «Todo era pronóstico de abundancia, de trojes altos y almiares llenos» y «desde la atalaya de la",
        "esperanza» (p. 157). Las pirwas son «silos aéreos» con una boca arriba y otra abajo (Yampara Blanco, 2019: 14). Alto: 3,6 a 4,6 m."])
    return L.guardar("detalle_E6")


DETALLES = {"E1": detalle_E1, "E2": detalle_E2, "E3": detalle_E3, "E4": detalle_E4, "E5": detalle_E5, "E6": detalle_E6}


def dibujar(nombre, ax, carpeta=AQUI):
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration, LineweightPolicy
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    doc = ezdxf.readfile(carpeta / f"{nombre}.dxf")
    # el motor de matplotlib toma los grosores en mm como si fueran puntos: 1 mm = 1 / 0,3527 pt
    config = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR,
                           lineweight_policy=LineweightPolicy.ABSOLUTE, lineweight_scaling=1 / 0.3527,
                           min_lineweight=0.05 / 0.3527)
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=config).draw_layout(doc.modelspace(), finalize=True)
    marco = [e for e in doc.modelspace().query("LWPOLYLINE[layer=='MARCO_FINO']")][0]
    xs = [p[0] for p in marco.get_points()]
    ys = [p[1] for p in marco.get_points()]
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.set_aspect("equal")
    ax.axis("off")


def vistas(claves, pdf=True):
    """Una imagen en grises de cada lámina de la lista y, si se pide, el PDF en A3 con las seis."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from PIL import Image
    A3 = (420 / 25.4, 297 / 25.4)
    for c in claves:
        fig = plt.figure(figsize=A3)
        dibujar(f"detalle_{c}", fig.add_axes([0, 0, 1, 1]))
        fig.set_size_inches(*A3)
        ruta = AQUI / f"detalle_{c}.png"
        fig.savefig(ruta, dpi=200, facecolor="white")
        plt.close(fig)
        Image.open(ruta).convert("L").quantize(32).save(ruta, optimize=True)
    if pdf:
        with PdfPages(AQUI / "laminas_de_detalle.pdf", metadata={"Title": "Chhaxwa. Láminas de detalle",
                                                                  "Author": "Joaquin Max Cuevas Ventura",
                                                                  "CreationDate": None}) as pdf:
            for c in DETALLES:
                fig = plt.figure(figsize=A3)
                dibujar(f"detalle_{c}", fig.add_axes([0, 0, 1, 1]))
                fig.set_size_inches(*A3)
                pdf.savefig(fig, facecolor="white")
                plt.close(fig)


if __name__ == "__main__":
    import os
    if os.environ.get("PYTHONHASHSEED") != "0":     # el orden de algunas tablas del DXF depende del azar de los hash
        os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0"})
    # Solo se rehacen la vista y el PDF de lo que cambió; con --todo, todo.
    claves = [a for a in sys.argv[1:] if a in DETALLES] or list(DETALLES)
    todo = "--todo" in sys.argv
    cambiadas = []
    for c in claves:
        if DETALLES[c]() or todo or not (AQUI / f"detalle_{c}.png").exists():
            cambiadas.append(c)
        print(f"detalle {c}: {'rehecho' if c in cambiadas else 'sin cambios'}")
    vistas(cambiadas, pdf=bool(cambiadas) or not (AQUI / "laminas_de_detalle.pdf").exists())
