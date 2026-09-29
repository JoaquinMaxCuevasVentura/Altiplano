"""Simula el taller analógico de Contenida: la propuesta de la máquina.

Uso (desde la raíz del repositorio, después de inventario.py):
    pip install numpy opencv-python-headless pillow scikit-image
    python3 tipografia/simulacion/simular.py

Corre las acciones 1 a 11 de 04_taller_analogico.md sobre las 56 celdas y las
119 placas y escribe en tipografia/simulacion/salida/:
  láminas (JPG y PNG) por acción y por estado,
  voz.gif (la palabra «voz» en el agua tocada),
  fichas_simuladas.json (una ficha por placa, con los campos de la ficha de hallazgo),
  informe.md (lo que decidió la máquina, con sus números).

Es una hipótesis hecha por código para confrontarla con la que se haga a mano.
Ninguna de estas formas entra en la caja ni en la fuente.
Tarda unos minutos. La semilla es fija: da siempre el mismo resultado.
"""

import json
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from comun import (BUCLE_MIN, CELDAS, FUENTE_TESTIGO, GLIFOS, POR_SIGNO, SALIDA, T, TES, VERSOS, a8, a_rgb, azar,
                   caja_tinta, componentes, fila_de_paneles, guardar, lamina, poliza, rotulo)
from contener import caja_abierta, caja_cerrada, foto_placa, repujar_placa, sesiones_de_vestir, signo_final, vestir
from desenterrar import calco, celda_notdef, desenterrar, dibujar_trazos, frotado, pared
from devolver import (agua, armar_matriz, aterrizar, componer, foto_agua, hectografiar, la_bandeja_bebe, matriz_de,
                      pagina, voz_del_verso)

ESTROFA = ["cada vuelta pasa por el agua", "y el agua no repite,", "la misma diosa dos veces", "y ninguna igual."]


def coma(x, d=1):
    """Números con coma decimal."""
    return f"{x:.{d}f}".replace(".", ",")


