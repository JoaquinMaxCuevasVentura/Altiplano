"""Mide en un .md del artículo algunos rasgos que la bibliografía asocia con la
redacción de IA. Uso: python3 -I patrones.py articulo.md"""
import re, sys, statistics
t = open(sys.argv[1], encoding='utf8').read()
t = t.split('## Bibliografía')[0]
t = re.sub(r'(?s)::: \{custom-style="Figura"\}.*?:::', '', t)
t = re.sub(r'(?m)^\|.*$', '', t)                       # tablas
t = re.sub(r'(?m)^#.*$', '', t)                        # títulos
t = re.sub(r'\[\^[a-z]+\]:?', '', t)
body = re.sub(r'«[^»]*»', 'CITA', t)                   # la prosa propia, sin citas
body = re.sub(r'\((?:ibid|cit\.|[^()]*\d{4})[^()]*\)', '', body)      # sin referencias
body = re.sub(r'\(\d+\)', '', body)
paras = [p.strip() for p in body.split('\n\n') if len(p.split()) > 25]
sents = [s for p in paras for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚ¿«*(])', p) if s.strip()]
lens = [len(s.split()) for s in sents]
words = sum(lens)
def n(rx): return len(re.findall(rx, body))
print(f'párrafos {len(paras)}, oraciones {len(sents)}, palabras de prosa propia {words}')
print(f'largo medio de oración {statistics.mean(lens):.1f}; mediana {statistics.median(lens)}; '
      f'cortas (≤10) {sum(l <= 10 for l in lens)/len(lens):.0%}; largas (≥35) {sum(l >= 35 for l in lens)/len(lens):.0%}')
print('por 1.000 palabras:')
for name, rx in [
  ('«no … sino»', r'\bno\b[^.;:]{0,80}\bsino\b'),
  ('«no es …, es …» / «no …: …»', r'\bno (?:es|son|era|fue)\b[^.;]{0,60}[,;:] (?:es|son|era|fue)\b'),
  ('«No es/No se trata/no … sino» al inicio', r'(?:^|[.!?] )No (?:es|son|se trata|todo|hay que|lo)\b'),
  ('dos puntos', r':'),
  ('punto y coma', r';'),
  ('paréntesis (sin referencias)', r'\('),
  ('oración que empieza con «Y»', r'(?:^|[.!?] )Y '),
  ('oración que empieza con «Pero»', r'(?:^|[.!?] )Pero '),
  ('«también»', r'\btambién\b'), ('«además»', r'\bademás\b'), ('«en cambio»', r'\ben cambio\b'),
  ('«es decir» / «o sea»', r'\b(?:es decir|o sea)\b'),
  ('«clave/crucial/fundamental»', r'\b(?:clave|crucial|fundamental)\b'),
  ('«a espaldas de»', r'a espaldas de'),
  ('series de tres «A, B y C»', r'\b\w+, \w+ y \w+\b'),
]:
    print(f'  {name:38s} {n(rx):4d}  ({1000*n(rx)/words:.1f})')
endings = [re.split(r'(?<=[.!?])\s+', p)[-1] for p in paras]
short_end = [e for e in endings if len(e.split()) <= 12]
print(f'párrafos que cierran con una frase de ≤12 palabras: {len(short_end)}/{len(paras)}')
