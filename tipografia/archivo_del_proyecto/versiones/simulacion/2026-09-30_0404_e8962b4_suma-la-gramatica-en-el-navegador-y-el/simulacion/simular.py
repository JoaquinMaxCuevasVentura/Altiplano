"""Simula el taller analógico de Contenida: la propuesta de la máquina.

Uso (desde la raíz del repositorio, después de inventario.py):
    pip install numpy scipy opencv-python-headless pillow scikit-image shapely
    python3 tipografia/simulacion/simular.py [--parametros parametros.json]

Arma el testigo del pie y la gramática, y corre los simuladores del taller
—calco, placa, cinta, frotado, agua y voz— sobre las 56 celdas y las 119 placas.
Escribe en tipografia/simulacion/salida/:
  láminas (JPG y PNG) por estado,
  agua.gif (la palabra «agua» en el agua tocada) y voz.gif (la palabra «voz» movida por una voz),
  fichas_simuladas.json (una ficha por placa, con los campos de la ficha de hallazgo),
  informe.md (lo que decidió la máquina, con sus números).

Con --parametros usa los ajustes de la gramática exportados por la aplicación
(tipografia/aplicacion/). Es una hipótesis hecha por código para confrontarla con
la que se haga a mano.
Ninguna de estas formas entra en la caja ni en la fuente.
Tarda unos minutos. La semilla es fija: da siempre el mismo resultado.
"""

import json
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from comun import (AJUSTES, CELDAS, FUENTE_TESTIGO, GLIFOS, POR_SIGNO, SALIDA, T, VERSOS, a8, a_rgb, azar,
                   fila_de_paneles, guardar, lamina, poliza, rotulo)
from contener import foto_placa, repujar_placa, reverso, signo_final
from desenterrar import calco, celda_notdef, desenterrar, dibujar_trazos, frotado, pared
from devolver import agua, agua_tocada_en_bucle, foto_agua, frotadas, voz_del_verso, voz_en_bucle
from gramatica import V, celda, encintar, imagen_cuerpo

OSCURO = dict(fondo=(0.06, 0.06, 0.08), tinta=(0.85, 0.9, 0.85), junta=(0.12, 0.12, 0.14))


def coma(x, d=1):
    """Números con coma decimal."""
    return f"{x:.{d}f}".replace(".", ",")


