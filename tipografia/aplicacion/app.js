/* Las decisiones de la letra: una sola mesa.
 *
 * A la izquierda, el plano del signo elegido: la celda con sus cuatro líneas, el cuerpo, los ejes,
 * los nodos, los alivios y las partes, con sus medidas en milímetros de la placa y en unidades de
 * la fuente. A la derecha, las nueve decisiones de anatomía que la mano puede discutir, cada una con
 * su porqué y el rombo de su plano (tipografia/planos/). Abajo, la caja, para elegir el signo.
 *
 * El motor es gramatica.js (la gramática de Python, portada): no se toca aquí.
 */
(function () {
  "use strict";
  const D = window.DATOS, G = window.Gramatica;
  const T = D.T;
  const $ = (s) => document.querySelector(s);
  const TINTA = "#1d1c1a", VIOLETA = "#4a2470", GRIS = "#6d6a63", GRIS2 = "#9a968d", PAPEL = "#f6f4ee", FILETE = "#cfcac0";
  const FAMILIA = { o: "oecdbpqóéá0689", l: "litjfkí()147", n: "nmhuúürvwxyzñ235", a: "a,sg.?;:¿«»—…" };
  const NOMBRE_GEN = { o: "la cuenca (o)", l: "el fuste (l)", n: "el hombro (n)", a: "el gancho y la gota (a)" };
  const familia = (s) => Object.keys(FAMILIA).find((g) => FAMILIA[g].includes(s)) || "a";
  const PARAM = Object.fromEntries(D.parametros.map((p) => [p.nombre, p]));
  const coma = (v, d = 1) => (Math.round(v * 10 ** d) / 10 ** d).toFixed(d).replace(".", ",").replace(/^-/, "−");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  // ------------------------------------------------------------------ las nueve decisiones
  /* tipo: "directo" se guarda tal cual; "canales" se guarda en canales y se pasa a px con el canal del momento. */
  const DECISIONES = [
    { clave: "razon_x", termino: "La altura de x", rombo: "P-01 · 4", min: 1.4, max: 2.0, paso: 0.01,
      obra: () => D.razon_foto, ver: (v) => coma(v, 2) + " de las ascendentes",
      por: "Las ascendentes miden 1,71 veces la altura de x: es la única proporción que se toma de la foto del pie real. El testigo sustituto daba 1,52." },
    { clave: "canal", termino: "El contraste: ninguno", rombo: "P-02 · 1", min: 20, max: 60, paso: 0.5,
      obra: (b) => b.base.e.canal, ver: (v, b) => `canal ${coma(v / 4)} mm (${Math.round(v * b.U)})`,
      por: "Un solo grosor en todo el recorrido: el punzón y la cinta no modulan (D2, D12). Sale de la o del pie: la media entre su grueso y su fino.",
      verso: "Desenterrar una voz / es desenterrar la mano del que la escribió." },
    { clave: "trapecio", termino: "La panza: el fondo plano", rombo: "P-03 · 2", min: 0.4, max: 1.0, paso: 0.01,
      obra: () => PARAM.trapecio.fijo, ver: (v) => coma(v, 2) + " del ancho mayor",
      por: "Cada cuenca baja hasta un fondo plano: el trapecio con que la proyección llega a la pared (D8), la piscina vacía (D6).",
      verso: "Una piscina vacía, / donde una vez aprendí a flotar, / ahora aprendo a mirar." },
    { clave: "pared", termino: "La panza: la pared", rombo: "P-03 · 2", min: 0, max: 1, paso: 0.01,
      obra: () => PARAM.pared.fijo, ver: (v) => coma(v, 2),
      por: "Cuánto se abomba la pared al bajar: 0 es el trapecio recto; 1, un cuenco. En medio, una vasija." },
    { clave: "hombro", termino: "El hombro: la tensión", rombo: "P-05 · 1", min: 2, max: 5, paso: 0.05,
      obra: () => PARAM.hombro.fijo, ver: (v) => "n = " + coma(v, 2),
      por: "El arco es una superelipse, no una elipse (n = 2): la chapa de aluminio doblada a la fuerza sobre un hombro (D3).",
      verso: "Es lo más parecido a estar viva / que puede hacer una imagen." },
    { clave: "hombro_caida", termino: "El hombro: dónde arranca", rombo: "P-05 · 3", min: 0.15, max: 0.7, paso: 0.01,
      obra: () => PARAM.hombro_caida.fijo, ver: (v) => coma(v, 2) + " del borde al fondo",
      por: "Dónde el arco se vuelve vertical. Se tomó a ojo del testigo de la n: es la medida más débil, y falta medirla en el libro." },
    { clave: "quiebre", termino: "El asta: el quiebre", rombo: "P-04 · 1", min: 0, max: 6, paso: 0.1,
      obra: () => PARAM.quiebre.fijo, ver: (v) => coma(v, 1) + "° por plano",
      por: "El asta tiene tres planos, como la placa que cambia de plano al apoyarse en el cuerpo (D3). Cada uno se aparta del eje apenas (D11).",
      verso: "Moverse como se mueve la piedra, / es decir, apenas, es decir, temblor," },
    { clave: "intemperie", termino: "Los remates: la intemperie", rombo: "P-02 · 3", min: 0, max: 0.3, paso: 0.005, canales: true,
      obra: () => PARAM.intemperie.canales, ver: (v, b) => `${coma(v, 3)} c · ${coma(v * b.c / 4)} mm`,
      por: "No hay remates: todas las esquinas se gastan con este radio. «Hoy está muy erosionado y casi no se ven esos detalles» (el pie)." },
    { clave: "gota_masa", termino: "El terminal: la gota", rombo: "P-06 · 2", min: 0.6, max: 2.0, paso: 0.05, canales: true,
      obra: () => PARAM.gota_masa.canales, ver: (v, b) => `${coma(v, 2)} c · ${coma(v * b.c / 4)} mm`,
      por: "Solo gotea lo que mira abajo: una masa que cae a plomada, por su peso. El líquido que chorrea de la boca (D16).",
      verso: "La tierra se dio de beber a sí misma" },
  ];
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

  let base = null, todo = null;
  function armar(todos) {
    const aj = ajustesDe(estado);
    base = G.preparar(D, aj);
    const [, y0, , y1] = G.celda(base.e, T);
    base.U = 1000 / (y1 - y0);
    base.c = base.e.canal;
    base.base = G.preparar(D, estado.razon_x !== undefined ? { razon_x: estado.razon_x } : {});
    if (todos || !todo) todo = G.construirTodo(D, aj);
    else todo.signos[seleccion] = G.construir(base, D, seleccion);
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
    const r = todo.signos[seleccion];
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

  // ------------------------------------------------------------------ las decisiones
  function armarDecisiones() {
    $("#decisiones").innerHTML = DECISIONES.map((dd, i) => `
      <div class="decision" id="d-${dd.clave}">
        <div class="linea"><span class="rombo">${esc(dd.rombo)}</span><label for="r-${dd.clave}">${esc(dd.termino)}</label></div>
        <div class="linea"><span class="valor" id="v-${dd.clave}"></span>
          <button class="volver" type="button" data-volver="${dd.clave}" hidden>volver a la obra</button></div>
        <input type="range" id="r-${dd.clave}" min="${dd.min}" max="${dd.max}" step="${dd.paso}" data-i="${i}">
        <p class="por-que">${esc(dd.por)}</p>
        ${dd.verso ? `<p class="verso">«${esc(dd.verso)}»</p>` : ""}
        ${dd.clave === "intemperie" ? '<p class="aviso" id="aviso-intemperie" hidden>Con más de 0,175 c, las cifras pierden su celda: el desgaste se come el trazo de 0,35 c.</p>' : ""}
      </div>`).join("");
    $("#fijas").innerHTML = FIJAS.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("");
    for (const r of document.querySelectorAll("#decisiones input[type=range]")) {
      r.addEventListener("input", () => { const dd = DECISIONES[+r.dataset.i]; estado[dd.clave] = +r.value; pedir(false); });
      r.addEventListener("change", () => pedir(true));
    }
    for (const b of document.querySelectorAll("[data-volver]")) {
      b.addEventListener("click", () => { delete estado[b.dataset.volver]; pedir(true); });
    }
  }

  function pintarDecisiones() {
    for (const dd of DECISIONES) {
      const v = estado[dd.clave] !== undefined ? estado[dd.clave] : dd.obra(base);
      $("#r-" + dd.clave).value = v;
      $("#v-" + dd.clave).textContent = dd.ver(v, base);
      const ajustada = estado[dd.clave] !== undefined;
      $("#d-" + dd.clave).classList.toggle("ajustada", ajustada);
      $(`[data-volver="${dd.clave}"]`).hidden = !ajustada;
    }
    const intem = estado.intemperie !== undefined ? estado.intemperie : PARAM.intemperie.canales;
    $("#aviso-intemperie").hidden = intem <= 0.175;
  }

  // ------------------------------------------------------------------ la caja
  function pintarCaja() {
    const o = [];
    for (const c of D.caja) {
      const x = (c.columna - 1) * 153, y = (c.fila - 1) * 153;
      const r = todo.signos[c.signo];
      const rec = c.estado === "reconstruida", sel = c.signo === seleccion;
      o.push(`<g class="celda" data-s="${esc(c.signo)}" transform="translate(${x} ${y})" ${r ? "" : 'aria-disabled="true"'}>` +
        `<rect class="fondo" width="150" height="150" fill="${PAPEL}" stroke="${sel ? VIOLETA : FILETE}" stroke-width="${sel ? 4 : 1}"/>` +
        `<text x="6" y="16" font-family="Courier Prime, monospace" font-size="13" fill="${rec ? VIOLETA : GRIS}">${c.celda}</text>`);
      if (r) {
        o.push(`<path transform="scale(0.25)" d="${d(r.geo)}" fill="${rec ? VIOLETA : TINTA}" fill-rule="evenodd" ${rec ? 'fill-opacity="0.85"' : ""}/>`);
        o.push(`<text x="144" y="16" text-anchor="end" font-family="Newsreader, serif" font-style="italic" font-size="14" fill="${GRIS2}">${familia(c.signo)}</text>`);
      } else {
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
    guardar();
    pintarCaja();
    pintarPlano();
  });

  // ------------------------------------------------------------------ armar y pintar, sin trabarse
  let pedido = null, todos = false;
  function pedir(completo) {
    todos = todos || completo;
    if (pedido) return;
    pedido = requestAnimationFrame(() => {
      pedido = null;
      const t = todos;
      todos = false;
      armar(t);
      pintarDecisiones();
      pintarPlano();
      if (t) pintarCaja();
      guardar();
    });
  }

  // ------------------------------------------------------------------ las salidas
  function nota(texto) { const n = $("#nota"); n.textContent = texto; clearTimeout(n._t); n._t = setTimeout(() => { n.textContent = ""; }, 6000); }
  /* Fuera de claude.ai, la descarga es un enlace. Dentro del visor los enlaces de descarga no hacen nada:
   * se usa la capacidad «downloads», y si no está, el texto se copia y queda a la vista para guardarlo a mano. */
  const enVisor = !!(window.claude && typeof window.claude.use === "function");
  let descargas = null;
  if (enVisor) window.claude.use("downloads").then((d) => { descargas = d; }, () => {});
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
  $("#a-obra").addEventListener("click", () => { estado = {}; pedir(true); nota("Volvió a la propuesta de la obra."); });
  $("#a-json").addEventListener("click", () => {
    const aj = ajustesDe(estado), valores = { razon_x: +base.razon.toFixed(4) };
    for (const [k, p] of Object.entries(base.P)) valores[k] = +(+p.valor).toFixed(3);
    const texto = JSON.stringify({
      contenida: "parámetros de la gramática",
      fecha: new Date().toISOString().slice(0, 10),
      uso: "python3 tipografia/simulacion/gramatica.py --parametros parametros.json",
      ajustes: Object.fromEntries(Object.entries(aj).map(([k, v]) => [k, +(+v).toFixed(4)])),
      valores,
    }, null, 1);
    bajar("parametros.json", "application/json", texto + "\n").then((hecho) => {
      if (hecho) nota(Object.keys(aj).length ? "parametros.json: solo van los ajustes." : "Sin ajustes: es la propuesta de la obra.");
    });
  });
  $("#a-svg").addEventListener("click", () => {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-110 -30 830 700" width="207.5mm" height="175mm">` +
      `<title>Contenida · ${esc(seleccion)} · plano</title>${svgPlano(todo.signos[seleccion])}</svg>\n`;
    bajar(`contenida_plano_${seleccion.codePointAt(0).toString(16)}.svg`, "image/svg+xml", svg).then((hecho) => {
      if (hecho) nota("El plano, a escala: 4 px del lienzo son 1 mm de la placa.");
    });
  });

  // ------------------------------------------------------------------ arrancar
  if (!todo) {
    armarDecisiones();
    armar(true);
    if (!todo.signos[seleccion]) seleccion = "o";
    pintarDecisiones();
    pintarPlano();
    pintarCaja();
  }
})();
