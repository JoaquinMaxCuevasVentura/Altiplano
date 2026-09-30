"""Genera las seis guías de composición para explorar los pasteles con GPT Image 2.

Uso (desde la raíz del repositorio):
    python3 analisis/esquemas/guias/generar_guias.py

Escribe en esta carpeta guia_figN_*.svg y guia_figN_*.png, con la numeración
del artículo (1 Cráneo/nido, 2 Signo, 3 Apacheta, 4 Castillete, 5 Pelvis,
6 Centinela). Los PNG tienen los tamaños que admite GPT Image 2: 1536 x 1024
(apaisado) o 1024 x 1536 (vertical).

Las guías no llevan texto ni rótulos: el modelo los copiaría. Son manchas de
valor con los bordes gastados y el grano del papel, como un encaje previo al
pastel. Los colores salen de la paleta matérica de
analisis/17_estilo_y_prompts_gpt_image.md. Para cambiar una guía, edita su
función y vuelve a correr el script; o abre el SVG en un editor vectorial.

Necesita Chromium (ruta en la variable CHROME).
"""

import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

DIR = Path(__file__).resolve().parent
CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome")

# Paleta matérica (véase analisis/17, §17.3)
HOLLIN = "#211c19"        # negro de humo: carbono del fogón
HOLLIN_SIENA = "#3a2a22"  # hollín sobre adobe
SOMBRA = "#5c4a3a"        # tierra de sombra: óxidos de hierro y manganeso
ADOBE = "#6b5a45"         # adobe: tierra con paja
SIENA = "#8a4b2f"         # siena tostada: óxido de hierro calentado
PENERIA = "#9a5a45"       # la «rojiza peñería»: arenisca con hematita
OCRE = "#b88a4a"          # ocre: limonita
POLVO = "#a79c8d"         # polvo de la puna: limo fino y seco
PAJA_HUMO = "#7d7468"     # paja «plomiza por el humo»
HUESO = "#e9e0cf"         # hueso: fosfato de calcio, mate
PLOMIZO = "#7f7b74"       # «plomizo y mineral»
PIZARRA = "#5d6670"       # pizarra: la piedra que se raja en láminas y en la que se escribe
BRASA = "#b5542b"         # brasa de boñiga: fuego de baja temperatura
BRASA_CLARA = "#e08a3a"
COCHINILLA = "#8e2f2b"    # carmín de cochinilla: tinte del tejido
VERDE_YUNGA = "#4f6b4a"   # hoja húmeda
VERDE_KOLLI = "#2f3d2c"   # hoja coriácea, verdinegra
NIEBLA = "#e6e9e6"        # gotas de agua: dispersión de toda la luz
NIEVE_SOMBRA = "#9fb3c6"  # la nieve devuelve azul en la sombra
CASITERITA = "#2b2420"    # mena de estaño: pardo negruzco con brillo
OXIDO = "#7a3e24"         # óxido de los rieles
COPAJIRA = "#b99a2f"      # agua ácida de mina: sulfatos de hierro
CARBURO = "#fff2c4"       # llama de acetileno
CALAMINA = "#9aa0a4"      # chapa galvanizada: zinc
MARTE = "#a4553a"         # hematita: el mismo óxido del adobe
SIRIO = "#dfe9ff"         # su color real, blanco azulado
NOCHE = "#0e1220"


def defs(semilla=3):
    return f"""<defs>
  <filter id="aspero" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="{semilla}" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="16" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="seco" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="{semilla + 1}" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="9" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="suave" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="blando" x="0" y="0" width="100%" height="100%"><feGaussianBlur stdDeviation="1.4"/></filter>
  <filter id="bruma" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
  <filter id="halo" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="grano" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{semilla + 2}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.42  0 0 0 0 0.38  0 0 0 0.55 0"/>
  </filter>
</defs>"""


def grano(w, h):
    return f'<rect width="{w}" height="{h}" filter="url(#grano)" style="mix-blend-mode:multiply" opacity="0.35"/>'


def svg(w, h, cuerpo, semilla=3):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'{defs(semilla)}\n<g filter="url(#blando)">{cuerpo}</g>\n{grano(w, h)}\n</svg>\n')


