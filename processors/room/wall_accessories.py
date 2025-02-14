from ...utils.type_utils import get_type_from_key


def process_wall_accessories(accessory_data):
    """Process wall accessories and route to specific handlers based on type"""
    accessories = []

    for wall_name, wall_accessories in accessory_data["children"].items():
        for acc_name, acc_info in wall_accessories["children"].items():
            type = get_type_from_key(acc_name)

            # Route to specific handler based on type
            if type == "wallaccessory":
                accessory = process_wall_accessory(acc_name, wall_name, acc_info)
            elif type == "lightswitch":
                accessory = process_light_switch(acc_name, wall_name, acc_info)
            elif type == "outlet":
                accessory = process_outlet(acc_name, wall_name, acc_info)
            elif type == "panrack":
                accessory = process_pan_rack(acc_name, wall_name, acc_info)
            else:
                continue

            accessories.append(accessory)

    return accessories


def process_wall_accessory(acc_name, wall_name, acc_info):
    """Process standard wall accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "wall_accessory",
        "attach_to": wall_name,
    }

    pos = list(acc_info["location"])

    # Set appropriate position based on wall orientation
    if wall_name.startswith("wall_left") or wall_name.startswith("wall_right"):
        pos[0] = None
    else:
        pos[1] = None

    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_light_switch(acc_name, wall_name, acc_info):
    """Process light switch accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "wall_accessory",
        "attach_to": wall_name,
        "config_name": "light_switch",
    }

    pos = list(acc_info["location"])

    # Set appropriate position based on wall orientation
    if wall_name.startswith("wall_left") or wall_name.startswith("wall_right"):
        pos[0] = None
    else:
        pos[1] = None

    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_outlet(acc_name, wall_name, acc_info):
    """Process outlet accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "wall_accessory",
        "attach_to": wall_name,
        "config_name": "outlet",
    }

    pos = list(acc_info["location"])

    # Set appropriate position based on wall orientation
    if wall_name.startswith("wall_left") or wall_name.startswith("wall_right"):
        pos[0] = None
    else:
        pos[1] = None

    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_pan_rack(acc_name, wall_name, acc_info):
    """Process pan rack accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "wall_accessory",
        "attach_to": wall_name,
        "config_name": "pan_rack",
    }

    pos = list(acc_info["location"])

    # Set appropriate position based on wall orientation
    if wall_name.startswith("wall_left") or wall_name.startswith("wall_right"):
        pos[0] = None
    else:
        pos[1] = None

    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data
