"""Render saved review scene. Animation is assembly explanation, not CFD."""
import bpy
from pathlib import Path
OUT = Path(__file__).resolve().parents[2] / 'reports/shareable_20261005/visuals'
scene = [s for s in bpy.data.scenes if s.name.startswith('AQI R03M Review Presentation')][-1]
bpy.context.window.scene = scene
scene.camera.data.animation_data_clear()  # Render-specific framing; saved source is untouched.
scene.frame_set(1)
scene.render.filepath = str(OUT/'assembly.png')
bpy.ops.render.render(write_still=True)
scene.frame_set(30)
scene.camera.data.ortho_scale = 1.95
scene.render.filepath = str(OUT/'exploded.png')
bpy.ops.render.render(write_still=True)
scene.camera.data.ortho_scale = 1.30
scene.frame_set(1)
for obj in scene.objects:
    if obj.get('source_kind') in ('panel','guard'):
        obj.hide_render = True
scene.render.filepath = str(OUT/'cutaway.png')
bpy.ops.render.render(write_still=True)
for obj in scene.objects:
    if not obj.get('illustrative_not_cfd'):
        obj.hide_render = False
scene.render.resolution_x = 640
scene.render.resolution_y = 540
scene.camera.data.ortho_scale = 1.95
(OUT/'frames').mkdir(exist_ok=True)
for frame in range(1,49,2):
    scene.frame_set(frame)
    scene.render.filepath = str(OUT/'frames'/f'{frame:03}.png')
    bpy.ops.render.render(write_still=True)
scene.frame_set(1)
for obj in scene.objects:
    if obj.get('source_kind'):
        obj.animation_data_clear()
        obj.hide_render = obj.get('source_kind') in ('panel','guard')
    if obj.get('illustrative_not_cfd'):
        obj.hide_render = False
scene.camera.data.ortho_scale = 1.35
(OUT/'air_frames').mkdir(exist_ok=True)
for frame in range(1,49,2):
    scene.frame_set(frame)
    scene.render.filepath = str(OUT/'air_frames'/f'{frame:03}.png')
    bpy.ops.render.render(write_still=True)
print('AQI_RENDERS_COMPLETE')
