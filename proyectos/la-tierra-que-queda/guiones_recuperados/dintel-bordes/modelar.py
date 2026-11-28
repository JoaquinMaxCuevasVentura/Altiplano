import math
import random
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

folder = Path('/workspace/La_tierra_que_queda')
sheet = bpy.data.materials['Cubierta · acero patinado']
joint = bpy.data.materials['Cubierta · juntas y remate']
scenes = list(bpy.data.scenes)
rock_library = bpy.data.collections['Biblioteca · 12 formas de piedra']

def bevel(obj, name, width, segments, angle=None):
    modifier = obj.modifiers.new(name, 'BEVEL')
    modifier.width = width
    modifier.segments = segments
    modifier.harden_normals = True
    if angle is not None:
        modifier.limit_method = 'ANGLE'
        modifier.angle_limit = math.radians(angle)
    return modifier

def round_stones():
    for index, piece in enumerate(sorted(rock_library.objects, key=lambda obj: obj.name)):
        bm = bmesh.new()
        bm.from_mesh(piece.data)
        if index % 3 != 1:
            rng = random.Random(902 + index * 39)
            facet_normal = Vector((rng.choice((-1, 1)) * .57,
                                   rng.choice((-1, 1)) * .74, rng.uniform(.30, .58))).normalized()
            extremum = max(facet_normal.dot(v.co) for v in bm.verts)
            limit = extremum - rng.uniform(.045, .075)
            for vertex in bm.verts:
                excess = facet_normal.dot(vertex.co) - limit
                if excess > 0:
                    vertex.co -= facet_normal * excess
        bm.normal_update()
        for face in bm.faces:
            face.smooth = True
        for edge in bm.edges:
            edge.smooth = edge.is_manifold and edge.calc_face_angle(0.) < math.radians(34)
        bm.to_mesh(piece.data)
        bm.free()
        piece.data.update()
        edge_rounding = bevel(piece, 'Aristas expuestas · redondeo localizado',
                              .025 if index % 3 == 0 else .018, 3, 27)
        edge_rounding.affect = 'EDGES'

def new_mesh(scene, name, vertices, faces, material):
    data = bpy.data.meshes.new(name)
    data.from_pydata(vertices, [], faces)
    if material:
        data.materials.append(material)
    bm = bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(data)
    bm.free()
    data.update()
    obj = bpy.data.objects.new(name, data)
    scene.collection.objects.link(obj)
    return obj

def sweep(scene, name, line, direction, profile, material, radius):
    vertices = [tuple(center + direction * lateral + Vector((0., 0., height)))
                for center in line for lateral, height in profile]
    sides = len(profile)
    faces = [tuple(reversed(range(sides)))]
    for i in range(len(line)-1):
        for j in range(sides):
            k = (j+1) % sides
            faces.append((i*sides+j, i*sides+k, (i+1)*sides+k, (i+1)*sides+j))
    faces.append(tuple(range(len(vertices)-sides, len(vertices))))
    obj = new_mesh(scene, name, vertices, faces, material)
    edge_rounding = bevel(obj, 'Radio de plegado', radius, 3, 19)
    edge_rounding.loop_slide = False
    return obj

def normal_xy(start, end, sign):
    delta = end-start
    return Vector((-delta.y * sign, delta.x * sign, 0.)).normalized()

def light_wave(start, end, normal):
    points = []
    subdivisions = max(2, math.ceil((end-start).length / .25))
    for index in range(subdivisions+1):
        t = index/subdivisions
        shift = math.sin(math.tau*4*t)*math.sin(math.pi*t)*.00055
        points.append(start.lerp(end, t) + normal*shift)
    return points

def old_part(scene, obj):
    scene.collection.objects.unlink(obj)
    if obj.users == 0:
        bpy.data.objects.remove(obj)

covered = set()
round_stones()
lip_profile = [(-.006,.0002),(.0025,.0002),(.0045,-.002),
               (.0045,-.0105),(.002,-.013),(-.0014,-.013),
               (-.0014,-.004),(-.006,-.004)]
