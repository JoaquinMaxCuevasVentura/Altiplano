from pathlib import Path
p=Path('/tmp/testeros')
s=Path('/tmp/fidelidad/laminas.py').read_text().replace("out=root/'Revision_3D'","out=Path('/tmp/testeros')").replace("(T/'testero.json')","(out/'traza.json')")
s=s.replace("header(2,'EL RECINTO","header(3,'EL RECINTO").replace("header(3,'EL CLARO","header(4,'EL CLARO").replace("header(4,'LAS TRES","header(5,'LAS TRES")
s=s.replace("La coronación asciende desde el fondo hasta una cumbrera descentrada y desciende hacia la boca. El muro de tierra arranca de un zócalo de piedra. La puerta atraviesa ambas capas y deja ver el espesor del testero.","La coronación asciende desde el fondo hasta una cumbrera descentrada y desciende hacia la boca. Los dos testeros comparten ese perfil desde el zócalo hasta la cubierta. La puerta baja atraviesa el testero oeste.")
insert=s.index("header(3,'EL RECINTO")
s=s[:insert]+'''header(2,'LA MIRADA EN CUCLILLAS','De testero a testero')
text(30,105,'Los dos faldones conservan sus pendientes a lo largo de la casa. Una viga de madera enlaza los testeros bajo la cumbrera.', 'Texto',12)
snap(rr/'chujlla_desde_arriba.png',29,137,442,260)
snap(rr/'chujlla_desde_el_fondo.png',488,137,442,260)
captions('Desde la puerta y el frente abierto','Desde el fondo y el testero opuesto',402)
datos=json.loads((out/'medicion.json').read_text())
lines=datos['mallas']
base_front,eave_front,peak,eave_back,base_back=datos['sección']
datum=576
scale=32
centers=[178,479,779]
guide_y=datum-peak[2]*scale
pdf.setStrokeColor(HexColor('#9b9287'));pdf.setLineWidth(.55);pdf.setDash(3,3)
pdf.line(64,H-guide_y,892,H-guide_y)
pdf.setDash()
for i,(key,label) in enumerate([('Oeste','Testero oeste'),('0','Centro de la cubierta'),('Este','Testero este')]):
    def plot(y,z):return (centers[i]+(2.20-y)*scale,H-datum+z*scale)
    coords=[plot(y,z) for y,z in lines[key]]
    path=pdf.beginPath()
    path.moveTo(*coords[0])
    for pt in coords[1:]:path.lineTo(*pt)
    if key!='0':
        path.lineTo(*plot(base_back[1],0));path.lineTo(*plot(base_front[1],0));path.close()
        pdf.setFillColor(HexColor('#ebe0d0'));pdf.setStrokeColor(HexColor('#796654'));pdf.setLineWidth(.85);pdf.drawPath(path,stroke=1,fill=1)
    path=pdf.beginPath();path.moveTo(*coords[0])
    for pt in coords[1:]:path.lineTo(*pt)
    pdf.setStrokeColor(HexColor('#93482f'));pdf.setLineWidth(1.65);pdf.drawPath(path)
    ptx,pty=plot(peak[1],lines[key][min(range(len(lines[key])),key=lambda k:abs(lines[key][k][0]-peak[1]))][1])
    pdf.setFillColor(HexColor(accent));pdf.circle(ptx,pty,2,stroke=0,fill=1)
    pdf.setFillColor(HexColor(ink));pdf.setFont('Negrita',11);pdf.drawCentredString(centers[i],H-595,label)
text(30,612,'Las tres coronaciones se midieron sobre las mallas de Blender y se dibujaron a la misma escala y con la misma orientación.','Texto',10,soft)
foot();pdf.showPage()
'''+s[insert:]
p.joinpath('laminas.py').write_text(s)
# Keep the filenames of the primary deliverables stable so older project links open this revision.
q=Path('/tmp/fidelidad/finishing.py').read_text().replace("stage=Path('/tmp/fidelidad')","stage=Path('/tmp/testeros')").replace("Path('/workspace/La_tierra_que_queda/Revision_3D/renders')","Path('/tmp/testeros/renders')")
a=q.index('sources={');b=q.index('for key in sys.argv',a)
q=q[:a]+"sources={'estudio_03':'raw_estudio_03','sitio_03':'raw_sitio_03','chujlla_desde_arriba':'raw_alta','chujlla_desde_el_fondo':'raw_fondo'}\n"+q[b:]
p.joinpath('limpiar.py').write_text(q)
