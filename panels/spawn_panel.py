import bpy
from ..utils.constants import BL_CATEGORY, BL_PANEL_ID
from ..operators.spawn import FLOORPLAN_OT_spawn

# Define the enum items for object types
object_types = [
    ('floor', "Floor", "Spawn a floor object"),
    ('wall', "Wall", "Spawn a wall object"),
    ('wall_accessory', "Wall Accessory", "Spawn a wall accessory"),
]

# Define wall side options
wall_sides = [
    ('none', "none", "No specific side"),
    ('left', "left", "Left wall"),
    ('right', "right", "Right wall"),
    ('main', "main", "Main wall"),
]

# Register the enum property
def register_properties():
    bpy.types.Scene.room_object_type = bpy.props.EnumProperty(
        items=object_types,
        name="Object Type",
        description="Select object type to spawn",
        default='floor'
    )
    
    # Add wall_side property
    bpy.types.Scene.wall_side = bpy.props.EnumProperty(
        items=wall_sides,
        name="Wall Side",
        description="Select wall side",
        default='none'
    )

    bpy.types.Scene.wall_name = bpy.props.StringProperty(
        name="Wall Name",
        description="Name of the wall",
        default="wall"
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
        
        # Show wall side options only when Wall is selected
        if context.scene.room_object_type == 'wall':
            layout.prop(context.scene, "wall_side")
            layout.prop(context.scene, "wall_name")

        # Add the spawn button
        layout.operator("floorplan.spawn", text="spawn")

def register_room_panel():
    register_properties()
    bpy.utils.register_class(FLOORPLAN_OT_spawn)
    bpy.utils.register_class(FLOORPLAN_PT_spawn_panel)

def unregister_room_panel():
    bpy.utils.unregister_class(FLOORPLAN_PT_spawn_panel)
    bpy.utils.unregister_class(FLOORPLAN_OT_spawn)
    del bpy.types.Scene.room_object_type
    del bpy.types.Scene.wall_name
    del bpy.types.Scene.wall_side