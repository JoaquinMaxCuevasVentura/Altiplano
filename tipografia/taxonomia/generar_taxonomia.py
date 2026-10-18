"""Las láminas de la taxonomía: las referencias de Contenida, ordenadas por su mecanismo.

Uso (desde la raíz del repositorio):
    pip install fonttools brotli pymupdf
    python3 tipografia/taxonomia/generar_taxonomia.py [--solo R-03]

Escribe en tipografia/taxonomia/:
  svg/R-00_… R-08_….svg      nueve láminas A3 apaisadas,
  png/R-00_… R-08_….png      vistas previas,
  contenida_taxonomia.pdf    las nueve, una por página, en A3, con los enlaces a los archivos.

Usa la hoja de los planos (planos/dibujo.py): el marco, el cajetín, las líneas,
los rombos y la columna del porqué. Del reel de Jason Murray se toma la manera
de ordenar, no la de mostrar: aquí cada operación lleva la marca de capítulo de
las láminas, cada técnica va en su celda, cada mecanismo se dibuja en corte,
planta o serie, y ninguna imagen de las referencias se reproduce. Los datos
están en taxonomia.py; el porqué de cada lámina, en por_que.py.
Necesita Chromium (o Chrome) para el PDF.
"""

import argparse
import base64
import datetime
import html
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
sys.path.insert(0, str(TIPO / "planos"))
sys.path.insert(0, str(AQUI))

import taxonomia as T  # noqa: E402
from dibujo import (DIBUJO, FILETE, GRIS, GRIS2, LINEAS, MEDIR, MONO, PAPEL, PLATA, SERIF, TINTA,  # noqa: E402
                    VIOLETA, Hoja, estilo, f)
from por_que import TEXTOS  # noqa: E402

X0, Y0, X1, Y1 = DIBUJO

SERIE = "las referencias · una taxonomía tomada con cuidado"
PIE = (("DIBUJÓ", "la máquina, desde las fichas de 10, sin ver las imágenes"),
       ("MIRA", "la mano: cada imagen en su archivo (10, §10.11)"),
       ("NOTA", "se dibuja el mecanismo, no la imagen: nada pasa a la letra"))
PIE_ATLAS = (("DIBUJÓ", "la máquina, desde las fichas de 10; las imágenes, de su archivo"),
             ("MIRA", "la mano: cada imagen en su archivo (10, §10.11)"),
             ("NOTA", "de dominio público: se miran, no se calcan; nada pasa a la letra"))
FECHA = {"R-09": "18.10.2026"}          # el atlas se rehizo con sus imágenes

LAMINAS = [
    ("R-00", "Índice y convenciones", "cómo se leen estas láminas", "indice"),
    ("R-01", "El método, reformado", "lo que se toma del reel, lo que se deja y lo que se suma", "metodo"),
    ("R-02", "El cuadro de las referencias", "de la técnica a la acción del taller", "cuadro"),
    ("R-03", "Diferenciar", "primera operación · técnicas 1 a 4", "diferenciar"),
    ("R-04", "Agrupar", "segunda operación · técnicas 5 a 7", "agrupar"),
    ("R-05", "Secuenciar", "tercera operación · técnicas 8 a 11", "secuenciar"),
    ("R-06", "Inferir", "cuarta operación · técnicas 12 a 17", "inferir"),
    ("R-07", "Del encargo a la referencia", "el camino al revés: del verso al archivo", "encargos"),
    ("R-08", "Lo que queda afuera", "lo dejado, lo no encontrado y lo pendiente", "afuera"),
    ("R-09", "El atlas de las referencias", "las obras, de su dominio a la acción donde caen", "atlas"),
]
LAMINA_DE_OP = {"diferenciar": "R-03", "agrupar": "R-04", "secuenciar": "R-05", "inferir": "R-06"}

ESTADO = {"toma": "se toma", "cambia": "se toma, cambiada", "deja": "se deja", "no": "no se hace",
          "suma": "se suma"}

CORTO_DESTINO = {"placa": "P-02 · 5", "gramatica": "P-07", "vaso": "P-01 · 3", "gota": "P-06 · 2", "a2": "A2",
                 "a4": "A4", "caja": "A5", "a7": "A7", "a8": "A8", "a9": "A9", "a10": "A10", "a11": "A11",
                 "colofon": "A12, el colofón", "cadena": "la cadena", "reparto": "el reparto (06)",
                 "no": "lo que no se hace"}


# ---------------------------------------------------------------- texto

def atar(texto):
    """Junta con espacios duros lo que no se corta: «P-02 · 5», «Acción 11», «06, §6.4»."""
    texto = re.sub(r"(P-\d\d) · (\d)", "\\1\u00a0·\u00a0\\2", texto)
    texto = re.sub(r"(Acci[oó]n|Acciones|técnica|regla) (\d)", "\\1\u00a0\\2", texto)
    return texto.replace(", §", ",\u00a0§")


def cortar(texto, ancho, tam, familia=MONO, peso=400, cursiva=False):
    """Corta un texto en renglones que caben en `ancho` mm."""
    texto = atar(texto)
    lineas, actual = [], ""
    for p in texto.split(" "):
        prueba = f"{actual} {p}".strip()
        if actual and MEDIR.ancho(prueba, tam, familia, peso, cursiva) > ancho:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    if actual:
        lineas.append(actual)
    return lineas


def renglones(h, x, y, lineas, tam, familia=MONO, peso=400, cursiva=False, color=TINTA, inter=1.3, ancla="start",
              dibujar=True):
    """Escribe renglones desde la línea de base y; devuelve la base del renglón siguiente."""
    for i, ln in enumerate(lineas):
        if dibujar:
            h.texto(x, y + i * tam * inter, ln, tam, ancla, familia=familia, peso=peso, cursiva=cursiva, color=color)
    return y + len(lineas) * tam * inter


def titulo_seccion(h, x, y, texto, ancho):
    h.texto(x, y, texto.upper(), 2.6, peso=700, espaciado=0.35)
    h.linea((x, y + 1.4), (x + ancho, y + 1.4), "filete", "textos")


def enlace(h, url, dibujar):
    """Lo que dibuja `dibujar` (en la capa de textos) lleva al archivo: en el PDF, se puede hacer clic."""
    h.add("textos", f'<a href="{html.escape(url, quote=True)}" target="_blank">')
    dibujar()
    h.add("textos", "</a>")


def subrayado(h, x, y, ancho, color=TINTA):
    h.linea((x, y + 0.45), (x + ancho, y + 0.45), "fina", "textos", color=color, w=0.13)


# ---------------------------------------------------------------- las piezas de la serie

def celda_abierta(h, x0, y0, x1, y1, tipo="celda", hueco=None, capa="fondo", **extra):
    """Un rectángulo que no cierra: se abre abajo, al centro, como todo contorno de Contenida (03b, regla 2)."""
    w = x1 - x0
    g = hueco if hueco is not None else min(3.0, w * 3 / 24)
    cx = (x0 + x1) / 2
    d = f"M{f(cx - g / 2)},{f(y1)} H{f(x0)} V{f(y0)} H{f(x1)} V{f(y1)} H{f(cx + g / 2)}"
    h.add(capa, f'<path d="{d}" {estilo(tipo, **extra)}/>')


def marca_tecnica(h, cx, cy, n, alto=5.0, capa="textos", no=False, violeta=False):
    """La técnica n en su celda: la de la cabeza (24 × 29), con su desagüe."""
    w = alto * 24 / 29
    x0, y0 = cx - w / 2, cy - alto / 2
    h.add(capa, f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(alto)}" fill="{PAPEL}"/>')
    color = VIOLETA if violeta else TINTA
    extra = dict(w=max(0.2, alto * 0.05), color=color)
    if no:
        extra["dash"] = f"{f(alto * 0.2)} {f(alto * 0.08)} {f(alto * 0.04)} {f(alto * 0.08)}"
    elif violeta:
        extra["dash"], extra["cap"] = "0.08 0.55", "round"
        extra["w"] = max(0.28, alto * 0.06)
    celda_abierta(h, x0, y0, x0 + w, y0 + alto, "celda", hueco=w * 3 / 24, capa=capa, **extra)
    tam = alto * (0.5 if n < 10 else 0.42)
    h.texto(cx, cy + tam * 0.36, str(n), tam, "middle", peso=700, capa=capa, color=color)
    return w


def marca_operacion(h, x, y, activa, alto=4.6, capa="textos"):
    """Las cuatro operaciones, como la marca de capítulo de las láminas: cuatro celdas de la cabeza, cada una
    con su desagüe abajo; la de la operación en curso lleva el centro violeta. Devuelve el ancho."""
    s = alto / 29
    for i in range(4):
        x0 = x + i * 34 * s
        on = i + 1 == activa
        trazo = TINTA if on else GRIS2
        h.add(capa, f'<path d="M{f(x0 + 10.5 * s)},{f(y + 29 * s)} H{f(x0)} V{f(y)} H{f(x0 + 24 * s)} '
                    f'V{f(y + 29 * s)} H{f(x0 + 13.5 * s)}" fill="none" stroke="{trazo}" '
                    f'stroke-width="{f(2 * s)}"/>')
        h.add(capa, f'<rect x="{f(x0 + 5 * s)}" y="{f(y + 5 * s)}" width="{f(14 * s)}" height="{f(19 * s)}" '
                    f'fill="{VIOLETA if on else "none"}" stroke="{trazo}" stroke-width="{f(1.5 * s)}"/>')
    return 126 * s


def notdef(h, x0, y0, ancho, alto, tipo="celda", capa="fondo", **extra):
    """La celda vacía (.notdef): un rectángulo dentro de otro, sin nada adentro; los dos con desagüe."""
    celda_abierta(h, x0, y0, x0 + ancho, y0 + alto, tipo, capa=capa, **extra)
    mx, my = ancho * 0.21, alto * 0.17
    celda_abierta(h, x0 + mx, y0 + my, x0 + ancho - mx, y0 + alto - my, tipo, capa=capa, **extra)


def hilo(h, p, q, toma=True, tipo="cota", color=TINTA, capa="cotas", w=None):
    """Un hilo del mapa 2: si termina en punto, se toma; si termina en corte, no."""
    extra = {"color": color}
    if w:
        extra["w"] = w
    h.linea(p, q, tipo, capa, **extra)
    if toma:
        h.punto(q, 0.55, color, capa)
    else:
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        h.linea((q[0] - nx * 1.3, q[1] - ny * 1.3), (q[0] + nx * 1.3, q[1] + ny * 1.3), "cota", capa, color=color,
                w=0.35)


def delta(h, cx, cy, lado=2.5, capa="textos", color=TINTA):
    """El triángulo de revisión de un plano: lo que se toma, cambiado."""
    a = lado * math.sqrt(3) / 2
    h.add(capa, f'<path d="M{f(cx)},{f(cy - a * 2 / 3)} L{f(cx + lado / 2)},{f(cy + a / 3)} '
                f'L{f(cx - lado / 2)},{f(cy + a / 3)} Z" fill="{PAPEL}" stroke="{color}" stroke-width="0.25"/>')


def punteado(h, x0, y0, x1, y1, capa="textos", w=0.3):
    """Un rectángulo a puntos y en violeta: lo que no se vio, o lo que se suma."""
    h.add(capa, f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" '
                f'{estilo("contorno_r", w=w)}/>')


def simbolo(h, x, y, estado, largo=5.0, capa="textos"):
    """El signo de cada estado, de `largo` mm y centrado en y."""
    if estado == "toma":
        hilo(h, (x, y), (x + largo - 0.6, y), True, capa=capa)
    elif estado == "cambia":
        hilo(h, (x, y), (x + largo - 3.0, y), True, capa=capa)
        delta(h, x + largo - 1.25, y + 0.2, 2.3, capa)
    elif estado == "deja":
        hilo(h, (x, y), (x + largo - 0.4, y), False, "comparar", GRIS, capa)
    elif estado == "no":
        hilo(h, (x, y), (x + largo - 0.4, y), False, "rotura", TINTA, capa, w=0.3)
    elif estado == "suma":
        punteado(h, x, y - 1.2, x + largo, y + 1.2, capa)
    return largo


def casilla(h, x, y, visto=False, lado=2.6, capa="textos"):
    """La casilla de visto: a puntos y en violeta mientras nadie la miró; continua y marcada si ya."""
    if visto:
        h.add(capa, f'<rect x="{f(x)}" y="{f(y)}" width="{f(lado)}" height="{f(lado)}" {estilo("celda", w=0.25)}/>')
        h.poli([(x + lado * 0.2, y + lado * 0.55), (x + lado * 0.42, y + lado * 0.8), (x + lado * 0.85, y + lado * 0.2)],
               "contorno", capa, w=0.35)
    else:
        punteado(h, x, y, x + lado, y + lado, capa, w=0.28)


def nivel(h, x, y, texto, tam=2.3, largo=15):
    """El símbolo de nivel de los planos: un triángulo sobre la línea."""
    h.linea((x - 2, y), (x + largo, y), "cota", "textos")
    h.add("textos", f'<path d="M{f(x)},{f(y)} L{f(x - 1.5)},{f(y - 2.5)} L{f(x + 1.5)},{f(y - 2.5)} Z" '
                    f'fill="{PAPEL}" stroke="{TINTA}" stroke-width="0.2"/>')
    h.add("textos", f'<path d="M{f(x)},{f(y)} L{f(x)},{f(y - 2.5)} L{f(x + 1.5)},{f(y - 2.5)} Z" fill="{TINTA}"/>')
    if texto:
        h.texto(x + 2.6, y - 0.8, texto, tam)


def cabeza_operacion(h, op):
    """La banda de arriba de las láminas de operación: la marca, el nombre, la figura y qué hace."""
    O = T.OPERACIONES[op]
    x, y = X0 + 3, Y0 + 4
    w = marca_operacion(h, x, y, O["i"], 6.4)
    h.texto(x + w + 4, y + 5.6, O["nombre"], 7.0, familia=SERIF, peso=300)
    xa = x + w + 6 + MEDIR.ancho(O["nombre"], 7.0, SERIF, 300)
    h.texto(xa, y + 2.4, f"{O['i']} · {O['murray']} · retórica: {O['figura'].lower()}", 2.2, color=GRIS)
    h.texto(xa, y + 5.6, O["que"], 3.0, familia=SERIF, cursiva=True, peso=400)
    return y + 11


def titulo_tecnica(h, x, y, n, ancho):
    """El título de un detalle: la técnica en su celda, su nombre y la vista con que se dibuja."""
    t = T.TECNICA[n]
    marca_tecnica(h, x + 2.9, y + 3.0, n, 6.6, no=t["estado"] == "no")
    titulo = t["nombre"].upper()
    h.texto(x + 8, y + 2.6, titulo, 2.75, peso=700, espaciado=0.12)
    wt = MEDIR.ancho(titulo, 2.75, MONO, 700) + len(titulo) * 0.12
    h.linea((x + 8, y + 3.6), (x + 8 + min(wt, ancho - 8), y + 3.6), "filete", "textos")
    de = "se suma: el reel no la trae" if t["murray"] == "—" else f"del reel: {t['murray']}"
    h.texto(x + 8, y + 6.6, f"{t['vista']} · {de} · {ESTADO[t['estado']]}", 1.95, color=GRIS)
    return y + 10


# ---------------------------------------------------------------- la ficha de una referencia

