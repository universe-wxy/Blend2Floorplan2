from utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('fridge')
def process_fridge(value, key, group_pos, group_z_rot):
    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )
    size = value.get('size')

    fridge_info = {
        'name': key,
        'type': 'fridge',
        'size': [size[0] - 0.04, size[1], size[2]]
    }

    housing_info = {
        'name': f"{key}_housing",
        'type': 'housing_cabinet',
        'interior_obj': key,
        'padding': [[0.02, 0.02], [-0.04, 0.02], [0, 0.02]],
        'pos': pos,
    }
    yield fridge_info
    yield housing_info