from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('stack')
def process_stack(value, key, group_pos, group_z_rot):
    """
    Process stack fixture
    
    Args:
        value: Stack data dictionary
        key: Stack identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding stack information
    """
    stack_info = {
        'name': key,
        'type': 'stack',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }
    
    if 'levels' in value:
        stack_info['levels'] = value['levels']
    
    if 'percentages' in value:
        stack_info['percentages'] = value['percentages']
    
    yield stack_info