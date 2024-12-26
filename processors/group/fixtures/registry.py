from functools import wraps
from typing import Callable, Dict

# Registry to store all fixture processors
fixture_processors: Dict[str, Callable] = {}

def register_fixture(fixture_type: str):
    """
    Decorator to register fixture processors
    
    Args:
        fixture_type: Type of the fixture to register
        
    Example:
        @register_fixture('counter')
        def process_counter(value, key, group_pos, group_z_rot):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        print(f"Registering processor for {fixture_type}")
        fixture_processors[fixture_type] = func
        return wrapper
    return decorator

def get_processor(fixture_type: str) -> Callable:
    """
    Get processor function for given fixture type
    
    Args:
        fixture_type: Type of fixture to process
        
    Returns:
        Processor function for the fixture type
    """
    processor = fixture_processors.get(fixture_type)
    return processor

