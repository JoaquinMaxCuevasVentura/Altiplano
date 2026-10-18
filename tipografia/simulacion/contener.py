"""Cuaderno 2 · Contener: la placa (acción 4), simulada.

El calco se da vuelta (espejo) y se repasa por el reverso de una hoja de papel de
aluminio de cocina, cortada a tijera, con un punzón de bola de 1 mm sobre una base
blanda. La mano que repuja sigue la línea de grafito del calco, no el contorno ideal,
con su propio pulso (pulso.py): en tramos, más despacio en las curvas, con dudas, y
con las dos manos (la otra lee el anverso cada tanto). Donde arranca, donde duda y
donde termina, el punzón descansa y hunde más; donde dos tramos se montan, el surco
se repasa. Por el reverso queda un surco: la letra al revés, hundida, un canal que
podría contener agua. Por el anverso, un relieve que se lee. Lo hallado es un surco
continuo; lo reconstruido, puntos, cada uno una presión. El punteado perfora: las
placas reconstruidas se rompen más, y se rompen donde la mano más apretó. Si una
placa se rompe, se guarda y se hace otra. El tiempo de cada placa sale de la mano.

El signo final: la máquina no tiene dedos. Simula las presiones de un pulgar
genérico: dos a cuatro, porque una mano no acierta a la primera.
"""

import cv2
import numpy as np
from shapely.geometry import Polygon

from comun import PX_MM, T, azar, ruido, sombrear
from pulso import Mano, cansancio, puntos, trazar, unir

ESTILETE_PX = 4            # punzón de bola de 1 mm
PREPARAR = 4.0             # minutos: cortar la hoja, dar vuelta el calco y pegarlo con cinta
RETIRAR = 1.0              # minutos: retirar el calco y dar vuelta la placa
LADO_MM = (T - 1) / PX_MM


# ---------------------------------------------------------------- la hoja

def tijera(rng, margen=16):
    """El contorno de una hoja cortada a tijera (un polígono de shapely).

    Cada lado es una recta apenas inclinada; se corta en dos o tres tramos casi rectos y,
    donde la tijera se retoma, queda un escalón chico. A veces una esquina se corta en
    diagonal.
    """
    m = [margen + rng.uniform(-5, 9) for _ in range(4)]
    a = [np.tan(np.radians(rng.normal(0, 0.8))) for _ in range(4)]
    c = T / 2

    def esquina(i):
        """Cruce del lado i con el siguiente (0 arriba, 1 derecha, 2 abajo, 3 izquierda)."""
        x, y = c, c
        for _ in range(4):
            if i == 0:      # arriba y derecha
                y = m[0] + (x - c) * a[0]
                x = T - m[1] - (y - c) * a[1]
            elif i == 1:    # derecha y abajo
                x = T - m[1] - (y - c) * a[1]
                y = T - m[2] - (x - c) * a[2]
            elif i == 2:    # abajo e izquierda
                y = T - m[2] - (x - c) * a[2]
                x = m[3] + (y - c) * a[3]
            else:           # izquierda y arriba
                x = m[3] + (y - c) * a[3]
                y = m[0] + (x - c) * a[0]
        return np.array([x, y])

    esquinas = [esquina(3), esquina(0), esquina(1), esquina(2)]      # arriba-izq, arriba-der, abajo-der, abajo-izq
    pts = []
    for lado in range(4):
        P, Q = esquinas[lado], esquinas[(lado + 1) % 4]
        u = (Q - P) / np.linalg.norm(Q - P)
        n = np.array([-u[1], u[0]])                                     # hacia adentro, en sentido horario
        cortes = np.concatenate([[0.0], np.sort(rng.uniform(0.2, 0.8, int(rng.integers(1, 3)))), [1.0]])
        for i in range(len(cortes) - 1):
            escalon = rng.normal(0, 1.1) if i > 0 else 0.0
            desvio = rng.normal(0, 1.4)                                 # cada tramo con su propio ángulo, apenas
            pts.append(P + cortes[i] * (Q - P) + escalon * n)
            pts.append(P + cortes[i + 1] * (Q - P) + (escalon + desvio) * n)
    hoja = Polygon(pts).buffer(0)
    for e in esquinas:
        if rng.random() < 0.35:                                         # la esquina, cortada en diagonal
            corte = rng.uniform(24, 50)
            hacia = (np.array([c, c]) - e) / np.linalg.norm(np.array([c, c]) - e)
            linea = e + hacia * corte / np.sqrt(2)
            normal = np.array([-hacia[1], hacia[0]])
            triangulo = Polygon([e - hacia * 40, linea + normal * 80, linea - normal * 80])
            hoja = hoja.difference(triangulo)
    if hasattr(hoja, "geoms"):
        hoja = max(hoja.geoms, key=lambda g: g.area)
    return hoja


