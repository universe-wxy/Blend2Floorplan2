import bpy
from ..operators.check_op import FLOORPLAN_OT_check, FLOORPLAN_OT_demo

class FLOORPLAN_PT_check_panel(bpy.types.Panel):
    """Creates a Panel for check operations"""
    bl_label = "Check"
    bl_idname = "FLOORPLAN_PT_check_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FloorPlan"
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        
        # 添加style_id输入框
        col = layout.column(align=True)
        col.prop(context.scene, "check_style_id", text="Style ID")
        
        # Check和Demo按钮
        col = layout.column(align=True)
        col.operator(FLOORPLAN_OT_check.bl_idname, text="Check")
        col.operator(FLOORPLAN_OT_demo.bl_idname, text="Demo")

def register_check_panel():
    # 先注册操作符
    bpy.utils.register_class(FLOORPLAN_OT_check)
    bpy.utils.register_class(FLOORPLAN_OT_demo)
    
    # 然后注册属性
    bpy.types.Scene.check_style_id = bpy.props.IntProperty(
        name="Style ID",
        description="Style ID for layout generation",
        default=6,
        min=0,
        max=10
    )
    
    # 最后注册面板
    bpy.utils.register_class(FLOORPLAN_PT_check_panel)

def unregister_check_panel():
    # 先注销面板
    bpy.utils.unregister_class(FLOORPLAN_PT_check_panel)
    
    # 然后注销操作符
    bpy.utils.unregister_class(FLOORPLAN_OT_demo)
    bpy.utils.unregister_class(FLOORPLAN_OT_check)
    
    # 最后删除属性
    if hasattr(bpy.types.Scene, "check_style_id"):
        del bpy.types.Scene.check_style_id

if __name__ == "__main__":
    register_check_panel()
