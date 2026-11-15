"""Cuenta tipos de cita por sección: directas (comillas con referencia), en bloque,
referencias parentéticas (Autor, año: p) y narrativas Autor (año: p), referencias sin comillas (paráfrasis)."""
import re,sys,collections
md=open(sys.argv[1],encoding='utf-8').read().split('## Bibliografía')[0]
md=re.sub(r'(?s)::: \{custom-style="(Figura|Pie de figura)"\}.*?:::','',md)
secs=re.split(r'\n(?=## )',md)
def words(s): return len(re.findall(r'\w+',s))
tot=collections.Counter()
for s in secs:
    title=s.split('\n',1)[0][:45]
    paras=[p for p in re.split(r'\n\s*\n',s) if p.strip() and not p.startswith('#') and not p.startswith('|')]
    c=collections.Counter()
    for p in paras:
        if p.lstrip().startswith('>'): c['bloque']+=1; continue
        q=re.findall(r'«[^«»]*(?:«[^«»]*»[^«»]*)*»',p)
        c['comillas']+=len(q)
        c['palabras_citadas']+=sum(words(x) for x in q)
        refs=re.findall(r'\(([^()]*?(?:ibid\.|\d{4}[a-z]?(?: \[\d{4}\])?)[^()]*)\)',p)
        for r in refs:
            for seg in r.split(';'):
                seg=seg.strip()
                if seg.startswith('ibid') or re.match(r'[A-ZÁÉÍÓÚ].+,\s*\d{4}',seg): c['parentetica']+=1
                elif re.match(r'^\d{4}',seg): c['narrativa']+=1
        c['palabras']+=words(re.sub(r'\([^()]*\)','',p))
        # paragraphs with references but no quotes
        if refs and not q: c['parr_parafrasis']+=1
    tot+=c
    print(f"{title:45} pal={c['palabras']:5} «»={c['comillas']:3} ({c['palabras_citadas']:4} pal) bloque={c['bloque']} parent={c['parentetica']:3} narr={c['narrativa']:2} parr_sin_comillas={c['parr_parafrasis']}")
print('TOTAL',dict(tot))
