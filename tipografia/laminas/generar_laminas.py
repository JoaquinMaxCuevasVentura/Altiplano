"""Láminas de exposición de Contenida: dieciséis láminas 4:3.

Uso (desde la raíz del repositorio, después de simular.py):
    python3 tipografia/laminas/imagenes.py
    python3 tipografia/laminas/generar_laminas.py

Escribe en tipografia/laminas/:
  html/     una página por lámina (y todas.html, para imprimir),
  png/      cada lámina a 2400 × 1800 px,
  contenida_laminas.pdf   las dieciséis, una por página (4:3, 1800 × 1350 pt).

La retícula de las láminas es la de la piscina: 16 × 12 azulejos de 150 px,
con un azulejo de margen. Los números salen de las fichas de la simulación.
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
N = 16

FICHAS = json.loads((SIM / "salida" / "fichas_simuladas.json").read_text(encoding="utf8"))
DATOS = json.loads((AQUI / "img" / "datos.json").read_text(encoding="utf8"))
CAJA = json.loads((TIPO / "esquemas" / "caja.json").read_text(encoding="utf8"))
PIE = (TIPO / "textos" / "pie_de_lamina.txt").read_text(encoding="utf8").strip()
POEMA = (TIPO / "textos" / "poema.txt").read_text(encoding="utf8")

CAPITULOS = {1: "la obra", 2: "el sistema", 3: "el taller simulado", 4: "lo que queda"}
CAPITULO_DE = {2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 4, 16: 4}
SIMULADAS = {1, 7, 8, 10, 11, 12, 13, 14, 15}


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
    n["tirada"] = primeras[0]["copia"]["tirada"]
    for e, fs in por.items():
        n[f"legible_{e}"] = media([f["copia"]["ultima_legible"] for f in fs])
        n[f"contraste_{e}"] = media([f["agua"]["contraste_de_la_letra"] for f in fs])
        placas = [f for f in todas if f["estado"] == e]
        n[f"placas_{e}"] = len(placas)
        n[f"roturas_{e}"] = sum(f["placa_"]["roturas"] for f in placas)
    n["placas"] = len(todas)
    n["horas"] = sum(f["placa_"]["minutos"] for f in todas) / 60
    juntas = [f["azulejo"]["juntas_que_la_cortan"] for f in primeras]
    n["juntas_min"], n["juntas_max"], n["juntas_media"] = min(juntas), max(juntas), media(juntas)
    op = [f["pie"]["opinion_pct"] for f in por["hallada"]]
    n["opinion_min"], n["opinion_max"] = min(op), max(op)
    n["desagues"] = sum(f.get("anatomia", {}).get("desagues", 0) for f in primeras)
    n["signos_con_desague"] = sum(1 for f in primeras if f.get("anatomia", {}).get("desagues"))
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
    """Un bloque sobre la retícula de azulejos (14 × 10 dentro del margen).

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


def l05():
    texto = (
        "<h1>56 celdas</h1>"
        '<p class="bajada">La caja de tipos sale de la cabeza del ídolo.</p>'
        "<p>Sobre el rostro de la Kochamama hay una retícula de celdas iguales: un rectángulo dentro de otro, sin "
        "nada adentro. En la foto de la lámina se cuentan 8 columnas y 7 filas. Es la parte que el pie llama "
        "calendario, la que nadie ha leído.</p>"
        "<p>Esa retícula es la caja. Cada signo ocupa una celda, en el orden en que aparece en el pie: primero la "
        "coma que sigue al nombre del ídolo. Después vienen los reconstruidos. En la última, el signo que se hace "
        "con los dedos.</p>"
        "<p>Lo que no cabe se ve como la celda vacía. No hay mayúsculas ni signos de exclamación: la voz contenida "
        "no exclama.</p>"
        "<p>La tapa tiene una sola puerta. Con la caja cerrada se ve la coma.</p>")
    return lamina(5, "".join([
        b(1, 1, 4, 10, texto),
        b(5, 1, 6, 10, fig("caja_8x7.png", "<b>fig. 5.1</b> La caja. Continuo, lo hallado; punteado, lo "
                                           "reconstruido. Abajo, la celda vacía y lo que no cabe.")),
        b(11, 1, 4, 5, fig("05_caja_abierta.jpg", "<b>fig. 5.2</b> Abierta: en cada compartimento, las placas de su "
                                                  "signo. Simulación.")),
        b(11, 6, 2, 5, fig("05b_puerta.jpg", "<b>fig. 5.3</b> Cerrada: por la única puerta se ve la coma.")),
        b(13, 6, 2, 5, fig("03b_notdef.jpg", "<b>fig. 5.4</b> La celda vacía, calcada. También tiene desagüe.")),
    ]))



