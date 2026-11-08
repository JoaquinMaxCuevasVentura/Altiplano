#!/usr/bin/env python3
"""Arma el espécimen de Contenida con Typst: contenida_especimen.pdf y sus vistas.

Uso (desde la raíz del repositorio):
    pip install typst fonttools brotli pillow numpy pymupdf
    python3 tipografia/especimen/armar.py

Prepara en tipografia/especimen/.cache/, que no entra en el repositorio:
  fuentes/   Newsreader y Courier Prime en TTF (Typst no lee WOFF2), de ../laminas/fuentes/;
  img/       las letras halladas del pie, recortadas de los testigos (simulacion/testigos/),
             y los estados de la «a» y de la «z», recortados de sus cadenas (simulacion/salida/);
  datos.json la caja con sus testigos, los estados, la póliza y los versos que se componen.

Compila especimen.typ con la raíz en tipografia/ (lee también esquemas/ y simulacion/) y deja
contenida_especimen.pdf y una vista de cada página en paginas/. Si está el programa typst, puede
usarse en su lugar: typst compile --root tipografia --font-path tipografia/especimen/.cache/fuentes
tipografia/especimen/especimen.typ, después de correr este script una vez (escribe la caché).

El espécimen no compone texto con la letra: la letra todavía no existe, la hacen las manos.
Lo que hizo la máquina va rotulado como propuesta de la máquina.
"""

import datetime
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
CACHE = AQUI / ".cache"
FUENTES = TIPO / "laminas" / "fuentes"
SALIDA = TIPO / "simulacion" / "salida"
TESTIGOS = TIPO / "simulacion" / "testigos"
PDF = AQUI / "contenida_especimen.pdf"
TINTA = (29, 28, 26)
FECHA = datetime.datetime(2026, 11, 8, 12, 0, tzinfo=datetime.timezone.utc)   # la del espécimen: rehacerlo no lo cambia

sys.path.insert(0, str(TIPO / "digital"))
import poliza as pz  # noqa: E402

ESTADOS = ["el pie", "la gramática", "calco", "placa, reverso", "placa", "cinta", "frotado", "agua quieta",
           "agua tocada", "voz"]
# los versos que se componen en la caja: los que piden una reconstruida, y el que cierra la obra
VERSOS = ["Quedó el contenedor", "Tocas el agua y la diosa se deforma.", "Termina y empieza,"]


def fuentes():
    """Las fuentes del proyecto, de WOFF2 a TTF: Typst no lee WOFF2."""
    from fontTools.ttLib import TTFont
    destino = CACHE / "fuentes"
    destino.mkdir(parents=True, exist_ok=True)
    for f in sorted(FUENTES.glob("*.woff2")):
        if "belle" in f.name:                 # la letra que imita una mano no se usa: lo de mano se hace a mano
            continue
        ttf = destino / (f.stem + ".ttf")
        if not ttf.exists():
            t = TTFont(f)
            t.flavor = None
            t.save(ttf)
    return destino


def tinta(g):
    """Un testigo en gris, como tinta sobre transparente: el papel es el de la página."""
    k = 1 - np.asarray(g, np.float32) / 255
    a = np.clip((k - 0.16) / 0.56, 0, 1)
    rgba = np.zeros(k.shape + (4,), np.uint8)
    rgba[..., :3] = TINTA
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def testigos(caja):
    """De cada signo hallado, su primera aparición en el pie, recortada con el mismo aire arriba y abajo."""
    letras = json.loads((TESTIGOS / "pie.json").read_text(encoding="utf8"))["letras"]
    destino = CACHE / "img"
    destino.mkdir(parents=True, exist_ok=True)
    for c in caja:
        if c["estado"] != "hallada":
            continue
        L = next(l for l in letras if l["signo"] == c["signo"])
        g = Image.open(TESTIGOS / L["archivo"]).convert("L")
        xh, b = L["xh"], L["base"]
        m = 0.18 * xh
        caja_ = (max(0, int(L["x0"] - m)), int(b - 2.1 * xh), min(g.width, int(L["x1"] + m)), int(b + 0.9 * xh))
        recorte = g.crop(caja_)
        ruta = destino / f"testigo_{c['celda']:02d}.png"
        tinta(recorte).save(ruta)
        c["testigo"] = f"/especimen/.cache/img/{ruta.name}"
        c["palabra"] = L["palabra"]
        c["ancho"] = round(recorte.width / recorte.height, 3)


def paneles(ruta, prefijo):
    """Los diez estados de una cadena (simulacion/salida/12_cadena_*.jpg), cada uno en su archivo."""
    im = Image.open(ruta).convert("RGB")
    a = np.asarray(im, np.float32)
    papel = a[5, 5]
    banda = np.abs(a[90:300] - papel).sum(axis=2).mean(axis=0) > 6       # las columnas con imagen
    tramos, i = [], 0
    while i < len(banda):
        if banda[i]:
            j = i
            while j + 1 < len(banda) and banda[j + 1]:
                j += 1
            if j - i > 60:
                tramos.append((i, j + 1))
            i = j + 1
        else:
            i += 1
    if len(tramos) != len(ESTADOS):
        sys.exit(f"{ruta.name}: se esperaban {len(ESTADOS)} estados y se encontraron {len(tramos)}")
    rutas = []
    for k, (x0, x1) in enumerate(tramos):
        col = np.abs(a[:, x0:x1] - papel).sum(axis=2).mean(axis=1) > 6
        filas = np.nonzero(col[40:330])[0] + 40
        y0, y1 = int(filas.min()), int(filas.max()) + 1
        destino = CACHE / "img" / f"{prefijo}_{k:02d}.jpg"
        im.crop((x0, y0, x1, y1)).save(destino, quality=92)
        rutas.append(f"/especimen/.cache/img/{destino.name}")
    return rutas


