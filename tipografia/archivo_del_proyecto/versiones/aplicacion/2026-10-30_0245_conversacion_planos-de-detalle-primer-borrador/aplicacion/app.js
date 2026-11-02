/* Las decisiones de la letra, en los planos de la anatomía.
 *
 * Cada decisión se mueve en su propio dibujo de detalle, con las convenciones de los planos (tipografia/planos/):
 * la celda y sus niveles, el corte del canal, la cuenca con su fondo plano y su desagüe, el fuste en tres planos,
 * el hombro en superelipse, la gota que cuelga por su peso y la esquina gastada por la intemperie. Cada dibujo
 * usa las mismas fórmulas que la gramática: lo que se mueve en él es lo que cambia en la letra. En tinta y
 * continuo, la obra; en violeta y a puntos, lo que se aparta de ella.
 *
 * A la izquierda, el plano del signo elegido; abajo, la caja. El motor es gramatica.js (la gramática de Python,
 * portada): no se toca aquí.
 */
(function () {
  "use strict";
  const D = window.DATOS, G = window.Gramatica;
  const T = D.T;
  const $ = (s) => document.querySelector(s);
  const TINTA = "#1d1c1a", VIOLETA = "#4a2470", GRIS = "#6d6a63", GRIS2 = "#9a968d", PAPEL = "#f6f4ee", FILETE = "#cfcac0",
    METAL = "#e2e0d9";
  const FAMILIA = { o: "oecdbpqóéá0689", l: "litjfkí()147", n: "nmhuúürvwxyzñ235", a: "a,sg.?;:¿«»—…" };
  const NOMBRE_GEN = { o: "la cuenca (o)", l: "el fuste (l)", n: "el hombro (n)", a: "el gancho y la gota (a)" };
  const familia = (s) => Object.keys(FAMILIA).find((g) => FAMILIA[g].includes(s)) || "a";
  const PARAM = Object.fromEntries(D.parametros.map((p) => [p.nombre, p]));
  const coma = (v, d = 1) => (Math.round(v * 10 ** d) / 10 ** d).toFixed(d).replace(".", ",").replace(/^-/, "−");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const clamp = (v, a, b) => Math.min(Math.max(v, a), b);
  const redondear = (v, paso) => Math.round(v / paso) * paso;
  const rad = (g) => g * Math.PI / 180;

  // ------------------------------------------------------------------ las nueve decisiones
  /* canales: el valor se guarda en canales y se pasa a px con el canal del momento. */
  const DECISIONES = [
    { clave: "razon_x", termino: "El borde: la altura de x", min: 1.4, max: 2.0, paso: 0.01,
      obra: () => D.razon_foto, ver: (v) => coma(v, 2) + " de las ascendentes",
      por: "Las ascendentes miden 1,71 veces la altura de x: es la única proporción que se toma de la foto del pie real. El testigo sustituto daba 1,52." },
    { clave: "canal", termino: "El contraste: ninguno", min: 20, max: 60, paso: 0.5,
      obra: (b) => b.base.e.canal, ver: (v, b) => `canal ${coma(v / 4)} mm (${Math.round(v * b.U)})`,
      por: "Un solo grosor en todo el recorrido: el punzón y la cinta no modulan (D2, D12). Sale de la o del pie: la media entre su grueso y su fino.",
      verso: "Desenterrar una voz / es desenterrar la mano del que la escribió." },
    { clave: "trapecio", termino: "El fondo plano", min: 0.4, max: 1.0, paso: 0.01,
      obra: () => PARAM.trapecio.fijo, ver: (v) => coma(v, 2) + " del ancho mayor",
      por: "Cada cuenca baja hasta un fondo plano: el trapecio con que la proyección llega a la pared (D8), la piscina vacía (D6).",
      verso: "Una piscina vacía, / donde una vez aprendí a flotar, / ahora aprendo a mirar." },
    { clave: "pared", termino: "La pared", min: 0, max: 1, paso: 0.01,
      obra: () => PARAM.pared.fijo, ver: (v) => coma(v, 2),
      por: "Cuánto se abomba la pared al bajar: 0 es el trapecio recto; 1, un cuenco. En medio, una vasija." },
    { clave: "quiebre", termino: "El quiebre", min: 0, max: 6, paso: 0.1,
      obra: () => PARAM.quiebre.fijo, ver: (v) => coma(v, 1) + "° por plano",
      por: "El asta tiene tres planos, como la placa que cambia de plano al apoyarse en el cuerpo (D3). Cada uno se aparta del eje apenas (D11).",
      verso: "Moverse como se mueve la piedra, / es decir, apenas, es decir, temblor," },
    { clave: "hombro", termino: "La tensión", min: 2, max: 5, paso: 0.05,
      obra: () => PARAM.hombro.fijo, ver: (v) => "n = " + coma(v, 2),
      por: "El arco es una superelipse, no una elipse (n = 2): la chapa de aluminio doblada a la fuerza sobre un hombro (D3).",
      verso: "Es lo más parecido a estar viva / que puede hacer una imagen." },
    { clave: "hombro_caida", termino: "Dónde arranca", min: 0.15, max: 0.7, paso: 0.01, debil: true,
      obra: () => PARAM.hombro_caida.fijo, ver: (v) => coma(v, 2) + " del borde al fondo",
      por: "Dónde el arco se vuelve vertical. Se tomó a ojo del testigo de la n: es la medida más débil, y falta medirla en el libro." },
    { clave: "gota_masa", termino: "La masa de la gota", min: 0.6, max: 2.0, paso: 0.05, canales: true,
      obra: () => PARAM.gota_masa.canales, ver: (v, b) => `${coma(v, 2)} c · ${coma(v * b.c / 4)} mm`,
      por: "Solo gotea lo que mira abajo: una masa que cae a plomada, por su peso. El líquido que chorrea de la boca (D16).",
      verso: "La tierra se dio de beber a sí misma" },
    { clave: "intemperie", termino: "El desgaste", min: 0, max: 0.3, paso: 0.005, canales: true,
      obra: () => PARAM.intemperie.canales, ver: (v, b) => `${coma(v, 3)} c · ${coma(v * b.c / 4)} mm`,
      por: "No hay remates: todas las esquinas se gastan con este radio. «Hoy está muy erosionado y casi no se ven esos detalles» (el pie)." },
  ];
  const DD = Object.fromEntries(DECISIONES.map((d) => [d.clave, d]));
  const FIJAS = [
    ["radio de la chapa · 0,6 c", "Mayor que medio canal: el contorno interior no se cruza y el aluminio no se rasga (P-02 · 2)."],
    ["desagüe · 3 mm", "El surco del punzón, que se detiene 3 mm antes de cerrar cada contorno (P-02 · 4)."],
    ["alivio · 0,28 c", "Un rebaje en cada rincón agudo, para que el metal no se desgarre (P-08 · 5)."],
    ["asiento · 2 × 0,9 c", "El pie del asta: de un canal a dos, en una curva cóncava (P-04 · 3)."],
    ["planos · 3", "Tres planos por asta (P-04 · 1)."],
    ["gancho · 105°", "Para que la gota cuelgue libre (P-06 · 1)."],
    ["gota · caída 0,3 c, cuello 0,55 c", "La gota cae por su peso (P-06 · 2)."],
    ["sifón · 0,6 c", "El enlace de la g y del 8: el único trazo más fino (P-08 · 4)."],
    ["cinta y punto · 1 c", "El punto es un trozo cuadrado de cinta (P-08 · 1)."],
  ];

  // ------------------------------------------------------------------ el estado (en este navegador)
  const GUARDA = "contenida-decisiones-v1";
  let estado = {}, seleccion = "o";
  try {
    const g = JSON.parse(localStorage.getItem(GUARDA) || "{}");
    estado = g.estado || {};
    if (g.seleccion) seleccion = g.seleccion;
  } catch (e) { estado = {}; }
  function guardar() {
    try { localStorage.setItem(GUARDA, JSON.stringify({ estado, seleccion })); } catch (e) { /* sin almacenamiento */ }
  }

  /* De las decisiones a los ajustes de la gramática (px, grados, razones). */
  function ajustesDe(est) {
    const aj = {};
    if (est.razon_x !== undefined) aj.razon_x = est.razon_x;
    const pre = G.preparar(D, aj);
    const c = est.canal !== undefined ? est.canal : pre.e.canal;
    for (const d of DECISIONES) {
      if (est[d.clave] === undefined || d.clave === "razon_x") continue;
      aj[d.clave] = d.canales ? est[d.clave] * c : est[d.clave];
    }
    return aj;
  }

  // ------------------------------------------------------------------ armar: rápido mientras se mueve, entero al soltar
  let base = null;
  const signos = {};
  function preparar() {
    const aj = ajustesDe(estado);
    base = G.preparar(D, aj);
    const [, y0, , y1] = G.celda(base.e, T);
    base.U = 1000 / (y1 - y0);
    base.c = base.e.canal;
    base.base = G.preparar(D, estado.razon_x !== undefined ? { razon_x: estado.razon_x } : {});
  }
  /* El signo elegido y las cuatro letras de los dibujos: unos milisegundos. */
  function armarRapido() {
    preparar();
    for (const s of new Set([seleccion, "o", "l", "n", "a"])) if (G.RECETAS[s]) signos[s] = G.construir(base, D, s);
  }
  /* La caja entera, de a poco: se llena celda por celda sin trabar la página. */
  let tanda = 0;
  function armarCaja() {
    const mia = ++tanda;
    const cola = D.caja.filter((c) => G.RECETAS[c.signo]).map((c) => c.signo);
    $("#caja").style.opacity = "0.5";
    const paso = () => {
      if (mia !== tanda) return;
      const t0 = performance.now();
      while (cola.length && performance.now() - t0 < 12) {
        const s = cola.shift();
        signos[s] = G.construir(base, D, s);
      }
      pintarCaja();
      if (cola.length) requestAnimationFrame(paso);
      else $("#caja").style.opacity = "";
    };
    requestAnimationFrame(paso);
  }

  const valor = (clave) => (estado[clave] !== undefined ? estado[clave] : DD[clave].obra(base));
  const obra = (clave) => DD[clave].obra(base);
  const movida = (clave) => estado[clave] !== undefined;

  // ------------------------------------------------------------------ piezas de dibujo, como en los planos
  const f = (v) => (+v).toFixed(1);
  const OBRA = `stroke="${TINTA}" fill="none"`;
  const TUYA = `stroke="${VIOLETA}" fill="none" stroke-dasharray="0.1 5" stroke-linecap="round" stroke-linejoin="round"`;
  const EJE = `stroke="${GRIS}" stroke-width="0.8" stroke-dasharray="20 4 2 4" fill="none"`;
  const pts = (ps) => ps.map(([x, y]) => f(x) + "," + f(y)).join(" ");
  function texto(x, y, t, o = {}) {
    return `<text x="${f(x)}" y="${f(y)}" text-anchor="${o.ancla || "start"}" font-family="Courier Prime, monospace" ` +
      `font-size="${o.tam || 12}" fill="${o.color || GRIS}"${o.fondo ? ` paint-order="stroke" stroke="${PAPEL}" stroke-width="3"` : ""}>${esc(t)}</text>`;
  }
  /* Una cota, con los ticks oblicuos de los planos. */
  function cota(x0, y0, x1, y1, t, o = {}) {
    const tick = (x, y) => `<line x1="${f(x - 4)}" y1="${f(y + 4)}" x2="${f(x + 4)}" y2="${f(y - 4)}" stroke="${o.color || TINTA}" stroke-width="1.4"/>`;
    const vertical = Math.abs(x1 - x0) < Math.abs(y1 - y0);
    const tx = vertical ? x0 + 6 : (x0 + x1) / 2, ty = vertical ? (y0 + y1) / 2 + 4 : y0 - 5;
    return `<line x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}" stroke="${o.color || TINTA}" stroke-width="0.8"/>${tick(x0, y0)}${tick(x1, y1)}` +
      texto(tx, ty, t, { ancla: vertical ? "start" : "middle", color: o.color || TINTA, fondo: true });
  }
  /* Un nivel: el triángulo de los planos, mitad en tinta. */
  function nivel(x, y, t, color = TINTA) {
    return `<path d="M${f(x)},${f(y)} l-6,-10 h12 z" fill="${PAPEL}" stroke="${color}" stroke-width="0.8"/>` +
      `<path d="M${f(x)},${f(y)} l0,-10 h6 z" fill="${color}"/>` + texto(x + 10, y - 2, t, { color });
  }
  /* El asa: lo que se toma con el dedo. En tinta si está como la obra; en violeta si se apartó. */
  function asa(clave, x, y) {
    const dd = DD[clave], v = valor(clave), mov = movida(clave);
    return `<g class="asa" data-clave="${clave}" tabindex="0" role="slider" aria-label="${esc(dd.termino)}" ` +
      `aria-valuemin="${dd.min}" aria-valuemax="${dd.max}" aria-valuenow="${+v.toFixed(4)}" ` +
      `aria-valuetext="${esc(dd.ver(v, base) + (mov ? "" : ", la obra"))}">` +
      `<circle class="golpe" cx="${f(x)}" cy="${f(y)}" r="18"/>` +
      `<circle cx="${f(x)}" cy="${f(y)}" r="6.5" fill="${mov ? VIOLETA : PAPEL}" stroke="${mov ? VIOLETA : TINTA}" stroke-width="1.6"/></g>`;
  }
  /* La letra del dibujo, chica, en su celda, arriba a la derecha: lo que cambia en ella. */
  function miniatura(s, x = 330, y = 8, lado = 62) {
    const r = signos[s];
    if (!r) return "";
    const k = lado / 600;
    return `<rect x="${x}" y="${y}" width="${lado}" height="${lado}" fill="${PAPEL}" stroke="${FILETE}"/>` +
      `<path transform="translate(${x} ${y}) scale(${k.toFixed(4)})" d="${dTrazo(r.geo)}" fill="${TINTA}" fill-rule="evenodd"/>` +
      texto(x + lado - 3, y + lado + 12, s, { ancla: "end", tam: 12 });
  }
  const dTrazo = (anillos) => anillos.map((a) => "M" + a.map(([x, y]) => x.toFixed(1) + "," + y.toFixed(1)).join(" L") + "Z").join(" ");
  /* Dos versiones de una forma: la obra en tinta y, si se apartó, la tuya en violeta y a puntos. */
  function dosVeces(claves, dibujar, ancho = 2) {
    const aparte = claves.some(movida);
    const enObra = Object.fromEntries(claves.map((k) => [k, obra(k)]));
    const ahora = Object.fromEntries(claves.map((k) => [k, valor(k)]));
    return dibujar(enObra, `${OBRA} stroke-width="${aparte ? 1 : ancho}"`) + (aparte ? dibujar(ahora, `${TUYA} stroke-width="${ancho + 0.6}"`) : "");
  }

  // ------------------------------------------------------------------ los siete dibujos
  /* Cada uno: sus decisiones, su dibujo y, para cada asa, del punto del dedo al valor. Lienzo de 400 × 270. */
  const DETALLES = [
    { id: "celda", rombo: "P-01 · 4", nombre: "la celda y sus niveles", origen: "medida del pie", claves: ["razon_x"],
      dibujo() {
        const e = base.e, y0 = 24, s = 222 / (e.desague - e.afuera), Y = (y) => y0 + (y - e.afuera) * s;
        const o = [];
        const lineas = [["afuera", e.afuera], ["fondo", e.fondo], ["desagüe", e.desague]];
        for (const [n, y] of lineas) {
          o.push(`<line x1="70" y1="${f(Y(y))}" x2="300" y2="${f(Y(y))}" stroke="${GRIS}" stroke-width="0.9" stroke-dasharray="10 5"/>`);
          o.push(texto(64, Y(y) + 4, n, { ancla: "end" }));
          o.push(nivel(318, Y(y), Math.round((e.fondo - y) * base.U) === 0 ? "±0" : (e.fondo > y ? "+" : "−") + Math.abs(Math.round((e.fondo - y) * base.U))));
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
        o.push(nivel(318, yv, "+" + Math.round((e.fondo - e.borde) * base.U), movida("razon_x") ? VIOLETA : TINTA));
        o.push(cota(282, Y(e.fondo), 282, yv, "x"));
        o.push(cota(268, Y(e.fondo), 268, Y(e.afuera), ""));
        o.push(texto(250, Y(e.afuera) + 14, "asc.", { ancla: "end" }));
        o.push(asa("razon_x", 300, yv));
        return o.join("");
      },
      mover: { razon_x(p) { const e = base.e, s = 222 / (e.desague - e.afuera), y = e.afuera + (p[1] - 24) / s; return (e.fondo - e.afuera) / Math.max(1, e.fondo - y); } } },

    { id: "canal", rombo: "P-02 · 1", nombre: "el canal", origen: "medida del pie", claves: ["canal"],
      dibujo() {
        const s = 1.9, cx = 180, yh = 92, o = [];
        o.push(texto(16, 24, "corte A–A · el aluminio, de canto"));
        const corte = (v, estilo) => {
          const w = v.canal * s, h = 0.42 * w;
          const d = `M16,${yh} H${f(cx - w / 2)} C${f(cx - w / 2)},${f(yh + h * 1.33)} ${f(cx + w / 2)},${f(yh + h * 1.33)} ${f(cx + w / 2)},${yh} H384`;
          return `<path d="${d}" ${estilo}/>`;
        };
        o.push(dosVeces(["canal"], corte, 2.2));
        const w = valor("canal") * s;
        o.push(cota(cx - w / 2, yh - 16, cx + w / 2, yh - 16, `${coma(valor("canal") / 4)} mm`));
        // en planta: un solo grosor
        o.push(texto(16, 168, "en planta: un solo grosor, sin contraste"));
        o.push(`<rect x="40" y="${f(214 - w / 2)}" width="300" height="${f(w)}" fill="${METAL}" stroke="${movida("canal") ? VIOLETA : TINTA}" stroke-width="1.2"${movida("canal") ? ' stroke-dasharray="0.1 5" stroke-linecap="round"' : ""}/>`);
        o.push(`<line x1="30" y1="214" x2="350" y2="214" ${EJE}/>`);
        o.push(miniatura("o"));
        o.push(asa("canal", cx + w / 2, yh));
        return o.join("");
      },
      mover: { canal(p) { return 2 * Math.abs(p[0] - 180) / 1.9; } } },

    { id: "cuenca", rombo: "P-03 · 2", nombre: "la cuenca", origen: "forma de la obra", claves: ["trapecio", "pared"],
      dibujo() {
        const cx = 190, cy = 104, rx = 128, yt = 30, yb = 218, des = 16, o = [];
        const forma = (v, estilo) => {
          const k = v.trapecio, p = v.pared;
          const izq = lado(cx - rx, cy, cx - k * rx, yb, p), der = lado(cx + rx, cy, cx + k * rx, yb, p);
          return `<path d="M${f(cx - rx)},${cy} A${rx},${cy - yt} 0 0 1 ${f(cx + rx)},${cy}" ${estilo}/>` +
            `<polyline points="${pts(izq)}" ${estilo}/><polyline points="${pts(der)}" ${estilo}/>` +
            `<line x1="${f(cx - k * rx)}" y1="${yb}" x2="${f(cx - des / 2)}" y2="${yb}" ${estilo}/>` +
            `<line x1="${f(cx + des / 2)}" y1="${yb}" x2="${f(cx + k * rx)}" y2="${yb}" ${estilo}/>`;
        };
        o.push(`<line x1="${cx}" y1="18" x2="${cx}" y2="${yb + 16}" ${EJE}/>`);
        o.push(dosVeces(["trapecio", "pared"], forma, 2.2));
        o.push(nivel(cx + rx + 30, yb, "fondo ±0"));
        o.push(texto(cx, yb + 18, "desagüe", { ancla: "middle" }));
        const k = valor("trapecio"), p = valor("pared");
        o.push(cota(cx - k * rx, yb + 34, cx + k * rx, yb + 34, `${coma(k, 2)} del ancho`));
        const M = medioDeLaPared(cx, cy, rx, yb, k, p);
        o.push(texto(M[0] + 14, M[1] - 8, `pared ${coma(p, 2)}`, { color: movida("pared") ? VIOLETA : TINTA, fondo: true }));
        o.push(miniatura("o"));
        o.push(asa("trapecio", cx + k * rx, yb));
        o.push(asa("pared", M[0], M[1]));
        return o.join("");
      },
      mover: {
        trapecio(p) { return (p[0] - 190) / 128; },
        pared(p) {
          const cx = 190, cy = 104, rx = 128, yb = 218, k = valor("trapecio");
          const M0 = medioDeLaPared(cx, cy, rx, yb, k, 0), xm = cx + rx, xf = cx + k * rx;
          const v = [3 / 8 * (xm - xf), 3 / 8 * (yb - cy)];
          return ((p[0] - M0[0]) * v[0] + (p[1] - M0[1]) * v[1]) / (v[0] * v[0] + v[1] * v[1]);
        },
      } },

    { id: "fuste", rombo: "P-04 · 1", nombre: "el fuste", origen: "forma de la obra", claves: ["quiebre"],
      dibujo() {
        const x = 180, y0 = 28, L = 196, X = 6, o = [];
        const planos = (q) => {
          const off = (L / 3) * Math.tan(rad(q)) * X;
          return [[x, y0], [x + off, y0 + L / 3], [x, y0 + 2 * L / 3], [x, y0 + L]];
        };
        o.push(`<polyline points="${pts(planos(valor("quiebre")))}" stroke="${METAL}" stroke-width="30" fill="none" stroke-linejoin="round"/>`);
        o.push(`<line x1="${x}" y1="14" x2="${x}" y2="${y0 + L + 10}" ${EJE}/>`);
        o.push(dosVeces(["quiebre"], (v, estilo) => `<polyline points="${pts(planos(v.quiebre))}" ${estilo}/>`, 2.2));
        const q = valor("quiebre"), p1 = planos(q)[1];
        if (q > 0.05) {
          const a = Math.atan2(p1[0] - x, p1[1] - y0), r = 54;
          o.push(`<path d="M${x},${y0 + r} A${r},${r} 0 0 0 ${f(x + r * Math.sin(a))},${f(y0 + r * Math.cos(a))}" fill="none" stroke="${TINTA}" stroke-width="0.8"/>`);
        }
        o.push(texto(x + 26, y0 + 70, `${coma(q, 1)}° por plano`, { color: movida("quiebre") ? VIOLETA : TINTA, fondo: true }));
        o.push(texto(16, 258, "los ángulos, dibujados × 6"));
        o.push(texto(x - 24, y0 + 6, "corte", { ancla: "end" }));
        o.push(texto(x - 24, y0 + L - 2, "asiento", { ancla: "end" }));
        o.push(miniatura("l"));
        o.push(asa("quiebre", p1[0], p1[1]));
        return o.join("");
      },
      mover: { quiebre(p) { return Math.atan(Math.max(0, p[0] - 180) / (6 * 196 / 3)) * 180 / Math.PI; } } },

    { id: "hombro", rombo: "P-05 · 1 · 3", nombre: "el hombro", origen: "forma de la obra · medida a ojo", claves: ["hombro", "hombro_caida"],
      dibujo() {
        const xi = 104, xd = 284, yt = 36, F = 232, cx = (xi + xd) / 2, rx = (xd - xi) / 2, o = [];
        const n_ = (v, estilo) => {
          const ya = yt + v.hombro_caida * (F - yt);
          const arco = superelipse(cx, ya, rx, ya - yt, v.hombro);
          return `<line x1="${xi}" y1="${yt}" x2="${xi}" y2="${F}" ${estilo}/><polyline points="${pts(arco)}" ${estilo}/>` +
            `<line x1="${xd}" y1="${f(ya)}" x2="${xd}" y2="${F}" ${estilo}/>`;
        };
        for (const [nombre, y] of [["borde", yt], ["fondo", F]]) {
          o.push(`<line x1="60" y1="${y}" x2="330" y2="${y}" stroke="${GRIS}" stroke-width="0.9" stroke-dasharray="10 5"/>`);
          o.push(texto(54, y + 4, nombre, { ancla: "end" }));
        }
        o.push(dosVeces(["hombro", "hombro_caida"], n_, 2.2));
        const n = valor("hombro"), cae = valor("hombro_caida"), ya = yt + cae * (F - yt), ry = ya - yt, s = Math.pow(2, -1 / n);
        const pt45 = [cx + rx * s, ya - ry * s];
        o.push(`<line x1="${cx}" y1="${f(ya)}" x2="${f(cx + rx)}" y2="${yt}" stroke="${FILETE}" stroke-width="0.8"/>`);
        o.push(texto(pt45[0] + 12, pt45[1] - 10, `n = ${coma(n, 2)}`, { color: movida("hombro") ? VIOLETA : TINTA, fondo: true }));
        o.push(nivel(xd + 42, ya, `arranca ${coma(cae, 2)}`, movida("hombro_caida") ? VIOLETA : TINTA));
        o.push(texto(xd + 42, ya + 14, "a ojo: falta medirlo"));
        o.push(miniatura("n", 8, 8));
        o.push(asa("hombro", pt45[0], pt45[1]));
        o.push(asa("hombro_caida", xd, ya));
        return o.join("");
      },
      mover: {
        hombro(p) {
          const xi = 104, xd = 284, yt = 36, F = 232, cx = (xi + xd) / 2, rx = (xd - xi) / 2;
          const ya = yt + valor("hombro_caida") * (F - yt), ry = ya - yt;
          const s = clamp(((p[0] - cx) * rx - (p[1] - ya) * ry) / (rx * rx + ry * ry), 0.5, 0.97);
          return -Math.LN2 / Math.log(s);
        },
        hombro_caida(p) { return (p[1] - 36) / (232 - 36); },
      } },

    { id: "gota", rombo: "P-06 · 2", nombre: "la gota", origen: "forma de la obra", claves: ["gota_masa"],
      dibujo() {
        const s = 1.15, c = base.c * s, px = 250, py = 104, o = [];
        // el gancho: termina mirando abajo
        o.push(`<path d="M90,${py + 36} A80,80 0 0 1 ${px},${py}" stroke="${METAL}" stroke-width="${f(c)}" fill="none"/>`);
        o.push(`<path d="M90,${py + 36} A80,80 0 0 1 ${px},${py}" ${EJE}/>`);
        const gota_ = (v, estilo) => {
          const m = v.gota_masa * c, caida = 0.3 * c, cuello = 0.55 * c;
          const cy = py + caida + m / 2, oy = cy - m / 2;
          return `<ellipse cx="${px}" cy="${f(oy + 1.15 * m / 2)}" rx="${f(m / 2)}" ry="${f(1.15 * m / 2)}" ${estilo}/>` +
            `<path d="M${f(px - c / 2)},${py} L${f(px - cuello / 2)},${f(cy)} M${f(px + c / 2)},${py} L${f(px + cuello / 2)},${f(cy)}" ${estilo}/>`;
        };
        o.push(dosVeces(["gota_masa"], gota_, 2));
        const m = valor("gota_masa") * c, abajo = py + 0.3 * c + 1.15 * m;
        o.push(cota(px + m / 2 + 18, py + 0.3 * c, px + m / 2 + 18, abajo, `${coma(valor("gota_masa"), 2)} c`));
        // la gravedad, en lugar del norte
        const gx = 360, gy = 40;
        o.push(`<circle cx="${gx}" cy="${gy}" r="14" fill="none" stroke="${TINTA}" stroke-width="1"/>` +
          `<line x1="${gx}" y1="${gy - 20}" x2="${gx}" y2="${gy + 8}" stroke="${TINTA}" stroke-width="1.2"/>` +
          `<path d="M${gx},${gy + 18} l-5,-12 h10 z" fill="${TINTA}"/>` + texto(gx, gy + 32, "GRAVEDAD", { ancla: "middle", tam: 10, color: TINTA }));
        o.push(texto(16, 258, "solo gotea lo que mira abajo"));
        o.push(miniatura("a", 8, 8));
        o.push(asa("gota_masa", px, abajo));
        return o.join("");
      },
      mover: { gota_masa(p) { const s = 1.15, c = base.c * s; return (p[1] - 104 - 0.3 * c) / (1.15 * c); } } },

    { id: "intemperie", rombo: "P-02 · 3", nombre: "la intemperie", origen: "forma de la obra", claves: ["intemperie"],
      dibujo() {
        const x0 = 130, x1 = 270, yt = 66, ancho = x1 - x0, o = [];
        const borde = (v, estilo) => {
          const r = Math.max(0.01, v.intemperie * ancho);
          return `<path d="M${x0},262 V${f(yt + r)} A${f(r)},${f(r)} 0 0 1 ${f(x0 + r)},${yt} H${f(x1 - r)} A${f(r)},${f(r)} 0 0 1 ${x1},${f(yt + r)} V262" ${estilo}/>`;
        };
        o.push(borde({ intemperie: valor("intemperie") }, `fill="${METAL}" stroke="none"`));
        o.push(`<path d="M${x0},${yt + 26} V${yt} H${x0 + 26} M${x1 - 26},${yt} H${x1} V${yt + 26}" fill="none" stroke="${GRIS2}" stroke-width="1" stroke-dasharray="2 3"/>`);
        o.push(dosVeces(["intemperie"], borde, 2));
        o.push(`<line x1="${(x0 + x1) / 2}" y1="40" x2="${(x0 + x1) / 2}" y2="262" ${EJE}/>`);
        const r = valor("intemperie") * ancho, k = 1 - Math.SQRT1_2;
        o.push(texto(x1 + 14, yt + 4, `r = ${coma(valor("intemperie"), 3)} c`, { color: movida("intemperie") ? VIOLETA : TINTA }));
        o.push(texto(x0 - 10, yt - 10, "sin remate: un corte", { ancla: "end" }));
        o.push(texto(16, 258, "la punta del fuste, × 4"));
        o.push(miniatura("l"));
        o.push(asa("intemperie", x1 - k * r, yt + k * r));
        return o.join("");
      },
      mover: { intemperie(p) { const k = 1 - Math.SQRT1_2, d = ((270 - p[0]) + (p[1] - 66)) / 2; return Math.max(0, d / k) / 140; } } },
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
  function medioDeLaPared(cx, cy, rx, yb, k, p) {
    const xm = cx + rx, xf = cx + k * rx;
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

  // ------------------------------------------------------------------ armar los dibujos y sus decisiones
  function armarDetalles() {
    const filas = (dd) => `
      <div class="decision" id="d-${dd.clave}">
        <div class="linea"><span class="nombre">${esc(dd.termino)}</span><span class="valor" id="v-${dd.clave}"></span>
          <button class="volver" type="button" data-volver="${dd.clave}" hidden>volver a la obra</button></div>
        <p class="por-que">${esc(dd.por)}</p>
        ${dd.verso ? `<p class="verso">«${esc(dd.verso)}»</p>` : ""}
        ${dd.clave === "intemperie" ? '<p class="aviso" id="aviso-intemperie" hidden>Con más de 0,175 c, las cifras pierden su celda: el desgaste se come el trazo de 0,35 c.</p>' : ""}
      </div>`;
    $("#detalles").innerHTML = DETALLES.map((det) => `
      <article class="detalle" id="det-${det.id}">
        <div class="titulo"><span class="rombo">${esc(det.rombo)}</span><h2>${esc(det.nombre)}</h2><span class="origen">${esc(det.origen)}</span></div>
        <svg class="dibujo" id="s-${det.id}" viewBox="0 0 400 270" role="group" aria-label="${esc(det.nombre)}"></svg>
        ${det.claves.map((k) => filas(DD[k])).join("")}
      </article>`).join("") +
      `<aside class="fijas"><h2>Lo que no se mueve</h2><dl>${FIJAS.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl></aside>`;

    for (const det of DETALLES) {
      const svg = $("#s-" + det.id);
      let clave = null;
      const punto = (ev) => {
        const m = svg.getScreenCTM();
        const q = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
        return [q.x, q.y];
      };
      svg.addEventListener("pointerdown", (ev) => {
        const a = ev.target.closest(".asa");
        if (!a) return;
        ev.preventDefault();
        clave = a.dataset.clave;
        enfocada = clave;
        a.focus({ preventScroll: true });
        svg.setPointerCapture(ev.pointerId);
      });
      svg.addEventListener("pointermove", (ev) => {
        if (!clave) return;
        poner(clave, det.mover[clave](punto(ev)));
      });
      const soltar = () => { if (clave) { clave = null; asentar(); } };
      svg.addEventListener("pointerup", soltar);
      svg.addEventListener("pointercancel", soltar);
      svg.addEventListener("keydown", (ev) => {
        const a = ev.target.closest(".asa");
        if (!a) return;
        const dd = DD[a.dataset.clave], v = valor(dd.clave), k = ev.shiftKey ? 10 : 1;
        let n = null;
        if (ev.key === "ArrowRight" || ev.key === "ArrowUp") n = v + dd.paso * k;
        else if (ev.key === "ArrowLeft" || ev.key === "ArrowDown") n = v - dd.paso * k;
        else if (ev.key === "Home") n = dd.min;
        else if (ev.key === "End") n = dd.max;
        else if (ev.key === "Delete" || ev.key === "Backspace" || ev.key === "Escape") { ev.preventDefault(); volver(dd.clave); return; }
        if (n === null) return;
        ev.preventDefault();
        enfocada = dd.clave;
        poner(dd.clave, n);
        clearTimeout(svg._t);
        svg._t = setTimeout(asentar, 250);
      });
      svg.addEventListener("focusin", (ev) => { const a = ev.target.closest(".asa"); if (a) enfocada = a.dataset.clave; });
    }
    for (const b of document.querySelectorAll("[data-volver]")) b.addEventListener("click", () => volver(b.dataset.volver));
  }

  let enfocada = null;
  function poner(clave, v) {
    const dd = DD[clave];
    v = clamp(redondear(v, dd.paso), dd.min, dd.max);
    if (Math.abs(v - dd.obra(base)) < dd.paso / 2) delete estado[clave];
    else estado[clave] = v;
    pedir();
  }
  function volver(clave) { delete estado[clave]; pedir(); asentar(); }

  function pintarDetalles() {
    const activo = document.activeElement && document.activeElement.closest ? document.activeElement.closest(".asa") : null;
    for (const det of DETALLES) {
      $("#s-" + det.id).innerHTML = det.dibujo();
      $("#det-" + det.id).classList.toggle("ajustado", det.claves.some(movida));
    }
    for (const dd of DECISIONES) {
      const mov = movida(dd.clave);
      $("#v-" + dd.clave).textContent = dd.ver(valor(dd.clave), base);
      $("#d-" + dd.clave).classList.toggle("ajustada", mov);
      $(`[data-volver="${dd.clave}"]`).hidden = !mov;
    }
    $("#aviso-intemperie").hidden = valor("intemperie") <= 0.175;
    if (activo && enfocada) {                                       // el dibujo se rehízo: el foco vuelve a su asa
      const a = document.querySelector(`.asa[data-clave="${enfocada}"]`);
      if (a) a.focus({ preventScroll: true });
    }
  }

  // ------------------------------------------------------------------ el plano
  const nivelUPM = (y) => { const u = Math.round((base.e.fondo - y) * base.U); return u === 0 ? "±0" : (u > 0 ? "+" : "−") + Math.abs(u); };
  const mmU = (px) => `${coma(px / 4)} (${Math.round(px * base.U)})`;

  function cotaPlano(x0, x1, y, t) {
    const tk = (x) => `<line x1="${x - 5}" y1="${y + 5}" x2="${x + 5}" y2="${y - 5}" stroke="${TINTA}" stroke-width="1.6"/>`;
    return `<line x1="${x0 - 6}" y1="${y}" x2="${x1 + 6}" y2="${y}" stroke="${TINTA}" stroke-width="0.8"/>${tk(x0)}${tk(x1)}` +
      `<text x="${(x0 + x1) / 2}" y="${y - 5}" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" ` +
      `fill="${TINTA}" paint-order="stroke" stroke="${PAPEL}" stroke-width="3">${esc(t)}</text>`;
  }

  function svgPlano(r) {
    const e = base.e, S = r.signo;
    const [cx0, cy0, cx1, cy1] = G.celda(e, T);
    const rec = (D.caja.find((c) => c.signo === S) || {}).estado === "reconstruida";
    const [x0, y0, x1, y1] = G.limites(r.geo);
    const o = [];
    o.push(`<defs><pattern id="metal" patternUnits="userSpaceOnUse" width="4.4" height="4.4" patternTransform="rotate(45)">` +
      `<rect width="4.4" height="4.4" fill="${rec ? "#ebe6ef" : "#e2e0d9"}"/><line x1="0" y1="0" x2="0" y2="4.4" ` +
      `stroke="${rec ? "#b9a9c9" : "#a9a69d"}" stroke-width="0.7"/></pattern></defs>`);
    o.push(`<rect x="-110" y="-30" width="830" height="700" fill="${PAPEL}"/>`);
    o.push(`<rect x="0" y="0" width="600" height="600" fill="none" stroke="${GRIS2}" stroke-width="1"/>`);
    o.push(`<rect x="${cx0}" y="${cy0}" width="${cx1 - cx0}" height="${cy1 - cy0}" fill="none" stroke="${TINTA}" stroke-width="1.2"/>`);
    o.push(`<line x1="300" y1="${cy0 - 18}" x2="300" y2="${cy1 + 18}" stroke="${GRIS}" stroke-width="0.7" stroke-dasharray="26 5 2.4 5"/>`);
    for (const [n, y] of [["afuera", e.afuera], ["borde", e.borde], ["fondo", e.fondo], ["desagüe", e.desague]]) {
      o.push(`<line x1="${cx0 - 40}" y1="${y}" x2="${cx1 + 40}" y2="${y}" stroke="${GRIS}" stroke-width="1" stroke-dasharray="12 6"/>`);
      o.push(`<text x="${cx0 - 46}" y="${y + 4}" text-anchor="end" font-family="Courier Prime, monospace" font-size="13" fill="${GRIS}">${n}</text>`);
      const xn = cx1 + 50;
      o.push(`<path d="M${xn},${y} l-6,-10 h12 z" fill="${PAPEL}" stroke="${TINTA}" stroke-width="0.8"/>` +
        `<path d="M${xn},${y} l0,-10 h6 z" fill="${TINTA}"/>` +
        `<text x="${xn + 10}" y="${y - 3}" font-family="Courier Prime, monospace" font-size="13" fill="${TINTA}">${nivelUPM(y)}</text>`);
    }
    o.push(`<text x="${cx1 + 40}" y="${cy0 - 8}" font-family="Courier Prime, monospace" font-size="11" fill="${GRIS}">NIVELES (UPM)</text>`);
    // el cuerpo
    o.push(`<path d="${dTrazo(r.geo)}" fill="url(#metal)" fill-rule="evenodd" stroke="${rec ? VIOLETA : TINTA}" ` +
      `stroke-width="${rec ? 2.2 : 2}" ${rec ? 'stroke-dasharray="0.5 4.5" stroke-linecap="round"' : ""} stroke-linejoin="round"/>`);
    // los ejes, los nodos, los alivios y las partes
    for (const [t, w] of r.glifo.trazos) {
      if (t.length < 2 || (w !== null && w < 1)) continue;
      o.push(`<polyline points="${t.map(([x, y]) => x.toFixed(1) + "," + y.toFixed(1)).join(" ")}" fill="none" stroke="${TINTA}" ` +
        `stroke-width="0.8" stroke-dasharray="26 5 2.4 5"/>`);
    }
    for (const [x, y] of r.glifo.nodos) o.push(`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.8" fill="${PAPEL}" stroke="${TINTA}" stroke-width="0.8"/>`);
    for (const m of r.glifo.menos) o.push(`<circle cx="${m.x.toFixed(1)}" cy="${m.y.toFixed(1)}" r="${m.r.toFixed(1)}" fill="none" stroke="${GRIS}" stroke-width="0.8" stroke-dasharray="4 3"/>`);
    const vistas = new Set();
    for (const [n, [x, y]] of r.glifo.marcas) {
      const k = n + Math.round(x / 20) + "," + Math.round(y / 20);
      if (vistas.has(k)) continue;
      vistas.add(k);
      o.push(`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.6" fill="${VIOLETA}"/>` +
        `<text x="${(x + 7).toFixed(1)}" y="${(y - 6).toFixed(1)}" font-family="Courier Prime, monospace" font-size="11" fill="${VIOLETA}" ` +
        `paint-order="stroke" stroke="${PAPEL}" stroke-width="3">${esc(n)}</text>`);
    }
    // cotas: los lados y la tinta, en mm de la placa (UPM)
    const yc = 624;
    o.push(cotaPlano(cx0, x0, yc, coma((x0 - cx0) / 4)));
    o.push(cotaPlano(x0, x1, yc, mmU(x1 - x0)));
    o.push(cotaPlano(x1, cx1, yc, coma((cx1 - x1) / 4)));
    o.push(cotaPlano(cx0, cx1, yc + 24, `celda ${mmU(cx1 - cx0)} · avance`));
    // la gravedad, en lugar del norte
    const gx = 660, gy = 40;
    o.push(`<circle cx="${gx}" cy="${gy}" r="16" fill="none" stroke="${TINTA}" stroke-width="1"/>` +
      `<line x1="${gx}" y1="${gy - 22}" x2="${gx}" y2="${gy + 8}" stroke="${TINTA}" stroke-width="1.2"/>` +
      `<path d="M${gx},${gy + 20} l-6,-14 h12 z" fill="${TINTA}"/>` +
      `<text x="${gx}" y="${gy + 36}" text-anchor="middle" font-family="Courier Prime, monospace" font-size="10" fill="${TINTA}">GRAVEDAD</text>`);
    o.push(`<text x="-100" y="662" font-family="Courier Prime, monospace" font-size="11" fill="${GRIS}">placa de 150 mm · 4 px = 1 mm · ` +
      `1000 UPM = la celda · Contenida · propuesta de la máquina</text>`);
    return o.join("");
  }

  function pintarPlano() {
    const r = signos[seleccion];
    if (!r) return;
    $("#plano").innerHTML = svgPlano(r);
    const c = D.caja.find((x) => x.signo === seleccion) || {};
    $("#p-signo").textContent = seleccion;
    const rec = c.estado === "reconstruida";
    $("#p-estado").textContent = `celda ${c.celda} · ${rec ? "reconstruido" : "hallado en el pie"} · su raíz: ${NOMBRE_GEN[familia(seleccion)]}`;
    $("#p-estado").classList.toggle("r", rec);
    $("#p-receta").textContent = r.receta;
    const e = base.e, [cx0, , cx1] = G.celda(e, T), [x0, y0, x1, y1] = G.limites(r.geo);
    const partes = [...new Set(r.glifo.marcas.map(([n]) => n))].join(" · ");
    const filas = [
      ["ancho de tinta", mmU(x1 - x0)], ["lado izquierdo", mmU(x0 - cx0)], ["lado derecho", mmU(cx1 - x1)],
      ["sube hasta", nivelUPM(y0) + " UPM"], ["baja hasta", nivelUPM(y1) + " UPM"], ["canal", mmU(base.c)],
      ["partes", partes || "—"],
    ];
    $("#p-medidas").innerHTML = filas.map(([k, v]) => `<li><span>${esc(k)}</span>${esc(v)}</li>`).join("");
  }

  // ------------------------------------------------------------------ la caja
  function pintarCaja() {
    const o = [];
    for (const c of D.caja) {
      const x = (c.columna - 1) * 153, y = (c.fila - 1) * 153;
      const r = signos[c.signo];
      const rec = c.estado === "reconstruida", sel = c.signo === seleccion;
      o.push(`<g class="celda" data-s="${esc(c.signo)}" transform="translate(${x} ${y})" ${G.RECETAS[c.signo] ? "" : 'aria-disabled="true"'}>` +
        `<rect class="fondo" width="150" height="150" fill="${PAPEL}" stroke="${sel ? VIOLETA : FILETE}" stroke-width="${sel ? 4 : 1}"/>` +
        `<text x="6" y="16" font-family="Courier Prime, monospace" font-size="13" fill="${rec ? VIOLETA : GRIS}">${c.celda}</text>`);
      if (r) {
        o.push(`<path transform="scale(0.25)" d="${dTrazo(r.geo)}" fill="${rec ? VIOLETA : TINTA}" fill-rule="evenodd" ${rec ? 'fill-opacity="0.85"' : ""}/>`);
        o.push(`<text x="144" y="16" text-anchor="end" font-family="Newsreader, serif" font-style="italic" font-size="14" fill="${GRIS2}">${familia(c.signo)}</text>`);
      } else if (!G.RECETAS[c.signo]) {
        o.push(`<text x="75" y="88" text-anchor="middle" font-family="Newsreader, serif" font-size="56" fill="${GRIS2}">¶</text>` +
          `<text x="75" y="134" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" fill="${GRIS}">con los dedos</text>`);
      }
      o.push("</g>");
    }
    $("#caja").innerHTML = o.join("");
  }
  $("#caja").addEventListener("click", (ev) => {
    const g = ev.target.closest(".celda");
    if (!g || g.getAttribute("aria-disabled")) return;
    seleccion = g.dataset.s;
    if (!signos[seleccion]) signos[seleccion] = G.construir(base, D, seleccion);
    guardar();
    pintarCaja();
    pintarPlano();
  });

  // ------------------------------------------------------------------ armar y pintar, sin trabarse
  function pintarTodo() {
    pintarPlano();
    pintarDetalles();
  }
  let pedido = null;
  function pedir() {
    if (pedido) return;
    pedido = requestAnimationFrame(() => {
      pedido = null;
      armarRapido();
      pintarTodo();
    });
  }
  /* Al soltar: se guarda, se anuncia y la caja se rehace entera. */
  function asentar() {
    if (pedido) { cancelAnimationFrame(pedido); pedido = null; }
    guardar();
    armarRapido();
    pintarTodo();
    armarCaja();
    const movidas = DECISIONES.filter((dd) => movida(dd.clave)).map((dd) => `${dd.termino}: ${dd.ver(valor(dd.clave), base)}`);
    $("#anuncio").textContent = movidas.length ? "Se aparta de la obra. " + movidas.join("; ") + "." : "Todo como la obra.";
  }

  // ------------------------------------------------------------------ las salidas
  function nota(t) { const n = $("#nota"); n.textContent = t; clearTimeout(n._t); n._t = setTimeout(() => { n.textContent = ""; }, 6000); }
  /* Fuera de claude.ai, la descarga es un enlace. Dentro del visor los enlaces de descarga no hacen nada:
   * se usa la capacidad «downloads», y si no está, el texto se copia y queda a la vista para guardarlo a mano. */
  const enVisor = !!(window.claude && typeof window.claude.use === "function");
  let descargas = null;
  if (enVisor) window.claude.use("downloads").then((x) => { descargas = x; }, () => {});
  function aMano(nombre, t) {
    $("#salida").hidden = false;
    const a = $("#salida-texto");
    a.value = t;
    a.focus();
    a.select();
    if (navigator.clipboard) navigator.clipboard.writeText(t).then(() => nota(`${nombre}: copiado.`), () => {});
  }
  async function bajar(nombre, tipo, t) {
    if (descargas) {
      try { await descargas.save({ filename: nombre, data: t }); nota(`${nombre}: guardado.`); }
      catch (e) {
        if (e && e.code === "declined") nota("Descarga cancelada.");
        else aMano(nombre, t);
      }
      return false;
    }
    if (enVisor) { aMano(nombre, t); return false; }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([t], { type: tipo }));
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    return true;
  }
  $("#a-obra").addEventListener("click", () => { estado = {}; asentar(); nota("Volvió a la propuesta de la obra."); });
  $("#a-json").addEventListener("click", () => {
    const aj = ajustesDe(estado), valores = { razon_x: +base.razon.toFixed(4) };
    for (const [k, p] of Object.entries(base.P)) valores[k] = +(+p.valor).toFixed(3);
    const t = JSON.stringify({
      contenida: "parámetros de la gramática",
      fecha: new Date().toISOString().slice(0, 10),
      uso: "python3 tipografia/simulacion/gramatica.py --parametros parametros.json",
      ajustes: Object.fromEntries(Object.entries(aj).map(([k, v]) => [k, +(+v).toFixed(4)])),
      valores,
    }, null, 1);
    bajar("parametros.json", "application/json", t + "\n").then((hecho) => {
      if (hecho) nota(Object.keys(aj).length ? "parametros.json: solo van los ajustes." : "Sin ajustes: es la propuesta de la obra.");
    });
  });
  $("#a-svg").addEventListener("click", () => {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-110 -30 830 700" width="207.5mm" height="175mm">` +
      `<title>Contenida · ${esc(seleccion)} · plano</title>${svgPlano(signos[seleccion])}</svg>\n`;
    bajar(`contenida_plano_${seleccion.codePointAt(0).toString(16)}.svg`, "image/svg+xml", svg).then((hecho) => {
      if (hecho) nota("El plano, a escala: 4 px del lienzo son 1 mm de la placa.");
    });
  });

  // ------------------------------------------------------------------ arrancar
  if (!G.RECETAS[seleccion]) seleccion = "o";
  armarDetalles();
  armarRapido();
  pintarTodo();
  pintarCaja();
  armarCaja();
})();
