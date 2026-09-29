"""Cuaderno 3 · Devolver: acciones 8 a 11, simuladas.

Acción 8: el hectógrafo. La matriz (las 56 placas vestidas, en alto contraste,
en cuerpo tesela) se apoya en la gelatina; cada copia se lleva una parte de la
tinta que queda, la tinta se difunde y se hunde. Se sigue hasta que la caja no
se lee. Cada signo tiene su última copia legible.
Acción 9: el agua. La luz de una lámpara rebota en la placa, en el fondo de
una bandeja con un dedo de agua, y cae en unos azulejos: cada punto de la placa
desvía la luz según su inclinación y la del agua (un mapa de cáusticas). La
superficie del agua devuelve además un reflejo débil (el eco) y la lámpara
misma (el punto fijo). Llega al revés y en trapecio, y verde por el celofán.
Acción 10: la voz. El agua vibra con el ritmo silábico del verso: ondas de
Faraday cuya longitud sale de la altura de la voz.
Acción 11: la luz llega a la pared de la piscina, ampliada y cortada por las
juntas; se calca lo que quedó. Y se compone un verso con las placas.
"""

import cv2
import numpy as np

from comun import TRAPECIO, T, caja_tinta, densidad_a_violeta, ruido, silabas
from desenterrar import foto_pared, frotado, pared

PX_H = 8                     # px/mm de las copias
CELDA_H = 25 * PX_H          # cuerpo tesela: una celda de 25 mm
A4 = (297 * PX_H, 210 * PX_H)
VERDE = np.array([0.30, 1.0, 0.58])


# ---------------------------------------------------------------- acción 8: hectógrafo

def matriz_de(vestida):
    """Alto contraste de la placa vestida: se marcan los surcos y los pliegues."""
    lineas = vestida["relieve"] + 0.55 * np.abs(vestida["pliegues"])
    m = (lineas > 0.32) & vestida["mascara"]
    chica = cv2.resize(m.astype(np.float32), (CELDA_H, CELDA_H), interpolation=cv2.INTER_AREA)
    return chica > 0.16


def armar_matriz(matrices, celdas):
    H, W = A4
    mat = np.zeros((H, W), bool)
    x0, y0 = (W - 8 * CELDA_H) // 2, 150
    cajas = {}
    for c in celdas:
        m = matrices.get(c["celda"])
        if m is None:
            continue
        x = x0 + (c["columna"] - 1) * CELDA_H
        y = y0 + (c["fila"] - 1) * CELDA_H
        mat[y:y + CELDA_H, x:x + CELDA_H] |= m
        cajas[c["celda"]] = (x, y)
    return mat, cajas


def hectografiar(mat, cajas, matrices, rng, max_copias=70, guardar_copias=(1, 5, 10, 20, 30)):
    H, W = mat.shape
    gel = cv2.GaussianBlur(mat.astype(np.float32) * 12 * (0.9 + 0.1 * ruido((H, W), 3, rng)), (0, 0), 0.7)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    borde = np.clip(np.minimum.reduce([x, y, W - x, H - y]) / 250, 0, 1)
    papel_ruido = ruido((H, W), 0.8, rng)
    ultima = {c: 0 for c in cajas}
    copias, n_legible = {}, 0
    for n in range(1, max_copias + 1):
        presion = np.clip(0.95 + 0.1 * ruido((H, W), 120, rng) - 0.18 * (1 - borde), 0.5, 1.2)
        f = 0.13 * presion
        copia = cv2.GaussianBlur(gel * f, (0, 0), 0.5)
        gel = cv2.GaussianBlur(gel * (1 - f), (0, 0), 0.4) * 0.985
        d = copia + 0.012 * papel_ruido
        legibles = 0
        for celda, (cx, cy) in cajas.items():
            m = matrices[celda]
            sub = d[cy:cy + CELDA_H, cx:cx + CELDA_H]
            anillo = cv2.dilate(m.astype(np.uint8), np.ones((9, 9), np.uint8)) == 0
            contraste = sub[m].mean() - sub[anillo].mean()
            if contraste > 3.0 * sub[anillo].std():
                ultima[celda] = n
                legibles += 1
        if n in guardar_copias:
            copias[n] = copia
        if legibles == 0:
            break
        n_legible, ultima_copia = n, copia
    copias[n_legible] = ultima_copia
    return copias, ultima, n_legible, gel


