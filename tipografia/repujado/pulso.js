/* El pulso: la mano simulada, la misma de simulacion/pulso.py.
 *
 * En la mesa, la mano es la tuya: este archivo no la toca. Lo usan las muestras (prueba.mjs --imagenes), que
 * antes repasaba la máquina con un temblor parejo. Una mano levanta el punzón (un contorno se hace en tramos, que
 * al retomar se montan sobre lo hecho), va más despacio en las curvas, sigue la línea con retardo, se desvía y se
 * corrige, tiembla un poco (apoyado en el aluminio, el roce lo frena), duda, aprieta distinto, tiene direcciones
 * cómodas y se cansa con los minutos de la sesión. Todo es sutil, como en una mano cuidadosa: se ve de cerca.
 * Son supuestos de la motricidad, no medidas de una mano.
 *
 * Sin dependencias: corre en el navegador y en Node.
 */
(function (raiz, fabrica) {
  const api = fabrica();
  if (typeof module === "object" && module.exports) module.exports = api;
  else raiz.Pulso = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  /* Los mismos números que OFICIOS en simulacion/pulso.py. v: mm/s en lo recto; deriva: mm; tau: s; temblor: mm;
   * tramo: mm antes de levantar; duda: dudas por segundo; seguir: Hz; monta: qué tan seguido, al retomar, se monta
   * sobre lo hecho (si no, deja un hueco, en mm); esquina: qué tan seguido levanta en una esquina. */
  const OFICIOS = {
    repujar: { v: 7, deriva: 0.09, tau: 0.6, temblor: 0.008, tramo: [30, 70], duda: 1 / 25, presion: 0.93, seguir: 3,
      monta: 0.95, hueco: [0.1, 0.3], esquina: 0.25 },
    puntear: { v: 4, deriva: 0.09, tau: 0.7, temblor: 0.008, tramo: [25, 55], duda: 1 / 20, presion: 0.95, seguir: 3,
      monta: 0.85, hueco: [0.15, 0.5], esquina: 0.2 },
  };
  const DT = 1 / 60, PASO = 0.05;

  const cansancio = (minutos) => 1 - Math.exp(-Math.max(0, minutos) / 100);
  const suave = (x) => x * x * (3 - 2 * x);
  const entre = (r, a, b) => a + (b - a) * r();
  function gauss(r) {
    let u = r();
    while (u <= 1e-12) u = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r());
  }
  function poisson(r, l) {
    let k = 0, p = Math.exp(-l), s = p;
    const u = r();
    while (u > s && k < 200) { k++; p *= l / k; s += p; }
    return k;
  }
  /* Hacia dónde empuja (y no tira) la mano, en coordenadas de la placa (y hacia abajo). */
  const empuje = (lado) => (lado === "izquierda" ? [-Math.SQRT1_2, -Math.SQRT1_2] : [Math.SQRT1_2, -Math.SQRT1_2]);

  /* Un proceso de Ornstein-Uhlenbeck de desvío 1: se aparta y vuelve, con memoria tau (s). */
  function ou(n, tau, r) {
    const a = Math.exp(-DT / tau), b = Math.sqrt(1 - a * a), y = new Float64Array(n);
    let x = gauss(r);
    for (let i = 0; i < n; i++) { x = a * x + b * gauss(r); y[i] = x; }
    return y;
  }
  /* El temblor fisiológico: tres componentes de 8 a 12 Hz que crecen y menguan; cansada, uno lento. */
  function temblor(n, c, r) {
    const y = new Float64Array(n);
    for (let k = 0; k < 3; k++) {
      const f = entre(r, 8, 12), fase = entre(r, 0, 2 * Math.PI), m = ou(n, 0.5, r);
      for (let i = 0; i < n; i++) y[i] += (1 + 0.4 * m[i]) * Math.sin(2 * Math.PI * f * i * DT + fase) / Math.sqrt(3);
    }
    if (c > 0.15) {
      const f = entre(r, 4, 6), fase = entre(r, 0, 2 * Math.PI);
      for (let i = 0; i < n; i++) y[i] += 0.4 * c * Math.sin(2 * Math.PI * f * i * DT + fase);
    }
    return y;
  }
  /* Seguir lo que mira con retardo: un sistema de segundo orden (amortiguado: 0,8), discretizado con la
   * transformación bilineal, como scipy.signal.bilinear. */
  function seguidor(hz) {
    const w = 2 * Math.PI * hz, K = 2 / DT, z = 0.8, a0 = K * K + 2 * z * w * K + w * w;
    return { b: [w * w / a0, 2 * w * w / a0, w * w / a0], a: [(2 * w * w - 2 * K * K) / a0, (K * K - 2 * z * w * K + w * w) / a0] };
  }
  function filtrar(f, x, x0) {
    const y = new Float64Array(x.length);
    let x1 = x0, x2 = x0, y1 = x0, y2 = x0;
    for (let i = 0; i < x.length; i++) {
      y[i] = f.b[0] * x[i] + f.b[1] * x1 + f.b[2] * x2 - f.a[0] * y1 - f.a[1] * y2;
      x2 = x1; x1 = x[i]; y2 = y1; y1 = y[i];
    }
    return y;
  }

  function remuestrear(q) {
    const s = [0];
    for (let i = 1; i < q.length; i++) s.push(s[i - 1] + Math.hypot(q[i][0] - q[i - 1][0], q[i][1] - q[i - 1][1]));
    const P = [], S = [];
    for (let t = 0, j = 0; t <= s.at(-1) + 1e-9; t += PASO) {
      while (j < s.length - 2 && s[j + 1] < t) j++;
      const f = s[j + 1] > s[j] ? (t - s[j]) / (s[j + 1] - s[j]) : 0;
      P.push([q[j][0] + (q[j + 1][0] - q[j][0]) * f, q[j][1] + (q[j + 1][1] - q[j][1]) * f]);
      S.push(t);
    }
    return { P, S };
  }

  /* Dónde levanta: al pasar su alcance, en algunas esquinas (cada una se decide una vez), donde tendría que
   * empujar (y gira la hoja) y, con las dos manos, cuando la otra lee el anverso. */
  function cortes(P, S, ang, mano, o, c, r) {
    const n = P.length, k = Math.round(0.5 / PASO), ventana = Math.round(1.5 / PASO), e = empuje(mano.lado);
    const idx = [], giro = [];
    for (let i = k; i < n - k; i += k) { idx.push(i); giro.push(Math.abs(ang[Math.min(n - 1, i + ventana)] - ang[Math.max(0, i - ventana)])); }
    const esquina = new Uint8Array(idx.length), agudo = (j) => giro[j] > (80 * Math.PI) / 180;
    for (let j = 0; j < idx.length;) {
      if (!agudo(j)) { j++; continue; }
      let m = j, mejor = j;
      while (m + 1 < idx.length && agudo(m + 1)) { m++; if (giro[m] > giro[mejor]) mejor = m; }
      esquina[mejor] = r() < o.esquina ? 1 : 0;
      j = m + 1;
    }
    const out = [0], giros = new Set(), lecturas = new Set();
    let desde = 0, alcance = entre(r, ...o.tramo) * (1 - 0.3 * c);
    idx.forEach((i, j) => {
      const hecho = S[i] - S[desde];
      const tx = P[Math.min(n - 1, i + 1)][0] - P[Math.max(0, i - 1)][0], ty = P[Math.min(n - 1, i + 1)][1] - P[Math.max(0, i - 1)][1];
      const empuja = (tx * e[0] + ty * e[1]) / (Math.hypot(tx, ty) + 1e-12) > 0.8;
      if (hecho > 6 && esquina[j]) out.push(i);
      else if (hecho > 10 && empuja && r() < 0.012) { out.push(i); giros.add(out.length - 1); }
      else if (mano.lado === "las dos" && hecho > 8 && r() < 0.004 * (1 + c)) { out.push(i); lecturas.add(out.length - 1); }
      else if (hecho > alcance) out.push(i);
      else return;
      desde = i; alcance = entre(r, ...o.tramo) * (1 - 0.3 * c);
    });
    if (S.at(-1) - S[out.at(-1)] < 3 && out.length > 1) out.pop();
    out.push(n - 1);
    return { cortes: out, giros, lecturas };
  }

  /** Recorre un camino abierto ([[x, y], …], mm) como una mano: mano = { oficio, lado, minutos }, r = azar().
   *  Devuelve los tramos, cada uno con sus puntos [x, y, presión, ms] (el último valor, 1, en las dudas: la mano
   *  quieta, apretando) y un resumen: segundos, levantadas, dudas y lecturas. */
  function trazar(camino, mano, r) {
    const o = OFICIOS[mano.oficio || "repujar"], c = cansancio(mano.minutos || 0);
    const { P, S } = remuestrear(camino), n = P.length;
    const resumen = { segundos: 0, levantadas: 0, dudas: 0, lecturas: 0 };
    if (n < 4) return { tramos: [], resumen };
    const tang = P.map((_, i) => {
      const a = P[Math.max(0, i - 1)], b = P[Math.min(n - 1, i + 1)], l = Math.hypot(b[0] - a[0], b[1] - a[1]) + 1e-12;
      return [(b[0] - a[0]) / l, (b[1] - a[1]) / l];
    });
    const ang = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      let t = Math.atan2(tang[i][1], tang[i][0]);
      if (i) { while (t - ang[i - 1] > Math.PI) t -= 2 * Math.PI; while (t - ang[i - 1] < -Math.PI) t += 2 * Math.PI; }
      ang[i] = t;
    }
    const kap = new Float64Array(n);                                   // la curvatura, promediada en 0,6 mm
    for (let i = 0; i < n; i++) {
      let s = 0, m = 0;
      for (let j = Math.max(1, i - 6); j < Math.min(n - 1, i + 6); j++) { s += Math.abs(ang[j + 1] - ang[j - 1]) / (2 * PASO); m++; }
      kap[i] = m ? s / m : 0;
    }
    const { cortes: C, giros, lecturas } = cortes(P, S, ang, mano, o, c, r);
    const v0 = o.v * (1 - 0.25 * c), f = seguidor(o.seguir), e = empuje(mano.lado);
    const tramos = [];
    let reloj = 0;
    for (let k = 0; k < C.length - 1; k++) {
      let a = C[k];
      const b = C[k + 1];
      if (k > 0) a = r() < o.monta ? Math.max(0, a - Math.round(entre(r, 0.3, 1.2) / PASO)) : Math.min(b - 2, a + Math.round(entre(r, ...o.hueco) / PASO));
      if (b - a < 4) continue;
      const m = b - a + 1, L = S[b] - S[a];
      const vIni = a === 0 ? 0.12 : 0.3, vFin = b === n - 1 ? 0.12 : 0.45;
      const v = new Float64Array(m), tiempo = new Float64Array(m);
      for (let i = 0; i < m; i++) {
        const s = S[a + i] - S[a];
        const rampa = Math.min(vIni + (1 - vIni) * suave(Math.min(1, s / 2.5)), vFin + (1 - vFin) * suave(Math.min(1, (L - s) / 2)));
        v[i] = v0 * Math.pow(1 + 4 * kap[a + i], -1 / 3) * rampa;
        if (i) tiempo[i] = tiempo[i - 1] + PASO / Math.max(v[i], 0.08 * v0);
      }
      const T0 = tiempo[m - 1];
      const pausas = [];
      for (let q = poisson(r, o.duda * (1 + c) * T0); q > 0; q--) pausas.push([entre(r, 0.1, 0.9) * T0, entre(r, 0.25, 0.9) * (1 + 0.5 * c)]);
      pausas.sort((x, y) => x[0] - y[0]);
      const T = T0 + pausas.reduce((s, p) => s + p[1], 0), ng = Math.floor(T / DT) + 1;
      // el reloj de la mano: tm, el tiempo en movimiento, se queda quieto mientras duda
      const tm = new Float64Array(ng), quieta = new Uint8Array(ng), marcas = [];
      for (let i = 0; i < ng; i++) tm[i] = i * DT;
      let antes = 0;
      for (const [cuando, cuanto] of pausas) {
        const r0 = cuando + antes;
        for (let i = 0; i < ng; i++) {
          const t = i * DT;
          if (t >= r0 + cuanto) tm[i] -= cuanto;
          else if (t >= r0) { tm[i] = cuando; quieta[i] = 1; }
        }
        marcas.push(Math.min(ng - 1, Math.ceil(r0 / DT)));
        antes += cuanto;
      }
      // dónde va la mano en cada instante, y hacia dónde
      const nm = Math.floor(T0 / DT) + 2, desvio = ou(nm, o.tau * (1 + 0.2 * c), r), dx = ou(nm, 0.8, r), dy = ou(nm, 0.8, r);
      const lento = (y, t) => { const u = Math.min(nm - 1.001, t / DT), i = Math.floor(u); return y[i] + (y[i + 1] - y[i]) * (u - i); };
      const gx = new Float64Array(ng), gy = new Float64Array(ng), ux = new Float64Array(ng), uy = new Float64Array(ng), vg = new Float64Array(ng);
      for (let i = 0, j = 0; i < ng; i++) {
        const t = Math.min(tm[i], T0);
        while (j < m - 2 && tiempo[j + 1] < t) j++;
        const w = tiempo[j + 1] > tiempo[j] ? (t - tiempo[j]) / (tiempo[j + 1] - tiempo[j]) : 0, A = a + j, B = a + j + 1;
        const x = P[A][0] + (P[B][0] - P[A][0]) * w, y = P[A][1] + (P[B][1] - P[A][1]) * w;
        const tx = tang[A][0] + (tang[B][0] - tang[A][0]) * w, ty = tang[A][1] + (tang[B][1] - tang[A][1]) * w, l = Math.hypot(tx, ty) + 1e-12;
        ux[i] = tx / l; uy[i] = ty / l; vg[i] = quieta[i] ? 0 : v[j] + (v[j + 1] - v[j]) * w;
        const incomodo = 1 + 0.4 * Math.max(0, ux[i] * e[0] + uy[i] * e[1]);
        const d = o.deriva * (1 + 0.3 * c) * incomodo * lento(desvio, t);
        gx[i] = x - uy[i] * d + 0.25 * o.deriva * lento(dx, t);
        gy[i] = y + ux[i] * d + 0.25 * o.deriva * lento(dy, t);
      }
      // aterriza un poco corrida y converge; tiembla poco (apoyada, menos)
      const hx = filtrar(f, gx, gx[0] + gauss(r) * (0.05 + 0.04 * c)), hy = filtrar(f, gy, gy[0] + gauss(r) * (0.05 + 0.04 * c));
      const t1 = temblor(ng, c, r), t2 = temblor(ng, c, r), lat = ou(ng, 0.6, r), tp = temblor(ng, 0, r);
      const puntos = [];
      for (let i = 0; i < ng; i++) {
        const incomodo = 1 + 0.4 * Math.max(0, ux[i] * e[0] + uy[i] * e[1]);
        const A = o.temblor * (1 + 0.5 * c) * incomodo * (quieta[i] ? 0.35 : 1);
        const x = hx[i] - uy[i] * A * t1[i] + ux[i] * 0.5 * A * t2[i], y = hy[i] + ux[i] * A * t1[i] + uy[i] * 0.5 * A * t2[i];
        const t = i * DT;
        let p = o.presion * (1 - 0.1 * c) * (1 + 0.15 * (1 - Math.min(1, Math.max(0, vg[i] / v0))));
        p *= (1 - Math.exp(-t / 0.09)) * (1 - Math.exp(-(T - t) / (b === n - 1 ? 0.07 : 0.1)));
        p *= 1 + 0.04 * lat[i] + 0.01 * tp[i];
        puntos.push([x, y, Math.min(1.3, Math.max(0, p)), Math.round((reloj + t) * 1000)]);
      }
      tramos.push({ puntos, dudas: marcas });
      resumen.dudas += pausas.length;
      reloj += T + entre(r, 0.4, 1.2) + (giros.has(k + 1) ? entre(r, 1.5, 3) : 0) + (lecturas.has(k + 1) ? entre(r, 1, 3) : 0);
    }
    resumen.segundos = Math.round(reloj * 10) / 10;
    resumen.levantadas = Math.max(0, tramos.length - 1);
    resumen.lecturas = lecturas.size;
    return { tramos, resumen };
  }

  /** Un tramo como lo recibe la placa (Placa.agregar), igual que desde la mesa: un punto cada 0,15 mm y, en cada
   *  duda, la mano quieta, apretando. escala lleva la presión de la mano a la de la mesa (0,8 de base). */
  function puntosDe(tramo, escala = 0.8 / 0.93) {
    const out = [], dudas = new Set(tramo.dudas);
    tramo.puntos.forEach(([x, y, p, ms], i) => {
      const u = out.at(-1);
      if (!u || Math.hypot(x - u[0], y - u[1]) >= 0.15 || i === tramo.puntos.length - 1) out.push([x, y, p * escala, ms]);
      if (dudas.has(i)) { const w = out.at(-1); out.push([w[0], w[1], w[2], ms, 1]); }
    });
    return out;
  }

  return { OFICIOS, cansancio, trazar, puntosDe };
});
