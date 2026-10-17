"""La materia de los mapas: aluminio, grafito, cinta, calco, papel, agua y tinta.

Los mapas se rehicieron el 17.10.2026 tomando como modelo las versiones mejoradas que
trajo Joaquin: cada estado se dibuja con su material, las notas van a máquina y un hilo
de tinta violeta une las etapas. Aquí no hay fotos: cada material es un filtro de SVG
(ruido, luz rasante, desplazamiento) o un trazo calculado. La luz viene siempre de arriba
a la izquierda, como en la foto de la placa (`simulacion/`).

  - el aluminio: un ruido que se arruga y una luz rasante; la letra, en relieve de
    contorno, porque el punzón repasa el borde (Acción 4);
  - el grafito: un rayado de lápiz, apretado y desparejo; el contorno en relieve sale más oscuro;
  - la cinta: tiras de masking color hueso, con los cortes dentados;
  - el calco: papel translúcido, con un pliegue;
  - el papel: rasgado, con grano y una sombra corta;
  - el agua: aguada lila, ondas y el reflejo que se deforma;
  - la tinta: un hilo violeta que corre y gotea.
"""

import math

from mano import GRAFITO, GRAFITO2, HUESO, LILA, MANO, MAQUINA, PAPEL, TINTA, VIOLETA, d_suave, fmt, normales, \
    remuestrear, spline

LUZ = '<feDistantLight azimuth="225" elevation="{e}"/>'


def _filtro(H, clave, cuerpo, caja="-10% -10% 120% 125%"):
    """Define un filtro una sola vez por hoja y devuelve su id."""
    if not hasattr(H, "_filtros"):
        H._filtros = {}
    if clave not in H._filtros:
        fid = H.uid("f")
        x, y, w, h = caja.split()
        H.defs.append(f'<filter id="{fid}" x="{x}" y="{y}" width="{w}" height="{h}" color-interpolation-filters="sRGB">'
                      f'{cuerpo}</filter>')
        H._filtros[clave] = fid
    return H._filtros[clave]


def _sombra(dx=1.6, dy=2.6, desv=2.4, op=0.22, entrada="SourceAlpha", salida="sombra"):
    return (f'<feGaussianBlur in="{entrada}" stdDeviation="{desv}" result="sb"/>'
            f'<feOffset in="sb" dx="{dx}" dy="{dy}" result="so"/>'
            f'<feFlood flood-color="#2a2622" flood-opacity="{op}"/>'
            f'<feComposite in2="so" operator="in" result="{salida}"/>')


def _gira(cx, cy, rot):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)


