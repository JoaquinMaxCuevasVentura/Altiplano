"""La póliza en OpenType: dentro de un verso, ninguna placa se repite.

Uso (desde la raíz del repositorio):
    python3 tipografia/digital/poliza.py            # escribe poliza.fea
    python3 tipografia/digital/poliza.py --probar   # y lo prueba con HarfBuzz, verso por verso

En la caja, cada aparición de un signo dentro de un verso es otra placa: 9 «a»,
8 «e»… (`textos/inventario.md`). En la fuente digital cada placa será una variante
(`a.01` … `a.09`), escaneada de una placa real (`05`, §5.3). Este archivo escribe la
regla que las reparte: a cada signo le toca la primera placa que no aparezca entre
los signos anteriores del verso. Si un texto pide más placas de las que hay, las que
sobran toman la última: la caja se acabó.

OpenType solo mira atrás una cantidad fija de signos. Por eso la regla mira tantos
como tiene el verso más largo del poema (44, con los espacios): para cualquier verso
del poema, el reparto es exacto. En un texto con líneas más largas, una placa puede
volver a aparecer más allá de esa distancia, y se dice.

La prueba arma una fuente de cajas vacías, sin ninguna forma de letra (las formas
las hace la mano), y nunca se guarda en el repositorio.
"""

import argparse
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

from fontTools.agl import UV2AGL

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
POEMA = TIPO / "textos" / "poema.txt"
CAJA = TIPO / "esquemas" / "caja.json"
SALIDA = AQUI / "poliza.fea"

# Las métricas de la celda (`05`, §5.3): el eme es el alto de la celda; el avance, 0,84 de él.
EME, AVANCE, ASCENDENTE, DESCENDENTE = 1000, 840, 734, -266


def nombre(signo):
    """El nombre de glifo de un signo (lista de Adobe), o uniXXXX."""
    return UV2AGL.get(ord(signo), f"uni{ord(signo):04X}")


def versos():
    return [v.strip() for v in POEMA.read_text(encoding="utf8").split("\n") if v.strip()]


def juego():
    """Los 55 signos de la caja y el signo final."""
    return [c["signo"] for c in json.loads(CAJA.read_text(encoding="utf8"))["celdas"]]


def poliza(signos, vs):
    """Placas por signo: las que pide el verso que más lo usa; al menos una por celda."""
    p = Counter({s: 1 for s in signos})
    for v in vs:
        for s, n in Counter(v.lower()).items():
            if s in p:
                p[s] = max(p[s], n)
    return p


def fea(p, ventana):
    """Una búsqueda por número de placa: la k-ésima placa va al signo que no la tiene detrás."""
    todos = []
    for s, n in p.items():
        todos.append(nombre(s))
        todos += [f"{nombre(s)}.{k:02d}" for k in range(1, n + 1)]
    lineas = ["# Generado por tipografia/digital/poliza.py: no editar a mano.",
              f"# {sum(p.values())} placas; mira {ventana - 1} signos atrás (el verso más largo tiene {ventana}).",
              "", "languagesystem DFLT dflt;", "languagesystem latn dflt;", "",
              "@TODO = [space " + " ".join(todos) + "];", ""]
    for k in range(1, max(p.values()) + 1):
        lineas.append(f"lookup placa_{k:02d} {{")
        for s, n in p.items():
            if n < k:
                continue
            base, placa = nombre(s), f"{nombre(s)}.{k:02d}"
            if k < n:                           # a la última placa le toca lo que quede: no hace falta mirar
                for hueco in range(ventana - 1):
                    lineas.append(f"    ignore sub {placa} {'@TODO ' * hueco}{base}';")
            lineas.append(f"    sub {base}' by {placa};")
        lineas.append(f"}} placa_{k:02d};")
        lineas.append("")
    lineas.append("feature calt {")
    lineas += [f"    lookup placa_{k:02d};" for k in range(1, max(p.values()) + 1)]
    lineas.append("} calt;")
    return "\n".join(lineas) + "\n"


