"""Los mapas del informe de decisiones de Contenida, dibujados a mano (con código).

Uso (desde la raíz del repositorio):
    python3 tipografia/informe/mapas.py            # los seis
    python3 tipografia/informe/mapas.py 1 4        # solo esos

Escribe en tipografia/informe/mapas/ seis mapas en SVG y en PNG (con Chromium,
como las láminas). Se rehicieron el 17.10.2026 tomando como modelo las versiones
mejoradas que trajo Joaquin: cada estado se dibuja con su material (materia.py:
aluminio, grafito, cinta, calco, papel, agua y un hilo de tinta violeta que une
las etapas), los títulos van a mano y lo que hay que saber, a máquina. El
repertorio de trazos sigue en mano.py: líneas que tiemblan apenas, aguadas de
tinta de esténcil, rayados de grafito.

Los cuerpos de los signos vienen de la gramática (simulacion/desenterrar.py): son
la propuesta de la máquina y, como en las láminas, no entran en la caja. Las cotas
del mapa 4 se miden sobre esos cuerpos.
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

from mano import (GRAFITO, GRAFITO2, HUESO, LILA, PAPEL, TINTA, VIOLETA, Hoja,  # noqa: E402
                  Perspectiva, bezier, d_suave, elipse_pts, normales, remuestrear, spline)
import materia as X  # noqa: E402

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


# ------------------------------------------------------------------ medidas de un signo (para las cotas)

_MASCARAS = {}


def mascara(s):
    """El signo rasterizado en el lienzo de la placa (1 px = 1 unidad), con 100 px de margen."""
    if s not in _MASCARAS:
        import re
        import numpy as np
        from PIL import Image, ImageChops, ImageDraw
        img = Image.new("1", (800, 800), 0)
        for sub in C_ACTUAL["signos"][s]["d"].split("Z"):
            nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", sub)]
            if len(nums) < 6:
                continue
            m = Image.new("1", (800, 800), 0)
            ImageDraw.Draw(m).polygon([(nums[i] + 100, nums[i + 1] + 100) for i in range(0, len(nums) - 1, 2)], fill=1)
            img = ImageChops.logical_xor(img, m)
        _MASCARAS[s] = np.array(img)
    return _MASCARAS[s]


def caja_signo(s):
    import numpy as np
    ys, xs = np.nonzero(mascara(s))
    return xs.min() - 100, ys.min() - 100, xs.max() - 100, ys.max() - 100


def en_hoja(x, y, cx, cy, e):
    """Del lienzo de la placa a la hoja, para un signo puesto con _tr(cx, cy, e, 0)."""
    return cx + (x - 300) * e, cy + (y - 320) * e


def cota(H, a, b, texto, lado=-1, sep=10.0, color=TINTA, tam=12.0, ancla="middle", rot_texto=0.0):
    """Una cota a mano: la línea entre a y b con sus topes y la medida escrita al lado."""
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    nx, ny = -math.sin(ang) * lado * sep, math.cos(ang) * lado * sep
    p, q = (a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny)
    for o in (a, b):                                          # las líneas de referencia
        H.trazo([o, (o[0] + nx * 1.4, o[1] + ny * 1.4)], GRAFITO2, 0.5, temblor=0.05, deriva=0)
    H.trazo([p, q], color, 0.7, temblor=0.1, deriva=0)
    for o, sgn in ((p, 1), (q, -1)):
        H.punta(o[0], o[1], ang + (math.pi if sgn > 0 else 0), color, 0.7, 6, 22)
    mx, my = (p[0] + q[0]) / 2 + nx * 0.9, (p[1] + q[1]) / 2 + ny * 0.9 + (4 if ny >= 0 else 0)
    H.maquina(mx, my, texto, tam, color, ancla, halo=True, rot=rot_texto)


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


# ------------------------------------------------------------------ mapa 1: el proyecto entero

def reconstruida_de_muestra():
    """Una letra reconstruida para mostrar el punteado: la ñ, como en el mapa 5."""
    return "ñ" if ESTADO.get("ñ") == "reconstruida" else next(
        c["signo"] for c in CAJA["celdas"] if c["estado"] == "reconstruida" and c["signo"].isalpha())


def mapa_1():
    H = Hoja(1200, 1600, 11)
    rec = reconstruida_de_muestra()
    definir(H, "oglna" + rec)
    a = ref("a")
    X.construccion(H, [96, 600, 1104], [250, 520, 960, 1300])

    # 1 · la obra: la piscina vacía
    P, z = piscina(H, 600, 205, ancho=480, fondo_=170, prof=(40, 70), baldosa=40, agua=True, foco=300, altura=400,
                   distancia=300)
    dx, dy = P(0, 170 * 0.72, z(170 * 0.72))
    X.charco(H, dx + 10, dy + 2, 70, 12, color=VIOLETA, opac=0.45)
    X.rotulo(H, 52, 120, "La obra", ["Contener una ruina · 22.8.2026"], tam=38, sub=13,
             verso=["«Quedó el contenedor", " de lo que ya no está.»"])
    H.maquinas(900, 120, ["partir del registro,", "no de la piedra."], 13, VIOLETA)
    H.trazo([(892, 128), (760, 150)], GRAFITO, 0.6)

    # 2 · desenterrar: el pie y el calco
    X.papel(H, 470, 360, 360, 74, 2.5)
    H.maquinas(310, 350, ["EL IDOLO KOCHAMAMA, según Posnansky", "la lámina y su pie"], 11.5, GRAFITO, halo=False, rot=2.5)
    X.calco(H, 740, 350, 250, 150, -7)
    contorno(H, "o", 668, 362, 0.2, TINTA, 1.0, rot=-7)
    contorno(H, "g", 742, 352, 0.2, TINTA, 1.0, rot=-7)
    contorno(H, rec, 812, 344, 0.2, VIOLETA, 1.4, punteado=True, rot=-7)
    H.maquina(150, 296, "Posnansky, 1945", 12, VIOLETA)
    H.flecha([(170, 304), (240, 322), (300, 338)], TINTA, 0.7)
    H.maquina(1000, 288, "Tshuma, 2025", 12, VIOLETA)
    H.flecha([(1000, 296), (930, 312), (868, 322)], TINTA, 0.7)
    X.rotulo(H, 930, 440, "Desenterrar", ["acciones 0 – 3", "30 hallados · 25 por", "reconstruir"], tam=36, sub=12.5)

    # 3 · contener: las vasijas, la placa y la caja
    for s, x in (("o", 300), ("l", 410), ("n", 500)):
        aguada_signo(H, s, x, 780 - (429 - 320) * 0.48, 0.48, VIOLETA, 0.8)
        H.maquina(x, 812, s, 13, TINTA, "middle", halo=False)
    X.gota_que_cae(H, 300, 800, 5)
    X.aluminio(H, 720, 700, 168, 196, -3)
    X.relieve(H, a, _tr(720, 712, 0.32, -3), 2.6, 0.32)
    H.maquina(720, 822, "a", 13, TINTA, "middle", halo=False)
    caja_a_mano(H, 900, 618, 23, color=TINTA)
    H.maquina(992, 800, "caja 8 × 7", 13, TINTA, "middle", halo=False)
    for y in (680, 740):
        H.flecha([(814, y), (890, y)], TINTA, 0.6, curva=False)
    X.rotulo(H, 52, 590, "Contener", ["acciones 4 – 7"], tam=38, sub=13,
             verso=["«y ningún contenedor", " aguanta lo que contiene.»"])
    H.maquinas(56, 730, ["cada letra,", "una placa suelta."], 13, VIOLETA)
    H.maquina(56, 870, "Mahendran, 2020 · escritura como vasija", 12, VIOLETA)
    H.flecha([(150, 856), (210, 830), (262, 790)], TINTA, 0.7)

    # 4 · devolver: el frotado, el agua y la voz
    X.frotado(H, a, 410, 1090, 220, 196, 0.36, -6, 1.0)
    X.charco(H, 790, 1094, 250, 74, opac=0.42)
    X.reflejo(H, a, 794, 1104, 0.28, VIOLETA, 0.45, 12)
    X.ondas(H, 790, 1094, 240, 70, 6)
    X.gota_que_cae(H, 790, 1030, 6)
    H.maquina(330, 980, "frotar", 13, VIOLETA)
    H.flecha([(352, 988), (370, 1000), (384, 1010)], VIOLETA, 0.8)
    H.maquina(800, 962, "tocar", 13, VIOLETA)
    H.maquina(1010, 1000, "voz: deformar", 13, VIOLETA)
    H.flecha([(1040, 1008), (1010, 1040), (960, 1066)], TINTA, 0.7)
    X.rotulo(H, 52, 1030, "Devolver", ["acciones 8 – 12"], tam=38, sub=13,
             verso=["«Tocas el agua", " y la diosa se deforma.»"])

    # 5 · lo digital, si cierra: todavía punteado
    contorno(H, "a", 600, 1400, 0.42, VIOLETA, 1.6, punteado=True)
    X.rotulo(H, 210, 1330, "Digital", ["si cierra"], tam=38, sub=13)
    v = H.flecha([(700, 1380), (1040, 1360), (1150, 1150), (1110, 780), (1080, 700)], VIOLETA, 1.1, punteado=True)
    H.maquina(1000, 1300, "volver a la caja", 13, VIOLETA, "end")
    H.maquina(660, 1500, "«termina y empieza.»", 13, VIOLETA)
    H.trazo([(600, 1470), (600, 1524)], VIOLETA, 1.0, punteado=True)
    X.gota_que_cae(H, 600, 1544, 5)

    # el hilo de tinta: de una etapa a la otra
    X.hilo(H, [(dx, dy + 6), (560, 250), (520, 316)], 6, 3)
    X.hilo(H, [(470, 400), (440, 470), (400, 560), (380, 600)], 5, 3)
    X.hilo(H, [(520, 398), (600, 470), (690, 560), (712, 598)], 5, 3)
    X.hilo(H, [(330, 820), (360, 900), (400, 990)], 5, 3)
    X.hilo(H, [(722, 800), (760, 900), (790, 1026)], 5, 3)
    X.hilo(H, [(430, 1192), (500, 1240), (590, 1290)], 5, 3)
    X.hilo(H, [(790, 1170), (700, 1240), (612, 1292)], 5, 3)

    X.pie_de_mapa(H, 1, "El proyecto entero")
    return H


# ------------------------------------------------------------------ mapa 2: teoría y fuentes

FUENTES_T = {
    "EthnoGraphemes": dict(autor="Mahendran, 2020", toma=[
        "escritura como vasija", "tocar · mojar · escuchar", "caja baja · cartas · inacabado",
        "ningún motivo pegado", "ética de quien viene de afuera"],
        no=["revitalizar una lengua", "frecuencia por letra", "tatuar"]),
    "Afrography": dict(autor="Tshuma, 2025", toma=[
        "¿quién lo escribió?", "letras sacadas de un muro: el pie", "objeto → signo → objeto",
        "restricción · custodia · herramientas", "la placa rota no se corrige", "desenterrar · contener · devolver"],
        no=["inventar una escritura", "letras por módulos", "el estallido"]),
    "Tihuanacu": dict(autor="Posnansky, 1945", toma=[
        "La Paz contiene la ruina", "piso · desagüe · piscina vacía", "el material decide", "ausencia: punteado"],
        no=["su cronología", "su tesis del título", "su lectura racial"]),
    "La iconografía Tiwanaku": dict(autor="Agüero, Uribe y Berenguer, 2003", toma=[
        "elementos · motivos · figuras", "pares: la ¿ no es la ? al revés", "pecho y espalda · perfiles"],
        no=["interpretar la iconografía", "traducir el «calendario»"]),
    "Manuaje": dict(autor="Cárcamo Pino, 2021-2025", toma=[
        "las manos no tienen lengua", "dos manos, una boca", "tocar por fuera, mirar por dentro",
        "el modo se inventa al hacer", "reescribir cruzado: el pie"],
        no=["el imbunche", "la cognición como prueba", "oralitura para lo andino"]),
    "Forest and Philosophy": dict(autor="Johnson, 2007", toma=[
        "el tacto también es estética", "los anillos: la serie de frotados", "pensar como el agua",
        "la bisagra de la tapa", "dado, nunca vendido"],
        no=["la letra de madera", "el taller sin nombres"]),
    "Contener una ruina": dict(autor="Rebeca Paz Prada, 2026", toma=[
        "registro", "aluminio", "cinta", "agua", "voz", "piscina vacía"],
        no=["lecturas rituales", "fotos y cuerpo de Rebeca"]),
}


def sombreado(H, d, caja, angulo=-38.0, paso=2.6, opac=0.7, desvanece=None):
    """Sombra de grafito, recortada a una forma."""
    H.rayado(d, caja, angulo, paso, GRAFITO, 0.6, opac, desvanece=desvanece)


def vasija(H, cx, cy, alto=170):
    """Una vasija rajada, a grafito: la escritura como vasija, que aquí no retiene."""
    a = alto
    medio = [(0.10, 0.0), (0.12, 0.06), (0.09, 0.12), (0.11, 0.18), (0.30, 0.34), (0.36, 0.52), (0.30, 0.74),
             (0.18, 0.92), (0.15, 1.0)]
    der = [(cx + x * a, cy - a / 2 + y * a) for x, y in medio]
    izq = [(cx - x * a, cy - a / 2 + y * a) for x, y in medio[::-1]]
    pts = spline(der + izq, 8, True)
    d = d_suave(pts, True)
    H.add("aguadas", f'<path d="{d}" fill="#d9d6cf"/>')
    sombreado(H, d, (cx - 0.4 * a, cy - a / 2, cx + 0.4 * a, cy + a / 2), -50, 2.2, 0.55)
    medio_der = f"M{cx + 0.02 * a:.1f},{cy - a / 2:.1f} L{cx + 0.4 * a:.1f},{cy - a / 2:.1f} L{cx + 0.4 * a:.1f},{cy + a / 2:.1f} " \
                f"L{cx + 0.04 * a:.1f},{cy + a / 2:.1f}Z"
    cid = H.uid("clip")
    H.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
    H.add("grafito", f'<g clip-path="url(#{cid})"><path d="{medio_der}" fill="{GRAFITO}" opacity="0.18"/></g>')
    H.trazo(pts, TINTA, 1.0, temblor=0.25, deriva=0.6)
    grieta = [(cx + 0.05 * a, cy - a * 0.44), (cx + 0.11 * a, cy - a * 0.2), (cx + 0.04 * a, cy - a * 0.05),
              (cx + 0.12 * a, cy + a * 0.12), (cx + 0.07 * a, cy + a * 0.3), (cx + 0.1 * a, cy + a * 0.48)]
    H.trazo(grieta, TINTA, 1.2, temblor=0.7, deriva=0.3)
    X.gota_que_cae(H, cx + 0.1 * a, cy + a * 0.64, 6)


def taburete(H, cx, cy, ancho=150):
    """Un taburete tallado, en negro: el objeto que se vuelve signo y otra vez objeto."""
    w = ancho
    pts = [(-0.5, -0.36), (-0.25, -0.28), (0, -0.26), (0.25, -0.28), (0.5, -0.36), (0.46, -0.2), (0.2, -0.14),
           (0.14, 0.0), (0.16, 0.2), (0.28, 0.3), (0.42, 0.36), (-0.42, 0.36), (-0.28, 0.3), (-0.16, 0.2),
           (-0.14, 0.0), (-0.2, -0.14), (-0.46, -0.2)]
    P = spline([(cx + x * w, cy + y * w) for x, y in pts], 5, True)
    d = d_suave(H.temblar(P, 0.3, 0.5), True)
    X.rayado_frotado(H, cx - 0.55 * w, cy + 0.33 * w, 1.1 * w, 0.1 * w, -8, 2.0, opac=0.45)   # la sombra en el piso
    H.add("objetos", f'<path d="{d}" fill="#1f1d1b"/>')
    sombreado(H, d, (cx - w / 2, cy - 0.4 * w, cx + w / 2, cy + 0.4 * w), 30, 3.4, 0.35)
    for k in (-1, 1):                                         # los calados
        dd, _ = H.mancha(cx + k * 0.05 * w, cy + 0.05 * w, 0.025 * w, 0.07 * w, 0.1, 6)
        H.add("objetos", f'<path d="{dd}" fill="{PAPEL}"/>')


def losa(H, cx, cy, ancho=190):
    """Una losa con su desagüe: la cloaca de Tiwanaku, hecha piso."""
    w, h, p = ancho, ancho * 0.26, ancho * 0.3
    frente = [(cx - w / 2, cy), (cx + w / 2, cy), (cx + w / 2, cy + h), (cx - w / 2, cy + h)]
    tapa = [(cx - w / 2, cy), (cx - w / 2 + p, cy - p * 0.55), (cx + w / 2 + p, cy - p * 0.55), (cx + w / 2, cy)]
    lado = [(cx + w / 2, cy), (cx + w / 2 + p, cy - p * 0.55), (cx + w / 2 + p, cy + h - p * 0.55), (cx + w / 2, cy + h)]
    for cara, color, op in ((tapa, "#e7e3da", 0.35), (frente, "#cfcac0", 0.6), (lado, "#b7b1a6", 0.85)):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in cara) + "Z"
        H.add("aguadas", f'<path d="{d}" fill="{color}"/>')
        xs, ys = [q[0] for q in cara], [q[1] for q in cara]
        sombreado(H, d, (min(xs), min(ys), max(xs), max(ys)), -35 if cara is not tapa else 15, 2.6, op)
        H.trazo(cara + cara[:1], TINTA, 0.8, temblor=0.3, deriva=0.6)
    # el desagüe: un hueco cuadrado en la tapa
    t = lambda u, v: (cx - w / 2 + u * w + v * p, cy - v * p * 0.55)   # noqa: E731
    hueco = [t(0.4, 0.3), t(0.62, 0.3), t(0.62, 0.72), t(0.4, 0.72)]
    H.add("objetos", f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in hueco)}Z" fill="#3a3733"/>')
    H.trazo(hueco + hueco[:1], TINTA, 0.8)
    for _ in range(40):                                       # polvo de la ruina
        H.punto(cx + H.rng.uniform(-w * 0.7, w * 0.9), cy + h + H.rng.uniform(-6, 26), H.rng.uniform(0.6, 1.4),
                VIOLETA if H.rng.random() < 0.3 else GRAFITO2, opac=0.6)


def lapiz(H, cx, cy, largo=190, ancho=18, rot=-18.0):
    """Un lápiz: madera y grafito; el agarre de tres dedos que escribe y dibuja."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    g = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)   # noqa: E731
    L, w = largo / 2, ancho / 2
    cuerpo_ = [g(-L, -w), g(L - 36, -w), g(L - 36, w), g(-L, w)]
    H.add("aguadas", f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in cuerpo_)}Z" fill="{HUESO}"/>')
    H.trazo(cuerpo_ + cuerpo_[:1], TINTA, 0.9)
    H.trazo([g(-L, 0), g(L - 36, 0)], GRAFITO2, 0.6)
    madera = [g(L - 36, -w), g(L - 10, -w * 0.3), g(L - 10, w * 0.3), g(L - 36, w)]
    H.add("objetos", f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in madera)}Z" fill="#e2c9a0" stroke="{TINTA}" '
                     f'stroke-width="0.8"/>')
    punta = [g(L - 10, -w * 0.3), g(L, 0), g(L - 10, w * 0.3)]
    H.add("objetos", f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in punta)}Z" fill="{GRAFITO}"/>')
    X.rayado_frotado(H, g(L, 0)[0] + 4, g(L, 0)[1] - 6, 60, 16, -10, 1.6, opac=0.5)


