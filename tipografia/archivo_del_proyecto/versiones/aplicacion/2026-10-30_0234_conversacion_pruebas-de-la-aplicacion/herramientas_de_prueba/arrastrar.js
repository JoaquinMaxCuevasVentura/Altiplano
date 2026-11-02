// Prueba las asas: arrastre con el ratón, teclado, «volver a la obra» y la caja.
const { chromium } = require("playwright");
const SAL = __dirname + "/capturas";

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errores = [];
  p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") errores.push(m.type() + ": " + m.text()); });
  p.on("pageerror", (e) => errores.push("pageerror: " + e.message));
  await p.goto("http://127.0.0.1:8765/aplicacion/", { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.reload({ waitUntil: "networkidle" });
  await p.waitForTimeout(800);

  const centro = async (clave) => {
    const a = p.locator(`.asa[data-clave="${clave}"] circle:not(.golpe)`);
    await a.scrollIntoViewIfNeeded();
    const r = await a.boundingBox();
    return [r.x + r.width / 2, r.y + r.height / 2];
  };
  const valor = (clave) => p.$eval(`.asa[data-clave="${clave}"]`, (a) => a.getAttribute("aria-valuetext"));
  const escala = (clave) => p.$eval(`.asa[data-clave="${clave}"]`, (a) => a.ownerSVGElement.getScreenCTM().a);

  // arrastres: [clave, dx, dy] en unidades del dibujo
  const pruebas = [
    ["razon_x", 0, -30], ["canal", 20, 0], ["trapecio", -30, 0], ["pared", 12, 14], ["quiebre", 20, 0],
    ["hombro", 10, -8], ["hombro_caida", 0, 40], ["gota_masa", 0, 25], ["intemperie", -10, 10],
  ];
  for (const [clave, dx, dy] of pruebas) {
    const [x, y] = await centro(clave), k = await escala(clave), antes = await valor(clave);
    const t0 = Date.now();
    await p.mouse.move(x, y);
    await p.mouse.down();
    const pasos = 8;
    for (let i = 1; i <= pasos; i++) await p.mouse.move(x + dx * k * i / pasos, y + dy * k * i / pasos);
    const tMover = Date.now() - t0;
    await p.waitForTimeout(60);
    const [x2, y2] = await centro(clave);
    await p.mouse.up();
    await p.waitForTimeout(100);
    const despues = await valor(clave);
    const dist = Math.hypot(x2 - (x + dx * k), y2 - (y + dy * k)) / k;
    console.log(`${clave.padEnd(13)} ${antes}  →  ${despues}   (el asa quedó a ${dist.toFixed(1)} del dedo; ${tMover} ms)`);
  }
  await p.waitForTimeout(1500);
  const opacidad = await p.$eval("#caja", (c) => getComputedStyle(c).opacity);
  console.log("caja: opacidad", opacidad);
  await p.screenshot({ path: `${SAL}/movida_1440.png`, fullPage: true });
  console.log("anuncio:", await p.$eval("#anuncio", (a) => a.textContent));
  console.log("guardado:", await p.evaluate(() => localStorage.getItem("contenida-decisiones-v1")));

  // teclado
  await p.focus('.asa[data-clave="canal"]');
  const k0 = await valor("canal");
  await p.keyboard.press("ArrowRight");
  await p.waitForTimeout(80);
  const k1 = await valor("canal");
  const foco = await p.evaluate(() => document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.clave : null);
  await p.keyboard.press("Shift+ArrowLeft");
  await p.waitForTimeout(80);
  const k2 = await valor("canal");
  await p.keyboard.press("Escape");
  await p.waitForTimeout(400);
  const k3 = await valor("canal");
  console.log("teclado canal:", k0, "| → ", k1, "| ⇧← ", k2, "| esc ", k3, "| foco en", foco);

  // volver a la obra (botón) y todo como la obra
  await p.click('[data-volver="trapecio"]');
  await p.waitForTimeout(300);
  console.log("volver trapecio:", await valor("trapecio"));
  await p.click("#a-obra");
  await p.waitForTimeout(1500);
  console.log("todo como la obra:", await p.evaluate(() => localStorage.getItem("contenida-decisiones-v1")),
    "| ajustados:", await p.$$eval(".detalle.ajustado", (d) => d.length));

  // elegir un signo en la caja
  await p.click('#caja .celda[data-s="g"]');
  await p.waitForTimeout(300);
  console.log("elegido:", await p.$eval("#p-signo", (e) => e.textContent), "|", await p.$eval("#p-estado", (e) => e.textContent));

  // tiempo de un cuadro mientras se arrastra el borde
  const ms = await p.evaluate(async () => {
    const svg = document.querySelector("#s-celda");
    const a = svg.querySelector('.asa[data-clave="razon_x"]');
    const r = a.querySelector("circle:not(.golpe)").getBoundingClientRect();
    const x = r.x + r.width / 2, y = r.y + r.height / 2;
    const ev = (t, yy) => new PointerEvent(t, { bubbles: true, clientX: x, clientY: yy, pointerId: 1, isPrimary: true });
    a.querySelector("circle").dispatchEvent(ev("pointerdown", y));
    const t = [];
    for (let i = 1; i <= 10; i++) {
      const t0 = performance.now();
      svg.dispatchEvent(ev("pointermove", y - i * 3));
      await new Promise((ok) => requestAnimationFrame(() => requestAnimationFrame(ok)));
      t.push(performance.now() - t0);
    }
    svg.dispatchEvent(ev("pointerup", y - 30));
    return t.map((v) => Math.round(v));
  });
  console.log("cuadros al arrastrar el borde (ms):", ms.join(" "));
  console.log("ERRORES:", errores.length ? errores.join("\n") : "ninguno");
  await b.close();
})();
