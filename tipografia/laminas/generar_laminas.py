"""Láminas de exposición de Contenida: diecisiete láminas 4:3.

Uso (desde la raíz del repositorio, después de simular.py):
    python3 tipografia/laminas/imagenes.py
    python3 tipografia/laminas/generar_laminas.py

Escribe en tipografia/laminas/:
  html/     una página por lámina (y todas.html, para imprimir),
  png/      cada lámina a 2400 × 1800 px,
  contenida_laminas.pdf   las diecisiete, una por página (4:3, 1800 × 1350 pt).

La retícula de las láminas es de 16 × 12 módulos de 150 px, con uno de
margen. Los números salen de las fichas de la simulación.
Necesita Chromium (o Chrome) para pasar el HTML a PNG y a PDF.
"""

import html
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TIPO = AQUI.parent
SIM = TIPO / "simulacion"
HTML, PNG = AQUI / "html", AQUI / "png"
N = 17

FICHAS = json.loads((SIM / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))
DATOS = json.loads((AQUI / "img" / "datos.json").read_text(encoding="utf8"))
CAJA = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
PIE = (TIPO / "textos" / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
RETICULA = json.loads((TIPO / "esquemas" / "celda_medida.json").read_text(encoding="utf8"))
POEMA = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8")

CAPITULOS = {1: "la obra", 2: "el sistema", 3: "el taller simulado", 4: "lo que queda"}
CAPITULO_DE = {2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 4, 17: 4}
SIMULADAS = {1, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16}


# ---------------------------------------------------------------- números

def coma(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def pct(x, d=1):
    return f"{coma(x, d)}\u00a0%"


def media(v):
    return sum(v) / len(v)


def numeros():
    """Los números de las láminas, leídos de las fichas de la simulación."""
    primeras = [f for k, f in FICHAS.items() if k.endswith(".01")]
    por = {e: [f for f in primeras if f["estado"] == e] for e in ("hallada", "reconstruida")}
    todas = list(FICHAS.values())
    n = {}
    n["frotadas_max"] = max(f["frotado"]["legibles"] for f in primeras)
    for e, fs in por.items():
        n[f"frotadas_{e}"] = media([f["frotado"]["legibles"] for f in fs])
        n[f"contraste_{e}"] = media([f["agua"]["contraste_de_la_letra"] for f in fs])
        placas = [f for f in todas if f["estado"] == e]
        n[f"placas_{e}"] = len(placas)
        n[f"roturas_{e}"] = sum(f["placa_"]["roturas"] for f in placas)
    n["placas"] = len(todas)
    n["horas"] = sum(f["placa_"]["minutos"] for f in todas) / 60
    op = [f["pie"]["opinion_pct"] for f in por["hallada"]]
    n["opinion_min"], n["opinion_max"] = min(op), max(op)
    n["desagues"] = sum(f.get("gramatica", {}).get("desagues", 0) for f in primeras)
    n["tramos"] = sum(f.get("cinta", {}).get("tramos", 0) for f in primeras)
    n["pliegues"] = sum(f.get("cinta", {}).get("pliegues", 0) for f in primeras)
    n.update(DATOS)
    return n


NUM = numeros()


def ficha(signo):
    return next(f for k, f in FICHAS.items() if f["signo"] == signo and k.endswith(".01"))


# ---------------------------------------------------------------- piezas

def marca(capitulo):
    """Cuatro celdas de la cabeza del ídolo, una por capítulo, con su desagüe abajo."""
    celdas = []
    for i in range(4):
        x = i * 34
        activa = i + 1 == capitulo
        trazo = "var(--tinta)" if activa else "var(--filete)"
        relleno = "var(--violeta)" if activa else "none"
        celdas.append(
            f'<path d="M{x + 11.5},30 H{x + 1} V1 H{x + 25} V30 H{x + 14.5}" fill="none" stroke="{trazo}" stroke-width="2"/>'
            f'<rect x="{x + 6}" y="6" width="14" height="19" fill="{relleno}" stroke="{trazo}" stroke-width="1.5"/>')
    return f'<svg class="marca" width="{4 * 34}" height="32" viewBox="0 0 {4 * 34} 32">{"".join(celdas)}</svg>'


def b(col, fila, ancho, alto, contenido, clase="", estilo=""):
    """Un bloque sobre la retícula de módulos (14 × 10 dentro del margen).

    Si no llega al borde derecho, deja una junta de 50 px con el bloque que sigue.
    """
    junta = "padding-right:50px;" if col + ancho - 1 < 14 else ""
    return (f'<div class="b {clase}" style="grid-column:{col}/span {ancho};grid-row:{fila}/span {alto};'
            f'{junta}{estilo}">{contenido}</div>')


def fig(src, pie="", clase="", estilo=""):
    leyenda = f"<figcaption>{pie}</figcaption>" if pie else ""
    return f'<figure class="{clase}" style="{estilo}"><img src="../img/{src}" alt="">{leyenda}</figure>'


def verso(lineas, de="del poema"):
    return f'<blockquote class="verso">{"<br>".join(lineas)}<span class="de">{de}</span></blockquote>'


def fichero(filas):
    return '<dl class="ficha">' + "".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in filas) + "</dl>"


def cifra(valor, rotulo, clase=""):
    return f'<div class="cifra {clase}"><span>{valor}</span><small>{rotulo}</small></div>'


def lamina(numero, cuerpo, oscura=False, rejilla=False):
    cap = CAPITULO_DE.get(numero)
    capitulo = f"{marca(cap)}<span>{cap} · {CAPITULOS[cap]}</span>" if cap else marca(0)
    nota = ("simulación: formas hechas con código; la caja se llena a mano"
            if numero in SIMULADAS else "")
    clases = "lamina" + (" oscura" if oscura else "") + (" rejilla" if rejilla else "")
    return f"""<section class="{clases}" id="l{numero:02d}">
<header class="cabeza"><span>contenida</span><span class="capitulo">{capitulo}</span><span>{numero:02d} / {N}</span></header>
<div class="cuerpo">{cuerpo}</div>
<footer class="pie"><span>acciones para componer una voz · láminas de exposición</span><span>{nota}</span></footer>
</section>"""


# ---------------------------------------------------------------- las láminas

def l01():
    return lamina(1, "".join([
        b(1, 1, 10, 1, '<p class="sobre">Un proyecto tipográfico en homenaje a <i>Contener una ruina: acciones para '
                       'desenterrar una voz</i>, de Rebeca Paz Prada, con CreaciónxAcuerpamiento.</p>'),
        b(1, 3, 14, 3, '<h1 class="nombre">contenida</h1>', estilo="align-self:end"),
        b(1, 6, 14, 2, fig("portada_contenida.jpg")),
        b(1, 7, 10, 2, '<p class="subtitulo">acciones para componer una voz</p>', estilo="align-self:center"),
        b(1, 9, 8, 2, '<p class="leyenda">El nombre pasando por el agua de una bandeja: llega al revés, abierto en '
                      'trapecio y verde. Cada letra es una placa de aluminio repujado. Las dos n son placas distintas. '
                      'Simulación.</p>', estilo="align-self:end"),
        b(10, 9, 5, 2, '<p class="firma">Joaquin Max Cuevas Ventura<br>septiembre de 2026</p>', estilo="align-self:end"),
    ]), oscura=True)


def montaje_svg():
    """El montaje de la obra según los dos videos: esquema en corte, sin escala."""
    t, g, f, v = "#1d1c1a", "#6d6a63", "#cfcac0", "#4a2470"
    teselas = "".join(f'<line x1="{x}" y1="700" x2="{x}" y2="712" stroke="{f}" stroke-width="2"/>'
                      for x in range(110, 960, 28))
    azulejos = "".join(f'<line x1="962" y1="{y}" x2="990" y2="{y}" stroke="{f}" stroke-width="2"/>'
                       for y in range(200, 690, 62))

    def persona(x, y):
        return (f'<circle cx="{x}" cy="{y - 128}" r="15" fill="none" stroke="{g}" stroke-width="2.5"/>'
                f'<path d="M{x},{y - 112} V{y - 50} M{x},{y - 50} L{x - 14},{y} M{x},{y - 50} L{x + 14},{y}'
                f' M{x - 22},{y - 90} H{x + 22}" stroke="{g}" stroke-width="2.5" fill="none"/>')
    return f"""<svg viewBox="0 0 1050 820" width="100%" class="montaje" font-family="Courier Prime" font-size="20">
<path d="M0,150 H60 V660 Q60,712 112,712 H938 Q990,712 990,660 V150 H1050" fill="none" stroke="{t}" stroke-width="3"/>
{teselas}{azulejos}
<path d="M510,628 L990,262 L990,494 Z" fill="{v}" opacity=".13"/>
<path d="M510,628 L990,262 M510,628 L990,494" stroke="{v}" stroke-width="2" fill="none"/>
<path d="M300,560 L510,628" stroke="{v}" stroke-width="2" fill="none" stroke-dasharray="7 6"/>
<path d="M990,262 V494" stroke="{v}" stroke-width="7"/>
<rect x="150" y="652" width="420" height="48" fill="{t}"/>
<path d="M430,626 H592 L584,652 H438 Z" fill="#f3f1ea" stroke="{t}" stroke-width="2.5"/>
<path d="M440,636 H584" stroke="{v}" stroke-width="3"/>
<g transform="rotate(18 250 556)"><rect x="200" y="534" width="96" height="46" rx="5" fill="#f3f1ea" stroke="{t}" stroke-width="2.5"/>
<rect x="296" y="545" width="12" height="24" fill="{t}"/></g>
<path d="M232,588 V652 M268,600 V652" stroke="{t}" stroke-width="2.5"/>
{persona(790, 700)}{persona(880, 700)}{persona(24, 150)}
<g fill="{g}">
<text x="72" y="190">la piscina vacía</text>
<text x="150" y="760">plataforma con plástico negro</text>
<text x="150" y="786">y bandeja con un dedo de agua</text>
<text x="120" y="512">proyector</text>
<text x="970" y="214" text-anchor="end" fill="{v}">la imagen llega temblando,</text>
<text x="970" y="238" text-anchor="end" fill="{v}">en trapecio y verde</text>
<text x="620" y="786">público, adentro y afuera</text>
<text x="1050" y="760" text-anchor="end">media caña</text>
</g></svg>"""


def l02():
    texto = (
        "<h1>una piscina vacía</h1>"
        '<p class="bajada">La obra de la que sale este proyecto ocurrió en una piscina sin agua, una tarde de agosto.</p>'
        "<p><i>Contener una ruina: acciones para desenterrar una voz</i> es una obra de Rebeca Paz Prada, hecha con "
        "CreaciónxAcuerpamiento. Se presentó en el patio de un estudio de tatuajes, dentro de una piscina de azulejo "
        "que ya nadie usa. El público estuvo parado adentro y afuera.</p>"
        "<p>Rebeca partió de una lámina de libro: el ídolo Kochamama, dibujado según Posnansky. Llevó sus relieves a "
        "placas de papel de aluminio repujado y se las puso sobre el cuerpo, sueltas, con piel entre una y otra.</p>"
        "<p>El video, filmado en la misma piscina, pasaba por una bandeja con un dedo de agua antes de llegar a la "
        "pared. Llegaba temblando, abierto en trapecio y teñido de verde. Al final de cada vuelta, de la boca tapada "
        "salía una placa: un signo, no un sonido. En vivo, Rebeca tocó el agua y la imagen se deformó en la pared.</p>"
        + fichero([("obra", "<i>Contener una ruina: acciones para desenterrar una voz</i>"),
                   ("artista", "Rebeca Paz Prada, con CreaciónxAcuerpamiento"),
                   ("fecha", "sábado 22 de agosto de 2026, 17:00"),
                   ("lugar", "Artefacto Tatuajes, local 12, av. Arce pasando Belisario Salinas, Sopocachi, La Paz"),
                   ("formato", "video en bucle y acción en vivo")]))
    return lamina(2, "".join([
        b(1, 1, 6, 10, texto),
        b(8, 1, 7, 6, montaje_svg() + "<figcaption><b>fig. 2.1</b> El montaje, según los dos videos que filmó el "
                      "público. Esquema sin escala. Las fotos de la obra y del cuerpo de Rebeca no se reproducen sin "
                      "su permiso.</figcaption>"),
        b(8, 8, 7, 3, verso(["Quedó el contenedor", "de lo que ya no está.", "Una piscina vacía,",
                             "donde una vez aprendí a flotar,", "ahora aprendo a mirar."]), estilo="align-self:end"),
    ]))


def pie_marcado():
    """El pie de la lámina con el testigo de cada signo hallado en violeta."""
    testigo = {f["signo"]: f["pie"]["testigo"] for f in FICHAS.values() if f["estado"] == "hallada" and "pie" in f}
    vistos, salida = {}, []
    for ch in PIE:
        if ch in testigo:
            vistos[ch] = vistos.get(ch, 0) + 1
            if vistos[ch] == testigo[ch]:
                salida.append(f'<span class="testigo">{html.escape(ch)}</span>')
                continue
        salida.append(html.escape(ch))
    return "".join(salida)


def l03():
    derecha = (
        '<p class="entrada">El pie confiesa tres cosas:</p>'
        '<ol class="confesiones"><li>que el dibujo es una reconstrucción hecha con fotografías viejas, porque la '
        'piedra está erosionada;</li><li>que su calendario no está bien interpretado;</li><li>que el ídolo estuvo, '
        'se supone, en otro lugar.</li></ol>'
        "<p>Con las letras que trae el pie se escriben 31 de los 42 versos del poema. Los otros once piden letras que "
        "no están: <i>quedó</i>, <i>vez</i>, <i>después</i>, <i>empieza</i>, <i>opinión</i>, <i>salvó</i>, "
        "<i>escribió</i>.</p><p>Y <i>voz</i>. Para escribir <i>voz</i> hay que rehacer la z.</p>")
    cifras = (cifra("30", "hallados en el pie") + cifra("25", "reconstruidos con partes de los hallados")
              + cifra("1", "hecho con los dedos") + cifra("56", "celdas", "total"))
    return lamina(3, "".join([
        b(1, 1, 9, 2, '<h1>lo que dice la lámina</h1><p class="bajada">Rebeca tomó lo que la lámina muestra. Esta '
                      'tipografía toma lo que dice.</p>'),
        b(1, 3, 9, 5, f'<p class="pie-lamina">{pie_marcado()}</p><figcaption><b>fig. 3.1</b> El pie de la lámina, '
                      'transcrito desde una foto; falta cotejarlo con el libro. En violeta, la aparición que la '
                      'simulación eligió como testigo de cada uno de los 30 signos: la mejor conservada. Las '
                      'mayúsculas no cuentan. El pie las usa para el nombre impuesto.</figcaption>'),
        b(1, 8, 10, 3, f'<div class="cifras">{cifras}</div>', estilo="align-self:end"),
        b(11, 3, 4, 8, derecha),
    ]))


def l04():
    etno = (
        '<p class="tesis-titulo"><i>EthnoGraphemes: Scripts as Vessels for Culture</i></p>'
        + fichero([("autora", "Vaishnavi Mahendran"), ("dónde", "Rhode Island School of Design"), ("año", "2020"),
                   ("para", "la escritura sora sompeng, con la comunidad sora")])
        + '<p class="entrada">Se toma:</p><ul class="toma">'
        "<li>la escritura como vasija, pero una que no retiene;</li>"
        "<li>la tipografía sonora: la voz que se ve en el agua;</li>"
        "<li>el diccionario de cartas sueltas: la caja de placas;</li>"
        "<li>la forma que decide el material: el punzón y el aluminio;</li>"
        "<li>lo inacabado, y la palabra <i>unearthing</i>: desenterrar.</li></ul>"
        + verso(["«you have to write in a rounded script,", "otherwise you'll damage the palm leaf»"],
                de="Tim Brookes, entrevistado en la tesis"))
    afro = (
        '<p class="tesis-titulo"><i>Afrography: Scripting Futures Anchored in Culture &amp; Community</i></p>'
        + fichero([("autor", "Osmond Tshuma"), ("dónde", "Rhode Island School of Design"), ("año", "2025"),
                   ("para", "el ndebele del norte, su lengua materna")])
        + '<p class="entrada">Se toma:</p><ul class="toma">'
        "<li>las preguntas de <i>sankofa</i>, hechas a la lámina;</li>"
        "<li>las letras sacadas de un muro (<i>Nedmural</i>): aquí, del pie;</li>"
        "<li>la restricción que viene de la ruina (<i>The Great Stone</i>): aquí, la piscina;</li>"
        "<li>los cuadernos de experimentos: <i>Desenterrar</i>, <i>Contener</i> y <i>Devolver</i>;</li>"
        "<li>el objeto que vuelve a ser objeto: la fuente vuelve a ser placa.</li></ul>"
        + verso(["«Whose history is this?", "Who wrote it?", "How was it recorded?»"], de="Osmond Tshuma, prólogo"))
    return lamina(4, "".join([
        b(1, 1, 12, 2, '<h1>dos tesis, un método</h1><p class="bajada">De dos tesis de diseño gráfico se toman '
                       'maneras de hacer, no su misión.</p>'),
        b(1, 3, 6, 7, etno),
        b(8, 3, 6, 7, afro),
        b(1, 10, 14, 1, '<p class="franja">Las dos diseñan para una lengua y sus hablantes. <i>Contenida</i> no '
                        'revitaliza una lengua ni inventa una escritura andina. Escribe en español, con el alfabeto '
                        'latino, y deja sin traducir lo que nadie ha leído.</p>', estilo="align-self:end"),
    ]))


def reticula_svg():
    """La retícula de la cabeza, con las medidas de la foto: cada columna, del ancho que tiene."""
    R = RETICULA
    px, py = R["paso_x"], R["paso_y"]
    anchos = [px[0]] + [(a + b) / 2 for a, b in zip(px, px[1:])] + [px[-1]]
    altos = [py[0]] + [(a + b) / 2 for a, b in zip(py, py[1:])] + [py[-1]]
    k = 560 / sum(anchos)
    W, H = 600, sum(altos) * k + 110
    o = [f'<svg viewBox="0 0 {W} {H:.0f}" width="100%" font-family="Courier Prime" font-size="15">']
    y = 10
    for fila, alto in enumerate(altos):
        x = 20
        for col, ancho in enumerate(anchos):
            w, h = ancho * k, alto * k
            g = 2.5
            o.append(f'<path d="M{x + w / 2 - 4:.1f},{y + h - g:.1f} H{x + g:.1f} V{y + g:.1f} H{x + w - g:.1f} '
                     f'V{y + h - g:.1f} H{x + w / 2 + 4:.1f}" fill="none" stroke="var(--tinta)" stroke-width="1.6"/>')
            hw = R["hueco"]["ancho_sobre_paso"] * ancho * k
            hh = R["hueco"]["alto_sobre_paso"] * alto * k
            o.append(f'<rect x="{x + (w - hw) / 2:.1f}" y="{y + (h - hh) / 2:.1f}" width="{hw:.1f}" height="{hh:.1f}" '
                     f'fill="none" stroke="var(--gris2)" stroke-width="1.2"/>')
            x += w
        y += alto * k
    x = 20 + anchos[0] * k
    for i, r in enumerate(R["ancho_por_alto"]):
        cx = 20 + sum(anchos[:i + 1]) * k
        color = "var(--violeta)" if r in (min(R["ancho_por_alto"]), max(R["ancho_por_alto"])) else "var(--gris)"
        o.append(f'<line x1="{cx:.1f}" y1="{y + 6:.1f}" x2="{cx:.1f}" y2="{y + 18:.1f}" stroke="var(--gris2)" stroke-width="1"/>')
        o.append(f'<text x="{cx:.1f}" y="{y + 38:.1f}" text-anchor="middle" fill="{color}">{coma(r, 2)}</text>')
    o.append(f'<text x="20" y="{y + 72:.1f}" fill="var(--gris)">el paso de celda a celda, de ancho por alto</text>')
    o.append("</svg>")
    return "".join(o)


def l05():
    R = RETICULA
    texto = (
        "<h1>56 celdas</h1>"
        '<p class="bajada">La caja de tipos sale de la cabeza del ídolo.</p>'
        "<p>Sobre el rostro de la Kochamama hay una retícula de celdas iguales: un rectángulo dentro de otro, sin "
        "nada adentro. En la foto de la lámina se cuentan 8 columnas y 7 filas. Es la parte que el pie llama "
        "calendario, la que nadie ha leído.</p>"
        f"<p>Medida en una foto cercana, la celda no es regular: mide {coma(min(R['ancho_por_alto']), 2)} de ancho por "
        f"alto en los bordes y {coma(max(R['ancho_por_alto']), 2)} al centro. El dibujo curva la cabeza como un "
        "cilindro. La celda de la tipografía, 0,84, cae dentro.</p>"
        "<p>Esa retícula es la caja. Cada signo ocupa una celda, en el orden en que aparece en el pie: primero la "
        "coma que sigue al nombre del ídolo. Después vienen los reconstruidos. En la última, el signo que se hace "
        "con los dedos. Lo que no cabe se ve como la celda vacía. No hay mayúsculas ni signos de exclamación: la voz "
        "contenida no exclama.</p>")
    return lamina(5, "".join([
        b(1, 1, 4, 10, texto),
        b(5, 1, 6, 10, fig("caja_8x7.png", "<b>fig. 5.1</b> La caja. Continuo, lo hallado; punteado, lo "
                                           "reconstruido. Abajo, la celda vacía y lo que no cabe.")),
        b(11, 1, 4, 6, "<figure>" + reticula_svg() + "<figcaption><b>fig. 5.2</b> La retícula de la cabeza, medida "
                       "en la foto: cada columna, del ancho que tiene. Las del borde son más angostas.</figcaption></figure>"),
        b(11, 7, 4, 4, fig("03b_notdef.jpg", "<b>fig. 5.3</b> La celda vacía, calcada. También tiene desagüe."),
          estilo="align-self:end"),
    ]))


def l06():
    texto = (
        "<h1>la celda es la pauta</h1>"
        '<p class="bajada">Una letra, una celda: la de la cabeza del ídolo, 0,84 de ancho por alto.</p>'
        "<p>Primero la pauta fue la piscina: una letra por azulejo, la tesela como unidad. Pero la piscina fue "
        "escenario y pantalla, no molde. Ahora la letra vive en la celda de la cabeza del ídolo, un rectángulo dentro "
        "de otro, con la proporción que se mide en la lámina.</p>"
        "<p>Las cuatro líneas las da el pie. Sus nombres son de vasija: afuera, borde, fondo y desagüe.</p>"
        "<p>La altura de x, el borde, sale de la foto del pie: es más baja que la de la letra sustituta. La piscina "
        "queda como escenario: el frotado de su pared es el papel sobre el que se calca.</p>")
    medidas = fichero([("celda", "0,84 de ancho por alto"), ("placa", "150 × 150 mm, hasta medir la pared"),
                       ("canal", f"{coma(NUM['canal'] / 4)} mm, sin contraste"), ("desagüe", "3 mm, el surco del punzón"),
                       ("afuera", f"{coma(NUM['asc'] / 4)} mm sobre el fondo"),
                       ("borde", f"{coma(NUM['xh'] / 4)} mm sobre el fondo"),
                       ("desagüe", f"{coma(NUM['desc'] / 4)} mm bajo el fondo")])
    return lamina(6, "".join([
        b(1, 1, 5, 10, texto + medidas),
        b(6, 1, 4, 6, fig("03b_notdef.jpg", "<b>fig. 6.1</b> La celda de la lámina, calcada: un rectángulo dentro "
                                            "de otro, sin nada adentro. También tiene desagüe.")),
        b(6, 7, 4, 4, fig("01_frotado_de_la_pared.jpg", "<b>fig. 6.2</b> El frotado de la pared: el papel del "
                                                       "calco, no su medida. Simulación."), estilo="align-self:end"),
        b(10, 1, 5, 10, fig("pauta_azulejo.png", "<b>fig. 6.3</b> La pauta de calco, en A4: la placa, la celda y las "
                                                 "cuatro líneas del pie.")),
    ]))


def l07():
    return lamina(7, "".join([
        b(1, 1, 4, 10, '<h1 class="largo">del pie, las medidas; de la obra, la forma</h1>'
          "<p>El pie dice dónde va cada trazo y cuánto mide. Cómo es cada parte lo deciden parámetros que salen de "
          "la obra. Primero se define la forma en vectores; recién después pasa por los estados.</p>"
          + fichero([("canal", "un solo grosor: el punzón y la cinta no modulan"),
                     ("chapa", "ninguna curva más cerrada que la que el aluminio aguanta"),
                     ("cuenca", "fondo plano y desagüe de 3 mm"), ("hombro", "un arco tenso, de exponente 3"),
                     ("fuste", "tres planos, con quiebres de 1,6°"), ("asiento", "el pie se ensancha en el fondo"),
                     ("intemperie", "arriba, un corte; ningún remate"), ("gota", "solo gotea lo que mira abajo")])),
        b(5, 1, 10, 10, fig("20_gramatica_generadores.jpg", clase="alto", pie="<b>fig. 7.1</b> Los cuatro generadores: la o (la cuenca), "
                                                            "la l (el fuste), la n (el hombro) y la a, que los junta. "
                                                            "De izquierda a derecha: el testigo del pie con sus medidas, "
                                                            "las curvas maestras, el cuerpo en vectores y el calco. "
                                                            "Simulación: las formas, de un testigo sustituto; la "
                                                            "altura de x, de la foto del pie.")),
    ]))


def l08():
    reglas = (
        '<ol class="sigue">'
        "<li>Todo lo cerrado es una cuenca y se abre abajo. El ojo de la e se abre en su barra.</li>"
        "<li>Solo gotea lo que mira abajo. Lo que mira arriba termina en un corte.</li>"
        "<li>Donde dos rectas se juntan en ángulo, un alivio: el aluminio no se rasga.</li>"
        "<li>El punto es un trozo cuadrado de cinta. La coma, un punto del que cae una gota.</li>"
        "<li>La g y el 8 son sifones: dos cuencas comunicadas.</li>"
        "<li>Los dobles opuestos varían: la ¿ no es la ? dada vuelta, porque la gravedad no se da vuelta.</li></ol>")
    return lamina(8, "".join([
        b(1, 1, 5, 10, "<h1>cuatro generadores, cincuenta y cinco signos</h1>"
          '<p class="bajada">Los otros 51 signos no se dibujan: se arman con las partes de los cuatro.</p>'
          "<p>Es el método con que Agüero, Uribe y Berenguer leen la escultura de Tiwanaku: los elementos forman "
          "motivos y los motivos, figuras. Aquí, las partes forman signos. Lo reconstruido usa las mismas partes; "
          "solo se calca y se repuja a puntos.</p>" + reglas),
        b(6, 1, 9, 10, fig("21_gramatica_caja_reticula.jpg", "<b>fig. 8.1</b> Los 55 cuerpos base en la caja. En "
                                                             "violeta, lo reconstruido. Simulación.")),
    ]))


ESTADOS = [
    ("calco", "papel de calco sobre el frotado de la pared"),
    ("placa", "aluminio repujado por el reverso con un punzón"),
    ("cinta", "la letra puesta con masking, que no curva"),
    ("frotado", "papel y grafito sobre la placa, hasta que no se lee"),
    ("agua", "la luz de la placa por una bandeja con agua"),
    ("voz", "el agua movida por una voz que lee el poema"),
]


def l09():
    estados = "".join(f"<div><b>{n}</b><span>{d}</span></div>" for n, d in ESTADOS)
    return lamina(9, "".join([
        b(1, 1, 7, 3, '<h1>no hay regular</h1><p class="bajada">Los estilos de la familia no son pesos. Son los '
                      'estados por los que pasa la letra.</p>'),
        b(9, 1, 6, 3, "<p>La figura de la obra no tiene rostro: la cinta le tapa los ojos y la boca. La familia "
                      "tampoco tiene una cara neutra, una versión normal de la que las demás se aparten.</p>"
                      "<p>Cada estado sale del anterior por una operación física. En el frotado, el peso se mide en "
                      "frotadas: la primera sale oscura y la última que se lee, apenas gris.</p>",
          estilo="align-self:end"),
        b(1, 4, 14, 5, fig("cadena_de_estados.png", "<b>fig. 9.1</b> La cadena de estados, del pie a la fuente "
                                                    "digital, que vuelve a pasar por el agua.")),
        b(1, 9, 14, 2, f'<div class="estados">{estados}</div>', estilo="align-self:end"),
    ]))


def l10():
    f = DATOS.get("foto", {})
    texto = (
        '<h1>la propuesta<br>de la máquina</h1>'
        '<p class="bajada">Antes de hacerlo a mano, el taller se simuló con código. Es una hipótesis para '
        'confrontarla con la mano.</p>'
        f"<p>El pie está en una foto de la lámina. Enderezado línea por línea, se lee y se mide: la altura de x mide "
        f"{coma(f.get('alto_x', 11.7))} píxeles y la tinta se corrió. Pero no se calca: los ojos de la a y de la e "
        "se cierran.</p>"
        "<p>Por eso la máquina partió de una letra de imprenta parecida, la imprimió con tipos de plomo simulados, la "
        "fotocopió tres veces y la amplió. De la foto tomó una sola medida: la altura de x, más baja que la de la "
        "letra sustituta.</p>"
        "<p>De cada signo eligió la aparición mejor conservada y la limpió; lo que tuvo que decidir del borde fue de "
        f"{coma(NUM['opinion_min'])} a {pct(NUM['opinion_max'])}. La forma la dio la gramática. Después calcó cada "
        "cuerpo, con temblor, sobre el frotado de la pared.</p>"
        "<p>Ninguna de estas formas entra en la caja.</p>"
        + fichero([("semilla", "20260822, el día de la obra"), ("formas", "Liberation Serif, con plomo simulado"),
                   ("altura de x", "la de la foto del pie"), ("calco", "el cuerpo de la gramática, en vectores")]))
    cifras = (cifra(str(NUM["placas"]), "placas: 94 para el poema, 24 para los signos que no usa y el signo final")
              + cifra("55", "signos calcados; el 56 se hace con los dedos"))
    return lamina(10, "".join([
        b(1, 1, 5, 10, texto),
        b(6, 1, 9, 2, fig("pie_foto.jpg", "<b>fig. 10.1</b> El pie en la foto de la lámina, enderezado: 336 letras "
                                          "recortadas. Se lee y se mide; no se calca.")),
        b(6, 3, 9, 2, fig("pie_sustituto.jpg", "<b>fig. 10.2</b> El testigo de las formas: el pie impreso con una letra "
                                               "sustituta y tipos de plomo simulados.")),
        b(6, 5, 5, 6, fig("03_calco_reticula.jpg", "<b>fig. 10.3</b> Calco. Continuo lo hallado, punteado lo "
                                                   "reconstruido; la celda, en lápiz.")),
        b(11, 5, 4, 6, f'<div class="cifras columna">{cifras}</div>'
          + verso(["No se salvó la piedra,", "solo la opinión sobre ella."]), estilo="align-self:end"),
    ]))


def l11():
    texto = (
        "<h1>placa, por las dos caras</h1>"
        '<p class="bajada">Papel de aluminio de cocina, cortado a tijera y repujado por el reverso.</p>'
        "<p>El calco se da vuelta y se repasa por el reverso con un punzón de bola de 1 mm, sobre una base blanda. "
        "Por el reverso, la letra queda al revés y hundida: una canaleta con dos lomas bajas, un canal que podría "
        "contener agua. Por el anverso se lee, en relieve.</p>"
        "<p>La hoja se corta a tijera: cada lado en dos o tres cortes, con un escalón donde la tijera se retoma. A "
        "veces una esquina se va en diagonal. Donde la mano arranca y donde se detiene, el punzón hunde un poco "
        "más.</p>"
        f"<p>{NUM['placas']} placas y {coma(NUM['horas'])} horas de repujado simulado. Las que se rompen no se "
        "corrigen: se guardan en la caja y se hace otra.</p>")
    return lamina(11, "".join([
        b(1, 1, 4, 10, texto + verso(["Moverse como se mueve la piedra,", "es decir, apenas, es decir, temblor,"])),
        b(5, 1, 5, 5, fig("04_placa_reverso_reticula.jpg", "<b>fig. 11.1</b> Por el reverso: la letra al revés, "
                                                           "hundida.")),
        b(10, 1, 5, 5, fig("04_placa_reticula.jpg", "<b>fig. 11.2</b> Por el anverso: se lee, en relieve. Luz rasante "
                                                    "desde la izquierda.")),
        b(5, 6, 10, 4, fig("04b_placas_rotas.jpg", "<b>fig. 11.3</b> Placas que se rompieron. No se corrigen: se "
                                                   "guardan en la caja y se hace otra."), estilo="align-self:center"),
    ]))


def l12():
    texto = (
        "<h1>cinta</h1>"
        '<p class="bajada">La cinta que tapó ojos y boca da otro estado.</p>'
        "<p>Es masking blanca, tirando a hueso claro, y se pone sobre el plástico negro de la plataforma. No curva en "
        "su plano: va recta, y para girar se pliega o se superpone. Donde hay dos capas pasa menos luz.</p>"
        f"<p>Para los 55 signos hicieron falta {NUM['tramos']} tramos y {NUM['pliegues']} pliegues. La cinta no "
        "hace gotas ni asientos: en ella, la letra pierde lo que le daba la gravedad.</p>"
        "<p>Arrancada, deja en el plástico un residuo: la letra que estuvo.</p>")
    return lamina(12, "".join([
        b(1, 1, 5, 10, texto + verso(["A la boca la taparon, a las manos no,"])),
        b(6, 1, 9, 10, fig("07_cinta_reticula.jpg", "<b>fig. 12.1</b> Cinta. La celda 56 es de los dedos.")),
    ]))


def l13():
    texto = (
        "<h1>frotado</h1>"
        '<p class="bajada">Un papel sobre la placa, frotado con grafito: el gesto con el que empezó todo.</p>'
        "<p>La primera acción del taller es frotar la pared de la piscina. Aquí se frota la placa, por el anverso. El "
        "papel no entra en los valles finos: toca toda la hoja y se carga donde la placa sube.</p>"
        "<p>Cada frotada aplasta un poco el relieve. Se frota hasta que la letra no se lee: el peso de una letra se "
        "mide en frotadas.</p>"
        "<p>El signo final, una presión de pulgar, no da frotada: el domo es liso y el papel lo acompaña.</p>")
    cifras = (cifra(coma(NUM["frotadas_hallada"]), "frotadas que se leen, en promedio: letras halladas")
              + cifra(coma(NUM["frotadas_reconstruida"]), "reconstruidas", "violeta"))
    return lamina(13, "".join([
        b(1, 1, 4, 10, texto + verso(["Todos los archivos funcionan así."])),
        b(5, 1, 6, 6, fig("08_frotado_reticula.jpg", "<b>fig. 13.1</b> La primera frotada de cada placa.")),
        b(11, 1, 4, 6, f'<div class="cifras columna">{cifras}</div>', estilo="align-self:center"),
        b(5, 7, 10, 4, fig("08b_frotadas_de_la_a.jpg", "<b>fig. 13.2</b> La misma a, frotada una y otra vez: 1, 5, 10, "
                                                       "20 y la última que se lee."), estilo="align-self:center"),
    ]))


def l14():
    a = ficha("a")
    voz = a["voz"]
    return lamina(14, "".join([
        b(1, 1, 7, 3, '<h1>agua y voz</h1><p class="bajada">La letra llega a la pared pasando por el agua que a la '
                      'piscina le falta.</p>'),
        b(8, 1, 7, 3, "<p>La placa va al fondo de una bandeja con un dedo de agua. La luz rebota en el relieve y en "
                      "la superficie y cae sobre los azulejos: al revés, abierta en trapecio, verde. El punto quieto "
                      "es la lámpara reflejada en el agua; también está en los videos de la obra.</p>"
                      "<p>Tocada, el agua mete ondas desde una esquina. Con voz, la bandeja vibra con las sílabas del "
                      "poema y aparecen ondas de Faraday. La voz no se graba ni se codifica: solo deforma.</p>",
          estilo="align-self:end"),
        b(1, 4, 14, 5, '<div class="trio">'
          + fig("a_quieta.jpg", "<b>fig. 14.1</b> La a en el agua quieta.")
          + fig("a_tocada.jpg", "<b>fig. 14.2</b> Tocada en una esquina.")
          + fig("a_voz.jpg", f"<b>fig. 14.3</b> Con voz: «{voz['verso'].rstrip(',.;')}», sílaba {voz['silaba']}, "
                             f"{voz['hz']} Hz.") + "</div>"),
        b(1, 9, 5, 2, verso(["Tocas el agua y la diosa se deforma."])),
        b(6, 9, 5, 2, verso(["la misma diosa dos veces", "y ninguna igual."])),
        b(11, 9, 4, 2, '<p class="leyenda">La voz de la simulación es inventada: alturas entre 110 y 220 Hz, con el '
                       'ritmo silábico del poema.</p>'),
    ]), oscura=True)


def fila_de_ficha(f):
    partes = []
    if "pie" in f:
        p = f["pie"]
        partes.append(("pie", f"«{p['palabra']}», línea {p['linea']}, testigo {p['testigo']} de {p['de']}; "
                              f"opinión {coma(p['opinion_pct'])} %"))
    else:
        partes.append(("receta", f["reconstruccion"]))
    pl = f["placa_"]
    partes.append(("placa", f"{coma(pl['minutos'])} min, {pl['recorrido_mm']} mm de surco, "
                            f"{pl['roturas']} {'rotura' if pl['roturas'] == 1 else 'roturas'}"))
    partes.append(("cinta", f"{f['cinta']['tramos']} tramos, {f['cinta']['pliegues']} pliegues"))
    partes.append(("frotado", f"se lee hasta la frotada {f['frotado']['legibles']}"))
    partes.append(("agua", f"contraste {coma(f['agua']['contraste_de_la_letra'], 2)}"))
    partes.append(("voz", f"«{f['voz']['verso'].rstrip(',.;')}», {f['voz']['hz']} Hz"))
    return '<dl class="linea">' + "".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in partes) + "</dl>"


