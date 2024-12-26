from utils import abs2rel_pos, get_type_from_key
from .registry import get_processor

def process_fixture(value, key, group_pos, group_z_rot):
    """
    Process fixture based on its type
    
    Args:
        value: Fixture data dictionary
        key: Fixture identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        List of processed fixture information
    """
    fixture_type = get_type_from_key(key)
    processor = get_processor(fixture_type)
    
    if processor:
        return processor(value, key, group_pos, group_z_rot)
    
    # Default processing if no specific processor found
    return [{
        'name': key,
        'type': fixture_type,
        'pos': abs2rel_pos(
            group_pos, 
            group_z_rot, 
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }]

