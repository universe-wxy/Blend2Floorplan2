import bpy
from math import pi
import mathutils

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

        try:
            bpy.ops.mesh.primitive_cube_add()
            wall_obj = context.active_object

            for col in wall_obj.users_collection:
                col.objects.unlink(wall_obj)


            if self.side == "main":
                wall_obj.rotation_euler[0] = pi / 2
                wall_obj.name = "wall_main"
            elif self.side == "left":
                wall_obj.rotation_euler[0] = pi / 2
                wall_obj.rotation_euler[2] = pi / 2
                wall_obj.name = "wall_left"
            elif self.side == "right":
                wall_obj.rotation_euler[0] = pi / 2
                wall_obj.rotation_euler[2] = -pi / 2
                wall_obj.name = "wall_right"
            elif self.side == "front":
                wall_obj.rotation_euler[0] = pi / 2
                wall_obj.rotation_euler[2] = pi
                wall_obj.name = "wall_front"

            wall_obj.location = (1.5, -1.5, 1.5)
            wall_obj.scale = (1.5, 1.5, 0.06)

            # TODO: Set offset

            # wall_obj.name = self.name
            self.walls_col.objects.link(wall_obj)

        except Exception as e:
            print(f"Error spawning wall: {e}")
