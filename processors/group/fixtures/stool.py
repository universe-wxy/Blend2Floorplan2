from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('stool')
def process_stool(value, key, group_pos, group_z_rot):
    """
    Process stool fixture
    """
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    stool_info = {
        'name': key,
        'type': 'stool',
        'pos': [pos[0], pos[1], 0.5],
    }

    yield stool_info