def tronco(H, cx, cy, r=70):
    """El corte de un tronco: sus anillos cuentan la vida del árbol, y se abren abajo."""
    d, _ = H.mancha(cx, cy, r * 1.06, r * 0.92, 0.04, 14)
    H.add("aguadas", f'<path d="{d}" fill="#e9dcc2"/>')
    sombreado(H, d, (cx - r * 1.1, cy - r, cx + r * 1.1, cy + r), 20, 4.2, 0.25)
    for k in range(1, 9):
        rr = r * k / 8
        H.orbita(cx, cy - (8 - k) * 1.0, rr * 1.04, rr * 0.9, -6, hueco=12, color=GRAFITO if k < 8 else TINTA,
                 ancho=0.55 if k < 8 else 1.2, pasadas=1, opac=0.9)
    H.punto(cx, cy - 8, 2.2, TINTA)
    H.trazo([(cx + 4, cy - 12), (cx + 20, cy - 34), (cx + 30, cy - 60)], TINTA, 0.9, temblor=0.7)


def lista(H, x, y, items, ancla="start", color=TINTA, tam=13.0, paso=24.0):
    """Lo que se toma, a máquina; devuelve dónde termina cada renglón (de ahí sale la hebra)."""
    puntas = []
    for i, t in enumerate(items):
        yy = y + i * paso
        H.maquina(x, yy, t, tam, color, ancla)
        largo = len(t) * tam * 0.6
        puntas.append((x + largo + 8 if ancla == "start" else x - largo - 8, yy - 4))
    return puntas


