from pathlib import Path
import time,subprocess,sys,os
from PIL import Image
p=Path('/tmp/testeros')
for key in ('estudio_03','sitio_03'):
    for _ in range(240):
        try:
            with Image.open(p/('raw_'+key+'.png')) as im:im.verify()
            break
        except (OSError,SyntaxError):time.sleep(2)
    else:raise RuntimeError(key)
    subprocess.run([sys.executable,str(p/'limpiar.py'),key],env=dict(os.environ,PYTHONPATH='/tmp/anteproyecto/denoise',OMP_NUM_THREADS='2'),check=True)
subprocess.run([sys.executable,str(p/'cerrar.py')],check=True)
