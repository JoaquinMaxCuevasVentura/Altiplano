"""Piloto paramétrico de E1, la montaña habitada: un cono de piedra de la cosecha con una cámara volada.

Cambian el radio al pie del cono, el radio de la cámara y lo que vuela cada hilada de la cámara. La cámara es vertical
hasta 1 m y después vuela hilada por hilada, de 20 cm, hasta el óculo de 64 cm. La E1 actual termina en punta justo en
el óculo, y sus últimas piedras no tienen nada detrás; el piloto le pone un collar de piedra de 40 cm alrededor del
óculo, la cola de la última hilada, y así barre todas las variantes.
Las reglas:
    T  el talud del cono no pasa de 40°, el que supone la prueba 1 para la piedra suelta (la prueba lo mide);
    C  el cono cubre la cola de cada hilada volada: detrás de cada piedra que vuela quedan sus 40 cm;
    V  la hilada vuela lo que aguanta la piedra con la cola cargada, en los escenarios de la prueba 3.
Mide la piedra, la altura y el piso de la cámara, y cuenta cuántas parcelas de 2 × 2 m habría que despedregar con
los 0,44 m³ que supone el dibujo de la prueba 1. Se corre desde la raíz: python3 chhaxwa/parametrico/montana_e1.py
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402

HZ, HV, R1, COLA = 0.20, 1.0, 0.32, 0.40                    # hilada, parte vertical, óculo y largo de la piedra (proyecto)
TALUD = 40.0                                               # grados, supuesto de la prueba 1
PARCELA = 0.44                                             # m³ de piedra por parcela de 2 × 2 m (dibujo de la prueba 1)
RADIOS = [round(3.0 + 0.2 * k, 1) for k in range(9)]       # radio al pie, de 3,0 a 4,6 m
CAMARAS = [round(1.0 + 0.1 * k, 1) for k in range(9)]      # radio de la cámara, de 1,0 a 1,8 m
VUELOS = [0.10, 0.12, 0.135, 0.15]
ACTUAL = (3.6, 1.4, 0.135)


def variante(R0, rc, v, collar=True):
    n = math.ceil((rc - R1) / v - 1e-9)                    # hiladas voladas hasta el óculo
    radios = [max(R1, rc - v * k) for k in range(1, n + 1)]
    H = HV + n * HZ
    Rt = R1 + (COLA if collar else 0.0)                    # el radio de la cima: con collar, el óculo y una piedra
    u = lambda z: R0 - (R0 - Rt) * z / H                   # el radio del cono a la altura z
    talud = math.degrees(math.atan(H / (R0 - Rt)))
    colas = all(u(HV + k * HZ) >= r + COLA - 1e-9 for k, r in enumerate(radios, start=1))
    cono = math.pi * H / 3 * (R0 * R0 + R0 * Rt + Rt * Rt)
    camara = math.pi * rc * rc * HV + sum(math.pi * r * r * HZ for r in radios)

    def ancho(z):
        if z < HV:
            return 2 * rc
        k = int((z - HV) / HZ)
        return 0.0 if k >= n else 2 * radios[k]
    v_ = dict(radio=R0, camara=rc, vuelo=v, collar=collar, cima=Rt, hiladas=n, radios=radios, alto=H, talud=talud, piedra=cono - camara,
              parcelas=(cono - camara) / PARCELA, piso=math.pi * rc * rc, ancho_de_pie=ancho(1.70))
    v_["falla"] = ("T" if talud > TALUD + 1e-9 else "") + ("" if colas else "C")
    v_["escenarios"] = [not v_["falla"] and v <= f * COLA + 1e-9 for _, f in P.FRACCIONES]
    v_["rinde"] = v_["piso"] / v_["piedra"]
    return v_


def barrer():
    return [variante(R0, rc, v) for v in VUELOS for rc in CAMARAS for R0 in RADIOS]


def buscar(vs, R0, rc, v):
    return next(x for x in vs if (x["radio"], x["camara"], x["vuelo"]) == (R0, rc, v))


def elegir(vs):
    """La que da más piso de cámara por metro cúbico de piedra, si la piedra vuela un tercio."""
    return max([x for x in vs if x["escenarios"][1]], key=lambda x: (round(x["rinde"], 4), x["piso"]))


def seccion(L, v, o):
    from dibujar_detalles import rect                     # noqa: F401
    ox, oz = o
    R0, rc, H, rs = v["radio"], v["camara"], v["alto"], v["radios"]
    borde = []
    for k in range(len(rs), 0, -1):
        borde += [(rs[k - 1], HV + k * HZ), (rs[k - 1], HV + (k - 1) * HZ)]
    for s in (-1, 1):
        pts = [(rc, 0), (R0, 0), (v["cima"], H)] + [p for p in borde if not (abs(p[0] - v["cima"]) < 1e-9 and abs(p[1] - H) < 1e-9)] + [(rc, HV)]
        L.cortado([(ox + s * x, oz + z) for x, z in pts], "P_LLENO", juntas=False)
    L.linea([(ox - R0 - 0.3, oz), (ox + R0 + 0.3, oz)], "TERRENO")
    if v["ancho_de_pie"] > 0:
        a = v["ancho_de_pie"] / 2
        L.linea([(ox - a, oz + 1.70), (ox + a, oz + 1.70)], "JUNTAS")


def textos(v):
    return [f"alto {P.coma(v['alto'])} m; talud de {round(v['talud'])}°",
            f"{P.coma(v['piedra'], 1)} m³ de piedra, {round(v['parcelas'])} parcelas",
            f"{v['hiladas']} hiladas voladas; {P.estado(v)}"]


def main():
    vs = barrer()
    P.escribir_csv("e1_variantes", [
        ("radio_al_pie_m", "radio", 2), ("radio_de_la_camara_m", "camara", 2), ("vuelo_m", "vuelo", 3),
        ("hiladas_voladas", "hiladas", None), ("alto_m", "alto", 2), ("talud_grados", "talud", 1),
        ("piedra_m3", "piedra", 2), ("parcelas", "parcelas", 1), ("piso_de_la_camara_m2", "piso", 2),
        ("ancho_de_pie_m", "ancho_de_pie", 2), ("falla", "falla", None),
        ("cumple_con_0_30", lambda x: x["escenarios"][0], None), ("cumple_con_un_tercio", lambda x: x["escenarios"][1], None),
        ("cumple_con_0_375", lambda x: x["escenarios"][2], None)], vs)
    actual, mejor = buscar(vs, *ACTUAL), elegir(vs)
    sin_collar = variante(*ACTUAL, collar=False)
    print(f"E1: {len(vs)} variantes; cumplen T y C {sum(not x['falla'] for x in vs)}; con un tercio {sum(x['escenarios'][1] for x in vs)}")
    for t, x in (("actual, sin collar", sin_collar), ("actual, con collar", actual), ("elegida", mejor)):
        print(f"  {t}: radio {x['radio']}, cámara {x['camara']}, vuelo {x['vuelo']}, alto {x['alto']:.2f}, talud {x['talud']:.1f}, "
              f"piedra {x['piedra']:.1f} m3 ({x['parcelas']:.0f} parcelas), piso {x['piso']:.2f}, de pie {x['ancho_de_pie']:.2f}, falla '{x['falla']}'")
    paneles = [(f"cada hilada vuela {P.cm(v)} cm" + (", la actual" if v == ACTUAL[2] else ""), [x for x in vs if x["vuelo"] == v])
               for v in (mejor["vuelo"], ACTUAL[2])] if mejor["vuelo"] != ACTUAL[2] else \
              [(f"cada hilada vuela {P.cm(ACTUAL[2])} cm, la actual", [x for x in vs if x["vuelo"] == ACTUAL[2]])]
    P.campo("e1_campo", paneles, CAMARAS, RADIOS, "camara", "radio", lambda x: x["piedra"], "piedra del cono (m³)",
            "radio de la cámara (m)", "radio al pie del cono (m)", [("la actual", actual), ("la elegida", mejor)],
            fmt_x=lambda x: P.coma(x, 1), fmt_y=lambda y: P.coma(y, 1))
    filas = [[buscar(vs, R0, rc, ACTUAL[2]) for R0 in (3.2, 3.6, 4.0, 4.4)] for rc in (1.0, 1.2, 1.4, 1.6)]
    cambio = P.lamina_matriz(
        "e1_matriz", "P7", 100, "E1. La montaña, en variantes", "Exploración paramétrica: la matriz", [
            "Cada corte es una variante de montana_e1.py, con collar de 40 cm en el óculo y la cámara volando 13,5 cm, como la actual. T: el talud",
            "no pasa de 40°, el que supone la prueba 1; C, detrás de cada piedra que vuela quedan sus 40 cm de cola. Las parcelas son de",
            "2 × 2 m, con los 0,44 m³ de piedra que supone el dibujo de la prueba 1. La línea corta marca el ancho donde se está de pie."],
        filas, None, (95, 54), seccion, textos, [f"cámara de\n{P.coma(2 * rc, 1)} m" for rc in (1.0, 1.2, 1.4, 1.6)],
        [f"radio al pie de {P.coma(R0, 1)} m" for R0 in (3.2, 3.6, 4.0, 4.4)],
        "Dieciséis variantes de la montaña habitada, en corte", lambda x: x is actual, 34)
    P.lamina_y_vista("e1_matriz", cambio)
    return vs, actual, mejor


if __name__ == "__main__":
    P.semilla()
    main()
