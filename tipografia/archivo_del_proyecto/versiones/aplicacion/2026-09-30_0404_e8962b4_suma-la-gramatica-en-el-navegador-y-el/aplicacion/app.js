/* La aplicación: la ficha de parámetros, la caja, el signo, el texto y los estados. */
(function () {
  "use strict";
  const D = window.DATOS, G = window.Gramatica, S = window.Simuladores;
  const T = D.T;
  const $ = (s) => document.querySelector(s);
  const coma = (v, d = 1) => Number(v).toFixed(d).replace(".", ",");
  const COLOR = {
    papel: "#f3f1ea", tinta: "#1d1c1a", violeta: "#4a2470", gris: "#6d6a63", gris2: "#9a968d", filete: "#cfcac0",
    junta: "#a8a49a", testigo: "#d9d5ca", lila: "#b9a6d6",
  };
  const POR_SIGNO = Object.fromEntries(D.caja.map((c) => [c.signo, c]));
  const SIGNOS = D.caja.filter((c) => G.RECETAS[c.signo]).map((c) => c.signo);
  const VERSOS = D.poema.toLowerCase().split("\n").filter((v) => v.trim());
  const leer = (k, def) => { try { const v = localStorage.getItem("contenida." + k); return v === null ? def : JSON.parse(v); } catch (e) { return def; } };
  const guardar = (k, v) => { try { localStorage.setItem("contenida." + k, JSON.stringify(v)); } catch (e) { /* sin almacenamiento */ } };
  const respiro = () => new Promise((r) => requestAnimationFrame(() => setTimeout(r, 0)));

  // ------------------------------------------------------------------ los parámetros
  const RAZON = {
    nombre: "razon_x", unidad: "",
    que: "Cuánto mide la ascendente sobre la altura de x. La base y la línea de afuera no se mueven: la zona de x se achata o se estira, y las ascendentes con ella.",
    de_donde: "La foto del pie: ascendentes de 20 px sobre una altura de x de 11,67 px (1,71). El sustituto impreso da 1,52.",
  };
  const META = Object.fromEntries([RAZON, ...D.parametros].map((p) => [p.nombre, p]));
  const ETIQUETA = {
    razon_x: "Ascendente sobre x", canal: "Canal", radio_chapa: "Radio de la chapa", trapecio: "Trapecio", pared: "Pared",
    desague: "Desagüe", hombro: "Hombro", hombro_caida: "Caída del hombro", facetas: "Facetas", quiebre: "Quiebre",
    asiento_ancho: "Ancho del asiento", asiento_alto: "Alto del asiento", intemperie: "Intemperie", alivio: "Alivio",
    gancho_fin: "Fin del gancho", gota_masa: "Masa de la gota", gota_caida: "Caída de la gota", gota_cuello: "Cuello de la gota",
    sifon: "Sifón", cinta: "Cinta", punto: "Punto",
  };
  const GRUPOS = [
    ["Del pie", ["razon_x", "canal"], true],
    ["Cuenca", ["trapecio", "pared", "desague", "sifon"], true],
    ["Hombro y gancho", ["hombro", "hombro_caida", "gancho_fin"], false],
    ["Fuste", ["facetas", "quiebre", "asiento_ancho", "asiento_alto"], false],
    ["Chapa", ["radio_chapa", "alivio", "intemperie"], false],
    ["Gota", ["gota_masa", "gota_caida", "gota_cuello"], false],
    ["Cinta", ["cinta", "punto"], false],
  ];
  const RANGO = {
    razon_x: [1.35, 2.0, 0.005], canal: [16, 56, 0.1], radio_chapa: [0, 50, 0.1], trapecio: [0.3, 1, 0.01], pared: [0, 1, 0.01],
    desague: [0, 30, 0.5], hombro: [1.5, 6, 0.05], hombro_caida: [0.1, 0.8, 0.01], facetas: [1, 6, 1], quiebre: [0, 6, 0.1],
    asiento_ancho: [0, 120, 0.5], asiento_alto: [0, 80, 0.5], intemperie: [0, 12, 0.1], alivio: [0, 25, 0.1],
    gancho_fin: [60, 160, 1], gota_masa: [10, 80, 0.5], gota_caida: [0, 40, 0.5], gota_cuello: [4, 50, 0.5], sifon: [0.2, 1, 0.01],
    cinta: [16, 60, 0.5], punto: [10, 60, 0.5],
  };
  const decimales = (k) => { const p = RANGO[k][2]; return p >= 1 ? 0 : p >= 0.1 ? 1 : p >= 0.01 ? 2 : 3; };

  let ajustes = limpiar(leer("ajustes", {}));
  function limpiar(a) {
    const o = {};
    if (a && typeof a === "object") for (const [k, v] of Object.entries(a)) if (META[k] && Number.isFinite(+v)) o[k] = +v;
    return o;
  }

  // ------------------------------------------------------------------ el modelo: se arma a pedido
  let modelo = null, firma = null, generacion = 0;
  function asegurar() {
    const f = JSON.stringify(ajustes);
    if (f !== firma) {
      firma = f;
      generacion++;
      modelo = { base: G.preparar(D, ajustes), signos: {}, gen: generacion };
    }
    return modelo;
  }
  function armado(s) {
    const m = asegurar();
    if (!m.signos[s]) {
      let r;
      try {
        r = G.construir(m.base, D, s);
        const [x0, y0, x1, y1] = G.limites(r.geo);
        if (!r.geo.length || ![x0, y0, x1, y1].every(Number.isFinite)) throw new Error("el cuerpo quedó vacío");
      } catch (e) {
        r = { signo: s, error: "no se pudo armar con estos parámetros" };
      }
      m.signos[s] = r;
    }
    return m.signos[s];
  }
  const valor = (k) => (k === "razon_x" ? asegurar().base.razon : asegurar().base.P[k].valor);
  const porDefecto = (k) => {
    if (k === "razon_x") return D.razon_foto;
    // el valor de la obra: con la altura de x y el canal que haya, salvo que se pregunte por el canal mismo
    const b = G.preparar(D, Object.fromEntries(Object.entries(ajustes).filter(([n]) => n === "razon_x" || (n === "canal" && k !== "canal"))));
    return b.P[k].porDefecto;
  };

  // ------------------------------------------------------------------ la ficha
  const controles = {};
  function armarFicha() {
    const cont = $("#grupos");
    for (const [titulo, nombres, abierto] of GRUPOS) {
      const det = document.createElement("details");
      det.className = "grupo";
      det.open = leer("grupo." + titulo, abierto);
      det.addEventListener("toggle", () => guardar("grupo." + titulo, det.open));
      const sum = document.createElement("summary");
      sum.innerHTML = `<span>${titulo}</span><span class="cuenta"></span>`;
      det.appendChild(sum);
      for (const k of nombres) det.appendChild(armarParametro(k));
      cont.appendChild(det);
      controles["grupo:" + titulo] = { sum, nombres };
    }
  }

  function armarParametro(k) {
    const m = META[k], [min, max, paso] = RANGO[k], id = "p-" + k;
    const div = document.createElement("div");
    div.className = "param";
    const unidad = m.unidad === "px" ? "px" : m.unidad === "°" ? "°" : "";
    div.innerHTML = `
      <div class="param-linea">
        <label for="${id}">${ETIQUETA[k]}<span class="codigo">${k}</span></label>
        <span class="valor"><input id="${id}-n" inputmode="decimal" aria-label="${ETIQUETA[k]}, valor"><span class="unidad">${unidad}</span></span>
        <span class="mm"></span>
      </div>
      <input type="range" id="${id}" min="${min}" max="${max}" step="${paso}">
      ${k === "razon_x" ? `<div class="marcas-rango" aria-hidden="true"><span style="left:${(100 * (D.razon_sustituto - min) / (max - min)).toFixed(1)}%">sustituto</span><span style="left:${(100 * (D.razon_foto - min) / (max - min)).toFixed(1)}%">foto</span></div>` : ""}
      <p class="que"></p>
      <p class="de-donde"></p>
      <button class="volver" type="button" hidden>volver al valor de la obra</button>`;
    div.querySelector(".que").textContent = m.que;
    div.querySelector(".de-donde").textContent = m.de_donde;
    const rango = div.querySelector("input[type=range]"), num = div.querySelector(`#${id}-n`);
    const volver = div.querySelector(".volver"), mm = div.querySelector(".mm");
    rango.addEventListener("input", () => fijar(k, +rango.value));
    num.addEventListener("change", () => {
      const v = parseFloat(num.value.replace(",", "."));
      if (Number.isFinite(v) && v >= 0 && v <= 1000) fijar(k, k === "facetas" ? Math.max(1, Math.round(v)) : v);
      else pintarFicha();
    });
    volver.addEventListener("click", () => { delete ajustes[k]; cambio(); });
    controles[k] = { div, rango, num, volver, mm };
    return div;
  }

  function fijar(k, v) { ajustes[k] = v; cambio(); }

  function pintarFicha() {
    const b = asegurar().base;
    for (const k of Object.keys(RANGO)) {
      const c = controles[k], v = valor(k), d = decimales(k);
      if (document.activeElement !== c.num) c.num.value = coma(v, k === "razon_x" ? 3 : d);
      if (document.activeElement !== c.rango) c.rango.value = v;
      const aj = k in ajustes;
      c.div.classList.toggle("ajustado", aj);
      c.volver.hidden = !aj;
      if (aj) c.volver.textContent = `volver al valor de la obra (${coma(porDefecto(k), k === "razon_x" ? 3 : d)})`;
      c.mm.textContent = META[k].unidad === "px" ? `${coma(v / 4, 2)} mm · ${coma(v / b.t.c, 2)} canales` :
        k === "razon_x" ? `altura de x: ${coma(b.e.xh, 1)} px = ${coma(b.e.xh / 4, 1)} mm` : "";
    }
    for (const [titulo] of GRUPOS) {
      const g = controles["grupo:" + titulo], n = g.nombres.filter((k) => k in ajustes).length;
      g.sum.querySelector(".cuenta").textContent = n ? `${n} ajustado${n > 1 ? "s" : ""}` : "";
    }
    const n = Object.keys(ajustes).length;
    $("#cuenta-ajustes").textContent = n ? `${n} ajuste${n > 1 ? "s" : ""}` : "sin ajustes: los valores de la obra";
    if (document.activeElement !== $("#json")) $("#json").value = json();   // no pisar lo que se está pegando
  }

  let pedido = 0;
  function cambio() {
    guardar("ajustes", ajustes);
    if (pedido) return;
    pedido = requestAnimationFrame(() => {
      pedido = 0;
      asegurar();
      pintarFicha();
      dibujarVista();
    });
  }

  // ------------------------------------------------------------------ exportar e importar
  function json() {
    const b = asegurar().base, valores = { razon_x: +b.razon.toFixed(4) };
    for (const [k, p] of Object.entries(b.P)) valores[k] = +(+p.valor).toFixed(3);
    const aj = Object.fromEntries(Object.entries(ajustes).map(([k, v]) => [k, +(+v).toFixed(4)]));
    return JSON.stringify({
      contenida: "parámetros de la gramática",
      fecha: new Date().toISOString().slice(0, 10),
      uso: "python3 tipografia/simulacion/simular.py --parametros parametros.json",
      ajustes: aj,
      valores,
    }, null, 1);
  }

  function importar(texto) {
    const d = JSON.parse(texto);
    const a = d && typeof d === "object" ? (d.ajustes || d) : {};
    const nuevos = limpiar(a);
    if (!Object.keys(nuevos).length && Object.keys(a).length) throw new Error("ningún parámetro conocido");
    ajustes = nuevos;
    cambio();
    return Object.keys(nuevos).length;
  }

  function avisar(sel, texto) { const e = $(sel); e.textContent = texto; clearTimeout(e._t); e._t = setTimeout(() => { e.textContent = ""; }, 5000); }

  async function copiar(texto, sel, respaldo) {
    try {
      await navigator.clipboard.writeText(texto);
      avisar(sel, "Copiado.");
    } catch (e) {
      if (respaldo) { respaldo(); avisar(sel, "El navegador no deja copiar desde aquí: el texto quedó seleccionado."); }
      else avisar(sel, "El navegador no deja copiar desde aquí.");
    }
  }

  let bajadas = null;
  async function bajar(nombre, datos, sel) {
    if (!bajadas) return;
    try { await bajadas.save({ filename: nombre, data: datos }); avisar(sel, "Descargado."); }
    catch (e) { avisar(sel, e && e.code === "declined" ? "Descarga cancelada." : "No se pudo descargar aquí."); }
  }

  function armarAcciones() {
    $("#copiar-json").addEventListener("click", () => copiar(json(), "#estado-json", () => {
      const d = $("#json").closest("details"); d.open = true; $("#json").select();
    }));
    $("#bajar-json").addEventListener("click", () => bajar("parametros.json", json(), "#estado-json"));
    $("#restablecer").addEventListener("click", () => { ajustes = {}; cambio(); avisar("#estado-json", "Volvieron los valores de la obra."); });
    $("#aplicar-json").addEventListener("click", () => {
      try { const n = importar($("#json").value); avisar("#estado-json", `Aplicado: ${n} ajuste${n === 1 ? "" : "s"}.`); }
      catch (e) { avisar("#estado-json", "Ese texto no es un parametros.json: " + e.message + "."); }
    });
    $("#archivo").addEventListener("change", (ev) => {
      const f = ev.target.files[0];
      if (!f) return;
      const r = new FileReader();
      r.onload = () => {
        try { const n = importar(r.result); avisar("#estado-json", `Abierto ${f.name}: ${n} ajuste${n === 1 ? "" : "s"}.`); }
        catch (e) { avisar("#estado-json", `${f.name} no es un parametros.json.`); }
      };
      r.readAsText(f);
      ev.target.value = "";
    });
  }

  // ------------------------------------------------------------------ dibujar el cuerpo
  function camino(ctx, geo) {
    ctx.beginPath();
    for (const a of geo) {
      ctx.moveTo(a[0][0] + 0.5, a[0][1] + 0.5);
      for (let i = 1; i < a.length; i++) ctx.lineTo(a[i][0] + 0.5, a[i][1] + 0.5);
      ctx.closePath();
    }
  }
  const colorDe = (s) => (POR_SIGNO[s].estado === "reconstruida" ? COLOR.violeta : COLOR.tinta);

  const testigos = new Map();
  function testigo(s) {
    const b = asegurar().base, m = b.M[s];
    if (!m) return null;
    const k = b.razon + "|" + s;
    if (!testigos.has(k)) {
      if (testigos.size > 80) testigos.clear();
      const c = document.createElement("canvas");
      c.width = T; c.height = T;
      const ctx = c.getContext("2d"), id = ctx.createImageData(T, T);
      for (let i = 0; i < T * T; i++) if (m[i]) { id.data[i * 4] = 217; id.data[i * 4 + 1] = 213; id.data[i * 4 + 2] = 202; id.data[i * 4 + 3] = 255; }
      ctx.putImageData(id, 0, 0);
      testigos.set(k, c);
    }
    return testigos.get(k);
  }

  function lineasPiscina(ctx, e, k, rotulos) {
    ctx.save();
    ctx.strokeStyle = COLOR.gris2;
    ctx.lineWidth = 1 / k;
    ctx.setLineDash([6 / k, 5 / k]);
    ctx.fillStyle = COLOR.gris;
    ctx.font = `${11 / k}px "Courier Prime", monospace`;
    for (const [n, y] of [["afuera", e.afuera], ["borde", e.borde], ["fondo", e.fondo], ["desagüe", e.desague]]) {
      ctx.beginPath(); ctx.moveTo(0, y + 0.5); ctx.lineTo(T, y + 0.5); ctx.stroke();
      if (rotulos) ctx.fillText(n, 6 / k, y - 5 / k);
    }
    ctx.restore();
  }

  // ------------------------------------------------------------------ vista: la caja
  const celdasCaja = {};
  function armarCaja() {
    const caja = $("#caja");
    for (const c of D.caja) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "celda" + (c.estado === "manos" ? " manos" : "");
      b.style.gridColumn = c.columna;
      b.style.gridRow = c.fila;
      if (c.estado === "manos") {
        b.innerHTML = `<span class="num">${c.celda}</span><span class="dedos">se hace con los dedos</span>`;
        b.setAttribute("aria-label", `celda ${c.celda}: el signo final, se hace con los dedos`);
        b.disabled = true;
      } else {
        b.innerHTML = `<canvas></canvas><span class="num">${c.celda}</span>`;
        b.setAttribute("aria-label", `celda ${c.celda}: ${c.signo}, ${c.estado}`);
        b.addEventListener("click", () => { elegir(c.signo); mostrar("signo"); });
        celdasCaja[c.signo] = { b, canvas: b.querySelector("canvas") };
      }
      caja.appendChild(b);
    }
    $("#caja-lineas").checked = leer("caja.lineas", false);
    $("#caja-testigo").checked = leer("caja.testigo", false);
    for (const id of ["caja-lineas", "caja-testigo"]) $("#" + id).addEventListener("change", (ev) => { guardar(id.replace("-", "."), ev.target.checked); dibujarVista(); });
    new ResizeObserver(() => { if (vista === "caja") dibujarVista(); }).observe(caja);
  }

  function dibujarCelda(s) {
    const { canvas } = celdasCaja[s], r = armado(s), b = asegurar().base;
    const dpr = window.devicePixelRatio || 1, lado = Math.max(40, Math.round(canvas.clientWidth * dpr));
    if (canvas.width !== lado) { canvas.width = lado; canvas.height = lado; }
    const ctx = canvas.getContext("2d"), k = lado / T;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = COLOR.papel;
    ctx.fillRect(0, 0, lado, lado);
    ctx.setTransform(k, 0, 0, k, 0, 0);
    if ($("#caja-lineas").checked) lineasPiscina(ctx, b.e, k / dpr, false);
    if ($("#caja-testigo").checked) { const t = testigo(s); if (t) ctx.drawImage(t, 0, 0); }
    const fallo = celdasCaja[s].b.querySelector(".fallo");
    if (fallo) fallo.remove();
    if (r.error) {
      const f = document.createElement("span"); f.className = "fallo"; f.textContent = "no se armó";
      celdasCaja[s].b.appendChild(f);
      return;
    }
    camino(ctx, r.geo);
    ctx.fillStyle = colorDe(s);
    ctx.globalAlpha = $("#caja-testigo").checked ? 0.85 : 1;
    ctx.fill("evenodd");
    ctx.globalAlpha = 1;
  }

  function dibujarCaja() {
    const gen = asegurar().gen, cola = [estadoApp.signo, ...SIGNOS.filter((s) => s !== estadoApp.signo)];
    for (const s of SIGNOS) celdasCaja[s].b.setAttribute("aria-pressed", s === estadoApp.signo ? "true" : "false");
    const paso = () => {
      if (vista !== "caja" || asegurar().gen !== gen) return;
      const t0 = performance.now();
      while (cola.length && performance.now() - t0 < 14) dibujarCelda(cola.shift());
      $("#caja-estado").textContent = cola.length ? `armando… faltan ${cola.length}` : "";
      if (cola.length) requestAnimationFrame(paso);
      else pintarMedidas();
    };
    paso();
  }

  function pintarMedidas() {
    const b = asegurar().base, e = b.e, [x0, y0, x1, y1] = G.celda(e, T);
    const fuente = "razon_x" in ajustes ? "ajustada" : "la foto";
    const filas = [
      ["canal", `${coma(b.t.c, 1)} px`, `${coma(b.t.c / 4, 1)} mm`],
      ["altura de x", `${coma(e.xh, 1)} px`, `${coma(e.xh / 4, 1)} mm`],
      ["ascendente / x", coma(b.razon, 3), fuente],
      ["ascendente", `${coma(e.fondo - e.afuera, 1)} px`, `${coma((e.fondo - e.afuera) / 4, 1)} mm`],
      ["descendente", `${coma(e.desague - e.fondo, 1)} px`, `${coma((e.desague - e.fondo) / 4, 1)} mm`],
      ["celda", `${coma((x1 - x0) / 4, 0)} × ${coma((y1 - y0) / 4, 0)} mm`, "0,84 de ancho por alto"],
    ];
    $("#medidas").innerHTML = filas.map(([t, v, n]) => `<div><dt>${t}</dt><dd>${v} <small>${n}</small></dd></div>`).join("");
  }

  // ------------------------------------------------------------------ vista: el signo
  const PARTES = {
    asiento: "asiento", corte: "corte", "desagüe": "desagüe", hombro: "hombro", gota: "gota", punto: "punto de cinta",
    tilde: "tilde en gota", onda: "onda", alivio: "alivio", celda: "celda", "sifón": "sifón",
  };

  function dibujarSigno() {
    const s = estadoApp.signo, r = armado(s), b = asegurar().base, e = b.e, gl = r.glifo;
    const cv = $("#lienzo-signo"), ctx = cv.getContext("2d"), W = cv.width;
    const u = W / (cv.clientWidth || W / 2);                 // píxeles del lienzo por píxel de pantalla
    const capa = (n) => $("#capa-" + n).checked, color = colorDe(s);
    // el encuadre: el azulejo entero, o la letra con aire alrededor
    let k = W / T, ox = 0, oy = 0;
    if ($("#encuadre").value === "letra" && !r.error) {
      const [x0, y0, x1, y1] = G.limites(r.geo), xs = [x0, x1], ys = [y0, y1];
      if (capa("marcas")) for (const [, [x, y]] of gl.marcas) { xs.push(x); ys.push(y); }
      const pad = 1.6 * b.t.c, a0 = Math.min(...xs) - pad, a1 = Math.max(...xs) + pad, b0 = Math.min(...ys) - pad, b1 = Math.max(...ys) + pad;
      const lado = Math.max(a1 - a0, b1 - b0, 200);
      k = W / lado; ox = -((a0 + a1) / 2 - lado / 2) * k; oy = -((b0 + b1) / 2 - lado / 2) * k;
    }
    const px = (n) => n * u / k;                             // n píxeles de pantalla, en unidades del azulejo
    const pant = (x, y) => [ox + (x + 0.5) * k, oy + (y + 0.5) * k];
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = COLOR.papel;
    ctx.fillRect(0, 0, W, W);
    ctx.setTransform(k, 0, 0, k, ox, oy);
    const lineas = [["afuera", e.afuera], ["borde", e.borde], ["fondo", e.fondo], ["desagüe", e.desague]];
    if (capa("lineas")) {
      const [x0, y0, x1, y1] = G.celda(e, T);
      ctx.strokeStyle = COLOR.filete; ctx.lineWidth = px(1.5);
      ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
      ctx.strokeStyle = COLOR.gris2; ctx.lineWidth = px(1); ctx.setLineDash([px(6), px(5)]);
      for (const [, y] of lineas) { ctx.beginPath(); ctx.moveTo(-T, y + 0.5); ctx.lineTo(2 * T, y + 0.5); ctx.stroke(); }
      ctx.setLineDash([]);
    }
    if (capa("testigo")) { const t = testigo(s); if (t) ctx.drawImage(t, 0, 0); }
    if (!r.error && capa("cuerpo")) {
      camino(ctx, r.geo);
      if (capa("ejes")) {
        ctx.fillStyle = color; ctx.globalAlpha = 0.13; ctx.fill("evenodd"); ctx.globalAlpha = 1;
        ctx.strokeStyle = color; ctx.lineWidth = px(1.2); ctx.stroke();
      } else { ctx.fillStyle = color; ctx.fill("evenodd"); }
    }
    if (!r.error && capa("ejes")) {
      ctx.strokeStyle = COLOR.gris; ctx.lineWidth = px(1);
      for (const m of gl.mas) { ctx.beginPath(); m.forEach(([x, y], i) => (i ? ctx.lineTo(x + .5, y + .5) : ctx.moveTo(x + .5, y + .5))); ctx.closePath(); ctx.stroke(); }
      ctx.strokeStyle = COLOR.violeta; ctx.lineWidth = px(3); ctx.lineJoin = "round"; ctx.lineCap = "butt";
      for (const [t] of gl.trazos) { if (t.length < 2) continue; ctx.beginPath(); t.forEach(([x, y], i) => (i ? ctx.lineTo(x + .5, y + .5) : ctx.moveTo(x + .5, y + .5))); ctx.stroke(); }
      ctx.lineWidth = px(1); ctx.strokeStyle = COLOR.tinta;
      for (const m of gl.menos) { ctx.beginPath(); ctx.arc(m.x + .5, m.y + .5, m.r, 0, 2 * Math.PI); ctx.stroke(); }
      const q = px(4.5);
      ctx.fillStyle = COLOR.papel;
      for (const [x, y] of gl.nodos) { ctx.fillRect(x + .5 - q / 2, y + .5 - q / 2, q, q); ctx.strokeRect(x + .5 - q / 2, y + .5 - q / 2, q, q); }
    }
    // los rótulos, en píxeles de pantalla: las líneas a la izquierda; las partes, a los costados
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.font = `${12 * u}px "Courier Prime", "Courier New", monospace`;
    const ocupados = [];
    if (capa("lineas")) {
      ctx.fillStyle = COLOR.gris;
      for (const [n, y] of lineas) {
        const yy = pant(0, y)[1] - 5 * u;
        if (yy < 12 * u || yy > W) continue;
        ctx.fillText(n, 8 * u, yy);
        ocupados.push([false, yy]);
      }
    }
    if (!r.error && capa("marcas")) {
      ctx.font = `${13 * u}px "Courier Prime", "Courier New", monospace`;
      for (const [nombre, [x, y]] of gl.marcas) {
        const [sx, sy] = pant(x, y), derecha = sx > W / 2, ancho = ctx.measureText(nombre).width;
        let ty = sy;
        while (ocupados.some((o) => o[0] === derecha && Math.abs(ty - o[1]) < 20 * u)) ty += 20 * u;
        ocupados.push([derecha, ty]);
        const tx = derecha ? W - 10 * u - ancho : 10 * u;
        ctx.strokeStyle = COLOR.gris2; ctx.lineWidth = u;
        ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(derecha ? tx - 5 * u : tx + ancho + 5 * u, ty - 4 * u); ctx.stroke();
        ctx.fillStyle = "rgba(243,241,234,.88)"; ctx.fillRect(tx - 3 * u, ty - 13 * u, ancho + 6 * u, 17 * u);
        ctx.fillStyle = COLOR.tinta; ctx.fillText(nombre, tx, ty);
      }
    }
    pintarFichaSigno(r);
  }

  function pintarFichaSigno(r) {
    const s = estadoApp.signo, c = POR_SIGNO[s], b = asegurar().base, f = $("#ficha-signo");
    const rec = c.estado === "reconstruida";
    let medidas = "";
    if (!r.error) {
      const [x0, y0, x1, y1] = G.limites(r.geo), m = G.rasterizar(r.geo, T);
      let area = 0;
      for (let i = 0; i < m.length; i++) area += m[i];
      const cuenta = (n) => r.glifo.marcas.filter(([x]) => x === n).length;
      medidas = `<dt>cuerpo</dt><dd>${coma((x1 - x0) / 4, 1)} × ${coma((y1 - y0) / 4, 1)} mm, ${coma(area / 16, 0)} mm² de chapa</dd>
        <dt>trazos</dt><dd>${r.glifo.trazos.length} ejes del ancho del canal (${coma(b.t.c / 4, 1)} mm)</dd>
        <dt>alivios</dt><dd>${r.glifo.menos.length || "ninguno"}</dd>
        <dt>gotas</dt><dd>${cuenta("gota") || "ninguna"}</dd>`;
    }
    const partes = r.glifo ? [...new Set(r.glifo.marcas.map(([n]) => n))] : [];
    const procedencia = c.estado === "hallada" && c.procedencia ? `${c.testigos} testigos en el pie; el mejor conservado, en «${c.procedencia}»` : "no está en el pie: se arma por analogía";
    f.innerHTML = `
      <p class="grande ${rec ? "reconstruida" : ""}"></p>
      <p class="celda-n">celda ${String(c.celda).padStart(2, "0")} · fila ${c.fila}, columna ${c.columna} · ${c.estado}</p>
      <p class="receta"></p>
      <dl>
        <dt>del pie</dt><dd></dd>
        <dt>partes</dt><dd></dd>
        ${medidas}
      </dl>
      ${r.error ? `<p class="estado-linea" style="color:#8a2a2a">${r.error}. Prueba otro valor o vuelve al de la obra.</p>` : ""}
      <div class="nav-signo">
        <button class="boton suave" type="button" data-ir="-1">← anterior</button>
        <button class="boton suave" type="button" data-ir="1">siguiente →</button>
        <button class="boton suave" type="button" id="copiar-svg" ${r.error ? "disabled" : ""}>Copiar SVG</button>
        <button class="boton suave" type="button" id="bajar-svg" ${r.error || !bajadas ? "hidden" : ""}>Descargar SVG</button>
        <button class="boton suave" type="button" id="ver-estados">Ver sus estados</button>
      </div>
      <p class="estado-linea" id="estado-svg" role="status"></p>`;
    f.querySelector(".grande").textContent = s;
    f.querySelector(".receta").textContent = r.receta ? r.receta.charAt(0).toUpperCase() + r.receta.slice(1) + "." : "";
    const dds = f.querySelectorAll("dd");
    dds[0].textContent = procedencia;
    dds[1].textContent = partes.join(", ") || "—";
    f.querySelectorAll("[data-ir]").forEach((btn) => btn.addEventListener("click", () => {
      const i = SIGNOS.indexOf(s), j = (i + +btn.dataset.ir + SIGNOS.length) % SIGNOS.length;
      elegir(SIGNOS[j]);
    }));
    const svg = () => G.aSvg(r.geo, b.e, T, s);
    const cel = String(c.celda).padStart(2, "0");
    f.querySelector("#copiar-svg").addEventListener("click", () => copiar(svg(), "#estado-svg"));
    f.querySelector("#bajar-svg").addEventListener("click", () => bajar(`contenida_celda_${cel}.svg`, svg(), "#estado-svg"));
    f.querySelector("#ver-estados").addEventListener("click", () => mostrar("estados"));
  }

  // ------------------------------------------------------------------ vista: el texto
  function notdef(ctx, k) {
    const alto = 0.62 * T, ancho = 0.84 * alto, x0 = (T - ancho) / 2, y0 = (T - alto) / 2, ix = 0.18 * ancho, iy = 0.13 * alto;
    ctx.strokeStyle = COLOR.gris; ctx.lineWidth = Math.max(2.5, 1.2 / k);
    for (const [a, b, c, d] of [[x0, y0, x0 + ancho, y0 + alto], [x0 + ix, y0 + iy, x0 + ancho - ix, y0 + alto - iy]]) {
      const m = (a + c) / 2, h = 6;                  // el desagüe: media junta a cada lado del centro de abajo
      ctx.beginPath(); ctx.moveTo(m + h, d); ctx.lineTo(c, d); ctx.lineTo(c, b); ctx.lineTo(a, b); ctx.lineTo(a, d); ctx.lineTo(m - h, d); ctx.stroke();
    }
  }

  function dibujarTexto() {
    const b = asegurar().base, [cx0, cy0, cx1, cy1] = G.celda(b.e, T);
    const altoPx = +$("#cuerpo-texto").value, k = altoPx / (cy1 - cy0), anchoPx = (cx1 - cx0) * k;
    $("#cuerpo-mm").textContent = `${coma(altoPx, 0)} px de pantalla por celda · en la piscina, ${coma((cy1 - cy0) / 4, 0)} mm`;
    const caja = $(".composicion"), margen = 16, cols = Math.max(4, Math.floor((caja.clientWidth - 2 * margen) / anchoPx));
    const lineas = [];
    for (const parrafo of $("#texto").value.toLowerCase().split("\n")) {
      let linea = "";
      for (const palabra of parrafo.split(" ")) {
        const prueba = linea ? linea + " " + palabra : palabra;
        if ([...prueba].length <= cols) linea = prueba;
        else {
          if (linea) lineas.push(linea);
          let resto = palabra;
          while ([...resto].length > cols) { lineas.push([...resto].slice(0, cols).join("")); resto = [...resto].slice(cols).join(""); }
          linea = resto;
        }
      }
      lineas.push(linea);
    }
    const dpr = window.devicePixelRatio || 1, cv = $("#lienzo-texto");
    const W = Math.ceil(Math.max(...lineas.map((l) => [...l].length), 1) * anchoPx + 2 * margen), H = Math.ceil(lineas.length * altoPx + 2 * margen);
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    cv.style.width = W + "px"; cv.style.height = H + "px";
    const ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = COLOR.papel; ctx.fillRect(0, 0, W, H);
    lineas.forEach((l, fila) => [...l].forEach((ch, col) => {
      if (ch === " ") return;
      ctx.setTransform(k * dpr, 0, 0, k * dpr, (margen + col * anchoPx - cx0 * k) * dpr, (margen + fila * altoPx - cy0 * k) * dpr);
      if (G.RECETAS[ch]) {
        const r = armado(ch);
        if (r.error) { notdef(ctx, k); return; }
        camino(ctx, r.geo); ctx.fillStyle = colorDe(ch); ctx.fill("evenodd");
      } else if (ch !== "¶") notdef(ctx, k);
    }));
    if ($("#juntas-texto").checked) {                 // los azulejos de 150 mm, con juntas de 3 mm
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = "rgba(168,164,154,0.95)";
      const paso = T * k, j = 12 * k;
      for (let x = margen - j / 2; x < W; x += paso) ctx.fillRect(x, 0, j, H);
      for (let y = margen - j / 2; y < H; y += paso) ctx.fillRect(0, y, W, j);
    }
  }

  function armarTexto() {
    const sel = $("#verso");
    sel.innerHTML = `<option value="">— elige un verso —</option>` + VERSOS.map((v, i) => `<option value="${i}"></option>`).join("");
    VERSOS.forEach((v, i) => { sel.options[i + 1].textContent = v; });
    sel.addEventListener("change", () => { if (sel.value !== "") { $("#texto").value = VERSOS[+sel.value]; guardar("texto", $("#texto").value); dibujarVista(); } });
    $("#texto").value = leer("texto", $("#texto").value);
    $("#cuerpo-texto").value = leer("cuerpo", 64);
    $("#juntas-texto").checked = leer("juntas", false);
    $("#texto").addEventListener("input", () => { guardar("texto", $("#texto").value); dibujarVista(); });
    $("#cuerpo-texto").addEventListener("input", () => { guardar("cuerpo", +$("#cuerpo-texto").value); dibujarVista(); });
    $("#juntas-texto").addEventListener("change", () => { guardar("juntas", $("#juntas-texto").checked); dibujarVista(); });
    new ResizeObserver(() => { if (vista === "texto") dibujarVista(); }).observe($(".composicion"));
  }

  // ------------------------------------------------------------------ vista: los estados
  const est = { gen: 0, mano: leer("mano", 1), placa: null, fr: null, frotadas: [], legibles: null, anim: null, cuadros: {} };
  const PANELES = [
    ["calco", "Calco", "En papel de calco sobre el frotado de la pared: el contorno, abierto en su punto más bajo."],
    ["reverso", "Placa, reverso", "Papel de aluminio cortado a tijera; punzón de bola de 1 mm: la letra al revés y hundida."],
    ["anverso", "Placa, anverso", "La misma hoja dada vuelta, con luz rasante desde la izquierda (15°): la letra se lee."],
    ["cinta", "Cinta", "Masking blanca sobre el plástico negro: tramos rectos que se pliegan para girar."],
    ["frotado", "Frotado", "Papel y grafito sobre la placa. Cada frotada aplasta el relieve: el peso se mide en frotadas."],
    ["agua", "Agua", "La placa en una bandeja con un dedo de agua: la luz cae en los azulejos, al revés y en trapecio."],
    ["voz", "Voz", "El agua vibra con una sílaba del verso leído en voz alta: ondas de Faraday."],
  ];
  const AGUA_W = 560, AGUA_H = 448;

  function armarEstados() {
    const cont = $("#estados");
    for (const [id, titulo, texto] of PANELES) {
      const fig = document.createElement("figure");
      fig.className = "estado";
      const ancho = id === "agua" || id === "voz";
      fig.innerHTML = `<div class="marco ${ancho ? "ancho" : ""}"><canvas id="c-${id}" width="${ancho ? AGUA_W : T}" height="${ancho ? AGUA_H : T}" role="img" aria-label="${titulo}"></canvas><div class="espera" id="e-${id}">esperando…</div></div>
        <figcaption><b>${titulo}</b><span id="t-${id}"></span></figcaption><div class="controles" id="k-${id}"></div>`;
      fig.querySelector(`#t-${id}`).textContent = texto;
      cont.appendChild(fig);
    }
    $("#k-cinta").innerHTML = `<label><input type="checkbox" id="arrancada"> arrancada</label><span id="d-cinta"></span>`;
    $("#k-anverso").innerHTML = `<span id="d-anverso"></span>`;
    $("#k-frotado").innerHTML = `<input type="range" id="n-frotadas" min="1" max="1" value="1" aria-label="Frotada"><span id="d-frotado" class="mono">frotada 1</span><button class="boton suave" type="button" id="frotar">Frotar hasta que no se lea</button>`;
    $("#k-agua").innerHTML = `<label><input type="checkbox" id="tocada"> un dedo toca el agua</label>`;
    $("#k-voz").innerHTML = `<select id="verso-voz" aria-label="Verso"></select><label>sílaba <input type="range" id="silaba" min="1" max="1" value="1"></label><label>volumen <input type="range" id="volumen" min="0.15" max="1" step="0.05" value="0.65"></label><span id="d-voz" class="mono"></span>`;
    const sv = $("#verso-voz");
    VERSOS.forEach((v, i) => { const o = document.createElement("option"); o.value = i; o.textContent = v; sv.appendChild(o); });
    sv.value = leer("verso.voz", VERSOS.indexOf("acciones del cuerpo.") >= 0 ? VERSOS.indexOf("acciones del cuerpo.") : 0);
    const selS = $("#signo-estados");
    for (const s of SIGNOS) { const o = document.createElement("option"); o.value = s; o.textContent = `${s}  · celda ${POR_SIGNO[s].celda}`; selS.appendChild(o); }
    selS.addEventListener("change", () => elegir(selS.value));
    $("#otra-mano").addEventListener("click", () => { est.mano++; guardar("mano", est.mano); correrEstados(); });
    $("#arrancada").addEventListener("change", () => cinta());
    $("#frotar").addEventListener("click", () => frotarHastaElFinal());
    $("#n-frotadas").addEventListener("input", () => mostrarFrotada(+$("#n-frotadas").value));
    $("#tocada").addEventListener("change", () => animarAgua());
    for (const id of ["verso-voz", "silaba", "volumen"]) $("#" + id).addEventListener("input", () => { guardar("verso.voz", +sv.value); prepararVoz(); });
  }

  function espera(id, texto) { const e = $("#e-" + id); e.hidden = !texto; e.textContent = texto || ""; }
  function pintarGris(id, img, w = T, h = T) { $("#c-" + id).getContext("2d").putImageData(S.aImageData([img], w, h), 0, 0); espera(id, null); }
  function pintarRGB(id, planos, w, h) { $("#c-" + id).getContext("2d").putImageData(S.aImageData(planos, w, h), 0, 0); espera(id, null); }

  const fondos = new Map();
  let reflectancia = null;

  async function correrEstados() {
    const gen = ++est.gen, s = estadoApp.signo, c = POR_SIGNO[s], r = armado(s);
    detenerAnimacion();
    $("#mano").textContent = est.mano;
    $("#signo-estados").value = s;
    for (const [id] of PANELES) espera(id, "esperando…");
    if (r.error) { for (const [id] of PANELES) espera(id, r.error); return; }
    const clave = [c.celda, est.mano], rec = c.estado === "reconstruida", b = asegurar().base, e = b.e;
    const sigue = async (id) => { if (id) espera(id, "calculando…"); await respiro(); return gen === est.gen && vista === "estados"; };
    $("#estados-estado").textContent = "calculando…";
    if (!await sigue("calco")) return;
    if (!fondos.has(c.celda)) { if (fondos.size > 12) fondos.clear(); fondos.set(c.celda, S.fondoFrotado(c.celda)); }
    const pauta = { celda: G.celda(e, T), fondo: e.fondo, borde: e.borde };
    const { img, trazos } = S.calco(r.geo, rec, fondos.get(c.celda), pauta, S.azar("calco", ...clave));
    pintarGris("calco", img);
    $("#t-calco").textContent = `En papel de calco sobre el frotado de la pared: ${trazos.length} contorno${trazos.length > 1 ? "s" : ""}, cada uno abierto en su punto más bajo. ${rec ? "Punteado: reconstruida." : "Continuo: hallada."}`;
    if (!await sigue("reverso")) return;
    const placa = S.repujarPlaca(trazos, rec, clave);
    est.placa = placa;
    const rev = S.reverso(placa);
    pintarGris("reverso", S.sombrear(rev.altura, rev.mascara, S.azar("foto reverso", ...clave)));
    if (!await sigue("anverso")) return;
    pintarGris("anverso", S.sombrear(placa.altura, placa.mascara, S.azar("foto", ...clave)));
    $("#d-anverso").textContent = `${coma(placa.largo_mm / 10, 0)} cm de surco · ${placa.intentos} intento${placa.intentos > 1 ? "s" : ""}` +
      (placa.roturas ? `, ${placa.roturas} rota${placa.roturas > 1 ? "s" : ""}: se guarda y se hace otra` : "") + ` · unos ${coma(placa.minutos, 0)} minutos`;
    if (!await sigue("cinta")) return;
    est.cintas = {};
    cinta();
    if (!await sigue("frotado")) return;
    $("#t-frotado").textContent = PANELES[4][2];
    est.fr = S.frotador(placa, S.azar("frotado", ...clave));
    est.frotadas = [];
    est.legibles = null;
    guardarFrotada(est.fr.frotar());
    mostrarFrotada(1);
    $("#frotar").disabled = false;
    if (!await sigue("agua")) return;
    if (!reflectancia) reflectancia = S.azulejos(AGUA_W, AGUA_H, S.azar("bandeja"));
    est.quieta = S.superficieQuieta(S.azar("agua", ...clave));
    est.cuadros = {};
    animarAgua();
    if (!await sigue("voz")) return;
    prepararVoz();
    $("#estados-estado").textContent = "";
  }

  function cinta() {
    const s = estadoApp.signo, r = armado(s), c = POR_SIGNO[s];
    if (r.error || !est.cintas) return;
    const arr = $("#arrancada").checked, k = arr ? "a" : "p";
    if (!est.cintas[k]) est.cintas[k] = S.encintar(r.glifo.trazos, G.V(asegurar().base.P, "cinta"), S.azar("cinta", c.celda, est.mano), arr);
    const q = est.cintas[k];
    pintarRGB("cinta", q.img, T, T);
    $("#d-cinta").textContent = `${q.tramos} tramos, ${q.pliegues} pliegues`;
  }

  // el frotado: se guardan las frotadas en chico para poder volver atrás
  function guardarFrotada(img) {
    const n = est.frotadas.length + 1, chica = new Float32Array(300 * 300);
    for (let y = 0; y < 300; y++) for (let x = 0; x < 300; x++) {
      const i = 2 * y * T + 2 * x;
      chica[y * 300 + x] = (img[i] + img[i + 1] + img[i + T] + img[i + T + 1]) / 4;
    }
    est.frotadas.push({ img: n === 1 ? img : null, chica, legible: est.fr.estado.legible, contraste: est.fr.estado.contraste });
  }

  function mostrarFrotada(n) {
    const f = est.frotadas[n - 1];
    if (!f) return;
    const cv = $("#c-frotado");
    if (f.img) { cv.width = T; cv.height = T; pintarGris("frotado", f.img); }
    else { cv.width = 300; cv.height = 300; pintarGris("frotado", f.chica, 300, 300); }
    $("#n-frotadas").max = est.frotadas.length;
    $("#n-frotadas").value = n;
    const leg = est.legibles === null ? "" : ` · se lee en ${est.legibles}`;
    $("#d-frotado").textContent = `frotada ${n}: ${f.legible ? "se lee" : "ya no se lee"} (contraste ${coma(f.contraste, 1)})${leg}`;
  }

  async function frotarHastaElFinal() {
    const gen = est.gen, boton = $("#frotar");
    boton.disabled = true;
    while (est.frotadas.length < 45 && est.frotadas[est.frotadas.length - 1].legible) {
      await respiro();
      if (gen !== est.gen) return;
      guardarFrotada(est.fr.frotar());
      mostrarFrotada(est.frotadas.length);
    }
    const i = est.frotadas.findIndex((f) => !f.legible);
    est.legibles = i < 0 ? est.frotadas.length : i;
    mostrarFrotada(est.frotadas.length);
    $("#t-frotado").textContent = `Papel y grafito sobre la placa. Cada frotada aplasta entre un 5 y un 9 % del relieve. Esta letra pesa ${est.legibles} frotada${est.legibles === 1 ? "" : "s"}.`;
  }

  // el agua y la voz: cuadros que se calculan de a uno y después se repiten
  function detenerAnimacion() { if (est.anim) cancelAnimationFrame(est.anim.raf); est.anim = null; }

  function fotoDe(superficie, clave) {
    const luz = S.reflejo(est.placa, superficie);
    return S.aImageData(S.fotoAgua(luz, AGUA_W, AGUA_H, reflectancia, S.azar("foto agua", ...clave)), AGUA_W, AGUA_H);
  }

  function animar(id, n, fuente, cada = 110) {
    const lista = new Array(n), anim = { raf: 0, i: 0, ultimo: 0 };
    const quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const paso = (t) => {
      if (est.anim !== anim && est.animVoz !== anim) return;
      if (!lista[anim.i]) { lista[anim.i] = fuente(anim.i); }
      if (t - anim.ultimo >= cada || anim.ultimo === 0) {
        $("#c-" + id).getContext("2d").putImageData(lista[anim.i], 0, 0);
        espera(id, null);
        anim.ultimo = t;
        if (!quieto) anim.i = (anim.i + 1) % n;
      }
      if (!quieto) anim.raf = requestAnimationFrame(paso);
    };
    anim.raf = requestAnimationFrame(paso);
    return anim;
  }

  function animarAgua() {
    if (!est.placa || !est.quieta) return;
    if (est.anim) cancelAnimationFrame(est.anim.raf);
    const c = POR_SIGNO[estadoApp.signo], clave = [c.celda, est.mano];
    if (!$("#tocada").checked) {
      est.anim = null;
      $("#c-agua").getContext("2d").putImageData(est.cuadros.quieta || (est.cuadros.quieta = fotoDe(est.quieta, clave)), 0, 0);
      espera("agua", null);
      return;
    }
    const cuadros = est.cuadros.tocada || (est.cuadros.tocada = []);
    est.anim = animar("agua", 16, (i) => cuadros[i] || (cuadros[i] = fotoDe(S.superficieTocada(est.quieta, i / 16 * 4), clave)));
  }

  function prepararVoz() {
    if (!est.placa) return;
    const verso = VERSOS[+$("#verso-voz").value] || VERSOS[0], sil = S.silabas(verso), n = Math.max(sil.length, 1);
    const sl = $("#silaba");
    sl.max = n;
    if (+sl.value > n) sl.value = n;
    const i = +sl.value - 1, hz = 195 + (125 - 195) * (n > 1 ? i / (n - 1) : 0), vol = +$("#volumen").value;
    const c = POR_SIGNO[estadoApp.signo], clave = [c.celda, est.mano];
    const F = S.faraday(hz, vol, S.azar("voz", ...clave));
    $("#d-voz").textContent = `sílaba ${i + 1} de ${n}, «${sil[i] || ""}» · ${coma(hz, 0)} Hz · λ ${coma(F.lamMm, 1)} mm`;
    $("#t-voz").textContent = "El agua vibra con una sílaba del verso leído en voz alta: ondas de Faraday. La altura y el volumen son inventados: no es tu voz.";
    if (est.animVoz) cancelAnimationFrame(est.animVoz.raf);
    const cuadros = [];
    est.animVoz = animar("voz", 12, (j) => cuadros[j] || (cuadros[j] = fotoDe(F.en(j / 12), clave)), 120);
  }

  // ------------------------------------------------------------------ vistas y signo elegido
  const estadoApp = { signo: SIGNOS.includes(leer("signo", "a")) ? leer("signo", "a") : "a" };
  let vista = ["caja", "signo", "texto", "estados"].includes(leer("vista", "caja")) ? leer("vista", "caja") : "caja";

  function elegir(s) {
    if (!SIGNOS.includes(s)) return;
    estadoApp.signo = s;
    guardar("signo", s);
    $("#n-signo").textContent = s;
    dibujarVista();
  }

  function mostrar(v) {
    vista = v;
    guardar("vista", v);
    for (const n of ["caja", "signo", "texto", "estados"]) {
      $("#t-" + n).setAttribute("aria-selected", n === v ? "true" : "false");
      $("#t-" + n).tabIndex = n === v ? 0 : -1;
      $("#vista-" + n).hidden = n !== v;
    }
    if (v !== "estados") { detenerAnimacion(); if (est.animVoz) { cancelAnimationFrame(est.animVoz.raf); est.animVoz = null; } est.gen++; }
    dibujarVista();
  }

  function dibujarVista() {
    if (vista === "caja") dibujarCaja();
    else if (vista === "signo") dibujarSigno();
    else if (vista === "texto") dibujarTexto();
    else if (vista === "estados") correrEstados();
  }

  function armarPestanas() {
    const tabs = ["caja", "signo", "texto", "estados"];
    tabs.forEach((n, i) => {
      const t = $("#t-" + n);
      t.addEventListener("click", () => mostrar(n));
      t.addEventListener("keydown", (ev) => {
        const d = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
        if (d) { const j = (i + d + tabs.length) % tabs.length; mostrar(tabs[j]); $("#t-" + tabs[j]).focus(); }
      });
    });
    $("#encuadre").value = leer("encuadre", "letra");
    $("#encuadre").addEventListener("change", () => { guardar("encuadre", $("#encuadre").value); dibujarVista(); });
    for (const n of ["testigo", "cuerpo", "ejes", "marcas", "lineas"]) {
      const c = $("#capa-" + n);
      c.checked = leer("capa." + n, c.checked);
      c.addEventListener("change", () => { guardar("capa." + n, c.checked); dibujarVista(); });
    }
  }

  // ------------------------------------------------------------------ versiones guardadas (si la página las tiene)
  async function versiones() {
    const cl = window.claude;
    if (!cl || typeof cl.use !== "function") return;
    const [db, user, dl] = await Promise.all([cl.use("db"), cl.use("user"), cl.use("downloads")]);
    if (dl) { bajadas = dl; $("#bajar-json").hidden = false; if (vista === "signo") dibujarSigno(); }
    if (!db) return;
    $("#versiones").hidden = false;
    const yo = user ? await user.id() : null, dueno = user ? await user.isOwner() : false;
    const puede = user ? await user.can("data.write") : null;
    if (puede === false) $("#form-guardar").hidden = true;
    $("#form-guardar").addEventListener("submit", async (ev) => {
      ev.preventDefault();
      const nombre = $("#nombre-version").value.trim() || `versión del ${new Date().toLocaleDateString("es-BO")}`;
      const boton = $("#guardar-version");
      boton.disabled = true;
      try {
        await db.collection("versiones").add({
          nombre, nota: $("#nota-version").value.trim(), ajustes: JSON.parse(JSON.stringify(ajustes)),
          razon_x: +asegurar().base.razon.toFixed(4), fecha: new Date().toISOString(), autor: yo,
        });
        $("#nombre-version").value = ""; $("#nota-version").value = "";
        avisar("#estado-version", "Guardada. Claude puede leerla y correr la simulación con ella.");
      } catch (e) {
        avisar("#estado-version", e && e.code === "invalid_argument" ? "Esta vista no puede guardar versiones." :
          e && e.code === "quota_exceeded" ? "No caben más versiones: borra alguna vieja." : "No se pudo guardar; prueba de nuevo.");
        if (e && e.code === "invalid_argument") $("#form-guardar").hidden = true;
      } finally { boton.disabled = false; }
    });
    const lista = $("#lista-versiones");
    db.collection("versiones").orderBy("fecha", "desc").limit(50).onSnapshot((snap) => {
      lista.innerHTML = "";
      if (snap.empty) {
        lista.innerHTML = `<li style="border:0;background:none;padding:0"><p class="vacia">Todavía no hay versiones. Guarda una y pide a Claude que corra la simulación con ella.</p></li>`;
        return;
      }
      for (const d of snap.docs) {
        const v = d.data(), li = document.createElement("li");
        const aj = limpiar(v.ajustes), resumen = Object.entries(aj).map(([k, x]) => `${k} ${coma(x, k === "razon_x" ? 3 : decimales(k))}`).join(" · ");
        li.innerHTML = `<span class="nombre"></span><span class="detalle"></span><span class="detalle nota"></span>
          <span class="fila"><button class="boton suave" type="button" data-a="cargar">Cargar</button><button class="boton suave" type="button" data-a="json">Copiar JSON</button>
          ${v.autor && (v.autor === yo || dueno) ? `<button class="boton suave" type="button" data-a="borrar">Borrar</button>` : ""}</span>`;
        li.querySelector(".nombre").textContent = String(v.nombre || "sin nombre");
        const f = v.fecha ? new Date(v.fecha) : null;
        li.querySelector(".detalle").textContent = (f && !isNaN(f) ? f.toLocaleString("es-BO", { dateStyle: "medium", timeStyle: "short" }) + " · " : "") + (resumen || "los valores de la obra") + (v.autor && v.autor === yo ? " · tuya" : "");
        li.querySelector(".nota").textContent = String(v.nota || "");
        li.querySelector('[data-a="cargar"]').addEventListener("click", () => { ajustes = aj; cambio(); avisar("#estado-version", `Cargada: ${v.nombre}.`); });
        li.querySelector('[data-a="json"]').addEventListener("click", () => copiar(JSON.stringify({ contenida: "parámetros de la gramática", nombre: v.nombre, ajustes: aj }, null, 1), "#estado-version"));
        const borrar = li.querySelector('[data-a="borrar"]');
        if (borrar) borrar.addEventListener("click", async () => {
          if (borrar.dataset.seguro !== "1") { borrar.dataset.seguro = "1"; borrar.textContent = "¿Seguro? Borrar"; return; }
          try { await db.collection("versiones").doc(d.id).delete(); }
          catch (e) { avisar("#estado-version", "No se pudo borrar."); }
        });
        lista.appendChild(li);
      }
    }, () => { $("#versiones").hidden = true; });
  }

  // ------------------------------------------------------------------ arranque
  function arrancar() {
    armarFicha();
    armarAcciones();
    armarCaja();
    armarTexto();
    armarEstados();
    armarPestanas();
    asegurar();
    pintarFicha();
    $("#n-signo").textContent = estadoApp.signo;
    mostrar(vista);
    versiones();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (vista === "signo" || vista === "texto") dibujarVista(); });
  }

  if (!window.ClipperLib) {
    document.querySelector(".trabajo").insertAdjacentHTML("afterbegin",
      `<p class="estado-linea" style="color:#8a2a2a;font-size:14px">No cargó la biblioteca de polígonos (clipper-lib, de cdn.jsdelivr.net). Sin ella la gramática no puede armar los cuerpos: revisa la conexión y vuelve a abrir la página.</p>`);
    return;
  }
  arrancar();
})();