def l06():
    texto = (
        "<h1>la piscina es la pauta</h1>"
        '<p class="bajada">Una letra, un azulejo. Seis teselas de alto. Entre letra y letra, una junta.</p>'
        "<p>La pauta no se dibuja: se frota. Se pone papel sobre la pared de la piscina y se pasa grafito. Salen las "
        "juntas y las grietas. Las manchas no salen, porque no tienen relieve.</p>"
        "<p>En las fotos, un azulejo de pared mide lo mismo que seis teselas del piso. Hasta medirlo, se supone de "
        "150 mm. Como cada letra ocupa un azulejo, la letra es monoespaciada: la m lo llena y la i queda rodeada de "
        "piel.</p>"
        "<p>Las cuatro líneas de la pauta se llaman como la piscina: afuera, borde, fondo y desagüe.</p>"
        '<p class="nota">Estas láminas están hechas sobre la misma pauta: 16 × 12 azulejos, con uno de margen. '
        'Aquí se ve.</p>')
    medidas = fichero([("azulejo", "150 × 150 mm, supuesto"), ("tesela", "25 mm, seis por azulejo"),
                       ("junta", "3 mm"), ("afuera", "5,5 teselas"), ("borde", "4 teselas"),
                       ("fondo", "1,5 teselas"), ("desagüe", "0,5 teselas")])
    return lamina(6, "".join([
        b(1, 1, 5, 10, texto),
        b(6, 1, 4, 10, fig("01_frotado_de_la_pared.jpg", "<b>fig. 6.1</b> Frotado de un paño de 8 × 7 azulejos. "
                                                        "Simulación: la piscina todavía no se midió ni se frotó.")
          + medidas),
        b(10, 1, 5, 10, fig("pauta_azulejo.png", "<b>fig. 6.2</b> La pauta de calco, en A4. Las líneas se cuentan en "
                                                 "teselas desde abajo.")),
    ]), rejilla=True)



def l07():
    paneles = "".join(f'<img src="../img/anatomia_{i}.png" alt="">' for i in range(1, 7))
    return lamina(7, "".join([
        b(1, 1, 10, 2, '<h1 class="largo">del pie, el esqueleto;<br>de la obra, el cuerpo</h1>'),
        b(11, 1, 4, 2, "<p>El pie dice dónde va cada trazo y cuánto mide. Eso no se toca. Cómo es cada parte de la "
                       "letra lo decide la obra.</p>", estilo="align-self:end"),
        b(1, 3, 12, 8, f'<div class="paneles">{paneles}</div>'),
        b(13, 3, 2, 8, "<figcaption><b>fig. 7.1</b> La a, la o, la j, la á, el 8 y la ñ, con sus partes "
                       "nombradas.<br><br>La letra es hueca: se dibuja el contorno del canal. Cada contorno se abre "
                       "abajo, en el desagüe. La mitad baja del ojo es una bandeja. Lo que termina mirando hacia "
                       "abajo gotea. El punto es una tesela; la tilde, una gota; la virgulilla, una onda. Las cifras "
                       "viven en una celda.<br><br>Simulación sobre un testigo sustituto.</figcaption>",
          estilo="align-self:end"),
    ]))


REGLAS = [
    ("canal", "La letra es hueca: se dibujan las dos paredes del trazo.", "contener; la piscina sin agua"),
    ("desagüe", "Todo contorno se abre en su punto más bajo, una junta de ancho.",
     "«ningún contenedor aguanta lo que contiene»"),
    ("bandeja", "La mitad baja de cada ojo se cierra hacia abajo, en la proporción del trapecio.",
     "la bandeja con un dedo de agua"),
    ("panza", "Por fuera, la panza se asienta plana, con media caña.", "el fondo de la piscina"),
    ("lluvia", "Los remates de arriba casi desaparecen; los de abajo quedan como muñones.",
     "«casi no se ven esos detalles»"),
    ("gotas", "Donde un trazo termina mirando hacia abajo, cuelga una gota.", "el líquido que chorrea de la boca"),
    ("puntos", "Son cuadrados de media tesela.", "la cinta sobre ojos y boca; la tesela"),
    ("tildes", "Son gotas: la punta arriba, el peso abajo.", "la voz que carga y cae"),
    ("virgulilla", "Es una onda.", "tocar el agua"),
    ("asta", "La letra se corre hasta que su asta cae en una línea de media tesela.", "la letra se acomoda"),
    ("líneas", "Se llaman desagüe, fondo, borde y afuera.", "el público, adentro y afuera"),
    ("cifras", "Cada una vive en una celda de la cabeza del ídolo.", "el calendario que nadie ha leído"),
]


