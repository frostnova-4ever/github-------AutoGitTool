import webview
import os
import json
from datetime import datetime
from pathlib import Path

# 全局窗口变量
global_window = None

def get_directory_contents(path):
    """
    获取指定路径下的所有文件和文件夹信息

    Args:
        path (str): 目录路径

    Returns:
        list: 包含文件/文件夹信息的列表
    """
    if not os.path.exists(path):
        return {"error": "路径不存在"}

    if not os.path.isdir(path):
        return {"error": "指定路径不是目录"}

    contents = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            stat_info = os.stat(item_path)

            # 获取文件大小
            if os.path.isfile(item_path):
                size = stat_info.st_size
                is_file = True
            else:
                size = get_directory_size(item_path)
                is_file = False

            # 获取修改时间
            mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            contents.append({
                "name": item,
                "path": item_path,
                "size": size,
                "modified_time": mtime,
                "is_file": is_file
            })
    except PermissionError:
        return {"error": "权限不足，无法访问该目录"}

    return contents

def get_directory_size(path):
    """
    递归计算目录大小

    Args:
        path (str): 目录路径

    Returns:
        int: 目录总大小(字节)
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except PermissionError:
        pass  # 忽略权限错误
    return total_size

def format_size(size_bytes):
    """
    将字节大小格式化为人类可读的格式

    Args:
        size_bytes (int): 字节大小

    Returns:
        str: 格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"

