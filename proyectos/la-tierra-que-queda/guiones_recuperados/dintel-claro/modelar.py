import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector, noise

out = Path('/workspace/La_tierra_que_queda')
base = next(s for s in bpy.data.scenes if s.name.startswith('B'))
scene = bpy.data.scenes.new('D · El claro de la piedra')
scene.use_fake_user = True
scene.unit_settings.system = 'METRIC'
scene['origen'] = 'Ensayo basado en las cinco maquetas de Joaquin Cuevas y el retorno de Altiplano, pp. 155–156.'
scene['decision'] = 'Conservar un paso bajo, abrir la planta al final y dejar una piedra fuera del eje.'
scene['hipotesis_material'] = 'Membrana translúcida sobre costillas delgadas. Geometría exploratoria.'

def blendstep(a, b, x):
    t = min(1., max(0., (x-a)/(b-a)))
    return t*t*(3-2*t)

def centerline(side, x):
    throat = math.exp(-((x-1.72)/1.22)**2)
    if side == 'sur':
        return Vector((x, .925+.27*throat-.91*blendstep(3.0,7.15,x)))
    if x <= 6.55:
        return Vector((x, 3.565-.25*throat+1.03*blendstep(3.1,6.55,x)))
    angle = .55*(x-6.55)
    return Vector((6.55+math.sin(angle)/.55, 4.595+(math.cos(angle)-1)/.55))

def frame(side, x):
    c = centerline(side,x)
    t = (centerline(side,x+.001)-centerline(side,x-.001)).normalized()
    return c, t, Vector((-t.y,t.x))

