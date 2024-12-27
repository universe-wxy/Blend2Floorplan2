from robosuite.models.tasks import Task
from robocasa.models.scenes import KitchenArena
import mujoco
import mujoco.viewer
import sys
import select

def create_and_load_scene():
    mujoco_arena = KitchenArena(
        layout_id=10,
        style_id=0,
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

model, data = create_and_load_scene()
renderer = mujoco.Renderer(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    config_cam(viewer)
    while viewer.is_running():
        mujoco.mj_step(model, data)

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line.strip() == "q":
                viewer.close()
                model, data = create_and_load_scene()
                renderer = mujoco.Renderer(model)
                config_cam(viewer)
                viewer = mujoco.viewer.launch_passive(model, data)

        mujoco.mj_forward(model, data)
        renderer.update_scene(data)
        renderer.render()
        viewer.sync()

viewer.close()