// Compara los cuerpos de la página con los de Python, signo por signo, sin contar el píxel del borde
// (cada lenguaje lo pinta a su modo). Uso: node comparar.js <carpeta de la aplicación> <prueba.json>,
// con el prueba.json que escribe exportar.py --prueba.
global.window = global;
const ap = require("path").resolve(process.argv[2] || __dirname), prueba = JSON.parse(require("fs").readFileSync(process.argv[3], "utf8"));
global.ClipperLib = require(ap + "/clipper.js");
require(ap + "/datos.js"); require(ap + "/gramatica.js");
const G = window.Gramatica, D = window.DATOS, todo = G.construirTodo(D, {}), T = todo.T, res = [];
for (const s of Object.keys(todo.signos)) {
  const m = G.rasterizar(todo.signos[s].geo, T), py = G.decodificar(prueba.cuerpos[s], T);
  let dif = 0, ar = 0;
  for (let y = 2; y < T - 2; y++) for (let x = 2; x < T - 2; x++) {
    const i = y * T + x; ar += py[i] ? 1 : 0;
    if (!!m[i] === !!py[i]) continue;
    let borde = false;                       // ¿hay en Python un píxel del otro valor a 1 de distancia?
    for (let dy = -1; dy <= 1 && !borde; dy++) for (let dx = -1; dx <= 1; dx++) if (!!py[i + dy * T + dx] !== !!py[i]) { borde = true; break; }
    if (!borde) dif++;
  }
  res.push([s, 100 * dif / ar]);
}
res.sort((p, q) => q[1] - p[1]);
const v = res.map((r) => r[1]).sort((p, q) => p - q);
console.log("fuera del borde: mediana", v[v.length >> 1].toFixed(3), "% · máximo", v[v.length - 1].toFixed(3), "% ·", res.slice(0, 5).map((r) => `${r[0]} ${r[1].toFixed(2)}`).join(" | "));
