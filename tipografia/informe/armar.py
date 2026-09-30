"""Arma el informe de decisiones: el .docx, su PDF y el índice con sus páginas.

Uso (desde la raíz del repositorio):
    python3 tipografia/informe/mapas.py      # los seis mapas (si cambiaron)
    python3 tipografia/informe/armar.py

Necesita node con el paquete docx (npm install docx; NODE_PATH si está en otra carpeta),
fontTools y brotli. Con LibreOffice (soffice, con Writer) y PyMuPDF, además convierte a PDF,
busca en qué página cae cada título y vuelve a armar el .docx con el índice paginado.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DOCX = AQUI / "contenida_informe_de_decisiones.docx"
PDF = DOCX.with_suffix(".pdf")


def armar_docx():
    subprocess.run(["node", str(AQUI / "informe.js")], check=True)


def a_pdf(destino):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    perfil = Path(tempfile.mkdtemp(prefix="contenida-lo-"))
    subprocess.run([soffice, "--headless", f"-env:UserInstallation={perfil.as_uri()}", "--convert-to", "pdf",
                    "--outdir", str(destino), str(DOCX)], check=True, capture_output=True)
    pdf = Path(destino) / (DOCX.stem + ".pdf")
    return pdf if pdf.exists() else None


def paginar(pdf):
    import pymupdf
    titulos = json.loads((AQUI / ".titulos.json").read_text(encoding="utf8"))
    doc = pymupdf.open(pdf)
    # el índice ocupa las primeras páginas: se busca cada título después de la página del índice
    inicio = next(i for i, p in enumerate(doc) if p.search_for("Índice")) + 1
    paginas, desde = {}, inicio
    for t in titulos:
        texto = t["t"]
        if texto in ("Resumen", "Índice"):
            continue
        for i in range(desde, doc.page_count):
            if doc[i].search_for(texto):
                paginas[texto] = i + 1
                desde = i
                break
    (AQUI / "paginas.json").write_text(json.dumps(paginas, ensure_ascii=False, indent=1), encoding="utf8")
    return paginas


def main():
    armar_docx()
    with tempfile.TemporaryDirectory() as tmp:
        pdf = a_pdf(tmp)
        if not pdf:
            print("Sin LibreOffice (con Writer): el índice queda sin páginas y no hay PDF.")
            return
        try:
            paginas = paginar(pdf)
        except ImportError:
            print("Sin PyMuPDF: el índice queda sin páginas.")
            shutil.copy(pdf, PDF)
            return
        armar_docx()
        pdf = a_pdf(tmp)
        shutil.copy(pdf, PDF)
    print(f"listo: {DOCX.name} y {PDF.name}, {len(paginas)} títulos paginados")


if __name__ == "__main__":
    os.chdir(AQUI.parent.parent)
    sys.exit(main())