def contraste_en_el_agua(luz, relieve):
    """Cuánto se aparta la luz de su entorno donde cae la letra, contra el resto de la placa."""
    desvio = np.abs(luz - cv2.GaussianBlur(luz, (0, 0), 16))
    letra = cv2.dilate((np.abs(relieve) > 0.32).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    resto = ~cv2.dilate(letra.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool)
    return float(desvio[letra].mean() / (desvio[resto].mean() + 1e-9))


def u8(img):
    return a8(img) if img.dtype != np.uint8 else img


def paso(msg, t0=[time.time()]):
    print(f"[{time.time() - t0[0]:6.1f} s] {msg}", flush=True)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    GLIFOS.mkdir(parents=True, exist_ok=True)
    pol = poliza()
    fichas = {}

    # ------------------------------------------------ el pie y la gramática
    paso("el pie, los testigos, la escala y la gramática")
    D = desenterrar()
    med, e = D["med"], D["esqueleto"]
    lamina_pie(D)
    lamina_anatomia(D)
    lamina_antes_y_despues(D)

    # ------------------------------------------------ calco: sobre el frotado de la pared
    paso("calco: la pared, su frotado y el calco de la gramática")
    P = pared(7, 8, 300, azar("pared"))
    F = frotado(P, azar("frotado"))
    guardar(SALIDA / "01_frotado_de_la_pared.jpg", cv2.resize(F, (1600, int(1600 * F.shape[0] / F.shape[1])), interpolation=cv2.INTER_AREA))
    fondos = {}
    j, px = P["junta"], P["px"]
    for c in CELDAS:
        x = j + (c["columna"] - 1) * (px + j)
        y = j + (c["fila"] - 1) * (px + j)
        fondos[c["celda"]] = cv2.resize(F[y:y + px, x:x + px], (T, T), interpolation=cv2.INTER_LINEAR)
    pauta = dict(celda=celda(e), fondo=e["fondo"], borde=e["borde"])
    calcos, trazos = {}, {}
    for c in CELDAS:
        s = c["signo"]
        if c["estado"] == "manos":
            calcos[c["celda"]] = 1 - 0.22 * (1 - fondos[c["celda"]])
            continue
        cuerpo = D["gramatica"][s]
        cv2.imwrite(str(GLIFOS / f"forma_{c['celda']:02d}.png"), (~cuerpo["mascara"]).astype(np.uint8) * 255)
        img, tr = calco(cuerpo["geo"], c["estado"] == "reconstruida", fondos[c["celda"]], pauta, azar("calco", c["celda"]))
        calcos[c["celda"]], trazos[c["celda"]] = img, tr
    D["desagues"] = {celda_: len(tr) for celda_, tr in trazos.items()}
    lamina(calcos, "Calco · simulación",
           "En papel de calco, sobre el frotado de la pared: el contorno del cuerpo de la gramática, abierto en su punto más bajo\n"
           f"(el desagüe). Continuo lo hallado, punteado lo reconstruido; la celda, en lápiz. Canal de {coma(med['canal'] / 4)} mm. "
           "La celda 56 no se calca: se hace con los dedos.", SALIDA / "03_calco.png")
    notdef = dibujar_trazos((T, T), celda_notdef(azar("notdef")), False, azar("notdef"))
    guardar(SALIDA / "03b_notdef.png", 1 - 0.85 * notdef)

    # ------------------------------------------------ placa: repujar por el reverso
    paso("placa: repujar 119 placas")
    claves = [(c["celda"], v) for c in CELDAS for v in range(1, pol[c["signo"]] + 1)]
    para_el_agua = {(POR_SIGNO["a"]["celda"], 2)}                 # la segunda «a» de la palabra «agua»
    foto_a, foto_r, placas, rotas = {}, {}, {}, []
    for celda_, v in claves:
        c = next(x for x in CELDAS if x["celda"] == celda_)
        if c["estado"] == "manos":
            p = signo_final(azar("signo", v))
        else:
            p = repujar_placa(trazos[celda_], c["estado"] == "reconstruida", celda_, v)
        if v == 1:
            foto_a[celda_] = u8(foto_placa(p, azar("foto", celda_, v)))
            foto_r[celda_] = u8(foto_placa(reverso(p), azar("foto reverso", celda_)))
        if v == 1 or (celda_, v) in para_el_agua:
            placas[(celda_, v)] = dict(altura=p["altura"], relieve=p["relieve"], mascara=p["mascara"])
        for r in p["rotas"][:1]:
            if len(rotas) < 6:
                rotas.append((c["signo"], foto_placa(r, azar("rota", celda_, v))))
        fichas[f"{celda_:02d}.{v:02d}"] = ficha_base(c, v, D, p)
    lamina(foto_r, "Placa por el reverso · simulación",
           "Papel de aluminio de cocina cortado a tijera. El calco, dado vuelta, se repasa por el reverso con un punzón de bola\n"
           "de 1 mm sobre una base blanda: la letra queda al revés y hundida, un canal. Las reconstruidas, a puntos.",
           SALIDA / "04_placa_reverso.jpg")
    lamina(foto_a, "Placa · simulación",
           "La misma placa por el anverso: la letra se lee, en relieve. Foto con luz rasante desde la izquierda (15°).\n"
           "Primera placa de cada celda. La celda 56, una presión de pulgar.", SALIDA / "04_placa.jpg")
    if rotas:
        fila_de_paneles([f for _, f in rotas], [f"«{s}» rota" for s, _ in rotas], SALIDA / "04b_placas_rotas.jpg", alto=260,
                        titulo="Placas que se rompieron: se guardan en la caja y se hace otra")

    # ------------------------------------------------ cinta: la letra con la masking de ojos y boca
    paso("cinta: la letra puesta con masking")
    cintas = {}
    for c in CELDAS:
        if c["estado"] == "manos":
            continue
        img, tramos, pliegues = encintar(D["gramatica"][c["signo"]]["glifo"], V(D["parametros"], "cinta"),
                                         azar("cinta", c["celda"]))
        cintas[c["celda"]] = img
        fichas[f"{c['celda']:02d}.01"]["cinta"] = {"tramos": tramos, "pliegues": pliegues}
    lamina(cintas, "Cinta · simulación",
           "La letra puesta con masking blanca, tirando a hueso, sobre el plástico negro de la plataforma. La cinta no\n"
           "curva en su plano: va recta, se pliega o se superpone. No hace gotas ni asientos. La celda 56 es de los dedos.",
           SALIDA / "07_cinta.jpg", fondo=(0.06, 0.06, 0.08), tinta=(0.85, 0.85, 0.82), junta=(0.12, 0.12, 0.14))

    # ------------------------------------------------ frotado: papel y grafito sobre la placa
    paso("frotado: frotar cada placa hasta que no se lea")
    frotados, legibles = {}, {}
    for c in CELDAS:
        celda_ = c["celda"]
        imgs, n = frotadas(placas[(celda_, 1)], azar("frotado", celda_))
        frotados[celda_] = imgs[1]
        legibles[celda_] = n
        fichas[f"{celda_:02d}.01"]["frotado"] = {"legibles": n}
        if celda_ == POR_SIGNO["a"]["celda"]:
            orden = sorted(imgs)
            fila_de_paneles([imgs[k] for k in orden], [f"frotada {k}" + (" (la última que se lee)" if k == n else "")
                                                         for k in orden],
                            SALIDA / "08b_frotadas_de_la_a.jpg", alto=300,
                            titulo=f"La misma «a» frotada una y otra vez: cada frotada aplasta el relieve. Se leyeron {n}")
    lamina(frotados, "Frotado · simulación",
           "Un papel sobre la placa, por el anverso, frotado con grafito: el mismo gesto con el que empezó todo (la pared).\n"
           "Se marca lo que sobresale. Primera frotada de cada placa; cada una aplasta un poco el relieve.",
           SALIDA / "08_frotado.jpg")

    # ------------------------------------------------ agua: la placa en la bandeja
    paso("agua: quieta y tocada")
    quietas, tocadas = {}, {}
    for c in CELDAS:
        celda_ = c["celda"]
        pl = placas[(celda_, 1)]
        lq, _ = agua(pl, azar("agua", celda_))
        quietas[celda_] = u8(foto_agua(lq, azar("foto agua", celda_)))
        fase = 1.5 + (celda_ % 5) * 0.5
        lt, _ = agua(pl, azar("tocada", celda_), fase=fase)
        tocadas[celda_] = u8(foto_agua(lt, azar("foto tocada", celda_)))
        fichas[f"{celda_:02d}.01"]["agua"] = {"quieta": True, "tocada": True, "fase_de_la_onda": fase,
                                              "contraste_de_la_letra": round(contraste_en_el_agua(lq, pl["relieve"]), 2)}
    lamina(quietas, "Agua quieta · simulación",
           "La placa en el fondo de una bandeja con un dedo de agua; la luz rebota y cae, al revés y en trapecio,\n"
           "sobre dos por dos azulejos sueltos. El punto brillante es la lámpara reflejada en el agua.",
           SALIDA / "09_agua_quieta.jpg", **OSCURO)
    lamina(tocadas, "Agua tocada · simulación",
           "Un dedo toca el agua en una esquina: ondas concéntricas. Cada foto, en otro momento de la onda.",
           SALIDA / "09b_agua_tocada.jpg", **OSCURO)
    gif_agua(placas)

    # ------------------------------------------------ voz: el verso mueve el agua
    paso("voz: el poema leído junto a la bandeja")
    voces = {}
    for c in CELDAS:
        celda_ = c["celda"]
        verso = VERSOS[(celda_ - 1) * len(VERSOS) // len(CELDAS)]
        hz, vol, sil, nsil = voz_del_verso(verso, azar("voz", celda_))
        lv, iv = agua(placas[(celda_, 1)], azar("agua voz", celda_), voz=(hz, vol))
        voces[celda_] = u8(foto_agua(lv, azar("foto voz", celda_)))
        fichas[f"{celda_:02d}.01"]["voz"] = {"verso": verso, "silaba": f"{sil} de {nsil}", "hz": round(hz),
                                             "volumen": round(vol, 2), "lambda_mm": round(iv["lambda_mm"], 1)}
    lamina(voces, "Voz · simulación",
           "El agua vibra con el ritmo silábico del poema, leído una vez mientras se fotografían las 56 placas.\n"
           "Ondas de Faraday: la longitud de onda sale de la altura de la voz (inventada, no la tuya).",
           SALIDA / "10_voz.jpg", **OSCURO)
    gif_voz(placas)

    # ------------------------------------------------ una letra de punta a punta
    paso("una letra de punta a punta")
    for celda_ in (8, 32):
        s = next(c["signo"] for c in CELDAS if c["celda"] == celda_)
        t = D["testigos"].get(s)
        primero = [cuadrado(1 - t["crudo"].astype(np.float32) * 0.9)] if t else [np.ones((T, T), np.float32)]
        paneles = primero + [imagen_cuerpo(D["gramatica"][s]["mascara"]), calcos[celda_], foto_r[celda_], foto_a[celda_],
                             cintas[celda_], frotados[celda_], quietas[celda_], tocadas[celda_], voces[celda_]]
        rot = (["pie (ampliado)"] if t else ["no está en el pie"]) + ["gramática", "calco", "placa, reverso", "placa",
                                                                     "cinta", "frotado", "agua quieta", "agua tocada",
                                                                     "voz"]
        fila_de_paneles(paneles, rot, SALIDA / f"12_cadena_{celda_:02d}.jpg", alto=260,
                        titulo=f"La cadena de una letra: «{s}» (celda {celda_}, {'hallada' if t else 'reconstruida'})")

    # ------------------------------------------------ fichas e informe
    paso("fichas e informe")
    (SALIDA / "fichas_simuladas.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf8")
    informe(D, fichas, pol, legibles)
    paso("listo")


def cuadrado(img, lado=T):
    """La imagen entera en un cuadrado, sin deformarla: se completa con papel."""
    h, w = img.shape[:2]
    k = lado / max(h, w)
    chica = cv2.resize(img, (max(1, round(w * k)), max(1, round(h * k))), interpolation=cv2.INTER_AREA)
    out = np.ones((lado, lado), np.float32)
    y, x = (lado - chica.shape[0]) // 2, (lado - chica.shape[1]) // 2
    out[y:y + chica.shape[0], x:x + chica.shape[1]] = chica
    return out


def ficha_base(c, v, D, p):
    s = c["signo"]
    f = {"placa": f"{s}.{v:02d}", "celda": c["celda"], "signo": s, "variante": v, "estado": c["estado"],
         "mano": "simulación (semilla fija)"}
    if c["estado"] == "hallada":
        t = D["testigos"][s]
        f["pie"] = {"palabra": t["palabra"], "linea": t["linea"], "testigo": t["elegido"], "de": t["de"],
                    "opinion_pct": round(float(t["opinion"]), 1)}
    elif c["estado"] == "reconstruida":
        f["reconstruccion"] = D["receta"][s]
    else:
        f["signo_final"] = "una presión de pulgar genérico: la máquina no tiene dedos"
    if c["estado"] != "manos":
        f["calco"] = {"linea": "punteada" if c["estado"] == "reconstruida" else "continua",
                      "desagues": D["desagues"].get(c["celda"], 0)}
    f["placa_"] = {"intentos": p["intentos"], "roturas": p["roturas"], "minutos": p["minutos"],
                   "recorrido_mm": round(float(p["largo_mm"]))}
    if v == 1 and c["estado"] != "manos":
        g = D["gramatica"][s]["glifo"]
        f["gramatica"] = {"desagues": D["desagues"].get(c["celda"], 0), "alivios": len(g.menos),
                          "partes": sorted({n for n, _ in g.marcas})}
    return f


def gif_agua(placas):
    """La palabra «agua» en el agua tocada, en bucle: cada «a» es otra placa."""
    a, g, u = (POR_SIGNO[s]["celda"] for s in "agu")
    fila = [placas[(a, 1)], placas[(g, 1)], placas[(u, 1)], placas.get((a, 2), placas[(a, 1)])]
    cuadros = [Image.fromarray(a8(f)).convert("P", palette=Image.ADAPTIVE, colors=64)
               for f in agua_tocada_en_bucle(fila, "agua", ancho=900, alto=300)]
    cuadros[0].save(SALIDA / "agua.gif", save_all=True, append_images=cuadros[1:], duration=110, loop=0, optimize=True)


def gif_voz(placas):
    """La palabra «voz» en el agua, movida por una voz: la onda quieta que va y vuelve."""
    fila = [placas[(POR_SIGNO[s]["celda"], 1)] for s in "voz"]
    hz, vol, _, _ = voz_del_verso("acciones para componer una voz", azar("voz", "gif"))
    cuadros = [Image.fromarray(a8(f)).convert("P", palette=Image.ADAPTIVE, colors=64)
               for f in voz_en_bucle(fila, hz, vol, "voz", ancho=720, alto=300)]
    cuadros[0].save(SALIDA / "voz.gif", save_all=True, append_images=cuadros[1:], duration=90, loop=0, optimize=True)


def lamina_pie(D):
    """El pie: en la foto de la lámina y, como testigo de las formas, impreso con una letra sustituta."""
    W = 1700
    bloques = []
    pf = D.get("pie_foto")
    if pf:
        real = pf["imagen"]
        real = cv2.resize(real, (W, int(W * real.shape[0] / real.shape[1])), interpolation=cv2.INTER_AREA)
        m = pf["medidas"]
        bloques.append((f"El pie en la foto de la lámina, enderezado línea por línea. La altura de x mide {coma(m['alto_x'])} px y la tinta "
                        f"se corrió (σ = {coma(m['sigma'], 2)} px):", real))
        bloques.append(("se lee, se mide, pero no se calca: los ojos de la a y de la e se cierran.", None))
    tinta, foto = D["tinta"], D["foto"]
    impreso = 1 - 0.85 * tinta[:, : tinta.shape[1] // 2]
    impreso = cv2.resize(impreso, (W, int(W * impreso.shape[0] / impreso.shape[1])), interpolation=cv2.INTER_AREA)
    fot = foto[:, : foto.shape[1] // 2]
    fot = cv2.resize(fot, (W, int(W * fot.shape[0] / fot.shape[1])), interpolation=cv2.INTER_NEAREST)
    bloques.append((f"El testigo de las formas: el pie impreso con una letra sustituta ({Path(FUENTE_TESTIGO).stem})", None))
    bloques.append(("y tipos de plomo simulados. La tinta se corre, falta o se mella", impreso))
    bloques.append(("Fotografiado con luz rasante, a 12 px por milímetro (ampliado sin suavizar)", fot))
    t = D["testigos"]["a"]
    gens = [cv2.resize(t["recorte"], (int(300 * t["recorte"].shape[1] / t["recorte"].shape[0]), 300), interpolation=cv2.INTER_NEAREST)]
    gens += [cv2.resize(1 - g * 0.9, (int(300 * g.shape[1] / g.shape[0]), 300), interpolation=cv2.INTER_AREA) for g in t["gens"]]
    gens += [cv2.resize(1 - t["mascara"].astype(np.float32) * 0.9, (int(300 * t["mascara"].shape[1] / t["mascara"].shape[0]), 300))]
    cands = D["candidatas"]["e"]
    te = D["testigos"]["e"]
    miniaturas = []
    for cd in cands:
        m_ = cv2.resize(1 - cd["propia"].astype(np.float32) * 0.9, (70, 110), interpolation=cv2.INTER_AREA)
        m_ = np.dstack([m_] * 3)
        if cd["k"] == te["elegido"]:
            for sl in (np.s_[:4], np.s_[-4:], np.s_[:, :4], np.s_[:, -4:]):
                m_[sl] = (0.35, 0.15, 0.55)
        miniaturas.append(m_)
    mini = np.vstack([np.hstack(miniaturas[i:i + 21] + [np.ones((110, 70, 3))] * (21 - len(miniaturas[i:i + 21])))
                      for i in range(0, len(miniaturas), 21)])
    alto = 60 + sum(34 + (b.shape[0] + 16 if b is not None else 0) for _, b in bloques) + 34 + 320 + 34 + mini.shape[0] + 40
    lienzo = Image.new("RGB", (W + 60, alto), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    y = 20
    for texto, img in bloques:
        d.text((30, y), texto, font=rotulo(20), fill=(40, 40, 40))
        y += 34
        if img is not None:
            lienzo.paste(Image.fromarray(a8(a_rgb(img))), (30, y))
            y += img.shape[0] + 16
    d.text((30, y), f"La «a» elegida (testigo {t['elegido']} de {t['de']}, «{t['palabra']}», línea {t['linea']}): la foto, tres "
                    f"fotocopias ampliadas y la opinión ({coma(t['opinion'])} % del borde)", font=rotulo(18), fill=(40, 40, 40))
    y += 34
    x = 30
    for g in gens:
        im = Image.fromarray(a8(a_rgb(g)))
        lienzo.paste(im, (x, y))
        x += im.width + 14
    y += 320
    d.text((30, y), f"Los {len(cands)} testigos de la «e» en el pie; en violeta, el elegido (nº {te['elegido']}, «{te['palabra']}»)",
           font=rotulo(18), fill=(40, 40, 40))
    y += 34
    lienzo.paste(Image.fromarray(a8(mini)), (30, y))
    guardar(SALIDA / "02_el_pie.jpg", lienzo.crop((0, 0, lienzo.width, y + mini.shape[0] + 30)))


TINTA_ANAT = (74, 36, 112)       # el violeta de la tinta para las marcas


def _panel_letra(D, s, lado=900, lineas=True):
    """Una letra grande: su celda, las líneas con nombre, relleno pálido, contorno abierto y sus partes nombradas."""
    from desenterrar import calcar, punto_de_desague
    med = D["med"]
    m = D["gramatica"][s]["mascara"]
    k = lado / T
    img = np.full((T, T, 3), (0.955, 0.95, 0.93), np.float32)
    img[m] = (0.86, 0.85, 0.82)
    tr = calcar(D["gramatica"][s]["geo"], azar("anat", s))
    linea = dibujar_trazos((T, T), tr, s in D["R"], azar("anat l", s), grosor=3)
    img *= (1 - 0.9 * linea)[..., None]
    im = Image.fromarray(a8(img)).resize((lado, lado), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = celda(D["esqueleto"])
    d.rectangle([x0 * k, y0 * k, x1 * k, y1 * k], outline=(190, 186, 176), width=2)
    f = rotulo(22)
    base, xh = med["base"], med["xh"]
    if lineas:
        for y, nombre in ((base + med["desc"], "desagüe"), (base, "fondo"), (base - xh, "borde"), (base - med["asc"], "afuera")):
            yy = int(y * k)
            for x in range(0, lado, 14):
                d.line([(x, yy), (x + 7, yy)], fill=(120, 120, 120), width=1)
            d.text((6, yy - 26), nombre, font=rotulo(18), fill=(110, 110, 110))
    puntos, vistos = [], set()
    for nombre, p in D["marcas"].get(s, []):
        if nombre not in vistos:
            vistos.add(nombre)
            puntos.append((nombre, np.array(p)))
    if tr and "desagüe" not in vistos:
        exterior = max(tr, key=lambda q: np.ptp(q[:, 0]) * np.ptp(q[:, 1]))
        puntos.append(("desagüe del canal", punto_de_desague(exterior)))
    ocupados = []
    for nombre, p in puntos:
        px, py = p[0] * k, p[1] * k
        derecha = px > lado / 2
        tx = lado - 16 if derecha else 130
        ty = py
        while any(abs(ty - o) < 34 for o in ocupados):
            ty += 34
        ocupados.append(ty)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], outline=TINTA_ANAT, width=3)
        ancho = d.textlength(nombre, font=f)
        fin = tx - ancho - 10 if derecha else tx + ancho + 10
        d.line([(px + (9 if derecha else -9), py), (fin, ty)], fill=TINTA_ANAT, width=2)
        d.text((tx - ancho if derecha else tx, ty - 14), nombre, font=f, fill=TINTA_ANAT)
    return im


LETRAS_ANATOMIA = ("a", "g", "k", "á", "8", "ñ")


def lamina_anatomia(D):
    """Seis signos con sus partes nombradas."""
    paneles = [_panel_letra(D, s) for s in LETRAS_ANATOMIA]
    W = 3 * 900 + 4 * 30
    H = 2 * 900 + 3 * 30 + 110
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    d.text((30, 26), "Gramática de Contenida · simulación", font=rotulo(34), fill=(30, 30, 30))
    d.text((30, 72), "Del pie, las medidas. De la obra, la forma: cuenca, desagüe, hombro, asiento, gota, alivio, sifón, "
                     "punto de cinta, tilde, onda, celda.", font=rotulo(20), fill=(90, 90, 90))
    for i, p in enumerate(paneles):
        lienzo.paste(p, (30 + (i % 3) * 930, 110 + (i // 3) * 930))
    guardar(SALIDA / "03c_anatomia.png", lienzo)


def lamina_antes_y_despues(D, letras="aoegrcfsjiáqbp"):
    """Arriba, la letra que dio el pie; en el medio, el cuerpo base de la gramática; abajo, su calco con los desagües."""
    from desenterrar import calcar
    lado = 170
    cols = []
    for s in letras:
        antes = D["antes"][s]
        despues = D["gramatica"][s]["mascara"]
        tr = calcar(D["gramatica"][s]["geo"], azar("ad", s))
        linea = dibujar_trazos((T, T), tr, False, azar("ad l", s), grosor=4)
        celdas = [1 - 0.88 * antes.astype(np.float32), 1 - 0.88 * despues.astype(np.float32), 1 - 0.9 * linea]
        cols.append(np.vstack([cv2.resize(c, (lado, lado), interpolation=cv2.INTER_AREA) for c in celdas]))
    tabla = np.hstack(cols)
    W, H = tabla.shape[1] + 260, tabla.shape[0] + 110
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    lienzo.paste(Image.fromarray(a8(a_rgb(tabla))), (230, 90))
    d = ImageDraw.Draw(lienzo)
    d.text((30, 24), "Antes y después · simulación", font=rotulo(30), fill=(30, 30, 30))
    for i, r in enumerate(("lo que dio el pie", "la gramática", "el calco")):
        d.text((30, 90 + i * lado + lado // 2 - 12), r, font=rotulo(20), fill=(90, 90, 90))
    guardar(SALIDA / "03d_antes_y_despues.png", lienzo)


def informe(D, fichas, pol, legibles):
    med, e = D["med"], D["esqueleto"]
    P = D["parametros"]

    def con(parte):
        return [c["signo"] for c in CELDAS if any(n.startswith(parte) for n, _ in D["marcas"].get(c["signo"], []))]

    def lista(signos):
        return ", ".join(f"«{s}»" for s in signos) or "—"

    halladas = [c for c in CELDAS if c["estado"] == "hallada"]
    placas = list(fichas.values())
    minutos = sum(f["placa_"]["minutos"] for f in placas)
    rot_h = sum(f["placa_"]["roturas"] for f in placas if f["estado"] == "hallada")
    rot_r = sum(f["placa_"]["roturas"] for f in placas if f["estado"] == "reconstruida")
    n_h = sum(1 for f in placas if f["estado"] == "hallada")
    n_r = sum(1 for f in placas if f["estado"] == "reconstruida")
    est = {c["celda"]: c["estado"] for c in CELDAS}
    ch = np.mean([fichas[f"{c:02d}.01"]["agua"]["contraste_de_la_letra"] for c in est if est[c] == "hallada"])
    cr = np.mean([fichas[f"{c:02d}.01"]["agua"]["contraste_de_la_letra"] for c in est if est[c] == "reconstruida"])
    agua_txt = (f"Contraste de la letra en el agua quieta (cuánto se aparta la luz donde cae la letra, contra el resto de la placa): "
                f"{coma(ch, 2)} en las halladas y {coma(cr, 2)} en las reconstruidas. "
                + ("**Lo que la máquina no diseñó y apareció:** las reconstruidas, hechas a puntos, llegan más débiles al agua. "
                   "El punteado tiene menos relieve que el surco y desvía menos luz: en el agua, las hipótesis se ven menos."
                   if cr < ch else "Las reconstruidas no llegan más débiles al agua."))
    sig = {c["celda"]: c["signo"] for c in CELDAS}
    orden = sorted(((c, n) for c, n in legibles.items() if est[c] != "manos"), key=lambda kv: kv[1])
    final = next(n for c, n in legibles.items() if est[c] == "manos")
    fh = np.mean([n for c, n in legibles.items() if est[c] == "hallada"])
    fr = np.mean([n for c, n in legibles.items() if est[c] == "reconstruida"])
    frotado_txt = (f"Las halladas se leen, en promedio, hasta la frotada {coma(fh)}; las reconstruidas, hasta la {coma(fr)}. "
                   + ("**Lo que la máquina no diseñó y apareció:** las hipótesis, hechas a puntos, tienen menos relieve que "
                      "tomar el grafito y se borran antes." if fr < fh else "Las reconstruidas no se borran antes que las halladas."))
    tramos = sum(f.get("cinta", {}).get("tramos", 0) for f in fichas.values())
    pliegues = sum(f.get("cinta", {}).get("pliegues", 0) for f in fichas.values())
    xh = e["xh"]
    foto = (D.get("pie_foto") or {}).get("medidas")
    L = ["# La propuesta de la máquina: el taller simulado",
         "",
         "Generado por `simular.py`. Es una **hipótesis hecha por código**, para confrontarla con la que se haga a mano. "
         "Ninguna de estas formas entra en la caja ni en la fuente: la caja se llena con placas repujadas por una persona.",
         "",
         "La semilla es fija (el 22 de agosto de 2026): el resultado es siempre el mismo. Cambiarla es cambiar de mano.",
         "",
         "La máquina simula seis estados del taller: **calco, placa, cinta, frotado, agua y voz**. Antes arma el testigo del "
         "pie y la gramática, que da el cuerpo base de cada signo.",
         "",
         *(["**Con parámetros ajustados en la aplicación** (`--parametros`): "
            + "; ".join(f"{k} {coma(v, 3 if k == 'razon_x' else 2)}" for k, v in AJUSTES.items())
            + ". El resto sale del pie y de la obra.", ""] if AJUSTES else []),
         "## Lo que la máquina tuvo que suponer",
         "",
         "- **El testigo de las formas.** El pie está en la foto de la lámina, pero la foto no alcanza para calcar: la altura "
         "de x mide unos 12 px y la tinta se corrió; los ojos de la a y de la e se cierran. Las formas del testigo salen de "
         f"una letra de imprenta parecida, **{Path(FUENTE_TESTIGO).stem}**, impresa con tipos de plomo simulados. La foto "
         "queda para mirar el pie real y para medirlo (más abajo, *Lo que dice la foto*).",
         "- **El cuerpo del pie:** 8,5 puntos.",
         "- **La piscina:** azulejo de 150 mm y junta de 3 mm, hasta que se mida. La pared da el frotado sobre el que se calca.",
         "- **La celda:** 0,84 de ancho por alto, la proporción de las celdas de la cabeza del ídolo. En la foto cercana de la "
         "cabeza, el paso de la retícula de 8 × 7 mide 0,81 en los bordes y 0,91 al centro (promedio 0,86): el dibujo curva "
         "la cabeza como un cilindro. El 0,84 cae dentro.",
         "- **El frotado:** cada frotada aplasta entre un 5 y un 9 % del relieve del surco. Es un supuesto: se mide frotando.",
         "- **La voz:** no es la tuya. Es el ritmo silábico del poema, con alturas inventadas entre 110 y 220 Hz.",
         "- **El signo final:** la máquina no tiene dedos. Simula una sola presión de un pulgar genérico.",
         "",
         "## El pie",
         "",
         "![El pie](salida/02_el_pie.jpg)",
         "",
         "Para cada signo hallado, la máquina amplió todos sus testigos en tres generaciones de fotocopia y eligió el mejor "
         "conservado: el que tiene las partes que debe tener (la i, dos) y el borde menos roto. La *opinión* es cuánto del "
         "borde tuvo que decidir al limpiar.",
         "",
         "| Celda | Signo | Testigo elegido | Palabra | Línea | Opinión |",
         "|---|---|---|---|---|---|"]
    for c in halladas:
        t = D["testigos"][c["signo"]]
        L.append(f"| {c['celda']} | `{c['signo']}` | {t['elegido']} de {t['de']} | {t['palabra']} | {t['linea']} | {coma(t['opinion'])} % |")
    if foto:
        L += ["",
              "### Lo que dice la foto",
              "",
              "`extraer_testigos.py` endereza las cuatro líneas de la foto (la tercera sube sobre el pliegue del papel), deshace "
              "en parte el desenfoque y corta cada palabra en sus letras, como con tijera. Las 336 letras quedan en "
              "`testigos/`, sin la foto. Lo que se puede medir, contra el sustituto:",
              "",
              "| Medida | La foto | El sustituto |",
              "|---|---|---|",
              f"| Altura de x | {coma(foto['alto_x'])} px de foto | — |",
              f"| Ascendentes, sobre la altura de x | {coma(foto['ascendente'] / foto['alto_x'], 2)} | {coma((e['fondo'] - e['afuera']) / xh, 2)} |",
              f"| Descendentes, sobre la altura de x | {coma(foto['descendente'] / foto['alto_x'], 2)} | {coma((e['desague'] - e['fondo']) / xh, 2)} |",
              f"| Trazo, sobre la altura de x | {coma(foto['asta'] / foto['alto_x'], 2)} o más | {coma(e['canal'] / xh, 2)} (el canal) |",
              f"| Desenfoque de la foto | σ = {coma(foto['sigma'], 2)} px | — |",
              "",
              f"El trazo se mide por la tinta que junta, no por su borde: el desenfoque corre la tinta, pero no cambia cuánta "
              f"hay. En {foto['trazos']} trazos aislados, el pico y la tinta total dan el desenfoque; la tinta llena no se puede "
              "despejar, porque todos los trazos son más finos que el desenfoque. Se la toma como negro pleno, y el ancho que "
              "resulta es un mínimo. El pie real tiene ascendentes más largas, descendentes más cortas y un trazo más "
              "grueso que el sustituto."]
    L += ["",
          "## La gramática",
          "",
          "La anatomía base se construye antes de los estados, en vectores (`03c_gramatica.md`, `gramatica.py`). Del pie se "
          "toman medidas; la forma la dictan parámetros que salen de la obra. Cuatro generadores (o, l, n, a) dan las partes; "
          "con ellas se arman los 55 signos: los elementos forman motivos y los motivos, signos.",
          "",
          "![Generadores](salida/20_gramatica.png)",
          "",
          "![Los 55](salida/21_gramatica_caja.png)",
          "",
          "![Partes](salida/03c_anatomia.png)",
          "",
          "![Antes y después](salida/03d_antes_y_despues.png)",
          "",
          "| Parámetro | Valor | Qué controla | De dónde sale |",
          "|---|---|---|---|"]
    L += [f"| `{k}` | {str(v['valor']).replace('.', ',')} {v['unidad']} | {v['que']} | {v['de_donde']} |" for k, v in P.items()]
    L += ["",
          "| Parte | Signos |",
          "|---|---|",
          f"| La cuenca con su desagüe | {lista(con('desagüe'))} |",
          f"| El asiento | {lista(con('asiento'))} |",
          f"| La gota | {lista(con('gota'))} |",
          f"| El alivio | {lista(con('alivio'))} |",
          f"| El punto de cinta | {lista(con('punto'))} |",
          f"| La tilde en gota | {lista(con('tilde'))} |",
          f"| El sifón | {lista(con('sifón'))} |",
          f"| La onda | {lista(con('onda'))} |",
          f"| La celda | {lista(con('celda'))} |",
          "",
          "**Las reconstrucciones:**",
          "",
          "| Signo | Receta |", "|---|---|"]
    for c in CELDAS:
        if c["estado"] == "reconstruida":
            L.append(f"| `{c['signo']}` | {D['receta'][c['signo']]} |")
    L += ["",
          "Una decisión propia de la máquina: **cifras elzevirianas**, de altura de x, con 6 y 8 que suben y 3, 4, 5, 7 y 9 "
          "que bajan. Cada cifra vive en su celda: un rectángulo dentro de otro, con desagüe.",
          "",
          "**Los dobles opuestos varían.** En la litoescultura de Tiwanaku, las figuras enfrentadas casi nunca son idénticas "
          "(Agüero, Uribe y Berenguer 2003). Aquí tampoco: la ¿ no es la ? dada vuelta, ni el 9 el 6, porque la gravedad no "
          "se da vuelta: la gota cae siempre hacia abajo, y el terminal que mira arriba termina en un corte.",
          "",
          "## Calco",
          "",
          "![Frotado](salida/01_frotado_de_la_pared.jpg)",
          "",
          "Un paño de 8 × 7 azulejos con juntas torcidas, craquelado, manchas y desportillados. En el frotado se marca lo que "
          "sobresale: juntas y grietas quedan blancas; las manchas no salen, porque no tienen relieve. Sobre ese frotado se "
          "pone el papel de calco.",
          "",
          "![Calco](salida/03_calco.png)",
          "",
          "Se calca el cuerpo de la gramática, en vectores: su contorno, con el temblor de la mano, abierto en su punto más "
          f"bajo. {sum(D['desagues'].values())} desagües en 55 signos. **La escala la decidió el pie:** la letra más alta y la "
          "más baja caben en la placa con aire. Medidas desde el fondo:",
          "",
          "| Línea | Desde el fondo |",
          "|---|---|",
          f"| Afuera (ascendentes) | {coma(med['asc'] / 4)} mm |",
          f"| Borde (altura de x) | {coma(med['xh'] / 4)} mm |",
          "| Fondo (base) | 0 |",
          f"| Desagüe (descendentes) | −{coma(med['desc'] / 4)} mm |",
          "",
          f"El trazo grueso de la o del testigo mide {coma(med['grueso'] / 4)} mm y el fino, {coma(med['fino'] / 4)} mm. El "
          f"canal de la gramática, sin contraste, mide {coma(med['canal'] / 4)} mm: la media entre los dos. "
          + ("Ningún signo desborda la placa." if not D["desbordes"]
             else "Desbordan: " + ", ".join(f"«{k}» {v} mm" for k, v in D["desbordes"].items()) + "."),
          "",
          "El `.notdef`, la celda de la lámina calcada: ![notdef](salida/03b_notdef.png)",
          "",
          "## Placa",
          "",
          "![Placa por el reverso](salida/04_placa_reverso.jpg)",
          "",
          "![Placa](salida/04_placa.jpg)",
          "",
          "Papel de aluminio de cocina, cortado a tijera: cada lado en dos o tres cortes, con un escalón donde la tijera se "
          "retoma y, a veces, una esquina cortada en diagonal. El calco se da vuelta y se repasa por el reverso con un punzón "
          "de bola de 1 mm sobre una base blanda. Por el reverso la letra queda al revés y hundida: una canaleta con dos lomas "
          "bajas, un canal. Por el anverso se lee, en relieve. Donde la mano arranca y donde se detiene, el punzón hunde un "
          "poco más; cerca del surco, las arrugas de la hoja se alisan.",
          "",
          f"- **119 placas** ({n_h} de signos hallados, {n_r} reconstruidos y {pol['¶']} signo final).",
          f"- **Tiempo simulado:** {coma(minutos / 60)} horas de repujado, contando las placas que se rompieron. El plan "
          "estimaba entre 30 y 40. La máquina supuso 20 mm de surco por minuto, 9 mm de punteado por minuto y 4 minutos "
          "para preparar cada placa.",
          f"- **Roturas:** {rot_h} en {n_h} placas halladas y {rot_r} en {n_r} reconstruidas. La máquina supuso que el "
          "punteado perfora: una placa punteada se rompe con más probabilidad (16 % por intento contra 6 %).",
          "",
          "![Rotas](salida/04b_placas_rotas.jpg)",
          "",
          "## Cinta",
          "",
          "![Cinta](salida/07_cinta.jpg)",
          "",
          "La letra puesta con masking blanca, tirando a hueso claro, sobre el plástico negro de la plataforma: la cinta que "
          f"tapó ojos y boca. Va recta; para girar se pliega o se superpone. Hicieron falta {tramos} tramos y {pliegues} "
          "pliegues para los 55 signos. No hace gotas ni asientos: en la cinta, la letra pierde lo que le daba la gravedad.",
          "",
          "## Frotado",
          "",
          "![Frotado](salida/08_frotado.jpg)",
          "",
          "![Frotadas de la a](salida/08b_frotadas_de_la_a.jpg)",
          "",
          "Un papel sobre la placa, por el anverso, frotado con grafito: el gesto de la acción 1, ahora sobre la letra. El papel "
          "no entra en los valles finos; toca toda la hoja y se carga donde la placa sube por encima de su entorno. Se frota "
          "hasta que la letra no se lee: **el peso de una letra se mide en frotadas.** " + frotado_txt,
          "",
          "**Las primeras en borrarse:** " + ", ".join(f"«{sig[c]}» ({n})" for c, n in orden[:8]) + ".",
          "",
          "**Las últimas:** " + ", ".join(f"«{sig[c]}» ({n})" for c, n in orden[-8:]) + ".",
          "",
          (f"El signo final, una presión de pulgar, da {final} frotadas legibles: el domo es liso y el papel lo acompaña; "
           "solo marca el filo." if final == 0 else f"El signo final, una presión de pulgar, da {final} frotadas legibles."),
          "",
          "## Agua",
          "",
          "![Agua quieta](salida/09_agua_quieta.jpg)",
          "",
          "![Agua tocada](salida/09b_agua_tocada.jpg)",
          "",
          "![agua](salida/agua.gif)",
          "",
          "La placa, por el anverso, en el fondo de una bandeja con un dedo de agua. " + agua_txt,
          "",
          "## Voz",
          "",
          "![Voz](salida/10_voz.jpg)",
          "",
          "![voz](salida/voz.gif)",
          "",
          "El poema se lee una vez en voz alta junto a la bandeja, mientras se fotografían las 56 placas: a cada placa le toca "
          "una sílaba de su verso. El agua responde con ondas de Faraday, a la mitad de la frecuencia de la voz; cuanto más "
          f"aguda la sílaba, más corta la onda (entre {coma(min(f['voz']['lambda_mm'] for f in fichas.values() if 'voz' in f))} "
          f"y {coma(max(f['voz']['lambda_mm'] for f in fichas.values() if 'voz' in f))} mm). Con volumen alto, la onda cruza "
          "tres frentes en lugar de dos.",
          "",
          "## Una letra de punta a punta",
          "",
          "![a](salida/12_cadena_08.jpg)",
          "",
          "![z](salida/12_cadena_32.jpg)",
          "",
          "## Lo que la máquina no sabe",
          "",
          "- **El libro:** qué letra tiene el pie en su tamaño real, ni cómo se imprimió. La foto da sus medidas, no sus formas.",
          "- **La mano:** el temblor es ruido con un ritmo; no cansa, no duda, no se distrae.",
          "- **El aluminio:** cómo se rompe de verdad. Aquí se rompe con una probabilidad.",
          "- **El grafito:** cuánto relieve se lleva cada frotada.",
          "- **La cinta:** cómo se despega de verdad; aquí cada tramo deja un residuo supuesto.",
          "- **El agua:** un solo rebote, un eco desplazado y ninguna polarización.",
          "- **La voz:** no es la tuya.",
          "",
          "## Cómo confrontar",
          "",
          "Cuando exista tu propuesta, conviene guardarla con los mismos nombres para compararlas placa por placa:",
          "",
          "- **Fotos:** `tipografia/mano/<estado>/<celda>_<variante>.jpg`, con dos dígitos (`mano/placa/08_01.jpg`) y estas "
          "carpetas de estado: `calco`, `placa`, `cinta`, `frotado`, `agua`, `voz`.",
          "- **Fichas:** `tipografia/mano/fichas.json`, con los mismos campos que `salida/fichas_simuladas.json`.",
          "",
          "**Qué se compara:**",
          "",
          "1. **Forma:** la silueta de cada calco superpuesta a la de la máquina, en dos colores; qué testigo eligió cada una "
          "y cuánto opinó.",
          "2. **Métricas:** la base y la altura de x que dio la foto contra las que dio el testigo sustituto.",
          "3. **Reconstrucciones:** las 25 recetas de la máquina contra las tuyas. Es donde más van a diferir, y donde más "
          "interesa.",
          "4. **Tiempo y roturas:** horas, intentos y roturas por placa.",
          "5. **Frotado:** cuántas frotadas se leen, y qué signos se borran primero.",
          "6. **Agua:** si las reconstruidas también llegan más débiles.",
          "7. **Voz:** qué sílaba le tocó a cada placa y qué onda dejó.",
          ""]
    (SALIDA.parent / "informe.md").write_text("\n".join(L), encoding="utf8")


if __name__ == "__main__":
    import sys
    from comun import argumento_parametros
    argumento_parametros(sys.argv)
    main()
