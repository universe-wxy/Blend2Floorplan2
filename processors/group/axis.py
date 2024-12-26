import math

def quaternion_to_euler(qw, qx, qy, qz):
    """Convert quaternion to Euler angles (returns only z-axis rotation)"""
    # Calculate z-axis rotation angle
    z_rot = math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy * qy + qz * qz))
    return z_rot

def process_axis(axis_data):
    """Process axis data to extract group position and rotation information"""
    if not axis_data:
        return None
        
    location = axis_data.get('location', [0, 0, 0])
    rotation_quaternion = axis_data.get('rotation_quaternion', [1, 0, 0, 0])
    
    # Extract position information
    group_pos = [location[0], location[1]]
    
    # Calculate z-axis rotation angle
    z_rot = quaternion_to_euler(*rotation_quaternion)
    
    return {
        'group_origin': [0, 0],  # Always [0, 0]
        'group_pos': group_pos,
        'group_z_rot': z_rot
    } 