def ficha(h, x, y, w, k, alto=None, rima=True, dibujar=True, marcas=None):
    """La ficha de una referencia: quién, cuándo, con qué medio y licencia (06, §6.4), qué se toma, qué no,
    dónde cae y la casilla de visto. A puntos y en violeta mientras nadie la miró. Devuelve el alto."""
    R = T.REFERENCIAS[k]
    marcas = marcas if marcas is not None else {}
    pad, lab = 2.1, 16.5
    tx, tw = x + pad + lab, w - 2 * pad - lab
    D = dibujar
    # las técnicas
    cy = y + pad + 2.9
    xm = x + pad
    for i, n in enumerate(R["tec"]):
        a = 5.4 if i == 0 else 4.0
        if D:
            wm = marca_tecnica(h, xm + a * 12 / 29, cy - (0 if i == 0 else 0.7), n, a, no=T.TECNICA[n]["estado"] == "no")
        else:
            wm = a * 24 / 29
        xm += wm + 1.2
    # quién, qué, cuándo, con qué medio
    xt = xm + 1.2
    wt = x + w - pad - xt
    yy = y + pad + 2.6
    marcas["tecnicas"] = (x + w, cy)
    marcas["quien"] = (x + w, yy - 1.0)
    yy = renglones(h, xt, yy, cortar(R["autor"], wt, 2.75, SERIF, 500), 2.75, SERIF, 500, dibujar=D, inter=1.18)
    yy = renglones(h, xt, yy + 0.2, cortar(R["obra"], wt, 2.3, SERIF, 400, True), 2.3, SERIF, 400, True,
                   dibujar=D, inter=1.22)
    yy = renglones(h, xt, yy + 0.2, cortar(f"{R['anio']} · {R['medio']}", wt, 1.75), 1.75, color=GRIS,
                   dibujar=D, inter=1.3)
    yy = max(yy, cy + 4.6)
    if D:
        h.linea((x + pad, yy - 0.6), (x + w - pad, yy - 0.6), "fina", "textos")
    yy += 2.6

    def fila(rotulo, estado, texto, tam=2.35, familia=SERIF, peso=300, color=TINTA, cursiva=False):
        nonlocal yy
        marcas[rotulo] = (x + w, yy - 0.7)
        if D:
            h.texto(x + pad, yy, rotulo, 1.75, color=GRIS)
            if estado:
                simbolo(h, x + pad + lab - 5.6, yy - 0.62, estado, 4.4)
        lineas = cortar(texto, tw, tam, familia, peso, cursiva)
        yy = renglones(h, tx, yy, lineas, tam, familia, peso, cursiva, color, inter=1.22, dibujar=D) + 0.75

    fila("se toma", "toma", R["toma"])
    if R["no_toma"]:
        fila("no se toma", "deja", R["no_toma"])
    fila("cae en", None, " · ".join(CORTO_DESTINO[d] for d in R["destinos"]), 1.9, MONO, 400)
    # dónde: el archivo, con su enlace
    nombre, url = R["archivo"]
    lineas = cortar(f"{nombre} · {R['licencia']}", tw, 1.85)
    marcas["dónde"] = (x + w, yy - 0.7)
    if D:
        h.texto(x + pad, yy, "dónde", 1.75, color=GRIS)
        primera = lineas[0]
        corte = primera.find(" · ")
        nom = primera[:corte] if corte >= 0 else primera
        resto = primera[len(nom):]
        enlace(h, url, lambda: h.texto(tx, yy, nom, 1.85))
        subrayado(h, tx, yy, MEDIR.ancho(nom, 1.85, MONO))
        h.texto(tx + MEDIR.ancho(nom, 1.85, MONO), yy, resto, 1.85, color=GRIS)
        for i, ln in enumerate(lineas[1:]):
            h.texto(tx, yy + (i + 1) * 1.85 * 1.3, ln, 1.85, color=GRIS)
    yy += len(lineas) * 1.85 * 1.3
    if R["otros"]:
        xo = tx
        if D:
            h.texto(xo, yy, "y:", 1.7, color=GRIS)
        xo += MEDIR.ancho("y: ", 1.7, MONO)
        for i, (nom, url) in enumerate(R["otros"]):
            s = nom + (", " if i < len(R["otros"]) - 1 else "")
            wn = MEDIR.ancho(nom, 1.7, MONO)
            if xo + wn > x + w - pad:
                xo, yy = tx + MEDIR.ancho("y: ", 1.7, MONO), yy + 1.7 * 1.3
            if D:
                enlace(h, url, lambda xo=xo, nom=nom: h.texto(xo, yy, nom, 1.7))
                subrayado(h, xo, yy, wn, GRIS)
                h.texto(xo + wn, yy, s[len(nom):], 1.7)
            xo += MEDIR.ancho(s + " ", 1.7, MONO)
        yy += 1.7 * 1.3
    yy += 0.75
    if rima and R["rima"]:
        lineas = cortar(R["rima"], tw, 2.2, SERIF, 400, True)
        yy = renglones(h, tx, yy, lineas, 2.2, SERIF, 400, True, GRIS, inter=1.22, dibujar=D) + 0.75
    # visto: la casilla, para la mano
    marcas["visto"] = (x + w, yy - 1.0)
    if D:
        h.texto(x + pad, yy, "visto", 1.75, color=GRIS)
        casilla(h, tx, yy - 2.3, R["mirada"])
        libre = (x + w - pad - tx - 4.2) / MEDIR.ancho("_", 1.75, MONO)
        n = max(4, int((libre - 16) * 0.6))
        h.texto(tx + 4.2, yy, f"por {'_' * n}  el __.__.____", 1.75, color=GRIS)
    yy += 2.2
    alto_real = yy - y
    marcas["marco"] = (x + w, y + alto_real - 0.6)
    if D:
        y1 = y + (alto if alto else alto_real)
        if R["mirada"]:
            celda_abierta(h, x, y, x + w, y1, "celda", capa="fondo", w=0.3)
        else:
            celda_abierta(h, x, y, x + w, y1, "contorno_r", capa="fondo", w=0.35)
    return alto_real


def alto_rejilla(claves, x0, x1, columnas, sep=3.4, rima=True):
    w = (x1 - x0 - sep * (columnas - 1)) / columnas
    filas = [claves[i:i + columnas] for i in range(0, len(claves), columnas)]
    return sum(max(ficha(None, 0, 0, w, k, rima=rima, dibujar=False) for k in fila) for fila in filas) + \
        sep * (len(filas) - 1)


def cruces(op):
    """La columna suma lo que conecta esta operación con las otras, y lo que se buscó y no apareció."""
    tecs = {t["n"] for t in T.TECNICAS if t["op"] == op}
    propias = set(T.de_la_operacion(op))
    otros = []
    for k in T.ORDEN:
        comunes = [n for n in T.REFERENCIAS[k]["tec"][1:] if n in tecs]
        if k not in propias and comunes:
            otra = LAMINA_DE_OP[T.TECNICA[T.REFERENCIAS[k]["tec"][0]]["op"]]
            otros.append(f"{T.REFERENCIAS[k]['corto']} ({', '.join(map(str, comunes))}; {otra})")
    faltan = [f"{q} ({n})" for q, col, n in T.NO_ENCONTRADO if T.TECNICA[n]["op"] == op]
    bloques = []
    if otros:
        bloques += [("titulo", "Cruces"),
                    ("p", "También usan estas técnicas, desde otra operación: " + "; ".join(otros) + ".")]
    if faltan:
        bloques += [("titulo", "Lo que falta"), ("p", "Se buscó y no apareció: " + "; ".join(faltan) + " (R-08).")]
    return bloques


def rejilla_fichas(h, claves, x0, y0, x1, columnas, sep=3.4, rima=True):
    """Las fichas en filas; cada fila, del alto de la más alta. Devuelve la y de abajo."""
    w = (x1 - x0 - sep * (columnas - 1)) / columnas
    y = y0
    for i in range(0, len(claves), columnas):
        fila = claves[i:i + columnas]
        alto = max(ficha(h, 0, 0, w, k, rima=rima, dibujar=False) for k in fila)
        for j, k in enumerate(fila):
            ficha(h, x0 + j * (w + sep), y, w, k, alto=alto, rima=rima)
        y += alto + sep
    return y - sep


# ---------------------------------------------------------------- R-00

def r00(h):
    x, y = X0 + 5, Y0 + 14
    h.texto(x, y, "Contenida", 13, familia=SERIF, peso=300)
    h.texto(x + 58, y, "las referencias, por su mecanismo", 5.0, familia=SERIF, cursiva=True, peso=300, color=GRIS)
    h.texto(x, y + 8, "Veinticinco obras de dominio público, ordenadas por lo que hacen y dibujadas con las reglas "
                      "de la letra.", 3.0, familia=SERIF, peso=300)
    # el índice
    y0 = y + 20
    titulo_seccion(h, x, y0, "Índice", 118)
    for i, (cod, tit, sub, _) in enumerate(LAMINAS):
        yy = y0 + 6.6 + i * 7.0
        h.texto(x, yy, cod, 2.8, peso=700)
        h.texto(x + 15, yy, tit, 3.3, familia=SERIF, peso=400)
        h.texto(x + 15, yy + 3.0, sub, 2.0, color=GRIS)
        for op, codigo in LAMINA_DE_OP.items():
            if codigo == cod:
                marca_operacion(h, x + 118 - 13.1, yy - 3.0, T.OPERACIONES[op]["i"], 3.0)
                h.texto(x + 118 - 15, yy, T.OPERACIONES[op]["figura"].lower(), 1.9, "end", color=GRIS)
        h.linea((x, yy + 4.2), (x + 118, yy + 4.2), "fina", "textos")
    # cómo se lee una ficha
    yo = y0 + 6.6 + len(LAMINAS) * 7.0 + 5
    titulo_seccion(h, x, yo, "Cómo se lee una ficha", 118)
    m = {}
    ficha(h, x, yo + 4.0, 72, "hauy", marcas=m)
    notas = [("tecnicas", "las técnicas: la principal, más grande"), ("quien", "quién, qué, cuándo, con qué medio"),
             ("se toma", "lo que se toma"), ("no se toma", "lo que no se toma"),
             ("cae en", "dónde cae: la acción o el plano"), ("dónde", "el archivo, con su enlace y licencia"),
             ("visto", "la casilla, para la mano"), ("marco", "a puntos: nadie la miró todavía")]
    xn = x + 78
    ys = [m[k][1] for k, _ in notas]
    for i, (k, txt) in enumerate(notas):
        yn = max(ys[i], (ys[i - 1] if i else 0) + 3.4)
        ys[i] = yn
        p = m[k]
        h.punto(p, 0.4, VIOLETA, "cotas")
        h.linea(p, (xn - 1.5, yn), "cota", "cotas", color=VIOLETA, w=0.13)
        h.texto(xn, yn + 0.7, txt, 1.95)
    # las convenciones
    cx = x + 132
    titulo_seccion(h, cx, y0, "Convenciones", 112)
    yy = y0 + 6.6
    for tipo, txt in (("contorno", "continuo: lo visto; lo que se toma"),
                      ("contorno_r", "a puntos, en violeta: lo no visto todavía; lo que se suma")):
        h.linea((cx, yy - 0.8), (cx + 20, yy - 0.8), tipo, "textos")
        h.texto(cx + 25, yy, txt, 2.3)
        yy += 5.6
    for estado, txt in (("toma", "termina en punto: se toma (como en el mapa 2)"),
                        ("cambia", "con el triángulo de revisión: se toma, cambiada"),
                        ("deja", "a trazos, termina en corte: se deja"),
                        ("no", "trazo y punto, en corte: no se hace (06, §6.4)")):
        simbolo(h, cx, yy - 0.8, estado, 20)
        h.texto(cx + 25, yy, txt, 2.3)
        yy += 5.6
    yy += 1.2
    marca_tecnica(h, cx + 10, yy - 1.0, 1, 5.4)
    h.texto(cx + 25, yy, "la técnica 1, en su celda: la de la cabeza", 2.3)
    yy += 7.4
    marca_operacion(h, cx + 2.5, yy - 3.3, 1, 3.8)
    h.texto(cx + 25, yy, "la operación 1 de 4: la marca de capítulo", 2.3)
    h.texto(cx + 25, yy + 3.0, "de las láminas", 2.3)
    yy += 9.4
    notdef(h, cx + 7.3, yy - 4.4, 5.4, 6.4, capa="textos", w=0.3)
    h.texto(cx + 25, yy, "la celda vacía (.notdef): lo que no cabe", 2.3)
    h.texto(cx + 25, yy + 3.0, "o no se encontró", 2.3)
    yy += 8.8
    casilla(h, cx + 8.7, yy - 2.6, False)
    h.texto(cx + 25, yy, "visto: lo marca la mano, con fecha", 2.3)
    yy += 7.0
    h.rombo((cx + 10, yy - 0.8), 3, capa="textos")
    h.texto(cx + 25, yy, "decisión 3 de la lámina: su porqué, en la columna", 2.3)
    yy += 7.0
    nivel(h, cx + 4, yy, "03", 2.1)
    h.texto(cx + 25, yy, "nivel del método, del 01 al 05", 2.3)
    yy += 8.4
    h.llamada(cx + 7, yy, 2, "R-01")
    h.texto(cx + 25, yy - 1.0, "llamada: vista 2 de la lámina R-01", 2.3)
    yy += 13.0
    h.gravedad(cx + 7, yy, 4.0)
    h.texto(cx + 25, yy - 1.0, "en lugar del norte, la gravedad: lo que se", 2.3)
    h.texto(cx + 25, yy + 2.4, "toma cae en Contenida (R-07)", 2.3)
    # las diecisiete técnicas
    yq = 184
    titulo_seccion(h, x, yq, "Las diecisiete técnicas", 244)
    mitad = 9
    for i, t in enumerate(T.TECNICAS):
        col, fila = divmod(i, mitad)
        xx = x + col * 126
        yy = yq + 6.4 + fila * 5.9
        marca_tecnica(h, xx + 1.9, yy - 0.95, t["n"], 4.4, no=t["estado"] == "no")
        h.texto(xx + 6, yy, t["nombre"], 2.6, familia=SERIF, peso=500)
        dom = T.DOMINIOS[t["dom"]]["nombre"].lower()
        h.texto(xx + 50, yy, f"{T.OPERACIONES[t['op']]['nombre'].lower()} · {dom}", 1.95)
        simbolo(h, xx + 89, yy - 0.7, t["estado"], 4.4)
        h.texto(xx + 95, yy, ESTADO[t["estado"]].replace(", cambiada", " cambiada"), 1.95, color=GRIS)
        refs = sum(1 for r in T.REFERENCIAS.values() if t["n"] in r["tec"])
        h.texto(xx + 118, yy, str(refs), 1.95, "end", color=VIOLETA)
        h.linea((xx, yy + 1.8), (xx + 118, yy + 1.8), "fina", "textos")
    h.texto(x + 126 + 118, yq + 6.4 + 8 * 5.9 + 0.2, "a la derecha: cuántas referencias", 1.8, "end", color=GRIS)
    # dónde caen
    yc = 247.5
    titulo_seccion(h, x, yc, "Dónde caen: las referencias en el taller (R-02)", 244)
    cadena(h, x, yc + 4, 244)
    h.columna(TEXTOS["R-00"])


def cuenta_columnas():
    cuenta = {c: 0 for c, *_ in T.COLUMNAS}
    for k in T.REFERENCIAS:
        for c in T.columnas_de(k):
            cuenta[c] += 1
    return cuenta


def cadena(h, x, y, ancho):
    """Las columnas del cuadro como una cadena: cada nodo, con cuántas referencias caen en él."""
    cuenta = cuenta_columnas()
    n = len(T.COLUMNAS)
    paso = ancho / n
    xs = [x + paso * (i + 0.5) for i in range(n)]
    yn = y + 11.5
    # los cuadernos, arriba
    for cuad, nombre in T.CUADERNOS.items():
        idx = [i for i, c in enumerate(T.COLUMNAS) if c[2] == cuad]
        a, b = xs[idx[0]] - paso * 0.42, xs[idx[-1]] + paso * 0.42
        h.linea((a, y + 4.6), (b, y + 4.6), "cota", "textos")
        for xx in (a, b):
            h.linea((xx, y + 4.6), (xx, y + 6.0), "cota", "textos")
        h.texto((a + b) / 2, y + 3.5, f"cuaderno {cuad} · {nombre}", 1.9, "middle", color=GRIS)
    for i, (c, nombre, cuad) in enumerate(T.COLUMNAS):
        xx = xs[i]
        if i and T.COLUMNAS[i - 1][2] is not None and cuad is not None:
            h.linea((xs[i - 1] + 2.6, yn), (xx - 2.8, yn), "cota", "textos")
            h.flecha((xx - 2.6, yn), (xx - 4.6, yn), largo=1.4, ancho=0.55, capa="textos")
        if cuenta[c]:
            h.circulo((xx, yn), 2.5, "filete", "textos", relleno=PAPEL)
            h.texto(xx, yn + 0.8, str(cuenta[c]), 2.2, "middle", peso=700)
        else:
            notdef(h, xx - 2.1, yn - 2.6, 4.2, 5.2, capa="textos", w=0.25)
        h.texto(xx, yn + 6.0, c, 1.95, "middle", peso=700)
        for j, ln in enumerate(cortar(nombre, paso - 1.0, 1.7)):
            h.texto(xx, yn + 8.6 + j * 2.2, ln, 1.7, "middle", color=GRIS)


