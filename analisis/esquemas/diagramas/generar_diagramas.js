/*
 * Genera los diagramas de las figuras 7 y 8 como notaciones: línea fina,
 * órbitas, escritura pequeña pegada a las líneas, una leyenda al margen y
 * pocas masas de materia (tierra siena, alquitrán, pan de oro, papel,
 * grafito, hoja de plata). El lenguaje sale de las referencias del autor
 * (analisis/21_diagramas_como_notaciones.md).
 *
 * Uso (desde la raíz del repositorio):
 *     node analisis/esquemas/diagramas/generar_diagramas.js
 *
 * Escribe en esta carpeta fig7_memoria_retorno.svg y fig8_tres_montones.svg,
 * que `python3 articulo/generar_figuras.py` pasa a figura_7.png y
 * figura_8.png. También escribe en ../guias/ las mismas notaciones sin texto,
 * como guías para GPT Image 2; `python3 analisis/esquemas/guias/generar_guias.py`
 * las pasa a PNG.
 *
 * La letra es Nothing You Could Do (SIL Open Font License, fuentes/),
 * incrustada en cada SVG. Las semillas son fijas: el mismo código da siempre
 * el mismo dibujo. Para cambiar un rótulo, edítalo aquí y vuelve a correr.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const FUENTE = fs.readFileSync(path.join(DIR, 'fuentes', 'NothingYouCouldDo-sub.ttf')).toString('base64');

// Papel y línea, como en las referencias: blanco, grafito y tinta.
const PAPEL = '#fcfbf7';
const GRAFITO = '#4a4440';
const CLARO = '#9a938c';
const TINTA = '#2b2623';
// Materias (paleta matérica de analisis/17, §17.3, y analisis/20, §20.3).
const SIENA = '#b0623a';
const SIENA_OSCURA = '#7a3a1d';
const ALQUITRAN = '#211b18';
const HUESO = '#efe7d6';
const ORO = '#d6b25c';
const PLATA = '#d8dce0';
const MARFIL = '#f1e9d6';
const MARFIL_BORDE = '#a59a8a';
const PLOMIZO = '#a7a19a';
const LANA = '#7b5d48';
const LODO = '#6f5a47';
const PAJA = '#c3a660';
const NEGRO = '#151211';

const f = n => Number(n.toFixed(2));

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

// Curva suave que pasa por los puntos (Catmull-Rom convertida a Bézier).
function suave(p, cerrada) {
  const n = p.length;
  const at = i => (cerrada ? p[(i + n) % n] : p[Math.max(0, Math.min(n - 1, i))]);
  let d = `M${f(p[0][0])},${f(p[0][1])}`;
  for (let i = 0; i < (cerrada ? n : n - 1); i++) {
    const [p0, p1, p2, p3] = [at(i - 1), at(i), at(i + 1), at(i + 2)];
    d += ` C${f(p1[0] + (p2[0] - p0[0]) / 6)},${f(p1[1] + (p2[1] - p0[1]) / 6)}` +
      ` ${f(p2[0] - (p3[0] - p1[0]) / 6)},${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])},${f(p2[1])}`;
  }
  return d + (cerrada ? ' Z' : '');
}

function dentro(px, py, poli) {
  let c = false;
  for (let i = 0, j = poli.length - 1; i < poli.length; j = i++) {
    const [xi, yi] = poli[i], [xj, yj] = poli[j];
    if ((yi > py) !== (yj > py) && px < ((xj - xi) * (py - yi)) / (yj - yi) + xi) c = !c;
  }
  return c;
}

const FILTROS = `
    <filter id="desplaza" x="-8%" y="-8%" width="116%" height="116%">
      <feTurbulence type="fractalNoise" baseFrequency="0.028" numOctaves="3" seed="4" result="r"/>
      <feDisplacementMap in="SourceGraphic" in2="r" scale="5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="difumina" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="0.9"/></filter>
    <filter id="grano" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="9" result="n"/>
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 3.2 -1.5" result="m"/>
      <feComposite in="SourceGraphic" in2="m" operator="in"/>
    </filter>
    <filter id="hoja" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.16 0.45" numOctaves="3" seed="21" result="t"/>
      <feDiffuseLighting in="t" surfaceScale="2.6" lighting-color="#ffffff" diffuseConstant="1.15" result="luz">
        <feDistantLight azimuth="235" elevation="50"/>
      </feDiffuseLighting>
      <feComposite in="luz" in2="SourceAlpha" operator="in" result="luz2"/>
      <feBlend in="SourceGraphic" in2="luz2" mode="multiply" result="b"/>
      <feComposite in="b" in2="SourceAlpha" operator="in"/>
    </filter>`;

class Hoja {
  constructor(ancho, alto, semilla, etiqueta, guia) {
    this.ancho = ancho;
    this.alto = alto;
    this.rnd = azar(semilla);
    this.etiqueta = etiqueta;
    this.guia = !!guia;
    this.capas = [];
  }

  add(s) { this.capas.push(s); }

  // Recta trazada con regla: apenas se curva.
  linea(x1, y1, x2, y2, o) {
    o = o || {};
    const len = Math.hypot(x2 - x1, y2 - y1);
    const b = (this.rnd() - 0.5) * Math.min(1.4, len * 0.004);
    const mx = (x1 + x2) / 2 - ((y2 - y1) / (len || 1)) * b, my = (y1 + y2) / 2 + ((x2 - x1) / (len || 1)) * b;
    const dash = o.dash ? ` stroke-dasharray="${o.dash}"` : '';
    this.add(`<path d="M${f(x1)},${f(y1)} Q${f(mx)},${f(my)} ${f(x2)},${f(y2)}" fill="none" stroke="${o.c || GRAFITO}"` +
      ` stroke-width="${o.w || 0.6}" stroke-linecap="round"${dash}${o.op ? ` opacity="${o.op}"` : ''}/>`);
  }

  // Punta de flecha pequeña y llena, o una «x», como en las notaciones.
  punta(x, y, ang, o) {
    o = o || {};
    if (o.x) {
      const s = 2.4;
      this.linea(x - s, y - s, x + s, y + s, { w: 0.6, c: o.c });
      this.linea(x - s, y + s, x + s, y - s, { w: 0.6, c: o.c });
      return;
    }
    const l = o.l || 5.5, a = 0.32;
    const p1 = [x - l * Math.cos(ang - a), y - l * Math.sin(ang - a)];
    const p2 = [x - l * Math.cos(ang + a), y - l * Math.sin(ang + a)];
    this.add(`<path d="M${f(x)},${f(y)} L${f(p1[0])},${f(p1[1])} L${f(p2[0])},${f(p2[1])} Z" fill="${o.c || GRAFITO}"/>`);
  }

  flecha(x1, y1, x2, y2, o) {
    o = o || {};
    this.linea(x1, y1, x2, y2, o);
    this.punta(x2, y2, Math.atan2(y2 - y1, x2 - x1), o);
  }

  curva(p, o) {
    o = o || {};
    const dash = o.dash ? ` stroke-dasharray="${o.dash}"` : '';
    this.add(`<path d="${suave(p, o.cerrada)}" fill="none" stroke="${o.c || GRAFITO}" stroke-width="${o.w || 0.6}"` +
      ` stroke-linecap="round"${dash}${o.op ? ` opacity="${o.op}"` : ''}/>`);
    if (o.punta) {
      const [a, b] = [p[p.length - 2], p[p.length - 1]];
      this.punta(b[0], b[1], Math.atan2(b[1] - a[1], b[0] - a[0]), { c: o.c });
    }
  }

  // Elipse a mano alzada: no cierra del todo y el final se monta un poco.
  orbita(cx, cy, rx, ry, o) {
    o = o || {};
    const giro = o.giro || 0, a0 = o.desde !== undefined ? o.desde : this.rnd() * 6.28, barrido = o.barrido || 6.55;
    const f1 = this.rnd() * 6.28, f2 = this.rnd() * 6.28, pts = [];
    for (let i = 0; i <= 96; i++) {
      const t = a0 + (barrido * i) / 96;
      const r = 1 + 0.018 * Math.sin(2 * t + f1) + 0.012 * Math.sin(3 * t + f2) + 0.03 * (i / 96);
      const ex = rx * r * Math.cos(t), ey = ry * r * Math.sin(t);
      pts.push([cx + ex * Math.cos(giro) - ey * Math.sin(giro), cy + ex * Math.sin(giro) + ey * Math.cos(giro)]);
    }
    this.curva(pts, { c: o.c || CLARO, w: o.w || 0.55, dash: o.dash });
    if (o.flecha !== undefined) {
      const k = Math.round(o.flecha * 96);
      const [a, b] = [pts[Math.max(0, k - 1)], pts[k]];
      this.punta(b[0], b[1], Math.atan2(b[1] - a[1], b[0] - a[0]), { c: o.c || CLARO, l: 4.5 });
    }
  }

  texto(x, y, cadena, o) {
    if (this.guia) return;  // las guías no llevan texto: el modelo lo copiaría
    o = o || {};
    const t = o.t || 12.5, il = o.il || t * 1.18;
    const giro = o.giro ? ` transform="rotate(${o.giro} ${f(x)} ${f(y)})"` : '';
    const sub = o.sub ? ' text-decoration="underline"' : '';
    const sp = o.esp ? ` letter-spacing="${o.esp}"` : '';
    (Array.isArray(cadena) ? cadena : [cadena]).forEach((l, i) => {
      this.add(`<text x="${f(x)}" y="${f(y + i * il)}" font-size="${t}" fill="${o.c || TINTA}" text-anchor="${o.ancla || 'start'}"${sub}${sp}${giro}>${esc(l)}</text>`);
    });
  }

  // Mancha de acuarela: capa traslúcida, borde que se acumula y grano del pigmento.
  acuarela(poli, color, oscuro, o) {
    o = o || {};
    const d = suave(poli, true);
    this.add(`<g filter="url(#desplaza)">` +
      `<path d="${d}" fill="${color}" fill-opacity="${o.op || 0.5}"/>` +
      `<path d="${d}" fill="none" stroke="${oscuro}" stroke-opacity="${o.borde || 0.42}" stroke-width="1.8" filter="url(#difumina)"/>` +
      `<path d="${d}" fill="${oscuro}" fill-opacity="${o.grano || 0.55}" filter="url(#grano)"/></g>`);
  }

  // Hoja de metal (oro, plata): plana, recortada, con arrugas finas.
  hojaMetal(poli, color, borde) {
    const d = suave(poli, true);
    this.add(`<path d="${d}" fill="${color}" filter="url(#hoja)"/>`);
    this.add(`<path d="${d}" fill="none" stroke="${borde}" stroke-width="0.4" opacity="0.7"/>`);
  }

  // Forma irregular alrededor de un centro (piedra, fragmento).
  forma(cx, cy, r, o) {
    o = o || {};
    const n = o.lados || (o.anguloso ? 4 + Math.floor(this.rnd() * 2) : 7), g = this.rnd() * 6.28, p = [];
    for (let i = 0; i < n; i++) {
      const a = g + (i / n) * 6.28 + (this.rnd() - 0.5) * 0.5;
      const rr = r * (o.anguloso ? 0.55 + this.rnd() * 0.6 : 0.78 + this.rnd() * 0.32);
      p.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a) * (o.aplana || 0.75)]);
    }
    const d = o.anguloso ? 'M' + p.map(q => `${f(q[0])},${f(q[1])}`).join(' L') + ' Z' : suave(p, true);
    this.add(`<path d="${d}" fill="${o.relleno || 'none'}" stroke="${o.c || GRAFITO}" stroke-width="${o.w || 0.5}"${o.op ? ` opacity="${o.op}"` : ''}/>`);
  }

  // Coloca piezas que no se enciman dentro de una región.
  empacar(region, caja, rmin, rmax, intentos) {
    const [x0, y0, x1, y1] = caja, hechos = [];
    for (let k = 0; k < intentos; k++) {
      const r = rmin + this.rnd() * (rmax - rmin);
      const x = x0 + this.rnd() * (x1 - x0), y = y0 + this.rnd() * (y1 - y0);
      if (!region(x, y, r)) continue;
      if (hechos.some(h => Math.hypot(h.x - x, h.y - y) < h.r + r + 0.6)) continue;
      hechos.push({ x, y, r });
    }
    return hechos.sort((a, b) => a.y - b.y);
  }

  // Montón: silueta de loma sobre una base.
  monton(cx, base, semi, alto, rmin, rmax, dibujar) {
    const cima = x => base - alto * Math.pow(Math.max(0, 1 - Math.pow((x - cx) / semi, 2)), 0.8);
    const region = (x, y, r) => y + r * 0.6 <= base && y - r * 0.6 >= cima(x) && Math.abs(x - cx) + r <= semi;
    for (const h of this.empacar(region, [cx - semi, base - alto, cx + semi, base], rmin, rmax, 6000)) dibujar(h);
  }

  // Marcas diminutas repetidas, como bandadas.
  marcas(puntos, o) {
    o = o || {};
    for (const [x, y] of puntos) {
      const a = (o.ang !== undefined ? o.ang : this.rnd() * Math.PI) + (this.rnd() - 0.5) * (o.var !== undefined ? o.var : 3.2);
      const l = (o.l || 2.6) * (0.7 + this.rnd() * 0.6);
      this.add(`<path d="M${f(x)},${f(y)} l${f(l * Math.cos(a))},${f(l * Math.sin(a))}" stroke="${o.c || GRAFITO}" stroke-width="${o.w || 0.7}" stroke-linecap="round"/>`);
    }
  }

  svg(titulo) {
    const fuente = this.guia ? '' :
      `<style>@font-face{font-family:'Mano';src:url(data:font/ttf;base64,${FUENTE}) format('truetype');}</style>`;
    // Las guías salen en los tamaños de GPT Image 2: 1536 x 1024 o, si son verticales, 1024 x 1536.
    let caja = [0, 0, this.ancho, this.alto], tam = '';
    if (this.guia) {
      const [PW, PH] = this.alto > this.ancho ? [1024, 1536] : [1536, 1024];
      let W = this.ancho, H = this.alto;
      if (W / H > PW / PH) H = (W * PH) / PW; else W = (H * PW) / PH;
      caja = [f((this.ancho - W) / 2), f((this.alto - H) / 2), f(W), f(H)];
      tam = ` width="${PW}" height="${PH}"`;
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${caja.join(' ')}"${tam} role="img"` +
      ` aria-label="${esc(this.etiqueta)}" font-family="Mano, 'Segoe Script', cursive">\n` +
      `  <title>${esc(titulo)}</title>\n  <defs>${fuente}${FILTROS}\n  </defs>\n` +
      `  <rect x="${caja[0]}" y="${caja[1]}" width="${caja[2]}" height="${caja[3]}" fill="${PAPEL}"/>\n  ` +
      this.capas.join('\n  ') + '\n</svg>\n';
  }
}

/* ------------------------------------------------------------------ */
/* Figura 7. La memoria del retorno (pp. 156-157)                      */
/* La línea de la mirada es también la del tiempo: lo cercano es el    */
/* hambre; lo lejano, lo pasado antiguo.                               */
/* ------------------------------------------------------------------ */
/* Figura 7. La memoria del retorno (pp. 156-157)                      */
/* La línea de la mirada es también la del tiempo: lo cercano es el    */
/* hambre; lo lejano, lo pasado antiguo.                               */
/* ------------------------------------------------------------------ */
function figura7(guia) {
  const h = new Hoja(700, 450, 7203,
    'Notación de la memoria del retorno: desde la atalaya, la mirada, que es también la línea del tiempo, pasa por encima ' +
    'de la muralla y del foso y llega al horizonte dorado de lo pasado antiguo. La muralla es una banda de tierra siena: ' +
    'sus caras son los apellidos que vuelven y su relleno, la legión sin tierra. En el foso de alquitrán, raspados, los muertos del hambre.',
    guia);
  const ojo = [98, 122], suelo = 336;

  // Construcción: proyecciones verticales desde la línea del tiempo.
  h.linea(612, ojo[1] + 4, 612, suelo + 2, { c: CLARO, w: 0.4, dash: '1.5 4' });

  // El suelo, una línea sola, que se abre en el foso.
  h.curva([[22, suelo + 1], [70, suelo - 1], [130, suelo + 1], [196, suelo], [270, suelo + 1], [334, suelo]], { w: 0.7 });
  h.curva([[560, suelo], [600, suelo - 1], [650, suelo + 1], [690, suelo]], { w: 0.7 });

  // El foso «hondo y alquitranado» (p. 157): una mancha plana, como un desgarro.
  const foso = [[334, suelo], [339, 349], [352, 362], [368, 371], [380, 383], [404, 388], [428, 395], [452, 392], [474, 396],
    [498, 388], [516, 380], [532, 367], [546, 356], [552, 345], [560, suelo]];
  h.add(`<g filter="url(#desplaza)"><path d="${suave(foso, true)}" fill="${ALQUITRAN}" fill-opacity="0.92"/>` +
    `<path d="${suave(foso, true)}" fill="none" stroke="${ALQUITRAN}" stroke-width="2" stroke-opacity="0.5" filter="url(#difumina)"/></g>`);
  h.add(`<ellipse cx="436" cy="347" rx="70" ry="2.6" fill="#9b928a" opacity="0.18" filter="url(#difumina)"/>`);
  // El foso como un lugar: una órbita a ras del suelo.
  h.orbita(447, suelo + 20, 146, 28, { flecha: 0.55 });
  // Más de ciento cincuenta marcas raspadas hasta el papel (p. 156).
  const muertos = [];
  while (muertos.length < 152) {
    const x = 340 + h.rnd() * 216, y = suelo + 4 + h.rnd() * 58;
    if (dentro(x, y, foso) && dentro(x + 3, y + 3, foso) && dentro(x - 3, y - 3, foso)) muertos.push([x, y]);
  }
  h.marcas(muertos, { c: HUESO, w: 0.75, l: 2.4 });
  h.flecha(392, 380, 380, 404, { c: CLARO, w: 0.4 });
  h.texto(300, 414, ['más de ciento cincuenta muertos,', '«sin culto y sin recuerdo» (156)'], { t: 11.5, c: GRAFITO });
  // Quispe, «en muchos sitios» (p. 69): cinco grupos dispersos con líneas que convergen fuera.
  const quispe = [[360, 352], [412, 380], [458, 360], [500, 382], [536, 356]];
  for (const [x, y] of quispe) {
    h.marcas([[x, y], [x + 3, y - 2], [x - 2, y + 2]], { c: '#fbf4e6', w: 0.95, l: 2.2 });
    h.linea(x, y, 608, 392, { c: CLARO, w: 0.4 });
  }
  h.punta(608, 392, 0, { c: CLARO, x: true });
  h.texto(616, 384, ['Quispe:', '«en muchos', 'sitios» (69)'], { t: 11.5, c: GRAFITO });
  // Condori, en el cementerio de los mineros (p. 154).
  h.marcas([[486, 378]], { c: '#fbf4e6', w: 1.1, l: 3.6, ang: 0.3, var: 0 });
  h.flecha(486, 381, 548, 432, { c: CLARO, w: 0.4 });
  h.texto(690, 444, 'Condori, en el cementerio de los mineros (154)', { t: 11.5, ancla: 'end', c: GRAFITO });

  // La muralla de su visión (pp. 156-157): una pirca de doble cara en sección. Su borde
  // superior queda en la línea que va del ojo al borde lejano del foso: lo tapa.
  const izq = yy => 250 + (suelo - yy) * 0.1, der = yy => 318 - (suelo - yy) * 0.11;
  const muro = [];
  for (let yy = suelo; yy >= 206; yy -= 13) muro.push([izq(yy), yy]);
  muro.push([izq(200) + 6, 198], [(izq(200) + der(200)) / 2, 196], [der(200) - 6, 198]);
  for (let yy = 206; yy <= suelo; yy += 13) muro.push([der(yy), yy]);
  h.acuarela(muro, SIENA, SIENA_OSCURA, { op: 0.44 });
  // El relleno: la «legión» de piedrecilla menuda (pp. 8, 22).
  const granos = [];
  for (let k = 0; k < 3000 && granos.length < 300; k++) {
    const x = 250 + h.rnd() * 70, yy = 198 + h.rnd() * 140;
    if (dentro(x, yy, muro) && dentro(x - 6, yy, muro) && dentro(x + 6, yy, muro)) granos.push([x, yy]);
  }
  for (const [x, yy] of granos) h.add(`<circle cx="${f(x)}" cy="${f(yy)}" r="${f(0.45 + h.rnd() * 0.8)}" fill="${SIENA_OSCURA}" opacity="0.75"/>`);
  // Las dos caras. La que mira a la atalaya está hecha de apellidos, uno por hilada (p. 156);
  // la que da al foso, de piedras sin nombre.
  h.curva([[izq(suelo), suelo], [izq(270), 270], [izq(206), 206], [izq(200) + 6, 198]], { w: 0.6 });
  const apellidos = ['Villca', 'Huanca', 'Huallpa', 'Yupanqui', 'Ticona', 'Choque', 'Chuquihuanca'];
  apellidos.forEach((a, k) => {
    const yy = 214 + k * 17.5;
    h.linea(izq(yy) - 1, yy + 2.5, izq(yy) - 13, yy + 2.5, { c: CLARO, w: 0.4 });
    h.texto(izq(yy) - 16, yy + 6, a, { t: 11, ancla: 'end' });
  });
  const arcos = [];
  for (let yy = suelo; yy >= 204; yy -= 7) arcos.push([der(yy) + (Math.round(yy / 7) % 2 ? 2.4 : 0), yy]);
  h.curva(arcos, { w: 0.55 });
  h.texto(232, 186, '«muralla de su visión» (156-157)', { t: 12.5, giro: -4 });
  // Líneas de mira: del ojo, rozando la muralla, a los dos bordes del foso. Lo que queda debajo no se ve.
  h.linea(ojo[0] + 2, ojo[1] + 2, 560, suelo, { c: CLARO, w: 0.4, dash: '1 3' });
  h.linea(ojo[0] + 2, ojo[1] + 2, 334, suelo - 2, { c: CLARO, w: 0.4, dash: '1 3' });
  // Rótulos que salen hacia los márgenes, con la palabra en la punta.
  h.flecha(290, 262, 326, 246, { c: SIENA_OSCURA, w: 0.45 });
  h.texto(330, 244, ['relleno: la «legión» sin tierra,', 'Condori, Mamani, Quispe (22),', 'y tres vigilantes (75)'], { t: 11, c: SIENA_OSCURA });
  h.flecha(200, 328, 168, 378, { c: GRAFITO, w: 0.45 });
  h.texto(24, 392, ['caras: los apellidos que vuelven (156);', 'faltan los de la «legión» sin tierra (22)'], { t: 11.5 });

  // La atalaya de la esperanza (p. 157): un eje con niveles, y arriba los que miran.
  h.linea(ojo[0], suelo, ojo[0], ojo[1] + 8, { w: 0.7 });
  for (const [y, rx] of [[302, 24], [262, 21], [222, 18], [182, 15]]) h.orbita(ojo[0], y, rx, 5, { giro: -0.05 });
  const gente = [];
  for (let i = 0; i < 9; i++) gente.push([ojo[0] - 13 + i * 3.1 + (h.rnd() - 0.5), ojo[1] + 5 + (h.rnd() - 0.5) * 2]);
  h.marcas(gente, { ang: -Math.PI / 2, var: 0.25, l: 5.5, w: 0.8, c: TINTA });
  h.texto(62, 330, '«atalaya de la esperanza» (157)', { t: 12, giro: -90 });

  // La mirada, que es también el tiempo.
  h.flecha(ojo[0] + 16, ojo[1], 676, ojo[1], { w: 0.6, dash: '6 3.5' });
  h.texto(330, ojo[1] - 8, '«sólo miraban el horizonte» (157)', { t: 12.5, ancla: 'middle' });
  for (const [x, rot] of [[122, 'ahora'], [446, 'el hambre'], [612, 'antes del hambre']]) {
    h.linea(x - 3, ojo[1] - 3, x + 3, ojo[1] + 3, { w: 0.6, c: TINTA });
    h.linea(x - 3, ojo[1] + 3, x + 3, ojo[1] - 3, { w: 0.6, c: TINTA });
    h.texto(x, ojo[1] + 15, rot, { t: 11, ancla: 'middle', c: CLARO });
  }
  h.texto(684, ojo[1] + 10, 'TIEMPO', { t: 11, c: CLARO, esp: 1.2, giro: 90 });
  // El horizonte: una tira delgada de pan de oro, «lo pasado antiguo» (p. 156).
  h.hojaMetal([[546, ojo[1] - 1.8], [570, ojo[1] - 2.6], [612, ojo[1] - 1.6], [648, ojo[1] - 2.4], [673, ojo[1] - 1.2], [671, ojo[1] + 2.2],
    [640, ojo[1] + 2.6], [600, ojo[1] + 1.8], [566, ojo[1] + 2.4], [548, ojo[1] + 1.6]], ORO, '#8a6a2a');
  h.texto(676, ojo[1] - 44, ['horizonte: «lo pasado antiguo,', 'lo bueno y lo alegre de las cosechas» (156)'], { t: 12, ancla: 'end' });

  // La mirada que no baja.
  h.linea(446, ojo[1] + 6, 446, 214, { w: 0.6, dash: '1.5 3', c: TINTA });
  h.linea(438, 218, 454, 218, { w: 1, c: TINTA });
  h.texto(458, 170, ['«sin atreverse a bajar la cabeza', 'al tremendo hoyo» (157)'], { t: 11.5 });
  h.texto(330, 300, ['foso «hondo y alquitranado»:', 'el intervalo del hambre (157)'], { t: 11.5 });
  h.flecha(456, 306, 468, 342, { w: 0.45 });

  // Leyenda, al margen y con corchete.
  h.linea(22, 34, 22, 98, { w: 0.5, c: CLARO });
  h.texto(30, 42, ['( ) páginas de Altiplano (1982 [1945])', '- - - la mirada, que es también el tiempo',
    'siena: la tierra del relleno', 'negro: el alquitrán del foso', 'oro: lo pasado antiguo'], { t: 11, c: GRAFITO, il: 13.6 });

  return h.svg('Figura 7. La memoria del retorno');
}

