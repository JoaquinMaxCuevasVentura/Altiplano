/* Los seis simuladores del taller de Contenida, en el navegador: calco, placa, cinta,
 * frotado, agua y voz. Son los modelos de desenterrar.py, contener.py, gramatica.py
 * (encintar) y devolver.py, con otro azar: la misma receta, otra mano.
 *
 * Todo a 4 px por milímetro: un azulejo de 150 mm es un lienzo de 600 × 600 px.
 * Las imágenes son Float32Array de w × h, con valores de 0 a 1 (o alturas).
 */
(function (raiz) {
  "use strict";
  const T = 600;
  const SEMILLA = 20260822;             // el día de la obra
  const JUNTA_MM = 3, AZULEJO_MM = 150;
  const TRAPECIO = 0.70;
  const PAPEL = [0.955, 0.948, 0.925];
  const CINTA = [0.935, 0.912, 0.852];  // masking blanca, tirando a hueso claro
  const PLASTICO = [0.07, 0.07, 0.075]; // el plástico negro de la plataforma
  const VERDE = [0.30, 1.0, 0.58];      // la luz, por el celofán

  // ------------------------------------------------------------------ azar
  function cyrb128(str) {
    let h1 = 1779033703, h2 = 3144134277, h3 = 1013904242, h4 = 2773480762;
    for (let i = 0, k; i < str.length; i++) {
      k = str.charCodeAt(i);
      h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
      h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
      h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
      h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
    }
    h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
    h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
    h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
    h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
    return [(h1 ^ h2 ^ h3 ^ h4) >>> 0, (h2 ^ h1) >>> 0, (h3 ^ h1) >>> 0, (h4 ^ h1) >>> 0];
  }

  function azar(...claves) {
    let [a, b, c, d] = cyrb128([SEMILLA, ...claves].join("|"));
    const f = () => {
      a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0;
      let t = (a + b) | 0;
      a = b ^ (b >>> 9);
      b = (c + (c << 3)) | 0;
      c = (c << 21) | (c >>> 11);
      d = (d + 1) | 0;
      t = (t + d) | 0;
      c = (c + t) | 0;
      return (t >>> 0) / 4294967296;
    };
    for (let i = 0; i < 15; i++) f();
    let resto = null;
    const r = {
      random: f,
      uniform: (x, y) => x + (y - x) * f(),
      integers: (x, y) => x + Math.floor(f() * (y - x)),          // [x, y)
      choice: (arr) => arr[Math.floor(f() * arr.length)],
      normal(mu = 0, sd = 1) {
        if (resto !== null) { const z = resto; resto = null; return mu + sd * z; }
        let u1 = f();
        while (u1 < 1e-12) u1 = f();
        const u2 = f(), m = Math.sqrt(-2 * Math.log(u1));
        resto = m * Math.sin(2 * Math.PI * u2);
        return mu + sd * m * Math.cos(2 * Math.PI * u2);
      },
      gauss(n) { const o = new Float32Array(n); for (let i = 0; i < n; i++) o[i] = r.normal(); return o; },
    };
    return r;
  }

  // ------------------------------------------------------------------ imágenes
  const nueva = (n, v = 0) => { const a = new Float32Array(n); if (v) a.fill(v); return a; };

  function normalizar(a) {
    let m = 0, s = 0;
    for (let i = 0; i < a.length; i++) m += a[i];
    m /= a.length;
    for (let i = 0; i < a.length; i++) s += (a[i] - m) ** 2;
    s = Math.sqrt(s / a.length) + 1e-9;
    for (let i = 0; i < a.length; i++) a[i] = (a[i] - m) / s;
    return a;
  }

  function nucleo(sigma) {
    const r = Math.max(1, Math.ceil(3 * sigma)), k = new Float32Array(2 * r + 1);
    let s = 0;
    for (let i = -r; i <= r; i++) { k[i + r] = Math.exp(-0.5 * (i / sigma) ** 2); s += k[i + r]; }
    for (let i = 0; i < k.length; i++) k[i] /= s;
    return k;
  }

  const reflejar = (i, n) => { if (n === 1) return 0; while (i < 0 || i >= n) i = i < 0 ? -i : 2 * n - 2 - i; return i; };

  // una pasada en una dirección: núcleo gaussiano exacto (sigma chico) o tres cajas (sigma grande)
  function pasada(src, w, h, sigma, horiz) {
    if (sigma < 0.2) return src;
    const n = horiz ? w : h, m = horiz ? h : w;
    const at = horiz ? (l, i) => l * w + i : (l, i) => i * w + l;
    let out = new Float32Array(w * h);
    const linea = new Float32Array(n);
    if (sigma <= 2.5) {
      const k = nucleo(sigma), r = (k.length - 1) / 2;
      for (let l = 0; l < m; l++) {
        for (let i = 0; i < n; i++) linea[i] = src[at(l, i)];
        for (let i = 0; i < n; i++) {
          let v = 0;
          if (i >= r && i < n - r) for (let j = -r; j <= r; j++) v += k[j + r] * linea[i + j];
          else for (let j = -r; j <= r; j++) v += k[j + r] * linea[reflejar(i + j, n)];
          out[at(l, i)] = v;
        }
      }
      return out;
    }
    // tres cajas (Kutskir): se aproximan a la gaussiana
    const wIdeal = Math.sqrt(12 * sigma * sigma / 3 + 1);
    let wl = Math.floor(wIdeal);
    if (wl % 2 === 0) wl--;
    const mIdeal = (12 * sigma * sigma - 3 * wl * wl - 12 * wl - 9) / (-4 * wl - 4);
    const cajas = [0, 1, 2].map((i) => ((i < Math.round(mIdeal) ? wl : wl + 2) - 1) / 2);
    const pre = new Float64Array(n + 1);
    let cur = src;
    for (const r of cajas) {
      const dst = new Float32Array(w * h), inv = 1 / (2 * r + 1);
      for (let l = 0; l < m; l++) {
        pre[0] = 0;
        for (let i = 0; i < n; i++) pre[i + 1] = pre[i] + cur[at(l, i)];
        for (let i = 0; i < n; i++) {
          const a = i - r, b = i + r;
          let v = pre[Math.min(b, n - 1) + 1] - pre[Math.max(a, 0)];
          if (a < 0) v += -a * cur[at(l, 0)];
          if (b > n - 1) v += (b - n + 1) * cur[at(l, n - 1)];
          dst[at(l, i)] = v * inv;
        }
      }
      cur = dst;
    }
    out = cur;
    return out;
  }

  function desenfocar(src, w, h, sx, sy = sx) {
    return pasada(pasada(src, w, h, sx, true), w, h, sy, false);
  }

  function ampliar(src, sw, sh, dw, dh, f) {
    const out = new Float32Array(dw * dh);
    for (let y = 0; y < dh; y++) {
      const fy = Math.min(Math.max((y + 0.5) / f - 0.5, 0), sh - 1), y0 = Math.min(Math.floor(fy), sh - 2), ty = fy - y0;
      for (let x = 0; x < dw; x++) {
        const fx = Math.min(Math.max((x + 0.5) / f - 0.5, 0), sw - 1), x0 = Math.min(Math.floor(fx), sw - 2), tx = fx - x0;
        const i = y0 * sw + x0;
        out[y * dw + x] = (src[i] * (1 - tx) + src[i + 1] * tx) * (1 - ty) + (src[i + sw] * (1 - tx) + src[i + sw + 1] * tx) * ty;
      }
    }
    return out;
  }

  /* Ruido suave de desvío 1. Para sigmas grandes se genera chico y se amplía. */
  function ruido(w, h, sigma, rng) {
    let n;
    if (sigma >= 8) {
      const f = sigma / 4;
      const cw = Math.max(2, Math.floor(w / f) + 2), ch = Math.max(2, Math.floor(h / f) + 2);
      const chico = desenfocar(rng.gauss(cw * ch), cw, ch, 4);
      n = ampliar(chico, cw, ch, w, h, f);
    } else {
      n = rng.gauss(w * h);
      if (sigma > 0) n = desenfocar(n, w, h, sigma);
    }
    return normalizar(n);
  }

  function ruido1d(n, sigma, rng) {
    const r = Math.ceil(3 * sigma), base = rng.gauss(n + 2 * r + 2), k = nucleo(Math.max(sigma, 1e-3)), kr = (k.length - 1) / 2;
    const out = new Float32Array(n);
    for (let i = 0; i < n; i++) {
      let v = 0;
      for (let j = -kr; j <= kr; j++) { const q = i + r + j; if (q >= 0 && q < base.length) v += k[j + kr] * base[q]; }
      out[i] = v;
    }
    return normalizar(out);
  }

  function gradiente(a, w, h) {
    const gx = new Float32Array(w * h), gy = new Float32Array(w * h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x;
      gx[i] = x === 0 ? a[i + 1] - a[i] : x === w - 1 ? a[i] - a[i - 1] : (a[i + 1] - a[i - 1]) / 2;
      gy[i] = y === 0 ? a[i + w] - a[i] : y === h - 1 ? a[i] - a[i - w] : (a[i + w] - a[i - w]) / 2;
    }
    return [gx, gy];
  }

  /* Distancia euclídea de cada píxel encendido al apagado más cercano (Felzenszwalb). */
  function distancia(m, w, h) {
    const INF = 1e20, f = new Float64Array(Math.max(w, h)), d = new Float64Array(Math.max(w, h));
    const v = new Int32Array(Math.max(w, h)), z = new Float64Array(Math.max(w, h) + 1);
    const g = new Float64Array(w * h);
    for (let i = 0; i < w * h; i++) g[i] = m[i] ? INF : 0;
    const dt = (n) => {
      let k = 0;
      v[0] = 0; z[0] = -INF; z[1] = INF;
      for (let q = 1; q < n; q++) {
        let s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
        while (s <= z[k]) { k--; s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]); }
        k++; v[k] = q; z[k] = s; z[k + 1] = INF;
      }
      k = 0;
      for (let q = 0; q < n; q++) { while (z[k + 1] < q) k++; d[q] = (q - v[k]) ** 2 + f[v[k]]; }
    };
    for (let x = 0; x < w; x++) { for (let y = 0; y < h; y++) f[y] = g[y * w + x]; dt(h); for (let y = 0; y < h; y++) g[y * w + x] = d[y]; }
    for (let y = 0; y < h; y++) { for (let x = 0; x < w; x++) f[x] = g[y * w + x]; dt(w); for (let x = 0; x < w; x++) g[y * w + x] = d[x]; }
    const out = new Float32Array(w * h);
    for (let i = 0; i < w * h; i++) out[i] = Math.sqrt(g[i]);
    return out;
  }

  // ------------------------------------------------------------------ dibujar con el lienzo del navegador
  const lienzos = new Map();
  function lienzo(w, h) {
    const k = w + "x" + h;
    if (!lienzos.has(k)) {
      const c = typeof OffscreenCanvas !== "undefined" ? new OffscreenCanvas(w, h) : Object.assign(document.createElement("canvas"), { width: w, height: h });
      lienzos.set(k, c.getContext("2d", { willReadFrequently: true }));
    }
    const ctx = lienzos.get(k);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.globalAlpha = 1;
    ctx.setLineDash([]);
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, w, h);
    return ctx;
  }

  /* Dibuja con fn(ctx) en blanco sobre negro y devuelve el canal rojo, de 0 a 1 (todo el lienzo,
   * o solo la región [x, y, ancho, alto] si se pide). */
  function pintar(w, h, fn, region) {
    const ctx = lienzo(w, h);
    fn(ctx);
    const [rx, ry, rw, rh] = region || [0, 0, w, h];
    const d = ctx.getImageData(rx, ry, rw, rh).data, out = new Float32Array(rw * rh);
    for (let i = 0; i < rw * rh; i++) out[i] = d[i * 4] / 255;
    return out;
  }

  const gris = (v) => { const g = Math.round(Math.min(Math.max(v, 0), 1) * 255); return `rgb(${g},${g},${g})`; };

  function polilinea(ctx, q, cerrada = false) {
    ctx.beginPath();
    ctx.moveTo(q[0][0] + 0.5, q[0][1] + 0.5);
    for (let i = 1; i < q.length; i++) ctx.lineTo(q[i][0] + 0.5, q[i][1] + 0.5);
    if (cerrada) ctx.closePath();
  }

  /* Imagen de 0 a 1 (gris) o RGB (3 planos) → ImageData para un canvas. */
  function aImageData(planos, w, h) {
    const id = new ImageData(w, h), d = id.data;
    const [r, g, b] = planos.length === 3 ? planos : [planos[0], planos[0], planos[0]];
    for (let i = 0; i < w * h; i++) {
      d[i * 4] = Math.round(Math.min(Math.max(r[i], 0), 1) * 255);
      d[i * 4 + 1] = Math.round(Math.min(Math.max(g[i], 0), 1) * 255);
      d[i * 4 + 2] = Math.round(Math.min(Math.max(b[i], 0), 1) * 255);
      d[i * 4 + 3] = 255;
    }
    return id;
  }

  // ------------------------------------------------------------------ acción 1: la pared y su frotado
  function pared(filas, columnas, px, rng) {
    const j = Math.max(2, Math.round(px * JUNTA_MM / AZULEJO_MM));
    const H = filas * px + (filas + 1) * j, W = columnas * px + (columnas + 1) * j;
    const juntas = pintar(W, H, (ctx) => {
      ctx.strokeStyle = "#fff";
      ctx.lineCap = "butt";
      for (let i = 0; i <= columnas; i++) {
        const x = i * (px + j) + j / 2 + rng.normal(0, px * 0.004), n = ruido1d(H, H / 5, rng);
        ctx.lineWidth = Math.max(1, Math.round(j * rng.uniform(0.8, 1.3)));
        ctx.beginPath();
        for (let y = 0; y < H; y += 4) ctx.lineTo(x + n[y] * px * 0.012, y);
        ctx.lineTo(x + n[H - 1] * px * 0.012, H);
        ctx.stroke();
      }
      for (let i = 0; i <= filas; i++) {
        const y = i * (px + j) + j / 2 + rng.normal(0, px * 0.004), n = ruido1d(W, W / 5, rng);
        ctx.lineWidth = Math.max(1, Math.round(j * rng.uniform(0.8, 1.3)));
        ctx.beginPath();
        for (let x = 0; x < W; x += 4) ctx.lineTo(x, y + n[x] * px * 0.012);
        ctx.lineTo(W, y + n[W - 1] * px * 0.012);
        ctx.stroke();
      }
    });
    const paso = px / 55;
    const grietas = pintar(W, H, (ctx) => {
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 1;
      for (let f = 0; f < filas; f++) for (let c = 0; c < columnas; c++) {
        const x0 = j + c * (px + j), y0 = j + f * (px + j);
        for (let g = rng.integers(2, 9); g > 0; g--) {
          let p = [x0 + rng.uniform(0, px), y0 + rng.uniform(0, px)], ang = rng.uniform(0, 2 * Math.PI);
          ctx.beginPath();
          ctx.moveTo(p[0], p[1]);
          for (let k = rng.integers(15, 70); k > 0; k--) {
            ang += rng.normal(0, 0.35);
            p = [p[0] + paso * Math.cos(ang), p[1] + paso * Math.sin(ang)];
            if (!(x0 < p[0] && p[0] < x0 + px && y0 < p[1] && p[1] < y0 + px)) break;
            ctx.lineTo(p[0], p[1]);
          }
          ctx.stroke();
        }
      }
    });
    const chips = pintar(W, H, (ctx) => {
      ctx.fillStyle = "#fff";
      for (let f = 0; f <= filas; f++) for (let c = 0; c <= columnas; c++) if (rng.random() < 0.09) {
        ctx.beginPath();
        ctx.arc(c * (px + j) + j / 2, f * (px + j) + j / 2, px * rng.uniform(0.03, 0.08), 0, 2 * Math.PI);
        ctx.fill();
      }
    });
    const dentro = new Uint8Array(W * H);
    for (let i = 0; i < W * H; i++) dentro[i] = juntas[i] > 0.5 || chips[i] > 0.5 ? 0 : 1;
    const dist = distancia(dentro, W, H), relieve = new Float32Array(W * H), mancha = ruido(W, H, px * 0.9, rng);
    for (let i = 0; i < W * H; i++) {
      relieve[i] = Math.pow(Math.min(Math.max(dist[i] / (j * 0.9), 0), 1), 0.6) * (1 - 0.45 * grietas[i]);
      mancha[i] = Math.min(Math.max((mancha[i] - 1.0) * 0.22, 0), 0.35);
    }
    return { relieve, dentro, grietas, mancha, px, junta: j, W, H };
  }

  /* El trazo del grafito: ruido corrido en diagonal (la mano va y viene). */
  function diagonal(w, h, rng) {
    const n = rng.gauss(w * h), out = new Float32Array(w * h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let v = 0;
      if (y >= 12 && y < h - 12 && x >= 12 && x < w - 12) {
        for (let k = (y - 12) * w + x - 12, i = 0; i < 25; i++, k += w + 1) v += n[k];
      } else for (let k = -12; k <= 12; k++) v += n[reflejar(y + k, h) * w + reflejar(x + k, w)];
      out[y * w + x] = v / 25;
    }
    return normalizar(out);
  }

  function frotadoPared(p, rng) {
    const { W, H } = p, grano = ruido(W, H, 0.7, rng), trazo = diagonal(W, H, rng);
    const presion = ruido(W, H, p.px * 0.6, rng), out = new Float32Array(W * H);
    for (let i = 0; i < W * H; i++) {
      const contacto = Math.pow(Math.min(Math.max(p.relieve[i], 0), 1), 1.5);
      const oscuro = 0.74 * contacto * Math.min(Math.max(0.85 + 0.12 * presion[i] + 0.1 * trazo[i] + 0.07 * grano[i], 0), 1.1);
      out[i] = Math.min(Math.max((0.96 + 0.015 * grano[i]) * (1 - oscuro), 0), 1);
    }
    return out;
  }

  /* El frotado de un azulejo de la pared, del tamaño de la celda (600 px). */
  function fondoFrotado(clave) {
    const p = pared(1, 1, 300, azar("pared", clave)), F = frotadoPared(p, azar("frotado", clave));
    const j = p.junta, rec = new Float32Array(300 * 300);
    for (let y = 0; y < 300; y++) for (let x = 0; x < 300; x++) rec[y * 300 + x] = F[(y + j) * p.W + x + j];
    return ampliar(rec, 300, 300, T, T, 2);
  }

  // ------------------------------------------------------------------ acción 3: el calco
  function rodar(a, k) { const n = a.length; return a.map((_, i) => a[((i + k) % n + n) % n]); }

  function abrirDesague(q, junta = JUNTA_MM * 4) {
    let ymax = -Infinity;
    for (const p of q) ymax = Math.max(ymax, p[1]);
    const fondo = [];
    q.forEach((p, i) => { if (p[1] >= ymax - 1.5) fondo.push(i); });
    const mx = fondo.reduce((a, i) => a + q[i][0], 0) / fondo.length;
    let i0 = fondo[0];
    for (const i of fondo) if (Math.abs(q[i][0] - mx) < Math.abs(q[i0][0] - mx)) i0 = i;
    const r = rodar(q, i0), s = [0];
    for (let i = 1; i < r.length; i++) s.push(s[i - 1] + Math.hypot(r[i][0] - r[i - 1][0], r[i][1] - r[i - 1][1]));
    const total = s[s.length - 1] + Math.hypot(r[0][0] - r[r.length - 1][0], r[0][1] - r[r.length - 1][1]);
    return r.filter((_, i) => !(s[i] < junta / 2 || s[i] > total - junta / 2));
  }

  /* Un contorno cerrado recorrido por una mano que tiembla un poco, abierto en su punto más bajo. */
  function temblar(p, rng, amplitud = 1.3, desague = true) {
    const pc = p.concat([p[0]]), s = [0];
    for (let i = 1; i < pc.length; i++) s.push(s[i - 1] + Math.hypot(pc[i][0] - pc[i - 1][0], pc[i][1] - pc[i - 1][1]));
    const L = s[s.length - 1], n = Math.max(12, Math.trunc(L / 3));
    let q = [], j = 0;
    for (let i = 0; i < n; i++) {
      const t = L * i / n;
      while (j < s.length - 2 && s[j + 1] < t) j++;
      const f = s[j + 1] > s[j] ? (t - s[j]) / (s[j + 1] - s[j]) : 0;
      q.push([pc[j][0] + f * (pc[j + 1][0] - pc[j][0]), pc[j][1] + f * (pc[j + 1][1] - pc[j][1])]);
    }
    const k = 3;
    q = q.map((_, i) => {
      let x = 0, y = 0;
      for (let d = -k; d <= k; d++) { const r = q[((i + d) % n + n) % n]; x += r[0]; y += r[1]; }
      return [x / (2 * k + 1), y / (2 * k + 1)];
    });
    const t1 = ruido1d(n, 14, rng), t2 = ruido1d(n, 2, rng);
    q = q.map((p0, i) => {
      const a = q[(i + 1) % n], b = q[(i - 1 + n) % n];
      let nx = -(a[1] - b[1]), ny = a[0] - b[0];
      const l = Math.hypot(nx, ny) + 1e-9;
      nx /= l; ny /= l;
      const tt = amplitud * t1[i] + 0.35 * t2[i];
      return [p0[0] + nx * tt, p0[1] + ny * tt];
    });
    return desague ? abrirDesague(q) : q.concat([q[0]]);
  }

  function anillos(geo) {
    return geo.filter((a) => {
      if (a.length < 4) return false;
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      for (const [x, y] of a) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
      return x1 - x0 + y1 - y0 > 8;
    });
  }

  function calcar(geo, rng, amplitud = 1.3) { return anillos(geo).map((a) => temblar(a, rng, amplitud)); }

  function dibujarTrazos(trazos, punteado, rng, grosor = 2, raya = 16, hueco = 10) {
    const capa = pintar(T, T, (ctx) => {
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = grosor;
      ctx.lineJoin = "round";
      for (const q of trazos) {
        if (q.length < 2) continue;
        if (punteado) { ctx.setLineDash([raya, hueco]); ctx.lineDashOffset = -rng.uniform(0, raya + hueco); }
        polilinea(ctx, q);
        ctx.stroke();
      }
    });
    const g = ruido(T, T, 1.2, rng);
    for (let i = 0; i < T * T; i++) capa[i] *= 0.6 + 0.4 * Math.min(Math.max(0.5 + 0.35 * g[i], 0), 1);
    return capa;
  }

  /* El calco en papel de calco puesto sobre el frotado de la pared: continuo lo hallado,
   * punteado lo reconstruido. La pauta (la celda, el fondo y el borde) en lápiz suave. */
  function calco(geo, reconstruida, fondo, pauta, rng) {
    const trazos = calcar(geo, rng), linea = dibujarTrazos(trazos, reconstruida, rng), papel = ruido(T, T, 30, rng);
    const img = new Float32Array(T * T);
    for (let i = 0; i < T * T; i++) img[i] = (1 - 0.22 * (1 - fondo[i])) * (0.985 + 0.015 * papel[i]);
    const [x0, y0, x1, y1] = pauta.celda.map(Math.round);
    for (const y of [y0, y1]) for (let x = x0; x < x1; x += 7) if (y >= 0 && y < T) img[y * T + x] *= 0.8;
    for (const x of [x0, x1]) for (let y = y0; y < y1; y += 7) if (x >= 0 && x < T) img[y * T + x] *= 0.8;
    for (const yy of [pauta.fondo, pauta.borde]) { const y = Math.round(yy); for (let x = x0; x < x1; x += 9) img[y * T + x] *= 0.82; }
    for (let i = 0; i < T * T; i++) img[i] = Math.min(Math.max(img[i] * (1 - 0.82 * linea[i]), 0), 1);
    return { img, trazos };
  }

  // ------------------------------------------------------------------ acción 4: la placa
  /* Una hoja de papel de aluminio cortada a tijera: el contorno. */
  function tijera(rng, margen = 16) {
    const m = [0, 1, 2, 3].map(() => margen + rng.uniform(-5, 9));
    const a = [0, 1, 2, 3].map(() => Math.tan(rng.normal(0, 0.8) * Math.PI / 180));
    const c = T / 2;
    const esquina = (i) => {
      let x = c, y = c;
      for (let k = 0; k < 4; k++) {
        if (i === 0) { y = m[0] + (x - c) * a[0]; x = T - m[1] - (y - c) * a[1]; }
        else if (i === 1) { x = T - m[1] - (y - c) * a[1]; y = T - m[2] - (x - c) * a[2]; }
        else if (i === 2) { y = T - m[2] - (x - c) * a[2]; x = m[3] + (y - c) * a[3]; }
        else { x = m[3] + (y - c) * a[3]; y = m[0] + (x - c) * a[0]; }
      }
      return [x, y];
    };
    const esquinas = [esquina(3), esquina(0), esquina(1), esquina(2)];
    const pts = [];
    for (let lado = 0; lado < 4; lado++) {
      const P = esquinas[lado], Q = esquinas[(lado + 1) % 4];
      const L = Math.hypot(Q[0] - P[0], Q[1] - P[1]), ux = (Q[0] - P[0]) / L, uy = (Q[1] - P[1]) / L, nx = -uy, ny = ux;
      const k = rng.integers(1, 3), cortes = [0];
      const medios = []; for (let i = 0; i < k; i++) medios.push(rng.uniform(0.2, 0.8));
      cortes.push(...medios.sort((x, y) => x - y), 1);
      for (let i = 0; i < cortes.length - 1; i++) {
        const escalon = i > 0 ? rng.normal(0, 1.1) : 0, desvio = rng.normal(0, 1.4);
        pts.push([P[0] + cortes[i] * (Q[0] - P[0]) + escalon * nx, P[1] + cortes[i] * (Q[1] - P[1]) + escalon * ny]);
        pts.push([P[0] + cortes[i + 1] * (Q[0] - P[0]) + (escalon + desvio) * nx, P[1] + cortes[i + 1] * (Q[1] - P[1]) + (escalon + desvio) * ny]);
      }
    }
    const triangulos = [];
    for (const e of esquinas) if (rng.random() < 0.35) {
      const corte = rng.uniform(24, 50);
      let hx = c - e[0], hy = c - e[1];
      const l = Math.hypot(hx, hy); hx /= l; hy /= l;
      const lx = e[0] + hx * corte / Math.SQRT2, ly = e[1] + hy * corte / Math.SQRT2, nx = -hy, ny = hx;
      triangulos.push([[e[0] - hx * 40, e[1] - hy * 40], [lx + nx * 80, ly + ny * 80], [lx - nx * 80, ly - ny * 80]]);
    }
    return { pts, triangulos };
  }

  function pliegue(rng, angulo, alto, ancho, largo = null, centro = null) {
    const [cx, cy] = centro || [rng.uniform(0.1, 0.9) * T, rng.uniform(0.1, 0.9) * T];
    const a = angulo * Math.PI / 180, ux = Math.cos(a), uy = Math.sin(a);
    const r = ruido(T, T, 45, rng), signo = rng.choice([-1, 1]), out = new Float32Array(T * T);
    for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
      const i = y * T + x;
      const d = -(x - cx) * uy + (y - cy) * ux + 3.5 * r[i], s = (x - cx) * ux + (y - cy) * uy;
      let p = signo * (alto * Math.exp(-0.5 * (d / ancho) ** 2) + 0.25 * alto * Math.tanh(d / 30));
      if (largo !== null) p *= 1 / (1 + Math.exp((Math.abs(s) - largo / 2) / 12));
      out[i] = p;
    }
    return out;
  }

  /* La hoja: arrugas grandes y suaves, el veteado del laminado, uno o dos pliegues y el filo levantado. */
  function hoja(rng) {
    const { pts, triangulos } = tijera(rng);
    const mf = pintar(T, T, (ctx) => {
      ctx.fillStyle = "#fff";
      polilinea(ctx, pts, true);
      ctx.fill("nonzero");
      ctx.fillStyle = "#000";
      for (const t of triangulos) { polilinea(ctx, t, true); ctx.fill(); }
    });
    const mascara = new Uint8Array(T * T);
    for (let i = 0; i < T * T; i++) mascara[i] = mf[i] > 0.5 ? 1 : 0;
    const h = ruido(T, T, 70, rng), fino = ruido(T, T, 12, rng);
    for (let i = 0; i < T * T; i++) h[i] = 0.22 * h[i] + 0.05 * fino[i];
    const vet = new Float32Array(T * T), blanco = rng.gauss(T * T);
    for (let y = 0; y < T; y++) { const v = rng.normal(); for (let x = 0; x < T; x++) vet[y * T + x] = v + 0.3 * blanco[y * T + x]; }
    const vetas = normalizar(desenfocar(vet, T, T, 30, 0.7));
    for (let i = 0; i < T * T; i++) h[i] += 0.007 * vetas[i];
    for (let k = 0; k < 2; k++) {
      const pl = pliegue(rng, rng.uniform(0, 180), rng.uniform(0.03, 0.07), rng.uniform(2, 4), rng.uniform(0.5, 1.2) * T);
      for (let i = 0; i < T * T; i++) h[i] += pl[i];
    }
    const dist = distancia(mascara, T, T), filo = ruido(T, T, 8, rng);
    for (let i = 0; i < T * T; i++) h[i] += 0.16 * Math.exp(-dist[i] / 2.5) * (1 + 0.5 * filo[i]);
    return { h, mascara };
  }

  /* El calco dado vuelta y repasado por el reverso: la mano que repuja agrega su temblor. */
  function repasar(trazos, rng) {
    return trazos.map((q) => {
      const n = q.length, r = ruido1d(n, 10, rng);
      return q.map((p, i) => {
        const a = q[Math.min(i + 1, n - 1)], b = q[Math.max(i - 1, 0)];
        let nx = -(a[1] - b[1]), ny = a[0] - b[0];
        const l = Math.hypot(nx, ny) + 1e-9;
        return [p[0] - (nx / l) * r[i], p[1] - (ny / l) * r[i]];
      });
    });
  }

  /* Una placa, vista por el anverso: relieve, máscara, largo del recorrido en mm y si se rompió. */
  function repujar(trazos, punteado, rng) {
    const { h, mascara } = hoja(rng);
    let largo = 0;
    const recorridos = repasar(trazos, rng).map((q) => {
      const s = [0];
      for (let i = 1; i < q.length; i++) s.push(s[i - 1] + Math.hypot(q[i][0] - q[i - 1][0], q[i][1] - q[i - 1][1]));
      largo += s[s.length - 1];
      const pr = ruido1d(q.length, 25, rng).map((v) => Math.min(Math.max(0.95 + 0.18 * v, 0.6), 1.3));
      return { q, s, pr };
    });
    const puntos = [];
    if (punteado) for (const { q, s, pr } of recorridos) {
      for (let t = rng.uniform(0, 9); t < s[s.length - 1]; t += 9) {
        let i = s.findIndex((v) => v >= t);
        if (i < 0) i = q.length - 1;
        puntos.push([q[i][0] + rng.normal(0, 0.6), q[i][1] + rng.normal(0, 0.6), pr[i]]);
      }
    }
    const surco = pintar(T, T, (ctx) => {
      ctx.globalCompositeOperation = "lighten";
      const K = 1.8;                 // la presión llega a 1,35 × 1,3: se escala para que entre en el canal
      if (punteado) {
        for (const [x, y, p] of puntos) { ctx.fillStyle = gris(p / K); ctx.beginPath(); ctx.arc(x + 0.5, y + 0.5, 2, 0, 2 * Math.PI); ctx.fill(); }
      } else {
        ctx.lineWidth = 3;
        ctx.lineCap = "round";
        for (const { q, pr } of recorridos) {
          for (let i = 0; i < q.length - 1; i++) {
            ctx.strokeStyle = gris(pr[i] / K);
            ctx.beginPath(); ctx.moveTo(q[i][0] + 0.5, q[i][1] + 0.5); ctx.lineTo(q[i + 1][0] + 0.5, q[i + 1][1] + 0.5); ctx.stroke();
          }
          for (const [p, v] of [[q[0], pr[0]], [q[q.length - 1], pr[pr.length - 1]]]) {  // donde el punzón descansa
            ctx.fillStyle = gris(1.35 * v / K);
            ctx.beginPath(); ctx.arc(p[0] + 0.5, p[1] + 0.5, 3, 0, 2 * Math.PI); ctx.fill();
          }
        }
      }
    });
    for (let i = 0; i < T * T; i++) surco[i] *= 1.8;
    const cresta = desenfocar(surco, T, T, 2.0), ancho = desenfocar(surco, T, T, 5.5), alis = desenfocar(surco, T, T, 10);
    const relieve = new Float32Array(T * T);
    for (let i = 0; i < T * T; i++) {
      relieve[i] = 2.6 * cresta[i] - 1.1 * Math.max(ancho[i] - cresta[i], 0);
      const alisado = Math.min(Math.max(alis[i] * 6, 0), 0.65);
      h[i] = h[i] * (1 - alisado) + relieve[i];
    }
    const rota = rng.random() < (punteado ? 0.16 : 0.06);
    if (rota) {
      const hay = [];
      for (let i = 0; i < T * T; i++) if (surco[i] > 0.5) hay.push(i);
      const i = hay[rng.integers(0, hay.length)] || (T * T / 2 + T / 2), x0 = i % T, y0 = Math.floor(i / T);
      const ang = rng.uniform(0, Math.PI), L = rng.uniform(15, 40);
      const x1 = x0 + L * Math.cos(ang), y1 = y0 + L * Math.sin(ang);
      const grieta = pintar(T, T, (ctx) => { ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); });
      const labios = desenfocar(pintar(T, T, (ctx) => { ctx.strokeStyle = "#fff"; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); }), T, T, 2);
      for (let k = 0; k < T * T; k++) { h[k] += 0.35 * labios[k]; if (grieta[k] > 0.5) mascara[k] = 0; }
    }
    return { altura: h, relieve, mascara, largo_mm: largo / 4, rota };
  }

  /* Hasta tres intentos: la placa rota no se tira, se cuenta y se hace otra. */
  function repujarPlaca(trazos, punteado, clave) {
    let intentos = 0, minutos = 0, roturas = 0, p;
    for (;;) {
      intentos++;
      const rng = azar("repujar", ...clave, intentos);
      p = repujar(trazos, punteado, rng);
      minutos += 4 + p.largo_mm / (punteado ? 9 : 20) + rng.normal(0, 1.5);
      if (p.rota) roturas++;
      if (!p.rota || intentos === 3) break;
    }
    return Object.assign(p, { intentos, roturas, minutos: Math.round(Math.max(minutos, 5) * 10) / 10 });
  }

  function reverso(p) {
    const altura = new Float32Array(T * T), relieve = new Float32Array(T * T), mascara = new Uint8Array(T * T);
    for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
      const i = y * T + x, j = y * T + (T - 1 - x);
      altura[i] = -p.altura[j]; relieve[i] = -p.relieve[j]; mascara[i] = p.mascara[j];
    }
    return Object.assign({}, p, { altura, relieve, mascara });
  }

  /* Foto con luz rasante de una lámina de aluminio: difusa más especular. */
  function sombrear(altura, mascara, rng, azimut = 200, elevacion = 15, k = 7.0, brillo = 0.9, fondo = 0.05) {
    const [gx, gy] = gradiente(altura, T, T);
    const az = azimut * Math.PI / 180, el = elevacion * Math.PI / 180;
    const L = [Math.cos(el) * Math.cos(az), Math.cos(el) * Math.sin(az), Math.sin(el)];
    const Hh = [L[0], L[1], L[2] + 1], hl = Math.hypot(...Hh);
    Hh[0] /= hl; Hh[1] /= hl; Hh[2] /= hl;
    const out = new Float32Array(T * T);
    for (let i = 0; i < T * T; i++) {
      if (!mascara[i]) { out[i] = fondo + 0.012 * rng.normal(); continue; }
      let nx = -gx[i] * k, ny = -gy[i] * k, nz = 1;
      const l = Math.hypot(nx, ny, nz); nx /= l; ny /= l; nz /= l;
      const dif = Math.max(nx * L[0] + ny * L[1] + nz * L[2], 0);
      const esp = Math.pow(Math.max(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0), 18);
      out[i] = Math.min(Math.max(0.16 + 0.95 * dif + 0.6 * brillo * esp + 0.012 * rng.normal(), 0), 1);
    }
    return out;
  }

  // ------------------------------------------------------------------ acción 6: la cinta
  function simplificar(pts, tol) {
    const n = pts.length;
    if (n < 3) return pts;
    const quedan = new Uint8Array(n);
    quedan[0] = quedan[n - 1] = 1;
    const pila = [[0, n - 1]];
    while (pila.length) {
      const [a, b] = pila.pop();
      const dx = pts[b][0] - pts[a][0], dy = pts[b][1] - pts[a][1], L = Math.hypot(dx, dy);
      let peor = -1, dmax = tol;
      for (let i = a + 1; i < b; i++) {
        const d = L > 1e-12 ? Math.abs(dy * (pts[i][0] - pts[a][0]) - dx * (pts[i][1] - pts[a][1])) / L : Math.hypot(pts[i][0] - pts[a][0], pts[i][1] - pts[a][1]);
        if (d > dmax) { dmax = d; peor = i; }
      }
      if (peor >= 0) { quedan[peor] = 1; pila.push([a, peor], [peor, b]); }
    }
    return pts.filter((_, i) => quedan[i]);
  }

  /* La letra puesta con masking sobre el plástico negro: bandas rectas de ancho constante que se
   * pliegan para girar, crepé con arrugas finas, extremos cortados con la mano. Arrancada, el rastro. */
  function encintar(trazos, ancho, rng, arrancada = false) {
    const S = 2, N = T * S;
    const capas = new Float32Array(N * N), crepe = new Float32Array(N * N);
    let tramos = 0, nPliegues = 0;
    const lineasPliegue = [];
    for (const [tr, w] of trazos) {
      if (tr.length < 2) continue;
      const simple = simplificar(tr, 0.3 * ancho), n = simple.length;
      for (let i = 0; i < n - 1; i++) {
        const p0 = simple[i], p1 = simple[i + 1], L = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]);
        if (L < 1) continue;
        const ux = (p1[0] - p0[0]) / L, uy = (p1[1] - p0[1]) / L, wx = -uy * ancho / 2, wy = ux * ancho / 2;
        const e0 = i === 0 ? 0 : ancho / 2, e1 = i === n - 2 ? 0 : ancho / 2;
        const a = [p0[0] - ux * e0, p0[1] - uy * e0], b = [p1[0] + ux * e1, p1[1] + uy * e1];
        const quad = [[a[0] + wx, a[1] + wy], [b[0] + wx, b[1] + wy], [b[0] - wx, b[1] - wy], [a[0] - wx, a[1] - wy]];
        const dientes = [];
        for (const [extremo, sg] of [[i === 0, -1], [i === n - 2, 1]]) {
          if (!extremo) continue;
          const q = sg < 0 ? p0 : p1, hx = ux * sg, hy = uy * sg;
          for (let k = 0; k < 7; k++) {
            const t = -0.5 + k / 6, bx = q[0] - hy * ancho * t, by = q[1] + hx * ancho * t, g = rng.uniform(1.5, 5.0);
            dientes.push([bx - hx * g, by - hy * g, rng.uniform(2, 4)]);
          }
        }
        let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
        for (const [x, y] of quad) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
        const X0 = Math.max(0, Math.floor(x0 * S) - 2), X1 = Math.min(N - 1, Math.ceil(x1 * S) + 2);
        const Y0 = Math.max(0, Math.floor(y0 * S) - 2), Y1 = Math.min(N - 1, Math.ceil(y1 * S) + 2);
        if (X1 < X0 || Y1 < Y0) continue;
        const bw = X1 - X0 + 1;
        const banda = pintar(N, N, (ctx) => {
          ctx.setTransform(S, 0, 0, S, 0, 0);
          ctx.fillStyle = "#fff";
          polilinea(ctx, quad, true);
          ctx.fill();
          ctx.fillStyle = "#000";
          for (const [x, y, r] of dientes) { ctx.beginPath(); ctx.arc(x + 0.5, y + 0.5, r, 0, 2 * Math.PI); ctx.fill(); }
        }, [X0, Y0, bw, Y1 - Y0 + 1]);
        const periodo = rng.uniform(2.0, 2.6);
        for (let y = Y0; y <= Y1; y++) for (let x = X0; x <= X1; x++) {
          const k = y * N + x, v = banda[(y - Y0) * bw + (x - X0)];
          if (!v) continue;
          const s = (x / S - p0[0]) * ux + (y / S - p0[1]) * uy;
          crepe[k] += v * (0.5 + 0.5 * Math.sin(2 * Math.PI * s / periodo));
          capas[k] += v;
        }
        tramos++;
      }
      for (let i = 1; i < n - 1; i++) {                           // pliegues y arrugas
        const p = simple[i], a = simple[i - 1], b = simple[i + 1];
        const la = Math.hypot(a[0] - p[0], a[1] - p[1]), lb = Math.hypot(b[0] - p[0], b[1] - p[1]);
        const ua = [(a[0] - p[0]) / la, (a[1] - p[1]) / la], ub = [(b[0] - p[0]) / lb, (b[1] - p[1]) / lb];
        const giro = Math.acos(Math.min(Math.max(ua[0] * ub[0] + ua[1] * ub[1], -1), 1)) * 180 / Math.PI;
        let bx = ua[0] + ub[0], by = ua[1] + ub[1];
        const bl = Math.hypot(bx, by) + 1e-9; bx /= bl; by /= bl;
        const L = ancho / 2 / Math.max(Math.sin(giro * Math.PI / 360), 0.35);
        lineasPliegue.push([p[0] - bx * L, p[1] - by * L, p[0] + bx * L, p[1] + by * L, 1.0, S]);
        nPliegues++;
        if (giro < 160) for (let k = rng.integers(3, 6); k > 0; k--) {
          const t = rng.uniform(0.2, 0.9), qx = p[0] + bx * L * t + rng.normal(0, 2), qy = p[1] + by * L * t + rng.normal(0, 2);
          const ang = Math.atan2(by, bx) + rng.normal(Math.PI / 2, 0.35), g = rng.uniform(4, 9);
          lineasPliegue.push([qx - Math.cos(ang) * g, qy - Math.sin(ang) * g, qx + Math.cos(ang) * g, qy + Math.sin(ang) * g, 0.6, 1]);
        }
      }
    }
    const plieguesS = pintar(N, N, (ctx) => {
      ctx.globalCompositeOperation = "lighten";
      for (const [xa, ya, xb, yb, v, g] of lineasPliegue) {
        ctx.strokeStyle = gris(v); ctx.lineWidth = g;
        ctx.beginPath(); ctx.moveTo(xa * S, ya * S); ctx.lineTo(xb * S, yb * S); ctx.stroke();
      }
    });
    const bajar = (a) => {                                            // de 1200 a 600: promedio de 2 × 2
      const o = new Float32Array(T * T);
      for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
        const k = 2 * y * N + 2 * x;
        o[y * T + x] = (a[k] + a[k + 1] + a[k + N] + a[k + N + 1]) / 4;
      }
      return o;
    };
    const cap = bajar(capas), cre = bajar(crepe), pli = desenfocar(bajar(plieguesS), T, T, 0.6);
    const hay = cap.map((v) => Math.min(Math.max(v, 0), 1));
    const variacion = ruido(T, T, 30, rng);
    const R = new Float32Array(T * T), G = new Float32Array(T * T), B = new Float32Array(T * T);
    for (let i = 0; i < T * T; i++) {
      const f = 1 + 0.004 * variacion[i];
      R[i] = PLASTICO[0] * f; G[i] = PLASTICO[1] * f; B[i] = PLASTICO[2] * f;
    }
    if (arrancada) {
      const rastro = desenfocar(cap.map((v) => Math.min(Math.max(v, 0), 2)), T, T, 1.0);
      for (let i = 0; i < T * T; i++) {
        const v = rastro[i] * 0.09 + 0.05 * Math.max(rng.normal(), 0) * hay[i];
        R[i] += v * 0.9; G[i] += v * 0.88; B[i] += v * 0.8;
      }
      return { img: [R, G, B], tramos, pliegues: nPliegues };
    }
    const lap = (() => {
      const bh = desenfocar(hay, T, T, 0.8), o = new Float32Array(T * T);
      for (let y = 1; y < T - 1; y++) for (let x = 1; x < T - 1; x++) {
        const i = y * T + x;
        o[i] = Math.min(Math.max((bh[i - 1] + bh[i + 1] + bh[i - T] + bh[i + T] - 4 * bh[i]) * 3, 0), 1);
      }
      return o;
    })();
    const fibra = desenfocar(rng.gauss(T * T), T, T, 0.7);
    for (let i = 0; i < T * T; i++) {
      const c = Math.min(Math.max(cap[i], 0), 3), opaca = 1 - Math.pow(0.18, c);
      const t = (1 - 0.06 * Math.min(Math.max(cap[i] - 1, 0), 2)) * (1 - 0.05 * cre[i] / Math.max(cap[i], 1));
      const sombra = (1 - 0.22 * Math.min(Math.max(pli[i], 0), 1)) * (1 - 0.3 * lap[i]), fb = 0.02 * fibra[i] * hay[i];
      R[i] = (R[i] * (1 - opaca) + CINTA[0] * t * opaca) * sombra + fb;
      G[i] = (G[i] * (1 - opaca) + CINTA[1] * t * opaca) * sombra + fb;
      B[i] = (B[i] * (1 - opaca) + CINTA[2] * t * opaca) * sombra + fb;
    }
    return { img: [R, G, B], tramos, pliegues: nPliegues };
  }

  // ------------------------------------------------------------------ acción 8: el frotado
  /* Frotadas sucesivas de una misma placa. Cada frotada aplasta entre un 5 y un 9 % del relieve
   * del surco. La letra se lee mientras el grafito sobre el surco se aparta del de su alrededor
   * más de tres veces lo que varía ese alrededor. */
  function frotador(placa, rng) {
    const trazos = [0, 1, 2].map(() => diagonal(T, T, rng)), grano = ruido(T, T, 0.7, rng);
    const presion = ruido(T, T, 150, rng);
    const relieve = Float32Array.from(placa.relieve), base = new Float32Array(T * T);
    for (let i = 0; i < T * T; i++) base[i] = placa.altura[i] - relieve[i];
    // la letra, lejos de la letra y lejos del filo
    const letra0 = new Uint8Array(T * T);
    for (let i = 0; i < T * T; i++) letra0[i] = Math.abs(relieve[i]) > 0.32 ? 1 : 0;
    const dil = (m, r) => { const o = new Uint8Array(T * T); const d = distancia(m.map((v) => 1 - v), T, T); for (let i = 0; i < T * T; i++) o[i] = d[i] <= r ? 1 : 0; return o; };
    const letra = dil(letra0, 2), cerca = dil(letra, 10), adentro = distancia(placa.mascara, T, T);
    const alrededor = new Uint8Array(T * T);
    for (let i = 0; i < T * T; i++) alrededor[i] = !cerca[i] && adentro[i] > 12 ? 1 : 0;
    let n = 0;
    const estado = { n: 0, legible: true, contraste: 0 };
    function frotar() {
      n++;
      const tr = trazos[n % 3], corr = 37 * n, h = new Float32Array(T * T);
      let minimo = Infinity;
      for (let i = 0; i < T * T; i++) { h[i] = base[i] + relieve[i]; if (placa.mascara[i] && h[i] < minimo) minimo = h[i]; }
      for (let i = 0; i < T * T; i++) if (!placa.mascara[i]) h[i] = minimo - 0.3;
      const env = desenfocar(h, T, T, 7), img = new Float32Array(T * T);
      for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
        const i = y * T + x, t = tr[y * T + ((x - corr) % T + T) % T];
        const contacto = 0.16 + 0.84 * Math.pow(Math.min(Math.max((h[i] - env[i]) / 0.9, 0), 1), 1.2);
        const oscuro = 0.8 * contacto * Math.min(Math.max(0.85 + 0.12 * presion[i] + 0.14 * t + 0.08 * grano[i], 0), 1.1);
        img[i] = Math.min(Math.max((0.965 + 0.012 * grano[i]) * (1 - oscuro), 0), 1);
      }
      const d = desenfocar(img.map((v) => 1 - v), T, T, 1.5);
      let sl = 0, nl = 0, sa = 0, na = 0, qa = 0;
      for (let i = 0; i < T * T; i++) {
        if (letra[i]) { sl += d[i]; nl++; }
        if (alrededor[i]) { sa += d[i]; qa += d[i] * d[i]; na++; }
      }
      const ma = sa / Math.max(na, 1), sd = Math.sqrt(Math.max(qa / Math.max(na, 1) - ma * ma, 0));
      estado.n = n;
      estado.contraste = (sl / Math.max(nl, 1) - ma) / (sd + 1e-9);
      estado.legible = estado.contraste > 3;
      const aplasta = 1 - rng.uniform(0.05, 0.09);
      for (let i = 0; i < T * T; i++) { relieve[i] *= aplasta; base[i] *= 0.98; }
      return img;
    }
    return { frotar, estado };
  }

  // ------------------------------------------------------------------ acciones 9 y 10: el agua y la voz
  function superficieQuieta(rng) { return ruido(T, T, 60, rng); }

  function superficieTocada(quieta, fase, punto = [0.08, 0.92], amplitud = 2.2, onda = 46, caida = 420) {
    const out = new Float32Array(T * T), px = punto[0] * T, py = punto[1] * T;
    for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
      const r = Math.hypot(x - px, y - py), frente = 1 / (1 + Math.exp((r - fase * onda - 60) / 25));
      out[y * T + x] = quieta[y * T + x] + amplitud * Math.sin(2 * Math.PI * r / onda - fase * 2 * Math.PI) * Math.exp(-r / caida) * (r / (r + 25)) * frente;
    }
    return out;
  }

  /* Ondas de Faraday: la bandeja vibra y el agua responde a la mitad de la frecuencia. El dibujo
   * de la onda queda quieto y su amplitud va y vuelve. */
  function faraday(hz, volumen, rng) {
    const sigma = 0.072, rho = 1000.0;
    const lamMm = Math.cbrt(2 * Math.PI * sigma / (rho * (hz / 2) ** 2)) * 1000, lam = lamMm * 4;
    const k = 2 * Math.PI / lam, m = volumen < 0.6 ? 2 : 3, base = rng.uniform(0, Math.PI);
    const w = new Float32Array(T * T);
    for (let i = 0; i < m; i++) {
      const th = base + i * Math.PI / m, c = Math.cos(th), s = Math.sin(th), f = rng.uniform(0, 2 * Math.PI);
      for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) w[y * T + x] += Math.cos(k * (x * c + y * s) + f);
    }
    const parches = ruido(T, T, 80, rng), quieta = superficieQuieta(rng);
    for (let i = 0; i < T * T; i++) w[i] *= 0.6 * volumen * (0.5 + 0.5 * Math.min(Math.max(parches[i], -1), 1)) / m;
    return { patron: w, quieta, lamMm, en: (momento) => {
      const va = Math.cos(2 * Math.PI * momento), out = new Float32Array(T * T);
      for (let i = 0; i < T * T; i++) out[i] = va * w[i] + quieta[i];
      return out;
    } };
  }

  function silabas(verso) {
    const n = [];
    for (const palabra of verso.toLowerCase().match(/[a-záéíóúüñ]+/g) || []) {
      for (const grupo of palabra.match(/[aeiouáéíóúü]+/g) || []) {
        n.push(palabra);
        if (grupo.length > 1 && /[íú]/.test(grupo)) n.push(palabra);
      }
    }
    return n;
  }

  /* Cáusticas: cada punto de la placa manda su luz a un punto de la pared. */
  function reflejo(placa, agua, kPlaca = 26, kAgua = 55) {
    const g = placa._grad || (placa._grad = gradiente(placa.altura, T, T));
    const [gx, gy] = g, [wx, wy] = gradiente(agua, T, T);
    const acc = new Float32Array(T * T);
    for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
      const i = y * T + x;
      if (!placa.mascara[i]) continue;
      const u = x + 2 * kPlaca * gx[i] + kAgua * wx[i], v = y + 2 * kPlaca * gy[i] + kAgua * wy[i];
      const u0 = Math.floor(u), v0 = Math.floor(v), fu = u - u0, fv = v - v0;
      if (u0 < -1 || v0 < -1 || u0 >= T || v0 >= T) continue;
      const pe = 0.9;
      if (u0 >= 0 && v0 >= 0) acc[v0 * T + u0] += pe * (1 - fu) * (1 - fv);
      if (u0 + 1 < T && v0 >= 0) acc[v0 * T + u0 + 1] += pe * fu * (1 - fv);
      if (u0 >= 0 && v0 + 1 < T) acc[(v0 + 1) * T + u0] += pe * (1 - fu) * fv;
      if (u0 + 1 < T && v0 + 1 < T) acc[(v0 + 1) * T + u0 + 1] += pe * fu * fv;
    }
    const luz = desenfocar(acc, T, T, 1.6), out = new Float32Array(T * T);
    for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
      const i = y * T + x, e = luz[((y - 6 + T) % T) * T + (x - 9 + T) % T];
      out[i] = luz[i] + 0.32 * e + 0.05 * (1 + 0.5 * Math.tanh(3 * (wx[i] + wy[i])));
    }
    return out;
  }

  /* Homografía de 4 puntos (src → dst), como cv2.getPerspectiveTransform. */
  function homografia(src, dst) {
    const A = [], b = [];
    for (let i = 0; i < 4; i++) {
      const [x, y] = src[i], [u, v] = dst[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
      A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
    }
    for (let c = 0; c < 8; c++) {                                   // Gauss con pivoteo
      let p = c;
      for (let r = c + 1; r < 8; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      [A[c], A[p]] = [A[p], A[c]]; [b[c], b[p]] = [b[p], b[c]];
      for (let r = 0; r < 8; r++) if (r !== c) {
        const f = A[r][c] / A[c][c];
        for (let k = c; k < 8; k++) A[r][k] -= f * A[c][k];
        b[r] -= f * b[c];
      }
    }
    const h = b.map((v, i) => v / A[i][i]);
    return [h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], 1];
  }

  /* La luz llega al revés y abierta en trapecio, verde por el celofán, sobre azulejos. */
  function fotoAgua(luz, W, H, reflectancia, rng, punto = [0.5, 0.84]) {
    const m = 0.04 * W, ab = (W - 2 * m) * TRAPECIO;
    const dst = [[m, 0.06 * H], [W - m, 0.06 * H], [W / 2 + ab / 2, 0.94 * H], [W / 2 - ab / 2, 0.94 * H]];
    const Hm = homografia(dst, [[0, 0], [T, 0], [T, T], [0, T]]);  // de la foto a la placa (ya dada vuelta)
    const R = new Float32Array(W * H), G = new Float32Array(W * H), B = new Float32Array(W * H);
    const px = punto[0] * W, py = punto[1] * H;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = y * W + x, d = Hm[6] * x + Hm[7] * y + 1;
      const sx = (Hm[0] * x + Hm[1] * y + Hm[2]) / d, sy0 = (Hm[3] * x + Hm[4] * y + Hm[5]) / d;
      let L = 0, zona = 0;
      if (sx >= 0 && sy0 >= 0 && sx < T - 1 && sy0 < T - 1) {
        const sy = T - 1 - sy0;                                     // al revés
        const x0 = Math.floor(sx), y0 = Math.floor(sy), tx = sx - x0, ty = sy - y0, k = y0 * T + x0;
        const y1 = Math.min(y0 + 1, T - 1) * T + x0;
        L = (luz[k] * (1 - tx) + luz[k + 1] * tx) * (1 - ty) + (luz[y1] * (1 - tx) + luz[y1 + 1] * tx) * ty;
        zona = 1;
      }
      const r2 = (x - px) ** 2 + (y - py) ** 2;
      const lampara = 2.6 * Math.exp(-r2 / (2 * 81)) + 0.5 * Math.exp(-r2 / (2 * 2025));
      const v = (0.55 * L * zona + lampara * zona) * reflectancia[i];
      const ruidoFoto = 0.01 * rng.normal();
      R[i] = Math.pow(Math.min(Math.max(v * VERDE[0] + 0.012 + ruidoFoto, 0), 1), 1 / 1.1);
      G[i] = Math.pow(Math.min(Math.max(v * VERDE[1] + 0.018 + ruidoFoto, 0), 1), 1 / 1.1);
      B[i] = Math.pow(Math.min(Math.max(v * VERDE[2] + 0.035 + ruidoFoto, 0), 1), 1 / 1.1);
    }
    return [R, G, B];
  }

  /* Dos por dos azulejos sueltos: el esmalte refleja, la junta no. */
  function azulejos(W, H, rng) {
    const px = Math.round(Math.max(W, H) / 2), p = pared(2, 2, px, rng);
    const alb = new Float32Array(p.W * p.H);
    for (let i = 0; i < alb.length; i++) alb[i] = (p.dentro[i] ? 0.88 - p.mancha[i] - 0.3 * p.grietas[i] : 0.28) * (0.8 + 0.2 * p.relieve[i]);
    const out = new Float32Array(W * H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      out[y * W + x] = alb[Math.min(p.H - 1, Math.floor(y * p.H / H)) * p.W + Math.min(p.W - 1, Math.floor(x * p.W / W))];
    }
    return out;
  }

  raiz.Simuladores = {
    T, PAPEL, CINTA, PLASTICO, azar, ruido, desenfocar, distancia, pintar, aImageData,
    fondoFrotado, calco, calcar, dibujarTrazos, repujarPlaca, reverso, sombrear, encintar, frotador,
    superficieQuieta, superficieTocada, faraday, silabas, reflejo, fotoAgua, azulejos,
  };
})(typeof window !== "undefined" ? window : globalThis);
