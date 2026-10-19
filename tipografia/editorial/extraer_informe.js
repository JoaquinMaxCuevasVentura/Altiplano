/* Saca el texto del informe de decisiones (tipografia/informe/informe.js) a un JSON de bloques,
 * para componerlo en el libro sin copiarlo a mano: si el informe cambia, el libro cambia.
 *
 * Uso (desde tipografia/editorial/):  node extraer_informe.js  →  .cache/informe.json
 *
 * El informe arma un .docx con el paquete docx de npm. Acá ese paquete se reemplaza por uno
 * de mentira que solo anota lo que recibe; con eso se reconstruye cada bloque: títulos,
 * párrafos (con sus marcas *cursiva*, **negrita** y `mono`), versos, citas, notas, listas,
 * tablas y figuras. No hace falta instalar docx ni las fuentes del informe.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const Module = require("module");

const AQUI = __dirname;
const INFORME = path.join(AQUI, "..", "informe", "informe.js");
const SALIDA = path.join(AQUI, ".cache", "informe.json");

// ------------------------------------------------------------------ el docx de mentira
class Anotado { constructor(o) { this.k = this.constructor.name; this.o = typeof o === "string" ? { text: o } : (o || {}); } }
const clases = ["Document", "Paragraph", "TextRun", "Table", "TableRow", "TableCell", "ImageRun", "PageBreak", "Header",
  "Footer", "Tab"];
const docx = {};
for (const c of clases) docx[c] = { [c]: class extends Anotado {} }[c];
docx.Packer = { toBuffer: async () => Buffer.alloc(0) };
const constantes = new Proxy({}, { get: (_, k) => String(k) });
for (const c of ["HeadingLevel", "AlignmentType", "WidthType", "BorderStyle", "ShadingType", "PageNumber", "LevelFormat",
  "PageOrientation", "VerticalAlign", "LineRuleType", "TabStopType", "LeaderType"]) docx[c] = constantes;

// ------------------------------------------------------------------ cargar el informe sin correr main()
function cargar() {
  let src = fs.readFileSync(INFORME, "utf8");
  // runs() deja anotado el texto con sus marcas, para no reconstruirlas desde las fuentes
  const i = src.indexOf("function runs(");
  const j = src.indexOf("  return out;\n}", i);
  if (i < 0 || j < 0) throw new Error("no encuentro runs() en el informe");
  src = src.slice(0, j) + "  out.__md = String(texto); out.__base = base; for (const r of out) r.__grupo = out;\n" + src.slice(j);
  src = src.replace(/main\(\)\.catch[\s\S]*$/, "module.exports = { contenido, MAPA, F, VIOLETA, GRIS };\n");
  const m = new Module(INFORME, null);
  m.filename = INFORME;
  m.paths = Module._nodeModulePaths(path.dirname(INFORME));
  const requerir = m.require.bind(m);
  m.require = (id) => (id === "docx" ? docx : requerir(id));
  const envoltura = Module.wrap(src);
  const fn = require("vm").runInThisContext(envoltura, { filename: INFORME });
  fn.call(m.exports, m.exports, m.require, m, INFORME, path.dirname(INFORME));
  return m.exports;
}

// ------------------------------------------------------------------ de los párrafos anotados a bloques
function main() {
  const I = cargar();
  const { F, VIOLETA, GRIS } = I;
  const secciones = I.contenido();

  // los grupos de runs de un párrafo, en orden: cada grupo es un texto con marcas
  function grupos(hijos) {
    const out = [];
    let ultimo = null;
    for (const h of hijos || []) {
      if (h.k !== "TextRun") continue;
      if (h.__grupo) {
        if (h.__grupo !== ultimo) { out.push({ md: h.__grupo.__md, base: h.__grupo.__base || {} }); ultimo = h.__grupo; }
      } else {
        out.push({ md: String(h.o.text || ""), base: { font: h.o.font, size: h.o.size, color: h.o.color }, suelto: true });
        ultimo = null;
      }
    }
    return out;
  }

  const bloques = [];
  let figura = null;            // la imagen espera su pie en el párrafo siguiente
  const mapas = Object.fromEntries(Object.entries(I.MAPA).map(([n, [archivo]]) => [archivo, Number(n)]));

  for (const s of secciones) {
    for (const h of s.hijos) {
      if (!h || h.marcador) continue;
      if (h.k === "Table") {
        const filas = h.o.rows.map((fila) => fila.o.children.map((celda) => {
          const ps = celda.o.children.map((p) => grupos(p.o.children));
          const base = (ps[0] && ps[0][0] && ps[0][0].base) || {};
          return {
            md: ps.map((g) => g.map((x) => x.md).join("")).join("\n"),
            mono: base.font === F.mono, violeta: base.color === VIOLETA, cursiva: base.font === F.cursiva,
            cabeza: !!fila.o.tableHeader,
          };
        }));
        const cabeza = filas.length && filas[0][0].cabeza ? filas.shift().map((c) => c.md) : null;
        bloques.push({ t: "tabla", cabeza, filas, anchos: h.o.columnWidths });
        continue;
      }
      if (h.k !== "Paragraph") continue;
      const o = h.o;
      const hijos = o.children || [];
      if (hijos.some((x) => x.k === "PageBreak")) { bloques.push({ t: "salto" }); continue; }
      const img = hijos.find((x) => x.k === "ImageRun");
      if (img) {
        figura = { t: "figura", archivo: img.o.altText.name, ancho: img.o.transformation.width, alto: img.o.transformation.height };
        continue;
      }
      if (o.heading) {
        const t = hijos.map((x) => x.o.text).join("");
        bloques.push({ t: { HEADING_1: "h1", HEADING_2: "h2", HEADING_3: "h3" }[o.heading], md: t });
        continue;
      }
      const g = grupos(hijos);
      if (figura) {                                   // el pie: «Figura N. » y el texto
        const n = Number(String(g[0].md).replace(/[^0-9]/g, ""));
        figura.n = n;
        figura.pie = g.slice(1).map((x) => x.md).join("");
        if (mapas[figura.archivo]) figura.mapa = mapas[figura.archivo];
        bloques.push(figura);
        figura = null;
        continue;
      }
      if (!g.length) continue;
      const base = g[0].base || {};
      const md = g.map((x) => x.md).join("");
      if (o.numbering) bloques.push({ t: "item", lista: o.numbering.reference, nivel: o.numbering.level || 0, md });
      else if (base.color === VIOLETA && base.font === F.cursiva) bloques.push({ t: "verso", md });
      else if (base.color === GRIS && base.size === 20) bloques.push({ t: "cita", md });
      else if (base.font === F.mono && base.size === 16 && base.color === GRIS) bloques.push({ t: "nota", md });
      else if (g.every((x) => x.suelto)) bloques.push({ t: "suelto", md, base, align: o.alignment });
      else bloques.push({ t: "p", md, align: o.alignment });
    }
  }
  fs.mkdirSync(path.dirname(SALIDA), { recursive: true });
  fs.writeFileSync(SALIDA, JSON.stringify(bloques, null, 1));
  const cuenta = {};
  for (const b of bloques) cuenta[b.t] = (cuenta[b.t] || 0) + 1;
  console.log("listo:", path.relative(process.cwd(), SALIDA), JSON.stringify(cuenta));
}

main();
