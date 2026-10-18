"""El pulso: la mano (y la voz) de una persona, no la de una máquina.

Hasta aquí la simulación temblaba con un ruido parejo a lo largo del recorrido: «no cansa, no
duda, no se distrae» (informe, «Lo que la máquina no sabe»). Una mano que calca, repuja, encinta
o frota hace otra cosa:

- **Levanta la herramienta.** Un contorno largo se hace en tramos. Al retomar, el tramo nuevo
  se monta sobre el anterior o deja un hueco chico. Levanta más en las esquinas y cuando el
  recorrido la obliga a empujar en lugar de tirar (ahí, además, gira la hoja).
- **Cambia de velocidad.** Arranca y frena en cada tramo, y va más despacio en las curvas: la
  ley de los dos tercios (la velocidad cae con la curvatura a la potencia −1/3). Donde levanta
  para seguir, levanta andando: la línea se afina en una cola.
- **Sigue el calco con retardo.** Redondea las esquinas y a veces se pasa un poco y vuelve.
- **Se desvía y se corrige.** Una deriva lenta que vuelve hacia la línea, en el tiempo y no en
  el espacio: cuanto más despacio va, más se nota.
- **Tiembla a su frecuencia.** El temblor fisiológico, de 8 a 12 Hz, con una amplitud que va y
  viene. Cansada, aparece otro más lento, de 4 a 6 Hz.
- **Duda.** Se detiene un momento y sigue. Donde se detiene, el punzón hunde más.
- **Aprieta distinto.** Entra y sale de la hoja de a poco, aprieta más cuando va despacio y la
  presión respira.
- **Tiene direcciones cómodas.** La derecha tira bien hacia abajo y a la izquierda, y empuja peor
  hacia arriba y a la derecha; la izquierda, al revés. Con las dos manos (el punzón en la derecha),
  la otra lee el anverso cada tanto (Acción 4): más pausas.
- **Se cansa.** Con los minutos de la sesión tiembla más, se desvía más, aprieta menos, va más
  lento y levanta más seguido.

Frotar tampoco es parejo: la mano va y viene en diagonal, cada pasada aprieta distinto, se carga
donde frena para volver y frota por parches, lo que alcanza el brazo; donde dos parches se montan,
el papel se frota dos veces. Un dedo nunca toca el agua en el mismo punto ni con la misma fuerza.
La voz no es un metrónomo: las sílabas duran distinto, se detiene en las comas y al final del
verso, la altura baja a lo largo de la frase y tiembla un poco.

Es una mano cuidadosa: todo es sutil, se ve de cerca y no a primera vista. Todo tiene semilla: la
misma mano, la misma sesión y la misma placa dan el mismo trazo; otra semilla es otra mano. Son supuestos de la motricidad, no medidas de tu pulso: se confrontan con
las placas y las fotos reales (informe, «Cómo confrontar»).
"""

import math
import re
from dataclasses import dataclass

import cv2
import numpy as np
from scipy.signal import bilinear, lfilter, lfilter_zi

# Cada oficio, su mano. v: mm/s en lo recto; deriva: mm (cuánto se aparta del calco); tau: s (cuánto
# tarda en volver); temblor: mm (el fisiológico, con la punta apoyada: el roce del aluminio lo frena);
# tramo: mm (cuánto recorre antes de levantar);
# duda: dudas por segundo; presion: la de base; seguir: Hz (qué tan rápido sigue lo que mira); monta: qué
# tan seguido, al retomar, se monta sobre lo hecho en lugar de dejar un hueco (y el hueco, en mm). El
# punzón busca el surco que dejó: se monta más seguido que el lápiz. esquina: qué tan seguido levanta
# en una esquina (la bola del punzón gira sin levantar; el lápiz, menos).
# Es una mano cuidadosa: todo es sutil, se ve de cerca y no a primera vista.
OFICIOS = {
    "calcar": dict(v=22.0, deriva=0.08, tau=0.4, temblor=0.012, tramo=(55.0, 110.0), duda=1 / 40, presion=0.6, seguir=4.0,
                   monta=0.85, hueco=(0.15, 0.5), esquina=0.35),
    "repujar": dict(v=7.0, deriva=0.09, tau=0.6, temblor=0.008, tramo=(30.0, 70.0), duda=1 / 25, presion=0.93, seguir=3.0,
                    monta=0.95, hueco=(0.1, 0.3), esquina=0.25),
    "puntear": dict(v=4.0, deriva=0.09, tau=0.7, temblor=0.008, tramo=(25.0, 55.0), duda=1 / 20, presion=0.95, seguir=3.0,
                    monta=0.85, hueco=(0.15, 0.5), esquina=0.2),
}
SESION_MIN = 120          # una sesión de trabajo: dos horas, después se descansa


