import bpy
import math
from pathlib import Path
scenes=sorted(bpy.data.scenes,key=lambda scene:scene.name)
assert len(scenes)==3
assert bpy.context.scene==scenes[0]
assert not any(image.source=='FILE' and not image.packed_file for image in bpy.data.images)
for scene in scenes:
    assert scene.unit_settings.system=='METRIC'
    assert scene.unit_settings.scale_length==1
    assert len([o for o in scene.objects if o.type=='CAMERA'])==2
    assert scene.camera.type=='CAMERA' and scene.camera.data.type=='PERSP'
    assert scene.render.filepath.startswith('//renders/')
    assert not any(o.name.startswith(('Mesa continua','D · Base estratificada','Tablero de maqueta','Suelo con relieve de árido')) for o in scene.objects)
    assert any(o.name.startswith('Pampa continua') for o in scene.objects)
rec,clear,chujlla=scenes
assert len([o for o in rec.objects if o.name.startswith('Zapata aislada')])==3
assert len([o for o in clear.objects if o.name.startswith('Fundación aislada')])==12
assert len([o for o in clear.objects if o.name.startswith('D · Costilla')])==4
cloth=next(o for o in clear.objects if o.name.startswith('D · Membrana'))
print('Borde bajo de la membrana:',round(min(v.co.z for v in cloth.data.vertices),2),'m')
assert any(o.name.startswith('Vidrio laminado') for o in chujlla.objects)
assert any(o.name.startswith('Reparto de luz') for o in chujlla.objects)
assert any(o.name.startswith('Conducto de extracción') for o in chujlla.objects)
assert sum(o.name.startswith('Atado de fibra') for o in chujlla.objects)>100
print('Escenas, Geometry Nodes, terrenos, fundaciones, cámaras y lucernario verificados al reabrir')