def fig1():
    """Cráneo/nido: sección de la chujlla con perfil de cráneo, de noche."""
    w, h = 1536, 1024
    c = f"""
<linearGradient id="cielo1" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#121624"/><stop offset="0.7" stop-color="#2a2a36"/><stop offset="1" stop-color="#46404a"/>
</linearGradient>
<radialGradient id="fogon" cx="0.40" cy="0.92" r="0.75">
  <stop offset="0" stop-color="#8a4424"/><stop offset="0.25" stop-color="{HOLLIN_SIENA}"/><stop offset="1" stop-color="{HOLLIN}"/>
</radialGradient>
<rect width="{w}" height="{h}" fill="url(#cielo1)"/>
<rect y="790" width="{w}" height="234" fill="#2f2822"/>
<path d="M1060,790 L1536,400 L1536,790 Z" fill="{PENERIA}" filter="url(#aspero)" opacity="0.85"/>
<g fill="#6e4636" filter="url(#aspero)"><ellipse cx="1250" cy="700" rx="26" ry="18"/><ellipse cx="1340" cy="610" rx="20" ry="15"/><ellipse cx="1430" cy="540" rx="30" ry="20"/><ellipse cx="1380" cy="730" rx="18" ry="13"/></g>
<path d="M478,790 L478,640 C470,600 455,560 470,500 C495,400 580,300 690,285 C820,268 960,300 1050,390 C1110,450 1128,540 1100,620 C1085,665 1080,720 1075,790 Z" fill="url(#fogon)" stroke="{PAJA_HUMO}" stroke-width="44" stroke-linejoin="round" filter="url(#aspero)"/>
<path d="M458,790 L458,650 C452,610 446,575 458,540 L525,540 L525,790 Z" fill="{ADOBE}" filter="url(#aspero)"/>
<path d="M1040,560 C1080,600 1090,660 1085,790 L1030,790 L1030,560 Z" fill="{ADOBE}" filter="url(#aspero)"/>
<path d="M462,790 L462,690 C462,628 524,618 532,676 L532,790 Z" fill="#23232e" filter="url(#seco)"/>
<path d="M468,686 C474,640 516,636 526,680" fill="none" stroke="#8a8272" stroke-width="5" opacity="0.6"/>
<g stroke="#d9c9a6" stroke-width="7" fill="none" stroke-linecap="round" filter="url(#seco)">
  <line x1="530" y1="520" x2="1030" y2="520"/>
  <path d="M600,520 L600,548 M582,548 Q603,586 628,552"/>
  <path d="M690,520 L690,660"/>
  <path d="M820,520 L820,544 M780,544 L862,544 M790,544 L790,570 M852,544 L852,570"/>
  <path d="M930,520 L930,552 M914,552 Q932,584 950,552"/>
</g>
<rect x="545" y="758" width="130" height="32" fill="#6d5f50" filter="url(#seco)"/>
<rect x="900" y="758" width="125" height="32" fill="#6d5f50" filter="url(#seco)"/>
<ellipse cx="985" cy="735" rx="26" ry="15" fill="#b9a37e" filter="url(#seco)"/>
<ellipse cx="765" cy="772" rx="70" ry="40" fill="{BRASA}" filter="url(#halo)" opacity="0.8"/>
<path d="M735,790 Q765,748 795,790 Z" fill="{BRASA}"/>
<path d="M752,790 Q765,770 778,790 Z" fill="{BRASA_CLARA}"/>
<g stroke="{HOLLIN}" stroke-width="9" stroke-linecap="round"><line x1="700" y1="175" x2="700" y2="262"/><line x1="672" y1="202" x2="728" y2="202"/></g>
<ellipse cx="700" cy="226" rx="11" ry="8" fill="#9b5a3a"/>
"""
    return w, h, c