def fuente_de_prueba(p, texto_fea, destino):
    """Una fuente de celdas vacías, con las métricas de la celda. Solo sirve para probar la regla."""
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    glifos = [".notdef", "space"]
    for s, n in p.items():
        glifos += [nombre(s)] + [f"{nombre(s)}.{k:02d}" for k in range(1, n + 1)]
    fb = FontBuilder(EME, isTTF=True)
    fb.setupGlyphOrder(glifos)
    cmap = {32: "space"}
    for s in p:
        cmap[ord(s)] = nombre(s)
        if s.upper() != s and len(s.upper()) == 1:
            cmap[ord(s.upper())] = nombre(s)          # las mayúsculas se escriben con la caja baja
    fb.setupCharacterMap(cmap)
    pen = TTGlyphPen(None)
    margen = 40                                         # la celda, un poco adentro de su avance
    for x0, y0, x1, y1 in ((margen, DESCENDENTE, AVANCE - margen, ASCENDENTE),
                           (2 * margen, DESCENDENTE + margen, AVANCE - 2 * margen, ASCENDENTE - margen)):
        pen.moveTo((x0, y0)), pen.lineTo((x0, y1)), pen.lineTo((x1, y1)), pen.lineTo((x1, y0)), pen.closePath()
    caja = pen.glyph()
    fb.setupGlyf({g: caja for g in glifos})
    fb.setupHorizontalMetrics({g: (AVANCE, margen) for g in glifos})
    fb.setupHorizontalHeader(ascent=ASCENDENTE, descent=DESCENDENTE)
    fb.setupNameTable({"familyName": "Poliza Prueba", "styleName": "Regular"})
    fb.setupOS2(sTypoAscender=ASCENDENTE, sTypoDescender=DESCENDENTE, sTypoLineGap=0,
                usWinAscent=ASCENDENTE, usWinDescent=-DESCENDENTE)
    fb.setupPost()
    addOpenTypeFeaturesFromString(fb.font, texto_fea)
    fb.font.save(destino)
    return destino


def probar(p, texto_fea, vs):
    import uharfbuzz as hb
    with tempfile.TemporaryDirectory() as tmp:
        ruta = fuente_de_prueba(p, texto_fea, Path(tmp) / "prueba.ttf")
        datos = Path(ruta).read_bytes()
    print(f"fuente de prueba: {len(datos) // 1024} KB, casi todo la regla (las cajas son un solo contorno)")
    import io
    from fontTools.ttLib import TTFont
    fuente = hb.Font(hb.Face(datos))
    orden = TTFont(io.BytesIO(datos)).getGlyphOrder()
    fallas = 0
    for v in vs:
        buf = hb.Buffer()
        buf.add_str(v)
        buf.guess_segment_properties()
        hb.shape(fuente, buf, {"calt": True})
        nombres = [orden[i.codepoint] for i in buf.glyph_infos]
        sin_placa = [n for n in nombres if n != "space" and "." not in n[1:] and n != ".notdef"]
        repetidas = [n for n, c in Counter(n for n in nombres if n != "space").items() if c > 1]
        if sin_placa or repetidas:
            fallas += 1
            print(f"  falla: «{v}» sin placa {sin_placa} repetidas {repetidas}")
    print(f"{len(vs)} versos probados con HarfBuzz {hb.__version__}: "
          f"{'ninguna placa se repite dentro de un verso' if not fallas else f'{fallas} con fallas'}")
    return fallas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probar", action="store_true")
    a = ap.parse_args()
    vs = versos()
    p = poliza(juego(), vs)
    ventana = max(len(v) for v in vs)
    texto = fea(p, ventana)
    SALIDA.write_text(texto, encoding="utf8")
    del_poema = sum(n for s, n in p.items() if any(s in v.lower() for v in vs))
    print(f"poliza.fea: {sum(p.values())} placas en la caja ({del_poema} las pide el poema), ventana {ventana}")
    if a.probar:
        return 1 if probar(p, texto, vs) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
