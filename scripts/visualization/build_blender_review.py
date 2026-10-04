"""Import actual R03M CAD tessellation; presentation only, never a CFD solver.
Run inside Blender. Preserves pre-existing scenes, saves a dedicated file.
"""
import bpy
import hashlib
import json
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/shareable_20261005/visuals'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'reports/prototype_d01/mechanical_package/cad_mesh.json'
parts = json.loads(SOURCE.read_text())
scene = bpy.data.scenes.new('AQI R03M Review Presentation')
bpy.context.window.scene = scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1100
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
formats = [e.identifier for e in scene.render.image_settings.bl_rna.properties['file_format'].enum_items]
assert 'PNG' in formats
scene.render.image_settings.file_format = 'PNG'
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 48
scene.world = bpy.data.worlds.new('AQI studio world')
scene.world.color = (.18, .18, .18)
palette = {'panel':(.11,.32,.36,1), 'support':(.20,.25,.29,1),
           'filter':(.88,.48,.12,1), 'fan':(.025,.06,.08,1),
           'guard':(.12,.55,.53,1), 'seal':(.22,.12,.05,1),
           'hardware':(.38,.45,.49,1), 'reservation':(.60,.26,.53,1)}
materials = {}
for kind, color in palette.items():
    mat = bpy.data.materials.new('AQI '+kind)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = .42
    bsdf.inputs['Metallic'].default_value = .3 if kind in ('hardware','guard') else .05
    materials[kind] = mat

cad = bpy.data.collections.new('Actual R03M CAD geometry')
scene.collection.children.link(cad)
for part in parts:
    mesh = bpy.data.meshes.new(part['name'])
    mesh.from_pydata([((v[0]-265)/1000,(v[1]-170)/1000,v[2]/1000) for v in part['vertices']], [], part['triangles'])
    mesh.update()
    obj = bpy.data.objects.new(part['name'],mesh)
    cad.objects.link(obj)
    obj.data.materials.append(materials[part['kind']])
    obj['source_kind'] = part['kind']
    obj['source_note'] = part.get('note','')
    obj['presentation_only'] = True
    obj.location = (0,0,0)
    obj.keyframe_insert(data_path='location',frame=1)
    obj.keyframe_insert(data_path='location',frame=12)
    obj.location = Vector(part['explode']) / 1000 * 1.6
    obj.keyframe_insert(data_path='location',frame=30)
    obj.keyframe_insert(data_path='location',frame=36)
    obj.location = (0,0,0)
    obj.keyframe_insert(data_path='location',frame=48)

def aim(obj, point):
    obj.rotation_euler = (Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()

camera_data = bpy.data.cameras.new('AQI Presentation Camera')
camera = bpy.data.objects.new('AQI Presentation Camera',camera_data)
scene.collection.objects.link(camera)
camera.location = (1.25,-1.55,1.20)
aim(camera,(.025,0,.31))
camera_data.type = 'ORTHO'
camera_data.ortho_scale = 1.30
for frame,scale in [(1,1.30),(12,1.30),(30,1.95),(36,1.95),(48,1.30)]:
    camera_data.ortho_scale = scale
    camera_data.keyframe_insert(data_path='ortho_scale',frame=frame)
scene.camera = camera
for name, loc, power, size in [('Key',(1,-2,3),600,3),('Fill',(-2,-.5,1.6),400,2),('Rim',(0,2,2.5),700,2)]:
    data = bpy.data.lights.new('AQI '+name,'AREA')
    data.energy = power
    data.shape = next(e.identifier for e in data.bl_rna.properties['shape'].enum_items if e.identifier == 'DISK')
    data.size = size
    obj = bpy.data.objects.new('AQI '+name,data)
    scene.collection.objects.link(obj)
    obj.location = loc
    aim(obj,(0,0,.3))

ground_mesh = bpy.data.meshes.new('AQI studio floor')
ground_mesh.from_pydata([(-200,-200,-.005),(200,-200,-.005),(200,200,-.005),(-200,200,-.005)],[],[(0,1,2,3)])
ground = bpy.data.objects.new('AQI studio floor',ground_mesh)
scene.collection.objects.link(ground)
floor_mat = bpy.data.materials.new('AQI warm white floor')
floor_mat.use_nodes = True
node = next(n for n in floor_mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
node.inputs['Base Color'].default_value = (.78,.83,.83,1)
node.inputs['Roughness'].default_value = .85
ground.data.materials.append(floor_mat)

scene['evidence_boundary'] = 'CAD-derived animation. No physical prototype, CFD velocity field, measured efficiency or build release.'
scene['source_sha256'] = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
air = bpy.data.collections.new('Illustrative airflow markers NOT CFD')
scene.collection.children.link(air)
for side in (-1,1):
    for lane in range(4):
        for phase in range(4):
            mesh = bpy.data.meshes.new('Air marker mesh')
            r = .006
            mesh.from_pydata([(r,0,0),(-r,0,0),(0,r,0),(0,-r,0),(0,0,r),(0,0,-r)],[],
                             [(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)])
            obj = bpy.data.objects.new(f'Illustrative_air_{side}_{lane}_{phase}',mesh)
            air.objects.link(obj)
            obj.data.materials.append(materials['guard'])
            obj['illustrative_not_cfd'] = True
            for frame in range(1,49):
                t = ((frame-1)/48+phase/4)%1
                x = -.16+lane*.105
                if t < .5:
                    obj.location = (x,side*(.48-.48*t/.5),.28+.08*t/.5)
                else:
                    obj.location = (x,0,.36+.43*(t-.5)/.5)
                obj.keyframe_insert(data_path='location',frame=frame)
            obj.hide_render = True
scene.frame_set(1)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.region_3d.view_distance = 1.8
        area.spaces.active.region_3d.view_location = (0,0,.3)
        area.spaces.active.region_3d.view_rotation = camera.rotation_euler.to_quaternion()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'AQI_R03M_REVIEW.blend'))
print(json.dumps({'scene':scene.name,'cad_objects':len(parts),'blend':str(OUT/'AQI_R03M_REVIEW.blend'),'source_sha256':scene['source_sha256']}))
