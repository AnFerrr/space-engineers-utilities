import bpy

from bpy.types      import Operator

from ..seut_errors                  import errorExportGeneral


class SEUT_OT_ExportAllScenes(Operator):
    """Exports all collections in all scenes and compresses them to MWM"""
    bl_idname = "scene.export_all_scenes"
    bl_label = "Export All Scenes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # If mode is not object mode, export fails horribly.
        currentArea = context.area.type
        context.area.type = 'VIEW_3D'
        if bpy.context.object is not None and bpy.context.object.mode is not 'OBJECT':
            bpy.context.object.hide_set(False)
            currentMode = bpy.context.object.mode
            bpy.ops.object.mode_set(mode='OBJECT')

        # Checks export path and whether SubtypeId exists
        result = errorExportGeneral(self, context)
        if not result == {'CONTINUE'}:
            return result

        originalScene = context.window.scene

        sceneCounter = 0
        notExportedCounter = 0
        for scn in bpy.data.scenes:
            sceneCounter += 1
            context.window.scene = scn
            print("SEUT Info: Exporting scene '" + scn.name + "'.")
            try:
                bpy.ops.scene.export()
            except RuntimeError:
                notExportedCounter += 1
                print("SEUT Info: Scene '" + scn.name + "' could not be exported.")

        context.window.scene = originalScene

        # Reset interaction mode
        try:
            if bpy.context.object is not None and currentMode is not None:
                bpy.ops.object.mode_set(mode=currentMode)
        except:
            pass

        context.area.type = currentArea
        
        self.report({'INFO'}, "SEUT: %i of %i scenes successfully exported. Refer to Blender System Console for details." % (sceneCounter - notExportedCounter, sceneCounter))

        return {'FINISHED'}