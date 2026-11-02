"""Cuaderno 1 · Desenterrar: acciones 1 a 3, simuladas.

Acción 1: una pared de azulejo con juntas torcidas, craquelado, manchas y
desportillados, y su frotado con grafito.
Acción 2: el pie impreso con tipos de plomo (tinta que se corre, tinta que
falta, mellas), fotografiado con luz rasante, ampliado en tres generaciones de
fotocopia; para cada signo se elige el testigo mejor conservado.
Acción 3: la escala que decide el pie, el calco con temblor de mano y la
reconstrucción por analogía de los signos que el pie no trae.
"""

import re

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from comun import (AZULEJO_MM, CELDAS, FUENTE_TESTIGO, JUNTA_MM, T, TES, azar, caja_tinta, centrar_h, componentes,
                   escalar, lineas_pie, mover, rotar, ruido, ruido_1d)

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


def foto_pared(p, rng, luz_desde_izquierda=True):
    """Foto de la pared: esmalte blanco con manchas, grietas sucias y juntas grises."""
    H, W = p["relieve"].shape
    esmalte = 0.9 - p["mancha"] - 0.12 * p["grietas"] + 0.015 * ruido((H, W), 1.0, rng)
    junta = 0.42 + 0.06 * ruido((H, W), 3, rng)
    alb = np.where(p["juntas"], junta, esmalte)
    alb = alb * (0.75 + 0.25 * np.clip(p["relieve"], 0, 1))
    x = np.linspace(0, 1, W)[None, :]
    luz = (0.72 + 0.3 * x) if luz_desde_izquierda else (1.02 - 0.3 * x)
    img = np.clip(alb * luz, 0, 1)
    return np.dstack([img * 0.98, img * 0.97, img * 0.93])


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


def _arriba_de_x(m, med, margen=0.08):
    """Las partes que están por encima de la altura de x: tildes y puntos."""
    linea = med["base"] - med["xh"] * (1 + margen)
    out = np.zeros_like(m)
    for c, st, cen in componentes(m):
        if cen[1] < linea:
            out |= c
    return out


def _abajo_de_x(m, med):
    linea = med["base"] - med["xh"] * 1.08
    out = np.zeros_like(m)
    for c, st, cen in componentes(m):
        if cen[1] >= linea:
            out |= c
    return out


def _linea(pts, grosor):
    m = np.zeros((T, T), np.uint8)
    cv2.polylines(m, [np.array(pts, np.int32)], False, 255, max(1, int(round(grosor))), cv2.LINE_AA)
    return m > 127


def _rect(x0, y0, x1, y1):
    m = np.zeros((T, T), bool)
    m[int(max(0, y0)):int(min(T, y1)), int(max(0, x0)):int(min(T, x1))] = True
    return m


def _poner_encima(base_m, acento, ref_m):
    """Pone un acento sobre base_m con la misma posición relativa que tenía sobre ref_m."""
    bx0, _, bx1, _ = caja_tinta(base_m)
    rx0, _, rx1, _ = caja_tinta(_sin(ref_m, acento))
    return base_m | mover(acento, (bx0 + bx1) / 2 - (rx0 + rx1) / 2, 0)


def _sin(m, parte):
    return m & ~parte


