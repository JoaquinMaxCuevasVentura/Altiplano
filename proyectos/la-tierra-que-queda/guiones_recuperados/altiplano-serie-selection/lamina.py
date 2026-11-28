from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

dest = Path('/workspace/La_tierra_que_queda/Serie_seleccionada')
w, h = landscape(A3)
page = Canvas(str(dest/'La_tierra_que_queda_serie.pdf'), pagesize=(w,h))
page.setTitle('La tierra que queda · Del lindero al fogón')
page.setSubject('Tres exploraciones de arquitectura a partir de Altiplano')
fonts = {
    'Serif':'/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf',
    'Sans':'/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf',
    'Italic':'/usr/share/fonts/truetype/open-sans/OpenSans-Italic.ttf',
    'Semi':'/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf',
}
for name,path in fonts.items():
    pdfmetrics.registerFont(TTFont(name,path))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='Semi',italic='Italic',boldItalic='Italic')

paper, ink, muted, rule, accent = map(HexColor,('#F9F6EE','#272920','#555347','#BFB39D','#8B432D'))
margin = 53
gap = 23
width = (w-2*margin-2*gap)/3
origin = [margin+i*(width+gap) for i in range(3)]

def text(x,y,body,font='Sans',size=12,color=ink,right=False):
    page.setFont(font,size)
    page.setFillColor(color)
    (page.drawRightString if right else page.drawString)(x,y,body)

def paragraph(x,y,body,column_width=width,size=12.8,leading=19,color=ink):
    style=ParagraphStyle('serie',fontName='Sans',fontSize=size,leading=leading,textColor=color)
    block=Paragraph(body,style)
    _, height = block.wrap(column_width,1000)
    block.drawOn(page,x,y-height)
    return height

def line(x1,y,x2):
    page.setLineWidth(.65)
    page.setStrokeColor(rule)
    page.line(x1,y,x2,y)

page.setFillColor(paper)
page.rect(0,0,w,h,fill=1,stroke=0)
text(margin,791,'COSECHA DE PIEDRAS  /  PROYECTO PARALELO','Semi',10,muted)
text(w-margin,791,'EXPLORACIONES SELECCIONADAS','Semi',10,muted,True)
line(margin,773,w-margin)
text(margin,706,'La tierra que queda','Serif',51)
text(margin+2,666,'Del lindero al fogón','Serif',22)
line(margin,640,w-margin)

root = 'https://github.com/JoaquinMaxCuevasVentura/Altiplano/blob/d9b53fb'
article = root + '/articulo/articulo_cosecha_de_piedras.md'
figure = root + '/articulo/figuras/figura_1.png'
pieces = [
    ('01 / LINDERO','El recinto que queda abierto','El_recinto_que_queda_abierto.png',
     'La pirca rodea el claro y deja una entrada entre dos remates desiguales. La cubierta junto al borde da sombra a una parte del terreno.',
     'En el regreso se recomponen las pircas. El artículo lee las ausencias en la lista del retorno (p. 156).',
     'Precedente formal en <i>Corral</i>, de Smiljan Radić.', 'Artículo, §7', article),
    ('02 / UMBRAL','El claro de la piedra','El_claro_de_la_piedra.png',
     'La tela se levanta sobre el paso y deja una piedra suelta en el claro. Su borde marca el tránsito entre la sombra y el suelo iluminado.',
     'Al volver a Jatun-Kolla, los comunarios se detienen en el dintel y se arrodillan para besar el suelo (p. 155).',
     'Estudio de paso y pausa en Blender.', 'Artículo, §7', article),
    ('03 / INTERIOR','La mirada en cuclillas','La_mirada_en_cuclillas.png',
     'La sección lleva la vista a la altura del cuerpo junto al fogón. La ranura ensayada en la cubierta lleva luz al suelo.',
     'El corte retoma <i>Cráneo/nido</i> y la lectura del interior de la <i>chujlla</i> (pp. 8 y 30–31).',
     'Precedente en la <i>Casa para el Poema del Ángulo Recto</i>, de Radić.', 'Figura Cráneo/nido', figure),
]

for x,(num,title,file,operation,source,precedent,link_text,url) in zip(origin,pieces):
    with Image.open(dest/file) as im:
        ratio=im.width/im.height
    picture_height=width/(4/3)
    picture_width=picture_height*ratio
    if picture_width>width:
        picture_width=width
        picture_height=width/ratio
    picture_x=x+(width-picture_width)/2
    picture_y=354+(width/(4/3)-picture_height)/2
    page.drawImage(str(dest/file),picture_x,picture_y,width=picture_width,height=picture_height)
    text(x,324,num,'Semi',10,accent)
    assert pdfmetrics.stringWidth(title,'Serif',21)<width
    text(x,291,title,'Serif',21)
    ph = paragraph(x,268,operation)
    assert ph<=58
    line(x,194,x+width)
    height=paragraph(x,180,source,size=11.5,leading=16.5,color=muted)
    assert height<=50
    precedent_y = 180-height-8
    reference_height=paragraph(x,precedent_y,precedent,size=10.4,leading=14.4,color=muted)
    assert reference_height<=30
    link_y=precedent_y-reference_height-16
    assert link_y>55
    text(x,link_y,link_text,'Semi',9.5,accent)
    page.linkURL(url,(x,link_y-3,x+pdfmetrics.stringWidth(link_text,'Semi',9.5)+2,link_y+10),
                 relative=0,thickness=0)
line(margin,68,w-margin)
text(margin,45,'Lectura de Altiplano · La paginación corresponde a la edición de 1982 citada en el artículo.',size=9.8,color=muted)
text(w-margin,45,'Tres estudios de proyecto',size=9.8,color=muted,right=True)
page.showPage()
page.save()