def fig2():
    """Signo Escalonado frente al mapa: sección arriba, planta abajo."""
    w, h = 1024, 1536

    def p(x, y):
        return (x - 40) * 2.444 + 70, (y - 72) * 4.237 + 190

    cerro = [(40, 190), (40, 176), (70, 176), (74, 150), (104, 150), (108, 122), (136, 122), (140, 96), (168, 96),
             (172, 74), (192, 72), (198, 80), (214, 96), (246, 104), (252, 126), (300, 130), (306, 152),
             (356, 156), (362, 174), (400, 176), (400, 190)]
    signo = [(40, 190), (40, 165), (90, 165), (90, 140), (140, 140), (140, 112), (190, 112), (190, 84), (250, 84),
             (250, 112), (300, 112), (300, 140), (350, 140), (350, 165), (400, 165), (400, 190)]
    d_cerro = "M" + " L".join(f"{p(x, y)[0]:.0f},{p(x, y)[1]:.0f}" for x, y in cerro) + " Z"
    d_signo = "M" + " L".join(f"{p(x, y)[0]:.0f},{p(x, y)[1]:.0f}" for x, y in signo)

    def casa(x, y, s=1.0, vacia=False):
        X, Y = p(x, y)
        a, b = 18 * s, 22 * s
        d = f"M{X - a:.0f},{Y:.0f} L{X - a:.0f},{Y - b:.0f} L{X:.0f},{Y - b - 16 * s:.0f} L{X + a:.0f},{Y - b:.0f} L{X + a:.0f},{Y:.0f} Z"
        if vacia:
            return f'<path d="{d}" fill="#e3d7c2" stroke="{SIENA}" stroke-width="6" filter="url(#seco)"/>'
        return f'<path d="{d}" fill="{CASITERITA}" filter="url(#seco)"/>'

    casas = "".join([casa(154, 96, 1.2), casa(88, 150), casa(228, 104), casa(51, 176, 0.8), casa(63, 176, 0.8),
                     casa(323, 156, 0.9), casa(377, 176, 0.8), casa(184, 73, 1.0, vacia=True)])
    proy = "".join(f'<line x1="{p(x, 190)[0]:.0f}" y1="690" x2="{p(x, 190)[0]:.0f}" y2="880" />'
                   for x in (40, 140, 190, 250, 350, 400))
    c = f"""
<linearGradient id="papel2" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#efe6d6"/><stop offset="0.48" stop-color="#e3d7c2"/><stop offset="0.56" stop-color="#7a828b"/><stop offset="1" stop-color="{PIZARRA}"/>
</linearGradient>
<rect width="{w}" height="{h}" fill="url(#papel2)"/>
<path d="{d_cerro}" fill="{PENERIA}" filter="url(#aspero)"/>
<g fill="#7d4636" filter="url(#aspero)" opacity="0.8"><ellipse cx="150" cy="640" rx="22" ry="14"/><ellipse cx="260" cy="520" rx="18" ry="12"/><ellipse cx="560" cy="330" rx="20" ry="13"/><ellipse cx="620" cy="480" rx="24" ry="15"/><ellipse cx="780" cy="600" rx="20" ry="13"/><ellipse cx="900" cy="650" rx="18" ry="12"/></g>
{casas}
<path d="{d_signo}" fill="none" stroke="#f3ead8" stroke-width="5" stroke-linejoin="miter" filter="url(#seco)" opacity="0.9"/>
<g stroke="#d8cfc0" stroke-width="2.5" opacity="0.7" filter="url(#seco)">{proy}</g>
<path d="M70,880 L950,880 L940,1430 L80,1420 Z" fill="#555e68" filter="url(#aspero)"/>
<g stroke="#d9d2c4" stroke-width="5" fill="none" filter="url(#seco)">
  <path d="M70,880 L950,880 L940,1430 L80,1420 Z"/>
  <path d="M215,880 L205,1422 M375,880 L388,1424 M535,880 L525,1426 M705,880 L717,1428 M825,880 L815,1429"/>
  <path d="M72,1040 Q470,1010 948,1062 M76,1230 Q500,1265 944,1215"/>
</g>
<g fill="{PENERIA}" filter="url(#seco)"><path d="M205,880 l12,-24 l12,24 Z"/><path d="M523,880 l12,-24 l12,24 Z"/><path d="M705,1428 l12,-24 l12,24 Z"/><path d="M380,1230 l10,-20 l10,20 Z"/></g>
<g stroke="{HUESO}" stroke-width="6" stroke-linecap="round"><line x1="455" y1="1100" x2="455" y2="1150"/><line x1="433" y1="1125" x2="477" y2="1125"/></g>
<rect x="760" y="1270" width="80" height="50" fill="{CASITERITA}" filter="url(#seco)"/>
<path d="M870,1330 L870,1270 L895,1236 L920,1270 L920,1330 Z" fill="{CASITERITA}" filter="url(#seco)"/>
"""
    return w, h, c


