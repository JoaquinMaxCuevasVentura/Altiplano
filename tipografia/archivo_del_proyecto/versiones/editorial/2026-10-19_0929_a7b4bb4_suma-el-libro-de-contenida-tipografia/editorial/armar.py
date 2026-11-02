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
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import cubierta  # noqa: E402
from libro import CACHE, FUENTES, LIBRO, Libro  # noqa: E402
from planas import componer  # noqa: E402


def construir(args):
    lb = Libro(imprenta=args.imprenta)
    componer(lb)
    escribir_html(lb)
    if args.sin_pdf:
        print("listo:", LIBRO / "libro.html")
        return
    pdf = AQUI / ("contenida_libro_imprenta.pdf" if args.imprenta else "contenida_libro.pdf")
    vivliostyle(LIBRO / "libro.html", pdf, args.imprenta)
    import pymupdf
    paginas = pymupdf.open(pdf).page_count
    lomo = cubierta.escribir(lb, paginas)
    if args.imprenta:                        # el pliego de la cubierta va aparte, con sus planchas
        vivliostyle(LIBRO / "cubierta.html", AQUI / "contenida_cubierta_imprenta.pdf", True, metadatos=False)
        print(f"lomo: {lomo} mm para {paginas} páginas")
    else:                                    # en pantalla, el libro empieza por su tapa y termina en su contratapa
        vivliostyle(LIBRO / "tapa.html", CACHE / "tapa.pdf", False, metadatos=False)
        vivliostyle(LIBRO / "contratapa.html", CACHE / "contratapa.pdf", False, metadatos=False)
        encuadernar(pdf, CACHE / "tapa.pdf", CACHE / "contratapa.pdf")
        lista_de_imagenes(pdf)
        muestras(pdf)
    if args.vistas:
        vistas(pdf)


def lista_de_imagenes(pdf):
    """imagenes.md: cada figura con su página, de dónde sale y su estado (la misma lista que cierra el libro)."""
    import re
    import pymupdf
    from libro import ESTADOS, FIGURAS
    d = pymupdf.open(pdf)
    pagina = {}
    for p in d:
        for m in re.finditer(r"fig\. (\d+)", p.get_text()):
            pagina.setdefault(int(m.group(1)), p.get_label())
    filas = ["# Las imágenes del libro", "",
             "Generada por `armar.py` desde el registro de figuras. Cada figura dice qué es: **propia** (dibujada para el",
             "proyecto, con código, desde sus documentos), **propuesta de la máquina** (sale de la simulación o de la",
             "aplicación; ninguna de sus formas entra en la caja ni en la fuente), **hallada en la lámina** (letras recortadas",
             "de la foto del pie), **dominio público** (con su licencia y su fuente en `../10_imagenes_de_dominio_publico.md`)",
             "o **pendiente** (un lugar punteado que espera un permiso o la mano). Las rutas son desde `tipografia/`.", "",
             "| Fig. | Pág. | Qué es | De dónde sale | Estado |", "|---|---|---|---|---|"]
    for f in FIGURAS:
        origen = f["origen"].replace("|", "·")
        filas.append(f"| {f['n']} | {pagina.get(f['n'], '—')} | {f['que']} | `{origen}` | {ESTADOS[f['estado']][0]} |")
    (AQUI / "imagenes.md").write_text("\n".join(filas) + "\n", encoding="utf8")
    print("imagenes.md:", len(FIGURAS), "figuras")


MUESTRAS = [("tapa", None), ("el_pie", "El pie, letra por letra"), ("el_sistema", "Nueve reglas"),
            ("la_caja", "La caja de 8 × 7, hoy"), ("la_ficha", "La misma ficha, llenada"), ("de_cerca", "la placa, de cerca"),
            ("el_poema", "El poema compuesto con la caja"), ("punta_a_punta", "Del pie a la voz, una letra")]


def muestras(pdf, dpi=96):
    """Algunas dobles páginas en JPG, para el README (muestras/)."""
    import pymupdf
    destino = AQUI / "muestras"
    shutil.rmtree(destino, ignore_errors=True)
    destino.mkdir()
    d = pymupdf.open(pdf)

    def imagen(i):
        pix = d[i].get_pixmap(dpi=dpi)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    for k, (nombre, marca) in enumerate(MUESTRAS, 1):
        if marca is None:                                     # la tapa sola, con la contratapa al lado
            par = [d.page_count - 1, 0]
        else:
            i = next(p.number for p in d if marca in p.get_text().replace("\u00ad", "").replace("\n", " "))
            n = int(d[i].get_label())
            izq = i if n % 2 == 0 else i - 1
            par = [izq, izq + 1]
        ims = [imagen(i) for i in par]
        w, h = ims[0].size
        s = Image.new("RGB", (2 * w + 8, h), (58, 58, 56))
        s.paste(ims[0], (0, 0))
        s.paste(ims[1], (w + 8, 0))
        s.save(destino / f"{k:02d}_{nombre}.jpg", quality=84, optimize=True, progressive=True)
    print("muestras:", destino, len(MUESTRAS))


def encuadernar(pdf, tapa, contratapa):
    """Pone la tapa adelante y la contratapa atrás, con etiquetas de página que respetan los folios."""
    import pymupdf
    libro = pymupdf.open(pdf)
    n = libro.page_count
    junto = pymupdf.open()
    junto.insert_pdf(pymupdf.open(tapa))
    junto.insert_pdf(libro)
    junto.insert_pdf(pymupdf.open(contratapa))
    junto.set_metadata(libro.metadata)
    toc = libro.get_toc(simple=False)
    junto.set_page_labels([{"startpage": 0, "prefix": "tapa", "style": "", "firstpagenum": 1},
                           {"startpage": 1, "prefix": "", "style": "D", "firstpagenum": 1},
                           {"startpage": n + 1, "prefix": "contratapa", "style": "", "firstpagenum": 1}])
    if toc:
        for entrada in toc:
            entrada[2] += 1
        junto.set_toc(toc)
    temporal = pdf.with_suffix(".tmp.pdf")
    junto.save(temporal, garbage=3, deflate=True)
    temporal.replace(pdf)
    print("encuadernado:", pdf, junto.page_count, "páginas")


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


def vivliostyle(html_, pdf, imprenta, metadatos=True):
    viv = AQUI / "node_modules" / ".bin" / "vivliostyle"
    if not viv.exists():
        sys.exit("falta Vivliostyle: corre `npm install` en tipografia/editorial/")
    cmd = [str(viv), "build", str(html_), "-o", str(pdf), "--timeout", "900", "--log-level", "info"]
    ch = chromium()
    if ch:
        cmd += ["--executable-browser", ch]
    subprocess.run(cmd, check=True, cwd=AQUI, stdout=subprocess.DEVNULL)
    if not metadatos:
        return
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
    # la tapa y la página 1 van solas, a la derecha; después, de a dos; la contratapa, sola a la izquierda
    etiquetas = [p.get_label() for p in d]
    pares, i = [], 0
    if etiquetas[0] == "tapa":
        pares.append([None, ims[0]])
        i = 1
    pares.append([None, ims[i]])
    i += 1
    while i < len(ims):
        if etiquetas[i] == "contratapa":
            pares.append([ims[i], None])
            break
        par = ims[i:i + 2] if i + 1 < len(ims) and etiquetas[i + 1] != "contratapa" else [ims[i], None]
        pares.append(par)
        i += len([p for p in par if p is not None])
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
    construir(ap.parse_args())
