"""Medidas, azar reproducible y utilidades de la simulación del taller de Contenida.

Todo se trabaja a 4 px por milímetro: un azulejo de 150 mm es un lienzo de
600 × 600 px y una tesela, 100 px. El azar sale de una semilla fija (el día de
la obra) combinada con la celda, la placa y la acción, de modo que la
simulación da siempre el mismo resultado y cada placa tiene su propia «mano».
"""

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
TIPO = BASE.parent
SALIDA = BASE / "salida"
GLIFOS = SALIDA / "glifos"

PX_MM = 4
AZULEJO_MM, TESELAS, JUNTA_MM = 150, 6, 3
T = AZULEJO_MM * PX_MM          # 600 px: un azulejo, una letra
TES = T // TESELAS              # 100 px: una tesela
JUNTA = JUNTA_MM * PX_MM        # 12 px
SEMILLA = 20260822              # el día de la obra

# Proporción del trapecio de la proyección: la base mide 0,72 del borde
# superior visible en el video 1 (el borde superior se sale del cuadro).
TRAPECIO = 0.70
# Duración supuesta del bucle, en minutos: no la sabemos (se le pide a Rebeca).
BUCLE_MIN = 5

FUENTES_TESTIGO = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    "/Library/Fonts/Times New Roman.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
FUENTES_ROTULO = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/System/Library/Fonts/Menlo.ttc",
]


def primera_que_exista(rutas):
    for r in rutas:
        if Path(r).exists():
            return r
    return None


FUENTE_TESTIGO = primera_que_exista(FUENTES_TESTIGO)
FUENTE_ROTULO = primera_que_exista(FUENTES_ROTULO)


def rotulo(tam):
    return ImageFont.truetype(FUENTE_ROTULO, tam) if FUENTE_ROTULO else ImageFont.load_default()


# ---------------------------------------------------------------- textos y caja

