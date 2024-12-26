# blend2floorplan

A blender add-on which models and converts the kitchen scene from blender to RoboCasa `yaml` format.

## Development in IDE

Some tips for development in IDE:

- `ln -s blend2floorplan ~/.config/blender/4.3/scripts/addons/blend2floorplan` to enable the plugin in Blender.
- `pip install fake-bpy-module` to enable type hinting in IDE like VSCode and Cursor.

## Usages

Three panels in the Blender UI:

- `Spawn Objects`: Spawn room objects.
- `Check Objects`: Check the room objects (whether satisfy the correct yaml format).
- `Export YAML`: Export the room objects to `yaml` file.

## TODO

- [ ] Check Objects
