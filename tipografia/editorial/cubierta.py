"""La cubierta del libro de Contenida: tapa, lomo y contratapa.

La tapa es la tapa de la caja (D4): «una sola puerta, calada del tamaño de una celda, sobre la celda 1.
Portada viene de puerta. Con la caja cerrada se ve solo la coma que sigue al nombre del ídolo, el primer
signo hallado». No lleva título: las 56 celdas van en relieve seco, sin tinta, y la celda 1 es un troquel
por el que se ve la coma de la página 1. El título va en el lomo y en la contratapa.

Escribe dos HTML en .cache/libro/: tapa.html y contratapa.html (210 × 250 mm, para la versión de pantalla) y
cubierta.html (el pliego entero, con lomo, 3 mm de sangre y marcas de corte, para la imprenta).
"""

from libro import ALTO, ANCHO, ARRIBA, ADENTRO, AFUERA, LIBRO, an, al, esc, x, y

W, H = 210.0, 250.0
LOMO_POR_HOJA = 0.15     # mm por hoja: un papel ahuesado de 100 g y 1,5 de volumen; a confirmar con la imprenta
TINTA, GRIS, FILETE = "#1d1c1a", "#6d6a63", "#cfcac0"


def lomo_mm(paginas):
    return round((paginas + 1) // 2 * LOMO_POR_HOJA + 1.0, 1)


def _relieve(ox, oy, papel_claro="#ffffff", sombra="rgba(29,28,26,0.16)", hueco=1):
    """Las 56 celdas en relieve seco, como se verían: luz rasante desde la izquierda, como en las fotos de las placas."""
    o = []
    for f in range(1, 8):
        for c in range(1, 9):
            if (c, f) == (1, 1) and hueco:
                continue
            x0, y0, w, h = ox + x(c), oy + y(f), an(1), al(1)
            o.append(f'<path d="M{x0:.3f} {y0 + h:.3f}V{y0:.3f}H{x0 + w:.3f}" fill="none" stroke="{papel_claro}" '
                     f'stroke-width="0.45" stroke-opacity="0.95"/>')
            o.append(f'<path d="M{x0 + w:.3f} {y0:.3f}V{y0 + h:.3f}H{x0:.3f}" fill="none" stroke="{sombra}" '
                     f'stroke-width="0.35"/>')
    return o


def _puerta(ox, oy):
    """El troquel de la celda 1: el canto del cartón hace sombra arriba y a la izquierda."""
    x0, y0, w, h = ox + x(1), oy + y(1), an(1), al(1)
    return [f'<path d="M{x0:.3f} {y0 + h:.3f}V{y0:.3f}H{x0 + w:.3f}" fill="none" stroke="rgba(29,28,26,0.55)" '
            f'stroke-width="0.7"/>',
            f'<path d="M{x0 + w:.3f} {y0:.3f}V{y0 + h:.3f}H{x0:.3f}" fill="none" stroke="#ffffff" stroke-width="0.5"/>']


def tapa_html(coma, papel_css):
    """La tapa sola, para la versión de pantalla: se ve la coma por la puerta."""
    ox, oy = ADENTRO, ARRIBA                       # la tapa es una página derecha: el margen de adentro va a la izquierda
    dibujo = _relieve(ox, oy) + _puerta(ox, oy)
    return _pagina(f'''
<img src="{coma["ruta"]}" style="position:absolute;left:{ox + x(1) + (an(1) - coma["w"]) / 2:.3f}mm;top:{oy + coma["arriba"]:.3f}mm;width:{coma["w"]:.3f}mm">
<svg style="position:absolute;left:0;top:0;width:{W}mm;height:{H}mm" viewBox="0 0 {W} {H}">{"".join(dibujo)}</svg>
''', papel_css, "tapa")


def contratapa_html(papel_css, ox=AFUERA, oy=ARRIBA):
    return _pagina(_contratapa(ox, oy), papel_css, "contratapa")


def _contratapa(ox, oy):
    return f'''
<p style="position:absolute;left:{ox:.3f}mm;top:{oy - 2:.3f}mm;width:{an(6):.3f}mm;font:300 25pt/27.5pt Newsreader">contenida</p>
<p style="position:absolute;left:{ox:.3f}mm;top:{oy + 9.5:.3f}mm;width:{an(6):.3f}mm;font:300 italic 11pt/1.3 Newsreader;color:{GRIS}">acciones para componer una voz</p>
<div style="position:absolute;left:{ox + x(4):.3f}mm;top:{oy + y(3):.3f}mm;width:{an(4):.3f}mm;font:400 9.4pt/4.4365mm Newsreader">
<p style="margin:0 0 2.2mm"><em>Contenida</em> es una familia tipográfica de caja baja y monoespaciada, pensada para hacerse a mano en papel
de aluminio repujado. Es un homenaje a <em>Contener una ruina: acciones para desenterrar una voz</em>, de Rebeca Paz Prada con
CreaciónxAcuerpamiento. Sus letras salen del pie de la lámina que usó la obra; su caja, de la retícula de 8 × 7 celdas de la
cabeza del ídolo. Lo hallado y lo reconstruido se distinguen siempre. No hay pesos: hay estados de la letra.</p>
<p style="margin:0">Este libro reúne el proyecto antes de que exista la letra: lo hallado, lo que falta hacer a mano y la
propuesta de la máquina, rotulada como tal. Su primera lectora es Rebeca: nada se hace sin su acuerdo.</p>
</div>
<p style="position:absolute;left:{ox:.3f}mm;top:{oy + y(7):.3f}mm;width:{an(4):.3f}mm;font:400 6.6pt/3.3mm 'Courier Prime';color:#55534e">
Joaquin Max Cuevas Ventura<br>documento de trabajo · La Paz, octubre de 2026<br>no es un producto comercial<br>
hecho con asistencia de inteligencia artificial</p>
'''


def cubierta_html(paginas, papel_css, sangre=3.0):
    """El pliego de la cubierta para la imprenta, en dos páginas del mismo tamaño (el del corte, con su sangre):

    1. lo que se imprime en tinta: la contratapa y el lomo (la tapa no lleva tinta);
    2. las planchas de terminación: las 55 celdas en relieve seco, sin tinta, y el troquel de la celda 1.
    """
    lomo = lomo_mm(paginas)
    total = 2 * W + lomo
    ox, oy = W + lomo + ADENTRO, ARRIBA               # la retícula de la tapa: margen de adentro a la izquierda
    lh = 7 * 0.3528
    texto_lomo = "contenida · acciones para componer una voz"
    tinta = f'''
{_contratapa(AFUERA, ARRIBA)}
<p style="position:absolute;left:{W + lomo / 2 + lh / 2:.3f}mm;top:{ARRIBA:.3f}mm;margin:0;transform:rotate(90deg);
  transform-origin:0 0;white-space:nowrap;font:400 7pt/1 'Courier Prime'">{esc(texto_lomo)}</p>
'''
    celdas = []
    for f in range(1, 8):
        for c in range(1, 9):
            x0, y0, w, h = ox + x(c), oy + y(f), an(1), al(1)
            if (c, f) == (1, 1):
                celdas.append(f'<rect x="{x0:.3f}" y="{y0:.3f}" width="{w:.3f}" height="{h:.3f}" fill="none" stroke="#000" '
                              f'stroke-width="0.25" stroke-dasharray="1.2 0.8"/>')
            else:
                celdas.append(f'<rect x="{x0:.3f}" y="{y0:.3f}" width="{w:.3f}" height="{h:.3f}" fill="#000"/>')
    planchas = f'''
<svg style="position:absolute;left:0;top:0;width:{total:.3f}mm;height:{H}mm" viewBox="0 0 {total:.3f} {H}">{"".join(celdas)}
<line x1="{W:.3f}" y1="0" x2="{W:.3f}" y2="{H}" stroke="#000" stroke-width="0.1" stroke-dasharray="0.6 0.6"/>
<line x1="{W + lomo:.3f}" y1="0" x2="{W + lomo:.3f}" y2="{H}" stroke="#000" stroke-width="0.1" stroke-dasharray="0.6 0.6"/></svg>
<p style="position:absolute;left:{ox:.3f}mm;top:{oy + ALTO + 6:.3f}mm;width:{ANCHO:.3f}mm;font:400 6.6pt/3.3mm 'Courier Prime'">
Planchas de terminación de la tapa (no se imprimen). En negro, las 55 celdas en relieve seco, sin tinta: se levantan desde
el reverso, como las placas. Punteada, la celda 1: el troquel, de {an(1):.1f} × {al(1):.1f} mm, a {ADENTRO:.0f} mm del lomo y
{ARRIBA:.0f} mm del borde de arriba; por él se ve la coma de la página 1. Lomo: {lomo:.1f} mm para {paginas} páginas en un papel de
{LOMO_POR_HOJA:.2f} mm por hoja (a confirmar con la imprenta).</p>
'''
    return _pagina([tinta, planchas], papel_css, "cubierta", ancho=total, sangre=sangre), lomo


def _pagina(contenido, papel_css, nombre, ancho=W, sangre=0.0):
    """Una o varias hojas del mismo tamaño, cada una con sus piezas en posición absoluta."""
    marcas = f"bleed: {sangre}mm; marks: crop;" if sangre else ""
    hojas = contenido if isinstance(contenido, list) else [contenido]
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Contenida: {nombre}</title>
<link rel="stylesheet" href="estilo.css">
<style>
@page {{ size: {ancho:.3f}mm {H}mm; margin: 0; background: {papel_css}; {marcas} }}
@page :left {{ margin: 0; }}
@page :right {{ margin: 0; }}
body {{ margin: 0; }}
.hoja {{ position: relative; width: {ancho:.3f}mm; height: {H}mm; overflow: visible; }}
.hoja p {{ margin: 0; }}
.hoja + .hoja {{ break-before: page; }}
</style></head><body>{"".join(f'<div class="hoja">{h}</div>' for h in hojas)}</body></html>'''


def escribir(lb, paginas):
    """Escribe tapa.html, contratapa.html y cubierta.html; devuelve el ancho del lomo."""
    papel_css = "#ffffff" if lb.imprenta else "#f6f4ee"
    (LIBRO / "tapa.html").write_text(tapa_html(lb.coma, papel_css), encoding="utf8")
    (LIBRO / "contratapa.html").write_text(contratapa_html(papel_css), encoding="utf8")
    html, lomo = cubierta_html(paginas, "#ffffff")
    (LIBRO / "cubierta.html").write_text(html, encoding="utf8")
    return lomo
