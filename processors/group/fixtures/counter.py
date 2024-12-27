from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('counter')
def process_counter(value, key, group_pos, group_z_rot):
    """
    Process counter fixture
    
    Args:
        value: Counter data dictionary
        key: Counter identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding counter information
    """
    fixture_info = {
        'name': key,
        'type': 'counter',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }

    if 'corner' in key:
        fixture_info['hollow'] = [False, False]
    
    yield fixture_info