# TODO: define a check operator to check whether the scene data is valid
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

            process = subprocess.Popen(
                ['conda', 'run', '-n', 'robocasa', 'python', python_script_path, layout_path],
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
