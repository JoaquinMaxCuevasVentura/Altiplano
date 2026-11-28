"""Corre el piloto paramétrico de E1, E2, E3, E4 y E6, uno tras otro, y resume lo que encuentra.

El piloto de E5 va aparte, en boveda_e5.py, que además arma la comparación con la bóveda verdadera. Se corre desde la
raíz: python3 chhaxwa/parametrico/todas.py (pide ezdxf, shapely, matplotlib y Pillow).
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import piloto as P                                         # noqa: E402

if __name__ == "__main__":
    P.semilla()
    import chullpa_e4
    import corral_e2
    import cupula_e3
    import montana_e1
    import pirwa_e6
    for modulo in (montana_e1, corral_e2, cupula_e3, chullpa_e4, pirwa_e6):
        modulo.main()
