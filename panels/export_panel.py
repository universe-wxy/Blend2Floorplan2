import bpy
from ..operators.export_op import FLOORPLAN_OT_convert

class FLOORPLAN_PT_export_panel(bpy.types.Panel):
    """
    Panel for exporting the floorplan scene info
    """
    bl_label = "Export"
    bl_idname = "FLOORPLAN_PT_export_panel"
    bl_category = "FloorPlan"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(FLOORPLAN_OT_convert.bl_idname, text="Export to Yaml")

def register_export_panel():
    bpy.utils.register_class(FLOORPLAN_OT_convert)
    bpy.utils.register_class(FLOORPLAN_PT_export_panel)

def unregister_export_panel():
    bpy.utils.unregister_class(FLOORPLAN_OT_convert)
    bpy.utils.unregister_class(FLOORPLAN_PT_export_panel)