def l15():
    a, z = ficha("a"), ficha("z")
    return lamina(15, "".join([
        b(1, 1, 8, 2, '<h1>una letra de punta a punta</h1><p class="bajada">La a, hallada en «erosionado». La z, que '
                      'no está en el pie.</p>'),
        b(10, 1, 5, 2, verso(["Desenterrar una voz", "es desenterrar la mano del que la escribió."]),
          estilo="align-self:end"),
        b(1, 3, 14, 8, '<div class="dos-filas"><div><p class="rotulo-fila"><b>a</b> celda 8 · hallada</p>'
          + fig("12_cadena_08.jpg") + fila_de_ficha(a) + '</div><div><p class="rotulo-fila"><b>z</b> celda 32 · '
          'reconstruida: hipótesis sobre hipótesis</p>' + fig("12_cadena_32.jpg") + fila_de_ficha(z) + "</div></div>",
          estilo="align-self:center"),
    ]))


def barra(rotulo, valor, maximo, texto, clase=""):
    return (f'<div class="barra {clase}"><span class="r">{rotulo}</span><span class="pista">'
            f'<span style="width:{100 * valor / maximo:.1f}%"></span></span><span class="v">{texto}</span></div>')


def l16():
    n = NUM
    tope_agua = 1.15 * max(n["contraste_hallada"], n["contraste_reconstruida"])
    rot_h = 100 * n["roturas_hallada"] / n["placas_hallada"]
    rot_r = 100 * n["roturas_reconstruida"] / n["placas_reconstruida"]
    tope_rot = 1.15 * max(rot_h, rot_r, 1)
    bloques = [
        ("en el agua", "Contraste de la letra en el agua quieta.",
         barra("halladas", n["contraste_hallada"], tope_agua, coma(n["contraste_hallada"], 2))
         + barra("reconstruidas", n["contraste_reconstruida"], tope_agua, coma(n["contraste_reconstruida"], 2),
                 "violeta"),
         "El punteado tiene menos relieve que el surco y desvía menos luz. En el agua, las hipótesis se ven menos."),
        ("en el frotado", "Frotadas que se leen, en promedio.",
         barra("halladas", n["frotadas_hallada"], n["frotadas_max"], coma(n["frotadas_hallada"]))
         + barra("reconstruidas", n["frotadas_reconstruida"], n["frotadas_max"], coma(n["frotadas_reconstruida"]),
                 "violeta"),
         "Hechas a puntos, tienen menos relieve que tome el grafito. Se borran antes."),
        ("en el taller", "Horas de repujado para las 119 placas.",
         barra("simuladas", n["horas"], 1.15 * max(n["horas"], 40), coma(n["horas"]))
         + barra("planeadas", 40, 1.15 * max(n["horas"], 40), "30 a 40", "gris"),
         "Contando las placas que se rompieron. El plan se quedó corto."),
        ("en el aluminio", "Intentos rotos, por cada cien placas.",
         barra("halladas", rot_h, tope_rot, f"{n['roturas_hallada']} en {n['placas_hallada']}")
         + barra("reconstruidas", rot_r, tope_rot, f"{n['roturas_reconstruida']} en {n['placas_reconstruida']}",
                 "violeta"),
         "La máquina supuso que el punteado se rompe más: 16\u00a0% por intento, contra 6\u00a0%. "
         + ("Salió así. Pero esto no apareció: se supuso." if n["roturas_reconstruida"] / n["placas_reconstruida"]
            > n["roturas_hallada"] / n["placas_hallada"] else
            "Con tan pocas placas, pesó más el azar que la regla. Esto no apareció: se supuso.")),
    ]
    html_b = "".join(f'<div class="comparacion"><h2>{t}</h2><p class="que">{q}</p>{bs}<p>{e}</p></div>'
                     for t, q, bs, e in bloques)
    return lamina(16, "".join([
        b(1, 1, 8, 3, '<h1>lo que apareció<br>sin buscarlo</h1><p class="bajada">Nadie le pidió a la simulación que '
                      'las letras reconstruidas se vieran menos. Se vieron menos.</p>'),
        b(10, 1, 5, 3, "<p>Las reconstruidas se repujan a puntos, como se dibuja en arqueología lo que no se "
                       "encontró. Esa sola decisión las hizo más débiles en cada estado que vino después.</p>"
                       "<p>El pie confiesa que el dibujo es una reconstrucción, pero no dice qué parte. Aquí la parte "
                       "reconstruida se nota sola, y es la primera en irse.</p>", estilo="align-self:end"),
        b(1, 4, 14, 7, f'<div class="comparaciones">{html_b}</div>', estilo="align-self:center"),
    ]))


