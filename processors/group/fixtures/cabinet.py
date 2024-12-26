from utils import abs2rel_pos
from .registry import register_fixture

def _process_cabinet_base(value, key, group_pos, group_z_rot, cabinet_type):
    """
    Base processor for all cabinet types
    """
    return {
        'name': key,
        'type': cabinet_type,
        'pos': abs2rel_pos(
            group_pos,
            group_z_rot,
            value.get('location', [0, 0, 0])
        ),
        'size': value.get('size')
    }

@register_fixture('cabinet')
def process_cabinet(value, key, group_pos, group_z_rot):
    yield _process_cabinet_base(value, key, group_pos, group_z_rot, 'cabinet')

@register_fixture('hingecabinet')
def process_hingecabinet(value, key, group_pos, group_z_rot):
    yield _process_cabinet_base(value, key, group_pos, group_z_rot, 'hinge_cabinet')

@register_fixture('singlecabinet')
def process_singlecabinet(value, key, group_pos, group_z_rot):
    yield _process_cabinet_base(value, key, group_pos, group_z_rot, 'single_cabinet')

@register_fixture('opencabinet')
def process_opencabinet(value, key, group_pos, group_z_rot):
    yield _process_cabinet_base(value, key, group_pos, group_z_rot, 'open_cabinet')

@register_fixture('panelcabinet')
def process_panelcabinet(value, key, group_pos, group_z_rot):
    yield _process_cabinet_base(value, key, group_pos, group_z_rot, 'panel_cabinet')