def reconstruir(M, med, rng):
    """Los 25 signos que el pie no trae, por analogía. Devuelve máscaras y la receta de cada una."""
    b, xh, g, f = med["base"], med["xh"], med["grueso"], med["fino"]
    xl = b - xh
    R, receta = {}, {}
    tilde = _arriba_de_x(M["á"], med)
    punto_i = _arriba_de_x(M["i"], med)
    o = M["o"]
    ox0, oy0, ox1, oy1 = caja_tinta(o)
    ocx, ocy, ow, oh = (ox0 + ox1) / 2, (oy0 + oy1) / 2, ox1 - ox0, oy1 - oy0

    R["ó"] = _poner_encima(M["o"], tilde, M["á"]); receta["ó"] = "la o con la tilde de la á"
    R["é"] = _poner_encima(M["e"], tilde, M["á"]); receta["é"] = "la e con la tilde de la á"
    u0, _, u1, _ = caja_tinta(M["u"])
    px0, _, px1, _ = caja_tinta(punto_i)
    uc, uw = (u0 + u1) / 2, u1 - u0
    R["ü"] = M["u"] | mover(punto_i, uc - 0.22 * uw - (px0 + px1) / 2, 0) | mover(punto_i, uc + 0.22 * uw - (px0 + px1) / 2, 0)
    receta["ü"] = "la u con dos puntos de la i"
    n0, _, n1, _ = caja_tinta(M["n"])
    _, ty0, _, ty1 = caja_tinta(tilde)
    xs = np.linspace(n0 + 0.08 * (n1 - n0), n1 - 0.08 * (n1 - n0), 40)
    ys = (ty0 + ty1) / 2 + 0.045 * xh * np.sin(np.linspace(0.2, 2 * np.pi - 0.2, 40) + np.pi)
    R["ñ"] = M["n"] | _linea(np.stack([xs, ys], 1), f * 1.15)
    receta["ñ"] = "la n con una virgulilla sin modelo, del grueso fino de la o"

    v = M["v"]
    vx0, vy0, vx1, vy1 = caja_tinta(v)
    vc = (vx0 + vx1) / 2
    vv = escalar(v, 0.72, 1, vc, 0)
    R["w"] = centrar_h(mover(vv, -0.3 * (vx1 - vx0), 0) | mover(vv, 0.3 * (vx1 - vx0), 0))
    receta["w"] = "dos v estrechadas"
    k = ((vx1 - vx0) / 2) / max(vy1 - vy0, 1)
    izq = v & (np.arange(T)[None, :] < vc)
    der = v & (np.arange(T)[None, :] >= vc)
    inclinar = lambda m, kk: cv2.warpAffine(m.astype(np.float32), np.float32([[1, kk, -kk * vy0], [0, 1, 0]]), (T, T)) > 0.5
    R["x"] = centrar_h(escalar(inclinar(izq, k) | inclinar(der, -k), 0.92, 1, vc, 0))
    receta["x"] = "los dos trazos de la v, inclinados hasta cruzarse (quedan con remates solo arriba)"
    xx0, xy0, xx1, xy1 = caja_tinta(R["x"])
    yy, xxg = np.mgrid[0:T, 0:T]
    d = np.abs((xy1 - xy0) * xxg + (xx1 - xx0) * yy - (xx1 * xy1 - xx0 * xy0)) / np.hypot(xy1 - xy0, xx1 - xx0)
    diag = R["x"] & (d < g * 0.55) & (yy > xy0 + f) & (yy < xy1 - f)
    R["z"] = diag | _rect(xx0 + 0.05 * (xx1 - xx0), xy0, xx1, xy0 + f * 1.3) | _rect(xx0, xy1 - f * 1.3, xx1 - 0.03 * (xx1 - xx0), xy1)
    receta["z"] = "la diagonal de la x reconstruida (hipótesis sobre hipótesis) y dos barras del grueso fino de la o"

    # cifras elzevirianas: de altura de x; 6 y 8 suben; 3, 4, 5, 7 y 9 bajan
    baja = b + 0.38 * xh
    R["0"] = escalar(o, 0.9, 1, ocx, ocy); receta["0"] = "la o, algo más estrecha"
    stem = _abajo_de_x(M["i"], med)
    sx0, sy0, sx1, _ = caja_tinta(stem)
    R["1"] = stem | _linea([(sx0 + 2, sy0 + f), (sx0 - 0.18 * xh, sy0 + 0.22 * xh)], f * 1.2)
    receta["1"] = "la i sin punto, con una bandera"
    arco = o & (yy < ocy + 0.05 * oh) & (xxg > ocx - 0.42 * ow)
    R["2"] = arco | _linea([(ox1 - 0.08 * ow, ocy), (ox0 + 0.04 * ow, b - f)], g * 0.75) | _rect(ox0, b - f * 1.3, ox1, b)
    receta["2"] = "el arco de arriba de la o, una diagonal y una barra de base"
    mitad_d = o & (xxg > ocx - 0.12 * ow)
    alto3 = baja - xl
    s1 = escalar(mitad_d, 0.85, 0.52 * alto3 / oh, ocx, oy0)
    s1 = mover(s1, 0, xl - oy0)
    s2 = escalar(mitad_d, 1.0, 0.6 * alto3 / oh, ocx, oy1)
    s2 = mover(s2, 0, baja - oy1)
    R["3"] = s1 | s2; receta["3"] = "dos mitades derechas de la o, la de abajo bajo la línea"
    tx = ocx + 0.12 * ow
    R["4"] = _rect(tx - g * 0.45, xl, tx + g * 0.45, baja) | _linea([(tx, xl), (ocx - 0.42 * ow, b - 0.08 * xh)], f * 1.3) | \
        _rect(ocx - 0.45 * ow, b - 0.08 * xh - f * 0.7, ocx + 0.4 * ow, b - 0.08 * xh + f * 0.7)
    receta["4"] = "un asta que baja, una diagonal fina y una barra"
    cuenco = o & (yy > ocy - 0.1 * oh) & (xxg > ocx - 0.25 * ow)
    cuenco = mover(escalar(cuenco, 1.05, 1.15, ocx, ocy), 0, baja - (oy1 + 0.07 * oh))
    R["5"] = _rect(ocx - 0.28 * ow, xl, ocx + 0.35 * ow, xl + f * 1.3) | _rect(ocx - 0.28 * ow - g * 0.4, xl, ocx - 0.28 * ow + g * 0.4, xl + 0.5 * xh) | cuenco
    receta["5"] = "una barra, un asta corta y la mitad baja de la o, bajo la línea"
    c = M["c"]
    cx0, cy0, cx1, cy1 = caja_tinta(c)
    grande = escalar(c, 1.0, 1.75, cx1, cy1)
    subida = grande & (yy < oy0 + 0.1 * oh) & (xxg < ocx + 0.3 * ow)
    subida = mover(subida, ox0 - caja_tinta(subida)[0], 0)
    R["6"] = centrar_h(o | subida); receta["6"] = "la o con la curva de una c agrandada que sube"
    R["7"] = _rect(ocx - 0.38 * ow, xl, ocx + 0.38 * ow, xl + f * 1.3) | _linea([(ocx + 0.36 * ow, xl + f), (ocx - 0.12 * ow, baja)], g * 0.8)
    receta["7"] = "una barra y una diagonal que baja"
    o_b = escalar(o, 0.78, 0.74, ocx, oy1)
    o_a = escalar(o, 0.66, 0.62, ocx, oy1)
    o_a = mover(o_a, 0, -(caja_tinta(o_b)[3] - caja_tinta(o_b)[1]) * 0.9)
    R["8"] = o_b | o_a; receta["8"] = "dos o apiladas, la de arriba más chica"
    x6 = caja_tinta(R["6"])
    nueve = rotar(R["6"], 180, (x6[0] + x6[2]) / 2, (x6[1] + x6[3]) / 2)
    R["9"] = mover(nueve, 0, xl - caja_tinta(nueve)[1]); receta["9"] = "el 6 dado vuelta"

    punto = M["."]
    p0, py0, p1, py1 = caja_tinta(punto)
    R[";"] = M[","] | mover(punto, 0, xl + 0.05 * xh - py0); receta[";"] = "la coma y el punto subido"
    R[":"] = punto | mover(punto, 0, xl + 0.05 * xh - py0); receta[":"] = "dos puntos"
    gancho = o & (yy < ocy + 0.22 * oh) & (xxg > ocx - 0.45 * ow)
    gancho = mover(escalar(gancho, 0.9, 0.9, ocx, oy0), 0, (b - med["asc"]) - oy0)
    gx0, gy0, gx1, gy1 = caja_tinta(gancho)
    gcx = (gx0 + gx1) / 2
    R["?"] = gancho | _linea([(gx1 - g * 0.5, gy1 - f * 0.5), (gcx, gy1 + 0.1 * xh), (gcx, b - 0.4 * xh)], g * 0.6) | \
        mover(punto, gcx - (p0 + p1) / 2, 0)
    receta["?"] = "el arco de arriba de la o, un asta que baja al centro y el punto"
    q = caja_tinta(R["?"])
    inv = rotar(R["?"], 180, (q[0] + q[2]) / 2, (q[1] + q[3]) / 2)
    R["¿"] = mover(inv, 0, baja - caja_tinta(inv)[3]); receta["¿"] = "la ? dada vuelta, bajo la línea"
    ang = escalar(v, 0.68, 0.62, vc, (vy0 + vy1) / 2)
    menor = rotar(ang, -90, vc, (vy0 + vy1) / 2)
    mayor = rotar(ang, 90, vc, (vy0 + vy1) / 2)
    cy_ = b - 0.45 * xh
    def _dos(m):
        x0, y0, x1, y1 = caja_tinta(m)
        m = mover(m, 0, cy_ - (y0 + y1) / 2)
        return centrar_h(mover(m, -0.26 * xh, 0) | mover(m, 0.26 * xh, 0))
    R["«"], R["»"] = _dos(menor), _dos(mayor)
    receta["«"] = receta["»"] = "ángulos de la v girada y achicada"
    R["—"] = _rect(0.06 * T, cy_ - f * 0.6, 0.94 * T, cy_ + f * 0.6); receta["—"] = "una barra sin modelo, del grueso fino de la o"
    R["…"] = mover(punto, T / 2 - 0.26 * T - (p0 + p1) / 2, 0) | mover(punto, T / 2 - (p0 + p1) / 2, 0) | \
        mover(punto, T / 2 + 0.26 * T - (p0 + p1) / 2, 0)
    receta["…"] = "tres puntos"

    for k in R:
        if k not in "—…«»":
            R[k] = centrar_h(R[k])
    # lo que se sale del azulejo se achica en alto, sobre la línea de base, y se anota
    arriba, abajo = TES / 2, T - TES / 2
    for k in R:
        x0, y0, x1, y1 = caja_tinta(R[k])
        sy = 1.0
        if y0 < arriba:
            sy = min(sy, (b - arriba) / (b - y0))
        if y1 > abajo:
            sy = min(sy, (abajo - b) / (y1 - b))
        if sy < 1:
            R[k] = escalar(R[k], 1, sy, (x0 + x1) / 2, b)
            receta[k] += f" (achicada en alto al {100 * sy:.0f} % para caber en el azulejo)"
    return R, receta