def _d(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"


def borde_rasgado(H, w, h, rasgado=(1.0, 1.0, 1.0, 1.0), paso=5.0, amplitud=2.4):
    """El contorno de una hoja rasgada, centrada en 0,0: cada lado con su propio rasgado."""
    r = H.rng
    pts = []
    lados = [((-w / 2, -h / 2), (w / 2, -h / 2)), ((w / 2, -h / 2), (w / 2, h / 2)),
             ((w / 2, h / 2), (-w / 2, h / 2)), ((-w / 2, h / 2), (-w / 2, -h / 2))]
    for (a, b), k in zip(lados, rasgado):
        L = math.dist(a, b)
        n = max(2, int(L / paso))
        nx, ny = (b[1] - a[1]) / L, -(b[0] - a[0]) / L
        deriva = 0.0
        for i in range(n):
            t = i / n
            deriva = deriva * 0.6 + r.uniform(-1, 1) * 0.4
            o = k * amplitud * (deriva + r.uniform(-0.6, 0.6))
            pts.append((a[0] + (b[0] - a[0]) * t + nx * o, a[1] + (b[1] - a[1]) * t + ny * o))
    return pts


# ------------------------------------------------------------------ papel

def papel(H, cx, cy, w, h, rot=0.0, color="#f4f1e8", rasgado=(1, 1, 1, 1), sombra=True, capa="objetos", grano=0.16,
          amplitud=2.4):
    """Una hoja de papel rasgada, con grano y una sombra corta. Devuelve (d, transform)."""
    cuerpo = ('<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="11" result="n"/>'
              '<feColorMatrix in="n" type="saturate" values="0" result="ng"/>'
              f'<feComponentTransfer in="ng" result="nl"><feFuncR type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              f'<feFuncG type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              f'<feFuncB type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              '<feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer>'
              '<feBlend in="SourceGraphic" in2="nl" mode="multiply" result="t"/>'
              '<feComposite in="t" in2="SourceAlpha" operator="in" result="tex"/>'
              + (_sombra() + '<feMerge><feMergeNode in="sombra"/><feMergeNode in="tex"/></feMerge>' if sombra else ""))
    fid = _filtro(H, f"papel{grano}{sombra}", cuerpo)
    d = _d(borde_rasgado(H, w, h, rasgado, amplitud=amplitud))
    tr = f"translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})"
    H.add(capa, f'<g transform="{tr}" filter="url(#{fid})"><path d="{d}" fill="{color}"/></g>')
    return d, tr


# ------------------------------------------------------------------ aluminio

def _filtro_aluminio(H, sem, brillo=1.0, arrugas=0.014, sombra=True):
    cuerpo = (f'<feTurbulence type="turbulence" baseFrequency="{arrugas}" numOctaves="4" seed="{sem}" result="t1"/>'
              f'<feTurbulence type="fractalNoise" baseFrequency="{arrugas * 2.6:.4f}" numOctaves="3" seed="{sem + 5}" result="t2"/>'
              '<feComposite in="t1" in2="t2" operator="arithmetic" k2="0.8" k3="0.3" result="h"/>'
              '<feColorMatrix in="h" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="ha"/>'
              f'<feDiffuseLighting in="ha" surfaceScale="2.6" diffuseConstant="{1.08 * brillo:.2f}" lighting-color="#d3d7da" '
              f'result="dif">{LUZ.format(e=48)}</feDiffuseLighting>'
              '<feSpecularLighting in="ha" surfaceScale="2.6" specularConstant="1.2" specularExponent="30" '
              f'lighting-color="#ffffff" result="esp">{LUZ.format(e=48)}</feSpecularLighting>'
              '<feComposite in="esp" in2="dif" operator="arithmetic" k2="0.6" k3="1" result="m"/>'
              '<feComposite in="m" in2="SourceAlpha" operator="in" result="foil"/>'
              + (_sombra(2.0, 3.2, 3.0, 0.28) + '<feMerge><feMergeNode in="sombra"/><feMergeNode in="foil"/></feMerge>'
                 if sombra else ""))
    return _filtro(H, f"alu{sem}{brillo}{arrugas}{sombra}", cuerpo)


def aluminio_d(H, d, capa="objetos", semilla=None, sombra=False, arrugas=0.02):
    """Papel de aluminio con la forma que se le dé."""
    fid = _filtro_aluminio(H, semilla or H.rng.randint(1, 900), 1.0, arrugas, sombra)
    H.add(capa, f'<g filter="url(#{fid})"><path d="{d}" fill="#888"/></g>')


def superficie(H, d, color, grano=0.3, frecuencia=0.03, capa="aguadas", transform=""):
    """Una superficie con grano: piedra, foto vieja, papel, pared. El ruido oscurece en manchas."""
    cuerpo = (f'<feTurbulence type="fractalNoise" baseFrequency="{frecuencia}" numOctaves="4" seed="17" result="n"/>'
              '<feColorMatrix in="n" type="saturate" values="0" result="ng"/>'
              f'<feComponentTransfer in="ng" result="nl"><feFuncR type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              f'<feFuncG type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              f'<feFuncB type="linear" slope="{grano}" intercept="{1 - grano * 0.7}"/>'
              '<feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer>'
              '<feBlend in="SourceGraphic" in2="nl" mode="multiply" result="t"/>'
              '<feComposite in="t" in2="SourceAlpha" operator="in"/>')
    fid = _filtro(H, f"sup{grano}{frecuencia}", cuerpo)
    tr = f' transform="{transform}"' if transform else ""
    H.add(capa, f'<g filter="url(#{fid})"><path d="{d}"{tr} fill="{color}"/></g>')


def aluminio(H, cx, cy, w, h, rot=0.0, capa="objetos", semilla=None, brillo=1.0, rota=False, arrugas=0.014):
    """Una placa de papel de aluminio: el ruido que se arruga, con luz rasante. Devuelve (d, transform)."""
    sem = semilla or H.rng.randint(1, 900)
    fid = _filtro_aluminio(H, sem, brillo, arrugas)
    pts = borde_rasgado(H, w, h, (0.6, 0.6, 0.6, 0.6), paso=7, amplitud=1.6)
    d = _d(pts)
    tr = f"translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})"
    H.add(capa, f'<g transform="{tr}" filter="url(#{fid})"><path d="{d}" fill="#888"/></g>')
    H.add(capa, f'<path d="{d}" transform="{tr}" fill="none" stroke="#6f7173" stroke-width="0.6" opacity="0.7"/>')
    if rota:                                                   # la placa rota no se corrige: se registra
        g = _gira(cx, cy, rot)
        x0 = w / 2
        grieta = [(x0, -h * 0.05), (x0 - w * 0.08, h * 0.02), (x0 - w * 0.13, -h * 0.03), (x0 - w * 0.2, h * 0.06),
                  (x0 - w * 0.26, h * 0.04)]
        H.trazo([g(x, y) for x, y in grieta], "#2b2b2b", 1.1, 0.85, temblor=0.6, deriva=0.2, capa=capa)
        H.trazo([g(x + 1.2, y + 1.4) for x, y in grieta], "#ffffff", 0.8, 0.7, temblor=0.6, deriva=0.2, capa=capa)
    return d, tr


def relieve(H, ref, transform, ancho=2.4, escala=1.0, capa="objetos", fuerza=1.0, punteado=False):
    """La letra repujada, vista por el anverso: el contorno sube; la luz rasante le hace un lado claro y otro oscuro."""
    cuerpo = ('<feGaussianBlur in="SourceAlpha" stdDeviation="1.5" result="b"/>'
              f'<feDiffuseLighting in="b" surfaceScale="{1.7 * fuerza:.2f}" diffuseConstant="0.78" lighting-color="#ffffff" '
              f'result="l">{LUZ.format(e=40)}</feDiffuseLighting>'
              f'<feSpecularLighting in="b" surfaceScale="{1.7 * fuerza:.2f}" specularConstant="0.8" specularExponent="16" '
              f'lighting-color="#ffffff" result="sp">{LUZ.format(e=40)}</feSpecularLighting>'
              '<feComposite in="sp" in2="l" operator="arithmetic" k2="0.45" k3="1" result="m"/>'
              '<feMorphology in="SourceAlpha" operator="dilate" radius="2.4" result="ma"/>'
              '<feGaussianBlur in="ma" stdDeviation="1.4" result="mb"/>'
              '<feComposite in="m" in2="mb" operator="in"/>')
    fid = _filtro(H, f"relieve{fuerza}", cuerpo, "-15% -15% 130% 130%")
    dash = f' stroke-dasharray="0.1 {2.6 / escala:.2f}" stroke-linecap="round"' if punteado else ""
    H.add(capa, f'<g filter="url(#{fid})" style="mix-blend-mode:hard-light"><use href="#{ref}" transform="{transform}" '
                f'fill="none" stroke="#000" stroke-width="{ancho / escala:.2f}" stroke-linejoin="round"{dash}/></g>')


# ------------------------------------------------------------------ grafito

def rayado_frotado(H, x0, y0, w, h, angulo=-34.0, paso=2.3, color="#4a4844", opac=0.3, ancho=0.65, capa="grafito",
                   clip=None):
    """El grafito del frotado: trazos largos y apretados en una dirección, con la presión que cambia."""
    r = H.rng
    a = math.radians(angulo)
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    cx, cy = x0 + w / 2, y0 + h / 2
    R = math.hypot(w, h) / 2 + 6
    trazos, t = [], -R
    presion = H.ruido(40)
    while t <= R:
        px, py = cx + vx * t, cy + vy * t
        s0 = -R + r.uniform(0, R * 0.3)
        while s0 < R:
            L = r.uniform(R * 0.25, R * 0.9)
            p0 = (px + ux * s0, py + uy * s0)
            p1 = (px + ux * (s0 + L), py + uy * (s0 + L))
            o = opac * max(0.15, 0.6 + 0.5 * presion(t * 3 + s0 * 0.2)) * r.uniform(0.6, 1.1)
            trazos.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" opacity="{min(1, o):.2f}"/>')
            s0 += L + r.uniform(2, 14)
        t += paso * r.uniform(0.7, 1.3)
    if not clip:                                              # sin forma propia, se recorta a su caja
        clip = H.uid("clip")
        H.defs.append(f'<clipPath id="{clip}"><rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath>')
    H.add(capa, f'<g clip-path="url(#{clip})" filter="url(#lapiz)" fill="none" stroke="{color}" stroke-width="{ancho}" '
                f'stroke-linecap="round" style="mix-blend-mode:multiply">{"".join(trazos)}</g>')


def frotado(H, ref, cx, cy, w, h, escala, rot=0.0, legible=1.0, capa="objetos", letra_y=0.0):
    """Una frotada: papel sobre la placa y grafito encima. El contorno en relieve sale más oscuro.
    `legible` baja con cada frotada: el relieve se aplasta."""
    d, tr = papel(H, cx, cy, w, h, rot, "#f3f0e7", capa=capa)
    cid = H.uid("clip")
    H.defs.append(f'<clipPath id="{cid}"><path d="{d}" transform="{tr}"/></clipPath>')
    rayado_frotado(H, cx - w / 2 - 10, cy - h / 2 - 10, w + 20, h + 20, -34 + rot, 2.2, opac=0.34, capa=capa, clip=cid)
    rayado_frotado(H, cx - w / 2 - 10, cy - h / 2 - 10, w + 20, h + 20, -20 + rot, 5.5, opac=0.16, capa=capa, clip=cid)
    t = (f"translate({cx:.1f} {cy + letra_y:.1f}) rotate({rot:.1f}) scale({escala:.4f}) translate(-300 -320)")
    H.add(capa, f'<g filter="url(#lapiz)" opacity="{0.22 + 0.7 * legible:.2f}" style="mix-blend-mode:multiply">'
                f'<use href="#{ref}" transform="{t}" fill="none" stroke="#2c2b29" stroke-width="{(1.4 + 1.6 * legible) / escala:.2f}" '
                f'stroke-linejoin="round"/></g>')
    return d, tr


# ------------------------------------------------------------------ cinta

def tira(H, a, b, ancho=13.0, color="#e7dbb9", capa="objetos", op=0.95):
    """Una tira de cinta de enmascarar de a a b, con los cortes dentados."""
    fid = _filtro(H, "cinta", '<feTurbulence type="fractalNoise" baseFrequency="0.25 0.05" numOctaves="2" seed="5" result="n"/>'
                              '<feColorMatrix in="n" type="saturate" values="0" result="ng"/>'
                              '<feComponentTransfer in="ng" result="nl"><feFuncR type="linear" slope="0.18" intercept="0.86"/>'
                              '<feFuncG type="linear" slope="0.18" intercept="0.86"/><feFuncB type="linear" slope="0.18" '
                              'intercept="0.86"/><feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer>'
                              '<feBlend in="SourceGraphic" in2="nl" mode="multiply" result="t"/>'
                              '<feComposite in="t" in2="SourceAlpha" operator="in" result="tex"/>'
                              + _sombra(0.8, 1.2, 1.0, 0.25) +
                              '<feMerge><feMergeNode in="sombra"/><feMergeNode in="tex"/></feMerge>')
    r = H.rng
    L = math.dist(a, b)
    if L < 1:
        return
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nx, ny = -uy * ancho / 2, ux * ancho / 2
    ext = 3.0                                                   # la tira sobresale un poco del punto
    a2, b2 = (a[0] - ux * ext, a[1] - uy * ext), (b[0] + ux * ext, b[1] + uy * ext)
    dientes = lambda p, s: [(p[0] + nx * t + ux * s * r.uniform(0, 1.6), p[1] + ny * t + uy * s * r.uniform(0, 1.6))  # noqa: E731
                            for t in [1 - 2 * k / 6 for k in range(7)]]
    pts = [(a2[0] + nx, a2[1] + ny), (b2[0] + nx, b2[1] + ny)] + dientes(b2, 1) + \
          [(b2[0] - nx, b2[1] - ny), (a2[0] - nx, a2[1] - ny)] + dientes(a2, -1)[::-1]
    H.add(capa, f'<g filter="url(#{fid})" opacity="{op}"><path d="{_d(pts)}" fill="{color}"/></g>')


TIRAS_A = [((-26, -40), (20, -42)), ((20, -42), (30, -30)), ((28, -32), (28, 46)), ((-28, -40), (-29, -26)),
           ((28, 0), (-18, 2)), ((-18, 2), (-30, 14)), ((-30, 12), (-30, 34)), ((-30, 32), (-18, 46)),
           ((-20, 45), (30, 44))]
TIRAS_N = [((-26, 46), (-24, -36)), ((-26, -30), (14, -36)), ((12, -36), (26, -22)), ((26, -24), (26, 46))]


def cinta_letra(H, cx, cy, escala=1.0, rot=0.0, letra="a", fondo=True, capa="objetos"):
    """La letra de cinta: tiras de masking sobre plástico negro. No curva: se pliega (estado Cinta)."""
    g = _gira(cx, cy, rot)
    e = escala
    if fondo:
        d, tr = papel(H, cx, cy, 120 * e, 130 * e, rot, "#1b1a19", grano=0.08, capa=capa, amplitud=1.4)
    for a, b in (TIRAS_A if letra == "a" else TIRAS_N):
        tira(H, g(a[0] * e, a[1] * e), g(b[0] * e, b[1] * e), 13 * e, capa=capa)


# ------------------------------------------------------------------ calco

def calco(H, cx, cy, w, h, rot=0.0, capa="objetos"):
    """Papel de calco: translúcido, con un pliegue y una esquina que se levanta."""
    fid = _filtro(H, "calco", '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="21" result="n"/>'
                              '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.35 0.45" '
                              'result="nb"/><feComposite in="nb" in2="SourceAlpha" operator="in" result="t"/>'
                              + _sombra(1.0, 1.6, 2.0, 0.12) +
                              '<feMerge><feMergeNode in="sombra"/><feMergeNode in="t"/></feMerge>')
    pts = borde_rasgado(H, w, h, (0.4, 0.3, 0.4, 0.3), paso=9, amplitud=1.2)
    tr = f"translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})"
    H.add(capa, f'<g transform="{tr}" filter="url(#{fid})"><path d="{_d(pts)}" fill="#fff"/></g>')
    H.add(capa, f'<path d="{_d(pts)}" transform="{tr}" fill="none" stroke="#b9b6ae" stroke-width="0.6" opacity="0.8"/>')
    g = _gira(cx, cy, rot)
    H.trazo([g(-w * 0.1, -h / 2), g(w * 0.04, h / 2)], "#cfccc4", 0.7, 0.8, temblor=0.4, capa=capa)   # el pliegue
    esq = [g(w / 2, -h / 2 + 26), g(w / 2 - 24, -h / 2), g(w / 2 - 10, -h / 2 + 12)]
    H.add(capa, f'<path d="{_d(esq)}" fill="#ffffff" opacity="0.8" stroke="#c9c6be" stroke-width="0.5"/>')


# ------------------------------------------------------------------ agua y tinta

def ondas(H, cx, cy, rx, ry, n=5, color=VIOLETA, capa="lineas", opac=0.75, sentido=1.0):
    """Las ondas: elipses que se abren desde un punto, cada vez más tenues."""
    for k in range(1, n + 1):
        f = k / n
        H.orbita(cx, cy, rx * f, ry * f, 0, hueco=8 + 6 * k, color=color, ancho=1.3 - 0.8 * f, pasadas=1,
                 opac=opac * (1.1 - f * 0.8), capa=capa)
        H.orbita(cx, cy - 1.5, rx * f * 0.985, ry * f * 0.94, 0, hueco=30, color="#ffffff", ancho=0.8, pasadas=1,
                 opac=0.55 * (1 - f * 0.6), capa=capa)


def reflejo(H, ref, cx, cy, escala, color=VIOLETA, opac=0.55, fuerza=6.0, capa="objetos", espejo=False):
    """La letra vista a través del agua, temblando; con `espejo`, reflejada: al revés."""
    fid = _filtro(H, f"ondula{fuerza}", '<feTurbulence type="fractalNoise" baseFrequency="0.012 0.09" numOctaves="2" '
                                        f'seed="13" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="{fuerza}" '
                                        'xChannelSelector="R" yChannelSelector="G" result="d"/>'
                                        '<feGaussianBlur in="d" stdDeviation="0.6"/>', "-20% -20% 140% 140%")
    t = f"translate({cx:.1f} {cy:.1f}) scale({escala:.4f} {-escala if espejo else escala:.4f}) translate(-300 -320)"
    H.add(capa, f'<g filter="url(#{fid})" opacity="{opac}" style="mix-blend-mode:multiply"><use href="#{ref}" '
                f'transform="{t}" fill="{color}"/></g>')


def charco(H, cx, cy, rx, ry, capa="aguadas", color=LILA, opac=0.5):
    """Un charco: aguada lila con el borde que se seca más oscuro."""
    d, _ = H.mancha(cx, cy, rx, ry, 0.08, 11)
    H.aguada(d, color, opac, desplaza=9, capa=capa)
    return d


def hilo(H, puntos, ancho0=6.0, ancho1=2.0, color=VIOLETA, halo=True, gotas=(), capa="aguadas", opac=0.72):
    """El hilo de tinta: corre de una etapa a la otra, se ensancha donde se junta y gotea."""
    base = remuestrear(spline(puntos, 16), 4)
    n = len(base)
    nor = normales(base)
    r = H.ruido(70)
    izq, der = [], []
    for i, ((x, y), (nx, ny)) in enumerate(zip(base, nor)):
        t = i / max(1, n - 1)
        w = (ancho0 + (ancho1 - ancho0) * t) * (1 + 0.45 * r(i * 4)) / 2
        izq.append((x + nx * w, y + ny * w))
        der.append((x - nx * w, y - ny * w))
    d = d_suave(izq + der[::-1], True)
    if halo:
        izq2 = [(x + nx * 7, y + ny * 7) for (x, y), (nx, ny) in zip(base, nor)]
        der2 = [(x - nx * 7, y - ny * 7) for (x, y), (nx, ny) in zip(base, nor)]
        H.aguada(d_suave(izq2 + der2[::-1], True), LILA, 0.32, desplaza=12, capas=1, capa=capa)
    H.aguada(d, color, opac, desplaza=2.5, capas=2, borde=0.5, erosion=0.8, capa=capa)
    for k in gotas:
        x, y = base[min(n - 1, int(k * (n - 1)))]
        H.aguada(H.gota(x, y + 9, 3.6), color, 0.85, desplaza=1.2, capas=1, capa=capa)
    return base


def gota_que_cae(H, x, y, r=5.0, color=VIOLETA, capa="aguadas"):
    H.aguada(H.gota(x, y, r), color, 0.9, desplaza=1.4, capas=1, capa=capa)


# ------------------------------------------------------------------ rótulos y construcción

def rotulo(H, x, y, titulo, lineas=(), ancla="start", tam=30, sub=12.5, color_sub=GRAFITO, verso=None, raya=True,
           mayus=False, inter=1.45):
    """Un rótulo: el título a mano, subrayado; debajo, a máquina, lo que hay que saber. El verso, en violeta."""
    t = titulo.upper() if mayus else titulo
    H.mano(x, y, t, tam, TINTA, ancla, rot=-1.0)
    largo = len(t) * tam * (0.5 if mayus else 0.42)
    x0 = x if ancla == "start" else x - largo if ancla == "end" else x - largo / 2
    if raya:
        H.trazo([(x0 - 4, y + 9), (x0 + largo * 0.6, y + 8), (x0 + largo + 10, y + 10)], TINTA, 0.9, pluma=True)
    yy = y + 14 + sub * 1.6
    for l in lineas:
        H.maquina(x, yy, l, sub, color_sub, ancla, halo=True)
        yy += sub * inter
    if verso:
        yy += sub * 0.5
        for l in verso:
            H.maquina(x, yy, l, sub, VIOLETA, ancla, halo=True)
            yy += sub * inter
    return yy


def construccion(H, verticales=(), horizontales=(), color="#cfcabe", ancho=0.5):
    """Las líneas de construcción del dibujo: finas, de lado a lado, con una marca donde se cruzan."""
    for x in verticales:
        H.trazo([(x, 30), (x + H.rng.uniform(-2, 2), H.H - 30)], color, ancho, 0.8, temblor=0.15, deriva=0.6, capa="papel")
    for y in horizontales:
        H.trazo([(30, y), (H.W - 30, y + H.rng.uniform(-2, 2))], color, ancho, 0.8, temblor=0.15, deriva=0.6, capa="papel")
    for x in verticales:
        for y in horizontales:
            H.trazo([(x - 5, y), (x + 5, y)], GRAFITO2, 0.6, 0.8, temblor=0.05, deriva=0, capa="papel")


def pie_de_mapa(H, n, titulo, x=60, y=None, fecha="17.10.2026"):
    """El pie de cada mapa: el número a máquina, el título a mano y, debajo, de dónde es."""
    y = y or H.H - 70
    H.maquina(x, y, f"mapa {n} ·", 15, TINTA, halo=False)
    H.mano(x + 86, y, titulo, 24, TINTA, rot=-0.8)
    w = 86 + len(titulo) * 10.5
    H.trazo([(x - 4, y + 12), (x + w * 0.5, y + 11), (x + w + 10, y + 13)], TINTA, 0.7)
    H.maquina(x, y + 36, f"Contenida · estudio de composición · {fecha}", 12.5, GRAFITO, halo=False)
