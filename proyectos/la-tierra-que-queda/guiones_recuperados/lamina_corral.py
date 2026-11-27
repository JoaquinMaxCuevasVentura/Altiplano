from pathlib import Path

import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

out=Path('/workspace/La_tierra_que_queda')
W,H=landscape(A3)
c=Canvas('/tmp/lamina_corral.pdf',pagesize=(W,H))
pdfmetrics.registerFont(TTFont('Serif','/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Sans','/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Semi','/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'))
paper,ink,gray,rust,rule,earth,rock,tile=map(HexColor,('#FAF7EF','#272920','#515247','#A33B26','#B2A387','#F1E7D3','#87816E','#D3A589'))

def txt(x,y,content,size=11,font='Sans',color=ink,right=False):
    c.setFillColor(color)
    c.setFont(font,size)
    (c.drawRightString if right else c.drawString)(x,y,content)
def block(x,y,content,size=11):
    for i,line in enumerate(content):
        txt(x,y-i*16,line,size)
def stroke(points,color=rule,width=.6,dash=None):
    c.setLineWidth(width)
    c.setStrokeColor(color)
    c.setDash(dash or [])
    p=c.beginPath()
    p.moveTo(*points[0])
    for x,y in points[1:]:
        p.lineTo(x,y)
    c.drawPath(p)
    c.setDash([])
def poly(points,color,edge=rule):
    c.setStrokeColor(edge)
    c.setFillColor(color)
    c.setLineWidth(.7)
    p=c.beginPath()
    p.moveTo(*points[0])
    for x,y in points[1:]: p.lineTo(x,y)
    p.close()
    c.drawPath(p,fill=1)
def panel_url(x,y,w,url):
    c.linkURL(url,(x,y-3,x+w,y+10),relative=0,thickness=0)

c.setFillColor(paper)
c.rect(0,0,W,H,fill=1,stroke=0)
txt(53,794,'LA TIERRA QUE QUEDA  /  EL DINTEL DE JATUN-KOLLA',10,'Semi',gray)
txt(W-53,794,'VARIANTE C  /  MODELO DIGITAL',10,'Semi',gray,True)
stroke([(53,776),(W-53,776)])
txt(53,709,'La pirca recompuesta',53,'Serif')
txt(55,666,'Un trecho del muro gira y la cubierta deja el último tramo a cielo abierto.',14,'Serif')
stroke([(53,642),(W-53,642)])
c.drawImage(str(out/'C_pirca_recompuesta.png'),53,190,width=654,height=436)
txt(53,171,'Vista desde el extremo descubierto. Modelo y render en Blender.',10,'Sans',gray)
stroke([(729,165),(729,626)])
origin_x,origin_y,unit=754,435,37.7
def plan(x,y): return origin_x+x*unit,origin_y+y*unit
def map_plan(points): return [plan(*q) for q in points]

txt(754,618,'PLANTA  /  UMBRAL Y LUGAR DE PAUSA',10,'Semi',gray)
poly(map_plan([(0,0),(9.4,0),(9.4,4.3),(0,4.3)]),earth)
poly(map_plan([(.47,.74),(7.63,.74),(7.63,1.11),(.47,1.11)]),rock)
poly(map_plan([(1.34,3.38),(7.62,3.38),(7.62,2.53),(7.99,2.53),(7.99,3.75),(1.34,3.75)]),rock)
poly(map_plan([(.82,.68),(7.34,.68),(7.34,1.73+.061*7.34-.14),(.82,1.73+.061*.82-.14)]),tile,HexColor('#A77656'))
poly(map_plan([(1.54,3.75),(6.72,3.75),(6.72,2.1+.061*6.72+.14),(1.54,2.1+.061*1.54+.14)]),tile,HexColor('#A77656'))
stroke(map_plan([(.12,2.22),(5.0,2.20),(6.68,2.2),(7.48,2.42)]),rust,1.05,[3,2])
stroke(map_plan([(7.38,2.31),(7.48,2.42),(7.36,2.44)]),rust,.8)
txt(*plan(7.18,1.63),'pausa',10,'Semi',rust)
txt(754,397,'QUÉ CAMBIA AL FINAL DEL RECORRIDO',10,'Semi',gray)
block(754,373,('La piedra sigue marcando un recinto cuando',
               'la cubierta se retira. El giro recoge un extremo',
               'del paso y lo convierte en un sitio de pausa.',
               'La luz llega desde arriba y desde el remate.'))
txt(754,283,'DOS PUNTOS DE PARTIDA',10,'Semi',gray)
block(754,259,('En Corral, Radić combina un cerco de piedra',
               'y un abrigo parcial. En Altiplano, el regreso',
               'se narra como un paso por un dintel y la tarea',
               'de recomponer las pircas (pp. 155–156).'))
stroke([(53,145),(W-53,145)])
txt(53,118,'OBRA GRUESA',10,'Semi',gray)
block(53,94,('Smiljan Radić. Corral, p. 204 impresa (p. 31 del PDF adjunto).',
              'Alan Chandler, «Trabajo de riesgo», pp. 214–217 impresas.'),10.5)
txt(642,118,'REFERENCIA DEL PROYECTO',10,'Semi',gray)
block(642,94,('Cosecha de piedras, sección 7. Las tres variantes quedan editables',
               'en el archivo de Blender. Estudio espacial y material.'),10.5)
panel_url(642,94,225,'https://github.com/JoaquinMaxCuevasVentura/Altiplano/blob/d9b53fb/articulo/articulo_cosecha_de_piedras.md')
c.showPage()
c.save()
doc=fitz.open('/tmp/lamina_corral.pdf')
with fitz.open(out/'La_tierra_que_queda_propuesta.pdf') as earlier:
    doc.insert_pdf(earlier,links=True)
doc.set_metadata({'title':'La tierra que queda · El dintel de Jatun-Kolla',
                  'subject':'Estudio espacial a partir de Altiplano y Obra Gruesa'})
doc.save(out/'La_tierra_que_queda_laminas.pdf',deflate=True,garbage=3)
