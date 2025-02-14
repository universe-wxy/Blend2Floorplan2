from .room.walls import process_walls
from .room.floors import process_floors
from .room.wall_accessories import process_wall_accessories


def process_room_data(room_data):
    result = {}

    # process walls
    if "children" in room_data and "walls" in room_data["children"]:
        wall_data = room_data["children"]["walls"]
        walls_result = process_walls(wall_data)
        if walls_result:
            result["walls"] = walls_result

    # process floors
    if "children" in room_data and "floors" in room_data["children"]:
        floor_data = room_data["children"]["floors"]
        floors_result = process_floors(floor_data)
        if floors_result:
            result["floor"] = floors_result

    # process wall_accessories
    if "children" in room_data and "wall_accessories" in room_data["children"]:
        wall_accessory_data = room_data["children"]["wall_accessories"]
        wall_accessories_result = process_wall_accessories(wall_accessory_data)
        if wall_accessories_result:
            result["wall_accessories"] = wall_accessories_result

    return result