def l08():
    items = "".join(f'<li><span class="n">{i:02d}</span><b>{p}.</b> {r} <em>{de}</em></li>'
                    for i, (p, r, de) in enumerate(REGLAS, 1))
    a = NUM["ajuste"]
    return lamina(8, "".join([
        b(1, 1, 7, 2, '<h1>doce reglas</h1><p class="bajada">Cada parte de la letra responde a una decisión de la '
                      'obra. Tres obedecen a la gravedad: el desagüe, la lluvia y las gotas.</p>'),
        b(9, 1, 6, 2, f"<p>Al acomodarse a la retícula, el fondo pasó de {coma(a['base_de'], 2)} a "
                      f"{coma(a['base_a'])} teselas, y la altura de x, de {coma(a['x_de'], 2)} a {coma(a['x_a'])}. La "
                      "pauta provisional ya proponía esas medidas.</p><p>En los 55 signos se abrieron "
                      f"{NUM['desagues']} desagües. Cuelgan cinco gotas: s, a, c, f y á.</p>", estilo="align-self:end"),
        b(1, 3, 14, 4, fig("03d_antes_y_despues.jpg", "<b>fig. 8.1</b> Catorce letras. Arriba, lo que dio el pie; al "
                                                      "medio, con la anatomía; abajo, el calco, abierto en cada "
                                                      "desagüe. Simulación.")),
        b(1, 7, 14, 4, f'<ol class="reglas">{items}</ol>'),
    ]))


ESTADOS = [
    ("calco", "papel de calco sobre el frotado de la pared"),
    ("placa", "aluminio repujado por el reverso con un punzón"),
    ("piel", "la placa puesta el tiempo de un bucle"),
    ("copia", "hectógrafo de gelatina, tinta violeta"),
    ("agua", "la luz de la placa por una bandeja con agua"),
    ("voz", "el agua movida por una voz que lee el poema"),
    ("azulejo", "la luz sobre la pared, calcada"),
]


def l09():
    estados = "".join(f"<div><b>{n}</b><span>{d}</span></div>" for n, d in ESTADOS)
    return lamina(9, "".join([
        b(1, 1, 7, 3, '<h1>no hay regular</h1><p class="bajada">Los estilos de la familia no son pesos. Son los '
                      'estados por los que pasa la letra.</p>'),
        b(9, 1, 6, 3, "<p>La figura de la obra no tiene rostro: la cinta le tapa los ojos y la boca. La familia "
                      "tampoco tiene una cara neutra, una versión normal de la que las demás se aparten.</p>"
                      "<p>Cada estado sale del anterior por una operación física. En el hectógrafo, el peso se mide "
                      "en copias: la primera sale casi negra y la última que se lee, apenas violeta.</p>",
          estilo="align-self:end"),
        b(1, 4, 14, 5, fig("cadena_de_estados.png", "<b>fig. 9.1</b> La cadena de estados, del pie a la fuente "
                                                    "digital, que vuelve a pasar por el agua.")),
        b(1, 9, 14, 2, f'<div class="estados">{estados}</div>', estilo="align-self:end"),
    ]))


