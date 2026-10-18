"""Cuaderno 3 · Devolver: el frotado, el agua y la voz (acciones 8 a 10), simulados.

El frotado: un papel sobre la placa, por el anverso, frotado con grafito, el mismo
gesto con el que empezó todo (la pared). El papel toca toda la hoja, pero se carga
donde la placa sube por encima de su entorno. Cada frotada aplasta un poco el
relieve: se frota hasta que la letra no se lee. El peso de una letra se mide en
frotadas. Frota una mano (pulso.frotada): en diagonal, cada pasada con su presión, y
cada vez más suave a medida que se cansa.

La placa en el fondo de una bandeja con un dedo de agua. La luz de una lámpara
rebota en la placa y cae en unos azulejos: cada punto de la placa desvía la luz
según su inclinación y la del agua (un mapa de cáusticas). La superficie del agua
devuelve además un reflejo débil (el eco) y la lámpara misma (el punto fijo). La
luz llega al revés y en trapecio, y verde por el celofán. El agua está quieta, o
la toca un dedo en una esquina y la letra tiembla con las ondas. El dedo nunca toca
en el mismo punto ni con la misma fuerza, y a veces toca dos veces (pulso.toque).

La voz: el agua vibra con el ritmo silábico del verso, leído en voz alta junto a
la bandeja. Son ondas de Faraday: la longitud de onda sale de la altura de la voz.
La lectura no es un metrónomo (pulso.lectura): la foto cae en un instante cualquiera,
a veces en el silencio después de una coma, cuando el agua todavía se mueve.
"""

import cv2
import numpy as np

from comun import PX_MM, TRAPECIO, azar, ruido
from desenterrar import pared
from pulso import Mano, frotada, instante, lectura, oir, rayas, toque

VERDE = np.array([0.30, 1.0, 0.58])


# ---------------------------------------------------------------- acción 8: el frotado

def frotar(altura, mascara, rng, trazo, grano, presion):
    """Una frotada: el papel no entra en los valles finos (se apoya a unos 2 mm); toca toda la hoja
    y se carga donde la placa sube por encima de su entorno, y en el filo del corte. La presión es la
    de la mano (pulso.frotada); el trazo, la textura fina del grafito en la dirección de las pasadas."""
    h = np.where(mascara, altura, altura[mascara].min() - 0.3)
    envolvente = cv2.GaussianBlur(h, (0, 0), 7)
    contacto = 0.16 + 0.84 * np.clip((h - envolvente) / 0.9, 0, 1) ** 1.2
    oscuro = 0.8 * contacto * np.clip(presion + 0.14 * trazo + 0.08 * grano, 0, 1.1)
    return np.clip((0.965 + 0.012 * grano) * (1 - oscuro), 0, 1)