def pagina(copia, rng, numero=None):
    H, W = copia.shape
    img = densidad_a_violeta(copia)
    img *= (0.985 + 0.015 * ruido((H, W), 1.0, rng))[..., None]
    return np.clip(img, 0, 1)


def la_bandeja_bebe(gel, cajas, rng, celdas=(8, 16, 24)):
    """La gelatina después de la tirada, a las 0, 12, 24 y 48 horas: la tinta se hunde."""
    x0 = min(cajas[c][0] for c in celdas)
    y0 = min(cajas[c][1] for c in celdas)
    x1 = max(cajas[c][0] for c in celdas) + CELDA_H
    y1 = max(cajas[c][1] for c in celdas) + CELDA_H
    sub = gel[y0:y1, x0:x1]
    paneles = []
    for horas in (0, 12, 24, 48):
        g = cv2.GaussianBlur(sub, (0, 0), 0.3 + 0.12 * horas) * np.exp(-horas / 14)
        base = np.array([0.86, 0.78, 0.6])[None, None, :] * (0.97 + 0.03 * ruido(g.shape, 2, rng))[..., None]
        img = base * np.exp(-g[..., None] * np.array([0.9, 1.4, 0.55])[None, None, :] * 0.6)
        paneles.append(np.clip(img, 0, 1))
    return paneles


# ---------------------------------------------------------------- acciones 9 y 10: agua y voz

def superficie_quieta(forma, rng):
    return 1.0 * ruido(forma, 60, rng)


def superficie_tocada(forma, fase, rng, punto=(0.08, 0.92), amplitud=2.2, onda=46, caida=420):
    H, W = forma
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(x - punto[0] * W, y - punto[1] * H)
    frente = 1 / (1 + np.exp((r - fase * onda - 60) / 25))   # la onda todavía no llegó más lejos
    return superficie_quieta(forma, rng) + amplitud * np.sin(2 * np.pi * r / onda - fase * 2 * np.pi) \
        * np.exp(-r / caida) * (r / (r + 25)) * frente


def onda_de_faraday(forma, hz, volumen, rng):
    """Ondas estacionarias de una bandeja que vibra: respuesta a la mitad de la frecuencia."""
    sigma, rho = 0.072, 1000.0
    lam_mm = (2 * np.pi * sigma / (rho * (hz / 2) ** 2)) ** (1 / 3) * 1000
    lam = lam_mm * 4
    H, W = forma
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    k = 2 * np.pi / lam
    m = 2 if volumen < 0.6 else 3
    base = rng.uniform(0, np.pi)
    w = np.zeros(forma, np.float32)
    for i in range(m):
        th = base + i * np.pi / m
        w += np.cos(k * (x * np.cos(th) + y * np.sin(th)) + rng.uniform(0, 2 * np.pi))
    parches = 0.5 + 0.5 * np.clip(ruido(forma, 80, rng), -1, 1)   # la bandeja no vibra pareja
    return 0.6 * volumen * parches * w / m + superficie_quieta(forma, rng), lam_mm


def reflejo(altura, mascara, agua, k_placa=26, k_agua=55):
    """Cáusticas: cada punto de la placa manda su luz a un punto de la pared."""
    H, W = altura.shape
    gy, gx = np.gradient(altura.astype(np.float32))
    wy, wx = np.gradient(agua.astype(np.float32))
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    u = (x + 2 * k_placa * gx + k_agua * wx).ravel()
    v = (y + 2 * k_placa * gy + k_agua * wy).ravel()
    peso = (mascara.astype(np.float32) * 0.9).ravel()
    acc = np.zeros(H * W, np.float64)
    u0, v0 = np.floor(u).astype(int), np.floor(v).astype(int)
    fu, fv = u - u0, v - v0
    for du, dv, wgt in ((0, 0, (1 - fu) * (1 - fv)), (1, 0, fu * (1 - fv)), (0, 1, (1 - fu) * fv), (1, 1, fu * fv)):
        uu, vv = u0 + du, v0 + dv
        ok = (uu >= 0) & (uu < W) & (vv >= 0) & (vv < H)
        np.add.at(acc, vv[ok] * W + uu[ok], (peso * wgt)[ok])
    luz = cv2.GaussianBlur(acc.reshape(H, W).astype(np.float32), (0, 0), 1.6)
    eco = np.roll(np.roll(luz, 9, axis=1), 6, axis=0)
    brillo_agua = 0.05 * (1 + 0.5 * np.tanh(3 * (wx + wy)))
    return luz + 0.32 * eco + brillo_agua