def fig3():
    """Umbral de la apacheta: puna seca / yunga húmedo, partidos por la cresta."""
    w, h = 1536, 1024
    c = f"""
<linearGradient id="puna3" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6f6384"/><stop offset="0.55" stop-color="#8f7fa0"/><stop offset="1" stop-color="#c9b7a8"/>
</linearGradient>
<linearGradient id="yunga3" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c9d3cc"/><stop offset="1" stop-color="{NIEBLA}"/>
</linearGradient>
<linearGradient id="rasante" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#e8c49a" stop-opacity="0.0"/><stop offset="0.85" stop-color="#e8c49a" stop-opacity="0.35"/><stop offset="1" stop-color="#e8c49a" stop-opacity="0"/>
</linearGradient>
<linearGradient id="costura3" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#8f7fa0" stop-opacity="0"/><stop offset="0.5" stop-color="#b8b3bd" stop-opacity="0.9"/><stop offset="1" stop-color="#c9d3cc" stop-opacity="0"/>
</linearGradient>
<rect width="770" height="{h}" fill="url(#puna3)"/>
<rect x="770" width="766" height="{h}" fill="url(#yunga3)"/>
<rect x="640" width="260" height="440" fill="url(#costura3)" filter="url(#bruma)"/>
<g filter="url(#aspero)" opacity="0.92">
  <path d="M230,610 L262,540 L276,560 L300,470 L322,548 L336,530 L368,610 Z" fill="#e7ebef"/>
  <path d="M300,470 L322,548 L336,530 L368,610 L318,610 Z" fill="{NIEVE_SOMBRA}"/>
  <path d="M930,470 L975,330 L990,360 L1030,200 L1062,330 L1080,300 L1120,470 Z" fill="#eef2f5"/>
  <path d="M1030,200 L1062,330 L1080,300 L1120,470 L1060,470 Z" fill="{NIEVE_SOMBRA}"/>
  <path d="M1140,470 L1170,380 L1182,400 L1205,280 L1228,390 L1240,370 L1270,470 Z" fill="#eef2f5"/>
  <path d="M1205,280 L1228,390 L1240,370 L1270,470 L1225,470 Z" fill="{NIEVE_SOMBRA}"/>
</g>
<path d="M0,610 L690,610 L770,430 L770,1024 L0,1024 Z" fill="{POLVO}" filter="url(#seco)"/>
<g stroke="#8a7f71" stroke-width="4" filter="url(#seco)" opacity="0.8"><line x1="30" y1="660" x2="640" y2="660"/><line x1="20" y1="730" x2="690" y2="730"/><line x1="40" y1="820" x2="720" y2="820"/><line x1="10" y1="930" x2="750" y2="930"/></g>
<ellipse cx="560" cy="600" rx="330" ry="70" fill="#e8c49a" opacity="0.28" filter="url(#bruma)"/>
<path d="M770,430 L880,560 L960,1024 L770,1024 Z" fill="{VERDE_YUNGA}" filter="url(#suave)"/>
<path d="M1536,480 L1400,590 L1190,1024 L1536,1024 Z" fill="#3f5a3c" filter="url(#suave)"/>
<ellipse cx="1080" cy="760" rx="170" ry="260" fill="{NIEBLA}" filter="url(#bruma)" opacity="0.85"/>
<path d="M1010,1024 Q1075,900 1140,1024 Z" fill="#9fb9b6" filter="url(#suave)"/>
<g stroke="#dfe7e0" stroke-width="5" opacity="0.7" filter="url(#suave)"><line x1="830" y1="620" x2="840" y2="760"/><line x1="880" y1="700" x2="888" y2="860"/><line x1="1420" y1="640" x2="1410" y2="800"/><line x1="1360" y1="760" x2="1350" y2="900"/></g>
<g stroke="{VERDE_KOLLI}" stroke-width="7" stroke-linecap="round"><line x1="950" y1="880" x2="1010" y2="846"/><line x1="1120" y1="850" x2="1070" y2="828"/></g>
<path d="M1010,846 Q1040,890 1070,828" fill="none" stroke="{CASITERITA}" stroke-width="5" stroke-dasharray="7,6"/>
<rect x="763" y="318" width="14" height="115" fill="{HOLLIN}" filter="url(#seco)"/>
<circle cx="770" cy="306" r="13" fill="{HOLLIN}"/>
<path d="M777,340 L848,352 L777,372 Z" fill="{COCHINILLA}" filter="url(#seco)"/>
<g fill="{HOLLIN}" filter="url(#seco)"><ellipse cx="742" cy="446" rx="11" ry="15"/><ellipse cx="718" cy="456" rx="11" ry="14"/><ellipse cx="696" cy="466" rx="9" ry="12"/></g>
"""
    return w, h, c