@dataclass
class Mano:
    oficio: str = "repujar"       # calcar | repujar | puntear
    lado: str = "derecha"         # derecha | izquierda | las dos (el punzón en la derecha; la izquierda lee)
    minutos: float = 0.0          # cuánto lleva trabajando en la sesión
    quien: str = "la mano simulada"


def cansancio(minutos):
    """De 0 (recién empieza) a 1 (agotada): crece rápido la primera hora y después se aplana."""
    return 1 - math.exp(-max(0.0, minutos) / 100)


def _empuje(lado):
    """Hacia dónde empuja la mano (y no tira): ahí tiembla y se desvía más. Coordenadas de imagen (y hacia abajo)."""
    s = 1 / math.sqrt(2)
    return np.array([-s, -s]) if lado == "izquierda" else np.array([s, -s])


def remuestrear(q, paso):
    """La polilínea a distancia pareja; devuelve los puntos y su recorrido."""
    q = np.asarray(q, np.float64)
    seg = np.linalg.norm(np.diff(q, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    if s[-1] <= 0:
        return q[:1], np.zeros(1)
    t = np.arange(0.0, s[-1] + 1e-9, paso)
    return np.stack([np.interp(t, s, q[:, 0]), np.interp(t, s, q[:, 1])], 1), t


def _ou(n, dt, tau, rng, x0=None):
    """Un proceso de Ornstein-Uhlenbeck de desvío 1: se aparta y vuelve, con memoria tau (s)."""
    a = math.exp(-dt / tau)
    w = rng.standard_normal(n)
    zi = np.array([(rng.standard_normal() if x0 is None else x0) * a])
    y, _ = lfilter([math.sqrt(1 - a * a)], [1, -a], w, zi=zi)
    return y


def _temblor(t, amplitud, cansancio_, rng):
    """El temblor fisiológico (tres componentes de 8 a 12 Hz, que crecen y menguan) y, cansada, uno lento."""
    y = np.zeros_like(t)
    dt = t[1] - t[0] if len(t) > 1 else 1 / 60
    for _ in range(3):
        f, fase = rng.uniform(8, 12), rng.uniform(0, 2 * math.pi)
        m = 1 + 0.4 * _ou(len(t), dt, 0.5, rng)
        y += amplitud / math.sqrt(3) * m * np.sin(2 * math.pi * f * t + fase)
    if cansancio_ > 0.15:
        y += 0.4 * amplitud * cansancio_ * np.sin(2 * math.pi * rng.uniform(4, 6) * t + rng.uniform(0, 2 * math.pi))
    return y


def _suave(x):
    return x * x * (3 - 2 * x)


def _cortes(P, s, mano, o, c, rng):
    """Dónde levanta la mano: al pasar su alcance, en algunas esquinas (cada una se decide una vez, en
    su punto más agudo), de vez en cuando donde tendría que empujar (y gira la hoja) y, con las dos
    manos, cuando la otra lee el anverso."""
    n = len(P)
    if n < 3:
        return [0, n - 1], []
    paso = s[1] - s[0]
    k = max(1, int(round(0.5 / paso)))                      # se decide cada medio milímetro
    tang = np.gradient(P, axis=0)
    tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-12
    ang = np.unwrap(np.arctan2(tang[:, 1], tang[:, 0]))
    ventana = max(1, int(round(1.5 / paso)))
    idx = np.arange(k, n - k, k)
    giro = np.abs(ang[np.minimum(n - 1, idx + ventana)] - ang[np.maximum(0, idx - ventana)])
    agudo = giro > math.radians(80)
    esquina, j = np.zeros(len(idx), bool), 0
    while j < len(idx):
        if agudo[j]:
            m = j
            while m + 1 < len(idx) and agudo[m + 1]:
                m += 1
            esquina[j + int(np.argmax(giro[j:m + 1]))] = rng.random() < o["esquina"]
            j = m + 1
        else:
            j += 1
    empuja = tang[idx] @ _empuje(mano.lado) > 0.8
    lee = mano.lado == "las dos"
    cortes, giros, lecturas, desde, alcance = [0], [], [], 0, rng.uniform(*o["tramo"]) * (1 - 0.3 * c)
    for jj, i in enumerate(idx):
        hecho = s[i] - s[desde]
        if hecho > 6 and esquina[jj]:
            cortes.append(i)
        elif hecho > 10 and empuja[jj] and rng.random() < 0.012:
            cortes.append(i)
            giros.append(len(cortes) - 1)                    # para seguir, gira la hoja
        elif lee and hecho > 8 and rng.random() < 0.004 * (1 + c):
            cortes.append(i)
            lecturas.append(len(cortes) - 1)                 # la otra mano lee el anverso
        elif hecho > alcance:
            cortes.append(i)
        else:
            continue
        desde, alcance = i, rng.uniform(*o["tramo"]) * (1 - 0.3 * c)
    if s[-1] - s[cortes[-1]] < 3 and len(cortes) > 1:
        cortes.pop()                                          # no se levanta para tres milímetros
    cortes.append(n - 1)
    return cortes, giros, lecturas


def trazar(camino, mano, rng, dt=1 / 60):
    """Recorre un camino abierto (n × 2, en mm) como lo recorrería una mano.

    Devuelve los tramos y un resumen. Cada tramo es un dict con xy (m × 2, mm), p (presión), t (s,
    desde que empezó el camino), s (mm: hasta dónde del camino llegó la mano en cada instante) y
    pausas (índice y segundos de cada duda). El resumen dice cuánto tardó (con las levantadas, los
    giros de la hoja y las lecturas de la otra mano), cuántas veces levantó, cuántas dudó y cuántas
    leyó.
    """
    o = OFICIOS[mano.oficio]
    c = cansancio(mano.minutos)
    P, s = remuestrear(camino, 0.05)
    resumen = dict(segundos=0.0, levantadas=0, dudas=0, lecturas=0, cansancio=round(c, 3))
    if len(P) < 4:
        return [], resumen
    tang = np.gradient(P, axis=0)
    tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-12
    ang = np.unwrap(np.arctan2(tang[:, 1], tang[:, 0]))
    kap = np.abs(np.gradient(ang, s))
    kap = np.convolve(kap, np.ones(12) / 12, mode="same")    # la curvatura, promediada en 0,6 mm
    cortes, giros, lecturas = _cortes(P, s, mano, o, c, rng)
    v0 = o["v"] * (1 - 0.25 * c)
    w = 2 * math.pi * o["seguir"]
    b_seg, a_seg = bilinear([w * w], [1, 2 * 0.8 * w, w * w], fs=1 / dt)
    zi0 = lfilter_zi(b_seg, a_seg)
    empuje = _empuje(mano.lado)
    tramos, reloj = [], 0.0
    for k in range(len(cortes) - 1):
        a, b = cortes[k], cortes[k + 1]
        if k > 0:                                              # al retomar: se monta o deja un hueco
            if rng.random() < o["monta"]:
                a = max(0, a - int(rng.uniform(0.3, 1.2) / 0.05))
            else:
                a = min(b - 2, a + int(rng.uniform(*o["hueco"]) / 0.05))
        if b - a < 4:
            continue
        Pt, st, kt, tt = P[a:b + 1], s[a:b + 1] - s[a], kap[a:b + 1], tang[a:b + 1]
        L = st[-1]
        # arranca quieta al principio del camino y andando al retomar; frena para terminar, pero
        # donde levanta para seguir, levanta andando
        v_ini, v_fin = (0.12 if a == 0 else 0.3), (0.12 if b == len(P) - 1 else 0.45)
        r_ini, r_fin = _suave(np.clip(st / 2.5, 0, 1)), _suave(np.clip((L - st) / 2.0, 0, 1))
        rampa = np.minimum(v_ini + (1 - v_ini) * r_ini, v_fin + (1 - v_fin) * r_fin)
        v = v0 * (1 + 4 * kt) ** (-1 / 3) * rampa
        tiempo = np.concatenate([[0.0], np.cumsum(np.diff(st) / np.maximum(v[1:], 0.08 * v0))])
        # las dudas: se detiene, apretando, y sigue
        pausas = sorted((rng.uniform(0.1, 0.9) * tiempo[-1], rng.uniform(0.25, 0.9) * (1 + 0.5 * c))
                        for _ in range(rng.poisson(o["duda"] * (1 + c) * tiempo[-1])))
        # el reloj de la mano: tm es el tiempo en movimiento, que se queda quieto mientras duda
        T = tiempo[-1] + sum(d for _, d in pausas)
        tg = np.arange(0.0, T + 1e-9, dt)
        tm, quieta, indices, antes = tg.copy(), np.zeros(len(tg), bool), [], 0.0
        for cuando, cuanto in pausas:
            r0 = cuando + antes
            dentro = (tg >= r0) & (tg < r0 + cuanto)
            tm[tg >= r0 + cuanto] -= cuanto
            tm[dentro] = cuando
            quieta |= dentro
            indices.append((int(np.searchsorted(tg, r0)), cuanto))
            antes += cuanto
        tm = np.clip(tm, 0, tiempo[-1])
        sg = np.interp(tm, tiempo, st)
        guia = np.stack([np.interp(sg, st, Pt[:, 0]), np.interp(sg, st, Pt[:, 1])], 1)
        dirg = np.stack([np.interp(sg, st, tt[:, 0]), np.interp(sg, st, tt[:, 1])], 1)
        dirg /= np.linalg.norm(dirg, axis=1, keepdims=True) + 1e-12
        normal = np.stack([-dirg[:, 1], dirg[:, 0]], 1)
        # la deriva, en el tiempo en movimiento: más donde empuja, más cansada
        nm = int(tiempo[-1] / dt) + 2
        tmg = np.arange(nm) * dt

        def lento(tau):
            return np.interp(tm, tmg, _ou(nm, dt, tau, rng))

        incomodo = 1 + 0.4 * np.clip(dirg @ empuje, 0, None)
        sigma = o["deriva"] * (1 + 0.3 * c) * incomodo
        apunta = guia + normal * (sigma * lento(o["tau"] * (1 + 0.2 * c)))[:, None]
        apunta += (0.25 * o["deriva"]) * np.stack([lento(0.8), lento(0.8)], 1)
        # el seguimiento, con retardo: aterriza un poco corrida y converge
        aterriza = apunta[0] + rng.normal(0, 0.05 + 0.04 * c, 2)
        xy = np.stack([lfilter(b_seg, a_seg, apunta[:, j], zi=zi0 * aterriza[j])[0] for j in (0, 1)], 1)
        # el temblor (quieta y apoyada, la punta tiembla menos)
        A = o["temblor"] * (1 + 0.5 * c) * incomodo * (1 - 0.65 * np.convolve(quieta, np.ones(5) / 5, mode="same"))
        xy += normal * (A * _temblor(tg, 1.0, c, rng))[:, None]
        xy += dirg * (0.5 * A * _temblor(tg, 1.0, c, rng))[:, None]
        # la presión: entra y sale de a poco, aprieta más despacio y quieta, y respira
        vg = np.interp(sg, st, v)
        vg[quieta] = 0
        p = o["presion"] * (1 - 0.1 * c) * (1 + 0.15 * (1 - np.clip(vg / v0, 0, 1)))
        p *= (1 - np.exp(-tg / 0.09)) * (1 - np.exp(-(T - tg) / (0.07 if b == len(P) - 1 else 0.1)))
        p *= 1 + 0.04 * _ou(len(tg), dt, 0.6, rng) + 0.01 * _temblor(tg, 1.0, 0, rng)
        p = np.clip(p, 0.0, 1.3)
        tramos.append(dict(xy=xy, p=p, t=tg + reloj, s=sg + s[a], pausas=indices))
        resumen["dudas"] += len(pausas)
        reloj += T + rng.uniform(0.4, 1.2) + (rng.uniform(1.5, 3.0) if k + 1 in giros else 0.0) \
            + (rng.uniform(1.0, 3.0) if k + 1 in lecturas else 0.0)
    resumen["segundos"] = round(float(reloj), 1)
    resumen["levantadas"] = max(0, len(tramos) - 1)
    resumen["lecturas"] = len(lecturas)
    return tramos, resumen


def unir(tramos):
    """Los tramos de una línea, unidos en un camino: lo que sigue la mano siguiente. Donde dos tramos
    se montan, sigue el último; donde quedó un hueco, lo salta."""
    partes, hasta = [], -np.inf
    for tr in tramos:
        nuevo = tr["s"] > hasta + 1e-6
        if nuevo.any():
            partes.append(tr["xy"][nuevo])
            hasta = float(tr["s"][nuevo].max())
    return np.concatenate(partes) if partes else np.zeros((0, 2))


def puntos(tramos, rng, paso, minutos=0.0):
    """El punteado a lo largo de los tramos de la mano que puntea: cada punto es una presión. El paso
    no es parejo, la punta no cae justo sobre la línea y cada punto aprieta distinto. Devuelve (x, y, p)."""
    c = cansancio(minutos)
    base = OFICIOS["puntear"]["presion"] * (1 - 0.1 * c)
    out = []
    for tr in tramos:
        xy, s = tr["xy"], tr["s"] - tr["s"][0]                   # avanza por la línea que mira, no por el temblor
        if len(xy) < 2:
            continue
        t = rng.uniform(0.1, 0.6) * paso
        while t < s[-1]:
            i = min(int(np.searchsorted(s, t)), len(s) - 1)
            q = xy[i] + rng.normal(0, 0.05 + 0.03 * c, 2)
            out.append((q[0], q[1], base * rng.lognormal(0, 0.05 + 0.03 * c)))
            t += paso * rng.lognormal(0, 0.07 + 0.04 * c)
    return np.array(out).reshape(-1, 3)


# ---------------------------------------------------------------- frotar

def _pasadas(a, b, presion, minutos, rng, ancho_mm, segundos):
    """Las pasadas de ida y vuelta de un parche: bandas del ancho del grafito, cada una con su presión."""
    suma, peso = np.zeros(a.shape), np.zeros(a.shape)
    bmin, bmax = b.min() - ancho_mm / 2, b.max() + ancho_mm / 2
    malla = np.linspace(a.min(), a.max(), 64)
    centro = bmin
    while centro < bmax:
        c = cansancio(minutos + segundos / 60)
        esta = presion * (1 - 0.08 * c) * (1 + 0.05 * rng.standard_normal())
        largo = rng.uniform(50, 110)                          # cada ida y vuelta, de 5 a 11 cm
        u = ((a + rng.uniform(0, largo)) % largo) / largo
        vuelta = 1 + 0.08 * np.exp(-(np.minimum(u, 1 - u) / 0.08) ** 2)      # donde la mano frena para volver
        deriva = 1 + 0.04 * np.interp(a, malla, rng.standard_normal(64))
        g = np.exp(-0.5 * ((b - centro) / (ancho_mm / 2.6)) ** 2)
        suma += g * esta * vuelta * deriva
        peso += g
        centro += ancho_mm * rng.uniform(0.45, 0.65)
        segundos += 1.5
    cubre = np.clip(peso / 1.1, 0, 1)
    return np.where(peso > 1e-6, suma / np.maximum(peso, 1e-6), presion) * (0.75 + 0.25 * cubre), segundos


def frotada(forma, px_mm, mano, rng, ancho_mm=18.0, presion=0.85, escala=0.25, alcance_mm=320.0):
    """Una frotada de grafito a mano, de plano: pasadas de ida y vuelta en diagonal (la derecha sube
    hacia la derecha; la izquierda, al revés), del ancho del grafito, que se montan unas sobre otras.
    Cada pasada aprieta distinto, aprieta más donde la mano frena para volver, y la mano se cansa.
    Un papel más grande que lo que alcanza el brazo se frota por parches, cada uno con su ángulo; donde
    dos parches se montan, el papel se frota dos veces. Devuelve la presión (media cerca de la pedida),
    el ángulo de los trazos en grados (para la textura fina) y los segundos que llevó."""
    H, W = forma
    h, w = max(8, int(H * escala)), max(8, int(W * escala))
    mm = 1 / (px_mm * escala)                                  # mm por píxel de la grilla chica
    lado = mano.lado if mano.lado != "las dos" else "derecha"
    ang0 = (32 if lado == "derecha" else 148) + rng.normal(0, 4)
    y, x = np.mgrid[0:h, 0:w].astype(np.float64) * mm
    nx, ny = max(1, round(w * mm / (0.75 * alcance_mm))), max(1, round(h * mm / (0.75 * alcance_mm)))
    margen, borde = 0.1 * alcance_mm, 25.0                     # cuánto se montan los parches; su borde, en mm

    def cortes(n, total):
        """Dónde termina un parche y empieza el siguiente, a lo largo de un eje (corridos a mano)."""
        return [-np.inf] + [k * total / n + rng.normal(0, 0.08 * alcance_mm) for k in range(1, n)] + [np.inf]

    def ventana(z, a, b):
        """Lo que cubre un parche a lo largo de un eje: hasta un poco pasado su corte, con un borde suave."""
        return np.clip((z - (a - margen)) / borde + 0.5, 0, 1) * np.clip(((b + margen) - z) / borde + 0.5, 0, 1)

    cy = cortes(ny, h * mm)
    suma, peso, segundos, angulos = np.zeros((h, w)), np.zeros((h, w)), 0.0, []
    for j in range(ny):
        cx = cortes(nx, w * mm)                                # cada fila de parches, con sus propios cortes
        for i in (range(nx) if j % 2 == 0 else reversed(range(nx))):     # recorre el papel en zigzag
            v = ventana(x[:1, :], cx[i], cx[i + 1]) * ventana(y[:, :1], cy[j], cy[j + 1])
            filas, cols = np.nonzero(v.any(axis=1))[0], np.nonzero(v.any(axis=0))[0]
            zona = np.s_[filas[0]:filas[-1] + 1, cols[0]:cols[-1] + 1]
            ang = math.radians(ang0 + rng.normal(0, 4 if nx * ny > 1 else 0.0))
            u = np.array([math.cos(ang), -math.sin(ang)])
            xs, ys = x[zona], y[zona]
            p, segundos = _pasadas(xs * u[0] + ys * u[1], xs * -u[1] + ys * u[0], presion, mano.minutos, rng,
                                   ancho_mm, segundos)
            suma[zona] += v[zona] * p
            peso[zona] += v[zona]
            angulos.append(math.degrees(ang))
    p = suma / np.maximum(peso, 1e-6) * np.maximum(peso, 1.0) ** 0.05    # dos veces frotado: apenas más oscuro
    return cv2.resize(p.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR), float(np.mean(angulos)), segundos


def rayas(forma, angulo, rng, largo=25):
    """La textura fina del grafito, rayada en la dirección de los trazos (desvío 1)."""
    k = np.zeros((largo, largo), np.float32)
    c = (largo - 1) / 2
    u = np.array([math.cos(math.radians(angulo)), -math.sin(math.radians(angulo))])
    for t in np.linspace(-c, c, 4 * largo):
        k[int(round(c + t * u[1])), int(round(c + t * u[0]))] = 1
    r = cv2.filter2D(rng.standard_normal(forma).astype(np.float32), -1, k / k.sum())
    return r / (r.std() + 1e-9)


# ---------------------------------------------------------------- poner la cinta

def colocar(vertices, rng, px_mm, deriva_mm=0.25, punta_mm=(-0.5, 1.0)):
    """Una cinta puesta a mano sobre un recorrido de tramos rectos: cada vértice queda un poco
    corrido (una deriva que se arrastra de un tramo al siguiente) y las puntas, cortadas con la
    mano, se quedan cortas o se pasan."""
    q = np.asarray(vertices, np.float64).copy()
    if len(q) < 2:
        return q
    d = rng.standard_normal((len(q), 2))
    for i in range(1, len(q)):
        d[i] = 0.6 * d[i - 1] + 0.8 * d[i]
    q += d * deriva_mm * px_mm * 0.7 + rng.normal(0, 0.08 * px_mm, q.shape)
    for i, j in ((0, 1), (-1, -2)):
        u = q[i] - q[j]
        u /= np.linalg.norm(u) + 1e-9
        q[i] = q[i] + u * rng.uniform(*punta_mm) * px_mm
    return q


# ---------------------------------------------------------------- el dedo en el agua

def toque(rng):
    """Un dedo que toca el agua en una esquina: nunca en el mismo punto ni con la misma fuerza, y a
    veces toca dos veces (el segundo toque, más débil, un poco después y un poco al lado)."""
    d = dict(punto=(0.08 + rng.normal(0, 0.01), 0.92 + rng.normal(0, 0.01)), amplitud=2.2 * rng.lognormal(0, 0.12))
    if rng.random() < 0.15:
        d["segundo"] = dict(retraso=rng.uniform(0.6, 1.4), amplitud=rng.uniform(0.2, 0.4),
                            corrimiento=(rng.normal(0, 0.01), rng.normal(0, 0.01)))
    return d


# ---------------------------------------------------------------- la voz

def lectura(verso, rng):
    """El verso leído en voz alta: cada sílaba dura distinto (unos 0,22 s), la última de cada frase
    se alarga, se detiene en las comas y al final, la voz baja a lo largo del verso y el acento va y
    viene. Las sílabas se cuentan como en comun.silabas. Devuelve, por sílaba, cuándo empieza,
    cuánto dura, su altura (Hz), su volumen y el silencio que la sigue; y cuánto dura todo."""
    pausa_tras = []
    for palabra, despues in re.findall(r"([a-záéíóúüñ]+)([^a-záéíóúüñ]*)", verso.lower()):
        k = sum(2 if len(g) > 1 and re.search(r"[íú]", g) else 1 for g in re.findall(r"[aeiouáéíóúü]+", palabra))
        if k == 0:
            continue
        pausa_tras += [0.0] * (k - 1)
        pausa_tras.append(rng.uniform(0.3, 0.6) if re.search(r"[,;:]", despues)
                          else rng.uniform(0.5, 0.9) if re.search(r"[.!?…]", despues) else 0.0)
    n = max(1, len(pausa_tras))
    pausa = np.array(pausa_tras + [0.0] * (n - len(pausa_tras)))
    pausa[-1] = max(pausa[-1], rng.uniform(0.5, 0.9))         # al final del verso, siempre
    dur = rng.lognormal(math.log(0.22), 0.25, n) * np.where(pausa > 0, 1.4, 1.0)
    inicio = np.concatenate([[0.0], np.cumsum(dur + pausa)[:-1]])
    alto0, alto1 = rng.uniform(175, 215), rng.uniform(112, 138)
    hz = np.interp(np.arange(n), [0, max(n - 1, 1)], [alto0, alto1]) * (1 + 0.04 * rng.standard_normal(n))
    volumen = np.clip(rng.normal(0.65, 0.15, n), 0.2, 1.0)
    volumen[np.arange(n) % 2 == 1] *= 0.85
    return dict(inicio=inicio, duracion=dur, pausa=pausa, hz=hz, volumen=volumen, total=float(inicio[-1] + dur[-1] + pausa[-1]))


def oir(hz, volumen, rng):
    """La altura y el volumen en el instante de la foto: tiemblan (jitter y shimmer)."""
    return float(hz * (1 + 0.012 * rng.standard_normal())), float(np.clip(volumen * (1 + 0.06 * rng.standard_normal()), 0.05, 1.0))


def instante(lec, t):
    """Qué suena en el instante t de la lectura: la sílaba (índice) y cuánto queda de su volumen. En un
    silencio, el agua sigue moviéndose y se apaga en unas décimas de segundo."""
    i = int(np.clip(np.searchsorted(lec["inicio"], t, side="right") - 1, 0, len(lec["inicio"]) - 1))
    fin = lec["inicio"][i] + lec["duracion"][i]
    if t <= fin:
        return i, 1.0, False
    return i, float(math.exp(-(t - fin) / 0.15)), True
