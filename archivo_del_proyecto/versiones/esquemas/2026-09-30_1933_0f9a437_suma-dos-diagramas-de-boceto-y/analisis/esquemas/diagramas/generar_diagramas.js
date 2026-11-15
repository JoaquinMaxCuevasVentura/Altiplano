/*
 * Genera los diagramas de las figuras 7 y 8 con trazo de boceto.
 *
 * Uso (desde la raíz del repositorio):
 *     node analisis/esquemas/diagramas/generar_diagramas.js
 *
 * Escribe fig7_memoria_retorno.svg y fig8_tres_montones.svg en esta carpeta.
 * Luego `python3 articulo/generar_figuras.py` los pasa a figura_7.png y
 * figura_8.png.
 *
 * El trazo irregular sale de rough.js (MIT, vendor/) y la letra es Caveat
 * (SIL Open Font License, fuentes/), incrustada en cada SVG. Las semillas son
 * fijas: el mismo código da siempre el mismo dibujo. Para cambiar un rótulo,
 * edítalo aquí y vuelve a correr el script.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const rough = require('./vendor/rough.cjs.js');

const DIR = __dirname;
const gen = rough.generator();

// Paleta: la de los esquemas de las figuras 1 a 6.
const PAPEL = '#f6f2ea';
const TINTA = '#3b3530';
const TEXTO = '#2f2a26';
const GRIS = '#8a8079';
const SIENA = '#b5542b';

const FUENTE = fs.readFileSync(path.join(DIR, 'fuentes', 'Caveat-Regular-sub.ttf')).toString('base64');

function azar(semilla) {
  let a = semilla >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

class Hoja {
  constructor(ancho, alto, semilla, etiqueta, y0) {
    this.ancho = ancho;
    this.alto = alto;
    this.y0 = y0 || 0;
    this.semilla = semilla;
    this.rnd = azar(semilla);
    this.etiqueta = etiqueta;
    this.capas = [];
  }

  op(extra) {
    return Object.assign({ roughness: 0.7, bowing: 0.6, stroke: TINTA, strokeWidth: 1, seed: this.semilla++ }, extra || {});
  }

  agregar(dibujo, atributos) {
    for (const p of gen.toPaths(dibujo)) {
      this.capas.push(`<path d="${p.d}" fill="${p.fill || 'none'}" stroke="${p.stroke}" stroke-width="${p.strokeWidth}"` +
        ` stroke-linecap="round" stroke-linejoin="round"${atributos || ''}/>`);
    }
  }

  linea(x1, y1, x2, y2, extra, atributos) {
    this.agregar(gen.line(x1, y1, x2, y2, this.op(extra)), atributos);
  }

  trazo(puntos, extra, atributos) {
    this.agregar(gen.linearPath(puntos, this.op(extra)), atributos);
  }

  curva(puntos, extra, atributos) {
    this.agregar(gen.curve(puntos, this.op(extra)), atributos);
  }

  poligono(puntos, extra, atributos) {
    this.agregar(gen.polygon(puntos, this.op(extra)), atributos);
  }

  circulo(x, y, d, extra, atributos) {
    this.agregar(gen.circle(x, y, d, this.op(extra)), atributos);
  }

  punteada(x1, y1, x2, y2, color, guion) {
    this.linea(x1, y1, x2, y2, { stroke: color || TINTA, strokeWidth: 0.9, disableMultiStroke: true, roughness: 0.5 },
      ` stroke-dasharray="${guion || '5 4'}"`);
  }

  // Punta abierta, como en las notaciones a mano: dos trazos cortos.
  punta(x, y, angulo, color, largo) {
    const l = largo || 7;
    for (const s of [-1, 1]) {
      const a = angulo + Math.PI + s * 0.42;
      this.linea(x, y, x + l * Math.cos(a), y + l * Math.sin(a), { stroke: color || TINTA, strokeWidth: 1, roughness: 0.4 });
    }
  }

  flecha(x1, y1, x2, y2, color, punteada) {
    if (punteada) this.punteada(x1, y1, x2, y2, color);
    else this.linea(x1, y1, x2, y2, { stroke: color || TINTA, strokeWidth: 1 });
    this.punta(x2, y2, Math.atan2(y2 - y1, x2 - x1), color);
  }

  flechaCurva(puntos, color, punteada) {
    const atributos = punteada ? ' stroke-dasharray="5 4"' : '';
    this.curva(puntos, { stroke: color || TINTA, strokeWidth: 1, disableMultiStroke: !!punteada }, atributos);
    const [xa, ya] = puntos[puntos.length - 2];
    const [xb, yb] = puntos[puntos.length - 1];
    this.punta(xb, yb, Math.atan2(yb - ya, xb - xa), color);
  }

  texto(x, y, cadena, o) {
    o = o || {};
    const t = o.tam || 13;
    const color = o.color || TEXTO;
    const ancla = o.ancla || 'start';
    const halo = o.halo === false ? '' : ` stroke="${PAPEL}" stroke-width="3.2" stroke-linejoin="round" paint-order="stroke"`;
    const grueso = o.grueso ? ` stroke="${color}" stroke-width="0.45" paint-order="normal"` : halo;
    const giro = o.giro ? ` transform="rotate(${o.giro} ${x} ${y})"` : '';
    const lineas = Array.isArray(cadena) ? cadena : [cadena];
    const interlinea = o.interlinea || Math.round(t * 1.12);
    lineas.forEach((l, i) => {
      this.capas.push(`<text x="${x}" y="${y + i * interlinea}" font-size="${t}" fill="${color}" text-anchor="${ancla}"${grueso}${giro}>${esc(l)}</text>`);
    });
  }

  // Piedra: polígono irregular alrededor de un centro.
  piedra(cx, cy, r, color, relleno, anguloso) {
    const n = anguloso ? 3 + Math.floor(this.rnd() * 3) : 6 + Math.floor(this.rnd() * 3);
    const giro = this.rnd() * Math.PI * 2;
    const pts = [];
    for (let i = 0; i < n; i++) {
      const a = giro + (i / n) * Math.PI * 2 + (this.rnd() - 0.5) * (anguloso ? 0.9 : 0.5);
      const rr = r * (anguloso ? 0.6 + this.rnd() * 0.6 : 0.78 + this.rnd() * 0.3);
      pts.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a) * (anguloso ? 0.8 : 0.72)]);
    }
    this.poligono(pts, { stroke: color, strokeWidth: 0.9, roughness: 0.5, fill: relleno || PAPEL, fillStyle: 'solid' });
  }

  // Coloca formas sin que se encimen dentro de una silueta dada.
  empacar(dentro, xmin, xmax, ymin, ymax, rmin, rmax, intentos) {
    const hechos = [];
    for (let k = 0; k < intentos; k++) {
      const r = rmin + this.rnd() * (rmax - rmin);
      const x = xmin + this.rnd() * (xmax - xmin);
      const y = ymin + this.rnd() * (ymax - ymin);
      if (!dentro(x, y, r)) continue;
      if (hechos.some(h => Math.hypot(h.x - x, h.y - y) < h.r + r + 0.8)) continue;
      hechos.push({ x, y, r });
    }
    return hechos.sort((a, b) => a.y - b.y);
  }

  // Montón: silueta parabólica sobre una base.
  monton(cx, base, semiancho, alto, dibujar, rmin, rmax) {
    const cima = x => base - alto * Math.pow(Math.max(0, 1 - Math.pow((x - cx) / semiancho, 2)), 0.85);
    const dentro = (x, y, r) => y + r * 0.7 <= base && y - r * 0.7 >= cima(x) && Math.abs(x - cx) + r <= semiancho;
    for (const h of this.empacar(dentro, cx - semiancho, cx + semiancho, base - alto, base, rmin, rmax, 5000)) dibujar(h);
  }

  svg(titulo) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 ${this.y0} ${this.ancho} ${this.alto}" role="img" aria-label="${esc(this.etiqueta)}" font-family="Caveat, 'Segoe Print', 'Comic Sans MS', cursive">\n` +
      `  <title>${esc(titulo)}</title>\n` +
      `  <defs><style>@font-face{font-family:'Caveat';src:url(data:font/ttf;base64,${FUENTE}) format('truetype');}</style></defs>\n` +
      `  <rect y="${this.y0}" width="${this.ancho}" height="${this.alto}" fill="${PAPEL}"/>\n  ` +
      this.capas.join('\n  ') + '\n</svg>\n';
  }
}

/* ------------------------------------------------------------------ */
/* Figura 7. La memoria del retorno, en sección (pp. 156-157)          */
/* ------------------------------------------------------------------ */
function figura7() {
  const h = new Hoja(700, 416, 7101,
    'Sección de la memoria del retorno: desde la atalaya, la mirada pasa sobre la muralla y el foso hasta el horizonte; ' +
    'la muralla es una pirca de doble cara cuyas caras son los apellidos que vuelven y cuyo relleno son los sin tierra; ' +
    'en el foso quedan los muertos del hambre.', 36);
  const suelo = 300;
  const ojo = 114;

  // Terreno cortado: una banda rayada bajo el suelo, con el foso.
  const foso = [[334, suelo], [360, 392], [532, 392], [558, suelo]];
  h.poligono([[16, suelo], [334, suelo], [360, 392], [532, 392], [558, suelo], [684, suelo], [684, suelo + 11],
    [566, suelo + 11], [540, 403], [352, 403], [326, suelo + 11], [16, suelo + 11]],
  { stroke: 'none', fill: GRIS, fillStyle: 'hachure', hachureGap: 4.2, fillWeight: 0.55, hachureAngle: -41, roughness: 0.6 });
  // El foso «hondo y alquitranado»: rayado cruzado.
  h.poligono(foso, { stroke: 'none', fill: TINTA, fillStyle: 'cross-hatch', hachureGap: 6.5, fillWeight: 0.45, roughness: 0.8 },
    ' opacity="0.42"');
  h.trazo([[16, suelo], [120, suelo - 1], [214, suelo + 1], [334, suelo], [360, 392], [532, 392], [558, suelo], [684, suelo - 1]],
    { strokeWidth: 1.3 });

  // Atalaya: una torre de piedras apiladas.
  for (let y = suelo - 8, fila = 0; y > 136; y -= 16, fila++) {
    const desfase = fila % 2 ? 14 : 0;
    for (let x = 44 + desfase; x < 100; x += 28) {
      const x2 = Math.min(x + 27, 104);
      if (x2 - x < 8) continue;
      h.poligono([[x, y - 7], [x2, y - 7.5], [x2, y + 7], [x, y + 7.5]], { strokeWidth: 0.9, roughness: 0.9, fill: PAPEL, fillStyle: 'solid' });
    }
    if (desfase) h.poligono([[44, y - 7], [58, y - 7.5], [58, y + 7], [44, y + 7.5]], { strokeWidth: 0.9, roughness: 0.9, fill: PAPEL, fillStyle: 'solid' });
  }
  h.trazo([[40, 129], [108, 128]], { strokeWidth: 1.2 });
  // Los que miran: figuras mínimas sobre la atalaya.
  for (let i = 0; i < 7; i++) {
    const x = 48 + i * 8.6 + (h.rnd() - 0.5) * 2;
    h.linea(x, 128, x, 118, { strokeWidth: 1.2, roughness: 0.3 });
    h.circulo(x, 115.6, 3.4, { strokeWidth: 0.8, roughness: 0.3, fill: TINTA, fillStyle: 'solid' });
  }
  h.texto(113, 206, ['atalaya', 'de la esperanza (157)'], { tam: 13 });

  // La mirada: sólo el horizonte.
  h.circulo(108, ojo, 3.2, { strokeWidth: 0.9, fill: TINTA, fillStyle: 'solid' });
  h.punteada(112, ojo, 676, ojo);
  h.punta(676, ojo, 0);
  h.texto(318, ojo - 9, '«sólo miraban el horizonte» (157)', { ancla: 'middle' });
  h.linea(684, ojo - 8, 684, ojo + 8, { strokeWidth: 1.1 });
  h.texto(684, ojo - 54, 'horizonte', { ancla: 'end', tam: 15 });
  h.texto(684, ojo - 38, ['la memoria: «lo pasado antiguo,', 'lo bueno y lo alegre de las cosechas» (156)'], { ancla: 'end', interlinea: 14 });

  // La muralla de su visión: pirca de doble cara.
  const mTop = 190;
  const caras = [[214, 237], [267, 290]];
  for (const [xa, xb] of caras) {
    let y = suelo;
    while (y > mTop + 4) {
      const alto = 13 + h.rnd() * 6;
      const y2 = Math.max(mTop, y - alto);
      h.poligono([[xa + h.rnd() * 2, y], [xb - h.rnd() * 2, y - 0.5], [xb - h.rnd() * 2.5, y2], [xa + h.rnd() * 2.5, y2 + 0.5]],
        { strokeWidth: 1, roughness: 1, fill: PAPEL, fillStyle: 'solid' });
      y = y2 - 0.6;
    }
  }
  const relleno = h.empacar((x, y, r) => x - r >= 238.5 && x + r <= 265.5 && y - r >= mTop + 2 && y + r <= suelo - 1,
    238, 266, mTop, suelo, 2, 3.6, 4000);
  for (const p of relleno) h.piedra(p.x, p.y, p.r, SIENA, PAPEL);
  h.texto(290, 182, '«muralla de su visión» (156-157)', { ancla: 'end' });
  h.texto(302, 130, ['relleno: la «legión»', 'sin tierra: Condori, Mamani,', 'Quispe (22) y los tres', 'vigilantes (75)'],
    { color: SIENA, interlinea: 14 });
  h.flechaCurva([[318, 180], [300, 200], [276, 212], [262, 214]], SIENA);
  // Las caras: los apellidos que vuelven.
  h.texto(24, 330, ['las caras: los apellidos que vuelven (156)', 'Villca, Huanca, Huallpa, Yupanqui,', 'Ticona, Choque, Chuquihuanca'], {});
  h.trazo([[196, 322], [210, 316], [219, 290]], { strokeWidth: 0.9, roughness: 0.4 });
  h.punta(219, 290, Math.atan2(290 - 316, 219 - 210));

  // No bajar la cabeza.
  h.punteada(446, ojo + 6, 446, 190, TINTA, '2 3');
  h.linea(436, 195, 456, 195, { strokeWidth: 1.4, roughness: 0.3 });
  h.texto(458, 150, ['«sin atreverse a bajar la cabeza', 'al tremendo hoyo» (157)'], {});
  h.texto(446, 226, ['foso «hondo y alquitranado»:', 'el intervalo del hambre (157)'], { ancla: 'middle' });
  h.punteada(446, 246, 446, 304, TINTA, '2 3');
  // En el foso: los muertos que el retorno no nombra.
  h.texto(446, 326, ['más de ciento cincuenta muertos,', '«sin culto y sin recuerdo» (156);', 'Condori, en el cementerio', 'de los mineros (154); Quispe,', '«en muchos sitios» (69)'],
    { ancla: 'middle', color: SIENA, tam: 12.5, interlinea: 13.5 });

  // Eje: más lejos, más atrás en el tiempo.
  const eje = 424;
  h.linea(40, eje, 676, eje, { strokeWidth: 0.9, stroke: GRIS });
  h.punta(676, eje, 0, GRIS);
  for (const [x, rotulo] of [[74, 'ahora: el retorno'], [446, 'el hambre'], [636, 'antes del hambre']]) {
    h.linea(x, eje - 4, x, eje + 4, { strokeWidth: 0.9, stroke: GRIS });
    h.texto(x, eje + 18, rotulo, { ancla: 'middle', color: GRIS });
  }
  h.texto(684, eje - 7, 'tiempo', { ancla: 'end', color: GRIS });
  h.texto(16, 58, '( ) páginas de la novela', { color: GRIS, tam: 12.5 });
  for (const [x, y] of [[74, 304], [446, 406]]) h.punteada(x, y, x, eje - 6, GRIS, '1.5 4');

  return h.svg('Figura 7. La memoria del retorno, en sección');
}

