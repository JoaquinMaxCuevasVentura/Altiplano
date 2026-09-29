"""Cuaderno 2 · Contener: acciones 4 a 7, simuladas.

Acción 4: el repujado. El calco se da vuelta (espejo) y se repasa por el
reverso de una hoja de papel de aluminio con un punzón de 1 mm: la mano que
repuja tiembla distinto de la que calcó. Lo hallado es un surco continuo; lo
reconstruido, puntos. El punteado perfora: las placas reconstruidas se rompen
más. Si una placa se rompe, se guarda y se hace otra.
Acción 5: la caja abierta y cerrada.
Acción 6: la placa vestida el tiempo de un bucle; deja pliegues que siguen el
eje de la parte del cuerpo, y después se aplana solo con la palma.
Acción 7: el signo final. La máquina no tiene dedos: simula una sola presión
de un pulgar genérico.
"""

import cv2
import numpy as np

from comun import BUCLE_MIN, T, azar, ruido, ruido_1d, sombrear

ESTILETE_PX = 4            # punzón de 1 mm
PARTES = [("antebrazo", 0), ("esternón", 5), ("cadera", 35), ("muslo", 0), ("espalda", 85), ("hombro", 50)]


def hoja(rng):
    """Una hoja de papel de aluminio de cocina cortada a tijera, nunca del todo plana."""
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    m = 14 + 1.8 * ruido((T, T), 40, rng)
    r = 26
    dx = np.maximum(np.maximum(m - x, x - (T - 1 - m)), 0)
    dy = np.maximum(np.maximum(m - y, y - (T - 1 - m)), 0)
    mascara = (dx == 0) & (dy == 0)
    for fx in (False, True):
        for fy in (False, True):
            xx = T - 1 - x if fx else x
            yy = T - 1 - y if fy else y
            fuera = (xx < m + r) & (yy < m + r) & ((xx - (m + r)) ** 2 + (yy - (m + r)) ** 2 > r * r)
            mascara &= ~fuera
    h = 0.22 * ruido((T, T), 70, rng) + 0.05 * ruido((T, T), 12, rng)
    vetas = rng.standard_normal((T, 1)).astype(np.float32) * np.ones((1, T), np.float32)
    vetas = cv2.GaussianBlur(vetas + 0.3 * rng.standard_normal((T, T)).astype(np.float32), (0, 0), sigmaX=30, sigmaY=0.7)
    h += 0.007 * vetas / (vetas.std() + 1e-9)
    for _ in range(2):
        h += _pliegue(rng, rng.uniform(0, 180), rng.uniform(0.03, 0.07), rng.uniform(2, 4), largo=rng.uniform(0.5, 1.2) * T)
    return h.astype(np.float32), mascara


def _pliegue(rng, angulo, alto, ancho, largo=None, centro=None):
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    cx, cy = centro if centro is not None else (rng.uniform(0.1, 0.9) * T, rng.uniform(0.1, 0.9) * T)
    a = np.radians(angulo)
    ux, uy = np.cos(a), np.sin(a)
    d = -(x - cx) * uy + (y - cy) * ux
    s = (x - cx) * ux + (y - cy) * uy
    d = d + 3.5 * _ondulacion(rng)
    signo = rng.choice([-1, 1])
    perfil = signo * (alto * np.exp(-0.5 * (d / ancho) ** 2) + 0.25 * alto * np.tanh(d / 30))
    if largo is not None:
        perfil *= 1 / (1 + np.exp((np.abs(s) - largo / 2) / 12))
    return perfil


def _ondulacion(rng):
    """Un pliegue de aluminio nunca es recto: se ondula un poco."""
    return ruido((T, T), 45, rng)


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
    """Una placa: relieve, máscara, largo del recorrido en mm y si se rompió."""
    h, mascara = hoja(rng)
    surco = np.zeros((T, T), np.float32)
    largo = 0.0
    for q in _repasar(trazos, rng):
        cerr = q                      # el punzón se detiene en el desagüe: la línea queda abierta
        seg = np.linalg.norm(np.diff(cerr, axis=0), axis=1)
        largo += seg.sum()
        presion = np.clip(0.95 + 0.18 * ruido_1d(len(cerr), 25, rng), 0.6, 1.3)
        if punteado:
            s = np.concatenate([[0], np.cumsum(seg)])
            for t_ in np.arange(rng.uniform(0, 9), s[-1], 9.0):
                i = min(np.searchsorted(s, t_), len(cerr) - 1)
                p = cerr[i] + rng.normal(0, 0.6, 2)
                cv2.circle(surco, (int(round(p[0] * 4)), int(round(p[1] * 4))), 2 * 4, float(presion[i]), -1, cv2.LINE_AA, shift=2)
        else:
            pts = np.round(cerr * 4).astype(np.int32)
            for i in range(len(pts) - 1):
                cv2.line(surco, tuple(pts[i]), tuple(pts[i + 1]), float(presion[i]), ESTILETE_PX - 1, cv2.LINE_AA, shift=2)
    relieve = cv2.GaussianBlur(surco, (0, 0), 2.2) * 2.6
    h = h + relieve
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
    return dict(altura=h, relieve=relieve, mascara=mascara, largo_mm=largo / 4, rota=rota)


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


def foto_placa(p, rng):
    return sombrear(p["altura"], p["mascara"], rng=rng)


