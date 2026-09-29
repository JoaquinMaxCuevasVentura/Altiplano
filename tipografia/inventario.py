"""Inventario de Contenida: qué letras da el pie de la lámina y cuáles hay que reconstruir.

Uso (desde la raíz del repositorio):
    python3 tipografia/inventario.py

Lee tipografia/textos/pie_de_lamina.txt y tipografia/textos/poema.txt y escribe:
  - tipografia/textos/inventario.md: signos hallados y reconstruidos, la caja de
    8 × 7, la póliza de placas y los versos que se pueden escribir solo con
    letras halladas;
  - tipografia/esquemas/caja.json: la caja, para generar_esquemas.py.

La transcripción del pie sale de una foto de baja resolución. Cuando lo
transcribas desde el libro, corrige pie_de_lamina.txt y vuelve a correr este
script: todos los recuentos dependen de esa transcripción.
"""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
TEXTOS = BASE / "textos"
COLUMNAS, FILAS = 8, 7  # la retícula de la cabeza, tal como se ve en la lámina

LETRAS = list("abcdefghijklmnñopqrstuvwxyz")
ACENTUADAS = list("áéíóúü")
CIFRAS = list("0123456789")
SIGNOS = list(".,;:¿?()«»—…")
SIGNO_FINAL = "¶"  # el signo hecho con las manos; ocupa la última celda
JUEGO = LETRAS + ACENTUADAS + CIFRAS + SIGNOS
CELDA_VACIA = "¡ ! (la voz contenida no exclama) · guion, comillas inglesas, apóstrofo · cualquier otro signo"
SIN_CELDA = "Las mayúsculas no tienen celda: se escriben con la caja baja."


def palabras_con(signo, texto):
    for palabra in texto.split():
        if signo in palabra:
            return palabra.strip(".,;:()")
    return ""


