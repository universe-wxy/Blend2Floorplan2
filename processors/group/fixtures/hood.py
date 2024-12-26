from utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('hood')
def process_hood(value, key, group_pos, group_z_rot):
    """
    Process hood fixture
    
    Args:
        value: Hood data dictionary
        key: Hood identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding hood information
    """
    hood_info = {
        'name': key,
        'type': 'hood',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        )
    }

    if 'size' in value:
        hood_info['size'] = [value['size'][0], value['size'][1], None]
    
    yield hood_info