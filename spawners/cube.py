import bpy


class Cube:
    """Base class for Cube objects"""
    def __init__(self,context):
        self.name="Cube"
    
    def spawn(self,context):
        print("Spawning Cube")
        try:
            bpy.ops.mesh.primitive_cube_add()
            cube_obj=context.active_object
            cube_obj.name="cube"
            cube_obj.location=(-3,-3,0)
            cube_obj.scale=(0.9,0.8,1.78)
        except Exception as e:
            print("Error Spawning floor,{}".format(e))