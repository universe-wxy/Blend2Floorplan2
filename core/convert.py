import json
import os
from pathlib import Path
from ..processors import process_room_data, process_group_data
from ..utils import custom_format

def json_to_yaml(json_file: str) -> str:
    try:
        yaml_file = str(Path(json_file).with_suffix('.yaml'))

        with open(json_file, 'r') as f:
            scene_data = json.load(f)

        yaml_data = {}

        for key, value in scene_data.items():
            if key == 'room':
                yaml_data[key] = process_room_data(value)
            elif '_group' in key:
                yaml_data[key] = process_group_data(value)
            else:
                pass
        
        with open(yaml_file, 'w') as f:
            formatted_lines = custom_format(yaml_data)
            f.write('\n'.join(formatted_lines))

        # 删除JSON文件
        os.remove(json_file)

        return yaml_file
        
    except Exception as e:
        print(f"Error converting JSON to YAML: {str(e)}")
        raise
