import bpy
import os

from math           import pi
from bpy.types      import Operator

from .seut_collections              import get_collections
from .seut_errors                   import check_collection, check_collection_excluded, seut_report, get_abs_path
from .seut_utils                    import get_parent_collection, to_radians, create_seut_collection, clear_selection, prep_context, seut_report
    

def setup_icon_render(self, context):
    """Sets up render utilities"""

    scene = context.scene
    collections = get_collections(scene)
    current_area = prep_context(context)

    result = check_collection(self, context, scene, collections['seut'], False)
    if not result == {'CONTINUE'}:
        scene.seut.mirroringToggle = 'off'
        return

    if not bpy.data.is_saved:
        seut_report(self, context, 'ERROR', False, 'E008')
        scene.seut.renderToggle = 'off'
        return {'CANCELLED'}
        
    tag = ' (' + scene.seut.subtypeId + ')'

    collection = create_seut_collection(collections['seut'], 'Render' + tag)
    
    if scene.render.filepath == '/tmp\\':
        scene.render.filepath = '//'

    # Spawn holder empty
    bpy.ops.object.add(type='EMPTY', location=scene.seut.renderEmptyLocation, rotation=scene.seut.renderEmptyRotation)
    empty = bpy.context.view_layer.objects.active
    empty.scale.x = scene.seut.renderDistance
    empty.scale.y = scene.seut.renderDistance
    empty.scale.z = scene.seut.renderDistance
    empty.name = 'Icon Render'
    empty.empty_display_type = 'SPHERE'
    
    # Spawn camera
    bpy.ops.object.camera_add(location=(0.0, -15, 0.0), rotation=(to_radians(90), 0.0, 0.0))
    camera = bpy.context.view_layer.objects.active
    camera.parent = empty
    scene.camera = camera
    camera.name = 'ICON'
    camera.data.name = 'ICON'
    camera.data.lens = scene.seut.renderZoom

    # Spawn lights
    bpy.ops.object.light_add(type='POINT', location=(-12.5, -12.5, 5.0), rotation=(0.0, 0.0, 0.0))
    keyLight = bpy.context.view_layer.objects.active
    keyLight.parent = empty
    keyLight.name = 'Key Light'
    keyLight.data.energy = 7500.0 * scene.seut.renderDistance
    
    bpy.ops.object.light_add(type='POINT', location=(10.0, -10.0, -2.5), rotation=(0.0, 0.0, 0.0))
    fillLight = bpy.context.view_layer.objects.active
    fillLight.parent = empty
    fillLight.name = 'Fill Light'
    fillLight.data.energy = 5000.0 * scene.seut.renderDistance
    
    bpy.ops.object.light_add(type='SPOT', location=(0.0, 15.0, 0.0), rotation=(to_radians(-90), 0.0, 0.0))
    rimLight = bpy.context.view_layer.objects.active
    rimLight.parent = empty
    rimLight.name = 'Rim Light'
    rimLight.data.energy = 10000.0 * scene.seut.renderDistance
    
    parentCollection = get_parent_collection(context, empty)
    if parentCollection != collection:
        collection.objects.link(empty)
        collection.objects.link(camera)
        collection.objects.link(keyLight)
        collection.objects.link(fillLight)
        collection.objects.link(rimLight)

        if parentCollection is None:
            scene.collection.objects.unlink(empty)
            scene.collection.objects.unlink(camera)
            scene.collection.objects.unlink(keyLight)
            scene.collection.objects.unlink(fillLight)
            scene.collection.objects.unlink(rimLight)
        else:
            parentCollection.objects.unlink(empty)
            parentCollection.objects.unlink(camera)
            parentCollection.objects.unlink(keyLight)
            parentCollection.objects.unlink(fillLight)
            parentCollection.objects.unlink(rimLight)

    # Spawn compositor node tree
    scene.use_nodes = True
    tree = scene.node_tree
    tree.nodes.clear()

    node_render_layers = tree.nodes.new(type='CompositorNodeRLayers')
    node_color_correction = tree.nodes.new(type='CompositorNodeColorCorrection')
    node_rgb = tree.nodes.new(type='CompositorNodeRGB')
    node_mix_rgb = tree.nodes.new(type='CompositorNodeMixRGB')
    node_bright_contrast = tree.nodes.new(type='CompositorNodeBrightContrast')
    node_viewer = tree.nodes.new(type='CompositorNodeViewer')

    tree.links.new(node_render_layers.outputs[0], node_color_correction.inputs[0])
    tree.links.new(node_color_correction.outputs[0], node_mix_rgb.inputs[1])
    tree.links.new(node_rgb.outputs[0], node_mix_rgb.inputs[2])
    tree.links.new(node_mix_rgb.outputs[0], node_bright_contrast.inputs[0])
    tree.links.new(node_bright_contrast.outputs[0], node_viewer.inputs[0])

    node_color_correction.midtones_gain = 2.0
    node_color_correction.shadows_gain = 2.5

    node_rgb.outputs[0].default_value = (0.23074, 0.401978, 0.514918, 1)  # 84AABE
    
    node_mix_rgb.blend_type = 'COLOR'

    node_bright_contrast.inputs[1].default_value = 0.35
    node_bright_contrast.inputs[2].default_value = 0.35

    # Force update render resolution
    scene.seut.renderResolution = scene.seut.renderResolution
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.film_transparent = True

    clear_selection(context)
    context.area.type = current_area