def l17():
    sigue = (
        "<h1>lo que sigue</h1>"
        '<ol class="sigue">'
        "<li>Hablar con Rebeca y con CreaciónxAcuerpamiento. Sin su acuerdo, nada de esto se hace.</li>"
        "<li>Encontrar el libro. Una pista: Posnansky 1945, vol. 2, figs. 100 a 102. Fotografiar el pie de cerca, con "
        "luz rasante, para que dé formas y no solo medidas.</li>"
        "<li>Medir la pared de la piscina y frotarla. No sacar nada; no dejar nada.</li>"
        "<li>Repujar a mano las 119 placas, con la gramática como pauta y la mano como juez.</li>"
        "<li>Poner la mano frente a la máquina, placa por placa y parámetro por parámetro.</li>"
        "<li>Recién entonces, lo digital: un molde para repujar placas nuevas, no un archivo que se guarda.</li></ol>")
    colofon = (
        '<div class="colofon"><p><b>contenida</b> · acciones para componer una voz</p>'
        "<p>Homenaje a <i>Contener una ruina: acciones para desenterrar una voz</i>, de Rebeca Paz Prada, con "
        "CreaciónxAcuerpamiento. Artefacto Tatuajes, La Paz, 22 de agosto de 2026.</p>"
        "<p>Proyecto y poema: Joaquin Max Cuevas Ventura.</p>"
        "<p>Con métodos de Vaishnavi Mahendran, <i>EthnoGraphemes: Scripts as Vessels for Culture</i> (RISD, 2020), "
        "y de Osmond Tshuma, <i>Afrography: Scripting Futures Anchored in Culture &amp; Community</i> (RISD, "
        "2025). La iconografía, según Carolina Agüero, Mauricio Uribe y José Berenguer, «La iconografía Tiwanaku: "
        "el caso de la escultura lítica», <i>Textos Antropológicos</i> 14 (2), 2003.</p>"
        "<p>Las letras de las imágenes son una simulación hecha con código, para confrontarla con la mano: las "
        "formas salen de un testigo sustituto (Liberation Serif); la altura de x, de la foto del pie. No entran en "
        "la caja ni en la fuente. El código, los esquemas y los textos se hicieron con asistencia de inteligencia "
        "artificial.</p>"
        "<p>Compuesto en Newsreader (Production Type) y Courier Prime (Alan Dague-Greene), con licencia SIL OFL, "
        "sobre una retícula de 16 × 12 módulos.</p></div>")
    return lamina(17, "".join([
        b(1, 1, 7, 6, sigue),
        b(8, 1, 7, 6, colofon),
        b(1, 6, 10, 5, verso(["A la boca la taparon, a las manos no,", "No tiene lengua pero igual dice."],
                             de="últimos versos del poema"), clase="final", estilo="align-self:end"),
        b(11, 6, 4, 5, fig("celda_56.jpg", "<b>fig. 17.1</b> Celda 56, el signo final: una presión de pulgar. La "
                                           "máquina no tiene dedos; simuló uno."), estilo="align-self:end"),
    ]))


