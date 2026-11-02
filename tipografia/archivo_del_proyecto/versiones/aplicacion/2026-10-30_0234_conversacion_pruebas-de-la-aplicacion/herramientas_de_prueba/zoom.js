// Capturas de los dibujos a 2×: node zoom.js id1 id2 ...
const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto("http://127.0.0.1:8765/aplicacion/", { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(800);
  for (const id of process.argv.slice(2)) {
    const el = await p.$("#s-" + id);
    await el.screenshot({ path: `${__dirname}/capturas/z_${id}.png` });
  }
  await b.close();
})();