def hoja(rng):
    """Una hoja de papel de aluminio de cocina cortada a tijera, nunca del todo plana.

    Tiene arrugas grandes y suaves, el veteado del laminado y uno o dos pliegues; el filo
    del corte queda un poco levantado y agarra la luz.
    """
    contorno = np.array(tijera(rng).exterior.coords)
    m8 = np.zeros((T, T), np.uint8)
    cv2.fillPoly(m8, [np.round(contorno * 16).astype(np.int32)], 1, cv2.LINE_8, shift=4)
    mascara = m8.astype(bool)
    h = 0.22 * ruido((T, T), 70, rng) + 0.05 * ruido((T, T), 12, rng)
    vetas = rng.standard_normal((T, 1)).astype(np.float32) * np.ones((1, T), np.float32)
    vetas = cv2.GaussianBlur(vetas + 0.3 * rng.standard_normal((T, T)).astype(np.float32), (0, 0), sigmaX=30, sigmaY=0.7)
    h += 0.007 * vetas / (vetas.std() + 1e-9)
    for _ in range(2):
        h += _pliegue(rng, rng.uniform(0, 180), rng.uniform(0.03, 0.07), rng.uniform(2, 4), largo=rng.uniform(0.5, 1.2) * T)
    distancia = cv2.distanceTransform(m8, cv2.DIST_L2, 5)
    h += 0.16 * np.exp(-distancia / 2.5) * (1 + 0.5 * ruido((T, T), 8, rng))       # el filo levantado
    return h.astype(np.float32), mascara


def _pliegue(rng, angulo, alto, ancho, largo=None, centro=None):
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    cx, cy = centro if centro is not None else (rng.uniform(0.1, 0.9) * T, rng.uniform(0.1, 0.9) * T)
    a = np.radians(angulo)
    ux, uy = np.cos(a), np.sin(a)
    d = -(x - cx) * uy + (y - cy) * ux
    s = (x - cx) * ux + (y - cy) * uy
    d = d + 3.5 * ruido((T, T), 45, rng)                  # un pliegue de aluminio nunca es recto
    signo = rng.choice([-1, 1])
    perfil = signo * (alto * np.exp(-0.5 * (d / ancho) ** 2) + 0.25 * alto * np.tanh(d / 30))
    if largo is not None:
        perfil *= 1 / (1 + np.exp((np.abs(s) - largo / 2) / 12))
    return perfil


# ---------------------------------------------------------------- el repujado

def _espejo(q):
    """El calco dado vuelta (en mm): lo que en el anverso está a la izquierda, en el reverso está a la derecha."""
    r = np.array(q, np.float64)
    r[:, 0] = LADO_MM - r[:, 0]
    return r


def _repasar(lineas, mano, rng):
    """El calco dado vuelta y repasado por el reverso: la mano que repuja sigue la línea de grafito (no
    el contorno ideal) con su propio pulso. Trabaja en espejo (sus direcciones cómodas son las del
    reverso) y devuelve los tramos en el anverso, en mm, marcados el primero y el último de cada línea;
    también el largo del recorrido (mm) y el resumen de la mano."""
    tramos, largo, resumen = [], 0.0, dict(segundos=0.0, levantadas=0, dudas=0, lecturas=0)
    for linea in lineas:
        camino = unir(linea["tramos"]) if isinstance(linea, dict) else np.asarray(linea, np.float64)
        if len(camino) < 4:
            continue
        camino = _espejo(camino / PX_MM)
        largo += float(np.linalg.norm(np.diff(camino, axis=0), axis=1).sum())
        trs, r = trazar(camino, mano, rng)
        for k, tr in enumerate(trs):
            tr["xy"] = _espejo(tr["xy"])
            tr["primero"], tr["ultimo"] = k == 0, k == len(trs) - 1
        tramos += trs
        for clave in resumen:
            resumen[clave] += r[clave]
    return tramos, largo, resumen


FINO = 2                   # el surco se dibuja al doble y se reduce: el borde no salta de píxel en píxel


def _px(q):
    return (int(round(q[0] * PX_MM * FINO * 4)), int(round(q[1] * PX_MM * FINO * 4)))       # con shift=2


def _reducir(capa):
    return cv2.resize(capa, (T, T), interpolation=cv2.INTER_AREA)


