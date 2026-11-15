"""Asigna cada cita («...» y bloques >) a su fuente y página. Entiende citas
parentéticas (Autor, año: p), narrativas Autor (año: p) e ibid. Para cada cita
usa la referencia parentética que la sigue en la misma oración; si no hay, la
narrativa anterior en la misma oración; si no, la siguiente del párrafo.
uso: citas2.py articulo.md salida.json"""
import re,sys,json
md=open(sys.argv[1],encoding='utf8').read().split('## Bibliografía')[0]
md=re.sub(r'(?s)::: \{custom-style="Figura"\}.*?:::','',md)
paras=[p for p in re.split(r'\n\s*\n',md) if p.strip()]
YEAR=r'\d{4}[a-z]?(?: \[\d{4}\])?'
NAME=r"(?:[A-ZÁÉÍÓÚÑ][\w'’\-]+(?: (?:de la|de|y|et al\.|[A-ZÁÉÍÓÚÑ][\w'’\-]+))*)"
NARR=re.compile(r'('+NAME+r') \(('+YEAR+r')(?::\s*([^)]*))?\)')
PAR=re.compile(r'\(([^()]*?(?:ibid\.|\b1\d{3}|\b20\d\d)[^()]*)\)')
ALIAS={'Fernando Freitas Fuão':'Fuão','Tim Ingold':'Ingold','Juhani Pallasmaa':'Pallasmaa','Kenneth Frampton':'Frampton',
 'Antonio Cornejo Polar':'Cornejo Polar','René Zavaleta Mercado':'Zavaleta Mercado','Pierre Duviols':'Duviols','Carolyn Dean':'Dean',
 'Javier Seguí de la Riva':'Seguí de la Riva','Simon Lundberg':'Lundberg','Abbie Garrington':'Garrington','James C. Scott':'Scott',
 'Alexander y su equipo':'Alexander et al.','Alexander':'Alexander et al.','Rivera Cusicanqui':'Rivera Cusicanqui','Monteys y Fuertes':'Monteys y Fuertes',
 'Seguí':'Seguí de la Riva','Cárcamo Pino':'Cárcamo Pino'}
def canon(n):
    n=n.strip()
    for k,v in ALIAS.items():
        if n.endswith(k): return v
    return n
def sentences(p):
    q=p.replace('ibid.','ibid§').replace('et al.','et al§').replace('s. p.','s§ p§').replace('n. ','n§ ').replace('cit. en','cit§ en')
    out=[];start=0
    for m in re.finditer(r'[.!?»]\s+(?=[A-ZÁÉÍÓÚ«¿¡(])',q):
        out.append((start,m.end())); start=m.end()
    out.append((start,len(q)))
    return out
def quotes(p):
    res=[];depth=0;cur='';st=0
    for i,ch in enumerate(p):
        if ch=='«':
            depth+=1
            if depth==1: cur='';st=i;continue
        if ch=='»':
            depth-=1
            if depth==0: res.append((st,cur));continue
        if depth>=1: cur+=ch
    return res
last=None; lastpage=''; rows=[]
for p in paras:
    blk=p.lstrip().startswith('>')
    ev=[]
    for m in PAR.finditer(p):
        ev.append((m.start(),'par',m.group(1)))
    for m in NARR.finditer(p):
        if p[m.start():m.start()+1]=='(' : continue
        ev.append((m.start(),'narr',(canon(m.group(1))+' '+m.group(2),(m.group(3) or '').strip())))
    ev.sort()
    sents=sentences(p)
    def sent_of(i):
        for k,(a,b) in enumerate(sents):
            if a<=i<b: return k
        return len(sents)-1
    resolved=[]
    for pos,kind,val in ev:
        if kind=='narr':
            last=val[0]; lastpage=val[1]; resolved.append((pos,'narr',val[0],val[1])); continue
        for s in [x.strip() for x in val.split(';')]:
            if s.startswith(('Imagen','Figura')): continue
            if 'cit. en' in s:
                a,b=s.split('cit. en',1); b=b.strip()
                cont=last if b.startswith('ibid') else (lambda mm: (mm.group(1)+' '+mm.group(2)) if mm else b)(re.match(r'(.+?),\s*('+YEAR+')',b))
                ma=re.match(r'(.+?),\s*('+YEAR+r')(?::\s*(.+))?',a.strip().rstrip(','))
                resolved.append((pos,'par',(ma.group(1)+' '+ma.group(2)) if ma else a.strip(),(ma.group(3) or '').strip().rstrip(',') if ma else ''))
                last=cont; continue
            if s.startswith('ibid'):
                mm=re.match(r'ibid\.(?::\s*(.+))?',s); pg=mm.group(1) if mm and mm.group(1) else lastpage; lastpage=pg; resolved.append((pos,'par',last,pg)); continue
            mm=re.match(r'(.+?),\s*('+YEAR+r')(?::\s*(.+))?$',s)
            if mm: last=mm.group(1)+' '+mm.group(2); lastpage=mm.group(3) or ''; resolved.append((pos,'par',last,mm.group(3) or ''))
    qs=quotes(p)
    if blk:
        b=re.sub(r'^\s*>\s?','',p,flags=re.M); qs=[(0,'BLOQUE: '+PAR.sub('',b).strip()[:80])]
    for qi,q in qs:
        k=sent_of(qi)
        after=[r for r in resolved if r[0]>qi and r[1]=='par' and sent_of(r[0])==k]
        before=[r for r in resolved if r[0]<qi and r[1]=='narr' and sent_of(r[0])==k]
        if after: r=after[0]
        elif before: r=before[-1]
        else:
            nxt=[r for r in resolved if r[0]>qi]
            r=nxt[0] if nxt else (None,None,'SIN-REFERENCIA','')
        rows.append({'cita':re.sub(r'\s+',' ',q).strip(),'fuente':r[2],'pagina':(r[3] or '').strip()})
json.dump(rows,open(sys.argv[2],'w',encoding='utf8'),ensure_ascii=False,indent=0)
print(len(rows),'citas;',sum(r['fuente']=='SIN-REFERENCIA' for r in rows),'sin referencia')
