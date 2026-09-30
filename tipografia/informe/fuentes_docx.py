"""Las fuentes del informe, para incrustarlas en el .docx.

Uso: python3 tipografia/informe/fuentes_docx.py CARPETA

Convierte las woff2 de laminas/fuentes/ (Newsreader y Courier Prime, licencia SIL OFL)
a TTF y le da a cada cara su propia familia («Newsreader Italic», «Courier Prime Bold»…),
porque un .docx incrusta una cara por familia y así la cursiva no se inventa.
Necesita fontTools y brotli.
"""

import sys
from pathlib import Path

from fontTools.ttLib import TTFont

FUENTES = Path(__file__).resolve().parent.parent / "laminas" / "fuentes"
CARAS = {
    "Newsreader": "newsreader-latin-400-normal.woff2",
    "Newsreader Light": "newsreader-latin-300-normal.woff2",
    "Newsreader Medium": "newsreader-latin-500-normal.woff2",
    "Newsreader Italic": "newsreader-latin-400-italic.woff2",
    "Newsreader Light Italic": "newsreader-latin-300-italic.woff2",
    "Courier Prime": "courier-prime-latin-400-normal.woff2",
    "Courier Prime Bold": "courier-prime-latin-700-normal.woff2",
}


def main(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for familia, archivo in CARAS.items():
        f = TTFont(FUENTES / archivo)
        f.flavor = None
        ps = familia.replace(" ", "")
        for registro in f["name"].names:
            if registro.nameID in (1, 16):
                registro.string = familia
            elif registro.nameID in (2, 17):
                registro.string = "Regular"
            elif registro.nameID == 4:
                registro.string = familia
            elif registro.nameID == 6:
                registro.string = ps
        f["OS/2"].fsSelection = (f["OS/2"].fsSelection & ~0b1100001) | 0b1000000   # regular
        f["head"].macStyle = 0
        f.save(destino / f"{ps}.ttf")
        print(familia)


if __name__ == "__main__":
    main(sys.argv[1])