# ---------------------------------------------------------------- R-01

def r01(h):
    x = X0 + 2
    h.llamada(x + 4.5, Y0 + 6.5, 1, "R-01", "EL MÉTODO, NIVEL POR NIVEL · CORTE", "lo que trae el reel y lo que "
                                                                                     "queda en Contenida")
    # la cabecera del corte
    y = Y0 + 17.5
    cols = (x, x + 40, x + 106)
    for xx, t in zip(cols, ("NIVEL", "EN EL REEL", "EN CONTENIDA")):
        h.texto(xx, y, t, 1.8, color=GRIS, espaciado=0.25)
    h.linea((x, y + 1.2), (X1 - 2, y + 1.2), "filete", "textos")
    filas = [dict(n="", nombre="El método", reel="«A Taxonomy of Visuals», Jason Murray", ideas=T.METODO)]
    filas += T.NIVELES
    y += 3.0
    for i, F in enumerate(filas):
        ytop = y
        yb = y + 4.0
        if F["n"]:
            nivel(h, x + 2, yb + 0.8, F["n"], 2.2, largo=10)
            h.texto(x + 15, yb, F["nombre"], 3.1, familia=SERIF, peso=400)
        else:
            h.texto(x, yb, F["nombre"], 3.1, familia=SERIF, peso=500)
        if F["n"] and F.get("murray") and F["murray"] != "—":
            h.texto(x + 15, yb + 3.0, F["murray"], 1.75, color=GRIS)
        lineas = cortar(F["reel"], cols[2] - cols[1] - 4, 1.95)
        yr = renglones(h, cols[1], yb, lineas, 1.95, color=GRIS, inter=1.3)
        # las ideas, con su signo, en renglones
        xx, yi = cols[2], yb
        for estado, idea in F["ideas"]:
            wi = 6.2 + MEDIR.ancho(idea, 2.6, SERIF, 400) + 4.0
            if xx + wi > X1 - 2 and xx > cols[2]:
                xx, yi = cols[2], yi + 4.0
            simbolo(h, xx, yi - 0.8, estado, 4.6)
            h.texto(xx + 6.2, yi, idea, 2.6, familia=SERIF, peso=400 if estado != "deja" else 300,
                    color=GRIS if estado in ("deja", "no") else TINTA)
            xx += wi
        y = max(yi + 2.2, yr + 0.2, yb + (4.6 if F["n"] else 2.4))
        h.linea((x, y), (X1 - 2, y), "fina", "textos")
        y += 1.4
    # la fuente, con sus enlaces
    yf = y + 2.6
    h.texto(x, yf, "FUENTE", 1.8, color=GRIS, espaciado=0.25)
    xx = x + 13
    t0 = f"{T.FUENTE['autor']}, {T.FUENTE['obra']}, {T.FUENTE['medio']} · "
    h.texto(xx, yf, t0, 1.95)
    xx += MEDIR.ancho(t0, 1.95, MONO)
    for i, (nom, url) in enumerate(T.ENLACES_FUENTE):
        wn = MEDIR.ancho(nom, 1.95, MONO)
        enlace(h, url, lambda xx=xx, nom=nom: h.texto(xx, yf, nom, 1.95))
        subrayado(h, xx, yf, wn)
        xx += wn
        if i == 0:
            h.texto(xx, yf, " · ", 1.95)
            xx += MEDIR.ancho(" · ", 1.95, MONO)
    # las técnicas por dominio: planta
    yv = yf + 9
    h.llamada(x + 4.5, yv, 2, "R-01", "LAS TÉCNICAS, POR DOMINIO · PLANTA",
              "41 del reel y 7 que se suman; lo que se deja cae por el desagüe")
    tecnicas_por_dominio(h, x, yv + 9, X1 - 2)
    c = T.contar()
    sirven = c["toma"] + c["cambia"]
    h.columna(TEXTOS["R-01"] + [
        ("titulo", "Lo que se aprende"),
        ("p", f"De las {c['murray']} técnicas del reel, {c['toma']} se toman, {c['cambia']} cambian, {c['deja']} se "
              f"dejan y {c['no']} no se hacen. Las {sirven} que sirven ya trabajaban en Contenida: cada una tiene su "
              f"plano, su acción o su regla. **El reel no trae formas: trae un orden para las referencias.**")])


def tecnicas_por_dominio(h, x0, y0, x1):
    """Los siete dominios como cajas abiertas abajo: adentro, lo que se queda; debajo del fondo, lo que se va."""
    columnas = []
    for en, es, estado, dom in T.DOMINIOS_MURRAY:
        tecs = T.TECNICAS_MURRAY[es]
        sumadas = T.SUMADAS.get(es, [])
        columnas.append(dict(en=en, nombre=T.DOMINIOS[dom]["nombre"], estado=estado, tecs=tecs, sumadas=sumadas))
    columnas.append(dict(en="—", nombre="Huella", estado="suma", tecs=[], sumadas=T.SUMADAS["Huella"]))
    n = len(columnas)
    sep = 2.6
    w = (x1 - x0 - sep * (n - 1)) / n
    tam_n, tam_d = 2.4, 1.6
    pad = 1.3

    def alto_celda(nombre, nota, ancho, tn=tam_n, td=tam_d):
        ancho -= 1.4
        ln = cortar(nombre, ancho, tn, SERIF, 400)
        ld = cortar(nota, ancho, td) if nota else []
        return ln, ld, pad + len(ln) * tn * 1.15 + len(ld) * td * 1.28 + pad * 0.6

    # cabeceras
    yh = y0
    for i, C in enumerate(columnas):
        xc = x0 + i * (w + sep)
        h.texto(xc, yh + 2.0, C["en"], 1.8, color=GRIS)
        simbolo(h, xc + w - 5.0, yh + 1.4, C["estado"], 4.6)
        for j, ln in enumerate(cortar(C["nombre"], w - 1, 3.0, SERIF, 400)):
            h.texto(xc, yh + 6.0 + j * 3.3, ln, 3.0, familia=SERIF, peso=400)
    ybox = yh + 9.6
    # lo que se queda: toma, cambia, suma
    quedan, van = [], []
    for C in columnas:
        q = [(t[0], t[3], t[2]) for t in C["tecs"] if t[2] in ("toma", "cambia")]
        q += [(nombre, f"técnica {nt} de Contenida", "suma") for nombre, nt in C["sumadas"]]
        quedan.append(q)
        grupos = {}
        for t in C["tecs"]:
            if t[2] in ("deja", "no"):
                grupos.setdefault((t[3], t[2]), []).append(t[0])
        van.append([(", ".join(nombres), nota, est) for (nota, est), nombres in grupos.items()])
    altos = []
    for q in quedan:
        a = ybox + 1.6
        for nombre, nota, est in q:
            a += alto_celda(nombre, nota, w - 2 * pad - 2.2)[2] + 1.2
        altos.append(a)
    yfondo = max(altos) + 1.2
    for i, (C, q) in enumerate(zip(columnas, quedan)):
        xc = x0 + i * (w + sep)
        tipo = "contorno_r" if C["estado"] == "suma" else "celda"
        celda_abierta(h, xc, ybox, xc + w, yfondo, tipo, capa="fondo", w=0.4 if tipo == "celda" else 0.45)
        yy = ybox + 1.6
        for nombre, nota, est in q:
            ln, ld, a = alto_celda(nombre, nota, w - 2 * pad - 2.2)
            cx0, cx1 = xc + 1.1, xc + w - 1.1
            if est == "suma":
                punteado(h, cx0, yy, cx1, yy + a, "fondo", w=0.3)
            else:
                h.add("fondo", f'<rect x="{f(cx0)}" y="{f(yy)}" width="{f(cx1 - cx0)}" height="{f(a)}" '
                               f'{estilo("celda", w=0.22)}/>')
            if est == "cambia":
                delta(h, cx1 - 1.7, yy + 1.7, 2.1)
            yt = yy + pad + tam_n * 0.8
            yt = renglones(h, cx0 + pad, yt, ln, tam_n, SERIF, 400, inter=1.15)
            renglones(h, cx0 + pad, yt - tam_n * 0.15 + 0.2, ld, tam_d,
                      color=VIOLETA if est == "suma" else TINTA, inter=1.28)
            yy += a + 1.2
    # el fondo y lo que cae
    h.linea((x0 - 1, yfondo), (x1 + 1, yfondo), "linea", "fondo")
    h.texto(x1, yfondo + 3.1, "fondo ±0 · arriba, lo que se queda; abajo, lo que cae", 1.8, "end", color=GRIS)
    for i, v in enumerate(van):
        if not v:
            continue
        xc = x0 + i * (w + sep)
        xm = xc + w / 2
        h.flecha((xm, yfondo + 5.2), (xm, yfondo + 0.6), largo=1.6, ancho=0.6, capa="cotas", color=GRIS)
        h.linea((xm, yfondo + 0.3), (xm, yfondo + 3.8), "aux", "cotas")
        yy = yfondo + 6.2
        for nombre, nota, est in v:
            ln, ld, a = alto_celda(nombre, nota, w - 2 * pad - 2.2, 2.2, 1.5)
            cx0, cx1 = xc + 1.1, xc + w - 1.1
            tipo = "comparar" if est == "deja" else "rotura"
            h.add("fondo", f'<rect x="{f(cx0)}" y="{f(yy)}" width="{f(cx1 - cx0)}" height="{f(a)}" '
                           f'{estilo(tipo, w=0.22 if est == "deja" else 0.2)}/>')
            yt = yy + pad + 2.2 * 0.8
            yt = renglones(h, cx0 + pad, yt, ln, 2.2, SERIF, 300, color=GRIS if est == "deja" else TINTA,
                           inter=1.15)
            renglones(h, cx0 + pad, yt - 2.2 * 0.15 + 0.2, ld, 1.5, color=GRIS, inter=1.28)
            yy += a + 0.9
        if yy > Y1:
            print(f"  ! R-01: el dominio {i + 1} se pasa {yy - Y1:.1f} mm")


# ---------------------------------------------------------------- R-02

def r02(h):
    x = X0 + 2
    h.llamada(x + 4.5, Y0 + 6.5, 1, "R-02", "CUADRO DE LAS REFERENCIAS",
              "cada fila, una referencia; cada columna, dónde cae en Contenida")
    xs_tec, xs_ref, xs_arch, xs_visto, xs_col = x + 1, x + 15.5, x + 79, x + 117.5, x + 124.5
    xf = X1 - 1
    cols = T.COLUMNAS
    cw = (xf - xs_col) / len(cols)
    cxs = [xs_col + cw * (i + 0.5) for i in range(len(cols))]
    yh = Y0 + 16
    # cabecera: los cuadernos, los códigos y los nombres de las columnas
    for cuad, nombre in T.CUADERNOS.items():
        idx = [i for i, c in enumerate(cols) if c[2] == cuad]
        a, b = cxs[idx[0]] - cw / 2 + 0.6, cxs[idx[-1]] + cw / 2 - 0.6
        h.linea((a, yh + 2.0), (b, yh + 2.0), "cota", "textos")
        for xx in (a, b):
            h.linea((xx, yh + 2.0), (xx, yh + 3.3), "cota", "textos")
        h.texto((a + b) / 2, yh + 0.9, f"{cuad} · {nombre}", 1.8, "middle", color=GRIS)
    ycod = yh + 7.6
    for i, (c, nombre, cuad) in enumerate(cols):
        h.texto(cxs[i], ycod, c, 1.9 if len(c) < 4 else 1.6, "middle", peso=700)
        h.texto(cxs[i] + 0.65, ycod + 2.0, nombre, 1.75, "end", rot=-90, color=GRIS)
    ytab = ycod + 19.5
    for xx, t in ((xs_tec, "TÉCNICA"), (xs_ref, "REFERENCIA"), (xs_arch, "DÓNDE"), (xs_visto - 1.2, "VISTO")):
        h.texto(xx, ytab - 2.2, t, 1.75, color=GRIS, espaciado=0.2)
    h.linea((x, ytab - 0.8), (xf, ytab - 0.8), "filete", "textos", w=0.35)
    # las filas, por operación
    y = ytab
    fila_h, cab_h = 6.55, 7.0
    for op, O in T.OPERACIONES.items():
        claves = T.de_la_operacion(op)
        yc = y + 4.9
        marca_operacion(h, xs_tec, yc - 3.4, O["i"], 3.8)
        h.texto(xs_ref + 3, yc, f"{O['i']} · {O['nombre']}", 3.0, familia=SERIF, peso=500)
        h.texto(xs_ref + 30, yc, f"{O['figura'].lower()} · {len(claves)} referencias · {LAMINA_DE_OP[op]}", 1.85,
                color=GRIS)
        y += cab_h
        h.linea((x, y - 0.2), (xf, y - 0.2), "fina", "textos")
        for k in claves:
            R = T.REFERENCIAS[k]
            yb = y + 2.9
            xm = xs_tec
            for j, n in enumerate(R["tec"]):
                a = 4.2 if j == 0 else 3.3
                wm = marca_tecnica(h, xm + a * 12 / 29, yb - 0.6 - (0 if j == 0 else 0.4), n, a,
                                   no=T.TECNICA[n]["estado"] == "no")
                xm += wm + 0.8
            h.texto(xs_ref, yb, R["corto"], 2.55, familia=SERIF, peso=400)
            obra = R["obra"]
            while MEDIR.ancho(obra, 1.95, SERIF, 400, True) > xs_arch - xs_ref - 3 and len(obra) > 4:
                obra = obra[:-2].rstrip(" ,;") + "…"
            h.texto(xs_ref, yb + 2.6, obra, 1.95, familia=SERIF, cursiva=True, color=GRIS)
            nom, url = R["archivo"]
            nomc = nom if MEDIR.ancho(nom, 1.7, MONO) < xs_visto - xs_arch - 3 else nom[:22].rstrip() + "…"
            enlace(h, url, lambda nomc=nomc, yb=yb: h.texto(xs_arch, yb, nomc, 1.7))
            subrayado(h, xs_arch, yb, MEDIR.ancho(nomc, 1.7, MONO))
            lic = R["licencia"]
            if MEDIR.ancho(lic, 1.45, MONO) > xs_visto - xs_arch - 3:
                lic = cortar(lic, xs_visto - xs_arch - 3, 1.45)[0] + "…"
            h.texto(xs_arch, yb + 2.4, lic, 1.45, color=GRIS)
            casilla(h, xs_visto, yb - 2.1, R["mirada"], 2.5)
            caen = T.columnas_de(k)
            for i, (c, *_r) in enumerate(cols):
                if c in caen:
                    if c == "no":
                        h.linea((cxs[i], yb - 2.0), (cxs[i], yb + 0.6), "cota", "textos", w=0.45)
                        h.linea((cxs[i] - 2.6, yb - 0.7), (cxs[i], yb - 0.7), "cota", "textos")
                    else:
                        h.punto((cxs[i], yb - 0.7), 0.95, TINTA, "textos")
            y += fila_h
            h.linea((x, y - 0.2), (xf, y - 0.2), "fina", "textos", w=0.1)
    # las rayas de las columnas
    ytop = ycod + 3.0
    for i in range(len(cols) + 1):
        xx = xs_col + i * cw
        cambio = i in (0, 1, 5, 9, 14, len(cols))
        h.linea((xx, ycod - 2.6 if cambio else ytop), (xx, y), "filete" if cambio else "fina", "fondo",
                w=0.3 if cambio else 0.1)
    # la cuenta y lo que falta
    cuenta = cuenta_columnas()
    yt = y + 3.6
    h.texto(xs_col - 2, yt, "cuántas caen", 1.8, "end", color=GRIS)
    for i, (c, *_r) in enumerate(cols):
        if cuenta[c]:
            h.texto(cxs[i], yt, str(cuenta[c]), 2.1, "middle", peso=700)
        else:
            notdef(h, cxs[i] - 1.8, yt - 3.3, 3.6, 4.5, capa="textos", w=0.22)
    yn = yt + 5.4
    vacias = [(c, n) for c, n, _ in cols if not cuenta[c]]
    faltan = {c: [q for q, col, _t in T.NO_ENCONTRADO if col == c] for c, _ in vacias}
    textos = []
    for c, n in vacias:
        if c == "A6":
            textos.append(f"**{c}, {n}:** ninguna. La oclusión se toma del reel (la cinta de D12), pero ningún "
                          "archivo trajo una.")
        elif faltan[c]:
            textos.append(f"**{c}, {n}:** ninguna; se buscó y no apareció: {', '.join(faltan[c])} (R-08).")
        else:
            textos.append(f"**{c}, {n}:** ninguna: es un acuerdo, no una imagen.")
    yy = yn
    for t in textos:
        yy = h.parrafo(x, yy, xf - x, t, 2.25, inter=1.3) + 0.3
    if yy > Y1:
        print(f"  ! R-02: el cuadro se pasa {yy - Y1:.1f} mm")
    vacias_ = [c for c, *_r in cols if not cuenta[c]]
    h.columna(TEXTOS["R-02"] + [
        ("titulo", "Lo que muestra"),
        ("p", f"Las referencias se juntan en los planos ({cuenta['P']}), en la caja ({cuenta['A5']}), en el "
              f"repujado ({cuenta['A4']}) y en la voz ({cuenta['A10']}). {cuenta['no']} caen en lo que no se hace: "
              f"son vecinas opuestas, y se citan para no repetirlas. Una sola cae en el reparto: Bell, la máquina "
              f"que lee sin tocar. Sin ninguna: {', '.join(vacias_)}."),
        ("titulo", "Para la mano"),
        ("p", "Cuando mires una referencia, marca su casilla y cambia su _mirada_ a True en taxonomia.py: al "
              "rehacer las láminas, su fila y su ficha pasan a línea continua.")])


