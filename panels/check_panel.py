import bpy
import os
from bpy.props import StringProperty, CollectionProperty
from ..operators.check_op import FLOORPLAN_OT_check, FLOORPLAN_OT_demo, get_latest_yaml

def get_yaml_files(self, context):
    """获取yaml文件列表"""
    items = []
    if not bpy.data.is_saved:
        return items

    blend_dir = os.path.dirname(bpy.data.filepath)
    blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    yaml_dir = os.path.join(blend_dir, blend_name)

    if os.path.exists(yaml_dir):
        yaml_files = [f for f in os.listdir(yaml_dir) 
                     if f.endswith(('.yaml', '.yml'))]
        yaml_files.sort(key=lambda x: os.path.getmtime(os.path.join(yaml_dir, x)), reverse=True)
        items = [(f, f, os.path.join(yaml_dir, f)) for f in yaml_files]
    
    return items

def get_full_yaml_path(filename):
    """获取YAML文件的完整路径"""
    if not filename or not bpy.data.is_saved:
        return None
    
    blend_dir = os.path.dirname(bpy.data.filepath)
    blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
    yaml_dir = os.path.join(blend_dir, blend_name)
    
    return os.path.join(yaml_dir, filename)

class FLOORPLAN_PT_check_panel(bpy.types.Panel):
    """Panel for checking the scene data"""
    bl_label = "检查"
    bl_idname = "FLOORPLAN_PT_check_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FloorPlan"
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        
        # YAML文件选择
        col = layout.column(align=True)
        col.prop(context.scene, "yaml_file_path", text="YAML文件")
        
        # Style ID输入框
        col.prop(context.scene, "check_style_id", text="Style ID")
        
        # Check和Demo按钮
        col = layout.column(align=True)
        col.operator(FLOORPLAN_OT_check.bl_idname, text="检查")
        col.operator(FLOORPLAN_OT_demo.bl_idname, text="预览")

def register_check_panel():
    # 注册属性
    bpy.types.Scene.yaml_file_path = bpy.props.EnumProperty(
        name="YAML文件",
        description="选择要使用的YAML文件",
        items=get_yaml_files,
        update=None
    )
    
    bpy.types.Scene.check_style_id = bpy.props.IntProperty(
        name="Style ID",
        description="Style ID for layout generation",
        default=6,
        min=0,
        max=10
    )
    
    # 设置默认yaml文件
    @bpy.app.handlers.persistent
    def set_default_yaml(dummy):
        if bpy.data.is_saved:
            latest_yaml = get_latest_yaml(bpy.data.filepath)
            if latest_yaml:
                # 只使用文件名，而不是完整路径
                filename = os.path.basename(latest_yaml)
                for scene in bpy.data.scenes:
                    scene.yaml_file_path = filename
    
    # 注册handler
    if set_default_yaml not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(set_default_yaml)
    
    # 注册类
    bpy.utils.register_class(FLOORPLAN_OT_check)
    bpy.utils.register_class(FLOORPLAN_OT_demo)
    bpy.utils.register_class(FLOORPLAN_PT_check_panel)

def unregister_check_panel():
    # 注销类
    bpy.utils.unregister_class(FLOORPLAN_PT_check_panel)
    bpy.utils.unregister_class(FLOORPLAN_OT_demo)
    bpy.utils.unregister_class(FLOORPLAN_OT_check)
    
    # 删除属性
    if hasattr(bpy.types.Scene, "yaml_file_path"):
        del bpy.types.Scene.yaml_file_path
    if hasattr(bpy.types.Scene, "check_style_id"):
        del bpy.types.Scene.check_style_id

if __name__ == "__main__":
    register_check_panel()
