"""Las planas del libro de Contenida (páginas compuestas en la retícula) y el orden de todo.

Cada plana es una página de 180 × 182,333 mm, la retícula, con sus piezas puestas en columnas y filas
(en() de libro.py). Las que van de a dos empiezan en página par (a la izquierda).
"""

from pathlib import Path

from PIL import Image

from libro import (ALTO, ANCHO, CELDAS, CERCA, FICHAS, IMG, LETRAS_PIE, PIE_TEXTO, POEMA, POLIZA, SIM, TIPO, al, an, en,
                   en_papel, esc, md, pie, plano, primera_aparicion, recorte_testigo, registrar, x, y)

TINTA, VIOLETA, FILETE, GRIS = "#1d1c1a", "#4a2470", "#cfcac0", "#6d6a63"
MONO = "Courier Prime"


# ------------------------------------------------------------------ piezas de dibujo (SVG en mm)
def svg(contenido, w=ANCHO, h=ALTO, estilo=""):
    return (f'<svg style="left:0;top:0;width:{w:.3f}mm;height:{h:.3f}mm;{estilo}" viewBox="0 0 {w:.3f} {h:.3f}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(contenido)}</svg>')


def marco(x0, y0, w, h, punteado=False, color=TINTA, grosor=0.2, hueco=2.0):
    """Un recuadro abierto abajo, en su punto más bajo: el desagüe."""
    cx = x0 + w / 2
    d = (f"M{cx - hueco / 2:.3f} {y0 + h:.3f}H{x0:.3f}V{y0:.3f}H{x0 + w:.3f}V{y0 + h:.3f}H{cx + hueco / 2:.3f}")
    rayas = ' stroke-dasharray="0.01 0.62" stroke-linecap="round"' if punteado else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}"{rayas}/>'


def texto_svg(x0, y0, t, tam=2.3, color=TINTA, ancla="start", peso=400, familia=MONO, estilo=""):
    return (f'<text x="{x0:.3f}" y="{y0:.3f}" font-family="{familia}" font-size="{tam}" font-weight="{peso}" '
            f'fill="{color}" text-anchor="{ancla}" {estilo}>{esc(t)}</text>')


def rotulo(estilo, html_, clase="rotulo"):
    return f'<div class="{clase}" style="{estilo}">{html_}</div>'


def titulo(estilo, t, rid=None):
    i = f' id="{rid}"' if rid else ""
    return f'<h2 class="titulo"{i} style="{estilo};font-weight:300">{md(t, False)}</h2>'


def guardar_png(im, nombre):
    destino = IMG / f"{nombre}.png"
    im.save(destino, optimize=True)
    return f"img/{destino.name}"


def guardar_jpg(im, nombre, calidad=90):
    destino = IMG / f"{nombre}.jpg"
    im.convert("RGB").save(destino, quality=calidad, optimize=True, progressive=True)
    return f"img/{destino.name}"


def img(ruta, estilo):
    return f'<img src="{ruta}" style="{estilo}" alt="">'


# ------------------------------------------------------------------ preliminares
def portadilla(lb):
    """Página 1. La tapa de la caja tiene una sola puerta, sobre la celda 1 (D4): detrás, la coma."""
    l = LETRAS_PIE[16]                                   # la coma de «KOCHAMAMA,»: el primer signo hallado
    assert l["signo"] == "," and l["palabra"] == "KOCHAMAMA"
    im = Image.open(TIPO / "simulacion" / "testigos" / l["archivo"]).convert("L").crop((l["x0"] - 2, 56, l["x1"] + 2, 96))
    im = im.resize((im.width * 16, im.height * 16), Image.LANCZOS)
    n, fid = registrar("La coma de «KOCHAMAMA,», el primer signo hallado", f"simulacion/testigos/{l['archivo']}", "hallada")
    ruta = guardar_png(en_papel(im, lb.papel), f"{n:03d}_coma")
    h = 10.0                                              # a 0,25 mm por píxel de la foto: la coma mide unos 4 mm
    w = h * im.width / im.height
    lb.coma = dict(ruta=ruta, w=w, arriba=7.0)           # la tapa la deja ver por su puerta
    lb.plana([
        svg([marco(x(1), y(1), an(1), al(1))]),
        img(ruta, f"left:{x(1) + (an(1) - w) / 2:.3f}mm;top:7mm;width:{w:.3f}mm"),
        rotulo(en(1, 2, 2), f'<b>celda 1</b><br>La coma que sigue a «KOCHAMAMA,»: el primer signo que se halla en el pie. '
                            f'Es el testigo 017 de las 336 letras recortadas de la foto de la lámina.'
                            f'<br><span class="fn">fig. {n}</span> {lb_etiqueta("hallada")}'),
        f'<p class="titulo" style="{en(4, 7, 5)}">contenida</p>',
        f'<p style="{en(4, 7, 5, dy=12)};font-style:italic;color:#6d6a63;font-size:11pt">acciones para componer una voz</p>',
    ], clase="derecha", pid=fid, rotulo="")


def lb_etiqueta(estado):
    from libro import etiqueta
    return etiqueta(estado)


def creditos(lb):
    lb.plana([
        rotulo(en(4, 1, 4), '<p class="lead"><em>Este libro es una propuesta.</em> Reúne el proyecto <em>Contenida</em> '
                            'para mostrárselo a Rebeca Paz Prada y a CreaciónxAcuerpamiento antes de hacer nada: si ellas '
                            'no están de acuerdo, el proyecto se detiene o cambia (Acción 0). Los nombres de los estilos '
                            'son propuestas. No hay fotos ni videos de la obra ni del cuerpo de Rebeca: donde harían falta, '
                            'queda un lugar punteado, pendiente de permiso.</p>', clase="lead"),
        rotulo(en(1, 6, 4, fs=2),
               "<b>Contenida: acciones para componer una voz</b><br>"
               "Un proyecto tipográfico de Joaquin Max Cuevas Ventura, en homenaje a <em>Contener una ruina: acciones para "
               "desenterrar una voz</em>, de Rebeca Paz Prada con CreaciónxAcuerpamiento (Artefacto Tatuajes, Sopocachi, "
               "La Paz, 22 de agosto de 2026).<br><br>"
               "Documento de trabajo. La Paz, octubre de 2026. No es un producto comercial.<br>"
               "Hecho con asistencia de inteligencia artificial: ver el colofón."),
    ], clase="izquierda")


def portada(lb):
    lb.plana([
        f'<p style="{en(1, 1, 8)};font:300 66pt/1 Newsreader;letter-spacing:-0.01em;top:-3mm">contenida</p>',
        f'<p style="{en(1, 2, 8, dy=-2)};font:300 italic 17pt/1.2 Newsreader;color:#6d6a63">acciones para componer una voz</p>',
        rotulo(en(4, 5, 4), '<p class="lead" style="font-size:10.4pt;line-height:5.2mm">Un proyecto tipográfico en homenaje '
                            'a <em>Contener una ruina: acciones para desenterrar una voz</em>, de Rebeca Paz Prada con '
                            'CreaciónxAcuerpamiento (Artefacto Tatuajes, Sopocachi, La Paz, 22 de agosto de 2026).</p>',
               clase="lead"),
        rotulo(en(1, 7, 3), "<b>Joaquin Max Cuevas Ventura</b><br>La Paz, octubre de 2026<br>documento de trabajo"),
    ], clase="derecha")


