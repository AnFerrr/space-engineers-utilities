import bpy

from bpy.types  import Operator
from bpy.props  import (EnumProperty,
                        IntProperty)

from ..seut_errors  import report_error

class SEUT_OT_MatCreate(Operator):
    """Create a SEUT material from the defined preset"""
    bl_idname = "object.mat_create"
    bl_label = "Create Material"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return context.active_object is not None


    def execute(self, context):
        
        wm = context.window_manager
        scene = context.scene

        presetName = wm.seut.matPreset
        
        # Find SMAT to pull preset from.
        presetMat = None

        for mat in bpy.data.materials:
            if mat.name == presetName:
                presetMat = mat
        
        if presetMat is None:
            report_error(self, context, True, 'E016', presetName)
            return {'CANCELLED'}
            
        newMat = presetMat.copy()
        newMat.name = "SEUT Material"

        context.active_object.active_material = newMat
        activeMat = context.active_object.active_material

        if activeMat.node_tree is None:
            report_error(self, context, True, 'E016', presetName)
            return {'CANCELLED'}
            
        else:
            activeMat.node_tree.make_local()
        
            for node in activeMat.node_tree.nodes:
                if node is not None and node.name == "SEUT_MAT" and node.node_tree is not None:
                    node.node_tree.make_local()

        return {'FINISHED'}