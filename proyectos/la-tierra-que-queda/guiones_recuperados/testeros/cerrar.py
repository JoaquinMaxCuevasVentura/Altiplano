from zipfile import ZipFile,ZIP_STORED
from pathlib import Path
import os,shutil,sys,subprocess
import fitz
from PIL import Image
p=Path('/tmp/testeros')
orig=Path('/workspace/La_tierra_que_queda/Revision_3D')
for name in ('cubierta_detalle','estudio_01','estudio_02','sitio_01','sitio_02'):
    shutil.copy2(orig/'renders'/(name+'.png'),p/'renders'/(name+'.png'))
for path in (p/'renders').glob('*.png'):
    with Image.open(path) as im:im.verify()
subprocess.run([sys.executable,str(p/'laminas.py')],check=True)
pdf=p/'La_tierra_que_queda_Revision.pdf';blend=p/'La_tierra_que_queda_Revision.blend'
proof=p/'Chujlla_de_testero_a_testero.png'
with fitz.open(pdf) as doc:
    assert len(doc)==5 and 'De testero a testero' in doc[1].get_text()
    assert len(doc[1].get_images())==2
    doc[1].get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False).save(proof)
    doc[1].get_pixmap(matrix=fitz.Matrix(.78,.78),alpha=False).save(p/'control.png')
srcs=[blend,pdf,proof,*sorted(p.glob('Comparacion_*.png')),*sorted((p/'renders').glob('*.png'))]
zipfile=p/'La_tierra_que_queda_Revision.zip'
with ZipFile(zipfile,'w',compression=ZIP_STORED) as z:
    for path in srcs:z.write(path,path.relative_to(p))
with ZipFile(zipfile) as z:
    assert len(z.namelist())==14 and z.testzip() is None
for src in [*srcs,zipfile]:
    dst=orig/src.relative_to(p)
    tmp=dst.with_name('.'+dst.name+'.incoming')
    shutil.copyfile(src,tmp);os.replace(tmp,dst)
print('Cinco páginas. Dos cámaras nuevas. Paquete verificado.')