def clean_icon_render(self, context):
    """Clean up render utilities"""

    scene = context.scene
    current_area = prep_context(context)

    tag = ' (' + scene.seut.subtypeId + ')'

    # Delete objects
    for obj in scene.objects:
        if obj is not None and obj.type == 'EMPTY':
            if obj.name == 'Icon Render':
                for child in obj.children:
                    if child.data is not None:
                        if child.type == 'CAMERA':
                            bpy.data.cameras.remove(child.data)
                        elif child.type == 'LIGHT':
                            bpy.data.lights.remove(child.data)

                clear_selection(context)
                bpy.data.objects.remove(obj)

    # Delete collection
    if 'Render' + tag in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections['Render' + tag])

    # Delete Node Tree
    try:
        scene.node_tree.nodes.clear()
    except AttributeError:
        pass

    context.area.type = current_area


class SEUT_OT_IconRenderPreview(Operator):
    """Shows a render preview window"""
    bl_idname = "scene.icon_render_preview"
    bl_label = "Render"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.scene.seut.renderToggle == 'on'


    def execute(self, context):

        scene = context.scene
        wm = context.window_manager

        if not os.path.isdir(get_abs_path(scene.render.filepath)):
            seut_report(self, context, 'ERROR', False, 'E003', 'Render', get_abs_path(scene.render.filepath))
            return {'CANCELLED'}
            
        tag = ' (' + scene.seut.subtypeId + ')'

        clear_selection(context)

        simple_nav = wm.seut.simpleNavigationToggle
        wm.seut.simpleNavigationToggle = False

        collections = get_collections(scene)

        for col in collections.values():
            if col is not None:
                if col.name == 'Main' + tag:
                    for obj in col.objects:
                        obj.hide_render = False
                        obj.hide_viewport = False
                else:
                    for obj in col.objects:
                        obj.hide_render = True
                        obj.hide_viewport = True

        # This path juggling is to prevent Blender from saving the default render output
        path = scene.render.filepath
        scene.render.filepath = scene.render.filepath + "//" + scene.seut.subtypeId

        bpy.ops.render.render()
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        image = area.spaces.active.image
        area.spaces.active.image = bpy.data.images['Viewer Node']

        scene.render.filepath = path
        
        for col in collections.values():
            if col is not None:
                for obj in col.objects:
                    obj.hide_render = False
                    obj.hide_viewport = False

        wm.seut.simpleNavigationToggle = simple_nav

        seut_report(self, context, 'INFO', True, 'I018', scene.render.filepath + "\\" + scene.seut.subtypeId + '.' + scene.render.image_settings.file_format.lower())

        return {'FINISHED'}