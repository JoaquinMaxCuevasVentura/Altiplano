"""Coteja citas contra el texto de una fuente paginada.
uso: cotejo.py citas.json fuente.txt 'Clave fuente' offset [pdfpage_de_impresa.json]"""
import re,sys,json,difflib,unicodedata
rows=json.load(open(sys.argv[1],encoding='utf-8'))
pages=open(sys.argv[2],encoding='utf-8',errors='replace').read().split('\f')
key=sys.argv[3]; off=int(sys.argv[4])
pmap=json.load(open(sys.argv[5])) if len(sys.argv)>5 else None
def pdfidx(p):  # printed page (str) -> list index
    if pmap: return pmap.get(str(p))
    try: return int(p)+off-1
    except: return None
def norm(s,keep_hyph=False):
    s=unicodedata.normalize('NFC',s)
    s=s.replace('­','')
    s=re.sub(r'(\w)-\s*\n\s*(\w)', (r'\1-\2' if keep_hyph else r'\1\2'), s)
    s=re.sub(r'[“”"«»„]','"',s); s=re.sub(r"[‘’`´]","'",s)
    s=s.replace('…','...')
    s=re.sub(r'\s+',' ',s)
    return s.strip()
def loose(s):
    s=norm(s).lower()
    s=re.sub(r'[^\w ]','',s); return re.sub(r'\s+',' ',s)
def expand(pg):
    out=[]
    for part in re.split(r',\s*',pg or ''):
        part=part.strip()
        m=re.match(r'^(\d+)-(\d+)$',part)
        if m: out+=list(range(int(m.group(1)),int(m.group(2))+1))
        elif re.match(r'^\d+$',part): out.append(int(part))
        elif re.match(r'^[ivxlc]+$',part): out.append(part)
    return out
def text_of(idxs,keep):
    return ' '.join(norm(pages[i],keep) for i in idxs if i is not None and 0<=i<len(pages))
res={'ok':0,'otra_pagina':[],'no':[]}
for r in rows:
    if not r['fuente'] or not r['fuente'].startswith(key): continue
    q=r['cita']
    if q.startswith('BLOQUE'): continue
    frags=[f.strip(' .,;:') for f in re.split(r'\[\.\.\.\]|\[…\]',q) if f.strip(' .,;:')]
    pgs=expand(r['pagina'])
    idxs=[pdfidx(p) for p in pgs]
    allbad=[]
    for f in frags:
        fn=norm(f)
        hit=False
        for keep in (False,True):
            if fn in text_of(idxs,keep): hit=True;break
        if hit: continue
        # other pages
        found=[i for i in range(len(pages)) if fn in norm(pages[i]) or fn in norm(pages[i],True)]
        # across page boundary
        if not found:
            for i in range(len(pages)-1):
                if fn in text_of([i,i+1],False) or fn in text_of([i,i+1],True): found=[i,i+1];break
        if found and any(i in idxs for i in found): continue
        if found: allbad.append(('OTRA',f,found)); continue
        # loose
        lf=loose(f); lt=loose(text_of(idxs,False))
        if lf and lf in lt: allbad.append(('LOOSE',f,None)); continue
        # closest
        t=text_of([i for i in idxs if i is not None],False)
        best=('',0)
        L=len(fn)
        for st in range(0,max(1,len(t)-L+1),3):
            w=t[st:st+L]; sc=difflib.SequenceMatcher(None,fn,w).ratio()
            if sc>best[1]: best=(w,sc)
        allbad.append(('NO',f,best))
    if not allbad: res['ok']+=1
    else:
        for kind,f,info in allbad:
            print(f"[{kind}] p.{r['pagina']} «{f}»", '→', info if kind!='NO' else f"más parecido ({info[1]:.2f}): «{info[0]}»")
print('OK:',res['ok'])
