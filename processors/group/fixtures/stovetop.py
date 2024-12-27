from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('stovetop')
def process_stovetop(value, key, group_pos, group_z_rot):
    """
    Process stovetop fixture
    
    Args:
        value: Stovetop data dictionary
        key: Stovetop identifier
        group_pos: Group position coordinates
        group_z_rot: Group rotation around Z axis
        
    Returns:
        Generator yielding stovetop, counter and hood information
    """
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    stovetop_info = {
        'name': key,
        'type': 'stovetop'
    }
    
    counter_info = {
        'name': f"{key}_counter",
        'type': 'counter',
        'interior_obj': key,
        'obj_x_percent': 0.5,
        'obj_y_percent': 0.5,
        'pos': pos,
        'size': size
    }
    
    hood_info = {
        'name': f"{key}_hood",
        'type': 'hood',
        'size': [key, 0.6, None],
        'offset': [0, 0, 0.75],
        'align_to': key,
        'side': 'top'
    }

    stack_info = {
        'name': f'{key}_stack',
        'type': 'stack',
        'levels': ['hinge_cabinet'],
        'percentages': [1],
        'pos': [pos[0], pos[1], 0.47],
        'size': [size[0], 0.65, 0.84]
    }

    yield stovetop_info
    yield counter_info
    yield hood_info
    yield stack_info