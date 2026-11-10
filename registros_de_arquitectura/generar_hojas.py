#!/usr/bin/env python3
"""Rehace catalogo.md y las hojas de contacto a partir de catalogo.json.

Uso:  python3 registros_de_arquitectura/generar_hojas.py
Necesita Pillow. No descarga nada: trabaja con lo que hay en imagenes/.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/dejavu/DejaVuSans.ttf',
    '/Library/Fonts/Arial.ttf',
    'C:/Windows/Fonts/arial.ttf',
]


def fuente(tam):
    for ruta in FUENTES:
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, tam)
    return ImageFont.load_default()


def partir(texto, letra, ancho, dibujo):
    """Corta el texto en renglones que caben en el ancho dado."""
    renglones, actual = [], ''
    for palabra in texto.split():
        prueba = (actual + ' ' + palabra).strip()
        if dibujo.textlength(prueba, font=letra) <= ancho:
            actual = prueba
        else:
            renglones.append(actual)
            actual = palabra
    if actual:
        renglones.append(actual)
    return renglones


def hoja(familia, fichas, salida):
    """Una hoja de contactos por familia: cada lámina con su número, su fuente y su tipo de dibujo."""
    columnas, lado, margen, pie = 4, 420, 28, 74
    filas = (len(fichas) + columnas - 1) // columnas
    cabeza = 120
    ancho = margen + columnas * (lado + margen)
    alto = cabeza + filas * (lado + pie + margen) + margen
    lienzo = Image.new('RGB', (ancho, alto), '#f6f3ec')
    d = ImageDraw.Draw(lienzo)
    d.text((margen, 26), familia['nombre'], font=fuente(34), fill='#1c1a17')
    d.text((margen, 76), familia['nota'], font=fuente(17), fill='#5c564c')
    chica, media = fuente(14), fuente(16)
    for i, f in enumerate(fichas):
        x = margen + (i % columnas) * (lado + margen)
        y = cabeza + (i // columnas) * (lado + pie + margen)
        d.rectangle([x, y, x + lado, y + lado], fill='#ffffff', outline='#d9d3c5')
        im = Image.open(os.path.join(AQUI, 'imagenes', f['archivo'])).convert('RGB')
        im.thumbnail((lado - 16, lado - 16), Image.LANCZOS)
        lienzo.paste(im, (x + (lado - im.size[0]) // 2, y + (lado - im.size[1]) // 2))
        titulo = partir('%d. %s' % (f['id'], f['titulo']), media, lado, d)[:2]
        for k, renglon in enumerate(titulo):
            d.text((x, y + lado + 8 + k * 20), renglon, font=media, fill='#1c1a17')
        linea = '%s, %d · %s' % (f['autor'], f['anio'], f['tipo_de_dibujo'])
        d.text((x, y + lado + 8 + len(titulo) * 20 + 2), linea, font=chica, fill='#7a7263')
    lienzo.save(salida, quality=86)
    return salida


def tabla(cat):
    """catalogo.md: la misma ficha en una tabla legible."""
    nombres = {c['id']: c['nombre'] for c in cat['caminos']}
    fam = {f['id']: f['nombre'] for f in cat['familias']}
    out = ['# Catálogo de registros de arquitectura del altiplano', '',
           'Lo escribe `generar_hojas.py` a partir de `catalogo.json`: no se edita a mano.', '']
    for f in cat['familias']:
        fichas = [i for i in cat['imagenes'] if i['familia'] == f['id']]
        out += ['## %s (%d)' % (f['nombre'], len(fichas)), '', f['nota'], '',
                '| N.º | Lámina | Fuente | Dibujo | Por qué entra |', '|---|---|---|---|---|']
        for i in fichas:
            caminos = ', '.join(nombres[c].lower() for c in i['caminos']) or 'contraste'
            porque = i['comentario'] + (' ' + i['nota'] if i['nota'] else '')
            porque += ' *Caminos: %s.*' % caminos
            fuente_ = '%s, %d, %s. [Página](%s)' % (i['autor'], i['anio'], i['ubicacion'], i['pagina'])
            if i['estado_derechos'] == 'por confirmar':
                fuente_ += ' **Derechos por confirmar.**'
            titulo = '**%s**<br>«%s»<br>%s' % (i['titulo'], i['titulo_original'], i['lugar'])
            out.append('| %d | %s | %s | %s | %s |' % (i['id'], titulo, fuente_, i['tipo_de_dibujo'], porque))
        out.append('')
    assert set(fam) == {i['familia'] for i in cat['imagenes']}
    return '\n'.join(out)


def main():
    with open(os.path.join(AQUI, 'catalogo.json'), encoding='utf8') as fh:
        cat = json.load(fh)
    for n, f in enumerate(cat['familias'], 1):
        fichas = [i for i in cat['imagenes'] if i['familia'] == f['id']]
        print(hoja(f, fichas, os.path.join(AQUI, 'hoja_%d_%s.jpg' % (n, f['id']))))
    with open(os.path.join(AQUI, 'catalogo.md'), 'w', encoding='utf8') as fh:
        fh.write(tabla(cat) + '\n')
    print('catalogo.md')


if __name__ == '__main__':
    main()
