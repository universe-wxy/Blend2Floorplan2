def get_type_from_key(key):
    """Extract type from key string.
    
    Args:
        key: String that might contain type information (e.g., 'microwave_1', 'microwave.001', 'microwave')
        
    Returns:
        str: Extracted type
    """
    if '_' in key:
        return key.split('_')[0]
    elif '.' in key:
        return key.split('.')[0]
    return key 