def hebras(H, puntas, destino, nudo, color=TINTA, abre=3.4):
    """De cada renglón, una hebra fina; las hebras se juntan en un haz que llega a la o."""
    n = len(puntas)
    for i, p in enumerate(puntas):
        off = (i - (n - 1) / 2) * abre
        pts = [p, (p[0] + (nudo[0] - p[0]) * 0.3, p[1]), (nudo[0], nudo[1] + off),
               (destino[0], destino[1] + off * 0.5)]
        c = color if i % 2 == 0 else (GRAFITO2 if color == TINTA else LILA)
        H.trazo(spline(pts), c, 0.6, 0.9, temblor=0.2, deriva=0.6)
        H.punto(p[0], p[1], 1.8, c)


def no_se_toma(H, items, x, y, ancla="start", paso=22.0, desde=None):
    """Lo que no se toma: una raya que sale de la fuente y se corta con un tope; la nota, en grafito."""
    for i, t in enumerate(items):
        yy = y + i * paso
        tope = x - 8 if ancla == "start" else x + 8
        if desde:
            H.trazo([desde, (tope, yy - 4)], GRAFITO, 0.6, temblor=0.15, deriva=0.4)
        H.trazo([(tope, yy - 10), (tope, yy + 2)], GRAFITO, 1.1, temblor=0.05, deriva=0)
        H.maquina(x, yy, t, 12, GRAFITO, ancla)


def titulo_fuente(H, x, y, nombre, autor, ancla="start", tam=28):
    H.cruz(x - 16 if ancla == "start" else x + 16, y - 8, 5)
    H.mano(x, y, nombre, tam, TINTA, ancla, rot=-1.5)
    H.maquina(x + (6 if ancla == "start" else -6), y + 24, autor, 13, GRAFITO, ancla, estilo="italic")


def mapa_2():
    H = Hoja(1600, 1300, 22)
    definir(H, "o¿?a")
    F = FUENTES_T
    X.construccion(H, [800], [640])
    c = (800, 600)
    # el centro: la o, abierta abajo; gotea
    d, _ = H.mancha(c[0], c[1] + 70, 170, 26, 0.2, 9)
    H.aguada(d, LILA, 0.45, desplaza=14)
    aguada_signo(H, "o", c[0], c[1], 0.92, VIOLETA, 0.82)
    X.gota_que_cae(H, c[0], c[1] + 130, 9)
    H.mano(c[0], c[1] + 210, "Contenida", 40, TINTA, "middle", rot=-1)
    H.maquina(c[0], c[1] + 240, "contener / dejar salir", 15, TINTA, "middle")
    H.eje(c[0], c[1] + 256, c[0] + 2, c[1] + 340, VIOLETA, 0.8)
    for _ in range(60):
        H.punto(c[0] + H.rng.gauss(0, 120), c[1] + H.rng.gauss(30, 140), H.rng.uniform(0.6, 1.6),
                VIOLETA if H.rng.random() < 0.6 else LILA, opac=0.6)
    izq, der, arr = (c[0] - 112, c[1] - 10), (c[0] + 112, c[1] - 10), (c[0], c[1] - 108)

    # EthnoGraphemes: arriba a la izquierda
    vasija(H, 150, 190, 180)
    titulo_fuente(H, 270, 112, "EthnoGraphemes", F["EthnoGraphemes"]["autor"])
    no_se_toma(H, F["EthnoGraphemes"]["no"], 300, 176, desde=(220, 220))
    p = lista(H, 70, 360, F["EthnoGraphemes"]["toma"])
    hebras(H, p, (izq[0], izq[1] - 30), (560, 470))

    # Contener una ruina: arriba, al centro
    X.charco(H, 690, 150, 92, 22, color=VIOLETA, opac=0.4)
    X.ondas(H, 690, 150, 110, 26, 5)
    X.aluminio(H, 690, 110, 84, 92, 4)
    titulo_fuente(H, 820, 92, "Contener una ruina", F["Contener una ruina"]["autor"])
    H.mano(580, 250, "no se toma:", 17, VIOLETA, "end", rot=-1)
    no_se_toma(H, F["Contener una ruina"]["no"], 584, 280, "end", desde=(650, 196))
    p = lista(H, 840, 186, F["Contener una ruina"]["toma"], color=VIOLETA, tam=14, paso=26)
    for i, q in enumerate(p):                                 # de la obra bajan hebras violetas
        H.trazo(spline([(690, 172), (700 + i * 6, 260 + i * 10), (q[0] - 4, q[1])]), VIOLETA, 0.7, 0.85)
    X.hilo(H, [(690, 176), (700, 300), (760, 420), (c[0], arr[1] + 6)], 5, 2.5)

    # Tihuanacu (Posnansky): arriba a la derecha
    losa(H, 1330, 230, 190)
    titulo_fuente(H, 1230, 104, "Tihuanacu", F["Tihuanacu"]["autor"], tam=26)
    no_se_toma(H, F["Tihuanacu"]["no"], 1440, 74, desde=(1380, 160))
    p = lista(H, 1530, 390, F["Tihuanacu"]["toma"], "end")
    hebras(H, p, (der[0], der[1] - 30), (1060, 470))

    # Afrography: a la izquierda, al medio
    taburete(H, 150, 700, 150)
    titulo_fuente(H, 280, 620, "Afrography", F["Afrography"]["autor"])
    no_se_toma(H, F["Afrography"]["no"], 300, 684, desde=(232, 700))
    p = lista(H, 70, 830, F["Afrography"]["toma"])
    hebras(H, p, (izq[0], izq[1] + 30), (560, 720))

    # La iconografía Tiwanaku (Agüero, Uribe y Berenguer): a la derecha, al medio
    for x in (1290, 1366, 1442):
        H.trazo([(x, 700), (x, 850)], GRAFITO2, 0.5, guiones="4 4")
    for y in (710, 840):
        H.trazo([(1270, y), (1460, y)], GRAFITO2, 0.5, guiones="4 4")
    cuerpo(H, "¿", 1328, 780, 0.24, TINTA)
    cuerpo(H, "?", 1404, 780, 0.24, TINTA)
    titulo_fuente(H, 1530, 592, "La iconografía Tiwanaku", F["La iconografía Tiwanaku"]["autor"], "end", tam=24)
    no_se_toma(H, F["La iconografía Tiwanaku"]["no"], 1530, 656, "end", desde=(1462, 712))
    p = lista(H, 1530, 900, F["La iconografía Tiwanaku"]["toma"], "end")
    hebras(H, p, (der[0], der[1] + 30), (1060, 720))

    # Manuaje (Cárcamo): abajo a la izquierda
    lapiz(H, 470, 1110, 200, 18, -18)
    titulo_fuente(H, 560, 1010, "Manuaje", F["Manuaje"]["autor"])
    no_se_toma(H, F["Manuaje"]["no"], 620, 1096, desde=(566, 1084))
    p = lista(H, 70, 1010, F["Manuaje"]["toma"])
    hebras(H, p, (c[0] - 70, c[1] + 96), (600, 860))

    # Forest and Philosophy (Johnson): abajo a la derecha
    tronco(H, 1060, 1100, 72)
    titulo_fuente(H, 980, 1000, "Forest and Philosophy", F["Forest and Philosophy"]["autor"], "end", tam=24)
    no_se_toma(H, F["Forest and Philosophy"]["no"], 1160, 1160, desde=(1110, 1140))
    p = lista(H, 1530, 1010, F["Forest and Philosophy"]["toma"], "end")
    hebras(H, p, (c[0] + 70, c[1] + 96), (1000, 860))

    # la leyenda
    lx, ly = 620, 1196
    H.trazo([(lx, ly), (lx + 40, ly)], TINTA, 1.0)
    H.maquina(lx + 54, ly + 4, "continuo: se toma", 12.5, TINTA, halo=False)
    H.trazo([(lx, ly + 24), (lx + 36, ly + 24)], GRAFITO, 0.7)
    H.trazo([(lx + 38, ly + 18), (lx + 38, ly + 30)], GRAFITO, 1.1, temblor=0.05, deriva=0)
    H.maquina(lx + 54, ly + 28, "corte: no se toma", 12.5, TINTA, halo=False)
    dd, _ = H.mancha(lx + 20, ly + 47, 20, 6, 0.1, 7)
    H.aguada(dd, VIOLETA, 0.6, desplaza=4, capas=1)
    H.maquina(lx + 54, ly + 52, "violeta: la obra", 12.5, TINTA, halo=False)
    X.pie_de_mapa(H, 2, "Teoría y fuentes")
    return H


