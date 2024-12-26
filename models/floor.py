import bpy

class Floor:
    """Base class for floor objects"""
    def __init__(self, context):
        self.name = "floor"

        self.init_collection()
        self.floors_col = bpy.data.collections.get("floors")

    def init_collection(self):
        room_col = bpy.data.collections.get("room")
        if not room_col:
            room_col = bpy.data.collections.new("room")
            bpy.context.scene.collection.children.link(room_col)
        
        floors_col = bpy.data.collections.get("floors")
        if not floors_col:
            floors_col = bpy.data.collections.new("floors")
            room_col.children.link(floors_col)

    def spawn(self, context):
        print("Spawning floor")

        try:
            bpy.ops.mesh.primitive_cube_add()
            floor_obj = context.active_object

            for col in floor_obj.users_collection:
                col.objects.unlink(floor_obj)

            floor_obj.name = "floor"
            floor_obj.location = (3, -3, 0)
            floor_obj.scale = (3, 3, 0.1)

            # TODO: Set offset

            # floor_obj.name = self.name
            self.floors_col.objects.link(floor_obj)
        except Exception as e:
            print(f"Error spawning floor: {e}")

