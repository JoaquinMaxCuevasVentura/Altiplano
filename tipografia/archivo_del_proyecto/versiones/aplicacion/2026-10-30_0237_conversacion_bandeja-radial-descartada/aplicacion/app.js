/* Las decisiones de la letra: la mesa.
 *
 * Arriba a la izquierda, la bandeja: un dedo de agua visto desde arriba. En reposo es la obra; el desagüe del
 * centro es lo que dicen el pie y la obra. Las seis decisiones de la forma son seis líneas que pasan por el
 * desagüe, cada una con sus dos extremos. Donde se toca el agua, cada decisión se mueve según cuánto mira el
 * dedo hacia su línea (la proyección del punto sobre ella): un solo punto mueve las seis a la vez, y las seis
 * quedan sobre el círculo que va del desagüe al dedo. La manera viene de Ultravaria, de Aimeric (un reel): un
 * campo radial donde una coordenada mueve muchos ejes. Aquí no hay ejes de una fuente variable: hay decisiones,
 * cada una con su porqué.
 *
 * A la derecha, el plano del signo elegido y las cuatro piezas (o, l, n, a: las letras que dan las partes).
 * Debajo, las nueve decisiones una por una: las tres medidas del pie, que el agua no mueve, y las seis de la
 * obra. Abajo, la caja.
 *
 * El motor es gramatica.js (la gramática de Python, portada): no se toca aquí.
 */