# ---------------------------------------------------------------- los mecanismos: cada técnica, como un detalle

def lamina_metal(h, puntos_arriba, puntos_abajo, patron="url(#metal)", w=0.35, capa="cuerpo"):
    """Una chapa en corte: el borde de arriba y el de abajo, rellena del rayado del metal."""
    pts = list(puntos_arriba) + list(reversed(puntos_abajo))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + " Z"
    h.relleno(d, patron, capa)
    h.add(capa, f'<path d="{d}" {estilo("contorno", w=w)}/>')


def perfil_relieve(x, xa, xb, xc, xd, alto):
    """La altura del relieve en x: plano, rampa, meseta, rampa y plano."""
    if x <= xa or x >= xd:
        return 0.0
    if x < xb:
        return alto * (1 - math.cos(math.pi * (x - xa) / (xb - xa))) / 2
    if x <= xc:
        return alto
    return alto * (1 + math.cos(math.pi * (x - xc) / (xd - xc))) / 2


def mec_1(h, x0, y0, x1, y1):
    """Textura contra plano, en corte: la placa dada vuelta, y el dedo que la recorre."""
    w = x1 - x0
    yb = y0 + (y1 - y0) * 0.66
    xi, xf = x0 + 6, x0 + w * 0.80
    xa, xd = x0 + w * 0.33, x0 + w * 0.60
    xb, xc = xa + 7.5, xd - 7.5
    alto, t = 7.0, 0.9
    xs = np.linspace(xi, xf, 180)
    arriba = [(xx, yb - perfil_relieve(xx, xa, xb, xc, xd, alto)) for xx in xs]
    abajo = [(xx, yy + t) for xx, yy in arriba]
    lamina_metal(h, arriba, abajo)
    # el recorrido del dedo, por encima del relieve
    dedo = [(xx, yy - 3.2) for xx, yy in arriba if xi + 4 <= xx <= xd + 2.5]
    h.poli(dedo, "aux", "cotas", w=0.3, color=TINTA)
    h.flecha(dedo[-1], dedo[-6], largo=2.0, ancho=0.7)
    h.nota(dedo[12], (x0 + 4, y0 + 4.0), "el dedo la recorre: se lee la diferencia", 2.1, ancla="start")
    h.nota(((xb + xc) / 2, yb - alto + t + 0.2), ((xb + xc) / 2 + 9, yb + 9.0), "reverso, abajo: el canal (P-02 · 3)",
           2.1)
    h.nota((xi + 8, yb + t + 0.1), (xi + 13, yb + 9.0), "plano", 2.1)
    h.nota(((xb + xc) / 2 - 3, yb - alto - 0.1), (xc + 8, y0 + 4.0), "relieve: la letra, por el frente", 2.1)
    xcota = xd + 6.5
    h.linea((xc + 1.5, yb - alto), (xcota + 1.6, yb - alto), "cota")
    h.cota((xcota, yb), (xcota, yb - alto), 0.001, "", tam=2.1, ext=False)
    h.texto(xcota + 3.6, yb - alto / 2 + 0.7, "h: la decide la mano", 2.1)
    h.texto(x0 + 2, y1 - 1.0, "anverso arriba, reverso abajo: es la placa de la Acción 4, dada vuelta", 1.9, color=GRIS)


def mec_2(h, x0, y0, x1, y1):
    """Huella en metal blando, en corte: algo aprieta una chapa sobre una base blanda. Y quién aprieta."""
    w = x1 - x0
    xl, xr = x0 + 4, x0 + w * 0.38
    yb = y0 + (y1 - y0) * 0.56
    xm = (xl + xr) / 2
    r, t = 3.4, 0.8

    def hundido(xx):
        d = abs(xx - xm)
        return 0.0 if d >= r else math.sqrt(r * r - d * d) * 0.85

    xs = np.linspace(xl, xr, 200)
    base_arriba = [(xx, yb + hundido(xx)) for xx in xs]
    base = base_arriba + [(xr, yb + 9.5), (xl, yb + 9.5)]
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in base) + " Z"
    h.relleno(d, "url(#blanda)", "cuerpo")
    h.add("cuerpo", f'<path d="{d}" {estilo("placa", w=0.25)}/>')
    lamina_metal(h, [(xx, yy - t) for xx, yy in base_arriba], base_arriba)
    rb = r * 0.78
    cyb = yb - t + hundido(xm) - rb
    h.circulo((xm, cyb), rb, "contorno", "cuerpo", relleno=PLATA, w=0.35)
    h.poli([(xm - 1.0, cyb - rb + 0.3), (xm - 1.6, y0 + 4.0), (xm + 1.6, y0 + 4.0), (xm + 1.0, cyb - rb + 0.3)],
           "contorno", "cuerpo", w=0.35)
    h.flecha((xm - 5.0, cyb - rb - 1.0), (xm - 5.0, y0 + 4.5), largo=2.4, ancho=0.9)
    h.linea((xm - 5.0, y0 + 4.5), (xm - 5.0, cyb - rb - 2.0), "cota")
    h.texto(xm - 6.4, y0 + 7.0, "aprieta", 2.1, "end")
    h.nota((xm + 1.4, y0 + 9.0), (xr + 1.0, y0 + 5.5), "lo que aprieta", 2.1)
    h.nota((xr - 4.0, yb - t / 2), (xr + 1.0, yb - 5.0), "metal blando", 2.1)
    h.nota((xr - 5.0, yb + 5.0), (xr + 1.0, yb + 7.5), "la base", 2.1)
    # quién aprieta y qué guarda la huella
    xt = x0 + w * 0.61
    yt = y0 + 4.5
    cols = (xt, xt + 17)
    h.texto(cols[0], yt, "QUIÉN APRIETA", 1.7, color=GRIS, espaciado=0.2)
    h.texto(cols[1], yt, "QUÉ GUARDA LA HUELLA", 1.7, color=GRIS, espaciado=0.2)
    h.linea((xt, yt + 1.2), (x1, yt + 1.2), "filete", "textos")
    filas = [("la mano", "aluminio de cocina", "Contenida, Acción 4"),
             ("la voz", "una hoja de estaño", "el fonógrafo, 1877"),
             ("un helecho", "una plancha de plomo", "Auer y Bradbury, 1852 (R-05)")]
    for i, (quien, que, donde) in enumerate(filas):
        yy = yt + 5.6 + i * 7.6
        h.texto(cols[0], yy, quien, 2.4, familia=SERIF, peso=500 if i == 0 else 400)
        h.texto(cols[1], yy, que, 2.1)
        h.texto(cols[1], yy + 2.8, donde, 1.8, color=GRIS)
        h.linea((xt, yy + 4.2), (x1, yy + 4.2), "fina", "textos")
    h.texto(xt, yt + 5.6 + 3 * 7.6 + 0.6, "el mismo corte: cambia quién aprieta", 1.9, color=GRIS)


def mec_3(h, x0, y0, x1, y1):
    """Contraste semántico: cada vecina, unida a Contenida por dos hilos (en qué se parece, en qué se separa)."""
    xn, xp = x0 + 2, x0 + 33
    xs = xp + (x1 - xp) / 2 + 1
    y = y0 + 3.2
    h.texto(xn, y, "LA VECINA", 1.7, color=GRIS, espaciado=0.2)
    simbolo(h, xp, y - 0.6, "toma", 4.4)
    h.texto(xp + 6, y, "EN QUÉ SE PARECE", 1.7, color=GRIS, espaciado=0.2)
    simbolo(h, xs, y - 0.6, "deja", 4.4)
    h.texto(xs + 6, y, "EN QUÉ SE SEPARA", 1.7, color=GRIS, espaciado=0.2)
    h.linea((xn, y + 1.2), (x1, y + 1.2), "filete", "textos")
    paso = min(5.4, (y1 - y - 3) / len(T.VECINAS))
    for i, (k, nombre, parece, separa) in enumerate(T.VECINAS):
        yy = y + 4.6 + i * paso
        h.texto(xn, yy, nombre, 2.0)
        hilo(h, (xp, yy - 0.7), (xp + 4.0, yy - 0.7), True, capa="textos")
        h.texto(xp + 6, yy, parece, 2.3, familia=SERIF, peso=400)
        hilo(h, (xs, yy - 0.7), (xs + 4.0, yy - 0.7), False, "comparar", GRIS, "textos")
        h.texto(xs + 6, yy, separa, 2.3, familia=SERIF, peso=300, color=GRIS)
        h.linea((xn, yy + 1.5), (x1, yy + 1.5), "fina", "textos", w=0.1)


def mec_4(h, x0, y0, x1, y1):
    """Quién lo hizo, como un cajetín: cada mano de la cadena, con su nombre; dos renglones, para la mano."""
    cx0, cx1 = x0 + 2, min(x1 - 2, x0 + 112)
    yt = y0 + 2
    filas = [("IMPRIMIERON", "los alumnos ciegos de Haüy, con Clousier · 1786"),
             ("HUNDIÓ", "¿Auer o Bradbury? · 1852-1855"),
             ("GRABARON", "unos cuarenta gabinetes, en España · 1896-1905"),
             ("REPUJA", None), ("MIRA", None)]
    fh, cab = 5.6, 7.0
    alto = cab + fh * len(filas)
    h.add("textos", f'<rect x="{f(cx0)}" y="{f(yt)}" width="{f(cx1 - cx0)}" height="{f(alto)}" fill="{PAPEL}" '
                    f'stroke="{TINTA}" stroke-width="0.5"/>')
    h.texto(cx0 + 2, yt + 4.8, "CONTENIDA", 3.0, peso=700, espaciado=0.4)
    h.texto(cx0 + 28, yt + 4.8, "el colofón de manos", 2.1, color=GRIS)
    xv = cx0 + 25
    for i, (k, v) in enumerate(filas):
        ya = yt + cab + i * fh
        h.linea((cx0, ya), (cx1, ya), "filete", "textos")
        h.texto(cx0 + 1.6, ya + 3.7, k, 1.7, color=GRIS, espaciado=0.2)
        if v:
            h.texto(xv, ya + 3.8, v, 2.0)
        else:
            h.linea((xv, ya + 4.0), (cx1 - 3, ya + 4.0), "contorno_r", "textos", w=0.3)
    h.linea((xv - 2, yt + cab), (xv - 2, yt + alto), "filete", "textos")
    h.texto(cx0, yt + alto + 4.2, "cada mano de la cadena, con su nombre o «sin nombre registrado» (06, §6.1)", 1.95,
            color=GRIS)


def mec_5(h, x0, y0, x1, y1):
    """Región común, en planta: la mano de Beda como casillas, sin la mano; y la caja de 8 × 7."""
    cw, ch, sep = 6.4, 5.8, 1.4
    yb = min(y1 - 9, y0 + 14 + 4 * ch + 8)
    xb = x0 + 5
    dedos = [("pulgar", 2), ("índice", 3), ("medio", 3), ("anular", 3), ("meñique", 3)]
    for i, (nombre, art) in enumerate(dedos):
        xx = xb + i * (cw + sep)
        for j in range(art + 1):
            yy = yb - (j + 1) * ch
            h.add("cuerpo", f'<rect x="{f(xx)}" y="{f(yy)}" width="{f(cw)}" height="{f(ch)}" '
                            f'{estilo("celda", w=0.28)}/>')
            if j == art:
                h.add("cuerpo", f'<rect x="{f(xx + 1.3)}" y="{f(yy + 1.2)}" width="{f(cw - 2.6)}" '
                                f'height="{f(ch - 2.4)}" fill="url(#metal)" stroke="none"/>')
        h.texto(xx + cw / 2, yb + 3.2, nombre, 1.65, "middle", color=GRIS)
    x5 = xb + 5 * (cw + sep) - sep
    h.nota((xb + 4 * (cw + sep) + cw / 2, yb - 4 * ch + ch / 2), (x5 + 4, yb - 4 * ch - 2.0), "uñas: 5", 2.0)
    h.nota((xb + 4 * (cw + sep) + cw - 1, yb - 1.5 * ch), (x5 + 4, yb - 2.5 * ch), "articulaciones:", 2.0)
    h.texto(x5 + 7.8, yb - 2.5 * ch + 3.2, "14", 2.0)
    h.texto(xb, y0 + 3.0, "la mano de Beda: 19 casillas (Cooperrider, 2022)", 2.1)
    h.texto(xb, y0 + 6.0, "se toma la retícula, no la figura", 1.9, color=GRIS)
    # la caja
    kx0 = x1 - 8 * 3.6 - 4
    kw, kh = 3.6, 4.3
    ky0 = yb - 7 * kh
    for fila in range(7):
        for col in range(8):
            xx, yy = kx0 + col * kw, ky0 + fila * kh
            h.add("cuerpo", f'<rect x="{f(xx)}" y="{f(yy)}" width="{f(kw)}" height="{f(kh)}" '
                            f'{estilo("celda", w=0.2)}/>')
    h.texto(kx0 + kw / 2, ky0 + kh * 0.72, ",", 2.6, "middle", familia=SERIF)
    h.texto(kx0 + 7.5 * kw, ky0 + 6.72 * kh, "¶", 2.4, "middle", familia=SERIF, color=GRIS2)
    h.texto(x1 - 2, y0 + 3.0, "la caja: 8 × 7 = 56 celdas", 2.1, "end")
    h.texto(x1 - 2, y0 + 6.0, "de la coma de la 1 al ¶ de la 56", 1.9, "end", color=GRIS)
    h.texto(kx0 + 4 * kw, yb + 3.2, "Acción 5 · P-10", 1.65, "middle", color=GRIS)


