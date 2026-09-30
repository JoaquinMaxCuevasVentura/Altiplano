"""Cuaderno 1 · Desenterrar: acciones 1 a 3, simuladas.

Acción 1: una pared de azulejo con juntas torcidas, craquelado, manchas y
desportillados, y su frotado con grafito: el papel sobre el que se calca.
Acción 2: el pie. En la foto de la lámina se lee y se mide, pero no alcanza para
calcar (testigos/, de extraer_testigos.py). El testigo de las formas es el pie
impreso con una letra sustituta y tipos de plomo simulados (tinta que se corre,
tinta que falta, mellas), fotografiado con luz rasante y ampliado en tres
generaciones de fotocopia; para cada signo se elige el testigo mejor conservado.
De la foto se toma una proporción: la altura de x, más baja que la del sustituto.
Acción 3: la escala que decide el pie, y el calco: el contorno del cuerpo de la
gramática, con temblor de mano, abierto en su punto más bajo.
"""

import json
import re

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from comun import (AZULEJO_MM, BASE, CELDAS, FUENTE_TESTIGO, JUNTA_MM, T, TES, azar, caja_tinta, componentes,
                   lineas_pie, ruido, ruido_1d)

PX_IMPRENTA = 40      # px/mm del papel impreso simulado
PX_FOTO = 12          # px/mm de la foto con luz rasante
CUERPO_PT = 8.5       # cuerpo supuesto del pie en el libro
GENERACIONES, FACTOR = 3, 2.5


# ---------------------------------------------------------------- acción 1: la pared y su frotado

def pared(filas, columnas, px, rng):
    """Relieve y color de un paño de azulejos: 1 en el esmalte, 0 en la junta."""
    j = max(2, round(px * JUNTA_MM / AZULEJO_MM))
    H, W = filas * px + (filas + 1) * j, columnas * px + (columnas + 1) * j
    juntas = np.zeros((H, W), np.uint8)
    for i in range(columnas + 1):
        x = i * (px + j) + j / 2 + rng.normal(0, px * 0.004)
        ys = np.arange(H)
        xs = x + ruido_1d(H, H / 5, rng) * px * 0.012
        grosor = max(1, int(round(j * rng.uniform(0.8, 1.3))))
        cv2.polylines(juntas, [np.stack([xs, ys], 1).astype(np.int32)], False, 255, grosor)
    for i in range(filas + 1):
        y = i * (px + j) + j / 2 + rng.normal(0, px * 0.004)
        xs = np.arange(W)
        ys = y + ruido_1d(W, W / 5, rng) * px * 0.012
        grosor = max(1, int(round(j * rng.uniform(0.8, 1.3))))
        cv2.polylines(juntas, [np.stack([xs, ys], 1).astype(np.int32)], False, 255, grosor)
    grietas = np.zeros_like(juntas)
    paso = px / 55
    for f in range(filas):
        for c in range(columnas):
            x0, y0 = j + c * (px + j), j + f * (px + j)
            for _ in range(rng.integers(2, 9)):
                p = np.array([x0 + rng.uniform(0, px), y0 + rng.uniform(0, px)])
                ang = rng.uniform(0, 2 * np.pi)
                pts = [p.copy()]
                for _ in range(rng.integers(15, 70)):
                    ang += rng.normal(0, 0.35)
                    p = p + paso * np.array([np.cos(ang), np.sin(ang)])
                    if not (x0 < p[0] < x0 + px and y0 < p[1] < y0 + px):
                        break
                    pts.append(p.copy())
                if len(pts) > 2:
                    cv2.polylines(grietas, [np.array(pts, np.int32)], False, 255, 1, cv2.LINE_AA)
    chips = np.zeros_like(juntas)
    for f in range(filas + 1):
        for c in range(columnas + 1):
            if rng.random() < 0.09:
                cv2.circle(chips, (int(c * (px + j) + j / 2), int(f * (px + j) + j / 2)),
                           int(px * rng.uniform(0.03, 0.08)), 255, -1)
    fuera = (juntas > 0) | (chips > 0)
    dist = cv2.distanceTransform((~fuera).astype(np.uint8), cv2.DIST_L2, 3)
    relieve = np.clip(dist / (j * 0.9), 0, 1) ** 0.6
    relieve = relieve * (1 - 0.45 * (grietas / 255.0))
    mancha = np.clip((ruido((H, W), px * 0.9, rng) - 1.0) * 0.22, 0, 0.35)
    return dict(relieve=relieve.astype(np.float32), juntas=juntas > 0, grietas=grietas / 255.0,
                mancha=mancha.astype(np.float32), px=px, junta=j, filas=filas, columnas=columnas)


