"""Cuaderno 2 · Contener: la placa (acción 4), simulada.

El calco se da vuelta (espejo) y se repasa por el reverso de una hoja de papel de
aluminio de cocina, cortada a tijera, con un punzón de bola de 1 mm sobre una base
blanda. La mano que repuja tiembla distinto de la que calcó. Por el reverso queda
un surco: la letra al revés, hundida, un canal que podría contener agua. Por el
anverso, un relieve que se lee. Lo hallado es un surco continuo; lo reconstruido,
puntos. El punteado perfora: las placas reconstruidas se rompen más. Si una placa
se rompe, se guarda y se hace otra.

El signo final: la máquina no tiene dedos. Simula una sola presión de un pulgar
genérico.
"""

import cv2
import numpy as np
from shapely.geometry import Polygon

from comun import T, azar, ruido, ruido_1d, sombrear

ESTILETE_PX = 4            # punzón de bola de 1 mm


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

def _repasar(trazos, rng):
    """El calco dado vuelta y repasado por el reverso: la mano que repuja agrega su temblor."""
    out = []
    for q in trazos:
        r = q.copy()
        r[:, 0] = T - 1 - r[:, 0]
        tang = np.roll(r, -1, 0) - np.roll(r, 1, 0)
        n = np.stack([-tang[:, 1], tang[:, 0]], 1)
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
        r = r + n * (1.0 * ruido_1d(len(r), 10, rng))[:, None]
        r[:, 0] = T - 1 - r[:, 0]
        out.append(r)
    return out


def repujar(trazos, punteado, rng):
    """Una placa, vista por el anverso: relieve, máscara, largo del recorrido en mm y si se rompió.

    El perfil del surco es el de una bola apretada contra una base blanda: por el reverso,
    una canaleta redonda con dos lomas bajas a los lados (el aluminio que se corrió); por
    el anverso, al revés, una cresta entre dos cunetas. Donde la mano arranca y donde se
    detiene, el punzón descansa y hunde un poco más. Cerca del surco, la herramienta alisa
    las arrugas de la hoja.
    """
    h, mascara = hoja(rng)
    surco = np.zeros((T, T), np.float32)
    largo = 0.0
    for q in _repasar(trazos, rng):
        seg = np.linalg.norm(np.diff(q, axis=0), axis=1)
        largo += seg.sum()
        presion = np.clip(0.95 + 0.18 * ruido_1d(len(q), 25, rng), 0.6, 1.3)
        if punteado:
            s = np.concatenate([[0], np.cumsum(seg)])
            for t_ in np.arange(rng.uniform(0, 9), s[-1], 9.0):
                i = min(np.searchsorted(s, t_), len(q) - 1)
                p = q[i] + rng.normal(0, 0.6, 2)
                cv2.circle(surco, (int(round(p[0] * 4)), int(round(p[1] * 4))), 2 * 4, float(presion[i]), -1, cv2.LINE_AA, shift=2)
        else:
            pts = np.round(q * 4).astype(np.int32)
            for i in range(len(pts) - 1):
                cv2.line(surco, tuple(pts[i]), tuple(pts[i + 1]), float(presion[i]), ESTILETE_PX - 1, cv2.LINE_AA, shift=2)
            for extremo, pr in ((q[0], presion[0]), (q[-1], presion[-1])):      # donde el punzón descansa
                cv2.circle(surco, (int(round(extremo[0] * 4)), int(round(extremo[1] * 4))), 3 * 4, float(1.35 * pr), -1,
                           cv2.LINE_AA, shift=2)
    cresta = cv2.GaussianBlur(surco, (0, 0), 2.0)
    ancho = cv2.GaussianBlur(surco, (0, 0), 5.5)
    relieve = 2.6 * cresta - 1.1 * np.clip(ancho - cresta, 0, None)
    alisado = np.clip(cv2.GaussianBlur(surco, (0, 0), 10) * 6, 0, 0.65)
    h = h * (1 - alisado) + relieve
    rota = rng.random() < (0.16 if punteado else 0.06)
    if rota:
        ys, xs = np.nonzero(surco > 0.5)
        i = rng.integers(len(xs))
        ang = rng.uniform(0, np.pi)
        L = rng.uniform(15, 40)
        p0 = np.array([xs[i], ys[i]], np.float32)
        p1 = p0 + L * np.array([np.cos(ang), np.sin(ang)])
        grieta = np.zeros((T, T), np.uint8)
        cv2.line(grieta, tuple(p0.astype(int)), tuple(p1.astype(int)), 255, 2, cv2.LINE_AA)
        labios = cv2.GaussianBlur(cv2.dilate(grieta, np.ones((5, 5), np.uint8)).astype(np.float32) / 255, (0, 0), 2)
        h = h + 0.35 * labios
        mascara = mascara & (grieta < 128)
    return dict(altura=h.astype(np.float32), relieve=relieve.astype(np.float32), mascara=mascara, largo_mm=largo / 4,
                rota=rota)


