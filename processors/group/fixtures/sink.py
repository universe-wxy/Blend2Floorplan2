from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('sink')
def process_sink(value, key, group_pos, group_z_rot):
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    sink_info = {
        'name': key,
        'type': 'sink',
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

    stack_info = {
        'name': f'{key}_stack',
        'type': 'stack',
        'levels': ['hinge_cabinet'],
        'percentages': [1],
        'pos': [pos[0], pos[1], 0.47],
        'size': [size[0], 0.65, 0.84],
        'open_top': True,
        'configs': {
            'hinge_cabinet': {
                'open_top': 'true',
                'panel_config': {
                    'handle_vpos': 'center'
                }
            }
        }
    }

    yield sink_info
    yield counter_info
    yield stack_info