def l10():
    texto = (
        '<h1>la propuesta<br>de la máquina</h1>'
        '<p class="bajada">Antes de hacerlo a mano, el taller se simuló con código. Es una hipótesis para '
        'confrontarla con la mano.</p>'
        "<p>La máquina no tiene el libro. En la foto que hay, la altura de x del pie mide unos 4 píxeles y no se puede "
        "calcar. Por eso partió de una letra de imprenta parecida, la imprimió con tipos de plomo simulados, la "
        "fotocopió tres veces y la amplió.</p>"
        "<p>De cada signo eligió la aparición mejor conservada y la limpió. Lo que tuvo que decidir del borde, la "
        f"opinión, fue de {coma(NUM['opinion_min'])} a {pct(NUM['opinion_max'])}. Después la calcó con temblor y "
        "la repujó por el reverso.</p>"
        "<p>Ninguna de estas formas entra en la caja.</p>"
        + fichero([("semilla", "20260822, el día de la obra"), ("testigo", "Liberation Serif, en lugar del libro"),
                   ("punzón", "1 mm, por el reverso"), ("luz", "rasante, desde la izquierda, a 15°")]))
    rotas = NUM["roturas_hallada"] + NUM["roturas_reconstruida"]
    cifras = (cifra(str(NUM["placas"]), "placas: 94 para el poema, 24 para los signos que no usa y el signo "
                                        "final")
              + cifra("55", "signos calcados; el 56 se hace con los dedos") + cifra(str(rotas), "intentos rotos"))
    return lamina(10, "".join([
        b(1, 1, 5, 10, texto),
        b(6, 1, 9, 5, '<div class="par">' + fig("03_calco_reticula.jpg", "<b>fig. 10.1</b> Calco. Continuo lo "
                                                "hallado, punteado lo reconstruido.")
          + fig("04_placa_reticula.jpg", "<b>fig. 10.2</b> Placa, fotografiada con luz rasante. La primera de cada "
                                         "celda.") + "</div>"),
        b(6, 6, 9, 2, fig("04b_placas_rotas.jpg", "<b>fig. 10.3</b> Placas que se rompieron. No se corrigen: se "
                                                  "guardan en la caja y se hace otra.")),
        b(6, 9, 6, 2, f'<div class="cifras">{cifras}</div>', estilo="align-self:end"),
        b(12, 8, 3, 3, verso(["No se salvó la piedra,", "solo la opinión sobre ella."]), estilo="align-self:end"),
    ]))



def l11():
    texto = (
        "<h1>piel y copia</h1>"
        '<p class="bajada">La placa se lleva puesta el tiempo de un bucle. Después se copia hasta que la tinta se '
        'acaba.</p>'
        "<p>Cada placa se viste cinco minutos, lo que se supone que dura el bucle, y después se aplana con la palma. "
        "Los pliegues no se corrigen: son lo que el cuerpo le escribió encima.</p>"
        "<p>Las placas vestidas se entintan y pasan a la gelatina de un hectógrafo. Cada hoja que se apoya se lleva "
        "un poco de tinta. La primera copia sale casi negra; las siguientes, violeta; al final, nada.</p>"
        "<p>La gelatina bebe la tinta que le queda. A las 48 horas está limpia y se puede volver a empezar.</p>")
    cifras = (cifra(str(NUM["tirada"]), "copias leídas")
              + cifra(coma(NUM["legible_hallada"]), "última copia legible, en promedio: letras halladas")
              + cifra(coma(NUM["legible_reconstruida"]), "reconstruidas", "violeta"))
    return lamina(11, "".join([
        b(1, 1, 5, 10, texto + verso(["La tierra se dio de beber a sí misma",
                                      "y ningún contenedor aguanta lo que contiene."])),
        b(6, 1, 5, 6, fig("06_piel_reticula.jpg", "<b>fig. 11.1</b> Piel. Los pliegues siguen la parte del cuerpo: "
                                                  "antebrazo, esternón, cadera, muslo, espalda, hombro.")),
        b(11, 1, 4, 6, f'<div class="cifras columna">{cifras}</div>'),
        b(6, 7, 9, 4, fig("08_hectografo_copias.jpg", f"<b>fig. 11.2</b> Copias 1, 5, 10, 20 y {NUM['tirada']}. La "
                                                      "caja entera en una hoja A4, en cuerpo tesela."),
          estilo="align-self:end"),
    ]))



def l12():
    a = ficha("a")
    voz = a["voz"]
    return lamina(12, "".join([
        b(1, 1, 7, 3, '<h1>agua y voz</h1><p class="bajada">La letra llega a la pared pasando por el agua que a la '
                      'piscina le falta.</p>'),
        b(8, 1, 7, 3, "<p>La placa va al fondo de una bandeja con un dedo de agua. La luz rebota en el relieve y en "
                      "la superficie y cae sobre los azulejos: al revés, abierta en trapecio, verde. El punto quieto "
                      "es la lámpara reflejada en el agua; también está en los videos de la obra.</p>"
                      "<p>Tocada, el agua mete ondas desde una esquina. Con voz, la bandeja vibra con las sílabas del "
                      "poema y aparecen ondas de Faraday. La voz no se graba ni se codifica: solo deforma.</p>",
          estilo="align-self:end"),
        b(1, 4, 14, 5, '<div class="trio">'
          + fig("a_quieta.jpg", "<b>fig. 12.1</b> La a en el agua quieta.")
          + fig("a_tocada.jpg", "<b>fig. 12.2</b> Tocada en una esquina.")
          + fig("a_voz.jpg", f"<b>fig. 12.3</b> Con voz: «{voz['verso'].rstrip(',.;')}», sílaba {voz['silaba']}, "
                             f"{voz['hz']} Hz.") + "</div>"),
        b(1, 9, 5, 2, verso(["Tocas el agua y la diosa se deforma."])),
        b(6, 9, 5, 2, verso(["la misma diosa dos veces", "y ninguna igual."])),
        b(11, 9, 4, 2, '<p class="leyenda">La voz de la simulación es inventada: alturas entre 110 y 220 Hz, con el '
                       'ritmo silábico del poema.</p>'),
    ]), oscura=True)