def _surco_continuo(tramos):
    """El surco de una pasada de punzón, tramo por tramo: hunde según la presión; donde dos tramos se
    montan, el aluminio ya cedió y hunde un poco más. Donde el punzón descansa (al arrancar y al terminar
    cada línea, y en cada duda) queda un hoyuelo; donde retoma, uno chico."""
    surco = np.zeros((T * FINO, T * FINO), np.float32)
    for tr in tramos:
        uno = np.zeros_like(surco)
        q, p = tr["xy"], tr["p"]
        for i in range(len(q) - 1):
            cv2.line(uno, _px(q[i]), _px(q[i + 1]), float(p[i]), (ESTILETE_PX - 1) * FINO, cv2.LINE_AA, shift=2)
        firme = float(np.percentile(p, 75))
        descansos = [(q[idx], (1.04 + 0.08 * min(dur, 1.0)) * float(p[min(idx, len(p) - 1)])) for idx, dur in tr["pausas"]]
        descansos += [(q[0], (1.12 if tr["primero"] else 1.02) * firme)]
        descansos += [(q[-1], 1.12 * firme)] if tr["ultimo"] else []
        for centro, hondo in descansos:
            cv2.circle(uno, _px(centro), 3 * 4 * FINO, float(hondo), -1, cv2.LINE_AA, shift=2)
        surco = np.maximum(surco, uno) + 0.08 * np.minimum(surco, uno)
    return _reducir(surco)


def _surco_punteado(tramos, rng, minutos):
    """El punteado: cada punto, una presión de la bola. El paso no es parejo y la punta no cae justo
    sobre la línea (pulso.puntos)."""
    surco = np.zeros((T * FINO, T * FINO), np.float32)
    for x, y, p in puntos(tramos, rng, 2.25, minutos):
        cv2.circle(surco, _px((x, y)), int(round(2 * 4 * FINO * np.sqrt(p / 0.95))), float(p), -1, cv2.LINE_AA, shift=2)
    return _reducir(surco)


