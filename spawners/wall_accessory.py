import bpy

class WallAccessory:
    """Base class for wall accessories like windows and doors"""
    def __init__(self,context):
        self.name = "wallaccessory"
        if not context:
            self.type="wallaccessory"
        else:
            self.type=context.scene.accessory_type
            
    def spawn(self, context):
        print("Spawning accessory")
        try:
            bpy.ops.mesh.primitive_cube_add()
            accessory_obj=context.active_object
            accessory_obj.name=self.type
            accessory_obj.location=(-3,-3,0)
            accessory_obj.scale=(1,1,1)
            accessory_obj.dimensions = (0.116, 0.116, 0.116)
            bpy.ops.object.transform_apply(scale=True)
        
        except Exception as e:
            print("Error Spawning floor,{}".format(e))
