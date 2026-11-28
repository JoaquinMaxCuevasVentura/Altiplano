import statistics
import bpy

scenes = {scene.name[0]: scene for scene in bpy.data.scenes}
assert set(scenes) == {'A','B','C','D'}
d = scenes['D']
assert bpy.context.window.scene == d
assert d.camera.name.startswith('D · Maqueta abierta')
walls = {o.name: o for o in d.objects if 'Pirca' in o.name or 'relleno de la pirca' in o.name}
assert len(walls) == 4
for obj in walls.values():
    assert obj.modifiers[0].node_group.name == 'Pirca · montaje de piedras'
north = walls['D · Pirca norte']
south = walls['D · Pirca sur']
def width_at(a,b):
    return (statistics.median(v.co.y for v in north.data.vertices if a < v.co.x < b)
            - statistics.median(v.co.y for v in south.data.vertices if a < v.co.x < b))
entry = width_at(1.4,2.2)
exit_ = width_at(5.65,6.12)
assert exit_ > entry+1.1
core = next(o for o in walls.values() if 'relleno' in o.name)
inner = next(o for o in walls.values() if 'interior' in o.name)
assert len(core.data.vertices) >= 260
assert max(v.co.x for v in core.data.vertices)-max(v.co.x for v in inner.data.vertices) > .12
mesh = next(o for o in d.objects if 'Rebaje seco' in o.name)
assert min(v.co.z for v in mesh.data.vertices) < -.13
assert not any(o.name.startswith('D · Piedra testigo') for o in d.objects)
assert {'D · Maqueta abierta','D · Hacia el relleno expuesto','D · Desde el umbral','D · Planta'} == {o.name for o in d.objects if o.type=='CAMERA'}
assert 'Altiplano' in bpy.data.texts['D · Referencias y decisiones'].as_string()
print(f'Variante D validada junto a A, B y C. Ejes de pirca: paso {entry:.2f} m, apertura {exit_:.2f} m. Relleno instanciado: {len(core.data.vertices)} piedras.')
