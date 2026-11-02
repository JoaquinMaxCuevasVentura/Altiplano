#!/usr/bin/env python3
"""Arma el libro de Contenida: un solo documento editorial con todo el proyecto.

Uso (necesita Node, Python 3 con Pillow, NumPy y PyMuPDF; pyphen, si está, corta las palabras):
    cd tipografia/editorial && npm install        # una vez: Vivliostyle
    python3 tipografia/editorial/armar.py         # → tipografia/editorial/contenida_libro.pdf

Opciones:
    --imprenta   papel blanco, 3 mm de sangre y marcas de corte → contenida_libro_imprenta.pdf
    --vistas     además, las dobles páginas en PNG, en .cache/vistas/
    --sin-pdf    solo el HTML (.cache/libro/libro.html), para verlo con `npx vivliostyle preview`

Qué hace:
1. saca el texto del informe de decisiones (extraer_informe.js → .cache/informe.json);
2. prepara las imágenes del repositorio: les saca los títulos a las láminas de la simulación,
   las lleva a 300 ppp en su tamaño de página e iguala su papel con el del libro;
3. compone libro.html: el texto del informe en la retícula y, entre capítulos, las planas
   (páginas compuestas en la retícula) con el pie, la caja, la ficha, el poema y los registros;
4. lo pasa a PDF con Vivliostyle, que compone con Chromium.

El sistema está explicado en README.md y en estilo.css.
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
CACHE = AQUI / ".cache"
LIBRO = CACHE / "libro"
IMG = LIBRO / "img"
FUENTES = TIPO / "laminas" / "fuentes"
SIM = TIPO / "simulacion" / "salida"
TESTIGOS = TIPO / "simulacion" / "testigos"
CERCA = AQUI / "imagenes"

try:
    import pyphen
    DIC = pyphen.Pyphen(lang="es", left=3, right=3)
except ImportError:                     # sin pyphen, el texto va sin cortes
    DIC = None

# ------------------------------------------------------------------ la retícula (mm)
COL, JUNTA, FILA = 19.0, 4.0, 22.619
PASO_C, PASO_F = COL + JUNTA, FILA + JUNTA
ANCHO, ALTO = 180.0, 182.333
ARRIBA, ABAJO, AFUERA, ADENTRO = 28.0, 39.667, 13.0, 17.0
PAPEL = (246, 244, 238)


def x(c):
    return (c - 1) * PASO_C


def y(f):
    return (f - 1) * PASO_F


def an(k):
    return k * PASO_C - JUNTA


def al(k):
    return k * PASO_F - JUNTA


def en(c, f, cs=None, fs=None, w=None, h=None, dx=0.0, dy=0.0):
    """Estilo de un elemento puesto en la retícula: columna c, fila f, cs columnas y fs filas."""
    s = f"left:{x(c) + dx:.3f}mm;top:{y(f) + dy:.3f}mm;"
    if w is not None or cs:
        s += f"width:{(w if w is not None else an(cs)):.3f}mm;"
    if h is not None or fs:
        s += f"height:{(h if h is not None else al(fs)):.3f}mm;"
    return s


# ------------------------------------------------------------------ texto con marcas
MARCAS = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")
FLECHA = ('<svg class="flecha" viewBox="0 0 19 12" aria-hidden="true"><path d="M1 6.5H17M12.2 2L17.6 6.5L12.2 11" '
          'fill="none" stroke="currentColor" stroke-width="1.1"/></svg>')
PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]{8,}")


def esc(t):
    return html.escape(str(t), quote=False)


def texto(t, cortar=True):
    t = esc(t)
    if cortar and DIC:
        t = PALABRA.sub(lambda m: DIC.inserted(m.group(0), hyphen="­"), t)
    return t.replace("→", FLECHA).replace("σ", '<span class="sigma">σ</span>')


def md(t, cortar=True):
    """*cursiva*, **negrita** y `mono`, como en el informe."""
    out = []
    for p in MARCAS.split(str(t)):
        if not p:
            continue
        if p.startswith("**"):
            out.append(f"<strong>{md(p[2:-2], cortar)}</strong>")
        elif p.startswith("*"):
            out.append(f"<em>{texto(p[1:-1], cortar)}</em>")
        elif p.startswith("`"):
            out.append(f"<code>{esc(p[1:-1])}</code>")
        else:
            out.append(texto(p, cortar))
    return "".join(out)


def minuscula(t):
    return t[:1].lower() + t[1:] if t and not t[1:2].isupper() else t


def plano(t):
    """El texto sin marcas, para rótulos y cadenas de la cabeza."""
    return re.sub(r"[*`]", "", str(t))


# ------------------------------------------------------------------ las imágenes y su registro
FIGURAS = []           # una por figura: n, id, qué es, de dónde sale, estado
ESTADOS = {
    "propia": ("propia", ""),
    "maquina": ("propuesta de la máquina", "maquina"),
    "hallada": ("hallada en la lámina", ""),
    "dominio": ("dominio público", ""),
    "permiso": ("pendiente de permiso", "pendiente"),
    "mano": ("pendiente: la mano", "pendiente"),
}


def registrar(que, origen, estado):
    n = len(FIGURAS) + 1
    FIGURAS.append(dict(n=n, id=f"fig-{n}", que=que, origen=origen, estado=estado))
    return n, f"fig-{n}"


def etiqueta(estado):
    nombre, clase = ESTADOS[estado]
    return f'<span class="etiqueta {clase}">{nombre}</span>'


def pie(n, estado, t, cortar=False):
    return f'<span class="fn">fig. {n}</span>{etiqueta(estado)}{md(t, cortar)}'


def fondo(im):
    """El color del papel de una imagen: la mediana de su borde."""
    a = np.asarray(im.convert("RGB"))
    borde = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    return np.median(borde, axis=0)


def igualar(im, papel):
    """Lleva el papel de la imagen al del libro: divide por su fondo y multiplica por el papel.

    Vale para dibujos sobre papel claro; las fotos oscuras quedan como están."""
    f = fondo(im)
    if f.min() < 200:
        return im
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    a = a * (np.array(papel, np.float32) / np.maximum(f, 1))
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8))


def recorte_de_lamina(im):
    """La retícula de una lámina de la simulación, sin su título ni su pie."""
    a = np.asarray(im.convert("L")).astype(np.int16)
    f = np.median(np.concatenate([a[:6].ravel(), a[:, :6].ravel()]))
    umbral = 12 if f < 128 else 40
    m = np.abs(a - f) > umbral
    filas = np.where(m[:, 300:-300].mean(axis=1) > 0.5)[0]
    cols = np.where(m[filas.min():filas.max(), :].mean(axis=0) > 0.5)[0]
    return im.crop((int(cols.min()), int(filas.min()), int(cols.max()) + 1, int(filas.max()) + 1))


class Imagenes:
    def __init__(self, papel):
        self.papel = papel
        IMG.mkdir(parents=True, exist_ok=True)

    def preparar(self, origen, ancho_mm, nombre=None, recorte=None, igualar_papel=True, ppp=300, calidad=88,
                 png=False, gris=False):
        """Copia una imagen del repositorio al libro, en su tamaño de página. Devuelve su ruta relativa."""
        origen = Path(origen)
        nombre = nombre or origen.stem
        destino = IMG / (nombre + (".png" if png else ".jpg"))
        im = Image.open(origen)
        im = im.convert("L" if gris else "RGB")
        if recorte == "lamina":
            im = recorte_de_lamina(im)
        elif recorte:
            im = im.crop(recorte)
        px = int(round(ancho_mm / 25.4 * ppp))
        if im.width > px:
            im = im.resize((px, max(1, round(im.height * px / im.width))), Image.LANCZOS)
        if igualar_papel and not gris:
            im = igualar(im, self.papel)
        if png:
            im.save(destino, optimize=True)
        else:
            im.save(destino, quality=calidad, optimize=True, progressive=True)
        return f"img/{destino.name}", im.size


# ------------------------------------------------------------------ los datos del proyecto
CAJA = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
CELDAS = CAJA["celdas"]
POR_SIGNO = {c["signo"]: c for c in CELDAS}
PIE_TEXTO = (TIPO / "textos" / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
POEMA = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8")
LETRAS_PIE = json.loads((TESTIGOS / "pie.json").read_text(encoding="utf8"))["letras"]
FICHAS = json.loads((SIM / "fichas_simuladas.json").read_text(encoding="utf8"))


def poliza():
    """Placas por signo: el máximo de apariciones en un verso (como inventario.py)."""
    p = Counter()
    for v in [v for v in POEMA.lower().split("\n") if v.strip()]:
        for c, n in Counter(ch for ch in v if not ch.isspace()).items():
            p[c] = max(p[c], n)
    return {c["signo"]: max(1, p[c["signo"]]) for c in CELDAS}


POLIZA = poliza()


def testigo_de(celda):
    """La letra del pie que eligió la simulación como testigo de una celda hallada (ficha de la placa 1)."""
    f = FICHAS[f"{celda['celda']:02d}.01"]["pie"]
    vistas = [l for l in LETRAS_PIE if l["signo"] == celda["signo"]]
    return vistas[f["testigo"] - 1], f


def recorte_testigo(l, arriba=8, abajo=100):
    im = Image.open(TESTIGOS / l["archivo"]).convert("L")
    return im.crop((l["x0"], arriba, l["x1"], abajo))


def en_papel(im_l, papel, tinta=(29, 28, 26)):
    """Una imagen en grises (blanco = papel) pasada a los colores del libro."""
    a = np.asarray(im_l).astype(np.float32) / 255.0
    p, t = np.array(papel, np.float32), np.array(tinta, np.float32)
    rgb = t + (p - t) * a[..., None]
    return Image.fromarray(np.clip(rgb + 0.5, 0, 255).astype(np.uint8))


# ------------------------------------------------------------------ el informe en bloques
def leer_informe():
    subprocess.run(["node", str(AQUI / "extraer_informe.js")], check=True, cwd=AQUI)
    bloques = json.loads((CACHE / "informe.json").read_text(encoding="utf8"))
    caps, actual, fuera = [], None, True
    for b in bloques:
        if b["t"] == "h1":
            t = b["md"]
            m = re.match(r"(\d+)\.\s+(.*)", t)
            if m:
                actual = dict(num=int(m.group(1)), titulo=m.group(2), bloques=[])
                caps.append(actual)
                fuera = False
            else:
                actual = dict(num=None, titulo=t, bloques=[])
                caps.append(actual)
                fuera = t in ("Índice",)
            continue
        if actual is not None and not fuera:
            actual["bloques"].append(b)
    return {(c["num"] if c["num"] is not None else c["titulo"]): c for c in caps}


def partir_numero(t):
    m = re.match(r"(\d+(?:\.\d+)*)\.?\s+(.*)", t)
    return (m.group(1), m.group(2)) if m else ("", t)


# ------------------------------------------------------------------ las tablas
def tabla_html(b, clase=""):
    filas = b["filas"]
    n = len(filas[0])
    largo = sum(len(c["md"]) for f in filas for c in f) / max(1, len(filas))
    ancha = n >= 4 or largo > 170 or "ancha" in clase
    total = sum(b["anchos"]) or 1
    cols = "".join(f'<col style="width:{100 * a / total:.1f}%">' for a in b["anchos"])
    o = [f'<table class="tabla {"ancha" if ancha else ""} {clase}"><colgroup>{cols}</colgroup>']
    if b.get("cabeza") and any(c.strip() for c in b["cabeza"]):
        o.append("<thead><tr>" + "".join(f"<th>{md(c, False)}</th>" for c in b["cabeza"]) + "</tr></thead>")
    o.append("<tbody>")
    for f in filas:
        if f[0]["md"].startswith("**") and all(not c["md"].strip() for c in f[1:]):
            o.append(f'<tr class="grupo"><td colspan="{n}">{md(f[0]["md"], False)}</td></tr>')
            continue
        tds = []
        for c in f:
            cl = " ".join(k for k in ("mono", "violeta", "cursiva") if c.get(k))
            contenido = "<br>".join(md(linea, not c.get("mono")) for linea in c["md"].split("\n"))
            tds.append(f'<td class="{cl}">{contenido}</td>')
        o.append("<tr>" + "".join(tds) + "</tr>")
    o.append("</tbody></table>")
    return "".join(o)


# ------------------------------------------------------------------ el libro
class Libro:
    def __init__(self, imprenta=False):
        self.imprenta = imprenta
        self.papel = (255, 255, 255) if imprenta else PAPEL
        self.im = Imagenes(self.papel)
        self.partes = []          # el HTML, en orden
        self.indice = []          # (id, título, nivel)
        self.caps = leer_informe()

    def add(self, *h):
        self.partes.extend(h)

    # -------------------------------------------------------------- figuras dentro del texto
    def figura(self, archivo_origen, que, estado, pie_texto, clase="flota ancho pie-abajo", ancho=180.0, recorte=None,
               origen_rel=None, png=False):
        n, fid = registrar(que, origen_rel or str(Path(archivo_origen).relative_to(TIPO)), estado)
        ancho_img = 134.0 if "pie-al-lado" in clase else ancho
        if estado == "maquina":
            ancho_img -= 4.8
        ruta, _ = self.im.preparar(archivo_origen, ancho_img, nombre=f"{n:03d}_{Path(archivo_origen).stem}",
                                   recorte=recorte, png=png)
        cls = f"{clase} {estado}"
        return (f'<figure id="{fid}" class="{cls}"><div class="marco"><img src="{ruta}" alt=""></div>'
                f'<figcaption>{pie(n, estado, pie_texto)}</figcaption></figure>')

    def vacio_margen(self, que, estado, t, alto=31.5):
        n, fid = registrar(que, "—", estado)
        violeta = " violeta" if estado in ("permiso", "mano") else ""
        return (f'<div class="margen" id="{fid}"><div class="vacio{violeta}" style="height:{alto}mm"></div>'
                f'<p style="margin-top:2mm">{pie(n, estado, t)}</p></div>')

    def al_margen(self, destino, t):
        """Una llamada al margen: el nombre de lo que sigue en otra página y su número."""
        return (f'<p class="margen salto"><a href="#{destino}">{esc(t)}</a> {FLECHA}'
                f'<span class="pag" data-ref="#{destino}"></span></p>')

    # -------------------------------------------------------------- un capítulo del informe
    def capitulo(self, num, extras=None, despues=None):
        extras = extras or {}
        c = self.caps[num]
        titulo = minuscula(c["titulo"])
        cid = f"cap-{num}"
        secciones = []
        for b in c["bloques"]:
            if b["t"] == "h2":
                n, t = partir_numero(b["md"])
                secciones.append((n, t, f"s-{n.replace('.', '-')}"))
        self.indice.append((cid, f"{num}", titulo))
        idx = "".join(f'<a href="#{sid}">{esc(n)} {md(minuscula(t), False)}</a>' for n, t, sid in secciones)
        o = [f'<section class="capitulo" id="{cid}">',
             f'<header class="apertura"><p class="num">capítulo<b>{num}</b></p>'
             f'<h1 data-corrida="{num} · {esc(plano(titulo))}">{md(titulo, False)}</h1>'
             f'<nav class="indice">{idx}</nav></header>',
             '<div class="texto">']
        o.extend(extras.get("inicio", []))
        mapas = []
        bl = c["bloques"]
        i = 0
        while i < len(bl):
            b = bl[i]
            t = b["t"]
            if t == "h2":
                n, tt = partir_numero(b["md"])
                sid = f"s-{n.replace('.', '-')}"
                o.append(f'<h2 id="{sid}" data-corrida="{esc(n)} {esc(plano(minuscula(tt)))}"><span class="n">{esc(n)}</span>'
                         f'{md(tt, False)}</h2>')
                o.extend(extras.get(n, []))
            elif t == "p":
                o.append(f"<p>{md(b['md'])}</p>")
            elif t == "item":
                lista = b["lista"]
                items = []
                while i < len(bl) and bl[i]["t"] == "item" and bl[i]["lista"] == lista:
                    items.append(f"<li>{md(bl[i]['md'])}</li>")
                    i += 1
                i -= 1
                etiqueta_lista = "ul" if lista == "vinetas" else "ol"
                o.append(f'<{etiqueta_lista} class="{lista}">{"".join(items)}</{etiqueta_lista}>')
            elif t == "verso":
                v = b["md"].replace(" / ", "<br>")
                o.append(f'<p class="verso">{md(v, False).replace("&lt;br&gt;", "<br>")}</p>')
            elif t == "cita":
                if "→" in b["md"]:
                    pasos = [p.strip() for p in b["md"].split("→")]
                    o.append('<p class="cita cadena">' + f" {FLECHA}<br>".join(esc(p) for p in pasos) + "</p>")
                else:
                    o.append(f'<p class="cita">{md(b["md"], False)}</p>')
            elif t == "tabla":
                o.append(tabla_html(b, extras.get(f"tabla-{len([x for x in bl[:i] if x['t'] == 'tabla'])}", "")))
            elif t == "figura":
                if b.get("mapa"):
                    mapas.append(b)
                else:
                    o.append(self.figura_del_informe(b))
            i += 1
        o.extend(extras.get("fin", []))
        o.append("</div></section>")
        self.add(*o)
        for m in mapas:
            self.plana_mapa(m)
        for f in despues or []:
            f()

    FIGS_INFORME = {
        "20_gramatica.png": (SIM / "20_gramatica.png", "Los cuatro generadores de la gramática", "maquina", "flota ancho pie-abajo"),
        "21_gramatica_caja.png": (SIM / "21_gramatica_caja.png", "Los 55 cuerpos base en la caja", "maquina",
                                  "flota ancho pie-al-lado"),
        "P-03_o_cuenca.png": (TIPO / "planos" / "png" / "P-03_o_cuenca.png", "Plano P-03: la o, la cuenca", "propia",
                              "flota ancho pie-abajo"),
        "12_cadena_08.jpg": (SIM / "12_cadena_08.jpg", "Una letra de punta a punta: la a", "maquina", "flota ancho pie-abajo"),
        "aplicacion.png": (TIPO / "informe" / "img" / "aplicacion.png", "La aplicación de las decisiones de la letra",
                           "maquina", "flota ancho pie-abajo"),
        "R-01_metodo.png": (TIPO / "taxonomia" / "png" / "R-01_metodo.png", "Lámina R-01: el método", "propia",
                            "flota ancho pie-abajo"),
        "R-02_cuadro.png": (TIPO / "taxonomia" / "png" / "R-02_cuadro.png", "Lámina R-02: el cuadro de las referencias",
                            "propia", "flota ancho pie-abajo"),
    }

    def figura_del_informe(self, b):
        origen, que, estado, clase = self.FIGS_INFORME[b["archivo"]]
        return self.figura(origen, que, estado, b["pie"], clase=clase)

    # -------------------------------------------------------------- las planas
    def plana(self, contenido, clase="", pid=None):
        pid_attr = f' id="{pid}"' if pid else ""
        self.add(f'<section class="plana {clase}"{pid_attr}>', *contenido, "</section>")

    def plana_mapa(self, b):
        n_mapa = b["mapa"]
        origen = TIPO / "informe" / "mapas" / b["archivo"]
        n, fid = registrar(f"Mapa {n_mapa}", str(origen.relative_to(TIPO)), "propia")
        w, h = Image.open(origen).size
        if w > h:                                     # el mapa 2, apaisado: a todo el ancho, el pie abajo
            ancho = ANCHO
            alto = ancho * h / w
            ruta, _ = self.im.preparar(origen, ancho, nombre=f"{n:03d}_mapa_{n_mapa}")
            self.plana([f'<div style="{en(1, 1, 8)}"><img src="{ruta}" style="width:100%" alt=""></div>',
                        f'<p class="rotulo" style="{en(4, 1, 5, dy=alto + 5)}">{pie(n, "propia", b["pie"])}</p>'],
                       pid=fid)
        else:                                         # en c3–c8, a toda la altura; el pie en c1–c2, abajo
            ancho = an(6)
            alto = min(ALTO, ancho * h / w)
            ancho = alto * w / h
            ruta, _ = self.im.preparar(origen, ancho, nombre=f"{n:03d}_mapa_{n_mapa}")
            self.plana([f'<div style="left:{ANCHO - ancho:.3f}mm;top:0;width:{ancho:.3f}mm"><img src="{ruta}" '
                        f'style="width:100%" alt=""></div>',
                        f'<p class="rotulo" style="left:0;bottom:0;width:{an(2)}mm">{pie(n, "propia", b["pie"])}</p>'],
                       pid=fid)


def construir(args):
    lb = Libro(imprenta=args.imprenta)
    from planas import componer          # las planas y el orden del libro
    componer(lb)
    escribir_html(lb)
    if args.sin_pdf:
        print("listo:", LIBRO / "libro.html")
        return
    pdf = AQUI / ("contenida_libro_imprenta.pdf" if args.imprenta else "contenida_libro.pdf")
    vivliostyle(LIBRO / "libro.html", pdf, args.imprenta)
    if args.vistas:
        vistas(pdf)


def escribir_html(lb):
    LIBRO.mkdir(parents=True, exist_ok=True)
    (LIBRO / "fuentes").mkdir(exist_ok=True)
    for f in FUENTES.glob("*.woff2"):
        if "belle" not in f.name:
            shutil.copy2(f, LIBRO / "fuentes" / f.name)
    css = (AQUI / "estilo.css").read_text(encoding="utf8")
    if lb.imprenta:
        css = css.replace("background: #f6f4ee;", "background: #ffffff;\n  bleed: 3mm;\n  marks: crop cross;")
        css = css.replace("--papel: #f6f4ee;", "--papel: #ffffff;")
    (LIBRO / "estilo.css").write_text(css, encoding="utf8")
    doc = ['<!doctype html>', '<html lang="es"><head><meta charset="utf-8">',
           '<title>Contenida: acciones para componer una voz</title>',
           '<meta name="author" content="Joaquin Max Cuevas Ventura">',
           '<meta name="description" content="El libro del proyecto tipográfico Contenida, en homenaje a Contener una ruina: '
           'acciones para desenterrar una voz, de Rebeca Paz Prada con CreaciónxAcuerpamiento.">',
           '<link rel="stylesheet" href="estilo.css"></head><body>']
    doc.extend(lb.partes)
    doc.append("</body></html>")
    (LIBRO / "libro.html").write_text("\n".join(doc), encoding="utf8")


def chromium():
    for c in [os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"]:
        if c and Path(c).exists():
            return c
    return None


def vivliostyle(html_, pdf, imprenta):
    viv = AQUI / "node_modules" / ".bin" / "vivliostyle"
    if not viv.exists():
        sys.exit("falta Vivliostyle: corre `npm install` en tipografia/editorial/")
    cmd = [str(viv), "build", str(html_), "-o", str(pdf), "--timeout", "900", "--log-level", "info"]
    ch = chromium()
    if ch:
        cmd += ["--executable-browser", ch]
    subprocess.run(cmd, check=True, cwd=AQUI)
    import pymupdf
    d = pymupdf.open(pdf)
    d.set_metadata({"title": "Contenida: acciones para componer una voz", "author": "Joaquin Max Cuevas Ventura",
                    "subject": "Un proyecto tipográfico en homenaje a Contener una ruina: acciones para desenterrar una voz, "
                               "de Rebeca Paz Prada con CreaciónxAcuerpamiento",
                    "keywords": "Contenida, tipografía, repujado, documento de trabajo",
                    "creator": "tipografia/editorial/armar.py · Vivliostyle", "producer": "Vivliostyle + PyMuPDF"})
    d.saveIncr()
    print("listo:", pdf, d.page_count, "páginas", f"{pdf.stat().st_size / 1e6:.1f} MB")


def vistas(pdf, dpi=40):
    import pymupdf
    out = CACHE / "vistas"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    d = pymupdf.open(pdf)
    ims = []
    for p in d:
        pix = p.get_pixmap(dpi=dpi)
        ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    w, h = ims[0].size
    # la primera página va sola, a la derecha; después, de a dos
    pares = [[None, ims[0]]] + [ims[i:i + 2] for i in range(1, len(ims), 2)]
    for k, par in enumerate(pares):
        s = Image.new("RGB", (2 * w + 6, h + 6), (70, 70, 70))
        for j, im in enumerate(par):
            if im is not None:
                s.paste(im, (3 + j * w, 3))
        s.save(out / f"doble_{k:03d}.png")
    print("vistas:", out, len(pares))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Arma el libro de Contenida.")
    ap.add_argument("--imprenta", action="store_true")
    ap.add_argument("--vistas", action="store_true")
    ap.add_argument("--sin-pdf", action="store_true")
    sys.path.insert(0, str(AQUI))
    construir(ap.parse_args())
