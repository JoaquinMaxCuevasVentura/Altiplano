// Guarda la página del poema (pagina.png) y la muestra de instancias (muestra.png).
// Antes hay que armar ../vasijas/ruina.html con python3 ../vasijas/armar.py.
// Uso: NODE_PATH=... node capturar.js
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const INSTANCIAS = [
  ["Piedra", ""],
  ["Intemperie", "'EROD' 50"],
  ["Polvo", "'EROD' 100"],
  ["Incisión", "'REFL' 50"],
  ["Repujado", "'REFL' 100"],
  ["Refracción", "'ONDA' 100"],
  ["Deriva", "'GRID' 100"],
  ["Vuelve escrito", "'EROD' 30, 'REFL' 100, 'ONDA' 40, 'GRID' 50"],
];

(async () => {
  const aqui = __dirname;
  const navegador = await chromium.launch();

  const hoja = await navegador.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 1 });
  await hoja.goto("file://" + path.join(aqui, "..", "vasijas", "ruina.html") + "#solo-hoja");
  await hoja.evaluate(() => document.fonts.ready);
  await hoja.waitForTimeout(400);
  await hoja.locator("#hoja").screenshot({ path: path.join(aqui, "pagina.png") });
  console.log("pagina.png");

  const filas = INSTANCIAS.map(([nombre, ajustes]) =>
    `<div class="e">${nombre}</div><div class="f" style="font-variation-settings:${ajustes || "normal"}">Contener una ruina</div>`).join("");
  const fuente = fs.readFileSync(path.join(aqui, "Ruina-Variable.woff2")).toString("base64");
  const muestra = await navegador.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await muestra.setContent(`<!doctype html><meta charset="utf-8"><style>
    @font-face { font-family: Ruina; src: url("data:font/woff2;base64,${fuente}") format("woff2"); }
    body { margin: 0; background: #0F1110; color: #E4E6E1; }
    main { padding: 48px 56px 40px; display: grid; grid-template-columns: 220px 1fr; align-items: center; row-gap: 6px; }
    .e { font: 18px/1.2 monospace; color: #9AA19E; }
    .f { font-family: Ruina; font-size: 80px; line-height: 1.32; white-space: nowrap; font-kerning: normal; }
  </style><main>${filas}</main>`, { waitUntil: "load" });
  await muestra.evaluate(() => document.fonts.ready);
  await muestra.waitForTimeout(300);
  await muestra.locator("main").screenshot({ path: path.join(aqui, "muestra.png") });
  console.log("muestra.png");
  await navegador.close();
})();