def trapecio(luz, ancho_salida, alto_salida, margen=0.04):
    """La imagen llega al revés y abierta en trapecio, como en los videos."""
    H, W = luz.shape
    al_reves = np.flipud(luz)
    m = margen * ancho_salida
    arriba = [m, ancho_salida - m]
    ab = (ancho_salida - 2 * m) * TRAPECIO
    abajo = [ancho_salida / 2 - ab / 2, ancho_salida / 2 + ab / 2]
    src = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    dst = np.float32([[arriba[0], 0.06 * alto_salida], [arriba[1], 0.06 * alto_salida],
                      [abajo[1], 0.94 * alto_salida], [abajo[0], 0.94 * alto_salida]])
    P = cv2.getPerspectiveTransform(src, dst)
    fuera = cv2.warpPerspective(al_reves, P, (ancho_salida, alto_salida))
    zona = cv2.warpPerspective(np.ones_like(al_reves), P, (ancho_salida, alto_salida))
    return fuera, zona, P


def foto_de_luz(luz, zona, reflectancia, rng, punto=(0.5, 0.84)):
    """Foto en un cuarto oscuro: luz verde sobre azulejo, con el punto fijo de la lámpara."""
    H, W = luz.shape
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = punto[0] * W, punto[1] * H
    lampara = 2.6 * np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * 9 ** 2)) + \
        0.5 * np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * 45 ** 2))
    L = (0.55 * luz * zona + lampara * zona) * reflectancia
    img = L[..., None] * VERDE[None, None, :] + np.array([0.012, 0.018, 0.035])[None, None, :]
    img = img + 0.01 * rng.standard_normal(img.shape)
    return np.clip(img, 0, 1) ** (1 / 1.1)


def muestra_de_azulejos(W, H, rng):
    """Dos por dos azulejos sueltos: el esmalte refleja, la junta no."""
    p = pared(2, 2, int(max(W, H) / 2), rng)
    alb = np.where(p["juntas"], 0.28, 0.88 - p["mancha"] - 0.3 * p["grietas"]) * (0.8 + 0.2 * p["relieve"])
    return cv2.resize(alb.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)


def agua(vestida, rng, fase=None, voz=None):
    """Una letra por el agua: quieta, tocada (fase de la onda) o movida por una voz (hz, volumen)."""
    forma = vestida["altura"].shape
    info = {}
    if voz is not None:
        superficie, info["lambda_mm"] = onda_de_faraday(forma, voz[0], voz[1], rng)
    elif fase is not None:
        superficie = superficie_tocada(forma, fase, rng)
    else:
        superficie = superficie_quieta(forma, rng)
    luz = reflejo(vestida["altura"], vestida["mascara"], superficie)
    info["superficie"] = superficie
    return luz, info


def foto_agua(luz, rng, ancho=700, alto=560, reflectancia=None):
    t, zona, _ = trapecio(luz, ancho, alto)
    if reflectancia is None:
        reflectancia = muestra_de_azulejos(ancho, alto, rng)
    return foto_de_luz(t, zona, reflectancia, rng)


def voz_del_verso(verso, rng):
    """Una sílaba del verso, con una altura y un volumen inventados (no es tu voz)."""
    s = silabas(verso)
    i = int(rng.integers(len(s)))
    hz = float(np.interp(i, [0, max(len(s) - 1, 1)], [rng.uniform(170, 220), rng.uniform(110, 140)]))
    volumen = float(np.clip(rng.normal(0.65, 0.2), 0.15, 1.0))
    return hz, volumen, i + 1, len(s)


# ---------------------------------------------------------------- acción 11: la pared

