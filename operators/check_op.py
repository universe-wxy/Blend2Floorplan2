import bpy
import subprocess
import os

def find_conda_path():
    """Try to find the conda executable in common locations."""
    conda_paths = [
        os.path.expanduser("~/miniconda3/bin/conda"),  # Linux/MacOS Miniconda
        os.path.expanduser("~/anaconda3/bin/conda"),   # Linux/MacOS Anaconda
        os.path.expanduser(r"~/miniconda3/Scripts/conda.exe"),  # Windows Miniconda
        os.path.expanduser(r"~/anaconda3/Scripts/conda.exe"),   # Windows Anaconda
    ]
    
    for path in conda_paths:
        if os.path.exists(path):
            return path
    return None

class FLOORPLAN_OT_check(bpy.types.Operator):
    """Check the scene data"""
    bl_idname = "floorplan.check"
    bl_label = "Check"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            python_script_path = os.path.join(current_dir, 'core', 'check.py')
            
            layout_path = bpy.context.scene.get('exported_yaml')
            if not layout_path:
                self.report({'ERROR'}, "请先导出YAML文件")
                return {'CANCELLED'}

            # 获取conda路径
            conda_path = find_conda_path()
            if not conda_path:
                self.report({'ERROR'}, "未找到Conda路径，请确保Conda已安装")
                return {'CANCELLED'}

            # 运行检查命令
            process = subprocess.Popen(
                [conda_path, 'run', '-n', 'robocasa', 'python', python_script_path, layout_path, '--check'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()
            
            # 解析输出
            if "检测到问题" in stdout:
                # 找出所有检测到的问题
                issues = [line for line in stdout.split('\n') if "检测到问题" in line]
                # 在Blender界面显示问题
                def draw(self, context):
                    layout = self.layout
                    for issue in issues:
                        layout.label(text=issue)
                
                bpy.context.window_manager.popup_menu(draw, title="检查结果", icon='ERROR')
                self.report({'WARNING'}, "发现问题，请查看详细信息")
            else:
                self.report({'INFO'}, "检查通过，未发现问题")
            
            return {'FINISHED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"检查失败: {str(e)}")
            return {'CANCELLED'}
    
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

            # 获取conda路径
            conda_path = find_conda_path()
            if not conda_path:
                self.report({'ERROR'}, "未找到Conda路径，请确保Conda已安装")
                return {'CANCELLED'}

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