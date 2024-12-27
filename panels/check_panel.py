import bpy

from ..operators.check_op import FLOORPLAN_OT_check

class FLOORPLAN_PT_check_panel(bpy.types.Panel):
    """Panel for checking the scene data"""
    bl_label = "Check"
    bl_idname = "FLOORPLAN_PT_check_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FloorPlan"

    def draw(self, context):
        layout = self.layout
        layout.operator(FLOORPLAN_OT_check.bl_idname, text="Check")

def register_check_panel():
    bpy.utils.register_class(FLOORPLAN_OT_check)
    bpy.utils.register_class(FLOORPLAN_PT_check_panel)

def unregister_check_panel():
    bpy.utils.unregister_class(FLOORPLAN_OT_check)
    bpy.utils.unregister_class(FLOORPLAN_PT_check_panel)