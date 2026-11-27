from pathlib import Path
import shutil, subprocess, sys,fitz
p=Path('/tmp/testeros')
q=p/'prueba';q.mkdir(exist_ok=True)
rr=q/'renders';rr.mkdir(exist_ok=True)
for src in Path('/workspace/La_tierra_que_queda/Revision_3D/renders').glob('*.png'):
    shutil.copy2(src,rr/src.name)
for key,src in [('chujlla_desde_arriba','raw_pre_alta.png'),('chujlla_desde_el_fondo','raw_pre_fondo.png')]:
    shutil.copy2(p/src,rr/(key+'.png'))
for n in ['traza.json','medicion.json']:shutil.copy2(p/n,q/n)
s=(p/'laminas.py').read_text().replace("out=Path('/tmp/testeros')","out=Path('/tmp/testeros/prueba')")
(q/'laminas.py').write_text(s)
subprocess.run([sys.executable,str(q/'laminas.py')],check=True)
with fitz.open(q/'La_tierra_que_queda_Revision.pdf') as d:d[1].get_pixmap(matrix=fitz.Matrix(.73,.73),alpha=False).save(q/'vistaprevia.png')
