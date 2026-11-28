"""Piloto de exploración paramétrica: la bóveda de E5, la casa de la bóveda.

La bóveda se vuelve una función de sus reglas de construcción. Cambian tres parámetros: el arranque (dónde empieza a
volar la bóveda), el vuelo de la primera hilada y el de la última. Lo demás queda fijo, con las medidas de
chhaxwa/exploraciones.md. El perfil es el de chhaxwa/blender/formas.py: cada hilada vuela un poco más que la de abajo.

El guion barre 825 variantes. En cada una revisa si cabe en la casa de la novela (las reglas A, C y K) y cuánto tiene
que volar el adobe para sostenerla (la regla V), que es lo que mide la prueba 3. Como esa medida todavía no existe, se
prueban tres escenarios: que el adobe vuele 12 cm, un tercio de su largo (13,3 cm, la hipótesis de hoy) o 15 cm. En cada
escenario elige la variante con más espacio para estar sentado en el suelo; si empatan, la de más espacio de pie, la de
menos adobes y la de menos relleno, en ese orden.

Se corre desde la raíz con un Python que tenga ezdxf, shapely y matplotlib:
    python3 chhaxwa/parametrico/boveda_e5.py
Escribe en chhaxwa/parametrico/: e5_variantes.csv, e5_campo.png (el campo de las variantes) y dos láminas en DXF con
su vista en PNG: e5_matriz (24 variantes a 1:100) y e5_elegidas (las tres elegidas a 1:50). Al final llama a
boveda_e5_verdadera.py, la otra familia, la de la bóveda verdadera, que escribe e5_variantes_verdaderas.csv y la lámina
e5_verdaderas.
"""

import csv
import math
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "detalles"))

# --- lo fijo: las medidas de E5 --------------------------------------------------------------------------------------
LI, WI = 5.75, 3.30            # el cuarto: la mediana de Šolc (2011 [1975]: 93-94)
HW = 2.0                       # el bloque: «apenas se alzan dos metros del suelo» (p. 30)
E0, CARA = 0.9, 0.32           # el muro al pie y el espesor de cada cara de la pirca (proyecto)
TALUD = math.tan(math.radians(10))
WO = WI + 2 * E0
HH = 0.11                      # una hilada: el adobe de 10 cm a tizón y 1 cm de junta (proyecto)
COLA = 0.40                    # el largo del adobe, que entra en el muro
PASO = 0.205                   # un adobe de 20 cm y su junta, a lo largo de la bóveda
LAJA, LAJA_ANCHO = 0.08, 0.75  # las lajas de la clave (proyecto)
R_CIERRE = 0.15                # el perfil se calcula para cerrar a 30 cm (como en formas.py)
PARAPETO = 0.30                # lo que la pirca sube sobre el relleno (proyecto)
CABEZA, SENTADO = 1.70, 1.00   # alto libre para estar de pie y para estar sentado en el suelo

REGLAS = {
    "A": "la clave, con sus lajas, no pasa de 2 m, la altura de las casas de la novela (p. 30)",
    "C": "el relleno carga las colas de todas las hiladas menos la última y deja un parapeto de 30 cm (proyecto)",
    "K": "la rendija de la clave no pasa de 50 cm, para que una laja de 75 cm apoye 12 cm de cada lado (proyecto)",
    "V": "ninguna hilada vuela más de lo que aguanta el adobe con la cola cargada; lo mide la prueba 3",
}
ESCENARIOS = [("12 cm", 0.12), ("un tercio, 13,3 cm", COLA / 3), ("15 cm", 0.15)]

ARRANQUES = [round(0.10 + 0.05 * k, 2) for k in range(15)]   # de 0,10 a 0,80 m
VUELOS_0 = [round(0.06 + 0.01 * k, 2) for k in range(11)]   # de 6 a 16 cm
AUMENTOS = [0.0, 0.01, 0.02, 0.03, 0.04]                     # cuánto más vuela la última hilada que la primera
ACTUAL = (0.35, 0.11, 0.13)                                  # E5 como está en formas.py