def l13():
    texto = (
        "<h1>la letra llega a la pared</h1>"
        '<p class="bajada">Ampliada, la luz de cada letra cae sobre la pared de la piscina. Alguien calca lo que '
        'queda.</p>'
        "<p>Quien calca no puede seguir la letra por las juntas. Cada letra quedó cortada por entre "
        f"{NUM['juntas_min']} y {NUM['juntas_max']} juntas; {coma(NUM['juntas_media'])} en promedio.</p>"
        "<p>Abajo, cuatro versos compuestos con placas vestidas sobre la pared, una por azulejo, sujetas con cinta de "
        "pintor. Cuando una letra se repite en un verso, es otra placa. Ninguna sale igual dos veces.</p>")
    return lamina(13, "".join([
        b(1, 1, 6, 5, texto),
        b(1, 5, 6, 2, f'<div class="cifras">{cifra(coma(NUM["juntas_media"]), "juntas por letra, en promedio")}</div>',
          estilo="align-self:end"),
        b(8, 1, 7, 6, fig("11_azulejo_reticula.jpg", "<b>fig. 13.1</b> Azulejo: el calco de la luz en la pared, al "
                                                     "revés y cortado por las juntas.")),
        b(1, 8, 14, 3, fig("11b_estrofa_en_la_pared.jpg", "<b>fig. 13.2</b> «cada vuelta pasa por el agua / y el "
                                                          "agua no repite, / la misma diosa dos veces / y ninguna "
                                                          "igual.»"), estilo="align-self:end"),
    ]))


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
    partes.append(("piel", f"{f['piel']['parte']}, {f['piel']['pliegues']} pliegues"))
    partes.append(("copia", f"legible hasta la {f['copia']['ultima_legible']} de {f['copia']['tirada']}"))
    partes.append(("agua", f"contraste {coma(f['agua']['contraste_de_la_letra'], 2)}"))
    partes.append(("voz", f"«{f['voz']['verso'].rstrip(',.;')}», {f['voz']['hz']} Hz"))
    partes.append(("pared", f"{f['azulejo']['juntas_que_la_cortan']} juntas"))
    return '<dl class="linea">' + "".join(f"<div><dt>{a}</dt><dd>{v}</dd></div>" for a, v in partes) + "</dl>"