def mec_6(h, x0, y0, x1, y1):
    """Composición por partes, en axonometría: los estados de una letra, uno sobre otro."""
    W, D = 30.0, 22.0
    k, ang = 0.55, math.radians(30)
    dx, dy = D * k * math.cos(ang), -D * k * math.sin(ang)
    sep = 12.5
    xb, yb = x0 + 6, min(y1 - 6, y0 + 2 * 12.5 + 22.0 * 0.55 * 0.5 + 14)

    def p(u, v, nivel_):
        return (xb + u + v / D * dx, yb - nivel_ * sep + v / D * dy)

    capas = [("placa", "Acción 4"), ("cinta", "Acción 6"), ("frotado", "Acción 8")]
    for i, (nombre, accion) in enumerate(capas):
        esquinas = [p(0, 0, i), p(W, 0, i), p(W, D, i), p(0, D, i)]
        d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in esquinas) + " Z"
        h.relleno(d, "url(#metal)" if nombre == "placa" else PAPEL, "cuerpo")
        h.add("cuerpo", f'<path d="{d}" {estilo("placa", w=0.3)}/>')
        anillo = [p(W / 2 + 7.5 * math.cos(a), D / 2 + 7.5 * math.sin(a) * 1.0, i)
                  for a in np.linspace(0, 2 * math.pi, 80)]
        if nombre == "placa":
            h.poli(anillo, "contorno", "cuerpo", cerrado=True, w=0.45)
        elif nombre == "cinta":
            h.poli(anillo, "contorno", "cuerpo", cerrado=True, w=1.3, color="#d8d1c2")
            h.poli(anillo, "contorno", "cuerpo", cerrado=True, w=0.15)
        else:
            h.poli(anillo, "contorno", "cuerpo", cerrado=True, w=0.9, color=GRIS2, dash="0.5 0.35")
        h.texto(p(W, D, i)[0] + 2.5, p(W, 0, i)[1] - 2.0, f"{nombre} · {accion}", 2.1)
        if i:
            for u, v in ((0, 0), (W, 0), (W, D), (0, D)):
                h.linea(p(u, v, i - 1), p(u, v, i), "aux", "aux")
    xt = x0 + 6 + W + dx + 26
    ancho = x1 - xt - 1
    yy = renglones(h, xt, y0 + 3.0, cortar("la misma letra, varias manos: los estados, uno sobre otro (10, §10.6)",
                                           ancho, 2.1), 2.1, inter=1.3)
    yy = renglones(h, xt, yy + 1.4, cortar("Page, 1874: un bloque de madera por color, impresos uno encima del otro",
                                           ancho, 1.9), 1.9, color=GRIS, inter=1.3)
    renglones(h, xt, yy + 1.4, cortar("Hoefnagel, h. 1595: cada letra con su construcción, como los planos P-03 a "
                                      "P-07", ancho, 1.9), 1.9, color=GRIS, inter=1.3)


def mec_no(h, x0, y0, x1, y1, texto, vecinas):
    """Lo que no se hace no se dibuja: una celda vacía, con trazo y punto."""
    celda_abierta(h, x0 + 1, y0 + 1, x1 - 1, y1 - 1, "rotura", capa="fondo", w=0.35)
    xc = x0 + 5
    h.texto(xc, y0 + 6.0, "NO SE DIBUJA", 2.4, peso=700, espaciado=0.2)
    yy = renglones(h, xc, y0 + 10.0, cortar(texto, x1 - x0 - 12, 2.5, SERIF, 400), 2.5, SERIF, 400, inter=1.25)
    for nombre in vecinas:
        hilo(h, (xc, yy - 0.2), (xc + 5, yy - 0.2), False, "rotura", TINTA, "textos", w=0.3)
        h.texto(xc + 7, yy + 0.5, nombre, 2.0, color=GRIS)
        yy += 3.6


def gota(cx, cy, r, n=40):
    """Una gota: la punta arriba y el peso abajo. (cx, cy) es el centro de la parte redonda."""
    pts = []
    for a in np.linspace(-math.pi / 2, 3 * math.pi / 2, n):
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        if math.sin(a) < 0:
            s = -math.sin(a)
            x = cx + r * math.cos(a) * (1 - s) ** 0.9
            y = cy - r * s * 1.9
        pts.append((x, y))
    return pts


def mec_8(h, x0, y0, x1, y1):
    """Síntesis temporal, en serie: la misma gota, cuadro por cuadro; abajo, los frotados."""
    n, sep = 5, 2.6
    fw = (x1 - x0 - 4 - sep * (n - 1)) / n
    fy0, fh = y0 + 1, (y1 - y0) * 0.6
    for i in range(n):
        fx0 = x0 + 2 + i * (fw + sep)
        h.add("fondo", f'<rect x="{f(fx0)}" y="{f(fy0)}" width="{f(fw)}" height="{f(fh)}" {estilo("fina")}/>')
        h.texto(fx0 + 1.2, fy0 + 3.0, f"{i + 1:02d}", 1.8, color=GRIS)
        yw = fy0 + fh * 0.7
        cx = fx0 + fw / 2
        xs = np.linspace(fx0 + 0.6, fx0 + fw - 0.6, 90)
        if i == 2:
            sup = [(x, yw + 2.4 * math.exp(-((x - cx) / 3.2) ** 2)) for x in xs]
        elif i == 4:
            sup = [(x, yw - 0.7 * math.cos((x - cx) * 1.5) * math.exp(-abs(x - cx) / 7)) for x in xs]
        else:
            sup = [(x, yw) for x in xs]
        h.poli(sup, "contorno", "cuerpo", w=0.3)
        for j in range(1, 4):
            h.linea((fx0 + 2.5 + j * 0.9, yw + 1.0 + j * 1.6), (fx0 + fw - 2.5 - j * 0.9, yw + 1.0 + j * 1.6),
                    "aux", "aux")
        if i == 0:
            h.poli(gota(cx, yw - fh * 0.42, 1.7), "contorno", "cuerpo", cerrado=True, w=0.3)
            h.flecha((cx + 4.0, yw - 4.0), (cx + 4.0, yw - 9.0), largo=1.4, ancho=0.5, color=GRIS)
        elif i == 1:
            h.poli(gota(cx, yw - 1.7, 1.7), "contorno", "cuerpo", cerrado=True, w=0.3)
        elif i == 2:
            for s in (-1, 1):
                h.circulo((cx + s * 4.2, yw - 2.4), 0.45, "contorno", "cuerpo", w=0.25)
                h.circulo((cx + s * 5.4, yw - 4.0), 0.35, "contorno", "cuerpo", w=0.25)
        elif i == 3:
            h.poli([(cx - 0.8, yw), (cx - 0.6, yw - 6.0), (cx + 0.6, yw - 6.0), (cx + 0.8, yw)], "contorno", "cuerpo",
                   w=0.3)
            h.circulo((cx, yw - 8.0), 0.9, "contorno", "cuerpo", w=0.3)
    h.texto(x0 + 2, fy0 + fh + 3.4, "la misma gota, cuadro por cuadro: ninguno igual (Acción 9: fotos seguidas)", 1.9,
            color=GRIS)
    # los frotados: la misma placa, cada vez más clara
    yf = fy0 + fh + 6.0
    tonos = [TINTA, GRIS, GRIS2, FILETE, "#e3dfd6"]
    for i, c in enumerate(tonos):
        fx0 = x0 + 2 + i * (fw + sep)
        hh = min(fw, y1 - yf - 1)
        h.add("fondo", f'<rect x="{f(fx0)}" y="{f(yf)}" width="{f(fw)}" height="{f(hh)}" {estilo("fina")}/>')
        h.circulo((fx0 + fw / 2, yf + hh / 2), hh * 0.28, "contorno", "cuerpo", w=0.9, color=c)
        rot = f"frotado {i + 1:02d}" if i < 4 else "frotado n"
        h.texto(fx0 + 1.0, yf + hh - 1.0, rot, 1.6, color=GRIS)
    h.texto(x0 + 2 + 5 * (fw + sep) - sep, yf + min(fw, y1 - yf - 1) + 3.2, "n: el último que se lee (Acción 8)", 1.8,
            "end", color=GRIS)


def mec_9(h, x0, y0, x1, y1):
    """Recorrido de lectura, en planta: un verso compuesto en los azulejos del fondo, y su recorrido."""
    filas = ["termina y", "empieza"]
    t = 7.6
    gx0, gy0 = x0 + 4, y0 + 6
    ncol, nfil = 9, 3
    for fila in range(nfil):
        for col in range(ncol):
            h.add("fondo", f'<rect x="{f(gx0 + col * t)}" y="{f(gy0 + fila * t)}" width="{f(t)}" height="{f(t)}" '
                           f'{estilo("fina")}/>')
    centros = []
    for fila, verso in enumerate(filas):
        for col, ch in enumerate(verso):
            cx, cy = gx0 + col * t + t / 2, gy0 + fila * t + t / 2
            if ch == " ":
                continue
            m = 1.1
            h.add("cuerpo", f'<rect x="{f(cx - t / 2 + m)}" y="{f(cy - t / 2 + m)}" width="{f(t - 2 * m)}" '
                            f'height="{f(t - 2 * m)}" fill="url(#metal)" {estilo("placa", w=0.25)[11:]}/>')
            h.texto(cx, cy + 1.1, ch, 3.0, "middle", familia=SERIF, peso=400, fondo=True)
            centros.append((cx, cy))
    # el recorrido: cada placa con su paso, y una flecha al final de cada renglón
    for i, (cx, cy) in enumerate(centros):
        h.texto(cx - t / 2 + 0.5, cy - t / 2 + 1.9, str(i + 1), 1.35, color=GRIS)
    filas_y = sorted({round(cy, 2) for _, cy in centros})
    for cy in filas_y:
        xs_ = [cx for cx, cy_ in centros if round(cy_, 2) == cy]
        yr = cy + t * 0.5 - 1.0
        h.linea((min(xs_) - t * 0.3, yr), (max(xs_) + t * 0.62, yr), "aux", "cotas", color=TINTA, w=0.28)
        h.flecha((max(xs_) + t * 0.72, yr), (max(xs_) + t * 0.3, yr), largo=1.5, ancho=0.55)
    # termina y empieza: del último paso, por arriba, al primero
    xu, yu = centros[-1][0] + t * 0.5, centros[-1][1]
    xp, yp = centros[0][0], centros[0][1] - t * 0.5
    ya = gy0 - 2.6
    vuelta = [(xu + 0.4, yu), (gx0 + ncol * t + 2.4, yu), (gx0 + ncol * t + 2.4, ya), (xp, ya), (xp, yp - 0.3)]
    h.poli(vuelta, "aux", "cotas", w=0.22, color=GRIS)
    h.flecha((xp, yp - 0.2), (xp, ya), largo=1.4, ancho=0.55, color=GRIS)
    xt = gx0 + ncol * t + 6.5
    h.texto(xt, gy0 + 2.6, "un verso, en el fondo de la piscina:", 2.0)
    h.texto(xt, gy0 + 5.4, "una placa por azulejo y un azulejo", 2.0)
    h.texto(xt, gy0 + 8.2, "vacío entre palabras (Acción 11)", 2.0)
    h.texto(xt, gy0 + 13.0, "el recorrido: si la pared no alcanza,", 1.9, color=GRIS)
    h.texto(xt, gy0 + 15.8, "el verso dobla la esquina", 1.9, color=GRIS)
    h.texto(xt, gy0 + 20.6, "Feuillet, 1701: la página escribe", 1.9, color=GRIS)
    h.texto(xt, gy0 + 23.4, "el recorrido de quien baila", 1.9, color=GRIS)
    h.texto(gx0, gy0 + nfil * t + 6.4, "termina y empieza: después de componer, se distribuye y se vuelve a empezar",
            1.9, color=GRIS)


def mec_10(h, x0, y0, x1, y1):
    """Cadena de soportes: la huella cambia de signo en cada paso. Arriba, 1852; abajo, Contenida."""
    w = x1 - x0 - 4
    n, sep = 4, 7.0
    cw = (w - sep * (n - 1)) / n
    yb = y0 + 12
    pasos = [("el helecho", "se aprieta"), ("el plomo", "hundido"), ("el cobre", "en relieve"),
             ("el papel", "la tinta")]
    for i, (nombre, estado) in enumerate(pasos):
        cx0 = x0 + 2 + i * (cw + sep)
        cxm = cx0 + cw / 2
        xs = np.linspace(cx0, cx0 + cw, 90)
        if i == 0:
            arriba = [(x, yb) for x in xs]
            h.poli([(x, yb - 1.3 - 0.6 * math.sin((x - cx0) * 2.2)) for x in np.linspace(cxm - 7, cxm + 7, 60)],
                   "contorno", "cuerpo", w=0.35)
            h.flecha((cxm, yb - 2.6), (cxm, yb - 8.0), largo=1.6, ancho=0.6)
        elif i == 1:
            arriba = [(x, yb + 1.6 * math.exp(-((x - cxm) / 4.5) ** 2) * (1 + 0.3 * math.sin((x - cxm) * 2.2)))
                      for x in xs]
        elif i == 2:
            arriba = [(x, yb - 1.6 * math.exp(-((x - cxm) / 4.5) ** 2) * (1 + 0.3 * math.sin((x - cxm) * 2.2)))
                      for x in xs]
        else:
            arriba = [(x, yb + 3.0) for x in xs]
        espesor = 0.8 if i == 3 else 4.0
        abajo = [(x, (yb + 3.0 if i == 3 else yb) + espesor) for x in xs]
        patron = PAPEL if i == 3 else ("url(#metal)" if i in (1, 2) else "url(#blanda)")
        lamina_metal(h, arriba, abajo, patron, 0.3)
        if i == 3:
            h.linea((cxm - 6, yb + 2.85), (cxm + 6, yb + 2.85), "contorno", "cuerpo", w=0.7)
        h.texto(cxm, yb + 8.0, nombre, 2.1, "middle")
        h.texto(cxm, yb + 10.6, estado, 1.8, "middle", color=GRIS)
        if i:
            xa = cx0 - sep + 1.0
            h.linea((xa, yb + 1.5), (cx0 - 1.2, yb + 1.5), "cota")
            h.flecha((cx0 - 1.0, yb + 1.5), (cx0 - 3.0, yb + 1.5), largo=1.4, ancho=0.55)
    h.texto(x0 + 2, y0 + 2.8, "1852: la impresión natural (Auer; Bradbury, 1855)", 2.0)
    # Contenida
    yc = yb + 19.5
    h.texto(x0 + 2, yc - 5.6, "Contenida: la cadena de estados (03, §3.7)", 2.0)
    estados = [("calco", "línea"), ("placa", "relieve"), ("cinta", "plano"), ("frotado", "gris"),
               ("agua", "luz"), ("voz", "onda")]
    paso = w / len(estados)
    xs_ = [x0 + 2 + paso * (i + 0.5) for i in range(len(estados))]
    for i, (e, q) in enumerate(estados):
        h.circulo((xs_[i], yc), 1.6, "filete", "textos", relleno=PAPEL)
        h.texto(xs_[i], yc + 4.4, e, 2.1, "middle")
        h.texto(xs_[i], yc + 7.0, q, 1.8, "middle", color=GRIS)
        if i:
            h.linea((xs_[i - 1] + 2.0, yc), (xs_[i] - 2.2, yc), "cota", "textos")
            h.flecha((xs_[i] - 2.0, yc), (xs_[i] - 4.0, yc), largo=1.4, ancho=0.55, capa="textos")
    h.texto(x0 + 2, yc + 11.4, "cada paso pierde materia y gana luz (Acción 8)", 1.9, color=GRIS)


def mec_11(h, x0, y0, x1, y1):
    """La voz como línea, en alzado: el trazo sobre papel ahumado; y lo que tardó en oírse, como una cota."""
    sx0, sx1 = x0 + 2, x1 - 2
    sy0, sh = y0 + 3, 12.0
    h.add("fondo", f'<rect x="{f(sx0)}" y="{f(sy0)}" width="{f(sx1 - sx0)}" height="{f(sh)}" fill="{PLATA}" '
                   f'{estilo("placa", w=0.25)[11:]}/>')
    xs = np.linspace(sx0 + 2, sx1 - 2, 900)
    u = (xs - xs[0]) / (xs[-1] - xs[0])
    env = 0.25 + 0.75 * np.abs(np.sin(u * math.pi * 7.3)) ** 1.5 * (0.6 + 0.4 * np.sin(u * 19))
    yy = sy0 + sh / 2 + env * 4.2 * np.sin(u * 2 * math.pi * 61) * np.cos(u * 2 * math.pi * 3.1)
    h.poli(list(zip(xs, yy)), "contorno", "cuerpo", w=0.18)
    h.flecha((sx1 - 1, sy0 + sh + 3.2), (sx1 - 10, sy0 + sh + 3.2), largo=1.6, ancho=0.6)
    h.linea((sx1 - 10, sy0 + sh + 3.2), (sx1 - 2, sy0 + sh + 3.2), "cota")
    h.texto(sx1 - 11, sy0 + sh + 3.9, "t", 2.2, "end", familia=SERIF, cursiva=True)
    h.texto(sx0, sy0 + sh + 3.9, "«Au clair de la lune», 9 de abril de 1860: la voz, escrita", 1.9, color=GRIS)
    # el tiempo, en una cota
    yt = sy0 + sh + 14
    a, b = sx0 + 6, sx1 - 6
    h.cota((a, yt), (b, yt), 0.001, "148 años: escrita, sin oírse", tam=2.2, ext=False)
    for xx, t in ((a, "1860 · Scott la escribe"), (b, "2008 · First Sounds la hace sonar")):
        h.linea((xx, yt - 2.0), (xx, yt + 2.0), "cota")
        h.texto(xx, yt + 5.0, t, 1.9, "start" if xx == a else "end")


