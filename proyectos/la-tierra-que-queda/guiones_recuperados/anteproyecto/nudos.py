from pathlib import Path
import random

folder=Path('/workspace/La_tierra_que_queda/Anteproyecto/graficos')
PAPER='#f4f0e8'
INK='#3f3a30'
GRAY='#76695f'
STONE='#c5b8a3'
CORE='#ddd0bd'
SOIL='#e9dfd0'
RUST='#9e5940'
RED_EARTH='#bf8c6e'
WOOD='#a77e5c'
CLOTH='#dfcaac'
SKY='#5e858b'

class SVG:
    def __init__(self):self.items=[]
    def rect(self,x,y,w,h,fill='none',stroke=INK,weight=1,r=0):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"/>')
    def path(self,d,fill='none',stroke=INK,weight=1,dash=''):
        self.items.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{weight}" stroke-linejoin="round" stroke-linecap="round" {dash}/>')
    def mark(self,x,y,n,tx,ty):
        self.path(f'M{x} {y} L{tx} {ty}',stroke=GRAY,weight=.9)
        self.items.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{PAPER}" stroke="{RUST}" stroke-width="1.1"/>')
        self.items.append(f'<text x="{x}" y="{y+4}" fill="{RUST}" text-anchor="middle" font-family="DejaVu Sans" font-size="12">{n}</text>')
    def emit(self,name):
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="415" height="245" viewBox="0 0 415 245">'+''.join(self.items)+'</svg>'
        (folder/f'{name}.svg').write_text(svg)

def rubble(svg,x,y,w,h,fill,seed):
    rand=random.Random(seed)
    v=[(x+rand.randint(1,5),y+h*.25),(x+w*.18,y+rand.randint(0,3)),
        (x+w*.71,y+rand.randint(0,4)),(x+w-rand.randint(0,4),y+h*.18),
        (x+w-2,y+h*.72),(x+w*.84,y+h-1),(x+w*.24,y+h),(x+1,y+h*.78)]
    s='M'+' L'.join(f'{a:.2f} {b:.2f}' for a,b in v)+' Z'
    svg.path(s,fill,GRAY,.78)

def ground(svg):
    svg.path('M29 192 L116 192 L132 195 L289 195 L312 191 L386 191 L386 232 L29 232 Z',
            SOIL,GRAY,.8)
    for k in range(32):
        x=31+k*11
        svg.path(f'M{x} 226 L{x+7} 218',stroke='#c8b9a7',weight=.65)

svg=SVG()
ground(svg)
rows=[(157,32),(126,28),(102,23),(78,22),(55,21)]
for i,(y,h) in enumerate(rows):
    a=118+8*i
    b=301-7*i
    if i==2:
        rubble(svg,a,y,b-a,h,STONE,217)
        continue
    rubble(svg,a,y,56-i*3,h,STONE,i+10)
    rubble(svg,b-(54-i*2),y,54-i*2,h,STONE,i+27)
    for j in range(5):
        rubble(svg,a+53-i*2+(j%3)*(22-i),y+(j//3)*10,24-i,10,CORE,21+i*j)
rubble(svg,112,182,196,25,STONE,22)
svg.mark(83,61,1,155,68)
svg.mark(333,97,2,232,112)
svg.mark(335,157,3,218,161)
svg.emit('nudo01')

svg=SVG()
ground(svg)
for i,(x,w) in enumerate([(61,58),(119,57),(43,56),(99,54),(56,54),(110,44)]):
    rubble(svg,x,166-i//2*25,w,23,STONE,i+9)
svg.rect(239,175,51,40,STONE,GRAY,1,2)
svg.rect(244,174,41,6,WOOD,INK,1,2)
svg.rect(258,72,7,105,WOOD,INK,1,1)
svg.path('M180 58 Q226 25 303 24 Q331 25 348 30 L348 43 Q302 37 266 42 Q218 47 182 71 Z',CLOTH,RUST,1.1)
svg.path('M181 71 Q226 48 266 42 Q305 37 348 43',stroke=INK,weight=2.9)
svg.path('M182 64 L262 64 L262 77',stroke=WOOD,weight=7)
svg.path('M266 57 L330 178',stroke=GRAY,weight=1.9)
svg.path('M319 154 L328 171',stroke=INK,weight=4)
svg.rect(318,177,34,38,STONE,GRAY,1,2)
svg.rect(325,174,23,5,WOOD,INK,1,2)
svg.mark(129,50,1,183,65)
svg.mark(290,102,2,264,69)
svg.mark(365,150,3,328,168)
svg.emit('nudo02')

svg=SVG()
svg.path('M22 108 L174 120 L171 151 L22 138 Z',RED_EARTH,RUST,1)
svg.path('M22 138 L171 151 L171 170 L22 158 Z',CLOTH,WOOD,1)
svg.path('M241 126 L393 139 L393 168 L241 156 Z',RED_EARTH,RUST,1)
svg.path('M241 156 L393 168 L393 187 L241 176 Z',CLOTH,WOOD,1)
svg.path('M22 163 L170 174 L169 188 L22 177 Z',WOOD,INK,.85)
svg.path('M241 180 L393 191 L393 205 L241 194 Z',WOOD,INK,.85)
svg.rect(155,144,20,58,WOOD,INK,1,2)
svg.rect(235,154,20,58,WOOD,INK,1,2)
svg.path('M127 117 L162 120 L174 87 L185 86 L181 122 L175 147',stroke=GRAY,weight=4)
svg.path('M279 128 L247 125 L238 94 L227 93 L232 130 L237 154',stroke=GRAY,weight=4)
svg.path('M172 83 L241 91 L239 98 L171 91 Z','#bdcdd1',SKY,1.2)
svg.path('M188 113 L199 166 L211 201 M205 114 L218 168 L221 192',stroke='#bc7b3e',weight=1.1,
         dash='stroke-dasharray="5 4"')
svg.mark(149,49,1,196,86)
svg.mark(286,71,2,243,106)
svg.mark(120,207,3,167,177)
svg.emit('nudo03')
