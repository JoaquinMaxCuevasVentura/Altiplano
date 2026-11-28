from pathlib import Path
import bpy

staging = Path('/tmp/serie-blender')
views = [
    ('01', 'Recinto · encuentro bajo la chapa'),
    ('02', 'Claro · dobladillo, costilla y tensor'),
    ('03', 'Chujlla · atado, fibra y borde del corte'),
]
for prefix, camera_name in views:
    scene = next(scene for scene in bpy.data.scenes if scene.name.startswith(prefix))
    bpy.context.window.scene = scene
    scene.camera = scene.objects[camera_name]
    scene.render.resolution_x = 552
    scene.render.resolution_y = 410
    scene.render.resolution_percentage = 100
    scene.cycles.samples = 20
    scene.render.filepath = str(staging / f'encuentro_{prefix}.png')
    bpy.ops.render.render(write_still=True)
