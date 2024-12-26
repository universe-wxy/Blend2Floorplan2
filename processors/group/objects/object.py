from utils import abs2rel_pos, get_type_from_key

def process_object(value, key, group_pos, group_z_rot):
    object_type = get_type_from_key(key)
    
    object_info = {
        'name': key,
        'type': object_type
    }
    
    # location info
    if 'location' in value:
        abs_pos = [
            value['location'][0],
            value['location'][1],
            value['location'][2]
        ]
        object_info['pos'] = abs2rel_pos(group_pos, group_z_rot, abs_pos)
    
    yield object_info