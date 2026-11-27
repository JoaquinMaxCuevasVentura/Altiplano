import bpy
from mathutils import Vector

scene = next(scene for scene in bpy.data.scenes if scene.name.startswith('03'))
camera = scene.objects['Chujlla · atado, fibra y borde del corte']
camera.location = (1.28, -3.35, 1.1)
camera.rotation_euler = (Vector((1.95, .73, 2.00)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.ortho_scale = 2.72
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, compress=True)