def indice(lb):
    lb.add("<!--INDICE-->")


def indice_html(lb):
    o = ['<section class="indice-general" id="indice">',
         '<p class="rotulo-indice">índice</p>']
    for iid, num, t, nivel in lb.entradas:
        if nivel == 1:
            o.append(f'<div class="ent cap"><a class="pag" href="#{iid}"></a>'
                     f'<span class="nn">{esc(num)}</span><a class="tt" href="#{iid}">{md(t, False)}</a></div>')
        else:
            o.append(f'<div class="ent menor"><a class="pag" href="#{iid}"></a>'
                     f'<a class="tt" href="#{iid}">{md(t, False)}</a></div>')
    o.append("</section>")
    return "".join(o)


def entrada(lb):
    """El resumen del informe, como entrada."""
    c = lb.caps["Resumen"]
    ps = "".join(f"<p>{md(b['md'])}</p>" for b in c["bloques"] if b["t"] == "p")
    lb.entrada("resumen", "resumen", 2)
    lb.plana([
        rotulo(en(1, 1, 2), "<b>resumen</b>"),
        f'<div class="resumen" style="{en(3, 1, 6)}">{ps}</div>',
        f'<p style="{en(4, 7, 5, dy=-4)};font:italic 12pt/5.8mm Newsreader;color:#4a2470">Desenterrar una voz<br>'
        f'es desenterrar la mano del que la escribió.</p>',
        rotulo(en(4, 7, 4, dy=8.5), "del poema"),
    ], clase="derecha", pid="resumen", rotulo="resumen")


# ------------------------------------------------------------------ el pie
def _hallados_en_orden():
    """La primera aparición de cada signo hallado en el pie, en caja baja: su índice en el texto → celda."""
    hallados = {c["signo"]: c["celda"] for c in CELDAS if c["estado"] == "hallada"}
    vistos, marcas = set(), {}
    for i, ch in enumerate(PIE_TEXTO):
        if ch.isupper() or ch.isspace():
            continue
        if ch in hallados and ch not in vistos:
            vistos.add(ch)
            marcas[i] = hallados[ch]
    return marcas


def pie_a_maquina(lb):
    marcas = _hallados_en_orden()
    spans = []
    for i, ch in enumerate(PIE_TEXTO):
        if i in marcas:
            spans.append(f'<span class="h" data-n="{marcas[i]}">{esc(ch)}</span>')
        elif ch.isupper():
            spans.append(f'<span class="M">{esc(ch)}</span>')
        else:
            spans.append(esc(ch))
    lb.entrada("el-pie", "el pie de la lámina, a máquina y letra por letra", 2)
    numeros = [(1, "30", "signos hallados en el pie", TINTA), (3, "25", "a reconstruir con sus partes", VIOLETA),
               (5, "1", "hecho con las manos", TINTA), (7, "56", "celdas", TINTA)]
    piezas = [
        rotulo(en(1, 1, 3, dy=-6.5), "<b>el pie de la lámina, a máquina</b>"),
        f'<p class="pie-maquina" style="{en(1, 1, 8)}">{"".join(spans)}</p>',
        rotulo(en(4, 4, 4, dy=6), '<p class="lead">El pie tiene 336 letras. Las mayúsculas no cuentan: son letras de monumento '
                                  'y la caja no las tiene. En violeta, la primera aparición de cada signo en caja baja, con el '
                                  'número de su celda: el orden en que el pie los muestra es el orden de la caja. El primero '
                                  'es la coma que sigue a «KOCHAMAMA,».</p>', clase="lead"),
    ]
    for c, num, t, color in numeros:
        piezas.append(f'<p style="{en(c, 6, 2)};font:300 40pt/1 Newsreader;color:{color};'
                      f'font-variant-numeric:lining-nums">{num}</p>')
        piezas.append(rotulo(en(c, 7, 2, dy=-5), t))
    lb.plana(piezas, clase="izquierda", pid="el-pie", rotulo="intermedio · el pie de la lámina")


