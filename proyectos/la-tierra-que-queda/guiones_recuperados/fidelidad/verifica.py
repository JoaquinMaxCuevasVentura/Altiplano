import bpy,math,sys
from pathlib import Path
from mathutils import Vector
out=Path('/workspace/La_tierra_que_queda/Revision_3D')
stages=sorted([s for s in bpy.data.scenes if not s.name.startswith('Sitio')],key=lambda s:s.name)
built=sorted([s for s in bpy.data.scenes if s.name.startswith('Sitio')],key=lambda s:s.name)
assert len(stages)==len(built)==3
def ob(scene,key):return next(o for o in scene.objects if o.name.startswith(key))
if 'ajustar' in sys.argv:
    for o in built[2].objects:
        if o.name.startswith('Pedestal bajo el pie derecho'):
            center=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
            x,y,_=center
            slit=1.61+.245*y+.027*math.sin(8.4*y)+.014*math.sin(24*y+.4)
            dx=x-slit
            f=max(0,1-abs(dx)/1.68)
            o.location.x-=.64*f*f*(3-2*f)*(1-.22*max(0,y)/5)
            if abs(dx)<.70:
                o.location.x+=math.copysign(.103,dx)*math.exp(-(dx/.42)**2)*max(.12,1-max(0,y)/4.7)
    note=bpy.data.texts.new('00 · Guía de la revisión')
    note.write('La tierra que queda · revisión de las tres referencias\n\n'
               '01, 02 y 03 abren las vistas de cotejo con sus cámaras de estudio. Las escenas Sitio contienen los anteproyectos implantados en el paisaje de ensayo. Las tres parejas comparten objetos de construcción.\n\n'
               '01. Pirca de dos caras con corazón de piedra y pasantes. El recinto gana profundidad. La chapa presenta una diagonal baja y dos extremos levantados.\n'
               '02. La escala se aplica al conjunto completo una vez recuperada la curva del paño seleccionado. Las costillas y la piedra testigo se pueden editar por separado.\n'
               '03. La vista de estudio abre el frente a la altura de los testeros y restituye la figura de escala. La escena Sitio 03 conserva la fachada y el sistema de resalto y tapajuntas sobre el vidrio. El haz de la sección es un ensayo de iluminación dirigido.\n')
    for idx,(s,t) in enumerate(zip(stages,built),1):
        s.render.filepath=f'//renders/estudio_{idx:02d}.png'
        t.render.filepath=f'//renders/sitio_{idx:02d}.png'
    bpy.context.window.scene=stages[0]
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath,compress=True)
for idx,(s,t) in enumerate(zip(stages,built)):
    key=['Abrigo independiente','D · Membrana con borde','Cubierta · costra de tierra'][idx]
    assert ob(s,key)==ob(t,key)
    assert s.camera.type=='CAMERA' and t.camera.type=='CAMERA'
    assert s.unit_settings.system==t.unit_settings.system=='METRIC'
    print(s.name,'y',t.name, 'comparten',ob(s,key).name)
assert any(o.name.startswith('Muro sur') for o in built[2].objects)
assert not any(o.name.startswith('Muro sur') for o in stages[2].objects)
assert any(o.name.startswith('Figura en cuclillas') for o in stages[2].objects)
canopy=ob(stages[1],'D · Membrana con borde')
z=min((canopy.matrix_world@v.co).z for v in canopy.data.vertices)
print('Borde mínimo respecto del plano base',round(z,3))
assert 1.99<z<2.04
assert not any(im.source=='FILE' and not im.packed_file for im in bpy.data.images)
print('Materiales autónomos. Fachada y sección comprobadas.')
