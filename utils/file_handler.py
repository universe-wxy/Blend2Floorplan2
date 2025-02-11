import bpy
import os
import json
import time
from typing import Any

def get_default_root_path() -> str:
    """Get default root path (parent directory of current file)"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

def get_output_dir() -> str:
    """Get output directory path"""
    blend_file_path = bpy.data.filepath
    if not blend_file_path:
        root_path = get_default_root_path()
        blend_file_path = os.path.join(root_path, "test_scene.blend")
        
    blend_file_dir = os.path.dirname(blend_file_path)
    blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]
    output_dir = os.path.join(blend_file_dir, blend_file_name)
    os.makedirs(output_dir, exist_ok=True)
    
    return output_dir

def get_output_path() -> str:
    """Generate scene info output file path"""
    blend_file_path = bpy.data.filepath
    if not blend_file_path:
        root_path = get_default_root_path()
        blend_file_path = os.path.join(root_path, "test_scene.blend")
    blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]
    return os.path.join(get_output_dir(), f"{blend_file_name}_{time.strftime('%Y%m%d_%H%M%S')}.json")

def save_scene_data(data: Any) -> str:
    """Save scene data to JSON file"""
    output_file = get_output_path()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # import pdb; pdb.set_trace()
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    return output_file
