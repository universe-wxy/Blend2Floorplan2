from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('oven')
def process_oven(value, key, group_pos, group_z_rot):
    """
    Process oven fixture
    
    Args:
        value: Oven data dictionary
        key: Oven identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding oven and housing cabinet information
    """
    oven_info = {
        'name': key,
        'type': 'oven',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }
    
    housing_info = {
        'name': f"{key}_housing",
        'type': 'housing_cabinet',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }

    yield oven_info
    yield housing_info