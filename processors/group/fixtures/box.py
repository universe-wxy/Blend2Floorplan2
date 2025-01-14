from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('box')
def process_box(value, key, group_pos, group_z_rot):
    """box fixture"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    size = value.get('size')

    box_info = {
        'name': key,
        'type': 'box',
        'size': size,
        'pos': pos
    }

    yield box_info
