// mide cuánto tarda la gramática: preparar, construir un signo y construir todo
global.window = global;
const ap = process.argv[2];
global.ClipperLib = require(ap + "/clipper.js");
require(ap + "/datos.js");
require(ap + "/gramatica.js");
const G = window.Gramatica, D = window.DATOS;
let t = Date.now();
const todo = G.construirTodo(D, {});
console.log("construirTodo", Date.now() - t, "ms", Object.keys(todo.signos).length, "signos");
const P = Object.fromEntries(D.parametros.map((p) => [p.nombre, p]));
console.log(D.parametros.map((p) => p.nombre + "=" + (p.fijo ?? p.canales)).join(" "));
for (const s of ["n", "o", "a", "l", "g", "m"]) {
  t = Date.now();
  for (let k = 0; k < 10; k++) {
    const base = G.preparar(D, { hombro: 3 + k * 0.1, trapecio: 0.6 + k * 0.02 });
    G.construir(base, D, s);
  }
  console.log(s, ((Date.now() - t) / 10).toFixed(1), "ms por preparar+construir");
}
t = Date.now();
for (let k = 0; k < 10; k++) G.preparar(D, { razon_x: 1.6 + k * 0.02 });
console.log("preparar (razon_x)", ((Date.now() - t) / 10).toFixed(1), "ms");