def repujar_placa(trazos, punteado, celda, variante):
    """Hasta tres intentos: la placa rota no se tira, se cuenta y se hace otra."""
    intentos, minutos, rotas = 0, 0.0, []
    while True:
        intentos += 1
        rng = azar("repujar", celda, variante, intentos)
        p = repujar(trazos, punteado, rng)
        minutos += 4 + p["largo_mm"] / (9 if punteado else 20) + rng.normal(0, 1.5)
        if p["rota"]:
            rotas.append(p)
        if not p["rota"] or intentos == 3:
            break
    p.update(intentos=intentos, roturas=len(rotas), minutos=round(max(minutos, 5), 1), rotas=rotas)
    return p


def reverso(p):
    """La misma hoja dada vuelta: la letra al revés y hundida."""
    return dict(p, altura=-np.fliplr(p["altura"]), relieve=-np.fliplr(p["relieve"]), mascara=np.fliplr(p["mascara"]))


def foto_placa(p, rng):
    """Foto con luz rasante desde la izquierda (15°)."""
    return sombrear(p["altura"], p["mascara"], rng=rng)


def signo_final(rng):
    """Una presión de pulgar desde el reverso: sale un domo con crestas finas y pliegues radiales."""
    h, mascara = hoja(rng)
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    cx, cy = T / 2 + rng.normal(0, 10), T / 2 + rng.normal(0, 10)
    a, b = 92, 122
    rot = np.radians(rng.uniform(-15, 15))
    xr = (x - cx) * np.cos(rot) + (y - cy) * np.sin(rot)
    yr = -(x - cx) * np.sin(rot) + (y - cy) * np.cos(rot)
    r = np.sqrt((xr / a) ** 2 + (yr / b) ** 2)
    domo = np.clip(1 - r ** 2, 0, 1) ** 1.5 * 5.0
    theta = np.arctan2(yr, xr)
    rho = r * a + 5 * np.sin(2 * theta) + 3 * np.sin(theta) + 1.5 * ruido((T, T), 6, rng)
    crestas = 0.018 * np.sin(2 * np.pi * rho / 3.4) * np.clip(1 - r, 0, 1) * 2
    h = h + domo + crestas
    for _ in range(rng.integers(6, 11)):
        ang = rng.uniform(0, 360)
        c = (cx + 1.15 * a * np.cos(np.radians(ang)), cy + 1.15 * b * np.sin(np.radians(ang)))
        h += _pliegue(rng, ang, rng.uniform(0.08, 0.2), rng.uniform(1.2, 2.2), largo=rng.uniform(40, 110), centro=c)
    return dict(altura=h.astype(np.float32), relieve=domo.astype(np.float32), mascara=mascara, largo_mm=0.0, rota=False,
                intentos=1, roturas=0, minutos=3.0, rotas=[])
