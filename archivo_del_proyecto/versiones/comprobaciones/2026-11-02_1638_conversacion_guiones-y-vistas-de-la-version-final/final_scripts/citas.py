"""Asigna cada cita del artículo («...» y bloques >) a la fuente y la página de
la referencia que la sigue en el mismo párrafo, resolviendo los ibid.
Uso: python3 -I citas.py articulo.md [salida.json]"""
import re, sys, json
md = open(sys.argv[1], encoding='utf8').read()
md = md.split('## Bibliografía')[0]
md = re.sub(r'(?s)::: \{custom-style="Figura"\}.*?:::', '', md)
paras = [p for p in re.split(r'\n\s*\n', md) if p.strip()]
CIT = re.compile(r'\(([^()]*?(?:ibid\.|\b1\d{3}|\b20\d\d)[^()]*)\)')
def quotes(p):
    out, depth, cur = [], 0, ''
    for ch in p:
        if ch == '«':
            depth += 1
            if depth == 1: cur = ''; continue
        if ch == '»':
            depth -= 1
            if depth == 0: out.append(cur); continue
        if depth >= 1: cur += ch
    return out
last = None; lastpage = None; rows = []
for p in paras:
    items = []
    for m in CIT.finditer(p):
        items.append((m.start(), m.group(1)))
    qs = []
    pos = 0
    for q in quotes(p):
        i = p.find('«' + q, pos); qs.append((i, q)); pos = i + 1
    if p.lstrip().startswith('>'):
        blk = re.sub(r'^\s*>\s?', '', p, flags=re.M)
        blk = CIT.sub('', blk).strip()
        qs.append((0, 'BLOQUE: ' + blk[:90]))
    resolved = []
    for start, c in items:
        segs = [s.strip() for s in c.split(';')]
        src = pg = None
        for s in segs:
            if s.startswith('Imagen') or s.startswith('Figura'): continue
            if 'cit. en' in s:
                a, b = s.split('cit. en', 1)
                b = b.strip()
                if b.startswith('ibid'):
                    container = last
                else:
                    mm = re.match(r'(.+?),\s*(\d{4}[a-z]?(?: \[\d{4}\])?)', b)
                    container = (mm.group(1) + ' ' + mm.group(2)) if mm else b
                ma = re.match(r'(.+?),\s*(\d{4}[a-z]?(?: \[\d{4}\])?)(?::\s*(.+))?', a.strip().rstrip(','))
                src = (ma.group(1) + ' ' + ma.group(2)) if ma else a.strip()
                pg = (ma.group(3) or '').strip().rstrip(',') if ma else ''
                last = container
                continue
            if s.startswith('ibid'):
                mm = re.match(r'ibid\.(?::\s*(.+))?', s)
                src = last; pg = mm.group(1) if mm and mm.group(1) else lastpage
            else:
                mm = re.match(r'(.+?),\s*(\d{4}[a-z]?(?: \[\d{4}\])?)(?::\s*(.+))?$', s)
                if mm:
                    src = mm.group(1) + ' ' + mm.group(2); pg = mm.group(3)
                else:
                    mm = re.match(r'(\d{4}[a-z]?(?: \[\d{4}\])?)(?::\s*(.+))?$', s)
                    if mm: src = 'AUTOR-EN-TEXTO ' + mm.group(1); pg = mm.group(2)
                    else: continue
                last = src
            lastpage = pg
        resolved.append((start, src, pg))
    for qi, q in qs:
        nxt = [r for r in resolved if r[0] > qi]
        src, pg = (nxt[0][1], nxt[0][2]) if nxt else ('SIN-REFERENCIA', None)
        rows.append({'cita': re.sub(r'\s+', ' ', q).strip(), 'fuente': src, 'pagina': (pg or '').strip()})
if len(sys.argv) > 2:
    json.dump(rows, open(sys.argv[2], 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(rows), 'citas;', sum(r['fuente'] == 'SIN-REFERENCIA' for r in rows), 'sin referencia en el párrafo')
