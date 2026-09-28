"""Arma las páginas de Vasijas a partir de plantillas/.

Incrusta en cada página las fuentes (Contenedor Seca, Placa y Ruina), los
modos de la placa, el canto y el poema, para que cada archivo se abra solo,
sin servidor.

Escribe index.html, agua.html, placa.html, espalda.html, cadena.html y
ruina.html en esta carpeta.
Con --artefacto RUTA escribe además una copia para publicar, en la que
index.html va sin la envoltura <html>, porque el publicador la agrega.

Uso:  python3 armar.py [--artefacto RUTA]
"""

import base64
import html
import io
import json
import os
import sys

from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PIEZAS = ["agua", "placa", "cadena", "espalda", "ruina"]

# En la página del poema, el verde fósforo va solo en el título y en los
# versos que nombran el agua y la voz desenterrada (marco, sección VI).
VERSOS_VERDES = {
    "Tocas el agua y la diosa se deforma.": "agua",
    "Cada vuelta pasa por el agua": "agua",
    "y el agua no repite,": "agua",
    "Desenterrar una voz": "voz",
    "es desenterrar la mano del que la escribió.": "voz",
}


def woff2_de(ruta_ttf):
    f = TTFont(ruta_ttf)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def muestra_de(ruta_ttf, texto):
    """Una instancia reducida a los signos de un texto (con sus vueltas)."""
    from fontTools import subset
    fuente = TTFont(ruta_ttf)
    opciones = subset.Options()
    opciones.layout_features = ["*"]
    opciones.flavor = "woff2"
    reductor = subset.Subsetter(opciones)
    reductor.populate(text=texto)
    reductor.subset(fuente)
    fuente.flavor = "woff2"
    buf = io.BytesIO()
    fuente.save(buf)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def archivo_de(ruta):
    with open(ruta, "rb") as fh:
        return "data:font/woff2;base64," + base64.b64encode(fh.read()).decode("ascii")


def poema_hoja(estrofas):
    """El poema como HTML para la hoja: un verso por línea, con su color."""
    salida = []
    for estrofa in estrofas:
        versos = []
        for verso in estrofa.split("\n"):
            tema = VERSOS_VERDES.get(verso)
            clase = "verso verde agua" if tema == "agua" else "verso verde" if tema else "verso plata"
            versos.append('<span class="%s">%s</span>' % (clase, html.escape(verso)))
        salida.append('          <p class="estrofa">%s</p>' % "".join(versos))
    faltan = set(VERSOS_VERDES) - {v for e in estrofas for v in e.split("\n")}
    assert not faltan, "versos verdes que no están en el poema: %s" % faltan
    return "\n".join(salida)


def datos():
    with open(os.path.join(RAIZ, "poema.txt"), encoding="utf-8") as fh:
        estrofas = [e.strip("\n") for e in fh.read().strip().split("\n\n")]
    with open(os.path.join(AQUI, "placa", "modos.json"), encoding="utf-8") as fh:
        modos = fh.read()
    with open(os.path.join(AQUI, "placa", "canto.json"), encoding="utf-8") as fh:
        canto = fh.read()
    return {
        "{{SECA}}": woff2_de(os.path.join(RAIZ, "fuente", "estaticas", "Contenedor-Seca.ttf")),
        "{{PLACA}}": archivo_de(os.path.join(AQUI, "placa", "Placa.woff2")),
        "{{RUINA}}": archivo_de(os.path.join(RAIZ, "ruina", "Ruina-Variable.woff2")),
        "{{RUINA_MUESTRA}}": muestra_de(os.path.join(RAIZ, "ruina", "estaticas", "Ruina-VuelveEscrito.ttf"),
                                        "Contener una ruina"),
        "{{POEMA_HOJA}}": poema_hoja(estrofas),
        "{{MODOS}}": modos,
        "{{CANTO}}": canto,
        "{{POEMA}}": json.dumps(estrofas, ensure_ascii=False),
    }


def rellenar(nombre, reemplazos):
    with open(os.path.join(AQUI, "plantillas", nombre + ".html"), encoding="utf-8") as fh:
        texto = fh.read()
    for clave, valor in reemplazos.items():
        texto = texto.replace(clave, valor)
    return texto


def main(argv):
    reemplazos = datos()
    salidas = {nombre: rellenar(nombre, reemplazos) for nombre in PIEZAS + ["index"]}
    envoltura = ('<!doctype html>\n<html lang="es">\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
    for nombre, texto in salidas.items():
        if nombre == "index":
            texto = envoltura + texto + "\n</html>\n"
        with open(os.path.join(AQUI, nombre + ".html"), "w", encoding="utf-8") as fh:
            fh.write(texto)
        print("%-12s %6.0f KB" % (nombre + ".html", len(texto.encode()) / 1024))

    if "--artefacto" in argv:
        destino = argv[argv.index("--artefacto") + 1]
        os.makedirs(destino, exist_ok=True)
        for nombre, texto in salidas.items():
            with open(os.path.join(destino, nombre + ".html"), "w", encoding="utf-8") as fh:
                fh.write(texto)
        print("copia para publicar en", destino)


if __name__ == "__main__":
    main(sys.argv[1:])