def frotado(p, rng):
    """Grafito frotado sobre papel: se marca lo que sobresale; juntas y grietas quedan blancas."""
    H, W = p["relieve"].shape
    grano = ruido((H, W), 0.7, rng)
    trazo = rng.standard_normal((H, W)).astype(np.float32)
    k = np.zeros((25, 25), np.float32)
    np.fill_diagonal(k, 1)
    trazo = cv2.filter2D(trazo, -1, k / k.sum())
    trazo /= trazo.std() + 1e-9
    presion = 0.85 + 0.12 * ruido((H, W), p["px"] * 0.6, rng)
    contacto = np.clip(p["relieve"], 0, 1) ** 1.5
    oscuro = 0.74 * contacto * np.clip(presion + 0.1 * trazo + 0.07 * grano, 0, 1.1)
    papel = 0.96 + 0.015 * grano
    return np.clip(papel * (1 - oscuro), 0, 1)


# ---------------------------------------------------------------- acción 2: el pie

def _glifo_impreso(ch, fuente, asc, desc, rng):
    pad = 14
    w = int(np.ceil(fuente.getlength(ch))) + 2 * pad
    h = asc + desc + 2 * pad
    im = Image.new("L", (w, h), 0)
    ImageDraw.Draw(im).text((pad, pad + asc), ch, font=fuente, fill=255, anchor="ls")
    a = np.asarray(im, np.float32) / 255
    a = cv2.GaussianBlur(a, (0, 0), rng.uniform(0.9, 1.7))
    a = (a > rng.uniform(0.36, 0.56)).astype(np.float32)          # la tinta se corre o no alcanza
    hambre = ruido(a.shape, 2.2, rng) > rng.uniform(1.7, 2.8)       # tinta que falta
    a[hambre & (a > 0)] = 0
    if rng.random() < 0.35 and a.sum() > 0:                         # mella del tipo
        borde = a - cv2.erode(a, np.ones((3, 3), np.uint8))
        ys, xs = np.nonzero(borde)
        if len(xs):
            i = rng.integers(len(xs))
            cv2.circle(a, (int(xs[i]), int(ys[i])), int(rng.uniform(2, 5)), 0, -1)
    return a, pad


def imprimir_pie(rng):
    tam = round(CUERPO_PT * 0.3528 * PX_IMPRENTA)
    fuente = ImageFont.truetype(FUENTE_TESTIGO, tam)
    asc, desc = fuente.getmetrics()
    lineas = lineas_pie()
    marg, sangria, inter = 60, 2 * tam, round(tam * 1.2)
    W = int(max(fuente.getlength(l) for l in lineas) + 2 * marg + sangria)
    H = len(lineas) * inter + 2 * marg
    tinta = np.zeros((H, W), np.float32)
    ocurrencias = []
    for li, linea in enumerate(lineas):
        x = marg + (sangria if li == 0 else 0)
        base = marg + asc + li * inter
        palabras = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", linea)]
        for ci, ch in enumerate(linea):
            adv = fuente.getlength(ch)
            if not ch.isspace():
                g, pad = _glifo_impreso(ch, fuente, asc, desc, rng)
                y0, x0 = int(base - asc - pad), int(round(x)) - pad
                sub = tinta[y0:y0 + g.shape[0], x0:x0 + g.shape[1]]
                sub[:] = np.maximum(sub, g[:sub.shape[0], :sub.shape[1]])
                palabra = next(p for a, b, p in palabras if a <= ci < b)
                ocurrencias.append(dict(signo=ch, linea=li + 1, palabra=palabra, x0=x, x1=x + adv, base=base))
            x += adv
    return tinta, ocurrencias, dict(tam=tam, asc=asc, desc=desc)


