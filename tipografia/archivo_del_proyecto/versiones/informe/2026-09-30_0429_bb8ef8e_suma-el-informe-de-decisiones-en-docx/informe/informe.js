/* El informe de decisiones de Contenida, en .docx.
 *
 * Uso (desde la raíz del repositorio; necesita el paquete docx de npm, fontTools y brotli):
 *   python3 tipografia/informe/mapas.py
 *   node tipografia/informe/informe.js
 *
 * Escribe tipografia/informe/contenida_informe_de_decisiones.docx, con Newsreader y
 * Courier Prime incrustadas (licencia SIL OFL) y los seis mapas de mapas/.
 */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType,
  BorderStyle, ShadingType, ImageRun, PageBreak, Header, Footer, PageNumber, LevelFormat,
  PageOrientation, VerticalAlign, LineRuleType, Tab, TabStopType, LeaderType,
} = require("docx");

const AQUI = __dirname;
const TIPO = path.join(AQUI, "..");
const SALIDA = path.join(TIPO, "simulacion", "salida");
const MAPAS = path.join(AQUI, "mapas");

// ------------------------------------------------------------------ la paleta y las fuentes de las láminas
const TINTA = "1D1C1A", VIOLETA = "4A2470", GRIS = "6D6A63", GRIS2 = "9A968D", FILETE = "CFCAC0", PAPEL2 = "EFECE4";
const F = {
  texto: "Newsreader", cursiva: "Newsreader Italic", ligera: "Newsreader Light", ligeraCursiva: "Newsreader Light Italic",
  media: "Newsreader Medium", mono: "Courier Prime", monoNegra: "Courier Prime Bold", simbolos: "Arial",
};

function fuentes() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "contenida-fuentes-"));
  execFileSync("python3", [path.join(AQUI, "fuentes_docx.py"), dir], { stdio: "ignore" });
  const archivos = {
    [F.texto]: "Newsreader.ttf", [F.cursiva]: "NewsreaderItalic.ttf", [F.ligera]: "NewsreaderLight.ttf",
    [F.ligeraCursiva]: "NewsreaderLightItalic.ttf", [F.media]: "NewsreaderMedium.ttf", [F.mono]: "CourierPrime.ttf",
    [F.monoNegra]: "CourierPrimeBold.ttf",
  };
  return Object.entries(archivos).map(([name, a]) => ({ name, data: fs.readFileSync(path.join(dir, a)) }));
}

// ------------------------------------------------------------------ medidas (A4, en DXA)
const A4_W = 11906, A4_H = 16838, MARGEN = 1247;
const ANCHO = A4_W - 2 * MARGEN;                  // 9412 DXA = 16,6 cm
const PX = (dxa) => Math.round(dxa / 15);         // 1 px (96 ppp) = 15 DXA

// ------------------------------------------------------------------ texto con marcas: *cursiva*, **negrita**, `mono`
function runs(texto, base = {}) {
  const out = [];
  const partes = String(texto).split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g).filter((p) => p !== "");
  for (const p of partes) {
    let t = p, o = {};
    if (p.startsWith("**")) { t = p.slice(2, -2); o = { font: base.mono ? F.monoNegra : F.media }; }
    else if (p.startsWith("*")) { t = p.slice(1, -1); o = { font: F.cursiva }; }
    else if (p.startsWith("`")) { t = p.slice(1, -1); o = { font: F.mono, size: (base.size || 21) - 3 }; }
    // → y σ no están en los subconjuntos latinos de las fuentes: van en una del sistema
    for (const q of t.split(/([→σ])/g).filter((x) => x !== "")) {
      const esSimbolo = q === "→" || q === "σ";
      out.push(new TextRun(Object.assign({ text: q, font: base.font || F.texto, size: base.size, color: base.color }, o,
        esSimbolo ? { font: F.simbolos } : {})));
    }
  }
  return out;
}

const P = (texto, o = {}) => new Paragraph({
  children: runs(texto, o), alignment: o.align, spacing: o.spacing, indent: o.indent, keepNext: o.keepNext,
  style: o.style,
});
const H1 = (t) => { TITULOS.push([t, 1]); return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(t)], pageBreakBefore: true }); };
const H2 = (t) => { TITULOS.push([t, 2]); return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(t)], keepNext: true }); };
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(t)], keepNext: true });
const verso = (t, o = {}) => new Paragraph({
  children: runs(t, { font: F.cursiva, size: 24, color: VIOLETA }), indent: { left: 567 },
  spacing: { before: o.antes || 60, after: o.despues || 60 }, keepNext: o.keepNext,
});
const cita = (t) => new Paragraph({ children: runs(t, { size: 20, color: GRIS }), indent: { left: 567, right: 567 },
  spacing: { before: 80, after: 140 } });
const nota = (t) => new Paragraph({ children: runs(t, { font: F.mono, size: 16, color: GRIS, mono: true }),
  spacing: { before: 60, after: 200 } });
const vineta = (t, nivel = 0) => new Paragraph({ children: runs(t), numbering: { reference: "vinetas", level: nivel },
  spacing: { after: 60 } });
const numerada = (t, ref = "numeros") => new Paragraph({ children: runs(t), numbering: { reference: ref, level: 0 },
  spacing: { after: 60 } });
const salto = () => new Paragraph({ children: [new PageBreak()] });

// ------------------------------------------------------------------ tablas
const borde = { style: BorderStyle.SINGLE, size: 4, color: FILETE };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };

function tabla(cabeza, filas, anchos, o = {}) {
  const total = anchos.reduce((a, b) => a + b, 0);
  const celda = (t, i, esCabeza) => new TableCell({
    width: { size: anchos[i], type: WidthType.DXA },
    borders: bordes,
    shading: esCabeza ? { fill: PAPEL2, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: VerticalAlign.TOP,
    children: String(t).split("\n").map((linea) => new Paragraph({
      children: runs(linea, esCabeza ? { font: F.mono, size: 16, color: GRIS, mono: true }
        : (o.mono || []).includes(i) ? { font: F.mono, size: 16, mono: true, color: (o.violeta || []).includes(i) ? VIOLETA : TINTA }
          : { size: 18, color: (o.violeta || []).includes(i) ? VIOLETA : TINTA, font: (o.cursiva || []).includes(i) ? F.cursiva : F.texto }),
      spacing: { after: 20 },
    })),
  });
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: anchos,
    rows: [
      ...(cabeza && cabeza.some((c) => c) ? [new TableRow({ tableHeader: true, children: cabeza.map((t, i) => celda(t, i, true)) })] : []),
      ...filas.map((f) => new TableRow({ cantSplit: true, children: f.map((t, i) => celda(t, i, false)) })),
    ],
  });
}

// ------------------------------------------------------------------ imágenes
function tamano(ruta) {
  const b = fs.readFileSync(ruta);
  if (b[0] === 0x89) return [b.readUInt32BE(16), b.readUInt32BE(20)];
  let i = 2;                                                    // JPEG: buscar el SOF
  while (i < b.length) {
    const m = b[i + 1], largo = b.readUInt16BE(i + 2);
    if (m >= 0xc0 && m <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(m)) return [b.readUInt16BE(i + 7), b.readUInt16BE(i + 5)];
    i += 2 + largo;
  }
  throw new Error("no sé medir " + ruta);
}

function imagen(ruta, anchoDxa, altoMaxDxa) {
  const [w, h] = tamano(ruta);
  let W = PX(anchoDxa), H = Math.round(W * h / w);
  if (altoMaxDxa && H > PX(altoMaxDxa)) { H = PX(altoMaxDxa); W = Math.round(H * w / h); }
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60, line: 240, lineRule: LineRuleType.AUTO }, keepNext: true,
    children: [new ImageRun({ type: ruta.endsWith(".png") ? "png" : "jpg", data: fs.readFileSync(ruta),
      transformation: { width: W, height: H }, altText: { title: path.basename(ruta), description: path.basename(ruta), name: path.basename(ruta) } })],
  });
}

let nFigura = 0;
function figura(ruta, pie, anchoDxa = ANCHO, altoMaxDxa) {
  nFigura++;
  return [imagen(ruta, anchoDxa, altoMaxDxa),
    new Paragraph({ children: [new TextRun({ text: `Figura ${nFigura}. `, font: F.monoNegra, size: 16, color: TINTA }), ...runs(pie, { font: F.mono, size: 16, color: GRIS, mono: true })],
      spacing: { after: 220 } })];
}

