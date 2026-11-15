"""Extrae el texto de un .docx convertido de PDF, sección por sección,
con el texto de su pie de página (el número visible). Uso:
python3 -I secciones.py entrada.docx salida.txt"""
import sys, zipfile, re
from xml.etree import ElementTree as ET
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
src, out = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src)
rels = ET.fromstring(z.read('word/_rels/document.xml.rels'))
target = {r.get('Id'): r.get('Target') for r in rels}
def footer_text(rid):
    if not rid: return ''
    try:
        x = z.read('word/' + target[rid])
    except KeyError:
        return ''
    t = ET.fromstring(x)
    s = ''.join(e.text or '' for e in t.iter(W + 't')).strip()
    if t.iter(W + 'instrText'):
        ins = ' '.join((e.text or '') for e in t.iter(W + 'instrText')).strip()
        if ins: s = (s + ' {' + ins + '}').strip()
    return s
body = ET.fromstring(z.read('word/document.xml')).find(W + 'body')
secs, cur = [], []
def close(sp):
    fid = None
    if sp is not None:
        for fr in sp.findall(W + 'footerReference'):
            if fr.get(W + 'type') in (None, 'default'):
                fid = fr.get(R + 'id')
        start = sp.find(W + 'pgNumType')
        st = start.get(W + 'start') if start is not None else None
    else:
        st = None
    secs.append((footer_text(fid), st, '\n'.join(cur)))
for el in body:
    if el.tag == W + 'p':
        txt = ''.join(e.text or '' for e in el.iter(W + 't'))
        cur.append(txt)
        sp = el.find(W + 'pPr/' + W + 'sectPr')
        if sp is not None:
            close(sp); cur = []
    elif el.tag == W + 'tbl':
        cur.append(' | '.join(''.join(e.text or '' for e in c.iter(W + 't')) for c in el.iter(W + 'tc')))
    elif el.tag == W + 'sectPr':
        close(el); cur = []
with open(out, 'w', encoding='utf8') as f:
    for i, (ft, st, tx) in enumerate(secs, 1):
        f.write(f'\n[[sec {i} | pie: {ft} | start: {st}]]\n{tx}\n')
print(len(secs), 'secciones')