def vestir(p, parte, angulo, minutos, rng):
    """La placa sobre el cuerpo el tiempo de un bucle; después se aplana con la palma."""
    y, x = np.mgrid[0:T, 0:T].astype(np.float32)
    dx = (x + 6 * ruido((T, T), 90, rng)).astype(np.float32)
    dy = (y + 6 * ruido((T, T), 90, rng)).astype(np.float32)
    h = cv2.remap(p["altura"], dx, dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    relieve = cv2.remap(p["relieve"], dx, dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    mascara = cv2.remap(p["mascara"].astype(np.float32), dx, dy, cv2.INTER_LINEAR) > 0.5
    n = 3 + int(minutos // 2) + int(rng.integers(0, 3))
    pliegues = np.zeros((T, T), np.float32)
    for _ in range(n):
        ang = angulo + rng.normal(0, 18) if rng.random() < 0.7 else rng.uniform(0, 180)
        pliegues += _pliegue(rng, ang, rng.uniform(0.2, 0.5), rng.uniform(2.0, 4.5), largo=rng.uniform(0.4, 1.2) * T)
    for _ in range(rng.integers(4, 10)):
        borde = rng.choice(4)
        t_ = rng.uniform(0.05, 0.95) * T
        centro = [(t_, 20), (t_, T - 20), (20, t_), (T - 20, t_)][borde]
        ang = (90 if borde < 2 else 0) + rng.normal(0, 20)
        pliegues += _pliegue(rng, ang, rng.uniform(0.1, 0.3), rng.uniform(1, 2), largo=rng.uniform(30, 80), centro=centro)
    h = h + pliegues
    return dict(altura=h, relieve=relieve, pliegues=pliegues, mascara=mascara, parte=parte, minutos=minutos, n_pliegues=n)


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
    for k in range(rng.integers(6, 11)):
        ang = rng.uniform(0, 360)
        c = (cx + 1.15 * a * np.cos(np.radians(ang)), cy + 1.15 * b * np.sin(np.radians(ang)))
        h += _pliegue(rng, ang, rng.uniform(0.08, 0.2), rng.uniform(1.2, 2.2), largo=rng.uniform(40, 110), centro=c)
    relieve = domo
    return dict(altura=h, relieve=relieve, mascara=mascara, largo_mm=0.0, rota=False, intentos=1, roturas=0,
                minutos=3.0, rotas=[])


def sesiones_de_vestir(placas):
    """Reparte las placas en sesiones de seis, cada una en una parte del cuerpo."""
    asignacion = {}
    for i, clave in enumerate(placas):
        parte, ang = PARTES[(i // 6) % len(PARTES)]
        asignacion[clave] = (parte, ang, BUCLE_MIN, i // 6 + 1)
    return asignacion


def caja_abierta(fotos, poliza, celdas, rng, lado=150, j=18):
    """La caja de cartón abierta: en cada compartimento, la pila de placas de su signo."""
    col, fil = 8, 7
    W, H = col * lado + (col + 1) * j, fil * lado + (fil + 1) * j
    carton = 0.46 + 0.03 * ruido((H, W), 1.2, rng) + 0.04 * ruido((H, W), 40, rng)
    img = np.dstack([carton * 1.02, carton * 0.97, carton * 0.9])
    for c in celdas:
        x = j + (c["columna"] - 1) * (lado + j)
        yy = j + (c["fila"] - 1) * (lado + j)
        img[yy:yy + lado, x:x + lado] *= 0.55
        n = poliza.get(c["signo"], 1)
        for k in range(min(n, 3) - 1, -1, -1):
            f = fotos.get((c["celda"], k + 1))
            if f is None:
                continue
            ang = rng.normal(0, 3)
            chica = cv2.resize(f, (lado - 14, lado - 14), interpolation=cv2.INTER_AREA)
            M = cv2.getRotationMatrix2D(((lado - 14) / 2, (lado - 14) / 2), ang, 1.0)
            M[:, 2] += [7 + k * 3, 7 + k * 3]
            rot = cv2.warpAffine(chica, M, (lado, lado), borderValue=0)
            alfa = cv2.warpAffine(np.ones_like(chica), M, (lado, lado), borderValue=0)
            sub = img[yy:yy + lado, x:x + lado]
            sub[:] = sub * (1 - alfa[..., None]) + np.dstack([rot] * 3) * alfa[..., None]
    return np.clip(img, 0, 1)


def caja_cerrada(foto_coma, rng, lado=150, j=18):
    """La tapa, con una sola puerta calada sobre la celda 1: se ve la coma."""
    col, fil = 8, 7
    W, H = col * lado + (col + 1) * j, fil * lado + (fil + 1) * j
    carton = 0.5 + 0.03 * ruido((H, W), 1.2, rng) + 0.05 * ruido((H, W), 50, rng)
    img = np.dstack([carton * 1.02, carton * 0.97, carton * 0.9])
    x, y = j, j
    puerta = cv2.resize(foto_coma, (lado, lado), interpolation=cv2.INTER_AREA)
    img[y:y + lado, x:x + lado] = np.dstack([puerta] * 3) * 0.85
    img[y:y + 6, x:x + lado] *= 0.55
    img[y:y + lado, x:x + 6] *= 0.6
    return np.clip(img, 0, 1)
