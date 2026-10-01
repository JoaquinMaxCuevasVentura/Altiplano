/*
 * Genera las ocho figuras del artículo como notaciones: línea fina, órbitas,
 * escritura pequeña pegada a las líneas, una leyenda al margen y pocas masas
 * de materia, cada una del color de lo que es (hollín, siena, pizarra, polvo
 * de la puna, casiterita, copajira, hueso, noche, alquitrán, pan de oro,
 * hoja de plata). El lenguaje sale de las referencias del autor
 * (analisis/21_diagramas_como_notaciones.md); las Figuras 1 a 6, los esquemas
 * de encaje de los pasteles, suman un aparato común: las cuatro funciones del
 * Cuadro 1 como signos, el asterisco para lo que decide el dibujo y las
 * mayúsculas para lo que hace la mano (analisis/23).
 *
 * Uso (desde la raíz del repositorio):
 *     node analisis/esquemas/diagramas/generar_diagramas.js          # las ocho
 *     node analisis/esquemas/diagramas/generar_diagramas.js fig2 fig5 # algunas
 *
 * Escribe en esta carpeta fig1_craneo_nido.svg … fig8_tres_montones.svg, que
 * `python3 articulo/generar_figuras.py` pasa a figura_1.png … figura_8.png.
 * Para las Figuras 7 y 8 también escribe en ../guias/, en los tamaños de
 * GPT Image 2, las mismas notaciones sin texto (guia_*) y con texto
 * (entrada_*), para explorarlas o mejorarlas con ese modelo (analisis/21 y
 * analisis/22); `python3 analisis/esquemas/guias/generar_guias.py` las pasa a
 * PNG y hace las máscaras.
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
// Materias que suman las Figuras 1 a 6 (analisis/17, §17.3).
const HUMO = '#241f1c';          // negro de humo: el hollín de la chujlla
const PAJA_PLOMIZA = '#8d857a';  // ichu con hollín pegado (p. 10)
const BRASA = '#b8502b';         // brasa de boñiga: rojo anaranjado, sin llama
const BARRO = '#a5583a';         // barro cocido de la huaca
const PIZARRA = '#7b8086';       // la planta del catastro
const POLVO_PUNA = '#cbbd9c';    // limo seco de la puna
const VERDE = '#5d7458';         // hoja mojada del yunga
const NIEBLA = '#eef0ef';        // gotas de agua: dispersan toda la luz
const NIEVE_SOMBRA = '#9db0c2';  // la nieve devuelve azul en la sombra
const CASITERITA = '#3a2f28';    // mena de estaño, pardo negruzco
const COPAJIRA = '#c7a23d';      // agua ácida que tiñe la roca de ocre amarillo
const CALAMINA = '#b7babb';      // chapa de zinc
const CARBURO = '#f3e7b3';       // llama de acetileno
const NOCHE = '#1d2027';         // la noche, donde se raspan las estrellas
const SIRIO = '#dde8f3';         // blanco azulado
const LLAMADA = '#b3aa9e';       // línea de llamada que cruza una masa oscura

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
  // modo: 'figura' (la del artículo), 'guia' (sin texto) o 'entrada' (con texto);
  // las dos últimas, en los tamaños de GPT Image 2.
  constructor(ancho, alto, semilla, etiqueta, modo) {
    this.ancho = ancho;
    this.alto = alto;
    this.rnd = azar(semilla);
    this.etiqueta = etiqueta;
    this.sinTexto = modo === 'guia';
    this.gpt = modo === 'guia' || modo === 'entrada';
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
    if (this.sinTexto) return;  // las guías no llevan texto: el modelo lo copiaría
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
    const d = o.recta ? 'M' + poli.map(q => `${f(q[0])},${f(q[1])}`).join(' L') + ' Z' : suave(poli, true);
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

  /* Lo que sigue lo usan las notaciones de las Figuras 1 a 6. */

  // Uno de los cuatro signos del Cuadro 1, donde la línea de llamada toca el dibujo:
  // apoyo, un poste sobre su base; vano, un aro; masa, un punto lleno; límite, dos rayas.
  signo(x, y, tipo, c) {
    c = c || TINTA;
    if (tipo === 'apoyo') {
      this.add(`<path d="M${f(x)},${f(y - 6.5)} V${f(y)} M${f(x - 3.8)},${f(y)} H${f(x + 3.8)}" fill="none" stroke="${c}" stroke-width="0.95" stroke-linecap="round"/>`);
    } else if (tipo === 'vano') {
      this.add(`<circle cx="${f(x)}" cy="${f(y)}" r="2.9" fill="none" stroke="${c}" stroke-width="0.85"/>`);
    } else if (tipo === 'masa') {
      this.add(`<circle cx="${f(x)}" cy="${f(y)}" r="2.8" fill="${c}"/>`);
    } else {
      this.add(`<path d="M${f(x - 4.2)},${f(y - 1.5)} H${f(x + 4.2)} M${f(x - 4.2)},${f(y + 1.5)} H${f(x + 4.2)}" fill="none" stroke="${c}" stroke-width="0.85" stroke-linecap="round"/>`);
    }
  }

  // Línea de llamada de una función: del rótulo al dibujo, con el signo en la punta.
  funcion(tipo, desde, hasta, o) {
    o = o || {};
    this.linea(desde[0], desde[1], hasta[0], hasta[1], { c: o.c || CLARO, w: 0.45 });
    this.signo(hasta[0], hasta[1], tipo, o.cs);
  }

  // Leyenda común de las Figuras 1 a 6; `extra` agrega las líneas de materia de cada una.
  leyenda(x, y, extra, o) {
    o = o || {};
    const lineas = ['( ) páginas de Altiplano (1982 [1945])'];
    if (o.bertonio) lineas.push('[B. ] Bertonio (2011 [1612])');
    lineas.push('* decisión del dibujo, no de la novela', 'MAYÚSCULAS: lo que hace la mano');
    const k = lineas.length, il = 13.6, total = k + 1 + extra.length;
    this.linea(x - 8, y - 8, x - 8, y + (total - 1) * il + 4, { w: 0.5, c: CLARO });
    this.texto(x, y, lineas, { t: 11, c: GRAFITO, il });
    const ys = y + k * il;
    ['apoyo', 'vano', 'masa', 'limite'].forEach((tipo, i) => this.signo(x + 4 + i * 11, ys - 3.5 + (tipo === 'apoyo' ? 3 : 0), tipo, GRAFITO));
    this.texto(x + 50, ys, 'apoyo, vano, masa, límite (Cuadro 1)', { t: 11, c: GRAFITO });
    if (extra.length) this.texto(x, ys + il, extra, { t: 11, c: GRAFITO, il });
  }

  // Cota de arquitecto: una línea con dos rayas oblicuas en los extremos.
  cota(x1, y1, x2, y2, o) {
    o = o || {};
    this.linea(x1, y1, x2, y2, { c: o.c || GRAFITO, w: 0.5 });
    const a = Math.atan2(y2 - y1, x2 - x1) + Math.PI / 4, l = 3.4;
    for (const [x, y] of [[x1, y1], [x2, y2]]) {
      this.linea(x - l * Math.cos(a), y - l * Math.sin(a), x + l * Math.cos(a), y + l * Math.sin(a), { c: o.c || GRAFITO, w: 0.75 });
    }
  }

  // Grieta o raya quebrada: tramos cortos que cambian de rumbo.
  grieta(x, y, ang, largo, o) {
    o = o || {};
    const n = o.n || 5, p = [[x, y]];
    let a = ang;
    for (let i = 0; i < n; i++) {
      a += (this.rnd() - 0.5) * (o.quiebre || 1.3);
      const [px, py] = p[p.length - 1];
      p.push([px + (largo / n) * Math.cos(a), py + (largo / n) * Math.sin(a)]);
    }
    this.add(`<path d="M${p.map(q => `${f(q[0])},${f(q[1])}`).join(' L')}" fill="none" stroke="${o.c || HUESO}"` +
      ` stroke-width="${o.w || 0.8}" stroke-linecap="round" stroke-linejoin="round"${o.op ? ` opacity="${o.op}"` : ''}/>`);
    return p;
  }

  // Chorreo de pigmento disuelto: una línea que baja y termina en gota.
  chorreo(x, y, largo, o) {
    o = o || {};
    const w = o.w || 0.9, dx = (this.rnd() - 0.5) * 1.6;
    this.add(`<path d="M${f(x)},${f(y)} q${f(dx * 0.4)},${f(largo / 2)} ${f(dx)},${f(largo)}" fill="none" stroke="${o.c || GRAFITO}"` +
      ` stroke-width="${w}" stroke-linecap="round" opacity="${o.op || 0.55}"/>` +
      `<circle cx="${f(x + dx)}" cy="${f(y + largo)}" r="${f(w * 0.95)}" fill="${o.c || GRAFITO}" opacity="${o.op || 0.55}"/>`);
  }

  // Polvo o grano: puntos sueltos dentro de un polígono.
  polvo(poli, n, o) {
    o = o || {};
    const xs = poli.map(q => q[0]), ys = poli.map(q => q[1]);
    const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
    let hechos = 0;
    for (let k = 0; k < n * 20 && hechos < n; k++) {
      const x = x0 + this.rnd() * (x1 - x0), y = y0 + this.rnd() * (y1 - y0);
      if (!dentro(x, y, poli)) continue;
      this.add(`<circle cx="${f(x)}" cy="${f(y)}" r="${f((o.r || 0.6) * (0.5 + this.rnd()))}" fill="${o.c || GRAFITO}"${o.op ? ` opacity="${o.op}"` : ''}/>`);
      hechos++;
    }
  }

  // Una mancha plana sin borde acumulado (hollín, noche, agua), con o sin grano.
  capa(poli, color, o) {
    o = o || {};
    const d = o.recta ? 'M' + poli.map(q => `${f(q[0])},${f(q[1])}`).join(' L') + ' Z' : suave(poli, true);
    this.add(`<g filter="url(#desplaza)"><path d="${d}" fill="${color}" fill-opacity="${o.op || 0.9}"/>` +
      (o.grano ? `<path d="${d}" fill="${o.grano}" fill-opacity="${o.og || 0.5}" filter="url(#grano)"/>` : '') + '</g>');
  }

  svg(titulo) {
    const fuente = this.sinTexto ? '' :
      `<style>@font-face{font-family:'Mano';src:url(data:font/ttf;base64,${FUENTE}) format('truetype');}</style>`;
    // Guías y entradas salen en los tamaños de GPT Image 2: 1536 x 1024 o, si son verticales, 1024 x 1536.
    let caja = [0, 0, this.ancho, this.alto], tam = '';
    if (this.gpt) {
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

// Punto a una fracción s (0 a 1) del largo de una polilínea.
function punto(poli, s) {
  const largos = [0];
  for (let i = 1; i < poli.length; i++) largos.push(largos[i - 1] + Math.hypot(poli[i][0] - poli[i - 1][0], poli[i][1] - poli[i - 1][1]));
  const meta = s * largos[largos.length - 1];
  let i = 1;
  while (i < poli.length - 1 && largos[i] < meta) i++;
  const t = (meta - largos[i - 1]) / ((largos[i] - largos[i - 1]) || 1);
  const [a, b] = [poli[i - 1], poli[i]];
  return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, Math.atan2(b[1] - a[1], b[0] - a[0])];
}

/* ------------------------------------------------------------------ */
/* Figura 1. Cráneo/nido: la chujlla de los Huanca en corte (pp. 8-34) */
/* Dos lugares para mirar: el del narrador, de pie en la puerta, y el  */
/* del cuerpo que habita, en cuclillas junto al fuego. El corte elige  */
/* el segundo, y la luz se saca raspando el hollín.                    */
/* ------------------------------------------------------------------ */
function figura1(modo) {
  const h = new Hoja(700, 470, 1203,
    'Notación del corte de la chujlla de los Huanca. Dos puntos de vista: el narrador, de pie en la puerta, y el cuerpo que ' +
    'habita, en cuclillas junto al fuego. El corte elige el segundo. Adentro todo es hollín, negro de humo sobre siena, y la luz ' +
    'se saca raspando: las vigas atadas con paja, las hoces, el arado y el yugo. Los muros son piedras del cerro; el límite, ' +
    'el techo de paja con su cruz y su huaca. El perfil de cráneo es una decisión del dibujo.',
    modo);
  const suelo = 360, m = 80;  // 80 unidades por metro

  // El suelo, una sola línea, que sigue hacia el cerro.
  h.curva([[20, suelo + 1], [90, suelo], [186, suelo + 0.5]], { w: 0.7 });
  h.curva([[516, suelo], [548, suelo + 0.5]], { w: 0.7 });

  // Interior: siena debajo y negro de humo encima, el hollín (p. 30).
  const techoIn = [[212, 262], [226, 246], [256, 230], [302, 219], [348, 216], [400, 219], [442, 229], [472, 245], [490, 263]];
  const interior = [[212, 278], [212, suelo], [490, suelo]].concat(techoIn.slice().reverse());
  h.capa(interior, SIENA, { recta: true, op: 0.55 });
  h.capa(interior, HUMO, { recta: true, op: 0.86, grano: '#000000', og: 0.35 });

  // Muros de piedra y adobe (pp. 8, 30): cimiento de piedras y, arriba, hiladas de adobe.
  const muroIzq = [[186, 258], [212, 262], [212, 279], [187, 279]];
  const muroDer = [[490, 263], [514, 259], [516, suelo], [490, suelo]];
  for (const muro of [muroIzq, muroDer]) h.acuarela(muro, SIENA, SIENA_OSCURA, { op: 0.5, grano: 0.5 });
  h.empacar((x, y, r) => x - r > 491 && x + r < 515 && y - r > 318 && y + r < suelo, [490, 316, 516, suelo], 3, 5.5, 900)
    .forEach(p => h.forma(p.x, p.y, p.r, { relleno: '#d9a989', c: SIENA_OSCURA, w: 0.4 }));
  for (let y = 270; y < 316; y += 9) h.linea(491, y, 515, y - 0.4, { c: SIENA_OSCURA, w: 0.4, op: 0.8 });
  // La puerta: el muro de la izquierda solo queda como dintel.
  h.add(`<path d="M188,${suelo} L188,286 Q200,277 212,286 L212,${suelo}" fill="none" stroke="${GRAFITO}" stroke-width="0.5" stroke-dasharray="2 2.5"/>`);

  // El techo de paja «plomiza por el humo» (p. 10): una banda de fibras.
  const techoOut = [[186, 258], [200, 236], [232, 214], [284, 201], [346, 197], [408, 201], [454, 213], [488, 233], [514, 259]];
  h.acuarela(techoOut.concat(techoIn.slice().reverse()), PAJA_PLOMIZA, '#5b544c', { op: 0.42, grano: 0.4 });
  for (let i = 0; i < 230; i++) {
    const s = h.rnd(), [xa, ya] = punto(techoOut, s), [xb, yb, ang] = punto(techoIn, s), k = 0.15 + h.rnd() * 0.75;
    const x = xa + (xb - xa) * k, y = ya + (yb - ya) * k, a = ang + 0.5 + (h.rnd() - 0.5) * 0.4, l = 4 + h.rnd() * 5;
    h.add(`<path d="M${f(x)},${f(y)} l${f(l * Math.cos(a))},${f(l * Math.sin(a))}" stroke="#5f584f" stroke-width="0.55" stroke-linecap="round" opacity="0.8"/>`);
  }

  // Lo que se raspa (p. 31): vigas atadas con paja, las hoces, el arado, el yugo; los camastros.
  const R = { c: HUESO, w: 1.1 };
  h.linea(214, 268, 488, 268, { c: HUESO, w: 1.4 });
  h.linea(214, 272.5, 488, 272.5, { c: HUESO, w: 0.55 });
  for (const x of [236, 304, 372, 444]) {
    h.linea(x - 2.6, 265.5, x + 2.6, 275, { c: HUESO, w: 0.7 });
    h.linea(x + 2.6, 265.5, x - 2.6, 275, { c: HUESO, w: 0.7 });
  }
  const hoz = x => {
    h.linea(x, 273, x, 282, { c: HUESO, w: 0.6 });
    h.add(`<path d="M${x - 8},${286} Q${x - 4},${303} ${x + 9},${292}" fill="none" stroke="${HUESO}" stroke-width="1.15" stroke-linecap="round"/>`);
    h.linea(x - 8, 286, x - 1, 281, { c: HUESO, w: 1.4 });
  };
  hoz(254); hoz(466);
  h.linea(292, 273, 292, 287, { c: HUESO, w: 0.6 });
  h.linea(332, 273, 332, 285, { c: HUESO, w: 0.6 });
  h.linea(280, 290, 352, 283, R);
  h.linea(284, 290, 276, 300, R);
  h.linea(347, 284, 356, 292, { c: HUESO, w: 0.9 });
  h.linea(386, 273, 386, 281, { c: HUESO, w: 0.6 });
  h.linea(424, 273, 424, 281, { c: HUESO, w: 0.6 });
  h.linea(374, 282, 436, 282, { c: HUESO, w: 1.5 });
  for (const x of [384, 414]) h.add(`<path d="M${x},282 q5,12 11,0" fill="none" stroke="${HUESO}" stroke-width="0.9"/>`);
  h.add(`<path d="M214,${suelo} V349 H268 V${suelo} M434,${suelo} V350 H488 V${suelo}" fill="none" stroke="${HUESO}" stroke-width="0.8"/>`);

  // El fuego en el centro: brasa de boñiga, sin llama (pp. 30, 32), y su humo, que tiñe el techo.
  h.add(`<circle cx="352" cy="354" r="13" fill="${BRASA}" opacity="0.35" filter="url(#difumina)"/>` +
    `<ellipse cx="352" cy="356" rx="7" ry="3.6" fill="${BRASA}"/><ellipse cx="352" cy="355.5" rx="3" ry="1.5" fill="#e3935a"/>`);
  h.curva([[352, 346], [347, 330], [356, 312], [348, 294], [354, 276], [349, 252], [352, 224]], { c: HUESO, w: 0.55, op: 0.5, dash: '3 3' });
  h.orbita(352, 352, 44, 8, { c: '#cbc2b3', w: 0.5, desde: 3.3 });
  h.orbita(352, 351, 70, 13, { c: '#cbc2b3', w: 0.45, desde: 0.2, flecha: 0.42 });

  // El ojo del corte: en cuclillas, cerca del fuego (p. 32). La línea sale de la casa.
  const ojo = [322, suelo - 0.75 * m];
  h.linea(150, ojo[1], 212, ojo[1], { c: CLARO, w: 0.45, dash: '5 3' });
  h.linea(214, ojo[1], 488, ojo[1], { c: HUESO, w: 0.5, dash: '5 3', op: 0.75 });
  h.linea(518, ojo[1], 540, ojo[1], { c: CLARO, w: 0.45, dash: '5 3' });
  h.add(`<path d="M${ojo[0] - 5},${ojo[1]} Q${ojo[0]},${ojo[1] - 4} ${ojo[0] + 5},${ojo[1]} Q${ojo[0]},${ojo[1] + 4} ${ojo[0] - 5},${ojo[1]} Z"` +
    ` fill="none" stroke="${HUESO}" stroke-width="0.8"/><circle cx="${ojo[0]}" cy="${ojo[1]}" r="1.3" fill="${HUESO}"/>`);

  // El narrador, de pie en la puerta: mira desde arriba los camastros, sin entrar.
  const nar = [96, suelo - 1.6 * m];
  h.linea(nar[0], suelo, nar[0], nar[1] + 6, { w: 0.7, c: TINTA });
  h.punta(nar[0], nar[1], 0, { x: true, c: TINTA });
  h.linea(nar[0] + 3, nar[1] + 2, 226, 351, { c: CLARO, w: 0.4, dash: '1 3' });
  h.linea(nar[0] + 3, nar[1] + 2, 262, 349, { c: CLARO, w: 0.4, dash: '1 3' });
  h.linea(212, 340, 226, 351, { c: HUESO, w: 0.4, dash: '1 3' });
  h.linea(212, 324, 262, 349, { c: HUESO, w: 0.4, dash: '1 3' });

  // La puerta es la órbita; la bóveda, la calota; el fuego, el pensamiento (decisión del dibujo).
  h.orbita(199, 322, 21, 43, { c: CLARO, w: 0.5, desde: -1.2 });
  h.texto(262, 192, 'calota *', { t: 10.5, c: CLARO, giro: -15 });
  h.texto(166, 318, 'órbita *', { t: 10.5, c: CLARO, ancla: 'end' });
  h.texto(360, 327, 'pensamiento *', { t: 10.5, c: '#cbc2b3' });

  // El cerro, «una especie de padre del ayllu», da las piedras de los muros (p. 8).
  const cerro = [[566, suelo], [596, 342], [626, 322], [656, 302], [684, 286], [704, 278], [704, suelo + 2]];
  h.acuarela(cerro, SIENA, SIENA_OSCURA, { op: 0.32, grano: 0.4 });
  h.empacar((x, y, r) => dentro(x, y, cerro) && dentro(x - r, y + r, cerro) && dentro(x + r, y - r, cerro), [566, 278, 704, suelo], 2.4, 4.6, 1400)
    .forEach(p => h.forma(p.x, p.y, p.r, { relleno: '#dcb194', c: SIENA_OSCURA, w: 0.35 }));
  for (let i = 0; i < 14; i++) {
    const t = i / 13, x = 626 - t * 98, y = 318 - Math.sin(t * Math.PI) * 30 + t * 20 + (h.rnd() - 0.5) * 5;
    h.forma(x, y, 2.4 - t * 0.8, { relleno: '#dcb194', c: SIENA_OSCURA, w: 0.35 });
  }
  h.punta(522, 340, 2.2, { c: SIENA_OSCURA });

  // Cotas: dos metros (p. 30) y la altura de un adobe (p. 31).
  h.cota(538, suelo, 538, 197);
  h.texto(546, 282, 'dos metros (30)', { t: 10.5, giro: -90, ancla: 'middle', c: GRAFITO });
  h.cota(476, 349, 476, suelo, { c: HUESO });

  // Cruz de palo y huaca de barro cocido, contra el rayo (p. 10).
  h.linea(346, 197, 346, 166, { w: 1.1, c: TINTA });
  h.linea(337, 175, 355, 175, { w: 1.1, c: TINTA });
  h.forma(346, 183, 3.4, { relleno: BARRO, c: '#6a3420', w: 0.4, aplana: 0.8 });
  h.add(`<path d="M432,124 L414,136 L422,139 L398,152 L405,155 L372,168" fill="none" stroke="${GRAFITO}" stroke-width="0.6" stroke-linejoin="round"/>`);
  h.punta(368, 170, 0, { x: true });
  h.texto(438, 124, 'contra «los perpetuos peligros del rayo» (10)', { t: 11 });

  // Rótulos de las cuatro funciones (Cuadro 1), abajo en cuatro columnas, y el narrador.
  h.funcion('limite', [312, 76], [300, 206]);
  h.texto(288, 44, ['límite: techo de paja «plomiza por el humo», cruz de palo', 'y «una pequeña huaca de barro cocido» (10)'], { t: 11 });
  h.funcion('apoyo', [478, 170], [444, 266], { cs: HUESO });
  h.texto(466, 152, ['apoyo: vigas «mal unidas con lazos', 'de paja trenzada» (31)'], { t: 11 });
  h.texto(22, 398, ['* el narrador, de pie', 'en la puerta, mira', 'desde arriba: «morada', 'de piojos y pulgas» (31)'], { t: 11, c: GRAFITO });
  h.funcion('vano', [204, 388], [196, 345]);
  h.texto(184, 398, ['vano: la puerta; desde', '«el portal de su chujlla»', 'Paulo mira irse a sus', 'hijos (34)'], { t: 11 });
  h.funcion('masa', [392, 388], [446, 336], { cs: HUESO });
  h.texto(366, 398, ['masa: hollín y brasero', '«en el centro del cuarto» (30);', 'camastros de «la altura', 'de un adobe» (31)'], { t: 11 });
  h.funcion('apoyo', [566, 388], [503, 346], { cs: SIENA_OSCURA });
  h.texto(552, 398, ['apoyo: los muros, «con sus', 'piedras» del cerro, «una', 'especie de padre del', 'ayllu» (8)'], { t: 11 });
  // El corte, a la altura del cuerpo.
  h.flecha(590, 248, 549, 297, { c: GRAFITO, w: 0.45 });
  h.texto(560, 204, ['el corte, a la altura de', 'quien está «en cuclillas,', 'cerca del fuego» (32)'], { t: 11 });
  // Lo que hace la mano.
  h.flecha(196, 128, 256, 287, { c: SIENA_OSCURA, w: 0.45 });
  h.flecha(232, 142, 262, 318, { c: SIENA_OSCURA, w: 0.45 });
  h.texto(22, 124, ['QUITAR: la luz se raspa', 'SUMAR: negro de humo sobre siena'], { t: 11, c: SIENA_OSCURA });

  h.leyenda(30, 30, ['negro sobre siena: el hollín · claro: lo raspado']);
  return h.svg('Figura 1. Cráneo/nido');
}

/* ------------------------------------------------------------------ */
/* Figura 2. Signo Escalonado frente al mapa (pp. 6-38)                */
/* El mismo cerro en sección y en planta. El signo, simétrico, no      */
/* encaja en la pendiente: flota de un lado y se hunde del otro, y el  */
/* peón vive arriba aunque el signo lo ponga abajo.                    */
/* ------------------------------------------------------------------ */
function figura2(modo) {
  const h = new Hoja(560, 800, 2203,
    'Notación vertical del cerro de Jatun-Kolla en sección, arriba, y en planta, abajo, unidas por líneas de proyección. ' +
    'Sobre la sección, el Signo Escalonado de los Villca, Huanca y Condori, simétrico, no encaja en la pendiente: flota de un ' +
    'lado y se hunde en la roca del otro. El peón Juan Condori vive en una chujlla abandonada cerro arriba, aunque el signo lo ponga ' +
    'abajo. La planta es el tablero desigual de los barbechos, con mojones, estacas y la tercera parte de los Villca.',
    modo);
  const base = 420;
  // Sección: pendiente irregular, más empinada a la izquierda, con terrazas (p. 8).
  const izq = [[40, base], [64, 418], [78, 396], [108, 394], [122, 366], [150, 362], [158, 336], [190, 332], [200, 300], [214, 296],
    [226, 260], [244, 256], [256, 220], [262, 216], [276, 186], [296, 180], [304, 182]];
  const der = [[318, 194], [350, 200], [364, 226], [402, 232], [414, 256], [452, 264], [462, 290], [494, 300], [502, 330], [514, 336],
    [522, 370], [526, base]];
  const perfil = izq.concat(der);
  const cerro = perfil.concat([[526, base + 2], [40, base + 2]]);
  h.acuarela(cerro, SIENA, SIENA_OSCURA, { op: 0.46, grano: 0.55 });
  h.empacar((x, y, r) => dentro(x, y, cerro) && dentro(x, y - r - 2, cerro) && dentro(x - r, y, cerro) && dentro(x + r, y, cerro),
    [40, 180, 526, base], 2.2, 4.4, 2600).forEach(p => h.forma(p.x, p.y, p.r, { relleno: '#d8a585', c: SIENA_OSCURA, w: 0.3, op: 0.85 }));
  h.curva(perfil, { w: 0.6, c: SIENA_OSCURA });
  h.linea(22, base, 540, base, { w: 0.7 });

  // Chujllas: las de los antiguos, arriba (p. 6); la del peón, abandonada «cerro arriba» (p. 35).
  const choza = (x, y, w, o) => {
    o = o || {};
    const al = w * 0.8;
    h.add(`<path d="M${f(x - w / 2)},${f(y)} V${f(y - al * 0.62)} L${f(x)},${f(y - al)} L${f(x + w / 2)},${f(y - al * 0.62)} V${f(y)} Z"` +
      ` fill="${o.vacia ? PAPEL : HUMO}" stroke="${o.vacia ? TINTA : 'none'}" stroke-width="0.7"/>`);
  };
  choza(238, 256, 15); choza(252, 220, 9);
  for (const [x, y, w] of [[176, 332, 10], [206, 296, 9], [136, 362, 9], [92, 394, 8], [62, 418, 8], [380, 232, 9], [432, 264, 9],
    [480, 300, 8], [506, 336, 8]]) choza(x, y, w);
  choza(296, 180, 11, { vacia: true });

  // El Signo Escalonado, simétrico, inciso encima: flota a la izquierda, se hunde a la derecha (p. 38).
  const signo = [[70, 414], [70, 350], [120, 350], [120, 286], [170, 286], [170, 222], [370, 222], [370, 286], [420, 286], [420, 350],
    [470, 350], [470, 414]];
  const d = 'M' + signo.map(q => `${q[0]},${q[1]}`).join(' L');
  h.add(`<path d="${d}" fill="none" stroke="${TINTA}" stroke-width="0.6"/>` +
    `<path d="${d}" fill="none" stroke="${TINTA}" stroke-width="0.6" transform="translate(2.6 -2.6)"/>`);
  h.texto(196, 216, 'Villca', { t: 11.5 });
  h.texto(124, 280, 'Huanca', { t: 11.5 });
  h.texto(72, 344, 'Condori', { t: 11.5 });
  h.texto(24, 160, ['Signo Escalonado: «los Villca, Huanca', 'y Condori» son sus generaciones (38)'], { t: 11 });
  h.texto(54, 300, 'flota', { t: 10.5, c: CLARO });
  h.texto(442, 318, 'se hunde', { t: 10.5, c: '#5a3a28' });
  // El peón vive arriba; el signo lo pone abajo.
  h.curva([[290, 186], [250, 194], [172, 214], [112, 262], [90, 336]], { c: TINTA, w: 0.5, dash: '3 3', punta: true });
  h.funcion('vano', [330, 128], [296, 170]);
  h.texto(318, 114, ['vano: la chujlla del peón Juan Condori,', '«abandonada cerro arriba» (35), de los', 'que «no tienen historia» (22): vive arriba;', 'el signo lo pone abajo'], { t: 11 });

  // Proyección de la sección a la planta.
  for (const x of [70, 170, 296, 370, 470]) h.linea(x, base + 4, x, 506, { c: CLARO, w: 0.45, dash: '1.5 3.5' });
  h.texto(536, 466, 'proyección', { t: 10.5, c: CLARO, giro: -90, ancla: 'middle' });

  // Planta: el catastro rayado en una losa de pizarra (p. 9).
  const losa = [[38, 512], [150, 509], [270, 511], [400, 508], [502, 510], [503, 600], [505, 690], [504, 744], [380, 746], [250, 743],
    [120, 746], [36, 745], [37, 650], [35, 580]];
  h.acuarela(losa, PIZARRA, '#4f5459', { op: 0.58, grano: 0.45 });
  const cols = [40, 104, 170, 232, 296, 370, 434, 502], filas = [512, 570, 628, 688, 744];
  const nodo = (i, j) => [cols[i] + (j % 2 ? 7 : -5) * Math.sin(i * 1.7 + j), filas[j] + (i % 2 ? -6 : 5) * Math.cos(j * 1.3 + i)];
  for (let i = 1; i < cols.length - 1; i++) h.curva(filas.map((_, j) => nodo(i, j)), { c: HUESO, w: 0.9 });
  for (let j = 1; j < filas.length - 1; j++) h.curva(cols.map((_, i) => nodo(i, j)), { c: HUESO, w: 0.9 });
  // Las demás familias, «cuatro o cinco hectáreas» (p. 21): parcelas partidas.
  for (let i = 3; i < cols.length - 1; i++) {
    for (let j = 0; j < filas.length - 1; j++) {
      const [a, b, c] = [nodo(i, j), nodo(i + 1, j), nodo(i, j + 1)];
      if ((i + j) % 2 === 0) h.linea((a[0] + b[0]) / 2, a[1] + 3, (a[0] + b[0]) / 2 + 4, c[1] - 3, { c: HUESO, w: 0.5, op: 0.85 });
      if ((i * j) % 3 === 1) h.linea(a[0] + 3, (a[1] + c[1]) / 2, b[0] - 3, (a[1] + c[1]) / 2 + 3, { c: HUESO, w: 0.5, op: 0.85 });
    }
  }
  // La tercera parte de los Villca (p. 20): rayado oblicuo, cercado de estacas.
  const [vx0, vy0, vx1, vy1] = [44, 516, 228, 684];
  for (let c = vx0 - (vy1 - vy0); c < vx1; c += 6) {
    const xa = Math.max(vx0, c), ya = vy1 - (xa - c), xb = Math.min(vx1, c + (vy1 - vy0)), yb = vy1 - (xb - c);
    if (xb > xa + 2) h.linea(xa, ya, xb, yb, { c: HUESO, w: 0.6, op: 0.9 });
  }
  for (let x = 48; x < 232; x += 13) h.linea(x, 692, x, 684, { c: TINTA, w: 0.8 });
  for (let y = 520; y < 690; y += 13) h.linea(232, y, 239, y, { c: TINTA, w: 0.8 });
  // Mojones «desde tiempos antiguos» (p. 9), en los cruces.
  for (const [i, j] of [[1, 3], [3, 1], [4, 2], [5, 3], [6, 1], [2, 2], [6, 3]]) {
    const [x, y] = nodo(i, j);
    h.forma(x, y, 3.2, { anguloso: true, relleno: '#d8d2c6', c: TINTA, w: 0.5 });
  }
  // El cerro en planta: curvas de nivel alrededor de la cumbre; la chujlla del peón en la cima.
  for (const r of [22, 44, 66]) h.orbita(296, 620, r * 1.15, r * 0.8, { c: '#f3ede2', w: 0.55, giro: -0.2 });
  h.add(`<rect x="291" y="615" width="10" height="10" fill="${PAPEL}" stroke="${TINTA}" stroke-width="0.7"/>`);
  h.add(`<rect x="232" y="644" width="11" height="9" fill="${HUMO}"/>`);
  // Más allá del pedrerío, la finca de Tarakota (p. 9).
  for (let k = 0; k < 40; k++) h.forma(510 + h.rnd() * 14, 514 + h.rnd() * 228, 1 + h.rnd() * 1.6, { relleno: '#d8d2c6', c: GRAFITO, w: 0.3 });
  h.texto(542, 628, 'pedrerío y, más allá, la finca de Tarakota (9)', { t: 10.5, giro: -90, ancla: 'middle', c: GRAFITO });
  // Escritura rayada en la losa: el reparto, escalonado como el signo.
  h.texto(440, 718, ['«cuatro o cinco hectáreas»', 'por familia (21)'], { t: 11, c: '#f6f1e7', ancla: 'middle' });
  h.texto(296, 648, ['el peón: de los que', '«no tienen tierras» (21)'], { t: 11, c: '#f6f1e7', ancla: 'middle' });

  // Funciones (Cuadro 1).
  h.funcion('apoyo', [40, 432], [96, 350]);
  h.texto(22, 446, ['apoyo: «unos seis indios» trabajan para', 'los Villca por «el puchero y la casa» (21)'], { t: 11 });
  h.funcion('masa', [150, 762], [140, 600], { cs: TINTA });
  h.texto(22, 772, ['masa: las tierras de los Villca, «la tercera', 'parte de las tierras de la comunidad» (20)'], { t: 11 });
  h.funcion('limite', [330, 762], [236, 598]);
  h.texto(300, 772, ['límite: mojones (9) y «las estacas', 'de propiedad» de los Villca (20)'], { t: 11 });
  // Lo que dice el cerro de cerca y de lejos (p. 8).
  h.texto(318, 50, ['el cerro: de lejos, «forma cónica»; de cerca,', '«roquedos, en punta, pizarras a medio', 'deslizarse» (8)'], { t: 11 });
  // Operaciones.
  h.texto(330, 446, ['SECCIÓN: MANCHAR con el dedo,', 'piedra sobre piedra'], { t: 11, c: SIENA_OSCURA });
  h.texto(24, 488, ['PLANTA: RAYAR la pizarra con punzón: «tablero de ajedrez', 'un poco desigual, un poco contrahecho» (9)'], { t: 11, c: SIENA_OSCURA });

  h.leyenda(30, 30, ['siena: el cerro · gris: la pizarra rayada']);
  return h.svg('Figura 2. Signo Escalonado frente al mapa');
}

/* ------------------------------------------------------------------ */
/* Figura 3. Umbral de la apacheta (pp. 108-121)                       */
/* La hoja se parte en la cresta: a un lado la puna, seca; al otro el  */
/* yunga, disuelto. En la cresta, un cuerpo clavado y una familia de   */
/* rodillas; el montón de piedras de la apachita, que la novela no     */
/* pone, falta.                                                        */
/* ------------------------------------------------------------------ */
function figura3(modo) {
  const h = new Hoja(700, 500, 3203,
    'Notación apaisada partida por la cresta de la cordillera. A la izquierda, la puna, pastel seco cuyo grano asoma como piedra; ' +
    'a la derecha, la fauce del yunga, pastel disuelto que chorrea, con la niebla que sube. En la cresta, Paulo Huanca, clavado como ' +
    'un gallardete, y su familia de rodillas; al fondo, cumbres góticas. Falta el montón de piedras de la apachita de Bertonio. ' +
    'Lo único que cruza el abismo es una cadena de manos.',
    modo);
  const X = 340, hz = 250;  // la cresta y el horizonte de la puna

  // La puna: polvo seco con grano, horizonte recto (p. 108).
  const puna = [[20, hz], [X, hz], [X + 1, 440], [20, 440]];
  h.capa(puna, POLVO_PUNA, { recta: true, op: 0.7, grano: '#6f6450', og: 0.55 });
  h.polvo(puna, 900, { r: 0.55, c: '#6f6450', op: 0.7 });
  h.linea(20, hz, X, hz, { w: 0.7 });

  // Cumbres «semejantes a fantásticas construcciones góticas» (p. 109), a los dos costados.
  const aguja = (x0, x1, picos) => {
    const p = [[x0, hz]];
    picos.forEach(([x, y], k) => {
      p.push([x, y]);
      if (k < picos.length - 1) p.push([(x + picos[k + 1][0]) / 2 + (h.rnd() - 0.5) * 4, Math.max(y, picos[k + 1][1]) + 30 + h.rnd() * 30]);
    });
    p.push([x1, hz]);
    // La nieve en sombra devuelve azul: el flanco que no mira a la puna, de donde viene la luz de la tarde.
    for (let k = 1; k < p.length - 1; k += 2) {
      const [a, b] = [p[k], p[k + 1]];
      const sombra = [a, b, [b[0] - 1, Math.min(hz, b[1] + 40)], [a[0] + (b[0] - a[0]) * 0.25, Math.min(hz, b[1] + 46)]];
      h.add(`<path d="M${sombra.map(q => `${f(q[0])},${f(q[1])}`).join(' L')} Z" fill="${NIEVE_SOMBRA}" opacity="0.5" filter="url(#difumina)"/>`);
    }
    h.add(`<path d="M${p.map(q => `${f(q[0])},${f(q[1])}`).join(' L')}" fill="none" stroke="${GRAFITO}" stroke-width="0.6" stroke-linejoin="round"/>`);
    return p;
  };
  aguja(270, 334, [[284, 178], [298, 132], [314, 160], [326, 140]]);
  aguja(384, 536, [[398, 172], [416, 118], [434, 96], [452, 146], [474, 112], [494, 158], [514, 128], [526, 186]]);

  // El yunga: dos paredes de verde mojado que chorrean, y la fauce entre ellas (p. 109).
  const fondo = [[X, hz], [536, hz], [700, 236], [700, 440], [X, 440]];
  h.capa(fondo, VERDE, { recta: true, op: 0.22 });
  const paredIzq = [[X, hz], [352, 256], [366, 270], [380, 292], [392, 318], [404, 346], [416, 376], [428, 410], [440, 440], [X, 440]];
  const paredDer = [[560, 440], [572, 410], [586, 382], [602, 352], [620, 324], [640, 298], [662, 276], [684, 262], [700, 256], [700, 440]];
  for (const pared of [paredIzq, paredDer]) {
    h.acuarela(pared, VERDE, '#3d4f3b', { op: 0.6, borde: 0.5, grano: 0.35, recta: true });
    h.acuarela(pared, VERDE, '#3d4f3b', { op: 0.22, borde: 0.3, grano: 0.15, recta: true });
  }
  for (let k = 0; k < 26; k++) {
    const t = h.rnd(), [x, y] = t < 0.5 ? punto(paredIzq.slice(0, 7), t * 2) : punto(paredDer.slice(3, 9).reverse(), (t - 0.5) * 2);
    h.chorreo(x + (t < 0.5 ? -5 : 5), y + 6, Math.min(16 + h.rnd() * 30, 424 - y), { c: '#3d4f3b', w: 0.8, op: 0.5 });
  }
  // La niebla, «muselina de vapor» que la fauce traga (p. 109): blanca, borra los bordes; sube.
  for (const [cx, cy, rx, ry] of [[496, 410, 40, 10], [520, 384, 52, 12], [508, 352, 60, 14], [536, 324, 70, 15], [526, 292, 84, 14],
    [560, 270, 92, 12]]) {
    const nube = [], giro = (h.rnd() - 0.5) * 0.25;
    for (let k = 0; k < 11; k++) {
      const a = (k / 11) * 6.28, r = 0.6 + h.rnd() * 0.55, ex = rx * r * Math.cos(a), ey = ry * r * Math.sin(a);
      nube.push([cx + ex * Math.cos(giro) - ey * Math.sin(giro), cy + ex * Math.sin(giro) + ey * Math.cos(giro)]);
    }
    h.add(`<path d="${suave(nube, true)}" fill="${NIEBLA}" opacity="${f(0.6 + h.rnd() * 0.3)}" filter="url(#difumina)"/>`);
  }
  h.flecha(540, 420, 552, 262, { c: CLARO, w: 0.45, dash: '2 3' });
  // El río al fondo y la cadena de monos (p. 121).
  h.curva([[446, 438], [480, 433], [520, 437], [560, 432]], { c: NIEVE_SOMBRA, w: 1.2 });
  h.linea(450, 410, 486, 404, { c: '#3d4f3b', w: 1.1 });
  h.linea(560, 402, 528, 398, { c: '#3d4f3b', w: 1.1 });
  const monos = [];
  for (let i = 0; i <= 8; i++) { const t = i / 8; monos.push([486 + 42 * t, 404 - 6 * t + 16 * Math.sin(t * Math.PI)]); }
  h.curva(monos, { c: TINTA, w: 0.5 });
  for (const [x, y] of monos.slice(1, -1)) h.add(`<circle cx="${f(x)}" cy="${f(y)}" r="1.5" fill="${TINTA}"/>`);

  // La cresta: la hoja se parte aquí.
  h.linea(X, 30, X, 452, { c: SIENA_OSCURA, w: 0.5, dash: '6 4' });
  // Paulo, «gallardete clavado», y la familia de rodillas (p. 109).
  h.linea(X, hz, X, hz - 34, { w: 1.6, c: TINTA });
  h.add(`<path d="M${X},${hz - 32} q6,-3 10,1 q5,4 11,0 l-1,7 q-6,4 -11,0 q-5,-3 -9,0 Z" fill="${LANA}" opacity="0.92"/>`);
  for (const [dx, r] of [[-22, 4.2], [-14, 3.2], [-8, 3]]) h.forma(X + dx, hz - r * 0.7, r, { relleno: HUMO, c: HUMO, aplana: 0.9 });
  // El montón que falta: la apachita de Bertonio (p. 317), punteada.
  h.add(`<path d="M${X - 26},${hz} Q${X - 18},${hz - 22} ${X},${hz - 24} Q${X + 18},${hz - 22} ${X + 26},${hz}" fill="none" stroke="${GRAFITO}" stroke-width="0.6" stroke-dasharray="1.2 2.6"/>`);

  // La mirada de la familia, de vuelta al páramo (p. 109).
  h.flecha(X - 30, hz - 8, 34, hz - 8, { c: GRAFITO, w: 0.5, dash: '5 3' });
  h.texto(34, hz - 30, ['su mujer e hijos «se habían postrado de hinojos»', 'y «volvieron los ojos al páramo» (109)'], { t: 11 });

  // Rótulos de las funciones (Cuadro 1).
  h.funcion('apoyo', [X + 6, 66], [X + 4, hz - 34]);
  h.texto(X + 10, 34, ['apoyo: Paulo Huanca, «como un', 'gallardete clavado en la ceja', 'de la apacheta» (109)'], { t: 11 });
  h.funcion('limite', [596, 92], [530, 166]);
  h.texto(560, 34, ['límite: «la muralla', 'que condena el', 'horizonte del', 'altiplano» (108)'], { t: 11 });
  h.funcion('masa', [470, 92], [452, 144]);
  h.texto(X + 10, 88, 'masa: cumbres «góticas» y niebla (109)', { t: 11 });
  h.funcion('vano', [600, 168], [512, 334]);
  h.texto(576, 150, ['vano: «las fauces', 'del abismo» (109)'], { t: 11 });
  // La apacheta, en la novela y en Bertonio.
  h.flecha(232, 188, X - 18, hz - 14, { c: CLARO, w: 0.45 });
  h.texto(24, 132, ['apacheta: «abra de las cordilleras y', 'cumbre de los caminos» (160); pero la', 'apachita es «montón de piedras, que', 'por superstición van haciendo los', 'caminantes» [B. 317]: aquí falta *'], { t: 11 });
  // Lo que hace la mano.
  h.texto(28, 300, ['«la uniforme y gris alfombra polvorienta de las punas» (108)'], { t: 11 });
  h.texto(28, 318, 'SUMAR EN SECO: el grano del papel asoma como piedra', { t: 11, c: SIENA_OSCURA });
  h.flecha(600, 224, 640, 300, { c: SIENA_OSCURA, w: 0.45 });
  h.texto(560, 200, ['DISOLVER: «se disuelven', 'la piedra y el hielo de', 'la cordillera» (108)'], { t: 11, c: SIENA_OSCURA });
  h.texto(X, 470, '* en la cresta, una técnica se vuelve la otra', { t: 11, ancla: 'middle', c: GRAFITO });
  h.flecha(560, 462, 512, 416, { c: GRAFITO, w: 0.45 });
  h.texto(500, 486, 'lo único que cruza: «una cadena cogiéndose de manos» (121)', { t: 11, ancla: 'middle' });

  h.leyenda(30, 30, ['ocre: el polvo de la puna · verde: la hoja mojada', 'azul: la sombra de la nieve · blanco: la niebla'], { bertonio: true });
  return h.svg('Figura 3. Umbral de la apacheta');
}

/* ------------------------------------------------------------------ */
/* Figura 4. El castillete y la caída al plano 450 (pp. 134-154)       */
/* Arriba, la escalera del campamento y la torre; abajo, el pique y    */
/* los planos, como los pisos de un edificio al revés. Al fondo, el    */
/* agua sube por el cuerpo, que sirve de regla, hasta el montón.       */
/* ------------------------------------------------------------------ */
function figura4(modo) {
  const h = new Hoja(600, 820, 4203,
    'Notación vertical de la mina. Arriba, el campamento en escalera, de los chalets a los cuchitriles, el desmonte por el que se ' +
    'entra y, en la cima del cerro, la torre como un encaje. Abajo, en la casiterita, el pique y los planos 300, 350 y 450, como los ' +
    'pisos de un edificio al revés; en el pique, la jaula con siete cuerpos contra la rejilla. La copajira de los planos de arriba ' +
    'cae al 450; allí el agua sube por el cuerpo, de los tobillos al ombligo, hasta el informe montón de rocas, lodo y maderos.',
    modo);
  const sup = 262, P = [390, 410], ejeX = 400;   // la superficie y las paredes del pique
  const prof = d => sup + 1.05 * d;               // profundidad del plano, en las unidades del dibujo
  const [y300, y350, y450] = [prof(300), prof(350), prof(450)];

  // La roca: casiterita, pardo negruzco con destellos (pp. 134, 138); el cerro y la mina son una sola masa.
  const roca = [[290, sup], [290, 222], [306, 208], [330, 186], [356, 160], [380, 136], [400, 122], [420, 128], [446, 148], [478, 176],
    [516, 204], [548, 222], [556, 300], [544, 380], [558, 460], [544, 540], [556, 620], [546, 700], [558, 798], [256, 798], [246, 720],
    [258, 640], [244, 560], [256, 480], [246, 400], [254, 320], [244, sup]];
  h.capa(roca, CASITERITA, { recta: true, op: 0.8, grano: '#000000', og: 0.4 });
  for (let k = 0; k < 80; k++) {
    const x = 246 + h.rnd() * 314, y = 124 + h.rnd() * 676;
    if (dentro(x, y, roca)) h.add(`<circle cx="${f(x)}" cy="${f(y)}" r="${f(0.4 + h.rnd() * 0.5)}" fill="#cfc7b8" opacity="0.7"/>`);
  }
  // Las luces del cerro, «prendedor de topacios y rubíes» (p. 134): llama de carburo y algún rojo.
  for (const [x, y, c] of [[330, 204, CARBURO], [358, 178, CARBURO], [430, 152, BRASA], [462, 180, CARBURO], [500, 206, CARBURO],
    [380, 196, BRASA], [416, 176, CARBURO], [528, 222, CARBURO]]) h.add(`<circle cx="${x}" cy="${y}" r="1.6" fill="${c}"/>`);

  // Los vacíos, en papel: la galería de entrada, los nichos, el pique y los planos.
  const vacio = (x0, y0, x1, y1) => h.add(`<path d="M${x0},${y0} H${x1} V${y1} H${x0} Z" fill="${PAPEL}" filter="url(#desplaza)"/>`);
  vacio(290, 226, P[1], 237);
  vacio(P[0], 230, P[1], y450);
  vacio(P[1], y300 - 5, 524, y300 + 5);          // «300», a la derecha
  vacio(262, y350 - 5, P[0], y350 + 5);          // «350», a la izquierda
  vacio(258, y450 - 34, 598, y450 + 30);         // «450», el más hondo
  // «Como dos enormes nichos se miraban en el muro» (p. 141).
  for (const x of [P[0] + 1, P[0] + 11]) h.add(`<path d="M${x},243 V233 Q${x + 4},226 ${x + 8},233 V243" fill="none" stroke="${GRAFITO}" stroke-width="0.6"/>`);

  // El suelo y el campamento en escalera (p. 135): chalets, casas iguales, cuchitriles de calamina.
  h.linea(20, sup, 246, sup, { w: 0.7 });
  for (const x of [30, 60]) {
    h.add(`<path d="M${x},${sup} V${sup - 22} L${x + 13},${sup - 32} L${x + 26},${sup - 22} V${sup} Z" fill="none" stroke="${TINTA}" stroke-width="0.6"/>`);
    h.marcas([[x + 4, sup - 2], [x + 22, sup - 3]], { ang: -Math.PI / 2, var: 0.6, l: 4, c: VERDE, w: 1 });
  }
  for (let k = 0; k < 5; k++) {
    const x = 94 + k * 13;
    h.add(`<rect x="${x}" y="${sup - 18}" width="10" height="18" fill="none" stroke="${TINTA}" stroke-width="0.55"/>` +
      `<line x1="${x}" y1="${sup - 9}" x2="${x + 10}" y2="${sup - 9}" stroke="${TINTA}" stroke-width="0.4"/>`);
  }
  for (let k = 0; k < 34; k++) {
    const x = 162 + h.rnd() * 40, y = sup - 2 - h.rnd() * 8;
    h.add(`<rect x="${f(x)}" y="${f(y - 3)}" width="4" height="3" fill="${CALAMINA}" stroke="${GRAFITO}" stroke-width="0.3"/>`);
  }
  h.add(`<path d="M26,${sup - 40} H90 V${sup - 26} H158 V${sup - 16} H206" fill="none" stroke="${GRAFITO}" stroke-width="0.6" stroke-dasharray="3 2.5"/>`);
  h.texto(22, 178, ['* la escalera del campamento: «chalets»,', 'casas «como las cuadras de un cuartel»', 'y «enjambre de cuchitriles de calamina» (135)'], { t: 11 });

  // El desmonte, roca sin mineral, por el que se entra (p. 140); los mineros «como hilera de hormigas».
  const desmonte = [[204, sup], [230, 252], [256, 240], [280, 228], [292, 224], [294, sup]];
  h.acuarela(desmonte, PLOMIZO, GRAFITO, { op: 0.5, grano: 0.3, recta: true });
  h.empacar((x, y, r) => dentro(x, y, desmonte) && dentro(x, y - r, desmonte), [204, 222, 294, sup], 1.2, 2.6, 900)
    .forEach(q => h.forma(q.x, q.y, q.r, { anguloso: true, relleno: '#cfcac2', c: GRAFITO, w: 0.3 }));
  for (let k = 0; k < 8; k++) {
    const x = 212 + k * 10, y = sup - 6 - (x - 204) * 0.36;
    h.marcas([[x, y]], { ang: -Math.PI / 2, var: 0.3, l: 4.4, c: TINTA, w: 0.8 });
  }
  h.flecha(150, 304, 236, 254, { c: GRAFITO, w: 0.45 });
  h.texto(22, 300, ['el desmonte «que conducía a la entrada', 'de la mina»; los mineros, «como hilera', 'de hormigas» (140)'], { t: 11 });

  // La torre, «encaje de acero» (p. 134), en la cima del cerro.
  const T = [400, 124];
  h.linea(T[0] - 11, T[1], T[0] - 2, T[1] - 66, { c: TINTA, w: 0.55 });
  h.linea(T[0] + 11, T[1], T[0] + 2, T[1] - 66, { c: TINTA, w: 0.55 });
  for (let k = 0; k < 6; k++) {
    const y0 = T[1] - k * 11, y1 = y0 - 11, w0 = 11 - k * 1.5, w1 = 11 - (k + 1) * 1.5;
    h.linea(T[0] - w0, y0, T[0] + w1, y1, { c: TINTA, w: 0.35 });
    h.linea(T[0] + w0, y0, T[0] - w1, y1, { c: TINTA, w: 0.35 });
  }
  h.flecha(462, 64, 412, 82, { c: SIENA_OSCURA, w: 0.45 });
  h.texto(468, 44, ['RAYAR: la torre,', '«el encaje de acero»,', 'sobre «la negra y', 'acurrucada silueta', 'de un cerro» (134)'], { t: 11, c: SIENA_OSCURA });

  // El pique, con un plano en cada órbita: los pisos de un edificio al revés.
  for (const [y, rx] of [[y300, 36], [y350, 36], [y450, 44]]) h.orbita(ejeX, y, rx, 6, { c: '#d6cdbd', w: 0.5, giro: -0.04 });
  h.texto(500, y300 - 10, '«300»', { t: 11, c: HUESO, ancla: 'middle' });
  h.texto(300, y350 - 10, '«350»', { t: 11, c: HUESO, ancla: 'middle' });
  h.texto(424, y450 - 52, ['«450», «la más honda', 'excavación» (140)'], { t: 11, c: HUESO });
  // La jaula: siete cuerpos contra la rejilla (p. 143); sube y baja.
  const J = [P[0] + 1, 404, 18, 30];
  h.add(`<rect x="${J[0]}" y="${J[1]}" width="${J[2]}" height="${J[3]}" fill="${HUMO}"/>`);
  for (const [dx, dy] of [[4, 6], [9, 5], [14, 7], [5, 14], [12, 15], [5, 23], [13, 23]]) {
    h.add(`<circle cx="${J[0] + dx}" cy="${J[1] + dy}" r="2.6" fill="#b49a86" filter="url(#difumina)"/>`);
  }
  for (let k = 1; k < 4; k++) h.linea(J[0] + k * 4.5, J[1], J[0] + k * 4.5, J[1] + J[3], { c: HUESO, w: 0.45 });
  for (let k = 1; k < 5; k++) h.linea(J[0], J[1] + k * 6, J[0] + J[2], J[1] + k * 6, { c: HUESO, w: 0.45 });
  h.linea(P[1] + 10, 380, P[1] + 10, 456, { c: HUESO, w: 0.6 });
  h.punta(P[1] + 10, 378, -Math.PI / 2, { c: HUESO, l: 4.5 });
  h.punta(P[1] + 10, 458, Math.PI / 2, { c: HUESO, l: 4.5 });
  // La copajira del 300 y del 350 cae hasta el 450 (p. 143).
  for (const [x, y0] of [[P[1] - 2, y300 + 4], [P[0] + 2, y350 + 4], [P[1] - 5, y300 + 30]]) {
    h.add(`<path d="M${x},${f(y0)} V${f(y450 - 6)}" stroke="${COPAJIRA}" stroke-width="0.9" stroke-dasharray="5 4" opacity="0.9"/>`);
  }

  // El 450: el agua sube por el cuerpo, que es la regla (pp. 145, 152-153).
  const pies = y450 + 28, cx = 450;
  h.add(`<path d="M258,${f(y450 + 2)} H598 V${f(y450 + 30)} H258 Z" fill="${COPAJIRA}" opacity="0.5" filter="url(#desplaza)"/>`);
  h.linea(cx, pies, cx, pies - 52, { c: TINTA, w: 1.1 });
  h.add(`<circle cx="${cx}" cy="${f(pies - 55.5)}" r="3.2" fill="none" stroke="${TINTA}" stroke-width="0.8"/>`);
  [['a los tobillos (145)', 3], ['a la rodilla (145, 152)', 12], ['hasta la cintura (153)', 21], ['al ombligo (153)', 30]].forEach(([r, d]) => {
    h.linea(cx - 4, pies - d, cx + 4, pies - d, { c: TINTA, w: 0.6 });
    h.linea(cx + 6, pies - d, 478, pies - d, { c: CLARO, w: 0.35 });
    h.texto(482, pies - d + 3, r, { t: 10, c: TINTA });
  });
  h.flecha(cx - 12, pies - 1, cx - 12, pies - 31, { c: TINTA, w: 0.55 });
  // Los callapos, la viga que se quiebra y el informe montón (pp. 145, 154).
  for (const x of [318, 340, 362]) h.linea(x, y450 - 34, x, pies + 2, { c: '#8a6d4c', w: 1.6 });
  h.linea(300, y450 - 32, 326, y450 - 26, { c: '#8a6d4c', w: 1.8 });
  h.linea(332, y450 - 29, 368, y450 - 33, { c: '#8a6d4c', w: 1.8 });
  const b3 = pies + 2;
  h.add(`<g filter="url(#desplaza)"><path d="${suave([[262, b3], [266, b3 - 24], [280, b3 - 38], [294, b3 - 32], [304, b3 - 14], [308, b3]], true)}"` +
    ` fill="${LODO}" fill-opacity="0.6"/></g>`);
  h.monton(284, b3, 24, 38, 1.6, 3.4, q => h.forma(q.x, q.y, q.r, { anguloso: true, relleno: PLOMIZO, c: GRAFITO, w: 0.4 }));
  for (const [x0, y0, x1, y1] of [[266, b3 - 10, 282, b3 - 22], [286, b3 - 26, 302, b3 - 12]]) h.linea(x0, y0, x1, y1, { c: '#8a6d4c', w: 1.3 });

  // Funciones (Cuadro 1) y operaciones, al margen.
  h.funcion('vano', [190, 384], [P[0] + 4, 300], { c: LLAMADA });
  h.texto(22, 372, ['vano: pique, nichos, jaula,', 'boquete (141-144)'], { t: 11 });
  h.funcion('limite', [206, 438], [J[0] + 2, J[1] + 12], { cs: HUESO, c: LLAMADA });
  h.texto(22, 430, ['límite: «siete hombres» quedan', '«apeñuscados contra la rejilla» (143)'], { t: 11 });
  h.texto(22, 472, ['MANCHAR: los cuerpos, con el dedo;', 'RAYAR: la rejilla, encima'], { t: 11, c: SIENA_OSCURA });
  h.texto(22, 540, ['* la mina, un edificio al revés:', 'sus pisos bajan'], { t: 11, c: GRAFITO });
  h.flecha(156, 550, 362, y300 - 2, { c: LLAMADA, w: 0.4 });
  h.flecha(196, 624, P[0] + 3, y350 + 40, { c: '#c58d6a', w: 0.45 });
  h.texto(22, 610, ['DISOLVER: «la copajira del “300”', 'y del “350” cae hasta allí» (143),', 'y sube por el cuerpo'], { t: 11, c: SIENA_OSCURA });
  h.funcion('apoyo', [170, 700], [318, y450 - 6], { cs: HUESO, c: LLAMADA });
  h.texto(22, 692, ['apoyo: «el revestimiento de', 'callapos» (145); «quebróse', 'la viga del techo» (154)'], { t: 11 });
  h.funcion('masa', [170, 770], [280, b3 - 10], { cs: HUESO, c: LLAMADA });
  h.texto(22, 762, ['masa: «un informe montón', 'de rocas, lodo y maderos', 'astillados» (154)'], { t: 11 });

  h.leyenda(30, 30, ['pardo negro: la casiterita · papel: el vacío', 'ocre: la copajira']);
  return h.svg('Figura 4. El castillete y la caída al plano 450');
}

/* ------------------------------------------------------------------ */
/* Figura 5. Pelvis telúrica / Pachamama sorda (pp. 56-66)             */
/* El cielo queda en papel, sin tocar. En la tierra agrietada, la      */
/* cuenca de las vertientes secas se dibuja como una pelvis: un hueso  */
/* que carga peso, no un recipiente.                                   */
/* ------------------------------------------------------------------ */
function figura5(modo) {
  const h = new Hoja(700, 520, 5203,
    'Notación de la sequía. El cielo es el papel sin tocar: ni una pincelada. Abajo, la tierra parda y plomiza, con grietas ' +
    'raspadas. En el centro, la cuenca seca de las vertientes, con su cauce arenoso, dibujada como una pelvis de blanco hueso, ' +
    'la cadera del ganado que el texto compara con una luna menguante; líneas de carga van del espinazo a las patas: un hueso ' +
    'que sostiene, no un recipiente. Al pie, la tierra sorda del Achachi y del narrador frente a la Pachamama de Bertonio.',
    modo);
  const hz = 210;
  // La tierra: parda y «plomiza y mineral» (pp. 56, 66), con su grano.
  const tierra = [[20, hz], [690, hz], [690, 404], [560, 410], [400, 405], [240, 410], [20, 406]];
  h.capa(tierra, LODO, { recta: true, op: 0.42 });
  h.capa(tierra, PLOMIZO, { recta: true, op: 0.35, grano: '#3e362e', og: 0.45 });
  h.linea(20, hz, 690, hz, { w: 0.7 });
  // El cerro de las ofrendas y su humo, lo único que sube al cielo (p. 58).
  h.acuarela([[34, hz], [60, 190], [86, 174], [100, 172], [118, 184], [146, hz]], LODO, '#3e362e', { op: 0.55 });
  h.curva([[100, 170], [95, 150], [104, 130], [96, 108], [104, 88], [98, 68], [103, 54]], { c: CLARO, w: 0.6 });
  h.curva([[103, 54], [99, 44], [104, 34]], { c: CLARO, w: 0.5, dash: '1.5 3' });
  h.texto(114, 92, ['ofrendas «en la cumbre del cerro»:', '«todo lo hemos quemado» (58)'], { t: 11 });

  // Grietas raspadas hasta el papel (p. 56), fuera de la pelvis.
  const pelvisCaja = (x, y) => x > 196 && x < 524 && y > 216 && y < 404;
  for (let k = 0, n = 0; k < 200 && n < 20; k++) {
    const x = 30 + h.rnd() * 650, y = hz + 14 + h.rnd() * 180;
    if (pelvisCaja(x, y) || pelvisCaja(x + 30, y) || pelvisCaja(x - 30, y)) continue;
    h.grieta(x, y, h.rnd() * 6.28, 22 + h.rnd() * 26, { c: '#f4efe4', w: 0.9, n: 4 });
    n++;
  }

  // La pelvis: la cuenca seca vista desde arriba, en blanco hueso mate.
  const der = [[360, 252], [382, 250], [396, 240], [424, 228], [462, 224], [494, 234], [512, 254], [514, 280], [500, 302], [474, 316],
    [456, 332], [450, 356], [436, 382], [412, 396], [392, 390], [376, 376], [360, 378]];
  const contorno = der.concat(der.slice(1, -1).reverse().map(([x, y]) => [720 - x, y]));
  h.add(`<g filter="url(#desplaza)"><path d="${suave(contorno, true)}" fill="${HUESO}"/>` +
    `<path d="${suave(contorno, true)}" fill="#d9cdb6" fill-opacity="0.5" filter="url(#grano)"/></g>`);
  h.add(`<path d="${suave(contorno, true)}" fill="none" stroke="${GRAFITO}" stroke-width="0.7"/>`);
  h.add(`<path d="M344,252 L376,252 L372,286 L360,293 L348,286 Z" fill="#e1d6c0" stroke="${GRAFITO}" stroke-width="0.4"/>`);
  for (const [x, g] of [[412, 22], [308, -22]]) {
    h.add(`<ellipse cx="${x}" cy="370" rx="13" ry="8.5" transform="rotate(${g} ${x} 370)" fill="#b5a996" stroke="${GRAFITO}" stroke-width="0.5"/>`);
  }
  // Por dentro, el cauce «arenoso y blanquecino», «tachonado de pedrisca» (p. 58).
  const cuenca = [[360, 292], [384, 286], [402, 298], [406, 318], [396, 340], [378, 352], [360, 355], [342, 352], [324, 340], [314, 318],
    [318, 298], [336, 286]];
  h.add(`<path d="${suave(cuenca, true)}" fill="#e7dcc5" stroke="${GRAFITO}" stroke-width="0.55"/>`);
  h.empacar((x, y, r) => dentro(x, y, cuenca) && dentro(x + r + 2, y, cuenca) && dentro(x - r - 2, y, cuenca) && dentro(x, y + r + 2, cuenca),
    [314, 286, 406, 355], 0.9, 2, 500).forEach(q => h.forma(q.x, q.y, q.r, { relleno: '#d2c6b0', c: GRAFITO, w: 0.3 }));
  // Líneas de carga: del espinazo a las patas, por el anillo del hueso (decisión del dibujo).
  for (const sg of [1, -1]) {
    const X = x => 360 + sg * (x - 360);
    h.curva([[X(366), 262], [X(400), 254], [X(446), 252], [X(476), 272], [X(470), 302], [X(452), 338]], { c: SIENA_OSCURA, w: 0.6, dash: '4 2.5', punta: true });
    h.flecha(X(452), 344, X(470), 372, { c: SIENA_OSCURA, w: 0.6 });
  }
  h.flecha(360, 226, 360, 248, { c: SIENA_OSCURA, w: 0.6 });

  // La luna menguante, a la que el texto compara la cadera del ganado (p. 64).
  h.add(`<path d="M330,50 A20,20 0 1,0 330,90 A26,26 0 0,1 330,50 Z" fill="${PAPEL}" stroke="${GRAFITO}" stroke-width="0.6"/>` +
    `<path d="M330,50 A20,20 0 1,0 330,90" fill="none" stroke="${BARRO}" stroke-width="0.6" opacity="0.6" transform="translate(-1.2 0)"/>`);
  h.linea(326, 94, 456, 222, { c: CLARO, w: 0.45, dash: '1 3' });
  h.texto(302, 74, '«luna menguante» (64)', { t: 11, ancla: 'end' });

  // Funciones (Cuadro 1).
  h.funcion('limite', [470, 160], [560, hz - 3]);
  h.texto(440, 150, ['límite: «ni una pincelada enturbió', 'el papel celeste» (57)'], { t: 11 });
  h.texto(440, 182, 'RESERVAR: el cielo es el papel sin tocar', { t: 11, c: SIENA_OSCURA });
  h.funcion('masa', [118, 268], [150, 330], { cs: TINTA });
  h.texto(28, 238, ['masa: las sementeras', '«se agrietan como', 'paredes envejecidas» (56)'], { t: 11 });
  h.texto(28, 384, ['QUITAR: las grietas', 'se raspan'], { t: 11, c: SIENA_OSCURA });
  h.funcion('vano', [540, 282], [398, 330]);
  h.texto(536, 238, ['vano: las vertientes', 'secas: «un arenoso y', 'blanquecino cauce,', 'tachonado de pedrisca» (58)'], { t: 11 });
  h.funcion('apoyo', [170, 432], [266, 346]);
  h.texto(24, 444, ['apoyo: la cadera del ganado,', '«las nalgas abiertas a la manera', 'de una luna menguante» (64)'], { t: 11 });
  h.texto(244, 444, ['el Achachi: «La tierra está vieja, y como toda', 'vieja, es sorda» (58); el narrador: «vientre', 'de sequedad inexorable» (66); para Bertonio,', 'Pachamama es «nombre de reverencia» [B. 420]'], { t: 11 });
  h.flecha(560, 432, 476, 360, { c: SIENA_OSCURA, w: 0.45 });
  h.texto(510, 444, ['* la cuenca, una pelvis:', 'un hueso que carga peso del', '«espinazo» a las «patas» (64),', 'no un recipiente'], { t: 11, c: GRAFITO });

  h.leyenda(440, 30, ['papel: el cielo · blanco hueso: la pelvis', 'pardo y plomizo: la tierra seca'], { bertonio: true });
  return h.svg('Figura 5. Pelvis telúrica / Pachamama sorda');
}

/* ------------------------------------------------------------------ */
/* Figura 6. El centinela de la resistencia (pp. 72-80)                */
/* Nocturno vertical: en el vano de la chujlla de los Villca, tres     */
/* vigías trazados como mojones y el cayado como cuarto apoyo. Los     */
/* muertos suben a mirar el cielo; los vigías miran el llano baldío.   */
/* ------------------------------------------------------------------ */
function figura6(modo) {
  const h = new Hoja(560, 840, 6203,
    'Notación vertical nocturna. En el vano de la chujlla de los Villca, la más amplia, tres vigías trazados como mojones de ' +
    'hueso y el cayado como cuarto apoyo. Del suelo suben los muertos a mirar el cielo, donde se raspan las estrellas, Marte ' +
    'y Sirio; los vigías miran inútilmente el llano baldío. A un lado, el campanario, la atalaya de los buitres, y las puertas ' +
    'batidas por el viento. El narrador los llama cancerberos; en aymara, el mojón es también amparo.',
    modo);
  const hz = 560;
  // La noche: negro, donde las estrellas se raspan.
  const noche = [[212, 34], [380, 30], [546, 36], [548, 200], [544, 380], [548, hz], [210, hz], [214, 380], [208, 200]];
  h.capa(noche, NOCHE, { recta: true, op: 0.9, grano: '#000000', og: 0.3 });
  for (let k = 0, n = 0; k < 900 && n < 150; k++) {
    const x = 218 + h.rnd() * 322, y = 40 + h.rnd() * 470;
    if (!dentro(x, y, noche)) continue;
    const r = h.rnd() < 0.85 ? 0.45 + h.rnd() * 0.4 : 0.9 + h.rnd() * 0.5;
    h.add(`<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="${HUESO}" opacity="${f(0.55 + h.rnd() * 0.45)}"/>`);
    n++;
  }
  // Marte, óxido de hierro; Sirio, blanco azulado (p. 72).
  const marte = [300, 148], sirio = [446, 104];
  h.add(`<circle cx="${marte[0]}" cy="${marte[1]}" r="3.4" fill="${SIENA}"/>` +
    `<circle cx="${sirio[0]}" cy="${sirio[1]}" r="6" fill="${SIRIO}" opacity="0.35" filter="url(#difumina)"/><circle cx="${sirio[0]}" cy="${sirio[1]}" r="2.8" fill="${SIRIO}"/>`);
  h.texto(marte[0] + 8, marte[1] + 4, 'Marte', { t: 10.5, c: HUESO });
  h.texto(sirio[0] + 9, sirio[1] + 4, 'Sirio', { t: 10.5, c: HUESO });

  // El suelo: polvo ocre de la puna, «un aguafuerte de tonos grises» (p. 79).
  const suelo = [[20, hz], [548, hz], [548, 640], [20, 642]];
  h.capa(suelo, POLVO_PUNA, { recta: true, op: 0.6, grano: '#6f6450', og: 0.5 });
  for (let k = 0; k < 16; k++) {
    const y = hz + 8 + k * 4.8;
    h.linea(24 + h.rnd() * 40, y, 540 - h.rnd() * 40, y + (h.rnd() - 0.5) * 2, { c: '#7d7262', w: 0.3, op: 0.6 });
  }
  h.linea(20, hz, 548, hz, { w: 0.7 });
  // Un ayllu vacío: pirca derruida y techo desfondado (p. 79).
  h.add(`<path d="M44,${hz} V${hz - 26} L60,${hz - 34} M74,${hz - 30} L92,${hz - 24} V${hz} M58,${hz - 12} H70" fill="none" stroke="${TINTA}" stroke-width="0.6"/>`);
  for (let k = 0; k < 9; k++) h.forma(104 + k * 9 + h.rnd() * 3, hz - 2 - (k % 3 === 0 ? 0 : 4 + h.rnd() * 4), 3, { relleno: '#d8cdb8', c: GRAFITO, w: 0.4 });

  // La chujlla de los Villca, «la más amplia y cómoda» (p. 79): adobe y paja.
  const casa = [[236, hz], [236, 514], [420, 514], [420, hz]];
  h.acuarela(casa, SIENA, SIENA_OSCURA, { op: 0.55, grano: 0.5, recta: true });
  h.acuarela([[228, 516], [262, 494], [328, 484], [394, 494], [428, 516]], PAJA_PLOMIZA, '#5b544c', { op: 0.6, grano: 0.4 });
  const vano = [302, 522, 52, hz - 522];
  h.add(`<path d="M${vano[0]},${hz} V${vano[1] + 6} Q${vano[0] + vano[2] / 2},${vano[1] - 4} ${vano[0] + vano[2]},${vano[1] + 6} V${hz} Z" fill="${NOCHE}"/>`);
  // Los tres vigías, trazados como mojones de hueso (decisión del dibujo), y el cayado.
  for (const [x, alto] of [[314, 30], [328, 33], [342, 29]]) {
    h.add(`<rect x="${x - 3.2}" y="${hz - alto}" width="6.4" height="${alto}" rx="3" fill="${HUESO}"/>`);
    h.linea(x - 5, hz - 0.5, x + 5, hz - 0.5, { c: HUESO, w: 1 });
  }
  h.add(`<path d="M362,${hz} L371,${hz - 40} q2,-6 7,-3" fill="none" stroke="#8a6d4c" stroke-width="1.6" stroke-linecap="round"/>`);
  // Lo que miran: el llano, «inútilmente» (p. 80); se pierde en una «x» a cada lado.
  h.flecha(298, hz - 22, 34, hz - 22, { c: HUESO, w: 0.5, dash: '1.5 3' });
  h.flecha(358, hz - 22, 210, hz - 22, { c: HUESO, w: 0.5, dash: '1.5 3' });
  h.linea(424, hz - 22, 540, hz - 22, { c: GRAFITO, w: 0.5, dash: '1.5 3' });
  h.linea(212, hz - 22, 234, hz - 22, { c: GRAFITO, w: 0.5, dash: '1.5 3' });
  h.punta(28, hz - 22, 0, { x: true, c: TINTA });
  h.punta(544, hz - 22, 0, { x: true, c: TINTA });

  // Los muertos salen de la tierra a mirar el cielo (p. 80): veladuras con el dedo, que suben.
  for (const [x, y0, n] of [[252, hz - 8, 6], [392, hz - 54, 7], [454, hz - 10, 5], [282, hz - 62, 4]]) {
    for (let k = 0; k < n; k++) {
      const y = y0 - k * 22 - h.rnd() * 6, w = 15 - k * 1.2 + h.rnd() * 5, dx = (h.rnd() - 0.5) * 8;
      h.add(`<ellipse cx="${f(x + dx)}" cy="${f(y)}" rx="${f(w)}" ry="${f(3 + h.rnd() * 2)}" transform="rotate(${f((h.rnd() - 0.5) * 24)} ${f(x + dx)} ${f(y)})"` +
        ` fill="#dcd8cf" opacity="${f(0.42 - k * 0.05)}" filter="url(#difumina)"/>`);
    }
    h.flecha(x, y0 - n * 14, x, y0 - n * 22 - 26, { c: '#d9d6cf', w: 0.5, dash: '2 3' });
  }

  // El campanario, «aquella atalaya» de los buitres (p. 79).
  const C = 504;
  h.add(`<path d="M${C - 8},${hz} V380 L${C},364 L${C + 8},380 V${hz}" fill="none" stroke="${HUESO}" stroke-width="0.7"/>`);
  for (const y of [470, 420]) h.orbita(C, y, 16, 4, { c: '#bdb6aa', w: 0.45 });
  h.marcas([[C - 6, 352], [C + 7, 346]], { c: HUESO, w: 0.9, l: 3.4, ang: -0.6, var: 0.2 });
  h.marcas([[C - 3, 352], [C + 10, 346]], { c: HUESO, w: 0.9, l: 3.4, ang: -2.5, var: 0.2 });
  h.texto(C - 14, 470, '«aquella atalaya» (79)', { t: 10.5, c: HUESO, giro: -90, ancla: 'middle' });
  // Las puertas batidas por el viento (p. 79): el arco de una hoja que va y viene.
  h.add(`<path d="M440,${hz} V${hz - 26} H470 V${hz}" fill="none" stroke="${HUESO}" stroke-width="0.6"/>`);
  h.add(`<path d="M450,${hz} L466,${hz - 12}" stroke="${HUESO}" stroke-width="1.2"/>` +
    `<path d="M466,${hz} A16,16 0 0,0 463.4,${f(hz - 9.4)}" fill="none" stroke="${HUESO}" stroke-width="0.5" stroke-dasharray="1.5 2"/>`);

  // Funciones (Cuadro 1) y lo demás, al margen.
  h.texto(22, 50, ['«Sirio y Marte eran semejantes', 'a coágulos de aquella sangre', 'estelar» (72)'], { t: 11 });
  h.linea(176, 54, marte[0] - 6, marte[1] - 2, { c: LLAMADA, w: 0.4 });
  h.texto(22, 104, ['* Marte, óxido de hierro: la', 'tierra en el cielo; Sirio,', 'blanco azulado'], { t: 11, c: GRAFITO });
  h.texto(22, 160, ['QUITAR: las estrellas', 'se raspan en el negro'], { t: 11, c: SIENA_OSCURA });
  h.texto(22, 214, ['los muertos «que en las noches', 'salían de la tierra para mirar', 'el cielo» (80)'], { t: 11 });
  h.texto(22, 256, 'MANCHAR: veladuras con el dedo', { t: 11, c: SIENA_OSCURA });
  h.linea(196, 232, 246, 468, { c: LLAMADA, w: 0.4 });
  h.texto(22, 304, ['el narrador: «aquellos cancerberos,', 'aquellos muertos en vida» (80),', 'pero también «celadores', 'y enfermeros» (79)'], { t: 11 });
  h.texto(22, 372, ['en aymara, achachi es «término', 'o mojón de las tierras» [B. 307];', 'y saywa, «amparo, defensor,', 'refugio, padre» [B. 447]'], { t: 11 });
  h.texto(22, 440, ['* los tres vigías, tres mojones', 'que cuidan: «acordaron dejar', 'tres vigilantes al cuidado', 'del ayllu» (75)'], { t: 11, c: GRAFITO });
  h.linea(170, 476, 312, 530, { c: LLAMADA, w: 0.4 });
  h.funcion('apoyo', [170, 514], [370, 536], { c: LLAMADA });
  h.texto(22, 506, ['apoyo: «el cayado de palo» (75),', 'como la «vara de Jilakata» (73)'], { t: 11 });
  h.funcion('vano', [470, 658], [458, hz - 6], { cs: TINTA });
  h.texto(384, 670, ['vano: «el viento zarandeaba', 'las puertas en las chujllas» (79)'], { t: 11 });
  h.funcion('masa', [282, 658], [270, 540], { c: LLAMADA });
  h.texto(206, 670, ['masa: «la chujlla de los Villca,', 'la más amplia y cómoda» (79)'], { t: 11 });
  h.funcion('limite', [110, 658], [100, hz - 22], { c: LLAMADA });
  h.texto(22, 670, ['límite: «sus miradas', 'penetraban inútilmente en la', 'silenciosa inmensidad» (80)'], { t: 11 });
  h.texto(284, 628, 'RAYAR: el llano, «un aguafuerte de tonos grises» (79)', { t: 11, c: SIENA_OSCURA, ancla: 'middle' });

  h.leyenda(30, 740, ['negro: la noche · blanco hueso: los vigías', 'ocre: el polvo · siena: el adobe'], { bertonio: true });
  return h.svg('Figura 6. El centinela de la resistencia');
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
function figura7(modo) {
  const h = new Hoja(700, 450, 7203,
    'Notación de la memoria del retorno: desde la atalaya, la mirada, que es también la línea del tiempo, pasa por encima ' +
    'de la muralla y del foso y llega al horizonte dorado de lo pasado antiguo. La muralla es una banda de tierra siena: ' +
    'sus caras son los apellidos que vuelven y su relleno, la legión sin tierra. En el foso de alquitrán, raspados, los muertos del hambre.',
    modo);
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
function figura8(modo) {
  const h = new Hoja(560, 790, 8203,
    'Notación vertical: el eje es la novela leída de la página 9 a la 154. Tres montones bajan por él, unidos por una espiral: ' +
    'la montaña de piedras del ayllu, el montón de papeles de la aldea y el desmonte de la mina. La montaña que debía ' +
    'sobrepasar la altura del cerro termina en el montón que sepulta a Juan Condori.',
    modo);
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

// Las Figuras 1 a 6 no escriben guías: en ../guias, los nombres guia_fig1… a guia_fig6… son las guías
// de composición de los pasteles (analisis/17), que son otra cosa.
const SOLO = process.argv.slice(2);
for (const [nombre, hacer, guias] of [
  ['fig1_craneo_nido.svg', figura1, false],
  ['fig2_signo_mapa.svg', figura2, false],
  ['fig3_apacheta.svg', figura3, false],
  ['fig4_castillete.svg', figura4, false],
  ['fig5_pelvis.svg', figura5, false],
  ['fig6_centinela.svg', figura6, false],
  ['fig7_memoria_retorno.svg', figura7, true],
  ['fig8_tres_montones.svg', figura8, true]]) {
  if (SOLO.length && !SOLO.some(s => nombre.startsWith(s))) continue;
  fs.writeFileSync(path.join(DIR, nombre), hacer('figura'), 'utf8');
  console.log('escrito', nombre);
  if (!guias) continue;
  for (const modo of ['guia', 'entrada']) {
    const destino = path.join(DIR, '..', 'guias', `${modo}_${nombre}`);
    fs.writeFileSync(destino, hacer(modo), 'utf8');
    console.log('escrito', path.relative(DIR, destino));
  }
}