LAMINAS = [l01, l02, l03, l04, l05, l06, l07, l08, l09, l10, l11, l12, l13, l14, l15, l16, l17]
NOMBRES = ["portada", "una_piscina_vacia", "lo_que_dice_la_lamina", "dos_tesis", "56_celdas", "la_celda",
           "la_gramatica", "cincuenta_y_cinco_signos", "no_hay_regular", "la_propuesta_de_la_maquina", "placa",
           "cinta", "frotado", "agua_y_voz", "de_punta_a_punta", "lo_que_aparecio", "lo_que_sigue"]


# ---------------------------------------------------------------- página y salida

def pagina(secciones, imprimir=False):
    extra = "@page{size:2400px 1800px;margin:0}" if imprimir else ""
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Contenida · láminas</title>
<link rel="stylesheet" href="../laminas.css"><style>{extra}</style></head>
<body>{secciones}</body></html>"""


def chrome():
    for c in (os.environ.get("CHROME"), "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
              "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and Path(c).exists():
            return c
    sys.exit("No encuentro Chromium: pon su ruta en la variable CHROME.")


def correr(args):
    ejecutable = chrome()
    modo = [] if ejecutable.endswith("headless_shell") else ["--headless=new"]
    base = [ejecutable, *modo, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--allow-file-access-from-files", "--virtual-time-budget=8000"]
    subprocess.run(base + args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    HTML.mkdir(exist_ok=True)
    PNG.mkdir(exist_ok=True)
    vigentes = {f"{i:02d}_{n}" for i, n in enumerate(NOMBRES, 1)}
    for viejo in list(HTML.glob("[0-9][0-9]_*.html")) + list(PNG.glob("[0-9][0-9]_*.png")):
        if viejo.stem not in vigentes:
            viejo.unlink()
    todas = []
    for i, (f, nombre) in enumerate(zip(LAMINAS, NOMBRES), 1):
        seccion = f()
        todas.append(seccion)
        ruta = HTML / f"{i:02d}_{nombre}.html"
        ruta.write_text(pagina(seccion), encoding="utf8")
        correr([f"--screenshot={PNG / f'{i:02d}_{nombre}.png'}", "--window-size=2400,1800", ruta.as_uri()])
        print(f"lámina {i:02d}: {nombre}")
    ruta = HTML / "todas.html"
    ruta.write_text(pagina("\n".join(todas), imprimir=True), encoding="utf8")
    correr([f"--print-to-pdf={AQUI / 'contenida_laminas.pdf'}", "--no-pdf-header-footer", ruta.as_uri()])
    print("listo:", AQUI / "contenida_laminas.pdf")


if __name__ == "__main__":
    main()
