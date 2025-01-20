import numpy as np
import yaml
from robosuite.utils.mjcf_utils import array_to_string as a2s
from robosuite.utils.mjcf_utils import string_to_array as s2a

from robocasa.models.scenes.scene_registry import get_style_path
from robocasa.models.scenes.scene_utils import *
from robocasa.models.fixtures import *
from robocasa.models.fixtures.counter import Counter
from robocasa.models.fixtures.stove import Stove

from robosuite.models.tasks import Task
from robosuite.models.arenas import Arena
from robosuite.utils.mjcf_utils import xml_path_completion

import robocasa

import mujoco
import mujoco.viewer
import sys
import select

# fixture string to class
FIXTURES = dict(
    hinge_cabinet=HingeCabinet,
    single_cabinet=SingleCabinet,
    open_cabinet=OpenCabinet,
    panel_cabinet=PanelCabinet,
    housing_cabinet=HousingCabinet,
    drawer=Drawer,
    counter=Counter,
    stove=Stove,
    stovetop=Stovetop,
    oven=Oven,
    microwave=Microwave,
    hood=Hood,
    sink=Sink,
    fridge=Fridge,
    dishwasher=Dishwasher,
    wall=Wall,
    floor=Floor,
    box=Box,
    accessory=Accessory,
    paper_towel=Accessory,
    plant=Accessory,
    knife_block=Accessory,
    stool=Stool,
    utensil_holder=Accessory,
    coffee_machine=CoffeeMachine,
    toaster=Toaster,
    utensil_rack=WallAccessory,
    wall_accessory=WallAccessory,
    window=Window,
    framed_window=FramedWindow,
    # needs some additional work
    # slide_cabinet=SlideCabinet,
)
# fixtures that are attached to other fixtures, disables positioning system in this script
FIXTURES_INTERIOR = dict(
    sink=Sink, stovetop=Stovetop, accessory=Accessory, wall_accessory=WallAccessory
)

ALL_SIDES = ["left", "right", "front", "back", "bottom", "top"]


def check_syntax(fixture):
    """
    Checks that specifications of a fixture follows syntax rules
    """

    if fixture["type"] != "stack" and fixture["type"] not in FIXTURES:
        raise ValueError(
            'Invalid value for fixture type: "{}".'.format(fixture["type"])
        )

    if "config_name" in fixture and "default_config_name" in fixture:
        raise ValueError('Cannot specify both "config_name" and "default_config_name"')

    if "align_to" in fixture or "side" in fixture or "alignment" in fixture:
        if not ("align_to" in fixture and "side" in fixture):
            raise ValueError(
                'Both or neither of "align_to" and ' '"side" need to be specified.'
            )
        if "pos" in fixture:
            raise ValueError("Cannot specify both relative and absolute positions.")

        # check alignment and side arguments are compatible
        if "alignment" in fixture:
            for keywords in AXES_KEYWORDS.values():
                if fixture["side"] in keywords:
                    # check that neither keyword is used for alignment
                    if (
                        keywords[0] in fixture["alignment"]
                        or keywords[1] in fixture["alignment"]
                    ):
                        raise ValueError(
                            'Cannot set alignment to "{}" when aligning to the "{}" side'.format(
                                fixture["alignment"], fixture["side"]
                            )
                        )

        # check if side is valid
        if fixture["side"] not in ALL_SIDES:
            raise ValueError(
                '"{}" is not a valid side for alignment'.format(fixture["side"])
            )


