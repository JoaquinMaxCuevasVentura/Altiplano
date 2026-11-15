import re,sys,json,collections
t=open(sys.argv[1],encoding='utf-8',errors='replace').read().split('\f')
pairs=[]
for i,pg in enumerate(t):
    lines=[l.strip() for l in pg.split('\n') if l.strip()]
    for l in lines[:2]+lines[-2:]:
        for m in re.finditer(r'(?:^|\s)(\d{1,4})(?:\s|$)',l):
            c=int(m.group(1))
            if c<2000 or c>2100: pairs.append((i,c))
diffs=collections.Counter(c-i for i,c in pairs)
mode=diffs.most_common(3)
print('modas c-i:',mode,file=sys.stderr)
m=mode[0][0]
mp={}
for i,c in pairs:
    if abs((c-i)-m)<=6:   # tolerate local shifts (plates)
        mp.setdefault(str(c),i)
json.dump(mp,open(sys.argv[2],'w'))
print('mapeadas',len(mp),'de',len(t),file=sys.stderr)
