/* El repujado de Contenida: la hoja, el punzón, la base, el surco, la rotura y la luz.
 *
 * Acción 4 del taller (04_taller_analogico.md): una hoja de papel de aluminio de cocina, cortada a tijera,
 * sobre una base blanda. La mano repasa el calco por el reverso, en espejo, con un punzón de bola; por el
 * anverso sale la letra en relieve. Todo se mide en milímetros: la placa es un azulejo de 150 mm y la altura
 * es la del aluminio, positiva hacia el anverso.
 *
 * La manera viene de una herramienta de dibujo, Vooolume, de Krftoools (README): un mapa de alturas donde cada
 * trazo levanta su perfil y se funde con los otros, una textura que es del material y no del trazo, y una luz
 * que se calcula al final, de modo que moverla vuelve a iluminar todo lo hecho. Lo que cambia es el material:
 * el perfil es el de una bola apretada contra una base blanda, la herramienta empuja hacia la cara de abajo,
 * el aluminio no olvida (no hay goma) y se rompe si se lo fuerza.
 *
 * Sin dependencias: corre en el navegador (index.html) y en Node (prueba.mjs).
 */
(function (raiz, fabrica) {
  const api = fabrica();
  if (typeof module === "object" && module.exports) module.exports = api;
  else raiz.Repujado = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const LADO = 150;              // mm: una placa es un azulejo
  const SEMILLA = 20260822;      // el día de la obra, como en simulacion/comun.py
  const TRAMO = 0.5;             // mm: el surco se estampa por tramos de este largo
  const PUNTEADO = 2.25;         // mm entre dos puntos (9 px a 4 px/mm, como simulacion/contener.py)
  const CELDA = 0.5;             // mm: la grilla donde el aluminio acumula el esfuerzo
  const GRILLA = Math.round(LADO / CELDA);
  const DESAGUE = 3;             // mm: el punzón se detiene antes de cerrar cada contorno (03b, regla 2)
  const TENACIDAD = 4.4;         // escala de Weibull del esfuerzo que rompe una celda (supuesto)
  /* El tiempo de la mano simulada (simulacion/pulso.py), con sus levantadas, dudas y lecturas del anverso: mm
   * por minuto de surco y de punteado, y minutos para cortar la hoja y pegar el calco, y para retirarlo. */
  const MANO = { surco: 230, punteado: 136, preparar: 4, retirar: 1 };

  /* La base decide cuánto se hunde el aluminio con presión 1 (hondo, mm), cuánto se abre el surco (abre),
   * cuánto sube a los lados el aluminio que se corre (lomas) y hasta dónde se hunde sin romperse (limite, mm).
   * Son supuestos de la máquina: se miden con una placa de prueba. */
  const BASES = {
    fieltro: { nombre: "fieltro", hondo: 1.0, abre: 0.85, lomas: 0.13, limite: 1.6 },
    eva: { nombre: "goma eva", hondo: 0.75, abre: 0.65, lomas: 0.17, limite: 1.2 },
    periodico: { nombre: "una pila de periódico", hondo: 0.52, abre: 0.5, lomas: 0.22, limite: 0.9 },
    alfombrilla: { nombre: "una alfombrilla de ratón", hondo: 0.8, abre: 0.7, lomas: 0.15, limite: 1.3 },
  };
  /* Las puntas de la Acción 4, por el radio de su bola (mm). */
  const PUNZONES = {
    bola: { nombre: "punzón de bola de 1 mm", radio: 0.5 },
    boligrafo: { nombre: "bolígrafo sin tinta", radio: 0.35 },
    brocheta: { nombre: "palito de brocheta, la punta redondeada", radio: 0.9 },
  };

  // ---------------------------------------------------------------- azar reproducible
  function hash32(texto) {
    let h = 2166136261;
    for (let i = 0; i < texto.length; i++) { h ^= texto.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  /* Un generador para cada cosa (la hoja, un trazo, una rotura): la misma placa sale siempre igual. */
  function azar(...claves) {
    let a = hash32([SEMILLA, ...claves].join("|"));
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function gauss(r) {
    let u = r();
    while (u <= 1e-12) u = r();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r());
  }

  /* Ruido de gradiente, suave, entre −1 y 1. */
  function ruido(semilla) {
    const r = azar("ruido", semilla);
    const p = new Uint8Array(256);
    for (let i = 0; i < 256; i++) p[i] = i;
    for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); const t = p[i]; p[i] = p[j]; p[j] = t; }
    const perm = new Uint8Array(512);
    for (let i = 0; i < 512; i++) perm[i] = p[i & 255];
    const gx = new Float32Array(256), gy = new Float32Array(256);
    for (let i = 0; i < 256; i++) { const a = r() * 2 * Math.PI; gx[i] = Math.cos(a); gy[i] = Math.sin(a); }
    return function (x, y) {
      const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
      const X = xi & 255, Y = yi & 255;
      const a = perm[X + perm[Y]], b = perm[X + 1 + perm[Y]], c = perm[X + perm[Y + 1]], d = perm[X + 1 + perm[Y + 1]];
      const u = xf * xf * xf * (xf * (xf * 6 - 15) + 10), v = yf * yf * yf * (yf * (yf * 6 - 15) + 10);
      const n00 = gx[a] * xf + gy[a] * yf, n10 = gx[b] * (xf - 1) + gy[b] * yf;
      const n01 = gx[c] * xf + gy[c] * (yf - 1), n11 = gx[d] * (xf - 1) + gy[d] * (yf - 1);
      const x0 = n00 + u * (n10 - n00), x1 = n01 + u * (n11 - n01);
      return 1.4 * (x0 + v * (x1 - x0));
    };
  }

  /* Celdas de Voronoi de lado l (mm): la distancia al segundo vecino menos la del primero, en unidades de celda.
   * Sus bordes son rectos y se cruzan en vértices, como los pliegues de una hoja arrugada y vuelta a alisar.
   * Los puntos se sortean una vez, para toda la placa. */
  function celdas(semilla, l) {
    const r = azar("celdas", semilla), n = Math.ceil(LADO / l) + 4;
    const px = new Float32Array(n * n), py = new Float32Array(n * n);
    for (let j = 0; j < n; j++) {
      for (let i = 0; i < n; i++) { px[j * n + i] = i - 2 + 0.1 + 0.8 * r(); py[j * n + i] = j - 2 + 0.1 + 0.8 * r(); }
    }
    return function (x, y) {
      const ix = Math.floor(x) + 2, iy = Math.floor(y) + 2;
      let f1 = 9, f2 = 9;
      for (let j = iy - 1; j <= iy + 1; j++) {
        const o = j * n;
        for (let i = ix - 1; i <= ix + 1; i++) {
          const dx = px[o + i] - x, dy = py[o + i] - y, d = dx * dx + dy * dy;
          if (d < f1) { f2 = f1; f1 = d; } else if (d < f2) f2 = d;
        }
      }
      return Math.sqrt(f2) - Math.sqrt(f1);
    };
  }

  // ---------------------------------------------------------------- la hoja
  /* El contorno de una hoja cortada a tijera, en mm (simulacion/contener.py, tijera): cada lado en dos o tres
   * cortes casi rectos, con un escalón chico donde la tijera se retoma; a veces una esquina va en diagonal. */
  function tijera(r) {
    const c = LADO / 2;
    const m = [0, 1, 2, 3].map(() => 4 - 1.25 + r() * 3.5);
    const a = [0, 1, 2, 3].map(() => Math.tan(gauss(r) * 0.8 * Math.PI / 180));
    function esquina(i) {
      let x = c, y = c;
      for (let k = 0; k < 4; k++) {
        if (i === 0) { y = m[0] + (x - c) * a[0]; x = LADO - m[1] - (y - c) * a[1]; }
        else if (i === 1) { x = LADO - m[1] - (y - c) * a[1]; y = LADO - m[2] - (x - c) * a[2]; }
        else if (i === 2) { y = LADO - m[2] - (x - c) * a[2]; x = m[3] + (y - c) * a[3]; }
        else { x = m[3] + (y - c) * a[3]; y = m[0] + (x - c) * a[0]; }
      }
      return [x, y];
    }
    const esq = [esquina(3), esquina(0), esquina(1), esquina(2)];      // en sentido horario, desde arriba a la izquierda
    const pts = [], inicio = [];
    for (let lado = 0; lado < 4; lado++) {
      const P = esq[lado], Q = esq[(lado + 1) % 4];
      const L = Math.hypot(Q[0] - P[0], Q[1] - P[1]);
      const n = [-(Q[1] - P[1]) / L, (Q[0] - P[0]) / L];                // hacia adentro
      const cortes = Array.from({ length: 1 + Math.floor(r() * 2) }, () => 0.2 + 0.6 * r()).sort((p, q) => p - q);
      const t = [0, ...cortes, 1];
      inicio.push(pts.length);
      for (let i = 0; i < t.length - 1; i++) {
        const escalon = i > 0 ? gauss(r) * 0.275 : 0, desvio = gauss(r) * 0.35;
        pts.push([P[0] + t[i] * (Q[0] - P[0]) + escalon * n[0], P[1] + t[i] * (Q[1] - P[1]) + escalon * n[1]]);
        pts.push([P[0] + t[i + 1] * (Q[0] - P[0]) + (escalon + desvio) * n[0],
          P[1] + t[i + 1] * (Q[1] - P[1]) + (escalon + desvio) * n[1]]);
      }
    }
    const hacia = (p, q, d) => { const L = Math.hypot(q[0] - p[0], q[1] - p[1]); return [p[0] + (q[0] - p[0]) * d / L, p[1] + (q[1] - p[1]) * d / L]; };
    for (let e = 0; e < 4; e++) {
      if (r() >= 0.35) continue;
      const corte = 6 + 6.5 * r(), s = inicio[e], n = pts.length;
      const antes = (s - 1 + n) % n;
      pts[antes] = hacia(pts[antes], pts[(s - 2 + n) % n], corte);
      pts[s] = hacia(pts[s], pts[(s + 1) % n], corte);
    }
    return pts;
  }

  /* El polígono en la grilla: cuánto de cada píxel es aluminio (M) y a qué distancia está del filo (B, mm). */
  function rasterizar(pol, N) {
    const mm = LADO / N, M = new Float32Array(N * N), B = new Float32Array(N * N).fill(99);
    const n = pol.length, xs = [];
    for (let y = 0; y < N; y++) {
      const yc = (y + 0.5) * mm;
      xs.length = 0;
      for (let i = 0; i < n; i++) {
        const [x0, y0] = pol[i], [x1, y1] = pol[(i + 1) % n];
        if ((y0 <= yc) !== (y1 <= yc)) xs.push(x0 + (yc - y0) * (x1 - x0) / (y1 - y0));
      }
      xs.sort((p, q) => p - q);
      for (let k = 0; k + 1 < xs.length; k += 2) {
        const a = Math.max(0, Math.ceil(xs[k] / mm - 0.5)), b = Math.min(N - 1, Math.floor(xs[k + 1] / mm - 0.5));
        M.fill(1, y * N + a, y * N + b + 1);
      }
    }
    const banda = 3;
    for (let i = 0; i < n; i++) {
      const [ax, ay] = pol[i], [bx, by] = pol[(i + 1) % n];
      const dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy || 1;
      const x0 = Math.max(0, Math.floor((Math.min(ax, bx) - banda) / mm)), x1 = Math.min(N - 1, Math.ceil((Math.max(ax, bx) + banda) / mm));
      const y0 = Math.max(0, Math.floor((Math.min(ay, by) - banda) / mm)), y1 = Math.min(N - 1, Math.ceil((Math.max(ay, by) + banda) / mm));
      for (let y = y0; y <= y1; y++) {
        const py = (y + 0.5) * mm - ay;
        for (let x = x0; x <= x1; x++) {
          const px = (x + 0.5) * mm - ax;
          let t = (px * dx + py * dy) / L2;
          t = t < 0 ? 0 : t > 1 ? 1 : t;
          const ex = px - t * dx, ey = py - t * dy, d = Math.sqrt(ex * ex + ey * ey), j = y * N + x;
          if (d < B[j]) B[j] = d;
        }
      }
    }
    for (let j = 0; j < N * N; j++) {          // el filo, suavizado
      const d = B[j] / mm;
      if (d < 0.5) M[j] = M[j] > 0.5 ? 0.5 + d : 0.5 - d;
    }
    return { M, B };
  }

  /* Las arrugas de la hoja, en mm: ondas largas, pliegues rectos que se cruzan en vértices (de la hoja
   * arrugada y vuelta a alisar), el veteado del laminado, uno o dos dobleces del rollo y el filo de la tijera,
   * un poco levantado. Son del material, no del trazo: están antes de repujar. */
  function arrugas(N, semilla, cantidad, M, B) {
    const mm = LADO / N, A = new Float32Array(N * N), r = azar("hoja", semilla);
    const ondas = ruido(semilla + "/ondas"), veta = ruido(semilla + "/veta"), filo = ruido(semilla + "/filo");
    const pendiente = 0.15 * cantidad;
    const pliegues = [16, 6.5, 2.6, 1.1].map((l, i) => ({ l, s: i % 2 ? -1 : 1, a: pendiente * l * 0.5, f: celdas(semilla + "/arruga" + i, l) }));
    const dobleces = [];
    const nd = 2 + Math.floor(r() * 2 * cantidad);                      // dos dobleces, como en contener.py
    for (let k = 0; k < nd; k++) {
      const ang = r() * Math.PI;
      dobleces.push({
        cx: (0.1 + 0.8 * r()) * LADO, cy: (0.1 + 0.8 * r()) * LADO, ux: Math.cos(ang), uy: Math.sin(ang),
        alto: (r() < 0.5 ? -1 : 1) * (0.06 + 0.08 * r()), ancho: 0.35 + 0.35 * r(),
        largo: (0.5 + 0.7 * r()) * LADO, desvio: ruido(semilla + "/doblez" + k),
      });
    }
    const ondaLarga = 0.45 * (0.8 + 0.4 * cantidad), ondaCorta = 0.09 * (0.6 + 0.8 * cantidad);
    for (let y = 0; y < N; y++) {
      const Y = (y + 0.5) * mm;
      for (let x = 0; x < N; x++) {
        const j = y * N + x;
        if (M[j] <= 0 && B[j] > 1) continue;                  // fuera de la hoja no hay aluminio
        const X = (x + 0.5) * mm;
        let h = ondaLarga * ondas(X / 30, Y / 30) + ondaCorta * ondas(X / 4.5 + 31.7, Y / 4.5 - 12.3);
        if (cantidad > 0) {
          for (const p of pliegues) h += p.s * p.a * Math.min(p.f(X / p.l, Y / p.l), 0.55);
        }
        h += 0.007 * veta(X / 22, Y / 0.2);                   // el veteado, a lo largo del laminado
        for (const d of dobleces) {
          const ex = X - d.cx, ey = Y - d.cy;
          const s = Math.abs(ex * d.ux + ey * d.uy) - d.largo / 2;
          if (s > 25) continue;                                 // más allá de la punta del doblez, nada
          const q = -ex * d.uy + ey * d.ux + 0.9 * d.desvio(X / 11, Y / 11), z = q / 7.5;
          const escalon = z > 3 ? 1 : z < -3 ? -1 : z * (27 + z * z) / (27 + 9 * z * z);      // tanh, aproximada
          const nucleo = q * q < 16 * d.ancho * d.ancho ? Math.exp(-0.5 * (q / d.ancho) ** 2) : 0;
          h += d.alto * (nucleo + 0.25 * escalon) / (1 + Math.exp(s / 3));
        }
        if (M[j] > 0) h += 0.11 * Math.exp(-B[j] / 0.55) * (1 + 0.5 * filo(X / 1.8, Y / 1.8));   // el filo de la tijera
        A[j] = h;
      }
    }
    return A;
  }

  /* El umbral de cada celda: cuánto esfuerzo aguanta antes de romperse. Weibull de módulo 6, con semilla: la hoja
   * es pareja, y se rompe por trabajarla de más, no por un punto débil al azar. */
  function umbral(semilla, c) {
    const u = (hash32(`fatiga|${semilla}|${c}`) + 0.5) / 4294967296;
    return TENACIDAD * Math.pow(-Math.log(1 - u), 1 / 6);
  }

  // ---------------------------------------------------------------- el perfil del surco
  function erf(x) {                                            // Abramowitz y Stegun, 7.1.26
    const s = x < 0 ? -1 : 1, z = Math.abs(x), t = 1 / (1 + 0.3275911 * z);
    return s * (1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z));
  }
  /* El perfil es el de la primera simulación (simulacion/contener.py): una cresta entre dos cunetas. La bola deja
   * una franja angosta; la base la redondea (la cresta) y, más lejos, el aluminio que se corre baja un poco a los
   * lados (las cunetas): 2,6 · cresta − 1,1 · (ancho − cresta). Allá se medía en píxeles de 4 por mm; aquí, en
   * medios anchos del surco (u), y las cunetas bajan más cuanto más firme es la base (lomas). */
  const PERFIL_U = 3.6, PERFIL_N = 1024;
  function tablaPerfil(lomas) {
    const W = 0.83, sc = 0.55, sa = 1.53, k = lomas / 0.1;
    const franja = (u, s) => 0.5 * (erf((u + W / 2) / (s * Math.SQRT2)) - erf((u - W / 2) / (s * Math.SQRT2)));
    const c0 = 2.6 * franja(0, sc), t = new Float32Array(PERFIL_N + 2);
    for (let i = 0; i <= PERFIL_N; i++) {
      const u = (i / PERFIL_N) * PERFIL_U, c = franja(u, sc), a = franja(u, sa);
      t[i] = (2.6 * c - 1.1 * k * Math.max(0, a - c)) / c0;
    }
    const cola = t[PERFIL_N];                                  // que llegue a cero en el borde
    for (let i = 0; i <= PERFIL_N; i++) t[i] -= cola * (i / PERFIL_N) ** 4;
    t[PERFIL_N] = t[PERFIL_N + 1] = 0;
    return t;
  }
  /* El medio ancho del surco (mm): la bola, más lo que la abre la base al hundirse. Un punto se abre menos. */
  const anchoSurco = (rb, D, abre, punto = false) => rb + 0.35 * Math.sqrt(2 * rb * D) + (punto ? 0.2 : 0.25) * abre * D;
  const vacio = () => ({ x0: Infinity, y0: Infinity, x1: -1, y1: -1 });
  function ampliar(r, x0, y0, x1, y1) {
    if (x0 < r.x0) r.x0 = x0;
    if (y0 < r.y0) r.y0 = y0;
    if (x1 > r.x1) r.x1 = x1;
    if (y1 > r.y1) r.y1 = y1;
  }

  // ---------------------------------------------------------------- la placa
  class Placa {
    /* o: { N (px de lado), semilla (de la hoja), arrugas (0 recién salida del rollo · 1 arrugada y alisada),
     *      doble (dos hojas juntas: «si se rompe demasiado, doble», Acción 4) } */
    constructor(o = {}) {
      this.N = o.N || 1024;
      this.mm = LADO / this.N;
      this.hoja = { semilla: String(o.semilla ?? "1"), arrugas: o.arrugas ?? 0.5, doble: !!o.doble };
      this.trazos = [];
      this.deshechos = [];
      this.actual = null;
      const n = this.N * this.N;
      this.R = new Float32Array(n);       // lo repujado, mm
      this.S = new Float32Array(n);       // cuánto alisó la herramienta las arrugas (0 a 1)
      this.H = new Float32Array(n);       // la altura de la hoja: R + A · (1 − S)
      this.K = new Float32Array(n);       // el trazo en curso: su perfil
      this.T = new Uint8Array(n);         // el trazo en curso: dónde tocó
      this.Gd = new Float32Array(n);      // el trazo en curso: las cunetas de sus puntos, sumadas
      this.R0 = new Float32Array(n);      // lo repujado antes del trazo en curso
      this.fatiga = new Float32Array(GRILLA * GRILLA);
      this.rota = new Uint8Array(GRILLA * GRILLA);
      this._I = null;
      this.cortar();
    }

    /** Una hoja nueva: el corte de la tijera y sus arrugas. Lo repujado se rehace sobre ella. */
    cortar() {
      this.contorno = tijera(azar("tijera", this.hoja.semilla));
      const { M, B } = rasterizar(this.contorno, this.N);
      this.M0 = M;
      this.A = arrugas(this.N, this.hoja.semilla, this.hoja.arrugas, M, B);
      this.reconstruir();
    }

    _limpiar() {
      this.R.fill(0);
      this.S.fill(0);
      this.H.set(this.A);
      this.K.fill(0);
      this.T.fill(0);
      this.Gd.fill(0);
      this.M = this.M0.slice();
      this.fatiga.fill(0);
      this.rota.fill(0);
      this.roturas = [];
      this.actual = null;
    }

    /** Rehace la placa desde la hoja: cada trazo, en su orden. Así se deshace y se exporta a otro tamaño. */
    reconstruir() {
      this._limpiar();
      this.trazos.forEach((t, n) => { this.empezar(t, n); this.terminar(true); });
    }

    /** Empieza un trazo. t: { herramienta, cara, punzon, base, fuerza, temblor, radio, puntos: [[x, y, presión, ms], …] }.
     *  Un punto con un quinto valor (1) es la mano quieta, apretando: el punzón descansa y hunde un poco más. */
    empezar(t, n = this.trazos.length) {
      if (this.actual) this.terminar();
      t.puntos = t.puntos || [];
      const base = BASES[t.base] || BASES.fieltro;
      const e = {
        base, punzon: PUNZONES[t.punzon] || PUNZONES.bola, sigma: t.cara === "anverso" ? -1 : 1,
        tabla: tablaPerfil(base.lomas), ruido: ruido(`trazo|${this.hoja.semilla}|${n}`),
        i: 0, prev: null, inicio: null, recorrido: 0, siguiente: 0, cerrado: false, roturas: 0,
        x0: Infinity, y0: Infinity, x1: -1, y1: -1,
      };
      const rb = e.punzon.radio, D = Math.min(base.limite, base.hondo * 0.8 * (t.fuerza ?? 1));
      e.ancho = anchoSurco(rb, D, base.abre);                                     // el medio ancho típico del surco
      this.actual = { t, e, n, linea: t.herramienta === "repasar" || t.herramienta === "puntear" };
      if (this.actual.linea) this._antes();
      return this._consumir();
    }

    /** Un punto más del trazo en curso (mm de la placa vista por el anverso). Quieto: la mano se detuvo ahí,
     *  apretando. Devuelve el rectángulo que cambió. */
    agregar(x, y, p = 0.8, ms = 0, quieto = false) {
      if (!this.actual) return null;
      const q = [Math.round(x * 1000) / 1000, Math.round(y * 1000) / 1000, Math.round(p * 1000) / 1000, Math.round(ms)];
      if (quieto) q.push(1);
      this.actual.t.puntos.push(q);
      return this._consumir();
    }

    /** Cierra el trazo en curso. Devuelve lo que pasó: si se cerró sin desagüe, si se rompió y dónde cambió. */
    terminar(rehaciendo = false) {
      if (!this.actual) return null;
      const { t, e, n } = this.actual, N = this.N;
      const sucio = vacio();
      if (t.herramienta === "repasar" && e.prev) {
        this._sellar(e.prev, e.recorrido, sucio);                                   // lo que quedaba hasta el último punto
        this._descanso(e.prev, e.recorrido, sucio);
      }
      if (sucio.x1 >= 0) this._componer(sucio);
      if (e.x1 >= 0) {
        for (let y = Math.max(0, e.y0); y <= Math.min(N - 1, e.y1); y++) {
          this.K.fill(0, y * N + Math.max(0, e.x0), y * N + Math.min(N - 1, e.x1) + 1);
          this.T.fill(0, y * N + Math.max(0, e.x0), y * N + Math.min(N - 1, e.x1) + 1);
          this.Gd.fill(0, y * N + Math.max(0, e.x0), y * N + Math.min(N - 1, e.x1) + 1);
        }
      }
      if (!rehaciendo) {
        const limpio = {};
        for (const k of ["herramienta", "cara", "punzon", "base", "fuerza", "temblor", "radio", "puntos"]) if (t[k] !== undefined) limpio[k] = t[k];
        this.trazos.push(limpio);
        this.deshechos.length = 0;
      }
      this.actual = null;
      return { n, cerrado: e.cerrado, roturas: e.roturas, largo: e.recorrido, sucio: sucio.x1 >= 0 ? sucio : null };
    }

    deshacer() {
      if (this.actual) this.terminar();
      if (!this.trazos.length) return false;
      this.deshechos.push(this.trazos.pop());
      this.reconstruir();
      return true;
    }

    rehacer() {
      if (this.actual) this.terminar();
      if (!this.deshechos.length) return false;
      const t = this.deshechos.pop();
      this.empezar(t, this.trazos.length);
      this.terminar(true);
      this.trazos.push(t);
      return true;
    }

    /** Lo que diría la ficha: trazos, mm de surco y de punteado, minutos, roturas y contornos sin desagüe. */
    registro() {
      const r = { trazos: this.trazos.length, surco: 0, punteado: 0, puntos: 0, relleno: 0, alisado: 0, sinDesague: 0,
        roturas: this.roturas.length, reverso: 0, anverso: 0 };
      for (const t of this.trazos) {
        const P = t.puntos;
        let L = 0, cerrado = false;
        for (let i = 1; i < P.length; i++) {
          L += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]);
          if (L > 5 * DESAGUE && Math.hypot(P[i][0] - P[0][0], P[i][1] - P[0][1]) < DESAGUE - 0.5) cerrado = true;
        }
        if (t.herramienta === "repasar") r.surco += L;
        else if (t.herramienta === "puntear") { r.punteado += L; r.puntos += 1 + Math.floor(L / PUNTEADO); }
        else if (t.herramienta === "rellenar") r.relleno += L;
        else r.alisado += L;
        if (cerrado && (t.herramienta === "repasar" || t.herramienta === "puntear")) r.sinDesague++;
        r[t.cara === "anverso" ? "anverso" : "reverso"]++;
      }
      r.minutos = this.trazos.length ? MANO.preparar + MANO.retirar + r.surco / MANO.surco + r.punteado / MANO.punteado +
        (r.relleno + r.alisado) / 60 : 0;
      return r;
    }

    /** La altura máxima menos la mínima de lo repujado (mm): cuánto puede llegar a dar sombra. */
    rango() {
      let lo = 0, hi = 0;
      const R = this.R;
      for (let j = 0; j < R.length; j += 7) { const v = R[j]; if (v < lo) lo = v; else if (v > hi) hi = v; }
      return hi - lo + 0.25;
    }

    aJSON() {
      return { contenida: "ensayo de repujado (la máquina): no entra en la caja ni en la fuente", version: 1,
        placa_mm: LADO, semilla: SEMILLA, hoja: { ...this.hoja }, trazos: this.trazos, registro: this.registro() };
    }

    static deJSON(o, N) {
      const h = o.hoja || {};
      const p = new Placa({ N, semilla: h.semilla, arrugas: h.arrugas, doble: h.doble });
      p.trazos = (o.trazos || []).map((t) => ({ ...t, puntos: t.puntos.map((q) => q.slice()) }));
      p.reconstruir();
      return p;
    }

    // ------------------------------------------------------------ por dentro
    /* Lo repujado antes del trazo, y su media en 2,4 mm (por integrales): el surco se mide desde ahí, de modo
     * que una línea sobre una zona rellena se hunde desde la zona, no desde el plano. */
    _antes() {
      const N = this.N, mm = this.mm, { t, e } = this.actual, P = t.puntos;
      const radio = Math.max(2, Math.round(2.4 / mm));
      let x0 = 0, y0 = 0, x1 = N - 1, y1 = N - 1;
      if (P.length > 2) {                       // rehaciendo: se conoce todo el trazo
        let a = Infinity, b = Infinity, c = -Infinity, d = -Infinity;
        for (const q of P) { if (q[0] < a) a = q[0]; if (q[1] < b) b = q[1]; if (q[0] > c) c = q[0]; if (q[1] > d) d = q[1]; }
        const rb = e.punzon.radio, lim = e.base.limite;
        const margen = PERFIL_U * 1.3 * anchoSurco(rb, lim, e.base.abre) + 9 + radio * mm;
        x0 = Math.max(0, Math.floor((a - margen) / mm)); y0 = Math.max(0, Math.floor((b - margen) / mm));
        x1 = Math.min(N - 1, Math.ceil((c + margen) / mm)); y1 = Math.min(N - 1, Math.ceil((d + margen) / mm));
      }
      for (let y = y0; y <= y1; y++) this.R0.set(this.R.subarray(y * N + x0, y * N + x1 + 1), y * N + x0);
      const w = x1 - x0 + 1, h = y1 - y0 + 1, W1 = w + 1;
      if (!this._I || this._I.length < W1 * (h + 1)) this._I = new Float64Array(W1 * (h + 1));
      const I = this._I;
      I.fill(0, 0, W1);
      for (let y = 1; y <= h; y++) {
        let fila = 0;
        I[y * W1] = 0;
        const o = (y0 + y - 1) * N + x0;
        for (let x = 1; x <= w; x++) { fila += this.R0[o + x - 1]; I[y * W1 + x] = I[(y - 1) * W1 + x] + fila; }
      }
      this._reg = { x0, y0, w, h, W1, r: radio };
    }

    _media(x, y) {
      const g = this._reg, I = this._I;
      const xa = Math.max(0, x - g.r - g.x0), xb = Math.min(g.w, x + g.r + 1 - g.x0);
      const ya = Math.max(0, y - g.r - g.y0), yb = Math.min(g.h, y + g.r + 1 - g.y0);
      if (xb <= xa || yb <= ya) return this.R0[y * this.N + x];
      return (I[yb * g.W1 + xb] - I[ya * g.W1 + xb] - I[yb * g.W1 + xa] + I[ya * g.W1 + xa]) / ((xb - xa) * (yb - ya));
    }

    /* La profundidad (D) y el medio ancho (w) del surco en un punto: de la presión, la fuerza, el temblor de la
     * mano (un ruido a lo largo del recorrido), la base y la bola. */
    _prof(q, s) {
      const { t, e } = this.actual;
      const p = q[2] * (1 + 0.15 * (t.temblor ?? 0.5) * e.ruido(s / 6, 0.37)) * (1 + 0.03 * e.ruido(s / 0.8, 7.7));
      const [hunde, abre] = this.hoja.doble ? [0.9, 1.12] : [1, 1];                 // la hoja doble se hunde menos y se abre más
      const D = Math.min(e.base.limite, Math.max(0, e.base.hondo * p * (t.fuerza ?? 1) * hunde));
      const w = anchoSurco(e.punzon.radio, D, e.base.abre);
      return [D, w * abre * (1 + 0.08 * (t.temblor ?? 0.5) * e.ruido(s / 3.5, 21.1))];     // el ancho también tiembla
    }

    _consumir() {
      const { t, e } = this.actual, P = t.puntos;
      const sucio = vacio();
      for (; e.i < P.length; e.i++) {
        const q = P[e.i];
        if (!e.prev) {
          e.prev = q; e.inicio = q; e.sello = q; e.sSello = 0;
          if (t.herramienta === "repasar") this._descanso(q, 0, sucio);
          else if (t.herramienta === "puntear") { this._punto(q, 0, 0, 0, sucio); e.siguiente = this._paso(0); }
          else { this._mancha(q, sucio); e.siguiente = this._pasoMancha(); }
          continue;
        }
        const a = e.prev, dx = q[0] - a[0], dy = q[1] - a[1], L = Math.hypot(dx, dy);
        if (L < 1e-3) {
          if (q[4] && t.herramienta === "repasar") this._descanso(a, e.recorrido, sucio);     // duda: descansa ahí
          continue;
        }
        const s0 = e.recorrido, tx = dx / L, ty = dy / L;
        if (t.herramienta === "repasar") {
          // se estampa cada TRAMO a lo largo del recorrido, lleguen los puntos tan juntos como lleguen
          while (e.sSello + TRAMO <= s0 + L) {
            const sb = e.sSello + TRAMO, f = (sb - s0) / L;
            this._sellar([a[0] + dx * f, a[1] + dy * f, a[2] + (q[2] - a[2]) * f], sb, sucio);
          }
        } else if (t.herramienta === "puntear") {
          while (e.siguiente <= s0 + L) {
            const f = (e.siguiente - s0) / L;
            this._punto([a[0] + dx * f, a[1] + dy * f, a[2] + (q[2] - a[2]) * f], tx, ty, e.siguiente, sucio);
            e.siguiente += this._paso(e.siguiente);
          }
        } else {
          const paso = this._pasoMancha();
          while (e.siguiente <= s0 + L) {
            const f = (e.siguiente - s0) / L;
            this._mancha([a[0] + dx * f, a[1] + dy * f, a[2] + (q[2] - a[2]) * f], sucio);
            e.siguiente += paso;
          }
        }
        e.recorrido = s0 + L;
        if (this.actual.linea && e.recorrido > 5 * DESAGUE && Math.hypot(q[0] - e.inicio[0], q[1] - e.inicio[1]) < DESAGUE - 0.5) e.cerrado = true;
        e.prev = q;
      }
      if (sucio.x1 >= 0) this._componer(sucio);
      return sucio.x1 >= 0 ? sucio : null;
    }

    /* Un tramo del surco, desde el último sello hasta pb (que está sb mm adentro del recorrido). */
    _sellar(pb, sb, sucio) {
      const { e } = this.actual, pa = e.sello, sa = e.sSello, L = Math.hypot(pb[0] - pa[0], pb[1] - pa[1]);
      if (L < 1e-3) return;
      const da = this._prof(pa, sa), db = this._prof(pb, sb);
      this._capsula(pa, pb, da, db, sucio, sa, sb);
      this._esfuerzo(pb, (db[0] / db[1]) ** 2 * L, (pb[0] - pa[0]) / L, (pb[1] - pa[1]) / L, sucio);
      e.sello = pb; e.sSello = sb;
    }

    /* Donde la mano arranca y donde se detiene, el punzón descansa y hunde un poco más (contener.py). */
    _descanso(q, s, sucio) {
      const [D] = this._prof(q, s), { e } = this.actual, rb = e.punzon.radio;
      const Dd = Math.min(e.base.limite, 1.12 * D);
      const w = anchoSurco(rb, Dd, e.base.abre);
      this._capsula(q, q, [Dd, w], [Dd, w], sucio);
    }

    /* Un punto del punteado: la punta se hunde más y el aluminio sufre más (contener.py: «el punteado perfora»). */
    /* Una mano que puntea no lo hace a paso de máquina: cada punto cae un poco antes o un poco después. */
    _paso(s) {
      const r = azar("paso", this.hoja.semilla, this.actual.n, Math.round(s * 100));
      return PUNTEADO * Math.exp(0.07 * gauss(r));
    }
    _punto(q, tx, ty, s, sucio) {
      const { e, n } = this.actual, r = azar("punto", this.hoja.semilla, n, Math.round(s * 100));
      const c = [q[0] + gauss(r) * 0.06, q[1] + gauss(r) * 0.06, q[2]];             // la punta no cae justo en la línea
      const [D0] = this._prof(c, s), rb = e.punzon.radio;
      const D = Math.min(e.base.limite, 1.2 * D0 * Math.exp(0.05 * gauss(r)));      // y cada punto aprieta distinto
      const w = anchoSurco(rb, D, e.base.abre, true);
      this._capsula(c, c, [D, w], [D, w], sucio, undefined, undefined, true);
      this._esfuerzo(c, 1.6 * (D / w) ** 2, tx, ty, sucio);
    }

    /* Un tramo del surco: una cápsula entre a y b, con la profundidad y el ancho de cada punta. Los tramos de un
     * mismo trazo se funden por el máximo, de modo que pasar dos veces por el mismo lugar no suma dos veces.
     * Con sa y sb (el recorrido en cada punta, mm), el aluminio que el surco tira hacia sí se frunce a los lados:
     * arrugas cortas, de través, que van y vienen a lo largo del trazo. Los puntos del punteado son golpes
     * aparte: sus crestas se funden por el máximo, pero sus cunetas se suman (como al desenfocar en contener.py),
     * para que no quede un pliegue entre dos puntos vecinos. */
    _capsula(a, b, [Da, wa], [Db, wb], sucio, sa, sb, punto = false) {
      const N = this.N, mm = this.mm, { e } = this.actual, tabla = e.tabla;
      const ext = PERFIL_U * Math.max(wa, wb);
      const x0 = Math.max(0, Math.floor((Math.min(a[0], b[0]) - ext) / mm)), x1 = Math.min(N - 1, Math.ceil((Math.max(a[0], b[0]) + ext) / mm));
      const y0 = Math.max(0, Math.floor((Math.min(a[1], b[1]) - ext) / mm)), y1 = Math.min(N - 1, Math.ceil((Math.max(a[1], b[1]) + ext) / mm));
      if (x1 < x0 || y1 < y0) return;
      const dx = b[0] - a[0], dy = b[1] - a[1], L2 = dx * dx + dy * dy;
      const K = this.K, T = this.T, S = this.S, Gd = this.Gd, escala = PERFIL_N / PERFIL_U, iu2 = 1 / (PERFIL_U * PERFIL_U);
      const frunce = sa !== undefined;
      let fa = 0, fb = 0, ma = 0, mb = 0;
      if (frunce) {
        const k = 2 * Math.PI / (2.6 * e.ancho);
        fa = sa * k + 1.7 * e.ruido(sa / 4, 11.3); fb = sb * k + 1.7 * e.ruido(sb / 4, 11.3);
        ma = 0.13 * (0.55 + 0.45 * e.ruido(sa / 5, 50.5)); mb = 0.13 * (0.55 + 0.45 * e.ruido(sb / 5, 50.5));
      }
      for (let y = y0; y <= y1; y++) {
        const py = (y + 0.5) * mm - a[1];
        for (let x = x0; x <= x1; x++) {
          const px = (x + 0.5) * mm - a[0];
          let f = L2 > 0 ? (px * dx + py * dy) / L2 : 0;
          f = f < 0 ? 0 : f > 1 ? 1 : f;
          const ex = px - f * dx, ey = py - f * dy;
          const u = Math.sqrt(ex * ex + ey * ey) / (wa + f * (wb - wa));
          if (u >= PERFIL_U) continue;
          let v = tabla[(u * escala) | 0];
          if (frunce && u > 0.7) {
            const z = (u - 2.1) / 0.7, fase = fa + f * (fb - fa);
            v += (ma + f * (mb - ma)) * Math.exp(-z * z) * (Math.sin(fase) + 0.5 * Math.sin(2.3 * fase + 1));
          }
          v *= Da + f * (Db - Da);
          const j = y * N + x;
          if (punto && v <= 0) Gd[j] += v;
          else if (!T[j] || v > K[j]) { K[j] = v; T[j] = 1; }
          const q = 1 - u * u * iu2, al = 0.75 * q * q;                 // cerca del punzón, las arrugas se alisan
          if (al > S[j]) S[j] = al;
        }
      }
      ampliar(sucio, x0, y0, x1, y1);
      ampliar(e, x0, y0, x1, y1);
    }

    _pasoMancha() {
      const t = this.actual.t;
      return Math.max(0.2, (t.radio || 3) * (t.herramienta === "alisar" ? 0.3 : 0.25));
    }

    /* Rellenar: el lado redondo empuja de a poco y la altura se acumula hasta el límite de la base. Alisar: la
     * yema baja las arrugas y suaviza lo chico; el surco queda. */
    _mancha(q, sucio) {
      const { t, e } = this.actual, N = this.N, mm = this.mm, rr = t.radio || 3;
      const ext = 1.8 * rr;
      const x0 = Math.max(0, Math.floor((q[0] - ext) / mm)), x1 = Math.min(N - 1, Math.ceil((q[0] + ext) / mm));
      const y0 = Math.max(0, Math.floor((q[1] - ext) / mm)), y1 = Math.min(N - 1, Math.ceil((q[1] + ext) / mm));
      if (x1 < x0 || y1 < y0) return;
      const R = this.R, S = this.S, ir2 = 1 / (rr * rr);
      if (t.herramienta === "rellenar") {
        const k = e.sigma * 0.05 * q[2] * (t.fuerza ?? 1), lim = e.base.limite;
        for (let y = y0; y <= y1; y++) {
          const py = (y + 0.5) * mm - q[1];
          for (let x = x0; x <= x1; x++) {
            const px = (x + 0.5) * mm - q[0], u2 = (px * px + py * py) * ir2;
            if (u2 > 3.24) continue;
            const g = Math.exp(-2.2 * u2), j = y * N + x;
            const ya = e.sigma * R[j], sat = ya > 0 ? Math.max(0, 1 - ya / lim) : 1;
            R[j] += k * g * sat;
            if (0.6 * g > S[j]) S[j] = 0.6 * g;
          }
        }
      } else {
        const w = x1 - x0 + 3, h = y1 - y0 + 3, copia = new Float32Array(w * h);
        for (let y = 0; y < h; y++) {
          const yy = Math.min(N - 1, Math.max(0, y0 - 1 + y));
          for (let x = 0; x < w; x++) copia[y * w + x] = R[yy * N + Math.min(N - 1, Math.max(0, x0 - 1 + x))];
        }
        for (let y = y0; y <= y1; y++) {
          const py = (y + 0.5) * mm - q[1];
          for (let x = x0; x <= x1; x++) {
            const px = (x + 0.5) * mm - q[0], u2 = (px * px + py * py) * ir2;
            if (u2 > 2.25) continue;
            const g = Math.exp(-2 * u2), j = y * N + x, c = (y - y0 + 1) * w + (x - x0 + 1);
            const media = (copia[c - w - 1] + copia[c - w] + copia[c - w + 1] + copia[c - 1] + copia[c] + copia[c + 1] +
              copia[c + w - 1] + copia[c + w] + copia[c + w + 1]) / 9;
            R[j] += 0.25 * g * (media - copia[c]);
            S[j] += (1 - S[j]) * 0.3 * g;
          }
        }
      }
      ampliar(sucio, x0, y0, x1, y1);
      ampliar(e, x0, y0, x1, y1);
    }

    /* El esfuerzo se acumula en una grilla de 0,5 mm. Cada celda aguanta hasta su umbral; si lo pasa, la hoja
     * se rompe ahí: una grieta corta, más o menos a lo largo del surco. */
    _esfuerzo(q, energia, tx, ty, sucio) {
      const cx = Math.floor(q[0] / CELDA), cy = Math.floor(q[1] / CELDA);
      if (cx < 0 || cy < 0 || cx >= GRILLA || cy >= GRILLA) return;
      const c = cy * GRILLA + cx;
      if (this.rota[c]) return;
      const N = this.N, j = Math.min(N - 1, Math.floor(q[1] / this.mm)) * N + Math.min(N - 1, Math.floor(q[0] / this.mm));
      if (this.M[j] < 0.5) return;
      this.fatiga[c] += energia;
      if (this.fatiga[c] > umbral(this.hoja.semilla, c) * (this.hoja.doble ? 2.5 : 1)) { this.rota[c] = 1; this._romper(q, tx, ty, c, sucio); }
    }

    _romper(q, tx, ty, c, sucio) {
      for (const o of this.roturas) if (Math.hypot(o.x - q[0], o.y - q[1]) < 3) return;
      const { e, n } = this.actual, r = azar("rotura", this.hoja.semilla, n, c);
      const ang = (tx || ty ? Math.atan2(ty, tx) : r() * Math.PI) + gauss(r) * 0.45;
      const L = 2 + 5 * r(), co = Math.cos(ang), si = Math.sin(ang), pts = [];
      for (let k = 0; k <= 4; k++) {
        const s = (k / 4 - 0.5) * L, z = k === 0 || k === 4 ? 0 : gauss(r) * 0.22;
        pts.push([q[0] + co * s - si * z, q[1] + si * s + co * z]);
      }
      const N = this.N, mm = this.mm, ext = 1.5;
      const x0 = Math.max(0, Math.floor((Math.min(...pts.map((p) => p[0])) - ext) / mm)), x1 = Math.min(N - 1, Math.ceil((Math.max(...pts.map((p) => p[0])) + ext) / mm));
      const y0 = Math.max(0, Math.floor((Math.min(...pts.map((p) => p[1])) - ext) / mm)), y1 = Math.min(N - 1, Math.ceil((Math.max(...pts.map((p) => p[1])) + ext) / mm));
      for (let y = y0; y <= y1; y++) {
        const py = (y + 0.5) * mm;
        for (let x = x0; x <= x1; x++) {
          const px = (x + 0.5) * mm;
          let d = Infinity;
          for (let k = 0; k < 4; k++) {
            const [ax, ay] = pts[k], [bx, by] = pts[k + 1], dx = bx - ax, dy = by - ay;
            let f = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy || 1);
            f = f < 0 ? 0 : f > 1 ? 1 : f;
            d = Math.min(d, Math.hypot(px - ax - f * dx, py - ay - f * dy));
          }
          if (d > ext) continue;
          const j = y * N + x, abre = Math.min(1, Math.max(0, (d - 0.05) / 0.14));
          if (abre < this.M[j]) this.M[j] = abre;
          const labio = e.sigma * 0.22 * Math.exp(-((d / 0.45) ** 2));    // los bordes se doblan hacia donde empujaba la punta
          this.R0[j] += labio;
          this.R[j] += labio;
        }
      }
      ampliar(sucio, x0, y0, x1, y1);
      ampliar(e, x0, y0, x1, y1);
      this.roturas.push({ x: Math.round(q[0] * 10) / 10, y: Math.round(q[1] * 10) / 10, largo: Math.round(L * 10) / 10, trazo: n });
      e.roturas++;
    }

    /* Lo repujado en un rectángulo: para el trazo en curso, el surco se funde con lo que había (el máximo hacia
     * donde empuja la herramienta) y las lomas se suman; después, la altura con las arrugas que quedan. */
    _componer(r) {
      const { t, e } = this.actual, N = this.N, R = this.R, R0 = this.R0, K = this.K, T = this.T, S = this.S, A = this.A, H = this.H;
      const Gd = this.Gd;
      const linea = this.actual.linea, sg = e.sigma, lim = e.base.limite;
      for (let y = r.y0; y <= r.y1; y++) {
        for (let x = r.x0; x <= r.x1; x++) {
          const j = y * N + x;
          if (linea && (T[j] || Gd[j] !== 0)) {
            const k = (T[j] ? K[j] : 0) + Gd[j], r0 = R0[j];
            if (k > 0) {
              const g = k < 0.12 ? k / 0.12 : 1;
              const objetivo = r0 + g * (this._media(x, y) + sg * Math.min(k, lim) - r0);
              R[j] = sg > 0 ? Math.max(r0, objetivo) : Math.min(r0, objetivo);
            } else R[j] = r0 + sg * k;
          }
          H[j] = R[j] + A[j] * (1 - S[j]);
        }
      }
      void t;
    }
  }

  // ---------------------------------------------------------------- la luz
  const FONDOS = { tinta: [29, 28, 26], papel: [246, 244, 238], fieltro: [58, 56, 53] };

  /* Lo que se ve de una cara, con una lámpara (azimut y elevación, en grados: 180 es desde la izquierda) y, si
   * se pide, el taller: una ventana grande arriba que la hoja refleja. Por el reverso la hoja se ve dada vuelta
   * (en espejo) y la altura cambia de signo. El metal es el del aluminio: casi todo reflejo, de Fresnel 0,91;
   * una cara es brillante y la otra mate, como el papel de cocina. Las sombras de la luz rasante se calculan
   * por barrido, desde el lado de la lámpara. */
  class Vista {
    constructor(placa) {
      this.o = { cara: "reverso", azimut: 160, elevacion: 15, taller: true, sombras: true, fondo: "tinta", brillante: "anverso" };
      this.usar(placa);
    }

    usar(placa) {
      this.placa = placa;
      if (this.N !== placa.N) {
        const N = this.N = placa.N, n = N * N;
        this.V = new Float32Array(n);
        this.C = new Float32Array(n);
        this.B1 = new Float32Array(n);
        this.Hb = new Float32Array(n);
        this.U = new Float32Array(n);
        this.rgba = new Uint8ClampedArray(n * 4);
        this.fieltro = null;
      }
      return this;
    }

    opciones(o) { Object.assign(this.o, o); return this; }

    /** Pinta lo que cambió (un rectángulo de la placa) o todo. Devuelve el rectángulo de la vista pintado. */
    pintar(sucio) {
      const N = this.N, mm = this.placa.mm, o = this.o, rev = o.cara === "reverso";
      const az = o.azimut * Math.PI / 180, el = Math.max(3, Math.min(88, o.elevacion)) * Math.PI / 180;
      const L = [Math.cos(el) * Math.cos(az), -Math.cos(el) * Math.sin(az), Math.sin(el)];
      const lleno = { x0: 0, y0: 0, x1: N - 1, y1: N - 1 };
      let r = lleno;
      if (sucio) r = rev ? { x0: N - 1 - sucio.x1, x1: N - 1 - sucio.x0, y0: sucio.y0, y1: sucio.y1 } : { ...sucio };
      const cortar = (q) => ({ x0: Math.max(0, q.x0), y0: Math.max(0, q.y0), x1: Math.min(N - 1, q.x1), y1: Math.min(N - 1, q.y1) });
      const rao = Math.max(1, Math.round(0.9 / mm));
      this.rao = rao;
      this._vista(cortar(r), rev);
      const E = cortar({ x0: r.x0 - 2 * rao - 1, y0: r.y0 - 2 * rao - 1, x1: r.x1 + 2 * rao + 1, y1: r.y1 + 2 * rao + 1 });
      this._oclusion(E);
      let Z = E;
      if (o.sombras) {
        const largo = Math.ceil((this.placa.rango() + 0.2) / Math.tan(el) / mm) + 2;
        const lx = L[0], ly = L[1], ll = Math.hypot(lx, ly) || 1;
        const ux = -lx / ll, uy = -ly / ll;                  // hacia donde caen las sombras
        const Es = cortar({
          x0: r.x0 - 1 + Math.min(0, Math.floor(ux * largo)), x1: r.x1 + 1 + Math.max(0, Math.ceil(ux * largo)),
          y0: r.y0 - 1 + Math.min(0, Math.floor(uy * largo)), y1: r.y1 + 1 + Math.max(0, Math.ceil(uy * largo)),
        });
        Z = cortar({ x0: Math.min(E.x0, Es.x0), y0: Math.min(E.y0, Es.y0), x1: Math.max(E.x1, Es.x1), y1: Math.max(E.y1, Es.y1) });
        this._horizonte(sucio ? Z : lleno, L, Math.tan(el), mm);
      }
      this._sombrear(Z, L);
      return Z;
    }

    /* La altura vista desde la cara elegida, y cuánto de cada píxel es aluminio. */
    _vista(r, rev) {
      const N = this.N, H = this.placa.H, M = this.placa.M, V = this.V, C = this.C;
      for (let y = r.y0; y <= r.y1; y++) {
        const o = y * N;
        if (rev) for (let x = r.x0; x <= r.x1; x++) { V[o + x] = -H[o + N - 1 - x]; C[o + x] = M[o + N - 1 - x]; }
        else for (let x = r.x0; x <= r.x1; x++) { V[o + x] = H[o + x]; C[o + x] = M[o + x]; }
      }
    }

    /* La media de la altura alrededor (una caja de 0,9 mm): donde la hoja está más abajo que su entorno, el
     * taller llega menos. Así se oscurecen los surcos y los pliegues. */
    _oclusion(E) {
      const N = this.N, V = this.V, B1 = this.B1, Hb = this.Hb, r = this.rao, n = 2 * r + 1;
      const cx = (k) => (k < 0 ? 0 : k > N - 1 ? N - 1 : k);
      const ya = Math.max(0, E.y0 - r), yb = Math.min(N - 1, E.y1 + r);
      for (let y = ya; y <= yb; y++) {
        const o = y * N;
        let s = 0;
        for (let k = E.x0 - r; k <= E.x0 + r; k++) s += V[o + cx(k)];
        for (let x = E.x0; x <= E.x1; x++) {
          B1[o + x] = s / n;
          s += V[o + cx(x + r + 1)] - V[o + cx(x - r)];
        }
      }
      const W = E.x1 - E.x0 + 1;
      if (!this._col || this._col.length < W) this._col = new Float64Array(N);
      const col = this._col;
      col.fill(0, 0, W);
      for (let k = E.y0 - r; k <= E.y0 + r; k++) { const o = cx(k) * N + E.x0; for (let i = 0; i < W; i++) col[i] += B1[o + i]; }
      for (let y = E.y0; y <= E.y1; y++) {
        const o = y * N + E.x0, mas = cx(y + r + 1) * N + E.x0, menos = cx(y - r) * N + E.x0;
        for (let i = 0; i < W; i++) {
          Hb[o + i] = col[i] / n;
          col[i] += B1[mas + i] - B1[menos + i];
        }
      }
    }

    /* U: la altura del horizonte que ve cada píxel mirando hacia la lámpara. Se barre desde el lado de la luz;
     * cada píxel toma el de su vecino hacia la lámpara, bajado lo que sube el rayo en un paso. */
    _horizonte(Z, L, tanEl, mm) {
      const N = this.N, V = this.V, U = this.U, lx = L[0], ly = L[1];
      if (Math.abs(lx) >= Math.abs(ly)) {
        const sx = lx > 0 ? 1 : -1, pend = ly / Math.abs(lx), sube = Math.hypot(1, pend) * mm * tanEl;
        for (let k = 0; k <= Z.x1 - Z.x0; k++) {
          const x = sx > 0 ? Z.x1 - k : Z.x0 + k, xu = x + sx;
          for (let y = Z.y0; y <= Z.y1; y++) {
            let h = -1e9;
            const yy = y + pend;
            if (xu >= 0 && xu < N && yy >= 0 && yy <= N - 1) {
              const y0 = Math.floor(yy), f = yy - y0, y1 = y0 < N - 1 ? y0 + 1 : y0;
              const a = Math.max(U[y0 * N + xu], V[y0 * N + xu]), b = Math.max(U[y1 * N + xu], V[y1 * N + xu]);
              h = a + f * (b - a) - sube;
            }
            U[y * N + x] = h;
          }
        }
      } else {
        const sy = ly > 0 ? 1 : -1, pend = lx / Math.abs(ly), sube = Math.hypot(1, pend) * mm * tanEl;
        for (let k = 0; k <= Z.y1 - Z.y0; k++) {
          const y = sy > 0 ? Z.y1 - k : Z.y0 + k, yu = y + sy;
          for (let x = Z.x0; x <= Z.x1; x++) {
            let h = -1e9;
            const xx = x + pend;
            if (yu >= 0 && yu < N && xx >= 0 && xx <= N - 1) {
              const x0 = Math.floor(xx), f = xx - x0, x1 = x0 < N - 1 ? x0 + 1 : x0, o = yu * N;
              const a = Math.max(U[o + x0], V[o + x0]), b = Math.max(U[o + x1], V[o + x1]);
              h = a + f * (b - a) - sube;
            }
            U[y * N + x] = h;
          }
        }
      }
    }

    /* El taller: un techo apagado, una ventana grande del lado de la lámpara (35° de la vertical) y una tira más
     * débil del otro lado. La hoja los refleja según hacia dónde mira cada faceta: así el aluminio se lee como
     * metal y no como papel. En el registro (la foto de la Acción 4) no hay taller: solo la lámpara, rasante. */
    _sombrear(Z, L) {
      const o = this.o, N = this.N, mm = this.placa.mm, V = this.V, C = this.C, Hb = this.Hb, U = this.U, rgba = this.rgba;
      const brillante = o.brillante === o.cara, taller = !!o.taller, sombras = !!o.sombras;
      const rug = brillante ? 0.2 : 0.42, a = rug * rug;
      const rugL = Math.max(rug, 0.32), aL = rugL * rugL, aL2 = aL * aL, kG = (rugL + 1) * (rugL + 1) / 8;   // la lámpara no es un punto
      const [Lx, Ly, Lz] = L;
      let hx = Lx, hy = Ly, hz = Lz + 1;
      const hl = Math.hypot(hx, hy, hz);
      hx /= hl; hy /= hl; hz /= hl;
      const F0 = 0.913, q5 = 1 - hz, F = F0 + (1 - F0) * q5 * q5 * q5 * q5 * q5;
      const lampara = taller ? 1.15 : 2.6, kd = brillante ? 0.02 : 0.07;
      const lh = Math.hypot(Lx, Ly) || 1, ux = Lx / lh, uy = Ly / lh;
      const s1 = Math.sin(35 * Math.PI / 180), c1 = Math.cos(35 * Math.PI / 180);
      const v1x = s1 * ux, v1y = s1 * uy, v1z = c1;                                       // la ventana
      const g2 = -110 * Math.PI / 180, s2 = Math.sin(50 * Math.PI / 180), c2 = Math.cos(50 * Math.PI / 180);
      const v2x = s2 * (ux * Math.cos(g2) - uy * Math.sin(g2)), v2y = s2 * (ux * Math.sin(g2) + uy * Math.cos(g2)), v2z = c2;
      const b1 = 1 / (0.03 + 1.2 * a), b2 = 1 / (0.02 + 1.2 * a), inv2 = 1 / (2 * mm);
      const ventana = brillante ? 1.2 : 0.8;                    // la cara mate abre el reflejo: menos intenso
      const tono = Vista.tono || (Vista.tono = (() => {        // de la luz al valor del píxel: exposición y gamma
        const t = new Uint8ClampedArray(4096);
        for (let i = 0; i < 4096; i++) t[i] = Math.round(255 * Math.pow(1 - Math.exp(-1.3 * (i / 512)), 1 / 2.2));
        return t;
      })());
      const transparente = o.fondo === "transparente", fieltro = o.fondo === "fieltro";
      const fondo = FONDOS[o.fondo] || FONDOS.tinta;
      if (fieltro && !this.fieltro) this._fieltro();
      const luzFieltro = 255 * (0.3 + 0.7 * Lz) * (taller ? 1 : 0.6);
      for (let y = Z.y0; y <= Z.y1; y++) {
        const ar = (y > 0 ? y - 1 : 0) * N, ab = (y < N - 1 ? y + 1 : N - 1) * N;
        for (let x = Z.x0; x <= Z.x1; x++) {
          const j = y * N + x, cob = C[j], k = j * 4;
          let fr = fondo[0], fg = fondo[1], fb = fondo[2];
          if (fieltro) { const v = this.fieltro[j] * luzFieltro; fr = v * 1.02; fg = v; fb = v * 0.96; }
          if (cob <= 0) {
            rgba[k] = fr; rgba[k + 1] = fg; rgba[k + 2] = fb; rgba[k + 3] = transparente ? 0 : 255;
            continue;
          }
          const dx = (V[x < N - 1 ? j + 1 : j] - V[x > 0 ? j - 1 : j]) * inv2, dy = (V[ab + x] - V[ar + x]) * inv2;
          const il = 1 / Math.sqrt(dx * dx + dy * dy + 1), nx = -dx * il, ny = -dy * il, nz = il;
          const m = cob >= 1 ? 1 : cob;
          if (!taller) {
            // la foto del registro, como la primera simulación (simulacion/comun.py, sombrear): difusa más especular, en gris
            const nl = nx * Lx + ny * Ly + nz * Lz, nh = nx * hx + ny * hy + nz * hz;
            let esp = nh > 0 ? nh : 0;
            const e2 = esp * esp, e4 = e2 * e2, e8 = e4 * e4;
            esp = brillante ? e8 * e8 * e2 : e8;                 // ^18 la cara brillante, ^8 la mate
            let luz = 0.95 * (nl > 0 ? nl : 0) + (brillante ? 0.54 : 0.3) * esp;
            if (sombras) {
              const s = (V[j] - U[j]) * 30 + 0.5;
              luz *= s <= 0 ? 0 : s >= 1 ? 1 : s * s * (3 - 2 * s);
            }
            const cav = Hb[j] - V[j], ao = cav > 0 ? (cav < 0.315 ? 1 - 2.6 * cav : 0.18) : 1;
            const g = 0.16 * ao + luz, v = g >= 1 ? 255 : g * 255;
            rgba[k] = fr + (v * 0.985 - fr) * m;
            rgba[k + 1] = fg + (v * 0.99 - fg) * m;
            rgba[k + 2] = fb + (v - fb) * m;
            rgba[k + 3] = transparente ? 255 * m : 255;
            continue;
          }
          let c = 0;
          const nl = nx * Lx + ny * Ly + nz * Lz;
          if (nl > 0) {
            const nh = nx * hx + ny * hy + nz * hz, dd = nh * nh * (aL2 - 1) + 1;
            const G = (nl / (nl * (1 - kG) + kG)) * (nz / (nz * (1 - kG) + kG));
            let luz = lampara * (aL2 / (Math.PI * dd * dd) * G * F / (4 * nz) + kd * nl);
            if (sombras) {
              const s = (V[j] - U[j]) * 30 + 0.5;
              luz *= s <= 0 ? 0 : s >= 1 ? 1 : s * s * (3 - 2 * s);
            }
            c += luz;
          }
          const cav = Hb[j] - V[j], ao = cav > 0 ? (cav < 0.315 ? 1 - 2.6 * cav : 0.18) : 1;
          const rz = 2 * nz * nz - 1, rx = 2 * nz * nx, ry = 2 * nz * ny, arriba = rz > 0 ? rz : 0;
          let env;
          if (taller) {
            env = 0.05 + 0.08 * arriba + ventana * Math.exp((rx * v1x + ry * v1y + rz * v1z - 1) * b1) +
              0.4 * ventana * Math.exp((rx * v2x + ry * v2y + rz * v2z - 1) * b2);
          } else env = 0.035 + 0.05 * arriba;
          const q = 1 - nz;
          c += env * ao * (F0 + (1 - F0) * q * q * q * q * q);
          const i = c * 512, v = tono[i < 4095 ? i | 0 : 4095];
          rgba[k] = fr + (v * 0.975 - fr) * m;
          rgba[k + 1] = fg + (v * 0.985 - fg) * m;
          rgba[k + 2] = fb + (v - fb) * m;
          rgba[k + 3] = transparente ? 255 * m : 255;
        }
      }
    }

    /* La base que asoma alrededor de la hoja y por las roturas: fieltro gris, con su pelusa. */
    _fieltro() {
      const N = this.N, mm = this.placa.mm, f = new Float32Array(N * N), n1 = ruido("fieltro"), n2 = ruido("fieltro/pelo");
      for (let y = 0; y < N; y++) {
        for (let x = 0; x < N; x++) {
          const X = (x + 0.5) * mm, Y = (y + 0.5) * mm;
          f[y * N + x] = 0.2 + 0.025 * n1(X / 3, Y / 3) + 0.03 * n2(X / 0.35, Y / 0.35) * n2(Y / 0.5 + 9, X / 0.5);
        }
      }
      this.fieltro = f;
    }
  }

  // ---------------------------------------------------------------- PNG con su procedencia
  /* Agrega fragmentos tEXt a un PNG (después de IHDR): la imagen dice qué es y de dónde sale. */
  const TABLA_CRC = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32(bytes) {
    let c = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++) c = TABLA_CRC[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }
  function pngConTexto(png, campos) {
    const latin1 = (s) => Uint8Array.from(String(s), (ch) => { const c = ch.charCodeAt(0); return c < 256 ? c : 63; });
    const trozos = [];
    for (const [clave, valor] of Object.entries(campos)) {
      const k = latin1(clave), v = latin1(valor), datos = new Uint8Array(k.length + 1 + v.length);
      datos.set(k, 0); datos.set(v, k.length + 1);
      const tipo = latin1("tEXt"), cuerpo = new Uint8Array(4 + datos.length);
      cuerpo.set(tipo, 0); cuerpo.set(datos, 4);
      const t = new Uint8Array(12 + datos.length), dv = new DataView(t.buffer);
      dv.setUint32(0, datos.length);
      t.set(cuerpo, 4);
      dv.setUint32(8 + datos.length, crc32(cuerpo));
      trozos.push(t);
    }
    const fin = 8 + 8 + 13 + 4;                 // firma + IHDR
    const total = png.length + trozos.reduce((s, t) => s + t.length, 0), out = new Uint8Array(total);
    out.set(png.subarray(0, fin), 0);
    let p = fin;
    for (const t of trozos) { out.set(t, p); p += t.length; }
    out.set(png.subarray(fin), p);
    return out;
  }

  return {
    LADO, SEMILLA, PUNTEADO, DESAGUE, MANO, BASES, PUNZONES, Placa, Vista,
    azar, ruido, tijera, rasterizar, arrugas, umbral, pngConTexto, crc32,
  };
});
