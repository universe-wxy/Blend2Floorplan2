from ....utils import abs2rel_pos
from .registry import register_fixture

@register_fixture('qianrugui')
def process_qianrugui(value, key, group_pos, group_z_rot):
    """custom fixture: qianrugui"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    bottom_info = {
        'name': f"{key}_bottom",
        'type': 'stack',
        'levels': ["drawer", "drawer"],
        'percentages': [0.5, 0.5],
        'pos': [pos[0], pos[1], 0.35],
        'size': [0.8, 0.6, 0.6]
    }

    oven_info = {
        'name': f"{key}_oven",
        'type': 'oven',
        'size': [0.75, 0.60, 0.68]
    }

    oven_housing_info = {
        'name': f"{key}_oven_housing",
        'type': 'housing_cabinet',
        'size': [0.8, 0.6, 0.7],
        'padding': '[null, [-0.01, null], null]',
        'align_to': f"{key}_bottom",
        'alignment': 'front',
        'side': 'top',
        'interior_obj': f"{key}_oven"
    }

    microwave_info = {
        'name': f"{key}_microwave",
        'type': 'microwave',
        'size': [0.75, 0.50, None]
    }

    microwave_housing_info = {
        'name': f"{key}_microwave_housing",
        'type': 'housing_cabinet',
        'size': [0.8, 0.6, 0.55],
        'padding': '[null, [-0.01, null], null]',
        'align_to': f"{key}_oven_housing",
        'alignment': 'front',
        'side': 'top',
        'interior_obj': f"{key}_microwave"
    }

    top_info = {
        'name': f"{key}_top",
        'type': 'hinge_cabinet',
        'size': [0.8, 0.6, None],
        'align_to': f"{key}_microwave_housing",
        'alignment': 'front',
        'side': 'top',
        'stack_height': 2.55,
        'stack_fixtures': [f"{key}_bottom", f"{key}_oven_housing", f"{key}_microwave_housing"]
    }

    yield bottom_info
    yield oven_info
    yield oven_housing_info
    yield microwave_info
    yield microwave_housing_info
    yield top_info

@register_fixture('pillar')
def process_pillar(value, key, group_pos, group_z_rot):
    """custom fixture: pillar"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    size = value.get('size')

    pillar_info = {
        'name': key,
        'type': 'box',
        'size': size,
        'pos': pos
    }

    yield pillar_info

@register_fixture('cube')
def process_cube(value, key, group_pos, group_z_rot):
    """custom fixture: cube"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    size = value.get('size')

    cube_info = {
        'name': key,
        'type': 'box',
        'size': size,
        'pos': pos
    }

    yield cube_info