def create_fixtures(args, rng=None):
    try:
        style = int(style)
    except:
        pass

    style_path = get_style_path(style_id=args.style_id)

    # load style
    with open(style_path, "r") as f:
        style = yaml.safe_load(f)

    # load arena
    with open(args.layout_path, "r") as f:
        arena_config = yaml.safe_load(f)

    # contains all fixtures with updated configs
    arena = list()

    # Update each fixture config. First iterate through groups: subparts of the arena that can be
    # rotated and displaced together. example: island group, right group, room group, etc
    for group_name, group_config in arena_config.items():
        group_fixtures = list()
        # each group is further divded into similar subcollections of fixtures
        # ex: main group counter accessories, main group top cabinets, etc
        for k, fixture_list in group_config.items():
            # these values are rotations/displacements that are applied to all fixtures in the group
            if k in ["group_origin", "group_z_rot", "group_pos"]:
                continue
            elif type(fixture_list) != list:
                raise ValueError('"{}" is not a valid argument for groups'.format(k))

            # add suffix to support different groups
            for fxtr_config in fixture_list:
                fxtr_config["name"] += "_" + group_name
                # update fixture names for alignment, interior objects, etc.
                for k in ATTACH_ARGS + ["align_to", "stack_fixtures", "size"]:
                    if k in fxtr_config:
                        if isinstance(fxtr_config[k], list):
                            for i in range(len(fxtr_config[k])):
                                if isinstance(fxtr_config[k][i], str):
                                    fxtr_config[k][i] += "_" + group_name
                        else:
                            if isinstance(fxtr_config[k], str):
                                fxtr_config[k] += "_" + group_name

            group_fixtures.extend(fixture_list)

        # update group rotation/displacement if necessary
        if "group_origin" in group_config:
            for fxtr_config in group_fixtures:
                # do not update the rotation of the walls/floor
                if fxtr_config["type"] in ["wall", "floor"]:
                    continue
                fxtr_config["group_origin"] = group_config["group_origin"]
                fxtr_config["group_pos"] = group_config["group_pos"]
                fxtr_config["group_z_rot"] = group_config["group_z_rot"]

        # addto overall fixture list
        arena.extend(group_fixtures)

    # maps each fixture name to its object class
    fixtures = dict()
    # maps each fixture name to its configuration
    configs = dict()
    # names of composites, delete from fixtures before returning
    composites = list()

    # initialize each fixture in the arena by processing config
    for fixture_config in arena:
        check_syntax(fixture_config)
        fixture_name = fixture_config["name"]

        # stack of fixtures, handled separately
        if fixture_config["type"] == "stack":
            stack = FixtureStack(
                fixture_config,
                fixtures,
                configs,
                style,
                default_texture=None,
                rng=rng,
            )
            fixtures[fixture_name] = stack
            configs[fixture_name] = fixture_config
            composites.append(fixture_name)
            continue

        # load style information and update config to include it
        default_config = load_style_config(style, fixture_config)
        if default_config is not None:
            for k, v in fixture_config.items():
                default_config[k] = v
            fixture_config = default_config

        # set fixture type
        fixture_config["type"] = FIXTURES[fixture_config["type"]]

        # pre-processing for fixture size
        size = fixture_config.get("size", None)
        if isinstance(size, list):
            for i in range(len(size)):
                elem = size[i]
                if isinstance(elem, str):
                    ref_fxtr = fixtures[elem]
                    size[i] = ref_fxtr.size[i]

        # initialize fixture
        fixture = initialize_fixture(fixture_config, fixtures, rng=rng)
        fixtures[fixture_name] = fixture
        configs[fixture_name] = fixture_config

        # update fixture position
        if fixture_config["type"] not in FIXTURES_INTERIOR.values():
            # relative positioning
            if "align_to" in fixture_config:
                pos = get_relative_position(
                    fixture,
                    fixture_config,
                    fixtures[fixture_config["align_to"]],
                    configs[fixture_config["align_to"]],
                )

            elif "stack_on" in fixture_config:
                stack_on = fixtures[fixture_config["stack_on"]]

                # account for off-centered objects
                stack_on_center = stack_on.center

                # infer unspecified axes of position
                pos = fixture_config["pos"]
                if pos[0] is None:
                    pos[0] = stack_on.pos[0] + stack_on_center[0]
                if pos[1] is None:
                    pos[1] = stack_on.pos[1] + stack_on_center[1]

                # calculate height of fixture
                pos[2] = stack_on.pos[2] + stack_on.size[2] / 2 + fixture.size[2] / 2
                pos[2] += stack_on_center[2]
            else:
                # absolute position
                pos = fixture_config.get("pos", None)
            if pos is not None and type(fixture) not in [Wall, Floor]:
                fixture.set_pos(pos)

    # composites are non-MujocoObjects, must remove
    for composite in composites:
        del fixtures[composite]

    # update the rotation and postion of each fixture based on their group
    for name, fixture in fixtures.items():
        # check if updates are necessary
        config = configs[name]
        if "group_origin" not in config:
            continue

        # TODO: add default for group origin?
        # rotate about this coordinate (around the z-axis)
        origin = config["group_origin"]
        pos = config["group_pos"]
        z_rot = config["group_z_rot"]
        displacement = [pos[0] - origin[0], pos[1] - origin[1]]

        if type(fixture) not in [Wall, Floor]:
            dx = fixture.pos[0] - origin[0]
            dy = fixture.pos[1] - origin[1]
            dx_rot = dx * np.cos(z_rot) - dy * np.sin(z_rot)
            dy_rot = dx * np.sin(z_rot) + dy * np.cos(z_rot)

            x_rot = origin[0] + dx_rot
            y_rot = origin[1] + dy_rot
            z = fixture.pos[2]
            pos_new = [x_rot + displacement[0], y_rot + displacement[1], z]

            # account for previous z-axis rotation
            rot_prev = fixture._obj.get("euler")
            if rot_prev is not None:
                # TODO: switch to quaternion since euler rotations are ambiguous
                rot_new = s2a(rot_prev)
                rot_new[2] += z_rot
            else:
                rot_new = [0, 0, z_rot]

            fixture._obj.set("pos", a2s(pos_new))
            fixture._obj.set("euler", a2s(rot_new))

    return fixtures