# ------------------------------------------------------------------ mapa 3: la obra, decisión por decisión

CADENA = ["piedra borrada", "fotografía vieja", "dibujo reconstructivo", "escaneo", "repujado en aluminio", "cuerpo",
          "video", "charco", "pared de azulejo"]
DECISIONES = [
    # número, lo que hizo la obra, lo que hace la letra, eslabón de la cadena del que sale, pictograma
    ("D1", "Lámina, no piedra", "las letras salen del pie de la lámina", 1, "pie"),
    ("D2", "Del asperón al aluminio", "aluminio repujado; solo caja baja", 4, "placa"),
    ("D3", "Placas sueltas, con piel entre ellas", "cada letra, un tipo móvil; entre palabras, la piel", 5, "placas"),
    ("D4", "Puertas en el pecho y la espalda", "la tapa de la caja: una puerta sobre la celda 1", 5, "tapa"),
    ("D5", "La iconografía, interpretada", "del monolito, solo la retícula y la celda vacía", 2, "reticula"),
    ("D6", "La piscina vacía", "fondo, borde, desagüe; el violeta del esténcil", 8, "piscina"),
    ("D7", "Placas en el fondo, como peces", "no se dibujan peces: las letras ya lo parecen", 7, "fondo"),
    ("D8", "La bandeja con un dedo de agua", "el estado Agua: se lee reflejada", 7, "bandeja"),
    ("D9", "Escenario, pantalla y tema", "la pared frotada es el papel del calco", 6, "pared"),
    ("D10", "El bucle", "frotar hasta que no se lea, y repujar otra", 6, "frotado"),
    ("D11", "Moverse como la piedra: apenas", "el temblor de la mano; tres planos a 1,6°", 5, "temblor"),
    ("D12", "Ojos y boca tapados con cinta", "el estado Cinta; el punto de cinta", 5, "cinta"),
    ("D13", "De la boca sale una placa", "el signo final ¶, hecho con los dedos", 5, "pulgar"),
    ("D14", "Un canto que no se entiende", "el estado Voz: la voz deforma, no se graba", 6, "voz"),
    ("D15", "Tocar el agua deforma la imagen", "el agua tocada; en lo digital, tocar deforma", 7, "ondas"),
    ("D16", "El líquido que chorrea de la boca", "toda cuenca se abre abajo; solo gotea lo que mira abajo", 7, "gota"),
]


def picto_d(H, tipo, x, y):
    """El pictograma de cada decisión, en unos 70 × 50 px."""
    a = ref("a")
    if tipo == "pie":
        contorno(H, "n", x, y + 4, 0.16, TINTA, 1.1)
        X.gota_que_cae(H, x, y + 30, 3.6)
    elif tipo == "placa":
        X.aluminio(H, x, y, 58, 50, -4)
        X.relieve(H, a, _tr(x, y + 4, 0.12, -4), 1.6, 0.12)
    elif tipo == "placas":
        X.aluminio(H, x - 20, y, 32, 40, -6)
        X.aluminio(H, x + 20, y + 2, 32, 40, 5)
        H.punto(x, y + 1, 2.4, VIOLETA)
    elif tipo in ("tapa", "reticula"):
        for i in range(5):
            for j in range(3):
                H.trazo([(x - 34 + i * 14, y - 18 + j * 14), (x - 20 + i * 14, y - 18 + j * 14)], GRAFITO2, 0.5)
        for i in range(6):
            H.trazo([(x - 34 + i * 14, y - 18), (x - 34 + i * 14, y + 24)], GRAFITO2, 0.5)
        if tipo == "tapa":
            H.add("objetos", f'<rect x="{x - 6}" y="{y - 4}" width="14" height="14" fill="{VIOLETA}" opacity="0.75"/>')
            H.trazo([(x - 40, y - 26), (x + 40, y - 26)], TINTA, 1.4)
        else:
            H.celda(x + 1, y + 3, 12, VIOLETA, 1.0, punteada=True, doble=False)
    elif tipo == "piscina":
        P, _ = piscina(H, x, y + 22, ancho=70, fondo_=40, prof=(8, 14), baldosa=14, agua=True, foco=60, altura=80,
                       distancia=60)
    elif tipo in ("fondo", "bandeja"):
        X.charco(H, x, y + 4, 36, 20, opac=0.55)
        H.trazo([(x - 38, y - 16), (x + 38, y - 16), (x + 38, y + 24), (x - 38, y + 24), (x - 38, y - 16)], GRAFITO, 0.6)
        if tipo == "fondo":
            cuerpo(H, "a", x, y + 6, 0.11, VIOLETA, opac=0.8)
        else:
            X.reflejo(H, a, x, y + 6, 0.11, VIOLETA, 0.6, 5)
    elif tipo == "pared":
        X.frotado(H, a, x, y, 66, 50, 0.1, -4, 0.8)
    elif tipo == "frotado":
        X.frotado(H, a, x, y, 66, 50, 0.1, 5, 0.12)
    elif tipo == "temblor":
        for k in range(3):
            cuerpo(H, "a", x - 10 + k * 10, y + 4 - k * 3, 0.11, LILA if k < 2 else VIOLETA, rot=-4 + k * 4,
                   opac=0.5 + 0.2 * k)
    elif tipo == "cinta":
        X.papel(H, x, y, 70, 46, -3, "#ece8de", grano=0.1)
        X.tira(H, (x - 26, y - 2), (x + 26, y - 4), 12, "#1d1c1a")
    elif tipo == "pulgar":
        X.aluminio(H, x, y, 52, 50, 3)
        H.maquina(x, y + 9, "¶", 24, TINTA, "middle", halo=False)
    elif tipo == "voz":
        X.reflejo(H, a, x, y + 6, 0.12, VIOLETA, 0.55, 16)
    elif tipo == "ondas":
        X.charco(H, x, y, 34, 12, opac=0.4)
        X.ondas(H, x, y, 36, 13, 4)
    elif tipo == "gota":
        contorno(H, "o", x, y + 2, 0.13, TINTA, 1.0)
        X.gota_que_cae(H, x, y + 28, 3.6)
        X.charco(H, x, y + 40, 18, 4, color=VIOLETA, opac=0.5)