(function () {
  "use strict";
  const D = window.DATOS, G = window.Gramatica;
  const T = D.T;
  const $ = (s) => document.querySelector(s);
  const TINTA = "#1d1c1a", VIOLETA = "#4a2470", LILA = "#b9a6d6", GRIS = "#6d6a63", GRIS2 = "#9a968d", PAPEL = "#f6f4ee",
    FILETE = "#cfcac0";
  const FAMILIA = { o: "oecdbpqóéá0689", l: "litjfkí()147", n: "nmhuúürvwxyzñ235", a: "a,sg.?;:¿«»—…" };
  const NOMBRE_GEN = { o: "la cuenca (o)", l: "el fuste (l)", n: "el hombro (n)", a: "el gancho y la gota (a)" };
  const PIEZAS = [["o", "la cuenca"], ["l", "el fuste"], ["n", "el hombro"], ["a", "el gancho y la gota"]];
  const familia = (s) => Object.keys(FAMILIA).find((g) => FAMILIA[g].includes(s)) || "a";
  const PARAM = Object.fromEntries(D.parametros.map((p) => [p.nombre, p]));
  const coma = (v, d = 1) => (Math.round(v * 10 ** d) / 10 ** d).toFixed(d).replace(".", ",").replace(/^-/, "−");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const clamp = (v, a, b) => Math.min(Math.max(v, a), b);
  const redondear = (v, paso) => Math.round(v / paso) * paso;

  // ------------------------------------------------------------------ las nueve decisiones
  /* grupo: «pie» son medidas (el agua no las mueve); «obra» es la forma, una línea de la bandeja.
   * angulo: hacia dónde apunta el extremo «mas» de la línea, en grados desde arriba y en sentido horario:
   * lo que pesa queda abajo (la gota pesada, el cuenco, lo gastado); lo nuevo y recto, arriba.
   * canales: el valor se guarda en canales y se pasa a px con el canal del momento.
   * pieza: la letra que da la parte que cambia («*», todas). */
  const DECISIONES = [
    { clave: "razon_x", grupo: "pie", termino: "La altura de x", rombo: "P-01 · 4", min: 1.4, max: 2.0, paso: 0.01,
      menos: "x alta", mas: "x baja", pieza: "*",
      obra: () => D.razon_foto, ver: (v) => coma(v, 2) + " de las ascendentes",
      por: "Las ascendentes miden 1,71 veces la altura de x: es la única proporción que se toma de la foto del pie real. El testigo sustituto daba 1,52." },
    { clave: "canal", grupo: "pie", termino: "El contraste: ninguno", rombo: "P-02 · 1", min: 20, max: 60, paso: 0.5,
      menos: "fino", mas: "grueso", pieza: "*",
      obra: (b) => b.base.e.canal, ver: (v, b) => `canal ${coma(v / 4)} mm (${Math.round(v * b.U)})`,
      por: "Un solo grosor en todo el recorrido: el punzón y la cinta no modulan (D2, D12). Sale de la o del pie: la media entre su grueso y su fino.",
      verso: "Desenterrar una voz / es desenterrar la mano del que la escribió." },
    { clave: "hombro_caida", grupo: "pie", termino: "El hombro: dónde arranca", rombo: "P-05 · 3", min: 0.15, max: 0.7, paso: 0.01,
      menos: "arranca alto", mas: "arranca bajo", pieza: "n",
      obra: () => PARAM.hombro_caida.fijo, ver: (v) => coma(v, 2) + " del borde al fondo",
      por: "Dónde el arco se vuelve vertical. Se tomó a ojo del testigo de la n: es la medida más débil, y falta medirla en el libro." },
    { clave: "hombro", grupo: "obra", angulo: 30, termino: "El hombro: la tensión", rombo: "P-05 · 1", min: 2, max: 5, paso: 0.05,
      menos: "hombro redondo", mas: "hombro tenso", pieza: "n",
      obra: () => PARAM.hombro.fijo, ver: (v) => "n = " + coma(v, 2),
      por: "El arco es una superelipse, no una elipse (n = 2): la chapa de aluminio doblada a la fuerza sobre un hombro (D3).",
      verso: "Es lo más parecido a estar viva / que puede hacer una imagen." },
    { clave: "quiebre", grupo: "obra", angulo: 60, termino: "El asta: el quiebre", rombo: "P-04 · 1", min: 0, max: 6, paso: 0.1,
      menos: "asta recta", mas: "asta quebrada", pieza: "l",
      obra: () => PARAM.quiebre.fijo, ver: (v) => coma(v, 1) + "° por plano",
      por: "El asta tiene tres planos, como la placa que cambia de plano al apoyarse en el cuerpo (D3). Cada uno se aparta del eje apenas (D11).",
      verso: "Moverse como se mueve la piedra, / es decir, apenas, es decir, temblor," },
    { clave: "trapecio", grupo: "obra", angulo: 90, termino: "La panza: el fondo plano", rombo: "P-03 · 2", min: 0.4, max: 1.0, paso: 0.01,
      menos: "fondo angosto", mas: "fondo ancho", pieza: "o",
      obra: () => PARAM.trapecio.fijo, ver: (v) => coma(v, 2) + " del ancho mayor",
      por: "Cada cuenca baja hasta un fondo plano: el trapecio con que la proyección llega a la pared (D8), la piscina vacía (D6).",
      verso: "Una piscina vacía, / donde una vez aprendí a flotar, / ahora aprendo a mirar." },
    { clave: "pared", grupo: "obra", angulo: 120, termino: "La panza: la pared", rombo: "P-03 · 2", min: 0, max: 1, paso: 0.01,
      menos: "pared recta", mas: "cuenco", pieza: "o",
      obra: () => PARAM.pared.fijo, ver: (v) => coma(v, 2),
      por: "Cuánto se abomba la pared al bajar: 0 es el trapecio recto; 1, un cuenco. En medio, una vasija." },
    { clave: "intemperie", grupo: "obra", angulo: 150, termino: "Los remates: la intemperie", rombo: "P-02 · 3", min: 0, max: 0.3, paso: 0.005,
      canales: true, menos: "nueva", mas: "gastada", pieza: "*",
      obra: () => PARAM.intemperie.canales, ver: (v, b) => `${coma(v, 3)} c · ${coma(v * b.c / 4)} mm`,
      por: "No hay remates: todas las esquinas se gastan con este radio. «Hoy está muy erosionado y casi no se ven esos detalles» (el pie)." },
    { clave: "gota_masa", grupo: "obra", angulo: 180, termino: "El terminal: la gota", rombo: "P-06 · 2", min: 0.6, max: 2.0, paso: 0.05,
      canales: true, menos: "gota chica", mas: "gota pesada", pieza: "a",
      obra: () => PARAM.gota_masa.canales, ver: (v, b) => `${coma(v, 2)} c · ${coma(v * b.c / 4)} mm`,
      por: "Solo gotea lo que mira abajo: una masa que cae a plomada, por su peso. El líquido que chorrea de la boca (D16).",
      verso: "La tierra se dio de beber a sí misma" },
  ];
  const POR_CLAVE = Object.fromEntries(DECISIONES.map((dd) => [dd.clave, dd]));
  const FORMA = DECISIONES.filter((dd) => dd.grupo === "obra");
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
  /* estado: los valores que se apartan de la obra. dedo: dónde se tocó el agua, en radios de la bandeja
   * ([0, 0] es el desagüe), o null si la forma viene de las decisiones una por una. */
  const GUARDA = "contenida-decisiones-v2";
  let estado = {}, seleccion = "o", dedo = null, abierta = null, viva = null;
  try {
    const g = JSON.parse(localStorage.getItem(GUARDA) || localStorage.getItem("contenida-decisiones-v1") || "{}");
    estado = g.estado || {};
    if (g.seleccion) seleccion = g.seleccion;
    if (Array.isArray(g.dedo)) dedo = g.dedo;
  } catch (e) { estado = {}; }
  function guardar() {
    try { localStorage.setItem(GUARDA, JSON.stringify({ estado, seleccion, dedo })); } catch (e) { /* sin almacenamiento */ }
  }

  /* De las decisiones a los ajustes de la gramática (px, grados, razones). */
  function ajustesDe(est) {
    const aj = {};
    if (est.razon_x !== undefined) aj.razon_x = est.razon_x;
    const pre = G.preparar(D, aj);
    const c = est.canal !== undefined ? est.canal : pre.e.canal;
    for (const dd of DECISIONES) {
      if (est[dd.clave] === undefined || dd.clave === "razon_x") continue;
      aj[dd.clave] = dd.canales ? est[dd.clave] * c : est[dd.clave];
    }
    return aj;
  }

  // ------------------------------------------------------------------ armar: rápido mientras se toca, entero al soltar
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
  /* El signo elegido y las cuatro piezas: unos milisegundos, a cada movimiento del dedo. */
  function armarRapido() {
    preparar();
    for (const s of new Set([seleccion, "o", "l", "n", "a"])) if (G.RECETAS[s]) signos[s] = G.construir(base, D, s);
  }
  /* La caja entera, de a poco: se llena celda por celda sin trabar la página. */
  let tanda = 0;
  function armarCaja() {
    const mia = ++tanda;
    const cola = D.caja.filter((c) => G.RECETAS[c.signo]).map((c) => c.signo);
    $("#caja").style.opacity = "0.55";
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

  // ------------------------------------------------------------------ entre valores y la bandeja
  const rad = (g) => g * Math.PI / 180;
  const dir = (dd) => [Math.sin(rad(dd.angulo)), -Math.cos(rad(dd.angulo))];        // y crece hacia abajo
  const valor = (dd) => (estado[dd.clave] !== undefined ? estado[dd.clave] : dd.obra(base));
  /* t: cuánto se aparta de la obra, de −1 (el extremo «menos») a 1 (el extremo «mas»). La obra no está en el
   * medio del recorrido: cada mitad se escala por su lado. */
  function tDe(dd, v) {
    const o = dd.obra(base);
    if (v >= o) return dd.max === o ? 0 : (v - o) / (dd.max - o);
    return o === dd.min ? 0 : (v - o) / (o - dd.min);
  }
  function vDe(dd, t) {
    const o = dd.obra(base);
    return t >= 0 ? o + t * (dd.max - o) : o + t * (o - dd.min);
  }
  /* El dedo mueve las seis a la vez: cada una, la proyección del punto sobre su línea. */
  function desdeElDedo(p) {
    for (const dd of FORMA) {
      const u = dir(dd), t = clamp(p[0] * u[0] + p[1] * u[1], -1, 1);
      if (Math.abs(t) < 0.005) { delete estado[dd.clave]; continue; }
      estado[dd.clave] = clamp(redondear(vDe(dd, t), dd.paso), dd.min, dd.max);
    }
  }
  /* Y al revés: la coordenada de las seis, (2/n) Σ t·u. Si vinieron del dedo, devuelve el dedo. */
  function coordenada() {
    let x = 0, y = 0;
    for (const dd of FORMA) {
      const t = tDe(dd, valor(dd)), u = dir(dd);
      x += t * u[0];
      y += t * u[1];
    }
    const k = 2 / FORMA.length;
    return [x * k, y * k];
  }

  // ------------------------------------------------------------------ la bandeja
  const C = 320, R = 228;
  const B = $("#bandeja");
  function pintarBandeja() {
    const o = [];
    // la bandeja y un dedo de agua
    o.push(`<rect x="30" y="30" width="580" height="580" rx="22" fill="${PAPEL}" stroke="${TINTA}" stroke-width="1.2"/>`);
    o.push(`<rect x="42" y="42" width="556" height="556" rx="14" fill="${LILA}" fill-opacity="0.13"/>`);
    for (const r of [R / 2, R]) o.push(`<circle cx="${C}" cy="${C}" r="${r}" fill="none" stroke="${GRIS2}" stroke-width="0.8" stroke-dasharray="1.5 5"/>`);
    // las seis líneas, con sus extremos
    for (const dd of FORMA) {
      const [ux, uy] = dir(dd);
      const ext = (s) => [C + s * ux * R, C + s * uy * R];
      const [ax, ay] = ext(-1), [bx, by] = ext(1);
      const marcas = [-1, -0.5, 0.5, 1].map((s) => {
        const [mx, my] = ext(s);
        return `<line x1="${mx - uy * 4}" y1="${my + ux * 4}" x2="${mx + uy * 4}" y2="${my - ux * 4}" stroke="${TINTA}" stroke-width="0.8" stroke-opacity="0.5"/>`;
      }).join("");
      const rotulo = (s, texto) => {
        const lx = C + s * ux * (R + 18), ly = C + s * uy * (R + 18);
        const ax_ = Math.abs(s * ux) < 0.25 ? "middle" : s * ux > 0 ? "start" : "end";
        const dy = s * uy < -0.25 ? -2 : s * uy > 0.25 ? 12 : 4.5;
        return `<text x="${lx.toFixed(1)}" y="${(ly + dy).toFixed(1)}" text-anchor="${ax_}" font-family="Courier Prime, monospace" ` +
          `font-size="14" fill="${TINTA}">${esc(texto)}</text>`;
      };
      o.push(`<g class="eje${viva === dd.clave ? " vivo" : ""}" data-clave="${dd.clave}">` +
        `<line x1="${ax}" y1="${ay}" x2="${bx}" y2="${by}" stroke="${TINTA}" stroke-opacity="0.42" stroke-width="0.9"/>${marcas}` +
        `<line x1="${ax}" y1="${ay}" x2="${bx}" y2="${by}" stroke="transparent" stroke-width="16"/>` +
        rotulo(-1, dd.menos) + rotulo(1, dd.mas) + "</g>");
    }
    // el desagüe: un círculo abierto abajo, en su punto más bajo
    const rd = 8, a0 = rad(90 + 35), a1 = rad(90 - 35 + 360);
    o.push(`<path d="M${C + rd * Math.cos(a0)},${C + rd * Math.sin(a0)} A${rd},${rd} 0 1 1 ${C + rd * Math.cos(a1)},${C + rd * Math.sin(a1)}" ` +
      `fill="none" stroke="${TINTA}" stroke-width="1.6"/>`);
    o.push(`<text x="${C + 9}" y="${C - 22}" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" fill="${GRIS}">la obra</text>`);
    // lo que se aparta de la obra: el punto de cada línea y la forma que hacen, abierta abajo
    const puntos = [];
    for (const dd of FORMA) {
      const t = tDe(dd, valor(dd));
      if (Math.abs(t) < 0.01) continue;
      const [ux, uy] = dir(dd);
      puntos.push({ x: C + t * ux * R, y: C + t * uy * R, clave: dd.clave });
    }
    const p = dedo || coordenada();
    const enReposo = Math.hypot(p[0], p[1]) < 0.01 && !puntos.length;
    if (dedo && Math.hypot(dedo[0], dedo[1]) > 0.01) {
      // el círculo que va del desagüe al dedo: ahí quedan las seis
      o.push(`<circle cx="${C + dedo[0] * R / 2}" cy="${C + dedo[1] * R / 2}" r="${Math.hypot(dedo[0], dedo[1]) * R / 2}" fill="none" stroke="${LILA}" stroke-width="2"/>`);
      o.push(`<line x1="${C}" y1="${C}" x2="${C + dedo[0] * R}" y2="${C + dedo[1] * R}" stroke="${LILA}" stroke-width="1.2" stroke-dasharray="2 4"/>`);
    }
    if (puntos.length >= 2) o.push(formaAbierta(puntos));
    for (const q of puntos) o.push(`<circle cx="${q.x.toFixed(1)}" cy="${q.y.toFixed(1)}" r="${viva === q.clave ? 6 : 4.5}" fill="${VIOLETA}"/>`);
    if (!enReposo) {
      o.push(`<circle cx="${C + p[0] * R}" cy="${C + p[1] * R}" r="15" fill="none" stroke="${VIOLETA}" stroke-width="1"${dedo ? "" : ' stroke-dasharray="2 3"'}/>` +
        `<circle cx="${C + p[0] * R}" cy="${C + p[1] * R}" r="${dedo ? 8 : 5}" fill="${dedo ? VIOLETA : PAPEL}" stroke="${VIOLETA}" stroke-width="1.4"/>`);
    }
    o.push('<g id="ondas"></g>');
    B.innerHTML = o.join("");
  }

  /* La forma de los puntos, por su ángulo alrededor del desagüe, abierta en el punto más bajo. */
  function formaAbierta(puntos) {
    const pp = puntos.slice().sort((a, b) => Math.atan2(a.y - C, a.x - C) - Math.atan2(b.y - C, b.x - C));
    if (pp.length === 2) return `<line x1="${pp[0].x}" y1="${pp[0].y}" x2="${pp[1].x}" y2="${pp[1].y}" stroke="${VIOLETA}" stroke-width="1.6" stroke-dasharray="0.1 5" stroke-linecap="round"/>`;
    let k = 0;
    pp.forEach((q, i) => { if (q.y > pp[k].y) k = i; });
    const n = pp.length, L = pp[k], A = pp[(k - 1 + n) % n], Bq = pp[(k + 1) % n];
    const cerca = (de, a) => { const l = Math.hypot(a.x - de.x, a.y - de.y) || 1, h = Math.min(7, l / 2); return [de.x + (a.x - de.x) * h / l, de.y + (a.y - de.y) * h / l]; };
    const [sx, sy] = cerca(L, Bq), [ex, ey] = cerca(L, A);
    let d = `M${sx.toFixed(1)},${sy.toFixed(1)}`;
    for (let j = 1; j < n; j++) { const q = pp[(k + j) % n]; d += ` L${q.x.toFixed(1)},${q.y.toFixed(1)}`; }
    d += ` L${ex.toFixed(1)},${ey.toFixed(1)}`;
    return `<path d="${d}" fill="none" stroke="${VIOLETA}" stroke-width="1.6" stroke-dasharray="0.1 5" stroke-linecap="round" stroke-linejoin="round"/>`;
  }

  /* Una onda donde se toca el agua. */
  let ultimaOnda = 0;
  function onda(p, forzar) {
    const ahora = performance.now();
    if (!forzar && ahora - ultimaOnda < 140) return;
    ultimaOnda = ahora;
    const g = B.querySelector("#ondas");
    if (!g) return;
    const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    c.setAttribute("class", "onda");
    c.setAttribute("cx", C + p[0] * R);
    c.setAttribute("cy", C + p[1] * R);
    c.setAttribute("r", 6);
    c.addEventListener("animationend", () => c.remove());
    g.appendChild(c);
  }

  function aRadios(ev) {
    const m = B.getScreenCTM();
    if (!m) return [0, 0];
    const pt = new DOMPoint(ev.clientX, ev.clientY).matrixTransform(m.inverse());
    let x = (pt.x - C) / R, y = (pt.y - C) / R;
    const l = Math.hypot(x, y);
    if (l > 1) { x /= l; y /= l; }
    if (l < 0.045) { x = 0; y = 0; }                  // cerca del desagüe, el agua se aquieta
    return [x, y];
  }

  let tocando = false;
  function tocar(p, forzar) {
    dedo = p;
    desdeElDedo(p);
    pedir(false);
    const ondas = B.querySelector("#ondas");
    requestAnimationFrame(() => onda(p, forzar || !ondas));
  }
  B.addEventListener("pointerdown", (ev) => {
    const eje = ev.target.closest(".eje");
    if (eje && ev.target.tagName === "text") { abrir(eje.dataset.clave, true); return; }
    ev.preventDefault();
    B.focus({ preventScroll: true });
    B.setPointerCapture(ev.pointerId);
    tocando = true;
    detenerVuelta();
    tocar(aRadios(ev), true);
  });
  B.addEventListener("pointermove", (ev) => {
    if (tocando) { tocar(aRadios(ev)); return; }
    const eje = ev.target.closest(".eje");
    marcarViva(eje ? eje.dataset.clave : null);
  });
  const soltar = () => { if (!tocando) return; tocando = false; asentar(); };
  B.addEventListener("pointerup", soltar);
  B.addEventListener("pointercancel", soltar);
  B.addEventListener("pointerleave", () => { if (!tocando) marcarViva(null); });
  B.addEventListener("keydown", (ev) => {
    const paso = ev.shiftKey ? 0.2 : 0.05;
    const p = (dedo || coordenada()).slice();
    if (ev.key === "ArrowLeft") p[0] -= paso;
    else if (ev.key === "ArrowRight") p[0] += paso;
    else if (ev.key === "ArrowUp") p[1] -= paso;
    else if (ev.key === "ArrowDown") p[1] += paso;
    else if (ev.key === "Escape" || ev.key === "Home") { ev.preventDefault(); aquietar(); return; }
    else return;
    ev.preventDefault();
    const l = Math.hypot(p[0], p[1]);
    if (l > 1) { p[0] /= l; p[1] /= l; }
    tocar(p, true);
    clearTimeout(B._t);
    B._t = setTimeout(asentar, 250);
  });

  /* Dejar quieta el agua: el dedo vuelve al desagüe y la forma, a la obra. Las medidas del pie no cambian. */
  let vuelta = null;
  function detenerVuelta() { if (vuelta) { cancelAnimationFrame(vuelta); vuelta = null; } }
  function aquietar() {
    detenerVuelta();
    const p0 = dedo || coordenada(), t0 = performance.now(), dur = 520;
    const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const paso = (ahora) => {
      const k = quieto ? 1 : Math.min(1, (ahora - t0) / dur), e = 1 - (1 - k) ** 3;
      const p = [p0[0] * (1 - e), p0[1] * (1 - e)];
      dedo = p;
      desdeElDedo(p);
      armarRapido();
      pintarTodo();
      if (k < 1) vuelta = requestAnimationFrame(paso);
      else { vuelta = null; dedo = null; for (const dd of FORMA) delete estado[dd.clave]; asentar(); nota("El agua quedó quieta: la forma es la de la obra."); }
    };
    vuelta = requestAnimationFrame(paso);
  }

  // ------------------------------------------------------------------ las decisiones, una por una
  const X0 = 12, X1 = 388;
  const xDe = (dd, v) => X0 + (X1 - X0) * (v - dd.min) / (dd.max - dd.min);
  function pistaSVG(dd) {
    const v = valor(dd), o = dd.obra(base), ajustada = estado[dd.clave] !== undefined;
    const xv = xDe(dd, v), xo = xDe(dd, o);
    return `<svg viewBox="0 0 400 38" aria-hidden="true">` +
      `<line x1="${X0}" y1="14" x2="${X1}" y2="14" stroke="${FILETE}" stroke-width="2"/>` +
      `<line x1="${X0}" y1="9" x2="${X0}" y2="19" stroke="${GRIS2}" stroke-width="1"/><line x1="${X1}" y1="9" x2="${X1}" y2="19" stroke="${GRIS2}" stroke-width="1"/>` +
      `<line x1="${xo}" y1="5" x2="${xo}" y2="23" stroke="${TINTA}" stroke-width="1.6"/>` +
      (ajustada ? `<line x1="${xo}" y1="14" x2="${xv}" y2="14" stroke="${VIOLETA}" stroke-width="2.4" stroke-dasharray="0.1 5" stroke-linecap="round"/>` : "") +
      `<circle cx="${xv}" cy="14" r="7" fill="${ajustada ? VIOLETA : TINTA}"/>` +
      `<text x="${X0}" y="35" font-family="Courier Prime, monospace" font-size="12" fill="${GRIS}">${esc(dd.menos)}</text>` +
      `<text x="${X1}" y="35" text-anchor="end" font-family="Courier Prime, monospace" font-size="12" fill="${GRIS}">${esc(dd.mas)}</text>` +
      `<text x="${clamp(xo, X0 + 40, X1 - 40)}" y="35" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" fill="${TINTA}">la obra</text>` +
      `</svg>`;
  }

  function armarDecisiones() {
    const fila = (dd) => `
      <div class="decision" id="d-${dd.clave}" data-clave="${dd.clave}">
        <div class="fila">
          <button class="nombre" type="button" aria-expanded="false" aria-controls="por-${dd.clave}"><span class="rombo">${esc(dd.rombo)}</span>${esc(dd.termino)}</button>
          <span class="valor" id="v-${dd.clave}"></span>
        </div>
        <div class="pista" id="p-${dd.clave}" role="slider" tabindex="0" aria-label="${esc(dd.termino)}"
             aria-valuemin="${dd.min}" aria-valuemax="${dd.max}"></div>
        <button class="volver" type="button" data-volver="${dd.clave}" hidden>volver a la obra</button>
        <div id="por-${dd.clave}" hidden>
          <p class="por-que">${esc(dd.por)}</p>
          ${dd.verso ? `<p class="verso">«${esc(dd.verso)}»</p>` : ""}
          ${dd.clave === "intemperie" ? '<p class="aviso" id="aviso-intemperie" hidden>Con más de 0,175 c, las cifras pierden su celda: el desgaste se come el trazo de 0,35 c.</p>' : ""}
        </div>
      </div>`;
    $("#g-pie").innerHTML = DECISIONES.filter((dd) => dd.grupo === "pie").map(fila).join("");
    $("#g-obra").innerHTML = FORMA.map(fila).join("");
    $("#fijas").innerHTML = FIJAS.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("");

    for (const dd of DECISIONES) {
      const pista = $("#p-" + dd.clave);
      let arrastre = false;
      const fijar = (ev) => {
        const r = pista.getBoundingClientRect();
        const x = (ev.clientX - r.left) / r.width * 400;
        const v = clamp(redondear(dd.min + (x - X0) / (X1 - X0) * (dd.max - dd.min), dd.paso), dd.min, dd.max);
        poner(dd, v, false);
      };
      pista.addEventListener("pointerdown", (ev) => { ev.preventDefault(); pista.focus({ preventScroll: true }); pista.setPointerCapture(ev.pointerId); arrastre = true; fijar(ev); });
      pista.addEventListener("pointermove", (ev) => { if (arrastre) fijar(ev); });
      const fin = () => { if (arrastre) { arrastre = false; asentar(); } };
      pista.addEventListener("pointerup", fin);
      pista.addEventListener("pointercancel", fin);
      pista.addEventListener("keydown", (ev) => {
        const v = valor(dd), k = ev.shiftKey ? 10 : 1;
        let n = null;
        if (ev.key === "ArrowRight" || ev.key === "ArrowUp") n = v + dd.paso * k;
        else if (ev.key === "ArrowLeft" || ev.key === "ArrowDown") n = v - dd.paso * k;
        else if (ev.key === "Home") n = dd.min;
        else if (ev.key === "End") n = dd.max;
        else if (ev.key === "Delete" || ev.key === "Backspace" || ev.key === "Escape") { ev.preventDefault(); volver(dd); return; }
        if (n === null) return;
        ev.preventDefault();
        poner(dd, clamp(redondear(n, dd.paso), dd.min, dd.max), true);
      });
      const caja = $("#d-" + dd.clave);
      caja.addEventListener("pointerenter", () => marcarViva(dd.clave));
      caja.addEventListener("pointerleave", () => marcarViva(null));
      caja.querySelector(".nombre").addEventListener("click", () => abrir(dd.clave, false));
      caja.querySelector("[data-volver]").addEventListener("click", () => volver(dd));
    }
  }

  function poner(dd, v, alFinal) {
    if (Math.abs(v - dd.obra(base)) < dd.paso / 2) delete estado[dd.clave];
    else estado[dd.clave] = v;
    if (dd.grupo === "obra") dedo = null;                // una por una: la forma ya no es la del dedo
    pedir(false);
    if (alFinal) { clearTimeout(poner._t); poner._t = setTimeout(asentar, 250); }
  }
  function volver(dd) {
    delete estado[dd.clave];
    if (dd.grupo === "obra") dedo = null;
    pedir(false);
    asentar();
  }
  function abrir(clave, desdeLaBandeja) {
    abierta = abierta === clave && !desdeLaBandeja ? null : clave;
    for (const dd of DECISIONES) {
      const a = abierta === dd.clave;
      $("#por-" + dd.clave).hidden = !a;
      $(`#d-${dd.clave} .nombre`).setAttribute("aria-expanded", String(a));
    }
    if (desdeLaBandeja && abierta) $("#d-" + clave).scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
  function marcarViva(clave) {
    if (viva === clave) return;
    viva = clave;
    for (const dd of DECISIONES) $("#d-" + dd.clave).classList.toggle("viva", viva === dd.clave);
    pintarBandeja();
    pintarPiezas();
  }

  function pintarDecisiones() {
    for (const dd of DECISIONES) {
      const v = valor(dd), ajustada = estado[dd.clave] !== undefined;
      $("#p-" + dd.clave).innerHTML = pistaSVG(dd);
      const pista = $("#p-" + dd.clave);
      pista.setAttribute("aria-valuenow", String(+v.toFixed(4)));
      pista.setAttribute("aria-valuetext", dd.ver(v, base) + (ajustada ? "" : ", la obra"));
      $("#v-" + dd.clave).textContent = dd.ver(v, base);
      $("#d-" + dd.clave).classList.toggle("ajustada", ajustada);
      $(`[data-volver="${dd.clave}"]`).hidden = !ajustada;
    }
    const intem = valor(POR_CLAVE.intemperie);
    $("#aviso-intemperie").hidden = intem <= 0.175;
  }

  // ------------------------------------------------------------------ el plano
  const d = (anillos) => anillos.map((a) => "M" + a.map(([x, y]) => x.toFixed(1) + "," + y.toFixed(1)).join(" L") + "Z").join(" ");
  const nivel = (y) => { const u = Math.round((base.e.fondo - y) * base.U); return u === 0 ? "±0" : (u > 0 ? "+" : "−") + Math.abs(u); };
  const mmU = (px) => `${coma(px / 4)} (${Math.round(px * base.U)})`;

  function cota(x0, x1, y, texto) {
    const t = (x) => `<line x1="${x - 5}" y1="${y + 5}" x2="${x + 5}" y2="${y - 5}" stroke="${TINTA}" stroke-width="1.6"/>`;
    return `<line x1="${x0 - 6}" y1="${y}" x2="${x1 + 6}" y2="${y}" stroke="${TINTA}" stroke-width="0.8"/>${t(x0)}${t(x1)}` +
      `<text x="${(x0 + x1) / 2}" y="${y - 5}" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" ` +
      `fill="${TINTA}" paint-order="stroke" stroke="${PAPEL}" stroke-width="3">${esc(texto)}</text>`;
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
        `<text x="${xn + 10}" y="${y - 3}" font-family="Courier Prime, monospace" font-size="13" fill="${TINTA}">${nivel(y)}</text>`);
    }
    o.push(`<text x="${cx1 + 40}" y="${cy0 - 8}" font-family="Courier Prime, monospace" font-size="11" fill="${GRIS}">NIVELES (UPM)</text>`);
    // el cuerpo
    o.push(`<path d="${d(r.geo)}" fill="url(#metal)" fill-rule="evenodd" stroke="${rec ? VIOLETA : TINTA}" ` +
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
    o.push(cota(cx0, x0, yc, coma((x0 - cx0) / 4)));
    o.push(cota(x0, x1, yc, mmU(x1 - x0)));
    o.push(cota(x1, cx1, yc, coma((cx1 - x1) / 4)));
    o.push(cota(cx0, cx1, yc + 24, `celda ${mmU(cx1 - cx0)} · avance`));
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
      ["sube hasta", nivel(y0) + " UPM"], ["baja hasta", nivel(y1) + " UPM"], ["canal", mmU(base.c)],
      ["partes", partes || "—"],
    ];
    $("#p-medidas").innerHTML = filas.map(([k, v]) => `<li><span>${esc(k)}</span>${esc(v)}</li>`).join("");
  }

  // ------------------------------------------------------------------ las cuatro piezas
  function pintarPiezas() {
    const de = viva ? POR_CLAVE[viva].pieza : null;
    $("#piezas").innerHTML = PIEZAS.map(([s, nombre]) => {
      const r = signos[s];
      const vivaP = de && (de === "*" || de === s);
      return `<figure class="pieza${vivaP ? " viva" : ""}" data-s="${s}"><svg viewBox="0 0 150 150" role="img" aria-label="${esc(nombre)}">` +
        `<rect width="150" height="150" fill="${PAPEL}"/>` +
        (r ? `<path transform="scale(0.25)" d="${d(r.geo)}" fill="${vivaP ? VIOLETA : TINTA}" fill-rule="evenodd"/>` : "") +
        `</svg><figcaption>${esc(s)} · ${esc(nombre)}</figcaption></figure>`;
    }).join("");
  }
  $("#piezas").addEventListener("click", (ev) => {
    const f = ev.target.closest(".pieza");
    if (!f) return;
    elegir(f.dataset.s);
  });

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
        o.push(`<path transform="scale(0.25)" d="${d(r.geo)}" fill="${rec ? VIOLETA : TINTA}" fill-rule="evenodd" ${rec ? 'fill-opacity="0.85"' : ""}/>`);
        o.push(`<text x="144" y="16" text-anchor="end" font-family="Newsreader, serif" font-style="italic" font-size="14" fill="${GRIS2}">${familia(c.signo)}</text>`);
      } else if (!G.RECETAS[c.signo]) {
        o.push(`<text x="75" y="88" text-anchor="middle" font-family="Newsreader, serif" font-size="56" fill="${GRIS2}">¶</text>` +
          `<text x="75" y="134" text-anchor="middle" font-family="Courier Prime, monospace" font-size="12" fill="${GRIS}">con los dedos</text>`);
      }
      o.push("</g>");
    }
    $("#caja").innerHTML = o.join("");
  }
  function elegir(s) {
    if (!G.RECETAS[s]) return;
    seleccion = s;
    if (!signos[s]) signos[s] = G.construir(base, D, s);
    guardar();
    pintarCaja();
    pintarPlano();
  }
  $("#caja").addEventListener("click", (ev) => {
    const g = ev.target.closest(".celda");
    if (!g || g.getAttribute("aria-disabled")) return;
    elegir(g.dataset.s);
  });

  // ------------------------------------------------------------------ armar y pintar, sin trabarse
  function pintarTodo() {
    pintarBandeja();
    pintarDecisiones();
    pintarPlano();
    pintarPiezas();
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
    guardar();
    armarRapido();
    pintarTodo();
    armarCaja();
    const movidas = FORMA.filter((dd) => estado[dd.clave] !== undefined)
      .map((dd) => `${tDe(dd, valor(dd)) > 0 ? dd.mas : dd.menos} ${dd.ver(valor(dd), base)}`);
    $("#anuncio").textContent = movidas.length ? "La forma: " + movidas.join("; ") + "." : "La forma es la de la obra.";
  }

  // ------------------------------------------------------------------ las salidas
  function nota(texto) { const n = $("#nota"); n.textContent = texto; clearTimeout(n._t); n._t = setTimeout(() => { n.textContent = ""; }, 6000); }
  /* Fuera de claude.ai, la descarga es un enlace. Dentro del visor los enlaces de descarga no hacen nada:
   * se usa la capacidad «downloads», y si no está, el texto se copia y queda a la vista para guardarlo a mano. */
  const enVisor = !!(window.claude && typeof window.claude.use === "function");
  let descargas = null;
  if (enVisor) window.claude.use("downloads").then((dd) => { descargas = dd; }, () => {});
  function aMano(nombre, texto) {
    $("#salida").hidden = false;
    const t = $("#salida-texto");
    t.value = texto;
    t.focus();
    t.select();
    if (navigator.clipboard) navigator.clipboard.writeText(texto).then(() => nota(`${nombre}: copiado.`), () => {});
  }
  async function bajar(nombre, tipo, texto) {
    if (descargas) {
      try { await descargas.save({ filename: nombre, data: texto }); nota(`${nombre}: guardado.`); }
      catch (e) {
        if (e && e.code === "declined") nota("Descarga cancelada.");
        else aMano(nombre, texto);
      }
      return false;
    }
    if (enVisor) { aMano(nombre, texto); return false; }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([texto], { type: tipo }));
    a.download = nombre;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    return true;
  }
  $("#a-obra").addEventListener("click", aquietar);
  $("#a-json").addEventListener("click", () => {
    const aj = ajustesDe(estado), valores = { razon_x: +base.razon.toFixed(4) };
    for (const [k, p] of Object.entries(base.P)) valores[k] = +(+p.valor).toFixed(3);
    const texto = JSON.stringify({
      contenida: "parámetros de la gramática",
      fecha: new Date().toISOString().slice(0, 10),
      uso: "python3 tipografia/simulacion/gramatica.py --parametros parametros.json",
      ajustes: Object.fromEntries(Object.entries(aj).map(([k, v]) => [k, +(+v).toFixed(4)])),
      valores,
      bandeja: dedo ? dedo.map((v) => +v.toFixed(3)) : null,
    }, null, 1);
    bajar("parametros.json", "application/json", texto + "\n").then((hecho) => {
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
  armarDecisiones();
  if (!G.RECETAS[seleccion]) seleccion = "o";
  armarRapido();
  pintarTodo();
  pintarCaja();
  armarCaja();
})();
