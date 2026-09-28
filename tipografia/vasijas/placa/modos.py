"""Los modos de la placa: qué figura dibuja cada letra cuando suena.

En 1787 Ernst Chladni esparció arena sobre una placa de metal y la hizo
vibrar con un arco. La arena se juntó en las líneas nodales, donde la placa
no se mueve: el sonido quedó dibujado. Aquí la placa es una de las placas de
aluminio del traje y la voz es el canto del video, que se oye pero no se
entiende.

Cada letra es un modo de vibración de una placa cuadrada, con la
aproximación clásica

    f(x, y) = cos(nπx)·cos(mπy) + s·cos(mπx)·cos(nπy),   x, y en [0, 1]

La arena queda donde |f| es pequeño. La frecuencia sale del mismo modo: crece
con n² + m², como en una placa real, comprimida con una raíz para que el
canto quede grave.

Las letras más frecuentes del castellano reciben los modos más simples, y
por eso suenan más graves: un texto corriente es un canto bajo.
"""

import json
import math
import os

# Letras del castellano de más a menos frecuentes.
FRECUENCIA = "eaosrnidlctumpbgvyqhfzjñxkw"
CIFRAS = "0123456789"
BASE_HZ = 82.0

# Una palabra del poema por cada inicial. Las letras que el poema nunca
# pronuncia al comienzo de una palabra quedan vacías.
ABECEDARIO = {
    "a": "agua", "b": "boca", "c": "contenedor", "d": "diosa", "e": "enterrar",
    "f": "flotar", "h": "hablado", "i": "ídolo", "l": "lengua", "m": "manos",
    "n": "nombre", "o": "opinión", "p": "piedra", "q": "quedó", "r": "ruinas",
    "s": "signo", "t": "temblor", "u": "una", "v": "voz", "y": "y",
}


def _candidatos():
    pares = [(n, m) for n in range(1, 10) for m in range(n + 1, 11)]
    pares.sort(key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0]))
    for n, m in pares:
        for s in (-1, 1):
            yield n, m, s


def modos():
    """{carácter: {"n", "m", "s", "hz"}} para letras y cifras."""
    tabla = {}
    candidatos = _candidatos()
    for ch in FRECUENCIA + CIFRAS:
        n, m, s = next(candidatos)
        hz = BASE_HZ * math.sqrt((n * n + m * m) / 5.0)
        if s > 0:
            # En una placa real, los dos modos de un mismo par (n, m) no
            # suenan igual: se separan un poco. Aquí, un tono entero.
            hz *= 2 ** (2 / 12)
        tabla[ch] = {"n": n, "m": m, "s": s, "hz": round(hz, 2)}
    return tabla


def f(x, y, n, m, s):
    """Amplitud de la placa en (x, y); acepta arreglos de numpy."""
    import numpy as np
    pi = math.pi
    return np.cos(n * pi * x) * np.cos(m * pi * y) + s * np.cos(m * pi * x) * np.cos(n * pi * y)


def exportar_json(ruta):
    datos = {"modos": modos(), "abecedario": ABECEDARIO}
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    for ch, mo in modos().items():
        print(ch, mo, ABECEDARIO.get(ch, "—"))
    exportar_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "modos.json"))