def tramo_del_rio(H, k, d, caja):
    """Cada eslabón de la cadena con su materia: cada paso pierde materia y gana luz."""
    x0, y0, x1, y1 = caja
    cid = H.uid("clip")
    H.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
    if k == 0:                                                # piedra borrada
        X.superficie(H, d, "#8f8b84", 0.6, 0.05)
        X.rayado_frotado(H, x0, y0, x1 - x0, y1 - y0, -40, 2.4, opac=0.5, clip=cid)
    elif k == 1:                                              # fotografía vieja
        X.superficie(H, d, "#b9b2a5", 0.55, 0.012)
    elif k == 2:                                              # dibujo reconstructivo
        X.superficie(H, d, "#efece4", 0.12, 0.03)
        lineas = "".join(f'<path d="M{x0},{y} H{x1}"/>' for y in range(int(y0), int(y1), 14)) + \
                 "".join(f'<path d="M{x},{y0} V{y1}"/>' for x in range(int(x0), int(x1), 14))
        H.add("lineas", f'<g clip-path="url(#{cid})" stroke="{GRAFITO2}" stroke-width="0.5" opacity="0.7">{lineas}</g>')
        H.add("lineas", f'<g clip-path="url(#{cid})"><path d="M{x0 + 20},{y0} C{x1},{(y0 + y1) / 2} {x0},{(y0 + y1) / 2} '
                        f'{x1 - 20},{y1}" fill="none" stroke="{TINTA}" stroke-width="0.9"/></g>')
    elif k == 3:                                              # escaneo
        X.superficie(H, d, "#f3f1ec", 0.08, 0.03)
        lineas = "".join(f'<path d="M{x0},{y} H{x1}"/>' for y in range(int(y0), int(y1), 7)) + \
                 "".join(f'<path d="M{x},{y0} V{y1}"/>' for x in range(int(x0), int(x1), 7))
        H.add("lineas", f'<g clip-path="url(#{cid})" stroke="{LILA}" stroke-width="0.5">{lineas}</g>')
        pix = "".join(f'<rect x="{H.rng.randrange(int(x0), int(x1)) // 7 * 7}" y="{H.rng.randrange(int(y0), int(y1)) // 7 * 7}" '
                      f'width="7" height="7"/>' for _ in range(60))
        H.add("lineas", f'<g clip-path="url(#{cid})" fill="{VIOLETA}" opacity="0.35">{pix}</g>')
    elif k == 4:                                              # repujado en aluminio
        X.aluminio_d(H, d, capa="aguadas", arrugas=0.024)
    elif k == 5:                                              # cuerpo: placas sobre la piel, con cinta
        X.superficie(H, d, "#e8e2d6", 0.15, 0.02)
        for j in range(4):
            yy = y0 + (j + 0.6) * (y1 - y0) / 4.4
            xx = (x0 + x1) / 2 + (j % 2 * 2 - 1) * (x1 - x0) * 0.16
            X.aluminio(H, xx, yy, (x1 - x0) * 0.34, (y1 - y0) * 0.16, H.rng.uniform(-12, 12))
        X.tira(H, (x0 + 10, y0 + (y1 - y0) * 0.45), (x1 - 10, y0 + (y1 - y0) * 0.4), 10)
    elif k == 6:                                              # video
        H.aguada(d, VIOLETA, 0.62, desplaza=10, capas=2)
    elif k == 7:                                              # charco
        H.aguada(d, LILA, 0.75, desplaza=10, capas=2)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        X.ondas(H, cx, cy, (x1 - x0) * 0.5, (y1 - y0) * 0.22, 5)
        X.reflejo(H, ref("a"), cx, cy + 8, 0.13, VIOLETA, 0.55, 8)
    elif k == 8:                                              # pared de azulejo
        X.superficie(H, d, "#eeedf1", 0.12, 0.03)
        lineas = "".join(f'<path d="M{x0},{y} H{x1}"/>' for y in range(int(y0), int(y1), 24)) + \
                 "".join(f'<path d="M{x},{y0} V{y1}"/>' for x in range(int(x0), int(x1), 24))
        H.add("lineas", f'<g clip-path="url(#{cid})" stroke="{GRAFITO2}" stroke-width="0.8">{lineas}</g>')
        tejas = "".join(f'<rect x="{H.rng.uniform(x0, x1) // 24 * 24}" y="{H.rng.uniform(y0, y1) // 24 * 24}" width="24" '
                        f'height="24"/>' for _ in range(7))
        H.add("lineas", f'<g clip-path="url(#{cid})" fill="{LILA}" opacity="0.55">{tejas}</g>')


