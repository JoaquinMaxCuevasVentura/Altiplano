  // ------------------------------------------------------------------ los siete dibujos
  /* Cada uno: sus decisiones, su dibujo y, para cada asa, del punto del dedo al valor. Lienzo de 400 × 270.
   * En gris metal, la letra como queda; encima, su eje: en tinta, el de la obra; en violeta y a puntos, el que se aparta. */
  const CU = { cx: 170, rx: 96, yt: 26, yb: 218, des: 12 };      // la cuenca de la o, a su tamaño (4 px = 1 mm)
  const FU = { x: 180, y0: 26, F: 236, S: 0.56, X: 6 };          // el fuste de la l, a 0,56; los ángulos, × 6
  const HO = { cx: 150, rx: 64, yt: 34, F: 256, S: 1.1 };        // el hombro de la n, a 1,1
  const GO = { px: 240, py: 110, R: 80, S: 1.15 };               // el gancho de la a y su gota, a 1,15
  const IN = { x0: 160, x1: 300, yt: 70 };                       // la punta del fuste, × 4: un canal mide 140
  const DETALLES = [
    { id: "celda", rombo: "P-01 · 4", nombre: "la celda y sus niveles", origen: "medida del pie", claves: ["razon_x"],
      dibujo() {
        const e = base.e, y0 = 24, s = 222 / (e.desague - e.afuera), Y = (y) => y0 + (y - e.afuera) * s;
        const o = [];
        for (const [n, y] of [["afuera", e.afuera], ["fondo", e.fondo], ["desagüe", e.desague]]) {
          o.push(`<line x1="70" y1="${f(Y(y))}" x2="300" y2="${f(Y(y))}" stroke="${GRIS}" stroke-width="0.9" stroke-dasharray="10 5"/>`);
          o.push(texto(64, Y(y) + 4, n, { ancla: "end" }));
          o.push(nivel(318, Y(y), nivelUPM(y)));
        }
        // las letras, a su altura: la n mide la x; la l, las ascendentes
        for (const [g, cx] of [["n", 130], ["l", 220]]) {
          const r = signos[g];
          if (r) o.push(`<path transform="translate(${f(cx - 300 * s)} ${f(y0 - e.afuera * s)}) scale(${s.toFixed(4)})" d="${dTrazo(r.geo)}" fill="${METAL}" stroke="${TINTA}" stroke-width="${(1 / s).toFixed(2)}" fill-rule="evenodd"/>`);
        }
        // el borde: la obra y lo que se aparta
        const bordeDe = (razon) => e.fondo - (e.fondo - e.afuera) / razon;
        const yo = Y(bordeDe(obra("razon_x"))), yv = Y(e.borde);
        o.push(`<line x1="70" y1="${f(yo)}" x2="300" y2="${f(yo)}" stroke="${TINTA}" stroke-width="${movida("razon_x") ? 1 : 1.4}"/>`);
        if (movida("razon_x")) o.push(`<line x1="70" y1="${f(yv)}" x2="300" y2="${f(yv)}" ${TUYA} stroke-width="2.4"/>`);
        o.push(texto(64, yv + 4, "borde", { ancla: "end", color: movida("razon_x") ? VIOLETA : TINTA }));
        o.push(nivel(318, yv, nivelUPM(e.borde), movida("razon_x") ? VIOLETA : TINTA));
        o.push(cota(282, Y(e.fondo), 282, yv, "x"));
        o.push(cota(268, Y(e.fondo), 268, Y(e.afuera), ""));
        o.push(texto(263, (Y(e.fondo) + Y(e.afuera)) / 2, "ascendentes", { ancla: "middle", giro: true, fondo: true }));
        o.push(asa("razon_x", 300, yv));
        return o.join("");
      },
      mover: { razon_x(p) { const e = base.e, s = 222 / (e.desague - e.afuera), y = e.afuera + (p[1] - 24) / s; return (e.fondo - e.afuera) / Math.max(1, e.fondo - y); } } },

    { id: "canal", rombo: "P-02 · 1", nombre: "el canal", origen: "medida del pie", claves: ["canal"],
      dibujo() {
        const s = 1.9, cx = 180, yh = 76, yp = 204, o = [];
        o.push(texto(16, 22, "corte A–A · el aluminio, de canto"));
        const corte = (v, estilo) => {
          const w = v.canal * s, h = 0.42 * w;
          return `<path d="M16,${yh} H${f(cx - w / 2)} C${f(cx - w / 2)},${f(yh + h * 1.33)} ${f(cx + w / 2)},${f(yh + h * 1.33)} ${f(cx + w / 2)},${yh} H384" ${estilo}/>`;
        };
        o.push(dosVeces(["canal"], corte, 2.2));
        const w = valor("canal") * s;
        o.push(cota(cx - w / 2, yh - 16, cx + w / 2, yh - 16, `${coma(valor("canal") / 4)} mm`));
        // en planta: un solo grosor
        o.push(texto(16, yp - 64, "en planta: un solo grosor, sin contraste"));
        const planta = (v, estilo) => `<rect x="40" y="${f(yp - v.canal * s / 2)}" width="300" height="${f(v.canal * s)}" ${estilo}/>`;
        o.push(planta({ canal: valor("canal") }, `fill="${METAL}" stroke="none"`));
        o.push(dosVeces(["canal"], planta, 1.4));
        o.push(`<line x1="30" y1="${yp}" x2="350" y2="${yp}" ${EJE}/>`);
        o.push(miniatura("o"));
        o.push(asa("canal", cx + w / 2, yh));
        return o.join("");
      },
      mover: { canal(p) { return 2 * Math.abs(p[0] - 180) / 1.9; } } },

    { id: "cuenca", rombo: "P-03 · 2", nombre: "la cuenca", origen: "forma de la obra", claves: ["trapecio", "pared"],
      dibujo() {
        const { cx, rx, yt, yb } = CU, c = base.c, o = [];
        const k = valor("trapecio"), p = valor("pared");
        o.push(`<polyline points="${pts(ejeCuenca(k, p))}" stroke="${METAL}" stroke-width="${f(c)}" fill="none" stroke-linejoin="round"/>`);
        o.push(`<line x1="${cx}" y1="${yt - c / 2 - 6}" x2="${cx}" y2="${yb + c / 2 + 6}" ${EJE}/>`);
        o.push(dosVeces(["trapecio", "pared"], (v, estilo) => `<polyline points="${pts(ejeCuenca(v.trapecio, v.pared))}" ${estilo}/>`, 2));
        o.push(nivel(cx + rx + 34, yb + c / 2, "fondo ±0"));
        o.push(texto(cx, yb - c / 2 - 8, "desagüe", { ancla: "middle", fondo: true }));
        o.push(cota(cx - k * rx, yb + c / 2 + 16, cx + k * rx, yb + c / 2 + 16, `${coma(k, 2)} del ancho`));
        const M = medioDeLaPared(k, p);
        o.push(texto(M[0] + 24, M[1] - 6, `pared ${coma(p, 2)}`, { color: movida("pared") ? VIOLETA : TINTA, fondo: true }));
        o.push(miniatura("o"));
        o.push(asa("trapecio", cx + k * rx, yb));
        o.push(asa("pared", M[0], M[1]));
        return o.join("");
      },
      mover: {
        trapecio(p) { return (p[0] - CU.cx) / CU.rx; },
        pared(p) {
          const { rx, yt, yb } = CU, cy = (yt + yb) / 2, k = valor("trapecio");
          const M0 = medioDeLaPared(k, 0), v = [3 / 8 * rx * (1 - k), 3 / 8 * (yb - cy)];
          return ((p[0] - M0[0]) * v[0] + (p[1] - M0[1]) * v[1]) / (v[0] * v[0] + v[1] * v[1]);
        },
      } },

    { id: "fuste", rombo: "P-04 · 1", nombre: "el fuste", origen: "forma de la obra", claves: ["quiebre"],
      dibujo() {
        const { x, y0, F, S } = FU, c = base.c * S, o = [];
        const alto = base.P.asiento_alto.valor * S, ancho = base.P.asiento_ancho.valor * S;
        o.push(`<line x1="${x - 70}" y1="${F}" x2="${x + 70}" y2="${F}" stroke="${GRIS}" stroke-width="0.9" stroke-dasharray="10 5"/>`);
        o.push(`<polyline points="${pts(planosDelFuste(valor("quiebre")))}" stroke="${METAL}" stroke-width="${f(c)}" fill="none" stroke-linejoin="round"/>`);
        o.push(`<path d="${dAsiento(x, F, c, ancho, alto)}" fill="${METAL}"/>`);
        o.push(`<line x1="${x}" y1="${y0 - 12}" x2="${x}" y2="${F + 8}" ${EJE}/>`);
        o.push(dosVeces(["quiebre"], (v, estilo) => `<polyline points="${pts(planosDelFuste(v.quiebre))}" ${estilo}/>`, 2));
        const q = valor("quiebre"), p1 = planosDelFuste(q)[1];
        if (q > 0.05) {
          const a = Math.atan2(p1[0] - x, p1[1] - y0), r = 44;
          o.push(`<path d="M${x},${y0 + r} A${r},${r} 0 0 0 ${f(x + r * Math.sin(a))},${f(y0 + r * Math.cos(a))}" fill="none" stroke="${TINTA}" stroke-width="0.8"/>`);
        }
        o.push(texto(p1[0] + 16, p1[1] + 4, `${coma(q, 1)}° por plano`, { color: movida("quiebre") ? VIOLETA : TINTA, fondo: true }));
        o.push(texto(x - 24, y0 + 6, "corte", { ancla: "end" }));
        o.push(texto(x - 30, F - 5, "asiento", { ancla: "end" }));
        o.push(texto(16, 258, "los ángulos, dibujados × 6"));
        o.push(miniatura("l"));
        o.push(asa("quiebre", p1[0], p1[1]));
        return o.join("");
      },
      mover: { quiebre(p) { const L = FU.F - base.P.asiento_alto.valor * FU.S + 2 * FU.S - FU.y0; return Math.atan(Math.max(0, p[0] - FU.x) / (FU.X * L / 3)) * 180 / Math.PI; } } },

    { id: "hombro", rombo: "P-05 · 1 · 3", nombre: "el hombro", origen: "forma de la obra · medida a ojo", claves: ["hombro", "hombro_caida"],
      dibujo() {
        const { cx, rx, yt, F, S } = HO, xi = cx - rx, xd = cx + rx, c = base.c * S, B = yt - c / 2, o = [];
        const alto = base.P.asiento_alto.valor * S, ancho = base.P.asiento_ancho.valor * S, fin = F - alto + 2 * S;
        const arcoYPata = (v) => {
          const ya = yt + v.hombro_caida * (F - yt);
          return superelipse(cx, ya, rx, ya - yt, v.hombro).concat([[xd, fin]]);
        };
        for (const [nombre, y] of [["borde", B], ["fondo", F]]) {
          o.push(`<line x1="44" y1="${f(y)}" x2="290" y2="${f(y)}" stroke="${GRIS}" stroke-width="0.9" stroke-dasharray="10 5"/>`);
          o.push(texto(40, y + 4, nombre, { ancla: "end" }));
        }
        // la n en metal, como queda
        const metal = `stroke="${METAL}" stroke-width="${f(c)}" fill="none" stroke-linejoin="round"`;
        o.push(`<line x1="${xi}" y1="${f(B)}" x2="${xi}" y2="${f(fin)}" ${metal}/>`);
        o.push(`<polyline points="${pts(arcoYPata({ hombro: valor("hombro"), hombro_caida: valor("hombro_caida") }))}" ${metal}/>`);
        o.push(`<path d="${dAsiento(xi, F, c, ancho, alto)} ${dAsiento(xd, F, c, ancho, alto)}" fill="${METAL}"/>`);
        // su eje: el fuste no se mueve aquí; el arco y la pata, sí
        o.push(`<line x1="${xi}" y1="${f(B)}" x2="${xi}" y2="${f(fin)}" ${OBRA} stroke-width="2"/>`);
        o.push(dosVeces(["hombro", "hombro_caida"], (v, estilo) => `<polyline points="${pts(arcoYPata(v))}" ${estilo}/>`, 2));
        const n = valor("hombro"), cae = valor("hombro_caida"), ya = yt + cae * (F - yt), ry = ya - yt, s = Math.pow(2, -1 / n);
        const pt45 = [cx + rx * s, ya - ry * s];
        o.push(`<line x1="${cx}" y1="${f(ya)}" x2="${f(cx + rx)}" y2="${yt}" stroke="${FILETE}" stroke-width="0.8"/>`);
        o.push(texto(pt45[0] + 16, pt45[1] - 10, `n = ${coma(n, 2)}`, { color: movida("hombro") ? VIOLETA : TINTA, fondo: true }));
        o.push(nivel(xd + c / 2 + 14, ya, `arranca ${coma(cae, 2)}`, movida("hombro_caida") ? VIOLETA : TINTA));
        o.push(texto(xd + c / 2 + 24, ya + 15, "(a ojo)", { tam: 11 }));
        o.push(miniatura("n", 330, 196, 58));
        o.push(asa("hombro", pt45[0], pt45[1]));
        o.push(asa("hombro_caida", xd, ya));
        return o.join("");
      },
      mover: {
        hombro(p) {
          const { cx, rx, yt, F } = HO, ya = yt + valor("hombro_caida") * (F - yt), ry = ya - yt;
          const s = clamp(((p[0] - cx) * rx - (p[1] - ya) * ry) / (rx * rx + ry * ry), 0.5, 0.97);
          return -Math.LN2 / Math.log(s);
        },
        hombro_caida(p) { return (p[1] - HO.yt) / (HO.F - HO.yt); },
      } },

    { id: "gota", rombo: "P-06 · 2", nombre: "la gota", origen: "forma de la obra", claves: ["gota_masa"],
      dibujo() {
        const { px, py, R, S } = GO, c = base.c * S, o = [];
        // el gancho: termina mirando abajo
        const a0 = rad(200), gancho = `M${f(px - R + R * Math.cos(a0))},${f(py - R * Math.sin(a0))} A${R},${R} 0 1 1 ${px},${py}`;
        o.push(`<path d="${gancho}" stroke="${METAL}" stroke-width="${f(c)}" fill="none"/>`);
        o.push(`<path d="${gancho}" ${EJE}/>`);
        o.push(`<path d="${dGota(valor("gota_masa"), c)}Z" fill="${METAL}"/>`);
        o.push(dosVeces(["gota_masa"], (v, estilo) => `<path d="${dGota(v.gota_masa, c)}" ${estilo}/>`, 2));
        // la masa es el ancho de la gota: el estirón es hacia abajo
        const m = valor("gota_masa") * c, oy = py + 0.3 * c, medio = oy + 1.15 * m / 2, abajo = oy + 1.15 * m, yc = abajo + 22;
        o.push(`<path d="M${f(px - m / 2)},${f(medio + 4)} V${f(yc + 4)} M${f(px + m / 2)},${f(medio + 4)} V${f(yc + 4)}" stroke="${GRIS}" stroke-width="0.6"/>`);
        o.push(cota(px - m / 2, yc, px + m / 2, yc, `${coma(valor("gota_masa"), 2)} c`));
        // la gravedad, en lugar del norte
        const gx = 360, gy = 40;
        o.push(`<circle cx="${gx}" cy="${gy}" r="14" fill="none" stroke="${TINTA}" stroke-width="1"/>` +
          `<line x1="${gx}" y1="${gy - 20}" x2="${gx}" y2="${gy + 8}" stroke="${TINTA}" stroke-width="1.2"/>` +
          `<path d="M${gx},${gy + 18} l-5,-12 h10 z" fill="${TINTA}"/>` + texto(gx, gy + 32, "GRAVEDAD", { ancla: "middle", tam: 10, color: TINTA }));
        o.push(texto(16, 258, "solo gotea lo que mira abajo"));
        o.push(miniatura("a", 330, 196, 58));
        o.push(asa("gota_masa", px, abajo));
        return o.join("");
      },
      mover: { gota_masa(p) { const c = base.c * GO.S; return (p[1] - GO.py - 0.3 * c) / (1.15 * c); } } },

    { id: "intemperie", rombo: "P-02 · 3", nombre: "la intemperie", origen: "forma de la obra", claves: ["intemperie"],
      dibujo() {
        const { x0, x1, yt } = IN, ancho = x1 - x0, o = [];
        const borde = (v, estilo) => {
          const r = Math.max(0.01, v.intemperie * ancho);
          return `<path d="M${x0},262 V${f(yt + r)} A${f(r)},${f(r)} 0 0 1 ${f(x0 + r)},${yt} H${f(x1 - r)} A${f(r)},${f(r)} 0 0 1 ${x1},${f(yt + r)} V262" ${estilo}/>`;
        };
        o.push(borde({ intemperie: valor("intemperie") }, `fill="${METAL}" stroke="none"`));
        o.push(`<path d="M${x0},${yt + 26} V${yt} H${x0 + 26} M${x1 - 26},${yt} H${x1} V${yt + 26}" fill="none" stroke="${GRIS2}" stroke-width="1" stroke-dasharray="2 3"/>`);
        o.push(dosVeces(["intemperie"], borde, 2));
        o.push(`<line x1="${(x0 + x1) / 2}" y1="${yt - 6}" x2="${(x0 + x1) / 2}" y2="262" ${EJE}/>`);
        const r = valor("intemperie") * ancho, k = 1 - Math.SQRT1_2;
        o.push(texto(x1 + 14, yt + 4, `r = ${coma(valor("intemperie"), 3)} c`, { color: movida("intemperie") ? VIOLETA : TINTA }));
        o.push(texto((x0 + x1) / 2, yt - 14, "sin remate: un corte", { ancla: "middle" }));
        o.push(texto(16, 240, "la punta del fuste"));
        o.push(texto(16, 256, "dibujada × 4"));
        o.push(miniatura("l", 330, 196, 58));
        o.push(asa("intemperie", x1 - k * r, yt + k * r));
        return o.join("");
      },
      mover: { intemperie(p) { const { x0, x1, yt } = IN, k = 1 - Math.SQRT1_2, d = ((x1 - p[0]) + (p[1] - yt)) / 2; return Math.max(0, d / k) / (x1 - x0); } } },
  ];

  /* La pared de la cuenca: la misma curva de la gramática (cuencaLado). */
  function lado(xMedio, cy, xFondo, ybot, pared, pasos = 40) {
    const P0 = [xMedio, cy], P3 = [xFondo, ybot];
    const P1 = [xMedio, cy + pared * (ybot - cy)], P2 = [xFondo + pared * (xMedio - xFondo), ybot];
    const out = [];
    for (let i = 0; i <= pasos; i++) {
      const t = i / pasos, a = (1 - t) ** 3, b = 3 * (1 - t) ** 2 * t, c = 3 * (1 - t) * t * t, d = t ** 3;
      out.push([a * P0[0] + b * P1[0] + c * P2[0] + d * P3[0], a * P0[1] + b * P1[1] + c * P2[1] + d * P3[1]]);
    }
    return out;
  }
  /* El eje de la cuenca, como en la gramática: el ojo arriba, las paredes, el fondo plano y el desagüe abierto en el eje. */
  function ejeCuenca(k, p) {
    const { cx, rx, yt, yb, des } = CU, cy = (yt + yb) / 2;
    const izq = lado(cx - rx, cy, cx - k * rx, yb, p).reverse(), der = lado(cx + rx, cy, cx + k * rx, yb, p);
    return [[cx - des / 2, yb]].concat(izq, superelipse(cx, cy, rx, cy - yt, 2).slice(1, -1), der, [[cx + des / 2, yb]]);
  }
  /* El medio de la pared derecha (t = ½ de la curva): ahí se toma. */
  function medioDeLaPared(k, p) {
    const { cx, rx, yt, yb } = CU, cy = (yt + yb) / 2, xm = cx + rx, xf = cx + k * rx;
    return [(4 * xm + 4 * xf + 3 * p * (xm - xf)) / 8, (4 * cy + 4 * yb + 3 * p * (yb - cy)) / 8];
  }
  /* El arco del hombro: media superelipse, de la izquierda a la derecha por arriba (la de la gramática). */
  function superelipse(cx, cy, rx, ry, n, pasos = 60) {
    const out = [];
    for (let i = 0; i <= pasos; i++) {
      const a = Math.PI - Math.PI * i / pasos, c = Math.cos(a), s = Math.sin(a);
      out.push([cx + rx * Math.sign(c) * Math.abs(c) ** (2 / n), cy - ry * Math.abs(s) ** (2 / n)]);
    }
    return out;
  }
  /* Los tres planos del fuste (facetar): el del medio se aparta del eje; los ángulos, × 6. */
  function planosDelFuste(q) {
    const { x, y0, F, S, X } = FU, fin = F - base.P.asiento_alto.valor * S + 2 * S, L = fin - y0;
    const off = (L / 3) * Math.tan(rad(q)) * X;
    return [[x, y0], [x + off, y0 + L / 3], [x, y0 + 2 * L / 3], [x, fin]];
  }
  /* El asiento de la gramática: de un canal a dos, en una curva cóncava. */
  const dAsiento = (x, F, c, ancho, alto) =>
    `M${f(x - c / 2)},${f(F - alto)} Q${f(x - c / 2)},${f(F)} ${f(x - ancho / 2)},${f(F)} H${f(x + ancho / 2)} ` +
    `Q${f(x + c / 2)},${f(F)} ${f(x + c / 2)},${f(F - alto)}Z`;
  /* La gota de la gramática: un círculo del diámetro de la masa, estirado 1,15 hacia abajo desde su tope, y el cuello
   * que la cuelga del gancho, de un canal a 0,55. El contorno queda abierto arriba, donde se une al gancho. */
  function dGota(masa, c) {
    const { px, py } = GO, m = masa * c, cuello = 0.55 * c;
    const oy = py + 0.3 * c, rx = m / 2, ry = 1.15 * m / 2, ecy = oy + ry, cyc = oy + m / 2;
    const dentro = (x, y) => ((x - px) / rx) ** 2 + ((y - ecy) / ry) ** 2 < 1;
    const entra = (lado) => {                       // el cuello baja de afuera hacia adentro: dónde cruza el cuerpo
      const A = [px + lado * c / 2, py], B = [px + lado * cuello / 2, cyc];
      let t0 = 0, t1 = 1;
      for (let i = 0; i < 30; i++) {
        const t = (t0 + t1) / 2;
        if (dentro(A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))) t1 = t; else t0 = t;
      }
      return [A[0] + t1 * (B[0] - A[0]), A[1] + t1 * (B[1] - A[1])];
    };
    const I = entra(-1), Dr = entra(1);
    return `M${f(px - c / 2)},${f(py)} L${f(I[0])},${f(I[1])} A${f(rx)},${f(ry)} 0 1 0 ${f(Dr[0])},${f(Dr[1])} L${f(px + c / 2)},${f(py)}`;
  }