def fig4():
    """El castillete y la caída al plano 450: corte vertical."""
    w, h = 1024, 1536
    torre = """
<g stroke="#d8d2c8" stroke-width="4" fill="none" stroke-linecap="round" filter="url(#seco)">
  <path d="M470,420 L512,90 L554,420"/>
  <path d="M478,356 L546,356 M487,286 L537,286 M496,216 L528,216 M504,150 L520,150"/>
  <path d="M478,356 L537,286 L496,216 L520,150 M546,356 L487,286 L528,216 L504,150"/>
</g>"""
    cuerpos = "".join(f'<ellipse cx="{x}" cy="{y}" rx="13" ry="16" fill="#9c7b62" filter="url(#suave)"/>'
                      for x, y in [(482, 730), (515, 724), (548, 732), (492, 775), (525, 770), (556, 780), (505, 820)])
    c = f"""
<linearGradient id="noche4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0e13"/><stop offset="1" stop-color="#1c1d22"/></linearGradient>
<rect width="{w}" height="420" fill="url(#noche4)"/>
<path d="M640,420 L820,250 L1000,420 Z" fill="#7a7062" filter="url(#aspero)"/>
{torre}
<g fill="#8a8272" filter="url(#seco)"><rect x="40" y="330" width="90" height="90"/><rect x="150" y="365" width="48" height="55"/><rect x="208" y="365" width="48" height="55"/><rect x="266" y="365" width="48" height="55"/><rect x="330" y="392" width="26" height="28"/><rect x="362" y="392" width="26" height="28"/><rect x="394" y="392" width="26" height="28"/><rect x="426" y="392" width="26" height="28"/></g>
<g fill="{CALAMINA}" opacity="0.8"><rect x="150" y="360" width="164" height="7"/><rect x="330" y="388" width="122" height="5"/></g>
<g><circle cx="120" cy="300" r="6" fill="{CARBURO}"/><circle cx="240" cy="340" r="5" fill="#e8a040"/><circle cx="600" cy="360" r="6" fill="{CARBURO}"/><circle cx="700" cy="300" r="5" fill="#e8a040"/></g>
<g filter="url(#halo)" opacity="0.7"><circle cx="120" cy="300" r="16" fill="{CARBURO}"/><circle cx="600" cy="360" r="16" fill="{CARBURO}"/></g>
<rect y="416" width="{w}" height="10" fill="#8a8272"/>
<rect y="426" width="{w}" height="1110" fill="{CASITERITA}" filter="url(#aspero)"/>
<g fill="#8c8a86" opacity="0.6"><circle cx="160" cy="600" r="3"/><circle cx="820" cy="700" r="3"/><circle cx="300" cy="900" r="2.5"/><circle cx="760" cy="1100" r="3"/><circle cx="200" cy="1300" r="2.5"/><circle cx="880" cy="1240" r="3"/></g>
<path d="M380,540 L380,488 A30,30 0 0,1 440,488 L440,540 Z" fill="#0d0d0e"/>
<path d="M584,540 L584,488 A30,30 0 0,1 644,488 L644,540 Z" fill="#0d0d0e"/>
<rect x="470" y="540" width="90" height="920" fill="#0b0b0c"/>
<rect x="458" y="700" width="114" height="150" fill="#3b3530"/>
{cuerpos}
<g stroke="#d8d2c8" stroke-width="3" filter="url(#seco)"><rect x="458" y="700" width="114" height="150" fill="none"/><line x1="486" y1="700" x2="486" y2="850"/><line x1="515" y1="700" x2="515" y2="850"/><line x1="544" y1="700" x2="544" y2="850"/><line x1="458" y1="752" x2="572" y2="752"/><line x1="458" y1="800" x2="572" y2="800"/></g>
<rect x="560" y="962" width="380" height="36" fill="#4a4038" filter="url(#seco)"/>
<rect x="90" y="1132" width="380" height="36" fill="#4a4038" filter="url(#seco)"/>
<rect x="560" y="1370" width="420" height="40" fill="#4a4038" filter="url(#seco)"/>
<rect x="560" y="1394" width="420" height="16" fill="{COPAJIRA}" filter="url(#suave)" opacity="0.9"/>
<ellipse cx="760" cy="1402" rx="190" ry="30" fill="{COPAJIRA}" filter="url(#bruma)" opacity="0.35"/>
<path d="M830,1410 L905,1318 L980,1410 Z" fill="#6e6452" filter="url(#aspero)"/>
<g stroke="#b9a37e" stroke-width="9" stroke-linecap="round"><line x1="820" y1="1330" x2="870" y2="1370"/><line x1="876" y1="1352" x2="930" y2="1334"/></g>
"""
    return w, h, c