def make_mesh(name, verts, faces, material, smooth=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    if material:
        data.materials.append(material)
    if smooth:
        for poly in data.polygons:
            poly.use_smooth = True
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    return obj

def bevel(obj, width, segments=3):
    mod = obj.modifiers.new('Canto redondeado', 'BEVEL')
    mod.width = width
    mod.segments = segments
    mod.harden_normals = True

def box(name, x0,x1,y0,y1,z0,z1, material):
    verts = [(x,y,z) for z in (z0,z1) for y in (y0,y1) for x in (x0,x1)]
    return make_mesh(name,verts,[(0,2,3,1),(4,5,7,6),(0,1,5,4),(1,3,7,5),(3,2,6,7),(2,0,4,6)],material)

def tube(name, points, radius, material):
    data = bpy.data.curves.new(name,'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 1
    data.bevel_depth = radius
    data.bevel_resolution = 3
    data.use_fill_caps = True
    data.materials.append(material)
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point, coord in zip(spline.points, points):
        point.co = (*coord,1.)
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    return obj

def simple(name, color, roughness, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color,1.)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color,1.)
    node.inputs['Roughness'].default_value = roughness
    node.inputs['Metallic'].default_value = metallic
    return mat

def move_wall(side, source_y):
    source = next(o for o in base.objects if o.name.startswith('Pirca '+side))
    new = source.copy()
    new.data = source.data.copy()
    new.name = 'D · Pirca '+side
    scene.collection.objects.link(new)
    rotations = new.data.attributes['giro'].data
    for vertex in new.data.vertices:
        x,y,z = vertex.co
        center, tangent, normal = frame(side,x)
        mapped = center + normal*(y-source_y)
        vertex.co = (*mapped,z)
        rotations[vertex.index].vector.z += math.atan2(tangent.y,tangent.x)
    new.data.update()
    new['operacion'] = 'La pirca conserva su aparejo por instancias y cambia de trazado en planta.'
    return new

walls = [move_wall('sur',.925), move_wall('norte',3.565)]
rod = simple('D · Metal oscurecido',(.085,.065,.041),.60,.53)
thread = simple('D · Costura de lino',(.37,.24,.115),.91)
stage = simple('D · Fondo de estudio',(.28,.25,.215),.87)
plywood = [
    simple('D · Contrachapado claro',(.39,.25,.128),.83),
    simple('D · Cola oscura del canto',(.18,.112,.055),.94),
]
earthen = bpy.data.materials['Tierra · árido y polvo']
box('D · Fondo continuo para fotografiar la maqueta',-80,80,-80,80,-.59,-.51,stage)
for k in range(7):
    bottom = -.50+k*.055
    piece = box(f'D · Base estratificada {k+1}',-.40,9.25,-1.08,5.75,bottom,bottom+.055,plywood[k%2])
    bevel(piece,.026)
silt = box('D · Borde del estrato de tierra',-.397,9.247,-1.077,5.747,-.118,-.018,earthen)
bevel(silt,.026)

stone_x, stone_y = 6.91,3.28
line_a = Vector((5.81,1.02))
line_b = Vector((6.66,2.94))
line_delta = line_b-line_a
def ground_z(x,y):
    recessed = math.exp(-(((x-stone_x)/.78)**2+((y-stone_y)/.96)**2))
    point = Vector((x,y))
    s = min(1.,max(0.,(point-line_a).dot(line_delta)/line_delta.length_squared))
    foot = line_a+line_delta*s
    groove = -.027*math.exp(-((point-foot).length/.045)**2)*math.sin(math.pi*s)**.32
    return -.014-.143*recessed + .017*noise.noise(Vector((x*1.65,y*1.65,1.7))) + groove

nx, ny = 163,114
terrain_verts = []
for j in range(ny+1):
    y = -1.074+(5.743+1.074)*j/ny
    for i in range(nx+1):
        x = -.394+(9.244+.394)*i/nx
        z = ground_z(x,y)
        if i in (0,nx) or j in (0,ny):
            z = -.018
        terrain_verts.append((x,y,z))
faces = [(j*(nx+1)+i, j*(nx+1)+i+1, (j+1)*(nx+1)+i+1, (j+1)*(nx+1)+i)
         for j in range(ny) for i in range(nx)]
make_mesh('D · Suelo excavado y surco discontinuo',terrain_verts,faces,earthen,True)

source_gravel = next(o for o in base.objects if o.name.startswith('Grava dispersa'))
gravel_obj = source_gravel.copy()
gravel_obj.data = source_gravel.data.copy()
scene.collection.objects.link(gravel_obj)
gravel_obj.name = 'D · Grava en el pie de las pircas'
for vertex in gravel_obj.data.vertices:
    x,y,z = vertex.co
    side = 'sur' if y<2.2 else 'norte'
    c, _, normal = frame(side,x)
    displacement = y-(.925 if side == 'sur' else 3.565)
    mapped = c+normal*displacement
    if mapped.x < 9.24 and -1.05 < mapped.y < 5.73:
        vertex.co = (*mapped,ground_z(*mapped)+z+.009)
    else:
        vertex.co = (x,.40,ground_z(x,.40)+.008)
gravel_obj.data.update()

library = bpy.data.collections['Biblioteca · 12 formas de piedra']
prototype = sorted(library.objects,key=lambda obj:obj.name)[6]
marker = prototype.copy()
marker.data = prototype.data.copy()
scene.collection.objects.link(marker)
marker.name = 'D · Piedra testigo fuera del eje'
marker.location = (stone_x,stone_y,ground_z(stone_x,stone_y)+.470)
marker.scale = (1.30,.96,.92)
marker.rotation_euler = (.04,.13,-.51)
marker.data.materials.clear()
marker.data.materials.append(bpy.data.materials['Piedra · gris clara'])

cloth = simple('D · Membrana cruda translúcida',(.76,.63,.45),.92)
n = cloth.node_tree.nodes
l = cloth.node_tree.links
principled = n.get('Principled BSDF')
principled.location = (430,125)
principled.inputs['Sheen Weight'].default_value = .28
trans = n.new('ShaderNodeBsdfTranslucent')
trans.location = (434,-125)
trans.inputs['Color'].default_value = (.86,.73,.54,1.)
mix = n.new('ShaderNodeMixShader')
mix.location = (710,140)
mix.inputs[0].default_value = .42
out_n = n.get('Material Output')
out_n.location = (950,140)
l.new(principled.outputs[0],mix.inputs[1])
l.new(trans.outputs[0],mix.inputs[2])
l.new(mix.outputs[0],out_n.inputs['Surface'])
geom = n.new('ShaderNodeNewGeometry')
geom.location = (-735,102)
fine = n.new('ShaderNodeTexNoise')
fine.location = (-300,130)
fine.inputs['Scale'].default_value = 255.
fine.inputs['Detail'].default_value = 2.3
fine.label = 'Fibra fina de la membrana'
anisotropy = n.new('ShaderNodeVectorMath')
anisotropy.operation = 'MULTIPLY'
anisotropy.inputs[1].default_value = (1.,2.7,1.)
anisotropy.location = (-520,115)
l.new(geom.outputs['Position'],anisotropy.inputs[0])
l.new(anisotropy.outputs[0],fine.inputs[0])
bump = n.new('ShaderNodeBump')
bump.location = (108,135)
bump.inputs['Strength'].default_value = .30
bump.inputs['Distance'].default_value = .004
l.new(fine.outputs['Fac'],bump.inputs['Height'])
l.new(bump.outputs[0],principled.inputs['Normal'])

def membrane(t, s):
    cut = .52*math.exp(-((s-.58)/.135)**2)
    a = .30+.52*s
    b = 5.70+.84*s-cut
    x = a+(b-a)*t
    left = centerline('sur',x).y-.18
    right = centerline('norte',x).y+.16
    y = left+(right-left)*s
    z0 = 1.70+.30*t+.12*math.cos(t*math.pi*1.45)
    z1 = 1.73+.44*t+.13*math.sin(t*math.pi/2)
    curvature = math.sin(math.pi*s)*(.55+.25*t+.13*math.sin(math.pi*t))
    sag = -.071*math.sin(t*math.pi*3)**2*math.sin(math.pi*s)
    return (x,y,z0*(1-s)+z1*s+curvature+sag)

nt, ns = 64,50
surface = [membrane(i/nt,j/ns) for j in range(ns+1) for i in range(nt+1)]
surface_faces = [(j*(nt+1)+i,j*(nt+1)+i+1,(j+1)*(nt+1)+i+1,(j+1)*(nt+1)+i)
                 for j in range(ns) for i in range(nt)]
hood = make_mesh('D · Membrana con borde recortado sobre el claro',surface,surface_faces,cloth,True)
solid = hood.modifiers.new('Espesor del tejido en el modelo','SOLIDIFY')
solid.thickness = .004
hood['operacion'] = 'Cubrir el tramo estrecho y recortar el borde sobre el claro.'

for edge,coords in [
    ('bajo', [membrane(i/80,0) for i in range(81)]),
    ('alto', [membrane(i/80,1) for i in range(81)]),
    ('en la llegada', [membrane(0,i/80) for i in range(81)]),
    ('recortado', [membrane(1,i/80) for i in range(81)]),
]:
    tube('D · Dobladillo '+edge,coords,.021,thread)

for i,t in enumerate((.04,.34,.68,.94),1):
    profile = [(x,y,z-.021) for x,y,z in [membrane(t,j/50) for j in range(51)]]
    tube(f'D · Costilla curvada {i}',profile,.025 if i != 4 else .019,rod)
    for side,s in (('sur',0.),('norte',1.)):
        x,y,z = membrane(t,s)
        center = centerline(side,x)
        tube(f'D · Montante {side} {i}',[(center.x,center.y,1.08),(x,y,z-.02)],.037,rod)
        if i in (1,4):
            anchor = (x+(-.23 if i==1 else .27), y+(-.57 if side=='sur' else .65))
            tube(f'D · Tirante {side} {i}',[(x,y,z),(*anchor,ground_z(*anchor)+.055)],.010,rod)

def aim(obj,target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

def camera(name, position, target, lens, scale=None):
    camera_data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name,camera_data)
    scene.collection.objects.link(cam)
    cam.location = position
    aim(cam,target)
    cam.data.lens = lens
    if scale:
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = scale
    return cam

def light(name, loc, target, energy, size, color):
    data = bpy.data.lights.new(name,'AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    data.color = color
    obj = bpy.data.objects.new(name,data)
    scene.collection.objects.link(obj)
    obj.location = loc
    aim(obj,target)

main_camera = camera('D · Maqueta abierta',(13.8,-12.2,10.0),(4.35,2.39,.60),50,12.62)
inside_camera = camera('D · Desde el umbral',(1.09,2.09,1.41),(7.62,2.97,.97),23)
camera('D · Planta',(4.49,2.36,13.0),(4.49,2.36,0),50,11.2)
light('D · Luz lateral de estudio',(5.8,-4.0,10.1),(4.2,2.4,.1),2750,5.6,(1.,.84,.67))
light('D · Luz a través del paño',(3.0,6.8,8.0),(4.1,2.4,.4),2625,4.6,(1.,.90,.77))
light('D · Relleno tenue',(-1.5,1.0,5.4),(4.6,2.5,1.0),550,4.,(.80,.87,1.))
world = bpy.data.worlds.new('D · Ambiente de maqueta')
world.use_nodes = True
background = world.node_tree.nodes.get('Background')
background.inputs['Color'].default_value = (.49,.48,.46,1.)
background.inputs['Strength'].default_value = .30
scene.world = world
scene.camera = main_camera
scene.render.engine = 'CYCLES'
scene.cycles.samples = 45
scene.cycles.use_denoising = False
scene.cycles.max_bounces = 7
scene.cycles.adaptive_threshold = .064
scene.cycles.sample_clamp_indirect = 2.8
scene.render.resolution_x = 960
scene.render.resolution_y = 690
scene.render.threads_mode = 'FIXED'
scene.render.threads = 3
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.render.filepath = '//D_El_claro_de_la_piedra.png'

notes = bpy.data.texts.new('D · Referencias y decisiones')
notes.write("""EL CLARO DE LA PIEDRA · Variante de El dintel de Jatun-Kolla

Maquetas de Joaquin Cuevas. El recinto curvo aporta la relación entre masa, pieza suelta y luz. Las maquetas de estratos y cavidades aportan la idea de un suelo rebajado y de un trazo ligero. El volumen con ranuras convierte la abertura en una operación del espacio. La membrana tensada aporta la relación de peso entre la piedra y una cubierta delgada.

Altiplano, edición de 1982, pp. 155–156. El retorno se cuenta como detenerse en el dintel, tocar el suelo y recomponer las pircas. En la variante D el trazado se abre al final. Una pirca curva delimita un claro de tierra rebajada. El borde recortado del paño deja a la piedra testigo fuera de la sombra. La pieza se coloca fuera del eje y se puede rodear.

El archivo contiene los estudios A, B, C y D. Las pircas y la grava de D se instancian con el grupo de Geometry Nodes del proyecto. Las costillas, los tensores y la membrana se pueden editar por separado. Las cámaras Maqueta abierta y Desde el umbral muestran dos lecturas de la misma geometría. La luminotecnia corresponde a una maqueta digital de estudio.
""")
for original in bpy.data.scenes:
    original.use_fake_user = True
window = bpy.context.window
window.scene = scene
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.region_3d.view_perspective = 'CAMERA'
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Dintel_Jatun_Kolla_El_claro.blend'))

for camera_, file in [(main_camera,'D_El_claro_de_la_piedra.png'),(inside_camera,'D_Desde_el_umbral.png')]:
    scene.camera = camera_
    scene.render.filepath = str(out/file)
    bpy.ops.render.render(write_still=True)
