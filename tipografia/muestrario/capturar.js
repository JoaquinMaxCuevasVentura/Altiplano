// Guarda una captura PNG de cada sección del muestrario.
// Uso: NODE_PATH=... node capturar.js index.html carpeta_de_salida
const path = require("path");
const { chromium } = require("playwright");

const SECCIONES = [
  [".portada", "01_portada.png"],
  ["#probador", "02_probador.png"],
  ["#contrastes", "03_contrastes.png"],
  ["#reglas", "04_reglas.png"],
  ["#vasos", "05_vasos.png"],
  ["#poema", "06_poema.png"],
  ["#repertorio", "07_repertorio.png"],
];

(async () => {
  const [, , entrada, salida] = process.argv;
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
  await pagina.goto("file://" + path.resolve(entrada));
  await pagina.evaluate(() => document.fonts.ready);
  await pagina.waitForTimeout(400);
  for (const [selector, archivo] of SECCIONES) {
    await pagina.locator(selector).screenshot({ path: path.join(salida, archivo) });
    console.log(archivo);
  }
  await navegador.close();
})();