# --- el modelo ------------------------------------------------------------------------------------------------------

def perfil(v0, v1):
    """El medio ancho libre de cada hilada (la misma cuenta de cupula_perfil en chhaxwa/blender/formas.py)."""
    R = WI / 2
    b = v0 / HH
    a2H = (v1 / HH - b) / 2
    H = (R - R_CIERRE) / (b + a2H)
    a2 = a2H / H
    n = math.ceil(H / HH - 0.5001) + 1               # el entero más cercano; en el empate, el de abajo (E5 da 12,5)
    return [max(R_CIERRE, R - b * i * HH - a2 * (i * HH) ** 2) for i in range(n)]


def variante(zr, v0, v1):
    """Una variante: su geometría, sus medidas, las reglas de la casa que no cumple y el vuelo que pide."""
    radios = perfil(v0, v1)
    n = len(radios)
    zc = zr + n * HH                                   # bajo de las lajas de la clave
    vuelos = [radios[i] - radios[i + 1] for i in range(n - 1)]

    def ancho(z):
        if z < zr:
            return WI
        i = int((z - zr) / HH)
        return 0.0 if i >= n else 2 * radios[i]
    zf = min(HW - PARAPETO, zc)                        # el relleno sube hasta el parapeto o hasta la clave
    area, dz = 0.0, 0.002
    for k in range(int(zf / dz)):
        z = (k + 0.5) * dz
        x_out = WO / 2 - CARA - TALUD * z
        x_in = WI / 2 + CARA if z < zr else radios[min(int((z - zr) / HH), n - 1)] + COLA
        area += max(0.0, x_out - x_in) * dz
    v = dict(arranque=zr, vuelo_inicial=v0, vuelo_final=v1, hiladas=n, radios=radios, clave=zc, relleno_alto=zf,
             techo=zc + LAJA, rendija=2 * radios[-1], vuelo_max=max(vuelos) if vuelos else 0.0,
             ancho_de_pie=ancho(CABEZA), ancho_sentado=ancho(SENTADO),
             adobes=n * 2 * round(LI / PASO), relleno=2 * area * LI)
    falla = ""
    if v["techo"] > HW + 1e-9:
        falla += "A"
    if zr + (n - 1) * HH > HW - PARAPETO + 1e-9:
        falla += "C"
    if v["rendija"] > 0.50 + 1e-9:
        falla += "K"
    v["falla"] = falla
    v["cabe"] = not falla
    v["escenarios"] = [v["cabe"] and v["vuelo_max"] <= tope + 1e-9 for _, tope in ESCENARIOS]
    return v


def clase(v):
    """0: basta 12 cm; 1: basta un tercio; 2: pide 15 cm; 3: pide más de 15 cm; 4: no cabe en la casa."""
    if not v["cabe"]:
        return 4
    for k, ok in enumerate(v["escenarios"]):
        if ok:
            return k
    return 3


def barrer():
    return [variante(zr, v0, round(v0 + d, 2)) for d in AUMENTOS for v0 in VUELOS_0 for zr in ARRANQUES]


def mejor(vs, k):
    """La elegida del escenario k: más ancho sentado, después más de pie, menos adobes y menos relleno."""
    return max([v for v in vs if v["escenarios"][k]],
               key=lambda v: (round(v["ancho_sentado"], 2), round(v["ancho_de_pie"], 2), -v["adobes"], -v["relleno"]))


def buscar(vs, zr, v0, v1):
    return next(v for v in vs if (v["arranque"], v["vuelo_inicial"], v["vuelo_final"]) == (zr, v0, v1))


