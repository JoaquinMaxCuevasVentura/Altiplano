"""Exporta a la aplicación lo que la gramática toma del pie.

Uso (desde la raíz del repositorio):
    python3 tipografia/aplicacion/exportar.py

Escribe tipografia/aplicacion/datos.js: los 30 testigos del pie ya escalados al
azulejo (antes de achatar la altura de x), sus medidas, la razón de la foto, la
caja de 8 × 7, las recetas, los parámetros con su valor, su unidad y de dónde
salen, el poema y el azar de cada receta (los mismos quiebres y desvíos que en
Python, para que la aplicación y la simulación dibujen el mismo signo).

Con --prueba RUTA escribe además los cuerpos que dibuja Python, para comparar.
"""

import base64
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "simulacion"))

import gramatica  # noqa: E402
from comun import CELDAS, POEMA, T, TES, caja_tinta  # noqa: E402
from desenterrar import TESTIGOS, desenterrar, escalar_y_colocar, medidas  # noqa: E402

# los parámetros que se miden en canales: el factor con que salen del canal
EN_CANALES = dict(radio_chapa=0.6, asiento_ancho=2.0, asiento_alto=0.9, intemperie=0.12, alivio=0.28, gota_masa=1.25,
                  gota_caida=0.3, gota_cuello=0.55, cinta=1.0, punto=1.0)


class Grabadora:
    """Un azar que anota lo que sale, en orden: la aplicación lo repite tal cual."""

    def __init__(self, rng):
        self.rng, self.cinta = rng, []

    def choice(self, a):
        v = self.rng.choice(a)
        self.cinta.append(int(v))
        return v

    def normal(self, loc=0.0, scale=1.0):
        v = float(self.rng.normal(loc, scale))
        self.cinta.append(round((v - loc) / scale, 6))
        return v


def rle(m):
    """Corridas de una máscara recortada a su caja: fondo, tinta, fondo… en bytes (255 sigue)."""
    x0, y0, x1, y1 = (int(v) for v in caja_tinta(m))
    plano = m[y0:y1 + 1, x0:x1 + 1].ravel()
    cambios = np.flatnonzero(np.diff(plano.astype(np.int8))) + 1
    bordes = np.concatenate([[0], cambios, [len(plano)]])
    largos = list(np.diff(bordes))
    if plano[0]:
        largos = [0] + largos
    out = bytearray()
    for n in largos:
        n = int(n)
        while n >= 255:
            out.append(255)
            n -= 255
        out.append(n)
    return dict(x=x0, y=y0, w=x1 - x0 + 1, h=y1 - y0 + 1, rle=base64.b64encode(bytes(out)).decode())


def main():
    grabadas = {}
    azar_real = gramatica.azar

    def azar_grabado(*claves):
        g = Grabadora(azar_real(*claves))
        if claves[0] == "gramatica":
            grabadas[claves[1]] = g.cinta
        return g

    gramatica.azar = azar_grabado
    D = desenterrar()
    gramatica.azar = azar_real

    M, escala, base, _ = escalar_y_colocar(D["testigos"])
    med = medidas(M, base)
    pie = json.loads((TESTIGOS / "pie.json").read_text(encoding="utf8"))["tinta"]
    e, P = D["esqueleto"], D["parametros"]
    c = e["canal"]
    for k, f in EN_CANALES.items():
        assert abs(P[k]["valor"] - round(f * c, 1)) < 0.051, k
    parametros = []
    for k, p in P.items():
        parametros.append(dict(nombre=k, unidad=p["unidad"], que=p["que"], de_donde=p["de_donde"],
                               canales=EN_CANALES.get(k), fijo=None if k in EN_CANALES or k == "canal" else p["valor"]))
    datos = dict(
        T=T, TES=TES,
        base=float(base), escala=float(escala),
        medidas_sustituto={k: float(med[k]) for k in ("xh", "asc", "desc", "grueso", "fino")},
        razon_foto=round(pie["ascendente"] / pie["alto_x"], 4),
        razon_sustituto=round(med["asc"] / med["xh"], 4),
        foto=pie,
        testigos={s: rle(m) for s, m in M.items()},
        caja=[{k: c_[k] for k in ("signo", "estado", "celda", "fila", "columna", "testigos", "procedencia") if k in c_}
              for c_ in CELDAS],
        recetas={s: r for s, (_, r) in gramatica.RECETAS.items()},
        parametros=parametros,
        azar=grabadas,
        poema=POEMA.strip(),
    )
    texto = ("// Generado por tipografia/aplicacion/exportar.py: lo que la gramática toma del pie.\n"
             "window.DATOS = " + json.dumps(datos, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (AQUI / "datos.js").write_text(texto, encoding="utf8")
    print("datos.js:", round(len(texto.encode()) / 1024), "KB ·", len(datos["testigos"]), "testigos ·",
          len(grabadas), "recetas · razón de la foto", datos["razon_foto"])
    if "--prueba" in sys.argv:
        ruta = Path(sys.argv[sys.argv.index("--prueba") + 1])
        prueba = dict(esqueleto={k: v for k, v in e.items() if k != "cajas"}, cajas=e["cajas"],
                      parametros={k: p["valor"] for k, p in P.items()},
                      med={k: float(v) for k, v in D["med"].items()},
                      cuerpos={s: rle(v["mascara"]) for s, v in D["gramatica"].items()},
                      achatados={s: rle(m) for s, m in D["antes"].items()},
                      marcas={s: [[n, list(p)] for n, p in v["glifo"].marcas] for s, v in D["gramatica"].items()})
        ruta.write_text(json.dumps(prueba, ensure_ascii=False, default=float), encoding="utf8")
        print("prueba:", ruta)


if __name__ == "__main__":
    main()
