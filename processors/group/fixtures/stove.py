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
    pass
