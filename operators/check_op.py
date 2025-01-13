# TODO: test the check operator on windows
import bpy
import subprocess  # Import subprocess to run system commands
import os

class FLOORPLAN_OT_check(bpy.types.Operator):
    """Check the scene data"""
    bl_idname = "floorplan.check"
    bl_label = "Check"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            python_script_path = os.path.join(current_dir, 'core', 'check.py')

            layout_path = bpy.context.scene.get('exported_yaml')

            # Get conda executable path based on OS
            if os.name == 'nt':  # Windows
                conda_path = os.path.expanduser(r"~/miniconda3/Scripts/conda.exe")
            else:  # Linux/MacOS
                conda_path = os.path.expanduser("~/miniconda3/bin/conda")
            print(conda_path)

            process = subprocess.Popen(
                [conda_path, 'run', '-n', 'robocasa', 'python', python_script_path, layout_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.report({'INFO'}, "Demo script executed successfully")
            else:
                self.report({'ERROR'}, f"Demo script failed: {stderr.decode()}")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to execute demo script: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}

class FLOORPLAN_OT_demo(bpy.types.Operator):
    """Check the scene data"""
    bl_idname = "floorplan.demo"
    bl_label = "Demo"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            python_script_path = os.path.join(current_dir, 'core', 'check.py')

            layout_path = bpy.context.scene.get('exported_yaml')

            if os.name == 'nt':  # Windows
                conda_path = os.path.expanduser(r"~/miniconda3/Scripts/conda.exe")
            else:  # Linux/MacOS
                conda_path = os.path.expanduser("~/miniconda3/bin/conda")

            process = subprocess.Popen(
                [conda_path, 'run', '-n', 'robocasa', 'python', python_script_path, layout_path, '--demo'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.report({'INFO'}, "Demo script executed successfully")
            else:
                self.report({'ERROR'}, f"Demo script failed: {stderr.decode()}")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to execute demo script: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}