def pie_letra_por_letra(lb, columnas=24):
    """Los 336 testigos del pie, cada uno en su celda de 0,84: el pie hecho monoespaciado con sus propias letras."""
    cw = ANCHO / columnas
    ch = cw / 0.84
    ppm = 15.0                                            # px por mm: 381 ppp
    W, filas = int(round(ANCHO * ppm)), -(-len(PIE_TEXTO) // columnas)
    H = int(round(filas * ch * ppm))
    lienzo = Image.new("L", (W, H), 255)
    marcas = _hallados_en_orden()
    letras = iter(LETRAS_PIE)
    dibujo = []
    for i, c in enumerate(PIE_TEXTO):
        col, fila = i % columnas, i // columnas
        x0, y0 = col * cw, fila * ch
        if c.isspace():
            continue
        l = next(letras)
        assert l["signo"] == c, (l, c)
        t = recorte_testigo(l, 8, 100)
        esc_ = ch * 0.94 * ppm / t.height
        t = t.resize((max(1, int(round(t.width * esc_))), int(round(t.height * esc_))), Image.BICUBIC)
        if c.isupper():                                   # las mayúsculas no cuentan: más claras
            t = Image.eval(t, lambda v: int(255 - (255 - v) * 0.38))
        px, py = int(round((x0 + cw / 2) * ppm - t.width / 2)), int(round((y0 + ch * 0.03) * ppm))
        lienzo.paste(Image.composite(t, lienzo.crop((px, py, px + t.width, py + t.height)), Image.eval(t, lambda v: 255 - v)),
                     (px, py))
        if i in marcas:
            dibujo.append(marco(x0 + 0.25, y0 + 0.25, cw - 0.5, ch - 0.5, color=VIOLETA, grosor=0.22, hueco=1.2))
            dibujo.append(texto_svg(x0 + 0.8, y0 + 2.0, str(marcas[i]), 1.7, VIOLETA))
    # las juntas: la retícula de celdas, apenas
    for k in range(columnas + 1):
        dibujo.insert(0, f'<line x1="{k * cw:.3f}" y1="0" x2="{k * cw:.3f}" y2="{filas * ch:.3f}" stroke="{FILETE}" stroke-width="0.12"/>')
    for k in range(filas + 1):
        dibujo.insert(0, f'<line x1="0" y1="{k * ch:.3f}" x2="{ANCHO:.3f}" y2="{k * ch:.3f}" stroke="{FILETE}" stroke-width="0.12"/>')
    n, fid = registrar("El pie, letra por letra: los 336 testigos en sus celdas", "simulacion/testigos/*.png", "hallada")
    ruta = guardar_jpg(en_papel(lienzo, lb.papel), f"{n:03d}_pie_letra_por_letra", calidad=90)
    alto = filas * ch
    lb.plana([
        img(ruta, f"left:0;top:0;width:{ANCHO}mm"),
        svg(dibujo, ANCHO, alto),
        rotulo(f"left:{x(4):.3f}mm;top:{alto + 6:.3f}mm;width:{an(5):.3f}mm",
               f'<span class="fn">fig. {n}</span>{lb_etiqueta("hallada")} El pie, letra por letra: las 336 letras recortadas de '
               f'la foto de la lámina, cada una en su celda de 0,84, como en una letra monoespaciada. La «i» queda rodeada '
               f'de piel; la «m» llena su celda. Entre palabras, una celda vacía. La retícula no mide la letra: la recibe, '
               f'y sus juntas cortan las palabras. En violeta, la primera aparición de cada signo hallado; en gris, las '
               f'mayúsculas, que no tienen celda.'),
    ], clase="derecha", pid=fid)


# ------------------------------------------------------------------ la caja
def caja(lb):
    """La caja, hoy, a la escala de la retícula: cada módulo de la página es una celda."""
    piezas, dibujo = [], []
    for c in CELDAS:
        cx, cy = x(c["columna"]), y(c["fila"])
        w, h = an(1), al(1)
        if c["estado"] == "hallada":
            l = primera_aparicion(c["signo"])
            t = recorte_testigo(l, 8, 100)
            t = t.resize((t.width * 6, t.height * 6), Image.BICUBIC)
            ruta = guardar_png(en_papel(t, lb.papel), f"caja_{c['celda']:02d}")
            alto = 15.2
            ancho = alto * t.width / t.height
            piezas.append(img(ruta, f"left:{cx + (w - ancho) / 2:.3f}mm;top:{cy + 1.6:.3f}mm;width:{ancho:.3f}mm"))
            dibujo.append(marco(cx, cy, w, h, grosor=0.2))
            dibujo.append(texto_svg(cx + 1.1, cy + 2.6, str(c["celda"]), 2.0, TINTA))
            dibujo.append(texto_svg(cx + w / 2, cy + h - 1.6, f"«{l['palabra']}»", 1.6, GRIS, "middle"))
        else:
            color = VIOLETA if c["estado"] == "reconstruida" else TINTA
            dibujo.append(marco(cx, cy, w, h, punteado=True, color=color, grosor=0.26))
            dibujo.append(texto_svg(cx + 1.1, cy + 2.6, str(c["celda"]), 2.0, color))
            signo = c["signo"]
            dibujo.append(texto_svg(cx + w / 2, cy + h / 2 + 1.2, signo, 3.4, color, "middle"))
            abajo = c.get("pedida_por") or ("con las manos" if c["estado"] == "manos" else "")
            if abajo:
                dibujo.append(texto_svg(cx + w / 2, cy + h - 1.6, abajo, 1.7, color, "middle"))
    n, fid = registrar("La caja, hoy: lo hallado en sus celdas y lo que falta", "simulacion/testigos/*.png · esquemas/caja.json",
                       "hallada")
    lb.entrada("la-caja", "la caja, celda por celda", 2)
    piezas.insert(0, svg(dibujo))
    piezas.append(rotulo(f"left:{x(4):.3f}mm;top:{ALTO + 5:.3f}mm;width:{an(5):.3f}mm",
                         f'<span class="fn" id="{fid}">fig. {n}</span>{lb_etiqueta("hallada")} La caja de 8 × 7, hoy, a la '
                         f'escala de la retícula: cada módulo de esta página es una celda. En las 30 halladas, su primera '
                         f'aparición en el pie, recortada de la foto de la lámina, sin retocar, y la palabra donde aparece. '
                         f'Punteado, lo que falta hacer a mano: en violeta, los 25 reconstruidos, con la palabra del poema '
                         f'que los pide; la celda 56 se hace con los dedos.'))
    lb.plana(piezas, clase="izquierda", pid="la-caja", rotulo="intermedio · la caja, celda por celda")


def indice_caja(lb):
    """El índice de la caja: cada celda con su signo, sus testigos o quién lo pide, y sus placas."""
    filas = []
    for c in CELDAS:
        s = c["signo"]
        if c["estado"] == "hallada":
            estado, de_donde = "hallada", f"{c['testigos']} · «{c['procedencia']}»"
        elif c["estado"] == "reconstruida":
            estado, de_donde = "reconstruida", (f"pide «{c['pedida_por']}»" if c.get("pedida_por") else "—")
        else:
            estado, de_donde = "con las manos", "el signo final"
        filas.append((c["celda"], s, estado, de_donde, POLIZA[s], c["estado"]))
    def tabla(parte):
        o = ['<table class="tabla-caja"><thead><tr><th>celda</th><th>signo</th><th>estado</th><th>testigos · primera palabra</th>'
             '<th>placas</th></tr></thead><tbody>']
        for celda, s, estado, de_donde, placas, e in parte:
            cl = "violeta" if e == "reconstruida" else ""
            o.append(f'<tr class="{cl}"><td>{celda:02d}</td><td class="s">{esc(s)}</td><td>{estado}</td><td>{esc(de_donde)}</td>'
                     f'<td class="d">{placas}</td></tr>')
        o.append("</tbody></table>")
        return "".join(o)
    total = sum(POLIZA.values())
    lb.plana([
        rotulo(en(1, 1, 3, dy=-6.5), "<b>la caja, celda por celda</b>"),
        f'<div style="{en(1, 1, 4)}">{tabla(filas[:28])}</div>',
        f'<div style="{en(5, 1, 4)}">{tabla(filas[28:])}</div>',
        rotulo(en(5, 7, 4, dy=-1), f"<b>{total} placas.</b> La póliza: tantas placas de cada signo como veces aparece en un "
                                   f"mismo verso, para componer el poema verso a verso sin repetir una placa. Los 24 signos que "
                                   f"el poema no usa llevan una cada uno, y el signo final otra."),
    ], clase="derecha")


# ------------------------------------------------------------------ galerías de láminas (índices de 12 lugares)
def galeria(lb, titulo_, lid, items, intro, estado="propia", clase="", ancho_c=2, alto_f=2, vacias=True):
    """Láminas en miniatura, de cuatro por fila (dos columnas cada una) y tres filas por página."""
    piezas = [rotulo(en(1, 1, 3, dy=-6.5), f"<b>{esc(titulo_)}</b>")]
    lugares = [(c, f) for f in (1, 3, 5) for c in (1, 3, 5, 7)]
    for k, (origen, codigo, t) in enumerate(items):
        c, f = lugares[k]
        n, fid = registrar(f"{codigo}: {plano(t)}", str(Path(origen).relative_to(TIPO)), estado)
        w = an(ancho_c)
        ruta, _ = lb.im.preparar(origen, w, nombre=f"{n:03d}_{Path(origen).stem}")
        piezas.append(f'<div id="{fid}" style="{en(c, f, ancho_c)}"><img src="{ruta}" style="width:100%;display:block" alt="">'
                      f'<p class="rotulo" style="margin-top:1.6mm"><span class="fn">{esc(codigo)}</span> {md(t, False)}</p></div>')
    for k in range(len(items), 12 if vacias else 0):     # lo que no cabe se ve como celda vacía
        c, f = lugares[k]
        piezas.append(f'<div class="vacio" style="{en(c, f, ancho_c, h=an(ancho_c) * 0.707)}"></div>')
    piezas.append(rotulo(en(1, 7, 4, dy=2), intro))
    lb.plana(piezas, clase=clase, pid=lid, rotulo=f"intermedio · {titulo_}")


PLANOS = [
    ("P-00_indice.png", "P-00", "índice, convenciones y las 24 decisiones anatómicas"),
    ("P-01_celda.png", "P-01", "la celda y las cuatro líneas, en la placa de 150 mm"),
    ("P-02_canal.png", "P-02", "el canal y la chapa: el radio mínimo, los cortes, la intemperie"),
    ("P-03_o_cuenca.png", "P-03", "**o**, la cuenca: la pared, el desagüe"),
    ("P-04_l_fuste.png", "P-04", "**l**, el fuste: el quiebre y el asiento"),
    ("P-05_n_hombro.png", "P-05", "**n**, el hombro: los arcos y el encuentro tangente"),
    ("P-06_a_gancho_y_gota.png", "P-06", "**a**, el gancho y la gota"),
    ("P-07_partes.png", "P-07", "el cuadro de las doce partes"),
    ("P-08_detalles.png", "P-08", "detalles: punto, tilde, onda, sifón, alivio, cifra"),
    ("P-09_dobles_opuestos.png", "P-09", "los dobles opuestos: ? ¿ · 6 9 · « »"),
    ("P-10_caja.png", "P-10", "el plan general de la caja de 8 × 7"),
]


def galeria_planos(lb):
    lb.entrada("los-planos", "los planos de la anatomía base", 2)
    galeria(lb, "los planos de la anatomía base", "los-planos",
            [(TIPO / "planos" / "png" / a, c, t) for a, c, t in PLANOS],
            "Once láminas A3 que dibujan la gramática como un plano de arquitectura, con cotas, escalas y, al lado de cada "
            "forma, el porqué de cada decisión. Se imprimen al 100 % desde <code>planos/contenida_planos.pdf</code>; aquí, "
            "a 1:10, son su índice. La celda que sobra queda vacía.")


TAXONOMIA = [
    ("R-00_indice.png", "R-00", "índice y convenciones"),
    ("R-01_metodo.png", "R-01", "el método, reformado"),
    ("R-02_cuadro.png", "R-02", "el cuadro de las referencias"),
    ("R-03_diferenciar.png", "R-03", "diferenciar (antítesis)"),
    ("R-04_agrupar.png", "R-04", "agrupar (sinécdoque)"),
    ("R-05_secuenciar.png", "R-05", "secuenciar (gradación y ciclo)"),
    ("R-06_inferir.png", "R-06", "inferir (elipsis y metáfora)"),
    ("R-07_encargos.png", "R-07", "del encargo a la referencia"),
    ("R-08_afuera.png", "R-08", "lo que queda afuera"),
]


def atlas(lb):
    origen = TIPO / "taxonomia" / "png" / "R-09_atlas.png"
    n, fid = registrar("Lámina R-09: el atlas de las referencias", "taxonomia/png/R-09_atlas.png", "dominio")
    ruta, (pw, ph) = lb.im.preparar(origen, ANCHO, nombre=f"{n:03d}_R-09_atlas", calidad=90)
    alto = ANCHO * ph / pw
    lb.entrada("el-atlas", "el atlas de las referencias", 2)
    lb.plana([
        rotulo(en(1, 1, 3, dy=-6.5), "<b>el atlas de las referencias</b>"),
        img(ruta, f"left:0;top:0;width:{ANCHO}mm"),
        rotulo(f"left:{x(4):.3f}mm;top:{alto + 5:.3f}mm;width:{an(5):.3f}mm",
               f'<span class="fn" id="{fid}">fig. {n}</span>{lb_etiqueta("propia")}{lb_etiqueta("dominio")} Lámina R-09: las obras de '
               f'dominio público con su imagen, al modo del cuadro de materiales de Kengo Kuma. Arriba, los siete dominios; en '
               f'el medio, cada obra en su celda, de la más antigua a la más nueva; abajo, la cadena del taller. Cada celda se '
               f'vacía por su desagüe. Cada imagen lleva su licencia y su fuente en <code>10_imagenes_de_dominio_publico.md</code>; '
               f'las imágenes no están en el repositorio: se bajan para armar la lámina.'),
    ], pid="el-atlas", rotulo="intermedio · el atlas de las referencias")


def galeria_taxonomia(lb):
    lb.entrada("la-taxonomia", "la taxonomía de las referencias", 2)
    galeria(lb, "la taxonomía de las referencias", "la-taxonomia",
            [(TIPO / "taxonomia" / "png" / a, c, t) for a, c, t in TAXONOMIA],
            "Las referencias ordenadas por su mecanismo, no por su estilo: diez láminas A3 en <code>taxonomia/</code> "
            "(<code>contenida_taxonomia.pdf</code>). R-09, el atlas, va en la página anterior.")


LAMINAS = [
    ("01_portada.png", "01", "contenida"), ("02_una_piscina_vacia.png", "02", "una piscina vacía"),
    ("03_lo_que_dice_la_lamina.png", "03", "lo que dice la lámina"), ("04_dos_tesis.png", "04", "dos tesis, un método"),
    ("05_56_celdas.png", "05", "56 celdas"), ("06_la_celda.png", "06", "la celda es la pauta"),
    ("07_la_gramatica.png", "07", "del pie, las medidas; de la obra, la forma"),
    ("08_cincuenta_y_cinco_signos.png", "08", "cuatro generadores, cincuenta y cinco signos"),
    ("09_no_hay_regular.png", "09", "no hay regular"), ("10_la_propuesta_de_la_maquina.png", "10", "la propuesta de la máquina"),
    ("11_placa.png", "11", "placa, por las dos caras"), ("12_cinta.png", "12", "cinta"),
    ("13_frotado.png", "13", "frotado"), ("14_agua_y_voz.png", "14", "agua y voz"),
    ("15_de_punta_a_punta.png", "15", "una letra de punta a punta"),
    ("16_lo_que_aparecio.png", "16", "lo que apareció sin buscarlo"), ("17_lo_que_sigue.png", "17", "lo que sigue"),
]


def galeria_laminas(lb):
    lb.entrada("las-laminas", "las láminas de exposición", 2)
    items = [(TIPO / "laminas" / "png" / a, c, t) for a, c, t in LAMINAS]
    galeria(lb, "las láminas de exposición", "las-laminas", items[:12],
            "Diecisiete láminas de 4:3 sobre una retícula de 16 × 12 módulos, para mostrar el proyecto en la pared o en "
            "pantalla (<code>laminas/contenida_laminas.pdf</code>). Las de la simulación son la propuesta de la máquina.",
            clase="izquierda")
    galeria(lb, "las láminas de exposición", None, items[12:], "", clase="", vacias=False)


# ------------------------------------------------------------------ una letra de punta a punta (doble página)
def punta_a_punta(lb):
    """Las cadenas de la «a» y de la «z», de punta a punta de la doble página."""
    tira_w = ANCHO + ANCHO + 2 * 17.0 - 0.0            # de c1 de la izquierda a c8 de la derecha, pasando por el lomo
    tira_w = (210 - 13.0) + (17.0 + ANCHO)               # 197 + 197 mm
    izq, der = [], []
    for k, (archivo, que, fila) in enumerate([("12_cadena_08.jpg", "la «a», hallada en «erosionado»", 2),
                                             ("12_cadena_32.jpg", "la «z», que no está en el pie", 5)]):
        origen = SIM / archivo
        n, fid = registrar(f"Una letra de punta a punta: {que}", f"simulacion/salida/{archivo}", "maquina")
        im = Image.open(origen).convert("RGB")
        im = im.crop((0, 0, im.width, im.height))
        px = int(round(tira_w / 25.4 * 300))
        im = im.resize((px, round(im.height * px / im.width)), Image.LANCZOS)
        from libro import igualar
        im = igualar(im, lb.papel)
        mitad = im.width // 2
        a = guardar_jpg(im.crop((0, 0, mitad, im.height)), f"{n:03d}_tira_izq")
        b = guardar_jpg(im.crop((mitad, 0, im.width, im.height)), f"{n:03d}_tira_der")
        alto = tira_w * im.height / im.width
        izq.append(img(a, f"left:0;top:{y(fila):.3f}mm;width:{tira_w / 2:.3f}mm"))
        der.append(img(b, f"left:-17mm;top:{y(fila):.3f}mm;width:{tira_w / 2:.3f}mm"))
        izq.append(rotulo(f"left:0;top:{y(fila) + alto + 3:.3f}mm;width:{an(4):.3f}mm",
                          f'<span class="fn" id="{fid}">fig. {n}</span>{lb_etiqueta("maquina")}{esc(que)}'))
    lb.entrada("punta-a-punta", "una letra de punta a punta", 2)
    izq.insert(0, f'<p class="titulo" style="{en(1, 1, 4, dy=-2)}">una letra de punta a punta</p>')
    izq.append(rotulo(en(5, 1, 4, dy=-1), '<p class="lead">Del pie a la voz, una letra por todos sus estados: el testigo, la '
                                   'gramática, el calco, la placa por las dos caras, la cinta, el frotado, el agua y la voz. '
                                   'Una hallada y una reconstruida, una sobre la otra: en el frotado y en el agua, la '
                                   'reconstruida se ve menos.</p>', clase="lead"))
    lb.plana(izq, clase="izquierda", pid="punta-a-punta", rotulo="intermedio · una letra de punta a punta")
    lb.plana(der, clase="")


# ------------------------------------------------------------------ la ficha y el registro de las 119 placas
FILAS_FICHA = [("Pie", "palabra ____ línea __ testigo __ de __"),
               ("Reconstrucción", "por analogía con ____"),
               ("Calco", "mano ____ fecha ____"),
               ("Placa", "mano ____ fecha ____ intentos __ roturas __"),
               ("Pulso", "sesión __ min. __ tardó __ min. levantadas ____"),
               ("Cinta", "tramos __ pliegues __ foto nº ____"),
               ("Frotado", "papel ____ frotadas legibles __ última __"),
               ("Agua", "quieta __ tocada __ foto nº ____"),
               ("Voz", "verso leído ____ foto nº ____"),
               ("Notas", "____")]


def _coma(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def ficha_maquina(f):
    p, ca, pl, pu, ci, fr, ag, vo = (f["pie"], f["calco"], f["placa_"], f["pulso"], f["cinta"], f["frotado"], f["agua"],
                                     f["voz"])
    return [
        f"palabra «{p['palabra'].strip(',.')}» línea {p['linea']} testigo {p['testigo']} de {p['de']}",
        "— (hallada)" if f["estado"] == "hallada" else "partes de la gramática",
        f"simulación · sesión {ca['sesion']} · min. {_coma(ca['minuto'])} · {_coma(ca['segundos'])} s · "
        f"levantadas {ca['levantadas']} · dudas {ca['dudas']}",
        f"simulación · intentos {pl['intentos']} · roturas {pl['roturas']} · {_coma(pl['minutos'])} min · "
        f"{pl['recorrido_mm']} mm de recorrido",
        f"sesión {pu['sesion']} · min. {_coma(pu['minuto'])} · punzón {_coma(pu['segundos_de_punzon'])} s · "
        f"levantadas {pu['levantadas']} · dudas {pu['dudas']} · cansancio {_coma(pu['cansancio'], 2)}",
        f"tramos {ci['tramos']} · pliegues {ci['pliegues']}",
        f"frotadas legibles {fr['legibles']} · sesión {fr['sesion']}",
        f"quieta y tocada · contraste de la letra {_coma(ag['contraste_de_la_letra'], 2)}",
        f"«{vo['verso']}» · sílaba {vo['silaba']} · {vo['hz']} Hz",
        f"{f['mano']}",
    ]


def ficha(lb):
    """La ficha de hallazgo: a la izquierda, en blanco, para la mano; a la derecha, la que llenó la máquina."""
    f = FICHAS["08.01"]                                    # la primera «a»
    maq = ficha_maquina(f)
    def bloque(col, filas, mano):
        o = []
        for k, (nombre, valor) in enumerate(filas):
            yy = y(2) + 3 + k * 10.6
            o.append(rotulo(f"left:{x(col):.3f}mm;top:{yy:.3f}mm;width:{an(4):.3f}mm",
                            f'<b>{nombre}</b><br>' + (f'<span class="raya">{"&nbsp;" * 2}</span>' if mano else esc(valor))))
        return o
    piezas = [
        rotulo(en(1, 1, 3, dy=-6.5), "<b>la ficha de hallazgo</b>"),
        f'<p class="titulo" style="{en(1, 1, 4, dy=-2)}">la mano</p>',
        f'<p class="titulo" style="{en(5, 1, 4, dy=-2)}">la máquina</p>',
        rotulo(en(1, 1, 3, dy=11), "Una por signo. Acompaña a la placa en su celda. Se llena a mano, con lápiz."),
        rotulo(en(5, 1, 3, dy=11), "La misma ficha, llenada por la simulación para la placa a.01 (celda 8)."),
    ]
    for k, (nombre, _) in enumerate(FILAS_FICHA):
        yy = y(2) + 6 + k * 11.4
        piezas.append(rotulo(f"left:{x(1):.3f}mm;top:{yy:.3f}mm;width:{an(4) - 2:.3f}mm",
                             f'<b>{nombre}</b><span class="raya"></span>'))
        piezas.append(rotulo(f"left:{x(5):.3f}mm;top:{yy:.3f}mm;width:{an(4):.3f}mm",
                             f'<b>{nombre}</b><br>{esc(maq[k])}', clase="rotulo maquina-texto"))
    n, fid = registrar("La ficha de hallazgo: la de la mano, en blanco, y la de la máquina", "esquemas/generar_esquemas.py · "
                       "simulacion/salida/fichas_simuladas.json", "mano")
    piezas.append(f'<div class="vacio violeta" style="left:{x(3):.3f}mm;top:{y(7) - 4:.3f}mm;width:{an(2):.3f}mm;'
                  f'height:{al(1) + 4:.3f}mm"></div>')
    piezas.append(rotulo(f"left:0;top:{y(7) - 4:.3f}mm;width:{an(2):.3f}mm",
                         f'<span class="fn" id="{fid}">fig. {n}</span>{lb_etiqueta("mano")} el signo, dibujado a mano, y el '
                         f'número de su celda'))
    lb.entrada("la-ficha", "la ficha y el registro de las 119 placas", 2)
    lb.plana(piezas, clase="izquierda", pid="la-ficha", rotulo="intermedio · la ficha y las 119 placas")


def registro(lb):
    """Las 119 placas: lo que anotó la máquina y una raya para la mano."""
    claves = sorted(FICHAS, key=lambda k: (FICHAS[k]["celda"], FICHAS[k]["variante"]))
    def fila(k):
        f = FICHAS[k]
        pu, pl, fr = f["pulso"], f["placa_"], f.get("frotado", {})
        cl = ' class="violeta"' if f["estado"] == "reconstruida" else ""
        punzon = _coma(pu["segundos_de_punzon"]) if "segundos_de_punzon" in pu else f'{pu.get("presiones", "—")} pres.'
        return (f'<tr{cl}><td>{esc(f["placa"])}</td><td class="d">{f["celda"]:02d}</td>'
                f'<td class="d">{pu["sesion"]}</td><td class="d">{_coma(pu["minuto"])}</td>'
                f'<td class="d">{punzon}</td><td class="d">{pu.get("levantadas", "—")}</td>'
                f'<td class="d">{pl["roturas"]}</td><td class="d">{fr.get("legibles", "·")}</td><td class="mano"></td></tr>')
    cabeza = ('<thead><tr><th>placa</th><th class="d">celda</th><th class="d">sesión</th><th class="d">min.</th>'
              '<th class="d">punzón s</th><th class="d">lev.</th><th class="d">rot.</th><th class="d">frot.</th>'
              '<th>la mano</th></tr></thead>')
    mitad = 60
    t1 = "".join(fila(k) for k in claves[:mitad])
    t2 = "".join(fila(k) for k in claves[mitad:])
    n, fid = registrar("El registro de las 119 placas, según la máquina", "simulacion/salida/fichas_simuladas.json", "maquina")
    lb.plana([
        rotulo(en(1, 1, 8, dy=-7), f'<b>las 119 placas</b> · <span class="fn" id="{fid}">fig. {n}</span>'
                                    f'{lb_etiqueta("maquina")} lo que anotó la simulación de cada placa, y una columna para '
                                    f'la mano'),
        f'<table class="registro" style="{en(1, 1, 4)}">{cabeza}<tbody>{t1}</tbody></table>',
        f'<table class="registro" style="{en(5, 1, 4)}">{cabeza}<tbody>{t2}</tbody></table>',
    ], clase="derecha")


# ------------------------------------------------------------------ la placa, de cerca
def de_cerca(lb):
    """La placa de la máquina, chica y terminada; la de la mano, a tamaño real y por hacer (doble página)."""
    f = FICHAS["08.01"]
    pu, pl = f["pulso"], f["placa_"]

    def placa(celda, cara, ancho, que):
        origen = CERCA / f"placa_{celda:02d}_{cara}.png"
        n, fid = registrar(que, f"editorial/imagenes/{origen.name}", "maquina")
        ruta, _ = lb.im.preparar(origen, ancho, nombre=f"{n:03d}_{origen.stem}", alfa=True)
        return n, fid, ruta

    n, fid, ruta = placa(8, "anverso", 75.0, "La placa a.01 por el anverso, a la mitad de su tamaño")
    piezas = [
        rotulo(en(1, 1, 3, dy=-6.5), "<b>la placa, de cerca</b>"),
        f'<figure id="{fid}" class="maquina" style="left:0;top:0;width:{75 + 4.8:.3f}mm"><div class="marco">'
        f'<img src="{ruta}" alt=""></div></figure>',
        rotulo(en(5, 1, 4), f'<span class="fn">fig. {n}</span>{lb_etiqueta("maquina")} La primera «a», por el anverso, a la '
                            f'mitad de su tamaño: papel de aluminio de cocina repujado por el reverso con un punzón de bola, '
                            f'con luz rasante desde la izquierda.<br><br>'
                            f'[ a.01 · celda 8 · sesión {pu["sesion"]} · minuto {_coma(pu["minuto"])} ]<br>'
                            f'punzón {_coma(pu["segundos_de_punzon"])} s · {pl["recorrido_mm"]} mm de recorrido<br>'
                            f'levantadas {pu["levantadas"]} · dudas {pu["dudas"]} · lecturas {pu["lecturas"]} · '
                            f'roturas {pl["roturas"]}<br>cansancio {_coma(pu["cansancio"], 2)}'),
    ]
    chicas = [(8, "reverso", "la misma «a», por el reverso: al revés y hundida"),
              (32, "anverso", "la «z», reconstruida: a puntos"),
              (56, "anverso", "el signo final: dos presiones de un pulgar que la máquina no tiene")]
    for k, (celda, cara, t) in enumerate(chicas):
        n, fid, ruta = placa(celda, cara, an(2) - 4.8, t[0].upper() + t[1:])
        piezas.append(f'<figure id="{fid}" class="maquina" style="{en(1 + 2 * k, 4, 2)}"><div class="marco">'
                      f'<img src="{ruta}" alt=""></div><figcaption>{pie(n, "maquina", t)}</figcaption></figure>')
    piezas.append(f'<p class="titulo" style="{en(1, 7, 8, dy=4)}">la de la máquina ya está hecha</p>')
    lb.entrada("de-cerca", "la placa, de cerca", 2)
    lb.plana(piezas, clase="izquierda", pid="de-cerca", rotulo="intermedio · la placa, de cerca")
    n2, fid2 = registrar("La placa a.01 de la mano, a tamaño real", "—", "mano")
    lb.plana([
        '<div class="vacio violeta" style="left:0;top:0;width:150mm;height:150mm"></div>',
        rotulo(f"left:0;top:{150 + 5:.3f}mm;width:{an(4):.3f}mm",
               f'<span class="fn" id="{fid2}">fig. {n2}</span>{lb_etiqueta("mano")} La placa de la mano, a tamaño real: '
               f'150 × 150 mm, el lado de un azulejo de la piscina. Va acá cuando exista.'),
        f'<p class="titulo" style="left:{x(5):.3f}mm;top:{y(7) + 4:.3f}mm;width:{an(4):.3f}mm;text-align:right">'
        f'la de la mano, no</p>',
    ], clase="derecha")


HOJAS = [
    ("03_calco.png", "calco", "En papel de calco, sobre el frotado de la pared: el contorno del cuerpo de la gramática, abierto "
                              "en su punto más bajo (el desagüe). Continuo lo hallado, punteado lo reconstruido."),
    ("04_placa_reverso.jpg", "placa por el reverso", "Papel de aluminio de cocina cortado a tijera. El calco, dado vuelta, se "
                                                     "repasa con un punzón de bola de 1 mm sobre una base blanda: un canal."),
    ("04_placa.jpg", "placa", "La misma placa por el anverso: la letra se lee, en relieve. Luz rasante desde la izquierda. "
                              "La celda 56, presiones de pulgar."),
    ("07_cinta.jpg", "cinta", "La letra puesta con masking sobre el plástico negro de la plataforma: no hace gotas ni asientos."),
    ("08_frotado.jpg", "frotado", "Papel sobre la placa, frotado con grafito: se marca lo que sobresale. La primera frotada de cada placa."),
    ("09_agua_quieta.jpg", "agua quieta", "La placa en el fondo de una bandeja con un dedo de agua: la luz rebota y cae, al revés y "
                                          "en trapecio. El verde es luz."),
    ("09b_agua_tocada.jpg", "agua tocada", "Un dedo toca el agua en una esquina: ondas concéntricas. Nunca en el mismo punto."),
    ("10_voz.jpg", "voz", "El agua vibra con el ritmo silábico del poema, leído una vez mientras se fotografían las 56 placas."),
]


def hojas_de_la_simulacion(lb):
    """Las ocho láminas de los estados, en la simulación, de a cuatro por página."""
    lb.entrada("los-estados-simulados", "los estados, simulados", 2)
    for parte, clase in ((HOJAS[:4], "izquierda"), (HOJAS[4:], "")):
        piezas = [rotulo(en(1, 1, 3, dy=-6.5), "<b>los estados, en la simulación</b>")] if clase else []
        for k, (archivo, nombre, t) in enumerate(parte):
            c, f = ((1, 1), (4, 1), (1, 4), (4, 4))[k]
            n, fid = registrar(f"{nombre.capitalize()}, en la simulación", f"simulacion/salida/{archivo}", "maquina")
            ruta, (pw, ph) = lb.im.preparar(SIM / archivo, an(3) - 4.8, nombre=f"{n:03d}_{Path(archivo).stem}", recorte="lamina")
            piezas.append(f'<figure id="{fid}" class="maquina" style="{en(c, f, 3)}"><div class="marco"><img src="{ruta}" alt="">'
                          f'</div><figcaption>{pie(n, "maquina", f"**{nombre}.** {t}")}</figcaption></figure>')
        lb.plana(piezas, clase=clase, pid="los-estados-simulados" if clase else None,
                 rotulo="intermedio · los estados, en la simulación")


# ------------------------------------------------------------------ el poema en la caja (doble página)
def poema(lb):
    """El poema compuesto con la caja, verso a verso: cada signo, una placa; entre palabras, la piel."""
    estrofas = [e.strip("\n").split("\n") for e in POEMA.strip().split("\n\n")]
    filas = []
    for k, e in enumerate(estrofas):
        if k:
            filas.append(None)
        filas.extend(v.strip().lower() for v in e)
    largo = max(len(v) for v in filas if v)
    cw = ANCHO / largo
    ch = cw / 0.84
    mitad = 25
    nverso = 0
    paginas = []
    estados = {c["signo"]: c["estado"] for c in CELDAS}
    con_reconstruidas = 0
    for pag, parte in enumerate((filas[:mitad], filas[mitad:])):
        dibujo = []
        for r, v in enumerate(parte):
            if v is None:
                continue
            nverso += 1
            y0 = r * ch
            pide = any(estados.get(s) == "reconstruida" for s in v)
            con_reconstruidas += pide
            dibujo.append(texto_svg(-3.2, y0 + ch * 0.68, f"{nverso:02d}", 1.6, VIOLETA if pide else GRIS, "end"))
            for i, s in enumerate(v):
                if s == " ":
                    continue
                x0 = i * cw
                e = estados.get(s)
                color = VIOLETA if e == "reconstruida" else TINTA
                dibujo.append(marco(x0 + 0.15, y0 + 0.15, cw - 0.3, ch - 0.3, punteado=(e != "hallada"),
                                    color=VIOLETA if e != "hallada" else FILETE, grosor=0.16 if e == "hallada" else 0.2,
                                    hueco=0.7))
                dibujo.append(texto_svg(x0 + cw / 2, y0 + ch * 0.66, s, 3.3, color, "middle"))
        paginas.append((dibujo, len(parte) * ch))
    n, fid = registrar("El poema compuesto con la caja", "textos/poema.txt · esquemas/caja.json", "propia")
    lb.entrada("el-poema", "el poema en la caja", 2)
    d1, h1 = paginas[0]
    d2, h2 = paginas[1]
    lb.plana([
        rotulo(en(1, 1, 3, dy=-6.5), "<b>el poema en la caja</b>"),
        svg(d1, ANCHO, h1, "overflow:visible"),
    ], clase="izquierda", pid="el-poema", rotulo="intermedio · el poema en la caja")
    lb.plana([
        svg(d2, ANCHO, h2, "overflow:visible"),
        rotulo(f"left:{x(4):.3f}mm;top:{h2 + 8:.3f}mm;width:{an(5):.3f}mm",
               f'<span class="fn" id="{fid}">fig. {n}</span>{lb_etiqueta("propia")} El poema compuesto con la caja, verso a '
               f'verso: cada signo, una placa; entre palabras, una celda vacía, la piel. Sin mayúsculas: la caja no las tiene. '
               f'En tinta lo hallado; en violeta y punteado lo reconstruido. Los versos que piden al menos un signo '
               f'reconstruido llevan su número en violeta: son {con_reconstruidas} de {nverso}. Las letras van a máquina, en '
               f'Courier Prime: las de la caja todavía no existen, las hace la mano.'),
    ], clase="")


# ------------------------------------------------------------------ al final
def referencias(lb):
    c = lb.caps["Referencias"]
    o = ['<section class="referencias" id="referencias">', '<p class="rotulo-seccion">referencias</p>', '<div class="refs">']
    for b in c["bloques"]:
        if b["t"] == "p":
            o.append(f'<p>{md(b["md"])}</p>')
        elif b["t"] == "h2":
            o.append(f'<h3>{md(b["md"], False)}</h3>')
    o.append("</div></section>")
    lb.entrada("referencias", "referencias", 1, num="")
    lb.add(*o)


def lista_de_imagenes(lb):
    lb.entrada("imagenes", "las imágenes, con su origen y su estado", 1, num="")
    lb.add("<!--IMAGENES-->")


def lista_html():
    from libro import FIGURAS, ESTADOS
    o = ['<section class="lista-imagenes" id="imagenes">', '<p class="rotulo-seccion">las imágenes</p>',
         '<p class="intro">Cada figura dice qué es. <b>Propia:</b> dibujada para el proyecto (con código, desde sus documentos). '
         '<b>Propuesta de la máquina:</b> sale de la simulación o de la aplicación; ninguna de sus formas entra en la caja ni en '
         'la fuente. <b>Hallada en la lámina:</b> letras recortadas de la foto del pie. <b>Dominio público:</b> con su licencia '
         'y su fuente. <b>Pendiente:</b> un lugar punteado que espera un permiso o la mano.</p>',
         '<table class="tabla-imagenes"><thead><tr><th>fig.</th><th>pág.</th><th>qué es</th><th>de dónde sale, en '
         '<code>tipografia/</code></th><th>estado</th></tr></thead><tbody>']
    for f in FIGURAS:
        nombre = ESTADOS[f["estado"]][0]
        o.append(f'<tr><td>{f["n"]}</td><td><a class="pag" href="#{f["id"]}"></a></td><td>{md(f["que"], False)}</td>'
                 f'<td class="ruta">{esc(f["origen"])}</td><td>{nombre}</td></tr>')
    o.append("</tbody></table></section>")
    return "".join(o)


def colofon(lb):
    lb.entrada("colofon", "colofón", 1, num="")
    lb.plana([
        rotulo(en(1, 1, 2), "<b>colofón</b>"),
        f'<div class="colofon" style="{en(4, 1, 5)}">'
        '<p><b>Contenida: acciones para componer una voz.</b> El libro de trabajo del proyecto, armado el 19 de octubre de 2026 '
        'desde <code>tipografia/</code> en el repositorio del proyecto. Homenaje a <em>Contener una ruina: acciones para desenterrar '
        'una voz</em>, de Rebeca Paz Prada con CreaciónxAcuerpamiento (Artefacto Tatuajes, Sopocachi, La Paz, 22 de agosto de 2026). '
        'Proyecto: Joaquin Max Cuevas Ventura.</p>'
        '<p><b>Las letras.</b> Newsreader (Production Type), para leer, y Courier Prime (Alan Dague-Greene), a máquina: lo que ya '
        'estaba escrito y lo que hay que saber. Las dos con licencia SIL Open Font License, incrustadas en este archivo. Un signo, '
        'σ, va en DejaVu Serif. Los mapas usan además La Belle Aurore (Kimberly Geswein, SIL OFL), que es una fuente y no una mano.</p>'
        '<p><b>La retícula.</b> La página mide 210 × 250 mm: tiene la proporción de la celda, 0,84. Su retícula es la caja: 8 '
        'columnas por 7 filas de celdas de 19 × 22,6 mm, con juntas de 4 mm; cada fila, con su junta, son seis líneas de texto. '
        'La retícula no se espeja: todas las páginas son la misma caja.</p>'
        '<p><b>El color.</b> Tinta y violeta, la tinta del esténcil y de lo reconstruido. El verde aparece solo como luz, en las '
        'fotos simuladas del agua y de la voz.</p>'
        '<p><b>Las imágenes.</b> Cada una dice qué es: propia, propuesta de la máquina, hallada en la lámina, de dominio público o '
        'pendiente. Lo hecho por la máquina va punteado, y todo marco se abre abajo, en su punto más bajo: el desagüe. No hay fotos '
        'ni videos de la obra ni del cuerpo de Rebeca. Los mapas se dibujaron con código, tomando como modelo las versiones '
        'mejoradas de Joaquin Max Cuevas Ventura.</p>'
        '<p><b>Cómo se hizo.</b> HTML y CSS compuestos en páginas con Vivliostyle, desde <code>tipografia/editorial/armar.py</code>. '
        'El texto sale del informe de decisiones (<code>tipografia/informe/informe.js</code>); si el informe cambia, el libro se '
        'vuelve a armar.</p>'
        '<p><b>Asistencia de inteligencia artificial.</b> Los textos, los esquemas, la simulación, las láminas, la aplicación, '
        'los planos, la taxonomía, el informe y sus mapas se hicieron con asistencia de inteligencia artificial (<code>06</code>, '
        '§6.3). Este libro también: su sistema editorial, la maqueta y el código que lo arma los propuso y los escribió un '
        'asistente de inteligencia artificial, a partir de los documentos del proyecto y de cinco referencias visuales elegidas '
        'por Joaquin Max Cuevas Ventura. Las formas de letra de sus figuras son la propuesta de la máquina: no entran en la caja '
        'ni en la fuente.</p>'
        '<p><b>No es un producto comercial.</b> Es una propuesta; su primera lectora es Rebeca Paz Prada.</p>'
        '</div>',
        f'<p style="{en(4, 7, 5)};font:italic 12pt/6mm Newsreader;color:#4a2470">Termina y empieza,<br>termina y empieza. ¶</p>',
    ], clase="", pid="colofon", rotulo="colofón")


# ------------------------------------------------------------------ el orden del libro
def componer(lb):
    portadilla(lb)
    creditos(lb)
    portada(lb)
    indice(lb)
    entrada(lb)
    pie_a_maquina(lb)
    pie_letra_por_letra(lb)

    obra = lb.vacio_texto("La obra: fotos y video de Rebeca Paz Prada", "permiso",
                          "La obra: las fotos y los dos videos son imágenes de Rebeca y de su cuerpo. Van acá si ella lo "
                          "autoriza.")
    lamina = lb.vacio_margen("La lámina «según Posnansky», del libro sin identificar", "permiso",
                             "La lámina: el dibujo del ídolo con su pie, en un libro todavía sin identificar. Su foto no se "
                             "reproduce.", alto=42.0)
    lb.capitulo(1, extras={"1.1": [obra], "1.2": [lamina]})
    lb.capitulo(2)
    lb.capitulo(3)
    lb.capitulo(4, extras={"4.2": [lb.al_margen("el-pie", "el pie, letra por letra")],
                           "4.3": [lb.al_margen("la-caja", "la caja, celda por celda")],
                           "4.5": [lb.al_margen("la-caja", "las placas de cada signo")]},
                despues=[lambda: caja(lb), lambda: indice_caja(lb)])
    lb.capitulo(5, extras={"5.5": [lb.al_margen("los-planos", "los once planos")]}, despues=[lambda: galeria_planos(lb)])
    lb.capitulo(6, extras={"6.3": [lb.al_margen("punta-a-punta", "una letra de punta a punta")]},
                despues=[lambda: punta_a_punta(lb)])
    lb.capitulo(7, extras={"inicio": [lb.al_margen("la-ficha", "la ficha y las 119 placas")]},
                despues=[lambda: ficha(lb), lambda: registro(lb)])
    lb.capitulo(8, extras={"8.1": [lb.al_margen("de-cerca", "la placa, de cerca")],
                           "8.2": [lb.al_margen("los-estados-simulados", "los estados, simulados")]},
                despues=[lambda: de_cerca(lb), lambda: hojas_de_la_simulacion(lb)])
    lb.capitulo(9, extras={"9.2": [lb.al_margen("el-poema", "el poema en la caja")]}, despues=[lambda: poema(lb)])
    lb.capitulo(10)
    lb.capitulo(11, extras={"11.4": [lb.al_margen("el-atlas", "el atlas")],
                            "11.5": [lb.al_margen("la-taxonomia", "las diez láminas")]},
                despues=[lambda: atlas(lb), lambda: galeria_taxonomia(lb)])
    lb.capitulo(12, despues=[lambda: galeria_laminas(lb)])
    referencias(lb)
    lista_de_imagenes(lb)
    colofon(lb)

    i = lb.partes.index("<!--INDICE-->")
    lb.partes[i] = indice_html(lb)
    i = lb.partes.index("<!--IMAGENES-->")
    lb.partes[i] = lista_html()
