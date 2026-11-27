from zipfile import ZipFile,ZIP_STORED
from pathlib import Path
from PIL import Image
import fitz
p=Path('/workspace/La_tierra_que_queda/Revision_3D')
docpath=p/'La_tierra_que_queda_Revision.pdf'
with fitz.open(docpath) as doc:
 assert len(doc)==4
 assert 'La casa de tres muros' in doc[0].get_text()
 assert all(len(page.get_images())>=2 for page in doc)
 thumbs=Image.new('RGB',(720,502),'#d4cdbf')
 for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(.362,.362),alpha=False)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    thumbs.paste(im,((i%2)*360+5,i//2*251+4))
 thumbs.save('/tmp/fidelidad/control_pdf.jpg',quality=85)
blend=p/'La_tierra_que_queda_Revision.blend'
with (p/'La_tierra_que_queda_Revision.zip').open('wb') as output:
 with ZipFile(output,'w',compression=ZIP_STORED) as archive:
    for path in [blend,docpath,*sorted(p.glob('Comparacion_*.png')),*sorted((p/'renders').glob('*.png'))]:
        if path.suffix=='.png':
            with Image.open(path) as im:im.verify()
        archive.write(path,str(path.relative_to(p)))
with ZipFile(p/'La_tierra_que_queda_Revision.zip') as archive:
 assert archive.testzip() is None and len(archive.namelist())==11
print('4 láminas, 7 renders, 2 cotejos y un proyecto Blender de seis escenas.')