def repujar(trazos, punteado, rng, minutos=0.0, lado="las dos"):
    """Una placa, vista por el anverso: relieve, máscara, largo del recorrido en mm, si se rompió, cuánto
    tardó y qué hizo la mano.

    El perfil del surco es el de una bola apretada contra una base blanda: por el reverso,
    una canaleta redonda con dos lomas bajas a los lados (el aluminio que se corrió); por
    el anverso, al revés, una cresta entre dos cunetas. Hunde según la presión de la mano.
    Cerca del surco, la herramienta alisa las arrugas de la hoja. Cansada, la mano se
    equivoca más: la placa se rompe un poco más seguido, y donde más apretó.
    """
    h, mascara = hoja(rng)
    mano = Mano("puntear" if punteado else "repujar", lado, minutos)
    tramos, largo, resumen = _repasar(trazos, mano, rng)
    surco = _surco_punteado(tramos, rng, minutos) if punteado else _surco_continuo(tramos)
    cresta = cv2.GaussianBlur(surco, (0, 0), 2.0)
    ancho = cv2.GaussianBlur(surco, (0, 0), 5.5)
    relieve = 2.6 * cresta - 1.1 * np.clip(ancho - cresta, 0, None)
    alisado = np.clip(cv2.GaussianBlur(surco, (0, 0), 10) * 6, 0, 0.65)
    h = h * (1 - alisado) + relieve
    rota = rng.random() < (0.16 if punteado else 0.06) * (1 + 0.4 * cansancio(minutos))
    if rota:
        peso = (cresta.ravel().astype(np.float64) ** 6)
        i = rng.choice(peso.size, p=peso / peso.sum())          # donde más apretó
        ang = rng.uniform(0, np.pi)
        L = rng.uniform(15, 40)
        p0 = np.array([i % T, i // T], np.float32)
        p1 = p0 + L * np.array([np.cos(ang), np.sin(ang)])
        grieta = np.zeros((T, T), np.uint8)
        cv2.line(grieta, tuple(p0.astype(int)), tuple(p1.astype(int)), 255, 2, cv2.LINE_AA)
        labios = cv2.GaussianBlur(cv2.dilate(grieta, np.ones((5, 5), np.uint8)).astype(np.float32) / 255, (0, 0), 2)
        h = h + 0.35 * labios
        mascara = mascara & (grieta < 128)
    tarda = PREPARAR * rng.lognormal(0, 0.2) + resumen["segundos"] / 60 + RETIRAR
    return dict(altura=h.astype(np.float32), relieve=relieve.astype(np.float32), mascara=mascara, largo_mm=largo,
                rota=rota, minutos_intento=tarda, mano=dict(resumen, cansancio=round(cansancio(minutos), 3)))


def repujar_placa(trazos, punteado, celda, variante, minuto=0.0, lado="las dos"):
    """Hasta tres intentos: la placa rota no se tira, se cuenta y se hace otra. minuto es el de la
    sesión en que empieza la placa: cada intento la encuentra más cansada."""
    intentos, minutos, rotas, manos = 0, 0.0, [], []
    while True:
        intentos += 1
        rng = azar("repujar", celda, variante, intentos)
        p = repujar(trazos, punteado, rng, minuto + minutos, lado)
        minutos += p["minutos_intento"]
        manos.append(p["mano"])
        if p["rota"]:
            rotas.append(p)
        if not p["rota"] or intentos == 3:
            break
    pulso = dict(lado=lado, minuto=round(minuto, 1), cansancio=p["mano"]["cansancio"],
                 segundos_de_punzon=round(sum(m["segundos"] for m in manos), 1),
                 levantadas=sum(m["levantadas"] for m in manos), dudas=sum(m["dudas"] for m in manos),
                 lecturas=sum(m["lecturas"] for m in manos))
    p.update(intentos=intentos, roturas=len(rotas), minutos=round(minutos, 1), rotas=rotas, pulso=pulso)
    return p


def reverso(p):
    """La misma hoja dada vuelta: la letra al revés y hundida."""
    return dict(p, altura=-np.fliplr(p["altura"]), relieve=-np.fliplr(p["relieve"]), mascara=np.fliplr(p["mascara"]))


def foto_placa(p, rng):
    """Foto con luz rasante desde la izquierda (15°)."""
    return sombrear(p["altura"], p["mascara"], rng=rng)


def signo_final(rng):
    """Presiones de pulgar desde el reverso: dos a cuatro, porque una mano no acierta a la primera. Cada
    una un poco corrida y girada, más honda del lado de la yema que del lado de la palma; la hoja guarda
    lo más hondo de cada punto. La última deja la huella del dedo; alrededor, pliegues radiales."""
    h, mascara = hoja(rng)
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    cx0, cy0 = T / 2 + rng.normal(0, 10), T / 2 + rng.normal(0, 10)
    giro0 = rng.uniform(-25, -5)                          # el pulgar derecho entra inclinado
    domo = np.zeros((T, T), np.float32)
    n = int(rng.integers(2, 5))
    for k in range(n):
        cx, cy = (cx0, cy0) if k == 0 else (cx0 + rng.normal(0, 8), cy0 + rng.normal(0, 8))
        rot = np.radians(giro0 + rng.normal(0, 4))
        a, b = 92 * rng.uniform(0.92, 1.03), 122 * rng.uniform(0.92, 1.03)
        fuerza = 1.0 if k == 0 else rng.uniform(0.7, 1.0)
        xr = (x - cx) * np.cos(rot) + (y - cy) * np.sin(rot)
        yr = -(x - cx) * np.sin(rot) + (y - cy) * np.cos(rot)
        yr = yr * np.where(yr < 0, 1.1, 0.94)                 # la yema arriba hunde más parejo; la palma, menos
        r = np.sqrt((xr / a) ** 2 + (yr / b) ** 2)
        domo = np.maximum(domo, np.clip(1 - r ** 2, 0, 1) ** 1.5 * 5.0 * fuerza)
    theta = np.arctan2(yr, xr)
    rho = r * a + 5 * np.sin(2 * theta) + 3 * np.sin(theta) + 1.5 * ruido((T, T), 6, rng)
    crestas = 0.018 * np.sin(2 * np.pi * rho / 3.4) * np.clip(1 - r, 0, 1) * 2
    h = h + domo + crestas
    for _ in range(rng.integers(6, 11)):
        ang = rng.uniform(0, 360)
        c = (cx0 + 1.15 * 92 * np.cos(np.radians(ang)), cy0 + 1.15 * 122 * np.sin(np.radians(ang)))
        h += _pliegue(rng, ang, rng.uniform(0.08, 0.2), rng.uniform(1.2, 2.2), largo=rng.uniform(40, 110), centro=c)
    return dict(altura=h.astype(np.float32), relieve=domo.astype(np.float32), mascara=mascara, largo_mm=0.0, rota=False,
                intentos=1, roturas=0, minutos=round(2.0 + 0.5 * n, 1), rotas=[],
                pulso=dict(lado="derecha", presiones=n))
