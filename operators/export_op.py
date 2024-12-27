import bpy
from ..core.export import export_scene_to_json
from ..core.convert import json_to_yaml

class FLOORPLAN_OT_export(bpy.types.Operator):
    """Export the scene to a JSON file"""
    bl_idname = "floorplan.export_to_json"
    bl_label = "Export Scene to JSON"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        file_path = export_scene_to_json()
        self.report({'INFO'}, f"Scene data exported to {file_path}")
        return {'FINISHED'}

class FLOORPLAN_OT_convert(bpy.types.Operator):
    """Convert JSON file to YAML format"""
    bl_idname = "floorplan.json_to_yaml"
    bl_label = "Convert JSON to YAML"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            json_file = context.scene.get('exported_json')
            if not json_file:
                self.report({'ERROR'}, "Please export to JSON first")
                return {'CANCELLED'}
                
            yaml_file = json_to_yaml(json_file)
            self.report({'INFO'}, f"JSON converted to YAML: {yaml_file}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Error converting file: {str(e)}")
            return {'CANCELLED'}

def register_export_op():
    bpy.utils.register_class(FLOORPLAN_OT_export)
    bpy.utils.register_class(FLOORPLAN_OT_convert)

def unregister_export_op():
    bpy.utils.unregister_class(FLOORPLAN_OT_export)
    bpy.utils.unregister_class(FLOORPLAN_OT_convert)
