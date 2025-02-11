import bpy
import subprocess
import os
import platform  # 添加platform模块

# def find_conda_path():
#     """Try to find the conda executable in common locations."""
#     conda_paths = [
#         os.path.expanduser("~/miniconda3/bin/conda"),  # Linux/MacOS Miniconda
#         os.path.expanduser("~/anaconda3/bin/conda"),   # Linux/MacOS Anaconda
#         os.path.expanduser(r"~/miniconda3/Scripts/conda.exe"),  # Windows Miniconda
#         os.path.expanduser(r"~/anaconda3/Scripts/conda.exe"),   # Windows Anaconda
#     ]
    
#     for path in conda_paths:
#         if os.path.exists(path):
#             return path
#     return None


def find_conda_path():
    """Try to find the conda executable in common locations."""
    if platform.system() == "Darwin":  # macOS
        conda_paths = [
            "/opt/homebrew/anaconda3/bin/conda",
            "/usr/local/anaconda3/bin/conda",
            "/opt/anaconda3/bin/conda",
            os.path.expanduser("~/anaconda3/bin/conda"),
            os.path.expanduser("~/opt/anaconda3/bin/conda"),
            "/opt/homebrew/miniconda3/bin/conda",
            "/usr/local/miniconda3/bin/conda",
            os.path.expanduser("~/miniconda3/bin/conda"),
        ]
    elif platform.system() == "Windows":
        conda_paths = [
            r"C:\ProgramData\Anaconda3\Scripts\conda.exe",
            r"C:\ProgramData\miniconda3\Scripts\conda.exe",
            os.path.expanduser(r"~\Anaconda3\Scripts\conda.exe"),
            os.path.expanduser(r"~\miniconda3\Scripts\conda.exe"),
        ]
    else:  # Linux
        conda_paths = [
            "/usr/bin/conda",
            "/usr/local/bin/conda",
            os.path.expanduser("~/anaconda3/bin/conda"),
            os.path.expanduser("~/miniconda3/bin/conda"),
        ]
    
    # 尝试从环境变量中获取conda路径
    if "CONDA_EXE" in os.environ:
        conda_paths.insert(0, os.environ["CONDA_EXE"])
    
    # 尝试从which命令获取conda路径（仅在Unix系统）
    if platform.system() != "Windows":
        try:
            conda_path = subprocess.check_output(["which", "conda"]).decode().strip()
            conda_paths.insert(0, conda_path)
        except:
            pass
    
    for path in conda_paths:
        if os.path.exists(path):
            return path
            
    # 如果找不到conda，尝试从PATH中查找
    try:
        if platform.system() == "Windows":
            conda_path = subprocess.check_output(["where", "conda"], shell=True).decode().strip().split('\n')[0]
        else:
            conda_path = subprocess.check_output(["which", "conda"]).decode().strip()
        if os.path.exists(conda_path):
            return conda_path
    except:
        pass
    
    return None

def get_python_interpreter():
    """根据操作系统返回合适的Python解释器"""
    if platform.system() == "Darwin":  # macOS
        return "mjpython"
    else:  # Windows 和 Linux
        return "python"

def get_latest_yaml(blend_path):
    """获取同名文件夹下最新的yaml文件"""
    if not blend_path:
        return None
    
    # 获取blend文件所在目录和文件名（不含扩展名）
    blend_dir = os.path.dirname(blend_path)
    blend_name = os.path.splitext(os.path.basename(blend_path))[0]
    
    # 构建同名文件夹路径
    yaml_dir = os.path.join(blend_dir, blend_name)
    
    if not os.path.exists(yaml_dir):
        return None
    
    # 获取所有yaml文件
    yaml_files = [f for f in os.listdir(yaml_dir) 
                 if f.endswith(('.yaml', '.yml'))]
    
    if not yaml_files:
        return None
    
    # 按修改时间排序，返回最新的
    latest_yaml = max(yaml_files,
                     key=lambda f: os.path.getmtime(os.path.join(yaml_dir, f)))
    return os.path.join(yaml_dir, latest_yaml)

class FLOORPLAN_OT_check(bpy.types.Operator):
    """Check the scene data"""
    bl_idname = "floorplan.check"
    bl_label = "Check"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            python_script_path = os.path.join(current_dir, 'core', 'check.py')
            
            # 使用选择的yaml文件路径
            layout_path = context.scene.yaml_file_path
            if not layout_path:
                self.report({'ERROR'}, "请选择YAML文件")
                return {'CANCELLED'}
              
            style_id = int(context.scene.check_style_id)

            # 获取conda路径
            conda_path = find_conda_path()
            if not conda_path:
                self.report({'ERROR'}, "未找到Conda路径, 请确保Conda已安装")
                return {'CANCELLED'}

            # 获取Python解释器
            python_interpreter = get_python_interpreter()

            # 运行检查命令
            process = subprocess.Popen(
                [conda_path, 'run', '-n', 'robocasa', python_interpreter, python_script_path, 
                 layout_path, '--check', '--style_id', str(style_id)],
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
            
            # 获取yaml文件名
            yaml_filename = context.scene.yaml_file_path
            if not yaml_filename:
                self.report({'ERROR'}, "请选择YAML文件")
                return {'CANCELLED'}
            
            # 获取完整路径
            blend_dir = os.path.dirname(bpy.data.filepath)
            blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
            yaml_dir = os.path.join(blend_dir, blend_name)
            layout_path = os.path.join(yaml_dir, yaml_filename)
            
            print(f"Debug info:")
            print(f"Current dir: {current_dir}")
            print(f"Python script path: {python_script_path}")
            print(f"YAML filename: {yaml_filename}")
            print(f"Layout path: {layout_path}")
            
            if not os.path.exists(layout_path):
                self.report({'ERROR'}, f"找不到YAML文件: {layout_path}")
                return {'CANCELLED'}
            
            style_id = int(context.scene.check_style_id)
            
            # 获取conda路径
            conda_path = find_conda_path()
            if not conda_path:
                self.report({'ERROR'}, "未找到Conda路径，请确保Conda已安装")
                return {'CANCELLED'}

            # 获取Python解释器
            python_interpreter = get_python_interpreter()
            
            # 构建完整命令
            cmd = [
                conda_path, 
                'run', 
                '-n', 
                'robocasa', 
                python_interpreter, 
                python_script_path,
                layout_path,
                '--demo',
                '--style_id',
                str(style_id)
            ]
            
            print(f"Executing command: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            stdout, stderr = process.communicate()
            print(f"Process stdout: {stdout}")
            print(f"Process stderr: {stderr}")
            
            if process.returncode != 0:
                self.report({'ERROR'}, f"执行失败: {stderr}")
                return {'CANCELLED'}
            
            self.report({'INFO'}, "执行成功")
            return {'FINISHED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"执行失败: {str(e)}")
            import traceback
            print(f"Error traceback: {traceback.format_exc()}")
            return {'CANCELLED'}
