"""Arma el muestrario de Contenedor a partir de plantilla.html.

Escribe index.html, que carga la fuente desde ../fuente/. Con --autonomo
RUTA escribe además una copia con la fuente embebida, que se abre sola en
cualquier navegador. Con --png guarda capturas de cada sección (necesita
Node, Playwright y Chromium).

Uso:  python3 generar_muestrario.py [--autonomo RUTA] [--png]
"""

import base64
import html
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "fuente"))
import glifos  # noqa: E402
import vasos  # noqa: E402

FUENTE = os.path.join(RAIZ, "fuente", "Contenedor-Variable.woff2")
VERSION = "0.100"

GRUPOS = [
    ("cerrado", "Vasos cerrados", True,
     "La contraforma no toca el exterior de la retícula. Igual pierde, porque entre "
     "placa y placa queda piel."),
    ("abierta", "Piscinas abiertas", True,
     "Retienen agua con la boca al cielo. La u es la piscina. La C guarda un poco "
     "en el labio de abajo."),
    ("volcada", "Piscinas volcadas", False,
     "No retienen nada. Dadas vuelta, sí: la n es una piscina boca abajo. El número "
     "dice cuánto retendrían."),
]


def html_vasos():
    grupos = {clave: [] for clave, _, _, _ in GRUPOS}
    for tabla in (glifos.MINUSCULAS, glifos.MAYUSCULAS, glifos.CIFRAS):
        for ch in sorted(tabla):
            if ch == "ı":
                continue
            cerrado, abierta, volcada = vasos.clasificar(tabla[ch])
            for clave, n in (("cerrado", cerrado), ("abierta", abierta), ("volcada", volcada)):
                if n:
                    grupos[clave].append((ch, n))
    partes = []
    for clave, titulo, con_agua, texto in GRUPOS:
        estilo = ' style="font-feature-settings:\'ss03\' 1"' if con_agua else ""
        letras = "\n".join(
            '          <span class="letra"><span class="c"%s>%s</span>'
            '<span class="rotulo">%d</span></span>' % (estilo, html.escape(ch), n)
            for ch, n in grupos[clave])
        partes.append(
            '      <div class="grupo">\n'
            '        <h3>%s</h3>\n'
            '        <p>%s</p>\n'
            '        <div class="letras">\n%s\n        </div>\n'
            '      </div>' % (titulo, texto, letras))
    return "\n".join(partes)


def html_poema():
    with open(os.path.join(RAIZ, "poema.txt"), encoding="utf-8") as f:
        estrofas = [e.strip("\n") for e in f.read().strip().split("\n\n")]
    partes = ["        <p>%s</p>" % html.escape(e) for e in estrofas]
    # Al final del ciclo, de la boca sale un signo: el escalonado.
    partes.append('        <p class="signo" aria-hidden="true">¶</p>')
    return "\n".join(partes)


def html_repertorio():
    caracteres = [ch for ch in glifos.todos() if ch not in (" ", " ")]
    caracteres += list(glifos.COMPUESTOS) + list(glifos.ORNAMENTOS)
    return "\n".join('      <span title="U+%04X">%s</span>' % (ord(ch), html.escape(ch))
                     for ch in caracteres)


def armar(fuente_url):
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as f:
        pagina = f.read()
    for clave, valor in (("{{FUENTE_URL}}", fuente_url), ("{{VERSION}}", VERSION),
                         ("{{VASOS}}", html_vasos()), ("{{POEMA}}", html_poema()),
                         ("{{REPERTORIO}}", html_repertorio())):
        pagina = pagina.replace(clave, valor)
    return pagina


def main(argv):
    contenido = armar("../fuente/Contenedor-Variable.woff2")
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html>\n<html lang="es">\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, '
                'viewport-fit=cover">\n' + contenido)
    print("index.html")

    if "--autonomo" in argv:
        ruta = argv[argv.index("--autonomo") + 1]
        with open(FUENTE, "rb") as f:
            datos = "data:font/woff2;base64," + base64.b64encode(f.read()).decode("ascii")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(armar(datos))
        print(ruta, "%.0f KB" % (os.path.getsize(ruta) / 1024))

    if "--png" in argv:
        entorno = dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules"))
        subprocess.run(["node", os.path.join(AQUI, "capturar.js"), os.path.join(AQUI, "index.html"), AQUI],
                       check=True, env=entorno)


if __name__ == "__main__":
    main(sys.argv[1:])
