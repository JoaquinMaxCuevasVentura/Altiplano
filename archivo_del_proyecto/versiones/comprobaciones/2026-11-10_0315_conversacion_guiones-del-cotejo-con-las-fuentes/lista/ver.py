import re,sys,unicodedata
pages=open(sys.argv[1],encoding='utf-8',errors='replace').read().split('\f')
def norm(s):
    s=unicodedata.normalize('NFC',s).replace('­','')
    s=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',s)
    return re.sub(r'\s+',' ',s)
for arg in sys.argv[2:]:
    pg,q=arg.split('|',1)
    idx=[int(x)-1 for x in pg.split(',')]
    t=' '.join(norm(pages[i]) for i in idx)
    words=re.findall(r'\w+',q)
    pat=r'\W+'.join(re.escape(w) for w in words)
    m=re.search(pat,t,re.I)
    print(f'p.{pg} ART «{q}»\n      FUE «{t[max(0,m.start()-25):m.end()+5] if m else "NO ENCONTRADO"}»')
