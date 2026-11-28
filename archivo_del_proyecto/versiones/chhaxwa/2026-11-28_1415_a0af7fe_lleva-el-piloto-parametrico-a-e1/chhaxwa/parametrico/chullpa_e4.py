"""Piloto paramétrico de E4, la chullpa: una pirámide escalonada de adobitos de pie con una cámara volada adentro.

Cambian lo que vuela cada hilada de la cámara, lo que se retira cada hilada de la pirámide y la pieza que forra la
cámara. Lo demás es la lámina 4: cuatro pilas de pirca de 1,2 m, una cama de lajas, una hilada de piedra y quince
hiladas de adobitos de 19 × 14 × 6 cm, de pie, con 2 cm de mortero; la pirámide arranca con 3,0 m de lado. La cámara
mide 1,0 × 1,0 m, sube tres hiladas a plomo y después vuela hasta que una laja cierra el hueco que queda, de 30 cm o
menos.
Las reglas:
    V  la pieza del forro vuela lo que aguanta con la cola cargada, en los escenarios de la prueba 3;
    C  la cola de cada pieza del forro cabe en el relleno, sin tocar los adobitos de la cara;
    T  sobre la laja que cierra la cámara queda al menos una hilada de la pirámide;
    R  cada adobito de la cara se apoya en la mitad de su fondo o más: la hilada no se retira más de 7 cm (proyecto).
Mide la cámara, el lado de la pirámide arriba y las piezas. Se corre desde la raíz: python3 chhaxwa/parametrico/chullpa_e4.py
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402

LADO, HILADAS, HA, MJ, PR = 3.0, 15, 0.19, 0.02, 0.14      # la pirámide y el adobito de pie (proyecto)
Z0, CAMARA, A_PLOMO, CIERRE, LAJA = 1.48, 0.5, 3, 0.15, 0.08
PASO_ADOBITO = 0.075                                        # 6 cm de adobito y 1,5 cm de separación (Agüero Benites et al., 2015: 6)
VUELOS = [round(0.03 + 0.01 * k, 2) for k in range(10)]    # de 3 a 12 cm
RETIROS = [round(0.044 + 0.006 * k, 3) for k in range(7)]  # de 4,4 a 8 cm
PIEZAS = [(0.14, "adobitos de pie, de 14 cm de fondo"), (0.40, "adobes de 40 cm, los de E5")]
ACTUAL = (0.10, 0.062, 0.14)


def variante(vc, ret, pieza):
    hz = HA + MJ
    n = math.ceil((CAMARA - CIERRE) / vc - 1e-9)           # hiladas voladas de la cámara
    cam = [CAMARA] * A_PLOMO + [CAMARA - k * vc for k in range(1, n + 1)]
    lados = [LADO - 2 * i * ret for i in range(HILADAS)]
    colas = all(c + pieza <= lados[i] / 2 - PR + 1e-9 for i, c in enumerate(cam) if i < HILADAS)
    cabe = len(cam) + 1 <= HILADAS
    z_cam = Z0 + len(cam) * hz
    volumen = sum((2 * c) ** 2 * hz for c in cam)
    cara = sum(4 * s / PASO_ADOBITO for s in lados)
    forro = sum(4 * 2 * c / (PASO_ADOBITO if pieza == 0.14 else 0.21) * (1 if pieza == 0.14 else 2) for c in cam)
    v = dict(vuelo=vc, retiro=ret, pieza=pieza, hiladas=n, camara=cam, lados=lados, alto_camara=len(cam) * hz,
             techo=z_cam, volumen=volumen, arriba=lados[-1], alto=Z0 + HILADAS * hz, cara=cara, forro=forro)
    v["falla"] = ("" if colas else "C") + ("" if cabe else "T") + ("R" if ret > PR / 2 + 1e-9 else "")
    v["escenarios"] = [not v["falla"] and vc <= f * pieza + 1e-9 for _, f in P.FRACCIONES]
    return v


def barrer():
    return [variante(vc, ret, pz) for pz, _ in PIEZAS for ret in RETIROS for vc in VUELOS]


def buscar(vs, vc, ret, pz):
    return next(x for x in vs if (x["vuelo"], x["retiro"], x["pieza"]) == (vc, ret, pz))


def elegir(vs):
    """Con los adobitos y el retiro de ahora, la cámara más grande que cumple si el adobito vuela un tercio."""
    return max([x for x in vs if x["escenarios"][1] and x["retiro"] == ACTUAL[1] and x["pieza"] == ACTUAL[2]],
               key=lambda x: (round(x["volumen"], 4), -x["vuelo"]))


def seccion(L, v, o):
    ox, oz = o
    hz = HA + MJ
    for s in (-1, 1):
        def m(pts):
            return [(ox + s * x, oz + z) for x, z in pts]
        L.cortado(m([(1.65, 0), (0.45, 0), (0.45, 0.8), (0.35, 0.8), (0.35, 1.0), (0.25, 1.0), (0.25, 1.2), (1.65, 1.2)]),
                  "P_LLENO", juntas=False)
        fuera = []
        for i, sd in enumerate(v["lados"]):
            fuera += [(sd / 2, Z0 + i * hz), (sd / 2, Z0 + (i + 1) * hz)]
        hueco = []
        for i, c in enumerate(v["camara"]):
            hueco += [(c, Z0 + i * hz), (c, Z0 + (i + 1) * hz)]
        L.cortado(m(fuera + [(0, v["alto"]), (0, v["techo"])] + hueco[::-1]), "T_LLENO", juntas=False)
        for i, sd in enumerate(v["lados"]):
            L.cortado(m([(sd / 2 - PR, Z0 + i * hz), (sd / 2, Z0 + i * hz), (sd / 2, Z0 + (i + 1) * hz),
                         (sd / 2 - PR, Z0 + (i + 1) * hz)]), "A_LLENO", juntas=False)
        for i, c in enumerate(v["camara"]):
            L.cortado(m([(c, Z0 + i * hz), (c + v["pieza"], Z0 + i * hz), (c + v["pieza"], Z0 + (i + 1) * hz),
                         (c, Z0 + (i + 1) * hz)]), "A_LLENO", juntas=False)
    L.cortado([(ox - 1.65, oz + 1.2), (ox + 1.65, oz + 1.2), (ox + 1.65, oz + 1.3), (ox - 1.65, oz + 1.3)], "L_LLENO", juntas=False)
    L.cortado([(ox - 1.55, oz + 1.3), (ox + 1.55, oz + 1.3), (ox + 1.55, oz + Z0), (ox - 1.55, oz + Z0)], "P_LLENO", juntas=False)
    c = v["camara"][-1]
    L.cortado([(ox - c - 0.05, oz + v["techo"]), (ox + c + 0.05, oz + v["techo"]), (ox + c + 0.05, oz + v["techo"] + LAJA),
               (ox - c - 0.05, oz + v["techo"] + LAJA)], "L_LLENO", juntas=False)
    L.linea([(ox - 2.0, oz), (ox + 2.0, oz)], "TERRENO")


def textos(v):
    return [f"cámara de {P.coma(v['alto_camara'])} m de alto, {P.coma(v['volumen'])} m³",
            f"{v['hiladas']} hiladas voladas; arriba, {P.coma(v['arriba'])} m de lado",
            P.estado(v)]


def main():
    vs = barrer()
    P.escribir_csv("e4_variantes", [
        ("vuelo_de_la_camara_m", "vuelo", 3), ("retiro_de_la_piramide_m", "retiro", 3), ("pieza_del_forro_m", "pieza", 2),
        ("hiladas_voladas", "hiladas", None), ("alto_de_la_camara_m", "alto_camara", 2), ("volumen_de_la_camara_m3", "volumen", 2),
        ("lado_arriba_m", "arriba", 2), ("adobitos_de_la_cara", "cara", 0), ("piezas_del_forro", "forro", 0),
        ("falla", "falla", None), ("cumple_con_0_30", lambda x: x["escenarios"][0], None),
        ("cumple_con_un_tercio", lambda x: x["escenarios"][1], None), ("cumple_con_0_375", lambda x: x["escenarios"][2], None)], vs)
    actual, mejor, con_adobe = buscar(vs, *ACTUAL), elegir(vs), buscar(vs, ACTUAL[0], ACTUAL[1], 0.40)
    print(f"E4: {len(vs)} variantes; cumplen C, T y R {sum(not x['falla'] for x in vs)}; con un tercio {sum(x['escenarios'][1] for x in vs)}")
    for t, x in (("actual", actual), ("elegida", mejor), ("la actual con adobes de 40", con_adobe)):
        print(f"  {t}: vuelo {x['vuelo']}, retiro {x['retiro']}, pieza {x['pieza']}, hiladas {x['hiladas']}, cámara {x['alto_camara']:.2f} m "
              f"y {x['volumen']:.2f} m3, arriba {x['arriba']:.2f}, cara {x['cara']:.0f}, forro {x['forro']:.0f}, falla '{x['falla']}', "
              f"escenarios {x['escenarios']}")
    paneles = [(f"forro de {nombre}", [x for x in vs if x["pieza"] == pz]) for pz, nombre in PIEZAS]
    P.campo("e4_campo", paneles, VUELOS, RETIROS, "vuelo", "retiro", lambda x: x["volumen"], "volumen de la cámara (m³)",
            "vuelo de cada hilada de la cámara (cm)", "retiro de la pirámide (cm)",
            [("la actual", actual), ("la elegida", mejor), ("la actual, con adobes", con_adobe)],
            fmt_x=lambda x: P.cm(x), fmt_y=lambda y: P.cm(y))
    cols = (0.044, 0.056, 0.062, 0.068, 0.080)
    filas = [[buscar(vs, vc, ret, 0.14) for ret in cols] for vc in (0.04, 0.07, 0.10)]
    cambio = P.lamina_matriz(
        "e4_matriz", "P13", 100, "E4. La chullpa, en variantes", "Exploración paramétrica: la matriz", [
            "Cada corte es una variante de chullpa_e4.py, con la cámara forrada de adobitos de pie, de 14 cm de fondo, sin la cornisa ni la boca.",
            "V: la pieza vuela, con la cola cargada, 0,30 de su fondo, un tercio o 0,375 (prueba 3); C, su cola cabe en el relleno; T, sobre la laja",
            "que cierra la cámara queda una hilada; R, la hilada no se retira más de 7 cm, la mitad del fondo del adobito."],
        filas, None, (76, 67), seccion, textos, [f"vuela\n{P.cm(vc)} cm" for vc in (0.04, 0.07, 0.10)],
        [f"se retira {P.cm(r)} cm" for r in cols], "Quince variantes de la chullpa, en corte", lambda x: x is actual, 47)
    P.lamina_y_vista("e4_matriz", cambio)
    return vs, actual, mejor, con_adobe


if __name__ == "__main__":
    P.semilla()
    main()
