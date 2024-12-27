from .group.axis import process_axis
from .group.fixtures.fixture import process_fixture
from .group.objects.object import process_object
from ..utils.constants import FIXTURES_SET, OBJECTS_SET
from ..utils.type_utils import get_type_from_key

def process_group_data(group_data):
    group_result = {}

    axis_info = None
    if 'children' in group_data and 'axis' in group_data['children']:
        axis_data = group_data['children']['axis']
        axis_info = process_axis(axis_data)
        if axis_info:
            group_result.update(axis_info)
    
    for group_key, group_value in group_data['children'].items():
        if group_key != 'axis':
            if isinstance(group_value, dict):
                if group_value.get('type') == 'COLLECTION':
                    if axis_info:
                        group_pos = axis_info['group_pos']
                        group_z_rot = axis_info['group_z_rot']
                    else:
                        group_pos = [0, 0]
                        group_z_rot = 0
                    
                    result = []
                    for key, value in group_value['children'].items():
                        type = get_type_from_key(key)
                        if type in FIXTURES_SET:
                            fixtures = list(process_fixture(value, key, group_pos, group_z_rot))
                            for fixture_info in fixtures:
                                result.append(fixture_info)
                        elif type in OBJECTS_SET:
                            for object_info in process_object(value, key, group_pos, group_z_rot):
                                result.append(object_info)
                    
                    if result:
                        group_result[group_key] = result
    
    return group_result