rib_profile = [(-.008,-.0015),(-.006,.001),(-.002,.008),
               (.002,.008),(.006,.001),(.008,-.0015)]
for scene in scenes:
    for side in ('sur', 'norte'):
        prefix = 'Cubierta ' + side
        roof = next(obj for obj in scene.objects if obj.type == 'MESH' and obj.name.startswith(prefix))
        start = [v.co.copy() for v in roof.data.vertices[:3]]
        end = [v.co.copy() for v in roof.data.vertices[3:]]
        if roof not in covered:
            solid = next(mod for mod in roof.modifiers if mod.type == 'SOLIDIFY')
            solid.name = 'Espesor de chapa · 5 mm'
            solid.thickness = .005
            solid.offset = -1
            original_bevel = next(mod for mod in roof.modifiers if mod.type == 'BEVEL')
            original_bevel.name = 'Bisel fino del canto'
            original_bevel.width = .00125
            original_bevel.segments = 3
            original_bevel.harden_normals = True
            covered.add(roof)
        for endpoint, name, sign in ((0, 'borde lateral', -1), (2, 'borde lateral', 1)):
            sky = (side == 'sur' and endpoint == 2) or (side == 'norte' and endpoint == 0)
            direction = normal_xy(start[endpoint], end[endpoint], sign)
            run = light_wave(start[endpoint], end[endpoint], direction)
            sweep(scene, prefix+' · '+('doblez junto a la luz' if sky else 'doblez de alero'),
                  run, direction, lip_profile, sheet, .00085)
        for edge, sign, label in ((start,-1,'entrada'), (end,1,'salida')):
            sweep(scene,prefix+' · canto de '+label,edge,Vector((sign,0.,0.)),lip_profile,sheet,.00085)

        existing = [o for o in scene.objects if o.type == 'CURVE' and o.name.startswith(prefix)]
        for part in existing:
            if 'junta de chapa' in part.name:
                x = part.data.splines[0].points[0].co.x
                t = (x-start[0].x)/(end[0].x-start[0].x)
                if 0. < t < 1.:
                    run = [a.lerp(b,t) for a,b in zip(start,end)]
                    for point in run:
                        point.x = x
                    sweep(scene,prefix+' · junta doblada',run,Vector((1.,0.,0.)),rib_profile,joint,.0012)
                old_part(scene,part)
            elif 'remate del apoyo' in part.name:
                old_part(scene,part)

        outer, fold, y_limits = (0,1,(.745,.825)) if side == 'sur' else (2,1,(3.61,3.71))
        a, b = start[outer], start[fold]
        def top_z(y):
            return a.z + (b.z-a.z)*(y-a.y)/(b.y-a.y) - .004
        bearing_profile = [(y_limits[0],1.153),(y_limits[1],1.153),
                           (y_limits[1],top_z(y_limits[1])),(y_limits[0],top_z(y_limits[0]))]
        sweep(scene,prefix+' · apoyo plegado', [Vector((start[0].x+.017,0.,0.)),
              Vector((end[0].x-.017,0.,0.))], Vector((0.,1.,0.)),bearing_profile,joint,.003)

readme = bpy.data.texts['LEEME · ensayo comparativo']
readme.write('\nBordes: las piedras tienen pequeños desconchados y aristas redondeadas por ángulo. '
             'Las hojas de cubierta tienen espesor de 5 mm para el estudio, dobleces en los cantos, '
             'juntas plegadas y apoyos con sus extremos cerrados. Las piezas de borde siguen la geometría del modelo.\n')
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'Dintel_Jatun_Kolla.blend'))
scene = next(s for s in scenes if s.name.startswith('C'))
bpy.context.window.scene = scene
scene.camera = next(o for o in scene.objects if o.type == 'CAMERA' and o.name.startswith('Encuentro'))
scene.render.threads = 3
scene.cycles.samples = 36
scene.render.resolution_x = 800
scene.render.resolution_y = 530
scene.render.filepath = str(folder/'Detalle_de_bordes.png')
bpy.ops.render.render(write_still=True)
