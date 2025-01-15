import bpy

from ..operators.check_op import FLOORPLAN_OT_check, FLOORPLAN_OT_demo

class FLOORPLAN_PT_check_panel(bpy.types.Panel):
    """Panel for checking the scene data"""
    bl_label = "检查"
    bl_idname = "FLOORPLAN_PT_check_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FloorPlan"

    def draw(self, context):
        layout = self.layout
        
        # 只添加检查和预览按钮
        check_op = layout.operator("floorplan.check", text="检查台面高度")
        layout.operator("floorplan.demo", text="3D预览")

def register_check_panel():
    bpy.utils.register_class(FLOORPLAN_OT_check)
    bpy.utils.register_class(FLOORPLAN_OT_demo)
    bpy.utils.register_class(FLOORPLAN_PT_check_panel)

def unregister_check_panel():
    bpy.utils.unregister_class(FLOORPLAN_OT_check)
    bpy.utils.unregister_class(FLOORPLAN_OT_demo)
    bpy.utils.unregister_class(FLOORPLAN_PT_check_panel)
