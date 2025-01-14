import bpy
import json
from typing import Dict, List, Any, Tuple

def get_wall_dimensions(obj: bpy.types.Object, wall_type: str) -> Tuple[List[float], List[float]]:
    """Process wall dimensions and position"""
    dims = obj.dimensions
    size = [0, 0, 0]
    pos = list(obj.location)
    
    if wall_type == "main" or wall_type == "front":
        size = [dims.x / 2, dims.z / 2, dims.y / 2]
        # pos[1] += -size[2] if wall_type == "main" else size[2]
    elif wall_type == "left" or wall_type == "right":
        size = [dims.y / 2, dims.z / 2, dims.x / 2]
        # pos[0] += size[2] if wall_type == "left" else -size[2]
    
    return size, pos

def get_object_data(obj: bpy.types.Object, parent_name: str) -> Dict[str, Any]:
    """Extract data from Blender object"""
    original_rotation_mode = obj.rotation_mode
    obj.rotation_mode = 'QUATERNION'
    
    try:
        obj_data = {
            "type": "MESH",
            "parent": parent_name,
            "rotation_quaternion": list(obj.rotation_quaternion)
        }

        if obj.name.startswith("wall"):
            wall_types = ["main", "front", "left", "right"]
            wall_type = next((wtype for wtype in wall_types if obj.name.startswith(f"wall_{wtype}")), None)
            if wall_type:
                size, pos = get_wall_dimensions(obj, wall_type)
            else:
                size = [d/2 for d in obj.dimensions]
                pos = list(obj.location)
        elif obj.name.startswith("floor"):
            size = [d/2 for d in obj.dimensions]
            pos = list(obj.location)
        elif obj.name.startswith("stack"):
            size = [d for d in obj.dimensions]
            pos = list(obj.location)
            levels = obj.data.get("levels", "none")
            percentages = obj.data.get("percentages", "none")
            
            if levels != "none":
                try:
                    levels = json.loads(levels)
                except:
                    import pdb; pdb.set_trace()
            if percentages != "none":
                try:
                    percentages = json.loads(percentages)
                except json.JSONDecodeError:
                    percentages = []
                
            obj_data["levels"] = levels
            obj_data["percentages"] = percentages
        elif obj.name.startswith("island"):
            size = [d for d in obj.dimensions]
            pos = list(obj.location)
            base_opening = obj.data.get("base_opening", "none")
            if base_opening != "none":
                base_opening = json.loads(base_opening)
                obj_data["base_opening"] = base_opening
        else:
            size = [d for d in obj.dimensions]
            pos = list(obj.location)

        obj_data.update({
            "size": size,
            "location": pos
        })

        return obj_data
    finally:
        obj.rotation_mode = original_rotation_mode

def get_axis_data(obj: bpy.types.Object, parent_name: str) -> Dict[str, Any]:
    """Extract axis data from Blender object"""
    original_rotation_mode = obj.rotation_mode
    obj.rotation_mode = 'QUATERNION'
    axis_data = {
        "type": "AXIS",
        "parent": parent_name,
        "rotation_quaternion": list(obj.rotation_quaternion),
        "location": list(obj.location)
    }
    return axis_data 
