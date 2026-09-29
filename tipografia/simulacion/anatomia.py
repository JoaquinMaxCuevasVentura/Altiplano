"""Anatomía de Contenida: lo que la obra le hace al esqueleto que da el pie.

Reemplazada por gramatica.py (03c_gramatica.md): la anatomía ya no se aplica al
final sobre la silueta del testigo, sino antes, en vectores. Este archivo queda
como registro de la primera versión (03b_anatomia.md); simular.py ya no lo usa.

Del pie se toma el esqueleto: dónde va cada trazo y cuánto mide. La anatomía
la dicta la obra (03b_anatomia.md). Estas funciones la aplican a las máscaras
de la simulación, en este orden:

  1. la retícula: base y altura de x caen en líneas de media tesela;
  2. la lluvia: la erosión baja desde arriba y se lleva primero los remates altos;
  3. la bandeja: la mitad baja de cada ojo toma el perfil de la bandeja;
  4. las gotas: los terminales que miran hacia abajo gotean;
  5. los puntos: cuadrados de media tesela, como la cinta que tapaba;
  6. las tildes: gotas;
  7. el asta: la letra se corre hasta que su asta principal cae en una línea de media tesela;
  8. las cifras: cada una dentro de una celda de la cabeza del ídolo.

El canal (la letra es hueca: se dibuja su contorno) y el desagüe (cada
contorno se abre en su punto más bajo) se aplican al calcar, en
desenterrar.contornos_temblorosos.
"""

import cv2
import numpy as np

from comun import T, TES, TRAPECIO, caja_tinta, componentes, mover

MEDIA = TES / 2
PUNTOS = "ij."          # los que tienen puntos en el pie; los demás los heredan al reconstruirse
TILDADAS = "áéíóú"


# ---------------------------------------------------------------- 1. la retícula

def ajustar_metricas(M, med):
    """Todo el juego se escala y se corre para que base y altura de x caigan en líneas de media tesela."""
    base_t = (T - med["base"]) / TES
    base_obj = round(base_t * 2) / 2
    xh_obj = max(MEDIA, round(med["xh"] / MEDIA) * MEDIA)
    f = xh_obj / med["xh"]
    base_px = T - base_obj * TES
    A = np.float32([[f, 0, T / 2 - f * T / 2], [0, f, base_px - f * med["base"]]])
    out = {k: cv2.warpAffine(m.astype(np.float32), A, (T, T)) > 0.5 for k, m in M.items()}
    return out, base_px, dict(base_de=round(float(base_t), 2), base_a=base_obj,
                              x_de=round(float(med["xh"] / TES), 2), x_a=xh_obj / TES)


# ---------------------------------------------------------------- 2. la lluvia

def llover(m, base, alto, pasos=6, sigma=3.0, sesgo=0.12):
    """Redondea todo, y gasta más cuanto más arriba: la lluvia corre de arriba hacia abajo."""
    y = np.arange(T, dtype=np.float32)[:, None]
    altura = np.clip((base - y) / max(alto, 1), 0, 1)
    f = m.astype(np.float32)
    for _ in range(pasos):
        g = cv2.GaussianBlur(f, (0, 0), sigma)
        f = (g > 0.5 + sesgo * altura).astype(np.float32)
    return f > 0.5


# ---------------------------------------------------------------- 3. la bandeja