def mapa_3():
    H = Hoja(1200, 1600, 33)
    definir(H, "anoa")
    X.construccion(H, [600], [205, 1490])
    H.mano(60, 64, "La obra, decisión por decisión", 30, TINTA, rot=-1)
    H.trazo([(56, 74), (300, 72), (430, 76)], TINTA, 0.9, pluma=True)
    H.maquina(60, 100, "Contenida · la cadena de desplazamientos", 13, GRAFITO, halo=False)
    # el río: la cadena de desplazamientos, cada tramo con su materia
    base = remuestrear(spline([(360, 130), (430, 300), (450, 560), (390, 850), (310, 1110), (280, 1300), (300, 1440)], 20), 4)
    n = len(base)
    nor = normales(base)
    r = H.ruido(200)
    izq, der = [], []
    for i, ((x, y), (nx, ny)) in enumerate(zip(base, nor)):
        t = i / (n - 1)
        w = (140 - 50 * t) * (1 + 0.12 * r(i * 4)) / 2
        a_, b_ = (x + nx * w, y + ny * w), (x - nx * w, y - ny * w)
        izq.append(a_ if a_[0] < b_[0] else b_)
        der.append(b_ if a_[0] < b_[0] else a_)
    m = len(CADENA)
    cortes_ = [int(k * (n - 1) / m) for k in range(m + 1)]
    puntos = {}
    for k in range(m):
        i0, i1 = cortes_[k], cortes_[k + 1]
        tramo_pts = izq[i0:i1 + 1] + der[i0:i1 + 1][::-1]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in tramo_pts) + "Z"
        xs, ys = [p[0] for p in tramo_pts], [p[1] for p in tramo_pts]
        tramo_del_rio(H, k, d, (min(xs), min(ys), max(xs), max(ys)))
        H.trazo([izq[i0], der[i0]], "#ffffff", 1.2, 0.8, temblor=0.6)       # el corte entre materias
        im = (i0 + i1) // 2
        lx, ly = izq[im]
        H.trazo([(lx - 6, ly), (lx - 40, ly + 2)], TINTA, 0.7)
        H.punto(lx - 6, ly, 2.0, TINTA)
        H.mano(lx - 46, ly + 6, CADENA[k], 19, TINTA, "end", rot=-1.5)
        puntos[k] = [der[i0 + (i1 - i0) * f // 6] for f in range(1, 6)]
    # el borde: aquí estaba el agua
    b = H.trazo([(30, 205), (600, 198), (1170, 210)], VIOLETA, 1.1, deriva=2.5)
    H.mano(40, 196, "borde", 17, VIOLETA, rot=-1)
    H.mano(1160, 198, "aquí estaba el agua", 17, VIOLETA, "end", rot=-1)
    # las decisiones: lo que hizo la obra (tinta) y lo que hace la letra (violeta)
    x_n, x_t, y0, paso = 596, 650, 262, 79
    usados = {}
    for j, (num, obra, letra, k, pic) in enumerate(DECISIONES):
        y = y0 + j * paso
        H.maquina(x_n, y, num, 13, TINTA, "end", peso=700, halo=False)
        H.maquina(x_t, y, obra, 13, TINTA, halo=True)
        for q, l in enumerate(partir(letra, 40)):
            H.maquina(x_t, y + 19 + q * 16, l, 12, VIOLETA, halo=True)
        picto_d(H, pic, 1112, y + 6)
        u = usados.get(k, 0)
        usados[k] = u + 1
        ox, oy = puntos[k][u % 5]
        H.trazo(bezier((ox + 4, oy), (ox + 90, oy), (x_n - 120, y - 4), (x_n - 44, y - 4), 50),
                VIOLETA if k >= 5 else GRAFITO, 0.6, 0.8, temblor=0.2, deriva=0.5)
        H.punto(ox + 4, oy, 2.0, VIOLETA if k >= 5 else TINTA)
    # la leyenda
    lx, ly = 760, 1540
    dd, _ = H.mancha(lx + 18, ly - 4, 18, 6, 0.1, 7)
    H.aguada(dd, GRAFITO2, 0.7, desplaza=3, capas=1)
    H.maquina(lx + 46, ly, "tinta: lo que hizo la obra", 12, TINTA, halo=False)
    dd, _ = H.mancha(lx + 18, ly + 20, 18, 6, 0.1, 7)
    H.aguada(dd, VIOLETA, 0.6, desplaza=3, capas=1)
    H.maquina(lx + 46, ly + 24, "violeta: lo que hace la letra", 12, VIOLETA, halo=False)
    X.pie_de_mapa(H, 3, "La obra, decisión por decisión")
    return H


# ------------------------------------------------------------------ mapa 4: del pie a los 55 signos

FAMILIA = {"o": "oecdbpqóéá0689", "l": "litjfkí1|()47", "n": "nmhuúürvwxyzñ235"}


def familia(s):
    for g, signos in FAMILIA.items():
        if s in signos:
            return g
    return "a"


def generador(H, s, cx, base, e, nombre, de_la_obra, lado_obra):
    """Un generador: la vasija en aguada, con sus cotas; su nombre; y la fuerza de la obra que le da la forma."""
    x0, y0, x1, y1 = caja_signo(s)
    cy = base - (y1 - 320) * e
    aguada_signo(H, s, cx, cy, e, VIOLETA, 0.8)
    contorno(H, s, cx, cy, e, VIOLETA, 0.5, opac=0.5)
    P = lambda x, y: en_hoja(x, y, cx, cy, e)   # noqa: E731
    izq = P(x0, y1)[0]
    xs = izq - 24 - (24 + len(f"· {nombre}") * 8.4)            # el nombre, a la izquierda del pie de la letra
    H.mano(xs, base - 2, s, 34, VIOLETA, rot=0)
    H.maquina(xs + 24, base - 4, f"· {nombre}", 14, TINTA, halo=False)
    # la fuerza de la obra: a mano, con una flecha que llega a la letra
    tx, ty, ancla, destino = de_la_obra
    H.mano(tx, ty, lado_obra, 21, TINTA, ancla, rot=-2)
    H.flecha([(tx + (40 if ancla == "start" else -40), ty + 10), ((tx + destino[0]) / 2, ty + 40), destino], TINTA, 0.8)
    return P, cy


def nota(H, x, y, lineas, punto=None, ancla="start", color=TINTA, tam=12.5):
    """Notas a máquina con una línea de referencia que toca la letra."""
    if punto:
        ancho = len(lineas[0]) * tam * 0.6
        derecha = x + ancho if ancla == "start" else x
        izquierda = x if ancla == "start" else x - ancho
        sale = (derecha + 6, y - 4) if punto[0] > derecha else (izquierda - 6, y - 4)
        H.trazo([sale, punto], GRAFITO, 0.6, temblor=0.1, deriva=0)
        H.punto(punto[0], punto[1], 1.8, GRAFITO)
    for i, l in enumerate(lineas):
        H.maquina(x, y + i * tam * 1.45, l, tam, color, ancla)


def fila_de_signos(H, signos, cx, y, paso=27.0):
    """La familia de un generador, en fila: tinta lo hallado, violeta lo reconstruido."""
    estado = {c["signo"]: c["estado"] for c in CAJA["celdas"]}
    x = cx - paso * (len(signos) - 1) / 2
    pos = []
    for s in signos:
        color = TINTA if estado.get(s) == "hallada" else VIOLETA
        cuerpo(H, s, x, y, 0.06 if s.isdigit() else 0.085, color)
        pos.append((x, y))
        x += paso
    return pos


def mapa_4():
    H = Hoja(1200, 1600, 44)
    signos = [c["signo"] for c in CAJA["celdas"] if c["signo"] in C_ACTUAL["signos"]]
    definir(H, "olna" + "".join(signos))
    X.construccion(H, [96, 600, 1104], [210, 610, 1000])
    e = 0.72

    # el pie, a máquina, en su tira; la cota de x y 1,71 x
    X.papel(H, 548, 104, 820, 122, -0.6)
    for i, l in enumerate(PIE):
        H.maquina(170, 74 + i * 19, l, 11.2, GRAFITO, halo=False, rot=-0.6)
    x0 = 1010
    for (ya, yb, t) in ((86, 122, "x"), (60, 122, "1,71 × x")):
        xx = x0 + (0 if t == "x" else 26)
        H.trazo([(xx, ya), (xx, yb)], VIOLETA, 0.9, temblor=0.1, deriva=0)
        for yy in (ya, yb):
            H.trazo([(xx - 6, yy), (xx + 6, yy)], VIOLETA, 0.9, temblor=0.05, deriva=0)
    H.mano(x0 + 38, 98, "1,71 × x", 20, VIOLETA, rot=0)
    H.maquina(600, 206, "del pie: las medidas  /  del soporte: la forma", 14, TINTA, "middle", halo=True)
    H.eje(600, 218, 600, 1012, GRAFITO, 0.6, marcas=(0.5,))
    H.flecha([(560, 216), (420, 236), (330, 300)], TINTA, 0.7)
    H.flecha([(640, 216), (780, 232), (872, 250)], TINTA, 0.7)
    H.sobre([(612, 640), (614, 940)], "20 parámetros y la altura de x", 13, GRAFITO, dy=-3)

    # o · la cuenca
    P, _ = generador(H, "o", 300, 520, e, "la cuenca", (60, 300, "start", (196, 380)), "vasija abierta → cuenca")
    cota(H, P(186, 201), P(414, 201), "trapecio 0,70", -1, 14)
    cota(H, P(186, 330), P(222, 330), "", 1, 0)
    H.maquina(P(186, 330)[0] - 8, P(186, 330)[1] + 4, "canal 8,9 mm", 12, TINTA, "end")
    nota(H, 440, 420, ["pared 0,55", "desagüe 3 mm", "radio de chapa 5,3 mm"], P(410, 360))
    gx, gy = P(300, 432)
    X.gota_que_cae(H, gx, gy + 18, 6)

    # l · el fuste
    P, _ = generador(H, "l", 880, 520, e, "el fuste", (1140, 260, "end", (900, 300)), "punzón → fuste")
    cota(H, P(282, 54), P(318, 54), "", -1, 10)
    H.maquina(P(300, 54)[0], P(300, 54)[1] - 18, "facetas 3 · quiebre 1,6°", 12, TINTA, "middle")
    nota(H, 960, 330, ["tres planos"], P(318, 200))
    nota(H, 960, 440, ["asiento 17,8 × 8 mm", "intemperie 1,1 mm"], P(322, 422))

    # n · el hombro
    P, _ = generador(H, "n", 300, 900, e, "el hombro", (60, 690, "start", (210, 760)), "la chapa sobre el cuerpo → hombro")
    cota(H, P(211, 212), P(389, 212), "hombro 3 · caída 0,40", -1, 14)
    nota(H, 124, 772, ["alivio 2,5 mm"], P(250, 262), ancla="start")

    # a · el gancho y la gota
    P, _ = generador(H, "a", 880, 900, e, "el gancho y la gota", (1150, 680, "end", (960, 740)), "gravedad → gota")
    cota(H, P(278, 214), P(363, 214), "gota 11,1 mm", -1, 14)
    gx, gy = P(286, 232)
    H.trazo([(gx - 30, gy + 4), (gx, gy)], GRAFITO, 0.6, temblor=0.05, deriva=0)
    H.trazo(elipse_pts(gx, gy, 18, 18, 0, math.radians(150), math.radians(255)), TINTA, 0.7)
    H.maquina(gx - 32, gy - 14, "gancho 105°", 12, TINTA, "end")
    nota(H, 1000, 800, ["cuello 4,9 mm", "sifón 0,6", "cinta y punto 8,9 mm"], P(384, 330))
    gx, gy = P(299, 432)
    X.gota_que_cae(H, gx, gy + 18, 6)

    # las familias: de cada vasija bajan sus signos
    fams = {g: [s for s in signos if familia(s) == g] for g in "olna"}
    filas = {"o": (300, 600), "l": (880, 600), "n": (300, 984), "a": (880, 984)}
    for g, (fx, fy) in filas.items():
        pos = fila_de_signos(H, fams[g], fx, fy)
        for k in (0, len(pos) // 2, len(pos) - 1):              # del generador a su familia
            H.flecha([(fx + (k - len(pos) // 2) * 12, fy - 52), (pos[k][0], fy - 24)], VIOLETA, 0.7, punteado=True)
        izq = g in "on"
        H.maquina(fx + (-1 if izq else 1) * (len(pos) * 13.5 + 16), fy + 6, str(len(pos)), 12, GRAFITO,
                  "end" if izq else "start", halo=False)
    # y bajan a la caja, como peces al fondo (D7)
    lado = 46
    gx, gy = 600 - 4 * lado, 1040
    for (sx, sy), (mx, my), (dx, dy) in (((470, 620), (560, 700), (560, gy - 6)), ((720, 620), (640, 700), (640, gy - 6)),
                                         ((470, 1004), (500, 1020), (520, gy - 6)),
                                         ((720, 1004), (700, 1020), (680, gy - 6))):
        H.flecha([(sx, sy), (mx, my), (dx, dy)], VIOLETA, 0.7)

    # la caja de 8 × 7
    for i in range(9):
        H.trazo([(gx + i * lado, gy), (gx + i * lado, gy + 7 * lado)], TINTA, 0.7, temblor=0.2, deriva=0.4)
    for j in range(8):
        H.trazo([(gx, gy + j * lado), (gx + 8 * lado, gy + j * lado)], TINTA, 0.7, temblor=0.2, deriva=0.4)
    for c in CAJA["celdas"]:
        x = gx + (c["columna"] - 0.5) * lado
        y = gy + (c["fila"] - 0.5) * lado
        if c["signo"] in C_ACTUAL["signos"]:
            cuerpo(H, c["signo"], x, y + 2, 0.066, TINTA if c["estado"] == "hallada" else VIOLETA)
        else:
            H.maquina(x, y + 7, c["signo"], 20, GRAFITO, "middle", halo=False)
    xr = gx + 8 * lado + 26
    H.maquina(xr, gy + 24, "30 hallados", 14, TINTA, halo=False)
    H.maquina(xr, gy + 48, "25 reconstruidos", 14, VIOLETA, halo=False)
    H.maquina(xr, gy + 72, "1 signo manual: ¶", 14, GRAFITO, halo=False)
    H.trazo([(xr, gy + 96), (xr + 190, gy + 95)], TINTA, 0.6)
    H.maquina(xr, gy + 122, "55 signos + ¶ =", 14, TINTA, halo=False)
    H.maquina(xr, gy + 144, "56 posiciones", 14, TINTA, halo=False)
    H.maquina(gx - 22, gy + 24, "caja 8 × 7", 14, TINTA, "end", halo=False)
    H.maquina(gx - 22, gy + 46, "como peces,", 12, GRAFITO, "end", halo=False)
    H.maquina(gx - 22, gy + 64, "al fondo (D7)", 12, GRAFITO, "end", halo=False)

    X.pie_de_mapa(H, 4, "Del pie a los 55 signos")
    H.maquina(1140, 1566, "medidas de referencia · la propuesta de la máquina", 12, GRAFITO, "end", halo=False)
    return H


# ------------------------------------------------------------------ mapa 5: la cadena de estados

def fichas_simuladas():
    return json.loads((TIPO / "simulacion" / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))


def promedios_frotado():
    """Las frotadas legibles, en promedio, de las halladas y de las reconstruidas (primera placa de cada celda)."""
    F = [v for v in fichas_simuladas().values() if v["variante"] == 1]
    out = {}
    for e in ("hallada", "reconstruida"):
        n = [v["frotado"]["legibles"] for v in F if v["estado"] == e]
        out[e] = sum(n) / len(n)
    return out


def coma(v):
    return f"{v:.1f}".replace(".", ",")


def mapa_5():
    H = Hoja(1200, 1600, 55)
    definir(H, "añ")
    a = ref("a")
    X.construccion(H, [128, 600, 1072], [150, 1040])
    prom = promedios_frotado()
    F = fichas_simuladas()
    roturas = sum(v["placa_"]["roturas"] for v in F.values())

    # el pie: una tira de dos celdas, el registro y la letra
    X.papel(H, 600, 108, 340, 72, -1.2)
    H.maquina(452, 100, "el pie", 13, TINTA, halo=False)
    H.maquina(452, 120, "registro · 01", 12, VIOLETA, halo=False)
    H.trazo([(636, 76), (638, 140)], GRAFITO2, 0.6, temblor=0.2)
    contorno(H, "a", 706, 118, 0.15, TINTA, 1.0)

    # el calco
    X.calco(H, 476, 330, 236, 200, -4)
    contorno(H, "a", 454, 346, 0.34, TINTA, 1.1, rot=-4)
    contorno(H, "ñ", 548, 360, 0.2, VIOLETA, 1.5, punteado=True, rot=-4)
    X.rotulo(H, 96, 290, "Calco", ["acción 3", "continuo: hallado", "punteado: reconstruido"], mayus=True,
             verso=["«No se salvó la piedra,", " solo la opinión", " sobre ella.»"])

    # la placa
    X.aluminio(H, 790, 520, 200, 236, 7, rota=True)
    X.relieve(H, a, _tr(790, 536, 0.36, 7), 2.8, 0.36)
    X.rotulo(H, 930, 316, "Placa", ["acción 4", "punzón de bola de 1 mm,", "por el reverso", f"119 placas · {roturas} roturas"],
             mayus=True, verso=["«de la boca sale un signo", " hecho con las manos»"])

    # la cinta
    X.cinta_letra(H, 480, 676, 1.25, -4)
    X.rotulo(H, 96, 620, "Cinta", ["acción 6", "masking sobre plástico", "negro: no curva,", "se pliega"], mayus=True,
             verso=["«A la boca la taparon,", " a las manos no,»"])

    # el frotado: la primera y una de las últimas que se leen
    X.frotado(H, a, 470, 912, 176, 196, 0.34, -3, 1.0)
    X.frotado(H, a, 680, 902, 176, 196, 0.34, 4, 0.12)
    H.maquina(470, 1032, "frotada 1", 11, GRAFITO, "middle", halo=False)
    H.maquina(680, 1022, "de las últimas que se leen", 11, GRAFITO, "middle", halo=False)
    X.rotulo(H, 96, 860, "Frotado", ["acción 8", "cada frotada aplasta", "legibles, en promedio:",
                                     f"hallados {coma(prom['hallada'])}", f"reconstruidos {coma(prom['reconstruida'])}"],
             mayus=True, verso=["«Es lo que hacemos", " con todo, no?»"])
    xx, yy = 790, 980                                         # el bucle: frotar hasta que no se lea, y repujar otra
    for k, t in enumerate(("frotar", "borrar", "repujar otra")):
        H.maquina(xx, yy, t, 11.5, VIOLETA, halo=False)
        xx += len(t) * 6.9 + 6
        if k < 2:
            H.flecha([(xx, yy - 4), (xx + 26, yy - 4)], VIOLETA, 0.8, curva=False)
            xx += 34

    # la piscina: el agua y la voz
    P, z = piscina(H, 600, 1480, ancho=800, fondo_=600, prof=(110, 200), baldosa=50, agua=False, foco=500, altura=800,
                   distancia=500)

    def piso(Xx, Y):
        return P(Xx, Y, z(Y))
    ax, ay = piso(-130, 300)
    vx, vy = piso(170, 330)
    X.charco(H, (ax + vx) / 2, (ay + vy) / 2 + 4, 300, 70, opac=0.36)
    X.charco(H, ax, ay, 140, 40, opac=0.4)
    X.reflejo(H, a, ax + 4, ay + 6, 0.26, VIOLETA, 0.5, 6)
    X.ondas(H, ax, ay, 150, 40, 6)
    X.reflejo(H, a, vx + 4, vy + 6, 0.24, VIOLETA, 0.4, 18)
    X.ondas(H, vx, vy, 120, 32, 4, opac=0.6)
    X.gota_que_cae(H, ax, ay - 40, 6)
    X.rotulo(H, 64, 1150, "Agua", ["acción 9", "tocar deforma"], mayus=True,
             verso=["«Tocas el agua y", " la diosa se deforma.»"])
    X.rotulo(H, 1140, 1150, "Voz", ["acción 10", "la voz deforma;", "no se graba"], ancla="end", mayus=True,
             verso=["«ninguna palabra»"])

    # el hilo de tinta: de un estado al siguiente
    X.hilo(H, [(600, 146), (586, 190), (540, 236)], 5, 3)
    X.hilo(H, [(590, 372), (640, 408), (700, 420)], 5, 3)
    X.hilo(H, [(760, 642), (700, 640), (600, 610), (560, 600)], 5, 3)
    X.hilo(H, [(480, 762), (486, 790), (476, 812)], 4, 3)
    X.hilo(H, [(560, 1004), (566, 1060), (ax + 30, ay - 120), (ax, ay - 56)], 6, 3, gotas=(1.0,))

    # generación 2: el esténcil vuelve a ser placa
    H.flecha([(vx + 126, vy - 6), (1010, 1110), (1060, 900), (1010, 720), (905, 600)], VIOLETA, 1.1, punteado=True)
    H.maquinas(1040, 800, ["generación 2 ·", "volver a ser", "placa"], 11.5, VIOLETA)

    X.pie_de_mapa(H, 5, "La cadena de estados")
    H.maquina(1140, 1566, "estados, no pesos.", 12.5, GRAFITO, "end", halo=False)
    return H


# ------------------------------------------------------------------ mapa 6: retórica y poética

def picto(H, tipo, x, y):
    """Los pictogramas de las figuras, a mano, en unos 60 px."""
    if tipo == "anáfora":                                     # olas que se repiten y varían
        for k, amp in enumerate((8, 6, 4)):
            H.trazo([(x - 30 + i * 2, y - 14 + k * 13 + amp * math.sin(i * 0.5 + k)) for i in range(31)], VIOLETA, 1.1)
    elif tipo == "paradoja":                                  # una vasija abierta abajo, que gotea
        pts = elipse_pts(x, y - 6, 24, 18, 0, math.pi * 0.6, math.pi * 2.4)
        H.trazo(pts, TINTA, 1.1)
        X.charco(H, x, y + 2, 20, 6, opac=0.6)
        X.gota_que_cae(H, x, y + 30, 4.5)
    elif tipo == "derivación":                                # una raíz que se abre
        H.trazo([(x, y - 30), (x, y - 4)], TINTA, 1.0)
        for dx, dy in ((-28, 26), (-12, 32), (6, 32), (24, 28)):
            H.curva([(x, y - 4), (x + dx * 0.5, y + dy * 0.4), (x + dx, y + dy)], color=TINTA, ancho=0.7)
        H.trazo([(x - 34, y - 4), (x + 34, y - 2)], GRAFITO, 0.6)
    elif tipo == "apóstrofe":                                 # ondas desde un punto: tocas el agua
        X.ondas(H, x, y, 30, 15, 3, opac=0.9)
        H.punto(x, y, 3, VIOLETA)
    elif tipo == "prosopopeya":                               # la tierra que bebe
        d = f"M{x - 32},{y + 16} Q{x},{y - 30} {x + 32},{y + 16} Z"
        H.rayado(d, (x - 32, y - 14, x + 32, y + 16), -40, 2.6, GRAFITO, 0.7, 0.9)
        H.trazo([(x - 34, y + 16), (x + 34, y + 16)], TINTA, 0.8)
        X.gota_que_cae(H, x, y - 24, 4)
    elif tipo == "ciclo":                                     # dos vueltas: termina y empieza
        H.orbita(x - 12, y, 18, 14, 0, hueco=30, color=VIOLETA, ancho=1.0, pasadas=1, sentido=0.5)
        H.orbita(x + 14, y, 18, 14, 0, hueco=30, color=VIOLETA, ancho=1.0, pasadas=1, punteado=True, sentido=0.5)
    elif tipo == "antítesis":                                 # escrito, continuo; hablado, punteado
        H.trazo([(x - 30, y - 6), (x + 30, y - 6)], TINTA, 1.6)
        H.trazo([(x - 30, y + 8), (x + 30, y + 8)], VIOLETA, 1.4, punteado=True)
    elif tipo == "metáfora":                                  # la letra es una vasija: agua en la cuenca
        X.charco(H, x, y + 6, 20, 9, opac=0.7)
        contorno(H, "o", x, y + 4, 0.15, TINTA, 1.0)
    elif tipo == "sinécdoque":                                # la cinta por el rostro tapado
        X.tira(H, (x - 30, y - 4), (x + 30, y - 8), 14)
    elif tipo == "elipsis":                                   # la celda vacía
        H.celda(x, y, 34, VIOLETA, 1.0, punteada=True, doble=False)
    elif tipo == "etimología":                                # boca, ojo, puerta
        contorno(H, "o", x - 22, y + 4, 0.09, TINTA, 0.9)
        cuerpo(H, "l", x, y + 4, 0.09, VIOLETA)
        contorno(H, "n", x + 22, y + 4, 0.09, TINTA, 0.9)
    elif tipo == "sentencia":                                 # una mancha de grafito: afirmar
        cid = H.uid("clip")
        d, _ = H.mancha(x, y, 30, 9, 0.2, 8, -6)
        H.defs.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>')
        X.rayado_frotado(H, x - 34, y - 12, 68, 24, -10, 1.3, opac=0.7, capa="grafito", clip=cid)
    elif tipo == "interrogación":                             # una ? que no espera
        cuerpo(H, "?", x, y + 4, 0.12, TINTA)


FIGURAS = [
    # figura, pictograma, glosa, lo que hace la letra, verso que la lleva, lado
    ("metáfora", "metáfora", "letra como vasija", "fondo, borde, desagüe", "Quedó el contenedor", -1),
    ("anáfora y gradación", "anáfora", "repetir y variar", "el temblor: tres planos a 1,6°",
     "es decir, apenas, es decir, temblor,", 1),
    ("apóstrofe", "apóstrofe", "tocar a quien mira", "tocar deforma el espécimen", "Tocas el agua y la diosa se deforma.", -1),
    ("sentencia", "sentencia", "afirmar", "de la piscina no se saca nada", "Todos los archivos funcionan así.", 1),
    ("derivación", "derivación", "enterrar / desenterrar", "el nombre no es Kochamama", "A la ídolo la desenterraron,", -1),
    ("interrogación retórica", "interrogación", "preguntar sin esperar", "la ¿ no es el espejo de la ?",
     "Es lo que hacemos con todo, no?", 1),
    ("prosopopeya", "prosopopeya", "la tierra bebe", "solo gotea lo que mira abajo", "La tierra se dio de beber a sí misma", -1),
    ("paradoja", "paradoja", "abrir lo que contiene", "toda cuenca se abre abajo",
     "y ningún contenedor aguanta lo que contiene.", 1),
    ("repetición y ciclo", "ciclo", "volver con diferencia", "frotar y repujar otra", "Termina y empieza,", -1),
    ("etimología", "etimología", "boca · ojo · puerta", "la puerta sobre la celda 1; el ¶", "de la boca sale un signo", -1),
    ("elipsis", "elipsis", "hacer visible el vacío", "la celda vacía: lo que no cabe", "ninguna palabra,", 1),
    ("antítesis", "antítesis", "escrito / hablado", "continuo y punteado, en todos los estados",
     "Y es que lo que vuelve, vuelve escrito;", 1),
    ("sinécdoque y metonimia", "sinécdoque", "parte / cuerpo", "el pie por la lámina; la cinta por el rostro",
     "A la boca la taparon, a las manos no,", -1),
]


def repartir(objetivos, minimo, arriba, abajo):
    """Pone cada rótulo cerca de su verso sin que se monten: de arriba abajo y, si no entra, de abajo arriba."""
    ys = []
    for y in objetivos:
        ys.append(max(y, (ys[-1] + minimo) if ys else arriba))
    exceso = ys[-1] - abajo
    if exceso > 0:
        ys[-1] -= exceso
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - minimo)
    return ys


def mapa_6():
    H = Hoja(1200, 1600, 66)
    definir(H, "?oln")
    versos = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8").split("\n")
    X.construccion(H, [96, 600, 1104], [120, 1380])
    tam, inter, hueco, x_v = 13.5, 23, 17, 452
    # el agua: una columna que baja y gotea; arriba, la mancha donde empieza
    y = 150
    pos = {}
    for v in versos:
        if not v.strip():
            y += hueco
            continue
        pos[v.strip()] = y
        y += inter
    y_fin = y
    r = H.ruido(220)
    izq = [(x_v - 34 - 46 * abs(r(t * 1.3)) - 22 * math.sin(t / 60), t) for t in range(110, int(y_fin) + 20, 26)]
    der = [(x_v + 370 + 60 * abs(r(t * 1.3 + 77)) + 24 * math.sin(t / 47), t) for t in range(110, int(y_fin) + 20, 26)]
    columna = d_suave(spline(izq + [(x_v + 175, y_fin + 64)] + der[::-1] + [(x_v + 175, 80)], 6, True), True)
    H.aguada(columna, LILA, 0.3, desplaza=30, capas=2, borde=0.75)
    d, _ = H.mancha(x_v + 120, 112, 46, 16, 0.25, 9)
    H.aguada(d, VIOLETA, 0.7, desplaza=8, capas=2)
    H.trazo([(x_v + 175, y_fin + 70), (x_v + 175, y_fin + 96)], VIOLETA, 1.1, punteado=True)
    X.gota_que_cae(H, x_v + 175, y_fin + 120, 7)
    operan = {f[4] for f in FIGURAS}
    for v, yy in pos.items():
        H.maquina(x_v, yy, v, tam, VIOLETA if v in operan else TINTA, halo=False)
    # los tres verbos, en los márgenes
    H.add("textos", f'<text x="64" y="330" font-family="La Belle Aurore" font-size="44" fill="{TINTA}" '
                    f'transform="rotate(-90 64 330)" letter-spacing="4">ENTERRAR</text>')
    H.eje(78, 60, 78, 470, TINTA, 0.6)
    H.add("textos", f'<text x="1148" y="560" font-family="La Belle Aurore" font-size="44" fill="{TINTA}" '
                    f'transform="rotate(90 1148 560)" letter-spacing="4">CONTENER</text>')
    H.eje(1134, 470, 1134, 1010, TINTA, 0.6)
    H.mano(1150, 1420, "DESENTERRAR", 44, TINTA, "end", rot=0)
    H.flecha([(x_v + 340, y_fin - 30), (900, y_fin + 40), (880, 1380)], TINTA, 0.8)
    # las figuras, a cada lado, cerca de su verso
    for lado in (-1, 1):
        figs = sorted([f for f in FIGURAS if f[5] == lado], key=lambda f: pos[f[4]])
        ys = repartir([pos[f[4]] - 30 for f in figs], 112, 150 if lado < 0 else 200, 1330)
        for (nombre, tipo, glosa, letra, verso, _), yy in zip(figs, ys):
            xt = 168 if lado < 0 else 924
            picto(H, tipo, xt - 52, yy + 4)
            H.mano(xt, yy + 10, nombre, 22, TINTA, rot=-1.2)
            H.maquina(xt, yy + 32, glosa, 12, GRAFITO, halo=False)
            n = 30 if lado < 0 else 26
            for k, l in enumerate(partir("la letra: " + letra, n)):
                H.maquina(xt, yy + 50 + k * 16, l, 11.5, VIOLETA, halo=False)
            vy = pos[verso] - 4
            if lado < 0:
                sx = xt + min(len(nombre) * 9.4, 230) + 8
                ex = x_v - 10
            else:
                sx = xt - 74
                ex = x_v + len(verso) * tam * 0.6 + 10
            H.curva([(sx, yy + 4), ((sx + ex) / 2, (yy + 4 + vy) / 2 + 6 * lado), (ex, vy)], color=GRAFITO, ancho=0.7)
            H.punto(ex, vy, 2.4, VIOLETA)
    X.pie_de_mapa(H, 6, "Retórica y poética")
    H.maquina(1140, 1566, "violeta: los versos que operan", 12, GRAFITO, "end", halo=False)
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