// ------------------------------------------------------------------ encabezado y pie de página
function encabezado() {
  return new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
    new TextRun({ text: "Contenida · informe de decisiones", font: F.mono, size: 15, color: GRIS2 })] })] });
}
function piePagina() {
  return new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
    new TextRun({ children: [PageNumber.CURRENT], font: F.mono, size: 15, color: GRIS2 })] })] });
}

// ------------------------------------------------------------------ los mapas
const MAPA = {
  1: ["mapa_1_el_proyecto_entero.png", "El proyecto entero. Las cinco etapas (la obra, desenterrar, contener, devolver y lo digital) giran en ciclo alrededor de *Contenida*. Cada una abre un haz hacia su concepto, su teoría, su figura retórica y su verso. Abajo, las cuatro vasijas: los generadores o, l, n y a, rayados en violeta y acotados en milímetros."],
  2: ["mapa_2_teoria_y_fuentes.png", "Teoría y fuentes. Sobre la caja de 8 × 7, como sobre un plano, cada fuente tiende líneas violetas hacia lo que se toma de ella; las líneas punteadas grises van a lo que no se toma. La curva oscura es el hilo del proyecto."],
  3: ["mapa_3_la_obra_decision_por_decision.png", "La obra, decisión por decisión. La espina es la cadena de desplazamientos de la obra, de la piedra borrada a la pared de azulejo. Cada una de las dieciséis decisiones sale de ella con su traducción en la letra."],
  4: ["mapa_4_del_pie_a_los_55.png", "Del pie a los 55 signos. Del pie de la lámina salen medidas; de la obra, la forma. Los 20 parámetros forman las partes, las partes arman los cuatro generadores y los generadores, la caja."],
  5: ["mapa_5_la_cadena_de_estados.png", "La cadena de estados. Arriba, rayado en violeta, la materia que la letra pierde en cada estado; abajo, en gris, la luz que gana. La curva punteada es la vuelta: lo digital se imprime como esténcil y vuelve a ser placa. Abajo, las frotadas legibles de cada celda en la simulación."],
  6: ["mapa_6_retorica_y_poetica.png", "Retórica y poética. A la izquierda, el poema verso a verso; al centro, las figuras que organizan sus versos; a la derecha, lo que cada figura hace en la letra. En violeta, los versos que operan."],
};

function paginaMapa(n) {
  const [archivo, pie] = MAPA[n];
  const ruta = path.join(MAPAS, archivo);
  const [w, h] = tamano(ruta);
  const apaisado = w > h;
  const anchoUtil = apaisado ? A4_H - 2 * MARGEN : ANCHO;
  const altoUtil = (apaisado ? A4_W : A4_H) - 2 * MARGEN - 900;
  return { apaisado, hijos: figura(ruta, pie, anchoUtil, altoUtil) };
}

// ------------------------------------------------------------------ el índice: los títulos y la página en que caen
const TITULOS = [];   // se llena al armar el contenido
const PAGINAS = (() => {
  try { return JSON.parse(fs.readFileSync(path.join(AQUI, "paginas.json"), "utf8")); } catch (e) { return {}; }
})();

function indice() {
  // se arma después del contenido: por ahora, un marcador que se reemplaza
  return [INDICE];
}
const INDICE = { marcador: true };

function lineaIndice(t, nivel) {
  const pag = PAGINAS[t];
  return new Paragraph({
    indent: { left: nivel === 2 ? 567 : 0 },
    tabStops: [{ type: TabStopType.RIGHT, position: ANCHO, leader: LeaderType.DOT }],
    spacing: { before: nivel === 1 ? 110 : 0, after: 0, line: 240, lineRule: LineRuleType.AUTO },
    children: [
      new TextRun({ text: t, font: nivel === 1 ? F.media : F.texto, size: nivel === 1 ? 20 : 18, color: TINTA }),
      new TextRun({ children: [new Tab(), pag ? String(pag) : ""], font: F.mono, size: 17, color: GRIS }),
    ],
  });
}

