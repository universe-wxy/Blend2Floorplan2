def custom_format(data, indent=0):
    """
    Format data structure into a custom YAML-like string representation.
    Skip empty collections.
    
    Args:
        data: The data to format (dict, list, or primitive type)
        indent: The current indentation level
        
    Returns:
        list: Lines of formatted string
    """
    result = []
    if isinstance(data, dict):
        # Only format non-empty dictionaries
        if data:
            result.extend(_format_dict(data, indent))
    return result

def _format_dict(data, indent):
    """Handle dictionary formatting, skip empty collections"""
    result = []
    for key, value in data.items():
        # Skip empty lists or dictionaries
        if isinstance(value, (list, dict)) and not value:
            continue
            
        if _is_group_attribute(key):
            result.extend(_format_group_attribute(key, value, indent))
        else:
            result.extend(_format_regular_key_value(key, value, indent))
    return result

def _is_group_attribute(key):
    """Check if the key is a special group-related attribute"""
    return key in ['group_z_rot', 'group_origin', 'group_pos']

def _format_group_attribute(key, value, indent):
    """Format special group-related attributes"""
    if isinstance(value, list):
        # Format list-type attributes as [x, y, z]
        formatted_values = [_format_value(x) for x in value]
        return [' ' * indent + f'{key}: [{", ".join(formatted_values)}]']
    return [' ' * indent + f'{key}: {value}']

def _format_regular_key_value(key, value, indent):
    """Format regular key-value pairs"""
    result = [' ' * indent + f'{key}:']
    
    if isinstance(value, dict):
        result.extend(custom_format(value, indent + 2))
    elif isinstance(value, list):
        result.extend(_format_list(value, indent))
    else:
        result.append(' ' * (indent + 2) + str(value))
    
    return result

def _format_list(items, indent):
    """Format list items, skip empty collections"""
    result = []
    for item in items:
        if isinstance(item, dict):
            # Skip empty dictionaries
            if item:
                result.extend(_format_dict_in_list(item, indent))
        else:
            result.append(' ' * (indent + 2) + f'- {item}')
    return result

def _format_dict_in_list(item, indent):
    """Format dictionary items within a list"""
    result = []
    if result and not result[-1].strip() == '':
        result.append('')
    
    # Add name field first
    result.append(' ' * (indent + 2) + '- name: ' + item['name'])
    
    # Add type field if present
    if 'type' in item:
        result.append(' ' * (indent + 4) + f'type: {item["type"]}')
    
    # Add other fields
    for k, v in item.items():
        if k not in ['name', 'type']:
            result.append(_format_field(k, v, indent + 4))
    
    result.append('')
    return result

def _format_field(key, value, indent):
    """Format a single field in a dictionary"""
    if isinstance(value, list):
        formatted_values = [_format_value(x) for x in value]
        return ' ' * indent + f'{key}: [{", ".join(formatted_values)}]'
    elif isinstance(value, bool):
        return ' ' * indent + f'{key}: {str(value).lower()}'
    else:
        return ' ' * indent + f'{key}: {value}'

def _format_value(value):
    """Format a single value"""
    if isinstance(value, float):
        return str(round(value, 3))
    elif value is None:
        return 'null'
    return str(value)