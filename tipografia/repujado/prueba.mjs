/* Pruebas del motor del repujado, sin navegador.
 *
 *   node tipografia/repujado/prueba.mjs [--imagenes CARPETA]
 *
 * Comprueba que la placa sale siempre igual (el azar tiene semilla), que el reverso es el anverso dado vuelta,
 * que el punzón por el reverso levanta el anverso y por el anverso lo hunde, que rehacer da lo mismo que dibujar,
 * que el punteado rompe más que el surco, que la mano quieta hunde un poco más, que la mano simulada (pulso.js)
 * sale siempre igual y que la luz se calcula en un tiempo razonable. Con --imagenes CARPETA guarda las muestras
 * del README: la a y la ó de la gramática, repujadas por la mano simulada, por las dos caras.
 */
import { createRequire } from "node:module";
import { deflateSync } from "node:zlib";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import assert from "node:assert/strict";

const require = createRequire(import.meta.url);
const R = require("./repujado.js");
const Pulso = require("./pulso.js");

let fallas = 0;
function prueba(nombre, f) {
  const t0 = performance.now();
  try { f(); console.log(`  ok  ${nombre} (${Math.round(performance.now() - t0)} ms)`); }
  catch (e) { fallas++; console.log(`  MAL ${nombre}: ${e.message}`); }
}