/* ------------------------------------------------------------------ */
/* Figura 8. Tres montones: la novela leída de la p. 9 a la p. 154     */
/* El eje vertical son las páginas; los montones bajan por él, de la   */
/* «altura del cerro» (p. 9) al «informe montón» (p. 154). El eje se   */
/* corta entre las pp. 40 y 80, donde no hay montones.                 */
/* ------------------------------------------------------------------ */
function figura8(guia) {
  const h = new Hoja(560, 790, 8203,
    'Notación vertical: el eje es la novela leída de la página 9 a la 154. Tres montones bajan por él, unidos por una espiral: ' +
    'la montaña de piedras del ayllu, el montón de papeles de la aldea y el desmonte de la mina. La montaña que debía ' +
    'sobrepasar la altura del cerro termina en el montón que sepulta a Juan Condori.',
    guia);
  const X = 280;
  const y = p => (p <= 40 ? 120 + 4.2 * p : 318 + 5 * (p - 80));

  // El eje: las páginas de la novela, con una marca cada diez y un corte.
  h.linea(X, 96, X, y(40) + 6, { c: CLARO, w: 0.55 });
  h.linea(X - 5, y(40) + 10, X + 5, y(40) + 6, { c: CLARO, w: 0.55 });
  h.linea(X - 5, y(80) - 6, X + 5, y(80) - 10, { c: CLARO, w: 0.55 });
  h.flecha(X, y(80) - 8, X, 752, { c: CLARO, w: 0.55 });
  for (const p of [10, 20, 30, 40, 80, 90, 100, 110, 120, 130, 140, 150]) {
    h.linea(X - 3, y(p), X + 3, y(p), { c: CLARO, w: 0.5 });
    h.texto(X - 6, y(p) + 3, String(p), { t: 8.5, ancla: 'end', c: CLARO });
  }
  h.texto(X + 6, 104, 'Altiplano, p.', { t: 10.5, c: CLARO });
  // La altura del cerro, que la montaña debía sobrepasar (p. 9).
  h.linea(36, 64, 524, 64, { c: GRAFITO, w: 0.6, dash: '1.5 3.5' });
  h.texto(280, 56, '«quizá un día la montaña de piedras sobrepase la altura del cerro» (9)', { t: 11.5, ancla: 'middle' });

  // Capítulos al margen derecho, con su corchete.
  for (const [p0, p1, rot] of [[6, 38, 'PIEDRA · el ayllu (6-38)'], [83, 107, 'PAPEL · la aldea (83-107)'], [134, 154, 'MÁQUINA · la mina (134-154)']]) {
    h.linea(536, y(p0), 536, y(p1), { c: GRAFITO, w: 0.5 });
    h.linea(532, y(p0), 536, y(p0), { c: GRAFITO, w: 0.5 });
    h.linea(532, y(p1), 536, y(p1), { c: GRAFITO, w: 0.5 });
    h.texto(544, (y(p0) + y(p1)) / 2, rot, { t: 11, ancla: 'middle', giro: 90, esp: 0.6 });
  }

  // La espiral: el mismo gesto, que baja por los tres montones.
  h.curva([[56, 116], [190, 128], [372, 142], [414, 172], [380, 200], [200, 206], [120, 232], [140, 300], [300, 352],
    [440, 404], [420, 452], [300, 468], [150, 474], [126, 520], [210, 566], [400, 588], [434, 624], [380, 664], [306, 696]],
  { c: CLARO, w: 0.55, punta: true });
  h.texto(60, 112, 'el mismo gesto: amontonar', { t: 11.5, c: GRAFITO, giro: 4 });

  // --- Piedra: el ayllu (p. 9). ---
  const b1 = y(9) + 32;
  const loma1 = [];
  for (let i = 0; i <= 16; i++) {
    const t = i / 16, x = X - 78 + 156 * t;
    loma1.push([x, b1 - 48 * Math.pow(Math.max(0, 1 - Math.pow(2 * t - 1, 2)), 0.8) + (h.rnd() - 0.5) * 2]);
  }
  h.acuarela(loma1.concat([[X + 78, b1 + 1], [X - 78, b1 + 1]]), SIENA, SIENA_OSCURA, { op: 0.32, grano: 0.45 });
  h.monton(X, b1, 74, 46, 1.4, 3, p => h.forma(p.x, p.y, p.r, { relleno: '#d9a989', c: SIENA_OSCURA, w: 0.35 }));
  h.orbita(X, b1 - 16, 110, 15, { flecha: 0.62 });
  h.orbita(X, b1 - 14, 94, 11, {});
  // Del erial al montón: una bandada de piedritas.
  for (let i = 0; i < 46; i++) {
    const t = i / 45, x = 30 + t * 172 + (h.rnd() - 0.5) * 8, yy = 196 - Math.sin(t * Math.PI) * 50 + t * 6 + (h.rnd() - 0.5) * 8;
    h.forma(x, yy, 0.8 + t * 1.3, { relleno: '#d9a989', c: SIENA_OSCURA, w: 0.3 });
  }
  h.texto(26, 214, ['erial de piedras: «extraen piedras', 'y las amontonan» (9)'], { t: 11 });
  h.flecha(326, b1 - 46, 368, 72, { dash: '4 3', w: 0.55 });
  h.texto(374, 86, '«tierra rescatada» (9)', { t: 11.5 });
  h.texto(372, b1 + 12, ['«montaña de piedras» (9)', 'de los comunarios'], { t: 11.5, c: SIENA_OSCURA });
  // Debajo, Melchora Mamani (p. 35).
  const m = y(35);
  for (const [dx, dy, r] of [[-8, 0, 2.6], [-3, -2, 2.4], [2, 0, 2.6], [7, 0.5, 2.3], [-5, -5, 2.2], [1, -5, 2.4], [-2, -9, 2]]) {
    h.forma(X - 52 + dx, m + dy, r, { relleno: PAPEL, w: 0.5 });
  }
  h.linea(X - 54, m - 18, X - 54, m - 11, { c: PAJA, w: 1 });
  h.linea(X - 57, m - 15.5, X - 51, m - 15.5, { c: PAJA, w: 1 });
  h.linea(X - 40, m - 2, X - 4, m, { c: CLARO, w: 0.4 });
  h.texto(X + 10, m - 4, ['debajo, Melchora Mamani:', '«amontonó piedras sobre el cadáver»;', 'una «crucecita de paja» (35)'], { t: 11 });

  // --- Papel: la aldea (pp. 92-106). ---
  const rc = [168, y(92)];
  h.orbita(rc[0], rc[1], 26, 26, { c: GRAFITO, w: 0.55, barrido: 6.4 });
  h.add(`<circle cx="${rc[0]}" cy="${f(rc[1])}" r="1.4" fill="${GRAFITO}"/>`);
  h.linea(rc[0], rc[1], rc[0] + 25, rc[1] - 6, { c: CLARO, w: 0.4 });
  for (const [dx, dy, s] of [[-11, -8, 1], [4, -12, -1], [-13, 6, 1], [3, 8, -1], [12, -1, 1]]) {
    const ax = rc[0] + dx, ay = rc[1] + dy;
    h.add(`<ellipse cx="${f(ax)}" cy="${f(ay)}" rx="4.2" ry="2.3" fill="${LANA}"/>` +
      `<ellipse cx="${f(ax + s * 4)}" cy="${f(ay - 1.5)}" rx="1.5" ry="1.2" fill="${LANA}"/>`);
    for (const px of [-2.5, -0.9, 0.9, 2.5]) h.linea(ax + px, ay + 1.5, ax + px, ay + 3.8, { c: LANA, w: 0.5 });
  }
  h.texto(rc[0], rc[1] - 46, ['radio urbano:', 'ordenanza y firma (96)'], { t: 11, ancla: 'middle' });
  // El embudo, en perspectiva (p. 102), a un lado del eje.
  const fx = 386, fy = y(95);
  h.orbita(fx, fy, 22, 5.5, { c: GRAFITO, w: 0.6, barrido: 6.35, desde: 0.3 });
  h.curva([[fx - 22, fy], [fx - 10, fy + 14], [fx - 3, fy + 24], [fx - 3, fy + 32]], { w: 0.6 });
  h.curva([[fx + 22, fy], [fx + 10, fy + 14], [fx + 3, fy + 24], [fx + 3, fy + 32]], { w: 0.6 });
  h.flecha(rc[0] + 28, rc[1], fx - 26, fy - 1, { w: 0.5 });
  h.texto(fx + 28, fy - 6, '«embudo» (102)', { t: 11.5 });
  h.flecha(fx + 24, fy + 4, 524, fy + 16, { w: 0.45, c: GRAFITO });
  h.texto(524, fy + 34, ['«hasta esfumarse»:', 'propiedades del Alcalde (102)'], { t: 11, ancla: 'end' });
  // Del embudo caen billetes al montón de papeles.
  for (const [x, yy, a] of [[380, fy + 40, 14], [368, fy + 47, -20], [354, fy + 53, 8], [341, fy + 58, -10]]) {
    h.add(`<rect x="${f(x - 4)}" y="${f(yy - 2.4)}" width="8" height="4.8" fill="${MARFIL}" stroke="${MARFIL_BORDE}"` +
      ` stroke-width="0.4" transform="rotate(${a} ${f(x)} ${f(yy)})"/>`);
  }
  h.texto(398, fy + 70, ['«mil seiscientos bolivianos', 'en papel» (103),', 'para el tinterillo (105)'], { t: 11 });
  const b2 = y(103) + 22;
  h.monton(X, b2, 70, 40, 2.6, 5.2, p => {
    const ang = (h.rnd() - 0.5) * 44, w = p.r * 2.3, al = p.r * (h.rnd() < 0.2 ? 1.3 : 0.85);
    h.add(`<rect x="${f(p.x - w / 2)}" y="${f(p.y - al / 2)}" width="${f(w)}" height="${f(al)}" fill="${MARFIL}"` +
      ` stroke="${MARFIL_BORDE}" stroke-width="0.4" transform="rotate(${f(ang)} ${f(p.x)} ${f(p.y)})"/>`);
  });
  h.orbita(X, b2 - 15, 104, 14, { flecha: 0.3 });
  h.orbita(X, b2 - 13, 88, 10, {});
  h.texto(176, b2 - 30, ['«montón de papeles', 'y libracos» (103),', 'del tinterillo'], { t: 11.5, ancla: 'end', c: '#6d6152' });
  // Debajo, dos guaguas (p. 106).
  const g = y(106);
  h.linea(X - 3, g, X + 3, g, { c: TINTA, w: 0.8 });
  h.linea(X - 4, g + 1, X - 60, b2 + 20, { c: CLARO, w: 0.4 });
  h.texto(X - 64, b2 + 26, ['debajo, dos guaguas:', '«bajo el suelo del pesebre» (106)'], { t: 11, ancla: 'end' });

  // --- Máquina: la mina (pp. 134-154). ---
  const gm = y(136);
  // El castillete, una silueta negra (pp. 134-135).
  h.add(`<path d="M${X - 15},${f(gm)} L${X - 3},${f(gm - 50)} L${X + 3},${f(gm - 50)} L${X + 15},${f(gm)} L${X + 10},${f(gm)} L${X},${f(gm - 41)}` +
    ` L${X - 10},${f(gm)} Z" fill="${NEGRO}"/>`);
  h.add(`<rect x="${X - 10}" y="${f(gm - 20)}" width="20" height="2" fill="${NEGRO}"/>` +
    `<circle cx="${X}" cy="${f(gm - 53)}" r="6" fill="${NEGRO}"/><circle cx="${X}" cy="${f(gm - 53)}" r="1.5" fill="${PAPEL}"/>`);
  h.orbita(X - 20, gm - 4, 126, 15, { flecha: 0.8 });
  // El pique y la jaula; la doble flecha de subir y bajar.
  h.linea(X - 5, gm, X - 5, y(154) + 6, { c: NEGRO, w: 0.8 });
  h.linea(X + 5, gm, X + 5, y(154) + 6, { c: NEGRO, w: 0.8 });
  h.add(`<rect x="${X - 3.5}" y="${f(y(143))}" width="7" height="9" fill="${NEGRO}"/>`);
  h.linea(X + 14, y(141), X + 14, y(147), { c: NEGRO, w: 1 });
  h.punta(X + 14, y(141) - 1, -Math.PI / 2, { c: NEGRO, l: 4 });
  h.punta(X + 14, y(147) + 1, Math.PI / 2, { c: NEGRO, l: 4 });
  // El estaño sale como una tira de hoja de plata (p. 142).
  h.hojaMetal([[X + 7, gm - 55.4], [X + 120, gm - 56.2], [X + 236, gm - 55.4], [X + 238, gm - 50.8], [X + 120, gm - 50.2], [X + 7, gm - 50.8]],
    PLATA, '#6f757b');
  h.punta(X + 246, gm - 53, 0, { c: GRAFITO });
  h.texto(X + 242, gm - 80, ['«cosecharás miles de cargas de estaño» (142):', 'para la compañía'], { t: 11.5, ancla: 'end' });
  // El desmonte, roca sin mineral (p. 140).
  h.monton(X - 86, gm, 48, 28, 1.8, 3.8, p => h.forma(p.x, p.y, p.r, { anguloso: true, relleno: PLOMIZO, c: GRAFITO, w: 0.4 }));
  h.texto(X - 86, gm + 14, ['desmonte, roca sin mineral (140),', 'de la compañía'], { t: 11, ancla: 'middle' });
  // Lo que baja: «rieles, maderos, dinamita, hombres» (p. 151). Los hombres, al final.
  const baja = [[150, y(147)], [176, y(148)], [200, y(150)], [224, y(151)], [248, y(152)]];
  baja.forEach(([x, yy], i) => {
    if (i === 0) { h.linea(x - 4, yy - 1, x + 4, yy - 1, { w: 0.6 }); h.linea(x - 4, yy + 1.5, x + 4, yy + 1.5, { w: 0.6 }); }
    else if (i === 1) h.linea(x - 5, yy, x + 5, yy - 1, { w: 1.6, c: '#8a6d4c' });
    else if (i === 2) h.add(`<rect x="${x - 3}" y="${f(yy - 1.4)}" width="6" height="2.8" fill="${SIENA_OSCURA}"/>`);
    else h.marcas([[x - 2, yy + 3], [x + 2, yy + 3]], { ang: -Math.PI / 2, var: 0.2, l: 6, w: 0.8, c: TINTA });
  });
  h.curva([[138, y(147) + 6], [200, y(150) + 6], [248, y(152) + 6], [X - 8, y(152) + 5]], { c: CLARO, w: 0.4, punta: true });
  h.texto(24, y(147), ['«rieles, maderos,', 'dinamita, hombres»', '(151)'], { t: 11 });
  // Debajo del pique, el «informe montón» (p. 154).
  const b3 = y(154) + 22;
  h.add(`<g filter="url(#desplaza)"><path d="${suave([[X - 38, b3], [X - 26, b3 - 12], [X - 6, b3 - 18], [X + 16, b3 - 15], [X + 36, b3 - 4], [X + 40, b3]], true)}"` +
    ` fill="${LODO}" fill-opacity="0.5"/></g>`);
  h.monton(X, b3, 36, 17, 1.6, 3.4, p => h.forma(p.x, p.y, p.r, { anguloso: true, relleno: PLOMIZO, c: GRAFITO, w: 0.4 }));
  for (const [x0, y0, x1, y1] of [[X - 24, b3 - 7, X - 9, b3 - 13], [X + 6, b3 - 12, X + 22, b3 - 5], [X - 6, b3 - 4, X + 9, b3 - 9]]) {
    h.linea(x0, y0, x1, y1, { c: '#8a6d4c', w: 1.4 });
  }
  h.marcas([[X + 1, b3 + 5]], { c: TINTA, w: 1, l: 4, ang: 0, var: 0 });
  h.texto(X + 46, b3 - 18, ['debajo, Juan Condori:', '«un informe montón de rocas,', 'lodo y maderos astillados» (154)'], { t: 11.5 });

  // Leyenda.
  h.linea(22, 754, 22, 778, { w: 0.5, c: CLARO });
  h.texto(30, 762, ['( ) páginas de Altiplano (1982 [1945]); el eje es la novela, leída', 'de la p. 9 a la 154, con un corte entre la 40 y la 80'], { t: 11, c: GRAFITO, il: 13 });

  return h.svg('Figura 8. Tres montones');
}

for (const [nombre, hacer] of [['fig7_memoria_retorno.svg', figura7], ['fig8_tres_montones.svg', figura8]]) {
  fs.writeFileSync(path.join(DIR, nombre), hacer(false), 'utf8');
  console.log('escrito', nombre);
  const guia = path.join(DIR, '..', 'guias', 'guia_' + nombre);
  fs.writeFileSync(guia, hacer(true), 'utf8');
  console.log('escrito', path.relative(DIR, guia));
}
