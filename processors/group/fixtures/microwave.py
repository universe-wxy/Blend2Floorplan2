from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('microwave')
def process_microwave(value, key, group_pos, group_z_rot):
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    microwave_info = {
        'name': key,
        'type': 'microwave',
        'size': size
    }

    housing_info = {
        'name': f"{key}_housing",
        'type': 'housing_cabinet',
        'interior_obj': key,
        'padding': [[0.02, 0.02], [-0.04, 0.02], [0, 0.02]],
        'pos': pos,
    }
    yield microwave_info
    yield housing_info