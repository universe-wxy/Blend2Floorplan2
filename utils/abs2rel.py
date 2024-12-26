import numpy as np
from typing import List

def _create_rotation_matrix(angle: float) -> np.ndarray:
    """Create a 2D rotation matrix.
    
    Args:
        angle: Rotation angle in radians
        
    Returns:
        2x2 rotation matrix
    """
    cos_theta = np.cos(-angle)
    sin_theta = np.sin(-angle)
    return np.array([[cos_theta, -sin_theta],
                    [sin_theta, cos_theta]])

def _transform_2d(vec: np.ndarray, rotation_matrix: np.ndarray) -> np.ndarray:
    """Transform a 2D vector.
    
    Args:
        vec: 2D vector
        rotation_matrix: 2x2 rotation matrix
        
    Returns:
        Transformed vector
    """
    return np.round(rotation_matrix @ vec, 4)

def abs2rel_pos(group_pos: List[float], group_z_rot: float, 
                abs_pos: List[float]) -> List[float]:
    """Convert absolute position to relative position.
    
    Args:
        group_pos: Group position [x, y, z]
        group_z_rot: Z-axis rotation angle in radians
        abs_pos: Absolute position [x, y, z]
        
    Returns:
        Relative position [x, y, z]
    """
    rel_pos = np.array(abs_pos[0:2])
    rel_pos -= np.array(group_pos[0:2])
    rotation_matrix = _create_rotation_matrix(group_z_rot)
    rel_pos = _transform_2d(rel_pos, rotation_matrix)
    
    return rel_pos.tolist() + [abs_pos[2]]

def abs2rel_size(group_z_rot: float, abs_size: List[float]) -> List[float]:
    """Convert absolute size to relative size.
    
    Args:
        group_z_rot: Z-axis rotation angle in radians
        abs_size: Absolute size [x, y, z]
        
    Returns:
        Relative size [x, y, z]
    """
    rel_size = np.array(abs_size[0:2])
    rotation_matrix = _create_rotation_matrix(group_z_rot)
    rel_size = _transform_2d(rel_size, rotation_matrix)
    rel_size = np.abs(rel_size)
    
    return rel_size.tolist() + [abs_size[2]]