/* Un contorno como el de una o, recorrido a mano: se detiene 3 mm antes de cerrar (el desagüe). */
function contorno(cx, cy, rx, ry, desague = 3, paso = 0.6, p = 0.8) {
  const pts = [];
  let s = 0, prev = null;
  for (let i = 0; i <= 4000; i++) {
    const a = -Math.PI / 2 + 2 * Math.PI * (i / 4000), q = [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
    if (prev) s += Math.hypot(q[0] - prev[0], q[1] - prev[1]);
    prev = q;
    if (s > 20 && Math.hypot(q[0] - pts[0][0], q[1] - pts[0][1]) < desague + 0.05) break;     // se detiene antes de cerrar
    if (!pts.length || s >= pts.length * paso) pts.push([q[0], q[1], p, pts.length * 16]);
  }
  return pts;
}
const huella = (a) => { let h = 0; for (let i = 0; i < a.length; i += 3) h = (h * 31 + Math.round(a[i] * 1e4)) | 0; return h; };
function dibujar(placa, t) {
  const [primero, ...resto] = t.puntos;
  placa.empezar({ ...t, puntos: [primero] });
  for (const q of resto) placa.agregar(q[0], q[1], q[2], q[3], !!q[4]);
  return placa.terminar();
}

console.log("El repujado: pruebas del motor");

prueba("la hoja sale siempre igual", () => {
  const a = new R.Placa({ N: 256, semilla: "7" }), b = new R.Placa({ N: 256, semilla: "7" }), c = new R.Placa({ N: 256, semilla: "8" });
  assert.equal(huella(a.H), huella(b.H));
  assert.notEqual(huella(a.H), huella(c.H));
  let dentro = 0;
  for (let j = 0; j < a.M.length; j++) dentro += a.M[j];
  const area = dentro * a.mm * a.mm;
  assert.ok(area > 120 * 120 && area < 150 * 150, `área de la hoja ${area.toFixed(0)} mm²`);
});

prueba("el punzón por el reverso levanta el anverso; por el anverso, lo hunde", () => {
  const p = new R.Placa({ N: 300, semilla: "1", arrugas: 0 });
  dibujar(p, { herramienta: "repasar", cara: "reverso", punzon: "bola", base: "fieltro", puntos: [[40, 75, 0.8, 0], [110, 75, 0.8, 500]] });
  const j = Math.floor(75 / p.mm) * p.N + Math.floor(75 / p.mm);
  assert.ok(p.R[j] > 0.5 && p.R[j] < 1.2, `relieve ${p.R[j].toFixed(3)} mm`);
  dibujar(p, { herramienta: "repasar", cara: "anverso", punzon: "bola", base: "fieltro", puntos: [[75, 30, 0.8, 0], [75, 50, 0.8, 300]] });
  const k = Math.floor(40 / p.mm) * p.N + Math.floor(75 / p.mm);
  assert.ok(p.R[k] < -0.5, `hundido ${p.R[k].toFixed(3)} mm`);
});

prueba("rehacer da lo mismo que dibujar, y deshacer vuelve atrás", () => {
  const p = new R.Placa({ N: 256, semilla: "3" });
  const antes = huella(p.H);
  dibujar(p, { herramienta: "repasar", cara: "reverso", punzon: "bola", base: "fieltro", puntos: contorno(75, 75, 30, 40) });
  dibujar(p, { herramienta: "puntear", cara: "reverso", punzon: "bola", base: "fieltro", puntos: contorno(75, 75, 15, 20) });
  dibujar(p, { herramienta: "rellenar", cara: "reverso", base: "fieltro", radio: 3, puntos: [[60, 60, 0.8, 0], [90, 90, 0.8, 400]] });
  dibujar(p, { herramienta: "alisar", cara: "anverso", radio: 4, puntos: [[20, 120, 0.8, 0], [130, 120, 0.8, 600]] });
  const dibujado = huella(p.H), registro = p.registro();
  p.reconstruir();
  assert.equal(huella(p.H), dibujado);
  const q = R.Placa.deJSON(JSON.parse(JSON.stringify(p.aJSON())), 256);
  assert.equal(huella(q.H), dibujado);
  assert.deepEqual(q.registro(), registro);
  for (let i = 0; i < 4; i++) p.deshacer();
  assert.equal(huella(p.H), antes);
  for (let i = 0; i < 4; i++) p.rehacer();
  assert.equal(huella(p.H), dibujado);
});

prueba("el reverso es el anverso dado vuelta", () => {
  const p = new R.Placa({ N: 200, semilla: "4" });
  dibujar(p, { herramienta: "repasar", cara: "reverso", puntos: [[30, 40, 0.9, 0], [70, 100, 0.9, 400]] });
  const v = new R.Vista(p);
  v.opciones({ cara: "anverso" }).pintar();
  const anv = Float32Array.from(v.V);
  v.opciones({ cara: "reverso" }).pintar();
  const N = p.N;
  for (const [x, y] of [[10, 10], [57, 80], [120, 33], [199, 199]]) assert.equal(v.V[y * N + (N - 1 - x)], -anv[y * N + x]);
});

prueba("el contorno que se cierra no tiene desagüe", () => {
  const p = new R.Placa({ N: 200, semilla: "5" });
  assert.equal(dibujar(p, { herramienta: "repasar", cara: "reverso", puntos: contorno(75, 75, 20, 30, 3) }).cerrado, false);
  assert.equal(dibujar(p, { herramienta: "repasar", cara: "reverso", puntos: contorno(75, 75, 40, 50, 0) }).cerrado, true);
  assert.equal(p.registro().sinDesague, 1);
});

prueba("el punteado rompe más que el surco", () => {
  let surco = 0, punteado = 0;
  for (let s = 0; s < 60; s++) {
    const a = new R.Placa({ N: 128, semilla: "r" + s }), b = new R.Placa({ N: 128, semilla: "r" + s });
    dibujar(a, { herramienta: "repasar", cara: "reverso", puntos: contorno(75, 75, 35, 45) });
    dibujar(b, { herramienta: "puntear", cara: "reverso", puntos: contorno(75, 75, 35, 45) });
    surco += a.roturas.length > 0; punteado += b.roturas.length > 0;
  }
  console.log(`       placas rotas de 60: surco ${surco}, punteado ${punteado}`);
  assert.ok(punteado > surco, "el punteado debería romper más");
});

prueba("pasar muchas veces por el mismo surco termina rompiendo", () => {
  let rotas = 0;
  for (let s = 0; s < 20; s++) {
    const p = new R.Placa({ N: 128, semilla: "f" + s });
    for (let k = 0; k < 8; k++) dibujar(p, { herramienta: "repasar", cara: "reverso", fuerza: 1.3, puntos: contorno(75, 75, 35, 45) });
    rotas += p.roturas.length > 0;
  }
  console.log(`       placas rotas de 20, con ocho pasadas fuertes: ${rotas}`);
  assert.ok(rotas >= 5);
});

prueba("la mano quieta, apretando, hunde un poco más (y rehacer lo repite)", () => {
  function hacer(duda) {
    const p = new R.Placa({ N: 300, semilla: "q", arrugas: 0 }), puntos = [];
    for (let x = 30; x <= 120; x += 0.5) {
      puntos.push([x, 75, 0.8, x * 20]);
      if (duda && x === 75) puntos.push([x, 75, 0.8, x * 20 + 400, 1]);          // se detiene a la mitad
    }
    dibujar(p, { herramienta: "repasar", cara: "reverso", puntos });
    return p;
  }
  const sin = hacer(false), con = hacer(true), j = Math.floor(75 / sin.mm) * sin.N + Math.floor(75 / sin.mm);
  assert.ok(con.R[j] > 1.02 * sin.R[j], `con la duda ${con.R[j].toFixed(3)} mm, sin ella ${sin.R[j].toFixed(3)} mm`);
  assert.ok(con.R[j] < 1.25 * sin.R[j], "la duda es sutil");
  const antes = huella(con.H);
  con.reconstruir();
  assert.equal(huella(con.H), antes);
  assert.equal(huella(R.Placa.deJSON(JSON.parse(JSON.stringify(con.aJSON())), 300).H), antes);
});

prueba("la mano simulada sale siempre igual, levanta y se cansa", () => {
  const cam = [];
  for (let i = 0; i <= 400; i++) { const a = -Math.PI / 2 + 1.94 * Math.PI * (i / 400); cam.push([75 + 30 * Math.cos(a), 75 + 40 * Math.sin(a)]); }
  const una = Pulso.trazar(cam, { oficio: "repujar", lado: "las dos" }, R.azar("mano", 1));
  const otra = Pulso.trazar(cam, { oficio: "repujar", lado: "las dos" }, R.azar("mano", 1));
  assert.deepEqual(una, otra);
  assert.ok(una.resumen.levantadas >= 1, "un contorno largo se hace en tramos");
  const cansada = Pulso.trazar(cam, { oficio: "repujar", lado: "las dos", minutos: 110 }, R.azar("mano", 1));
  assert.ok(cansada.resumen.segundos > una.resumen.segundos, "cansada va más lento");
  let lejos = 0;
  for (const t of una.tramos) for (const [x, y] of t.puntos) lejos = Math.max(lejos, Math.abs(Math.hypot((x - 75) / 30, (y - 75) / 40) - 1) * 30);
  assert.ok(lejos < 0.8, `se aparta de la línea ${lejos.toFixed(2)} mm: sutil`);
});

let placa, vista;
prueba("una placa de 1024 px: la hoja, una letra y la luz", () => {
  let t0 = performance.now();
  placa = new R.Placa({ N: 1024, semilla: "1", arrugas: 0.55 });
  const tHoja = performance.now() - t0;
  t0 = performance.now();
  dibujar(placa, { herramienta: "repasar", cara: "reverso", puntos: contorno(75, 72, 34, 44) });
  dibujar(placa, { herramienta: "repasar", cara: "reverso", puntos: contorno(75, 72, 17, 26) });
  dibujar(placa, { herramienta: "puntear", cara: "reverso", puntos: [[75, 122, 0.8, 0], [75, 140, 0.8, 300]] });
  dibujar(placa, { herramienta: "rellenar", cara: "reverso", radio: 2.5, puntos: contorno(75, 72, 25.5, 35, 5, 1.2) });
  dibujar(placa, { herramienta: "repasar", cara: "anverso", punzon: "boligrafo", puntos: [[20, 20, 0.7, 0], [60, 24, 0.6, 400], [130, 18, 0.7, 900]] });
  const tTrazos = performance.now() - t0;
  vista = new R.Vista(placa);
  t0 = performance.now();
  vista.opciones({ cara: "anverso" }).pintar();
  const tLuz = performance.now() - t0;
  t0 = performance.now();
  const s = placa.empezar({ herramienta: "repasar", cara: "anverso", puntos: [[100, 130, 0.8, 0]] });
  const r = placa.agregar(103, 131, 0.8, 16);
  vista.pintar(r || s);
  placa.terminar();
  const tTrazo = performance.now() - t0;
  console.log(`       hoja ${tHoja.toFixed(0)} ms · cinco trazos ${tTrazos.toFixed(0)} ms · luz entera ${tLuz.toFixed(0)} ms · un tramo y su luz ${tTrazo.toFixed(1)} ms`);
  assert.ok(tLuz < 2000);
});

const i = process.argv.indexOf("--imagenes");
if (i > 0 && fallas === 0) {
  /* Muestras para el README: la a (hallada, surco continuo) y la ó (reconstruida, a puntos), repujadas sobre el
   * calco de la gramática por la mano simulada (pulso.js): en tramos, con dudas, con las dos manos. Trabaja por
   * el reverso, en espejo. Son muestras de la herramienta, no placas. */
  const dir = process.argv[i + 1];
  mkdirSync(dir, { recursive: true });
  globalThis.window = globalThis;
  globalThis.ClipperLib = require("../aplicacion/clipper.js");
  require("../aplicacion/datos.js");
  require("../aplicacion/gramatica.js");
  const G = globalThis.Gramatica, D = globalThis.DATOS, base = G.preparar(D, {});
  const espejo = (q) => q.map(([x, y, ...resto]) => [R.LADO - x, y, ...resto]);
  function repasar(placa, signo, herramienta) {
    G.construir(base, D, signo).geo.map((a) => a.map(([x, y]) => [x / 4, y / 4])).forEach((anillo, k) => {
      let L = 0;
      const pts = [anillo[0]];
      for (let j = 1; j < anillo.length; j++) {
        L += Math.hypot(anillo[j][0] - anillo[j - 1][0], anillo[j][1] - anillo[j - 1][1]);
        if (L > 20 && Math.hypot(anillo[j][0] - anillo[0][0], anillo[j][1] - anillo[0][1]) < 3.2) break;   // el desagüe
        pts.push(anillo[j]);
      }
      const mano = { oficio: herramienta === "puntear" ? "puntear" : "repujar", lado: "las dos", minutos: 0 };
      for (const tramo of Pulso.trazar(espejo(pts), mano, R.azar("muestra", signo, k)).tramos)
        dibujar(placa, { herramienta, cara: "reverso", punzon: "bola", base: "fieltro", puntos: espejo(Pulso.puntosDe(tramo)) });
    });
  }
  const png = (rgba, W, H) => {
    const fila = W * 4 + 1, crudo = Buffer.alloc(fila * H);
    for (let y = 0; y < H; y++) { crudo[y * fila] = 0; Buffer.from(rgba.buffer, rgba.byteOffset + y * W * 4, W * 4).copy(crudo, y * fila + 1); }
    const trozo = (tipo, datos) => {
      const t = Buffer.alloc(12 + datos.length);
      t.writeUInt32BE(datos.length, 0); t.write(tipo, 4, "latin1"); datos.copy(t, 8);
      t.writeUInt32BE(R.crc32(t.subarray(4, 8 + datos.length)), 8 + datos.length);
      return t;
    };
    const ihdr = Buffer.alloc(13);
    ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4); ihdr[8] = 8; ihdr[9] = 6;
    const bytes = Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), trozo("IHDR", ihdr), trozo("IDAT", deflateSync(crudo, { level: 9 })), trozo("IEND", Buffer.alloc(0))]);
    return R.pngConTexto(new Uint8Array(bytes), { Title: "Contenida · muestra del ensayo de repujado", Comment: "Simulación: no entra en la caja ni en la fuente" });
  };
  /* Un recorte de la placa (en mm), a la mitad de su tamaño. */
  function recorte(v, N, x0mm, y0mm, ladoMm) {
    const k = N / R.LADO, x0 = Math.round(x0mm * k), y0 = Math.round(y0mm * k), l = Math.round(ladoMm * k / 2) * 2, m = l / 2;
    const out = new Uint8ClampedArray(m * m * 4);
    for (let y = 0; y < m; y++) for (let x = 0; x < m; x++) for (let c = 0; c < 4; c++) {
      const a = ((y0 + 2 * y) * N + x0 + 2 * x) * 4 + c;
      out[(y * m + x) * 4 + c] = (v[a] + v[a + 4] + v[a + N * 4] + v[a + N * 4 + 4]) / 4;
    }
    return png(out, m, m);
  }
  const muestras = [["a", "repasar", "a"], ["ó", "puntear", "o_tilde"]];
  for (const [signo, herramienta, nombre] of muestras) {
    const placa = new R.Placa({ N: 1400, semilla: "muestra-" + nombre, arrugas: 0.1 });
    repasar(placa, signo, herramienta);
    const v = new R.Vista(placa);
    for (const [cara, taller] of [["anverso", false], ["reverso", false], ["anverso", true]]) {
      v.opciones({ cara, taller, sombras: true, fondo: "tinta", azimut: taller ? 135 : 160, elevacion: taller ? 38 : 15 }).pintar();
      const x0 = cara === "reverso" ? R.LADO - 115 : 35;
      writeFileSync(join(dir, `${nombre}_${cara}_${taller ? "taller" : "registro"}.png`), recorte(v.rgba, placa.N, x0, 38, 80));
    }
  }
  console.log("  muestras en", dir);
}
console.log(fallas ? `${fallas} pruebas fallaron` : "todas bien");
process.exit(fallas ? 1 : 0);
