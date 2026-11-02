// Junta capturas en una hoja: node hoja.js salida.png a.png b.png ...
const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const [salida, ...imgs] = process.argv.slice(2);
  const cols = +(process.env.COLS || 2), ancho = +(process.env.ANCHO || 420);
  const html = `<body style="margin:0;background:#888;display:grid;grid-template-columns:repeat(${cols},${ancho}px);gap:6px;padding:6px">` +
    imgs.map((i) => `<img src="${path.relative(path.dirname(path.resolve(salida)), path.resolve(i))}" style="width:${ancho}px;display:block">`).join("") + "</body>";
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: cols * (ancho + 6) + 6, height: 400 } });
  const fs = require("fs"), tmp = path.resolve(salida) + ".html";
  fs.writeFileSync(tmp, html);
  await p.goto("file://" + tmp, { waitUntil: "load" });
  await p.screenshot({ path: salida, fullPage: true });
  await b.close();
})();
