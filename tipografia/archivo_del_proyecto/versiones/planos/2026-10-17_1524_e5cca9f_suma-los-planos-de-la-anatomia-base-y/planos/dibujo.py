"""El dibujo técnico de los planos: la hoja A3, las líneas, las cotas y el cajetín.

Todo se dibuja en milímetros de la hoja (420 × 297, y hacia abajo). Las
convenciones siguen el dibujo de arquitectura (ISO 128 y 129, a mano alzada
de la norma): grosores fijos por tipo de línea, cotas con trazo oblicuo,
ejes de trazo y punto, y un cajetín abajo a la derecha. En lugar del norte,
cada lámina lleva la gravedad.
"""

import html
import math
from pathlib import Path

from fontTools.ttLib import TTFont

AQUI = Path(__file__).resolve().parent
FUENTES = AQUI.parent / "laminas" / "fuentes"

ANCHO, ALTO = 420.0, 297.0
MARCO = (20.0, 10.0, 410.0, 287.0)          # izquierda 20 mm, para encuadernar
COLUMNA = (289.0, 15.0, 405.0, 229.0)       # el «por qué»
CAJETIN = (284.0, 234.0, 410.0, 287.0)
DIBUJO = (25.0, 15.0, 279.0, 282.0)

TINTA, GRIS, GRIS2, FILETE = "#1d1c1a", "#6d6a63", "#9a968d", "#cfcac0"
VIOLETA, PAPEL, PLATA = "#4a2470", "#f6f4ee", "#e2e0d9"
MONO, SERIF = "Courier Prime", "Newsreader"

# grosores (mm) y trazos de cada tipo de línea
LINEAS = {
    "contorno": dict(w=0.5, color=TINTA),
    "contorno_r": dict(w=0.5, color=VIOLETA, dash="0.1 1.05", cap="round"),     # lo reconstruido: a puntos
    "eje": dict(w=0.18, color=TINTA, dash="7 1.2 0.6 1.2"),
    "linea": dict(w=0.25, color=GRIS, dash="3 1.6"),
    "celda": dict(w=0.3, color=TINTA),
    "placa": dict(w=0.35, color=GRIS),
    "cota": dict(w=0.18, color=TINTA),
    "aux": dict(w=0.15, color=GRIS, dash="0.8 0.9"),
    "aux_continua": dict(w=0.15, color=GRIS),
    "fina": dict(w=0.13, color=GRIS2),
    "marco": dict(w=0.7, color=TINTA),
    "filete": dict(w=0.25, color=TINTA),
    "comparar": dict(w=0.25, color=GRIS, dash="1.6 1.2"),
    "rotura": dict(w=0.35, color=TINTA, dash="2.4 1 0.5 1"),
}


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def coma(x, d=1):
    s = f"{x:.{d}f}".replace(".", ",")
    return "0" if s in ("-0", "-0,0") else s


def estilo(tipo, **extra):
    L = dict(LINEAS[tipo], **extra)
    s = f'fill="none" stroke="{L["color"]}" stroke-width="{f(L["w"])}"'
    if L.get("dash"):
        s += f' stroke-dasharray="{L["dash"]}"'
    s += f' stroke-linecap="{L.get("cap", "butt")}" stroke-linejoin="round"'
    return s


# ---------------------------------------------------------------- medir texto

class Medidor:
    def __init__(self):
        self.f = {}

    def fuente(self, familia, peso, cursiva):
        clave = (familia, peso, cursiva)
        if clave not in self.f:
            if familia == MONO:
                nombre = "courier-prime-latin-700-normal" if peso >= 600 else (
                    "courier-prime-latin-400-italic" if cursiva else "courier-prime-latin-400-normal")
            else:
                p = 500 if peso >= 500 else (300 if peso <= 300 else 400)
                nombre = f"newsreader-latin-{p}-{'italic' if cursiva else 'normal'}"
                if not (FUENTES / f"{nombre}.woff2").exists():
                    nombre = f"newsreader-latin-400-{'italic' if cursiva else 'normal'}"
            t = TTFont(FUENTES / f"{nombre}.woff2")
            self.f[clave] = (t.getBestCmap(), t["hmtx"].metrics, t["head"].unitsPerEm)
        return self.f[clave]

    def ancho(self, s, tam, familia=SERIF, peso=400, cursiva=False):
        cmap, hmtx, upm = self.fuente(familia, peso, cursiva)
        total = 0
        for ch in s:
            g = cmap.get(ord(ch))
            total += hmtx[g][0] if g else upm * 0.5
        return total * tam / upm


