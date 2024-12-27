import bpy
from .panels.spawn_panel import register_room_panel, unregister_room_panel
from .panels.export_panel import register_export_panel, unregister_export_panel
from .panels.check_panel import register_check_panel, unregister_check_panel
bl_info = {
    "name": "FloorPlan",
    "author": "Chenyu Cao",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > FloorPlan",
    "description": "Create floor plans",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
}

def register():
    register_room_panel()
    register_export_panel()
    register_check_panel()

def unregister():
    unregister_room_panel()
    unregister_export_panel()
    unregister_check_panel()
if __name__ == "__main__":
    register()
