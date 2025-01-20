# TODO: define a check operator to check whether the scene data is valid
import bpy
import subprocess  # Import subprocess to run system commands
import os
import platform  # 添加platform模块

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
            style_id = str(context.scene.check_style_id)  # 使用check_style_id而不是style_id

            # 根据操作系统选择Python解释器
            python_interpreter = 'mjpython' if platform.system() == 'Darwin' else 'python'
            
            process = subprocess.Popen(
                ['conda', 'run', '-n', 'robocasa', python_interpreter, python_script_path, layout_path, '--style_id', style_id],  # 添加style_id参数
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
            style_id = str(context.scene.check_style_id)  # 使用check_style_id而不是style_id

            # 根据操作系统选择Python解释器
            python_interpreter = 'mjpython' if platform.system() == 'Darwin' else 'python'
            
            process = subprocess.Popen(
                ['conda', 'run', '-n', 'robocasa', python_interpreter, python_script_path, layout_path, '--demo', '--style_id', style_id],  # 添加style_id参数
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



