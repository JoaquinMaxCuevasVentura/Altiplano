"""Qué letras son contenedores.

Se echa agua sobre cada letra de la retícula y se mira dónde queda. El agua
baja o se corre hacia los lados, nunca sube; si desde un azulejo vacío no
puede salir de la caja de la letra ni caer por debajo de ella, ese azulejo
retiene agua. Así se distinguen tres casos:

    vaso cerrado     la contraforma no toca el exterior (o, a, b, 8, B)
    piscina abierta  retiene agua con la boca al cielo (u, v, y, w, H)
    piscina volcada  retendría agua si la letra se diera vuelta (n, h, m)

Ninguna de esas contraformas se cierra de verdad, porque entre placa y placa
queda piel: ningún contenedor aguanta lo que contiene.

Uso:  python3 vasos.py   (imprime la tabla de capacidades en Markdown)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glifos  # noqa: E402

FILAS = range(6, -3, -1)


def _llena(filas):
    return {(c, f) for f, t in filas.items() for c, ch in enumerate(t) if ch == "#"}


def celdas_con_agua(filas):
    """Azulejos vacíos que retienen agua, como pares (columna, fila)."""
    placas = _llena(filas)
    if not placas:
        return set()
    abajo = min(f for c, f in placas)
    arriba = max(f for c, f in placas)
    ancho = max(len(t) for t in filas.values())
    agua = set()
    for f in range(arriba, abajo - 1, -1):
        for c in range(ancho):
            if (c, f) in placas:
                continue
            vistos, pila, escapa = set(), [(c, f)], False
            while pila and not escapa:
                x, y = pila.pop()
                if (x, y) in vistos:
                    continue
                vistos.add((x, y))
                for dx, dy in ((0, -1), (-1, 0), (1, 0)):
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= ancho or ny < abajo:
                        escapa = True
                        break
                    if (nx, ny) not in placas:
                        pila.append((nx, ny))
            if not escapa:
                agua.add((c, f))
    return agua


def cerradas(filas):
    """Azulejos vacíos que no se comunican con el exterior (vaso cerrado)."""
    placas = _llena(filas)
    if not placas:
        return set()
    ancho = max(len(t) for t in filas.values())
    caja = {(c, f) for c in range(-1, ancho + 1) for f in range(-3, 8)}
    exterior, pila = set(), [(-1, -3)]
    while pila:
        p = pila.pop()
        if p in exterior or p in placas or p not in caja:
            continue
        exterior.add(p)
        x, y = p
        pila.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return {p for p in caja if p not in placas and p not in exterior}


def volcar(filas):
    """La misma letra dada vuelta de arriba abajo."""
    return {4 - f: t for f, t in filas.items()}


def clasificar(filas):
    agua = celdas_con_agua(filas)
    cerr = cerradas(filas)
    abierta = agua - cerr
    volcada = celdas_con_agua(volcar(filas))
    volcada_propia = len(volcada) - len(cerradas(volcar(filas)))
    return len(cerr), len(abierta), volcada_propia


def tabla():
    lineas = ["| Letra | Vaso cerrado | Piscina abierta | Piscina volcada |",
              "|---|---|---|---|"]
    for grupo in (glifos.MINUSCULAS, glifos.MAYUSCULAS, glifos.CIFRAS):
        for ch in sorted(grupo):
            if ch == "ı":
                continue
            c, a, v = clasificar(grupo[ch])
            if c or a or v:
                lineas.append("| %s | %s | %s | %s |" % (
                    ch, c or "·", a or "·", v or "·"))
    return "\n".join(lineas)


if __name__ == "__main__":
    print(tabla())
