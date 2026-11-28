"""Piloto paramétrico de E3, la casa redonda: una pirca redonda con una cúpula de champa volada y un relleno de tierra.

Cambian el radio del cuarto, el alto de la pirca y cómo vuela la cúpula: lo que vuela la primera hilada y lo que vuela
la última. La cúpula es la de la lámina 3 (detalles/dibujar_detalles.py, cupula_perfil): hiladas de champa de 12 cm
y 40 cm de largo que vuelan cada vez más, hasta un óculo de 60 cm. Encima, un relleno de tierra de perfil elíptico,
que baja hasta el borde de la pirca.
Las reglas:
    K  la pirca es al menos tan alta como el paso de 96 cm de la prueba 3 y la laja que lo cubre, de 8 cm;
    C  el relleno de tierra cubre la cola de cada hilada: si no, la hilada no tiene qué la cargue;
    V  la hilada que más vuela no pasa de lo que aguanta la champa con la cola cargada, en los escenarios de la prueba 3.
Mide el área donde se está de pie (1,70 m libres), los bloques de champa de 40 × 25 × 12 cm, la tierra del relleno y la
piedra de la pirca, en parcelas de 2 × 2 m. Se corre desde la raíz: python3 chhaxwa/parametrico/cupula_e3.py
"""

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402
from dibujar_detalles import cupula_perfil                 # noqa: E402

E, HH, COLA, ANCHO, R_OCULO = 0.6, 0.12, 0.40, 0.25, 0.30  # pirca, hilada, largo y ancho del bloque, óculo (proyecto)
PASO, LAJA, CABEZA, TALUD = 0.96, 0.08, 1.70, math.tan(math.radians(5))
PARCELA = 0.44
RADIOS = [round(1.4 + 0.1 * k, 1) for k in range(15)]      # radio del cuarto, de 1,4 a 2,8 m
PIRCAS = [round(0.9 + 0.1 * k, 1) for k in range(8)]       # alto de la pirca, de 0,9 a 1,6 m
VUELOS = [(0.08, 0.12), (0.10, 0.13), (0.12, 0.15)]        # lo que vuelan la primera y la última hilada
ACTUAL = (2.0, 1.2, (0.08, 0.12))                          # desde el 28 de noviembre
ANTES = (2.0, 1.2, (0.10, 0.13))


def variante(Ri, Hb, vuelos):
    v0, v1 = vuelos
    rs = cupula_perfil(Ri, HH, v0=v0, v1=v1, r_oculo=R_OCULO)
    n = len(rs)
    z_c = Hb + n * HH
    r_ocu = rs[-1] + 0.15
    R = Ri + E
    A = R - TALUD * Hb + 0.02 - r_ocu                       # el relleno: un cuarto de elipse, como en la lámina 3
    Hd = z_c - Hb + 0.1
    z0 = Hb - 0.02

    def x_relleno(z):
        t = (z - z0) / Hd
        return r_ocu + A * math.sqrt(max(0.0, 1 - t * t))
    colas = all(x_relleno(Hb + (i + 1) * HH) >= r + COLA - 1e-9 for i, r in enumerate(rs))
    vuelo_max = max(a - b for a, b in zip(rs, rs[1:]))
    k = math.floor((CABEZA - Hb) / HH + 1e-9)
    r_pie = Ri if Hb >= CABEZA else (rs[k] if k < n else 0.0)
    bloques = sum(2 * math.pi * (r + COLA / 2) / ANCHO for r in rs)
    tierra = 0.0
    pasos = 200
    for q in range(pasos):                                   # el relleno, por rebanadas, menos las colas que tapa
        z = z0 + (Hd + 0.0) * (q + 0.5) / pasos
        i = int((z - Hb) / HH)
        dentro = rs[i] + COLA if 0 <= i < n else (rs[-1] if z > z_c else R)
        tierra += math.pi * max(0.0, x_relleno(z) ** 2 - dentro ** 2) * Hd / pasos
    piedra = math.pi * (R * R - Ri * Ri) * Hb
    v = dict(radio=Ri, pirca=Hb, vuelos=vuelos, v0=v0, v1=v1, hiladas=n, radios=rs, cima=z_c, alto=z0 + Hd,
             vuelo_max=vuelo_max, r_pie=r_pie, de_pie=math.pi * r_pie ** 2, piso=math.pi * Ri * Ri, bloques=bloques,
             champa=bloques * COLA * ANCHO * HH, tierra=tierra, piedra=piedra, parcelas=piedra / PARCELA,
             r_ocu=r_ocu, A=A, Hd=Hd, z0=z0)
    v["falla"] = ("K" if Hb < PASO + LAJA - 1e-9 else "") + ("" if colas else "C")
    v["escenarios"] = [not v["falla"] and vuelo_max <= f * COLA + 1e-9 for _, f in P.FRACCIONES]
    v["rinde"] = v["de_pie"] / v["bloques"] * 100
    return v