def aterrizar(luz, vestida, superficie, rng, aumento=3.0, k_agua=55):
    """La luz de la letra sobre la pared de la piscina: ampliada, en trapecio y cortada por las juntas.

    Devuelve la foto y el calco de lo que quedó. Quien calca sigue la letra donde
    cae (no los pliegues ni el borde de la placa) y no puede seguirla por las juntas.
    """
    p = pared(4, 4, T, rng)
    Hp, Wp = p["relieve"].shape
    ancho = int(T * aumento)
    alto = int(ancho * 0.8)
    t, zona, _ = trapecio(luz, ancho, alto)
    wy, wx = np.gradient(superficie.astype(np.float32))
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    letra = (vestida["relieve"] > 0.32).astype(np.float32)
    letra = cv2.remap(letra, x - k_agua * wx, y - k_agua * wy, cv2.INTER_LINEAR)
    lt, _, _ = trapecio(letra, ancho, alto)
    lienzo = {k: np.zeros((Hp, Wp), np.float32) for k in ("luz", "zona", "letra")}
    x0 = int((Wp - ancho) // 2 + rng.uniform(-0.12, 0.12) * T)
    y0 = int((Hp - alto) // 2 + rng.uniform(-0.12, 0.12) * T)
    for k, v in (("luz", t), ("zona", zona), ("letra", lt)):
        lienzo[k][y0:y0 + alto, x0:x0 + ancho] = v
    alb = np.where(p["juntas"], 0.22, 0.9 - p["mancha"] - 0.3 * p["grietas"]) * (0.7 + 0.3 * p["relieve"])
    foto = foto_de_luz(lienzo["luz"], lienzo["zona"], alb, rng, punto=((x0 + 0.5 * ancho) / Wp, (y0 + 0.84 * alto) / Hp))
    juntas = cv2.dilate(p["juntas"].astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool)
    from skimage.morphology import skeletonize
    eje = skeletonize(lienzo["letra"] > 0.4)
    trazo = cv2.dilate(eje.astype(np.uint8), np.ones((4, 4), np.uint8)).astype(bool) & ~juntas
    frot = frotado(p, rng)
    calco = np.where(trazo, 0.1, frot * 0.25 + 0.75)
    lx0, ly0, lx1, ly1 = caja_tinta(lienzo["letra"] > 0.4)
    lado = int(max(lx1 - lx0, ly1 - ly0) * 1.35) + 40
    cx, cy = (lx0 + lx1) // 2, (ly0 + ly1) // 2
    recorte = (max(0, cx - lado // 2), max(0, cy - lado // 2), lado)
    return foto, calco, _juntas_que_cruzan(lienzo["letra"] > 0.4, p["juntas"]), recorte


def _juntas_que_cruzan(trazo, juntas):
    if not trazo.any():
        return 0
    x0, y0, x1, y1 = caja_tinta(trazo)
    sub = juntas[y0:y1 + 1, x0:x1 + 1]
    cols = sub.mean(axis=0) > 0.5
    filas = sub.mean(axis=1) > 0.5
    cuenta = lambda v: int(np.sum(np.diff(v.astype(int)) == 1))
    return cuenta(cols) + cuenta(filas)


def componer(versos, fotos, rng, px=120, columnas=30):
    """Un verso por fila sobre la pared de la piscina: una placa por azulejo, cinta de pintor en las esquinas."""
    filas = len(versos) + 2
    p = pared(filas, columnas, px, rng)
    img = foto_pared(p, rng)
    j = p["junta"]
    usadas = []
    for fi, verso in enumerate(versos):
        cuenta = {}
        for ci, ch in enumerate(verso):
            if ch == " ":
                continue
            cuenta[ch] = cuenta.get(ch, 0) + 1
            clave = (ch, cuenta[ch])
            f = fotos.get(clave)
            if f is None:
                f = fotos.get((ch, 1))
            usadas.append(clave)
            if f is None:
                continue
            x = j + (ci + 1) * (px + j)
            y = j + (fi + 1) * (px + j)
            lado = px - 8
            chica = 0.3 + 0.75 * cv2.resize(f, (lado, lado), interpolation=cv2.INTER_AREA)  # a la luz del día
            ox, oy = x + 4, y + 4
            sombra = img[oy + 3:oy + 3 + lado, ox + 4:ox + 4 + lado]
            sombra *= 0.7
            placa = np.dstack([chica * 0.98, chica, chica * 1.02])
            img[oy:oy + lado, ox:ox + lado] = placa
            for tx in (ox - 6, ox + lado - 14):
                cinta = img[oy - 4:oy + 10, tx:tx + 20]
                cinta[:] = cinta * 0.35 + np.array([0.85, 0.8, 0.62]) * 0.65
    return np.clip(img, 0, 1), usadas
