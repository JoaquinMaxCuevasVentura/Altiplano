import re,sys,collections
t=open(sys.argv[1],encoding='utf-8').read()
t=t.split('## Bibliografía')[0]
# citation tokens: "Author, year: pages" or "Author, year" or "ibid.: pages" / "ibid."
pat=re.compile(r"(ibid\.(?::\s*([^);\]]+))?)|([A-ZÁÉÍÓÚ][\w'’ÁÉÍÓÚáéíóúñçãõ\.\- ]+?(?: y [A-ZÁÉÍÓÚ][\w\- ]+)?(?:\+The Voidz)?),\s*(\d{4}[ab]?(?: \[\d{4}\])?)(?::\s*([^);\]]+))?")
last=None
res=collections.defaultdict(set)
for par in t.split('\n'):
    for m in re.finditer(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)",par):
        inner=m.group(1)
        for part in re.split(r";\s*",inner):
            part=part.strip()
            mm=re.search(r"cit\. en (.*)",part)
            if mm: part=mm.group(1)
            if part.startswith('ibid.'):
                pg=part[5:].lstrip(':').strip()
                if last: res[last].add(pg or '(misma)')
                continue
            m2=re.match(r"([A-ZÁÉÍÓÚ][^,]+?),\s*(\d{4}[ab]?(?: \[\d{4}\])?)(?::\s*(.+))?$",part)
            if m2:
                last=(m2.group(1).strip(),m2.group(2))
                res[last].add((m2.group(3) or '').strip())
    # prose form: Author (year: pages)
for k in sorted(res):
    print(k[0],'|',k[1],'|',', '.join(sorted(p for p in res[k] if p)))
