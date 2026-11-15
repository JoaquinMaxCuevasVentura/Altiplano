import re,sys,unicodedata
b=sys.argv[1]
t=open(b,encoding='utf-8',errors='replace').read().split('\f')
def N(s): s=unicodedata.normalize('NFKC',s); s=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',s); return re.sub(r'\s+',' ',s)
for ph in sys.argv[2:]:
    words=re.findall(r'\w+',ph)
    pat=r'\W+'.join(re.escape(w) for w in words)
    hits=[]
    for i,p in enumerate(t):
        s=N(p); 
        for m in re.finditer(pat,s,re.I):
            lines=[l.strip() for l in p.split('\n') if l.strip()]
            pie=' / '.join(x[-30:] for x in (lines[:1]+lines[-1:]))
            hits.append(f'pdf{i+1} «{s[max(0,m.start()-150):m.end()+150]}» [{pie}]')
    print(f'«{ph}»:', '\n    '.join(hits[:4]) if hits else 'NO')