def fotografiar(tinta, rng):
    """Foto del pie con luz rasante desde la izquierda: se ve la mordida del tipo."""
    H, W = tinta.shape
    papel = 0.88 + 0.03 * ruido((H, W), 1.5, rng) + 0.02 * ruido((H, W), 60, rng)
    mordida = np.gradient(cv2.GaussianBlur(tinta, (0, 0), 2.5), axis=1)
    refl = papel * (1 - 0.85 * tinta) - 0.9 * mordida * (1 - tinta)
    luz = np.linspace(1.04, 0.86, W)[None, :]
    img = refl * luz
    e = PX_FOTO / PX_IMPRENTA
    chica = cv2.resize(img, None, fx=e, fy=e, interpolation=cv2.INTER_AREA)
    chica = cv2.GaussianBlur(chica, (0, 0), 0.6) + rng.normal(0, 0.015, chica.shape)
    ok, buf = cv2.imencode(".jpg", (np.clip(chica, 0, 1) * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 78])
    return cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255, e


def recorte(foto, e, oc, met):
    X0 = int(np.floor((oc["x0"] - 5) * e))
    X1 = int(np.ceil((oc["x1"] + 5) * e))
    Y0 = int(np.floor((oc["base"] - met["asc"] - 6) * e))
    Y1 = int(np.ceil((oc["base"] + met["desc"] + 6) * e))
    return foto[Y0:Y1, X0:X1], (oc["x0"] * e - X0, oc["x1"] * e - X0), oc["base"] * e - Y0


def ampliar(img, rng):
    """Tres generaciones de fotocopia ampliada: cada una decide un borde y pierde detalle."""
    generaciones = []
    for g in range(GENERACIONES):
        img = cv2.resize(img, None, fx=FACTOR, fy=FACTOR, interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (0, 0), 0.45 * FACTOR)
        umbral = 0.52 + 0.05 * ruido(img.shape, 6, rng)
        tinta = (img < umbral).astype(np.float32)
        motas = (rng.random(img.shape) < 0.0003).astype(np.uint8)
        tinta = np.maximum(tinta, cv2.dilate(motas, np.ones((3, 3), np.uint8)).astype(np.float32))
        generaciones.append(tinta)
        img = 1 - 0.88 * tinta
    return generaciones, FACTOR ** GENERACIONES


def _componentes_esperadas(signo, cache={}):
    if signo not in cache:
        f = ImageFont.truetype(FUENTE_TESTIGO, 200)
        im = Image.new("L", (300, 320), 0)
        ImageDraw.Draw(im).text((50, 240), signo, font=f, fill=255, anchor="ls")
        a = np.asarray(im) > 128
        comps = componentes(a, minimo=int(0.005 * a.sum()) + 1)
        cache[signo] = (len(comps), _rugosidad(a))
    return cache[signo]


def _rugosidad(m):
    cont, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    P = sum(cv2.arcLength(c, True) for c in cont)
    A = max(m.sum(), 1)
    return P * P / (4 * np.pi * A)


def aislar(tinta, intervalo, F):
    """Se queda con las manchas que caen en el ancho propio del signo, no con las vecinas."""
    a, b = intervalo[0] * F, intervalo[1] * F
    total = tinta.sum()
    propia = np.zeros(tinta.shape, bool)
    polvo = 0
    for m, st, _ in componentes(tinta > 0.5):
        x, w, area = st[0], st[2], st[4]
        solape = max(0, min(x + w, b) - max(x, a))
        if area < 0.004 * total:
            polvo += 1
            continue
        if solape >= 0.5 * w:
            propia |= m
    return propia, polvo


def puntuar(signo, propia, polvo):
    n_esp, rug_limpia = _componentes_esperadas(signo)
    n = len(componentes(propia, minimo=int(0.004 * propia.sum()) + 1))
    rug = _rugosidad(propia) / max(rug_limpia, 1e-6)
    return 3 * abs(n - n_esp) + (rug - 1) + 0.2 * polvo


