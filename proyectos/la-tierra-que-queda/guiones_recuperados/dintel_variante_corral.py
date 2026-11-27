import math
from pathlib import Path

import bpy
from mathutils import Vector

out=Path('/workspace/La_tierra_que_queda')
base=next(s for s in bpy.data.scenes if abs(s['ancho_junta_m']-.65)<.001)
scene=base.copy()
scene.name='C · la pirca recompuesta'
scene['alcance']='Ensayo espacial. La cubierta acaba antes que el muro, cuyo último tramo gira.'
scene['giro_del_tramo_grados']=-90.
scene['abertura_final']='Parcialmente descubierta, sin cambiar la abertura longitudinal en el resto del paso.'

def from_scene(prefix):
    return next(o for o in scene.objects if o.name.startswith(prefix))
def replace(obj):
    new=obj.copy()
    new.data=obj.data.copy()
    scene.collection.objects.unlink(obj)
    scene.collection.objects.link(new)
    return new

wall=replace(from_scene('Pirca norte'))
wall.name='Pirca norte · tramo girado'
pivot_x=7.62
pivot_y=3.565
turned_count=0
for v in wall.data.vertices:
    x,y,z=v.co
    if x>pivot_x:
        v.co=(pivot_x+y-pivot_y,pivot_y-(x-pivot_x),z)
        wall.data.attributes['giro'].data[v.index].vector.z-=math.pi/2
        turned_count+=1
assert turned_count
scene['piedras_reubicadas']=turned_count
wall.data.update()

roof=replace(next(o for o in scene.objects if o.type=='MESH' and o.name.startswith('Cubierta norte')))
roof.name='Cubierta norte · termina antes de la pirca'
end=6.72
for v in roof.data.vertices:
    if v.co.x>end:
        delta=v.co.x-end
        v.co.x=end
        if v.index==3:
            v.co.y-=.061*delta
roof.data.update()
for obj in [o for o in scene.objects if o.type=='CURVE' and o.name.startswith('Cubierta norte')]:
    if 'junta de chapa' in obj.name and obj.data.splines[0].points[0].co.x>end:
        scene.collection.objects.unlink(obj)
    if 'remate del apoyo' in obj.name:
        remate=replace(obj)
        remate.data.splines[0].points[1].co.x=end

def camera(name,position,target,lens):
    data=bpy.data.cameras.new(name)
    cam=bpy.data.objects.new(name,data)
    scene.collection.objects.link(cam)
    cam.location=position
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    data.lens=lens
    return cam

scene.camera=camera('Pausa · pirca y cielo',(9.54,1.67,1.90),(5.43,2.76,1.14),27)
scene.render.filepath='//C_pirca_recompuesta.png'
readme=bpy.data.texts['LEEME · ensayo comparativo']
readme.write('\nC: se conserva la junta de B. Se acorta una de las dos hojas de cubierta y se giran '
             + str(turned_count) + ' piedras del último tramo de la pirca norte para dejar un pequeño recinto abierto. '
             'La cámara Pausa mira el remate desde el otro extremo. Se inspira en la relación entre cerco y '
             'resguardo de Corral, en Obra Gruesa de Smiljan Radić (PDF, p. 31 / impresa 204), '
             'y en el retorno y la reparación de las pircas en Altiplano (ed. 1982, pp. 155–156).\n')
window=bpy.context.window
window.scene=scene
# Preserve the A/B file for reproducibility and save the book-informed proposal as a new artifact.
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Dintel_Jatun_Kolla.blend'))
scene.cycles.samples=40
scene.render.threads=2
scene.render.filepath=str(out/'C_pirca_recompuesta.png')
bpy.ops.render.render(write_still=True)
print(f'Tres escenas listas. La variante C reubica {turned_count} piedras.')