def segmentos_cero(Z, xs, ys):
    """Marching squares: los segmentos donde Z cruza el cero (en coordenadas xs, ys)."""
    segs = []
    ny, nx = Z.shape
    for j in range(ny - 1):
        for i in range(nx - 1):
            c = [Z[j, i], Z[j, i + 1], Z[j + 1, i + 1], Z[j + 1, i]]
            esquinas = [(xs[i], ys[j]), (xs[i + 1], ys[j]), (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])]
            pts = []
            for a in range(4):
                b = (a + 1) % 4
                if (c[a] > 0) != (c[b] > 0):
                    t = c[a] / (c[a] - c[b])
                    pts.append((esquinas[a][0] + t * (esquinas[b][0] - esquinas[a][0]),
                                esquinas[a][1] + t * (esquinas[b][1] - esquinas[a][1])))
            if len(pts) == 2:
                segs.append(pts)
            elif len(pts) == 4:
                segs += [pts[:2], pts[2:]]
    return segs


def mec_12(h, x0, y0, x1, y1):
    """Hacer visible lo que suena, en planta: la arena en las líneas donde la placa no vibra."""
    lado = min(y1 - y0 - 8, 34.0)
    px0, py0 = x0 + 5, y0 + 4
    h.add("fondo", f'<rect x="{f(px0)}" y="{f(py0)}" width="{f(lado)}" height="{f(lado)}" fill="{PLATA}" '
                   f'{estilo("placa", w=0.35)[11:]}/>')
    n, m = 1, 4
    N = 121
    us = np.linspace(0, 1, N)
    U, V = np.meshgrid(us, us)
    Z = np.cos(n * math.pi * U) * np.cos(m * math.pi * V) - np.cos(m * math.pi * U) * np.cos(n * math.pi * V)
    for (a, b) in segmentos_cero(Z, px0 + us * lado, py0 + us * lado):
        h.add("cuerpo", f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="{TINTA}" '
                        f'stroke-width="0.55" stroke-linecap="round" stroke-dasharray="0.05 0.62"/>')
    # los dedos: donde las líneas llegan al borde
    bordes = [u for u in range(1, N - 1) if (Z[0, u] > 0) != (Z[0, u + 1] > 0)]
    for u in bordes[:2]:
        h.circulo((px0 + us[u] * lado, py0 - 1.6), 1.3, "contorno", "cuerpo", relleno=PAPEL, w=0.3)
    xx = px0 + us[bordes[0]] * lado if bordes else px0 + lado / 2
    xn = px0 + lado + 5
    an = x1 - xn - 4.5
    h.nota((xx, py0 - 2.9), (xn, py0 - 0.6), "los dedos la sujetan", 2.0)
    h.linea((px0 + lado + 0.6, py0 + lado * 0.3), (px0 + lado + 0.6, py0 + lado * 0.52), "contorno", "cuerpo", w=1.0)
    h.nota((px0 + lado + 1.2, py0 + lado * 0.41), (xn, py0 + lado * 0.41), "el arco la hace sonar", 2.0)
    lineas = cortar("la arena se junta donde la placa no vibra", an, 2.0)
    h.nota((px0 + lado * 0.5, py0 + lado * 0.5), (xn, py0 + lado * 0.74), "", 2.0, lineas=lineas)
    renglones(h, xn + 3.8, py0 + lado * 0.74 + 0.7 + len(lineas) * 2.5 + 0.6,
              cortar("la figura depende de dónde apoyan los dedos", an, 1.85), 1.85, color=GRIS)


def mec_13(h, x0, y0, x1, y1):
    """Leer sin tocar, en corte: la luz lee el surco; la aguja no existe, se calcula: va a puntos."""
    xl, xr = x0 + 4, x0 + (x1 - x0) * 0.62
    yt = y0 + (y1 - y0) * 0.58
    xm = (xl + xr) / 2
    surco = [(xl, yt), (xm - 4.0, yt), (xm - 1.2, yt + 3.6), (xm + 1.2, yt + 3.6), (xm + 4.0, yt), (xr, yt),
             (xr, yt + 9), (xl, yt + 9)]
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in surco) + " Z"
    h.relleno(d, PLATA, "cuerpo")
    h.add("cuerpo", f'<path d="{d}" {estilo("contorno", w=0.35)}/>')
    fuente = (xm - 16, y0 + 3.5)
    lector = (xm + 16, y0 + 3.5)
    h.circulo(fuente, 1.4, "contorno", "cuerpo", relleno=PAPEL, w=0.3)
    h.add("cuerpo", f'<rect x="{f(lector[0] - 1.8)}" y="{f(lector[1] - 1.2)}" width="3.6" height="2.4" '
                    f'fill="{PAPEL}" {estilo("contorno", w=0.3)[11:]}/>')
    for pared, sale in (((xm - 2.6, yt + 1.8), lector), ((xm + 2.6, yt + 1.8), lector)):
        h.linea(fuente, pared, "aux", "cotas", color=TINTA)
        h.linea(pared, sale, "aux", "cotas", color=TINTA)
    h.flecha(lector, (lector[0] - 3.0, lector[1] + 2.0), largo=1.4, ancho=0.5)
    # la aguja, calculada
    h.poli([(xm, yt + 3.4), (xm + 1.0, yt - 1.0), (xm + 5.5, yt - 12.0), (xm + 4.3, yt - 12.6), (xm - 0.6, yt - 1.4),
            (xm, yt + 3.4)], "contorno_r", "cuerpo", w=0.5)
    an = x1 - xr - 9
    h.nota((xm + 4.8, yt - 11.5), (xr + 3, yt - 13.5), "", 2.0, color=VIOLETA,
           lineas=cortar("la aguja: no existe, se calcula", an, 2.0))
    h.nota(fuente, (xr + 3, y0 + 1.5), "", 2.0, lineas=cortar("la luz no toca el surco", an, 2.0))
    h.nota((xr - 3, yt + 4.5), (xr + 3, yt + 5.5), "", 2.0, lineas=cortar("la cera, 1885; leída en 2013", an, 2.0))


def mec_14(h, x0, y0, x1, y1):
    """El gesto como signo: la celda 56, con el ¶ que no se dibuja."""
    alto = min(y1 - y0 - 4, 30.0)
    ancho = alto * 0.84
    cx0, cy0 = x0 + 5, y0 + 2
    celda_abierta(h, cx0, cy0, cx0 + ancho, cy0 + alto, "celda", capa="fondo", w=0.4)
    h.texto(cx0 + 1.2, cy0 + 3.0, "56", 1.8, color=GRIS)
    h.texto(cx0 + ancho / 2, cy0 + alto * 0.66, "¶", alto * 0.55, "middle", familia=SERIF, peso=300, color=FILETE)
    xt = cx0 + ancho + 5
    h.nota((cx0 + ancho * 0.62, cy0 + alto * 0.42), (xt, cy0 + 3.5), "no se dibuja: se hace", 2.0)
    yy = renglones(h, xt + 2.2, cy0 + 8.6, ["con los dedos, sin punzón", "(Acción 7); la forma la decide",
                                           "quien la hace"], 2.0, color=GRIS)
    h.texto(xt + 2.2, yy + 1.6, "Bulwer, 1644: el gesto es un signo", 1.9)
    h.texto(xt + 2.2, yy + 4.4, "Bonet, 1620: un alfabeto de una mano", 1.9)


def vasija(h, cx, ytop, ancho, alto, tipo="contorno", w=0.4, color=None):
    """La vasija de Contenida, en corte: paredes que bajan a un fondo plano que se abre abajo."""
    g = min(1.6, ancho * 0.14)
    extra = {"w": w}
    if color:
        extra["color"] = color
    for s in (-1, 1):
        pts = [(cx + s * ancho / 2, ytop), (cx + s * ancho / 2, ytop + alto * 0.45)]
        for a in np.linspace(0, math.pi / 2, 14)[1:]:
            pts.append((cx + s * (ancho / 2 - ancho * 0.18 * (1 - math.cos(a))), ytop + alto * 0.45 +
                        alto * 0.55 * math.sin(a)))
        pts.append((cx + s * g / 2, ytop + alto))
        h.poli(pts, tipo, "cuerpo", **extra)


def mec_15(h, x0, y0, x1, y1):
    """Sustitución de forma: arriba, una cosa distinta por letra (1482); abajo, la misma vasija para todas."""
    cw, ch, sep = 11.5, 11.5, 2.2
    xr = x0 + 25
    ya, yb = y0 + 2, y0 + 2 + ch + 4
    h.texto(x0 + 2, ya + 5.0, "1482: una cosa", 1.9, color=GRIS)
    h.texto(x0 + 2, ya + 7.8, "por letra", 1.9, color=GRIS)
    h.texto(x0 + 2, yb + 5.0, "Contenida: la", 1.9)
    h.texto(x0 + 2, yb + 7.8, "misma vasija", 1.9)
    for i, (L, l) in enumerate((("A", "a"), ("B", "b"), ("C", "c"))):
        xx = xr + i * (cw + sep)
        for yy in (ya, yb):
            h.add("fondo", f'<rect x="{f(xx)}" y="{f(yy)}" width="{f(cw)}" height="{f(ch)}" {estilo("fina")}/>')
        h.texto(xx + 1.0, ya + 2.8, L, 2.2, familia=SERIF, color=GRIS)
        h.texto(xx + 1.0, yb + 2.8, l, 2.2, familia=SERIF)
        cx, cy = xx + cw / 2, ya + ch / 2 + 0.8
        if i == 0:
            h.poli([(cx - 3.4, cy + 4.2), (cx, cy - 4.2), (cx + 3.4, cy + 4.2)], "comparar", "cuerpo")
            for yy_ in (cy - 1.2, cy + 1.2, cy + 3.4):
                d = 3.4 * (yy_ - (cy - 4.2)) / 8.4
                h.linea((cx - d, yy_), (cx + d, yy_), "comparar", "cuerpo")
        elif i == 1:
            h.circulo((cx - 0.8, cy + 1.6), 2.9, "comparar", "cuerpo")
            h.linea((cx + 1.2, cy - 0.4), (cx + 4.2, cy - 4.6), "comparar", "cuerpo")
        else:
            pts = [(cx + 3.6 * math.cos(a), cy - 0.6 + 4.2 * math.sin(a)) for a in np.linspace(-0.9, math.pi + 0.9, 30)]
            h.poli(pts, "comparar", "cuerpo")
        vasija(h, xx + cw / 2, yb + 3.4, cw * 0.56, ch * 0.62)
    h.texto(x0 + 2, yb + ch + 4.2, "a trazos, la forma que no se elige; dada vuelta, todas son una", 1.9, color=GRIS)


def mec_16(h, x0, y0, x1, y1):
    """Metáfora material, en alzado: lo blando como ornamento (a trazos) y lo blando que sale del agua."""
    cx, cy = x0 + 13, y0 + 12
    pts = [(cx + (1.0 + 1.25 * a) * math.cos(a * 1.0), cy + (1.0 + 1.25 * a) * math.sin(a * 1.0) * 0.9)
           for a in np.linspace(0, 3.3 * math.pi, 120)]
    h.poli(pts, "comparar", "cuerpo")
    yl = y0 + 27
    h.texto(x0 + 2, yl, "h. 1650: lo blando,", 1.9, color=GRIS)
    h.texto(x0 + 2, yl + 2.8, "como ornamento", 1.9, color=GRIS)
    # el terminal que mira abajo, con su gota
    xt0, xt1, yt = x0 + 36, x0 + 56, y0 + 8
    h.add("cuerpo", f'<path d="M{f(xt0)},{f(yt)} H{f(xt1)} V{f(yt + 4.0)} H{f(xt0)}" fill="url(#metal)" '
                    f'{estilo("contorno", w=0.4)[11:]}/>')
    g = gota(xt1 - 2.4, yt + 4.0 + 2.2 * 1.9 - 0.1, 2.2)
    h.relleno("M" + " L".join(f"{f(a)},{f(b)}" for a, b in g) + " Z", "url(#metal)", "cuerpo")
    h.poli(g, "contorno", "cuerpo", cerrado=True, w=0.4)
    h.gravedad(xt1 + 9, yt + 9, 3.2)
    h.texto(xt0, yl, "solo gotea lo que mira", 1.9)
    h.texto(xt0, yl + 2.8, "abajo (P-07 · 2)", 1.9)


def mec_17(h, x0, y0, x1, y1):
    mec_no(h, x0, y0, x1, y1, "Los signos no se personifican; la máquina no habla.",
           ["Kempelen, 1791: la máquina que habla", "Punctuation Personified, 1824"])


def mec_7(h, x0, y0, x1, y1):
    mec_no(h, x0, y0, x1, y1, "La obra ya pone el cuerpo, y el de Rebeca no se usa (06, §6.1).",
           ["The Human Alphabet, 1534-1789: la vecina opuesta"])


MECANISMOS = {1: mec_1, 2: mec_2, 3: mec_3, 4: mec_4, 5: mec_5, 6: mec_6, 7: mec_7, 8: mec_8, 9: mec_9,
              10: mec_10, 11: mec_11, 12: mec_12, 13: mec_13, 14: mec_14, 15: mec_15, 16: mec_16, 17: mec_17}


def detalles(h, cajas):
    """Cada caja: (técnica, x0, y0, x1, y1). Arriba, el título; abajo, el mecanismo."""
    for n, x0, y0, x1, y1 in cajas:
        yy = titulo_tecnica(h, x0, y0, n, x1 - x0)
        MECANISMOS[n](h, x0, yy, x1, y1)


# ---------------------------------------------------------------- R-03 a R-06: las cuatro operaciones

def r03(h):
    y = cabeza_operacion(h, "diferenciar") + 2
    xa, xb = X0 + 1, X1 - 1
    xm = (xa + xb) / 2
    claves = T.de_la_operacion("diferenciar")
    hd = min(62, (Y1 - 1 - y - alto_rejilla(claves, xa, xb, 3) - 4 - 7) / 2)
    detalles(h, [(1, xa, y, xm - 3, y + hd), (2, xm + 3, y, xb, y + hd),
                 (3, xa, y + hd + 4, xm - 3, y + 2 * hd + 4), (4, xm + 3, y + hd + 4, xb, y + 2 * hd + 4)])
    rejilla_fichas(h, claves, xa, y + 2 * hd + 11, xb, 3)
    h.columna(TEXTOS["R-03"] + cruces("diferenciar"))


def r04(h):
    y = cabeza_operacion(h, "agrupar") + 2
    xa, xb = X0 + 1, X1 - 1
    xm = (xa + xb) / 2
    claves = T.de_la_operacion("agrupar")
    tira = 27
    hd = min(66, Y1 - 1 - y - alto_rejilla(claves, xa, xb, 3) - 4 - tira - 7)
    detalles(h, [(5, xa, y, xm - 3, y + hd), (6, xm + 3, y, xb, y + hd), (7, xa, y + hd + 4, xb, y + hd + 4 + tira)])
    rejilla_fichas(h, claves, xa, y + hd + tira + 11, xb, 3)
    h.columna(TEXTOS["R-04"] + cruces("agrupar"))


def r05(h):
    y = cabeza_operacion(h, "secuenciar") + 2
    xa, xb = X0 + 1, X1 - 1
    xm = (xa + xb) / 2
    claves = T.de_la_operacion("secuenciar")
    hd = min(64, (Y1 - 1 - y - alto_rejilla(claves, xa, xb, 4) - 4 - 7) / 2)
    detalles(h, [(8, xa, y, xm - 3, y + hd), (9, xm + 3, y, xb, y + hd),
                 (10, xa, y + hd + 4, xm - 3, y + 2 * hd + 4), (11, xm + 3, y + hd + 4, xb, y + 2 * hd + 4)])
    rejilla_fichas(h, claves, xa, y + 2 * hd + 11, xb, 4)
    h.columna(TEXTOS["R-05"] + cruces("secuenciar"))


