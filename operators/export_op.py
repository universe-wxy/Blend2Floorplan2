import bpy
from ..core.export import export_scene_to_json
from ..core.convert import json_to_yaml

class FLOORPLAN_OT_convert(bpy.types.Operator):
    """Export scene to YAML format"""
    bl_idname = "floorplan.json_to_yaml"
    bl_label = "Export to YAML"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # 先导出JSON
            json_file = export_scene_to_json()
            
            # 转换为YAML并删除JSON
            yaml_file = json_to_yaml(json_file)
            self.report({'INFO'}, f"Scene exported to YAML: {yaml_file}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting to YAML: {str(e)}")
            return {'CANCELLED'}

def register_export_op():
    bpy.utils.register_class(FLOORPLAN_OT_convert)

def unregister_export_op():
    bpy.utils.unregister_class(FLOORPLAN_OT_convert)