def componer(verso, placas):
    """Un verso en la caja: cada signo es una placa; a cada uno le toca la primera que no esté ya en el verso.
    Las mayúsculas se escriben en caja baja; entre palabras, una celda vacía."""
    usadas, celdas = Counter(), []
    for ch in verso.lower():
        if ch == " ":
            celdas.append(dict(s=" "))
            continue
        usadas[ch] += 1
        n = placas.get(ch, 0)
        celdas.append(dict(s=ch, placa=min(usadas[ch], n) if n else 0, de=n))
    return celdas


def datos():
    caja = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))["celdas"]
    testigos(caja)
    p = pz.poliza(pz.juego(), pz.versos())
    placas = dict(p)
    versos = pz.versos()
    for v in VERSOS:
        assert v in versos, v
    # las medidas de la letra, de la gramática (en px del lienzo de la placa: 4 por mm)
    e = json.loads((SALIDA / "gramatica" / "gramatica.json").read_text(encoding="utf8"))["esqueleto"]
    razon_celda = json.loads((TIPO / "esquemas" / "celda_medida.json").read_text(encoding="utf8"))["celda"]
    alto, cy = (e["desague"] - e["afuera"]) * 1.1, (e["afuera"] + e["desague"]) / 2      # como gramatica.celda()
    x0, y0, x1, y1 = 300 - razon_celda / 2 * alto, cy - alto / 2, 300 + razon_celda / 2 * alto, cy + alto / 2
    U = 1000 / (y1 - y0)
    medidas = dict(celda=dict(x0=x0 / 4, y0=y0 / 4, ancho=(x1 - x0) / 4, alto=(y1 - y0) / 4, avance=round((x1 - x0) * U)),
                   lineas={k: dict(mm=e[k] / 4, upm=round((e["fondo"] - e[k]) * U)) for k in ("afuera", "borde", "fondo", "desague")},
                   canal=dict(mm=round(e["canal"] / 4, 1), upm=round(e["canal"] * U)), celda_razon=razon_celda)
    import re
    informe = (TIPO / "simulacion" / "informe.md").read_text(encoding="utf8")
    m = re.search(r"hasta la frotada ([0-9,]+); las reconstruidas, hasta la ([0-9,]+)", informe)
    # el pie, a máquina: la primera aparición de cada signo hallado, con el número de su celda
    pie = (TIPO / "textos" / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
    primera = {}
    for c in caja:
        if c["estado"] == "hallada":
            primera[pie.index(c["signo"])] = c["celda"]
    tramos, actual = [], ""
    for i, ch in enumerate(pie):
        if i in primera:
            if actual:
                tramos.append(dict(t=actual))
            tramos.append(dict(t=ch, celda=primera[i]))
            actual = ""
        else:
            actual += ch
    if actual:
        tramos.append(dict(t=actual))
    d = dict(
        pie=tramos,
        medidas=medidas,
        frotadas=dict(halladas=m.group(1), reconstruidas=m.group(2)),
        caja=caja,
        estados=dict(nombres=ESTADOS, a=paneles(SALIDA / "12_cadena_08.jpg", "a"), z=paneles(SALIDA / "12_cadena_32.jpg", "z")),
        poliza=dict(total=sum(p.values()), placas=placas, versos=len(versos),
                    maximo=max(len(v) for v in versos)),
        compuestos=[dict(verso=v, celdas=componer(v, placas)) for v in VERSOS],
        fecha=FECHA.strftime("%d.%m.%Y"),
    )
    (CACHE / "datos.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
    return d


def compilar(fuentes_):
    try:
        import typst
    except ImportError:
        typst = None
    if typst is not None:
        typst.compile(str(AQUI / "especimen.typ"), output=str(PDF), root=str(TIPO), font_paths=[str(fuentes_)],
                      ignore_system_fonts=True, timestamp=FECHA)
    elif shutil.which("typst"):
        subprocess.run(["typst", "compile", "--root", str(TIPO), "--font-path", str(fuentes_), "--ignore-system-fonts",
                        str(AQUI / "especimen.typ"), str(PDF)], check=True,
                       env={"SOURCE_DATE_EPOCH": str(int(FECHA.timestamp())), "PATH": "/usr/bin:/bin:/usr/local/bin"})
    else:
        sys.exit("Falta Typst: pip install typst (o el programa typst).")


def vistas():
    try:
        import pymupdf
    except ImportError:
        return 0
    destino = AQUI / "paginas"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir()
    doc = pymupdf.open(PDF)
    for i, pag in enumerate(doc, 1):
        pag.get_pixmap(dpi=72).save(destino / f"{i:02d}.png")
    n = doc.page_count
    doc.close()
    return n


def main():
    CACHE.mkdir(exist_ok=True)
    f = fuentes()
    d = datos()
    compilar(f)
    n = vistas()
    print(f"listo: {PDF} · {n} páginas · {sum(1 for c in d['caja'] if c.get('testigo'))} letras halladas · "
          f"{d['poliza']['total']} placas")


if __name__ == "__main__":
    main()
