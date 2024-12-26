def process_walls(wall_data):
    SIDE_MAPPING = {
        'left': 'left',
        'right': 'right',
        'front': 'front'
    }
    
    walls = []
    for wall_name, wall_info in wall_data['children'].items():
        # Determine wall side
        wall_side = next(
            (side for key, side in SIDE_MAPPING.items() if key in wall_name.lower()),
            None
        )
        
        # Common data for both wall and backing
        size = [float(wall_info['size'][0]), float(wall_info['size'][1])]
        pos = [float(val) for val in wall_info['location']]
        
        # Adjust position based on wall_side
        if wall_side == 'front':
            pos[1] += 0.06
        elif wall_side == 'left':
            pos[0] += 0.06
        elif wall_side == 'right':
            pos[0] -= 0.06
        elif wall_side is None:
            pos[1] -= 0.06
        
        # Main wall
        wall = {
            'name': wall_name,
            'type': 'wall',
            'size': size + [0.02],
            'pos': pos.copy()
        }
        if wall_side:
            wall['wall_side'] = wall_side
        walls.append(wall)
        
        # Wall backing
        backing = {
            'name': f"{wall_name}_backing",
            'type': 'wall',
            'backing': True,
            'backing_extended': [True, True],
            'size': size + [0.1],
            'pos': pos.copy()
        }
        if wall_side:
            backing['wall_side'] = wall_side
        walls.append(backing)

    return walls