class KitchenArena(Arena):
    """
    Kitchen arena class holding all of the fixtures

    Args:
        layout_id (int or LayoutType): layout of the kitchen to load

        style_id (int or StyleType): style of the kitchen to load

        rng (np.random.Generator): random number generator used for initializing
            fixture state in the KitchenArena
    """

    def __init__(self, layout_path, rng=None):
        super().__init__(
            xml_path_completion(
                "arenas/empty_kitchen_arena.xml", root=robocasa.models.assets_root
            )
        )
        self.fixtures = create_fixtures(
            layout_path=layout_path
        )

    def get_fixture_cfgs(self):
        """
        Returns config data for all fixtures in the arena

        Returns:
            list: list of fixture configurations
        """
        fixture_cfgs = []
        for (name, fxtr) in self.fixtures.items():
            cfg = {}
            cfg["name"] = name
            cfg["model"] = fxtr
            cfg["type"] = "fixture"
            if hasattr(fxtr, "_placement"):
                cfg["placement"] = fxtr._placement

            fixture_cfgs.append(cfg)

        return fixture_cfgs
    
def create_and_load_scene(layout_path):
    mujoco_arena = KitchenArena(
        layout_path=layout_path,
    )

    fixture_cfgs = mujoco_arena.get_fixture_cfgs()
    fixtures = {cfg["name"]: cfg["model"] for cfg in fixture_cfgs}

    model = Task(
        mujoco_arena=mujoco_arena,
        mujoco_robots=[],
        mujoco_objects=list(fixtures.values()),
    )

    xml = model.get_xml()
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    return model, data


def config_cam(viewer):
    viewer.cam.azimuth = 90
    viewer.cam.elevation = -20
    viewer.cam.distance = 3.0
    viewer.cam.lookat[0:3] = [1.8, -8.0, 3.5]

def check_stove_height_alignment(bm):
    """检查相邻灶台的高度是否对齐"""
    stoves = [obj for obj in bm.objects if obj.name.startswith("Stove")]
    
    if len(stoves) < 2:
        return True  # 如果只有一个灶台或没有灶台，则无需检查对齐
        
    issues = []
    tolerance = 0.001  # 允许的高度误差范围(米)
    
    for i, stove1 in enumerate(stoves):
        for stove2 in stoves[i+1:]:
            # 检查两个灶台是否相邻
            distance = (stove1.location - stove2.location).length
            if distance < 1.5:  # 如果灶台间距小于1.5米，认为是相邻的
                height1 = stove1.location.z
                height2 = stove2.location.z
                
                if abs(height1 - height2) > tolerance:
                    issues.append(f"灶台 {stove1.name} 和 {stove2.name} 的高度不一致")
    
    return len(issues) == 0, issues

