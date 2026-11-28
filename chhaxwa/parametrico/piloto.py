"""Piezas comunes del piloto paramétrico de E1, E2, E3, E4 y E6: la tabla, el campo y la lámina-matriz.

Cada exploración tiene su guion (montana_e1.py, corral_e2.py, cupula_e3.py, chullpa_e4.py y pirwa_e6.py), con sus
parámetros, sus reglas y su corte. Este módulo escribe la tabla de variantes, dibuja el campo (un mapa de dos
parámetros, con las variantes que cumplen en gris y las que no en blanco, con la letra de la regla que fallan) y arma
la lámina en DXF con una matriz de cortes. todas.py corre los cinco.
"""

import csv
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "detalles"))

TINTA, GRIS = "#151413", "#8d8a85"
FRACCIONES = [("0,30 del largo", 0.30), ("un tercio", 1 / 3), ("0,375 del largo", 0.375)]   # los escenarios de la prueba 3


def semilla():
    """El mismo orden de las tablas del DXF en cada corrida."""
    if os.environ.get("PYTHONHASHSEED") != "0":
        os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0"})


def coma(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def cm(x):
    return coma(x * 100, 1).replace(",0", "")


def estado(v):
    """Con qué escenario de la prueba 3 cumple una variante, o qué regla falla."""
    e = v["escenarios"]
    if all(e):
        return "cumple"
    if e[1]:
        return "cumple con un tercio"
    if e[2]:
        return "cumple con 0,375"
    return "no cumple: " + (", ".join(v["falla"]) if v["falla"] else "V")


def escribir_csv(nombre, campos, filas):
    """campos: [(encabezado, función o clave, decimales)]."""
    with open(AQUI / f"{nombre}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow([c for c, _, _ in campos])
        for v in filas:
            fila = []
            for _, k, d in campos:
                x = k(v) if callable(k) else v[k]
                if isinstance(x, bool):
                    x = "sí" if x else "no"
                elif isinstance(x, float) and d is not None:
                    x = f"{x:.{d}f}"
                fila.append(x)
            w.writerow(fila)


def campo(nombre, paneles, xs, ys, xk, yk, valor, etiqueta_valor, xlabel, ylabel, marcas, fmt_x=None, fmt_y=None):
    """paneles: [(título, variantes)]. Cada variante es un dict con xk, yk, 'falla' (letras) y el valor que da el gris.
    marcas: [(texto, variante)]. Dibuja un mapa por panel, del mismo tamaño, con una escala de grises abajo."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    from matplotlib.patches import Rectangle
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 5.6, "axes.linewidth": 0.4,
                         "xtick.major.width": 0.4, "ytick.major.width": 0.4, "xtick.major.size": 2,
                         "ytick.major.size": 2})
    grises = LinearSegmentedColormap.from_list("grises", ["#dedbd5", "#3d3b38"])
    buenas = [valor(v) for _, vs in paneles for v in vs if not v["falla"]]
    norma = Normalize(min(buenas), max(buenas)) if buenas else Normalize(0, 1)
    dx = (xs[1] - xs[0]) if len(xs) > 1 else 1
    dy = (ys[1] - ys[0]) if len(ys) > 1 else 1
    hay_v = any(not v["falla"] and not v["escenarios"][1] for _, vs in paneles for v in vs)
    alto = 55 if hay_v else 50
    fig, ejes = plt.subplots(1, len(paneles), figsize=(95 / 25.4, alto / 25.4), squeeze=False, sharey=True)
    fig.subplots_adjust(left=0.13, right=0.98, top=1 - 6 / alto, bottom=(18 + (4 if hay_v else 0)) / alto, wspace=0.12)
    ids = {id(v): t for t, v in marcas}
    for ax, (titulo, vs) in zip(ejes[0], paneles):
        for v in vs:
            x, y = v[xk], v[yk]
            color = "#ffffff" if v["falla"] else grises(norma(valor(v)))
            ax.add_patch(Rectangle((x - dx / 2, y - dy / 2), dx, dy, facecolor=color, edgecolor="#d9d6d0", linewidth=0.25))
            if v["falla"]:
                ax.text(x, y, v["falla"], ha="center", va="center", fontsize=3.4, color=GRIS)
            elif not v["escenarios"][1]:                     # cumple la forma, pero la pieza tendría que volar más
                ax.text(x, y, "V", ha="center", va="center", fontsize=3.6,
                        color="#ffffff" if norma(valor(v)) > 0.45 else TINTA)
            if id(v) in ids:
                ax.add_patch(Rectangle((x - dx / 2, y - dy / 2), dx, dy, facecolor="none", edgecolor=TINTA, linewidth=1.0))
        aqui = sorted([(t, v) for t, v in marcas if any(v is w for w in vs)], key=lambda m: m[1][xk])
        for k, (t, v) in enumerate(aqui):                  # el rótulo, arriba de la grilla, con una línea a su celda
            pos = (v[xk] - xs[0]) / (xs[-1] - xs[0]) if len(xs) > 1 else 0.5
            lado = 1 if pos < 0.3 else (-1 if pos > 0.7 else 0)
            xt = v[xk] - lado * dx * 0.4
            ax.annotate(t, (v[xk], v[yk] + dy / 2), xytext=(xt, ys[-1] + dy * 1.25), textcoords="data",
                        ha={-1: "right", 0: "center", 1: "left"}[lado], va="center", fontsize=5.2, color=TINTA,
                        arrowprops=dict(arrowstyle="-", linewidth=0.4, color=TINTA, shrinkA=1, shrinkB=0))
        ax.set_xlim(xs[0] - dx / 2, xs[-1] + dx / 2)
        ax.set_ylim(ys[0] - dy / 2, ys[-1] + dy / 2 + dy * 1.3)
        paso_x = 1 if len(xs) * len(paneles) <= 8 else 2
        ax.set_xticks(xs[::paso_x])
        ax.set_yticks(ys[::1 if len(ys) <= 8 else 2])
        if fmt_x:
            ax.set_xticklabels([fmt_x(x) for x in xs[::paso_x]])
        if fmt_y:
            ax.set_yticklabels([fmt_y(y) for y in ys[::1 if len(ys) <= 8 else 2]])
        ax.set_xlabel(xlabel)
        if len(paneles) > 1:
            ax.set_title(titulo, fontsize=5.8, pad=2)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    ejes[0][0].set_ylabel(ylabel)
    barra = fig.add_axes([0.13, 4.2 / alto, 0.45, 2 / alto])
    import numpy as np
    barra.imshow(np.linspace(0, 1, 256)[None, :], aspect="auto", cmap=grises, extent=(norma.vmin, norma.vmax, 0, 1))
    barra.set_yticks([])
    barra.tick_params(labelsize=5.0, width=0.4, length=2)
    for s in barra.spines.values():
        s.set_linewidth(0.4)
    barra.set_title(etiqueta_valor + "; en blanco, las que no cumplen" +
                    ("\ncon V, las que cumplen solo si la pieza vuela más de un tercio de su largo" if hay_v else ""),
                    fontsize=5.2, loc="left", pad=2)
    ruta = AQUI / f"{nombre}.png"
    fig.savefig(ruta, dpi=300, facecolor="white", metadata={"Software": None})
    plt.close(fig)
    from PIL import Image
    Image.open(ruta).convert("L").save(ruta, optimize=True)


def lamina_matriz(nombre, numero, escala, titulo, subtitulo, notas, filas, cols, celda, seccion, textos, rotulos_filas,
                  rotulos_cols, encabezado, es_actual, alto_dibujo, materiales=None, rotulo_actual="la actual"):
    """Una matriz de cortes: filas × columnas de variantes, cada una con tres líneas de texto debajo.
    celda: (ancho, alto) en mm de papel; alto_dibujo: mm que ocupa el corte sobre su suelo."""
    from dibujar_detalles import Lamina, TA
    L = Lamina(escala, (0, 0), materiales={"P_LLENO": ("SOLID", 1, 172), "T_LLENO": ("SOLID", 1, 226),
                                           "A_LLENO": ("SOLID", 1, 92), "L_LLENO": ("SOLID", 1, 60),
                                           "C_LLENO": ("SOLID", 1, 120), "PAJA_LLENO": ("SOLID", 1, 200),
                                           **(materiales or {})})
    x0 = 30
    L.titulo(x0, 279, encabezado)
    for j, rc in enumerate(rotulos_cols):
        L.texto(x0 + celda[0] * (j + 0.5), 271, rc, 2.5, TA.MIDDLE_CENTER)
    for i, fila in enumerate(filas):
        yg = 262 - alto_dibujo - i * celda[1]
        lineas = rotulos_filas[i].split("\n")
        for k, ln in enumerate(lineas):
            L.texto(14, yg + 10 - k * 4.5, ln, 2.3)
        for j, v in enumerate(fila):
            cx = x0 + celda[0] * (j + 0.5)
            seccion(L, v, L.h(cx, yg))
            for k, ln in enumerate(textos(v)):
                L.texto(cx, yg - 4.5 - k * 3.5, ln, 2.1, TA.MIDDLE_CENTER)
            if es_actual(v):
                L.linea([L.h(cx - celda[0] / 2 + 1, yg - 15.5), L.h(cx + celda[0] / 2 - 1, yg - 15.5),
                         L.h(cx + celda[0] / 2 - 1, yg + alto_dibujo + 4), L.h(cx - celda[0] / 2 + 1, yg + alto_dibujo + 4)],
                        "MARCO", cerrada=True)
                L.texto(cx - celda[0] / 2 + 2, yg + alto_dibujo + 1, rotulo_actual, 2.1)
    L.marco(numero, titulo, subtitulo, notas, serie="piloto")
    return L.guardar(nombre, AQUI)


def vista(nombre):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    from dibujar_detalles import dibujar
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    dibujar(nombre, fig.add_axes([0, 0, 1, 1]), carpeta=AQUI)
    fig.set_size_inches(420 / 25.4, 297 / 25.4)
    ruta = AQUI / f"{nombre}.png"
    fig.savefig(ruta, dpi=200, facecolor="white")
    plt.close(fig)
    Image.open(ruta).convert("L").quantize(32).save(ruta, optimize=True)


def lamina_y_vista(nombre, cambio):
    if cambio or not (AQUI / f"{nombre}.png").exists():
        vista(nombre)
    print(f"{nombre}: {'rehecha' if cambio else 'sin cambios'}")
