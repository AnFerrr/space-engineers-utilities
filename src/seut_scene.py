import bpy

from bpy.types  import PropertyGroup
from bpy.props  import (EnumProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        IntProperty,
                        StringProperty,
                        BoolProperty)

def update_GridScale(self, context):
    bpy.ops.object.gridscale()
    bpy.ops.object.bbox('INVOKE_DEFAULT')

def update_BBox(self, context):
    bpy.ops.object.bbox('INVOKE_DEFAULT')

def update_SceneName(self, context):
    context.scene.name = context.scene.seut.prop_subtypeId

class SEUT_Scene(PropertyGroup):
    """Holder for the various scene properties"""

    # Grid Scale
    prop_gridScale: EnumProperty(
        name='Scale',
        items=(
            ('large', 'Large', 'Large grid blocks (2.5m)'),
            ('small', 'Small', 'Small grid blocks (0.5m)')
            ),
        default='large',
        update=update_GridScale
    )

    # Bounding Box
    prop_bBoxToggle: EnumProperty(
        name='Bounding Box',
        items=(
            ('on', 'On', ''),
            ('off', 'Off', '')
            ),
        default='off',
        update=update_BBox
    )
    prop_bBox_X: IntProperty(
        name="X:",
        description="",
        default=1,
        min=1
    )
    prop_bBox_Y: IntProperty(
        name="Y:",
        description="",
        default=1,
        min=1
    )
    prop_bBox_Z: IntProperty(
        name="Z:",
        description="",
        default=1,
        min=1
    )

    # Export
    prop_subtypeId: StringProperty(
        name="SubtypeId",
        description="The SubtypeId for this model",
        update=update_SceneName
    )
    prop_export_deleteLooseFiles: BoolProperty(
        name="Delete Loose Files",
        description="Whether the intermediary files should be deleted after the MWM has been created",
        default=True
    )
    prop_export_fbx: BoolProperty(
        name="FBX",
        description="Whether to export to FBX",
        default=True
    )
    prop_export_xml: BoolProperty(
        name="XML",
        description="Whether to export to XML",
        default=True
    )
    prop_export_hkt: BoolProperty(
        name="HKT",
        description="Whether to export to HKT (Collision model filetype)",
        default=True
    )
    prop_export_sbc: BoolProperty(
        name="SBC",
        description="Whether to export to SBC (CubeBlocks definition)",
        default=True
    )
    prop_export_rescaleFactor: FloatProperty(
        name="Rescale Factor:",
        description="What to set the Rescale Factor to",
        default=1,
        min=0
    )
    prop_export_exportPath: StringProperty(
        name="Export Folder",
        description="What folder to export to",
        subtype="DIR_PATH"
    )
    prop_export_lod1Distance: IntProperty(
        name="LOD1:",
        description="From what distance this LOD should display",
        default=25,
        min=0
    )
    prop_export_lod2Distance: IntProperty(
        name="LOD2:",
        description="From what distance this LOD should display",
        default=50,
        min=0
    )
    prop_export_lod3Distance: IntProperty(
        name="LOD3:",
        description="From what distance this LOD should display",
        default=150,
        min=0
    )
    
    # Materials
    prop_matPreset: EnumProperty(
        name='SEUT Material Preset',
        description="Select a nodetree preset for your material",
        items=(
            ('SMAT_Preset_Full', 'Full', '[X] Alpha\n[X] Emissive\n[X] ADD\n[X] NG'),
            ('SMAT_Preset_Full_NoEmissive', 'No Emissive', '[X] Alpha\n[_] Emissive\n[X] ADD\n[X] NG'),
            ('SMAT_Preset_Full_NoADD', 'Full, No ADD', '[X] Alpha\n[_] Emissive\n[_] ADD\n[X] NG'),
            ('SMAT_Preset_NoAlpha', 'No Alpha', '[_] Alpha\n[X] Emissive\n[X] ADD\n[X] NG'),
            ('SMAT_Preset_NoAlpha_NoEmissive', 'No Alpha, No Emissive', '[_] Alpha\n[_] Emissive\n[X] ADD\n[X] NG'),
            ('SMAT_Preset_NoADD', 'No ADD', '[_] Alpha\n[_] Emissive\n[_] ADD\n[X] NG')
            ),
        default='SMAT_Preset_Full'
    )