def l14():
    a, z = ficha("a"), ficha("z")
    return lamina(14, "".join([
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


def l15():
    n = NUM
    bloques = [
        ("en el agua", "Contraste de la letra en el agua quieta.",
         barra("halladas", n["contraste_hallada"], 2.5, coma(n["contraste_hallada"], 2))
         + barra("reconstruidas", n["contraste_reconstruida"], 2.5, coma(n["contraste_reconstruida"], 2), "violeta"),
         "El punteado tiene menos relieve que el surco y desvía menos luz. En el agua, las hipótesis se ven menos."),
        ("en el hectógrafo", f"Última copia legible, de {n['tirada']}.",
         barra("halladas", n["legible_hallada"], n["tirada"], coma(n["legible_hallada"]))
         + barra("reconstruidas", n["legible_reconstruida"], n["tirada"], coma(n["legible_reconstruida"]), "violeta"),
         "Hechas a puntos, dejan menos tinta en la matriz. Se borran antes."),
        ("en el taller", "Horas de repujado para las 119 placas.",
         barra("simuladas", n["horas"], 75, coma(n["horas"]))
         + barra("planeadas", 40, 75, "30 a 40", "gris"),
         "Contando las placas que se rompieron. El plan se quedó corto."),
        ("en el aluminio", "Intentos rotos, por cada cien placas.",
         barra("halladas", 100 * n["roturas_hallada"] / n["placas_hallada"], 20,
               f"{n['roturas_hallada']} en {n['placas_hallada']}")
         + barra("reconstruidas", 100 * n["roturas_reconstruida"] / n["placas_reconstruida"], 20,
                 f"{n['roturas_reconstruida']} en {n['placas_reconstruida']}", "violeta"),
         "La máquina supuso que el punteado se rompe más: 16\u00a0% por intento, contra 6\u00a0%. Con tan pocas "
         "placas, pesó más el azar que la regla. Esto no apareció: se supuso."),
    ]
    html_b = "".join(f'<div class="comparacion"><h2>{t}</h2><p class="que">{q}</p>{bs}<p>{e}</p></div>'
                     for t, q, bs, e in bloques)
    return lamina(15, "".join([
        b(1, 1, 8, 3, '<h1>lo que apareció<br>sin buscarlo</h1><p class="bajada">Nadie le pidió a la simulación que '
                      'las letras reconstruidas se vieran menos. Se vieron menos.</p>'),
        b(10, 1, 5, 3, "<p>Las reconstruidas se repujan a puntos, como se dibuja en arqueología lo que no se "
                       "encontró. Esa sola decisión las hizo más débiles en cada estado que vino después.</p>"
                       "<p>El pie confiesa que el dibujo es una reconstrucción, pero no dice qué parte. Aquí la parte "
                       "reconstruida se nota sola, y es la primera en irse.</p>", estilo="align-self:end"),
        b(1, 4, 14, 7, f'<div class="comparaciones">{html_b}</div>', estilo="align-self:center"),
    ]))


def l16():
    sigue = (
        "<h1>lo que sigue</h1>"
        '<ol class="sigue">'
        "<li>Hablar con Rebeca y con CreaciónxAcuerpamiento. Sin su acuerdo, nada de esto se hace.</li>"
        "<li>Identificar el libro de la lámina y fotografiar el pie con luz rasante.</li>"
        "<li>Medir la piscina y frotar sus paredes. No sacar nada; no dejar nada.</li>"
        "<li>Repujar a mano las 119 placas.</li>"
        "<li>Poner la mano frente a la máquina, placa por placa.</li>"
        "<li>Recién entonces, la fuente digital. Y que vuelva a pasar por el agua.</li></ol>")
    colofon = (
        '<div class="colofon"><p><b>contenida</b> · acciones para componer una voz</p>'
        "<p>Homenaje a <i>Contener una ruina: acciones para desenterrar una voz</i>, de Rebeca Paz Prada, con "
        "CreaciónxAcuerpamiento. Artefacto Tatuajes, La Paz, 22 de agosto de 2026.</p>"
        "<p>Proyecto y poema: Joaquin Max Cuevas Ventura.</p>"
        "<p>Con métodos de Vaishnavi Mahendran, <i>EthnoGraphemes: Scripts as Vessels for Culture</i> (RISD, 2020), "
        "y de Osmond Tshuma, <i>Afrography: Scripting Futures Anchored in Culture &amp; Community</i> (RISD, "
        "2025).</p>"
        "<p>Las letras de las imágenes son una simulación hecha con código, a partir de un testigo sustituto "
        "(Liberation Serif), para confrontarla con la mano. No entran en la caja ni en la fuente. El código, los "
        "esquemas y los textos se hicieron con asistencia de inteligencia artificial.</p>"
        "<p>Compuesto en Newsreader (Production Type) y Courier Prime (Alan Dague-Greene), con licencia SIL OFL, "
        "sobre la pauta de la piscina: 16 × 12 azulejos.</p></div>")
    return lamina(16, "".join([
        b(1, 1, 7, 6, sigue),
        b(8, 1, 7, 6, colofon),
        b(1, 6, 10, 5, verso(["A la boca la taparon, a las manos no,", "No tiene lengua pero igual dice."],
                             de="últimos versos del poema"), clase="final", estilo="align-self:end"),
        b(11, 6, 4, 5, fig("celda_56.jpg", "<b>fig. 16.1</b> Celda 56, el signo final: una presión de pulgar. La "
                                           "máquina no tiene dedos; simuló uno."), estilo="align-self:end"),
    ]))


LAMINAS = [l01, l02, l03, l04, l05, l06, l07, l08, l09, l10, l11, l12, l13, l14, l15, l16]
NOMBRES = ["portada", "una_piscina_vacia", "lo_que_dice_la_lamina", "dos_tesis", "56_celdas", "la_pauta",
           "anatomia", "doce_reglas", "no_hay_regular", "la_propuesta_de_la_maquina", "piel_y_copia", "agua_y_voz",
           "la_pared", "de_punta_a_punta", "lo_que_aparecio", "lo_que_sigue"]


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
