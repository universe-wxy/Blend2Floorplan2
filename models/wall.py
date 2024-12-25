import bpy

class Wall:
    """Base class for wall objects"""
    def __init__(self, context=None):
        if context:
            self.name = context.scene.wall_name
            self.side = context.scene.wall_side
        else:
            self.name = "wall"
            self.side = "none"

        self.init_collection()
        self.walls_col = bpy.data.collections.get("walls")

    def init_collection(self):
        room_col = bpy.data.collections.get("room")
        if not room_col:
            room_col = bpy.data.collections.new("room")
            bpy.context.scene.collection.children.link(room_col)

        walls_col = bpy.data.collections.get("walls")
        if not walls_col:
            walls_col = bpy.data.collections.new("walls")
            room_col.children.link(walls_col)
        
    def spawn(self, context):
        print(f"Spawning wall with name: {self.name} and side: {self.side}")

        if self.side == "none":
            bpy.ops.mesh.primitive_cube_add()
            wall_obj = context.active_object
            
            wall_obj.location = (1.5, 0, 1.5)
            wall_obj.scale = (1.5, 0.06, 1.5)
            wall_obj.name = self.name
            
            self.walls_col.objects.link(wall_obj)
