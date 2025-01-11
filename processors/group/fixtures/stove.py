from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('stove')
def process_stove(value, key, group_pos, group_z_rot):
    """
    Process stove fixture
    
    Args:
        value: Stove data dictionary
        key: Stove identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding stove informationq
    """
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    stove_info = {
        'name': key,
        'type': 'stove',
        'pos': pos,
        'size': size
    }

    yield stove_info