def coma(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def cm(x):
    return coma(x * 100, 1).replace(",0", "")


# --- el CSV ---------------------------------------------------------------------------------------------------------

def escribir_csv(vs):
    campos = ["arranque_m", "vuelo_inicial_m", "vuelo_final_m", "hiladas", "clave_m", "techo_m", "rendija_m",
              "vuelo_max_m", "ancho_de_pie_m", "ancho_sentado_m", "adobes", "relleno_m3", "cabe", "falla",
              "cumple_con_12cm", "cumple_con_un_tercio", "cumple_con_15cm"]
    with open(AQUI / "e5_variantes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(campos)
        for v in vs:
            w.writerow([f"{v['arranque']:.2f}", f"{v['vuelo_inicial']:.2f}", f"{v['vuelo_final']:.2f}", v["hiladas"],
                        f"{v['clave']:.3f}", f"{v['techo']:.3f}", f"{v['rendija']:.3f}", f"{v['vuelo_max']:.3f}",
                        f"{v['ancho_de_pie']:.3f}", f"{v['ancho_sentado']:.3f}", v["adobes"], f"{v['relleno']:.2f}",
                        "sí" if v["cabe"] else "no", v["falla"]] + ["sí" if ok else "no" for ok in v["escenarios"]])


# --- el campo: un mapa de las 825 variantes ---------------------------------------------------------------------------

GRISES = ["#3d3b38", "#7d7a75", "#b8b5af", "#e6e3dd", "#ffffff"]
CLASES = ["basta que el adobe vuele 12 cm", "basta un tercio del adobe, 13,3 cm", "pide que vuele 15 cm",
          "pide más de 15 cm", "no cabe en la casa (A, C o K)"]


def campo(vs, elegidas):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch, Rectangle
    plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 6.6, "axes.linewidth": 0.4,
                         "xtick.major.width": 0.4, "ytick.major.width": 0.4, "xtick.major.size": 2,
                         "ytick.major.size": 2, "svg.hashsalt": "chhaxwa"})
    fig, ejes = plt.subplots(1, len(AUMENTOS), figsize=(195 / 25.4, 78 / 25.4), sharey=True)
    fig.subplots_adjust(left=0.07, right=0.995, top=0.88, bottom=0.30, wspace=0.12)
    marcas = {id(v): t for t, v in elegidas}
    for ax, d in zip(ejes, AUMENTOS):
        for v in vs:
            if round(v["vuelo_final"] - v["vuelo_inicial"], 2) != d:
                continue
            x, y = v["vuelo_inicial"] * 100, v["arranque"] * 100
            ax.add_patch(Rectangle((x - 0.5, y - 2.5), 1, 5, facecolor=GRISES[clase(v)], edgecolor="#d9d6d0",
                                   linewidth=0.25))
            if id(v) in marcas:
                ax.add_patch(Rectangle((x - 0.5, y - 2.5), 1, 5, facecolor="none", edgecolor="#151413", linewidth=1.1))
                ax.annotate(marcas[id(v)], (x - 0.5, y + 2.5), xytext=(5.9, y + 17), fontsize=6.3, ha="left",
                            arrowprops=dict(arrowstyle="-", linewidth=0.4, color="#151413", shrinkA=1, shrinkB=0),
                            color="#151413")
        ax.set_xlim(5.5, 16.5)
        ax.set_ylim(7.5, 82.5)
        ax.set_xticks([6, 8, 10, 12, 14, 16])
        ax.set_yticks([10, 20, 30, 40, 50, 60, 70, 80])
        ax.set_title(f"la última vuela {cm(d)} cm más" if d else "todas vuelan igual", fontsize=6.8, pad=3)
        ax.set_xlabel("vuelo de la primera hilada (cm)")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    ejes[0].set_ylabel("arranque de la bóveda (cm)")
    fig.legend(handles=[Patch(facecolor=g, edgecolor="#8d8a85", linewidth=0.4, label=c) for g, c in zip(GRISES, CLASES)],
               loc="lower center", ncol=5, frameon=False, fontsize=6.4, handlelength=1.4, columnspacing=1.6)
    ruta = AQUI / "e5_campo.png"
    fig.savefig(ruta, dpi=300, facecolor="white", metadata={"Software": None})
    plt.close(fig)
    from PIL import Image
    Image.open(ruta).convert("L").save(ruta, optimize=True)


