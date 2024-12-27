from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('island')
def process_island(value, key, group_pos, group_z_rot):
    """
    Process island fixture
    
    Args:
        value: Island data dictionary
        key: Island identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding island information
    """
    island_info = {
        'name': key,
        'type': 'counter',
        'default_config_name': 'island',
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }

    if 'base_opening' in value:
        island_info['base_opening'] = value['base_opening']
    else:
        island_info['base_opening'] = [True, False]

    yield island_info