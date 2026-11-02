// La captura del informe: la parte de arriba de la página, con la a elegida y todo como la obra.
const { chromium } = require("playwright");
(async () => {
  const [ancho, alto, salida] = [+process.argv[2], +process.argv[3], process.argv[4]];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: ancho, height: alto }, deviceScaleFactor: 2 });
  await p.goto("http://127.0.0.1:8765/aplicacion/", { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.setItem("contenida-decisiones-v1", JSON.stringify({ estado: {}, seleccion: "a" })));
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: salida });
  await b.close();
})();