def contornos_temblorosos(m, rng, amplitud=1.3):
    """Contornos de la máscara, recorridos por una mano que tiembla un poco."""
    cont, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    salida = []
    for c in cont:
        p = c[:, 0, :].astype(np.float32)
        if len(p) < 16:
            continue
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
        salida.append(q + norm * temblor[:, None])
    return salida


def dibujar_trazos(forma, trazos, punteado, rng, grosor=2, raya=16, hueco=10):
    capa = np.zeros(forma, np.float32)
    for q in trazos:
        cerr = np.vstack([q, q[:1]])
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


def calco(m, reconstruida, fondo_frotado, med, rng):
    """El calco sobre papel de calco puesto encima del frotado: línea continua o punteada."""
    trazos = contornos_temblorosos(m, rng)
    linea = dibujar_trazos((T, T), trazos, reconstruida, rng)
    fondo = 1 - 0.22 * (1 - fondo_frotado)
    img = fondo.copy()
    for y, alto in ((med["base"], 1), (med["base"] - med["xh"], 1)):
        yy = int(round(y))
        img[yy:yy + alto, ::9] *= 0.82
    img = img * (1 - 0.82 * linea)
    return np.clip(img, 0, 1), trazos


def celda_notdef(rng):
    """La celda de la lámina, calcada a mano: un rectángulo dentro de otro (proporciones medidas en la foto)."""
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
        trazos.append(pts + norm * (1.3 * ruido_1d(len(pts), 14, rng))[:, None])
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
    med["escala"] = s
    R, receta = reconstruir(M, med, azar("reconstruir"))
    return dict(tinta=tinta, foto=foto, ocurrencias=ocurrencias, testigos=testigos, candidatas=todos,
                M=M, R=R, receta=receta, med=med, desbordes=desbordes)
