// Abre la aplicación, junta los errores, saca capturas y prueba unas asas.
const { chromium } = require("playwright");
const SAL = __dirname + "/capturas";
require("fs").mkdirSync(SAL, { recursive: true });

(async () => {
  const b = await chromium.launch();
  const ancho = +(process.argv[2] || 1440);
  const p = await b.newPage({ viewport: { width: ancho, height: 1000 }, deviceScaleFactor: 1 });
  const errores = [];
  p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") errores.push(m.type() + ": " + m.text()); });
  p.on("pageerror", (e) => errores.push("pageerror: " + e.message));
  await p.goto("http://127.0.0.1:8765/aplicacion/", { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: `${SAL}/entera_${ancho}.png`, fullPage: true });
  // cada detalle por separado, más grande
  for (const id of ["celda", "canal", "cuenca", "fuste", "hombro", "gota", "intemperie"]) {
    const el = await p.$("#det-" + id);
    if (el) await el.screenshot({ path: `${SAL}/det_${id}.png` });
  }
  // las asas: dónde están
  const asas = await p.$$eval(".asa", (as) => as.map((a) => {
    const r = a.querySelector("circle:not(.golpe)").getBoundingClientRect();
    return { clave: a.dataset.clave, x: r.x + r.width / 2, y: r.y + r.height / 2, v: a.getAttribute("aria-valuetext") };
  }));
  console.log(JSON.stringify(asas, null, 1));
  console.log("ERRORES:", errores.length ? errores.join("\n") : "ninguno");
  await b.close();
})();