def contraste_en_el_agua(luz, relieve):
    """Cuánto se aparta la luz de su entorno donde cae la letra, contra el resto de la placa."""
    desvio = np.abs(luz - cv2.GaussianBlur(luz, (0, 0), 16))
    letra = cv2.dilate((relieve > 0.32).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
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

    # ------------------------------------------------ acción 1: medir y frotar
    paso("acción 1: la pared y su frotado")
    P = pared(7, 8, 300, azar("pared"))
    F = frotado(P, azar("frotado"))
    guardar(SALIDA / "01_frotado_de_la_pared.jpg", cv2.resize(F, (1600, int(1600 * F.shape[0] / F.shape[1])), interpolation=cv2.INTER_AREA))
    fondos = {}
    j, px = P["junta"], P["px"]
    for c in CELDAS:
        x = j + (c["columna"] - 1) * (px + j)
        y = j + (c["fila"] - 1) * (px + j)
        fondos[c["celda"]] = cv2.resize(F[y:y + px, x:x + px], (T, T), interpolation=cv2.INTER_LINEAR)

    # ------------------------------------------------ acciones 2 y 3: el pie, la escala, el calco
    paso("acciones 2 y 3: el pie, los testigos, la escala y las reconstrucciones")
    D = desenterrar()
    med = D["med"]
    lamina_pie(D)
    calcos, trazos = {}, {}
    for c in CELDAS:
        s = c["signo"]
        if c["estado"] == "manos":
            calcos[c["celda"]] = 1 - 0.22 * (1 - fondos[c["celda"]])
            continue
        m = D["M"][s] if c["estado"] == "hallada" else D["R"][s]
        cv2.imwrite(str(GLIFOS / f"forma_{c['celda']:02d}.png"), (~m).astype(np.uint8) * 255)
        img, tr = calco(m, c["estado"] == "reconstruida", fondos[c["celda"]], med, azar("calco", c["celda"]))
        calcos[c["celda"]], trazos[c["celda"]] = img, tr
    D["desagues"] = {celda: len(tr) for celda, tr in trazos.items()}
    lamina(calcos, "Calco · simulación",
           "Continuo lo hallado, punteado lo reconstruido: solo el contorno, abierto en su punto más bajo (el desagüe).\n"
           f"Fondo a {coma(med['base_teselas'])} teselas, borde a {coma(med['x_teselas'])}. La celda 56 no se calca: se hace con los dedos.",
           SALIDA / "03_calco.png")
    notdef = dibujar_trazos((T, T), celda_notdef(azar("notdef")), False, azar("notdef"))
    guardar(SALIDA / "03b_notdef.png", 1 - 0.85 * notdef)
    lamina_anatomia(D)
    lamina_antes_y_despues(D)

    # ------------------------------------------------ acción 4 y 6: repujar y vestir
    paso("acciones 4 y 6: repujar 119 placas y vestirlas")
    claves = [(c["celda"], v) for c in CELDAS for v in range(1, pol[c["signo"]] + 1)]
    sesiones = sesiones_de_vestir(claves)
    foto_p, foto_v, vestidas, rotas = {}, {}, {}, []
    for celda, v in claves:
        c = next(x for x in CELDAS if x["celda"] == celda)
        if c["estado"] == "manos":
            p = signo_final(azar("signo", v))
        else:
            p = repujar_placa(trazos[celda], c["estado"] == "reconstruida", celda, v)
        foto_p[(celda, v)] = u8(foto_placa(p, azar("foto", celda, v)))
        for r in p["rotas"][:1]:
            if len(rotas) < 6:
                rotas.append((c["signo"], foto_placa(r, azar("rota", celda, v))))
        parte, ang, minutos, sesion = sesiones[(celda, v)]
        vs = vestir(p, parte, ang, minutos, azar("vestir", celda, v))
        foto_v[(celda, v)] = u8(foto_placa(vs, azar("foto piel", celda, v)))
        if v == 1:
            vestidas[celda] = dict(altura=vs["altura"].astype(np.float32), relieve=vs["relieve"].astype(np.float16),
                                   pliegues=vs["pliegues"].astype(np.float16), mascara=vs["mascara"])
        fichas[f"{celda:02d}.{v:02d}"] = ficha_base(c, v, D, p, vs, sesion)
    lamina({k[0]: f for k, f in foto_p.items() if k[1] == 1}, "Placa · simulación",
           "Papel de aluminio repujado por el reverso con un punzón de 1 mm; foto con luz rasante desde la izquierda (15°).\n"
           "Las reconstruidas, a puntos. Primera placa de cada celda.", SALIDA / "04_placa.jpg")
    if rotas:
        fila_de_paneles([f for _, f in rotas], [f"«{s}» rota" for s, _ in rotas], SALIDA / "04b_placas_rotas.jpg", alto=260,
                        titulo="Placas que se rompieron: se guardan en la caja y se hace otra")
    lamina({k[0]: f for k, f in foto_v.items() if k[1] == 1}, "Piel · simulación",
           f"La placa vestida {BUCLE_MIN} minutos (el bucle, supuesto) y aplanada con la palma. Los pliegues siguen el eje\n"
           "de la parte del cuerpo: antebrazo, esternón, cadera, muslo, espalda, hombro, por sesiones de seis.", SALIDA / "06_piel.jpg")

    # ------------------------------------------------ acción 5: la caja
    paso("acción 5: la caja")
    fl = {k: f.astype(np.float32) / 255 for k, f in foto_v.items()}
    guardar(SALIDA / "05_caja_abierta.jpg", caja_abierta(fl, pol, CELDAS, azar("caja")))
    guardar(SALIDA / "05b_caja_cerrada.jpg", caja_cerrada(fl[(1, 1)], azar("tapa")))

    # ------------------------------------------------ acción 8: hectógrafo
    paso("acción 8: el hectógrafo")
    matrices = {c: matriz_de(v) for c, v in vestidas.items()}
    mat, cajas = armar_matriz(matrices, CELDAS)
    copias, ultima, tirada, gel = hectografiar(mat, cajas, matrices, azar("hectografo"))
    for celda, n in ultima.items():
        for k in fichas:
            if int(k[:2]) == celda and k.endswith(".01"):
                fichas[k]["copia"] = {"hectografo": 1, "ultima_legible": n, "tirada": tirada}
    lamina_hectografo(copias, tirada, ultima, gel, cajas)

    # ------------------------------------------------ acciones 9, 10 y 11: agua, voz, pared
    paso("acciones 9 a 11: agua, voz y pared")
    quietas, tocadas, voces, azulejos = {}, {}, {}, {}
    for c in CELDAS:
        celda = c["celda"]
        vs = vestidas[celda]
        vs = dict(vs, relieve=vs["relieve"].astype(np.float32), pliegues=vs["pliegues"].astype(np.float32))
        lq, iq = agua(vs, azar("agua", celda))
        quietas[celda] = u8(foto_agua(lq, azar("foto agua", celda)))
        fase = 1.5 + (celda % 5) * 0.5
        lt, _ = agua(vs, azar("tocada", celda), fase=fase)
        tocadas[celda] = u8(foto_agua(lt, azar("foto tocada", celda)))
        verso = VERSOS[(celda - 1) * len(VERSOS) // len(CELDAS)]
        hz, vol, sil, nsil = voz_del_verso(verso, azar("voz", celda))
        lv, iv = agua(vs, azar("agua voz", celda), voz=(hz, vol))
        voces[celda] = u8(foto_agua(lv, azar("foto voz", celda)))
        foto_pared, calco_pared, n_juntas, (x, y, l) = aterrizar(lq, vs, iq["superficie"], azar("pared", celda))
        azulejos[celda] = u8(cv2.resize(calco_pared[y:y + l, x:x + l], (T, T), interpolation=cv2.INTER_AREA))
        k1 = f"{celda:02d}.01"
        fichas[k1]["agua"] = {"quieta": True, "tocada": True, "fase_de_la_onda": fase,
                              "contraste_de_la_letra": round(contraste_en_el_agua(lq, vs["relieve"]), 2)}
        fichas[k1]["voz"] = {"verso": verso, "silaba": f"{sil} de {nsil}", "hz": round(hz), "volumen": round(vol, 2),
                             "lambda_mm": round(iv["lambda_mm"], 1)}
        fichas[k1]["azulejo"] = {"juntas_que_la_cortan": n_juntas}
    lamina(quietas, "Agua quieta · simulación",
           "La placa en el fondo de una bandeja con un dedo de agua; la luz rebota y cae, al revés y en trapecio,\n"
           "sobre dos por dos azulejos sueltos. El punto brillante es la lámpara reflejada en el agua.", SALIDA / "09_agua_quieta.jpg",
           fondo=(0.06, 0.06, 0.08), tinta=(0.85, 0.9, 0.85), junta=(0.12, 0.12, 0.14))
    lamina(tocadas, "Agua tocada · simulación", "Un dedo toca el agua en una esquina: ondas concéntricas. Cada foto, en otro momento de la onda.",
           SALIDA / "09b_agua_tocada.jpg", fondo=(0.06, 0.06, 0.08), tinta=(0.85, 0.9, 0.85), junta=(0.12, 0.12, 0.14))
    lamina(voces, "Voz · simulación",
           "El agua vibra con el ritmo silábico del poema, leído una vez mientras se fotografían las 56 placas.\n"
           "Ondas de Faraday: la longitud de onda sale de la altura de la voz (inventada, no la tuya).", SALIDA / "10_voz.jpg",
           fondo=(0.06, 0.06, 0.08), tinta=(0.85, 0.9, 0.85), junta=(0.12, 0.12, 0.14))
    lamina(azulejos, "Azulejo · simulación",
           "La luz de la letra cae ampliada en la pared de la piscina y se calca lo que quedó:\n"
           "al revés, en trapecio y cortada por las juntas (quien calca no puede seguirla por la junta).", SALIDA / "11_azulejo.png")

    # ------------------------------------------------ componer un verso y la cadena de una letra
    paso("acción 11: componer una estrofa en la pared")
    fotos_por_signo = {(c["signo"], v): foto_v[(c["celda"], v)].astype(np.float32) / 255
                       for c in CELDAS for v in range(1, pol[c["signo"]] + 1)}
    img, usadas = componer(ESTROFA, fotos_por_signo, azar("componer"))
    guardar(SALIDA / "11b_estrofa_en_la_pared.jpg", img)
    for celda in (8, 32):
        s = next(c["signo"] for c in CELDAS if c["celda"] == celda)
        t = D["testigos"].get(s)
        primero = [cv2.resize(1 - t["crudo"].astype(np.float32) * 0.9, (T, T))] if t else [np.ones((T, T), np.float32)]
        paneles = primero + [calcos[celda], foto_p[(celda, 1)], foto_v[(celda, 1)], quietas[celda], tocadas[celda],
                             voces[celda], azulejos[celda]]
        rot = (["pie (ampliado)"] if t else ["no está en el pie"]) + ["calco", "placa", "piel", "agua quieta", "agua tocada", "voz", "azulejo"]
        fila_de_paneles(paneles, rot, SALIDA / f"12_cadena_{celda:02d}.jpg", alto=260,
                        titulo=f"La cadena de una letra: «{s}» (celda {celda}, {'hallada' if t else 'reconstruida'})")
    gif_voz(vestidas)

    # ------------------------------------------------ fichas e informe
    paso("fichas e informe")
    (SALIDA / "fichas_simuladas.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf8")
    informe(D, fichas, ultima, tirada, pol)
    paso("listo")


def ficha_base(c, v, D, p, vs, sesion):
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
    f["placa_"] = {"intentos": p["intentos"], "roturas": p["roturas"], "minutos": p["minutos"],
                   "recorrido_mm": round(float(p["largo_mm"]))}
    f["piel"] = {"parte": vs["parte"], "minutos": vs["minutos"], "sesion": sesion, "pliegues": vs["n_pliegues"]}
    if v == 1 and c["estado"] != "manos":
        f["anatomia"] = {"desagues": D["desagues"].get(c["celda"], 0), "asta_en": D["astas"].get(s)}
        f["anatomia"].update({k: len(p_) for k, p_ in D["marcas"].get(s, {}).items() if p_})
    return f


def lamina_pie(D):
    """El pie impreso, fotografiado y ampliado; y los testigos de la «e»."""
    tinta, foto = D["tinta"], D["foto"]
    W = 1700
    impreso = 1 - 0.85 * tinta[:, : tinta.shape[1] // 2]
    impreso = cv2.resize(impreso, (W, int(W * impreso.shape[0] / impreso.shape[1])), interpolation=cv2.INTER_AREA)
    fot = foto[:, : foto.shape[1] // 2]
    fot = cv2.resize(fot, (W, int(W * fot.shape[0] / fot.shape[1])), interpolation=cv2.INTER_NEAREST)
    t = D["testigos"]["a"]
    gens = [cv2.resize(t["recorte"], (int(300 * t["recorte"].shape[1] / t["recorte"].shape[0]), 300), interpolation=cv2.INTER_NEAREST)]
    gens += [cv2.resize(1 - g * 0.9, (int(300 * g.shape[1] / g.shape[0]), 300), interpolation=cv2.INTER_AREA) for g in t["gens"]]
    gens += [cv2.resize(1 - t["mascara"].astype(np.float32) * 0.9, (int(300 * t["mascara"].shape[1] / t["mascara"].shape[0]), 300))]
    cands = D["candidatas"]["e"]
    miniaturas = []
    for cd in cands:
        m = cv2.resize(1 - cd["propia"].astype(np.float32) * 0.9, (70, 110), interpolation=cv2.INTER_AREA)
        m = np.dstack([m] * 3)
        if cd["k"] == t_e(D):
            m[:4], m[-4:], m[:, :4], m[:, -4:] = (0.35, 0.15, 0.55), (0.35, 0.15, 0.55), (0.35, 0.15, 0.55), (0.35, 0.15, 0.55)
        miniaturas.append(m)
    filas_m = [np.hstack(miniaturas[i:i + 21] + [np.ones((110, 70, 3))] * (21 - len(miniaturas[i:i + 21]))) for i in range(0, len(miniaturas), 21)]
    mini = np.vstack(filas_m)
    lienzo = Image.new("RGB", (W + 60, 60 + impreso.shape[0] + fot.shape[0] + 440 + mini.shape[0] + 200), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    y = 20
    d.text((30, y), "El pie, impreso con tipos de plomo (simulado): la tinta se corre, falta o se mella", font=rotulo(20), fill=(40, 40, 40))
    y += 34
    lienzo.paste(Image.fromarray(a8(a_rgb(impreso))), (30, y)); y += impreso.shape[0] + 16
    d.text((30, y), "Fotografiado con luz rasante, a 12 px por milímetro (ampliado sin suavizar)", font=rotulo(20), fill=(40, 40, 40)); y += 34
    lienzo.paste(Image.fromarray(a8(a_rgb(fot))), (30, y)); y += fot.shape[0] + 24
    d.text((30, y), f"La «a» elegida (testigo {t['elegido']} de {t['de']}, «{t['palabra']}», línea {t['linea']}): foto, tres fotocopias ampliadas y la opinión ({coma(t['opinion'])} % del borde)",
           font=rotulo(18), fill=(40, 40, 40)); y += 34
    x = 30
    for g in gens:
        im = Image.fromarray(a8(a_rgb(g)))
        lienzo.paste(im, (x, y)); x += im.width + 14
    y += 320
    te = D["testigos"]["e"]
    d.text((30, y), f"Los {len(cands)} testigos de la «e» en el pie; en violeta, el elegido (nº {te['elegido']}, «{te['palabra']}»)", font=rotulo(18), fill=(40, 40, 40)); y += 34
    lienzo.paste(Image.fromarray(a8(mini)), (30, y))
    guardar(SALIDA / "02_el_pie.jpg", lienzo.crop((0, 0, lienzo.width, y + mini.shape[0] + 30)))


TINTA_ANAT = (74, 36, 112)       # violeta de hectógrafo para las marcas


def _panel_letra(D, s, marcas_extra=(), lado=900, lineas=True, solo_derecha=False):
    """Una letra grande: retícula de teselas, líneas con nombre, relleno pálido, contorno con desagües."""
    from desenterrar import contornos_temblorosos, dibujar_trazos, punto_de_desague
    med = D["med"]
    m = D["M"].get(s, D["R"].get(s))
    k = lado / T
    img = np.full((T, T, 3), (0.955, 0.95, 0.93), np.float32)
    for i in range(1, 6):
        img[i * TES, :] *= 0.88
        img[:, i * TES] *= 0.88
    img[m] = (0.86, 0.85, 0.82)
    tr = contornos_temblorosos(m, azar("anat", s))
    linea = dibujar_trazos((T, T), tr, s in D["R"], azar("anat l", s), grosor=3)
    img *= (1 - 0.9 * linea)[..., None]
    im = Image.fromarray(a8(img)).resize((lado, lado), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    f = rotulo(22)
    base, xh = med["base"], med["xh"]
    if lineas:
        for y, nombre in ((base + med["desc"], "desagüe"), (base, "fondo"), (base - xh, "borde"), (base - med["asc"], "afuera")):
            yy = int(y * k)
            for x in range(0, lado, 14):
                d.line([(x, yy), (x + 7, yy)], fill=(120, 120, 120), width=1)
            d.text((6, yy - 26), nombre, font=rotulo(18), fill=(110, 110, 110))
    puntos = []
    if tr:
        exterior = max(tr, key=lambda q: np.ptp(q[:, 0]) * np.ptp(q[:, 1]))
        puntos.append(("desagüe", punto_de_desague(exterior)))
    mk = D["marcas"].get(s, {})
    for regla, nombre in (("bandejas", "bandeja"), ("gotas", "gota"), ("puntos", "tesela"), ("tildes", "tilde: gota")):
        for p in mk.get(regla, [])[:1]:
            puntos.append((nombre, np.array(p)))
    partes = [c for c in componentes(m) if c[1][2] < 3 * TES] or componentes(m)   # sin el marco de la celda
    cuerpo = max(partes, key=lambda c: c[1][4])[0]
    dist = cv2.distanceTransform(cuerpo.astype(np.uint8), cv2.DIST_L2, 5)
    yx = np.unravel_index(np.argmax(dist), dist.shape)
    puntos.append(("canal", np.array([yx[1], yx[0]], float)))
    puntos += list(marcas_extra)
    ocupados = []
    for nombre, p in puntos:
        px, py = p[0] * k, p[1] * k
        derecha = solo_derecha or px > lado / 2
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


def lamina_anatomia(D):
    """Seis letras con sus partes nombradas."""
    med = D["med"]
    extra = {"a": [("remate gastado", np.array([D["astas"].get("a") or T / 2, med["base"] - 4]))]}
    o8 = D["R"]["8"]
    x0, y0, x1, y1 = caja_tinta(o8)
    extra["8"] = [("celda", np.array([x1 - 3, (y0 + y1) / 2 + 60]))]
    comps = [c for c in componentes(D["R"]["ñ"]) if c[2][1] < med["base"] - med["xh"] * 1.05]
    if comps:
        extra["ñ"] = [("onda", np.array(comps[0][2]))]
    paneles = [_panel_letra(D, s, extra.get(s, ()), solo_derecha=(s == "8")) for s in ("a", "o", "j", "á", "8", "ñ")]
    W = 3 * 900 + 4 * 30
    H = 2 * 900 + 3 * 30 + 110
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    d = ImageDraw.Draw(lienzo)
    d.text((30, 26), "Anatomía de Contenida · simulación", font=rotulo(34), fill=(30, 30, 30))
    d.text((30, 72), "Del pie, el esqueleto. De la obra, el cuerpo: canal, desagüe, bandeja, lluvia, gota, tesela, onda, celda.",
           font=rotulo(20), fill=(90, 90, 90))
    for i, p in enumerate(paneles):
        lienzo.paste(p, (30 + (i % 3) * 930, 110 + (i // 3) * 930))
    guardar(SALIDA / "03c_anatomia.png", lienzo)


def lamina_antes_y_despues(D, letras="aoegrcfsjiáqbp"):
    """Arriba, la letra que dio el pie; en el medio, la anatomía; abajo, el calco con sus desagües."""
    from desenterrar import contornos_temblorosos, dibujar_trazos
    lado = 170
    cols = []
    for s in letras:
        antes = D["antes"][s]
        despues = D["M"][s]
        tr = contornos_temblorosos(despues, azar("ad", s))
        linea = dibujar_trazos((T, T), tr, False, azar("ad l", s), grosor=4)
        celdas = [1 - 0.88 * antes.astype(np.float32), 1 - 0.88 * despues.astype(np.float32), 1 - 0.9 * linea]
        cols.append(np.vstack([cv2.resize(c, (lado, lado), interpolation=cv2.INTER_AREA) for c in celdas]))
    tabla = np.hstack(cols)
    W, H = tabla.shape[1] + 260, tabla.shape[0] + 110
    lienzo = Image.new("RGB", (W, H), (247, 246, 242))
    lienzo.paste(Image.fromarray(a8(a_rgb(tabla))), (230, 90))
    d = ImageDraw.Draw(lienzo)
    d.text((30, 24), "Antes y después · simulación", font=rotulo(30), fill=(30, 30, 30))
    for i, r in enumerate(("lo que dio el pie", "la anatomía", "el calco")):
        d.text((30, 90 + i * lado + lado // 2 - 12), r, font=rotulo(20), fill=(90, 90, 90))
    guardar(SALIDA / "03d_antes_y_despues.png", lienzo)


def t_e(D):
    return D["testigos"]["e"]["elegido"]


def lamina_hectografo(copias, tirada, ultima, gel, cajas):
    paginas = []
    rot = []
    for n in sorted(copias):
        pg = pagina(copias[n], azar("pagina", n))
        paginas.append(cv2.resize(pg, (pg.shape[1] // 3, pg.shape[0] // 3), interpolation=cv2.INTER_AREA))
        rot.append(f"copia {n}")
    fila_de_paneles(paginas, rot, SALIDA / "08_hectografo_copias.jpg", alto=560,
                    titulo=f"Hectógrafo: la caja en cuerpo tesela, en una A4. Se leyeron {tirada} copias; cada una sale más clara")
    beber = la_bandeja_bebe(gel, cajas, azar("bebe"))
    fila_de_paneles(beber, ["0 h", "12 h", "24 h", "48 h"], SALIDA / "08b_la_bandeja_bebe.jpg", alto=220,
                    titulo="La gelatina después de la tirada: la tinta se hunde y la bandeja queda limpia")


def gif_voz(vestidas):
    """La palabra «voz» en el agua tocada, en bucle."""
    celdas = [POR_SIGNO[s]["celda"] for s in "voz"]
    alt = np.hstack([vestidas[c]["altura"] for c in celdas])
    mas = np.hstack([vestidas[c]["mascara"] for c in celdas])
    vs = {"altura": alt, "mascara": mas}
    cuadros = []
    for i in range(16):
        luz, _ = agua(vs, azar("gif"), fase=i / 16 * 4)
        f = foto_agua(luz, azar("gif foto"), ancho=720, alto=300)
        cuadros.append(Image.fromarray(a8(f)).convert("P", palette=Image.ADAPTIVE, colors=64))
    cuadros[0].save(SALIDA / "voz.gif", save_all=True, append_images=cuadros[1:], duration=110, loop=0, optimize=True)


def informe(D, fichas, ultima, tirada, pol):
    med = D["med"]
    ajuste = med["ajuste"]

    def con(regla):
        return [c["signo"] for c in CELDAS if D["marcas"].get(c["signo"], {}).get(regla)]
    halladas = [c for c in CELDAS if c["estado"] == "hallada"]
    placas = list(fichas.values())
    minutos = sum(f["placa_"]["minutos"] for f in placas)
    rot_h = sum(f["placa_"]["roturas"] for f in placas if f["estado"] == "hallada")
    rot_r = sum(f["placa_"]["roturas"] for f in placas if f["estado"] == "reconstruida")
    n_h = sum(1 for f in placas if f["estado"] == "hallada")
    n_r = sum(1 for f in placas if f["estado"] == "reconstruida")
    orden = sorted(ultima.items(), key=lambda kv: kv[1])
    sig = {c["celda"]: c["signo"] for c in CELDAS}
    juntas = [fichas[f"{c['celda']:02d}.01"]["azulejo"]["juntas_que_la_cortan"] for c in CELDAS]
    est = {c["celda"]: c["estado"] for c in CELDAS}
    uh = np.mean([v for c, v in ultima.items() if est[c] == "hallada"])
    ur = np.mean([v for c, v in ultima.items() if est[c] == "reconstruida"])
    hecto = (f"Las halladas se leen, en promedio, hasta la copia {coma(uh)}; las reconstruidas, hasta la {coma(ur)}. "
             + ("**Lo que la máquina no diseñó y apareció:** las hipótesis, hechas a puntos, dejan menos tinta en la matriz y se borran antes." if ur < uh
                else "Las reconstruidas no se borran antes que las halladas."))
    ch = np.mean([fichas[f"{c:02d}.01"]["agua"]["contraste_de_la_letra"] for c in est if est[c] == "hallada"])
    cr = np.mean([fichas[f"{c:02d}.01"]["agua"]["contraste_de_la_letra"] for c in est if est[c] == "reconstruida"])
    agua_txt = (f"Contraste de la letra en el agua quieta (cuánto se aparta la luz donde cae la letra, contra el resto de la placa): "
                f"{coma(ch, 2)} en las halladas y {coma(cr, 2)} en las reconstruidas. "
                + ("**Lo que la máquina no diseñó y apareció:** las reconstruidas, hechas a puntos, llegan más débiles al agua. El punteado tiene menos relieve que el surco y desvía menos luz: en el agua, las hipótesis se ven menos." if cr < ch
                   else "Las reconstruidas no llegan más débiles al agua."))
    L = []
    L += ["# La propuesta de la máquina: el taller simulado",
          "",
          "Generado por `simular.py`. Es una **hipótesis hecha por código**, para confrontarla con la que se haga a mano. Ninguna de estas formas entra en la caja ni en la fuente: la caja se llena con placas repujadas por una persona.",
          "",
          "La semilla es fija (el 22 de agosto de 2026): el resultado es siempre el mismo. Cambiarla es cambiar de mano.",
          "",
          "## Lo que la máquina tuvo que suponer",
          "",
          f"- **El testigo.** No tenemos el pie del libro en alta resolución: en la foto, la altura de x mide unos 4 px y no se puede calcar. La máquina lo reemplaza por una letra de imprenta parecida, **{Path(FUENTE_TESTIGO).stem}**, impresa con tipos de plomo simulados. Es su suposición más débil: tu propuesta partirá del libro.",
          "- **El cuerpo del pie:** 8,5 puntos.",
          "- **La piscina:** azulejo de 150 mm, 6 teselas y junta de 3 mm, hasta que se mida.",
          f"- **El bucle:** {BUCLE_MIN} minutos, hasta que Rebeca diga cuánto dura.",
          "- **La voz:** no es la tuya. Es el ritmo silábico del poema, con alturas inventadas entre 110 y 220 Hz.",
          "- **El signo final:** la máquina no tiene dedos. Simula una sola presión de un pulgar genérico.",
          "",
          "## Acción 1 · La pared y su frotado",
          "",
          "![Frotado](salida/01_frotado_de_la_pared.jpg)",
          "",
          "Un paño de 8 × 7 azulejos con juntas torcidas, craquelado, manchas y desportillados. En el frotado se marca lo que sobresale: juntas y grietas quedan blancas; las manchas no salen, porque no tienen relieve.",
          "",
          "## Acción 2 · El pie",
          "",
          "![El pie](salida/02_el_pie.jpg)",
          "",
          "Para cada signo hallado, la máquina amplió todos sus testigos en tres generaciones de fotocopia y eligió el mejor conservado: el que tiene las partes que debe tener (la i, dos) y el borde menos roto. La *opinión* es cuánto del borde tuvo que decidir al limpiar.",
          "",
          "| Celda | Signo | Testigo elegido | Palabra | Línea | Opinión |",
          "|---|---|---|---|---|---|"]
    for c in halladas:
        t = D["testigos"][c["signo"]]
        L.append(f"| {c['celda']} | `{c['signo']}` | {t['elegido']} de {t['de']} | {t['palabra']} | {t['linea']} | {coma(t['opinion'])} % |")
    L += ["",
          "## Acción 3 · La escala y el calco",
          "",
          "![Calco](salida/03_calco.png)",
          "",
          "**La escala la decidió el pie.** La letra más alta y la más baja caben en el azulejo con media tesela de aire. Después, la anatomía corre y escala todo el juego para que el fondo y el borde caigan en líneas de media tesela (`03b_anatomia.md`, regla 8). Así caen las líneas, en teselas desde abajo:",
          "",
          "| Línea | Pauta provisional (`03`, §3.6) | Lo que dio el pie | En la retícula |",
          "|---|---|---|---|",
          f"| Desagüe (descendentes) | 0,5 | — | {coma(med['desc_teselas'], 2)} |",
          f"| Fondo (base) | 1,5 | {coma(ajuste['base_de'], 2)} | {coma(ajuste['base_a'], 1)} |",
          f"| Borde (altura de x) | 4 | {coma(ajuste['base_de'] + ajuste['x_de'], 2)} (la x mide {coma(ajuste['x_de'], 2)}) | {coma(ajuste['base_a'] + ajuste['x_a'], 1)} (la x mide {coma(ajuste['x_a'], 1)}) |",
          f"| Afuera (ascendentes) | 5,5 | — | {coma(med['asc_teselas'], 2)} |",
          "",
          f"El trazo grueso de la o mide {coma(med['grueso'] / 4)} mm y el fino, {coma(med['fino'] / 4)} mm. " +
          ("Ningún signo desborda el azulejo." if not D["desbordes"] else "Desbordan: " + ", ".join(f"«{k}» {v} mm" for k, v in D["desbordes"].items()) + "."),
          "",
          "**Las reconstrucciones de la máquina:**",
          "",
          "| Signo | Receta |", "|---|---|"]
    for c in CELDAS:
        if c["estado"] == "reconstruida":
            L.append(f"| `{c['signo']}` | {D['receta'][c['signo']]} |")
    L += ["",
          "Una decisión propia de la máquina: **cifras elzevirianas**, de altura de x, con 6 y 8 que suben y 3, 4, 5, 7 y 9 que bajan. En una tipografía de caja baja, las cifras de monumento (todas a la altura de las mayúsculas) serían ajenas.",
          "",
          "El `.notdef`, la celda de la lámina calcada: ![notdef](salida/03b_notdef.png)",
          "",
          "## La anatomía",
          "",
          "Del pie, la máquina tomó el esqueleto; la anatomía la dicta la obra (`03b_anatomia.md`). Estas son las reglas que aplicó y a qué signos alcanzaron:",
          "",
          "![Anatomía](salida/03c_anatomia.png)",
          "",
          "![Antes y después](salida/03d_antes_y_despues.png)",
          "",
          "| Regla | Qué hizo la máquina | Signos |",
          "|---|---|---|",
          "| El canal | Dibujó solo el contorno: la letra es hueca | los 55 |",
          f"| El desagüe | Abrió cada contorno en su punto más bajo, con una junta de ancho | {sum(D['desagues'].values())} desagües en 55 signos |",
          f"| La bandeja | Rehízo la mitad baja de cada ojo y asentó plana la panza | {', '.join(f'«{s}»' for s in con('bandejas'))} |",
          "| La lluvia | Redondeó todo y gastó más arriba: los remates altos casi desaparecen | los 30 hallados |",
          f"| Las gotas | Colgó una gota donde un trazo termina mirando hacia abajo | {', '.join(f'«{s}»' for s in con('gotas'))} |",
          f"| Los puntos | Los volvió cuadrados de media tesela | {', '.join(f'«{s}»' for s in con('puntos'))}, y los que heredan sus puntos |",
          f"| Las tildes | Las volvió gotas | {', '.join(f'«{s}»' for s in con('tildes'))}, y la é y la ó, que heredan la de la á |",
          "| La onda | La virgulilla de la ñ es una onda de agua tocada | «ñ» |",
          f"| El asta | Corrió la letra hasta que su asta cae en una línea de media tesela | {sum(1 for v in D['astas'].values() if v is not None)} signos con asta |",
          "| La celda | Cada cifra, dentro de una celda de la cabeza del ídolo | las 10 cifras |",
          "",
          "## Acción 4 · Repujar",
          "",
          "![Placa](salida/04_placa.jpg)",
          "",
          f"- **119 placas** ({n_h} de signos hallados, {n_r} reconstruidos y {pol['¶']} signo final).",
          f"- **Tiempo simulado:** {coma(minutos / 60)} horas de repujado, contando las placas que se rompieron. El plan estimaba entre 30 y 40. La máquina supuso 20 mm de surco por minuto, 9 mm de punteado por minuto y 4 minutos para preparar cada placa.",
          f"- **Roturas:** {rot_h} en {n_h} placas halladas y {rot_r} en {n_r} reconstruidas. La máquina supuso que el punteado perfora: una placa punteada se rompe con más probabilidad (16 % por intento contra 6 %).",
          "",
          "![Rotas](salida/04b_placas_rotas.jpg)",
          "",
          "## Acción 5 · La caja",
          "",
          "![Caja abierta](salida/05_caja_abierta.jpg)",
          "",
          "![Caja cerrada](salida/05b_caja_cerrada.jpg)",
          "",
          "Cerrada, por la única puerta se ve la coma.",
          "",
          "## Acción 6 · Vestir",
          "",
          "![Piel](salida/06_piel.jpg)",
          "",
          "## Acción 8 · El hectógrafo",
          "",
          "![Copias](salida/08_hectografo_copias.jpg)",
          "",
          "![La bandeja bebe](salida/08b_la_bandeja_bebe.jpg)",
          "",
          f"Se leyeron **{tirada} copias**. La primera sale casi negra y las siguientes, violeta: el color depende de cuánta tinta queda. " + hecto,
          "",
          "**Los primeros en borrarse:** " + ", ".join(f"«{sig[c]}» ({n})" for c, n in orden[:8]) + ".",
          "",
          "**Los últimos:** " + ", ".join(f"«{sig[c]}» ({n})" for c, n in orden[-8:]) + ".",
          "",
          "## Acción 9 · Agua",
          "",
          "![Agua quieta](salida/09_agua_quieta.jpg)",
          "",
          "![Agua tocada](salida/09b_agua_tocada.jpg)",
          "",
          "![voz](salida/voz.gif)",
          "",
          agua_txt,
          "",
          "## Acción 10 · Voz",
          "",
          "![Voz](salida/10_voz.jpg)",
          "",
          "## Acción 11 · Azulejo y la estrofa en la pared",
          "",
          "![Azulejo](salida/11_azulejo.png)",
          "",
          f"Juntas que cortan cada letra al caer ampliada: entre {min(juntas)} y {max(juntas)} (media {coma(np.mean(juntas))}).",
          "",
          "![Estrofa](salida/11b_estrofa_en_la_pared.jpg)",
          "",
          "La séptima estrofa compuesta con placas vestidas: cada aparición de una letra es otra placa, así que ninguna se repite igual dentro de un verso.",
          "",
          "## Una letra de punta a punta",
          "",
          "![a](salida/12_cadena_08.jpg)",
          "",
          "![z](salida/12_cadena_32.jpg)",
          "",
          "## Lo que la máquina no sabe",
          "",
          "- **El libro:** qué letra tiene realmente el pie, ni cómo se imprimió.",
          "- **La mano:** el temblor es ruido con un ritmo; no cansa, no duda, no se distrae.",
          "- **El aluminio:** cómo se rompe de verdad. Aquí se rompe con una probabilidad.",
          "- **El cuerpo:** los pliegues siguen un eje supuesto para cada parte.",
          "- **La gelatina:** transfiere una fracción fija por copia, con presión irregular.",
          "- **El agua:** un solo rebote, un eco desplazado y ninguna polarización.",
          "- **La voz:** no es la tuya.",
          "",
          "## Cómo confrontar",
          "",
          "Cuando exista tu propuesta, conviene guardarla con los mismos nombres para compararlas placa por placa:",
          "",
          "- **Fotos:** `tipografia/mano/<estado>/<celda>_<variante>.jpg`, con dos dígitos (`mano/placa/08_01.jpg`) y estas carpetas de estado: `calco`, `placa`, `piel`, `copia`, `agua`, `voz`, `azulejo`.",
          "- **Fichas:** `tipografia/mano/fichas.json`, con los mismos campos que `salida/fichas_simuladas.json`.",
          "",
          "**Qué se compara:**",
          "",
          "1. **Forma:** la silueta de cada calco superpuesta a la de la máquina, en dos colores; qué testigo eligió cada una y cuánto opinó.",
          "2. **Métricas:** la base y la altura de x que dio el libro contra las que dio el testigo sustituto.",
          "3. **Reconstrucciones:** las 25 recetas de la máquina contra las tuyas. Es donde más van a diferir, y donde más interesa.",
          "4. **Tiempo y roturas:** horas, intentos y roturas por placa.",
          "5. **Hectógrafo:** la tirada, y qué signos se borran primero.",
          "6. **Agua y pared:** si las reconstruidas también llegan más débiles, y cuántas juntas cortan cada letra.",
          ""]
    (SALIDA.parent / "informe.md").write_text("\n".join(L), encoding="utf8")


if __name__ == "__main__":
    main()
