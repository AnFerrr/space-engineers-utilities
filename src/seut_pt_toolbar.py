import bpy

class SEUT_PT_Panel(bpy.types.Panel):
    """Creates the topmost panel for SEUT"""
    bl_idname = "SEUT_PT_Panel"
    bl_label = "Space Engineers Utilities"
    bl_category = "SEUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Grid Scale")
        row = box.row()
        row.prop(scene.seut,'prop_gridScale', expand=True)
        
        layout.operator('object.recreate_collections', text="Recreate Collections")


class SEUT_PT_Panel_BoundingBox(bpy.types.Panel):
    """Creates the bounding box panel for SEUT"""
    bl_idname = "SEUT_PT_Panel_BoundingBox"
    bl_label = "Bounding Box"
    bl_category = "SEUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Toggle
        layout.prop(scene.seut,'prop_bBoxToggle', expand=True)

        # Size
        box = layout.box()
        box.label(text="Size")
        row = box.row()
        row.prop(scene.seut, "prop_bBox_X")
        row.prop(scene.seut, "prop_bBox_Y")
        row.prop(scene.seut, "prop_bBox_Z")
        
        row = box.row()
        row.operator('object.bbox_auto', text="Automatic")

class SEUT_PT_Panel_Export(bpy.types.Panel):
    """Creates the export panel for SEUT"""
    bl_idname = "SEUT_PT_Panel_Export"
    bl_label = "Export"
    bl_category = "SEUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Export
        row = layout.row()
        row.scale_y = 2.0
        row.operator('object.export', text="Export")
        layout.prop(scene.seut, "prop_export_deleteLooseFiles")
        
        # Partial
        box = layout.box()
        box.label(text="Partial Export")
        split = box.split()
        
        col = split.column()
        col.operator('object.export_main', text="Main")
        col.operator('object.export_lod', text="LODs")

        col = split.column()
        col.operator('object.export_buildstages', text="Build Stages")
        col.operator('object.export_hkt', text="Collision")

        # Options
        box = layout.box()
        box.label(text="Options")
        split = box.split()
        
        col = split.column()
        col.prop(scene.seut, "prop_export_fbx")
        col.prop(scene.seut, "prop_export_sbc")

        col = split.column()
        col.prop(scene.seut, "prop_export_xml")
        col.prop(scene.seut, "prop_export_hkt")
        
        box.prop(scene.seut, "prop_export_rescaleFactor")
        
        box.prop(scene.seut, "prop_export_exportPath", text="Folder", expand=True)

        # SubtypeId
        box = layout.box()
        box.label(text="SubtypeId")
        box.prop(scene.seut, "prop_subtypeId", text="", expand=True)
        
        # LOD
        box = layout.box()
        box.label(text="LOD Distance")
        box.prop(scene.seut, "prop_export_lod1Distance")
        box.prop(scene.seut, "prop_export_lod2Distance")
        box.prop(scene.seut, "prop_export_lod3Distance")


class SEUT_PT_Panel_Import(bpy.types.Panel):
    """Creates the import panel for SEUT"""
    bl_idname = "SEUT_PT_Panel_Import"
    bl_label = "Import"
    bl_category = "SEUT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # Import
        row = layout.row()
        row.scale_y = 2.0
        row.operator('scene.import', text="Import")

        # Repair
        box = layout.box()
        box.label(text="Repair")
        box.operator('object.emptytocubetype', text="Display Empties as 'Cube'")
        box.operator('object.remapmaterials', text="Remap Materials")


class SEUT_PT_Panel_Materials(bpy.types.Panel):
    """Creates the materials panel for SEUT"""
    bl_idname = "SEUT_PT_Panel_Materials"
    bl_label = "Space Engineers Utilities"
    bl_category = "SEUT"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if bpy.context.active_object.active_material != None:

            material = bpy.context.active_object.active_material

            box = layout.box()
            box.label(text=material.name, icon_value=layout.icon(material))

            for node in material.node_tree.nodes:
                if node.name == "SEUT_MAT":
                    box.label(text="Preset: " + node.node_tree.name)
                    break

            box.prop(material.seut, 'overrideMatLib')
            box.prop(material.seut, 'technique')

            if material.seut.technique == 'GLASS' or material.seut.technique == 'ALPHA_MASKED':
                boxSpec = box.box()
                boxSpec.label(text="Specularity")
                boxSpec.prop(material.seut, 'specularIntensity')
                boxSpec.prop(material.seut, 'specularPower')

                boxDiff = box.box()
                boxDiff.prop(material.seut, 'diffuseColor', text="Diffuse Color")

        box = layout.box()
        box.label(text="Create new SEUT Material")
        box.prop(scene.seut, 'prop_matPreset', text="Preset")
        box.operator('object.mat_create')