def r06(h):
    y = cabeza_operacion(h, "inferir") + 2
    xa, xb = X0 + 1, X1 - 1
    w = (xb - xa - 2 * 5) / 3
    claves = T.de_la_operacion("inferir")
    hd = min(60, (Y1 - 1 - y - alto_rejilla(claves, xa, xb, 3, 3.0, False) - 3 - 7) / 2)
    cajas = []
    for i, n in enumerate((12, 13, 14, 15, 16, 17)):
        fila, col = divmod(i, 3)
        x0 = xa + col * (w + 5)
        y0 = y + fila * (hd + 3)
        cajas.append((n, x0, y0, x0 + w, y0 + hd))
    detalles(h, cajas)
    rejilla_fichas(h, claves, xa, y + 2 * hd + 10, xb, 3, sep=3.0, rima=False)
    h.columna(TEXTOS["R-06"] + cruces("inferir"))


# ---------------------------------------------------------------- R-07: del encargo a la referencia

def r07(h):
    x = X0 + 2
    h.llamada(x + 4.5, Y0 + 6.5, 1, "R-07", "DEL ENCARGO A LA REFERENCIA · CORTE",
              "cada columna baja de un verso, o de una decisión de la obra, hasta lo que cae en Contenida")
    xl = x + 27
    n = len(T.ENCARGOS) + 1
    cw = (X1 - 1 - xl) / n
    niveles = [("el encargo", None, Y0 + 19), ("operación", "01", Y0 + 62), ("dominio", "02", Y0 + 82),
               ("técnica", "03", Y0 + 97), ("referencias", "04", Y0 + 113), ("cae en", "±0", Y0 + 152)]
    for nombre, cod, yy in niveles:
        if cod:
            nivel(h, x + 2, yy, cod, 2.2, largo=12)
            h.texto(x + 2, yy + 3.6, nombre, 2.1)
        else:
            h.texto(x + 2, yy + 2.4, nombre, 2.1)
    y_op, y_dom, y_tec, y_ref, y_cae = (n_[2] for n_ in niveles[1:])
    h.linea((x, y_cae), (X1 - 1, y_cae), "linea", "fondo")
    h.texto(X1 - 1, y_cae - 1.2, "±0 · Contenida", 1.9, "end", color=GRIS)
    for i in range(n):
        cx0 = xl + i * cw
        xc = cx0 + 2.4
        ancho = cw - 4.8
        vacia = i == len(T.ENCARGOS)
        E = None if vacia else T.ENCARGOS[i]
        xbaj = cx0 + 1.0
        # la bajante: del encargo al fondo, con la gravedad
        tipo = "contorno_r" if vacia else "contorno"
        h.linea((xbaj, Y0 + 44), (xbaj, y_cae - 2.0), tipo, "cotas", w=0.35)
        h.flecha((xbaj, y_cae), (xbaj, y_cae - 3.0), largo=2.0, ancho=0.75, color=VIOLETA if vacia else TINTA)
        if vacia:
            h.texto(xc, Y0 + 21.4, "tu encargo", 2.6, familia=SERIF, cursiva=True, peso=400, color=VIOLETA)
            for yy in (Y0 + 28, Y0 + 33, Y0 + 38):
                h.linea((xc, yy), (xc + ancho, yy), "contorno_r", "textos", w=0.28)
            for yy in (y_op, y_dom, y_tec):
                h.linea((xc, yy + 2.5), (xc + ancho, yy + 2.5), "contorno_r", "textos", w=0.28)
            punteado(h, xc, y_ref - 2.6, xc + ancho, y_ref + 6, "textos")
            h.linea((xc, y_cae + 6.5), (xc + ancho, y_cae + 6.5), "contorno_r", "textos", w=0.28)
            h.texto(xc, y_cae + 12.0, "la máquina propone;", 1.9, color=GRIS)
            h.texto(xc, y_cae + 14.6, "la mano completa", 1.9, color=GRIS)
            continue
        yy = renglones(h, xc, Y0 + 21.4, E["encargo"].split("\n"), 2.75, SERIF, 400, True, inter=1.22)
        renglones(h, xc, yy + 0.8, cortar(f"de: {E['de']}", ancho, 1.8), 1.8, color=GRIS)
        O = T.OPERACIONES[E["op"]]
        marca_operacion(h, xc, y_op - 4.6, O["i"], 3.6)
        h.texto(xc, y_op + 2.4, O["nombre"].lower(), 2.3)
        h.texto(xc, y_op + 5.2, O["figura"].lower(), 1.8, color=GRIS)
        h.texto(xc, y_dom, T.DOMINIOS[E["dom"]]["nombre"], 2.7, familia=SERIF, peso=400)
        t = T.TECNICA[E["tec"]]
        marca_tecnica(h, xc + 2.2, y_tec - 1.2, t["n"], 5.0)
        renglones(h, xc + 6.0, y_tec, cortar(t["nombre"], ancho - 6, 2.5, SERIF, 500), 2.5, SERIF, 500, inter=1.18)
        yr = y_ref
        for k in E["refs"]:
            R = T.REFERENCIAS[k]
            lineas = cortar(R["corto"], ancho - 3.0, 2.4, SERIF, 400)
            alto = len(lineas) * 2.4 * 1.2 + 2.0
            if R["mirada"]:
                h.add("textos", f'<rect x="{f(xc)}" y="{f(yr - 2.8)}" width="{f(ancho)}" height="{f(alto)}" '
                                f'{estilo("celda", w=0.25)}/>')
            else:
                punteado(h, xc, yr - 2.8, xc + ancho, yr - 2.8 + alto, "textos")
            renglones(h, xc + 1.4, yr, lineas, 2.4, SERIF, 400, inter=1.2)
            yr += alto + 2.0
        renglones(h, xc, y_cae + 4.6, cortar(E["cae"], ancho, 2.2, SERIF, 400), 2.2, SERIF, 400, inter=1.25)
    h.gravedad(x + 9, y_cae - 16, 4.2)
    # los encargos que ninguna referencia contesta todavía
    yv = y_cae + 30
    h.llamada(x + 4.5, yv, 2, "R-07", "ENCARGOS SIN REFERENCIA, TODAVÍA",
              "la obra los pide; ningún archivo los contestó: a puntos, para la mano")
    m = len(T.ENCARGOS_ABIERTOS)
    sep = 4.0
    ew = (X1 - 1 - x - sep * (m - 1)) / m
    ye = yv + 9.5
    for i, E in enumerate(T.ENCARGOS_ABIERTOS):
        ex0 = x + i * (ew + sep)
        yy = renglones(h, ex0 + 2.0, ye + 4.4, cortar(E["encargo"].replace(" / ", " "), ew - 4, 2.6, SERIF, 400, True),
                       2.6, SERIF, 400, True, inter=1.2)
        O = T.OPERACIONES[E["op"]]
        marca_operacion(h, ex0 + 2.0, yy - 0.6, O["i"], 3.0)
        h.texto(ex0 + 16.6, yy + 1.8, O["nombre"].lower(), 2.0)
        yy = renglones(h, ex0 + 2.0, yy + 6.6, cortar(E["tecnica"], ew - 4, 2.0), 2.0, inter=1.3)
        yy = renglones(h, ex0 + 2.0, yy + 0.6, cortar(f"cae en: {E['cae']}", ew - 4, 2.0), 2.0, color=GRIS, inter=1.3)
        notdef(h, ex0 + 2.0, yy + 0.4, 4.4, 5.4, capa="textos", w=0.25)
        h.texto(ex0 + 8.0, yy + 4.0, "referencia: ninguna, todavía", 2.0, color=VIOLETA)
        celda_abierta(h, ex0, ye, ex0 + ew, yy + 8.0, "contorno_r", capa="fondo", w=0.35)
    h.columna(TEXTOS["R-07"])


# ---------------------------------------------------------------- R-08: lo que queda afuera

def r08(h):
    x = X0 + 2
    h.llamada(x + 4.5, Y0 + 6.5, 1, "R-08", "LO QUE SE DEJÓ AFUERA, A PROPÓSITO", "cada cosa con su corte y su razón")
    y = Y0 + 19
    for nombre, razon in T.AFUERA:
        h.texto(x, y, nombre, 2.9, familia=SERIF, peso=400)
        xx = x + 92
        hilo(h, (xx, y - 0.9), (xx + 9, y - 0.9), False, "comparar", GRIS, "textos")
        h.texto(xx + 12, y, razon, 2.2, color=GRIS)
        h.linea((x, y + 2.0), (X1 - 1, y + 2.0), "fina", "textos")
        y += 6.6
    # lo que no se encontró
    y += 6
    h.llamada(x + 4.5, y, 2, "R-08", "LO QUE SE BUSCÓ Y NO APARECIÓ", "una celda vacía cada uno; a puntos, dónde caería")
    y += 9
    n = len(T.NO_ENCONTRADO)
    paso = (X1 - 1 - x) / n
    cw, ch = paso * 0.56, paso * 0.66
    for i, (que, col, tec) in enumerate(T.NO_ENCONTRADO):
        cx = x + paso * (i + 0.5)
        notdef(h, cx - cw / 2, y, cw, ch, capa="fondo", w=0.35)
        yy = renglones(h, cx, y + ch + 4.0, cortar(que, paso - 2.0, 1.95), 1.95, ancla="middle", inter=1.25)
        marca_tecnica(h, cx - 4.0, yy + 1.0, tec, 4.0, violeta=True)
        h.texto(cx - 1.0, yy + 1.8, f"→ {col}", 2.0, color=VIOLETA)
    y += ch + 22
    # dónde seguir buscando
    h.llamada(x + 4.5, y, 3, "R-08", "DÓNDE SEGUIR BUSCANDO", "los archivos: queda el enlace, nada se baja")
    y += 9.5
    for nombre, que, url in T.ARCHIVOS:
        enlace(h, url, lambda nombre=nombre, y=y: h.texto(x, y, nombre, 2.7, familia=SERIF, peso=400))
        h.texto(x + 78, y, que, 2.1)
        corto = url.replace("https://", "").rstrip("/")
        enlace(h, url, lambda corto=corto, y=y: h.texto(X1 - 1, y, corto, 1.8, "end", color=GRIS))
        h.linea((x, y + 1.9), (X1 - 1, y + 1.9), "fina", "textos")
        y += 6.0
    # pendientes
    y += 6
    h.llamada(x + 4.5, y, 4, "R-08", "PENDIENTES", "para la mano: la casilla, con fecha")
    y += 9.5
    for p in T.PENDIENTES:
        casilla(h, x, y - 2.3, False)
        y = h.parrafo(x + 5, y, X1 - 1 - x - 5, p, 2.45, inter=1.3) + 1.2
    # cómo entra una referencia nueva
    y += 7
    h.llamada(x + 4.5, y, 5, "R-08", "CÓMO ENTRA UNA REFERENCIA NUEVA",
              "los pasos del reel, a la medida de Contenida")
    y += 9.5
    m = len(T.PASOS)
    sep = 5.0
    pw = (X1 - 1 - x - sep * (m - 1)) / m
    altos = [len(cortar(p_, pw - 4, 2.4, SERIF, 400)) for p_ in T.PASOS]
    ph = max(altos) * 2.4 * 1.22 + 9.0
    for i, p_ in enumerate(T.PASOS):
        px0 = x + i * (pw + sep)
        celda_abierta(h, px0, y, px0 + pw, y + ph, "celda", capa="fondo", w=0.3)
        h.texto(px0 + 2.0, y + 4.4, f"{i + 1:02d}", 2.4, peso=700)
        renglones(h, px0 + 2.0, y + 8.6, cortar(p_, pw - 4, 2.4, SERIF, 400), 2.4, SERIF, 400, inter=1.22)
        if i:
            h.linea((px0 - sep + 0.6, y + ph / 2), (px0 - 1.0, y + ph / 2), "cota", "textos")
            h.flecha((px0 - 0.6, y + ph / 2), (px0 - 2.8, y + ph / 2), largo=1.5, ancho=0.55, capa="textos")
    y += ph
    if y > Y1:
        print(f"  ! R-08: se pasa {y - Y1:.1f} mm")
    por_columna = {}
    for que, col, _n in T.NO_ENCONTRADO:
        por_columna.setdefault(col, []).append(que)
    nombres = {c: nom for c, nom, _ in T.COLUMNAS}
    orden = sorted(por_columna.items(), key=lambda kv: -len(kv[1]))
    partes = [f"{len(v)} en {c} ({nombres[c]})" for c, v in orden]
    h.columna(TEXTOS["R-08"] + [
        ("titulo", "Lo que dice lo que falta"),
        ("p", f"De las {len(T.NO_ENCONTRADO)} búsquedas que no dieron nada, caerían {', '.join(partes)}. La voz y el "
              "calco son los que más esperan: ahí conviene seguir buscando, y en la cinta, que no tiene ninguna.")])


# ---------------------------------------------------------------- R-09: el atlas

DOMINIOS_ATLAS = ["materia", "estructura", "sentido", "mano", "tiempo", "huella", "procedencia"]
CARPETA_IMAGENES = AQUI / "imagenes"
ARCHIVO_DE = {"pdimagearchive.org": "Public Domain Image Archive", "publicdomainreview.org": "The Public Domain Review",
              "wellcomecollection.org": "Wellcome Collection", "en.wikipedia.org": "Wikipedia y Wikimedia Commons",
              "commons.wikimedia.org": "Wikimedia Commons", "www.getty.edu": "Getty Museum",
              "www.firstsounds.org": "First Sounds", "insider.si.edu": "Smithsonian"}


def anio(k):
    m = re.search(r"\d{4}", T.REFERENCIAS[k]["anio"])
    return int(m.group(0)) if m else 0


def archivo_imagen(k):
    for ext in ("jpg", "jpeg", "png", "webp"):
        ruta = CARPETA_IMAGENES / f"{k}.{ext}"
        if ruta.exists():
            return ruta
    return None


def en_tinta(ruta, ancho_mm, alto_mm, ppp=300, girar=0):
    """La imagen, en tinta sobre papel, como el resto de las láminas (el color es material: 03, §3.9), reducida a
    su celda y metida en el SVG: la lámina no depende de la carpeta imagenes/, que no se sube. Devuelve también
    su proporción (alto / ancho)."""
    from PIL import Image, ImageOps
    im = Image.open(ruta).convert("L")
    if girar:
        im = im.rotate(-girar, expand=True)        # en el sentido del reloj
    im.thumbnail((int(ancho_mm / 25.4 * ppp), int(alto_mm / 25.4 * ppp)))
    im = ImageOps.colorize(ImageOps.autocontrast(im, cutoff=1), black=TINTA, white=PAPEL)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84)
    return base64.b64encode(buf.getvalue()).decode("ascii"), im.height / im.width


def celda_atlas(h, k, x, y, w, alto):
    """Una referencia en su celda: arriba su técnica, su nombre y su archivo; abajo, su imagen. Se abre abajo."""
    R, I = T.REFERENCIAS[k], T.IMAGENES[k]
    pad = 1.2
    t = T.TECNICA[R["tec"][0]]
    marca_tecnica(h, x + pad + 1.75, y + pad + 2.3, t["n"], 4.2, no=t["estado"] == "no")
    xt = x + pad + 4.9
    lineas = cortar(R["corto"], x + w - pad - xt, 2.2, SERIF, 400)[:2]
    yy = renglones(h, xt, y + pad + 2.5, lineas, 2.2, SERIF, 400, inter=1.12)
    archivo = ARCHIVO_DE.get(I["pagina"].split("/")[2], I["pagina"].split("/")[2])
    ya = max(yy, y + pad + 5.2) + 0.2
    enlace(h, I["pagina"], lambda: h.texto(xt, ya, archivo, 1.4, color=GRIS))
    subrayado(h, xt, ya, MEDIR.ancho(archivo, 1.4, MONO), GRIS)
    # la imagen
    ix0, iy0 = x + pad, ya + 1.6
    iw, ih = w - 2 * pad, y + alto - pad - iy0
    ruta = archivo_imagen(k)
    if ruta:
        datos, proporcion = en_tinta(ruta, iw, ih, girar=I.get("girar", 0))
        h.add("cuerpo", f'<image x="{f(ix0)}" y="{f(iy0)}" width="{f(iw)}" height="{f(ih)}" '
                        f'preserveAspectRatio="xMidYMax meet" href="data:image/jpeg;base64,{datos}"/>')
        if "revisar" in I["licencia"]:
            # sobre la imagen, si queda lugar; si no, en su pie
            arriba = y + alto - pad - min(ih, iw * proporcion)
            yr = arriba - 0.9 if arriba - iy0 > 3.0 else y + alto - pad - 0.8
            h.texto(x + w / 2, yr, "licencia por revisar", 1.3, "middle", color=VIOLETA, fondo=True)
    elif not I.get("descarga", True):
        renglones(h, x + w / 2, iy0 + ih / 2 - 1.0, ["solo enlace:"] + cortar("es una foto de hoy, no de dominio "
                                                                          "público", iw - 2, 1.4),
                  1.4, ancla="middle", color=GRIS, inter=1.3)
    else:
        h.texto(x + w / 2, iy0 + ih / 2, "imagen sin bajar", 1.5, "middle", color=VIOLETA)
        h.texto(x + w / 2, iy0 + ih / 2 + 2.4, f"imagenes/{k}.jpg", 1.3, "middle", color=GRIS)
    if R["mirada"]:
        celda_abierta(h, x, y, x + w, y + alto, "celda", capa="textos", w=0.3)
    else:
        celda_abierta(h, x, y, x + w, y + alto, "contorno_r", capa="textos", w=0.35)