def barrer():
    return [variante(Ri, Hb, vu) for vu in VUELOS for Hb in PIRCAS for Ri in RADIOS]


def buscar(vs, Ri, Hb, vu):
    return next(x for x in vs if (x["radio"], x["pirca"], x["vuelos"]) == (Ri, Hb, vu))


def elegir(vs):
    """Con el cuarto y la pirca de ahora, la que cumple aunque la champa vuele solo 0,30 de su largo, con más área de pie."""
    return max([x for x in vs if x["escenarios"][0] and (x["radio"], x["pirca"]) == ACTUAL[:2]], key=lambda x: x["de_pie"])


def seccion(L, v, o):
    ox, oz = o
    Ri, Hb, rs, z_c = v["radio"], v["pirca"], v["radios"], v["cima"]
    R = Ri + E
    for s in (-1, 1):
        def m(pts):
            return [(ox + s * x, oz + z) for x, z in pts]
        L.cortado(m([(Ri, 0), (R, 0), (R - TALUD * Hb, Hb), (Ri, Hb)]), "P_LLENO", juntas=False)
        dentro, subida = [], []
        for i, r in enumerate(rs):
            dentro += [(r, Hb + i * HH), (r, Hb + (i + 1) * HH)]
            subida += [(r + COLA, Hb + i * HH), (r + COLA, Hb + (i + 1) * HH)]
        bajada = subida[::-1]                                # las colas, de arriba abajo
        L.cortado(m(dentro + bajada), "C_LLENO", juntas=False)
        elipse = [(v["r_ocu"] + v["A"] * math.cos(math.pi / 2 * q / 30), v["z0"] + v["Hd"] * math.sin(math.pi / 2 * q / 30))
                  for q in range(31)]
        L.cortado(m(elipse + [(rs[-1], v["alto"]), (rs[-1], z_c)] + bajada), "T_LLENO", juntas=False)
    L.linea([(ox - R - 0.3, oz), (ox + R + 0.3, oz)], "TERRENO")
    if v["r_pie"] > 0:
        L.linea([(ox - v["r_pie"], oz + CABEZA), (ox + v["r_pie"], oz + CABEZA)], "JUNTAS")


def textos(v):
    return [f"{v['hiladas']} hiladas; alto {P.coma(v['alto'])} m; vuela hasta {P.cm(v['vuelo_max'])} cm",
            f"{P.coma(v['de_pie'], 1)} m² de pie; {round(v['bloques'] / 10) * 10} bloques",
            P.estado(v)]