# --- las láminas ----------------------------------------------------------------------------------------------------

def seccion(L, v, o, lleno):
    """El corte de través de una variante, con su centro en el punto o del modelo. lleno: rellenos grises (1:100)."""
    from dibujar_detalles import rect
    ox, oz = o
    m_p, m_t, m_a, m_l = (("P_LLENO", "T_LLENO", "A_LLENO", "L_LLENO") if lleno else ("PIEDRA", "TIERRA", "ADOBE", "LAJA"))
    radios, zr, n = v["radios"], v["arranque"], v["hiladas"]

    def t(pts, s=1):
        return [(ox + s * x, oz + z) for (x, z) in pts]
    for s in (-1, 1):
        L.cortado(t([(WO / 2 - CARA, 0), (WO / 2, 0), (WO / 2 - TALUD * HW, HW), (WO / 2 - CARA - TALUD * HW, HW)], s), m_p,
                  juntas=not lleno)
        L.cortado(t(rect(WI / 2, 0, WI / 2 + CARA, zr), s), m_p, juntas=not lleno)
        zf = v["relleno_alto"]
        cola = []
        for i in range(n - 1, -1, -1):
            z0, z1 = zr + i * HH, zr + (i + 1) * HH
            if z0 >= zf:
                continue
            cola += [(radios[i] + COLA, min(z1, zf)), (radios[i] + COLA, z0)]
        L.cortado(t([(WI / 2 + CARA, 0), (WO / 2 - CARA, 0), (WO / 2 - CARA - TALUD * zf, zf)] + cola +
                    [(WI / 2 + CARA, zr)], s), m_t, juntas=False)
        for i in range(n):
            L.cortado(t(rect(radios[i], zr + i * HH, radios[i] + COLA, zr + (i + 1) * HH), s), m_a)
    L.cortado(t(rect(-LAJA_ANCHO / 2, v["clave"], LAJA_ANCHO / 2, v["techo"])), m_l)
    for i in range(1, n):                                                # las hiladas del fondo, vistas
        L.linea(t([(-radios[i], zr + i * HH), (radios[i], zr + i * HH)]), "VISTA")
    L.linea(t([(-WO / 2 - 0.3, 0), (WO / 2 + 0.3, 0)]), "TERRENO")
    L.linea(t([(-WO / 2 - 0.15, HW), (WO / 2 + 0.15, HW)]), "OCULTO")
    if v["ancho_de_pie"] > 0:
        a = v["ancho_de_pie"] / 2
        L.linea(t([(-a, CABEZA), (a, CABEZA)]), "JUNTAS")


