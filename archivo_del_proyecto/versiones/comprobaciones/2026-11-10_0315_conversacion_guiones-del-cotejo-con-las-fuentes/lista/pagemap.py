import re,sys
# usage: pagemap.py file.txt  -> for each pdf page, candidate printed page numbers from first/last 3 non-empty lines
t=open(sys.argv[1],encoding='utf-8',errors='replace').read().split('\f')
for i,pg in enumerate(t,1):
    lines=[l.strip() for l in pg.split('\n') if l.strip()]
    cand=[]
    for l in lines[:3]+lines[-3:]:
        for m in re.finditer(r'(?:^|\s)(\d{1,4}|[ivxlc]{1,6})(?:\s|$)',l):
            cand.append(m.group(1))
    head=(lines[0][:70] if lines else '')
    print(i,'|',' '.join(cand[:6]),'|',head)
