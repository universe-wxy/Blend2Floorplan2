from utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('framedwindow')
def process_framed_window(value, key, group_pos, group_z_rot):
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    window_info = {
        'name': key,
        'type': 'framed_window',
        'num_windows': 3,
        'pos': pos,
        'size': size
    }

    yield window_info