def lamina_matriz(vs):
    from dibujar_detalles import Lamina, TA, rect
    L = Lamina(100, (0, 0), materiales={"P_LLENO": ("SOLID", 1, 172), "T_LLENO": ("SOLID", 1, 226),
                                         "A_LLENO": ("SOLID", 1, 92), "L_LLENO": ("SOLID", 1, 60)})
    filas = [0.20, 0.35, 0.60, 0.80]
    perfiles = [(0.08, 0.08), (0.10, 0.10), (0.11, 0.13), (0.12, 0.12), (0.14, 0.15), (0.16, 0.16)]
    textos = ["basta que vuele 12 cm", "basta un tercio, 13,3 cm", "pide que vuele 15 cm", "pide más de 15 cm"]
    L.titulo(30, 279, "Veinticuatro variantes de la bóveda de E5, en corte de través")
    for j, (v0, v1) in enumerate(perfiles):
        L.texto(30 + 31 + j * 62, 270, f"vuelo de {cm(v0)} a {cm(v1)} cm" if v0 != v1 else f"vuelo de {cm(v0)} cm",
                2.6, TA.MIDDLE_CENTER)
    for i, zr in enumerate(filas):
        yg = 238 - i * 50                                                  # el suelo de la fila
        L.texto(14, yg + 12, "arranque", 2.4)
        L.texto(14, yg + 7.5, f"a {cm(zr)} cm", 2.4)
        for j, (v0, v1) in enumerate(perfiles):
            v = buscar(vs, zr, v0, v1)
            cx = 30 + 31 + j * 62
            seccion(L, v, L.h(cx, yg), lleno=True)
            k = clase(v)
            linea3 = textos[k] if k < 4 else "no cabe: " + ", ".join(v["falla"])
            L.texto(cx, yg - 4.5, f"{v['hiladas']} hiladas; clave a {coma(v['clave'])} m", 2.2, TA.MIDDLE_CENTER)
            pie = f"de pie {coma(v['ancho_de_pie'])} m" if v["ancho_de_pie"] > 0 else "sin alto de pie"
            L.texto(cx, yg - 8.0, f"{pie}; sentado {coma(v['ancho_sentado'])} m", 2.2, TA.MIDDLE_CENTER)
            L.texto(cx, yg - 11.5, linea3, 2.2, TA.MIDDLE_CENTER)
            if (zr, v0, v1) == ACTUAL:
                L.linea([L.h(cx - 30, yg - 14.5), L.h(cx + 30, yg - 14.5), L.h(cx + 30, yg + 27), L.h(cx - 30, yg + 27)],
                        "MARCO", cerrada=True)
                L.texto(cx - 29, yg + 24, "E5, la actual", 2.2)
    L.marco("P2", "E5. La bóveda, en variantes", "Exploración paramétrica: la matriz", [
        "Cada corte es una variante del guion boveda_e5.py. La línea de trazos marca los 2 m de la novela (p. 30), y la línea corta, el ancho",
        "donde se está de pie, con 1,70 m libres. Las reglas: A, la clave no pasa de 2 m; C, el relleno carga las colas y deja 30 cm de",
        "parapeto; K, la rendija de la clave no pasa de 50 cm. Cuánto vuela el adobe lo dirá la prueba 3."], serie="piloto")
    return L.guardar("e5_matriz", AQUI)


def lamina_elegidas(vs, elegidas):
    from dibujar_detalles import Lamina, TA
    L = Lamina(50, (0, 0))
    for j, (titulo, v) in enumerate(elegidas):
        cx, yg = 75 + j * 135, 168
        o = L.h(cx, yg)
        seccion(L, v, o, lleno=False)
        L.texto(cx, 236, titulo, 3.0, TA.MIDDLE_CENTER)
        ox, oz = o
        if v["ancho_de_pie"] > 0:
            a = v["ancho_de_pie"] / 2
            L.msp.add_linear_dim(base=(ox, oz + CABEZA), p1=(ox - a, oz + CABEZA), p2=(ox + a, oz + CABEZA),
                                 dimstyle="CHHAXWA", override={"dimtad": 0},
                                 dxfattribs={"layer": "COTAS"}).render()          # el texto, sobre la línea misma
        a = v["ancho_sentado"] / 2
        L.cota((ox - a, oz + SENTADO), (ox + a, oz + SENTADO), (ox, oz + SENTADO))
        L.nivel(ox - WI / 2 + 0.12, oz + v["arranque"], "+" + coma(v["arranque"]))
        L.nivel(ox + v["radios"][-1] + 0.45, oz + v["clave"], "+" + coma(v["clave"]))
        filas = [f"arranque a {coma(v['arranque'])} m",
                 (f"vuelo de {cm(v['vuelo_inicial'])} a {cm(v['vuelo_final'])} cm por hilada"
                  if v["vuelo_inicial"] != v["vuelo_final"] else f"vuelo de {cm(v['vuelo_inicial'])} cm en todas las hiladas"),
                 f"{v['hiladas']} hiladas; la última vuela {cm(v['vuelo_max'])} cm",
                 f"clave a {coma(v['clave'])} m; lajas hasta {coma(v['techo'])} m",
                 f"rendija de {round(v['rendija'] * 100)} cm",
                 f"de pie, {coma(v['ancho_de_pie'])} m de ancho",
                 f"sentado, {coma(v['ancho_sentado'])} m de ancho",
                 f"{v['adobes']} adobes en la bóveda",
                 f"{coma(v['relleno'], 1)} m³ de relleno de tierra"]
        for i, f in enumerate(filas):
            L.texto(cx - 48, 140 - i * 7.2, f, 2.6)
    L.marco("P3", "E5. La bóveda, según vuele el adobe", "Exploración paramétrica: las tres elegidas", [
        "En cada escenario, la variante que cumple con más ancho para estar sentado (a 1 m del suelo); si empatan, la de más ancho de",
        "pie (a 1,70 m), menos adobes y menos relleno. La línea de trazos marca los 2 m de la novela (p. 30). Lo que vuela el adobe lo dirá",
        "la prueba 3; hasta entonces son escenarios."], serie="piloto")
    return L.guardar("e5_elegidas", AQUI)


