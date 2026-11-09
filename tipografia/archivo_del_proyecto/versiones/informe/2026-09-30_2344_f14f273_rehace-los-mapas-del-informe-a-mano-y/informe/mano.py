"""La mano de los mapas: un repertorio de trazos orgánicos en SVG.

Los mapas del informe no se trazan con regla. Toman de sus referencias (notaciones
dibujadas a mano con acuarela, órbitas, ejes y haces; una sala en perspectiva con un
embudo y bandadas de signos; un cuaderno de pictogramas) el modo de dibujar, y de
Contenida el sentido de cada gesto:

  - la línea tiembla apenas, como la mano del que calca (D11);
  - toda órbita se abre abajo, en su punto más bajo: el desagüe (D16);
  - lo continuo es lo hallado; lo punteado, lo reconstruido o lo que todavía no es;
  - cada color es un material del proyecto: violeta, la tinta del esténcil; lila, el
    agua; grafito, el frotado; plata, el aluminio; hueso, la cinta de enmascarar; y la
    tinta, lo hallado. El verde es solo luz: no se dibuja;
  - a máquina va lo que ya estaba escrito (el pie, el poema, los datos); a mano, lo
    que se hace con eso.

La letra de mano es una fuente (La Belle Aurore, de Kimberly Geswein, SIL OFL), no una
mano: el colofón del informe lo dice.
"""

import math
import random

PAPEL, TINTA, VIOLETA, LILA = "#f6f4ee", "#1d1c1a", "#4a2470", "#b9a6d6"
GRAFITO, GRAFITO2, PLATA, HUESO = "#55534e", "#8f8b83", "#a7a9a6", "#e4d9bd"
MANO, MAQUINA, SERIF = "La Belle Aurore", "Courier Prime", "Newsreader"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------------ geometría

