"""Aplica pares (viejo, nuevo) a un archivo y lo guarda: python3 reemplazar.py archivo pares.py"""
import pathlib, runpy, sys
ruta = pathlib.Path(sys.argv[1])
pares = runpy.run_path(sys.argv[2])["PARES"]
s = ruta.read_text(encoding="utf8")
for viejo, nuevo in pares:
    n = s.count(viejo)
    if n != 1:
        sys.exit(f"no está una sola vez ({n}): {viejo[:120]!r}")
    s = s.replace(viejo, nuevo)
ruta.write_text(s, encoding="utf8")
print(f"{ruta.name}: {len(pares)} cambios guardados")
