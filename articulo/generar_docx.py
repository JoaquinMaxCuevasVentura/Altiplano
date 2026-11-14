"""Genera el .docx del artículo con las normas de Estudios Bolivianos, la revista
para la que se escribió. Hasta elegir revista, es la versión de trabajo.

Normas aplicadas: tamaño carta, márgenes de 2,5 cm, Times New Roman 12,
interlineado 1,5 (notas al pie en 10 pt, interlineado sencillo).

Uso (desde la raíz del repositorio):
    pip install pypandoc_binary python-docx
    python3 articulo/generar_docx.py [archivo.md] [--plantilla]

La plantilla de estilos se arma cada vez en una carpeta temporal, a partir de
este mismo guion. La copia guardada, plantilla_estudios_bolivianos.docx, solo
se reescribe con --plantilla. El .docx tampoco se toca si su contenido no
cambia, para que git no muestre diferencias donde no las hay.

Sin argumento lee articulo/articulo_cosecha_de_piedras.md (versión definitiva)
y escribe el .docx del mismo nombre; con un argumento convierte ese archivo
(por ejemplo, articulo/articulo_altiplano.md, la versión 3). Al final informa
la extensión en caracteres con espacios y en palabras, con bibliografía y notas
(cada revista pone su límite: véase reports/Convocatorias abiertas para el
artículo.md), y las palabras de cada resumen.

Las figuras van en bloques ::: {custom-style="Figura"} con la imagen, por
ejemplo ![](figuras/figura_1.png){width=14cm}, seguidos de su pie en un
bloque ::: {custom-style="Pie de figura"} (véase figuras/LEEME.md). El
epígrafe va en un bloque ::: {custom-style="Epígrafe"}.
"""

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import pypandoc
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt

BASE = Path(__file__).resolve().parent
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
MD = Path(ARGS[0]).resolve() if ARGS else BASE / "articulo_cosecha_de_piedras.md"
DOCX = MD.with_suffix(".docx")
REF = BASE / "plantilla_estudios_bolivianos.docx"
FONT = "Times New Roman"


def set_font(style, size, bold=None, italic=None):
    style.font.name = FONT
    style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(attr), FONT)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if fonts.get(qn(attr)) is not None:
            del fonts.attrib[qn(attr)]
    # Texto en negro (la plantilla de pandoc colorea los títulos).
    color = rpr.find(qn("w:color"))
    if color is not None:
        rpr.remove(color)


def set_spacing(style, line=1.5, before=0, after=6):
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)


def partes(docx):
    """El contenido de un .docx sin las fechas de creación y de guardado."""
    with zipfile.ZipFile(docx) as z:
        out = {}
        for name in sorted(z.namelist()):
            data = z.read(name)
            if name == "docProps/core.xml":
                data = re.sub(rb"<dcterms:(created|modified)[^>]*>[^<]*</dcterms:\1>", b"", data)
            out[name] = data
        return out


def reemplazar_si_cambia(nuevo, destino):
    """Copia nuevo sobre destino solo si su contenido es distinto. Dice si lo copió."""
    if destino.exists() and partes(nuevo) == partes(destino):
        return False
    shutil.copyfile(nuevo, destino)
    return True


def build_reference(ref):
    data = subprocess.run(
        [pypandoc.get_pandoc_path(), "--print-default-data-file", "reference.docx"],
        check=True, capture_output=True,
    ).stdout
    ref.write_bytes(data)
    doc = Document(str(ref))
    styles = {s.name: s for s in doc.styles}
    for name in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text",
                 "Abstract", "Author", "Date", "Bibliography", "Table", "Definition",
                 "Definition Term", "Image Caption", "Caption", "Table Caption",
                 "Figure", "Captioned Figure"):
        if name in styles:
            set_font(styles[name], 12)
            set_spacing(styles[name])
    for name, size in (("Title", 14), ("Subtitle", 12), ("Heading 1", 12),
                       ("Heading 2", 12), ("Heading 3", 12), ("Heading 4", 12)):
        if name in styles:
            set_font(styles[name], size, bold=True, italic=False)
            set_spacing(styles[name], before=12, after=6)
    for name in ("Image Caption", "Caption", "Table Caption"):
        if name in styles:
            set_font(styles[name], 10, italic=False)
            set_spacing(styles[name], line=1.0, before=3, after=12)
    for name in ("Figure", "Captioned Figure", "Image Caption"):
        if name in styles:
            styles[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Estilos propios para las figuras: la imagen y su pie.
    for name, size, line, before, after in (("Figura", 12, 1.0, 12, 3),
                                            ("Pie de figura", 10, 1.0, 3, 12)):
        style = styles.get(name) or doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = styles["Normal"]
        set_font(style, size, italic=False)
        set_spacing(style, line=line, before=before, after=after)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style.paragraph_format.keep_with_next = name == "Figura"
    # Estilo propio para el epígrafe: 11 pt, sangrado a la izquierda.
    style = styles.get("Epígrafe") or doc.styles.add_style("Epígrafe", WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = styles["Normal"]
    set_font(style, 11, italic=False)
    set_spacing(style, line=1.0, before=0, after=6)
    style.paragraph_format.left_indent = Cm(7)
    if "Footnote Text" in styles:
        set_font(styles["Footnote Text"], 10)
        set_spacing(styles["Footnote Text"], line=1.0, after=2)
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Cm(2.5))
    doc.save(str(ref))


def convert(ref, salida):
    pypandoc.convert_file(
        str(MD), "docx", outputfile=str(salida),
        extra_args=[f"--reference-doc={ref}", f"--resource-path={BASE}"],
    )
    doc = Document(str(salida))
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Cm(2.5))
        # Word exige estos tres atributos de los márgenes; pandoc no los escribe.
        section.header_distance = Cm(1.25)
        section.footer_distance = Cm(1.25)
        section.gutter = Cm(0)
    # Tablas en 10 pt con interlineado sencillo para que quepan en la caja.
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.line_spacing = 1.0
                    par.paragraph_format.space_after = Pt(2)
                    for run in par.runs:
                        run.font.size = Pt(10)
                        run.font.name = FONT
    doc.save(str(salida))


def report():
    doc = Document(str(DOCX))
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    with zipfile.ZipFile(DOCX) as z:
        notes_xml = z.read("word/footnotes.xml").decode("utf8") if "word/footnotes.xml" in z.namelist() else ""
    notes = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", notes_xml)
    body = "\n".join(parts)
    total = len(body.replace("\n", " ")) + len(" ".join(notes))
    print(f"Caracteres con espacios (texto + tablas + notas): {total:,}".replace(",", "."))
    palabras = len(body.split()) + len(" ".join(notes).split())
    print(f"Palabras (texto + tablas + notas): {palabras:,}".replace(",", "."))
    md = MD.read_text(encoding="utf8")
    for label in ("Resumen", "Abstract"):
        m = re.search(rf"\*\*{label}\*\*\s*\n\s*\n(.+?)\n", md, re.S)
        if m:
            words = re.sub(r"[*«»\"]", "", m.group(1)).split()
            print(f"Palabras en {label}: {len(words)}")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "plantilla.docx"
        build_reference(ref)
        if "--plantilla" in sys.argv and reemplazar_si_cambia(ref, REF):
            print(f"Escrita la plantilla: {REF}")
        salida = Path(tmp) / DOCX.name
        convert(ref, salida)
        cambio = reemplazar_si_cambia(salida, DOCX)
    report()
    print(f"{'Escrito' if cambio else 'Sin cambios'}: {DOCX}")
