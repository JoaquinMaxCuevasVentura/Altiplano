/* Gramática de Contenida en el navegador: el mismo orden que gramatica.py.
 *
 * Del pie, las medidas: los testigos (ya escalados al azulejo) se achatan a la altura
 * de x que se pida, se miden y dan el esqueleto. De la obra, la forma: los parámetros.
 * Con las partes del Taller (fuste, cuenca, hombro, gota, punto, tilde, onda, recta,
 * alivio) cada receta arma un signo; el cuerpo es el trazo del ancho del canal, más
 * asientos, gotas y tildes, menos alivios, gastado por la intemperie.
 *
 * El azar de cada receta es el de Python (lo exporta exportar.py): los mismos quiebres.
 * Necesita ClipperLib (clipper-lib 6.4.2) y DATOS (datos.js).
 */
(function (raiz) {
  "use strict";
  const CL = raiz.ClipperLib || (typeof require !== "undefined" ? require("clipper-lib") : null);

  // ------------------------------------------------------------------ vectores
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
  const mul = (a, k) => [a[0] * k, a[1] * k];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
  const len = (a) => Math.hypot(a[0], a[1]);
  const unit = (a) => { const l = len(a); return [a[0] / l, a[1] / l]; };
  const clamp = (v, a, b) => Math.min(Math.max(v, a), b);
  const rad = (g) => g * Math.PI / 180;
  const pmod = (a, m) => ((a % m) + m) % m;
  const u = (a, b) => unit(sub(b, a));
  const copia = (pts) => pts.map((p) => [p[0], p[1]]);

  function linspace(a, b, n) {
    const r = new Array(n);
    for (let i = 0; i < n; i++) r[i] = n === 1 ? a : a + (b - a) * i / (n - 1);
    return r;
  }

  // ------------------------------------------------------------------ máscaras
  function crear(T) { return new Uint8Array(T * T); }

  function decodificar(t, T) {
    const bin = atob(t.rle);
    const m = crear(T);
    let i = 0, pos = 0, val = 0;
    while (i < bin.length) {
      let n = 0, b;
      do { b = bin.charCodeAt(i++); n += b; } while (b === 255 && i < bin.length);
      if (val) for (let k = pos; k < pos + n; k++) m[(t.y + Math.floor(k / t.w)) * T + t.x + (k % t.w)] = 1;
      pos += n;
      val ^= 1;
    }
    return m;
  }

  function cajaTinta(m, T, filas) {
    const H = filas === undefined ? T : Math.max(0, Math.min(T, filas));
    let x0 = T, y0 = -1, x1 = -1, y1 = -1;
    for (let y = 0; y < H; y++) {
      const r = m.subarray(y * T, y * T + T);
      const a = r.indexOf(1);
      if (a < 0) continue;
      const b = r.lastIndexOf(1);
      if (y0 < 0) y0 = y;
      y1 = y;
      if (a < x0) x0 = a;
      if (b > x1) x1 = b;
    }
    return x1 < 0 ? [0, 0, 0, 0] : [x0, y0, x1, y1];
  }

  function corridas(v) {
    const out = [];
    let ini = -1;
    for (let x = 0; x < v.length; x++) {
      if (v[x] && ini < 0) ini = x;
      else if (!v[x] && ini >= 0) { out.push([ini, x]); ini = -1; }
    }
    if (ini >= 0) out.push([ini, v.length]);
    return out;
  }

  function fila(m, T, y) { return m.subarray(y * T, y * T + T); }
  function columna(m, T, x) { const c = new Uint8Array(T); for (let y = 0; y < T; y++) c[y] = m[y * T + x]; return c; }

  /* Lleva la altura de x a xh_nueva sin mover la base ni la línea de afuera (como desenterrar.achatar:
   * el mapa en float32 y la interpolación lineal de cv2.remap). */
  function achatar(m, T, base, asc, xh, xhNueva) {
    const afuera = base - asc, borde = base - xh, bordeN = base - xhNueva;
    const out = crear(T);
    const [cx0, , cx1] = cajaTinta(m, T);
    for (let y = 0; y < T; y++) {
      let f = y;
      if (y >= afuera && y < bordeN) f = afuera + (y - afuera) * (borde - afuera) / (bordeN - afuera);
      else if (y >= bordeN && y <= base) f = borde + (y - bordeN) * (base - borde) / (base - bordeN);
      f = Math.fround(f);
      const y0 = Math.floor(f), fy = f - y0;
      if (y0 < -1 || y0 >= T) continue;
      for (let x = cx0; x <= cx1; x++) {
        const a = y0 >= 0 && y0 < T ? m[y0 * T + x] : 0;
        const b = y0 + 1 >= 0 && y0 + 1 < T ? m[(y0 + 1) * T + x] : 0;
        if (a + fy * (b - a) > 0.5) out[y * T + x] = 1;
      }
    }
    return out;
  }

  const LETRAS_X = "acemnorsuv", ASCENDENTES = "bdfhklí", DESCENDENTES = "gjpqy";

  function mediana(v) {
    const s = v.slice().sort((a, b) => a - b), n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }

  function medidas(M, T, base) {
    const hay = (cs) => [...cs].filter((c) => M[c]);
    const xh = mediana(hay(LETRAS_X).map((c) => base - cajaTinta(M[c], T)[1]));
    const asc = Math.max(...hay(ASCENDENTES).map((c) => base - cajaTinta(M[c], T)[1]));
    const desc = Math.max(...hay(DESCENDENTES).map((c) => cajaTinta(M[c], T)[3] - base));
    const o = M.o;
    let r = corridas(fila(o, T, Math.trunc(base - xh / 2)));
    const grueso = r.length ? r[0][1] - r[0][0] : 30;
    const [x0, , x1] = cajaTinta(o, T);
    r = corridas(columna(o, T, Math.trunc((x0 + x1) / 2)));
    const fino = r.length ? r[0][1] - r[0][0] : 12;
    return { base, xh, asc, desc, grueso, fino };
  }

  // los huecos de una máscara (el fondo que no toca el borde, en 4 vecinos) y el mayor, en 8
  function mayorHueco(m, T) {
    const fuera = crear(T), pila = [];
    const empujar = (x, y) => { const i = y * T + x; if (!m[i] && !fuera[i]) { fuera[i] = 1; pila.push(i); } };
    for (let k = 0; k < T; k++) { empujar(k, 0); empujar(k, T - 1); empujar(0, k); empujar(T - 1, k); }
    while (pila.length) {
      const i = pila.pop(), x = i % T, y = (i - x) / T;
      if (x > 0) empujar(x - 1, y);
      if (x < T - 1) empujar(x + 1, y);
      if (y > 0) empujar(x, y - 1);
      if (y < T - 1) empujar(x, y + 1);
    }
    const visto = crear(T);
    let mejor = null;
    for (let i0 = 0; i0 < T * T; i0++) {
      if (m[i0] || fuera[i0] || visto[i0]) continue;
      let n = 0, x0 = T, y0 = T, x1 = -1, y1 = -1;
      visto[i0] = 1; pila.push(i0);
      while (pila.length) {
        const i = pila.pop(), x = i % T, y = (i - x) / T;
        n++;
        if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
          const xx = x + dx, yy = y + dy;
          if (xx < 0 || yy < 0 || xx >= T || yy >= T) continue;
          const j = yy * T + xx;
          if (!m[j] && !fuera[j] && !visto[j]) { visto[j] = 1; pila.push(j); }
        }
      }
      if (!mejor || n > mejor.n) mejor = { n, caja: [x0, y0, x1, y1] };
    }
    return mejor ? mejor.caja : [0, 0, 0, 0];
  }

  // ------------------------------------------------------------------ el esqueleto y los parámetros
  function esqueleto(A, med, T, halladas) {
    const fondo = med.base, xh = med.xh;
    const e = {
      fondo, borde: fondo - xh, afuera: fondo - med.asc, desague: fondo + med.desc, xh,
      canal: Math.sqrt(med.grueso * med.fino), cajas: {},
    };
    for (const s of halladas) e.cajas[s] = cajaTinta(A[s], T);
    e.ojo_a = mayorHueco(A.a, T);
    e.gancho_a = cajaTinta(A.a, T, Math.trunc(e.ojo_a[1]) - 4)[0];
    return e;
  }

  const r1 = (v) => Math.round(v * 10) / 10;

  function parametros(e, ajustes, lista) {
    const c = ajustes.canal !== undefined ? ajustes.canal : e.canal;
    const P = {};
    for (const p of lista) {
      let valor;
      if (p.nombre === "canal") valor = r1(c);
      else if (p.canales !== null && p.canales !== undefined) valor = r1(p.canales * c);
      else valor = p.fijo;
      P[p.nombre] = { valor, unidad: p.unidad, que: p.que, de_donde: p.de_donde, porDefecto: valor, ajustado: false };
    }
    for (const [k, v] of Object.entries(ajustes)) {
      if (P[k]) { P[k].valor = k === "facetas" ? Math.round(v) : v; P[k].ajustado = true; }
    }
    return P;
  }

  const V = (P, k) => Number(P[k].valor);

  // ------------------------------------------------------------------ geometría
  function superelipse(cx, cy, rx, ry, n, a0, a1, pasos = 120) {
    return linspace(a0, a1, pasos).map((g) => {
      const t = rad(g), co = Math.cos(t), si = Math.sin(t);
      return [cx + rx * Math.sign(co) * Math.pow(Math.abs(co), 2 / n), cy - ry * Math.sign(si) * Math.pow(Math.abs(si), 2 / n)];
    });
  }

  function filetear(pts, r, pasos = 14) {
    const out = [pts[0].slice()];
    for (let i = 1; i < pts.length - 1; i++) {
      const p = pts[i];
      let a = sub(pts[i - 1], p), b = sub(pts[i + 1], p);
      const la = len(a), lb = len(b);
      a = mul(a, 1 / la); b = mul(b, 1 / lb);
      const ang = Math.acos(clamp(dot(a, b), -1, 1));
      if (ang > Math.PI - 1e-3) { out.push(p.slice()); continue; }
      const d = Math.min(r / Math.tan(ang / 2), 0.5 * la, 0.5 * lb);
      const rr = d * Math.tan(ang / 2);
      const bis = unit(add(a, b));
      const centro = add(p, mul(bis, rr / Math.sin(ang / 2)));
      const p1 = add(p, mul(a, d)), p2 = add(p, mul(b, d));
      const a1 = Math.atan2(p1[1] - centro[1], p1[0] - centro[0]);
      const a2 = Math.atan2(p2[1] - centro[1], p2[0] - centro[0]);
      const da = pmod(a2 - a1 + Math.PI, 2 * Math.PI) - Math.PI;
      for (const t of linspace(0, 1, pasos)) {
        const g = a1 + da * t;
        out.push([centro[0] + rr * Math.cos(g), centro[1] + rr * Math.sin(g)]);
      }
    }
    out.push(pts[pts.length - 1].slice());
    return out;
  }

  function facetar(p0, p1, n, quiebre, rng) {
    const L = len(sub(p1, p0));
    const s = rng.choice();
    if (L < 1e-9) return [p0.slice(), p1.slice()];
    const d = mul(sub(p1, p0), 1 / L), nrm = [-d[1], d[0]];
    const pts = [p0.slice()];
    let off = 0;
    for (let k = 1; k < n; k++) {
      off += s * (k % 2 ? -1 : 1) * (L / n) * Math.tan(rad(quiebre));
      pts.push(add(add(p0, mul(d, L * k / n)), mul(nrm, off)));
    }
    pts.push(p1.slice());
    return pts;
  }

  function asiento(x, fondo, c, ancho, alto, pasos = 18) {
    const P0 = [x - c / 2, fondo - alto], P1 = [x - c / 2, fondo], P2 = [x - ancho / 2, fondo];
    const izq = linspace(0, 1, pasos).map((t) => [
      (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0],
      (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]]);
    const der = izq.map((p) => [2 * x - p[0], p[1]]).reverse();
    return izq.concat(der);
  }

  function circulo(cx, cy, r, lados) {
    const out = [];
    for (let i = 0; i < lados; i++) {
      const a = 2 * Math.PI * i / lados;
      out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
    }
    return out;
  }

  function gota(p, c, P) {
    const masa = V(P, "gota_masa"), caida = V(P, "gota_caida"), cuello = V(P, "gota_cuello");
    const centro = [p[0], p[1] + caida + masa / 2];
    const oy = centro[1] - masa / 2;
    const cuerpo = circulo(centro[0], centro[1], masa / 2, 192).map(([x, y]) => [x, oy + (y - oy) * 1.15]);
    const cuelloP = [[p[0] - c / 2, p[1]], [p[0] + c / 2, p[1]], [centro[0] + cuello / 2, centro[1]],
      [centro[0] - cuello / 2, centro[1]]];
    return { formas: [cuerpo, cuelloP], fin: [centro[0], centro[1] + masa / 2] };
  }

  function cuencaLado(xMedio, cy, xFondo, ybot, pared, pasos = 60) {
    const P0 = [xMedio, cy], P3 = [xFondo, ybot];
    const P1 = [xMedio, cy + pared * (ybot - cy)], P2 = [xFondo + pared * (xMedio - xFondo), ybot];
    return linspace(0, 1, pasos).map((t) => {
      const a = (1 - t) ** 3, b = 3 * (1 - t) ** 2 * t, cc = 3 * (1 - t) * t * t, d = t ** 3;
      return [a * P0[0] + b * P1[0] + cc * P2[0] + d * P3[0], a * P0[1] + b * P1[1] + cc * P2[1] + d * P3[1]];
    });
  }

  function remuestrear(pts, paso = 1.0) {
    const s = [0];
    for (let i = 1; i < pts.length; i++) s.push(s[i - 1] + len(sub(pts[i], pts[i - 1])));
    const total = s[s.length - 1];
    if (total === 0) return copia(pts);
    const out = [];
    let j = 0;
    for (let t = 0; t < total + 1e-9; t += paso) {
      while (j < s.length - 2 && s[j + 1] < t) j++;
      const L = s[j + 1] - s[j], f = L > 0 ? clamp((t - s[j]) / L, 0, 1) : 0;
      out.push([pts[j][0] + f * (pts[j + 1][0] - pts[j][0]), pts[j][1] + f * (pts[j + 1][1] - pts[j][1])]);
    }
    return out;
  }

  function cortar(pts, huecos, cerrado = false) {
    const q = remuestrear(cerrado ? pts.concat([pts[0]]) : pts);
    const fuera = q.map((p) => huecos.every(([x, y, d]) =>
      !(Math.hypot(p[0] - x, p[1] - y) < 3 * d && Math.abs(p[0] - x) < d / 2)));
    let tramos = [], actual = [];
    q.forEach((p, i) => {
      if (fuera[i]) actual.push(p);
      else if (actual.length) { tramos.push(actual); actual = []; }
    });
    if (actual.length) tramos.push(actual);
    if (cerrado && tramos.length > 1 && fuera[0] && fuera[fuera.length - 1]) tramos[0] = tramos.pop().concat(tramos[0]);
    return tramos.filter((t) => t.length > 1);
  }

  // ------------------------------------------------------------------ el glifo y el taller
  class Glifo {
    constructor(signo) {
      this.signo = signo;
      this.trazos = []; this.mas = []; this.menos = []; this.marcas = []; this.nodos = [];
    }
    trazo(pts, ancho = null) { this.trazos.push([copia(pts), ancho]); }
    marca(nombre, p) { this.marcas.push([nombre, [p[0], p[1]]]); }
    mover(dx) {
      this.trazos = this.trazos.map(([t, w]) => [t.map((p) => [p[0] + dx, p[1]]), w]);
      this.mas = this.mas.map((m) => m.map((p) => [p[0] + dx, p[1]]));
      this.menos = this.menos.map((m) => ({ x: m.x + dx, y: m.y, r: m.r }));
      this.marcas = this.marcas.map(([n, p]) => [n, [p[0] + dx, p[1]]]);
      this.nodos = this.nodos.map((p) => [p[0] + dx, p[1]]);
    }
  }

  function celda(e, T) {
    const alto = (e.desague - e.afuera) * 1.1, cy = (e.afuera + e.desague) / 2;
    return [T / 2 - 0.42 * alto, cy - alto / 2, T / 2 + 0.42 * alto, cy + alto / 2];
  }

  class Taller {
    constructor(e, P, A, T) {
      this.e = e; this.P = P; this.A = A; this.T = T;
      this.c = e.canal;
      this.F = e.fondo; this.B = e.borde; this.Af = e.afuera; this.D = e.desague; this.xh = e.xh;
    }
    v(k) { return V(this.P, k); }
    caja(s) { return this.e.cajas[s]; }
    astas(s, y) {
      return corridas(fila(this.A[s], this.T, Math.trunc(y))).filter(([a, b]) => b - a > 6).map(([a, b]) => (a + b) / 2);
    }

    fuste(G, rng, x, arriba, abajo = null) {
      abajo = abajo === null ? this.F : abajo;
      const asienta = Math.abs(abajo - this.F) < 1;
      const fin = asienta ? abajo - this.v("asiento_alto") + 2 : abajo;
      const eje = facetar([x, arriba], [x, fin], Math.trunc(this.v("facetas")), this.v("quiebre"), rng);
      G.trazo(eje);
      G.nodos.push(...copia(eje));
      if (asienta) {
        G.mas.push(asiento(x, this.F, this.c, this.v("asiento_ancho"), this.v("asiento_alto")));
        G.marca("asiento", [x, this.F]);
      }
      return eje;
    }

    cuenca(G, xIzq, xDer, yArriba, yAbajo, o = {}) {
      const fuste = o.fuste || null, huecosArriba = o.huecos_arriba || [], anchoArriba = o.ancho_arriba || null;
      const exp = o.exp || 2.0;
      const c = this.c, k = this.v("trapecio"), d = this.v("desague"), pared = this.v("pared");
      const cx = (xIzq + xDer) / 2, rx = (xDer - xIzq) / 2, cy = (yArriba + yAbajo) / 2;
      const arriba = superelipse(cx, cy, rx, cy - yArriba, exp, 0, 180);
      const izq = cuencaLado(cx - rx, cy, cx - k * rx, yAbajo, pared);
      const der = cuencaLado(cx + rx, cy, cx + k * rx, yAbajo, pared);
      let xd, poli;
      if (fuste === "der") {
        xd = (cx - k * rx + xDer - c / 2) / 2;
        poli = arriba.concat(izq.slice(1), [[xDer, yAbajo]]);
      } else if (fuste === "izq") {
        xd = (xIzq + c / 2 + cx + k * rx) / 2;
        poli = arriba.slice().reverse().concat(der.slice(1), [[xIzq, yAbajo]]);
      } else {
        xd = cx;
        poli = der.slice().reverse().concat(arriba.slice(1, -1), izq);
      }
      const huecos = [[xd, yAbajo, d]].concat(huecosArriba.map((x) => [x, yArriba, d]));
      for (const t of cortar(poli, huecos, fuste === null)) G.trazo(t, anchoArriba);
      G.marca("desagüe", [xd, yAbajo + c / 2]);
      G.nodos.push([cx - k * rx, yAbajo], [cx + k * rx, yAbajo], [cx - rx, cy], [cx + rx, cy]);
      return { cx, cy, rx, ry: cy - yArriba, xd };
    }

    hombro(G, rng, xIzq, xDer, yTope, pie = true) {
      const yt = yTope + this.c / 2;
      const ya = yt + this.v("hombro_caida") * (this.F - yt);
      const arco = superelipse((xIzq + xDer) / 2, ya, (xDer - xIzq) / 2, ya - yt, this.v("hombro"), 180, 0);
      const fin = pie ? this.F - this.v("asiento_alto") + 2 : this.F;
      const bajada = facetar([xDer, ya], [xDer, fin], Math.trunc(this.v("facetas")), this.v("quiebre"), rng);
      G.trazo(arco.concat(bajada.slice(1)));
      if (pie) G.mas.push(asiento(xDer, this.F, this.c, this.v("asiento_ancho"), this.v("asiento_alto")));
      G.marca("hombro", arco[60]);
      return ya;
    }

    gota(G, p) {
      const g = gota(p, this.c, this.P);
      G.mas.push(...g.formas);
      G.marca("gota", g.fin);
      return g.fin;
    }

    arco(cx, cy, rx, ry, a0, a1, exp = null) {
      return superelipse(cx, cy, rx, ry, exp === null ? this.v("hombro") : exp, a0, a1);
    }

    punto(G, x, y) {
      const lado = this.v("punto");
      G.trazo([[x, y - lado / 2], [x, y + lado / 2]], lado);
      G.marca("punto", [x + lado / 2, y]);
    }

    tilde(G, x, y) {
      const c = this.c;
      G.mas.push(circulo(x, y + 0.35 * c, 0.5 * c, 128));
      G.mas.push([[x - 0.42 * c, y + 0.2 * c], [x + 0.42 * c, y + 0.5 * c], [x + 0.7 * c, y - 1.2 * c]]);
      G.trazo([[x, y + 0.35 * c], [x + 0.6 * c, y - 1.0 * c]], 0.001);
      G.marca("tilde", [x + 0.7 * c, y - 1.2 * c]);
    }

    onda(G, x0, x1, y) {
      G.trazo(linspace(0, 1, 80).map((t) => [x0 + (x1 - x0) * t, y - 0.35 * this.c * Math.sin(2 * Math.PI * t)]));
      G.marca("onda", [x1, y]);
    }

    recta(G, rng, p0, p1, planos = 2) {
      const eje = facetar(p0, p1, planos, this.v("quiebre"), rng);
      G.trazo(eje);
      return eje;
    }

    quebrada(G, pts) {
      const eje = filetear(pts, this.v("radio_chapa"));
      G.trazo(eje);
      return eje;
    }

    alivio(G, v, d1, d2, r = 0.0) {
      d1 = unit(d1); d2 = unit(d2);
      const ang = Math.acos(clamp(dot(d1, d2), -1, 1));
      const b = unit(add(d1, d2));
      const sen = Math.max(Math.sin(ang / 2), 0.2);
      const lejos = r > this.c / 2 ? r / sen - (r - this.c / 2) : (this.c / 2) / sen;
      const esquina = add(v, mul(b, lejos));
      G.menos.push({ x: esquina[0], y: esquina[1], r: this.v("alivio") });
      G.marca("alivio", esquina);
    }

    celdaCifra(G) {
      const [x0, y0, x1, y1] = celda(this.e, this.T);
      const c = this.c, xm = (x0 + x1) / 2;
      for (const m of [0.3 * c, 1.3 * c]) {
        const anillo = [[xm, y1 - m], [x0 + m, y1 - m], [x0 + m, y0 + m], [x1 - m, y0 + m], [x1 - m, y1 - m], [xm, y1 - m]];
        for (const t of cortar(anillo, [[xm, y1 - m, this.v("desague")]])) G.trazo(t, 0.35 * c);
      }
      G.marca("celda", [x1 - 0.3 * c, (y0 + y1) / 2]);
      return [x0 + 1.3 * c, y0 + 1.3 * c, x1 - 1.3 * c, y1 - 1.3 * c];
    }
  }

  // ------------------------------------------------------------------ las recetas
  function alivios(t, G, pts, indices) {
    for (const i of indices) t.alivio(G, pts[i], u(pts[i], pts[i - 1]), u(pts[i], pts[i + 1]), t.v("radio_chapa"));
  }
  const cxDe = (caja) => (caja[0] + caja[2]) / 2;
  const ultimo = (a) => a[a.length - 1];

  function r_o(t, G) {
    const [x0, y0, x1] = t.caja("o"), c = t.c;
    return t.cuenca(G, x0 + c / 2, x1 - c / 2, y0 + c / 2, t.F - c / 2);
  }
  function r_l(t, G, rng) {
    const [, y0] = t.caja("l");
    const xs = Math.max(...t.astas("l", (y0 + t.F) / 2));
    t.fuste(G, rng, xs, y0);
    G.marca("corte", [xs, y0]);
  }
  function r_n(t, G, rng, s = "n") {
    const [, y0] = t.caja(s);
    const a = t.astas(s, t.F - 0.3 * t.xh);
    t.fuste(G, rng, a[0], t.B);
    t.hombro(G, rng, a[0], ultimo(a), y0);
    return [a[0], ultimo(a)];
  }
  function r_h(t, G, rng) {
    const [, y0] = t.caja("h");
    const a = t.astas("h", t.F - 0.3 * t.xh);
    t.fuste(G, rng, a[0], y0);
    t.hombro(G, rng, a[0], ultimo(a), t.B - 3);
  }
  function r_m(t, G, rng) {
    const [, y0] = t.caja("m");
    const a = t.astas("m", t.F - 0.3 * t.xh);
    const xi = a[0], xd = ultimo(a);
    const xm = a.length >= 3 ? a[Math.floor(a.length / 2)] : (xi + xd) / 2;
    t.fuste(G, rng, xi, t.B);
    t.hombro(G, rng, xi, xm, y0);
    t.hombro(G, rng, xm, xd, y0);
  }
  function r_a(t, G, rng) {
    const c = t.c, e = t.e;
    const [, y0] = t.caja("a");
    const xs = ultimo(t.astas("a", t.F - 0.25 * t.xh));
    const xg = e.gancho_a + c / 2;
    const yt = y0 + c / 2;
    const yh = yt + t.v("hombro_caida") * (t.F - yt);
    const gancho = t.arco((xg + xs) / 2, yh, (xs - xg) / 2, yh - yt, t.v("gancho_fin"), 0);
    G.trazo(gancho);
    const fin = t.gota(G, gancho[0]);
    t.fuste(G, rng, xs, yh);
    const [hx0, hy0] = e.ojo_a;
    const arriba = Math.max(hy0 - c / 2, fin[1] + 0.4 * c + c / 2);
    t.cuenca(G, hx0 - c / 2, xs, arriba, t.F - c / 2, { fuste: "der" });
    return (xg + xs) / 2;
  }
  function _u(t, G, rng, s = "u") {
    const c = t.c, k = t.v("trapecio"), pared = t.v("pared");
    const a = t.astas(s, t.B + 0.3 * t.xh);
    const xi = a[0], xd = ultimo(a);
    const ym = t.B + 0.5 * t.xh, yb = t.F - c / 2;
    const cx = (xi + xd) / 2, rx = (xd - xi) / 2;
    const izq = cuencaLado(xi, ym, cx - k * rx, yb, pared);
    const der = cuencaLado(xd, ym, cx + k * rx, yb, pared);
    G.trazo([[xi, t.B]].concat(izq, der.slice().reverse()));
    G.marca("cuenca abierta", [cx, yb + c / 2]);
    t.fuste(G, rng, xd, t.B);
    return [cx, xd - xi];
  }
  function r_u(t, G, rng) { _u(t, G, rng); }
  function r_ú(t, G, rng) { const [cx] = _u(t, G, rng, "ú"); t.tilde(G, cx + 0.1 * t.c, t.B - 1.9 * t.c); }
  function r_ü(t, G, rng) {
    const [cx, w] = _u(t, G, rng);
    for (const dx of [-0.3 * w, 0.3 * w]) t.punto(G, cx + dx, t.B - 1.5 * t.c);
  }
  function r_i(t, G, rng) {
    const [, y0] = t.caja("i");
    const xs = t.astas("i", t.F - 0.3 * t.xh)[0];
    t.fuste(G, rng, xs, t.B);
    t.punto(G, xs, y0 + t.v("punto") / 2);
  }
  function r_í(t, G, rng) {
    const xs = t.astas("í", t.F - 0.3 * t.xh)[0];
    t.fuste(G, rng, xs, t.B);
    t.tilde(G, xs + 0.1 * t.c, t.B - 1.9 * t.c);
  }
  function r_j(t, G) {
    const c = t.c;
    const [x0, y0, , y1] = t.caja("j");
    const xs = ultimo(t.astas("j", t.B + 0.4 * t.xh));
    const yj = t.F + 0.25 * (t.D - t.F);
    const lado = cuencaLado(xs, yj, xs - 0.5 * (xs - x0), y1 - c / 2, t.v("pared"));
    G.trazo([[xs, t.B]].concat(lado, [[x0 + c / 2, y1 - c / 2]]));
    G.marca("corte: mira arriba", [x0 + c / 2, y1 - c / 2]);
    t.punto(G, xs, y0 + t.v("punto") / 2);
  }
  function r_f(t, G, rng) {
    const c = t.c;
    const [x0, y0, x1] = t.caja("f");
    const xs = t.astas("f", t.F - 0.3 * t.xh)[0];
    const yt = y0 + c / 2, ya = yt + 0.85 * (t.B - yt);
    const rx = (x1 - c / 2 - xs) / 2;
    const gancho = t.arco(xs + rx, ya, rx, ya - yt, 180, 40);
    G.trazo(gancho);
    t.gota(G, ultimo(gancho));
    t.fuste(G, rng, xs, ya);
    t.recta(G, rng, [x0 + c / 2, t.B + c / 2], [xs + 0.55 * (x1 - xs), t.B + c / 2]);
  }
  function r_t(t, G, rng) {
    const c = t.c;
    const [x0, y0, x1] = t.caja("t");
    const xs = t.astas("t", t.B + 0.5 * t.xh)[0];
    const ym = t.F - 0.3 * t.xh, yb = t.F - c / 2;
    const lado = cuencaLado(xs, ym, xs + 0.45 * (x1 - c / 2 - xs), yb, t.v("pared"));
    G.trazo([[xs, y0]].concat(lado, [[x1 - c / 2, yb]]));
    G.marca("corte", [xs, y0]);
    t.recta(G, rng, [x0 + c / 2, t.B + c / 2], [x1 - c / 2 - 6, t.B + c / 2]);
  }
  function r_r(t, G, rng) {
    const c = t.c;
    const [, y0, x1] = t.caja("r");
    const xs = t.astas("r", t.F - 0.3 * t.xh)[0];
    t.fuste(G, rng, xs, t.B);
    const yt = y0 + c / 2, ya = yt + 0.3 * (t.F - yt);
    const rx = (x1 - c / 2 - xs) / 2;
    const brazo = t.arco(xs + rx, ya, rx, ya - yt, 180, 55);
    G.trazo(brazo);
    t.gota(G, ultimo(brazo));
  }
  function r_k(t, G, rng) {
    const c = t.c;
    const [, y0, x1] = t.caja("k");
    const xs = t.astas("k", (t.Af + t.B) / 2)[0];
    t.fuste(G, rng, xs, y0);
    const J = [xs, t.F - 0.45 * t.xh];
    const E1 = [x1 - c / 2 - 4, t.B + c / 2];
    const Q = add(J, mul(sub(E1, J), 0.42));
    const E2 = [x1 - c / 2, t.F - 0.3 * c];
    t.recta(G, rng, J, E1, 1);
    t.recta(G, rng, Q, E2, 1);
    t.alivio(G, J, [0, -1], u(J, E1));
    t.alivio(G, Q, u(Q, E1), u(Q, E2));
  }
  function _v(t, G, x0, x1) {
    const c = t.c, cx = (x0 + x1) / 2;
    const pts = [[x0 + c / 2 + 2, t.B + 0.1 * c], [cx, t.F - c / 2], [x1 - c / 2 - 2, t.B + 0.1 * c]];
    t.quebrada(G, pts);
    alivios(t, G, pts, [1]);
  }
  function r_v(t, G) { const [x0, , x1] = t.caja("v"); _v(t, G, x0, x1); }
  function r_y(t, G, rng) {
    const c = t.c;
    const [x0, , x1, y1] = t.caja("y");
    const cx = (x0 + x1) / 2;
    const P0 = [x0 + c / 2 + 2, t.B + 0.1 * c], Vv = [cx, t.F - c / 2], P2 = [x1 - c / 2 - 2, t.B + 0.1 * c];
    const d = u(P2, Vv);
    const cola = add(Vv, mul(d, (y1 - 2.2 * c - Vv[1]) / d[1]));
    t.recta(G, rng, P0, Vv, 1);
    t.recta(G, rng, P2, cola, 2);
    t.gota(G, cola);
    t.alivio(G, Vv, u(Vv, P0), u(Vv, P2));
  }
  function r_p(t, G, rng) {
    const c = t.c;
    const [, y0, x1, y1] = t.caja("p");
    const xs = t.astas("p", (t.F + t.D) / 2)[0];
    t.fuste(G, rng, xs, t.B, y1);
    t.cuenca(G, xs, x1 - c / 2, y0 + c / 2, t.F - c / 2, { fuste: "izq" });
  }
  function r_q(t, G, rng) {
    const c = t.c;
    const [x0, y0, , y1] = t.caja("q");
    const xs = ultimo(t.astas("q", (t.F + t.D) / 2));
    t.fuste(G, rng, xs, t.B, y1);
    t.cuenca(G, x0 + c / 2, xs, y0 + c / 2, t.F - c / 2, { fuste: "der" });
  }
  function r_b(t, G, rng) {
    const c = t.c;
    const [, y0, x1] = t.caja("b");
    const xs = t.astas("b", (t.Af + t.B) / 2)[0];
    t.fuste(G, rng, xs, y0);
    t.cuenca(G, xs, x1 - c / 2, t.B + c / 2 - 3, t.F - c / 2, { fuste: "izq" });
  }
  function r_d(t, G, rng) {
    const c = t.c;
    const [x0, y0] = t.caja("d");
    const xs = ultimo(t.astas("d", (t.Af + t.B) / 2));
    t.fuste(G, rng, xs, y0);
    t.cuenca(G, x0 + c / 2, xs, t.B + c / 2 - 3, t.F - c / 2, { fuste: "der" });
  }
  function _e(t, G, s = "e") {
    const c = t.c, k = t.v("trapecio"), pared = t.v("pared"), d = t.v("desague");
    const [x0, y0, x1] = t.caja(s);
    const cx = (x0 + x1) / 2, rx = (x1 - x0) / 2 - c / 2;
    const yt = y0 + c / 2, yb = t.F - c / 2;
    const yb_ = yt + 0.47 * (yb - yt);
    const arriba = t.arco(cx, yb_, rx, yb_ - yt, 0, 180, 2);
    const izq = cuencaLado(cx - rx, yb_, cx - k * rx, yb, pared);
    const der = cuencaLado(cx + rx, yb_, cx + k * rx, yb, pared).reverse();
    const remate = der.slice(0, Math.trunc(0.45 * der.length));
    G.trazo(arriba.concat(izq.slice(1), remate));
    G.trazo([[cx - rx, yb_], [cx - d / 2, yb_]]);
    G.trazo([[cx + d / 2, yb_], [cx + rx, yb_]]);
    G.marca("desagüe del ojo", [cx, yb_ + c / 2]);
    G.marca("corte: mira arriba", ultimo(remate));
    return cx;
  }
  function r_e(t, G) { _e(t, G); }
  function r_c(t, G) {
    const c = t.c, k = t.v("trapecio"), pared = t.v("pared");
    const [x0, y0, x1] = t.caja("c");
    const cx = (x0 + x1) / 2, rx = (x1 - x0) / 2 - c / 2;
    const yt = y0 + c / 2, yb = t.F - c / 2, cy = (yt + yb) / 2;
    const arriba = t.arco(cx, cy, rx, cy - yt, 40, 180, 2);
    const izq = cuencaLado(cx - rx, cy, cx - k * rx, yb, pared);
    const der = cuencaLado(cx + rx, cy, cx + k * rx, yb, pared).reverse();
    G.trazo(arriba.concat(izq.slice(1), der.slice(0, Math.trunc(0.4 * der.length))));
    t.gota(G, arriba[0]);
  }
  function r_s(t, G) {
    const c = t.c;
    const [x0, y0, x1] = t.caja("s");
    const cx = (x0 + x1) / 2, w = x1 - x0;
    const yt = y0 + c / 2, yb = t.F - c / 2, ym = (yt + yb) / 2;
    const arriba = t.arco(cx, (yt + ym) / 2, 0.86 * (w / 2 - c / 2), (ym - yt) / 2, 25, 270, 2.2);
    const abajo = t.arco(cx, (ym + yb) / 2, w / 2 - c / 2, (yb - ym) / 2, 90, -160, 2.2);
    G.trazo(arriba.concat(abajo.slice(1)));
    t.gota(G, arriba[0]);
    G.marca("corte: mira arriba", ultimo(abajo));
  }
  function r_g(t, G, rng) {
    const c = t.c;
    const [x0, y0, x1, y1] = t.caja("g");
    const w = x1 - x0;
    const arriba = t.cuenca(G, x0 + c / 2 + 0.06 * w, x1 - c / 2 - 0.2 * w, y0 + c / 2 + 6, t.F - 0.22 * t.xh);
    const yl = t.F + 0.12 * (y1 - t.F);
    const abajo = t.cuenca(G, x0 + c / 2, x1 - c / 2 - 0.05 * w, yl, y1 - c / 2);
    const ybu = arriba.cy + arriba.ry;
    G.trazo([[arriba.cx - 0.35 * arriba.rx, ybu], [abajo.cx - 0.45 * abajo.rx, yl + 2]], t.v("sifon") * c);
    G.marca("sifón", [arriba.cx - 0.4 * arriba.rx, (ybu + yl) / 2]);
    const yo = y0 + c / 2 + 4;
    t.recta(G, rng, [arriba.cx + 0.55 * arriba.rx, yo], [x1 - c / 2, yo], 1);
  }
  function r_coma(t, G, rng, cx = null) {
    if (cx === null) cx = cxDe(t.caja(","));
    t.punto(G, cx, t.F - t.v("punto") / 2);
    t.gota(G, [cx, t.F]);
  }
  function r_punto(t, G) { t.punto(G, cxDe(t.caja(".")), t.F - t.v("punto") / 2); }
  function _parentesis(t, G, s, izq) {
    const c = t.c;
    const [x0, y0, x1, y1] = t.caja(s);
    const rx = (x1 - x0) - c;
    const cy = (y0 + y1) / 2, ry = (y1 - y0) / 2 - c / 2;
    G.trazo(izq ? t.arco(x0 + c / 2 + rx, cy, rx, ry, 118, 242, 2.4) : t.arco(x1 - c / 2 - rx, cy, rx, ry, 62, -62, 2.4));
  }
  function r_abre(t, G) { _parentesis(t, G, "(", true); }
  function r_cierra(t, G) { _parentesis(t, G, ")", false); }
  function r_á(t, G, rng) { const cx = r_a(t, G, rng); t.tilde(G, cx + 0.2 * t.c, t.B - 1.9 * t.c); }
  function r_ó(t, G, rng) { const m = r_o(t, G, rng); t.tilde(G, m.cx + 0.1 * t.c, t.B - 1.9 * t.c); }
  function r_é(t, G) { const cx = _e(t, G); t.tilde(G, cx + 0.1 * t.c, t.B - 1.9 * t.c); }
  function r_ñ(t, G, rng) {
    const [xi, xd] = r_n(t, G, rng);
    t.onda(G, xi - 0.1 * t.c, xd + 0.1 * t.c, t.B - 1.6 * t.c);
  }
  function r_z(t, G) {
    const c = t.c;
    const [x0, , x1] = t.caja("v");
    const pts = [[x0 + c / 2 + 6, t.B + c / 2], [x1 - c / 2 - 6, t.B + c / 2], [x0 + c / 2 + 6, t.F - c / 2],
      [x1 - c / 2 - 6, t.F - c / 2]];
    t.quebrada(G, pts);
    alivios(t, G, pts, [1, 2]);
  }
  function r_w(t, G) {
    const c = t.c;
    const [x0, , x1] = t.caja("m");
    const W = x1 - x0, cx = (x0 + x1) / 2;
    const pts = [[x0 + c / 2, t.B + 0.1 * c], [x0 + 0.27 * W, t.F - c / 2], [cx, t.B + 0.32 * t.xh],
      [x1 - 0.27 * W, t.F - c / 2], [x1 - c / 2, t.B + 0.1 * c]];
    t.quebrada(G, pts);
    alivios(t, G, pts, [1, 2, 3]);
  }
  function r_x(t, G, rng) {
    const c = t.c;
    const [x0, , x1] = t.caja("v");
    const a = [x0 + c / 2, t.B + 0.1 * c], b = [x1 - c / 2, t.F - 0.1 * c];
    const a2 = [x1 - c / 2, t.B + 0.1 * c], b2 = [x0 + c / 2, t.F - 0.1 * c];
    t.recta(G, rng, a, b, 2);
    t.recta(G, rng, a2, b2, 2);
    const C = mul(add(a, b), 0.5);
    t.alivio(G, C, u(C, a), u(C, a2));
    t.alivio(G, C, u(C, b), u(C, b2));
  }
  function anchoO(t) { const [x0, , x1] = t.caja("o"); return x1 - x0; }
  function r_pregunta(t, G, rng) {
    const c = t.c, cx = t.T / 2;
    const rx = 0.8 * (anchoO(t) / 2 - c / 2);
    const yt = t.Af + 0.3 * (t.B - t.Af) + c / 2;
    const ry = 0.27 * (t.F - yt), yc = yt + ry;
    const arco = t.arco(cx, yc, rx, ry, 165, -90, 2.2);
    G.trazo(arco);
    t.gota(G, arco[0]);
    t.recta(G, rng, [cx, yc + ry], [cx, t.F - 1.9 * c], 1);
    t.punto(G, cx, t.F - t.v("punto") / 2);
  }
  function r_abre_pregunta(t, G, rng) {
    const c = t.c, cx = t.T / 2;
    const rx = 0.8 * (anchoO(t) / 2 - c / 2);
    const yt = t.Af + 0.3 * (t.B - t.Af) + c / 2;
    const ry = 0.27 * (t.F - yt);
    const abajo = t.D - 0.2 * (t.D - t.F);
    const ys = abajo - c / 2 - 2 * ry;
    t.punto(G, cx, t.B + t.v("punto") / 2);
    t.recta(G, rng, [cx, t.B + 1.9 * c], [cx, ys], 1);
    const arco = t.arco(cx, ys + ry, rx, ry, 90, 345, 2.2);
    G.trazo(arco);
    G.marca("sin gota: la gravedad no se da vuelta", ultimo(arco));
  }
  function r_punto_y_coma(t, G, rng) { t.punto(G, t.T / 2, t.B + 0.9 * t.c); r_coma(t, G, rng, t.T / 2); }
  function r_dos_puntos(t, G) { t.punto(G, t.T / 2, t.B + 0.9 * t.c); t.punto(G, t.T / 2, t.F - t.v("punto") / 2); }
  function _comillas(t, G, rng, abre) {
    const c = t.c, ym = t.B + 0.5 * t.xh, h = 0.26 * t.xh;
    const wc = 0.28 * anchoO(t);
    for (const i of [-1, 1]) {
      const xa = t.T / 2 + i * (wc / 2 + 0.4 * c) + rng.normal(0, 1.5);
      const tip = abre ? [xa - wc / 2, ym + rng.normal(0, 1.5)] : [xa + wc / 2, ym + rng.normal(0, 1.5)];
      const lado = abre ? xa + wc / 2 : xa - wc / 2;
      const p0 = [lado, ym - h + rng.normal(0, 1.5)];
      const p2 = [lado, ym + h + rng.normal(0, 1.5)];
      const pts = [p0, tip, p2];
      t.quebrada(G, pts);
      alivios(t, G, pts, [1]);
    }
  }
  function r_abre_comillas(t, G, rng) { _comillas(t, G, rng, true); }
  function r_cierra_comillas(t, G, rng) { _comillas(t, G, rng, false); }
  function r_raya(t, G, rng) {
    const w = 0.62 * anchoO(t) * 2;
    t.recta(G, rng, [t.T / 2 - w / 2, t.B + 0.5 * t.xh], [t.T / 2 + w / 2, t.B + 0.5 * t.xh], 3);
  }
  function r_suspensivos(t, G) { for (const dx of [-1.9, 0, 1.9]) t.punto(G, t.T / 2 + dx * t.c, t.F - t.v("punto") / 2); }

  function _cifra(t, G) {
    const [, iy0, , iy1] = t.celdaCifra(G);
    const c = t.c, w = 0.78 * anchoO(t);
    return { cx: t.T / 2, rx: w / 2 - c / 2, w, sube: iy0 + 1.1 * c, baja: iy1 - 1.1 * c };
  }
  function r_0(t, G) {
    const k = _cifra(t, G);
    t.cuenca(G, k.cx - 0.85 * k.rx, k.cx + 0.85 * k.rx, t.B + t.c / 2, t.F - t.c / 2);
  }
  function r_1(t, G, rng) {
    const k = _cifra(t, G), c = t.c;
    const xs = k.cx + 0.05 * k.w;
    t.fuste(G, rng, xs, t.B);
    const top = [xs, t.B + c / 2], fin = [xs - 0.34 * k.w, t.B + 0.32 * t.xh];
    t.recta(G, rng, top, fin, 1);
    t.alivio(G, top, u(top, fin), [0, 1]);
  }
  function r_2(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const yt = t.B + c / 2, ry = 0.3 * t.xh;
    const arco = t.arco(cx, yt + ry, rx, ry, 160, -25, 2.2);
    const esquina = [cx - rx, t.F - c / 2];
    const base = filetear([ultimo(arco), esquina, [cx + rx, t.F - c / 2]], t.v("radio_chapa"));
    G.trazo(arco.concat(base.slice(1)));
    t.gota(G, arco[0]);
    t.alivio(G, esquina, u(esquina, ultimo(arco)), [1, 0], t.v("radio_chapa"));
  }
  function r_3(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const yt = t.B + c / 2, yb = k.baja - c / 2, ym = yt + 0.42 * (yb - yt);
    const arriba = t.arco(cx, (yt + ym) / 2, 0.85 * rx, (ym - yt) / 2, 150, -90, 2.2);
    const abajo = t.arco(cx, (ym + yb) / 2, rx, (yb - ym) / 2, 90, -150, 2.2);
    G.trazo(arriba.concat(abajo.slice(1)));
    t.gota(G, arriba[0]);
    G.marca("corte: mira arriba", ultimo(abajo));
  }
  function r_4(t, G, rng) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const xs = cx + 0.22 * k.w, yb = t.F - 0.2 * t.xh;
    t.fuste(G, rng, xs, t.B, k.baja);
    const top = [xs, t.B + c / 2], esq = [cx - rx - 0.1 * c, yb];
    t.recta(G, rng, top, esq, 1);
    t.recta(G, rng, esq, [cx + rx + 0.1 * c, yb], 1);
    t.alivio(G, top, u(top, esq), [0, 1]);
    t.alivio(G, esq, u(esq, top), [1, 0]);
  }
  function r_5(t, G, rng) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const yt = t.B + c / 2, yb = k.baja - c / 2, ym = yt + 0.36 * (yb - yt);
    const panza = t.arco(cx, (ym + yb) / 2, rx, (yb - ym) / 2, 145, -150, 2.2);
    const xs = panza[0][0];
    t.recta(G, rng, [xs, yt], [cx + rx, yt], 1);
    t.recta(G, rng, [xs, yt], panza[0], 1);
    G.trazo(panza);
    G.marca("corte: mira arriba", ultimo(panza));
  }
  function r_6(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const m = t.cuenca(G, cx - rx, cx + rx, t.B + c / 2, t.F - c / 2);
    const sube = t.arco(cx, m.cy, rx, m.cy - (k.sube + c / 2), 180, 55, 2.2);
    G.trazo(sube);
    t.gota(G, ultimo(sube));
  }
  function r_7(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const yt = t.B + c / 2;
    const pts = [[cx - rx, yt], [cx + rx, yt], [cx - 0.2 * rx, k.baja]];
    t.quebrada(G, pts);
    alivios(t, G, pts, [1]);
  }
  function r_8(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const yt = k.sube + c / 2, yb = t.F - c / 2, ym = yt + 0.44 * (yb - yt);
    t.cuenca(G, cx - 0.78 * rx, cx + 0.78 * rx, yt, ym);
    t.cuenca(G, cx - rx, cx + rx, ym, yb, { huecos_arriba: [cx] });
    G.marca("sifón", [cx, ym]);
  }
  function r_9(t, G) {
    const k = _cifra(t, G), c = t.c, cx = k.cx, rx = k.rx;
    const m = t.cuenca(G, cx - rx, cx + rx, t.B + c / 2, t.F - c / 2);
    const baja = t.arco(cx, m.cy, rx, k.baja - c / 2 - m.cy, 0, -140, 2.2);
    G.trazo(baja);
    G.marca("sin gota: la gravedad no se da vuelta", ultimo(baja));
  }

  const RECETAS = {
    o: r_o, l: r_l, n: r_n, a: r_a, h: r_h, m: r_m, u: r_u, "ú": r_ú, i: r_i, "í": r_í, j: r_j, f: r_f, t: r_t,
    r: r_r, k: r_k, v: r_v, y: r_y, p: r_p, q: r_q, b: r_b, d: r_d, e: r_e, c: r_c, s: r_s, g: r_g, ",": r_coma,
    ".": r_punto, "(": r_abre, ")": r_cierra, "á": r_á, "ó": r_ó, "é": r_é, "ñ": r_ñ, z: r_z, w: r_w, x: r_x,
    "ü": r_ü, "?": r_pregunta, "¿": r_abre_pregunta, ";": r_punto_y_coma, ":": r_dos_puntos, "«": r_abre_comillas,
    "»": r_cierra_comillas, "—": r_raya, "…": r_suspensivos, 0: r_0, 1: r_1, 2: r_2, 3: r_3, 4: r_4, 5: r_5,
    6: r_6, 7: r_7, 8: r_8, 9: r_9,
  };

  // ------------------------------------------------------------------ el azar de Python, repetido
  function azarGrabado(cinta) {
    let i = 0;
    return {
      choice() { const v = i < cinta.length ? cinta[i] : 1; i++; return v; },
      normal(mu, sd) { const z = i < cinta.length ? cinta[i] : 0; i++; return mu + sd * z; },
    };
  }

  // ------------------------------------------------------------------ el cuerpo, con Clipper
  const S = 256;                    // escala entera de Clipper: 1/256 de píxel
  const TOLERANCIA = 0.02 * S;      // el error de cada arco: 0,02 px

  const aRuta = (pts) => pts.map((p) => ({ X: Math.round(p[0] * S), Y: Math.round(p[1] * S) }));

  /* Ramer-Douglas-Peucker: saca los puntos que se apartan menos de tol de la recta (el eje
   * remuestreado cada píxel tiene cientos; el contorno no cambia en más de tol). */
  function simplificar(pts, tol) {
    const n = pts.length;
    if (n < 3) return pts;
    const quedan = new Uint8Array(n);
    quedan[0] = quedan[n - 1] = 1;
    const pila = [[0, n - 1]];
    while (pila.length) {
      const [a, b] = pila.pop();
      const [ax, ay] = pts[a], [bx, by] = pts[b];
      const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy);
      let peor = -1, dmax = tol;
      for (let i = a + 1; i < b; i++) {
        const [px, py] = pts[i];
        const d = L > 1e-12 ? Math.abs(dy * (px - ax) - dx * (py - ay)) / L : Math.hypot(px - ax, py - ay);
        if (d > dmax) { dmax = d; peor = i; }
      }
      if (peor >= 0) { quedan[peor] = 1; pila.push([a, peor], [peor, b]); }
    }
    return pts.filter((_, i) => quedan[i]);
  }
  const deRuta = (r) => r.map((p) => [p.X / S, p.Y / S]);

  function positiva(r) { return CL.Clipper.Orientation(r) ? r : r.slice().reverse(); }

  function ensanchar(rutas, delta, abiertas) {
    const co = new CL.ClipperOffset(2, TOLERANCIA);
    co.AddPaths(rutas, CL.JoinType.jtRound, abiertas ? CL.EndType.etOpenButt : CL.EndType.etClosedPolygon);
    const sol = new CL.Paths();
    co.Execute(sol, delta);
    return sol;
  }

  function operar(tipo, sujeto, recorte, relleno) {
    const c = new CL.Clipper();
    c.AddPaths(sujeto, CL.PolyType.ptSubject, true);
    if (recorte.length) c.AddPaths(recorte, CL.PolyType.ptClip, true);
    const sol = new CL.Paths();
    c.Execute(tipo, sol, relleno, relleno);
    return sol;
  }

  /* Trazos del ancho del canal (o del suyo), más asientos, gotas y tildes, menos alivios; gastado.
   * Devuelve anillos en píxeles (exteriores positivos, huecos al revés). */
  function cuerpo(G, P, c) {
    const porAncho = new Map();
    for (const [t, w] of G.trazos) {
      const ancho = w === null ? c : w;
      if (t.length < 2 || ancho < 0.05) continue;
      if (!porAncho.has(ancho)) porAncho.set(ancho, []);
      porAncho.get(ancho).push(aRuta(simplificar(t, 0.1)));
    }
    let partes = [];
    for (const [ancho, rutas] of porAncho) partes = partes.concat(ensanchar(rutas, ancho / 2 * S, true));
    for (const m of G.mas) partes.push(positiva(aRuta(m)));
    let geo = operar(CL.ClipType.ctUnion, partes, [], CL.PolyFillType.pftPositive);
    if (G.menos.length) {
      const menos = G.menos.map((m) => positiva(aRuta(circulo(m.x, m.y, m.r, 128))));
      geo = operar(CL.ClipType.ctDifference, geo, menos, CL.PolyFillType.pftNonZero);
    }
    const r = V(P, "intemperie");
    if (r > 0) geo = ensanchar(ensanchar(geo, -r * S, false), r * S, false);
    return geo.map(deRuta);
  }

  function limites(anillos) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const a of anillos) for (const [x, y] of a) {
      if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
    }
    return [x0, y0, x1, y1];
  }

  /* Relleno par-impar, muestreando cada píxel en su centro (como cv2.fillPoly). */
  function rasterizar(anillos, T) {
    const m = crear(T);
    const bordes = [];
    for (const a of anillos) for (let i = 0; i < a.length; i++) {
      const p = a[i], q = a[(i + 1) % a.length];
      if (p[1] !== q[1]) bordes.push(p[1] < q[1] ? [p[0], p[1], q[0], q[1]] : [q[0], q[1], p[0], p[1]]);
    }
    const xs = [];
    for (let y = 0; y < T; y++) {
      xs.length = 0;
      for (const [xa, ya, xb, yb] of bordes) if (y >= ya && y < yb) xs.push(xa + (y - ya) * (xb - xa) / (yb - ya));
      xs.sort((a, b) => a - b);
      for (let k = 0; k + 1 < xs.length; k += 2) {
        const a = Math.max(0, Math.ceil(xs[k])), b = Math.min(T - 1, Math.floor(xs[k + 1]));
        for (let x = a; x <= b; x++) m[y * T + x] = 1;
      }
    }
    return m;
  }

  // ------------------------------------------------------------------ todo junto
  /* Arma el pie: decodifica los testigos (una vez) y los achata a la razón pedida. */
  const cacheTestigos = new Map();
  function testigos(D) {
    if (!cacheTestigos.has(D)) {
      const M = {};
      for (const [s, t] of Object.entries(D.testigos)) M[s] = decodificar(t, D.T);
      cacheTestigos.set(D, M);
    }
    return cacheTestigos.get(D);
  }

  function pie(D, razon) {
    const T = D.T, M0 = testigos(D), m0 = D.medidas_sustituto;
    const xhNueva = m0.asc / razon;
    const M = {};
    for (const [s, m] of Object.entries(M0)) M[s] = Math.abs(xhNueva - m0.xh) < 1e-9 ? m : achatar(m, T, D.base, m0.asc, m0.xh, xhNueva);
    const med = medidas(M, T, D.base);
    return { M, med };
  }

  // el pie achatado y su esqueleto solo cambian con la razón: se guardan los dos últimos
  const cachePie = [];
  function pieYEsqueleto(D, razon, halladas) {
    let p = cachePie.find((c) => c.D === D && c.razon === razon);
    if (!p) {
      const { M, med } = pie(D, razon);
      p = { D, razon, M, med, e: esqueleto(M, med, D.T, halladas) };
      cachePie.unshift(p);
      cachePie.length = Math.min(cachePie.length, 2);
    }
    return p;
  }

  function preparar(D, ajustes) {
    const T = D.T;
    const halladas = D.caja.filter((c) => c.estado === "hallada").map((c) => c.signo);
    const razon = ajustes.razon_x !== undefined ? ajustes.razon_x : D.razon_foto;
    const { M, med, e: e0 } = pieYEsqueleto(D, razon, halladas);
    const e = Object.assign({}, e0);
    const P = parametros(e, ajustes, D.parametros);
    if (ajustes.canal !== undefined) e.canal = ajustes.canal;
    const t = new Taller(e, P, M, T);
    return { T, M, med, e, P, t, razon, halladas };
  }

  function construir(base, D, s) {
    const G = new Glifo(s);
    RECETAS[s](base.t, G, azarGrabado(D.azar[s] || []));
    let geo = cuerpo(G, base.P, base.t.c);
    const [x0, , x1] = limites(geo);
    const dx = base.T / 2 - (x0 + x1) / 2;
    G.mover(dx);
    geo = geo.map((a) => a.map((p) => [p[0] + dx, p[1]]));
    return { signo: s, glifo: G, geo, receta: D.recetas[s] + (/\d/.test(s) ? "; en su celda" : "") };
  }

  function construirTodo(D, ajustes = {}) {
    const base = preparar(D, ajustes);
    const signos = {};
    for (const c of D.caja) if (RECETAS[c.signo]) signos[c.signo] = construir(base, D, c.signo);
    return Object.assign(base, { signos });
  }

  /* El cuerpo en SVG, en píxeles del azulejo (600 = 150 mm). */
  function aSvg(geo, e, T, signo) {
    let d = "";
    for (const a of geo) d += "M" + a.map(([x, y]) => x.toFixed(2) + "," + y.toFixed(2)).join(" L") + " Z ";
    const [x0, y0, x1, y1] = celda(e, T);
    const lineas = [["afuera", e.afuera], ["borde", e.borde], ["fondo", e.fondo], ["desagüe", e.desague]]
      .map(([n, y]) => `<line x1="0" y1="${y.toFixed(1)}" x2="${T}" y2="${y.toFixed(1)}" stroke="#9a968d" stroke-dasharray="6 5"/>` +
        `<text x="6" y="${(y - 6).toFixed(1)}" font-family="monospace" font-size="14" fill="#6d6a63">${n}</text>`).join("");
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${T} ${T}" width="150mm" height="150mm">\n` +
      `<rect width="${T}" height="${T}" fill="#f3f1ea"/>\n` +
      `<rect x="${x0.toFixed(1)}" y="${y0.toFixed(1)}" width="${(x1 - x0).toFixed(1)}" height="${(y1 - y0).toFixed(1)}" fill="none" stroke="#cfcac0" stroke-width="2"/>\n` +
      `${lineas}\n<path d="${d.trim()}" fill="#1d1c1a" fill-rule="evenodd"/>\n` +
      `<!-- Contenida · ${signo} · cuerpo base (propuesta de la máquina) -->\n</svg>\n`;
  }

  raiz.Gramatica = {
    construirTodo, preparar, construir, rasterizar, cajaTinta, celda, aSvg, limites, decodificar, achatar, medidas,
    esqueleto, parametros, RECETAS, V, superelipse, filetear, circulo, remuestrear, corridas,
  };
})(typeof window !== "undefined" ? window : globalThis);
