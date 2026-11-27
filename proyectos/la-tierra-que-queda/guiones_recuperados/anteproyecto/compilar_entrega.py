from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import typst
from PIL import Image

root=Path('/workspace/La_tierra_que_queda/Anteproyecto')
dossier=root/'La_tierra_que_queda_Dossier.pdf'
archive=root/'La_tierra_que_queda_Fuentes_editoriales.zip'
files=[root/'Dossier.typ']
for kind in ('graficos','renders','img2img'):
    files.extend(sorted((root/kind).glob('*')))
assert all(f.stat().st_size>0 for f in files)
for kind in ('renders','img2img'):
    captures=sorted((root/kind).glob('*.jpg'))
    assert len(captures)==4
    for f in captures:
        with Image.open(f) as im:
            assert im.width>=1400 and im.height>=900, (f,im.size)
            im.verify()
typst.compile(str(root/'Dossier.typ'),output=str(dossier))
with ZipFile(archive,mode='w',compression=ZIP_DEFLATED,compresslevel=5) as zip_file:
    zip_file.write('/tmp/anteproyecto/LEEME_fuentes.txt','LEEME.txt')
    for file in files:
        zip_file.write(file,file.relative_to(root))
with ZipFile(archive) as zip_file:
    assert zip_file.testzip() is None
print(dossier,archive,sep='\n')
