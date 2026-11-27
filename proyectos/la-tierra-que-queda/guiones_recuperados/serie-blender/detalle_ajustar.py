from pathlib import Path
import bpy
from mathutils import Vector

scene = next(scene for scene in bpy.data.scenes if scene.name.startswith('03'))
camera = scene.objects['Chujlla · atado, fibra y borde del corte']
camera.location = (1.28, -3.35, 1.1)
target = Vector((1.95, .73, 2.00))
camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.ortho_scale = 2.72
bpy.context.window.scene = scene
scene.camera = camera
scene.cycles.use_denoising = True
scene.cycles.samples = 24
scene.render.resolution_x = 560
scene.render.resolution_y = 420
scene.render.resolution_percentage = 100
scene.view_settings.exposure += .35
scene.render.filepath = '/tmp/serie-blender/encuentro_03_ajustado.png'
bpy.ops.render.render(write_still=True)
