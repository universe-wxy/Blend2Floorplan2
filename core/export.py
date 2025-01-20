import bpy
from typing import Dict, Any
from ..utils.object_processor import get_object_data, get_axis_data
from ..utils.file_handler import save_scene_data

def traverse_collection(collection: bpy.types.Collection, parent_name: str = "") -> Dict[str, Any]:
    """Recursively traverse collection"""
    data = {}
    
    # Process mesh objects
    for obj in collection.objects:
        if obj.type == 'MESH':
            data[obj.name] = get_object_data(obj, parent_name)
        elif obj.name.find("axis") != -1:
            data["axis"] = get_axis_data(obj, parent_name)

    # Process child collections
    for child_collection in collection.children:
        data[child_collection.name] = {
            "type": "COLLECTION",
            "parent": parent_name,
            "children": traverse_collection(child_collection, child_collection.name)
        }
    
    return data

def export_scene_to_json() -> str:
    """Export scene data to JSON file"""
    try:
        scene_data = traverse_collection(bpy.context.scene.collection)
        output_file = save_scene_data(scene_data)
        
        bpy.context.scene['exported_json'] = output_file
        
        print(f"Scene data exported to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error during export: {str(e)}")
        raise

