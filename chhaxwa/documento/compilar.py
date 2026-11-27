"""Compila el documento de Chhaxwa con Typst: chhaxwa/documento/chhaxwa.typ -> chhaxwa/documento/chhaxwa.pdf.

Necesita Typst como paquete de Python (pip install typst) y la letra Inter, libre (OFL). Se corre desde la raíz:
    python3 chhaxwa/documento/compilar.py
Usa los renders de chhaxwa/renders/. Escribe el PDF solo si cambió.
"""
import sys
from pathlib import Path

import typst

AQUI = Path(__file__).resolve().parent


def main():
    pdf = typst.compile(str(AQUI / "chhaxwa.typ"), root=str(AQUI.parent))
    destino = AQUI / "chhaxwa.pdf"
    if destino.exists() and destino.read_bytes() == pdf:
        print("Sin cambios.")
        return
    destino.write_bytes(pdf)
    print(f"{destino.relative_to(AQUI.parent.parent)} ({len(pdf) / 1e6:.1f} MB)")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
