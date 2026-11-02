PARES = [
    # los rombos: el detalle de los planos que cada dibujo repite
    ('{ id: "celda", rombo: "P-01 · 4",', '{ id: "celda", rombo: "P-01 · 1",'),
    ('{ id: "canal", rombo: "P-02 · 1",', '{ id: "canal", rombo: "P-02 · 3",'),
    ('{ id: "cuenca", rombo: "P-03 · 2",', '{ id: "cuenca", rombo: "P-03 · 1 · 2",'),
    ('{ id: "fuste", rombo: "P-04 · 1",', '{ id: "fuste", rombo: "P-04 · 2",'),
    ('{ id: "hombro", rombo: "P-05 · 1 · 3",', '{ id: "hombro", rombo: "P-05 · 2 · 3",'),
    ('{ id: "intemperie", rombo: "P-02 · 3",', '{ id: "intemperie", rombo: "P-02 · 5",'),
    ('["planos · 3", "Tres planos por asta (P-04 · 1)."],', '["planos · 3", "Tres planos por asta (P-04 · 2)."],'),
    ('el aluminio no se rasga (P-02 · 2)."],', 'el aluminio no se rasga (P-02 · 1 · 2)."],'),
    # el fuste: como en P-04 · 2, los desvíos × 10
    ('  const FU = { x: 180, y0: 26, F: 236, S: 0.56, X: 6 };          // el fuste de la l, a 0,56; los ángulos, × 6',
     '  const FU = { x: 180, y0: 26, F: 236, S: 0.56, X: 10 };         // el fuste de la l, a 0,56; los desvíos, × 10'),
    ('        o.push(texto(16, 258, "los ángulos, dibujados × 6"));', '        o.push(texto(16, 258, "los desvíos, dibujados × 10"));'),
    ('  /* Los tres planos del fuste (facetar): el del medio se aparta del eje; los ángulos, × 6. */',
     '  /* Los tres planos del fuste (facetar): el del medio se aparta del eje; los desvíos, × 10 (como en P-04 · 2). */'),
    # el hombro: la familia de arcos de P-05 · 2, en gris
    ('''        o.push(dosVeces(["hombro", "hombro_caida"], (v, estilo) => `<polyline points="${pts(arcoYPata(v))}" ${estilo}/>`, 2));
        const n = valor("hombro"), cae = valor("hombro_caida"), ya = yt + cae * (F - yt), ry = ya - yt, s = Math.pow(2, -1 / n);''',
     '''        const n = valor("hombro"), cae = valor("hombro_caida"), ya = yt + cae * (F - yt), ry = ya - yt, s = Math.pow(2, -1 / n);
        for (const m of [2, 5]) o.push(`<polyline points="${pts(superelipse(cx, ya, rx, ry, m))}" fill="none" stroke="${GRIS2}" stroke-width="0.8" stroke-dasharray="3 3"/>`);
        o.push(texto(396, 268, "en gris, n = 2 y n = 5", { ancla: "end", tam: 11 }));
        o.push(dosVeces(["hombro", "hombro_caida"], (v, estilo) => `<polyline points="${pts(arcoYPata(v))}" ${estilo}/>`, 2));'''),
]