def frotadas(placa, rng, maximo=45, guardar=(1, 5, 10, 20), minuto=0.0, lado="derecha"):
    """Frotadas sucesivas de una misma placa, hasta que la letra no se lee.

    Cada frotada aplasta entre un 5 y un 9 % del relieve del surco, y un poco las arrugas
    de la hoja. La letra se lee mientras el grafito sobre el surco se aparta del de su
    alrededor más de tres veces lo que varía ese alrededor. La mano frota cada vez con otra
    presión y, con los minutos, más suave: minuto es el de la sesión en que empieza la placa.
    Devuelve las frotadas pedidas (y la última legible), cuántas se leyeron y cuántos minutos
    llevó (cada frotada: poner el papel, frotar y sacarlo).
    """
    forma = placa["altura"].shape
    _, angulo, _ = frotada(forma, PX_MM, Mano(lado=lado, minutos=minuto), rng)
    trazos = [rayas(forma, angulo, rng) for _ in range(3)]
    grano = ruido(forma, 0.7, rng)
    relieve = placa["relieve"].astype(np.float32).copy()
    base = placa["altura"] - relieve
    letra = cv2.dilate((np.abs(relieve) > 0.32).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    lejos = ~(cv2.dilate(letra.astype(np.uint8), np.ones((21, 21), np.uint8)) > 0)
    adentro = cv2.distanceTransform(placa["mascara"].astype(np.uint8), cv2.DIST_L2, 5) > 12
    alrededor = lejos & adentro                         # la hoja lejos de la letra y del filo del corte
    imagenes, legibles, ultima, minutos = {}, 0, None, 0.0
    for n in range(1, maximo + 1):
        presion, _, segundos = frotada(forma, PX_MM, Mano(lado=lado, minutos=minuto + minutos), rng)
        minutos += (segundos + rng.uniform(15, 30)) / 60
        img = frotar(base + relieve, placa["mascara"], rng, np.roll(trazos[n % 3], 37 * n, axis=1), grano, presion)
        d = cv2.GaussianBlur(1 - img, (0, 0), 1.5)       # el ojo junta los granos del grafito
        se_lee = d[letra].mean() - d[alrededor].mean() > 3 * d[alrededor].std()
        if n in guardar:
            imagenes[n] = img
        if not se_lee:
            break
        legibles, ultima = n, img
        relieve *= 1 - rng.uniform(0.05, 0.09)
        base = base * 0.98
    if ultima is not None:
        imagenes[legibles] = ultima
    return imagenes, legibles, minutos


# ---------------------------------------------------------------- acciones 9 y 10: agua y voz

def superficie_quieta(forma, rng):
    return 1.0 * ruido(forma, 60, rng)


def _anillos(forma, fase, punto, amplitud, onda, caida):
    H, W = forma
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.hypot(x - punto[0] * W, y - punto[1] * H)
    frente = 1 / (1 + np.exp((r - fase * onda - 60) / 25))   # la onda todavía no llegó más lejos
    return amplitud * np.sin(2 * np.pi * r / onda - fase * 2 * np.pi) * np.exp(-r / caida) * (r / (r + 25)) * frente


def superficie_tocada(forma, fase, rng, dedo=None, onda=46, caida=420):
    """El agua tocada por un dedo en una esquina (pulso.toque: dónde, con cuánta fuerza y si tocó dos veces)."""
    dedo = dedo or dict(punto=(0.08, 0.92), amplitud=2.2)
    z = superficie_quieta(forma, rng) + _anillos(forma, fase, dedo["punto"], dedo["amplitud"], onda, caida)
    otro = dedo.get("segundo")
    if otro and fase > otro["retraso"]:
        punto = (dedo["punto"][0] + otro["corrimiento"][0], dedo["punto"][1] + otro["corrimiento"][1])
        z = z + _anillos(forma, fase - otro["retraso"], punto, dedo["amplitud"] * otro["amplitud"], onda, caida)
    return z


def onda_de_faraday(forma, hz, volumen, rng, momento=0.0):
    """Ondas estacionarias de una bandeja que vibra: responde a la mitad de la frecuencia.

    El dibujo de la onda queda quieto y su amplitud va y vuelve: momento (de 0 a 1) es
    el punto de esa oscilación. Devuelve la superficie y la longitud de onda en mm.
    """
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
    va_y_vuelve = np.cos(2 * np.pi * momento)
    return 0.6 * volumen * va_y_vuelve * parches * w / m + superficie_quieta(forma, rng), lam_mm


def voz_del_verso(verso, rng, sostenida=False):
    """El verso leído en voz alta junto a la bandeja (pulso.lectura) y la foto en un instante cualquiera
    de la lectura: la sílaba que sonaba, con su altura y su volumen, que tiemblan (jitter y shimmer); o
    el silencio que la sigue, con el agua todavía moviéndose. Sostenida, la foto cae dentro de una
    sílaba. Alturas y volúmenes inventados: no es tu voz. Devuelve la altura, el volumen, la sílaba
    (desde 1), cuántas tiene el verso y si era silencio."""
    lec = lectura(verso, rng)
    if sostenida:
        k = rng.choice(len(lec["duracion"]), p=lec["duracion"] / lec["duracion"].sum())
        t = lec["inicio"][k] + rng.uniform(0, lec["duracion"][k])
    else:
        t = rng.uniform(0, lec["total"])
    i, queda, silencio = instante(lec, t)
    hz, volumen = oir(lec["hz"][i], lec["volumen"][i], rng)
    return hz, volumen * queda, i + 1, len(lec["hz"]), silencio


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


def agua(placa, rng, fase=None, voz=None, momento=0.0, dedo=None):
    """Una placa por el agua: quieta, tocada por un dedo (fase de la onda; el dedo, de pulso.toque) o
    movida por una voz (hz, volumen). Devuelve la luz y lo que pasó en la superficie."""
    forma = placa["altura"].shape
    info = {}
    if voz is not None:
        superficie, info["lambda_mm"] = onda_de_faraday(forma, voz[0], voz[1], rng, momento)
    elif fase is not None:
        superficie = superficie_tocada(forma, fase, rng, dedo)
    else:
        superficie = superficie_quieta(forma, rng)
    info["superficie"] = superficie
    return reflejo(placa["altura"], placa["mascara"], superficie), info


def foto_agua(luz, rng, ancho=700, alto=560, reflectancia=None):
    t, zona, _ = trapecio(luz, ancho, alto)
    if reflectancia is None:
        reflectancia = muestra_de_azulejos(ancho, alto, rng)
    return foto_de_luz(t, zona, reflectancia, rng)


def agua_tocada_en_bucle(placas, clave, cuadros=16, ancho=720, alto=300):
    """Varias placas en fila en la misma bandeja, tocada: una vuelta de la onda, cuadro por cuadro.

    La bandeja, los azulejos, el grano de la foto y el toque del dedo son los mismos en todos
    los cuadros; solo avanza la onda.
    """
    vs = {"altura": np.hstack([p["altura"] for p in placas]), "mascara": np.hstack([p["mascara"] for p in placas])}
    reflectancia = muestra_de_azulejos(ancho, alto, azar("bandeja", clave))
    dedo = toque(azar("dedo", clave))
    salida = []
    for i in range(cuadros):
        luz, _ = agua(vs, azar("onda", clave), fase=i / cuadros * 4, dedo=dedo)
        salida.append(foto_agua(luz, azar("grano", clave), ancho=ancho, alto=alto, reflectancia=reflectancia))
    return salida


def voz_en_bucle(placas, hz, volumen, clave, cuadros=12, ancho=720, alto=300):
    """Varias placas en fila en la misma bandeja, movida por una voz: la onda quieta que va y vuelve.
    La voz que se sostiene no se sostiene pareja: su volumen respira un poco (y vuelve, para que el
    bucle cierre)."""
    vs = {"altura": np.hstack([p["altura"] for p in placas]), "mascara": np.hstack([p["mascara"] for p in placas])}
    reflectancia = muestra_de_azulejos(ancho, alto, azar("bandeja", clave))
    r = azar("respira", clave)
    f1, f2 = r.uniform(0, 2 * np.pi), r.uniform(0, 2 * np.pi)
    salida = []
    for i in range(cuadros):
        respira = 1 + 0.06 * np.sin(2 * np.pi * i / cuadros + f1) + 0.03 * np.sin(4 * np.pi * i / cuadros + f2)
        luz, _ = agua(vs, azar("voz", clave), voz=(hz, volumen * respira), momento=i / cuadros)
        salida.append(foto_agua(luz, azar("grano", clave), ancho=ancho, alto=alto, reflectancia=reflectancia))
    return salida