def main():
    pie = (TEXTOS / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
    poema = (TEXTOS / "poema.txt").read_text(encoding="utf8")
    assert len(JUEGO) + 1 == COLUMNAS * FILAS, "el juego tiene que llenar la caja"

    # Solo cuenta la caja baja: una mayúscula del pie es otra forma, no un testigo.
    testigos = Counter(c for c in pie if c in JUEGO)
    halladas = []
    for c in pie:
        if c in JUEGO and c not in halladas:
            halladas.append(c)
    reconstruir = [c for c in JUEGO if c not in halladas]
    poema_bajo = poema.lower()
    por_necesidad = []
    for c in poema_bajo:
        if c in reconstruir and c not in por_necesidad:
            por_necesidad.append(c)
    reconstruidas = por_necesidad + [c for c in reconstruir if c not in por_necesidad]

    celdas = []
    for c in halladas:
        celdas.append({"signo": c, "estado": "hallada", "testigos": testigos[c],
                       "procedencia": palabras_con(c, pie)})
    for c in reconstruidas:
        celdas.append({"signo": c, "estado": "reconstruida",
                       "pedida_por": palabras_con(c, poema_bajo) if c in por_necesidad else ""})
    celdas.append({"signo": SIGNO_FINAL, "estado": "manos"})
    for n, celda in enumerate(celdas, 1):
        celda["celda"] = n
        celda["fila"], celda["columna"] = (n - 1) // COLUMNAS + 1, (n - 1) % COLUMNAS + 1

    versos = [v for v in poema_bajo.split("\n") if v.strip()]
    poliza = Counter()
    for verso in versos:
        for c, n in Counter(ch for ch in verso if not ch.isspace()).items():
            poliza[c] = max(poliza[c], n)
    solo_halladas = [v for v in versos if all(ch in halladas or ch.isspace() for ch in v)]
    palabras = sorted({p.strip(".,;:?") for p in poema_bajo.split()
                       if any(ch in reconstruir for ch in p.strip(".,;:?"))})

    (BASE / "esquemas").mkdir(exist_ok=True)
    (BASE / "esquemas" / "caja.json").write_text(json.dumps(
        {"columnas": COLUMNAS, "filas": FILAS, "celdas": celdas, "celda_vacia": CELDA_VACIA, "sin_celda": SIN_CELDA},
        ensure_ascii=False, indent=1), encoding="utf8")

    L = ["# Inventario de Contenida",
         "",
         "Generado por `tipografia/inventario.py` a partir de `textos/pie_de_lamina.txt` y `textos/poema.txt`. "
         "No lo edites a mano: corrige los textos y vuelve a correr el script.",
         "",
         f"- **Juego:** {len(JUEGO)} signos más el signo final = {len(celdas)} celdas "
         f"({COLUMNAS} columnas × {FILAS} filas).",
         f"- **Hallados en el pie (caja baja):** {len(halladas)}.",
         f"- **A reconstruir:** {len(reconstruidas)}.",
         f"- **Testigo único** (una sola aparición en el pie): "
         + ", ".join(f"«{c}» ({palabras_con(c, pie)})" for c in halladas if testigos[c] == 1) + ".",
         f"- **Se ven como celda vacía:** {CELDA_VACIA}.",
         f"- **Sin celda propia:** {SIN_CELDA}",
         "",
         "## Hallados, por orden de aparición en el pie",
         "",
         "| Celda | Signo | Testigos | Primera palabra |",
         "|---|---|---|---|"]
    L += [f"| {c['celda']} | `{c['signo']}` | {c['testigos']} | {c['procedencia']} |"
          for c in celdas if c["estado"] == "hallada"]
    L += ["", "## Reconstruidos: primero los que pide el poema, en el orden en que los pide", "",
          "| Celda | Signo | Lo pide |", "|---|---|---|"]
    L += [f"| {c['celda']} | `{c['signo']}` | {c['pedida_por'] or '—'} |"
          for c in celdas if c["estado"] == "reconstruida"]
    L += ["", f"La celda {len(celdas)} es el signo final `{SIGNO_FINAL}`, hecho con las manos.", "",
          "## La caja", ""]
    L.append("| " + " | ".join(str(i) for i in range(1, COLUMNAS + 1)) + " |")
    L.append("|" + "---|" * COLUMNAS)
    for f in range(FILAS):
        fila = celdas[f * COLUMNAS:(f + 1) * COLUMNAS]
        L.append("| " + " | ".join(
            (f"`{c['signo']}`" if c["estado"] == "hallada" else f"*`{c['signo']}`*")
            for c in fila) + " |")
    L += ["", "En cursiva, los reconstruidos.", "",
          "## Póliza: cuántas placas de cada signo para componer el poema verso a verso", "",
          f"Total: **{sum(poliza.values())} placas**. Con esta póliza ningún signo se repite "
          "dentro de un verso: cada aparición es una placa distinta.", "",
          "| Signo | Placas | | Signo | Placas | | Signo | Placas |", "|---|---|---|---|---|---|---|---|"]
    orden = [c for c in JUEGO if poliza[c]]
    tercio = -(-len(orden) // 3)
    for i in range(tercio):
        trio = [f"`{orden[j]}` | {poliza[orden[j]]}" if j < len(orden) else " | "
                for j in (i, i + tercio, i + 2 * tercio)]
        L.append("| " + " | | ".join(trio) + " |")
    sin_uso = [c for c in JUEGO if not poliza[c]]
    L += ["", f"El poema no usa {len(sin_uso)} signos del juego ("
          + " ".join(f"`{c}`" for c in sin_uso) + "); cada uno lleva igual una placa, y el signo final "
          f"otra. **La caja completa: {sum(poliza.values()) + len(sin_uso) + 1} placas.**"]
    L += ["", f"## Versos que se escriben solo con letras halladas: {len(solo_halladas)} de {len(versos)}", "",
          "Los demás necesitan al menos una letra reconstruida. Las palabras que lo exigen son: "
          + ", ".join(f"«{p}»" for p in palabras) + ".", ""]
    (TEXTOS / "inventario.md").write_text("\n".join(L), encoding="utf8")

    print(f"hallados {len(halladas)} · reconstruidos {len(reconstruidas)} · placas del poema {sum(poliza.values())} · "
          f"versos solo con halladas {len(solo_halladas)}/{len(versos)}")
    print("palabras que exigen reconstrucción:", ", ".join(palabras))


if __name__ == "__main__":
    main()
