"""Piloto paramétrico de E6, la pirwa: un depósito de champa sobre dos apoyos de piedra, con una V volada entre ellos.

Cambian lo que vuela cada hilada de la V y el alto del depósito. Lo demás es la lámina 6: una planta de 3,0 × 1,6 m,
muros de champa de 25 cm, bloques de 40 × 25 × 12 cm, apoyos de 0,9 m con una laja encima y un hueco de 1,0 m entre
ellos, que la V cierra hilada a hilada hasta dejar 6 cm o menos. En la clave va la trampa, y encima, el piso de palos.
El techo es de un agua: el lado bajo queda un metro por debajo del alto.
Las reglas:
    V  la champa vuela lo que aguanta con la cola cargada, en los escenarios de la prueba 3;
    P  bajo la trampa se está de pie: la clave queda a 1,70 m o más, el alto que se usa en E5 (proyecto);
    E  el lado alto no pasa de 4,6 m, el que aceptó el autor al bajarla un metro, hasta que se pruebe uno mayor.
Mide lo que se guarda, los bloques de champa y las hiladas de la V. Se corre desde la raíz:
python3 chhaxwa/parametrico/pirwa_e6.py
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402

X, Y, HP, LAJA, G = 1.5, 0.8, 0.9, 0.05, 0.5                # media planta, apoyos y medio hueco (proyecto)
BH, BA, BL, CIERRE, PISO = 0.12, 0.25, 0.40, 0.03, 0.12     # el bloque de champa y el piso de palos (proyecto)
CABEZA, ALTO_MAX, DESNIVEL = 1.70, 4.6, 1.0
VUELOS = [round(0.04 + 0.01 * k, 2) for k in range(10)]    # de 4 a 13 cm
ALTOS = [round(3.6 + 0.2 * k, 1) for k in range(10)]       # lado alto, de 3,6 a 5,4 m
ACTUAL = (0.06, 4.6)


def variante(vv, Hh):
    z0 = HP + LAJA
    n = math.ceil((G - CIERRE) / vv - 1e-9) - 1             # las hiladas de la V, como en la lámina 6
    huecos = [G - vv * (i + 1) for i in range(n)]
    clave = z0 + n * BH
    Hl = Hh - DESNIVEL
    medio = (Hl + Hh) / 2
    guardado = (2 * X - 2 * BA) * (2 * Y - 2 * BA) * max(0.0, medio - 0.1 - clave - PISO)
    largos = 0.0
    for alto_muro in (Hl, Hh):                               # los dos muros largos, con la V abajo
        k = 0
        while z0 + k * BH < alto_muro - 1e-9:
            largos += (2 * X - 2 * huecos[k]) if k < n else 2 * X
            k += 1
    cortos = 2 * (2 * Y - 2 * BA) * math.ceil((medio - z0) / BH - 1e-9)
    bloques = (largos + cortos) / BL
    v = dict(vuelo=vv, alto=Hh, bajo=Hl, medio=medio, hiladas=n, huecos=huecos, clave=clave, guardado=guardado,
             bloques=bloques, z0=z0)
    v["falla"] = ("P" if clave < CABEZA - 1e-9 else "") + ("E" if Hh > ALTO_MAX + 1e-9 else "")
    v["escenarios"] = [not v["falla"] and vv <= f * BL + 1e-9 for _, f in P.FRACCIONES]
    return v


def barrer():
    return [variante(vv, Hh) for Hh in ALTOS for vv in VUELOS]


def buscar(vs, vv, Hh):
    return next(x for x in vs if (x["vuelo"], x["alto"]) == (vv, Hh))


def elegir(vs):
    """La que más guarda si la champa vuela un tercio."""
    return max([x for x in vs if x["escenarios"][1]], key=lambda x: (round(x["guardado"], 4), x["vuelo"]))


def seccion(L, v, o):
    ox, oz = o
    z0, clave, Hm = v["z0"], v["clave"], v["medio"]

    def m(pts):
        return [(ox + x, oz + z) for x, z in pts]
    L.cortado(m([(-X - 0.1, 0), (-G, 0), (-G, HP), (-X - 0.1, HP)]), "P_LLENO", juntas=False)
    L.cortado(m([(0.0, 0), (2.0, 0), (1.55, HP), (0.45, HP)]), "P_LLENO", juntas=False)
    for a, b in ((-X - 0.1, -G), (G, X + 0.1)):
        L.cortado(m([(a, HP), (b, HP), (b, z0), (a, z0)]), "L_LLENO", juntas=False)
    der = []
    for i, w in enumerate(v["huecos"]):
        der += [(w, z0 + i * BH), (w, z0 + (i + 1) * BH)]
    izq = [(-x, z) for x, z in der[::-1]]
    L.cortado(m([(X, z0)] + der + izq + [(-X, z0), (-X, clave + PISO), (X, clave + PISO)]), "C_LLENO", juntas=False)
    for s in (-1, 1):
        L.cortado(m([(s * X, clave + PISO), (s * (X - BA), clave + PISO), (s * (X - BA), Hm), (s * X, Hm)]), "C_LLENO",
                  juntas=False)
    L.cortado(m([(-X + BA, clave + PISO), (X - BA, clave + PISO), (X - BA, Hm - 0.1), (-X + BA, Hm - 0.1)]), "PAJA_LLENO",
              juntas=False)
    L.cortado(m([(-X - 0.25, Hm), (X + 0.25, Hm), (X + 0.25, Hm + 0.08), (-X - 0.25, Hm + 0.08)]), "L_LLENO", juntas=False)
    L.linea([(ox - 2.1, oz), (ox + 2.4, oz)], "TERRENO")


def textos(v):
    return [f"clave a {P.coma(v['clave'])} m; {v['hiladas']} hiladas en la V",
            f"guarda {P.coma(v['guardado'], 1)} m³; {round(v['bloques'] / 10) * 10} bloques",
            P.estado(v)]


def main():
    vs = barrer()
    P.escribir_csv("e6_variantes", [
        ("vuelo_m", "vuelo", 3), ("lado_alto_m", "alto", 2), ("lado_bajo_m", "bajo", 2), ("hiladas_de_la_v", "hiladas", None),
        ("clave_m", "clave", 2), ("guardado_m3", "guardado", 2), ("bloques_de_champa", "bloques", 0), ("falla", "falla", None),
        ("cumple_con_0_30", lambda x: x["escenarios"][0], None), ("cumple_con_un_tercio", lambda x: x["escenarios"][1], None),
        ("cumple_con_0_375", lambda x: x["escenarios"][2], None)], vs)
    actual, mejor = buscar(vs, *ACTUAL), elegir(vs)
    print(f"E6: {len(vs)} variantes; cumplen P y E {sum(not x['falla'] for x in vs)}; con un tercio {sum(x['escenarios'][1] for x in vs)}")
    for t, x in (("actual", actual), ("elegida", mejor)):
        print(f"  {t}: vuelo {x['vuelo']}, alto {x['alto']}, hiladas {x['hiladas']}, clave {x['clave']:.2f}, "
              f"guarda {x['guardado']:.2f} m3, bloques {x['bloques']:.0f}, falla '{x['falla']}', escenarios {x['escenarios']}")
    marcas = [("la actual", actual)] if mejor is actual else [("la actual", actual), ("la elegida", mejor)]
    P.campo("e6_campo", [("", vs)], VUELOS, ALTOS, "vuelo", "alto", lambda x: x["guardado"], "lo que se guarda (m³)",
            "vuelo de cada hilada de la V (cm)", "alto del lado alto (m)", marcas,
            fmt_x=lambda x: P.cm(x), fmt_y=lambda y: P.coma(y, 1))
    cols, filas_h = (0.04, 0.06, 0.08, 0.10), (4.0, 4.6, 5.2)
    filas = [[buscar(vs, vv, Hh) for vv in cols] for Hh in filas_h]
    cambio = P.lamina_matriz(
        "e6_matriz", "P15", 100, "E6. La pirwa, en variantes", "Exploración paramétrica: la matriz", [
            "Cada corte es una variante de pirwa_e6.py, por el eje largo, donde el muro mide el promedio de sus dos lados. La V se ve en el muro",
            "largo, al fondo. V: la champa vuela, con la cola cargada, 0,30 de su largo, un tercio o 0,375 (prueba 3); P, la clave queda a 1,70 m",
            "o más, para estar de pie bajo la trampa; E, el lado alto no pasa de 4,6 m, el que aceptó el autor, hasta que se pruebe uno mayor."],
        filas, None, (95, 66), seccion, textos, [f"lado alto\nde {P.coma(h, 1)} m" for h in filas_h],
        [f"vuela {P.cm(vv)} cm" for vv in cols], "Doce variantes de la pirwa, en corte", lambda x: x is actual, 46)
    P.lamina_y_vista("e6_matriz", cambio)
    return vs, actual, mejor


if __name__ == "__main__":
    P.semilla()
    main()