// ------------------------------------------------------------------ el contenido
function contenido() {
  const secciones = [];   // los mapas apaisados cortan la sección vertical
  let actual = [];
  const cerrar = (apaisado = false) => { if (actual.length) secciones.push({ apaisado, hijos: actual }); actual = []; };
  const add = (...b) => actual.push(...b.flat());
  const mapa = (n) => {
    const m = paginaMapa(n);
    if (m.apaisado) { cerrar(false); secciones.push({ apaisado: true, hijos: m.hijos }); }
    else add(salto(), ...m.hijos);
  };

  // ---------------------------------------------------------------- portada
  add(
    new Paragraph({ spacing: { before: 2600 }, children: [new TextRun({ text: "INFORME DE DECISIONES", font: F.mono, size: 18, color: GRIS, characterSpacing: 40 })] }),
    new Paragraph({ spacing: { before: 200, after: 0 }, children: [new TextRun({ text: "Contenida", font: F.ligera, size: 120, color: TINTA })] }),
    new Paragraph({ spacing: { after: 600 }, children: [new TextRun({ text: "acciones para componer una voz", font: F.ligeraCursiva, size: 44, color: GRIS })] }),
    P("Un proyecto tipográfico en homenaje a *Contener una ruina: acciones para desenterrar una voz*, de Rebeca Paz Prada con CreaciónxAcuerpamiento (Artefacto Tatuajes, Sopocachi, La Paz, 22 de agosto de 2026).", { size: 26, spacing: { after: 1600 } }),
    new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 4, color: FILETE, space: 8 } }, children: [
      new TextRun({ text: "La Paz, 30 de septiembre de 2026 · documento de trabajo · hecho con asistencia de inteligencia artificial", font: F.mono, size: 16, color: GRIS })] }),
    salto(),
    new Paragraph({ spacing: { before: 4200 }, alignment: AlignmentType.CENTER, children: runs("«Desenterrar una voz / es desenterrar la mano del que la escribió.»", { font: F.cursiva, size: 30, color: VIOLETA }) }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120 }, children: [new TextRun({ text: "del poema de la lámina", font: F.mono, size: 16, color: GRIS })] }),
  );

  // ---------------------------------------------------------------- resumen e índice
  add(
    H1("Resumen"),
    P("*Contenida* es una familia tipográfica de caja baja y monoespaciada, pensada para hacerse a mano en papel de aluminio repujado. Es un homenaje a *Contener una ruina: acciones para desenterrar una voz*, una obra que partió de la lámina de un libro: el dibujo reconstructivo del ídolo llamado Kochamama, con su pie de imprenta."),
    P("*Contenida* toma de esa lámina el pie, no la imagen. Sus letras salen del texto que acompaña al dibujo. Cada decisión de la obra se traduce en una decisión tipográfica. El aluminio reemplaza al asperón. La caja sale de la retícula de 8 × 7 celdas de la cabeza del ídolo. Lo hallado y lo reconstruido se distinguen siempre. En lugar de pesos, la familia tiene estados de la letra (calco, placa, cinta, frotado, agua y voz), y el peso se mide en frotadas."),
    P("Este informe ordena esas decisiones: de dónde salen, qué teoría las sostiene, qué figuras retóricas las organizan y qué versos del poema las acompañan. Seis mapas esquemáticos conectan conceptos, teoría, retórica y poética en cada etapa del proyecto: la obra, desenterrar, contener, devolver y lo digital."),
    P("El informe incluye también la propuesta de la máquina: una simulación del taller y una aplicación para intervenir la gramática paramétrica de las letras. Las dos están hechas para confrontarlas con el trabajo de la mano, y ninguna de sus formas entra en la caja ni en la fuente."),
    H1("Índice"),
    ...indice(),
  );

  // ---------------------------------------------------------------- 1. introducción
  add(
    H1("1. Introducción: una tipografía que contiene"),
    H2("1.1. La obra"),
    tabla(["", ""], [
      ["Obra", "*Contener una ruina: acciones para desenterrar una voz*"],
      ["Artista", "Rebeca Paz Prada, con CreaciónxAcuerpamiento"],
      ["Fecha", "Sábado 22 de agosto de 2026, 17:00"],
      ["Lugar", "Artefacto Tatuajes, local 12 de un edificio sobre la avenida Arce (Sopocachi, La Paz). La pieza ocurrió en el patio, en una piscina de azulejo vacía y en desuso"],
      ["Formato", "Video en bucle y acción en vivo. El público estuvo parado dentro y fuera de la piscina"],
    ], [1800, ANCHO - 1800], { mono: [0] }),
    P("En la obra, placas de papel de aluminio repujado se apoyan sobre el cuerpo, con piel a la vista entre una y otra. La figura tiene los ojos y la boca tapados con cinta y se mueve apenas, como la piedra. Un video en bucle, filmado en la misma piscina, se proyecta a través de una bandeja con un dedo de agua y llega a la pared temblando, verde y en trapecio. Rebeca toca el agua y la imagen se deforma. Al final de cada ciclo, de la boca tapada sale una placa: un signo, no un sonido.", { spacing: { before: 200 } }),
    H2("1.2. Una lámina, no una piedra"),
    P("La obra no parte del monolito sino de su registro: una lámina desplegable de un libro, con el ídolo en dos vistas. El pie de la lámina dice:"),
    cita("EL IDOLO KOCHAMAMA, según Posnansky, presentado en amplio detalle reconstructivo, según viejas fotografías (hoy está muy erosionado y casi no se ven esos detalles). Su calendario, todavía no bien interpretado, es distinto del de la Puerta del Sol y muestra motivos mucho más antiguos. Suponemos que originariamente se encontraba en Pumapuncu, en el lugar en donde luego se puso la Puerta de la Luna."),
    P("El pie confiesa tres cosas:"),
    numerada("el dibujo es una reconstrucción hecha desde fotografías viejas, porque la piedra está erosionada;", "confesiones"),
    numerada("su calendario no ha sido bien interpretado;", "confesiones"),
    numerada("se supone que estuvo en otro lugar.", "confesiones"),
    P("El objeto de origen es ilegible, su registro es una hipótesis y lo que codifica nadie lo ha leído. De ahí sale el proyecto.", { spacing: { before: 120 } }),
    H2("1.3. Qué es Contenida"),
    P("*Contenida* es una familia tipográfica de caja baja, monoespaciada, hecha a mano en papel de aluminio. Sus letras salen del pie de la lámina que Rebeca usó. Su pauta sale de la piscina donde ocurrió la obra, y su caja, de la retícula de la cabeza del ídolo. Sus estilos no son pesos: son los estados por los que pasa la letra, del papel a la placa, al cuerpo, al agua y a la pared."),
    P("**El nombre.** Es el participio del verbo del título de Rebeca. Es femenino, como la «Monolita» del boceto y como «la ídolo» del poema. En español, una voz contenida es la que no sale del todo, que es la condición de la voz en la obra. Y en tipografía, contener es lo que hacen la caja y el cuerpo. El subtítulo, *acciones para componer una voz*, juega con *componer*, que se dice de los tipos y de la música."),
    P("**El nombre no es Kochamama.** El poema lo dice: «le pusieron nombre, / otra manera de enterrar». Ponerle a la fuente el nombre del ídolo sería enterrarlo otra vez."),
    H2("1.4. Método"),
    P("**Primero analógico. Después, digital, solo si cierra.** El proyecto se hace con acciones, como la obra. Las acciones se documentan en tres cuadernos con verbos de la obra: *Desenterrar* (acciones 0 a 3), *Contener* (4 a 7) y *Devolver* (8 a 12). Cada acción lleva el verso del poema que le corresponde, la decisión de la obra con la que rima, los materiales, los pasos y lo que queda registrado."),
    P("Las referencias de método son dos tesis de maestría en Diseño Gráfico de la Rhode Island School of Design. Una es *EthnoGraphemes: Scripts as Vessels for Culture*, de Vaishnavi Mahendran (2020). La otra es *Afrography: Scripting Futures Anchored in Culture & Community*, de Osmond Tshuma (2025). De ellas se toman métodos, no su misión (§2)."),
    P("**La máquina, para confrontar.** Una simulación hecha con código propone su versión de cada acción. Una aplicación deja intervenir la gramática de las letras en el navegador. Las dos sirven para discutir con la mano; ninguna forma que producen entra en la caja (§8)."),
    H2("1.5. Cómo leer los mapas"),
    P("Los mapas de este informe toman su modo de dibujar de cuatro referencias: un plano técnico con haces de líneas finas, vasijas rayadas y una ficha en la esquina; un análisis espacial de borde con rayado vertical rojo; un haz de líneas con rótulos en sus puntas; y una red de círculos y líneas sobre un plano urbano. Todo lo demás viene de *Contenida*:"),
    vineta("**la tinta** es el violeta del esténcil de tatuaje y el gris del grafito; el verde, que en el proyecto es solo luz, no aparece;"),
    vineta("**los nodos** son celdas de la cabeza del ídolo, un rectángulo dentro de otro, abiertas abajo en su desagüe. Las fuentes son círculos;"),
    vineta("**los haces** de líneas finas conectan: salen juntos de un nodo, se aprietan en un nudo y se abren hacia sus rótulos;"),
    vineta("**el violeta** marca la retórica, la poética y lo reconstruido; **la tinta**, los conceptos y lo hallado; **el gris**, lo que no se toma y la luz;"),
    vineta("**las vasijas** son los cuatro generadores de la gramática, rayados en violeta y acotados en milímetros;"),
    vineta("**la ficha** de cada mapa, abajo a la derecha, dice qué cuenta y con qué tinta, como la ficha de cada placa."),
  );
  mapa(1);

  // ---------------------------------------------------------------- 2. marco
  add(
    H1("2. Marco: de dónde vienen las ideas"),
    H2("2.1. Dos tesis que diseñan para una lengua"),
    P("Las dos tesis diseñan para una lengua. Mahendran trabaja con la comunidad sora, para revitalizar el alfabeto sora sompeng; Tshuma, para su lengua materna, el ndebele del norte. *Contenida* no revitaliza una lengua ni inventa una escritura andina. Es un homenaje a una obra contemporánea y una traducción formal de sus decisiones, en español y con el alfabeto latino. De las tesis toma **métodos**, no su misión."),
    H2("2.2. EthnoGraphemes (Mahendran, 2020)"),
    tabla(["Idea de la tesis", "Qué toma Contenida", "Qué no toma"], [
      ["La escritura como vasija, contra los «frozen arks» de la preservación estática", "La vasija, pero la de la obra: una que no retiene. El juego no alcanza, la tinta se va en cada copia, el agua no repite", "La idea de que la escritura conserva sin pérdida"],
      ["«Metallurgy of Language?»: el lenguaje como metal que se funde; el río de Heráclito", "El metal (aluminio en lugar de plomo) y el agua: «y el agua no repite»", "—"],
      ["Transmodalidad: la lengua «should be seen, felt, and experienced»", "La letra como materia que se toca, se viste y se moja", "—"],
      ["La tipografía sonora, desde la cimática", "El estado *Voz*: la voz hace vibrar el agua que deforma las letras", "Asignar una frecuencia a cada letra: la voz no se codifica, deforma"],
      ["Brookes: las mayúsculas vienen de los monumentos; la hoja de palma pide letra redonda", "Solo caja baja: la letra de la mano. El punzón y el aluminio deciden la forma", "—"],
      ["Brookes: escrituras guardadas en joyas y tatuajes", "El estudio de tatuajes como sede y el esténcil como matriz", "Tatuar: el proyecto se queda en el esténcil, que se lava"],
      ["Morcos, contra las «Alladin typefaces»", "Ningún motivo tiwanacota se pega sobre una letra latina. Del monolito, solo la retícula y el marco vacío", "La «tipografía andina» de catálogo"],
      ["El diccionario de cartas sueltas; *Ellipsis*, lo que queda abierto", "La caja de placas sueltas; el signo «…» en el juego", "—"],
      ["La ética del que viene de afuera", "El protocolo de consentimiento: la Acción 0", "—"],
    ], [3200, 3800, ANCHO - 7000]),
    H2("2.3. Afrography (Tshuma, 2025)"),
    tabla(["Idea de la tesis", "Qué toma Contenida", "Qué no toma"], [
      ["*Sankofa*: «Whose history is this? / Who wrote it? / How was it recorded?»", "Se le hacen a la lámina. Por eso las letras salen del pie, la voz del archivo", "—"],
      ["*Nedmural*: letras extraídas de un mural; solo el arquitecto quedó documentado", "Las letras se extraen del pie tal como están. El colofón nombra la cadena de manos y dice «sin nombre registrado» donde falta", "—"],
      ["*The Great Stone*: once módulos de granito, la restricción de la ruina", "La restricción viene de la ruina moderna: la piscina y el archivo", "Construir letras con módulos"],
      ["La cabeza de Oba, un objeto desplazado", "La cadena de custodia: el colofón y la cadena de estados", "—"],
      ["El cartel de los bronces que el público rompe", "El espécimen digital: tocar deforma el texto", "El estallido: aquí el agua vuelve a su lugar, nunca igual"],
      ["Isiko, documentada en tres libros", "Tres cuadernos con verbos de la obra: *Desenterrar*, *Contener*, *Devolver*", "Inventar signos para una lengua"],
      ["La mesa serif: objeto, signo y objeto otra vez", "El cierre: la fuente vuelve a ser placa (esténcil y repujado)", "—"],
      ["Bil'ak: las máquinas que simplificaron escrituras", "La monoespaciada, a sabiendas: solo en la caja baja latina, que la soporta", "Imponerla a otra escritura"],
      ["La economía del trabajo creativo; «not perfection… a transformation»", "Herramientas libres, acuerdo antes de vender; la placa rota no se corrige", "—"],
    ], [3200, 3800, ANCHO - 7000]),
    H2("2.4. Posnansky, la voz del archivo"),
    P("Arthur Posnansky, *Tihuanacu, la cuna del hombre americano* (tomo I, 1945). El pie lo cita en tercera persona: «según Posnansky». No es una autoridad para el proyecto."),
    P("**Lo que no se toma:** su cronología, su tesis del título, su lectura racial de la historia y sus lecturas de los signos como significados."),
    P("**Lo que se toma, como rima:**"),
    vineta("**La Paz contiene la ruina.** Con piedra de Tiwanaku se levantó la primera parte de la ciudad (p. 59)."),
    vineta("**El desagüe hecho piso.** Las losas de la cloaca máxima sirven de pavimento en la plaza del pueblo (p. 60)."),
    vineta("**El agua que se fue.** El lago que se retiró; el río Desaguadero sin agua (pp. 25-40): un lugar hecho para el agua, del que el agua se fue. La piscina vacía, a escala de un lago."),
    vineta("**El material decide.** Los primeros constructores eligieron el asperón por blando (p. 51), como el aluminio de cocina que cede al punzón."),
    vineta("**Lo que no está se reconstruye.** Las murallas desaparecidas solo se reconstruyen con planos (p. 59): la condición del punteado."),
    H2("2.5. La iconografía Tiwanaku"),
    P("Agüero, Uribe y Berenguer (2003) estudian la escultura lítica de Tiwanaku, con la Kochamama entre sus piezas. Su dibujo de la Kochamama sale de Posnansky (1945, vol. 2, figs. 100, 101a, 101b y 102a). De su análisis se toman estructuras, no motivos:"),
    vineta("**elementos, motivos y figuras:** las partes de la gramática forman signos como los elementos forman motivos;"),
    vineta("**los dobles opuestos varían:** las figuras enfrentadas casi nunca son idénticas. La ¿ no es la ? dada vuelta, ni el 9 el 6;"),
    vineta("**el Personaje Frontal en el pecho y en la espalda** rima con las puertas de la obra (D4); **las cabezas de pez**, con las placas que se leen como peces (D7)."),
    H2("2.6. Dónde Contenida se aparta"),
    numerada("**Lo ilegible.** Las tesis quieren que una escritura se pueda leer y codificar (Noto viene de *no tofu*). *Contenida* no le da valor fonético a ningún signo de la Kochamama y deja que lo que no cabe se vea como celda vacía: el *tofu*. No por gusto de la pérdida, sino para no fingir una lectura que no existe.", "aparta"),
    numerada("**La comunidad.** Aquí no es una lengua y sus hablantes: son las personas de la obra (Rebeca, CreaciónxAcuerpamiento, el estudio que prestó su patio). Con ellas se acuerda el proyecto.", "aparta"),
    numerada("**La ruina.** La fuente de forma es la ruina moderna (la piscina) y el archivo (el pie). La piedra tiwanacota solo presta su manera de contener: una retícula de celdas vacías.", "aparta"),
  );
  mapa(2);

  // ---------------------------------------------------------------- 3. la obra
  add(
    H1("3. La obra, decisión por decisión"),
    P("Las decisiones de la obra, numeradas D1 a D16, salen del texto de la crónica, de los dos videos, de las fotos y de la lámina. Cada una tiene su traducción tipográfica y una razón por la que rima."),
    tabla(["Nº", "La obra", "Contenida", "Por qué rima"], [
      ["D1", "Partir de la lámina y no de la piedra", "Las letras salen del pie de la lámina", "Las dos parten del registro: Rebeca toma la imagen; *Contenida*, el texto"],
      ["—", "El pie confiesa un dibujo reconstructivo", "Hallado continuo y reconstruido punteado, en todos los estados", "La letra cumple la confesión que el dibujo no cumple"],
      ["—", "El calendario sin interpretar", "No se traduce ningún signo; las diez cifras son todas reconstruidas", "Lo que mide el tiempo es lo que no se sabe leer"],
      ["D2", "Asperón → papel de aluminio", "Matrices de aluminio repujado; solo caja baja", "Material doméstico y letra de la mano; el tipo de plomo también era un relieve en espejo"],
      ["D3", "Placas sueltas, con piel entre ellas", "Cada letra es un tipo móvil; entre palabras, una celda vacía", "Componer es distribuir placas sobre un soporte"],
      ["D4", "Puertas en el pecho y la espalda", "La tapa de la caja: una puerta sobre la celda 1", "*Portada* viene de *puerta*"],
      ["D5", "Iconografía interpretada, no copiada", "Del monolito, solo la retícula y la celda vacía", "Rebeca interpreta; *Contenida* toma el marco vacío"],
      ["D6", "La piscina vacía en un estudio de tatuajes", "La piscina nombra las líneas; el violeta del esténcil es la tinta", "Un contenedor vacío recibe a otro"],
      ["D7", "Placas en el fondo, como peces", "No se dibujan peces", "El signo «pez» llega sin copiarlo"],
      ["D8", "La bandeja con un dedo de agua", "El estado *Agua*", "La imagen llega pasando por el agua que le falta al lugar"],
      ["D9", "Escenario, pantalla y tema", "La pared frotada es el papel del calco", "La piscina escribe, sostiene y recibe la letra"],
      ["D10", "El bucle", "Frotar hasta que no se lea, y repujar otra", "«Termina y empieza»"],
      ["D11", "Moverse como la piedra: apenas", "El temblor de la mano; fustes en tres planos", "El cuerpo escribe sobre la letra"],
      ["D12", "Ojos y boca tapados con cinta", "No hay Regular; el estado *Cinta*", "Ninguna cara neutra"],
      ["D13", "De la boca sale una placa", "El signo final ¶, hecho con los dedos", "«Un signo / hecho con las manos, / ninguna palabra»"],
      ["D14", "Un canto que no se entiende", "El estado *Voz*; sin exclamación", "La voz aparece como deformación"],
      ["D15", "Tocar el agua deforma la imagen", "El agua tocada; en lo digital, tocar deforma", "«La misma diosa dos veces / y ninguna igual»"],
      ["D16", "El líquido negro que chorrea", "Toda cuenca se abre abajo; solo gotea lo que mira abajo", "«Ningún contenedor aguanta lo que contiene»"],
    ], [700, 2500, 3000, ANCHO - 6200], { mono: [0] }),
    H2("3.1. La cadena de desplazamientos"),
    cita("piedra borrada → fotografía vieja → dibujo reconstructivo → escaneo → repujado en aluminio → cuerpo → video → charco → pared de azulejo"),
    P("Cada paso pierde materia y gana luz. Todo en la obra es un continente (el monolito, la piscina, el recipiente, el cuerpo), y ninguno retiene lo que le ponen adentro. La familia tipográfica es esa cadena: cada estado es un eslabón (§6)."),
    H2("3.2. Lo que no se usa"),
    vineta("La hipótesis sobre los nombres del edificio y el Litoral, que la crónica dejó afuera por no estar comprobada."),
    vineta("Las lecturas rituales: no se ritualiza nada. La coincidencia material que sí se usa es el desagüe."),
    vineta("Las fotos de la obra y los videos: son imágenes de Rebeca y de su cuerpo. No se suben al repositorio sin su permiso."),
  );
  mapa(3);

  // ---------------------------------------------------------------- 4. el sistema
  add(
    H1("4. El sistema"),
    H2("4.1. Nueve reglas"),
    numerada("**De la lámina se toma el pie, no la imagen.** Rebeca tomó lo que la lámina muestra; la tipografía toma lo que la lámina dice.", "reglas"),
    numerada("**Lo hallado y lo reconstruido se distinguen siempre:** continuo y punteado, en el calco, en el repujado y en todos los estados. Es la convención del dibujo arqueológico, la que la lámina no cumple.", "reglas"),
    numerada("**La forma la decide el material.** El punzón sobre el aluminio no permite ángulos agudos sin romper. Una placa rota no se corrige: se registra y se guarda.", "reglas"),
    numerada("**Solo caja baja.** Las mayúsculas latinas son letras de monumento, y el pie escribe en mayúsculas justamente el nombre impuesto: «EL IDOLO KOCHAMAMA».", "reglas"),
    numerada("**Monoespaciada: una letra, una celda,** de 0,84 de ancho por alto. La «m» llena su celda y la «i» queda rodeada de piel.", "reglas"),
    numerada("**No hay Regular.** La figura de la obra no tiene rostro; la familia no tiene una cara neutra. En español, el *ojo* del tipo es su cara de imprimir.", "reglas"),
    numerada("**El juego cabe en 56 celdas; lo que no cabe se ve como celda vacía.**", "reglas"),
    numerada("**Primero la mano, después lo digital, y lo digital vuelve a pasar por el agua.**", "reglas"),
    numerada("**De la piscina no se saca nada.** «Nos fuimos con las manos secas, / que es como se sale de todas las ruinas.» Tampoco hay letras hechas por una máquina en lugar de la mano.", "reglas"),
    H2("4.2. El pie: 30 hallados y 25 reconstruidos"),
    P("El pie trae **30 de los 55 signos** del juego: 26 letras en caja baja, contando las acentuadas, y 4 signos de puntuación. Faltan 25: la ñ, la w, la x y la z; é, ó y ü; las diez cifras; y ; : ¿ ? « » — …"),
    P("Dos hallazgos salen de contar, no de diseñar:"),
    vineta("**Con las letras halladas se escriben 31 de los 42 versos del poema.** La primera palabra ya necesita una hipótesis: la ó de «quedó». *Salvó* y *opinión* solo se escriben con letras reconstruidas. Y la z de *voz* hay que rehacerla: la voz no se puede desenterrar del pie."),
    vineta("**El primer signo que se halla no es una letra:** es la coma que sigue a «KOCHAMAMA,», una pausa después del nombre."),
    H2("4.3. La caja de 8 × 7"),
    P("La retícula de la cabeza del ídolo es la única parte de la lámina hecha de contenedores vacíos: 8 columnas por 7 filas. *Contenida* usa su número de celdas y no su contenido."),
    tabla(["Grupo", "Signos", "Cantidad"], [
      ["Letras", "a–z y ñ", "27"], ["Acentuadas", "á é í ó ú ü", "6"], ["Cifras", "0–9", "10"],
      ["Signos", ". , ; : ¿ ? ( ) « » — …", "12"], ["Signo final", "¶", "1"], ["Total", "", "56"],
    ], [2400, ANCHO - 3800, 1400], { mono: [2] }),
    P("**Lo que no cabe:** la exclamación (la voz de la obra no exclama), el guion corto (las palabras no se parten) y las comillas inglesas. Todo eso se ve como el `.notdef`: la celda vacía de la lámina, calcada a mano. Las mayúsculas se escriben con la caja baja.", { spacing: { before: 160 } }),
    H2("4.4. La celda y sus líneas"),
    P("La letra vive en una celda de 0,84 de ancho por alto, la proporción de las celdas de la cabeza. En la foto cercana, la retícula mide 0,81 en los bordes y 0,91 al centro, porque el dibujo curva la cabeza como un cilindro: el 0,84 cae dentro. Las líneas tienen nombres de vasija:"),
    tabla(["Línea", "Qué es", "Desde el fondo"], [
      ["afuera", "Ascendentes", "94,1 mm"], ["borde", "Altura de x", "54,8 mm"], ["fondo", "Base", "0"],
      ["desagüe", "Descendentes", "−30,2 mm"],
    ], [2200, ANCHO - 4400, 2200], { mono: [0, 2] }),
    P("El borde sale de la foto del pie: sus ascendentes miden 1,71 veces la altura de x. La celda cabe en una placa cuadrada de 150 mm.", { spacing: { before: 160 } }),
    H2("4.5. La póliza"),
    P("En la imprenta de tipos móviles, la póliza dice cuántas piezas de cada letra trae una fuente. Aquí la dicta el poema: **94 placas** alcanzan para componer cualquier verso sin repetir placa, y **119** hacen la caja completa. Dentro de un verso ninguna letra se repite igual: cada «a» es una placa distinta. «La misma diosa dos veces / y ninguna igual.»"),
    H2("4.6. El color"),
    tabla(["Color", "Qué es", "De dónde viene"], [
      ["Plata", "La letra: el material", "Las placas de Rebeca"],
      ["Violeta", "La tinta: versos, testigos y lo reconstruido", "El esténcil de tatuaje del estudio"],
      ["Gris grafito", "El frotado", "La pared frotada de la Acción 1"],
      ["Verde", "Solo luz, nunca tinta", "La luz del proyector"],
      ["Blanco", "El azulejo y el papel", "La piscina"],
      ["Piel", "El blanco entre palabras cuando el soporte es un cuerpo", "D3"],
    ], [1900, 4000, ANCHO - 5900], { violeta: [] }),
    H2("4.7. El signo final y el colofón de manos"),
    P("El signo final es `¶`, el calderón: en los manuscritos marcaba dónde empezaba un párrafo; en música, suspende el compás. Aquí va al final de cada texto, un signo de comienzo puesto al final. Se hace con los dedos, sin punzón, y es el único que puede tener otra autora: se le propone a Rebeca que lo haga ella."),
    P("El colofón nombra cada mano de la cadena. Donde no hay nombre, lo dice: «piedra tallada en tiwanaku por manos sin nombre registrado; movida de lugar por manos sin nombre registrado…»."),
  );

  // ---------------------------------------------------------------- 5. la gramática
  add(
    H1("5. La gramática: del pie las medidas, de la obra la forma"),
    P("La anatomía de la letra se construye antes que sus estados, en vectores. Del pie se toman medidas; la forma la dictan parámetros que salen de la obra."),
    H2("5.1. Qué se toma del pie"),
    P("**El testigo de las formas es un sustituto.** La foto de la lámina deja leer y medir el pie, pero no calcarlo: la altura de x mide unos 12 px y la tinta corrida cierra los ojos de la a y de la e. Las formas del testigo salen de una letra de imprenta parecida, Liberation Serif, impresa con tipos de plomo simulados y ampliada en tres generaciones de fotocopia."),
    P("**De la foto, la altura de x.** Enderezadas las cuatro líneas del pie y cortadas sus 336 letras, la foto da medidas: las ascendentes miden 1,71 veces la altura de x (el sustituto, 1,52); las descendentes, 0,43; el trazo, al menos 0,19; el desenfoque, σ = 1,66 px. La gramática toma de ella una sola proporción: la zona de x se achata hasta 1,71, sin mover la base ni la línea de afuera. En la placa, el borde baja de 62 a 55 mm."),
    H2("5.2. Los parámetros"),
    P("Cada parámetro controla una sola cosa y sale de una decisión de la obra. Las medidas van en píxeles del lienzo de la placa, a 4 px por milímetro, o en canales."),
    tabla(["Parámetro", "Valor", "Qué controla", "De dónde sale"], [
      ["canal", "8,9 mm", "El grosor único del trazo, sin contraste", "El punzón y la cinta no modulan (D2, D12)"],
      ["radio_chapa", "0,6 canal", "El radio mínimo de toda curva", "El aluminio se rasga en un ángulo agudo (D2)"],
      ["trapecio", "0,70", "El fondo plano de cada cuenca", "La proyección en trapecio; la bandeja (D8)"],
      ["pared", "0,55", "Cuánto se abomba la pared de la cuenca", "El vaso"],
      ["desague", "3 mm", "La abertura en el fondo de cada cuenca", "«Ningún contenedor aguanta lo que contiene» (D16)"],
      ["hombro", "3", "La tensión de los arcos altos (superelipse)", "La chapa curvada sobre un hombro (D3)"],
      ["hombro_caida", "0,40", "Dónde el arco se vuelve vertical", "El testigo de la n, a ojo"],
      ["facetas, quiebre", "3 planos, 1,6°", "Cada fuste en tres planos, apenas quebrados", "«Moverse como se mueve la piedra, es decir, apenas» (D11)"],
      ["asiento", "2 y 0,9 canales", "El pie del fuste se ensancha hacia el fondo", "El peso se asienta en la tierra"],
      ["intemperie", "0,12 canal", "El radio con que se gastan las esquinas", "«Hoy está muy erosionado» (el pie)"],
      ["alivio", "0,28 canal", "El rebaje en cada rincón agudo", "Que el aluminio no se desgarre (D2)"],
      ["gancho_fin", "105°", "Dónde termina el gancho que suelta la gota", "Que la gota cuelgue libre"],
      ["gota", "1,25, 0,3 y 0,55 canal", "La gota: masa, caída y cuello. Solo gotea lo que mira abajo", "El líquido que chorrea de la boca (D16)"],
      ["sifon", "0,6 canal", "El cuello que une dos cuencas (g, 8)", "Vasos comunicantes"],
      ["cinta, punto", "1 canal", "El ancho de la cinta y el lado del punto", "La cinta que tapó ojos y boca (D12)"],
    ], [1750, 1500, 3000, ANCHO - 6250], { mono: [0, 1] }),
    P("**Una condición geométrica que es también material:** si una curva tiene un radio menor que medio canal, el contorno interior se cruza. Es la misma curva en la que el aluminio se rasga. `radio_chapa` cumple las dos.", { spacing: { before: 160 } }),
    H2("5.3. Las partes y los cuatro generadores"),
    P("Cuatro letras dan las partes: la **o**, la cuenca (arriba el ojo del pie; abajo pared, fondo plano y desagüe); la **l**, el fuste en tres planos con su asiento; la **n**, el hombro que sale del fuste y baja como otro fuste; la **a**, el gancho que gotea. Con esas partes, más el punto (un trozo cuadrado de cinta), la tilde en gota, la onda del agua tocada, la recta y el alivio, se arman los 55 signos."),
    ...figura(path.join(SALIDA, "20_gramatica.png"), "Los cuatro generadores: el testigo del pie con sus medidas, las curvas maestras, el cuerpo en vectores, el calco y la cinta puesta y arrancada. Propuesta de la máquina.", ANCHO),
    H2("5.4. De cuatro a cincuenta y cinco"),
    P("Lo que falta se arma por analogía, dejando dicho de qué letras sale cada parte: é y ó con la tilde de á, í y ú; la ñ, de la n con la onda; la w, de dos v; la z, con dos alivios en sus rincones. **Los dobles opuestos varían**, como en la litoescultura de Tiwanaku: la ¿ no es la ? dada vuelta, ni el 9 el 6, porque la gravedad no se da vuelta. La gota cae siempre hacia abajo y el terminal que mira arriba termina en un corte. Cada cifra vive en su celda, un rectángulo dentro de otro, con desagüe."),
    ...figura(path.join(SALIDA, "21_gramatica_caja.png"), "Los 55 cuerpos base en la caja de 8 × 7: en tinta lo hallado, en violeta lo reconstruido. La celda 56 se hace con los dedos. Propuesta de la máquina.", ANCHO),
  );
  mapa(4);

  // ---------------------------------------------------------------- 6. los estados
  add(
    H1("6. Los estados: una familia sin pesos"),
    P("No hay Light ni Bold. Cada estilo es un estado de la letra en la cadena de la obra, y ninguno es la versión normal de los demás."),
    tabla(["Estado", "Acción", "Cómo se hace", "Rima con"], [
      ["Calco", "3", "Calco sobre el frotado de la pared: continuo lo hallado, punteado lo reconstruido. Todo contorno se abre abajo", "El dibujo reconstructivo, hecho desde fotos viejas"],
      ["Placa", "4", "Repujado por el reverso, en espejo, con un punzón de bola de 1 mm: por el reverso un canal hundido, por el anverso un relieve", "Asperón → aluminio"],
      ["Cinta", "6", "La letra puesta con masking sobre plástico negro: no curva, se pliega", "La cinta sobre ojos y boca"],
      ["Frotado 01 … n", "8", "Papel y grafito sobre la placa: cada frotada aplasta el relieve y sale más clara", "La pared frotada; «otra manera de enterrar»"],
      ["Agua", "9", "La placa en el fondo de una bandeja, reflejada hacia un azulejo; quieta o tocada", "La proyección a través del agua"],
      ["Voz", "10", "El agua movida por la voz que lee el poema", "El canto que no se entiende"],
    ], [1700, 900, 4000, ANCHO - 6600], { mono: [1] }),
    H2("6.1. El peso se mide en frotadas"),
    P("La serie va del *Frotado 01*, el más cargado de grafito, al último que se lee. Es la cadena de la obra hecha escala tipográfica: cada frotada se lleva un poco del relieve. En la presentación, los frotados se reparten en orden de llegada: quien llega primero recibe el *Frotado 01*; quien llega último, casi nada."),
    H2("6.2. En pausa"),
    P("*Piel* (la placa vestida el tiempo de un bucle), *Copia* (el hectógrafo) y *Azulejo* (la luz sobre la pared) salieron de la cadena. Sus acciones siguen escritas, por si se retoman."),
    ...figura(path.join(SALIDA, "12_cadena_08.jpg"), "Una letra de punta a punta: la «a» (celda 8) en el pie, la gramática, el calco, la placa por las dos caras, la cinta, el frotado, el agua y la voz. Propuesta de la máquina.", ANCHO),
  );
  mapa(5);

  // ---------------------------------------------------------------- 7. el taller
  add(
    H1("7. El taller: trece acciones en tres cuadernos"),
    P("Cada acción lleva su verso y la decisión de la obra con la que rima. Los materiales, los pasos, el registro y la seguridad están en `04_taller_analogico.md`, y las plantillas para imprimir, en `esquemas/plantillas_imprimibles.pdf`."),
    tabla(["Acción", "Verso", "Rima con"], [
      ["**Desenterrar**", "", ""],
      ["0 · Pedir", "«Vuelve sin que la llames.»", "La obra se hizo junto a otros, en un lugar prestado"],
      ["1 · Medir y frotar", "«Quedó el contenedor / de lo que ya no está.»", "D6 y D9; de la piscina no se saca nada"],
      ["2 · Desenterrar el pie", "«A la ídolo la desenterraron, / le pusieron nombre, / otra manera de enterrar.»", "D1 y *Nedmural*"],
      ["3 · Calcar y reconstruir", "«No se salvó la piedra, / solo la opinión sobre ella.»", "El dibujo reconstructivo"],
      ["**Contener**", "", ""],
      ["4 · Repujar", "«de la boca sale un signo / hecho con las manos»", "D2 y D3"],
      ["5 · Llenar la caja", "«ningún contenedor aguanta lo que contiene»", "D5 y D4"],
      ["6 · Encintar", "«A la boca la taparon, a las manos no,»", "D12 y el plástico negro"],
      ["7 · El signo final", "«Al final del ciclo, / de la boca sale un signo / hecho con las manos»", "D13"],
      ["**Devolver**", "", ""],
      ["8 · Frotar", "«otra manera de enterrar»", "La Acción 1; cada copia se aleja de la piedra"],
      ["9 · Pasar por el agua", "«Tocas el agua y la diosa se deforma. / Todos los archivos funcionan así.»", "D8 y D15"],
      ["10 · Dar voz", "«Y es que lo que vuelve, vuelve escrito; / pocas veces vuelve hablado.»", "D14 y la tipografía sonora"],
      ["11 · Componer", "«Cada vuelta pasa por el agua / y el agua no repite»", "D9, D7 y D10"],
      ["12 · Cerrar la caja", "«Nos fuimos con las manos secas, / que es como se sale de todas las ruinas.»", "La regla 9"],
    ], [2500, 4200, ANCHO - 6700], { mono: [0], violeta: [1], cursiva: [1] }),
  );

  // ---------------------------------------------------------------- 8. la máquina
  add(
    H1("8. La propuesta de la máquina"),
    H2("8.1. Qué hace y qué supone"),
    P("La simulación (`simulacion/`) arma el testigo del pie y la gramática, y corre seis estados sobre las 56 celdas y las 119 placas. La semilla es fija, el 22 de agosto de 2026: el resultado es siempre el mismo, y cambiarla es cambiar de mano. Es una hipótesis hecha con código, para confrontarla con la de la mano."),
    P("**Lo que tuvo que suponer:** el testigo sustituto; el cuerpo del pie (8,5 puntos); la piscina (azulejo de 150 mm, junta de 3 mm); la celda (0,84); cuánto relieve se lleva cada frotada (entre un 5 y un 9 %); la voz (no es la de nadie); y el signo final, una presión de pulgar genérico, porque la máquina no tiene dedos."),
    H2("8.2. Lo que apareció sin diseñarlo"),
    vineta("**Las hipótesis pesan menos.** Las halladas se leen, en promedio, hasta la frotada 22,1; las reconstruidas, hasta la 9,8. Hechas a puntos, tienen menos relieve que tomar el grafito."),
    vineta("**En el agua, las hipótesis se ven menos.** El contraste de la letra en el agua quieta es de 4,07 en las halladas y de 1,34 en las reconstruidas."),
    vineta("**El tiempo.** 86 horas de repujado para las 119 placas, contando las que se rompieron; el plan estimaba entre 30 y 40. Se rompieron 12: 6 de 93 halladas y 6 de 25 reconstruidas."),
    vineta("**La cinta pierde la gravedad.** 444 tramos y 303 pliegues para los 55 signos, sin gotas ni asientos."),
    vineta("**El signo final no se frota:** el domo del pulgar es liso y el papel lo acompaña. Da 0 frotadas legibles."),
    vineta("**La intemperie borra las celdas de las cifras.** En la aplicación, si la intemperie pasa de 0,175 canales se come el trazo de la celda, que mide 0,35 canal."),
    H2("8.3. Lo que la máquina no sabe"),
    P("Qué letra tiene el pie en su tamaño real. Cómo tiembla una mano que se cansa y duda. Cómo se rompe de verdad el aluminio. Cuánto se lleva el grafito. Cómo se despega la cinta. El agua de la simulación rebota una sola vez, y la voz no es la tuya."),
    H2("8.4. La gramática en el navegador"),
    P("La aplicación (`aplicacion/`) arma la gramática en JavaScript, en el mismo orden que Python, y deja mover la altura de x y los 20 parámetros. Cada uno lleva su valor en milímetros y canales, qué controla y de dónde sale. Tiene cuatro vistas:"),
    vineta("**Caja:** los 55 cuerpos, en tinta y violeta, que se vuelven a armar al mover un parámetro."),
    vineta("**Signo:** un signo con sus partes: testigo, cuerpo, ejes, nodos, alivios, gotas y asientos."),
    vineta("**Texto:** un verso compuesto celda por celda, que puede ir sobre la piscina: las juntas de los azulejos cortan la letra."),
    vineta("**Estados:** los seis simuladores sobre un signo, con el frotado hasta que la letra no se lee y el agua tocada."),
    P("Los ajustes vuelven a Python como `parametros.json` (`simular.py --parametros`). Con los mismos ajustes, los 55 cuerpos de la página y los de Python coinciden hasta el píxel del borde, porque la página repite el azar de las recetas. Las versiones guardadas en la página las puede leer Claude para correr la simulación con ellas."),
  );
  const app = path.join(AQUI, "img", "aplicacion.png");
  if (fs.existsSync(app)) add(...figura(app, "La aplicación: la ficha de parámetros y la caja de 8 × 7. Propuesta de la máquina.", ANCHO));

  // ---------------------------------------------------------------- 9. retórica y poética
  add(
    H1("9. Retórica y poética"),
    P("La retórica ordena cómo el proyecto dice lo que dice; la poética, cómo el poema decide la forma. En *Contenida* los versos no ilustran: cada acción lleva uno, y varios se vuelven medidas."),
    H2("9.1. Las figuras del proyecto"),
    tabla(["Figura", "En el poema o la obra", "En la letra"], [
      ["Anáfora y gradación", "«es decir, apenas, es decir, temblor, / es decir, un presente continuo»", "El temblor de la mano; tres planos a 1,6°"],
      ["Paradoja", "«ningún contenedor aguanta lo que contiene»", "Toda cuenca se abre abajo, en un desagüe"],
      ["Derivación", "enterrar, desenterrar; contener, *Contenida*", "El nombre; el primer cuaderno"],
      ["Apóstrofe", "«Tocas el agua y la diosa se deforma»", "El agua tocada; en lo digital, tocar deforma"],
      ["Prosopopeya", "«La tierra se dio de beber a sí misma»", "La gota: solo gotea lo que mira abajo"],
      ["Repetición y ciclo", "«Termina y empieza, / termina y empieza»", "El bucle, las frotadas, la generación 2"],
      ["Antítesis", "«lo que vuelve, vuelve escrito; / pocas veces vuelve hablado»", "Continuo y punteado; la voz que deforma"],
      ["Metáfora", "La letra es una vasija", "Fondo, borde, desagüe y afuera; la cuenca"],
      ["Sinécdoque y metonimia", "El pie por la lámina; la cinta por el rostro tapado", "Las letras salen del pie; el punto de cinta"],
      ["Elipsis", "«No tiene lengua pero igual dice»", "La celda vacía; el signo «…»"],
      ["Etimología", "*Portada* viene de *puerta*; el *ojo* del tipo; *componer*; el *calderón*", "La puerta sobre la celda 1; no hay Regular; ¶"],
      ["Sentencia", "«Todos los archivos funcionan así»", "De la piscina no se saca nada"],
      ["Interrogación retórica", "«Es lo que hacemos con todo, no?»", "La ? se arma sin modelo; la ¿ no es su espejo"],
    ], [2300, 3700, ANCHO - 6000], { mono: [0], violeta: [1], cursiva: [] }),
    H2("9.2. El verso como instrucción"),
    P("Tres versos se vuelven números. «Moverse como se mueve la piedra, / es decir, apenas» se vuelve un quiebre de 1,6° entre los planos del fuste. «Ningún contenedor aguanta lo que contiene» se vuelve un desagüe de 3 mm en cada cuenca. «La misma diosa dos veces / y ninguna igual» se vuelve la póliza de 94 placas, en la que ninguna letra se repite dentro de un verso."),
    P("Otros versos se vuelven orden. «Termina y empieza» pone el signo de comienzo al final. «Nos fuimos con las manos secas» cierra la caja sin sacar nada de la piscina. Y «desenterrar una voz / es desenterrar la mano del que la escribió» deja la mano en el centro: la máquina propone, la mano hace."),
  );
  mapa(6);

  // ---------------------------------------------------------------- 10. lo digital
  add(
    H1("10. Lo digital, si cierra"),
    P("La obra ya migra y no termina en lo digital: repujado, video, agua y pared. La migración de *Contenida* es coherente solo si repite ese lugar: lo digital es un estado más, que vuelve a pasar por el agua y vuelve a ser placa."),
    H2("10.1. Condiciones"),
    numerada("La caja está completa: 56 celdas, 119 placas, 119 fichas.", "digital"),
    numerada("Rebeca está de acuerdo con la versión digital y con su licencia.", "digital"),
    numerada("La procedencia viaja con la fuente: las fichas y el colofón van dentro del archivo.", "digital"),
    numerada("Lo reconstruido sigue punteado en todos los estilos digitales.", "digital"),
    numerada("No hay un estilo limpio ni un Regular: cada estilo sale de un registro físico.", "digital"),
    numerada("La salida vuelve a lo analógico: se proyecta a través del agua y se imprime como esténcil para placas nuevas.", "digital"),
    H2("10.2. Lo que no se hace"),
    vineta("No se publica un máster limpio ni se interpolan pesos."),
    vineta("No se generan letras con inteligencia artificial ni por procedimiento: las variantes son placas."),
    vineta("No se agregan mayúsculas, exclamaciones ni signos fuera de la caja."),
    vineta("No se usa el nombre del ídolo ni signos tiwanacotas, y no se vende sin acuerdo."),
    H2("10.3. Termina y empieza"),
    P("La fuente se imprime en la máquina de esténcil térmico del estudio, y el esténcil sirve de calco para repujar placas nuevas. Esas placas llenan una segunda caja, cuyas fichas dicen «generación 2». Lo digital no termina la cadena: le da la vuelta."),
  );

  // ---------------------------------------------------------------- 11. ética
  add(
    H1("11. Ética, fuentes y pendientes"),
    H2("11.1. Consentimiento y créditos"),
    vineta("**Rebeca primero.** Nada se hace antes de la Acción 0. Si ella no está de acuerdo, el proyecto se detiene o cambia."),
    vineta("**Créditos.** Rebeca Paz Prada y CreaciónxAcuerpamiento van en el colofón, en la forma que ellas elijan; Artefacto Tatuajes, como sede; cada mano de la cadena, con su nombre o con «sin nombre registrado»."),
    vineta("**El cuerpo** de Rebeca no se usa salvo que ella lo proponga. **La piscina** se usa con permiso escrito, y no se saca ni se deja nada."),
    H2("11.2. Lo que no está en el repositorio"),
    P("Las fotos de la obra y los dos videos, la foto de la lámina, el dibujo de la lámina con el poema, el libro de Posnansky y el artículo de Agüero, Uribe y Berenguer. Lo que el proyecto usa de ellos está descrito, y del pie solo se guardan letras sueltas, recortadas."),
    H2("11.3. Asistencia de inteligencia artificial"),
    P("Los textos, los esquemas, la simulación, las láminas, la aplicación y este informe se hicieron con asistencia de inteligencia artificial. Las formas de letra que genera la simulación son la propuesta de la máquina: están hechas para confrontarlas con las de la mano y no entran en la caja ni en la fuente."),
    H2("11.4. Lo que el proyecto no afirma"),
    P("No interpreta la iconografía de Tiwanaku ni el «calendario» de la Kochamama. Los números del sistema son convenios, no lecturas: las 56 celdas y los 30 hallazgos cuentan contenedores y letras. No es una tipografía «andina»: es una tipografía latina de caja baja, hecha con las operaciones de una obra que ocurrió en La Paz."),
    H2("11.5. Pendientes"),
    numerada("Acción 0: hablar con Rebeca y con CreaciónxAcuerpamiento; pedir los permisos del estudio y del edificio.", "pendientes"),
    numerada("Identificar el libro de la lámina y fotografiar el pie de cerca, con luz rasante, para que dé formas y no solo medidas.", "pendientes"),
    numerada("Medir la piscina y regenerar la pauta de calco con la celda en lugar del azulejo.", "pendientes"),
    numerada("Medir en el libro lo que hoy es a ojo: la caída del hombro, el grueso y el fino, y la proporción de la celda.", "pendientes"),
    numerada("Probar el repujado y el frotado: qué papel, qué grafito y cuántas frotadas aguanta una placa.", "pendientes"),
    numerada("Verificar los datos de Posnansky, el nombre del ídolo y la ficha del «vaso».", "pendientes"),
    numerada("Pasar la especificación de la fuente digital (`05`, §5.3) de la tesela a la celda, y revisar en el colofón los estados en pausa (vestida, copiada).", "pendientes"),
    numerada("Confrontar la propuesta de la mano con la de la máquina, placa por placa.", "pendientes"),
  );

  // ---------------------------------------------------------------- referencias y colofón
  add(
    H1("Referencias"),
    P("Agüero Piwonka, Carolina; Mauricio Uribe Rodríguez y José Berenguer Rodríguez (2003). «La iconografía Tiwanaku: el caso de la escultura lítica». *Textos Antropológicos* 14 (2): 47-82."),
    P("Mahendran, Vaishnavi (2020). *EthnoGraphemes: Scripts as Vessels for Culture*. Tesis de maestría en Diseño Gráfico, Rhode Island School of Design."),
    P("Paz Prada, Rebeca, con CreaciónxAcuerpamiento (2026). *Contener una ruina: acciones para desenterrar una voz*. Video en bucle y acción en vivo. Artefacto Tatuajes, La Paz, 22 de agosto."),
    P("Posnansky, Arthur (1945). *Tihuanacu, la cuna del hombre americano / Tihuanacu, the Cradle of American Man*, tomo I. Traducción de James F. Shearer. Nueva York: J. J. Augustin."),
    P("Tshuma, Osmond (2025). *Afrography: Scripting Futures Anchored in Culture & Community*. Tesis de maestría en Diseño Gráfico, Rhode Island School of Design."),
    P("El libro que reproduce la lámina «según Posnansky»: sin identificar."),
    H2("Documentos del proyecto"),
    P("`tipografia/01` a `07` (la obra, las tesis, el sistema, la gramática, el taller, la migración, la ética y Posnansky), `simulacion/informe.md` (la propuesta de la máquina) y `aplicacion/` (la gramática en el navegador)."),
    H1("Colofón"),
    P("Compuesto en Newsreader (Production Type) y Courier Prime (Alan Dague-Greene), las dos con licencia SIL Open Font License e incrustadas en este archivo. Los mapas se dibujan con `tipografia/informe/mapas.py` y el documento se arma con `tipografia/informe/informe.js`."),
    P("Documento de trabajo, hecho con asistencia de inteligencia artificial. Las formas de letra que muestran sus figuras vienen de la simulación: son la propuesta de la máquina y no entran en la caja ni en la fuente."),
    verso("«Termina y empieza, / termina y empieza.» ¶", { antes: 400 }),
  );
  cerrar(false);
  const lineas = TITULOS.filter(([t]) => !["Resumen", "Índice"].includes(t)).map(([t, n]) => lineaIndice(t, n));
  for (const s of secciones) {
    const i = s.hijos.indexOf(INDICE);
    if (i >= 0) s.hijos.splice(i, 1, ...lineas);
  }
  fs.writeFileSync(path.join(AQUI, ".titulos.json"), JSON.stringify(TITULOS.map(([t, n]) => ({ t, n }))));
  return secciones;
}