def main():
    vs = barrer()
    P.escribir_csv("e3_variantes", [
        ("radio_del_cuarto_m", "radio", 2), ("alto_de_la_pirca_m", "pirca", 2), ("vuelo_primera_m", "v0", 3),
        ("vuelo_ultima_m", "v1", 3), ("hiladas", "hiladas", None), ("alto_m", "alto", 2), ("vuelo_maximo_m", "vuelo_max", 3),
        ("area_de_pie_m2", "de_pie", 2), ("piso_m2", "piso", 2), ("bloques_de_champa", "bloques", 0),
        ("tierra_m3", "tierra", 2), ("piedra_m3", "piedra", 2), ("parcelas", "parcelas", 1), ("falla", "falla", None),
        ("cumple_con_0_30", lambda x: x["escenarios"][0], None), ("cumple_con_un_tercio", lambda x: x["escenarios"][1], None),
        ("cumple_con_0_375", lambda x: x["escenarios"][2], None)], vs)
    actual, mejor, antes = buscar(vs, *ACTUAL), elegir(vs), buscar(vs, *ANTES)
    print(f"E3: {len(vs)} variantes; cumplen K y C {sum(not x['falla'] for x in vs)}; "
          f"con 0,30 {sum(x['escenarios'][0] for x in vs)}; con un tercio {sum(x['escenarios'][1] for x in vs)}; "
          f"con 0,375 {sum(x['escenarios'][2] for x in vs)}")
    for t, x in (("la de antes", antes), ("actual", actual), ("elegida", mejor)):
        print(f"  {t}: radio {x['radio']}, pirca {x['pirca']}, vuelos {x['vuelos']}, hiladas {x['hiladas']}, alto {x['alto']:.2f}, "
              f"vuelo máx {x['vuelo_max']:.3f}, de pie {x['de_pie']:.2f} de {x['piso']:.2f} m2, bloques {x['bloques']:.0f}, "
              f"tierra {x['tierra']:.1f}, piedra {x['piedra']:.1f} ({x['parcelas']:.0f} parcelas), falla '{x['falla']}', "
              f"escenarios {x['escenarios']}")
    nombre = {(0.08, 0.12): "de 8 a 12 cm", (0.10, 0.13): "de 10 a 13 cm", (0.12, 0.15): "de 12 a 15 cm"}
    paneles = [(f"las hiladas vuelan {nombre[vu]}" + (", la actual" if vu == ACTUAL[2] else ", la de antes"),
                [x for x in vs if x["vuelos"] == vu]) for vu in (ACTUAL[2], ANTES[2])]
    marcas = ([("la actual", actual)] if mejor is actual else [("la actual", actual), ("la elegida", mejor)]) + \
        [("la de antes", antes)]
    P.campo("e3_campo", paneles, RADIOS, PIRCAS, "radio", "pirca", lambda x: x["de_pie"],
            "área de pie (m²)", "radio del cuarto (m)", "alto de la pirca (m)",
            marcas, fmt_x=lambda x: P.coma(x, 1), fmt_y=lambda y: P.coma(y, 1))
    cols = (1.6, 2.0, 2.4, 2.8)
    filas = [[buscar(vs, Ri, ACTUAL[1], vu) for Ri in cols] for vu in VUELOS]
    cambio = P.lamina_matriz(
        "e3_matriz", "P11", 100, "E3. La casa redonda, en variantes", "Exploración paramétrica: la matriz", [
            "Cada corte es una variante de cupula_e3.py, con la pirca de 1,2 m. K: la pirca es al menos tan alta como el paso de 96 cm de la",
            "prueba 3 y su laja; C, el relleno cubre la cola de cada hilada; la champa vuela, con la cola cargada, 0,30 del largo, un tercio o",
            "0,375 (prueba 3). La línea corta marca el ancho donde quedan 1,70 m libres. Los bloques son de 40 × 25 × 12 cm, a tizón."],
        filas, None, (95, 66), seccion, textos, [f"vuela\n{nombre[vu]}" for vu in VUELOS],
        [f"cuarto de {P.coma(2 * Ri, 1)} m" for Ri in cols],
        "Doce variantes de la casa redonda, en corte", lambda x: x is actual, 45)
    P.lamina_y_vista("e3_matriz", cambio)
    return vs, actual, mejor


if __name__ == "__main__":
    P.semilla()
    main()