def r09(h):
    XA, XB = X0 + 3, 402.0
    h.texto(XA, Y0 + 10, "el atlas de las referencias", 9.0, familia=SERIF, peso=300)
    h.texto(XA, Y0 + 16.2, "arriba, el dominio; en el medio, cada obra en su celda, de la más antigua a la más nueva; "
                           "abajo, la acción del taller donde cae. Cada celda se vacía por su desagüe.", 2.2,
            color=GRIS)
    # las columnas: un dominio cada una
    refs = {d: sorted((k for k in T.REFERENCIAS if T.TECNICA[T.REFERENCIAS[k]["tec"][0]]["dom"] == d),
                      key=lambda k: (anio(k), k)) for d in DOMINIOS_ATLAS}
    ncol = {d: 2 if len(refs[d]) > 3 else 1 for d in DOMINIOS_ATLAS}
    gap_dom, gap_in = 7.0, 4.6
    cw = (XB - XA - gap_dom * (len(DOMINIOS_ATLAS) - 1) - gap_in * sum(n - 1 for n in ncol.values())) / \
        sum(ncol.values())
    alto, paso = 32.0, 40.0
    yh, yg = Y0 + 22, Y0 + 38
    columnas = []          # (x0, x1) de cada columna de celdas, de izquierda a derecha
    celdas = {}            # clave → (x, y, columna, ¿es la última de su columna?)
    x = XA
    for d in DOMINIOS_ATLAS:
        D = T.DOMINIOS[d]
        ancho = ncol[d] * cw + (ncol[d] - 1) * gap_in
        murray = "se suma: el reel no lo trae" if D["murray"] == "—" else D["murray"].lower()
        h.texto(x, yh + 3.0, murray, 1.75, color=VIOLETA if D["estado"] == "suma" else GRIS)
        h.texto(x, yh + 8.6, D["nombre"], 3.6, familia=SERIF, peso=400)
        simbolo(h, x + ancho - 5.0, yh + 2.4, D["estado"], 5.0)
        h.linea((x, yh + 11.2), (x + ancho, yh + 11.2), "cota", "textos")
        for xx in (x, x + ancho):
            h.linea((xx, yh + 10.0), (xx, yh + 12.4), "cota", "textos")
        primera = len(columnas)
        for j in range(ncol[d]):
            columnas.append((x + j * (cw + gap_in), x + j * (cw + gap_in) + cw))
        for i, k in enumerate(refs[d]):
            fila, col = divmod(i, ncol[d])
            celdas[k] = (columnas[primera + col][0], yg + fila * paso, primera + col)
        x += ancho + gap_dom
    fondo_de = {}
    for cx, cy, c in celdas.values():
        fondo_de[c] = max(fondo_de.get(c, cy), cy)
    celdas = {k: (cx, cy, c, cy == fondo_de[c]) for k, (cx, cy, c) in celdas.items()}
    yfin = yg + 2 * paso + alto + 2.2           # donde terminan las celdas y empieza la bajada
    # las bocas: la cadena del taller
    n = len(T.COLUMNAS)
    yn = 208.0
    xs = [XA + 4 + i * (XB - XA - 8) / (n - 1) for i in range(n)]
    cuenta = cuenta_columnas()
    # las líneas: de cada celda, por su desagüe, a cada acción donde cae
    canales = {}           # canal (entre columnas) → líneas que bajan por él
    lineas = []
    for k, (cx, cy, c, ultima) in celdas.items():
        destinos = [i for i, (col, *_r) in enumerate(T.COLUMNAS) if col in T.columnas_de(k)]
        for j, i in enumerate(destinos):
            L = dict(k=k, salida=(cx + cw / 2 + (j - (len(destinos) - 1) / 2) * 0.7, cy + alto), boca=i,
                     no=T.COLUMNAS[i][0] == "no", y=cy, recta=ultima, orden=j)
            if not ultima:
                lado = -1 if xs[i] < cx + cw / 2 else 1
                L["canal"] = (c, lado)
                canales.setdefault((c, lado), []).append(L)
            lineas.append(L)

    def x_canal(c, lado):
        x0, x1 = columnas[c]
        if lado < 0:
            return (columnas[c - 1][1] + x0) / 2 if c else x0 - 2.0
        return (x1 + columnas[c + 1][0]) / 2 if c + 1 < len(columnas) else x1 + 2.0

    # en cada canal, las que entran desde más abajo van más cerca de su celda: así no se cruzan
    por_canal = {}
    for (c, lado), Ls in canales.items():
        g = x_canal(c, lado)
        por_canal.setdefault(round(g, 2), []).extend((lado, L) for L in Ls)
    for g, items in por_canal.items():
        desde_izq = sorted((L for lado, L in items if lado > 0), key=lambda L: (-L["y"], L["orden"]))
        desde_der = sorted((L for lado, L in items if lado < 0), key=lambda L: (L["y"], -L["orden"]))
        orden = desde_izq + desde_der
        for m, L in enumerate(orden):
            L["gx"] = g + (m - (len(orden) - 1) / 2) * 0.6
    for L in lineas:
        sx, sy = L["salida"]
        ox, oy = xs[L["boca"]], yn - 2.6
        if L["recta"]:
            pts = [(sx, sy), (sx, yfin)]
            x0_, y0_ = sx, yfin
        else:
            yv = sy + 2.4 + L["orden"] * 0.6
            pts = [(sx, sy), (sx, yv), (L["gx"], yv), (L["gx"], yfin)]
            x0_, y0_ = L["gx"], yfin
        dy = oy - y0_
        curva = [(x0_ + (ox - x0_) * (3 * u * u - 2 * u ** 3), y0_ + dy * u) for u in np.linspace(0, 1, 40)]
        extra = dict(color=GRIS, w=0.17)
        if L["no"]:
            extra.update(color=GRIS2, dash="1.4 0.5 0.3 0.5")
        h.poli(pts + curva[1:], "contorno", "aux", **extra)
        if L["no"]:
            h.linea((ox - 1.2, oy), (ox + 1.2, oy), "cota", "aux", w=0.35, color=GRIS2)
        else:
            h.punto((ox, oy), 0.42, GRIS, "aux")
    # las celdas, encima de las líneas
    for k, (cx, cy, c, ultima) in celdas.items():
        celda_atlas(h, k, cx, cy, cw, alto)
    # la cadena del taller
    for i, (col, nombre, cuad) in enumerate(T.COLUMNAS):
        xx = xs[i]
        if cuenta[col]:
            h.circulo((xx, yn), 2.5, "filete", "textos", relleno=PAPEL)
            h.texto(xx, yn + 0.8, str(cuenta[col]), 2.2, "middle", peso=700)
        else:
            notdef(h, xx - 2.1, yn - 2.6, 4.2, 5.2, capa="textos", w=0.25)
        h.texto(xx, yn + 6.0, col, 1.95, "middle", peso=700)
        for j, ln in enumerate(cortar(nombre, 19, 1.7)):
            h.texto(xx, yn + 8.4 + j * 2.1, ln, 1.7, "middle", color=GRIS)
    for cuad, nombre in T.CUADERNOS.items():
        idx = [i for i, c in enumerate(T.COLUMNAS) if c[2] == cuad]
        a, b = xs[idx[0]] - 6, xs[idx[-1]] + 6
        h.linea((a, yn + 13.6), (b, yn + 13.6), "cota", "textos")
        for xx in (a, b):
            h.linea((xx, yn + 12.4), (xx, yn + 13.6), "cota", "textos")
        h.texto((a + b) / 2, yn + 16.4, f"cuaderno {cuad} · {nombre}", 1.8, "middle", color=GRIS)
    # cómo se lee y las imágenes
    yl = 238.0
    titulo_seccion(h, XA, yl, "Cómo se lee", 108)
    yy = yl + 6.2
    muestras = [("celda", "en línea continua: ya la miraste en su archivo"),
                ("contorno_r", "a puntos y en violeta: nadie la miró todavía"),
                ("toma", "cae en esa acción del taller: se toma"),
                ("no", "cae en lo que no se hace (06, §6.4)"),
                ("notdef", "una acción sin ninguna referencia"),
                ("tecnica", "la técnica de la obra (R-00)")]
    for tipo, txt in muestras:
        if tipo in ("celda", "contorno_r"):
            celda_abierta(h, XA + 3, yy - 3.4, XA + 9.5, yy + 0.9, tipo, capa="textos", w=0.3)
        elif tipo == "toma":
            hilo(h, (XA + 1, yy - 1.2), (XA + 11, yy - 1.2), True, color=GRIS, capa="textos", w=0.17)
        elif tipo == "no":
            hilo(h, (XA + 1, yy - 1.2), (XA + 11, yy - 1.2), False, "rotura", GRIS, "textos", w=0.17)
        elif tipo == "notdef":
            notdef(h, XA + 4.2, yy - 3.6, 3.8, 4.6, capa="textos", w=0.25)
        else:
            marca_tecnica(h, XA + 6.2, yy - 1.3, 5, 4.2)
        h.texto(XA + 15, yy, txt, 2.05)
        yy += 6.6
    xi = XA + 118
    titulo_seccion(h, xi, yl, "Las imágenes", 278 - xi)
    faltan = [k for k in T.REFERENCIAS if T.IMAGENES[k].get("descarga", True) and not archivo_imagen(k)]
    textos = ["**Solo de dominio público,** cada una con su archivo, enlazado en su celda. Van en tinta sobre papel, "
              "como el resto de las láminas: el color es material (03, §3.9). Las fotos de hoy quedan como enlace: "
              + "; ".join(f"{a}, {q}" for a, q in T.SOLO_ENLACE) + "."]
    if faltan:
        textos.append(f"**Faltan {len(faltan)} imágenes.** Cada celda vacía espera la suya: las baja "
                      "descargar_imagenes.py desde su página, o se ponen a mano en imagenes/, con el nombre de su "
                      "clave. Esa carpeta no entra en el repositorio (06, §6.4).")
    else:
        registro = CARPETA_IMAGENES / "fuentes.json"
        fechas = sorted({v["fecha"] for v in json.loads(registro.read_text(encoding="utf8")).values()}) \
            if registro.exists() else []
        cuando = ""
        if fechas:
            a, b = (datetime.date.fromisoformat(x) for x in (fechas[0], fechas[-1]))
            cuando = f" el {b:%d.%m.%Y}" if a == b else f" entre el {a.day} y el {b:%d.%m.%Y}"
        textos.append(f"**Se bajaron{cuando},** con descargar_imagenes.py, cada una desde su archivo; "
                      "imagenes/fuentes.json anota de dónde salió y con qué licencia. Esa carpeta no entra en el "
                      "repositorio (06, §6.4): la lámina las lleva reducidas a su celda.")
    for k in T.REFERENCIAS:
        lic = T.IMAGENES[k]["licencia"]
        if "revisar:" in lic and archivo_imagen(k):
            textos.append(f"**Por revisar,** la licencia de {T.REFERENCIAS[k]['corto'].split(',')[0]}: "
                          f"{lic.split('revisar:', 1)[1].strip()}.")
    yy = yl + 5.6
    for t in textos:
        yy = h.parrafo(xi, yy, 278 - xi, t, 2.3, inter=1.32) + 1.0
    for v in ("Una piscina vacía,", "donde una vez aprendí a flotar,", "ahora aprendo a mirar."):
        h.texto(xi + 3, yy + 1.6, v, 2.5, familia=SERIF, cursiva=True, peso=400)
        yy += 3.3
    if yy > Y1:
        print(f"  ! R-09: el texto se pasa {yy - Y1:.1f} mm")
    print(f"    R-09: {len(celdas)} celdas, {len(lineas)} líneas; faltan {len(faltan)} imágenes")


# ---------------------------------------------------------------- salida

def chrome():
    for c in (os.environ.get("CHROME"), "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
              "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and Path(c).exists():
            return c
    sys.exit("No encuentro Chromium: pon su ruta en la variable CHROME.")


def imprimir(hojas, ruta_pdf):
    """Las láminas en un HTML de páginas A3, y Chromium lo pasa a PDF (los enlaces siguen funcionando)."""
    paginas = "\n".join(f'<div class="hoja">{svg}</div>' for svg in hojas)
    html_ = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Contenida · taxonomía</title>'
             f'<style>@page{{size:420mm 297mm;margin:0}}html,body{{margin:0;padding:0;background:{PAPEL}}}'
             f'.hoja{{width:420mm;height:297mm;overflow:hidden;page-break-after:always;break-after:page}}'
             f'.hoja svg{{display:block;width:420mm;height:297mm}}</style></head><body>{paginas}</body></html>')
    tmp = AQUI / "_imprimir.html"
    tmp.write_text(html_, encoding="utf8")
    ejecutable = chrome()
    modo = [] if ejecutable.endswith("headless_shell") else ["--headless=new"]
    subprocess.run([ejecutable, *modo, "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--virtual-time-budget=8000", f"--print-to-pdf={ruta_pdf}", "--no-pdf-header-footer",
                    tmp.as_uri()], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp.unlink()


def svg_preciso(h, fuentes):
    """El SVG de la hoja, con el texto en posiciones exactas: Chromium redondea los tamaños chicos si no."""
    return h.svg(fuentes).replace("<svg xmlns=", '<svg text-rendering="geometricPrecision" xmlns=', 1)


FUNCIONES = {"R-00": r00, "R-01": r01, "R-02": r02, "R-03": r03, "R-04": r04, "R-05": r05, "R-06": r06,
             "R-07": r07, "R-08": r08, "R-09": r09}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", help="solo esta lámina (R-03, por ejemplo), sin el PDF completo")
    args = ap.parse_args()
    SVG, PNG = AQUI / "svg", AQUI / "png"
    for d in (SVG, PNG):
        d.mkdir(exist_ok=True)
    hojas, hechas = [], []
    for i, (cod, tit, sub, nombre) in enumerate(LAMINAS):
        if args.solo and cod != args.solo:
            continue
        h = Hoja(cod, tit, sub, "sin escala", i + 1, len(LAMINAS), serie=SERIE, fecha=FECHA.get(cod, "17.10.2026"),
                 pie=PIE_ATLAS if cod == "R-09" else PIE, unidades="—", columna=cod != "R-09")
        FUNCIONES[cod](h)
        h.marco()
        (SVG / f"{cod}_{nombre}.svg").write_text(svg_preciso(h, "../../laminas/fuentes"), encoding="utf8")
        hojas.append(svg_preciso(h, "../laminas/fuentes"))
        hechas.append((cod, nombre))
        print(f"{cod}: {tit}")
    ruta_pdf = AQUI / ("contenida_taxonomia.pdf" if not args.solo else f"_{args.solo}.pdf")
    imprimir(hojas, ruta_pdf)
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    doc = fitz.open(ruta_pdf)
    for pag, (cod, nombre) in zip(doc, hechas):
        pag.get_pixmap(dpi=110).save(PNG / f"{cod}_{nombre}.png")
    doc.close()
    if args.solo:
        ruta_pdf.unlink()
        return
    print("listo:", ruta_pdf)


if __name__ == "__main__":
    main()