def vista(nombre):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image
    from dibujar_detalles import dibujar
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4))
    dibujar(nombre, fig.add_axes([0, 0, 1, 1]), carpeta=AQUI)
    fig.set_size_inches(420 / 25.4, 297 / 25.4)
    ruta = AQUI / f"{nombre}.png"
    fig.savefig(ruta, dpi=200, facecolor="white")
    plt.close(fig)
    Image.open(ruta).convert("L").quantize(32).save(ruta, optimize=True)


if __name__ == "__main__":
    if os.environ.get("PYTHONHASHSEED") != "0":       # el mismo orden de las tablas del DXF en cada corrida
        os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0"})
    vs = barrer()
    escribir_csv(vs)
    elegidas = [(f"Si el adobe vuela {nombre}", mejor(vs, k)) for k, (nombre, _) in enumerate(ESCENARIOS)]
    print(f"{len(vs)} variantes; caben en la casa {sum(v['cabe'] for v in vs)}; cumplen con 12 cm, un tercio y 15 cm: "
          + ", ".join(str(sum(v['escenarios'][k] for v in vs)) for k in range(len(ESCENARIOS))))
    for t, v in elegidas:
        print(f"{t}: arranque {v['arranque']}, vuelo {v['vuelo_inicial']}-{v['vuelo_final']}, {v['hiladas']} hiladas, "
              f"techo {v['techo']:.2f}, de pie {v['ancho_de_pie']:.2f}, sentado {v['ancho_sentado']:.2f}, "
              f"{v['adobes']} adobes, {v['relleno']:.1f} m3")
    campo(vs, [("E5, la actual" if elegidas[1][1] is buscar(vs, *ACTUAL) else "mejor con un tercio", elegidas[1][1]),
               ("mejor con 12 cm", elegidas[0][1]), ("mejor con 15 cm", elegidas[2][1])])
    import boveda_e5_verdadera as V                    # la otra familia: la bóveda verdadera
    ws = V.barrer()
    V.escribir_csv(ws)
    verdaderas = V.elegir(ws)
    print(f"bóveda verdadera: {len(ws)} variantes; cumplen {sum(w['cumple'] for w in ws)}")
    for t_, w in verdaderas:
        print(f"{t_}: arranque {w['arranque']}, flecha {w['flecha']}, anillo {w['espesor']}, techo {w['techo']:.2f}, "
              f"de pie {w['ancho_de_pie']:.2f}, sentado {w['ancho_sentado']:.2f}, {w['adobes']} adobes, "
              f"empuje {w['empuje']:.1f} kN/m, tercio central {'sí' if w['tercio'] else 'no'}")
    if "--sin-laminas" not in sys.argv:
        for nombre, cambio in (("e5_matriz", lamina_matriz(vs)), ("e5_elegidas", lamina_elegidas(vs, elegidas)),
                               ("e5_verdaderas", V.lamina(buscar(vs, *ACTUAL), verdaderas))):
            if cambio or not (AQUI / f"{nombre}.png").exists():
                vista(nombre)
            print(f"{nombre}: {'rehecha' if cambio else 'sin cambios'}")
