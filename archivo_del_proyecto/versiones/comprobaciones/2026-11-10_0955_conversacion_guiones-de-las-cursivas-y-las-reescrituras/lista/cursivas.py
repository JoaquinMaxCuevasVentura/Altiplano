"""Pone en cursiva las voces aymaras fuera de citas, bloques, rutas y bibliografía.
Dentro de un tramo ya en cursiva, aplica la cursiva inversa (la voz va en redonda)."""
import re,sys,pathlib
VOCES=r"(?:ayllus?|chujllas?|apachetas?|huacas?|yatiris?|achachis?|pututus?|[Jj]ilakatas?|Ayllu|Chujlla|Apacheta)"
WORD=re.compile(r'(?<![\w\'’*])('+VOCES+r')(?![\w\'’])')
f=pathlib.Path(sys.argv[1]); t=f.read_text(encoding='utf-8')
head,bib=t.split('## Bibliografía',1)
out=[];cambios=[]
skip_block=False
for line in head.split('\n'):
    s=line.lstrip()
    if s.startswith('>') or s.startswith('![') or s.startswith(':::') or s.startswith('**Palabras clave') or s.startswith('**Keywords') or s.startswith('[^autor]'):
        out.append(line); continue
    # segmentar: citas «» protegidas; seguir estado de cursiva (* simple, no **)
    res=[];i=0;depth=0;ital=False;buf=''
    def flush():
        global buf
    segs=[]  # (texto, protegido, en_cursiva)
    cur='';prot=False
    n=len(line)
    while i<n:
        ch=line[i]
        if ch=='«':
            if depth==0:
                segs.append((cur,False,ital)); cur=''
            depth+=1; cur+=ch; i+=1; continue
        if ch=='»' and depth>0:
            depth-=1; cur+=ch; i+=1
            if depth==0: segs.append((cur,True,ital)); cur=''
            continue
        if depth==0 and ch=='*':
            if line.startswith('**',i):
                segs.append((cur,False,ital)); segs.append(('**',True,ital)); cur=''; i+=2; continue
            segs.append((cur,False,ital)); segs.append(('*',True,ital)); cur=''; ital=not ital; i+=1; continue
        cur+=ch; i+=1
    segs.append((cur,depth>0,ital))
    new=''
    for txt,p,it in segs:
        if p or not txt: new+=txt; continue
        if not it:
            def rep(m): cambios.append(m.group(1)); return '*'+m.group(1)+'*'
            new+=WORD.sub(rep,txt)
        else:
            def rep2(m): cambios.append('inv:'+m.group(1)); return '*'+m.group(1)+'*'
            new+=WORD.sub(rep2,txt)   # dentro de cursiva: cerrar y reabrir
    out.append(new)
t2='\n'.join(out)+'## Bibliografía'+bib
# limpiar marcas vacías como "**" creadas por cursiva inversa al borde de un tramo: "* *" no se generan; revisar "**" pegados
f.write_text(t2,encoding='utf-8')
import collections; print(collections.Counter(cambios))
