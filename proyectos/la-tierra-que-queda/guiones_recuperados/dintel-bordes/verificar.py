from math import isclose
from collections import Counter
import bpy
import bmesh

assert len(bpy.data.scenes) == 3
lib = bpy.data.collections['Biblioteca · 12 formas de piedra']
assert len(lib.objects) == 12 and all(len(o.modifiers) == 1 and o.modifiers[0].type == 'BEVEL' for o in lib.objects)
assert all(any(edge.use_edge_sharp for edge in stone.data.edges) for stone in lib.objects)
data = []
for scene in sorted(bpy.data.scenes, key=lambda s: s.name):
    names = Counter()
    roofs = [o for o in scene.objects if o.type == 'MESH' and any(m.type == 'SOLIDIFY' for m in o.modifiers)]
    assert len(roofs) == 2
    for roof in roofs:
        solid = next(m for m in roof.modifiers if m.type == 'SOLIDIFY')
        assert isclose(solid.thickness, .005, abs_tol=1e-6)
    for obj in scene.objects:
        if obj.type != 'MESH' or not obj.name.startswith('Cubierta'):
            continue
        for label in ('doblez de alero','doblez junto a la luz','canto de entrada','canto de salida','apoyo plegado','junta doblada'):
            if label in obj.name:
                names[label] += 1
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                assert all(e.is_manifold for e in bm.edges), obj.name
                bm.free()
    assert all(names[key] == 2 for key in ('doblez de alero','doblez junto a la luz','canto de entrada','canto de salida','apoyo plegado'))
    assert names['junta doblada'] >= 12
    sur = next(o for o in roofs if o.name.startswith('Cubierta sur'))
    norte = next(o for o in roofs if o.name.startswith('Cubierta norte'))
    test_x = 4.
    def at_x(points):
        a,b = points
        return a.y+(b.y-a.y)*(test_x-a.x)/(b.x-a.x)
    measure = at_x([norte.data.vertices[i].co for i in (0,3)]) - at_x([sur.data.vertices[i].co for i in (2,5)])
    assert isclose(measure,scene['ancho_junta_m'],abs_tol=.00001)
    sol = next(o for o in scene.objects if o.type == 'LIGHT')
    camera = next(o for o in scene.objects if o.type == 'CAMERA' and o.name.startswith('Encuentro'))
    data.append((tuple(sol.rotation_euler),tuple(camera.location),tuple(camera.rotation_euler)))
    print(scene.name, round(measure,2), 'm de apertura de referencia', dict(names))
assert all(item == data[0] for item in data)
assert 'Bordes:' in bpy.data.texts['LEEME · ensayo comparativo'].as_string()
print('12 piedras verificadas. Las tres variantes reabren con sus cantos plegados y con las juntas nominales conservadas.')
