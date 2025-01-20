import os
import subprocess

def get_style_path(style_id):
    """
    Get the path to the style file based on style_id
    """
    style_id = int(style_id)
    
    # 运行conda环境中的Python脚本来获取robocasa路径
    process = subprocess.Popen(
        ['conda', 'run', '-n', 'robocasa', 'mjpython', '-c', 
         'import robocasa; print(robocasa.models.assets_root)'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise ValueError(f"Failed to get robocasa path: {stderr.decode()}")
        
    assets_root = stdout.decode().strip()
    style_filename = f"style_{style_id}.yaml"
    style_path = os.path.join(assets_root, "styles", style_filename)
    
    if not os.path.exists(style_path):
        raise ValueError(f"Style file not found: {style_path}")
    
    return style_path