def fig5():
    """Pelvis telúrica: la cuenca seca como pelvis, bajo un cielo sin tocar."""
    w, h = 1536, 1024
    c = f"""
<radialGradient id="hueso5" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#f1eadb"/><stop offset="0.7" stop-color="{HUESO}"/><stop offset="1" stop-color="#cfc3ad"/></radialGradient>
<linearGradient id="tierra5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b5845"/><stop offset="1" stop-color="{SOMBRA}"/></linearGradient>
<rect width="{w}" height="{h}" fill="#c9d6dc"/>
<path d="M1262,108 a60,60 0 1,0 0,120 a46,60 0 1,1 0,-120 Z" fill="#efe9dc"/>
<path d="M1262,108 a60,60 0 1,0 0,120" fill="none" stroke="#b77b5a" stroke-width="3" opacity="0.6"/>
<path d="M60,390 L200,300 L360,390 Z" fill="{PLOMIZO}" filter="url(#aspero)"/>
<path d="M200,300 q-14,-28 4,-52 q18,-24 0,-52 q-12,-20 4,-40" fill="none" stroke="#8d949a" stroke-width="7" filter="url(#suave)" opacity="0.8"/>
<rect y="385" width="{w}" height="{h - 385}" fill="url(#tierra5)" filter="url(#seco)"/>
<g stroke="#2e241c" stroke-width="5" fill="none" filter="url(#seco)">
  <path d="M90,470 l70,40 l-20,48 l64,36"/><path d="M1300,460 l-50,50 l36,42 l-56,56"/><path d="M150,800 l84,-22 l36,56"/><path d="M1340,820 l-70,-36 l-28,50"/><path d="M420,930 l40,-30 l50,20"/><path d="M1100,940 l-40,-24 l-46,18"/>
</g>
<path d="M768,470 C725,430 640,410 560,410 C470,410 410,460 410,540 C410,620 470,675 540,710 C585,732 605,775 625,815 C645,855 700,875 740,855 C755,845 760,830 768,830 C776,830 781,845 796,855 C836,875 891,855 911,815 C931,775 951,732 996,710 C1066,675 1126,620 1126,540 C1126,460 1066,410 976,410 C896,410 811,430 768,470 Z" fill="url(#hueso5)" filter="url(#aspero)"/>
<path d="M768,540 C700,540 660,590 660,640 C660,700 710,735 768,735 C826,735 876,700 876,640 C876,590 836,540 768,540 Z" fill="{SOMBRA}" filter="url(#aspero)"/>
<path d="M710,600 Q768,640 820,690" fill="none" stroke="#d9ccb0" stroke-width="16" stroke-linecap="round" filter="url(#seco)" opacity="0.8"/>
<g fill="#cdbf9f"><circle cx="735" cy="626" r="5"/><circle cx="782" cy="660" r="4"/><circle cx="806" cy="676" r="5"/></g>
<path d="M726,478 C745,458 791,458 810,478 L790,560 C782,580 754,580 746,560 Z" fill="#d8ccb6" filter="url(#seco)"/>
<ellipse cx="672" cy="790" rx="30" ry="22" fill="{SOMBRA}" filter="url(#seco)"/>
<ellipse cx="864" cy="790" rx="30" ry="22" fill="{SOMBRA}" filter="url(#seco)"/>
"""
    return w, h, c