def opinar(signo, propia):
    """Decidir el borde: sin motas, sin poros, con el contorno suavizado. Devuelve cuánto se cambió.

    Quien calca sabe cuántas partes tiene el signo (la i tiene dos): se queda con
    esas y con cualquier trozo grande; las motas de la fotocopia no se calcan.
    """
    n_esp, _ = _componentes_esperadas(signo)
    partes = sorted(componentes(propia), key=lambda c: -c[1][4])
    total = max(propia.sum(), 1)
    limpia = np.zeros_like(propia)
    for i, (c, st, _) in enumerate(partes):
        if i < n_esp or st[4] >= 0.08 * total:
            limpia |= c
    m = limpia.astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.5) > 0.5
    cambio = np.logical_xor(m, propia).sum() / max(propia.sum(), 1)
    return m, 100 * cambio


# ---------------------------------------------------------------- el pie en la foto

TESTIGOS = BASE / "testigos"


def pie_de_la_foto():
    """El pie tal como está en la foto de la lámina: armado de vuelta, línea por línea, con
    las letras que recortó extraer_testigos.py; y lo que la foto deja medir.

    La foto no alcanza para calcar (una altura de x de unos 11 px, con la tinta corrida:
    los ojos de la a y de la e se cierran). Alcanza para medir alturas y grosor. El testigo
    de las formas sigue siendo el sustituto impreso; esto queda como el pie real, para
    mirarlo y para comparar.
    """
    ruta = TESTIGOS / "pie.json"
    if not ruta.exists():
        return None
    datos = json.loads(ruta.read_text(encoding="utf8"))
    lineas = {}
    for l in datos["letras"]:
        g = cv2.imread(str(TESTIGOS / l["archivo"]), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
        lineas.setdefault(l["linea"], []).append((l["x_linea"], g))
    filas = []
    for li in sorted(lineas):
        W = max(x + g.shape[1] for x, g in lineas[li])
        fila = np.ones((max(g.shape[0] for _, g in lineas[li]), W), np.float32)
        for x, g in lineas[li]:
            fila[:g.shape[0], x:x + g.shape[1]] = np.minimum(fila[:g.shape[0], x:x + g.shape[1]], g)
        filas.append(fila)
    W = max(f.shape[1] for f in filas)
    imagen = np.vstack([np.pad(f, ((0, 0), (0, W - f.shape[1])), constant_values=1) for f in filas])
    return dict(imagen=imagen, medidas=datos["tinta"], letras=len(datos["letras"]))


# ---------------------------------------------------------------- acción 3: escala, calco y reconstrucción

LETRAS_X = "acemnorsuv"
ASCENDENTES = "bdfhklí"
DESCENDENTES = "gjpqy"


def escalar_y_colocar(testigos):
    """La escala la decide el pie: la letra más alta y la más baja caben con media tesela de aire."""
    letras = {s: t for s, t in testigos.items() if s.isalpha()}
    asc = max(t["base"] - caja_tinta(t["mascara"])[1] for t in letras.values())
    desc = max(caja_tinta(t["mascara"])[3] - t["base"] for t in letras.values())
    s = (5 * TES) / (asc + desc)
    base_azulejo = T - TES / 2 - desc * s
    colocadas, desbordes = {}, {}
    for signo, t in testigos.items():
        m = cv2.resize(t["mascara"].astype(np.float32), None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR) > 0.5
        x0, y0, x1, y1 = caja_tinta(m)
        dx, dy = T / 2 - (x0 + x1) / 2, base_azulejo - t["base"] * s
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        colocadas[signo] = cv2.warpAffine(m.astype(np.float32), M, (T, T)) > 0.5
        fuera = max(0, -(y0 + dy), (y1 + dy) - (T - 1), -(x0 + dx), (x1 + dx) - (T - 1))
        if fuera > 0:
            desbordes[signo] = round(fuera / 4, 1)  # en mm
    return colocadas, s, base_azulejo, desbordes


def achatar(m, base, asc, xh, xh_nueva):
    """Lleva la altura de x de una letra a xh_nueva sin mover la base ni la línea de afuera: la
    zona de x se comprime y la de las ascendentes se estira. Abajo de la base, nada cambia."""
    afuera, borde, borde_n = base - asc, base - xh, base - xh_nueva
    y = np.arange(T, dtype=np.float32)
    fuente = y.copy()
    arriba = (y >= afuera) & (y < borde_n)
    fuente[arriba] = afuera + (y[arriba] - afuera) * (borde - afuera) / (borde_n - afuera)
    medio = (y >= borde_n) & (y <= base)
    fuente[medio] = borde + (y[medio] - borde_n) * (base - borde) / (base - borde_n)
    mapa_y = np.repeat(fuente[:, None], T, axis=1)
    mapa_x = np.repeat(np.arange(T, dtype=np.float32)[None, :], T, axis=0)
    return cv2.remap(m.astype(np.float32), mapa_x, mapa_y, cv2.INTER_LINEAR) > 0.5


def medidas(M, base):
    tops = [caja_tinta(M[c])[1] for c in LETRAS_X if c in M]
    xh = float(np.median([base - t for t in tops]))
    asc = max(base - caja_tinta(M[c])[1] for c in ASCENDENTES if c in M)
    desc = max(caja_tinta(M[c])[3] - base for c in DESCENDENTES if c in M)
    o = M["o"]
    fila = o[int(base - xh / 2)]
    corridas = np.diff(np.concatenate([[0], fila.astype(int), [0]]))
    ini, fin = np.nonzero(corridas == 1)[0], np.nonzero(corridas == -1)[0]
    grueso = int(fin[0] - ini[0]) if len(ini) else 30
    x0, _, x1, _ = caja_tinta(o)
    col = o[:, int((x0 + x1) / 2)]
    corridas = np.diff(np.concatenate([[0], col.astype(int), [0]]))
    ini, fin = np.nonzero(corridas == 1)[0], np.nonzero(corridas == -1)[0]
    fino = int(fin[0] - ini[0]) if len(ini) else 12
    return dict(base=base, xh=xh, asc=asc, desc=desc, grueso=grueso, fino=fino,
                base_teselas=(T - base) / TES, x_teselas=(T - base + xh) / TES,
                asc_teselas=(T - base + asc) / TES, desc_teselas=(T - base - desc) / TES)


def abrir_desague(q, junta=JUNTA_MM * 4):
    """Todo contorno cerrado se abre en su punto más bajo, con una abertura del ancho de una junta.

    Recibe un contorno cerrado (sin repetir el primer punto) y devuelve una línea
    abierta que empieza y termina a los lados del desagüe.
    """
    ymax = q[:, 1].max()
    fondo = np.nonzero(q[:, 1] >= ymax - 1.5)[0]
    i = fondo[np.argmin(np.abs(q[fondo, 0] - q[fondo, 0].mean()))]
    q = np.roll(q, -i, axis=0)                      # el desagüe queda en el punto 0
    seg = np.linalg.norm(np.diff(np.vstack([q, q[:1]]), axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])[:-1]
    total = s[-1] + seg[-1]
    fuera = (s < junta / 2) | (s > total - junta / 2)
    return q[~fuera]


def punto_de_desague(q):
    """Dónde quedó el desagüe de una línea abierta: entre su último punto y el primero."""
    return (q[0] + q[-1]) / 2


def temblar(p, rng, amplitud=1.3, desague=True):
    """Un contorno cerrado recorrido por una mano que tiembla un poco. Con desagüe, queda
    abierto en su punto más bajo; sin él, se devuelve cerrado (el último punto repite el primero)."""
    p = np.asarray(p, np.float32)
    seg = np.linalg.norm(np.diff(np.vstack([p, p[:1]]), axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(12, int(s[-1] / 3))
    t = np.linspace(0, s[-1], n, endpoint=False)
    pc = np.vstack([p, p[:1]])
    q = np.stack([np.interp(t, s, pc[:, 0]), np.interp(t, s, pc[:, 1])], 1)
    k = 3
    q = np.stack([np.convolve(np.r_[q[-k:, i], q[:, i], q[:k, i]], np.ones(2 * k + 1) / (2 * k + 1), "valid") for i in (0, 1)], 1)
    tang = np.roll(q, -1, 0) - np.roll(q, 1, 0)
    norm = np.stack([-tang[:, 1], tang[:, 0]], 1)
    norm /= np.linalg.norm(norm, axis=1, keepdims=True) + 1e-9
    temblor = amplitud * ruido_1d(n, 14, rng) + 0.35 * ruido_1d(n, 2, rng)
    q = q + norm * temblor[:, None]
    return abrir_desague(q) if desague else np.vstack([q, q[:1]])


def contornos_temblorosos(m, rng, amplitud=1.3, desague=True):
    """Los contornos de una máscara, calcados con temblor (para lo que solo existe en píxeles)."""
    cont, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    return [temblar(c[:, 0, :], rng, amplitud, desague) for c in cont if len(c) >= 16]


def anillos(geo):
    """Los contornos del cuerpo en vectores: el borde de cada parte y el de cada hueco."""
    partes = list(geo.geoms) if hasattr(geo, "geoms") else [geo]
    out = []
    for p in partes:
        out.append(np.array(p.exterior.coords)[:-1])
        out += [np.array(h.coords)[:-1] for h in p.interiors]
    return [q for q in out if len(q) >= 4 and np.ptp(q[:, 0]) + np.ptp(q[:, 1]) > 8]


def calcar(geo, rng, amplitud=1.3):
    """El calco de un cuerpo de la gramática: su contorno, en vectores, con el temblor de la mano."""
    return [temblar(q, rng, amplitud) for q in anillos(geo)]


def dibujar_trazos(forma, trazos, punteado, rng, grosor=2, raya=16, hueco=10):
    """Dibuja las líneas tal como vienen: abiertas en el desagüe o cerradas."""
    capa = np.zeros(forma, np.float32)
    for q in trazos:
        cerr = q
        if not punteado:
            cv2.polylines(capa, [np.round(cerr * 4).astype(np.int32)], False, 1.0, grosor, cv2.LINE_AA, shift=2)
            continue
        seg = np.linalg.norm(np.diff(cerr, axis=0), axis=1)
        s = np.concatenate([[0], np.cumsum(seg)])
        fase = rng.uniform(0, raya + hueco)
        dentro = ((s + fase) % (raya + hueco)) < raya
        i = 0
        while i < len(cerr) - 1:
            if dentro[i]:
                j = i
                while j < len(cerr) - 1 and dentro[j]:
                    j += 1
                cv2.polylines(capa, [np.round(cerr[i:j + 1] * 4).astype(np.int32)], False, 1.0, grosor, cv2.LINE_AA, shift=2)
                i = j
            i += 1
    grafito = 0.6 + 0.4 * np.clip(0.5 + 0.35 * ruido(forma, 1.2, rng), 0, 1)
    return np.clip(capa, 0, 1) * grafito


def calco(geo, reconstruida, fondo_frotado, pauta, rng):
    """El calco en papel de calco puesto sobre el frotado de la pared: línea continua lo
    hallado, punteada lo reconstruido. Se calca el cuerpo de la gramática, en vectores. La
    pauta es la celda de la letra, con sus líneas de fondo y de borde, en lápiz muy suave:
    una letra, una celda."""
    trazos = calcar(geo, rng)
    linea = dibujar_trazos((T, T), trazos, reconstruida, rng)
    img = 1 - 0.22 * (1 - fondo_frotado)
    img = img * (0.985 + 0.015 * ruido((T, T), 30, rng))          # el papel de calco no es parejo
    x0, y0, x1, y1 = (int(round(v)) for v in pauta["celda"])
    for y in (y0, y1):
        img[y, x0:x1:7] *= 0.8
    for x in (x0, x1):
        img[y0:y1:7, x] *= 0.8
    for y in (pauta["fondo"], pauta["borde"]):
        img[int(round(y)), x0:x1:9] *= 0.82
    img = img * (1 - 0.82 * linea)
    return np.clip(img, 0, 1), trazos


def celda_notdef(rng):
    """La celda de la lámina, calcada a mano: un rectángulo dentro de otro (proporciones medidas en la foto).

    También tiene desagüe: ni la celda vacía retiene.
    """
    alto = 0.62 * T
    ancho = 0.84 * alto
    x0, y0 = (T - ancho) / 2, (T - alto) / 2
    fuera = np.array([[x0, y0], [x0 + ancho, y0], [x0 + ancho, y0 + alto], [x0, y0 + alto]])
    ix, iy = 0.18 * ancho, 0.13 * alto
    dentro = np.array([[x0 + ix, y0 + iy], [x0 + ancho - ix, y0 + iy], [x0 + ancho - ix, y0 + alto - iy], [x0 + ix, y0 + alto - iy]])
    trazos = []
    for r in (fuera, dentro):
        q = np.vstack([r, r[:1]])
        pts = np.concatenate([np.linspace(q[i], q[i + 1], 60, endpoint=False) for i in range(4)])
        tang = np.roll(pts, -1, 0) - np.roll(pts, 1, 0)
        norm = np.stack([-tang[:, 1], tang[:, 0]], 1)
        norm /= np.linalg.norm(norm, axis=1, keepdims=True) + 1e-9
        trazos.append(abrir_desague(pts + norm * (1.3 * ruido_1d(len(pts), 14, rng))[:, None]))
    return trazos


def desenterrar():
    """Corre las acciones 2 y 3. Devuelve todo lo que necesitan los otros cuadernos."""
    rng = azar("pie")
    tinta, ocurrencias, met = imprimir_pie(rng)
    foto, e = fotografiar(tinta, rng)
    halladas = [c["signo"] for c in CELDAS if c["estado"] == "hallada"]
    testigos, todos = {}, {}
    for signo in halladas:
        candidatas = [o for o in ocurrencias if o["signo"] == signo]
        mejores = []
        for k, oc in enumerate(candidatas, 1):
            r, intervalo, base = recorte(foto, e, oc, met)
            gens, F = ampliar(r, azar("ampliar", signo, k))
            propia, polvo = aislar(gens[-1], intervalo, F)
            mejores.append(dict(k=k, oc=oc, recorte=r, gens=gens, propia=propia, base=base * F,
                                puntaje=puntuar(signo, propia, polvo)))
        elegido = min(mejores, key=lambda d: d["puntaje"])
        mascara, opinion = opinar(signo, elegido["propia"])
        testigos[signo] = dict(mascara=mascara, base=elegido["base"], elegido=elegido["k"], de=len(candidatas),
                               palabra=elegido["oc"]["palabra"], linea=elegido["oc"]["linea"], opinion=opinion,
                               crudo=elegido["propia"], gens=elegido["gens"], recorte=elegido["recorte"])
        todos[signo] = mejores
    M, s, base, desbordes = escalar_y_colocar(testigos)
    med = medidas(M, base)
    # del pie real, la proporción: la foto da una altura de x más baja que la del sustituto (sus
    # ascendentes miden 1,71 veces la altura de x). Las formas siguen siendo las del testigo; la
    # zona de x se achata y las ascendentes crecen hasta la misma línea de afuera.
    pie_foto = pie_de_la_foto()
    if pie_foto:
        f = pie_foto["medidas"]
        razon = f["ascendente"] / f["alto_x"]
        xh_foto = med["asc"] / razon
        M = {k: achatar(v, base, med["asc"], med["xh"], xh_foto) for k, v in M.items()}
        med = dict(medidas(M, base), xh_sustituto=med["xh"], razon_foto=round(razon, 3))
    med["escala"] = s
    # la gramática (03c_gramatica.md): del pie, las medidas; de la obra, la forma. Anatomía base → estados
    from gramatica import construir_todo
    antes = {k: v.copy() for k, v in M.items()}
    todo, esq, par = construir_todo(antes, med)
    med["canal"] = esq["canal"]
    M = {k: todo[k]["mascara"] for k in halladas}
    R = {k: v["mascara"] for k, v in todo.items() if k not in halladas}
    receta = {k: v["receta"] for k, v in todo.items() if k not in halladas}
    marcas = {k: v["glifo"].marcas for k, v in todo.items()}
    return dict(tinta=tinta, foto=foto, ocurrencias=ocurrencias, testigos=testigos, candidatas=todos,
                pie_foto=pie_foto,
                M=M, R=R, receta=receta, med=med, desbordes=desbordes, antes=antes, marcas=marcas,
                gramatica=todo, esqueleto=esq, parametros=par)