/* ------------------------------------------------------------------ */
/* Figura 8. Tres montones: piedra, papel y máquina                    */
/* ------------------------------------------------------------------ */
function figura8() {
  const h = new Hoja(700, 432, 8101,
    'Tres estaciones con el mismo esquema. En el ayllu se extraen piedras y se amontonan para rescatar tierra; ' +
    'en la aldea los animales entran por el embudo y sale papel, que termina en el montón de papeles del tinterillo; ' +
    'en la mina salen estaño para la compañía y desmonte. Debajo, quién queda enterrado en cada lugar.');
  const cols = [118, 350, 582];
  const base = 290;

  // Separadores y suelo común.
  for (const x of [234, 466]) h.punteada(x, 18, x, 410, GRIS, '1.5 5');
  h.trazo([[16, base], [230, base + 1], [470, base - 1], [684, base]], { strokeWidth: 1.2 });

  h.texto(684, 424, '( ) páginas de la novela', { ancla: 'end', color: GRIS, tam: 12 });
  const encabezados = [['PIEDRA', 'el ayllu'], ['PAPEL', 'la aldea'], ['MÁQUINA', 'la mina']];
  encabezados.forEach(([a, b], i) => {
    h.texto(cols[i], 34, a, { ancla: 'middle', tam: 22, grueso: true });
    h.texto(cols[i], 51, b, { ancla: 'middle', tam: 14, color: GRIS });
  });

  // --- Ayllu: se sacan piedras del erial y se amontonan. ---
  let c = cols[0];
  h.texto(c - 100, 80, ['erial de', 'piedras (9)'], { interlinea: 14 });
  h.trazo([[c - 100, 112], [c - 40, 111]], { strokeWidth: 1 });
  for (const [dx, r] of [[-94, 3], [-84, 2.4], [-73, 3.4], [-63, 2.2], [-54, 3], [-45, 2.5]]) h.piedra(c + dx, 108.5 - r * 0.4, r, TINTA);
  h.flechaCurva([[c - 66, 118], [c - 62, 160], [c - 40, 196], [c - 18, 214]]);
  h.texto(c - 56, 150, ['extraen piedras', 'y las amontonan (9)'], { tam: 12.5 });
  h.trazo([[c + 40, 112], [c + 100, 111]], { strokeWidth: 1 }, ' stroke-dasharray="5 4"');
  for (let x = c + 46; x < c + 98; x += 8) h.linea(x, 111, x + 4, 106, { strokeWidth: 0.7, stroke: GRIS, roughness: 0.3 });
  h.texto(c + 100, 80, ['«tierra', 'rescatada» (9)'], { ancla: 'end', interlinea: 14 });
  h.flechaCurva([[c + 14, 212], [c + 38, 180], [c + 58, 146], [c + 66, 120]], TINTA, true);
  h.texto(c + 64, 172, ['«quizá', 'un día»'], { tam: 12.5, color: GRIS });

  // --- Aldea: radio urbano, embudo, papel. ---
  c = cols[1];
  const rx = c - 60, ry = 104;
  h.circulo(rx, ry, 50, { strokeWidth: 1 });
  h.linea(rx, ry, rx + 25, ry - 2, { strokeWidth: 0.7, stroke: GRIS });
  h.circulo(rx, ry, 2.2, { fill: TINTA, fillStyle: 'solid', strokeWidth: 0.6 });
  for (const [dx, dy, s] of [[-11, -10, 1], [5, -12, -1], [-13, 5, 1], [3, 8, -1], [12, -1, 1]]) {
    const x = rx + dx, y = ry + dy;
    h.agregar(gen.ellipse(x, y, 7.5, 4, h.op({ strokeWidth: 0.8, roughness: 0.4 })));
    h.circulo(x + s * 4.6, y - 2, 2.6, { strokeWidth: 0.7, roughness: 0.2 });
    for (const px of [-2.4, -0.8, 1, 2.6]) h.linea(x + px, y + 1.6, x + px * 1.1, y + 4.6, { strokeWidth: 0.55, roughness: 0.2 });
  }
  h.curva([[rx + 13, ry + 25], [rx + 18, ry + 21], [rx + 22, ry + 26], [rx + 28, ry + 20]], { strokeWidth: 0.8, roughness: 0.5 });
  h.texto(rx, ry + 42, ['radio urbano,', 'ordenanza, firma (96)'], { ancla: 'middle', tam: 12.5, interlinea: 13 });
  const fx = c + 18, fy = 100;
  h.poligono([[fx - 24, fy], [fx + 24, fy], [fx + 4, fy + 26], [fx + 4, fy + 38], [fx - 4, fy + 38], [fx - 4, fy + 26]], { strokeWidth: 1.1 });
  h.flecha(rx + 28, ry - 2, fx - 28, fy + 6);
  h.texto(fx, fy - 9, '«embudo» (102)', { ancla: 'middle' });
  h.flecha(fx + 26, fy + 8, c + 104, fy + 8);
  h.texto(c + 104, fy + 26, ['«hasta esfumarse»:', 'propiedades', 'del Alcalde (102)'], { ancla: 'end', tam: 12.5, interlinea: 13 });
  for (const [dx, dy, a] of [[-3, 50, 12], [5, 62, -18], [-2, 74, 8]]) {
    const x = fx + dx, y = fy + dy;
    h.agregar(gen.rectangle(x - 5, y - 3, 10, 6, h.op({ strokeWidth: 0.8, roughness: 0.4 })), ` transform="rotate(${a} ${x} ${y})"`);
  }
  h.flecha(fx, fy + 84, fx - 10, 208);
  h.texto(fx + 10, 178, ['«mil seiscientos', 'bolivianos en papel»', '(103), para el', 'tinterillo (105)'], { tam: 12.5, interlinea: 13 });

  // --- Mina: castillete, pique, estaño y desmonte. ---
  c = cols[2];
  const tx = c - 24;
  h.trazo([[tx - 22, 150], [tx, 84], [tx + 22, 150]], { strokeWidth: 1.1 });
  h.linea(tx - 14, 126, tx + 14, 126, { strokeWidth: 0.8 });
  h.linea(tx - 7, 104, tx + 7, 104, { strokeWidth: 0.8 });
  h.circulo(tx, 84, 13, { strokeWidth: 1 });
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2;
    h.linea(tx + 6.5 * Math.cos(a), 84 + 6.5 * Math.sin(a), tx + 9 * Math.cos(a), 84 + 9 * Math.sin(a), { strokeWidth: 0.9, roughness: 0.2 });
  }
  h.linea(tx - 6, 150, tx - 6, 196, { strokeWidth: 1 });
  h.linea(tx + 6, 150, tx + 6, 196, { strokeWidth: 1 });
  h.agregar(gen.rectangle(tx - 4.5, 160, 9, 12, h.op({ strokeWidth: 0.8, roughness: 0.3, fill: TINTA, fillStyle: 'cross-hatch', hachureGap: 2.5, fillWeight: 0.4 })));
  h.texto(c - 102, 76, ['«rieles,', 'maderos,', 'dinamita,', 'hombres»', '(151)'], { tam: 12.5, interlinea: 12.5 });
  h.flechaCurva([[c - 90, 136], [c - 86, 158], [c - 64, 170], [tx - 8, 170]]);
  h.flecha(tx + 16, 84, c + 102, 84);
  h.texto(c + 102, 100, ['«cosecharás miles de', 'cargas de estaño» (142):', 'para la compañía'], { ancla: 'end', tam: 12.5, interlinea: 13 });
  h.flechaCurva([[tx + 7, 190], [tx + 18, 202], [tx + 32, 214]]);
  h.texto(tx + 26, 186, 'roca sin mineral', { tam: 12.5 });

  // --- Los tres montones, el mismo gesto. ---
  const piedras = hh => h.piedra(hh.x, hh.y, hh.r, SIENA, PAPEL);
  h.monton(cols[0], base, 72, 70, piedras, 3.2, 6.5);
  h.monton(cols[1], base, 72, 66, p => {
    const ang = (h.rnd() - 0.5) * 50;
    const w = p.r * 2.2, al = p.r * (h.rnd() < 0.2 ? 1.25 : 0.9);
    const giro = ` transform="rotate(${ang.toFixed(1)} ${p.x.toFixed(1)} ${p.y.toFixed(1)})"`;
    h.agregar(gen.rectangle(p.x - w / 2, p.y - al / 2, w, al, h.op({ stroke: SIENA, strokeWidth: 0.85, roughness: 0.5, fill: PAPEL, fillStyle: 'solid' })), giro);
    if (al > p.r) h.linea(p.x - w / 2 + 2, p.y, p.x + w / 2 - 2, p.y, { stroke: SIENA, strokeWidth: 0.5, roughness: 0.2 }, giro);
  }, 3.6, 6.8);
  h.monton(cols[2], base, 76, 74, p => h.piedra(p.x, p.y, p.r, SIENA, PAPEL, true), 3, 7);

  const nombres = [['«montaña de piedras» (9)', 'de los comunarios'], ['«montón de papeles', 'y libracos» (103)', 'del tinterillo'],
    ['desmonte (140)', 'de la compañía']];
  nombres.forEach((n, i) => {
    const lineas = n.slice(0, -1);
    h.texto(cols[i], base + 17, lineas, { ancla: 'middle', color: SIENA, interlinea: 13.5 });
    h.texto(cols[i], base + 17 + lineas.length * 13.5, n[n.length - 1], { ancla: 'middle', color: GRIS, tam: 12.5 });
  });

  // --- Quién queda debajo en cada lugar. ---
  const debajo = [
    ['debajo, Melchora Mamani:', '«amontonó piedras', 'sobre el cadáver» (35)'],
    ['debajo, dos guaguas:', '«bajo el suelo', 'del pesebre» (106)'],
    ['debajo, Juan Condori:', '«un informe montón de rocas,', 'lodo y maderos astillados» (154)']];
  debajo.forEach((s, i) => {
    h.linea(cols[i] - 80, 356, cols[i] + 80, 356, { strokeWidth: 0.7, stroke: GRIS, roughness: 0.5 });
    h.texto(cols[i], 373, s, { ancla: 'middle', tam: 13, interlinea: 14.5 });
  });

  return h.svg('Figura 8. Tres montones: piedra, papel y máquina');
}

for (const [nombre, hacer] of [['fig7_memoria_retorno.svg', figura7], ['fig8_tres_montones.svg', figura8]]) {
  fs.writeFileSync(path.join(DIR, nombre), hacer(), 'utf8');
  console.log('escrito', nombre);
}