class Api:
    def get_files(self, path):
        """
        API方法：获取指定路径下的文件列表

        Args:
            path (str): 目录路径

        Returns:
            dict: 文件列表信息
        """
        contents = get_directory_contents(path)

        # 如果返回的是错误信息，直接返回
        if isinstance(contents, dict) and "error" in contents:
            return contents

        # 格式化大小信息
        for item in contents:
            if item['is_file']:
                item['size_formatted'] = format_size(item['size'])
            else:
                item['size_formatted'] = format_size(item['size']) + " (目录)"

        return {
            "path": path,
            "contents": contents
        }
    
    def read(self,file_path):
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return "文件不存在"

            # 检查是否为文件
            if not os.path.isfile(file_path):
                return "指定路径不是文件"

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            return content
        except Exception as e:
            return  f"读取文件失败: {str(e)}"

    def list_paths(self):
        """
        API方法：列出系统中的常用路径
        
        Returns:
            dict: 包含常用路径的列表
        """
        paths = []
        
        try:
            # 添加当前目录
            current_dir = os.getcwd()
            paths.append({"name": "当前目录", "path": current_dir, "type": "directory"})
            
            # 添加用户主目录
            home_dir = os.path.expanduser("~")
            paths.append({"name": "用户主目录", "path": home_dir, "type": "directory"})
            
            # 使用pywin32获取Windows特殊文件夹路径
            if os.name == 'nt':
                try:
                    import win32com.shell
                    from win32com.shell import shell, shellcon
                    
                    # 获取桌面目录
                    desktop_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
                    if os.path.exists(desktop_dir):
                        paths.append({"name": "桌面", "path": desktop_dir, "type": "directory"})
                    
                    # 获取文档目录
                    docs_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
                    if os.path.exists(docs_dir):
                        paths.append({"name": "文档", "path": docs_dir, "type": "directory"})
                    
                    # 获取下载目录
                    downloads_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_DOWNLOADS, None, 0)
                    if os.path.exists(downloads_dir):
                        paths.append({"name": "下载", "path": downloads_dir, "type": "directory"})
                    
                    # 获取音乐目录
                    music_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, None, 0)
                    if os.path.exists(music_dir):
                        paths.append({"name": "音乐", "path": music_dir, "type": "directory"})
                    
                    # 获取图片目录
                    pictures_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)
                    if os.path.exists(pictures_dir):
                        paths.append({"name": "图片", "path": pictures_dir, "type": "directory"})
                    
                    # 获取视频目录
                    videos_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_MYVIDEO, None, 0)
                    if os.path.exists(videos_dir):
                        paths.append({"name": "视频", "path": videos_dir, "type": "directory"})
                    
                    # 获取程序目录
                    programs_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0)
                    if os.path.exists(programs_dir):
                        paths.append({"name": "程序", "path": programs_dir, "type": "directory"})
                    
                    # 获取系统目录
                    system_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_SYSTEM, None, 0)
                    if os.path.exists(system_dir):
                        paths.append({"name": "系统", "path": system_dir, "type": "directory"})
                    
                except Exception as e:
                    # 如果pywin32调用失败，回退到传统方法
                    print(f"pywin32调用失败: {str(e)}")
                    # 使用传统方法获取桌面目录
                    desktop_dir = os.path.join(home_dir, "Desktop")
                    if os.path.exists(desktop_dir):
                        paths.append({"name": "桌面", "path": desktop_dir, "type": "directory"})
                    
                    # 使用传统方法获取文档目录
                    docs_dir = os.path.join(home_dir, "Documents")
                    if os.path.exists(docs_dir):
                        paths.append({"name": "文档", "path": docs_dir, "type": "directory"})
                    
                    # 使用传统方法获取下载目录
                    downloads_dir = os.path.join(home_dir, "Downloads")
                    if os.path.exists(downloads_dir):
                        paths.append({"name": "下载", "path": downloads_dir, "type": "directory"})
            
            # 添加本地磁盘根目录（Windows系统）
            if os.name == 'nt':
                # 使用pywin32获取磁盘驱动器
                try:
                    import win32api
                    drives = win32api.GetLogicalDriveStrings()
                    drives = drives.split('\\')[:-1]
                    for drive in drives:
                        if os.path.exists(drive):
                            paths.append({"name": f"磁盘 {drive}", "path": drive, "type": "drive"})
                except Exception as e:
                    # 如果pywin32调用失败，回退到传统方法
                    print(f"获取磁盘驱动器失败: {str(e)}")
                    import string
                    for letter in string.ascii_uppercase:
                        drive = letter + ":\\"
                        if os.path.exists(drive):
                            paths.append({"name": f"磁盘 {drive}", "path": drive, "type": "drive"})
            
            return {"paths": paths}
            
        except Exception as e:
            return {"error": f"获取路径列表失败: {str(e)}", "paths": paths}
    
    def open_folder_dialog(self):
        """
        API方法：打开文件夹选择对话框
        
        Returns:
            str: 选中的文件夹路径，如果用户取消则返回None
        """
        global global_window
        try:
            if global_window:
                # 使用新的FileDialog.FOLDER方式
                result = global_window.create_file_dialog(
                    dialog_type=webview.FileDialog.FOLDER,
                    allow_multiple=False
                )
                
                if result and len(result) > 0:
                    return result[0]
            return None
        except Exception as e:
            print(f"打开文件夹对话框失败: {str(e)}")
            return None
    
    def is_git_repository(self, path):
        """
        API方法：检查指定路径是否是Git仓库（是否包含.git目录）
        
        Args:
            path (str): 要检查的目录路径
            
        Returns:
            bool: 如果是Git仓库返回True，否则返回False
        """
        if not os.path.exists(path):
            return False
        if not os.path.isdir(path):
            return False
        
        git_dir = os.path.join(path, '.git')
        return os.path.exists(git_dir) and os.path.isdir(git_dir)
    
    def execute_command(self, command, cwd=None):
        """
        API方法：执行系统命令
        
        Args:
            command (str): 要执行的命令字符串
            cwd (str): 命令执行的当前工作目录
            
        Returns:
            dict: 包含命令输出、错误和新工作目录的结果
        """
        import subprocess
        import shlex
        
        try:
            # 如果没有指定工作目录，使用当前目录
            if not cwd:
                cwd = os.getcwd()
            
            # 处理cd命令的特殊情况
            if command.strip().lower().startswith('cd '):
                new_dir = command.strip()[3:]
                # 处理相对路径
                if new_dir.startswith('.') or not os.path.isabs(new_dir):
                    new_dir = os.path.join(cwd, new_dir)
                # 标准化路径
                new_dir = os.path.normpath(new_dir)
                # 检查路径是否存在
                if os.path.exists(new_dir) and os.path.isdir(new_dir):
                    return {
                        "output": f"切换到目录: {new_dir}",
                        "error": "",
                        "cwd": new_dir
                    }
                else:
                    return {
                        "output": "",
                        "error": f"目录不存在: {new_dir}",
                        "cwd": cwd
                    }
            
            # 执行其他命令
            # 根据操作系统选择shell
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(
                    command,
                    cwd=cwd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:  # Linux/macOS
                process = subprocess.Popen(
                    shlex.split(command),
                    cwd=cwd,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            # 获取命令输出和错误
            stdout, stderr = process.communicate()
            
            return {
                "output": stdout,
                "error": stderr,
                "cwd": cwd
            }
            
        except Exception as e:
            return {
                "output": "",
                "error": f"执行命令失败: {str(e)}",
                "cwd": cwd
            }

def on_window_loaded():
    """
    窗口加载完成后的回调函数
    """
    global global_window
    print("窗口已加载完成")

if __name__ == '__main__':
    try:
        # 创建API实例
        api = Api()

        # 使用pathlib处理路径
        current_script = Path(__file__).resolve()
        html_path = current_script.parent.parent / "demo" / "index.html"

        # 检查文件是否存在
        if not html_path.exists():
            print(f"HTML文件不存在: {html_path}")
            exit(1)

        # 直接使用文件路径而不是读取内容
        global_window = webview.create_window(
            '文件浏览器',
            url="../demo/index.html",
            js_api=api,
            width=1000,
            height=700,
            resizable=True
        )

        # 启动应用
        webview.start(on_window_loaded, debug=True)
    except Exception as e:
        print(f"启动应用失败: {str(e)}")
