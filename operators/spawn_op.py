import bpy
from ..models.floor import Floor
from ..models.wall import Wall
from ..models.wall_accessory import WallAccessory

class FLOORPLAN_OT_spawn(bpy.types.Operator):
    """Spawn selected object type in the scene"""
    bl_idname = "floorplan.spawn"
    bl_label = "Spawn Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get the selected object type from the scene properties
        object_type = context.scene.room_object_type
        
        # Create and spawn the selected object
        if object_type == 'floor':
            obj = Floor(context)
        elif object_type == 'wall':
            obj = Wall(context)
        elif object_type == 'wall_accessory':
            obj = WallAccessory(context)

        obj.spawn(context)
        return {'FINISHED'}
    

def register_spawn_op():
    bpy.utils.register_class(FLOORPLAN_OT_spawn)

def unregister_spawn_op():
    bpy.utils.unregister_class(FLOORPLAN_OT_spawn)