def bandejas(m, pared_min=9, k=TRAPECIO):
    """La mitad baja de cada ojo: paredes rectas que se cierran hacia abajo (0,70) y fondo con media caña."""
    fondo = (~m).astype(np.uint8)
    n, et, st, _ = cv2.connectedComponentsWithStats(fondo, connectivity=4)
    out = m.copy()
    marcas = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if x == 0 or y == 0 or x + w >= T or y + h >= T or area < 300:
            continue
        hueco = et == i
        cy = int(y + h // 2)
        fila = np.nonzero(hueco[cy])[0]
        if len(fila) < 4:
            continue
        xa, xb = fila.min(), fila.max()
        cx, w0 = (xa + xb) / 2, (xb - xa) / 2
        fy = y + h - 1
        r = 0.2 * (fy - cy)
        wb = max(k * w0, r + 1)
        pts = [(cx - w0, cy), (cx - wb, fy - r)]
        pts += [(cx - wb + r + r * np.cos(a), fy - r + r * np.sin(a)) for a in np.linspace(np.pi, np.pi / 2, 10)]
        pts += [(cx + wb - r + r * np.cos(a), fy - r + r * np.sin(a)) for a in np.linspace(np.pi / 2, 0, 10)]
        pts += [(cx + wb, fy - r), (cx + w0, cy)]
        poli = np.zeros((T, T), np.uint8)
        cv2.fillPoly(poli, [np.round(np.array(pts) * 4).astype(np.int32)], 1, cv2.LINE_AA, shift=2)
        filas = np.arange(T)[:, None]
        nuevo = (hueco & (filas <= cy)) | ((poli > 0) & (filas > cy))
        lleno = out | hueco
        dist = cv2.distanceTransform(lleno.astype(np.uint8), cv2.DIST_L2, 5)
        nuevo &= dist > pared_min
        out = lleno & ~nuevo
        # por fuera, la panza se asienta plana: el fondo de la piscina, con su media caña
        c = int(round(cx))
        fy_fuera = fy + 1
        while fy_fuera + 1 < T and out[fy_fuera + 1, c]:
            fy_fuera += 1
        izq = xa
        while izq - 1 >= 0 and out[cy, izq - 1]:
            izq -= 1
        der = xb
        while der + 1 < T and out[cy, der + 1]:
            der += 1
        wo = k * (der - izq) / 2
        if fy_fuera > fy + 2 and wo > 4:
            rb = min(10, (fy_fuera - fy) / 2)
            base = np.zeros((T, T), np.uint8)
            x0b, x1b = cx - wo, cx + wo
            pts = [(x0b, fy + 1), (x1b, fy + 1), (x1b, fy_fuera - rb)]
            pts += [(x1b - rb + rb * np.cos(a), fy_fuera - rb + rb * np.sin(a)) for a in np.linspace(0, np.pi / 2, 6)]
            pts += [(x0b + rb + rb * np.cos(a), fy_fuera - rb + rb * np.sin(a)) for a in np.linspace(np.pi / 2, np.pi, 6)]
            cv2.fillPoly(base, [np.round(np.array(pts) * 4).astype(np.int32)], 1, cv2.LINE_AA, shift=2)
            out |= (base > 0) & ~nuevo
        marcas.append((float(cx), float(fy)))
    return out, marcas


# ---------------------------------------------------------------- 4. las gotas

def _recorrer(esq, p, n):
    """Camina por el esqueleto desde un extremo; se detiene al llegar a una bifurcación."""
    camino, vistos = [p], {p}
    for _ in range(n):
        y, x = camino[-1]
        if len(camino) > 1 and esq[max(0, y - 1):y + 2, max(0, x - 1):x + 2].sum() - 1 >= 3:
            break
        siguiente = None
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                q = (y + dy, x + dx)
                if q != (y, x) and q not in vistos and 0 <= q[0] < T and 0 <= q[1] < T and esq[q]:
                    siguiente = q
                    break
            if siguiente:
                break
        if siguiente is None:
            break
        vistos.add(siguiente)
        camino.append(siguiente)
    return camino


def gotas(m, base, xh, fino, grueso):
    """Donde un trazo termina mirando hacia abajo, en el aire, cuelga una gota."""
    from skimage.morphology import skeletonize
    partes = componentes(m)
    if not partes:
        return m, []
    mayor = max(st[4] for _, st, _ in partes)
    cuerpo = np.zeros_like(m)
    for c, st, _ in partes:
        if st[4] >= 0.25 * mayor:        # las tildes y los puntos no gotean: ya son gotas y teselas
            cuerpo |= c
    esq = skeletonize(cuerpo)
    vecinos = cv2.filter2D(esq.astype(np.float32), -1, np.ones((3, 3), np.float32)) - esq
    ys, xs = np.nonzero(esq & (np.round(vecinos) == 1))
    out = m.astype(np.uint8)
    marcas = []
    for y, x in zip(ys, xs):
        if y > base - 0.12 * xh:         # pies y colas bajo la línea: no
            continue
        camino = _recorrer(esq, (int(y), int(x)), 30)
        if len(camino) < 30:             # una rama corta es una rebaba del borde, no un terminal
            continue
        dy, dx = y - camino[-1][0], x - camino[-1][1]
        L = np.hypot(dy, dx)
        if L == 0 or dy / L < 0.35:      # no mira hacia abajo
            continue
        yb = int(y)
        while yb + 1 < T and m[yb + 1, x]:
            yb += 1
        libre = 0
        while yb + libre + 1 < T and not m[yb + libre + 1, x] and libre < 0.45 * TES:
            libre += 1
        if libre < 18:                   # no hay lugar para caer
            continue
        largo = min(0.3 * TES, libre - grueso * 0.8)
        if largo < 6:
            continue
        cv2.line(out, (int(x), yb), (int(x), int(yb + largo)), 1, max(2, int(fino * 0.55)))
        cv2.circle(out, (int(x), int(yb + largo + grueso * 0.3)), max(4, int(grueso * 0.38)), 1, -1)
        marcas.append((float(x), float(yb + largo)))
    return out > 0, marcas


# ---------------------------------------------------------------- 5 y 6. puntos y tildes

def _perimetro(c):
    cont, _ = cv2.findContours(c.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return sum(cv2.arcLength(k, True) for k in cont) or 1.0


def puntos_en_teselas(m, xh):
    """Todo punto redondo se vuelve un cuadrado de media tesela: la tesela del piso, la cinta que tapaba."""
    out = m.copy()
    marcas = []
    for c, st, cen in componentes(m):
        x, y, w, h, area = st
        if w > 0.32 * xh or h > 0.32 * xh:
            continue
        circ = 4 * np.pi * area / _perimetro(c) ** 2
        if circ < 0.6:
            continue
        out &= ~c
        s = MEDIA
        out[int(cen[1] - s / 2):int(cen[1] + s / 2), int(cen[0] - s / 2):int(cen[0] + s / 2)] = True
        marcas.append((float(cen[0]), float(cen[1])))
    return out, marcas


def tildes_en_gotas(m, base, xh):
    """La tilde, que marca dónde carga la voz, se vuelve una gota que cae: la punta arriba, el peso abajo."""
    out = m.copy()
    marcas = []
    linea = base - xh * 1.08
    for c, st, cen in componentes(m):
        x, y, w, h, area = st
        if cen[1] >= linea or area / max(w * h, 1) > 0.9:
            continue
        ys, xs = np.nonzero(c)
        pts = np.stack([xs, ys], 1).astype(np.float32)
        media = pts.mean(0)
        _, vecs = np.linalg.eigh(np.cov((pts - media).T))
        v = vecs[:, 1]
        proy = (pts - media) @ v
        a, b = media + v * proy.min(), media + v * proy.max()
        arriba, abajo = (a, b) if a[1] < b[1] else (b, a)
        L = float(np.linalg.norm(abajo - arriba))
        if L < 8:
            continue
        u = (abajo - arriba) / L
        r = max(7.0, 0.22 * L)
        centro = abajo - u * r
        perp = np.array([-u[1], u[0]])
        gota = np.zeros((T, T), np.uint8)
        cv2.circle(gota, (int(round(centro[0])), int(round(centro[1]))), int(round(r)), 1, -1, cv2.LINE_AA)
        tri = np.array([arriba, centro + perp * r * 0.96, centro - perp * r * 0.96])
        cv2.fillPoly(gota, [np.round(tri).astype(np.int32)], 1, cv2.LINE_AA)
        out = (out & ~c) | (gota > 0)
        marcas.append((float(centro[0]), float(centro[1])))
    return out, marcas


# ---------------------------------------------------------------- 7. el asta

def _corrida_vertical(m):
    out = np.zeros(m.shape[1], int)
    for x in np.nonzero(m.any(axis=0))[0]:
        d = np.diff(np.concatenate([[0], m[:, x].astype(np.int8), [0]]))
        out[x] = (np.nonzero(d == -1)[0] - np.nonzero(d == 1)[0]).max()
    return out


def apoyar(m, xh):
    """Si la letra tiene un asta, se corre hasta que el asta cae en una línea de media tesela."""
    corridas = _corrida_vertical(m)
    if corridas.max() < 0.8 * xh:
        return m, None, 0.0
    cols = np.nonzero(corridas >= 0.85 * corridas.max())[0]
    grupos = np.split(cols, np.nonzero(np.diff(cols) > 1)[0] + 1)
    cx = (grupos[0][0] + grupos[0][-1]) / 2
    obj = round(cx / MEDIA) * MEDIA
    return mover(m, obj - cx, 0), float(obj), float(obj - cx)


# ---------------------------------------------------------------- 8. las cifras

CIFRAS = "0123456789"


def enmarcar_cifras(R, fino):
    """Cada cifra dentro de una celda: el calendario que nadie leyó vuelve como cifra contenida."""
    presentes = [c for c in CIFRAS if c in R]
    if not presentes:
        return R
    arriba = max(4, min(caja_tinta(R[c])[1] for c in presentes) - 0.3 * TES)
    abajo = min(T - 5, max(caja_tinta(R[c])[3] for c in presentes) + 0.3 * TES)
    x0, x1 = T / 2 - 2 * TES, T / 2 + 2 * TES
    g = max(6, int(fino * 0.7))
    marco = np.zeros((T, T), bool)
    marco[int(arriba):int(abajo), int(x0):int(x1)] = True
    marco[int(arriba + g):int(abajo - g), int(x0 + g):int(x1 - g)] = False
    return {k: (v | marco if k in presentes else v) for k, v in R.items()}


# ---------------------------------------------------------------- aplicar

def anatomia_de_lo_hallado(M, med):
    base, xh, fino, grueso = med["base"], med["xh"], med["fino"], med["grueso"]
    out, marcas = {}, {}
    for s, m in M.items():
        mk = {}
        m = llover(m, base, med["asc"])
        m, mk["bandejas"] = bandejas(m, pared_min=max(8, fino * 0.45))
        m, mk["gotas"] = gotas(m, base, xh, fino, grueso)
        if s in PUNTOS:
            m, mk["puntos"] = puntos_en_teselas(m, xh)
        if s in TILDADAS:
            m, mk["tildes"] = tildes_en_gotas(m, base, xh)
        out[s], marcas[s] = m, mk
    return out, marcas


def anatomia_de_lo_reconstruido(R, med):
    """Las reconstruidas heredan la anatomía de las partes de donde salen; los ojos nuevos, la bandeja."""
    out, marcas = {}, {}
    for s, m in R.items():
        m, b = bandejas(m, pared_min=max(8, med["fino"] * 0.45))
        out[s], marcas[s] = m, {"bandejas": b}
    return out, marcas


def apoyar_todo(M, R, xh, marcas):
    """Corre cada letra hasta la retícula y corre también sus marcas de anatomía."""
    astas = {}
    for dic in (M, R):
        for s in list(dic):
            dic[s], x, dx = apoyar(dic[s], xh)
            astas[s] = x
            for k, lista in marcas.get(s, {}).items():
                marcas[s][k] = [(px + dx, py) for px, py in lista]
    return M, R, astas
