#!/usr/bin/env python3
"""Revisa las láminas en SVG (planos, taxonomía): busca textos encimados entre sí y líneas que cruzan un texto sin halo.

Uso (desde la raíz del repositorio):
    python3 tipografia/planos/revisar_encimados.py tipografia/planos/svg/*.svg

Mide cada texto con las mismas tablas de anchos que usa el dibujo (dibujo.MEDIR) y respeta los recortes.
Es una revisión, no una prueba: lo que encuentra hay que mirarlo.
"""
import math, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import Polygon, LineString
from shapely import affinity
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dibujo import MEDIR, MONO, SERIF

NS = "{http://www.w3.org/2000/svg}"
def num(s, d=0.0):
    try: return float(s)
    except (TypeError, ValueError): return d

def textos_y_lineas(ruta):
    raiz = ET.parse(ruta).getroot()
    T, L = [], []
    clips = {}
    for c in raiz.iter(NS + "clipPath"):
        r = c.find(NS + "rect")
        if r is not None:
            x, y, w, h = (num(r.get(k)) for k in ("x", "y", "width", "height"))
            clips[c.get("id")] = Polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
    def pon(ln, color, w, clip):
        if clip is not None:
            ln = ln.intersection(clip)
            if ln.is_empty: return
        for g in (ln.geoms if hasattr(ln, "geoms") else [ln]):
            if g.geom_type == "LineString": L.append((g, color, w))
    def anda(e, clip=None):
        tag = e.tag.replace(NS, "")
        if tag in ("defs", "clipPath", "pattern", "style"): return
        m = re.match(r"url\(#(.+)\)", e.get("clip-path", ""))
        if m and m.group(1) in clips: clip = clips[m.group(1)]
        if tag == "text":
            x, y, tam = num(e.get("x")), num(e.get("y")), num(e.get("font-size"), 2.5)
            fam = e.get("font-family", SERIF); ancla = e.get("text-anchor", "start")
            partes = [(e.text or "", e)] + [(t.text or "", t) for t in e]
            w = 0.0
            for s, el in partes:
                peso = int(num(el.get("font-weight") or e.get("font-weight"), 400))
                cur = (el.get("font-style") or e.get("font-style")) == "italic"
                w += MEDIR.ancho(s, tam, fam, peso, cur)
            w += num(e.get("letter-spacing")) * len("".join(s for s, _ in partes))
            s = "".join(p for p, _ in partes).strip()
            if not s or w < 0.3: return
            x0 = x if ancla == "start" else x - w if ancla == "end" else x - w / 2
            p = Polygon([(x0, y - 0.72 * tam), (x0 + w, y - 0.72 * tam), (x0 + w, y + 0.2 * tam), (x0, y + 0.2 * tam)])
            m = re.match(r"rotate\(([-\d.]+) ([-\d.]+) ([-\d.]+)\)", e.get("transform", ""))
            if m: p = affinity.rotate(p, float(m.group(1)), origin=(float(m.group(2)), float(m.group(3))))
            T.append(dict(s=s, p=p, halo=e.get("paint-order") == "stroke", tam=tam, fill=e.get("fill")))
            return
        if tag == "line" and e.get("stroke") not in (None, "none"):
            pon(LineString([(num(e.get("x1")), num(e.get("y1"))), (num(e.get("x2")), num(e.get("y2")))]), e.get("stroke"), num(e.get("stroke-width"), 0.2), clip)
        if tag == "path" and e.get("stroke") not in (None, "none") and e.get("fill") in (None, "none"):
            d = e.get("d", "")
            if re.fullmatch(r"[MLHVZ\d\s,.\-e]+", d):
                pts, cx, cy = [], 0, 0
                for c, args in re.findall(r"([MLHVZ])([^MLHVZ]*)", d):
                    v = [float(a) for a in re.findall(r"-?[\d.]+(?:e-?\d+)?", args)]
                    if c in "ML":
                        for i in range(0, len(v) - 1, 2): cx, cy = v[i], v[i + 1]; pts.append((cx, cy))
                    elif c == "H" and v: cx = v[-1]; pts.append((cx, cy))
                    elif c == "V" and v: cy = v[-1]; pts.append((cx, cy))
                if len(pts) >= 2: pon(LineString(pts), e.get("stroke"), num(e.get("stroke-width"), 0.2), clip)
        for h in e: anda(h, clip)
    anda(raiz)
    return T, L

for ruta in sys.argv[1:]:
    T, L = textos_y_lineas(ruta)
    hallazgos = []
    for i, a in enumerate(T):
        for b in T[i + 1:]:
            if a["p"].intersects(b["p"]):
                ar = a["p"].intersection(b["p"]).area
                if ar > 0.12 * min(a["p"].area, b["p"].area):
                    hallazgos.append(f"  texto sobre texto: «{a['s'][:38]}» ✕ «{b['s'][:38]}»  @ {a['p'].centroid.x:.0f},{a['p'].centroid.y:.0f}")
    for t in T:
        if t["halo"]: continue
        nucleo = t["p"].buffer(-0.22 * t["tam"])
        if nucleo.is_empty: continue
        for ln, color, w in L:
            if ln.length < 3 or w > 0.6: continue
            if ln.intersects(nucleo) and ln.intersection(nucleo).length > 0.5 * t["tam"]:
                hallazgos.append(f"  línea sobre texto: «{t['s'][:44]}»  @ {t['p'].centroid.x:.0f},{t['p'].centroid.y:.0f} (trazo {w})")
                break
    print(f"{Path(ruta).name}: {len(T)} textos, {len(hallazgos)} hallazgos")
    for h in hallazgos: print(h)
