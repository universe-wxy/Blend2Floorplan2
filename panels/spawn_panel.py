import bpy
from ..utils.constants import BL_CATEGORY, BL_PANEL_ID
from ..operators.spawn import FLOORPLAN_OT_spawn_object

# Define the enum items for object types
object_types = [
    ('FLOOR', "Floor", "Spawn a floor object"),
    ('WALL', "Wall", "Spawn a wall object"),
    ('WALL_ACCESSORY', "Wall Accessory", "Spawn a wall accessory"),
]

# Register the enum property
def register_properties():
    bpy.types.Scene.room_object_type = bpy.props.EnumProperty(
        items=object_types,
        name="Object Type",
        description="Select object type to spawn",
        default='FLOOR'
    )

class FLOORPLAN_PT_spawn_panel(bpy.types.Panel):
    """Panel for spawning room objects"""
    bl_label = "Spawn Objects"
    bl_idname = BL_PANEL_ID
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = BL_CATEGORY
    
    def draw(self, context):
        layout = self.layout
        
        # Add the enum menu
        layout.prop(context.scene, "room_object_type")
        
        # Add the spawn button
        layout.operator("floorplan.spawn_object", text="Spawn Object")

def register_room_panel():
    register_properties()
    bpy.utils.register_class(FLOORPLAN_OT_spawn_object)
    bpy.utils.register_class(FLOORPLAN_PT_spawn_panel)

def unregister_room_panel():
    bpy.utils.unregister_class(FLOORPLAN_PT_spawn_panel)
    bpy.utils.unregister_class(FLOORPLAN_OT_spawn_object)
    del bpy.types.Scene.room_object_type