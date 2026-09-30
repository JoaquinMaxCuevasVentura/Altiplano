"""Extrae de la foto de la lámina los testigos de las letras del pie.

Uso (desde la raíz del repositorio; necesita tesseract con el idioma spa):
    python3 tipografia/simulacion/extraer_testigos.py RUTA/A/LA/FOTO_DEL_PIE

La foto es un recorte cercano del pie de la lámina, tal como se ve en la
fotografía original: cuatro líneas, con la luz desigual y el papel doblado.
Sobre el pliegue, la tercera línea sube en «originariamente se» hasta tocar la
segunda. La altura de x mide unos 10 px. El script:

1. empareja la luz: divide la foto por su fondo;
2. busca las palabras con OCR solo para saber dónde van las líneas, y en cada
   una sigue la línea de base, palabra por palabra, hasta tener su curva;
3. reparte la tinta entre las líneas: cada mancha es de la línea que toca; si
   toca dos, se reparte pixel por pixel;
4. endereza cada línea con su curva;
5. separa las palabras: entre los blancos de la línea elige como espacios los
   que mejor reparten las palabras que se saben (textos/pie_de_lamina.txt),
   con el ancho esperado de cada una, y prefiere los blancos más hondos;
6. corta cada palabra en tantas letras como tiene, como con tijera: cada corte
   cae en el blanco más hondo cerca de donde lo pone el ancho esperado. Los
   anchos esperados salen de la letra sustituta (FUENTE_TESTIGO, en comun.py);
   aquí no se toma de ella ninguna forma, solo dónde buscar el corte.

Escribe en tipografia/simulacion/testigos/:
  NNN.png     cada letra del pie, en gris, enderezada, a tres veces la foto, en el orden del texto;
  pie.json    por letra: el signo, la línea, la palabra, dónde empieza el recorte en la línea,
              los dos cortes de tijera y la línea de base.

La foto no se sube al repositorio: solo letras sueltas. Ver 07_posnansky.md, §3.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from scipy.optimize import least_squares
from scipy.signal import find_peaks
from scipy.special import erf
from skimage.restoration import richardson_lucy

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comun import FUENTE_TESTIGO, lineas_pie  # noqa: E402
from PIL import ImageFont  # noqa: E402

TESTIGOS = AQUI / "testigos"
ESCALA = 3              # se lee y se recorta a tres veces la foto
ARRIBA, ABAJO = 2.3, 1.1  # la franja de cada línea, en alturas de x sobre y bajo la base


def tesseract(img, salida, psm, *args):
    subprocess.run(["tesseract", str(img), str(salida), "-l", "spa", "--psm", str(psm), *args],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def emparejar_luz(gris):
    """La foto dividida por su fondo: el papel queda en 1 aunque la luz no sea pareja."""
    fondo = cv2.morphologyEx(gris, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    fondo = cv2.GaussianBlur(fondo, (0, 0), 8)
    return np.clip(gris / np.maximum(fondo, 1), 0, 1)


def palabras(img, tmp):
    ruta = tmp / "pie.png"
    cv2.imwrite(str(ruta), (img * 255).astype(np.uint8))
    tesseract(ruta, tmp / "pie", 6, "tsv")
    out = []
    for fila in (tmp / "pie.tsv").read_text(encoding="utf8").splitlines()[1:]:
        c = fila.split("\t")
        if len(c) == 12 and c[0] == "5" and c[11].strip():
            x, y, w, h = map(int, c[6:10])
            out.append(dict(linea=(int(c[2]), int(c[3]), int(c[4])), caja=(x, y, x + w, y + h), texto=c[11].strip()))
    return out


def base_de_palabra(tinta, caja):
    """La base de una palabra: la mediana del fondo de la tinta, columna por columna.
    Las descendentes son pocas columnas y no la mueven."""
    x0, y0, x1, y1 = caja
    sub = tinta[y0:y1, x0:x1]
    fondos = [y0 + np.nonzero(col)[0].max() for col in sub.T if col.any()]
    techos = [y0 + np.nonzero(col)[0].min() for col in sub.T if col.any()]
    return float(np.median(fondos)), float(np.median(fondos) - np.median(techos))


def curva_de_base(ws, tinta, ancho):
    """La base de la línea como función de x: un punto por palabra (dos si es larga), interpolado y suavizado.
    Donde el papel se dobla, la línea de abajo sube y entra en la caja de la palabra: esas cajas,
    más altas que las otras de su línea, se recortan al alto de siempre, desde arriba."""
    alto = float(np.median([w["caja"][3] - w["caja"][1] for w in ws]))
    pts, xhs = [], []
    for w in ws:
        x0, y0, x1, y1 = w["caja"]
        if y1 - y0 > 1.3 * alto:
            y1 = int(y0 + alto)
        tramos = [(x0, (x0 + x1) // 2), ((x0 + x1) // 2, x1)] if x1 - x0 > 60 * ESCALA else [(x0, x1)]
        for a, c in tramos:
            b, xh = base_de_palabra(tinta, (a, y0, c, y1))
            pts.append(((a + c) / 2, b))
            xhs.append(xh)
    pts.sort()
    xs, bs = map(np.array, zip(*pts))
    curva = np.interp(np.arange(ancho), xs, bs)
    curva = cv2.GaussianBlur(curva.reshape(1, -1).astype(np.float32), (0, 0), 12 * ESCALA).ravel()
    extremos = (min(w["caja"][0] for w in ws), max(w["caja"][2] for w in ws))
    return curva, float(np.median(xhs)), extremos


def duenos(tinta, curvas, xhs):
    """A qué línea pertenece cada pixel de tinta. Cada mancha es de la línea cuya zona
    de altura de x toca; si toca dos (donde el papel se dobla, una línea sube y se
    pega a la de arriba), se reparte pixel por pixel, por cercanía. Las manchas que no
    tocan ninguna zona (tildes, puntos, comas) van con la línea más cercana."""
    H, W = tinta.shape
    n, lab = cv2.connectedComponents(tinta.astype(np.uint8), connectivity=8)
    ys = np.arange(H, dtype=np.float32)[:, None]
    centros = [c[None, :] - xh / 2 for c, xh in zip(curvas, xhs)]
    distancias = np.stack([np.abs(ys - c) for c in centros])            # (líneas, H, W)
    cercana = np.argmin(distancias, axis=0)
    toques = np.stack([np.bincount(lab[(ys >= c[None, :] - xh) & (ys <= c[None, :])], minlength=n)
                       for c, xh in zip(curvas, xhs)])                   # (líneas, manchas)
    area = np.maximum(np.bincount(lab.ravel(), minlength=n), 1)
    varias = (toques > 0.05 * area).sum(axis=0) >= 2
    dueno_mancha = np.where(toques.max(axis=0) > 0, np.argmax(toques, axis=0), -1)
    dueno = np.where(tinta, dueno_mancha[lab], -2)
    reparto = tinta & (varias[lab] | (dueno_mancha[lab] == -1))
    dueno[reparto] = cercana[reparto]
    return dueno


def solo_la_linea(img, tinta, dueno, i, curva, xh, extremos):
    """La foto con la tinta de las otras líneas borrada, y lo que queda fuera de la
    línea (más arriba de las ascendentes, más abajo de las descendentes, antes de la
    primera palabra y después de la última)."""
    ys = np.arange(img.shape[0], dtype=np.float32)[:, None]
    fuera = (ys < curva[None, :] - 1.9 * xh) | (ys > curva[None, :] + 1.0 * xh)
    ajena = tinta & ((dueno != i) | fuera)
    propia = tinta & ~ajena
    halo = cv2.dilate(ajena.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & ~propia
    limpia = np.where(halo, np.maximum(img, 0.97), img)
    margen = int(xh)
    limpia[:, :max(0, extremos[0] - margen)] = 1.0
    limpia[:, extremos[1] + margen:] = 1.0
    return limpia


def enderezar(img, curva, xh):
    arriba, abajo = int(ARRIBA * xh), int(ABAJO * xh)
    alto = arriba + abajo
    W = img.shape[1]
    mx = np.tile(np.arange(W, dtype=np.float32), (alto, 1))
    my = (curva[None, :] - arriba + np.arange(alto, dtype=np.float32)[:, None]).astype(np.float32)
    return cv2.remap(img.astype(np.float32), mx, my, cv2.INTER_LINEAR, borderValue=1.0), arriba


def palabras_de_linea(recta, anchos, espacio, xh):
    """Las palabras de una línea enderezada. Entre cada par de tramos de tinta hay un
    blanco; se eligen como espacios los blancos que mejor reparten la línea en palabras
    del ancho esperado, prefiriendo los más hondos (un espacio es más ancho que el aire
    entre dos letras)."""
    tinta = (recta < 0.72).any(axis=0)
    cols = np.nonzero(tinta)[0]
    n = len(anchos)
    huecos = [(int(a) + 1, int(b)) for a, b in zip(cols[:-1], cols[1:]) if b - a > 1]
    if len(huecos) < n - 1:
        return None
    x_ini, x_fin = int(cols[0]), int(cols[-1]) + 1
    a = np.array(anchos, float)
    s = (x_fin - x_ini) / (a.sum() + (n - 1) * espacio)
    esperado = a * s
    hondura = np.array([min((b - a_) / (0.4 * xh), 1.0) for a_, b in huecos])
    G = len(huecos)
    # costo[k][g]: la palabra k termina en el hueco g (la última, en el borde derecho)
    inf = float("inf")
    costo = np.full((n, G + 1), inf)
    previo = np.zeros((n, G + 1), int)
    fin_de = [h[0] for h in huecos] + [x_fin]
    ini_de = [x_ini] + [h[1] for h in huecos]
    for g in range(G + 1):
        w = fin_de[g] - x_ini
        costo[0, g] = 4 * ((w - esperado[0]) / esperado[0]) ** 2 + (3 * (1 - 2 * hondura[g]) if g < G else 0)
    for k in range(1, n):
        for g in range(k, G + 1):
            if (g == G) != (k == n - 1):
                continue
            w = fin_de[g] - np.array(ini_de[1:g + 1])            # empieza después del hueco h (h < g)
            c = costo[k - 1, :g] + 4 * ((w - esperado[k]) / esperado[k]) ** 2
            h = int(np.argmin(c))
            costo[k, g] = c[h] + (3 * (1 - 2 * hondura[g]) if g < G else 0)
            previo[k, g] = h
    if not np.isfinite(costo[n - 1, G]):
        return None
    elegidos, g = [], G
    for k in range(n - 1, 0, -1):
        g = previo[k, g]
        elegidos.append(g)
    elegidos = elegidos[::-1]
    bordes = [x_ini] + [v for g in elegidos for v in huecos[g]] + [x_fin]
    return [(int(p), int(q)) for p, q in zip(bordes[::2], bordes[1::2])]


def cortar_palabra(recta, x0, x1, texto, avances):
    """Corta la palabra en tantas letras como tiene, con tijera: cada corte cae en el
    blanco más hondo cerca de donde lo pone el ancho esperado de cada letra."""
    n = len(texto)
    if n == 1:
        return [(x0, x1)]
    oscuro = (1 - recta[:, x0:x1]).sum(axis=0)
    oscuro = np.convolve(oscuro, np.ones(3) / 3, "same")
    oscuro = oscuro / max(oscuro.max(), 1e-6)
    W = x1 - x0
    w = np.array(avances, float)
    w = w * W / w.sum()
    xs = np.arange(W + 1, dtype=float)
    salto = xs[None, :] - xs[:, None]                         # de un corte (fila) al siguiente (columna)
    tinta = 3 * np.append(oscuro, 0)
    costo = (xs - w[0]) ** 2 / w[0] ** 2 + tinta              # el primer corte, desde el borde izquierdo
    costo[:2] = np.inf
    previos = []
    for i in range(1, n - 1):
        paso = np.where(salto >= 2, (salto - w[i]) ** 2 / w[i] ** 2, np.inf)
        total = costo[:, None] + paso
        previos.append(np.argmin(total, axis=0))
        costo = total.min(axis=0) + tinta
    final = costo + ((W - xs) - w[-1]) ** 2 / w[-1] ** 2
    final[W - 1:] = np.inf
    x = int(np.argmin(final))
    cortes = [x]
    for p in reversed(previos):
        x = int(p[x])
        cortes.append(x)
    cortes = [0] + cortes[::-1] + [W]
    return [(x0 + a, x0 + b) for a, b in zip(cortes[:-1], cortes[1:])]


def avance(fuente, ch):
    return max(fuente.getlength(ch), 0.25 * fuente.size)


def trazos_aislados(lineas):
    """En las filas de la zona de x, cada pico de oscuridad que cae casi a cero a los dos
    lados es un trazo aislado. Devuelve, por trazo, su tinta total (en px de la foto) y su pico."""
    totales, picos = [], []
    for L in lineas:
        recta, b, xh = L["recta"], L["base"], L["xh"]
        for y in range(int(b - 0.8 * xh), int(b - 0.2 * xh), 3):
            fila = recta[y]
            papel = np.percentile(fila, 95)
            d = np.clip(papel - fila, 0, None) / papel
            for i in find_peaks(d, prominence=0.1)[0]:
                izq, der = d[max(0, i - 4 * ESCALA):i][::-1], d[i + 1:i + 1 + 4 * ESCALA]
                if len(izq) < 4 * ESCALA or len(der) < 4 * ESCALA:
                    continue
                bajo_i, bajo_d = izq < 0.15 * d[i], der < 0.15 * d[i]
                if not bajo_i.any() or not bajo_d.any():
                    continue                                   # pegado a otro trazo: no está aislado
                a, z = int(np.argmax(bajo_i)), int(np.argmax(bajo_d))
                totales.append(d[i - a:i + z + 1].sum() / ESCALA)
                picos.append(d[i])
    return np.array(totales), np.array(picos)


def tinta_y_desenfoque(lineas):
    """Cuán negra era la tinta y cuánto la corrió la foto, medidos en los trazos aislados.

    Un trazo de ancho w, con tinta de oscuridad I, desenfocado con una campana de ancho σ,
    junta una tinta total I·w (el desenfoque la corre, pero no cambia cuánta hay) y llega a
    un pico I·erf(w / (2√2 σ)). Cada trazo aislado da su tinta total y su pico; con muchos
    se despejan I y σ.
    """
    A, P = trazos_aislados(lineas)
    ajuste = least_squares(lambda p: p[0] * erf(A / p[0] / (2 * np.sqrt(2) * p[1])) - P, [0.8, 0.8],
                           bounds=([0.3, 0.2], [1.0, 5.0]))
    I, sigma = (float(v) for v in ajuste.x)
    return dict(tinta=round(I, 3), sigma=round(sigma, 3), trazos=int(len(A)),
                error=round(float(np.sqrt(np.mean(ajuste.fun ** 2))), 4), asta=round(float(np.median(A / I)), 3))


def deshacer_desenfoque(recta, sigma, pasadas=10):
    """Richardson–Lucy con la campana medida: la tinta vuelve hacia donde estaba. Conserva
    la tinta total; con pocas pasadas no inventa bordes (con muchas, aparecen anillos)."""
    s = sigma * ESCALA
    r = int(3 * s)
    x = np.arange(-r, r + 1)
    g = np.exp(-x ** 2 / (2 * s * s))
    campana = np.outer(g, g) / np.outer(g, g).sum()
    papel = np.percentile(recta, 95)
    d = np.clip(1 - recta / papel, 0, 1) + 1e-3
    return np.clip(1 - richardson_lucy(d, campana, num_iter=pasadas, clip=False), 0, 1).astype(np.float32)


def grosor_de_la_o(lineas, tinta):
    """El grosor del trazo de la o, por la tinta que junta y no por su borde: la oscuridad
    sumada a lo ancho del trazo, dividida por la de la tinta llena. El papel se toma de la
    fila entera de la línea, no de adentro de la letra. En px de la foto: el lado (el grueso)
    y el tope (el fino), como mediana de todas las o del pie."""
    def ancho(perfil, papel):
        o = np.clip((papel - perfil) / papel / tinta, 0, 1)
        a = b = int(np.argmax(o))
        while a > 0 and o[a - 1] > 0.05:
            a -= 1
        while b < len(o) - 1 and o[b + 1] > 0.05:
            b += 1
        return o[a:b + 1].sum() / ESCALA

    lado, tope = [], []
    for L in lineas:
        recta, b, xh = L["cruda"], L["base"], L["xh"]
        papel_fila = np.percentile(recta, 95, axis=1)
        papel = float(np.median(papel_fila[int(b - xh):int(b)]))
        for P in L["palabras"]:
            for ch, (x0, x1) in zip(P["texto"], P["letras"]):
                if ch != "o":
                    continue
                c = (x0 + x1) // 2
                lado += [ancho(recta[y, x0:c], papel) for y in range(int(b - 0.6 * xh), int(b - 0.4 * xh))]
                tope += [ancho(recta[int(b - 1.3 * xh):int(b - 0.5 * xh), x], papel) for x in range(c - 2, c + 3)]
    return dict(lado=round(float(np.median(lado)), 3), tope=round(float(np.median(tope)), 3))


def alturas_por_astas(lineas):
    """Las alturas del pie medidas en las astas, a media oscuridad de cada una, en la foto con
    el desenfoque deshecho. El extremo de un asta es un borde neto: a media oscuridad no se
    mueve. Devuelve, en px de la foto y como medianas: la altura de x (astas de n, m, u, r),
    la de las ascendentes (l, d, b, h, k) y cuánto bajan las descendentes (astas de p y q)."""
    def asta(recta, x0, x1, y0, y1):
        sub = 1 - recta[y0:y1, x0:x1]
        c = x0 + int(np.argmax(sub.sum(axis=0)))
        p = 1 - recta[:, max(0, c - 1):c + 2].mean(axis=1)
        mitad = float(np.median(p[y0:y1])) / 2
        a = z = (y0 + y1) // 2
        while a > 0 and p[a - 1] > mitad:
            a -= 1
        while z < len(p) - 1 and p[z + 1] > mitad:
            z += 1
        return a, z

    x, sube, baja, bases = [], [], [], []
    for L in lineas:
        recta, b, xh = L["recta"], L["base"], L["xh"]
        for P in L["palabras"]:
            for ch, (x0, x1) in zip(P["texto"], P["letras"]):
                if ch in "nmur":
                    a, z = asta(recta, x0, x1, int(b - 0.8 * xh), int(b - 0.2 * xh))
                    x.append(z - a + 1)
                    bases.append(z - b)
                elif ch in "ldbhk":
                    a, z = asta(recta, x0, x1, int(b - 1.4 * xh), int(b - 1.1 * xh))
                    sube.append(b - a)
                elif ch in "pq":
                    a, z = asta(recta, x0, x1, int(b + 0.2 * xh), int(b + 0.5 * xh))
                    baja.append(z - b)
    correccion = float(np.median(bases))             # la base a media oscuridad, respecto de la base medida
    alto_x = float(np.median(x))
    return dict(alto_x=round(alto_x / ESCALA, 2),
                ascendente=round((float(np.median(sube)) + correccion) / ESCALA, 2),
                descendente=round((float(np.median(baja)) - correccion) / ESCALA, 2))


def leer(ruta_foto):
    """La foto del pie, leída: por línea, la franja enderezada (cruda y sin desenfoque) y, por
    palabra, dónde cae cada letra; y lo que se midió de la tinta."""
    color = cv2.imread(str(ruta_foto), cv2.IMREAD_COLOR)
    if color is None:
        sys.exit(f"no se pudo leer {ruta_foto}")
    gris = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY).astype(np.float32)
    img = emparejar_luz(gris)
    img = np.clip(cv2.resize(img, None, fx=ESCALA, fy=ESCALA, interpolation=cv2.INTER_CUBIC), 0, 1)
    tinta = img < 0.72
    sabidas = lineas_pie()
    fuente = ImageFont.truetype(FUENTE_TESTIGO, 100)   # solo para saber dónde buscar cada corte
    with tempfile.TemporaryDirectory() as t:
        ws = palabras(img, Path(t))
    claves = sorted({w["linea"] for w in ws}, key=lambda k: np.median([w["caja"][1] for w in ws if w["linea"] == k]))
    claves = [k for k in claves if sum(len(w["texto"]) for w in ws if w["linea"] == k) >= 10]
    if len(claves) != len(sabidas):
        sys.exit(f"se leyeron {len(claves)} líneas y el pie tiene {len(sabidas)}")
    lineas = [curva_de_base([w for w in ws if w["linea"] == c], tinta, img.shape[1]) for c in claves]
    dueno = duenos(tinta, [c for c, _, _ in lineas], [xh for _, xh, _ in lineas])
    leidas = []
    for li, ((curva, xh, extremos), sabida) in enumerate(zip(lineas, sabidas), 1):
        sola = solo_la_linea(img, tinta, dueno, li - 1, curva, xh, extremos)
        recta, base = enderezar(sola, curva, xh)
        leidas.append(dict(recta=recta, cruda=recta, base=base, xh=xh, curva=curva, sabida=sabida))
    medida = tinta_y_desenfoque(leidas)
    for li, L in enumerate(leidas, 1):
        L["recta"] = recta = deshacer_desenfoque(L["cruda"], medida["sigma"])
        palabras_t = L["sabida"].split()
        tramos = palabras_de_linea(recta, [sum(avance(fuente, ch) for ch in p) for p in palabras_t],
                                   fuente.getlength(" "), L["xh"])
        if tramos is None:
            sys.exit(f"línea {li}: no se pudo separar en {len(palabras_t)} palabras")
        ps, j = [], 0
        for texto, (x0, x1) in zip(palabras_t, tramos):
            j = L["sabida"].index(texto, j)
            ps.append(dict(texto=texto, inicio=j, x0=x0, x1=x1,
                           letras=cortar_palabra(recta, x0, x1, texto, [avance(fuente, ch) for ch in texto])))
            j += len(texto)
        L["palabras"] = ps
    medida.update(grosor_de_la_o(leidas, medida["tinta"]))
    medida.update(alturas_por_astas(leidas))
    medida["xh"] = round(float(np.median([L["xh"] for L in leidas])) / ESCALA, 2)
    return leidas, medida


def main(ruta_foto):
    leidas, medida = leer(ruta_foto)
    TESTIGOS.mkdir(exist_ok=True)
    for f in list(TESTIGOS.glob("*.png")) + list(TESTIGOS.glob("*.json")):
        f.unlink()
    registro, n = [], 0
    for li, L in enumerate(leidas, 1):
        recta, base, xh = L["recta"], L["base"], L["xh"]
        print(f"línea {li}: {len(L['palabras'])} palabras; altura de x {xh / ESCALA:.1f} px en la foto")
        margen = int(0.5 * xh)
        for P in L["palabras"]:
            for k, (ch, (a, b)) in enumerate(zip(P["texto"], P["letras"])):
                c0, c1 = max(0, a - margen), min(recta.shape[1], b + margen)
                n += 1
                nombre = f"{n:03d}.png"
                cv2.imwrite(str(TESTIGOS / nombre), (recta[:, c0:c1] * 255).astype(np.uint8))
                registro.append(dict(archivo=nombre, signo=ch, linea=li, palabra=P["texto"].strip(".,()"),
                                     posicion=P["inicio"] + k, x_linea=int(c0), x0=int(a - c0), x1=int(b - c0), base=int(base),
                                     xh=round(float(xh), 1)))
    (TESTIGOS / "pie.json").write_text(json.dumps(dict(
        fuente="Foto de la lámina de la Kochamama (recorte cercano del pie), enderezada línea por línea "
               "y con el desenfoque deshecho en parte",
        escala=ESCALA, tinta=medida, letras=registro), ensure_ascii=False, indent=1), encoding="utf8")
    print(f"tinta llena {medida['tinta']}, desenfoque σ = {medida['sigma']} px ({medida['trazos']} trazos aislados, "
          f"error {medida['error']}); asta {medida['asta']} px, o: lado {medida['lado']} y tope {medida['tope']} px")
    print(f"por astas: altura de x {medida['alto_x']} px, ascendente {medida['ascendente']} px, "
          f"descendente {medida['descendente']} px")
    total = sum(1 for L in leidas for ch in L["sabida"] if not ch.isspace())
    print(f"letras del pie: {total}; con testigo: {len(registro)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
