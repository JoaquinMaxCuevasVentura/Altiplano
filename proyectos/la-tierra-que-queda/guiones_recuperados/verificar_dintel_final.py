from math import isclose
from pathlib import Path
import bpy

scenes={s.name[0]:s for s in bpy.data.scenes}
assert set(scenes)=={'A','B','C'}, list(scenes)
coords=[]
for key,scene in scenes.items():
    walls=[o for o in scene.objects if o.name.startswith('Pirca')]
    assert len(walls)==2
    assert all(o.modifiers[0].node_group.name=='Pirca · montaje de piedras' for o in walls)
    assert all(o.data.attributes.get('medidas') and o.data.attributes.get('giro') for o in walls)
    assert scene.unit_settings.system=='METRIC'
    shades={next(o for o in scene.objects if o.type=='MESH' and o.name.startswith(prefix)).data.materials[0].name for prefix in ('Suelo','Cubierta sur')}
    assert shades=={'Tierra · árido y polvo','Cubierta · acero patinado'}
    cam=next(o for o in scene.objects if o.type=='CAMERA' and o.name.startswith('Llegada'))
    sol=next(o for o in scene.objects if o.type=='LIGHT')
    coords.append((tuple(cam.location),tuple(cam.rotation_euler),tuple(sol.rotation_euler)))
    bpy.context.window.scene=scene
    inst_count=sum(i.is_instance for i in bpy.context.evaluated_depsgraph_get().object_instances)
    assert inst_count>550, inst_count
    print(scene.name, inst_count, 'instancias evaluadas')
assert coords[0]==coords[1]==coords[2]
assert isclose(scenes['A']['ancho_junta_m'],.30) and isclose(scenes['B']['ancho_junta_m'],.65)
assert scenes['C']['piedras_reubicadas']>0
assert all(not i.filepath or i.source in ('GENERATED','VIEWER') for i in bpy.data.images)
print('Piezas que giran en C:', scenes['C']['piedras_reubicadas'])

scene=scenes['C']
scene.camera=next(o for o in scene.objects if o.type=='CAMERA' and o.name.startswith('Encuentro'))
scene.render.threads=2
scene.cycles.samples=36
scene.render.resolution_x=800
scene.render.resolution_y=530
scene.render.filepath=str(Path('/workspace/La_tierra_que_queda')/'Detalle_piedra_y_cubierta.png')
bpy.ops.render.render(write_still=True)