def fig6():
    """El centinela de la resistencia: nocturno vertical."""
    w, h = 1024, 1536
    estrellas = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e8e0d0"/>'
                        for x, y, r in [(90, 150, 2.5), (230, 90, 2), (420, 180, 2.5), (560, 110, 2), (880, 150, 2.5),
                                        (140, 420, 2), (640, 380, 2), (930, 470, 2), (300, 560, 1.8), (720, 600, 2)])
    c = f"""
<linearGradient id="noche6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NOCHE}"/><stop offset="0.7" stop-color="#1c2233"/><stop offset="1" stop-color="#2a2f40"/></linearGradient>
<linearGradient id="suelo6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b5a45"/><stop offset="1" stop-color="#4a4034"/></linearGradient>
<rect width="{w}" height="1130" fill="url(#noche6)"/>
{estrellas}
<circle cx="340" cy="330" r="6" fill="{MARTE}"/>
<circle cx="760" cy="260" r="16" fill="{SIRIO}" filter="url(#halo)" opacity="0.7"/><circle cx="760" cy="260" r="6" fill="{SIRIO}"/>
<path d="M770,1130 L770,760 L815,690 L860,760 L860,1130 Z" fill="#2f3446" filter="url(#seco)"/>
<g stroke="#bfb8ac" stroke-width="4" fill="none"><path d="M786,650 l12,10 l12,-10"/><path d="M816,636 l12,10 l12,-10"/></g>
<rect y="1126" width="{w}" height="410" fill="url(#suelo6)" filter="url(#seco)"/>
<path d="M150,1130 L150,930 L650,930 L650,1130 Z" fill="#5b5243" filter="url(#aspero)"/>
<path d="M120,936 Q400,810 680,936 Z" fill="#6e6452" filter="url(#aspero)"/>
<rect x="320" y="960" width="160" height="170" fill="#0d0f16" filter="url(#seco)"/>
<g fill="{HUESO}" filter="url(#seco)"><rect x="345" y="982" width="22" height="148" rx="10"/><rect x="389" y="970" width="22" height="160" rx="10"/><rect x="433" y="982" width="22" height="148" rx="10"/></g>
<line x1="505" y1="985" x2="530" y2="1130" stroke="#c9b48f" stroke-width="7" stroke-linecap="round"/>
<path d="M652,965 L700,945 L700,1110 L652,1132 Z" fill="none" stroke="#c9c0b1" stroke-width="5" filter="url(#seco)"/>
<g fill="{HUESO}" filter="url(#bruma)" opacity="0.32"><ellipse cx="150" cy="1300" rx="40" ry="110"/><ellipse cx="580" cy="1370" rx="34" ry="95"/><ellipse cx="890" cy="1320" rx="38" ry="105"/></g>
"""
    return w, h, c


GUIAS = [(1, "craneo_nido", fig1, 3), (2, "signo_mapa", fig2, 5), (3, "apacheta", fig3, 7),
         (4, "castillete", fig4, 11), (5, "pelvis", fig5, 13), (6, "centinela", fig6, 17)]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for n, nombre, f, semilla in GUIAS:
            w, h, cuerpo = f()
            texto = svg(w, h, cuerpo, semilla)
            destino = DIR / f"guia_fig{n}_{nombre}.svg"
            destino.write_text(texto, encoding="utf8")
            html = Path(tmp) / f"g{n}.html"
            html.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#000}"
                            f"svg{{display:block}}</style>{texto}", encoding="utf8")
            png = DIR / f"guia_fig{n}_{nombre}.png"
            captura = Path(tmp) / f"g{n}.png"
            subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={w},{h + 200}",
                            f"--screenshot={captura}", html.as_uri()],
                           check=True, capture_output=True)
            Image.open(captura).convert("RGB").crop((0, 0, w, h)).save(png)
            print(destino.name, "->", png.name, f"({w} x {h})")
    mascara_fig5()


def mascara_fig5():
    """Máscara opcional para la Figura 5: el cielo queda como papel sin tocar (reserva).

    GPT Image 2 edita las zonas transparentes (alfa 0) y conserva las opacas (alfa 255).
    Aquí se conserva el cielo, con la luna, y se repintan la tierra, la pelvis y el cerro del humo.
    """
    w, h = 1536, 1024
    m = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    px = m.load()
    for y in range(h):
        for x in range(w):
            if y >= 372 or (30 <= x <= 390 and 120 <= y):
                px[x, y] = (0, 0, 0, 0)
    m.save(DIR / "guia_fig5_pelvis_mascara.png")
    print("guia_fig5_pelvis_mascara.png (cielo conservado)")


if __name__ == "__main__":
    main()