MEDIR = Medidor()


def _palabras(texto):
    """Divide un texto con **negrita** y _cursiva_ en palabras con su estilo."""
    out, negrita, cursiva, actual = [], False, False, ""
    i = 0
    while i < len(texto):
        if texto.startswith("**", i):
            if actual:
                out.append((actual, negrita, cursiva))
                actual = ""
            negrita = not negrita
            i += 2
            continue
        ch = texto[i]
        if ch == "_" and (i == 0 or not texto[i - 1].isalnum() or cursiva):
            if actual:
                out.append((actual, negrita, cursiva))
                actual = ""
            cursiva = not cursiva
            i += 1
            continue
        if ch == " ":
            if actual:
                out.append((actual, negrita, cursiva))
                actual = ""
            out.append((" ", negrita, cursiva))
        else:
            actual += ch
        i += 1
    if actual:
        out.append((actual, negrita, cursiva))
    return out


# ---------------------------------------------------------------- la hoja

class Hoja:
    CAPAS = ("papel", "fondo", "aux", "cuerpo", "ejes", "cotas", "textos", "marco")

    def __init__(self, codigo, titulo, subtitulo, escala, n, total, fecha="17.10.2026"):
        self.codigo, self.titulo, self.subtitulo, self.escala = codigo, titulo, subtitulo, escala
        self.n, self.total, self.fecha = n, total, fecha
        self.capas = {c: [] for c in self.CAPAS}
        self.defs = []
        self._clip = 0

    def add(self, capa, s):
        self.capas[capa].append(s)

    # -- primitivas
    def linea(self, a, b, tipo="cota", capa="cotas", **extra):
        self.add(capa, f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" {estilo(tipo, **extra)}/>')

    def poli(self, pts, tipo="contorno", capa="cuerpo", cerrado=False, **extra):
        if len(pts) < 2:
            return
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + (" Z" if cerrado else "")
        self.add(capa, f'<path d="{d}" {estilo(tipo, **extra)}/>')

    def circulo(self, c, r, tipo="cota", capa="cotas", relleno=None, **extra):
        s = estilo(tipo, **extra)
        if relleno:
            s = s.replace('fill="none"', f'fill="{relleno}"')
        self.add(capa, f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" {s}/>')

    def punto(self, c, r=0.45, color=TINTA, capa="cotas"):
        self.add(capa, f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="{f(r)}" fill="{color}"/>')

    def nodo(self, c, capa="ejes"):
        self.add(capa, f'<circle cx="{f(c[0])}" cy="{f(c[1])}" r="0.7" fill="{PAPEL}" stroke="{TINTA}" '
                       f'stroke-width="0.18"/>')

    def relleno(self, d, color, capa="cuerpo", regla="evenodd", opacidad=1.0):
        self.add(capa, f'<path d="{d}" fill="{color}" fill-rule="{regla}" fill-opacity="{f(opacidad)}" stroke="none"/>')

    def texto(self, x, y, s, tam=2.5, ancla="start", familia=MONO, peso=400, cursiva=False, color=TINTA,
              rot=0, capa="textos", espaciado=0.0, fondo=False):
        tr = f' transform="rotate({f(rot)} {f(x)} {f(y)})"' if rot else ""
        st = ' font-style="italic"' if cursiva else ""
        es = f' letter-spacing="{f(espaciado)}"' if espaciado else ""
        halo = (f' paint-order="stroke" stroke="{PAPEL}" stroke-width="{f(tam * 0.32)}" stroke-linejoin="round"'
                if fondo else "")
        self.add(capa, f'<text x="{f(x)}" y="{f(y)}" font-family="{familia}" font-size="{f(tam)}" '
                       f'font-weight="{peso}"{st}{es} fill="{color}" text-anchor="{ancla}"{tr}{halo}>'
                       f'{html.escape(s)}</text>')

    def parrafo(self, x, y, ancho, texto, tam=2.9, inter=1.38, familia=SERIF, peso=300, cursiva=False,
                color=TINTA, sangria=0.0, capa="textos"):
        """Un párrafo con **negrita** y _cursiva_, cortado al ancho. Devuelve la y de la línea siguiente."""
        palabras = _palabras(texto)
        lineas, linea, w = [], [], sangria
        for p, neg, cur in palabras:
            ancho_p = MEDIR.ancho(p, tam, familia, 500 if neg else peso, cur or cursiva)
            if p == " ":
                if linea:
                    linea.append((p, neg, cur))
                    w += ancho_p
                continue
            if w + ancho_p > ancho and linea:
                while linea and linea[-1][0] == " ":
                    linea.pop()
                lineas.append(linea)
                linea, w = [], 0.0
            linea.append((p, neg, cur))
            w += ancho_p
        if linea:
            lineas.append(linea)
        for i, ln in enumerate(lineas):
            partes = []
            for p, neg, cur in ln:
                if partes and partes[-1][1:] == (neg, cur):
                    partes[-1] = (partes[-1][0] + p, neg, cur)
                else:
                    partes.append((p, neg, cur))
            it = ' font-style="italic"'
            tspans = "".join(
                f'<tspan font-weight="{500 if neg else peso}"{it if (cur or cursiva) else ""}>'
                f'{html.escape(p)}</tspan>' for p, neg, cur in partes)
            x0 = x + (sangria if i == 0 else 0)
            self.add(capa, f'<text x="{f(x0)}" y="{f(y)}" font-family="{familia}" font-size="{f(tam)}" '
                           f'fill="{color}" xml:space="preserve">{tspans}</text>')
            y += tam * inter
        return y

    def recorte(self, x0, y0, x1, y1):
        """Abre un grupo recortado a un rectángulo; cerrar con fin_recorte()."""
        self._clip += 1
        cid = f"r{self.codigo}_{self._clip}"
        self.defs.append(f'<clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" '
                         f'height="{f(y1 - y0)}"/></clipPath>')
        for c in ("aux", "cuerpo", "ejes"):
            self.add(c, f'<g clip-path="url(#{cid})">')
        return cid

    def fin_recorte(self):
        for c in ("aux", "cuerpo", "ejes"):
            self.add(c, "</g>")

    # -- cotas (ISO 129, con trazo oblicuo de arquitectura)
    def cota(self, a, b, sep, texto, tam=2.4, ext=True, desde=1.2, sobra=1.6, color=TINTA, lado_texto=1,
             ticks=True, capa="cotas"):
        """Cota alineada con a→b, corrida `sep` mm a la izquierda del sentido a→b (negativo: a la derecha)."""
        ax, ay = a
        bx, by = b
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-6:
            return
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = uy, -ux                        # normal a la izquierda (y hacia abajo)
        s = 1 if sep >= 0 else -1
        pa = (ax + nx * sep, ay + ny * sep)
        pb = (bx + nx * sep, by + ny * sep)
        if ext:
            for p in (a, b):
                self.linea((p[0] + nx * s * desde, p[1] + ny * s * desde),
                           (p[0] + nx * (sep + s * sobra), p[1] + ny * (sep + s * sobra)), "cota", capa)
        self.linea((pa[0] - ux * 1.5, pa[1] - uy * 1.5), (pb[0] + ux * 1.5, pb[1] + uy * 1.5), "cota", capa)
        if ticks:
            for p in (pa, pb):                  # el trazo oblicuo, a 45°
                tx, ty = (ux + nx) / math.sqrt(2), (uy + ny) / math.sqrt(2)
                self.add(capa, f'<line x1="{f(p[0] - tx * 1.3)}" y1="{f(p[1] - ty * 1.3)}" x2="{f(p[0] + tx * 1.3)}" '
                               f'y2="{f(p[1] + ty * 1.3)}" stroke="{color}" stroke-width="0.4"/>')
        ang = math.degrees(math.atan2(uy, ux))
        if ang > 90.01 or ang < -90.01:
            ang += 180
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        # el texto, encima de la línea de cota (del lado de afuera)
        rad = math.radians(ang)
        ox, oy = math.sin(rad), -math.cos(rad)
        d = 0.9 * lado_texto
        tx, ty = mx + ox * d, my + oy * d
        if lado_texto < 0:
            tx, ty = mx - ox * (tam * 0.75 + 0.9), my - oy * (tam * 0.75 + 0.9)
        self.texto(tx, ty, texto, tam, "middle", rot=ang, color=color, capa=capa, fondo=True)

    def cota_angular(self, c, r, a0, a1, texto, tam=2.4, capa="cotas"):
        """Arco de cota entre los ángulos a0 y a1 (grados, antihorario como en el papel: y hacia arriba)."""
        pts = []
        n = max(8, int(abs(a1 - a0) / 3))
        for i in range(n + 1):
            t = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((c[0] + r * math.cos(t), c[1] - r * math.sin(t)))
        self.poli(pts, "cota", capa)
        for ang, sgn in ((a0, 1), (a1, -1)):
            t = math.radians(ang)
            p = (c[0] + r * math.cos(t), c[1] - r * math.sin(t))
            # flecha tangente al arco
            tg = (-math.sin(t) * sgn * (1 if a1 > a0 else -1), -math.cos(t) * sgn * (1 if a1 > a0 else -1))
            self.flecha(p, (p[0] + tg[0] * 2.2, p[1] + tg[1] * 2.2), capa=capa)
        tm = math.radians((a0 + a1) / 2)
        self.texto(c[0] + (r + 2.6) * math.cos(tm), c[1] - (r + 2.6) * math.sin(tm) + tam * 0.35, texto, tam,
                   "middle", capa=capa, fondo=True)

    def flecha(self, punta, cola, largo=2.2, ancho=0.75, capa="cotas", color=TINTA):
        dx, dy = punta[0] - cola[0], punta[1] - cola[1]
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        b = (punta[0] - ux * largo, punta[1] - uy * largo)
        p1 = (b[0] + uy * ancho, b[1] - ux * ancho)
        p2 = (b[0] - uy * ancho, b[1] + ux * ancho)
        self.add(capa, f'<path d="M{f(punta[0])},{f(punta[1])} L{f(p1[0])},{f(p1[1])} L{f(p2[0])},{f(p2[1])} Z" '
                       f'fill="{color}"/>')

    def cota_radio(self, c, r, ang, texto, largo=10, tam=2.4, capa="cotas", prefijo="R "):
        t = math.radians(ang)
        p = (c[0] + r * math.cos(t), c[1] - r * math.sin(t))
        q = (c[0] + (r + largo) * math.cos(t), c[1] - (r + largo) * math.sin(t))
        self.linea(c, q, "cota", capa)
        self.flecha(p, q, capa=capa)
        derecha = math.cos(t) >= 0
        h = (q[0] + (6 if derecha else -6), q[1])
        self.linea(q, h, "cota", capa)
        self.texto(h[0] + (0.8 if derecha else -0.8), h[1] + tam * 0.35, prefijo + texto, tam,
                   "start" if derecha else "end", capa=capa)

    def nota(self, p, q, texto, tam=2.4, ancla=None, color=TINTA, punto=True, lineas=None, familia=MONO,
             capa="cotas", cursiva=False):
        """Una llamada: un punto en p, una línea hasta q y el texto (una o varias líneas) a continuación."""
        if punto:
            self.punto(p, 0.5, color, capa)
        self.linea(p, q, "cota", capa, color=color)
        derecha = (ancla or ("start" if q[0] >= p[0] else "end")) == "start"
        h = (q[0] + (3 if derecha else -3), q[1])
        self.linea(q, h, "cota", capa, color=color)
        renglones = lineas if lineas else [texto]
        for i, r in enumerate(renglones):
            self.texto(h[0] + (0.8 if derecha else -0.8), h[1] + tam * 0.35 + i * tam * 1.25, r, tam,
                       "start" if derecha else "end", familia=familia, color=color, capa=capa, cursiva=cursiva)

    # -- símbolos de arquitectura
    def llamada(self, x, y, numero, hoja=None, titulo="", escala="", r=4.2):
        """El círculo de vista o de detalle: número arriba, hoja abajo; el título y la escala al lado."""
        self.circulo((x, y), r, "filete", "textos")
        self.linea((x - r, y), (x + r, y), "filete", "textos")
        self.texto(x, y - 1.0, str(numero), 3.0, "middle", peso=700)
        self.texto(x, y + 3.0, hoja or self.codigo, 1.9, "middle")
        if titulo:
            self.texto(x + r + 2.5, y - 0.6, titulo, 3.0, peso=700, espaciado=0.15)
            w = MEDIR.ancho(titulo, 3.0, MONO, 700) + len(titulo) * 0.15
            self.linea((x + r + 2.5, y + 0.8), (x + r + 2.5 + w, y + 0.8), "filete", "textos")
            if escala:
                self.texto(x + r + 2.5, y + 4.2, escala, 2.3, color=GRIS)

    def gravedad(self, x, y, r=5.0):
        """En el lugar del norte: la gravedad. Lo que mira abajo gotea."""
        self.circulo((x, y), r, "filete", "textos")
        self.linea((x, y - r - 1.5), (x, y + r - 2.4), "filete", "textos", w=0.35)
        self.flecha((x, y + r + 1.2), (x, y - r), largo=3.6, ancho=1.5, capa="textos")
        self.texto(x, y - r - 2.6, "g", 2.6, "middle", familia=SERIF, cursiva=True)
        self.texto(x, y + r + 4.6, "GRAVEDAD", 1.9, "middle", espaciado=0.25)

    def escala_grafica(self, x, y, mm_por_mm=1.0, total=50, paso=10, rotulo="mm"):
        """Barra de escala: `total` mm reales, dibujados a la escala de la vista."""
        n = int(total / paso)
        L = paso * mm_por_mm
        for i in range(n):
            color = TINTA if i % 2 == 0 else PAPEL
            self.add("textos", f'<rect x="{f(x + i * L)}" y="{f(y)}" width="{f(L)}" height="1.4" fill="{color}" '
                               f'stroke="{TINTA}" stroke-width="0.18"/>')
        for i in range(n + 1):
            self.texto(x + i * L, y + 4.0, str(i * paso), 1.9, "middle")
        self.texto(x + n * L + 3, y + 1.4, rotulo, 1.9)

    # -- el marco y el cajetín
    def marco(self):
        x0, y0, x1, y1 = MARCO
        self.add("marco", f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" '
                          f'{estilo("marco")}/>')
        # zonas de referencia, como en los planos: números arriba, letras al costado
        for i, x in enumerate(range(int(x0), int(x1), 65)):
            if i:
                self.linea((x, y0), (x, y0 - 3), "filete", "marco")
                self.linea((x, y1), (x, y1 + 3), "filete", "marco")
            self.texto(x + 32.5, y0 - 1.5, str(i + 1), 2.0, "middle", capa="marco", color=GRIS)
            self.texto(x + 32.5, y1 + 4.5, str(i + 1), 2.0, "middle", capa="marco", color=GRIS)
        for i, y in enumerate(range(int(y0), int(y1), 55)):
            if i:
                self.linea((x0, y), (x0 - 3, y), "filete", "marco")
                self.linea((x1, y), (x1 + 3, y), "filete", "marco")
            self.texto(x0 - 4.5, y + 27.5 + 0.7, "ABCDEF"[i], 2.0, "middle", capa="marco", color=GRIS)
            self.texto(x1 + 4.5, y + 27.5 + 0.7, "ABCDEF"[i], 2.0, "middle", capa="marco", color=GRIS)
        # marcas de centrado
        for p, q in (((ANCHO / 2, 0), (ANCHO / 2, y0)), ((ANCHO / 2, y1), (ANCHO / 2, ALTO)),
                     ((0, ALTO / 2), (x0, ALTO / 2)), ((x1, ALTO / 2), (ANCHO, ALTO / 2))):
            self.linea(p, q, "filete", "marco", w=0.5)
        # la columna del «por qué»
        self.linea((CAJETIN[0], y0), (CAJETIN[0], y1), "filete", "marco", w=0.5)
        self.cajetin()

    def cajetin(self):
        x0, y0, x1, y1 = CAJETIN
        c = "marco"
        self.add(c, f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{PAPEL}" '
                    f'stroke="{TINTA}" stroke-width="0.5"/>')
        filas = [y0 + 12, y0 + 27, y0 + 38]
        for y in filas:
            self.linea((x0, y), (x1, y), "filete", c)
        xc = x1 - 26
        self.linea((xc, y0), (xc, filas[1]), "filete", c)
        cols = [x0 + 30, x0 + 64, x0 + 96]
        for x in cols:
            self.linea((x, filas[1]), (x, filas[2]), "filete", c)
        T = self.texto
        T(x0 + 2.5, y0 + 5.6, "CONTENIDA", 4.4, peso=700, espaciado=0.6, capa=c)
        T(x0 + 2.5, y0 + 9.8, "la anatomía base · planos de la gramática", 2.3, capa=c, color=GRIS)
        T(xc + 13, y0 + 10.2, self.codigo, 7.0, "middle", peso=700, capa=c)
        T(x0 + 2.5, y0 + 19.6, self.titulo, 5.0, familia=SERIF, peso=400, capa=c)
        T(x0 + 2.5, y0 + 24.6, self.subtitulo, 2.3, capa=c, color=GRIS)
        T(xc + 13, y0 + 16.0, "HOJA", 1.8, "middle", capa=c, color=GRIS, espaciado=0.2)
        T(xc + 13, y0 + 22.8, f"{self.n} / {self.total}", 3.6, "middle", capa=c)
        campos = [("ESCALA", self.escala), ("UNIDADES", "mm · (UPM)"), ("FECHA", self.fecha),
                  ("FORMATO", "A3 · 420 × 297")]
        xs = [x0] + cols
        for (k, v), x in zip(campos, xs):
            T(x + 1.6, filas[1] + 3.2, k, 1.7, capa=c, color=GRIS, espaciado=0.2)
            T(x + 1.6, filas[1] + 8.4, v, 2.5, capa=c)
        T(x0 + 1.6, filas[2] + 3.4, "DIBUJÓ", 1.7, capa=c, color=GRIS, espaciado=0.2)
        T(x0 + 16, filas[2] + 3.4, "la gramática (simulacion/gramatica.py): propuesta de la máquina", 2.1, capa=c)
        T(x0 + 1.6, filas[2] + 7.6, "CALCA", 1.7, capa=c, color=GRIS, espaciado=0.2)
        T(x0 + 16, filas[2] + 7.6, "la mano, desde el pie de la lámina (04, acciones 3 y 4)", 2.1, capa=c)
        T(x0 + 1.6, filas[2] + 11.8, "NOTA", 1.7, capa=c, color=GRIS, espaciado=0.2)
        T(x0 + 16, filas[2] + 11.8, "regla de la forma, no pauta de calco: no entra en la caja", 2.1, capa=c)

    # -- la referencia: el número de una decisión, en un rombo (como las notas clave de un plano)
    def rombo(self, c, n, r=2.5, capa="cotas"):
        x, y = c
        self.add(capa, f'<path d="M{f(x)},{f(y - r)} L{f(x + r)},{f(y)} L{f(x)},{f(y + r)} L{f(x - r)},{f(y)} Z" '
                       f'fill="{PAPEL}" stroke="{VIOLETA}" stroke-width="0.3"/>')
        self.texto(x, y + 0.85, str(n), 2.35, "middle", peso=700, color=VIOLETA, capa=capa)

    def clave(self, p, q, n):
        """Marca en el dibujo el lugar de la decisión n: un punto, una línea y el rombo."""
        self.punto(p, 0.45, VIOLETA)
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        if L > 2.6:
            self.linea(p, (q[0] - dx / L * 2.5, q[1] - dy / L * 2.5), "cota", "cotas", color=VIOLETA, w=0.2)
        self.rombo(q, n)

    # -- la columna del porqué
    def columna(self, bloques, tam=2.75):
        """bloques: lista de (tipo, contenido). tipo: titulo, p, verso, decision, linea, espacio."""
        x0, y, x1, ymax = COLUMNA
        ancho = x1 - x0
        for tipo, cont in bloques:
            if tipo == "titulo":
                y += 0.8
                self.texto(x0, y + 2.4, cont.upper(), 2.45, peso=700, espaciado=0.35)
                self.linea((x0, y + 3.5), (x1, y + 3.5), "filete", "textos", w=0.3)
                y += 7.0
            elif tipo == "p":
                y = self.parrafo(x0, y + 2.3, ancho, cont, tam, peso=300) - 2.3 + 1.5
            elif tipo == "verso":
                for v in cont.split("\n"):
                    self.texto(x0 + 4, y + 2.6, v, tam * 1.06, familia=SERIF, cursiva=True, peso=400)
                    y += tam * 1.06 * 1.3
                y += 1.6
            elif tipo == "decision":
                n, termino, texto, verso = cont
                self.rombo((x0 + 2.5, y + 2.3), n, capa="textos")
                self.texto(x0 + 6.6, y + 3.1, termino.upper(), 2.3, peso=700, espaciado=0.1, capa="textos")
                y += 5.6
                y = self.parrafo(x0 + 6.6, y + 2.3, ancho - 6.6, texto, tam, peso=300) - 2.3 + 0.4
                if verso:
                    y += 0.6
                    for v in verso.split("\n"):
                        self.texto(x0 + 10, y + 2.5, v, tam * 1.04, familia=SERIF, cursiva=True, peso=400)
                        y += tam * 1.04 * 1.3
                y += 2.6
            elif tipo == "linea":
                self.linea((x0, y + 1), (x1, y + 1), "fina", "textos")
                y += 3
            elif tipo == "espacio":
                y += cont
        if y > ymax + 0.5:
            print(f"  ! {self.codigo}: la columna se pasa {y - ymax:.1f} mm")
        else:
            print(f"    {self.codigo}: sobran {ymax - y:.1f} mm en la columna")
        return y

    def svg(self, fuentes_rel="../../laminas/fuentes"):
        caras = "".join(
            f'@font-face{{font-family:"{fam}";src:url({fuentes_rel}/{arch}.woff2) format("woff2"),'
            f'url(../fuentes/{arch}.woff2) format("woff2");'
            f'font-weight:{p};font-style:{st}}}'
            for fam, arch, p, st in (
                (SERIF, "newsreader-latin-300-normal", 300, "normal"),
                (SERIF, "newsreader-latin-400-normal", 400, "normal"),
                (SERIF, "newsreader-latin-500-normal", 500, "normal"),
                (SERIF, "newsreader-latin-300-italic", 300, "italic"),
                (SERIF, "newsreader-latin-400-italic", 400, "italic"),
                (MONO, "courier-prime-latin-400-normal", 400, "normal"),
                (MONO, "courier-prime-latin-700-normal", 700, "normal"),
                (MONO, "courier-prime-latin-400-italic", 400, "italic")))
        patron = (f'<pattern id="metal" patternUnits="userSpaceOnUse" width="1.1" height="1.1" '
                  f'patternTransform="rotate(45)"><rect width="1.1" height="1.1" fill="{PLATA}"/>'
                  f'<line x1="0" y1="0" x2="0" y2="1.1" stroke="#a9a69d" stroke-width="0.16"/></pattern>'
                  f'<pattern id="metal_r" patternUnits="userSpaceOnUse" width="1.1" height="1.1" '
                  f'patternTransform="rotate(45)"><rect width="1.1" height="1.1" fill="#ebe6ef"/>'
                  f'<line x1="0" y1="0" x2="0" y2="1.1" stroke="#b9a9c9" stroke-width="0.16"/></pattern>'
                  f'<pattern id="blanda" patternUnits="userSpaceOnUse" width="2.2" height="2.2">'
                  f'<rect width="2.2" height="2.2" fill="{PAPEL}"/><circle cx="0.55" cy="0.55" r="0.22" fill="{GRIS2}"/>'
                  f'<circle cx="1.65" cy="1.65" r="0.22" fill="{GRIS2}"/></pattern>')
        cuerpo = "\n".join("\n".join(self.capas[c]) for c in self.CAPAS)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(ANCHO)} {f(ALTO)}" width="{f(ANCHO)}mm" '
                f'height="{f(ALTO)}mm">\n<title>Contenida · {self.codigo} · {html.escape(self.titulo)}</title>\n'
                f'<defs><style>{caras}</style>{patron}{"".join(self.defs)}</defs>\n'
                f'<rect width="{f(ANCHO)}" height="{f(ALTO)}" fill="{PAPEL}"/>\n{cuerpo}\n</svg>\n')


# ---------------------------------------------------------------- la vista: del lienzo de la placa a la hoja

class Vista:
    """Pone el lienzo de la placa (px, 4 por mm) en la hoja, a una escala: 1 es 1:1, 2 es 2:1, 0,5 es 1:2."""

    def __init__(self, hoja, ox, oy, escala=1.0, px0=0.0, py0=0.0):
        self.h, self.ox, self.oy, self.k = hoja, ox, oy, escala
        self.px0, self.py0 = px0, py0

    def p(self, x, y=None):
        if y is None:
            x, y = x
        return (self.ox + self.k * (x - self.px0) / 4, self.oy + self.k * (y - self.py0) / 4)

    def mm(self, v_px):
        return self.k * v_px / 4

    def d(self, anillos):
        return " ".join("M" + " L".join(f"{f(a)},{f(b)}" for a, b in (self.p(x, y) for x, y in r)) + " Z"
                        for r in anillos)

    def signo(self, S, reconstruido=None, ejes=True, nodos=True, rayado=True, capa="cuerpo", contorno=None,
              color_relleno=None):
        """El cuerpo del signo: relleno de metal y contorno; encima, los ejes de sus trazos y los nodos."""
        r = S["estado"] == "reconstruida" if reconstruido is None else reconstruido
        d = self.d(S["contorno"])
        if color_relleno:
            self.h.relleno(d, color_relleno, capa)
        elif rayado:
            self.h.relleno(d, "url(#metal_r)" if r else "url(#metal)", capa)
        tipo = contorno or ("contorno_r" if r else "contorno")
        w = LINEAS[tipo]["w"] * (min(1.0, max(0.55, self.k)) if self.k < 1 else 1.0)
        self.h.add(capa, f'<path d="{d}" {estilo(tipo, w=w)}/>')
        if ejes:
            for pts, ancho in S["trazos"]:
                if ancho is not None and ancho < 1:
                    continue
                self.h.poli([self.p(x, y) for x, y in pts], "eje", "ejes")
        if nodos:
            for x, y in S["nodos"]:
                self.h.nodo(self.p(x, y))

    def lineas(self, e, x0_px, x1_px, rotulos=True, tam=2.2, lado="izq", valores=True):
        """Las cuatro líneas de la gramática, de x0 a x1 (px)."""
        for nombre, clave in (("afuera", "afuera"), ("borde", "borde"), ("fondo", "fondo"), ("desagüe", "desague")):
            y = e[clave]
            a, b = self.p(x0_px, y), self.p(x1_px, y)
            self.h.linea(a, b, "linea", "fondo")
            if rotulos:
                if lado == "izq":
                    self.h.texto(a[0] - 1.5, a[1] + tam * 0.35, nombre, tam, "end", color=GRIS, capa="cotas")
                else:
                    self.h.texto(b[0] + 1.5, b[1] + tam * 0.35, nombre, tam, "start", color=GRIS, capa="cotas")

    def celda(self, e, tipo="celda"):
        x0, y0, x1, y1 = e["celda"]
        a, b = self.p(x0, y0), self.p(x1, y1)
        self.h.add("fondo", f'<rect x="{f(a[0])}" y="{f(a[1])}" width="{f(b[0] - a[0])}" height="{f(b[1] - a[1])}" '
                            f'{estilo(tipo)}/>')

    def placa(self, tipo="placa"):
        a, b = self.p(0, 0), self.p(600, 600)
        self.h.add("fondo", f'<rect x="{f(a[0])}" y="{f(a[1])}" width="{f(b[0] - a[0])}" height="{f(b[1] - a[1])}" '
                            f'{estilo(tipo)}/>')