def largo(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def remuestrear(pts, paso=4.0):
    """Puntos a distancia pareja a lo largo de la polilínea."""
    if len(pts) < 2:
        return list(pts)
    out, resto = [pts[0]], 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if d == 0:
            continue
        t = paso - resto
        while t <= d:
            out.append((a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d))
            t += paso
        resto = d - (t - paso)
    if math.dist(out[-1], pts[-1]) > paso * 0.3:
        out.append(pts[-1])
    return out


def spline(pts, n=14, cerrada=False):
    """Catmull-Rom por los puntos: la curva que pasa por donde pasa la mano."""
    P = list(pts)
    if cerrada:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(P[-2])
    return out


def bezier(p0, p1, p2, p3, n=40):
    """Una cúbica de Bézier como polilínea: sin sobrepasarse, de tangente a tangente."""
    out = []
    for k in range(n + 1):
        t = k / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def normales(pts):
    out = []
    for i in range(len(pts)):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        out.append((-dy / L, dx / L))
    return out


def tangente(pts, final=True):
    a, b = (pts[-4] if len(pts) > 3 else pts[0], pts[-1]) if final else (pts[min(3, len(pts) - 1)], pts[0])
    return math.atan2(b[1] - a[1], b[0] - a[0])


def d_suave(pts, cerrada=False):
    """Un path suave: cuadráticas por los puntos medios."""
    if len(pts) < 3:
        return "M" + " L".join(f"{fmt(x)},{fmt(y)}" for x, y in pts)
    d = [f"M{fmt(pts[0][0])},{fmt(pts[0][1])}"]
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d.append(f"Q{fmt(pts[i][0])},{fmt(pts[i][1])} {fmt(mx)},{fmt(my)}")
    d.append(f"L{fmt(pts[-1][0])},{fmt(pts[-1][1])}")
    return " ".join(d) + (" Z" if cerrada else "")


def elipse_pts(cx, cy, rx, ry, rot, t0, t1, paso=0.03):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    n = max(4, int(abs(t1 - t0) / paso))
    out = []
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


class Perspectiva:
    """Una perspectiva de un punto: X a la derecha, Y hacia el fondo, Z hacia arriba."""

    def __init__(self, vx, vy, foco, altura, distancia):
        self.vx, self.vy, self.f, self.c, self.d = vx, vy, foco, altura, distancia

    def __call__(self, X, Y, Z):
        k = self.f / (Y + self.d)
        return (self.vx + X * k, self.vy + (self.c - Z) * k)


# ------------------------------------------------------------------ la hoja

class Hoja:
    def __init__(self, ancho, alto, semilla):
        self.W, self.H = ancho, alto
        self.rng = random.Random(semilla)
        self.semilla = semilla
        self.defs = []
        self.capas = {k: [] for k in ("papel", "aguadas", "grafito", "lineas", "objetos", "textos")}
        self.n = 0
        self.defs.append(
            '<filter id="lapiz" x="-5%" y="-5%" width="110%" height="110%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="g"/>'
            '<feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.6 0 0 0 -0.1" result="ga"/>'
            '<feComposite in="SourceGraphic" in2="ga" operator="in"/></filter>')
        self.add("papel", f'<rect width="{self.W}" height="{self.H}" fill="{PAPEL}"/>')

    def add(self, capa, s):
        self.capas[capa].append(s)

    def uid(self, p="m"):
        self.n += 1
        return f"{p}{self.n}"

    def ruido(self, escala):
        """Un ruido suave en [-1, 1] a lo largo de un recorrido, con longitud de onda ~escala."""
        r = self.rng
        comps = [(r.uniform(0.8, 1.25) * 2 * math.pi / (escala / k), r.uniform(0, 2 * math.pi), 1 / k) for k in (1, 2.2, 4.7)]
        norma = sum(a for _, _, a in comps)
        return lambda s: sum(a * math.sin(f * s + p) for f, p, a in comps) / norma

    def temblar(self, pts, temblor=0.35, deriva=None, paso=4.0):
        """El temblor de la mano (apenas) y la deriva de un trazo largo."""
        pts = remuestrear(pts, paso)
        L = largo(pts)
        deriva = min(3.5, L * 0.006) if deriva is None else deriva
        r1, r2 = self.ruido(14), self.ruido(max(60.0, L * 0.6))
        out, s = [], 0.0
        for i, ((x, y), (nx, ny)) in enumerate(zip(pts, normales(pts))):
            if i:
                s += math.dist(pts[i - 1], pts[i])
            o = temblor * r1(s) + deriva * r2(s)
            out.append((x + nx * o, y + ny * o))
        return out

    # -------------------------------------------------------------- trazos
    def trazo(self, pts, color=TINTA, ancho=0.9, opac=1.0, punteado=False, capa="lineas", temblor=0.35, deriva=None,
              pluma=False, guiones=None, extra=""):
        """Una línea a mano. Continua: lo hallado. Punteada: lo reconstruido, lo que todavía no es."""
        p = self.temblar(pts, temblor, deriva)
        op = f' opacity="{round(opac, 3)}"' if opac < 1 else ""
        if pluma and not punteado and len(p) > 3:
            r = self.ruido(40)
            n = normales(p)
            L, s, izq, der = largo(p), 0.0, [], []
            for i, ((x, y), (nx, ny)) in enumerate(zip(p, n)):
                if i:
                    s += math.dist(p[i - 1], p[i])
                punta = min(1.0, s / 8 + 0.35, (L - s) / 14 + 0.25)
                w = ancho * (0.85 + 0.3 * r(s)) * punta / 2
                izq.append((x + nx * w, y + ny * w))
                der.append((x - nx * w, y - ny * w))
            d = d_suave(izq) + " L" + d_suave(der[::-1])[1:] + " Z"
            self.add(capa, f'<path d="{d}" fill="{color}"{op}{extra}/>')
            return p
        if punteado:
            dash = guiones or f"0.1 {fmt(ancho * 3.2 + 2.2)}"
            estilo = f' stroke-dasharray="{dash}" stroke-linecap="round"'
        elif guiones:
            estilo = f' stroke-dasharray="{guiones}" stroke-linecap="round"'
        else:
            estilo = ' stroke-linecap="round"'
        self.add(capa, f'<path d="{d_suave(p)}" fill="none" stroke="{color}" stroke-width="{fmt(ancho) if ancho >= 0.1 else ancho}"'
                       f' stroke-linejoin="round"{estilo}{op}{extra}/>')
        return p

    def curva(self, puntos, **kw):
        """Un trazo por varios puntos de paso (spline)."""
        return self.trazo(spline(puntos), **kw)

    def punta(self, x, y, ang, color=TINTA, ancho=0.9, largo_=10.0, abre=19.0, capa="lineas", llena=False):
        """La punta de una flecha: dos trazos cortos, como la hace la mano."""
        a1, a2 = ang + math.pi - math.radians(abre), ang + math.pi + math.radians(abre)
        l1, l2 = largo_ * self.rng.uniform(0.85, 1.1), largo_ * self.rng.uniform(0.85, 1.1)
        p1 = (x + l1 * math.cos(a1), y + l1 * math.sin(a1))
        p2 = (x + l2 * math.cos(a2), y + l2 * math.sin(a2))
        if llena:
            self.add(capa, f'<path d="M{fmt(p1[0])},{fmt(p1[1])} L{fmt(x)},{fmt(y)} L{fmt(p2[0])},{fmt(p2[1])} '
                           f'Q{fmt((x * 2 + p1[0] + p2[0]) / 4)},{fmt((y * 2 + p1[1] + p2[1]) / 4)} {fmt(p1[0])},{fmt(p1[1])}Z" '
                           f'fill="{color}"/>')
            return
        self.add(capa, f'<path d="M{fmt(p1[0])},{fmt(p1[1])} L{fmt(x)},{fmt(y)} L{fmt(p2[0])},{fmt(p2[1])}" fill="none" '
                       f'stroke="{color}" stroke-width="{fmt(ancho)}" stroke-linecap="round" stroke-linejoin="round"/>')

    def flecha(self, puntos, color=TINTA, ancho=0.8, punteado=False, doble=False, capa="lineas", curva=True, **kw):
        """Una flecha a mano por los puntos dados; la punta, en el último."""
        p = self.trazo(spline(puntos) if curva and len(puntos) > 2 else puntos, color=color, ancho=ancho,
                       punteado=punteado, capa=capa, **kw)
        self.punta(p[-1][0], p[-1][1], tangente(p), color, max(0.8, ancho), capa=capa)
        if doble:
            self.punta(p[0][0], p[0][1], tangente(p, final=False), color, max(0.8, ancho), capa=capa)
        return p

    def cruz(self, x, y, r=4.5, color=TINTA, ancho=0.9):
        """× : un centro externo, o donde algo se detiene."""
        for s in (1, -1):
            self.trazo([(x - r, y - r * s), (x + r, y + r * s)], color, ancho, temblor=0.2, deriva=0)

    def punto(self, x, y, r=2.4, color=TINTA, capa="lineas", opac=1.0):
        rr = self.rng
        pts = [(x + r * (1 + rr.uniform(-0.18, 0.18)) * math.cos(a), y + r * (1 + rr.uniform(-0.18, 0.18)) * math.sin(a))
               for a in [k * math.pi / 4 for k in range(8)]]
        op = f' opacity="{opac}"' if opac < 1 else ""
        self.add(capa, f'<path d="{d_suave(spline(pts, 4, True), True)}" fill="{color}"{op}/>')

    # -------------------------------------------------------------- órbitas y ejes
    def orbita(self, cx, cy, rx, ry, rot=0.0, hueco=11.0, color=TINTA, ancho=0.7, pasadas=2, punteado=False, opac=1.0,
               capa="lineas", sentido=None):
        """Una órbita a mano, abierta en su punto más bajo: el desagüe. Devuelve sus puntos."""
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        t_bajo = math.atan2(c * ry, s * rx)                    # donde la órbita toca más abajo
        h = math.radians(hueco) / 2
        r = self.ruido(3.0)
        base = None
        for k in range(pasadas):
            f = 1 + (0.018 * k if k else 0)
            g = 1 - (0.014 * k if k else 0)
            if k == 0:
                t0, t1 = t_bajo + h, t_bajo + 2 * math.pi - h
            else:
                ini = self.rng.uniform(0.05, 0.5)
                t0 = t_bajo + h + ini * 2 * math.pi
                t1 = min(t_bajo + 2 * math.pi - h, t0 + self.rng.uniform(0.35, 0.6) * 2 * math.pi)
            pts = elipse_pts(cx, cy, rx * f, ry * g, rot + (1.1 * k), t0, t1)
            pts = [(cx + (x - cx) * (1 + 0.012 * r(i * 0.05)), cy + (y - cy) * (1 + 0.012 * r(i * 0.05)))
                   for i, (x, y) in enumerate(pts)]
            p = self.trazo(pts, color, ancho * (1 if k == 0 else 0.8), opac * (1 if k == 0 else 0.75), punteado, capa,
                           temblor=0.3, deriva=1.2)
            base = base or p
        if sentido is not None:                                # una punta que dice hacia dónde gira
            i = int(len(base) * sentido)
            a = tangente(base[:i + 1])
            self.punta(base[i][0], base[i][1], a, color, ancho + 0.1, 9)
        return base

    def eje(self, x0, y0, x1, y1, color=TINTA, ancho=0.7, puntas=(False, True), marcas=(), punteado=False, capa="lineas"):
        """Un eje: la línea de caída. Por defecto apunta abajo, adonde va el agua."""
        p = self.trazo([(x0, y0), (x1, y1)], color, ancho, punteado=punteado, capa=capa, temblor=0.25)
        if puntas[1]:
            self.punta(p[-1][0], p[-1][1], tangente(p), color, ancho + 0.1, 11)
        if puntas[0]:
            self.punta(p[0][0], p[0][1], tangente(p, final=False), color, ancho + 0.1, 11)
        a = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
        for t in marcas:
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            self.trazo([(x - 6 * math.cos(a), y - 6 * math.sin(a)), (x + 6 * math.cos(a), y + 6 * math.sin(a))], color,
                       ancho, temblor=0.2, deriva=0, capa=capa)
        return p

    def haz(self, puntos, hebras=9, abre=10.0, color=TINTA, ancho=0.45, opac=0.8, colores=None, capa="lineas",
            punteado=False):
        """Un haz estratificado: hebras paralelas que se aprietan y se abren (sus capas son sus colores)."""
        base = spline(puntos)
        n = normales(remuestrear(base, 4))
        base = remuestrear(base, 4)
        L = largo(base)
        out = []
        for k in range(hebras):
            off = (k - (hebras - 1) / 2) * abre / max(1, hebras - 1)
            r = self.ruido(L * 0.7 + 1)
            pts, s = [], 0.0
            for i, ((x, y), (nx, ny)) in enumerate(zip(base, n)):
                if i:
                    s += math.dist(base[i - 1], base[i])
                t = s / L
                o = off * (0.35 + 0.65 * math.sin(math.pi * min(1, t * 1.3)) ** 0.5) + 1.2 * r(s)
                pts.append((x + nx * o, y + ny * o))
            c = colores[k % len(colores)] if colores else color
            out.append(self.trazo(pts, c, ancho, opac * self.rng.uniform(0.65, 1), punteado, capa, temblor=0.2, deriva=0.6))
        return out

    # -------------------------------------------------------------- manchas, aguadas y rayados
    def filtro_aguada(self, desplaza=16.0, frecuencia=0.016, borde=0.62, grano=0.8, erosion=3.0):
        """Aguada: borde irregular, más oscura donde se seca (el borde), manchas y un grano leve."""
        fid = self.uid("aguada")
        sem = self.rng.randint(1, 999)
        self.defs.append(
            f'<filter id="{fid}" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{frecuencia}" numOctaves="3" seed="{sem}" result="r"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="r" scale="{desplaza}" xChannelSelector="R" yChannelSelector="G" result="f"/>'
            f'<feMorphology in="f" operator="erode" radius="{erosion}" result="e"/>'
            f'<feGaussianBlur in="e" stdDeviation="{erosion * 2}" result="eb"/>'
            f'<feComposite in="f" in2="eb" operator="arithmetic" k1="0" k2="1" k3="-{borde}" k4="0" result="b"/>'
            f'<feTurbulence type="fractalNoise" baseFrequency="{frecuencia * 2.2:.4f}" numOctaves="2" seed="{sem + 3}" result="m"/>'
            f'<feColorMatrix in="m" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 2.2 0 0 -0.35" result="ma"/>'
            f'<feComposite in="f" in2="ma" operator="in" result="fm"/>'
            f'<feComposite in="fm" in2="eb" operator="arithmetic" k1="0" k2="0.5" k3="0" k4="0" result="manchas"/>'
            f'<feMerge result="t"><feMergeNode in="b"/><feMergeNode in="manchas"/></feMerge>'
            f'<feTurbulence type="fractalNoise" baseFrequency="{grano}" numOctaves="2" seed="{sem + 7}" result="g"/>'
            f'<feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.7 0 0 0 0.62" result="ga"/>'
            f'<feComposite in="t" in2="ga" operator="in"/>'
            f'</filter>')
        return fid

    def aguada(self, d, color=VIOLETA, opac=0.55, transform="", desplaza=16.0, capas=2, borde=0.55, capa="aguadas",
               erosion=3.0):
        """Una aguada: la tinta del esténcil con agua. Se oscurece en el borde, donde se seca primero."""
        tr = f' transform="{transform}"' if transform else ""
        for k in range(capas):
            fid = self.filtro_aguada(desplaza * (1 if k == 0 else 0.7), borde=borde, erosion=erosion)
            self.add(capa, f'<g filter="url(#{fid})" style="mix-blend-mode:multiply" opacity="{round(opac * (1 if k == 0 else 0.55), 3)}">'
                           f'<path d="{d}"{tr} fill="{color}" fill-rule="evenodd"/></g>')

    def mancha(self, cx, cy, rx, ry, irregular=0.18, lobulos=9, rot=0.0):
        """Una forma blanda, cerrada: el contorno de una mancha."""
        r = self.rng
        pts = []
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        for k in range(lobulos):
            a = 2 * math.pi * k / lobulos + r.uniform(-0.15, 0.15)
            f = 1 + r.uniform(-irregular, irregular)
            x, y = rx * f * math.cos(a), ry * f * math.sin(a)
            pts.append((cx + x * c - y * s, cy + x * s + y * c))
        return d_suave(spline(pts, 10, True), True), spline(pts, 10, True)

    def gota(self, x, y, r, largo_=2.2, rot=0.0):
        """Una gota que cae: redonda abajo, aguzada arriba (hacia donde estaba)."""
        pts = []
        for k in range(40):
            t = 2 * math.pi * k / 40
            px = r * math.sin(t) * (0.25 + 0.75 * ((1 - math.cos(t)) / 2) ** 0.9)
            py = -r * math.cos(t)
            if math.cos(t) > 0:
                py *= largo_
            pts.append((px, py))
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts = [(x + a * c - b * s, y + a * s + b * c) for a, b in pts]
        return d_suave(pts + pts[:2], True)

    def rayado(self, d, caja, angulo=-38.0, paso=3.4, color=GRAFITO, ancho=0.8, opac=0.95, transform="", capa="grafito",
               desvanece=None):
        """El grafito: un rayado a mano recortado a una forma. `desvanece` aclara el rayado hacia abajo."""
        cid = self.uid("clip")
        tr = f' transform="{transform}"' if transform else ""
        self.defs.append(f'<clipPath id="{cid}"><path d="{d}"{tr} clip-rule="evenodd"/></clipPath>')
        x0, y0, x1, y1 = caja
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        R = math.hypot(x1 - x0, y1 - y0) / 2 + 4
        a = math.radians(angulo)
        ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
        lineas, t = [], -R
        while t <= R:
            px, py = cx + vx * t, cy + vy * t
            p = self.temblar([(px - ux * R, py - uy * R), (px + ux * R, py + uy * R)], 0.3, 0.8, 5)
            o = opac * self.rng.uniform(0.6, 1)
            if desvanece is not None:
                o *= max(0.08, 1 - desvanece * (py - y0) / max(1, y1 - y0))
            lineas.append(f'<path d="{d_suave(p)}" opacity="{round(o, 2)}"/>')
            t += paso * self.rng.uniform(0.8, 1.2)
        self.add(capa, f'<g clip-path="url(#{cid})" filter="url(#lapiz)" fill="none" stroke="{color}" '
                       f'stroke-width="{ancho}" stroke-linecap="round">{"".join(lineas)}</g>')

    # -------------------------------------------------------------- celdas y signos
    def celda(self, cx, cy, w, color=TINTA, ancho=0.9, punteada=False, doble=True, capa="lineas"):
        """La celda de la cabeza del ídolo (0,84), a mano, abierta abajo en su desagüe."""
        h = w / 0.84
        cajas = [(cx - w / 2, cy - h / 2, w, h)]
        if doble:
            cajas.append((cx - w * 0.32, cy - h * 0.37, w * 0.64, h * 0.74))
        for x0, y0, ww, hh in cajas:
            g = min(5.0, ww * 0.09)
            m = x0 + ww / 2
            self.trazo([(m + g, y0 + hh), (x0 + ww, y0 + hh), (x0 + ww, y0), (x0, y0), (x0, y0 + hh), (m - g, y0 + hh)],
                       color, ancho, punteado=punteada, capa=capa, temblor=0.3, deriva=0.8)

    def signo(self, ref, x, y, escala, color=TINTA, rot=0.0, opac=1.0, capa="objetos"):
        """Un cuerpo de la gramática (definido una vez en defs) puesto en la hoja."""
        op = f' opacity="{opac}"' if opac < 1 else ""
        self.add(capa, f'<use href="#{ref}" transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(rot)}) scale({escala:.4f}) '
                       f'translate(-300 -300)" fill="{color}"{op}/>')

    # -------------------------------------------------------------- escritura
    def mano(self, x, y, t, tam=17.0, color=TINTA, ancla="start", rot=None, halo=True, opac=1.0, capa="textos"):
        """Letra de mano: lo que se hace con lo escrito."""
        rot = self.rng.uniform(-1.3, 1.3) if rot is None else rot
        h = f' stroke="{PAPEL}" stroke-width="{fmt(tam * 0.28)}" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        op = f' opacity="{opac}"' if opac < 1 else ""
        cuerpo = esc(t)
        if "{" in cuerpo:                                    # {…}: un signo suelto, a máquina, dentro de la nota
            cuerpo = cuerpo.replace("{", f'<tspan font-family="{MAQUINA}" font-size="{fmt(tam * 0.82)}">').replace(
                "}", "</tspan>")
        self.add(capa, f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{MANO}" font-size="{fmt(tam)}" fill="{color}" '
                       f'text-anchor="{ancla}" transform="rotate({fmt(rot)} {fmt(x)} {fmt(y)})"{h}{op}>{cuerpo}</text>')

    def manos(self, x, y, lineas, tam=17.0, color=TINTA, ancla="start", inter=1.12, **kw):
        for i, l in enumerate(lineas):
            self.mano(x + self.rng.uniform(-1.5, 1.5), y + i * tam * inter, l, tam, color, ancla, **kw)
        return y + (len(lineas) - 1) * tam * inter

    def maquina(self, x, y, t, tam=12.5, color=VIOLETA, ancla="start", halo=True, estilo="", peso=400, esp=0.0,
                rot=0.0, capa="textos", opac=1.0):
        """A máquina: lo que ya estaba escrito (el pie, el poema, los datos)."""
        h = f' stroke="{PAPEL}" stroke-width="{fmt(tam * 0.3)}" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        st = f' font-style="{estilo}"' if estilo else ""
        ls = f' letter-spacing="{esp}"' if esp else ""
        tr = f' transform="rotate({fmt(rot)} {fmt(x)} {fmt(y)})"' if rot else ""
        op = f' opacity="{opac}"' if opac < 1 else ""
        self.add(capa, f'<text x="{fmt(x)}" y="{fmt(y)}" font-family="{MAQUINA}" font-size="{fmt(tam)}" fill="{color}" '
                       f'text-anchor="{ancla}" font-weight="{peso}"{st}{ls}{tr}{h}{op}>{esc(t)}</text>')

    def maquinas(self, x, y, lineas, tam=12.5, color=VIOLETA, ancla="start", inter=1.3, **kw):
        for i, l in enumerate(lineas):
            self.maquina(x, y + i * tam * inter, l, tam, color, ancla, **kw)
        return y + (len(lineas) - 1) * tam * inter

    def sobre(self, pts, t, tam=15.0, color=TINTA, desde=50.0, dy=-4.0, ancla="middle", fuente=MANO, halo=True,
              capa="textos"):
        """Una nota escrita a lo largo de una línea, como se anota una órbita."""
        pid = self.uid("camino")
        pts = remuestrear(pts, 6)
        if pts[-1][0] < pts[0][0]:                              # que se lea de izquierda a derecha
            pts = pts[::-1]
        self.defs.append(f'<path id="{pid}" d="{d_suave(pts)}"/>')
        h = f' stroke="{PAPEL}" stroke-width="{fmt(tam * 0.28)}" paint-order="stroke" stroke-linejoin="round"' if halo else ""
        self.add(capa, f'<text font-family="{fuente}" font-size="{fmt(tam)}" fill="{color}" dy="{fmt(dy)}"{h}>'
                       f'<textPath href="#{pid}" startOffset="{fmt(desde)}%" text-anchor="{ancla}">{esc(t)}</textPath></text>')

    def muestra(self, x, y, tipo):
        """La muestra de una entrada de la leyenda, en 36 px de ancho."""
        if tipo == "continuo":
            self.trazo([(x, y), (x + 34, y - 1)], TINTA, 1.0)
        elif tipo == "punteado":
            self.trazo([(x, y), (x + 34, y - 1)], VIOLETA, 1.3, punteado=True)
        elif tipo == "orbita":
            self.orbita(x + 17, y, 17, 6, -8, hueco=26, ancho=0.8, pasadas=1)
        elif tipo == "flecha":
            self.flecha([(x, y), (x + 34, y)], TINTA, 0.8, curva=False)
        elif tipo == "corte":
            self.trazo([(x, y), (x + 30, y - 1)], GRAFITO, 0.7)
            self.trazo([(x + 31, y - 6), (x + 31, y + 5)], GRAFITO, 1.0, temblor=0.1, deriva=0)
        elif tipo == "cruz":
            self.trazo([(x, y), (x + 26, y)], TINTA, 0.8)
            self.cruz(x + 30, y, 4)
        elif tipo in ("violeta", "lila", "plata", "hueso", "gris"):
            color = {"violeta": VIOLETA, "lila": LILA, "plata": PLATA, "hueso": HUESO, "gris": GRAFITO}[tipo]
            d, _ = self.mancha(x + 17, y - 1, 17, 7, 0.12, 7)
            self.aguada(d, color, 0.7 if tipo == "violeta" else 0.95, desplaza=5, capas=1)
        elif tipo == "grafito":
            d, _ = self.mancha(x + 17, y - 1, 17, 7, 0.12, 7)
            self.rayado(d, (x - 2, y - 10, x + 36, y + 8), paso=2.6, ancho=0.7)
        elif tipo == "maquina":
            self.maquina(x, y + 4, "abc", 13, TINTA, halo=False)
        elif tipo == "mano":
            self.mano(x, y + 5, "abc", 17, TINTA, halo=False, rot=0)

    def leyenda(self, x, y, titulo, entradas, tam=15.5, inter=24.0):
        """La leyenda, a mano, en una esquina: una lista, sin caja."""
        if titulo:
            self.mano(x, y, titulo, tam + 2, TINTA, rot=-0.6)
            self.trazo([(x - 2, y + 7), (x + len(titulo) * tam * 0.48, y + 6)], TINTA, 0.7, temblor=0.4)
        for i, (tipo, texto) in enumerate(entradas):
            yy = y + 30 + i * inter
            self.muestra(x, yy - 4, tipo)
            self.mano(x + 46, yy, texto, tam, TINTA, rot=self.rng.uniform(-0.8, 0.5))
        return y + 30 + len(entradas) * inter

    def firma(self, x, y, n, total, titulo, fecha="La Paz, 30.9.2026", ancla="end"):
        self.mano(x, y, f"mapa {n} / {total} · {titulo}", 17, TINTA, ancla, rot=-1.0)
        self.mano(x, y + 22, f"Contenida · {fecha}", 15, GRAFITO, ancla, rot=-1.0)
        w = (len(f"Contenida · {fecha}")) * 7.2
        x0 = x - w if ancla == "end" else x
        self.trazo([(x0 - 6, y + 30), (x0 + w * 0.5, y + 28), (x0 + w + 8, y + 31)], TINTA, 0.8, pluma=True)

    # -------------------------------------------------------------- salida
    def svg(self):
        orden = ["papel", "aguadas", "grafito", "lineas", "objetos", "textos"]
        cuerpo = "\n".join("\n".join(self.capas[c]) for c in orden)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}" width="{self.W}" '
                f'height="{self.H}"><defs>{"".join(self.defs)}</defs>\n{cuerpo}\n</svg>\n')
