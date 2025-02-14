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

    size = value.get('size')

    bottom_info = {
        'name': f"{key}_bottom",
        'type': 'stack',
        'levels': ["drawer"],
        'percentages': [1],
        'pos': [pos[0], pos[1], 0.15],
        'size': [size[0], size[1], 0.3]
    }

    oven_info = {
        'name': f"{key}_oven",
        'type': 'oven',
        'size': [size[0] - 0.1, size[1], 0.68]
    }

    oven_housing_info = {
        'name': f"{key}_oven_housing",
        'type': 'housing_cabinet',
        'size': [size[0], size[1], 0.7],
        'padding': '[null, [-0.01, null], null]',
        'align_to': f"{key}_bottom",
        'alignment': 'front',
        'side': 'top',
        'interior_obj': f"{key}_oven"
    }

    microwave_info = {
        'name': f"{key}_microwave",
        'type': 'microwave',
        'size': [size[0] - 0.05, size[1]-0.15, None]
    }

    microwave_housing_info = {
        'name': f"{key}_microwave_housing",
        'type': 'housing_cabinet',
        'size': [size[0], size[1], 0.55],
        'padding': '[null, [-0.01, null], null]',
        'align_to': f"{key}_oven_housing",
        'alignment': 'front',
        'side': 'top',
        'interior_obj': f"{key}_microwave"
    }

    top_info = {
        'name': f"{key}_top",
        'type': 'hinge_cabinet',
        'size': [size[0], size[1], None],
        'align_to': f"{key}_microwave_housing",
        'alignment': 'front',
        'side': 'top',
        'stack_height': size[2],
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

@register_fixture('cabcorner')
def process_cab_corner(value, key, group_pos, group_z_rot):
    """custom fixture: cab_corner"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    size = value.get('size')

    cab_corner_info = {
        'name': key,
        'type': 'box',
        'size': size,
        'pos': pos
    }

    yield cab_corner_info

@register_fixture('panelbox')
def process_panel_box(value, key, group_pos, group_z_rot):
    """custom fixture: panel_box"""

    pos = abs2rel_pos(
        group_pos,
        group_z_rot,
        value.get('location', [0, 0, 0])
    )

    size = value.get('size')

    panel_box_info = {
        'name': key,
        'type': 'stack',
        'size': size,
        'pos': pos,
        'levels': ["panel_cabinet"],
        'percentages': [1],
        'configs': {
            'panel_cabinet': {
                'solid_body': True,
                'panel_type': "slab"
            }
        }
    }

    # levels: [panel_cabinet]
    #   percentages: [1]

    #   configs:
    #     panel_cabinet:
    #       solid_body: true
    #       panel_type: "slab"

    yield panel_box_info