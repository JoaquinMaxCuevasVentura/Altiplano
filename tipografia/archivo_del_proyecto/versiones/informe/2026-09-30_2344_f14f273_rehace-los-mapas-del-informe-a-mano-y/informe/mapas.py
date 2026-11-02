"""Los mapas del informe de decisiones de Contenida, dibujados a mano (con código).

Uso (desde la raíz del repositorio):
    python3 tipografia/informe/mapas.py            # los seis
    python3 tipografia/informe/mapas.py 1 4        # solo esos

Escribe en tipografia/informe/mapas/ seis mapas en SVG y en PNG (con Chromium,
como las láminas). El repertorio de trazos está en mano.py: líneas que tiemblan
apenas, órbitas abiertas en su punto más bajo, aguadas de tinta de esténcil,
rayados de grafito, notas a mano sobre las líneas y, a máquina, lo que ya estaba
escrito. No hay marcos, ni cajas, ni tablas: cada mapa lleva su leyenda a mano,
en una esquina, y su firma.

Los cuerpos de los signos vienen de la gramática (simulacion/desenterrar.py): son
la propuesta de la máquina y, como en las láminas, no entran en la caja.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
SALIDA = AQUI / "mapas"
FUENTES = TIPO / "laminas" / "fuentes"
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(TIPO / "laminas"))

from mano import (GRAFITO, GRAFITO2, HUESO, LILA, PAPEL, PLATA, TINTA, VIOLETA, Hoja,  # noqa: E402
                  Perspectiva, bezier, d_suave, elipse_pts, normales, remuestrear, spline)

TOTAL = 6
CAJA = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
ESTADO = {c["signo"]: c["estado"] for c in CAJA["celdas"]}
C_ACTUAL = {}


# ------------------------------------------------------------------ los cuerpos de la gramática

def cuerpos(cache=None):
    """{signo: path d} en el lienzo de la placa (600 px = 150 mm), y el esqueleto."""
    if cache and Path(cache).exists():
        return json.loads(Path(cache).read_text(encoding="utf8"))
    sys.path.insert(0, str(TIPO / "simulacion"))
    from desenterrar import desenterrar
    D = desenterrar()

    def d_de(geo):
        out = []
        for p in (list(geo.geoms) if hasattr(geo, "geoms") else [geo]):
            for anillo in [p.exterior, *p.interiors]:
                c = list(anillo.coords)[:-1]
                out.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in c) + "Z")
        return " ".join(out)

    e = D["esqueleto"]
    datos = dict(signos={s: dict(d=d_de(v["geo"].simplify(0.4)), receta=v["receta"]) for s, v in D["gramatica"].items()},
                 esqueleto={k: float(e[k]) for k in ("afuera", "borde", "fondo", "desague", "xh", "canal")})
    if cache:
        Path(cache).write_text(json.dumps(datos, ensure_ascii=False), encoding="utf8")
    return datos


def partir(texto, ancho):
    """Corta un texto en renglones de a lo sumo `ancho` caracteres, por palabras."""
    renglones, r = [], ""
    for p in texto.split():
        if r and len(r) + 1 + len(p) > ancho:
            renglones.append(r)
            r = p
        else:
            r = f"{r} {p}".strip()
    return renglones + ([r] if r else [])


def ref(s):
    return f"s{ord(s)}"


def definir(H, signos):
    """Pone en defs los cuerpos que el mapa usa (cada uno una vez)."""
    for s in dict.fromkeys(signos):
        H.defs.append(f'<path id="{ref(s)}" d="{C_ACTUAL["signos"][s]["d"]}" fill-rule="evenodd"/>')


def _tr(x, y, escala, rot):
    return f"translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({escala:.4f}) translate(-300 -320)"


def contorno(H, s, x, y, escala, color=TINTA, ancho=0.9, punteado=False, rot=0.0, capa="objetos", opac=1.0):
    """El contorno de un signo, como se calca: continuo si es hallado, punteado si es reconstruido."""
    dash = f' stroke-dasharray="0.1 {3.6 / escala:.1f}" stroke-linecap="round"' if punteado else ""
    op = f' opacity="{opac}"' if opac < 1 else ""
    H.add(capa, f'<use href="#{ref(s)}" transform="{_tr(x, y, escala, rot)}" fill="none" stroke="{color}" '
                f'stroke-width="{ancho / escala:.2f}" stroke-linejoin="round"{dash}{op}/>')


def cuerpo(H, s, x, y, escala, color=TINTA, rot=0.0, opac=1.0, capa="objetos", espejo=False):
    op = f' opacity="{opac}"' if opac < 1 else ""
    tr = _tr(x, y, escala, rot).replace(f"scale({escala:.4f})", f"scale({escala:.4f} {-escala:.4f})") if espejo \
        else _tr(x, y, escala, rot)
    H.add(capa, f'<use href="#{ref(s)}" transform="{tr}" fill="{color}"{op}/>')


def aguada_signo(H, s, x, y, escala, color=VIOLETA, opac=0.6, rot=0.0):
    """Un signo en aguada: la tinta del esténcil con agua, dentro de la forma de la letra."""
    H.aguada(C_ACTUAL["signos"][s]["d"], color, opac, transform=_tr(x, y, escala, rot), desplaza=3.0, capas=2, borde=0.6,
             erosion=1.0)


def lineas_de_la_letra(H, ys, x0=40, x1=None):
    """Las cuatro líneas de la anatomía (afuera, borde, fondo, desagüe) cruzando la hoja, apenas."""
    x1 = x1 or H.W - 40
    for nombre, y in ys:
        borde = nombre == "borde"
        p = H.trazo([(x0, y), (x1, y + H.rng.uniform(-4, 4))], LILA if borde else GRAFITO2, 1.0 if borde else 0.6,
                    1.0 if borde else 0.55, guiones=None if borde else "7 6", deriva=2.5)
        H.sobre(p[:40], nombre, 15, VIOLETA if borde else GRAFITO, desde=0, ancla="start", dy=-5)


# ------------------------------------------------------------------ objetos del proyecto

def piscina(H, cx, arriba, ancho=300, fondo_=260, prof=(60, 110), baldosa=30, agua=True, foco=380, altura=260,
            distancia=380):
    """La piscina vacía en perspectiva, desde el borde: el lugar de la obra."""
    P = Perspectiva(cx, arriba - altura * foco / distancia, foco, altura, distancia)
    X = ancho / 2
    borde = [P(-X, 0, 0), P(X, 0, 0), P(X, fondo_, 0), P(-X, fondo_, 0)]
    cid = H.uid("pileta")
    H.defs.append(f'<clipPath id="{cid}"><path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in borde)}Z"/></clipPath>')
    z = lambda Y: -prof[0] - (prof[1] - prof[0]) * Y / fondo_   # noqa: E731
    g = []

    def lin(pts, c=GRAFITO2, w=0.5, o=0.8):
        g.append(f'<path d="{d_suave(H.temblar(pts, 0.25, 0.6))}" fill="none" stroke="{c}" stroke-width="{w}" '
                 f'opacity="{o}"/>')
    n = max(2, int(ancho // baldosa))
    for i in range(n + 1):                                   # el piso: baldosas que se van al fondo
        x = -X + i * ancho / n
        lin([P(x, Y, z(Y)) for Y in range(0, fondo_ + 1, 20)])
    for Y in range(0, fondo_ + 1, baldosa):
        lin([P(-X, Y, z(Y)), P(X, Y, z(Y))])
    for Zs in range(0, int(prof[1]) + 1, baldosa):           # la pared del fondo
        lin([P(-X, fondo_, -Zs), P(X, fondo_, -Zs)], w=0.45)
    for i in range(n + 1):
        x = -X + i * ancho / n
        lin([P(x, fondo_, 0), P(x, fondo_, z(fondo_))], w=0.45)
    for s in (-1, 1):                                        # las paredes de los lados
        lin([P(s * X, Y, z(Y)) for Y in range(0, fondo_ + 1, 20)], TINTA, 0.6, 0.9)
        for Zs in range(baldosa, int(prof[1]) + 1, baldosa):
            lin([P(s * X, Y, max(-Zs, z(Y))) for Y in range(0, fondo_ + 1, 20)], w=0.4, o=0.6)
    lin([P(-X, fondo_, z(fondo_)), P(X, fondo_, z(fondo_))], TINTA, 0.6, 0.9)
    for s in (-1, 1):
        lin([P(s * X, fondo_, 0), P(s * X, fondo_, z(fondo_))], TINTA, 0.6, 0.9)
    H.add("lineas", f'<g clip-path="url(#{cid})" stroke-linecap="round">{"".join(g)}</g>')
    for k, w in ((0, 1.0), (1, 0.5)):                        # el borde, doble: la piedra de la orilla
        e = 6 * k
        H.trazo([P(-X - e, -e, 0), P(X + e, -e, 0), P(X + e, fondo_ + e, 0), P(-X - e, fondo_ + e, 0), P(-X - e, -e, 0)],
                TINTA, w, temblor=0.3, deriva=1.0)
    dx, dy = P(0, fondo_ * 0.72, z(fondo_ * 0.72))           # el desagüe y lo que queda del agua
    if agua:
        d, _ = H.mancha(dx + ancho * 0.06, dy + 3, ancho * 0.2, ancho * 0.045, 0.15, 9, 2)
        H.aguada(d, LILA, 0.95, desplaza=8)
    H.add("objetos", f'<ellipse cx="{dx:.1f}" cy="{dy:.1f}" rx="{ancho / 60:.1f}" ry="{ancho / 150:.1f}" fill="{TINTA}"/>')
    return P, z


PIE = ["EL IDOLO KOCHAMAMA, según Posnansky, presentado en amplio detalle reconstructivo,",
       "según viejas fotografías (hoy está muy erosionado y casi no se ven esos detalles).",
       "Su calendario, todavía no bien interpretado, es distinto del de la Puerta del Sol y",
       "muestra motivos mucho más antiguos. Suponemos que originariamente se encontraba en",
       "Pumapuncu, en el lugar en donde luego se puso la Puerta de la Luna."]


def tira_del_pie(H, cx, cy, ancho=380, alto=78, rot=-3.0, lineas=4, tam=7.1):
    """La tira del pie de la lámina: papel rasgado con sus líneas a máquina."""
    r = H.rng
    x0, x1, y0, y1 = -ancho / 2, ancho / 2, -alto / 2, alto / 2
    arriba = [(x0 + (x1 - x0) * k / 30, y0 + r.uniform(-1.8, 1.8)) for k in range(31)]
    abajo = [(x1 - (x1 - x0) * k / 30, y1 + r.uniform(-2.2, 2.2)) for k in range(31)]
    pts = arriba + [(x1 + r.uniform(-3, 3), 0)] + abajo + [(x0 + r.uniform(-3, 3), 0)]
    tr = f"translate({cx:.1f} {cy:.1f}) rotate({rot})"
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    H.add("objetos", f'<path d="{d}" transform="{tr}" fill="#fbfaf6" stroke="{GRAFITO2}" stroke-width="0.7"/>')
    paso = (alto - 18) / lineas
    for i, l in enumerate(PIE[:lineas]):
        H.add("objetos", f'<text transform="{tr}" x="{x0 + 12:.1f}" y="{y0 + 14 + tam + i * paso:.1f}" '
                         f'font-family="Courier Prime" font-size="{tam}" fill="{GRAFITO}" textLength="{ancho - 24}" '
                         f'lengthAdjust="spacingAndGlyphs">{l}</text>')
    return tr


def placa(H, cx, cy, w, h, rot=0.0, opac=0.6):
    """Una placa de papel de aluminio: plata, con el borde apenas arrugado y algún pliegue."""
    r = H.rng
    pts = []
    for k in range(48):
        t = k / 48
        if t < 0.25:
            x, y = -w / 2 + w * t * 4, -h / 2
        elif t < 0.5:
            x, y = w / 2, -h / 2 + h * (t - 0.25) * 4
        elif t < 0.75:
            x, y = w / 2 - w * (t - 0.5) * 4, h / 2
        else:
            x, y = -w / 2, h / 2 - h * (t - 0.75) * 4
        pts.append((x + r.uniform(-2.2, 2.2), y + r.uniform(-2.2, 2.2)))
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    gira = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)   # noqa: E731
    pts = [gira(x, y) for x, y in pts]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    H.aguada(d, PLATA, opac, desplaza=4, capas=2, borde=0.5)
    H.trazo(pts + pts[:1], GRAFITO, 0.6, 0.8, temblor=0.2, deriva=0.4)
    for _ in range(5):                                        # pliegues
        x0, y0 = r.uniform(-w / 2, w / 2), r.uniform(-h / 2, h / 2)
        a = r.uniform(0, math.pi)
        L = r.uniform(12, 30)
        H.trazo([gira(x0, y0), gira(x0 + L * math.cos(a), y0 + L * math.sin(a))], GRAFITO2, 0.5, 0.6, temblor=0.2,
                deriva=0.5)
    return d


def repujado(H, s, x, y, escala, rot=0.0):
    """La letra repujada: el contorno y su luz, corrida medio milímetro."""
    contorno(H, s, x + 1.3, y + 1.3, escala, "#ffffff", 1.4, rot=rot, opac=0.9)
    contorno(H, s, x, y, escala, GRAFITO, 0.9, rot=rot)


def charco(H, cx, cy, rx, ry, ondas=3, color=LILA):
    """Un charco: aguada y sus ondas, abiertas abajo."""
    d, _ = H.mancha(cx, cy, rx, ry, 0.08, 10)
    H.aguada(d, color, 0.95, desplaza=7)
    for k in range(1, ondas + 1):
        H.orbita(cx, cy, rx * (0.25 + 0.28 * k), ry * (0.25 + 0.28 * k), 0, hueco=18, color=VIOLETA, ancho=0.55,
                 pasadas=1, opac=0.8 - 0.15 * k)


def frotado(H, s, cx, cy, w, h, escala, capa="objetos"):
    """Una frotada: el grafito sobre el papel apoyado en la placa. La letra sale más oscura."""
    x0, y0 = cx - w / 2, cy - h / 2
    d = f"M{x0:.1f},{y0:.1f} h{w:.1f} v{h:.1f} h{-w:.1f}Z"
    H.add(capa, f'<path d="{d}" fill="#fbfaf6" stroke="{GRAFITO2}" stroke-width="0.6"/>')
    H.rayado(d, (x0, y0, x0 + w, y0 + h), -52, 3.2, GRAFITO, 0.6, 0.4, capa=capa, desvanece=0.6)
    H.rayado(C_ACTUAL["signos"][s]["d"], (x0, y0, x0 + w, y0 + h), -52, 1.3, GRAFITO, 0.9, 1.0,
             transform=_tr(cx, cy + 8, escala, 0), capa=capa, desvanece=0.3)


def caja_a_mano(H, gx, gy, gl, marcas=True, color=GRAFITO):
    """La caja de 8 × 7, a mano; un punto por signo: tinta si es hallado, violeta si es reconstruido."""
    for i in range(9):
        H.trazo([(gx + i * gl, gy), (gx + i * gl, gy + 7 * gl)], color, 0.5, 0.8, temblor=0.25, deriva=0.5)
    for j in range(8):
        H.trazo([(gx, gy + j * gl), (gx + 8 * gl, gy + j * gl)], color, 0.5, 0.8, temblor=0.25, deriva=0.5)
    if marcas:
        for c in CAJA["celdas"]:
            x, y = gx + (c["columna"] - 0.5) * gl, gy + (c["fila"] - 0.5) * gl
            if c["estado"] == "hallada":
                H.punto(x, y, gl * 0.15, TINTA)
            elif c["estado"] == "reconstruida":
                H.punto(x, y, gl * 0.15, VIOLETA, opac=0.8)


def tramo(p, a, b):
    """Un tramo de una polilínea, de la fracción a a la b."""
    return p[int(len(p) * a):max(int(len(p) * a) + 2, int(len(p) * b))]


# ------------------------------------------------------------------ mapa 1: el proyecto entero

def mapa_1():
    H = Hoja(1200, 1600, 11)
    definir(H, "oaqgln")
    cx = 600
    lineas_de_la_letra(H, [("afuera", 118), ("borde", 392), ("fondo", 1112), ("desagüe", 1392)])
    H.eje(cx, 58, cx - 4, 1452, TINTA, 0.8, marcas=(0.13, 0.34, 0.54, 0.73, 0.9))
    H.mano(cx + 12, 1446, "hacia el desagüe", 15, GRAFITO)
    arco = (0.34, 0.62)                                       # las notas van en el arco de arriba de cada órbita

    # 1 · la obra: la piscina vacía
    o = H.orbita(cx, 236, 350, 96, -5, color=TINTA, ancho=0.75, sentido=0.2)
    piscina(H, cx, 190, 290, 240, baldosa=29)
    H.sobre(tramo(o, 0.25, 0.42), "vuelta 1/5 · la obra", 15, GRAFITO)
    H.mano(92, 196, "La obra", 30, TINTA, rot=-2)
    H.mano(94, 222, "Contener una ruina · 22.8.2026", 15, GRAFITO)
    H.manos(975, 196, ["partir del registro,", "no de la piedra"], 17)
    H.manos(975, 272, ["todo es un continente,", "y ninguno retiene"], 17)
    H.maquinas(96, 300, ["«Quedó el contenedor", " de lo que ya no está.»"], 13)

    # 2 · desenterrar: el pie y el calco
    o = H.orbita(cx + 10, 540, 330, 112, 7, color=TINTA, ancho=0.75, sentido=0.8)
    tira_del_pie(H, cx - 30, 530, 380, 76, -3)
    calco = H.mancha(cx + 120, 500, 118, 64, 0.06, 8, 5)[0]
    H.aguada(calco, PLATA, 0.35, desplaza=3, capas=1)
    contorno(H, "o", cx + 72, 500, 0.19, TINTA, 1.0)
    contorno(H, "g", cx + 132, 492, 0.19, TINTA, 1.0)
    contorno(H, "q", cx + 192, 500, 0.19, VIOLETA, 1.4, punteado=True)
    H.sobre(tramo(o, *arco), "vuelta 2/5 · desenterrar · acciones 0 a 3", 15, GRAFITO)
    H.mano(952, 478, "Desenterrar", 30, TINTA, rot=-2)
    H.manos(952, 620, ["del pie, las medidas:", "30 hallados y 25", "por reconstruir"], 17)
    H.mano(262, 676, "sinécdoque: el pie por la lámina", 16, VIOLETA, rot=-3)
    H.maquinas(78, 452, ["«No se salvó la piedra,", " solo la opinión sobre ella.»"], 13)

    # 3 · contener: la placa y la caja
    o = H.orbita(cx - 6, 812, 340, 118, -8, color=TINTA, ancho=0.75, sentido=0.25)
    H.orbita(cx + 2, 806, 118, 150, 12, color=GRAFITO, ancho=0.5, pasadas=1, opac=0.8)
    placa(H, cx, 800, 136, 160, -3, 0.5)
    repujado(H, "a", cx - 2, 812, 0.25, -3)
    for i, s in enumerate("olna"):
        aguada_signo(H, s, 318 + i * 50 + (6 if s == "l" else 0), 808 + (i % 2) * 8, 0.19, VIOLETA, 0.62)
    H.mano(318, 890, "las cuatro vasijas: o, l, n, a", 15, GRAFITO, rot=-2)
    caja_a_mano(H, 770, 758, 15)
    H.mano(768, 886, "la caja de 8 × 7", 15, GRAFITO)
    H.sobre(tramo(o, *arco), "vuelta 3/5 · contener · acciones 4 a 7", 15, GRAFITO)
    H.mano(70, 742, "Contener", 30, TINTA, rot=-2)
    H.manos(72, 776, ["cada letra, una placa", "suelta de aluminio"], 17)
    H.manos(958, 890, ["lo que no cabe", "se ve vacío"], 17)
    H.mano(520, 962, "paradoja: toda cuenca se abre abajo", 16, VIOLETA, rot=2)
    H.maquinas(70, 1000, ["«y ningún contenedor", " aguanta lo que contiene.»"], 13)

    # 4 · devolver: la frotada y el charco
    o = H.orbita(cx + 4, 1086, 350, 100, 4, color=TINTA, ancho=0.75, sentido=0.72)
    H.orbita(cx + 128, 1106, 130, 44, -12, color=VIOLETA, ancho=0.55, pasadas=1, opac=0.85)
    frotado(H, "a", cx - 120, 1072, 120, 132, 0.2)
    charco(H, cx + 128, 1110, 92, 22)
    cuerpo(H, "o", cx + 128, 1116, 0.11, VIOLETA, opac=0.35, espejo=True)
    H.aguada(H.gota(cx + 128, 1040, 7), VIOLETA, 0.8, desplaza=2, capas=1)
    H.trazo([(cx + 128, 1002), (cx + 128, 1028)], VIOLETA, 0.9, punteado=True)
    H.sobre(tramo(o, *arco), "vuelta 4/5 · devolver · acciones 8 a 12", 15, GRAFITO)
    H.mano(962, 1040, "Devolver", 30, TINTA, rot=-2)
    H.manos(72, 1176, ["estados, no pesos:", "el peso se mide en frotadas"], 17)
    H.mano(700, 1204, "la voz deforma, no dice", 16, VIOLETA, rot=-2)
    H.maquinas(70, 1062, ["«Tocas el agua", " y la diosa se deforma.»"], 13)

    # 5 · lo digital: todavía punteado
    H.orbita(cx - 10, 1318, 170, 48, -6, color=VIOLETA, ancho=0.9, punteado=True, pasadas=1)
    H.celda(cx - 10, 1310, 62, VIOLETA, 1.2, punteada=True, doble=False)
    contorno(H, "o", cx - 10, 1318, 0.13, VIOLETA, 1.3, punteado=True)
    H.mano(410, 1266, "Digital", 30, TINTA, rot=-2, ancla="end")
    H.mano(410, 1290, "si cierra: un estado más", 15, GRAFITO, ancla="end")
    v = H.flecha([(cx + 168, 1316), (1030, 1300), (1142, 1150), (1132, 930), (900, 812)], VIOLETA, 1.1, punteado=True)
    H.sobre(tramo(v, 0.0, 0.42), "termina y empieza · vuelve a la caja (generación 2)", 15, VIOLETA, desde=45)
    H.maquinas(700, 1374, ["«Termina y empieza,", " termina y empieza.»"], 13)

    # los centros externos: de dónde se toma
    externos = [
        ((70, 604), [(cx - 200, 560)], "Posnansky, 1945: la lámina y su pie", "start"),
        ((1150, 420), [(cx + 205, 506)], "Tshuma, 2025: sankofa, ¿quién la escribió?", "end"),
        ((70, 940), [(300, 846)], "Mahendran, 2020: la escritura como vasija", "start"),
        ((70, 1346), [(cx - 186, 1326)], "Tshuma: objeto, signo, objeto otra vez", "start"),
    ]
    for (x, y), destino, texto, ancla in externos:
        H.cruz(x, y)
        H.mano(x + (14 if ancla == "start" else -14), y - 8, texto, 16, TINTA, ancla)
        d = destino[0]
        medio = ((x + d[0]) / 2, (y + d[1]) / 2 + 12)
        H.flecha([(x + (8 if ancla == "start" else -8), y + 6), medio, d], TINTA, 0.6, deriva=2)

    H.leyenda(60, 1478, "mapa 1 · el proyecto entero", [("continuo", "lo hallado"),
                                                        ("punteado", "lo reconstruido, lo que aún no es"),
                                                        ("orbita", "una etapa; se abre abajo")])
    H.leyenda(470, 1478, "", [("cruz", "una fuente, afuera"), ("violeta", "la tinta del esténcil"), ("lila", "el agua")])
    H.leyenda(790, 1478, "", [("plata", "el aluminio"), ("grafito", "el frotado"),
                              ("maquina", "lo escrito; a mano, lo que se hace")])
    H.firma(1150, 50, 1, TOTAL, "el proyecto entero")
    return H


# ------------------------------------------------------------------ mapa 2: teoría y fuentes

FUENTES_T = {
    "EthnoGraphemes": dict(autor="Mahendran, 2020", toma=[
        "la escritura como vasija (aquí no retiene)", "transmodalidad: la letra se toca, se moja",
        "la cimática: el estado Voz", "caja baja, la letra de la mano (Brookes)",
        "contra el exotismo: ningún motivo pegado", "el diccionario de cartas: la caja de placas",
        "Ellipsis, lo inacabado: el signo …", "la ética del que viene de afuera: Acción 0"],
        no=["revitalizar una lengua", "una frecuencia por letra", "tatuar: se queda en el esténcil"]),
    "Afrography": dict(autor="Tshuma, 2025", toma=[
        "sankofa: ¿quién lo escribió?", "Nedmural: letras sacadas de un muro, el pie",
        "The Great Stone: la restricción de la ruina", "la cabeza de Oba: el colofón como custodia",
        "tres cuadernos: desenterrar, contener, devolver", "objeto, signo, objeto: la vuelta a la placa",
        "herramientas libres; la economía del trabajo", "la placa rota no se corrige"],
        no=["inventar una escritura", "el estallido: el agua vuelve", "letras hechas con módulos"]),
    "Tihuanacu": dict(autor="Posnansky, 1945", toma=[
        "La Paz contiene la ruina", "la cloaca máxima hecha piso: el desagüe", "el agua que se fue: la piscina vacía",
        "el asperón, elegido por blando: el material decide", "lo que no está se reconstruye: el punteado"],
        no=["su cronología", "su tesis del título", "su lectura racial de la historia"]),
    "La iconografía Tiwanaku": dict(autor="Agüero, Uribe y Berenguer, 2003", toma=[
        "elementos, motivos, figuras: partes y signos", "dobles opuestos: la {¿} no es la {?} al revés",
        "el Personaje Frontal en pecho y espalda (D4)", "cabezas de pez de perfil (D7)"],
        no=["interpretar la iconografía", "traducir el «calendario»"]),
    "Contener una ruina": dict(autor="Rebeca Paz Prada, 2026", toma=[
        "partir del registro: el pie de la lámina", "el aluminio, la cinta, el agua, la voz",
        "la piscina vacía: escenario y pantalla"],
        no=["las lecturas rituales", "las fotos y el cuerpo de Rebeca"]),
}


def vasija(H, cx, cy, alto=150):
    """Una vasija de metal con una grieta: la escritura como vasija, que aquí no retiene."""
    a = alto
    medio = [(0.10, 0.0), (0.12, 0.06), (0.09, 0.12), (0.11, 0.18), (0.30, 0.34), (0.36, 0.52), (0.30, 0.74),
             (0.18, 0.92), (0.15, 1.0)]
    der = [(cx + x * a, cy - a / 2 + y * a) for x, y in medio]
    izq = [(cx - x * a, cy - a / 2 + y * a) for x, y in medio[::-1]]
    pts = spline(der + izq, 8, True)
    d = d_suave(pts, True)
    H.aguada(d, PLATA, 0.75, desplaza=5, capas=2, borde=0.55)
    H.trazo(pts, TINTA, 0.9, temblor=0.25, deriva=0.6)
    grieta = [(cx + 0.05 * a, cy - a * 0.38), (cx + 0.11 * a, cy - a * 0.2), (cx + 0.04 * a, cy - a * 0.05),
              (cx + 0.12 * a, cy + a * 0.12), (cx + 0.07 * a, cy + a * 0.3), (cx + 0.1 * a, cy + a * 0.44)]
    H.trazo(grieta, TINTA, 1.0, temblor=0.6, deriva=0.3)
    H.aguada(H.gota(cx + 0.1 * a, cy + a * 0.62, 5), VIOLETA, 0.85, desplaza=1.5, capas=1)


def taburete(H, cx, cy, ancho=130):
    """Un taburete tallado, en negro: el objeto que se vuelve signo y otra vez objeto."""
    w = ancho
    pts = [(-0.5, -0.36), (-0.25, -0.28), (0, -0.26), (0.25, -0.28), (0.5, -0.36), (0.46, -0.2), (0.2, -0.14),
           (0.14, 0.0), (0.16, 0.2), (0.28, 0.3), (0.42, 0.36), (-0.42, 0.36), (-0.28, 0.3), (-0.16, 0.2),
           (-0.14, 0.0), (-0.2, -0.14), (-0.46, -0.2)]
    P = spline([(cx + x * w, cy + y * w) for x, y in pts], 5, True)
    H.add("objetos", f'<path d="{d_suave(H.temblar(P, 0.3, 0.5), True)}" fill="{TINTA}"/>')
    for k in (-1, 1):                                         # los calados
        d, _ = H.mancha(cx + k * 0.05 * w, cy + 0.05 * w, 0.025 * w, 0.07 * w, 0.1, 6)
        H.add("objetos", f'<path d="{d}" fill="{PAPEL}"/>')


def piedra(H, cx, cy, ancho=170):
    """Una losa con su canal: la cloaca máxima de Tiwanaku, hecha piso."""
    w, h, p = ancho, ancho * 0.28, ancho * 0.22
    frente = [(cx - w / 2, cy), (cx + w / 2, cy), (cx + w / 2, cy + h), (cx - w / 2, cy + h)]
    tapa = [(cx - w / 2, cy), (cx - w / 2 + p, cy - p * 0.6), (cx + w / 2 + p, cy - p * 0.6), (cx + w / 2, cy)]
    lado = [(cx + w / 2, cy), (cx + w / 2 + p, cy - p * 0.6), (cx + w / 2 + p, cy + h - p * 0.6), (cx + w / 2, cy + h)]
    for cara, paso, op in ((frente, 3.2, 0.9), (lado, 2.4, 1.0), (tapa, 5.0, 0.5)):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in cara) + "Z"
        xs, ys = [q[0] for q in cara], [q[1] for q in cara]
        H.rayado(d, (min(xs), min(ys), max(xs), max(ys)), -35 if cara is not tapa else 10, paso, GRAFITO, 0.6, op)
        H.trazo(cara + cara[:1], TINTA, 0.8, temblor=0.3, deriva=0.6)
    c0, c1 = 0.42, 0.58                                       # el canal, a lo largo de la tapa
    for t in (c0, c1):
        H.trazo([(cx - w / 2 + p * 0.1 + w * t, cy - p * 0.06), (cx - w / 2 + p * 0.9 + w * t, cy - p * 0.54)], TINTA,
                0.8)
    H.trazo([(cx - w / 2 + w * c0 + 2, cy), (cx - w / 2 + w * c0 + 2, cy + h * 0.35),
             (cx - w / 2 + w * c1 - 2, cy + h * 0.35), (cx - w / 2 + w * c1 - 2, cy)], TINTA, 0.8)


def haz_de_fuente(H, etiquetas, x, y0, paso, lado, destino, nudo, color=TINTA, tam=15.5, inter_haz=4.2):
    """Una lista a mano; de la punta de cada renglón sale una hebra, y las hebras hacen un haz hacia el centro."""
    n = len(etiquetas)
    for i, t in enumerate(etiquetas):
        y = y0 + i * paso
        H.mano(x, y, t, tam, TINTA if color == TINTA else color, "start" if lado > 0 else "end",
               rot=H.rng.uniform(-0.8, 0.6))
        largo = len(t.replace("{", "").replace("}", "")) * tam * 0.43
        xa = x + lado * (largo + 8)
        off = (i - (n - 1) / 2) * inter_haz
        pts = [(xa, y - 5), (xa + lado * 24, y - 5 + (nudo[1] - y) * 0.15),
               (nudo[0], nudo[1] + off), (destino[0] + (nudo[0] - destino[0]) * 0.35, destino[1] + off * 0.8 +
                                          (nudo[1] - destino[1]) * 0.25),
               (destino[0], destino[1] + off * 0.35)]
        cs = [color, GRAFITO2] if color == TINTA else [color, LILA]
        H.trazo(spline(pts), cs[i % 2], 0.55, 0.9, temblor=0.25, deriva=0.8)
        H.punto(xa, y - 5, 1.6, cs[i % 2])


def no_se_toma(H, etiquetas, origen, puntas, tam=14.5):
    """Lo que no se toma: una línea que sale hacia afuera y se corta con un tope; la nota, en grafito."""
    for t, (x1, y1, ancla) in zip(etiquetas, puntas):
        H.trazo([origen, (x1, y1)], GRAFITO, 0.6, 0.9, temblor=0.25, deriva=0.5)
        ang = math.atan2(y1 - origen[1], x1 - origen[0]) + math.pi / 2
        H.trazo([(x1 - 5 * math.cos(ang), y1 - 5 * math.sin(ang)), (x1 + 5 * math.cos(ang), y1 + 5 * math.sin(ang))],
                GRAFITO, 1.0, temblor=0.1, deriva=0)
        H.mano(x1 + (9 if ancla == "start" else -9), y1 + 5, "no: " + t, tam, GRAFITO, ancla)


def mapa_2():
    H = Hoja(1600, 1200, 22)
    definir(H, "o¿?")
    F = FUENTES_T
    centro = (806, 640)
    # el centro: la o como vasija, con sus órbitas; se abre abajo y gotea
    H.eje(centro[0] - 4, 360, centro[0] + 6, 930, TINTA, 0.7, marcas=(0.49,))
    for rx, ry, rot, c, w in ((190, 64, -9, TINTA, 0.8), (128, 170, 14, GRAFITO, 0.55), (250, 100, 6, VIOLETA, 0.6)):
        H.orbita(centro[0], centro[1], rx, ry, rot, color=c, ancho=w, sentido=0.62)
    aguada_signo(H, "o", centro[0], centro[1] + 6, 0.5, VIOLETA, 0.7)
    H.aguada(H.gota(centro[0] - 2, centro[1] + 128, 7), VIOLETA, 0.8, desplaza=2, capas=1)
    H.mano(centro[0] + 26, centro[1] + 196, "Contenida", 34, TINTA, rot=-2)
    H.mano(centro[0] + 30, centro[1] + 222, "lo que entra en la vasija no se queda:", 15, GRAFITO)
    H.mano(centro[0] + 30, centro[1] + 242, "se abre abajo, en su desagüe", 15, GRAFITO)
    llegada = centro

    # EthnoGraphemes: arriba a la izquierda
    vasija(H, 190, 190, 150)
    H.orbita(190, 196, 118, 40, -12, color=TINTA, ancho=0.6, sentido=0.3)
    H.orbita(186, 190, 70, 110, 8, color=GRAFITO, ancho=0.45, pasadas=1)
    H.cruz(282, 112)
    H.mano(296, 118, "EthnoGraphemes", 26, TINTA, rot=-2)
    H.mano(298, 142, F["EthnoGraphemes"]["autor"], 15, GRAFITO)
    haz_de_fuente(H, F["EthnoGraphemes"]["toma"], 60, 322, 24, 1, (llegada[0] - 150, llegada[1] - 40), (520, 470))
    no_se_toma(H, F["EthnoGraphemes"]["no"], (262, 214), [(350, 186, "start"), (360, 212, "start"), (352, 238, "start")])

    # Afrography: abajo a la izquierda
    taburete(H, 180, 800, 130)
    H.orbita(180, 806, 120, 38, 8, color=TINTA, ancho=0.6, sentido=0.7)
    H.cruz(270, 738)
    H.mano(286, 744, "Afrography", 26, TINTA, rot=-2)
    H.mano(288, 768, F["Afrography"]["autor"], 15, GRAFITO)
    haz_de_fuente(H, F["Afrography"]["toma"], 60, 880, 24, 1, (llegada[0] - 160, llegada[1] + 40), (540, 820))
    no_se_toma(H, F["Afrography"]["no"], (130, 752), [(66, 612, "start"), (80, 640, "start"), (94, 668, "start")])

    # Contener una ruina: arriba, al centro
    placa(H, 792, 150, 62, 74, 6, 0.8)
    charco(H, 800, 206, 70, 13, ondas=2)
    H.orbita(796, 170, 130, 48, -4, color=VIOLETA, ancho=0.7, sentido=0.25)
    H.cruz(946, 110)
    H.mano(960, 116, "Contener una ruina", 26, TINTA, rot=-2)
    H.mano(962, 140, F["Contener una ruina"]["autor"], 15, GRAFITO)
    haz_de_fuente(H, F["Contener una ruina"]["toma"], 960, 190, 25, 1, (llegada[0] + 30, llegada[1] - 60),
                  (960, 330), color=VIOLETA)
    no_se_toma(H, F["Contener una ruina"]["no"], (700, 214), [(690, 292, "end"), (676, 318, "end")])

    # Tihuanacu (Posnansky): arriba a la derecha
    piedra(H, 1370, 210, 170)
    H.orbita(1400, 206, 140, 46, 10, color=TINTA, ancho=0.6, sentido=0.3)
    H.cruz(1300, 300)
    H.mano(1316, 306, "Tihuanacu", 26, TINTA, rot=-2)
    H.mano(1318, 330, F["Tihuanacu"]["autor"], 15, GRAFITO)
    haz_de_fuente(H, F["Tihuanacu"]["toma"], 1540, 390, 25, -1, (llegada[0] + 160, llegada[1] - 20), (1080, 520))
    no_se_toma(H, F["Tihuanacu"]["no"], (1440, 160), [(1500, 64, "end"), (1520, 90, "end"), (1540, 116, "end")])

    # La iconografía Tiwanaku (Agüero, Uribe y Berenguer): a la derecha, abajo
    cuerpo(H, "¿", 1352, 790, 0.2, TINTA)
    cuerpo(H, "?", 1446, 790, 0.2, TINTA)
    H.trazo([(1398, 712), (1398, 868)], VIOLETA, 1.0, punteado=True)
    H.mano(1500, 800, "no es", 14, VIOLETA, rot=-2)
    H.mano(1500, 818, "su espejo", 14, VIOLETA, rot=-2)
    H.orbita(1400, 790, 128, 60, -6, color=TINTA, ancho=0.6, sentido=0.75)
    H.cruz(1260, 896)
    H.mano(1274, 902, "La iconografía Tiwanaku", 24, TINTA, rot=-2)
    H.mano(1276, 924, F["La iconografía Tiwanaku"]["autor"], 15, GRAFITO)
    haz_de_fuente(H, F["La iconografía Tiwanaku"]["toma"], 1540, 968, 24, -1, (llegada[0] + 170, llegada[1] + 50),
                  (1110, 850))
    no_se_toma(H, F["La iconografía Tiwanaku"]["no"], (1360, 734), [(1300, 628, "end"), (1316, 654, "end")])

    H.leyenda(60, 1124, "mapa 2 · teoría y fuentes", [])
    H.leyenda(420, 1110, "", [("cruz", "una fuente: un centro externo"), ("continuo", "una hebra: lo que se toma")])
    H.leyenda(780, 1110, "", [("violeta", "lo que viene de la obra"), ("corte", "una línea cortada: lo que no se toma")])
    H.firma(1550, 1150, 2, TOTAL, "teoría y fuentes")
    return H


# ------------------------------------------------------------------ mapa 3: la obra, decisión por decisión

CADENA = [("piedra borrada", GRAFITO), ("fotografía vieja", GRAFITO), ("dibujo reconstructivo", GRAFITO2),
          ("escaneo", GRAFITO2), ("repujado en aluminio", PLATA), ("cuerpo", VIOLETA), ("video", VIOLETA),
          ("charco", LILA), ("pared de azulejo", LILA)]
DECISIONES = [
    # número, lo que hizo la obra, lo que hace la letra, eslabón de la cadena del que sale
    ("D1", "partir de la lámina y no de la piedra", "las letras salen del pie de la lámina", 1),
    ("D2", "del asperón al papel de aluminio", "matrices de aluminio repujado; solo caja baja", 4),
    ("D3", "placas sueltas, con piel entre ellas", "cada letra es un tipo móvil; entre palabras, la piel", 5),
    ("D4", "puertas en el pecho y la espalda", "la tapa de la caja: una puerta sobre la celda 1", 5),
    ("D5", "iconografía interpretada, no copiada", "del monolito, solo la retícula y la celda vacía", 2),
    ("D6", "la piscina vacía, en un estudio de tatuajes", "fondo, borde, desagüe; el violeta del esténcil", 8),
    ("D7", "placas en el fondo, como peces", "no se dibujan peces: las letras ya lo parecen", 7),
    ("D8", "la bandeja con un dedo de agua", "el estado Agua: se lee reflejada", 7),
    ("D9", "escenario, pantalla y tema", "la pared frotada es el papel del calco", 6),
    ("D10", "el bucle", "frotar hasta que no se lea, y repujar otra", 6),
    ("D11", "moverse como la piedra: apenas", "el temblor de la mano; fustes de tres planos a 1,6°", 5),
    ("D12", "ojos y boca tapados con cinta", "no hay Regular; el estado Cinta; el punto de cinta", 5),
    ("D13", "de la boca sale una placa", "el signo final {¶}, hecho con los dedos", 5),
    ("D14", "un canto que no se entiende", "el estado Voz: la voz deforma, no se graba", 6),
    ("D15", "tocar el agua deforma la imagen", "el agua tocada; en lo digital, tocar deforma", 7),
    ("D16", "el líquido que chorrea de la boca", "toda cuenca se abre abajo; solo gotea lo que mira abajo", 7),
]


def rio(H, puntos, ancho0, ancho1, colores):
    """Un río de aguada: la cadena de desplazamientos. Pierde materia (ancho, tinta) y gana luz."""
    base = remuestrear(spline(puntos, 20), 6)
    n = len(base)
    nor = normales(base)
    r = H.ruido(260)
    orillas = []
    for i, ((x, y), (nx, ny)) in enumerate(zip(base, nor)):
        t = i / (n - 1)
        w = (ancho0 + (ancho1 - ancho0) * t ** 0.8) * (1 + 0.12 * r(i * 6)) / 2
        orillas.append(((x + nx * w, y + ny * w), (x - nx * w, y - ny * w)))
    gid = H.uid("cadena")
    y0, y1 = base[0][1], base[-1][1]
    opac = {GRAFITO: 0.75, GRAFITO2: 0.6, PLATA: 0.85, VIOLETA: 0.6, LILA: 0.9}
    paradas = "".join(f'<stop offset="{(k + 0.5) / len(colores):.3f}" stop-color="{c}" stop-opacity="{opac[c]}"/>'
                      for k, c in enumerate(colores))
    H.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{y0:.0f}" x2="0" '
                  f'y2="{y1:.0f}">{paradas}</linearGradient>')
    d = d_suave([o[0] for o in orillas] + [o[1] for o in orillas][::-1], True)
    H.aguada(d, f"url(#{gid})", 0.8, desplaza=16, capas=2, borde=0.62)
    return base, orillas


def mapa_3():
    H = Hoja(1200, 1600, 33)
    # el borde de la piscina: la línea del horizonte
    b = H.trazo([(40, 214), (560, 204), (1160, 222)], LILA, 1.1, deriva=3)
    H.sobre(b[:50], "borde", 15, VIOLETA, desde=0, ancla="start", dy=-5)
    H.sobre(b[-80:], "aquí estaba el agua", 15, VIOLETA, desde=100, ancla="end", dy=-5)
    base, orillas = rio(H, [(70, 96), (250, 250), (390, 520), (350, 830), (250, 1110), (160, 1350)], 124, 26,
                        [c for _, c in CADENA])
    n = len(base)
    # los eslabones, en la orilla izquierda
    pos = {}
    for k, (nombre, _) in enumerate(CADENA):
        i = min(n - 1, int((k + 0.5) * n / len(CADENA)))
        (xi, yi), (xd, yd) = orillas[i]
        izq_x, izq_y = (xi, yi) if xi < xd else (xd, yd)
        der = (xd, yd) if xi < xd else (xi, yi)
        pos[k] = der
        H.trazo([(izq_x - 4, izq_y), (izq_x - 16, izq_y + 2)], TINTA, 0.8, temblor=0.1, deriva=0)
        if izq_x > 200:
            H.mano(izq_x - 20, izq_y + 5, nombre, 16, TINTA, "end", rot=-2)
        else:
            H.mano(izq_x + 8, izq_y - 10, nombre, 16, TINTA, "start", rot=-2, halo=False)
    for i in range(5):                                        # la pared de azulejo, donde el río se deshace
        for j in range(3):
            x, y = 104 + i * 26 + j * 3, 1352 + j * 24
            H.trazo([(x, y), (x + 23, y), (x + 23, y + 21), (x, y + 21), (x, y + 1)], LILA, 0.8, 0.9, temblor=0.2,
                    deriva=0.3)
    H.mano(96, 70, "la cadena de desplazamientos", 20, TINTA, rot=-1.5)
    H.mano(98, 92, "cada paso pierde materia y gana luz", 15, GRAFITO)
    # el haz: cada decisión sale de su eslabón y va a su traducción, a la derecha
    x_txt, y0, paso = 690, 286, 74
    for j, (num, obra, letra, k) in enumerate(DECISIONES):
        ox, oy = pos[k]
        ox += H.rng.uniform(-6, 6)
        oy += (j % 5 - 2) * 7
        ty = y0 + j * paso
        off = (j - 7.5) * 4.4
        color = {GRAFITO: TINTA, GRAFITO2: TINTA, PLATA: GRAFITO, VIOLETA: VIOLETA, LILA: LILA}[CADENA[k][1]]
        ida = spline([(ox, oy), (ox + 40, oy + (790 - oy) * 0.3), (420, 782 + off), (490, 790 + off)])
        abanico = bezier((490, 790 + off), (570, 790 + off), (560, ty - 6), (x_txt - 46, ty - 6))
        H.trazo(ida + abanico[1:], color, 1.3 if color == LILA else 0.8, 0.9, temblor=0.2, deriva=0.6)
        H.punto(ox, oy, 2.2, VIOLETA if color == LILA else color)
        H.maquina(x_txt - 42, ty - 2, num, 12, VIOLETA, halo=False)
        H.mano(x_txt, ty - 8, obra, 15, GRAFITO, rot=H.rng.uniform(-1, 0.6))
        H.mano(x_txt + 8, ty + 14, letra, 17, TINTA, rot=H.rng.uniform(-1, 0.6))
    # dos rizos: el bucle (D10) y la placa que sale de la boca (D13)
    for j in (9, 12):
        H.orbita(x_txt - 70, y0 + j * paso - 4, 46, 18, -18, color=VIOLETA, ancho=1.0, pasadas=2, sentido=0.4)
    H.mano(x_txt - 20, 1480, "gris: lo que hizo la obra · tinta: lo que hace la letra", 15, GRAFITO, rot=-1)
    H.leyenda(60, 1488, "mapa 3 · la obra, decisión por decisión", [])
    H.leyenda(60, 1500, "", [("gris", "la piedra, la foto, el dibujo"), ("plata", "el aluminio")], inter=23)
    H.leyenda(380, 1500, "", [("violeta", "el cuerpo, la tinta, el video"), ("lila", "el agua: charco y pared")],
              inter=23)
    H.firma(1150, 50, 3, TOTAL, "la obra, decisión por decisión")
    return H


# ------------------------------------------------------------------ mapa 4: del pie a los 55 signos

GENERADORES = {
    "o": dict(nombre="la cuenca", centro=(262, 640), notas=["canal 8,9 mm", "trapecio 0,70", "pared 0,55",
                                                             "desagüe 3 mm", "radio de chapa 5,3 mm"]),
    "l": dict(nombre="el fuste", centro=(880, 600), notas=["facetas 3", "quiebre 1,6°", "asiento 17,8 × 8 mm",
                                                           "intemperie 1,1 mm"]),
    "n": dict(nombre="el hombro", centro=(290, 1000), notas=["hombro 3", "caída del hombro 0,40", "alivio 2,5 mm"]),
    "a": dict(nombre="el gancho y la gota", centro=(880, 980), notas=["gancho 105°", "gota 11,1 mm", "cuello 4,9 mm",
                                                                      "sifón 0,6", "cinta y punto 8,9 mm"]),
}
FAMILIA = {"o": "oecdbpqóéá0689", "l": "litjfkí1|()47", "n": "nmhuúürvwxyzñ235"}
FUERZAS = [  # de la obra, la forma: centros externos que empujan la gramática
    ((1150, 404), "l", "el punzón sobre el aluminio (D2)", "end"),
    ((50, 430), "o", "la vasija abierta (D16)", "start"),
    ((50, 846), "n", "la chapa sobre el cuerpo (D3)", "start"),
    ((1150, 800), "a", "la gravedad: solo gotea lo que mira abajo", "end"),
    ((50, 1180), "n", "la intemperie (el pie)", "start"),
    ((1150, 1190), "a", "la cinta de ojos y boca (D12)", "end"),
]
MEDIDAS = [((96, 318), "x: los ascendentes miden 1,71 veces la x"),
           ((500, 350), "la o del pie: 11,2 y 7,0 mm; el canal, 8,9"),
           ((150, 386), "las astas, los ojos y la caja de cada testigo"),
           ((640, 300), "afuera, borde, fondo y desagüe, en milímetros")]
PARTES = ["cuenca", "fuste", "hombro", "gancho", "gota", "asiento", "punto", "tilde", "onda", "recta", "alivio", "sifón"]


def familia(s):
    for g, signos in FAMILIA.items():
        if s in signos:
            return g
    return "a"


def mapa_4():
    H = Hoja(1200, 1600, 44)
    signos = [c["signo"] for c in CAJA["celdas"] if c["signo"] in C_ACTUAL["signos"]]
    definir(H, "olna" + "".join(signos))
    eje_x = 580
    # el pie, arriba: a máquina; las medidas, a mano
    H.mano(80, 88, "el pie de la lámina: la foto da medidas, no formas", 18, TINTA, rot=-1.5)
    tira_del_pie(H, 560, 196, 700, 118, -1.5, lineas=5, tam=10.5)
    for (x, y), t in MEDIDAS:
        H.flecha([(x + 30, 262 if y > 280 else 256), (x + 22, y - 26), (x + 14, y - 16)], GRAFITO, 0.6)
        H.mano(x, y, t, 15, TINTA)
    x0 = 928                                                    # una cota a mano: x y 1,71 x
    for (ya, yb, t) in ((168, 216, "x"), (134, 216, "1,71 x")):
        xx = x0 + (0 if t == "x" else 22)
        H.trazo([(xx, ya), (xx, yb)], VIOLETA, 0.8, temblor=0.2, deriva=0)
        for y in (ya, yb):
            H.trazo([(xx - 5, y), (xx + 5, y)], VIOLETA, 0.8, temblor=0.1, deriva=0)
        H.mano(xx + 8, (ya + yb) / 2 + 5, t, 14, VIOLETA, halo=False)
    # el eje de la gramática: del pie a la caja
    H.eje(eje_x, 270, eje_x + 6, 1168, TINTA, 0.8, marcas=(0.3, 0.72))
    H.sobre([(eje_x + 14, 470), (eje_x + 16, 700)], "20 parámetros y la altura de x", 15, GRAFITO, dy=-2)
    # las cuatro vasijas, con sus órbitas anotadas
    for s, g in GENERADORES.items():
        cx, cy = g["centro"]
        H.eje(cx, cy - 170, cx + 2, cy + 150, GRAFITO, 0.55)
        a = H.orbita(cx, cy, 158, 54, -8 if s in "on" else 7, color=TINTA, ancho=0.7, sentido=0.3)
        b = H.orbita(cx + 4, cy - 6, 76, 132, 12 if s in "on" else -10, color=GRAFITO, ancho=0.5, pasadas=1)
        aguada_signo(H, s, cx, cy + 10, 0.36, VIOLETA, 0.72)
        notas = g["notas"]
        H.sobre(tramo(a, 0.36, 0.64), notas[0], 15, TINTA)
        H.sobre(tramo(b, 0.38, 0.62), notas[1], 14, GRAFITO)
        for k, t in enumerate(notas[2:]):
            H.mano(cx + 70, cy + 96 + k * 20, t, 14.5, TINTA)
        H.mano(cx - 140, cy + 118, s, 34, VIOLETA, rot=0)
        H.mano(cx - 118, cy + 116, "· " + g["nombre"], 17, TINTA)
    # de la obra, la forma: centros externos
    for (x, y), s, t, ancla in FUERZAS:
        cx, cy = GENERADORES[s]["centro"]
        H.cruz(x, y)
        H.mano(x + (14 if ancla == "start" else -14), y - 8, t, 15.5, VIOLETA, ancla)
        dx = cx + (160 if x > cx else -160)
        H.flecha([(x + (-8 if x > cx else 8), y + 6), ((x + dx) / 2, (y + cy) / 2 + 14), (dx, cy - 10)], VIOLETA, 0.6,
                 deriva=2)
    # las partes, a los lados del eje
    for k, p in enumerate(PARTES):
        izq = k % 2 == 0
        y = 730 + (k // 2) * 26
        H.punto(eje_x + (-12 if izq else 16), y - 5, 1.6, TINTA)
        H.mano(eje_x + (-20 if izq else 24), y, p, 15, TINTA, "end" if izq else "start")
    H.mano(eje_x - 20, 706, "las partes", 16, GRAFITO, "end", rot=-2)
    # la bandada: de cada vasija bajan sus signos, como peces, hasta la caja
    lado, gx, gy = 36, eje_x - 4 * 36 + 3, 1196
    celdas = {c["signo"]: c for c in CAJA["celdas"]}
    por_familia = {g: [s for s in signos if familia(s) == g] for g in "olna"}
    rutas = {"o": [(336, 772), (440, 930), (505, 1070), (548, gy - 22)],
             "l": [(816, 740), (716, 900), (650, 1066), (614, gy - 22)],
             "n": [(400, 1070), (470, 1046), (522, 1110), (550, gy - 20)],
             "a": [(764, 1010), (692, 1060), (650, 1120), (618, gy - 20)]}
    for g, lista in por_familia.items():
        ruta = remuestrear(spline(rutas[g]), 3)
        for k, s in enumerate(lista):
            t = (k + 0.5) / len(lista)
            i = int(t * (len(ruta) - 1))
            x, y = ruta[i]
            a = math.degrees(math.atan2(ruta[min(i + 2, len(ruta) - 1)][1] - ruta[max(i - 2, 0)][1],
                                        ruta[min(i + 2, len(ruta) - 1)][0] - ruta[max(i - 2, 0)][0]))
            x += (k % 3 - 1) * 12 + H.rng.uniform(-4, 4)
            y += H.rng.uniform(-5, 5)
            color = TINTA if celdas[s]["estado"] == "hallada" else VIOLETA
            cuerpo(H, s, x, y, 0.032 if s.isdigit() else 0.044, color, rot=(a - 90) * 0.3 + H.rng.uniform(-10, 10),
                   opac=0.85)
    # la caja de 8 × 7, a mano, con los 55 y el ¶
    for i in range(9):
        H.trazo([(gx + i * lado, gy), (gx + i * lado, gy + 7 * lado)], GRAFITO, 0.55, 0.85, temblor=0.25, deriva=0.6)
    for j in range(8):
        H.trazo([(gx, gy + j * lado), (gx + 8 * lado, gy + j * lado)], GRAFITO, 0.55, 0.85, temblor=0.25, deriva=0.6)
    for c in CAJA["celdas"]:
        x = gx + (c["columna"] - 0.5) * lado
        y = gy + (c["fila"] - 0.5) * lado
        if c["signo"] in C_ACTUAL["signos"]:
            cuerpo(H, c["signo"], x, y + 2, 0.052, TINTA if c["estado"] == "hallada" else VIOLETA)
        else:
            H.maquina(x, y + 6, c["signo"], 16, GRAFITO, "middle", halo=False)
    H.mano(gx + 8 * lado + 18, gy + 20, "30 hallados", 16, TINTA)
    H.mano(gx + 8 * lado + 18, gy + 42, "25 reconstruidos", 16, VIOLETA)
    H.mano(gx + 8 * lado + 18, gy + 64, "1 hecho con los dedos: {¶}", 16, GRAFITO)
    H.mano(gx - 18, gy + 20, "la caja de 8 × 7", 16, GRAFITO, "end")
    H.mano(gx - 18, gy + 42, "como peces, al fondo (D7)", 15, GRAFITO, "end")
    H.leyenda(60, 1500, "mapa 4 · del pie a los 55 signos", [])
    H.leyenda(420, 1486, "", [("violeta", "una vasija: un generador"), ("cruz", "de la obra, la forma")])
    H.leyenda(760, 1486, "", [("maquina", "el pie, como está escrito"), ("orbita", "sus parámetros, en órbita")])
    H.firma(1150, 50, 4, TOTAL, "del pie a los 55 signos")
    return H


# ------------------------------------------------------------------ mapa 5: la cadena de estados

def fichas_simuladas():
    return json.loads((TIPO / "simulacion" / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))


def cinta_letra(H, cx, cy, escala=1.0):
    """La letra de cinta: tiras de masking, color hueso, sobre plástico negro. No curva: se pliega."""
    e = escala
    fondo = [(cx - 52 * e, cy - 46 * e), (cx + 52 * e, cy - 50 * e), (cx + 56 * e, cy + 48 * e), (cx - 50 * e, cy + 50 * e)]
    H.add("objetos", f'<path d="{d_suave(H.temblar(fondo + fondo[:1], 0.4, 0.6), True)}" fill="{TINTA}"/>')
    tiras = [((-26, 34), (-24, -26)), ((-24, -26), (14, -28)), ((14, -28), (24, -16)), ((24, -16), (24, 34))]
    for (a, b) in tiras:
        x0, y0, x1, y1 = cx + a[0] * e, cy + a[1] * e, cx + b[0] * e, cy + b[1] * e
        L = math.hypot(x1 - x0, y1 - y0)
        nx, ny = -(y1 - y0) / L * 8 * e, (x1 - x0) / L * 8 * e
        tira = [(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)]
        H.add("objetos", f'<path d="{d_suave(H.temblar(tira + tira[:1], 0.5, 0.3), True)}" fill="{HUESO}" '
                         f'stroke="#cbbf9f" stroke-width="0.5" opacity="0.97"/>')


def estratos(H, x, y, n, ancho=64, color=GRAFITO, paso=4.2):
    """Frotadas apiladas: cada una más clara que la anterior, hasta que no se lee."""
    for k in range(n):
        op = max(0.06, 1 - k / (n + 2))
        H.trazo([(x, y + k * paso), (x + ancho, y + k * paso + H.rng.uniform(-1, 1))], color, 1.1, op, temblor=0.5,
                deriva=0.6, capa="grafito")


def faraday(H, cx, cy, rx, ry, anillos=4):
    """Las ondas de Faraday sobre el charco: puntos en anillos, a la mitad de la frecuencia de la voz."""
    for k in range(1, anillos + 1):
        n = 10 + k * 8
        for i in range(n):
            if (i + k) % 2:
                continue
            a = 2 * math.pi * i / n + k * 0.2
            H.punto(cx + rx * k / anillos * math.cos(a), cy + ry * k / anillos * math.sin(a), 1.5, VIOLETA, opac=0.8)


ESTADOS = [
    # nombre, acción, notas, verso, D
    ("el pie", "el registro", ["la foto mide; el sustituto da la forma"], "«le pusieron nombre, / otra manera de enterrar.»", "D1"),
    ("calco", "acción 3", ["continuo lo hallado, punteado lo reconstruido"], "«No se salvó la piedra, / solo la opinión sobre ella.»", "D9"),
    ("placa", "acción 4", ["punzón de bola de 1 mm, por el reverso", "119 placas · 12 rotas"],
     "«de la boca sale un signo / hecho con las manos»", "D2 · D3"),
    ("cinta", "acción 6", ["masking sobre plástico negro: no curva, se pliega"], "«A la boca la taparon, a las manos no,»", "D12"),
    ("frotado", "acción 8", ["papel y grafito: cada frotada aplasta", "el peso se mide en frotadas"],
     "«Es lo que hacemos con todo, no?»", "D10"),
    ("agua", "acción 9", ["la placa en una bandeja: llega al revés y en trapecio"], "«Tocas el agua y la diosa se deforma.»",
     "D8 · D15"),
    ("voz", "acción 10", ["ondas de Faraday, a la mitad", "de la frecuencia: no es tu voz"], "«ninguna palabra»", "D14"),
]


def mapa_5():
    H = Hoja(1200, 1600, 55)
    definir(H, "oagqnse")
    F = fichas_simuladas()
    # la sala: la piscina vacía en perspectiva, y las líneas de la sala que van a su fondo
    P, z = piscina(H, 600, 1196, ancho=860, fondo_=700, prof=(160, 300), baldosa=62, agua=False, foco=600, altura=500,
                   distancia=600)
    for (x0, y0), (X, Y) in (((40, 40), (-430, 700)), ((1160, 40), (430, 700)), ((40, 1560), (-430, 0)),
                             ((1160, 1560), (430, 0))):
        x1, y1 = P(X, Y, 0)
        H.trazo([(x0, y0), (x1, y1)], GRAFITO2, 0.45, 0.55, temblor=0.2)
    # el embudo: un reloj de arena. Arriba entra el pie; en la cintura, la placa (la matriz); abajo, el charco
    cx, arriba, cintura = 600, 196, 470
    charco_y = P(0, 504, z(504))[1] - 4                       # el charco, sobre el desagüe
    H.orbita(cx, arriba, 172, 28, 0, color=GRAFITO, ancho=0.7, pasadas=1, hueco=8)
    trap = [(cx - 250, 120), (cx + 250, 120), (cx + 190, 176), (cx - 190, 176), (cx - 250, 120)]
    H.trazo(trap, GRAFITO, 0.6, 0.8, temblor=0.2)
    for s in (-1, 1):
        H.trazo([(cx + s * 172, arriba), (cx + s * 12, cintura), (cx + s * 150, charco_y)], GRAFITO, 0.6, 0.85,
                temblor=0.25)
    # la grieta: por donde baja la gota
    grieta = [(cx + 8, 150), (cx - 14, 250), (cx + 10, 330), (cx - 4, 420), (cx + 2, cintura), (cx + 20, 620),
              (cx - 16, 760), (cx + 12, 900), (cx - 2, charco_y - 10)]
    H.trazo(spline(grieta), TINTA, 0.8, temblor=0.9, deriva=1.0)
    H.trazo([(cx - 14, 250), (cx - 40, 280), (cx - 52, 318)], TINTA, 0.6, temblor=0.8)
    H.trazo([(cx + 20, 620), (cx + 46, 652)], TINTA, 0.6, temblor=0.8)
    H.aguada(H.gota(cx + 4, 940, 6), VIOLETA, 0.85, desplaza=1.5, capas=1)
    # los estados, bajando
    tira_del_pie(H, cx, arriba - 2, 150, 34, -2, lineas=2, tam=5.4)
    calco = H.mancha(420, 330, 78, 50, 0.06, 8, -6)[0]
    H.aguada(calco, PLATA, 0.35, desplaza=3, capas=1)
    contorno(H, "g", 396, 334, 0.15, TINTA, 1.0)
    contorno(H, "q", 450, 334, 0.15, VIOLETA, 1.3, punteado=True)
    placa(H, 700, cintura, 78, 92, 4, 0.7)
    repujado(H, "a", 699, cintura + 6, 0.15, 4)
    cinta_letra(H, 460, 610, 0.9)
    estratos(H, 708, 700, 22)
    estratos(H, 790, 700, 10, color=VIOLETA)
    H.mano(708, 812, "22", 14, TINTA, halo=False)
    H.mano(790, 752, "10", 14, VIOLETA, halo=False)
    d, _ = H.mancha(cx, charco_y, 150, 32, 0.07, 11)
    H.aguada(d, LILA, 0.95, desplaza=9)
    H.aguada(H.mancha(cx + 20, charco_y + 2, 90, 18, 0.1, 9)[0], VIOLETA, 0.35, desplaza=6)
    cuerpo(H, "a", cx - 40, charco_y + 4, 0.1, VIOLETA, opac=0.4, espejo=True)
    faraday(H, cx + 214, charco_y - 30, 62, 14)
    for k in range(1, 4):
        H.orbita(cx, charco_y, 150 + k * 26, 32 + k * 7, 0, hueco=16, color=VIOLETA, ancho=0.5, pasadas=1,
                 opac=0.75 - 0.15 * k)
    for k, (s, X, Y) in enumerate((("o", -250, 380), ("n", -200, 300), ("s", -300, 250), ("e", 180, 420),
                                   ("g", 260, 330), ("q", 120, 260))):      # placas en el fondo, como peces
        x, y = P(X, Y, z(Y))
        cuerpo(H, s, x, y - 10, 0.05 * 600 / (Y + 600), TINTA, rot=H.rng.uniform(-40, 40), opac=0.6)
    # la vuelta: de lo digital a una placa nueva (generación 2)
    v = H.flecha([(cx + 176, charco_y - 20), (1010, 1000), (1134, 760), (1080, 520), (900, 420), (760, cintura - 10)],
                 VIOLETA, 1.1, punteado=True)
    H.sobre(tramo(v, 0.3, 0.62), "digital, si cierra: termina y empieza", 15, VIOLETA, dy=-6)
    H.mano(930, 372, "generación 2: el esténcil", 15, VIOLETA, rot=-3)
    H.mano(940, 392, "vuelve a ser placa", 15, VIOLETA, rot=-3)
    # rótulos: a la izquierda y a la derecha del embudo
    lugares = [(860, 206, "start"), (330, 316, "end"), (820, 452, "start"), (370, 590, "end"), (880, 704, "start"),
               (330, 1000, "end"), (900, 1030, "start")]
    for (nombre, accion, notas, verso, dd), (x, y, ancla) in zip(ESTADOS, lugares):
        H.mano(x, y, nombre, 26, TINTA, ancla, rot=-2)
        H.mano(x + (0 if ancla == "start" else 0), y + 20, f"{accion} · {dd}", 14, GRAFITO, ancla)
        yy = y + 42
        for t in notas:
            H.mano(x, yy, t, 15, TINTA, ancla)
            yy += 19
        H.maquinas(x, yy + 6, [p.strip() for p in verso.split("/")], 12, VIOLETA, ancla=ancla)
    H.sobre([(cx - 190, 160), (cx + 190, 160)], "baja la materia, sube la luz", 15, GRAFITO, dy=-2)
    # los datos: las frotadas legibles de cada celda, colgando del borde
    datos = sorted(((v["celda"], v["frotado"]["legibles"], v["estado"]) for v in F.values() if v["variante"] == 1))
    x0, x1, base = 210, 990, 1210
    for i, (celda, n, estado) in enumerate(datos):
        x = x0 + (x1 - x0) * (i + 0.5) / len(datos)
        color = TINTA if estado == "hallada" else VIOLETA if estado == "reconstruida" else GRAFITO2
        H.trazo([(x, base), (x + H.rng.uniform(-1, 1), base + n * 3.6)], color, 1.6, 0.9, temblor=0.25, deriva=0.3)
    H.mano(x0, base + 124, "las frotadas legibles de cada celda, de la 1 a la 56: la tinta cuelga del borde", 15, TINTA)
    H.mano(x0, base + 144, "las halladas aguantan 22,1 en promedio; las reconstruidas, 9,8", 15, GRAFITO)
    H.leyenda(60, 1450, "mapa 5 · la cadena de estados", [])
    H.leyenda(60, 1462, "", [("plata", "el calco, la placa"), ("hueso", "la cinta")], inter=23)
    H.leyenda(380, 1462, "", [("grafito", "el frotado"), ("lila", "el agua")], inter=23)
    H.leyenda(680, 1462, "", [("punteado", "lo que todavía no es"), ("maquina", "los versos, a máquina")], inter=23)
    H.firma(1150, 50, 5, TOTAL, "la cadena de estados")
    return H


# ------------------------------------------------------------------ mapa 6: retórica y poética

def picto(H, tipo, x, y):
    """Los pictogramas de las figuras, a mano, en unos 70 px."""
    if tipo == "anáfora":                                     # olas que se repiten, cada vez menos: apenas
        for k, amp in enumerate((9, 6, 3)):
            H.trazo([(x - 34 + i * 2, y - 16 + k * 16 + amp * math.sin(i * 0.5)) for i in range(35)], TINTA, 0.9)
    elif tipo == "paradoja":                                  # una vasija con un agujero y su gota
        pts = elipse_pts(x, y - 4, 26, 24, 0, math.pi * 0.62, math.pi * 2.38)
        H.trazo(pts, TINTA, 1.1)
        H.aguada(H.gota(x, y + 34, 5), VIOLETA, 0.85, desplaza=1.2, capas=1)
        H.trazo([(x, y + 22), (x, y + 27)], VIOLETA, 0.9, punteado=True)
    elif tipo == "derivación":                                # una raíz: enterrar, desenterrar, contener, contenida
        H.trazo([(x, y - 30), (x, y)], TINTA, 1.0)
        for dx, dy in ((-26, 28), (-8, 34), (10, 32), (28, 24)):
            H.curva([(x, y), (x + dx * 0.5, y + dy * 0.4), (x + dx, y + dy)], color=TINTA, ancho=0.7)
        H.trazo([(x - 36, y - 2), (x + 36, y + 1)], GRAFITO, 0.6)
    elif tipo == "apóstrofe":                                 # ondas desde un punto: tocas el agua
        H.punto(x, y, 2.6, VIOLETA)
        for k in (1, 2, 3):
            H.orbita(x, y, 10 * k, 5 * k, 0, hueco=20, color=VIOLETA, ancho=0.7, pasadas=1, opac=1 - 0.2 * k)
    elif tipo == "prosopopeya":                               # la tierra que se bebe a sí misma
        d = f"M{x - 36},{y + 20} Q{x},{y - 34} {x + 36},{y + 20} Z"
        H.rayado(d, (x - 36, y - 14, x + 36, y + 20), -40, 2.6, GRAFITO, 0.7, 0.9)
        H.trazo([(x - 38, y + 20), (x + 38, y + 20)], TINTA, 0.8)
        pts = [(x + 14 * (1 - t) * math.cos(t * 9), y - 20 + 34 * t + 5 * (1 - t) * math.sin(t * 9)) for t in
               [i / 40 for i in range(41)]]
        H.trazo(pts, VIOLETA, 0.9)
    elif tipo == "ciclo":                                     # una espiral abierta: termina y empieza
        pts = [(x + (4 + 2.6 * t) * math.cos(t), y + (4 + 2.6 * t) * math.sin(t)) for t in
               [i * 0.1 for i in range(120)]]
        H.trazo(pts, TINTA, 0.9)
        H.punta(pts[-1][0], pts[-1][1], math.atan2(pts[-1][1] - pts[-4][1], pts[-1][0] - pts[-4][0]), TINTA, 0.9, 8)
    elif tipo == "antítesis":                                 # dos flechas opuestas: una continua, otra punteada
        H.flecha([(x - 34, y - 8), (x + 34, y - 8)], TINTA, 1.0, curva=False)
        H.flecha([(x + 34, y + 10), (x - 34, y + 10)], VIOLETA, 1.3, punteado=True, curva=False)
    elif tipo == "metáfora":                                  # la letra es una vasija: agua en la cuenca de la a
        H.aguada(f"M{x - 22},{y + 4} L{x + 22},{y + 4} L{x + 20},{y + 28} L{x - 20},{y + 28}Z", LILA, 0.9, desplaza=2,
                 capas=1)
        contorno(H, "a", x, y, 0.16, TINTA, 1.0)
    elif tipo == "sinécdoque":                                # la cinta por el rostro tapado
        H.punto(x - 12, y - 4, 2.4, TINTA)
        H.punto(x + 12, y - 4, 2.4, TINTA)
        tira = [(x - 32, y - 14), (x + 32, y - 8), (x + 30, y + 4), (x - 34, y - 2)]
        H.add("objetos", f'<path d="{d_suave(H.temblar(tira + tira[:1], 0.4, 0.3), True)}" fill="{HUESO}" '
                         f'stroke="#cbbf9f" stroke-width="0.6"/>')
        H.trazo([(x - 12, y + 18), (x + 12, y + 18)], TINTA, 0.9)
    elif tipo == "elipsis":                                   # una celda vacía
        H.celda(x, y, 40, VIOLETA, 1.1, punteada=True, doble=False)
        H.maquina(x, y + 44, "…", 16, VIOLETA, "middle", halo=False)
    elif tipo == "etimología":                                # la portada: una puerta abierta
        H.trazo([(x - 20, y + 28), (x - 20, y - 18), (x - 12, y - 28), (x + 12, y - 28), (x + 20, y - 18), (x + 20, y + 28)],
                TINTA, 1.0)
        H.trazo([(x - 20, y + 28), (x - 4, y + 34), (x - 4, y - 16), (x - 20, y - 18)], TINTA, 0.8)
    elif tipo == "sentencia":                                 # una piedra
        d, _ = H.mancha(x, y, 30, 20, 0.16, 8, -8)
        H.rayado(d, (x - 34, y - 24, x + 34, y + 24), 30, 2.4, GRAFITO, 0.7, 0.95)
        H.add("lineas", f'<path d="{d}" fill="none" stroke="{TINTA}" stroke-width="0.9"/>')
    elif tipo == "interrogación":                             # una ? de la que cae una gota
        cuerpo(H, "?", x, y, 0.13, TINTA)
        H.aguada(H.gota(x + 2, y + 44, 4.5), VIOLETA, 0.85, desplaza=1.2, capas=1)


FIGURAS = [
    # figura, pictograma, glosa, lo que hace la letra, verso que la lleva, lado
    ("anáfora y gradación", "anáfora", "«es decir» vuelve, y cada vez dice menos", "el temblor de la mano; tres planos a 1,6°",
     "es decir, apenas, es decir, temblor,"),
    ("paradoja", "paradoja", "ningún contenedor aguanta lo que contiene", "toda cuenca se abre en un desagüe",
     "y ningún contenedor aguanta lo que contiene."),
    ("derivación", "derivación", "enterrar, desenterrar, contener, contenida", "el nombre no es Kochamama",
     "A la ídolo la desenterraron,"),
    ("apóstrofe", "apóstrofe", "«Tocas»: le habla a quien mira", "tocar deforma el espécimen",
     "Tocas el agua y la diosa se deforma."),
    ("prosopopeya", "prosopopeya", "la tierra bebe, como un cuerpo", "la gota: solo gotea lo que mira abajo",
     "La tierra se dio de beber a sí misma"),
    ("repetición y ciclo", "ciclo", "«termina y empieza», dos veces", "el bucle; frotar y repujar otra",
     "Termina y empieza,"),
    ("antítesis", "antítesis", "escrito y hablado; hallado y reconstruido", "continuo y punteado, en todos los estados",
     "Y es que lo que vuelve, vuelve escrito;"),
    ("metáfora", "metáfora", "la letra es una vasija", "fondo, borde, desagüe y afuera", "Quedó el contenedor"),
    ("sinécdoque y metonimia", "sinécdoque", "el pie por la lámina; la cinta por el rostro",
     "las letras salen del pie; el punto de cinta", "A la boca la taparon, a las manos no,"),
    ("elipsis", "elipsis", "lo que falta se ve vacío", "la celda vacía: lo que no cabe", "ninguna palabra,"),
    ("etimología", "etimología", "portada y puerta; el ojo del tipo; componer", "la puerta sobre la celda 1; el {¶}",
     "de la boca sale un signo"),
    ("sentencia", "sentencia", "«Todos los archivos funcionan así»", "de la piscina no se saca nada",
     "Todos los archivos funcionan así."),
    ("interrogación retórica", "interrogación", "«no?»: pregunta sin esperar respuesta",
     "la {?} se arma sin modelo; la {¿} no es su espejo", "Es lo que hacemos con todo, no?"),
]


def mapa_6():
    H = Hoja(1200, 1600, 66)
    definir(H, "a?")
    versos = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8").split("\n")
    # los márgenes: los verbos, como en un cuaderno
    H.add("textos", f'<text x="58" y="300" font-family="La Belle Aurore" font-size="40" fill="{TINTA}" '
                    f'transform="rotate(-90 58 300)" letter-spacing="3">ENTERRAR</text>')
    H.add("textos", f'<text x="1162" y="120" font-family="La Belle Aurore" font-size="40" fill="{TINTA}" '
                    f'transform="rotate(90 1162 120)" letter-spacing="3">CONTENER</text>')
    H.mano(1150, 1560, "DESENTERRAR", 40, TINTA, "end", rot=0)
    # el agua: el poema entero, a máquina, adentro
    cx, cy, rx, ry = 600, 800, 226, 356
    d, _ = H.mancha(cx, cy, rx, ry, 0.05, 12)
    H.aguada(d, LILA, 0.42, desplaza=18, capas=2, borde=0.7)
    H.orbita(cx, cy, rx + 16, ry + 10, 2, hueco=10, color=TINTA, ancho=0.8, pasadas=2)
    H.aguada(H.gota(cx + 4, cy + ry + 44, 7), VIOLETA, 0.85, desplaza=2, capas=1)
    H.trazo([(cx + 4, cy + ry + 14), (cx + 4, cy + ry + 32)], VIOLETA, 1.0, punteado=True)
    y = cy - 316
    pos = {}
    operan = {f[4] for f in FIGURAS}
    for v in versos:
        if not v.strip():
            y += 7
            continue
        pos[v.strip()] = y
        H.maquina(cx, y, v.strip(), 11, VIOLETA if v.strip() in operan else GRAFITO, "middle", halo=False)
        y += 13.4
    # las figuras, alrededor, en el orden de sus versos; cada una unida al suyo por una línea que serpentea
    orden = sorted(FIGURAS, key=lambda f: pos[f[4]])
    izq = [(96, 150 + 210 * k) for k in range(6)]
    der = [(872, 176 + 210 * k) for k in range(6)]
    lugares = [izq[k // 2] if k % 2 == 0 else der[k // 2] for k in range(12)] + [(470, 1300)]
    for (nombre, tipo, glosa, letra, verso), (x, y0) in zip(orden, lugares):
        picto(H, tipo, x + 36, y0)
        H.mano(x + 84, y0 + 4, nombre, 20, TINTA, rot=-1.5)
        yy = H.manos(x, y0 + 58, partir(glosa, 36), 14.5, GRAFITO, inter=1.2)
        H.manos(x, yy + 22, partir("la letra: " + letra, 34), 15, TINTA, inter=1.2)
        vy = pos[verso] - 4
        medio_verso = len(verso) * 11 * 0.6 / 2
        abajo = y0 > 1250
        izquierda = x < cx
        if abajo:                                               # la de abajo sube al último verso
            vx = cx - medio_verso - 6
            camino = [(x + 36, y0 - 44), (x + 10, y0 - 120), (cx - rx - 10, vy + 30), (cx - rx + 30, vy), (vx, vy)]
        else:
            vx = cx - medio_verso - 6 if izquierda else cx + medio_verso + 6
            borde = cx - rx - 30 if izquierda else cx + rx + 30
            sx = x + 92 + len(nombre) * 8.6 if izquierda else x - 6
            camino = [(sx, y0), ((sx + borde) / 2 + H.rng.uniform(-20, 20), (y0 + vy) / 2 + H.rng.uniform(-30, 30)),
                      (borde, vy + (18 if vy > y0 else -18)), (borde + (26 if izquierda else -26), vy), (vx, vy)]
        c = spline(camino, 22)
        ondulado = [(px + 2.6 * math.sin(i * 0.33), py + 2.6 * math.cos(i * 0.27)) for i, (px, py) in enumerate(c)]
        H.trazo(ondulado, GRAFITO, 0.6, 0.85, temblor=0.3, deriva=1.0)
        H.punto(vx, vy, 2.2, VIOLETA)
    H.leyenda(60, 1440, "mapa 6 · retórica y poética", [])
    H.leyenda(60, 1452, "", [("maquina", "el poema: en violeta, los versos que operan"),
                             ("lila", "el agua: cada vuelta pasa por ella")], inter=23)
    H.mano(96, 1540, "un dibujo por figura; debajo, lo que hace la letra", 15, GRAFITO)
    H.firma(1090, 50, 6, TOTAL, "retórica y poética")
    return H


# ------------------------------------------------------------------ salida

CARAS = (("Courier Prime", "courier-prime-latin-400-normal.woff2", 400, "normal"),
         ("Courier Prime", "courier-prime-latin-700-normal.woff2", 700, "normal"),
         ("Courier Prime", "courier-prime-latin-400-italic.woff2", 400, "italic"),
         ("Newsreader", "newsreader-latin-300-normal.woff2", 300, "normal"),
         ("Newsreader", "newsreader-latin-400-normal.woff2", 400, "normal"),
         ("Newsreader", "newsreader-latin-400-italic.woff2", 400, "italic"),
         ("La Belle Aurore", "la-belle-aurore-latin-400-normal.woff2", 400, "normal"))


def html(svg, W, H):
    caras = "".join(f'@font-face{{font-family:"{fam}";src:url("{(FUENTES / arch).as_uri()}") format("woff2");'
                    f'font-weight:{peso};font-style:{est}}}' for fam, arch, peso, est in CARAS)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{caras}html,body{{margin:0;background:{PAPEL}}}'
            f'svg{{display:block;width:{W}px;height:{H}px}}</style></head><body>{svg}</body></html>')


MAPAS = {1: ("el_proyecto_entero", mapa_1), 2: ("teoria_y_fuentes", mapa_2),
         3: ("la_obra_decision_por_decision", mapa_3), 4: ("del_pie_a_los_55", mapa_4),
         5: ("la_cadena_de_estados", mapa_5), 6: ("retorica_y_poetica", mapa_6)}


def preparar(cache=None):
    global C_ACTUAL
    C_ACTUAL = cuerpos(cache)
    return C_ACTUAL


def main(numeros=None, cache=None):
    from generar_laminas import chrome
    SALIDA.mkdir(exist_ok=True)
    preparar(cache)
    ejecutable = chrome()
    modo = [] if ejecutable.endswith("headless_shell") else ["--headless=new"]
    for i in numeros or sorted(MAPAS):
        nombre, hacer = MAPAS[i]
        H = hacer()
        svg = H.svg()
        base = SALIDA / f"mapa_{i}_{nombre}"
        base.with_suffix(".svg").write_text(svg, encoding="utf8")
        pagina = SALIDA / f".mapa_{i}.html"
        pagina.write_text(html(svg, H.W, H.H), encoding="utf8")
        subprocess.run([ejecutable, *modo, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--allow-file-access-from-files", "--virtual-time-budget=5000",
                        f"--window-size={H.W},{H.H}", f"--screenshot={base.with_suffix('.png')}", pagina.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pagina.unlink()
        print(f"mapa {i}: {nombre}")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:] if not a.startswith("--")] or None)
