# TODO: define a check operator to check whether the scene data is valid
import bpy

class FLOORPLAN_OT_check(bpy.types.Operator):
    """Check the scene data"""
    bl_idname = "floorplan.check"
    bl_label = "Check"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        return {'FINISHED'}
