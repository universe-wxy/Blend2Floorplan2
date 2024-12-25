import bpy
from ..models.floor import Floor
from ..models.wall import Wall
from ..models.wall_accessory import WallAccessory

class FLOORPLAN_OT_spawn_object(bpy.types.Operator):
    """Spawn selected object type in the scene"""
    bl_idname = "floorplan.spawn_object"
    bl_label = "Spawn Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get the selected object type from the scene properties
        object_type = context.scene.room_object_type
        
        # Create and spawn the selected object
        if object_type == 'FLOOR':
            obj = Floor()
        elif object_type == 'WALL':
            obj = Wall()
        elif object_type == 'WALL_ACCESSORY':
            obj = WallAccessory()
            
        obj.spawn(context)
        return {'FINISHED'}
