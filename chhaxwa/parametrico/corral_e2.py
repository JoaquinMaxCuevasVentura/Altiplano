"""Piloto paramétrico de E2, el corral techado: un corral redondo de pirca con un cono de ichu y p'ira encima.

Cambian el diámetro del corral, el alto del cono y cuántos pares lo arman. La pirca es la de la lámina 2: 1,4 m de alto,
0,7 m de base y abierta un cuarto al sur. El techo arranca 90 cm más arriba, sobre palos de queñua parados en la pirca y
un anillo atado, vuela 40 cm afuera de la pirca y se cierra a 30 cm del eje.
Las reglas:
    P  la pendiente del techo es de 45° o más, la de la prueba 4 (cálculo, con las fotos de Šolc);
    S  los pares quedan a 70 cm o menos en el alero, el ancho de la faja de p'ira, que se apoya de par a par (prueba 4).
Mide la queñua (pares, palos y anillo), las fajas de p'ira de 2,5 × 0,7 m, traslapadas 15 cm a lo largo, y la piedra
de la pirca, en parcelas de 2 × 2 m de la prueba 1. Se corre desde la raíz: python3 chhaxwa/parametrico/corral_e2.py
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402

ALTO, BASE, FRANJA, ALERO, RA = 1.4, 0.7, 0.9, 0.4, 0.30   # la pirca, la franja de cielo, el alero y la punta (proyecto)
PENDIENTE, FAJA, ANCHO_FAJA, TRASLAPO = 45.0, 2.5, 0.70, 0.15   # prueba 4; el traslapo, el de E3
PARCELA = 0.44
DIAMETROS = [round(5.0 + 0.5 * k, 1) for k in range(7)]    # de 5 a 8 m
ALTOS = [round(2.2 + 0.3 * k, 1) for k in range(9)]        # alto del cono, de 2,2 a 4,6 m
PARES = [16, 24, 32]
ACTUAL = (6.0, 3.4, 16)


def variante(D, Hc, n):
    R = D / 2
    Rb, za = R + ALERO, ALTO + FRANJA
    pend = Hc / (Rb - RA)
    ang = math.degrees(math.atan(pend))
    cos = math.cos(math.atan(pend))
    rp = R - BASE / 2                                       # el anillo, sobre el eje de la pirca
    z_par = za + (Rb - rp) * pend - 0.15 * math.hypot(pend, 1)   # bajo del par sobre el anillo, como en la lámina 2
    palo = z_par - 0.10 - ALTO
    par = (rp - RA) / cos
    faldon = (Rb - RA) / cos
    queñua = n * par + 7 * palo + 2 * (palo + ALTO) + 2 * math.pi * rp
    por_tira = math.ceil(faldon / (FAJA - TRASLAPO) - 1e-9)
    fajas = n * por_tira
    piedra = 0.75 * math.pi * (R * R - (R - BASE) ** 2) * ALTO
    sep = 2 * math.pi * Rb / n
    v = dict(diametro=D, cono=Hc, pares=n, pendiente=ang, alto=za + Hc, palo=palo, par=par, faldon=faldon,
             queñua=queñua, separacion=sep, fajas=fajas, techos=fajas / 20, piedra=piedra, parcelas=piedra / PARCELA,
             radio=R, alero=Rb, arranque=za, punta=RA)
    v["falla"] = ("P" if ang < PENDIENTE - 1e-9 else "") + ("S" if sep > ANCHO_FAJA + 1e-9 else "")
    v["escenarios"] = [not v["falla"]] * 3                  # E2 no vuela nada: los escenarios de la prueba 3 no la tocan
    return v


def barrer():
    return [variante(D, Hc, n) for n in PARES for Hc in ALTOS for D in DIAMETROS]


def buscar(vs, D, Hc, n):
    return next(x for x in vs if (x["diametro"], x["cono"], x["pares"]) == (D, Hc, n))


def elegir(vs):
    """Con el corral de 6 m, la que cumple con menos queñua."""
    return min([x for x in vs if not x["falla"] and x["diametro"] == ACTUAL[0]], key=lambda x: (round(x["queñua"], 3), x["pares"]))


def seccion(L, v, o):
    ox, oz = o
    R, Rb, za, Hc, RA_ = v["radio"], v["alero"], v["arranque"], v["cono"], v["punta"]
    pend = Hc / (Rb - RA_)
    nr, nz = pend / math.hypot(pend, 1), 1 / math.hypot(pend, 1)
    e = 0.25
    for s in (-1, 1):
        L.cortado([(ox + s * x, oz + z) for x, z in [(R - BASE, 0), (R, 0), (R, ALTO), (R - BASE, ALTO)]], "P_LLENO", juntas=False)
        rp = R - BASE / 2
        L.cortado([(ox + s * x, oz + z) for x, z in [(rp - 0.06, ALTO), (rp + 0.06, ALTO), (rp + 0.06, ALTO + v["palo"]),
                                                       (rp - 0.06, ALTO + v["palo"])]], "L_LLENO", juntas=False)
        cima = za + e * nz + (Rb + e * nr) * pend                       # el ichu se cierra sobre el eje
        techo = [(Rb, za), (RA_, za + Hc), (0, za + Hc), (0, cima), (Rb + e * nr, za + e * nz)]
        L.cortado([(ox + s * x, oz + z) for x, z in techo], "PAJA_LLENO", juntas=False)
    L.linea([(ox - Rb - 0.4, oz), (ox + Rb + 0.4, oz)], "TERRENO")


def textos(v):
    estado = "cumple" if not v["falla"] else "no cumple: " + ", ".join(v["falla"])
    return [f"pendiente de {round(v['pendiente'])}°; alto {P.coma(v['alto'], 1)} m",
            f"{v['pares']} pares a {P.coma(v['separacion'])} m; {v['fajas']} fajas",
            f"{round(v['queñua'])} m de queñua; {estado}"]


def main():
    vs = barrer()
    P.escribir_csv("e2_variantes", [
        ("diametro_m", "diametro", 2), ("alto_del_cono_m", "cono", 2), ("pares", "pares", None),
        ("pendiente_grados", "pendiente", 1), ("alto_total_m", "alto", 2), ("palo_m", "palo", 2), ("par_m", "par", 2),
        ("separacion_en_el_alero_m", "separacion", 2), ("queñua_m", "queñua", 1), ("fajas_de_pira", "fajas", None),
        ("techos_de_enquelga", "techos", 2), ("piedra_m3", "piedra", 2), ("parcelas", "parcelas", 1), ("falla", "falla", None)], vs)
    actual, mejor = buscar(vs, *ACTUAL), elegir(vs)
    print(f"E2: {len(vs)} variantes; cumplen P y S {sum(not x['falla'] for x in vs)}")
    for t, x in (("actual", actual), ("elegida", mejor)):
        print(f"  {t}: diámetro {x['diametro']}, cono {x['cono']}, pares {x['pares']} a {x['separacion']:.2f}, "
              f"pendiente {x['pendiente']:.1f}, palo {x['palo']:.2f}, par {x['par']:.2f}, queñua {x['queñua']:.0f} m, "
              f"fajas {x['fajas']} ({x['techos']:.1f} techos), piedra {x['piedra']:.1f} m3 ({x['parcelas']:.0f} parcelas), falla '{x['falla']}'")
    paneles = [(f"{n} pares" + (", los de ahora" if n == ACTUAL[2] else ""), [x for x in vs if x["pares"] == n])
               for n in (ACTUAL[2], mejor["pares"])]
    P.campo("e2_campo", paneles, DIAMETROS, ALTOS, "diametro", "cono", lambda x: x["queñua"], "queñua de pares, palos y anillo (m)",
            "diámetro del corral (m)", "alto del cono (m)", [("la actual", actual), ("la elegida", mejor)],
            fmt_x=lambda x: P.coma(x, 1), fmt_y=lambda y: P.coma(y, 1))
    filas = [[buscar(vs, D, Hc, 32) for D in (5.0, 6.0, 7.0, 8.0)] for Hc in (2.5, 3.1, 3.4, 4.0)]
    cambio = P.lamina_matriz(
        "e2_matriz", "P9", 200, "E2. El corral techado, en variantes", "Exploración paramétrica: la matriz", [
            "Cada corte es una variante de corral_e2.py con 32 pares; la de ahora tiene 16, a 1,34 m en el alero. P: la pendiente es de 45° o más,",
            "la de la prueba 4; S, los pares quedan a 70 cm o menos en el alero, el ancho de la faja de p'ira. La pirca, los palos y la franja de",
            "cielo de 90 cm son los de la lámina 2. Las fajas son de 2,5 × 0,7 m (Šolc, 2011 [1975]: 105), traslapadas 15 cm a lo largo."],
        filas, None, (95, 52), seccion, textos, [f"cono de\n{P.coma(Hc, 1)} m" for Hc in (2.5, 3.1, 3.4, 4.0)],
        [f"corral de {P.coma(D, 1)} m" for D in (5.0, 6.0, 7.0, 8.0)],
        "Dieciséis variantes del corral techado, en corte, con 32 pares", lambda x: x is buscar(vs, 6.0, 3.4, 32), 33,
        rotulo_actual="la actual, con 32 pares")
    P.lamina_y_vista("e2_matriz", cambio)
    return vs, actual, mejor


if __name__ == "__main__":
    P.semilla()
    main()