// ------------------------------------------------------------------ el documento
async function main() {
  const estilos = {
    default: { document: { run: { font: F.texto, size: 21, color: TINTA } } },
    paragraphStyles: [
      { id: "Normal", name: "Normal", run: { font: F.texto, size: 21 },
        paragraph: { spacing: { after: 120, line: 300, lineRule: LineRuleType.AUTO } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: F.ligera, size: 44, color: TINTA }, paragraph: { spacing: { before: 0, after: 280 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: F.media, size: 26, color: TINTA }, paragraph: { spacing: { before: 320, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: F.mono, size: 18, color: GRIS }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
    ],
  };
  const lista = (ref, formato, texto) => ({ reference: ref, levels: [{ level: 0, format: formato, text: texto, alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 567, hanging: 340 } } } }] });
  const numeracion = {
    config: [
      { reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 567, hanging: 283 } }, run: { color: VIOLETA } } }] },
      ...["numeros", "confesiones", "aparta", "reglas", "digital", "pendientes"].map((r) => lista(r, LevelFormat.DECIMAL, "%1.")),
    ],
  };
  const secciones = contenido().map((s) => ({
    properties: {
      page: {
        size: { width: A4_W, height: A4_H, orientation: s.apaisado ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT },
        margin: { top: MARGEN, bottom: MARGEN, left: MARGEN, right: MARGEN },
      },
    },
    headers: { default: encabezado() },
    footers: { default: piePagina() },
    children: s.hijos,
  }));
  const doc = new Document({
    creator: "Contenida",
    title: "Contenida: informe de decisiones",
    description: "Informe de decisiones del proyecto tipográfico Contenida, con seis mapas.",
    styles: estilos,
    numbering: numeracion,
    fonts: fuentes(),
    sections: secciones,
  });
  const destino = path.join(AQUI, "contenida_informe_de_decisiones.docx");
  fs.writeFileSync(destino, await Packer.toBuffer(doc));
  console.log("listo:", destino, secciones.length, "secciones");
}

main().catch((e) => { console.error(e); process.exit(1); });
