/* El repujado: la mesa.
 *
 * La placa, la mano y sus herramientas. La mano dibuja con el puntero (el ratón, el dedo o el lápiz de una
 * tableta); el motor (repujado.js) pone el aluminio y la luz. Lo que se dibuja queda guardado en este navegador,
 * y sale como imagen (con su procedencia en los datos) o como ensayo en JSON, para rehacerlo.
 *
 * El calco puede ser un signo de la caja (la gramática de ../aplicacion/, la propuesta de la máquina) o una
 * imagen: la foto del calco de la mano.
 */
(function () {
  "use strict";
  const R = window.Repujado, LADO = R.LADO;
  const G = window.Gramatica, D = window.DATOS;
  const $ = (s) => document.querySelector(s);
  const TINTA = "#1d1c1a", VIOLETA = "#4a2470", PAPEL = "#f6f4ee";
  const coma = (v, d = 1) => (Math.round(v * 10 ** d) / 10 ** d).toFixed(d).replace(".", ",");

  const HERRAMIENTAS = {
    repasar: "El punzón hunde un surco; por la otra cara sale el relieve. Los surcos se funden. Lo hallado, con un trazo continuo.",
    puntear: "Lo reconstruido, a puntos, cada 2,25 mm, más o menos, como los pondría una mano. El punteado queda en relieve para siempre, y perfora más.",
    rellenar: "El lado redondo sube la letra de a poco, si pide más cuerpo. Se anota.",
    alisar: "La yema alisa las arrugas y suaviza lo chico. El surco queda.",
  };
  const LUCES = {
    taller: "Una ventana grande y una tira de luz: el aluminio se ve como metal. La lámpara se mueve libre.",
    registro: "La foto de la Acción 4: una sola lámpara, rasante, desde un lado fijo: la misma altura y el mismo ángulo. Por eso no se mueve.",
  };
  const REGISTRO = { azimut: 160, elevacion: 15 };

  // ------------------------------------------------------------------ lo guardado en este navegador
  const GUARDA = "contenida-repujado-v1";
  const a = {
    herramienta: "repasar", cara: "reverso", punzon: "bola", base: "fieltro", fuerza: 1, temblor: 0.5, radio: 3,
    presion: "velocidad", arrugas: 0.1, brillante: "anverso", doble: false, luz: "registro", azimut: 135, elevacion: 38,
    sombras: true, fondo: "tinta", zoom: 1, signo: "", verCalco: true, calcoOpacidad: 0.7, mano: "derecha",
    semilla: "1", tamano: 1024,
  };
  let guardado = null;
  try { guardado = JSON.parse(localStorage.getItem(GUARDA) || "null"); } catch (e) { guardado = null; }
  if (guardado && guardado.ajustes) Object.assign(a, guardado.ajustes);
  let rotas = (guardado && guardado.rotas) || [];
  function guardar() {
    try {
      localStorage.setItem(GUARDA, JSON.stringify({ ajustes: a, trazos: placa.trazos, rotas: rotas.map((r) => ({ ...r, ensayo: undefined })) }));
    } catch (e) { /* sin almacenamiento, o lleno: la placa sigue en pantalla */ }
  }

  // ------------------------------------------------------------------ la placa y su luz
  const N = Math.min(window.screen.width, window.screen.height) < 700 ? 768 : 1024;
  let placa = new R.Placa({ N, semilla: a.semilla, arrugas: a.arrugas, doble: a.doble });
  if (guardado && Array.isArray(guardado.trazos) && guardado.trazos.length) {
    placa.trazos = guardado.trazos;
    placa.reconstruir();
  }
  const vista = new R.Vista(placa);
  const lienzo = $("#placa");
  lienzo.width = lienzo.height = N;
  const ctx = lienzo.getContext("2d");
  let imagen = new ImageData(vista.rgba, N, N);

  function opcionesVista() {
    const reg = a.luz === "registro";
    return { cara: a.cara, brillante: a.brillante, taller: !reg, sombras: a.sombras, fondo: a.fondo,
      azimut: reg ? REGISTRO.azimut : a.azimut, elevacion: reg ? REGISTRO.elevacion : a.elevacion };
  }

  /* Pintar sin trabarse: lo que cambió se junta y se pinta una vez por cuadro. */
  let sucio = null, todo = true, pedido = 0;
  function pedir(r) {
    if (r) sucio = sucio ? { x0: Math.min(sucio.x0, r.x0), y0: Math.min(sucio.y0, r.y0), x1: Math.max(sucio.x1, r.x1), y1: Math.max(sucio.y1, r.y1) } : { ...r };
    else todo = true;
    if (!pedido) pedido = requestAnimationFrame(pintar);
  }
  function pintar() {
    pedido = 0;
    vista.opciones(opcionesVista());
    let Z = null;
    if (todo) { Z = vista.pintar(); todo = false; sucio = null; }
    else if (sucio) { Z = vista.pintar(sucio); sucio = null; }
    if (Z) ctx.putImageData(imagen, 0, 0, Z.x0, Z.y0, Z.x1 - Z.x0 + 1, Z.y1 - Z.y0 + 1);
  }

  /* Mientras se mueve la luz: la placa a la mitad, que se ilumina rápido; al soltar, entera. */
  const previa = { N: N / 2, mm: LADO / (N / 2), H: new Float32Array(N * N / 4), M: new Float32Array(N * N / 4), rango: () => placa.rango() };
  const vistaPrevia = new R.Vista(previa);
  const lienzoPrevia = document.createElement("canvas");
  lienzoPrevia.width = lienzoPrevia.height = N / 2;
  function pintarPrevia() {
    const n = N / 2, H = placa.H, M = placa.M;
    for (let y = 0; y < n; y++) {
      for (let x = 0; x < n; x++) {
        const j = 2 * y * N + 2 * x;
        previa.H[y * n + x] = (H[j] + H[j + 1] + H[j + N] + H[j + N + 1]) / 4;
        previa.M[y * n + x] = (M[j] + M[j + 1] + M[j + N] + M[j + N + 1]) / 4;
      }
    }
    vistaPrevia.opciones(opcionesVista()).pintar();
    lienzoPrevia.getContext("2d").putImageData(new ImageData(vistaPrevia.rgba, n, n), 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(lienzoPrevia, 0, 0, N, N);
  }
  let pedidoPrevia = 0;
  function pedirPrevia() { if (!pedidoPrevia) pedidoPrevia = requestAnimationFrame(() => { pedidoPrevia = 0; pintarPrevia(); }); }

  // ------------------------------------------------------------------ la cara
  function ponerCara() {
    const rev = a.cara === "reverso";
    $("#cara-nombre").innerHTML = rev ? 'Reverso <small>se trabaja aquí, en espejo</small>' : 'Anverso <small>la letra al derecho, en relieve</small>';
    $("#calco").classList.toggle("espejo", rev);
    pedir();
    pintarBarra();
  }
  function darVuelta() {
    if (dibujando) return;                                   // no se da vuelta la placa con el punzón apoyado
    a.cara = a.cara === "reverso" ? "anverso" : "reverso";
    ponerCara();
    guardar();
  }
  $("#dar-vuelta").addEventListener("click", darVuelta);

  // ------------------------------------------------------------------ el calco
  let calcoImagen = null;
  const svgNS = "http://www.w3.org/2000/svg";
  let base = null;
  function signos() {
    const sel = $("#signo");
    if (!G || !D) {
      sel.disabled = true;
      sel.options[0].textContent = "la gramática no cargó: solo imágenes";
      return;
    }
    for (const c of D.caja) {
      const o = document.createElement("option");
      o.value = c.signo;
      o.textContent = `celda ${c.celda} · ${c.signo} · ${c.estado === "manos" ? "con los dedos" : c.estado}`;
      sel.appendChild(o);
    }
  }
  function pintarCalco() {
    const svg = $("#calco");
    svg.innerHTML = "";
    svg.style.opacity = a.verCalco ? a.calcoOpacidad : 0;
    const nota = $("#calco-nota");
    if (calcoImagen) {
      const im = document.createElementNS(svgNS, "image");
      im.setAttribute("href", calcoImagen);
      im.setAttribute("x", 0); im.setAttribute("y", 0); im.setAttribute("width", LADO); im.setAttribute("height", LADO);
      im.setAttribute("preserveAspectRatio", "xMidYMid meet");
      svg.appendChild(im);
      return;
    }
    if (!a.signo || !G || !D) return;
    const celda = D.caja.find((c) => c.signo === a.signo) || {};
    if (celda.estado === "manos") {
      nota.textContent = "El ¶ no se calca: es el signo final, una placa trabajada solo con los dedos (Acción 7). La máquina no tiene dedos.";
      return;
    }
    nota.textContent = "Por el reverso el calco va en espejo, como en la Acción 4. Del signo de la caja se ve la propuesta de la máquina: lo hallado en línea continua, lo reconstruido a puntos y en violeta, y el desagüe.";
    try {
      if (!base) base = G.preparar(D, {});
      const r = G.construir(base, D, a.signo), k = LADO / D.T;
      const d = r.geo.map((anillo) => "M" + anillo.map(([x, y]) => (x * k).toFixed(2) + "," + (y * k).toFixed(2)).join(" L") + "Z").join(" ");
      const rec = celda.estado === "reconstruida";
      const fondo = document.createElementNS(svgNS, "path");
      fondo.setAttribute("d", d); fondo.setAttribute("fill", "none"); fondo.setAttribute("stroke", PAPEL);
      fondo.setAttribute("stroke-width", "0.9"); fondo.setAttribute("stroke-linejoin", "round"); fondo.setAttribute("opacity", "0.85");
      svg.appendChild(fondo);
      const linea = document.createElementNS(svgNS, "path");
      linea.setAttribute("d", d); linea.setAttribute("fill", "none"); linea.setAttribute("stroke", rec ? VIOLETA : TINTA);
      linea.setAttribute("stroke-width", "0.35"); linea.setAttribute("stroke-linejoin", "round");
      if (rec) { linea.setAttribute("stroke-dasharray", "0.1 1.3"); linea.setAttribute("stroke-linecap", "round"); linea.setAttribute("stroke-width", "0.55"); }
      svg.appendChild(linea);
      for (const [nombre, [x, y]] of r.glifo.marcas) {
        if (nombre !== "desagüe") continue;
        const c = document.createElementNS(svgNS, "circle");
        c.setAttribute("cx", (x * k).toFixed(2)); c.setAttribute("cy", (y * k).toFixed(2)); c.setAttribute("r", R.DESAGUE / 2);
        c.setAttribute("fill", "none"); c.setAttribute("stroke", VIOLETA); c.setAttribute("stroke-width", "0.4");
        svg.appendChild(c);
      }
    } catch (e) {
      nota.textContent = "No se pudo armar ese signo.";
    }
  }
  $("#signo").addEventListener("change", (ev) => {
    a.signo = ev.target.value;
    calcoImagen = null;
    const celda = D && D.caja.find((c) => c.signo === a.signo);
    if (celda && celda.estado === "reconstruida" && a.herramienta === "repasar") {
      aviso("Ese signo es reconstruido: va a puntos (Puntear).");
    }
    pintarCalco();
    guardar();
  });
  $("#imagen-calco").addEventListener("change", (ev) => {
    const f = ev.target.files && ev.target.files[0];
    if (!f) return;
    const lector = new FileReader();
    lector.onload = () => { calcoImagen = lector.result; a.verCalco = true; $("#ver-calco").checked = true; pintarCalco(); };
    lector.readAsDataURL(f);
    ev.target.value = "";
  });
  $("#sin-calco").addEventListener("click", () => { calcoImagen = null; a.signo = ""; $("#signo").value = ""; pintarCalco(); guardar(); });
  $("#ver-calco").addEventListener("change", (ev) => { a.verCalco = ev.target.checked; pintarCalco(); guardar(); });

  // ------------------------------------------------------------------ la mano
  const marco = $("#marco"), caja = $("#lienzo"), guia = $("#guia");
  let dibujando = false, ultimo = null, velocidad = 0, inicio = null, recorrido = 0, t0 = 0, puntero = null, quietoT = 0;

  /* La pantalla no es el aluminio: si la mano se queda quieta apretando, el punzón descansa y hunde un poco
   * más (una vez por cada parada). El resto del pulso es el tuyo. */
  function esperarQuieta() {
    clearTimeout(quietoT);
    quietoT = setTimeout(() => {
      if (!dibujando || !ultimo || a.herramienta !== "repasar") return;
      pedir(placa.agregar(ultimo.q[0], ultimo.q[1], ultimo.p, performance.now() - t0, true));
    }, 350);
  }

  function aPlaca(ev) {
    const r = caja.getBoundingClientRect();
    let x = ((ev.clientX - r.left) / r.width) * LADO;
    const y = ((ev.clientY - r.top) / r.height) * LADO;
    if (a.cara === "reverso") x = LADO - x;
    return [x, y];
  }
  const aVista = (x) => (a.cara === "reverso" ? LADO - x : x);

  function presion(ev, q, t) {
    if (a.presion === "tableta" && ev.pointerType === "pen" && ev.pressure > 0) return 0.25 + 0.75 * ev.pressure;
    if (a.presion === "pareja") return 0.8;
    if (ultimo) {
      const dt = Math.max(4, t - ultimo.t), v = (Math.hypot(q[0] - ultimo.q[0], q[1] - ultimo.q[1]) / dt) * 1000;
      velocidad = 0.8 * velocidad + 0.2 * v;
    }
    return Math.max(0.35, Math.min(1, 1.05 - velocidad / 220));             // mm/s: despacio hunde más
  }

  /* El pie de la herramienta, bajo el puntero, y el desagüe cuando el contorno vuelve a su principio. */
  function pintarGuia() {
    let s = "";
    if (puntero) {
      const r = a.herramienta === "rellenar" || a.herramienta === "alisar" ? a.radio : (R.PUNZONES[a.punzon] || R.PUNZONES.bola).radio * 2.2;
      s += `<circle cx="${aVista(puntero[0]).toFixed(2)}" cy="${puntero[1].toFixed(2)}" r="${r.toFixed(2)}" fill="none" stroke="${PAPEL}" stroke-width="0.5" opacity="0.9"/>` +
        `<circle cx="${aVista(puntero[0]).toFixed(2)}" cy="${puntero[1].toFixed(2)}" r="${r.toFixed(2)}" fill="none" stroke="${TINTA}" stroke-width="0.25"/>`;
    }
    if (dibujando && inicio && (a.herramienta === "repasar" || a.herramienta === "puntear") && recorrido > 5 * R.DESAGUE && puntero &&
        Math.hypot(puntero[0] - inicio[0], puntero[1] - inicio[1]) < 12) {
      s += `<circle cx="${aVista(inicio[0]).toFixed(2)}" cy="${inicio[1].toFixed(2)}" r="${R.DESAGUE}" fill="none" stroke="${VIOLETA}" stroke-width="0.45" stroke-dasharray="0.8 0.6"/>` +
        `<text x="${(aVista(inicio[0]) + R.DESAGUE + 1).toFixed(2)}" y="${(inicio[1] + 1).toFixed(2)}" font-family="Courier Prime, monospace" font-size="3" fill="${VIOLETA}" stroke="${PAPEL}" stroke-width="0.6" paint-order="stroke">desagüe: 3 mm</text>`;
    }
    guia.innerHTML = s;
  }

  caja.addEventListener("pointerdown", (ev) => {
    if (ev.pointerType === "mouse" && ev.button !== 0) return;
    ev.preventDefault();
    caja.setPointerCapture(ev.pointerId);
    dibujando = true; ultimo = null; velocidad = 55; recorrido = 0; t0 = ev.timeStamp;   // se apoya con presión media (0,8)
    const q = aPlaca(ev), p = presion(ev, q, ev.timeStamp);
    inicio = q; puntero = q;
    placa.empezar({ herramienta: a.herramienta, cara: a.cara, punzon: a.punzon, base: a.base, fuerza: a.fuerza, temblor: a.temblor,
      radio: a.radio, puntos: [] });
    pedir(placa.agregar(q[0], q[1], p, 0));
    ultimo = { q, p, t: ev.timeStamp };
    esperarQuieta();
    pintarGuia();
  });
  caja.addEventListener("pointermove", (ev) => {
    const evs = dibujando && ev.getCoalescedEvents ? ev.getCoalescedEvents() : [ev];
    for (const e of evs.length ? evs : [ev]) {
      const q = aPlaca(e);
      puntero = q;
      if (!dibujando) continue;
      if (ultimo && Math.hypot(q[0] - ultimo.q[0], q[1] - ultimo.q[1]) < 0.15) continue;
      const p = presion(e, q, e.timeStamp);
      if (ultimo) recorrido += Math.hypot(q[0] - ultimo.q[0], q[1] - ultimo.q[1]);
      pedir(placa.agregar(q[0], q[1], p, e.timeStamp - t0));
      ultimo = { q, p, t: e.timeStamp };
      esperarQuieta();
    }
    pintarGuia();
  });
  function soltar() {
    if (!dibujando) return;
    dibujando = false;
    clearTimeout(quietoT);
    const r = placa.terminar();
    if (r && r.sucio) pedir(r.sucio);
    if (r && r.cerrado) aviso("Ese contorno se cerró: le falta el desagüe. El punzón se detiene 3 mm antes de cerrar (03b, regla 2).");
    if (r && r.roturas) aviso("La hoja se rompió. La placa rota no se tira: va a la ficha y a la caja, junto a la que se haga después (Acción 4).");
    pintarRegistro();
    pintarGuia();
    guardar();
  }
  caja.addEventListener("pointerup", soltar);
  caja.addEventListener("pointercancel", soltar);
  caja.addEventListener("pointerleave", () => { if (!dibujando) { puntero = null; pintarGuia(); } });

  // ------------------------------------------------------------------ los controles
  function botonera(sel, clave, valor, alElegir) {
    for (const b of document.querySelectorAll(`${sel} button`)) {
      b.setAttribute("aria-pressed", b.dataset[clave] === valor ? "true" : "false");
      if (!b._listo) { b._listo = true; b.addEventListener("click", () => alElegir(b.dataset[clave])); }
    }
  }
  function elegirHerramienta(h) {
    a.herramienta = h;
    botonera("#herramientas", "h", h, elegirHerramienta);
    $("#herramienta-que").textContent = HERRAMIENTAS[h];
    const ancha = h === "rellenar" || h === "alisar";
    $("#campo-radio").classList.toggle("oculto", !ancha);
    $("#campo-punzon").classList.toggle("oculto", ancha);
    pintarBarra();
    guardar();
  }
  function elegirLuz(l) {
    a.luz = l;
    botonera("#luces", "luz", l, elegirLuz);
    $("#luz-que").textContent = LUCES[l];
    const reg = l === "registro";
    $("#azimut").disabled = $("#elevacion").disabled = reg;
    pintarLuz();
    pedir();
    guardar();
  }
  function pintarLuz() {
    const reg = a.luz === "registro", az = reg ? REGISTRO.azimut : a.azimut, el = reg ? REGISTRO.elevacion : a.elevacion;
    $("#azimut").value = az; $("#elevacion").value = el;
    const lado = (g) => ["la derecha", "arriba a la derecha", "arriba", "arriba a la izquierda", "la izquierda", "abajo a la izquierda", "abajo", "abajo a la derecha"][Math.round(((g % 360) + 360) % 360 / 45) % 8];
    $("#azimut-v").textContent = `desde ${lado(az)} · ${az}°`;
    $("#elevacion-v").textContent = `${el}°${el <= 20 ? " · rasante" : ""}`;
  }

  function rango(id, clave, texto, alMover, alSoltar) {
    const el = $("#" + id);
    el.value = a[clave];
    const mostrar = () => { const o = $("#" + id + "-v"); if (o) o.textContent = texto(+el.value); };
    mostrar();
    el.addEventListener("input", () => { a[clave] = +el.value; mostrar(); if (alMover) alMover(); });
    el.addEventListener("change", () => { a[clave] = +el.value; mostrar(); if (alSoltar) alSoltar(); guardar(); });
  }
  function lista(id, clave, alCambiar) {
    const el = $("#" + id);
    el.value = String(a[clave]);
    el.addEventListener("change", () => { a[clave] = el.value; if (alCambiar) alCambiar(); guardar(); });
  }

  for (const [k, p] of Object.entries(R.PUNZONES)) $("#punzon").add(new Option(p.nombre, k));
  for (const [k, b] of Object.entries(R.BASES)) $("#base").add(new Option(b.nombre, k));
  lista("punzon", "punzon", pintarBarra);
  lista("base", "base", pintarBarra);
  lista("presion", "presion", pintarBarra);
  lista("brillante", "brillante", () => pedir());
  lista("fondo", "fondo", () => pedir());
  lista("mano", "mano", pintarRegistro);
  lista("tamano", "tamano");
  lista("zoom", "zoom", ponerZoom);
  rango("fuerza", "fuerza", (v) => "×" + coma(v, 2));
  rango("temblor", "temblor", (v) => (v < 0.15 ? "pareja" : v < 0.6 ? "la de siempre" : "temblorosa") + " · " + coma(v, 2));
  rango("radio", "radio", (v) => coma(v) + " mm");
  rango("calco-opacidad", "calcoOpacidad", (v) => Math.round(v * 100) + " %", pintarCalco);
  rango("arrugas", "arrugas", (v) => (v < 0.15 ? "recién salida del rollo" : v < 0.6 ? "alisada con la mano" : "arrugada") + " · " + coma(v, 2), null, () => nuevaHoja(a.semilla));
  rango("azimut", "azimut", () => "", () => { pintarLuz(); pedirPrevia(); }, () => { pintarLuz(); pedir(); });
  rango("elevacion", "elevacion", () => "", () => { pintarLuz(); pedirPrevia(); }, () => { pintarLuz(); pedir(); });
  $("#sombras").checked = a.sombras;
  $("#sombras").addEventListener("change", (ev) => { a.sombras = ev.target.checked; pedir(); guardar(); });
  $("#doble").checked = a.doble;
  $("#doble").addEventListener("change", (ev) => { a.doble = ev.target.checked; nuevaHoja(a.semilla); });
  $("#ver-calco").checked = a.verCalco;

  function ponerZoom() {
    caja.style.width = +a.zoom > 1 ? (100 * +a.zoom) + "%" : "min(100%, calc(100vh - 170px))";
    caja.style.margin = +a.zoom > 1 ? "0" : "0 auto";
  }

  // ------------------------------------------------------------------ la hoja, deshacer, empezar otra
  function rehacerPlaca(p) {
    placa = p;
    vista.usar(placa);
    imagen = new ImageData(vista.rgba, N, N);
    pedir();
    pintarRegistro();
    pintarBarra();
  }
  function nuevaHoja(semilla) {
    a.semilla = semilla;
    nota("Cortando la hoja…");
    setTimeout(() => {
      const p = new R.Placa({ N, semilla, arrugas: a.arrugas, doble: a.doble });
      p.trazos = placa.trazos;
      p.reconstruir();
      rehacerPlaca(p);
      nota("");
      guardar();
    }, 20);
  }
  $("#hoja-nueva").addEventListener("click", () => nuevaHoja(String(Math.floor(Math.random() * 1e6))));
  $("#deshacer").addEventListener("click", deshacer);
  $("#rehacer").addEventListener("click", rehacer);
  function deshacer() { if (placa.deshacer()) { pedir(); pintarRegistro(); guardar(); } }
  function rehacer() { if (placa.rehacer()) { pedir(); pintarRegistro(); guardar(); } }
  /* Empezar otra placa borra la que está: se pide un segundo clic (el visor de claude.ai no muestra confirm()). */
  let armado = 0;
  $("#empezar").addEventListener("click", () => {
    const b = $("#empezar");
    if (placa.trazos.length && !armado) {
      b.textContent = "¿Seguro? Se borra esta placa";
      armado = setTimeout(() => { armado = 0; b.textContent = "Empezar otra placa"; }, 4000);
      return;
    }
    clearTimeout(armado);
    armado = 0;
    b.textContent = "Empezar otra placa";
    nuevaHojaVacia();
  });
  function nuevaHojaVacia() {
    a.semilla = String(Math.floor(Math.random() * 1e6));
    rehacerPlaca(new R.Placa({ N, semilla: a.semilla, arrugas: a.arrugas, doble: a.doble }));
    guardar();
  }
  $("#guardar-rota").addEventListener("click", () => {
    const mini = document.createElement("canvas");
    mini.width = mini.height = 128;
    mini.getContext("2d").drawImage(lienzo, 0, 0, 128, 128);
    rotas.push({ miniatura: mini.toDataURL("image/jpeg", 0.8), roturas: placa.roturas.length, ensayo: placa.aJSON() });
    nuevaHojaVacia();
    pintarRegistro();
    aviso("La rota quedó guardada. Esta es la que se hizo después.");
  });

  // ------------------------------------------------------------------ el registro y la barra
  function pintarRegistro() {
    const r = placa.registro();
    const filas = [
      ["trazos", r.trazos + (r.trazos ? ` (${r.reverso} por el reverso, ${r.anverso} por el anverso)` : "")],
      ["surco continuo", coma(r.surco, 0) + " mm"],
      ["punteado", r.puntos ? `${coma(r.punteado, 0)} mm · ${r.puntos} puntos` : "—"],
      ["relleno y alisado", r.relleno + r.alisado ? coma(r.relleno + r.alisado, 0) + " mm de recorrido" : "—"],
      ["contornos sin desagüe", String(r.sinDesague)],
      ["roturas", String(r.roturas)],
      ["tiempo, a mano", r.trazos ? `unos ${Math.round(r.minutos)} min` : "—"],
    ];
    $("#registro").innerHTML = filas.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
    $("#acciones-rota").hidden = !r.roturas;
    $("#rotas").innerHTML = rotas.map((x, i) => x.miniatura ? `<img src="${x.miniatura}" alt="Placa rota ${i + 1}" title="Placa rota ${i + 1}: ${x.roturas} rotura(s)">` : "").join("");
    $("#deshacer").disabled = !placa.trazos.length;
    $("#rehacer").disabled = !placa.deshechos.length;
  }
  function pintarBarra() {
    const nombres = { velocidad: "velocidad", tableta: "tableta", pareja: "pareja" };
    $("#barra").innerHTML = [
      `presión: <b>${nombres[a.presion]}</b>`,
      `<b>${a.herramienta}</b>`,
      `<b>${a.cara}</b>`,
      `${(R.PUNZONES[a.punzon] || R.PUNZONES.bola).nombre} · ${(R.BASES[a.base] || R.BASES.fieltro).nombre}`,
      `placa de ${LADO} mm · ${N} px`,
    ].join("<span aria-hidden=\"true\"> · </span>");
  }
  let avisoT = 0;
  function aviso(texto) { const n = $("#aviso"); n.textContent = texto; clearTimeout(avisoT); avisoT = setTimeout(() => { n.textContent = ""; }, 9000); }
  function nota(texto) { $("#nota").textContent = texto; }

  // ------------------------------------------------------------------ las salidas
  /* Fuera de claude.ai, la descarga es un enlace. Dentro del visor se usa la capacidad «downloads»; si no está,
   * el texto queda a la vista para copiarlo. */
  const enVisor = !!(window.claude && typeof window.claude.use === "function");
  const pedirDescargas = enVisor ? window.claude.use("downloads").catch(() => null) : Promise.resolve(null);
  async function bajar(nombre, tipo, datos) {
    const descargas = await pedirDescargas;
    if (descargas) {
      try { await descargas.save({ filename: nombre, data: datos }); nota(`${nombre}: guardado.`); }
      catch (e) { nota(e && e.code === "declined" ? "Descarga cancelada." : "No se pudo descargar."); }
      return;
    }
    if (enVisor) {
      if (typeof datos === "string") { $("#salida").hidden = false; $("#salida-texto").value = datos; nota(`${nombre}: cópialo.`); }
      else nota("Aquí no se puede descargar una imagen.");
      return;
    }
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(new Blob([datos], { type: tipo }));
    enlace.download = nombre;
    document.body.appendChild(enlace);
    enlace.click();
    setTimeout(() => { URL.revokeObjectURL(enlace.href); enlace.remove(); }, 800);
    nota(`${nombre}: descargado.`);
  }
  const procedencia = (que) => ({
    Title: `Contenida · ${que}`,
    Author: "la mano, con la máquina",
    Description: `Ensayo de repujado: placa de ${LADO} mm, papel de aluminio de cocina${placa.hoja.doble ? " doble" : ""}, ` +
      `${(R.BASES[a.base] || R.BASES.fieltro).nombre}. ${placa.trazos.length} trazos, con la mano ${a.mano}.`,
    Comment: "Simulación: la propuesta de la máquina. No entra en la caja ni en la fuente (06, §6.3).",
    Software: "tipografia/repujado (Contenida). La manera de dibujar, tomada de Vooolume (Krftoools).",
  });
  async function aPng(canvas, campos) {
    const blob = await new Promise((ok) => canvas.toBlob(ok, "image/png"));
    const bytes = new Uint8Array(await blob.arrayBuffer());
    return R.pngConTexto(bytes, campos);
  }
  /* La placa a otro tamaño: se rehace desde la hoja, trazo por trazo. */
  function placaGrande(n) {
    if (n === N) return placa;
    const p = new R.Placa({ N: n, semilla: placa.hoja.semilla, arrugas: placa.hoja.arrugas, doble: placa.hoja.doble });
    p.trazos = placa.trazos;
    p.reconstruir();
    return p;
  }
  function render(p, opciones) {
    const v = new R.Vista(p).opciones(opciones);
    v.pintar();
    const c = document.createElement("canvas");
    c.width = c.height = p.N;
    c.getContext("2d").putImageData(new ImageData(v.rgba, p.N, p.N), 0, 0);
    return c;
  }
  const nombreBase = () => `contenida_repujado${a.signo ? "_" + a.signo.codePointAt(0).toString(16) : ""}`;
  $("#png-cara").addEventListener("click", () => {
    nota("Rehaciendo la placa a " + a.tamano + " px…");
    setTimeout(async () => {
      const p = placaGrande(+a.tamano);
      const c = render(p, opcionesVista());
      await bajar(`${nombreBase()}_${a.cara}_${p.N}.png`, "image/png", await aPng(c, procedencia(`placa simulada, ${a.cara}`)));
    }, 30);
  });
  $("#png-registro").addEventListener("click", () => {
    nota("La foto del registro: las dos caras, con la lámpara fija…");
    setTimeout(async () => {
      const p = placaGrande(+a.tamano), n = p.N, margen = Math.round(n * 0.04), pie = Math.round(n * 0.09);
      const op = { brillante: a.brillante, taller: false, sombras: true, fondo: "fieltro", azimut: REGISTRO.azimut, elevacion: REGISTRO.elevacion };
      const anv = render(p, { ...op, cara: "anverso" }), rev = render(p, { ...op, cara: "reverso" });
      const c = document.createElement("canvas");
      c.width = 2 * n + 3 * margen; c.height = n + 2 * margen + pie;
      const g = c.getContext("2d");
      g.fillStyle = PAPEL; g.fillRect(0, 0, c.width, c.height);
      g.drawImage(anv, margen, margen); g.drawImage(rev, 2 * margen + n, margen);
      g.fillStyle = TINTA;
      g.font = `${Math.round(pie * 0.32)}px "Courier Prime", monospace`;
      g.fillText("anverso", margen, n + margen + pie * 0.42);
      g.fillText("reverso", 2 * margen + n, n + margen + pie * 0.42);
      g.fillStyle = "#6d6a63";
      g.font = `${Math.round(pie * 0.24)}px "Courier Prime", monospace`;
      g.fillText(`luz rasante: ${REGISTRO.elevacion}° desde la izquierda · placa de ${LADO} mm · simulación: no entra en la caja ni en la fuente`, margen, n + margen + pie * 0.8);
      await bajar(`${nombreBase()}_registro_${n}.png`, "image/png", await aPng(c, procedencia("la foto del registro (simulada)")));
    }, 30);
  });
  $("#json").addEventListener("click", () => {
    const o = placa.aJSON();
    o.fecha = new Date().toISOString().slice(0, 10);
    o.mano = a.mano;
    o.calco = a.signo ? { signo: a.signo } : calcoImagen ? { imagen: "una imagen propia (no se guarda)" } : null;
    o.rotas = rotas.filter((r) => r.ensayo).map((r) => r.ensayo);
    bajar(`${nombreBase()}.json`, "application/json", JSON.stringify(o) + "\n");
  });
  $("#abrir-json").addEventListener("change", (ev) => {
    const f = ev.target.files && ev.target.files[0];
    if (!f) return;
    f.text().then((t) => {
      try {
        const o = JSON.parse(t);
        nota("Rehaciendo el ensayo…");
        setTimeout(() => {
          const p = R.Placa.deJSON(o, N);
          a.semilla = p.hoja.semilla; a.arrugas = p.hoja.arrugas; a.doble = p.hoja.doble;
          $("#arrugas").value = a.arrugas; $("#doble").checked = a.doble;
          if (o.mano) { a.mano = o.mano; $("#mano").value = o.mano; }
          if (o.calco && o.calco.signo) { a.signo = o.calco.signo; $("#signo").value = a.signo; pintarCalco(); }
          rehacerPlaca(p);
          nota(`${p.trazos.length} trazos.`);
          guardar();
        }, 20);
      } catch (e) { nota("Ese archivo no es un ensayo."); }
    });
    ev.target.value = "";
  });

  // ------------------------------------------------------------------ el teclado
  document.addEventListener("keydown", (ev) => {
    if (ev.target.closest && ev.target.closest("input, select, textarea")) return;
    const k = ev.key.toLowerCase();
    if ((ev.ctrlKey || ev.metaKey) && k === "z") { ev.preventDefault(); if (ev.shiftKey) rehacer(); else deshacer(); return; }
    if ((ev.ctrlKey || ev.metaKey) && k === "y") { ev.preventDefault(); rehacer(); return; }
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (k === " ") { ev.preventDefault(); darVuelta(); }
    else if (k >= "1" && k <= "4") elegirHerramienta(["repasar", "puntear", "rellenar", "alisar"][+k - 1]);
    else if (k === "c") { a.verCalco = !a.verCalco; $("#ver-calco").checked = a.verCalco; pintarCalco(); }
    else if (k === "l") elegirLuz(a.luz === "taller" ? "registro" : "taller");
  });

  // ------------------------------------------------------------------ arrancar
  signos();
  $("#signo").value = a.signo;
  elegirHerramienta(a.herramienta);
  elegirLuz(a.luz);
  $("#fondo").value = a.fondo;
  ponerZoom();
  ponerCara();
  pintarCalco();
  pintarRegistro();
  pintarBarra();
  pedir();
})();
