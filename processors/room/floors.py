def process_floors(floor_data):
    """process_floors"""
    floor = []
    for floor_name, floor_info in floor_data['children'].items():
        # floor
        floor_data = {
            'name': floor_name,
            'type': 'floor',
            'size': [
                float(floor_info['size'][0]),
                float(floor_info['size'][1]),
                0.02
            ],
            'pos': [
                float(floor_info['location'][0]),
                float(floor_info['location'][1]),
                float(floor_info['location'][2])
            ]
        }
        floor.append(floor_data)

        # floor_backing
        floor_backing_data = {
            'name': f"{floor_name}_backing",
            'type': 'floor',
            'backing': True,
            'size': [
                float(floor_info['size'][0]),
                float(floor_info['size'][1]),
                0.1
            ],
            'pos': [
                float(floor_info['location'][0]),
                float(floor_info['location'][1]),
                float(floor_info['location'][2])
            ]
        }
        floor.append(floor_backing_data)
    
    return floor