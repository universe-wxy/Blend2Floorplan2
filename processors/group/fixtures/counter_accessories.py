from ....utils.type_utils import get_type_from_key

# possible to modeify
def process_counter_accessories(accessory_data):
    """Process counter accessories and route to specific handlers based on type"""
    accessories = []

    for group_name, group_accessories in accessory_data["children"].items():
        for acc_name, acc_info in group_accessories["children"].items():
            type = get_type_from_key(acc_name)

            if type == "counter_accessory":
                accessory = process_counter_accessory(acc_name, group_name, acc_info)

            elif type == "paper_towel":
                accessory = process_paper_towel(acc_name, group_name, acc_info)

            elif type == "coffee_machine":
                accessory = process_coffee_machine(acc_name, group_name, acc_info)

            elif type == "knife_block":
                accessory = process_knife_block(acc_name, group_name, acc_info)

            elif type == "toaster":
                accessory = process_toaster(acc_name, group_name, acc_info)

            else:
                continue

            accessories.append(accessory)

    return accessories


def process_counter_accessory(acc_name, group_name, acc_info):
    """Process standard counter accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "counter_accessory",
        "attach_to": group_name,
    }
    pos = list(acc_info["location"])
    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_paper_towel(acc_name, group_name, acc_info):
    """Process paper towel accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "paper_towel",
        "attach_to": group_name,
    }
    pos = list(acc_info["location"])
    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_coffee_machine(acc_name, group_name, acc_info):
    """Process coffee machine accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "coffee_machine",
        "attach_to": group_name,
    }
    pos = list(acc_info["location"])
    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_knife_block(acc_name, group_name, acc_info):
    """Process knife block accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "knife_block",
        "attach_to": group_name,
    }
    pos = list(acc_info["location"])
    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data


def process_toaster(acc_name, group_name, acc_info):
    """Process toaster accessory"""
    accessory_data = {
        "name": acc_name,
        "type": "toaster",
        "attach_to": group_name,
    }
    pos = list(acc_info["location"])
    accessory_data["pos"] = [round(x, 3) if x is not None else None for x in pos]
    return accessory_data