CAJA = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
CELDAS = CAJA["celdas"]
POR_SIGNO = {c["signo"]: c for c in CELDAS}
PIE = (TIPO / "textos" / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
POEMA = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8")
VERSOS = [v for v in POEMA.lower().split("\n") if v.strip()]
CORTES_PIE = ["(hoy", "Puerta del Sol", "en donde luego"]  # los cortes de línea del libro


def lineas_pie():
    lineas, resto = [], PIE
    for corte in CORTES_PIE:
        i = resto.find(corte)
        if i < 0:
            import textwrap
            return textwrap.wrap(PIE, 120)
        lineas.append(resto[:i + len(corte)].strip())
        resto = resto[i + len(corte):]
    lineas.append(resto.strip())
    return lineas


def poliza():
    """Placas por signo: el máximo de apariciones en un verso (como inventario.py)."""
    p = Counter()
    for v in VERSOS:
        for c, n in Counter(ch for ch in v if not ch.isspace()).items():
            p[c] = max(p[c], n)
    return {c["signo"]: max(1, p[c["signo"]]) for c in CELDAS}


# ---------------------------------------------------------------- azar

def azar(*claves):
    h = hashlib.sha256("|".join(map(str, (SEMILLA,) + claves)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def ruido(forma, sigma, rng):
    """Ruido suave de desvío 1. Para sigmas grandes se genera chico y se amplía."""
    h, w = forma
    if sigma >= 8:
        f = sigma / 4
        chico = rng.standard_normal((max(2, int(h / f) + 2), max(2, int(w / f) + 2))).astype(np.float32)
        chico = cv2.GaussianBlur(chico, (0, 0), 4)
        n = cv2.resize(chico, (int(chico.shape[1] * f), int(chico.shape[0] * f)), interpolation=cv2.INTER_CUBIC)[:h, :w]
        n = cv2.copyMakeBorder(n, 0, max(0, h - n.shape[0]), 0, max(0, w - n.shape[1]), cv2.BORDER_REFLECT)
    else:
        n = rng.standard_normal((h, w)).astype(np.float32)
        if sigma > 0:
            n = cv2.GaussianBlur(n, (0, 0), sigma)
    return (n - n.mean()) / (n.std() + 1e-9)


def ruido_1d(n, sigma, rng):
    r = rng.standard_normal(n + int(6 * sigma) + 2).astype(np.float32)
    k = np.exp(-0.5 * (np.arange(-3 * sigma, 3 * sigma + 1) / max(sigma, 1e-3)) ** 2)
    r = np.convolve(r, k / k.sum(), mode="same")[int(3 * sigma):int(3 * sigma) + n]
    return (r - r.mean()) / (r.std() + 1e-9)


# ---------------------------------------------------------------- máscaras

def componentes(mascara, minimo=1):
    n, etiquetas, stats, centros = cv2.connectedComponentsWithStats(mascara.astype(np.uint8), connectivity=8)
    return [(etiquetas == i, stats[i], centros[i]) for i in range(1, n) if stats[i][4] >= minimo]


def caja_tinta(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return 0, 0, 0, 0
    return xs.min(), ys.min(), xs.max(), ys.max()


def mover(m, dx, dy, forma=(T, T)):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(m.astype(np.float32), M, (forma[1], forma[0])) > 0.5


def escalar(m, sx, sy, cx, cy):
    M = np.float32([[sx, 0, cx - sx * cx], [0, sy, cy - sy * cy]])
    return cv2.warpAffine(m.astype(np.float32), M, (m.shape[1], m.shape[0])) > 0.5


def rotar(m, grados, cx, cy):
    M = cv2.getRotationMatrix2D((float(cx), float(cy)), grados, 1.0)
    return cv2.warpAffine(m.astype(np.float32), M, (m.shape[1], m.shape[0])) > 0.5


def centrar_h(m):
    x0, _, x1, _ = caja_tinta(m)
    return mover(m, T / 2 - (x0 + x1) / 2, 0, m.shape)


# ---------------------------------------------------------------- luz

def sombrear(altura, mascara, azimut=200, elevacion=15, k=7.0, brillo=0.9, fondo=0.05, rng=None):
    """Foto con luz rasante de una lámina de aluminio: difusa más especular."""
    gy, gx = np.gradient(altura.astype(np.float32))
    n = np.dstack([-gx * k, -gy * k, np.ones_like(gx)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    az, el = np.radians(azimut), np.radians(elevacion)
    L = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    V = np.array([0, 0, 1.0])
    Hh = (L + V) / np.linalg.norm(L + V)
    difusa = np.clip(n @ L, 0, None)
    especular = np.clip(n @ Hh, 0, None) ** 18
    img = 0.16 + 0.95 * difusa + 0.6 * brillo * especular
    img = np.where(mascara, img, fondo)
    if rng is not None:
        img = img + 0.012 * rng.standard_normal(img.shape)
    return np.clip(img, 0, 1)


def densidad_a_violeta(d, papel=(0.955, 0.94, 0.905)):
    """Tinta de anilina sobre papel: casi negra cuando es densa, violeta cuando queda poca."""
    absorcion = np.array([2.1, 3.3, 1.35])
    return np.clip(np.array(papel)[None, None, :] * np.exp(-d[..., None] * absorcion[None, None, :]), 0, 1)


# ---------------------------------------------------------------- salida

def a8(img):
    return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)


def guardar(ruta, img, calidad=84):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(img, np.ndarray):
        img = Image.fromarray(a8(img) if img.dtype != np.uint8 else img)
    if ruta.suffix.lower() in (".jpg", ".jpeg"):
        img.convert("RGB").save(ruta, quality=calidad, optimize=True)
    else:
        img.save(ruta, optimize=True)
    return ruta


def a_rgb(img):
    if img.ndim == 2:
        return np.dstack([img] * 3)
    return img


def lamina(celdas, titulo, subtitulo, ruta, lado=190, fondo=(0.97, 0.965, 0.95), tinta=(0.12, 0.12, 0.12),
           junta=(0.62, 0.62, 0.58), notas=None):
    """Arma una lámina de 8 × 7 con una imagen por celda (dict celda → imagen)."""
    col, fil, j, mx, arriba = CAJA["columnas"], CAJA["filas"], 6, 48, 118
    W = mx * 2 + col * lado + (col - 1) * j
    H = arriba + fil * lado + (fil - 1) * j + 60 + (26 * len(notas) if notas else 0)
    lienzo = Image.new("RGB", (W, H), tuple(int(c * 255) for c in fondo))
    d = ImageDraw.Draw(lienzo)
    d.text((mx, 26), titulo, font=rotulo(30), fill=tuple(int(c * 255) for c in tinta))
    for i, linea in enumerate(subtitulo.split("\n")):
        d.text((mx, 68 + i * 20), linea, font=rotulo(15), fill=(100, 100, 100))
    d.rectangle([mx - j, arriba - j, W - mx + j - 1, arriba + fil * lado + (fil - 1) * j + j - 1],
                fill=tuple(int(c * 255) for c in junta))
    for c in CELDAS:
        x = mx + (c["columna"] - 1) * (lado + j)
        y = arriba + (c["fila"] - 1) * (lado + j)
        img = celdas.get(c["celda"])
        if img is None:
            continue
        im = Image.fromarray(a8(a_rgb(img)) if img.dtype != np.uint8 else a_rgb(img)).resize((lado, lado), Image.LANCZOS)
        lienzo.paste(im, (x, y))
        d.text((x + 6, y + 4), str(c["celda"]), font=rotulo(12), fill=(140, 140, 140))
    if notas:
        y0 = arriba + fil * lado + (fil - 1) * j + 30
        for i, n in enumerate(notas):
            d.text((mx, y0 + i * 26), n, font=rotulo(15), fill=(80, 80, 80))
    guardar(ruta, lienzo)
    return lienzo


def fila_de_paneles(paneles, rotulos, ruta, alto=300, titulo=None):
    """Una fila de imágenes con su rótulo debajo."""
    ims = []
    for p in paneles:
        im = Image.fromarray(a8(a_rgb(p)) if p.dtype != np.uint8 else a_rgb(p))
        ims.append(im.resize((int(im.width * alto / im.height), alto), Image.LANCZOS))
    W = sum(i.width for i in ims) + 12 * (len(ims) + 1)
    H = alto + 70 + (50 if titulo else 0)
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    y0 = 12
    if titulo:
        d.text((12, 12), titulo, font=rotulo(24), fill=(30, 30, 30))
        y0 = 58
    x = 12
    for im, r in zip(ims, rotulos):
        lienzo.paste(im, (x, y0))
        d.text((x, y0 + alto + 8), r, font=rotulo(15), fill=(70, 70, 70))
        x += im.width + 12
    guardar(ruta, lienzo)
    return lienzo


def silabas(verso):
    """Silabeo aproximado: grupos vocálicos, con hiato si hay í o ú acentuadas."""
    n = []
    for palabra in re.findall(r"[a-záéíóúüñ]+", verso):
        for grupo in re.findall(r"[aeiouáéíóúü]+", palabra):
            n.append(palabra)
            if len(grupo) > 1 and re.search(r"[íú]", grupo):
                n.append(palabra)
    return n
