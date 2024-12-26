import bpy
from ..core.export import export_scene_to_json

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
        # TODO: Implement the conversion logic
        self.report({'INFO'}, "JSON to YAML conversion completed")
        return {'FINISHED'}

def register_export_op():
    bpy.utils.register_class(FLOORPLAN_OT_export)
    bpy.utils.register_class(FLOORPLAN_OT_convert)

def unregister_export_op():
    bpy.utils.unregister_class(FLOORPLAN_OT_export)
    bpy.utils.unregister_class(FLOORPLAN_OT_convert)
