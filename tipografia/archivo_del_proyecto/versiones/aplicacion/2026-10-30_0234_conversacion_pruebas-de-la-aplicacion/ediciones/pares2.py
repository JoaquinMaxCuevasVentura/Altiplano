VIEJO = '''      dibujo() {
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
      mover: { intemperie(p) { const { x0, x1, yt } = IN, k = 1 - Math.SQRT1_2, d = ((x1 - p[0]) + (p[1] - yt)) / 2; return Math.max(0, d / k) / (x1 - x0); } } },'''

NUEVO = '''      dibujo() {
        const { x0, x1, yt, yc } = IN, ancho = x1 - x0, xm = (x0 + x1) / 2, o = [];
        const contorno = (v) => {
          const r = Math.max(0.01, v * ancho);
          return `M${x0},${yc} V${f(yt + r)} A${f(r)},${f(r)} 0 0 1 ${f(x0 + r)},${yt} H${f(x1 - r)} A${f(r)},${f(r)} 0 0 1 ${x1},${f(yt + r)} V${yc}`;
        };
        // abajo, la línea de corte de los planos: el fuste sigue
        const quiebra = `H${xm + 16} L${xm + 6},${yc + 9} L${xm - 6},${yc - 9} L${xm - 16},${yc} H${x0}`;
        o.push(`<path d="${contorno(valor("intemperie"))} ${quiebra}Z" fill="${METAL}"/>`);
        o.push(`<path d="M${x1},${yc} ${quiebra}" fill="none" stroke="${TINTA}" stroke-width="0.8"/>`);
        o.push(`<path d="M${x0},${yt + 40} V${yt} H${x0 + 40} M${x1 - 40},${yt} H${x1} V${yt + 40}" fill="none" stroke="${GRIS2}" stroke-width="1" stroke-dasharray="2 3"/>`);
        o.push(dosVeces(["intemperie"], (v, estilo) => `<path d="${contorno(v.intemperie)}" ${estilo}/>`, 2));
        o.push(`<line x1="${xm}" y1="${yt - 6}" x2="${xm}" y2="${yc + 12}" ${EJE}/>`);
        // el radio, como lo acotan los planos: desde su centro, hasta el arco
        const v = valor("intemperie"), r = v * ancho, C = [x1 - r, yt + r], col = movida("intemperie") ? VIOLETA : TINTA;
        if (r > 10) o.push(flecha(C, [C[0] + r * Math.SQRT1_2, C[1] - r * Math.SQRT1_2], col));
        o.push(texto(C[0] - 14, C[1] + 4, `R ${coma(v, 3)} c`, { ancla: "end", color: col, fondo: true }));
        o.push(texto(xm, yt - 14, "sin remate: un corte", { ancla: "middle" }));
        o.push(texto(16, 258, "la punta del fuste, dibujada × 8"));
        o.push(miniatura("l", 340, 4, 52));
        o.push(asa("intemperie", C[0], C[1]));
        return o.join("");
      },
      mover: { intemperie(p) { const { x0, x1, yt } = IN, r = ((x1 - p[0]) + (p[1] - yt)) / 2; return Math.max(0, r) / (x1 - x0); } } },'''

PARES = [
    (VIEJO, NUEVO),
    ('''  /* La pared de la cuenca: la misma curva de la gramática (cuencaLado). */''',
     '''  /* Una línea con su punta, la de las cotas de radio de los planos. */
  function flecha(a, b, color) {
    const l = Math.hypot(b[0] - a[0], b[1] - a[1]), d = [(b[0] - a[0]) / l, (b[1] - a[1]) / l], n = [-d[1], d[0]];
    const base = [b[0] - 8 * d[0], b[1] - 8 * d[1]];
    return `<line x1="${f(a[0])}" y1="${f(a[1])}" x2="${f(base[0])}" y2="${f(base[1])}" stroke="${color}" stroke-width="0.8"/>` +
      `<path d="M${f(b[0])},${f(b[1])} L${f(base[0] + 2.6 * n[0])},${f(base[1] + 2.6 * n[1])} L${f(base[0] - 2.6 * n[0])},${f(base[1] - 2.6 * n[1])}Z" fill="${color}"/>`;
  }
  /* La pared de la cuenca: la misma curva de la gramática (cuencaLado). */'''),
]