def check_countertop_height_alignment(fixtures):
    """检查台面尺寸是否符合标准，特别关注灶台高度"""
    # 获取所有台面类型的设备（counter和stove），排除岛台
    countertops = []
    stoves = []  # 单独存储灶台
    for name, fixture in fixtures.items():
        if 'island' not in name.lower():
            if isinstance(fixture, Counter):
                countertops.append((name, fixture))
            elif isinstance(fixture, Stove):
                stoves.append((name, fixture))
    
    if len(countertops) < 1:
        return True, []
        
    issues = []
    tolerance = 0.001  # 允许的误差范围(米)
    
    # 从普通台面获取标准高度和深度
    counter_depths = [fixture.size[1] for name, fixture in countertops]
    counter_heights = [fixture.size[2] for name, fixture in countertops]
    
    # 使用普通台面的尺寸作为标准
    from collections import Counter as CollectionCounter
    standard_depth = CollectionCounter(counter_depths).most_common(1)[0][0]
    standard_height = CollectionCounter(counter_heights).most_common(1)[0][0]
    
    print(f"\n标准台面尺寸:")
    print(f"- 标准深度: {standard_depth:.3f}m")
    print(f"- 标准高度: {standard_height:.3f}m")
    
    # 检查灶台
    for name, stove in stoves:
        current_depth = stove.size[1]
        current_height = stove.size[2]
        
        # 检查深度
        if abs(current_depth - standard_depth) > tolerance:
            issue = f"警告: 灶台 {name} 的深度为 {current_depth:.3f}m, 与标准深度 {standard_depth:.3f}m 不符"
            issues.append(issue)
        
        # 检查高度
        if abs(current_height - standard_height) > tolerance:
            issue = f"警告: 灶台 {name} 的高度为 {current_height:.3f}m, 与标准高度 {standard_height:.3f}m 不符"
            issues.append(issue)
            # 添加修改建议
            if current_height < standard_height:
                issues.append(f"建议: 请检查 {name} 的高度设置，可能需要调整到 {standard_height:.3f}m")
    
    # 检查其他台面
    for name, counter in countertops:
        current_depth = counter.size[1]
        current_height = counter.size[2]
        
        # 检查深度
        if abs(current_depth - standard_depth) > tolerance:
            issue = f"台面 {name} 的深度为 {current_depth:.3f}m, 与标准深度 {standard_depth:.3f}m 不符"
            issues.append(issue)
        
        # 检查高度
        if abs(current_height - standard_height) > tolerance:
            issue = f"台面 {name} 的高度为 {current_height:.3f}m, 与标准高度 {standard_height:.3f}m 不符"
            issues.append(issue)
    
    return len(issues) == 0, issues

def check_kitchen(fixtures):
    """主检查函数"""
    issues = []
    all_passed = True
    
    # 检查台面高度对齐
    height_aligned, height_issues = check_countertop_height_alignment(fixtures)
    if not height_aligned:
        all_passed = False
        issues.extend(height_issues)
    
    return all_passed, issues

if __name__ == "__main__":
    import argparse
    
    # 修改参数解析器
    parser = argparse.ArgumentParser(description='Create fixtures from a layout YAML file')
    parser.add_argument('layout_path', type=str, help='Path to the layout YAML file')
    parser.add_argument('--demo', action='store_true', help='Whether to run the demo')
    parser.add_argument('--style_id', type=int, default=6, help='Style ID to use for layout generation')
    parser.add_argument('--check', action='store_true', help='Run kitchen layout checks')
    
    try:
        args = parser.parse_args()
        fixtures = create_fixtures(args.layout_path)
        
        # 如果指定了check参数，运行检查
        if args.check:
            passed, issues = check_kitchen(fixtures)
            if not passed:
                for issue in issues:
                    print(f"检测到问题: {issue}")
            
        # 如果指定了demo参数，运行demo
        if args.demo:
            model, data = create_and_load_scene(args.layout_path)
            renderer = mujoco.Renderer(model)

            with mujoco.viewer.launch_passive(model, data) as viewer:
                config_cam(viewer)
                while viewer.is_running():
                    mujoco.mj_step(model, data)
                    
                    line = sys.stdin.readline()
                    if line.strip() == "q":
                        viewer.close()
                        model, data = create_and_load_scene(args.layout_path)
                        renderer = mujoco.Renderer(model)
                        config_cam(viewer)
                        viewer = mujoco.viewer.launch_passive(model, data)

                    mujoco.mj_forward(model, data)
                    renderer.update_scene(data)
                    renderer.render()
                    viewer.sync()

            viewer.close()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        parser.print_help()
        viewer.close()
    else:
        fixtures = create_fixtures(args)
