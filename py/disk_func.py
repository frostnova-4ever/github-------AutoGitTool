import os
import sys
import json
from datetime import datetime
from response_utils import create_response_dict
import format_func


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
    
def get_directory_contents(path):
    """
    获取指定路径下的所有文件和文件夹信息

    Args:
        path (str): 目录路径

    Returns:
        list: 包含文件/文件夹信息的列表
    """
    if not os.path.exists(path):
        return create_response_dict(success=False, error="路径不存在")
    if not os.path.isdir(path):
        return create_response_dict(success=False, error="指定路径不是目录")

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

            contents.append({"name": item,"path": item_path,"size": size,"modified_time": mtime,"is_file": is_file })
    except PermissionError:
        return create_response_dict(success=False, error="权限不足，无法访问该目录")
    return create_response_dict(success=True, contents=contents)



def read_file(file_path):
    """
    读取文件内容

    Args:
        file_path (str): 文件路径

    Returns:
        dict: 包含文件内容或错误信息的响应字典
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return create_response_dict(success=False, error="文件不存在")

        # 检查是否为文件
        if not os.path.isfile(file_path):
            return create_response_dict(success=False, error="指定路径不是文件")
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return create_response_dict(success=True, content=content)
    except Exception as e:
        return create_response_dict(success=False, error=f"读取文件失败: {str(e)}")

def is_git_repository(path):
    """
    检查指定路径是否是Git仓库（是否包含.git目录）
    
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

def get_files(path):
    """
    获取指定路径下的文件列表
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
    for item in contents['contents']:
        if item['is_file']:
            item['size_formatted'] = format_func.format_size(item['size'])
        else:
            item['size_formatted'] = format_func.format_size(item['size']) + " (目录)"

    return {
        "success": True,
        "path": path,
        "contents": contents['contents']
    }


def list_common_paths():
    """
    列出系统中的常用路径
    
    Returns:
        dict: 包含常用路径的响应字典
    """
    paths = []
    try:
        # 添加当前目录
        current_dir = os.getcwd()
        paths.append({"name": "当前目录", "path": current_dir, "type": "directory"})
        
        home_dir = os.path.expanduser("~")
        paths.append({"name": "用户主目录", "path": home_dir, "type": "directory"})
        
        if os.name == 'nt':
            # 添加Windows特殊文件夹路径
            try:
                import ctypes
                from ctypes import wintypes, windll
                
                # 定义常量
                CSIDL_DESKTOP = 0
                CSIDL_DOCUMENTS = 5
                CSIDL_DOWNLOADS = 16
                CSIDL_MUSIC = 13
                CSIDL_PICTURES = 39
                CSIDL_VIDEOS = 14
                CSIDL_PROGRAM_FILES = 38
                CSIDL_PROGRAM_FILES_X86 = 42
                CSIDL_PROGRAM_DATA = 35
                CSIDL_APPDATA = 26
                CSIDL_LOCAL_APPDATA = 28
                
                # 创建路径映射
                special_folders = [
                    (CSIDL_DESKTOP, "桌面", home_dir),
                    (CSIDL_DOCUMENTS, "文档", home_dir),
                    (CSIDL_DOWNLOADS, "下载", home_dir),
                    (CSIDL_MUSIC, "音乐", home_dir),
                    (CSIDL_PICTURES, "图片", home_dir),
                    (CSIDL_VIDEOS, "视频", home_dir),
                    (CSIDL_PROGRAM_FILES, "Program Files", None),
                    (CSIDL_PROGRAM_FILES_X86, "Program Files (x86)", None),
                    (CSIDL_PROGRAM_DATA, "ProgramData", None),
                    (CSIDL_APPDATA, "AppData\Roaming", None),
                    (CSIDL_LOCAL_APPDATA, "AppData\Local", None),
                ]
                
                # 获取特殊文件夹路径
                for csidl, display_name, parent_path in special_folders:
                    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                    if windll.shell32.SHGetFolderPathW(None, csidl, None, 0, buf) == 0:
                        path = buf.value
                        # 如果指定了父路径，且路径包含父路径，则创建相对路径显示
                        if parent_path and path.startswith(parent_path):
                            display_path = path.replace(parent_path, "~")
                        else:
                            display_path = path
                        paths.append({"name": display_name,"path": path,"display_path": display_path,"type": "directory"})
            except Exception as e:
                print(f"添加Windows特殊文件夹失败: {str(e)}")
            
            # 添加Windows磁盘驱动器
            try:
                import string
                for letter in string.ascii_uppercase:
                    drive_path = f"{letter}:\\"
                    if os.path.exists(drive_path):
                        # 尝试获取驱动器卷标
                        try:
                            volume_name = windll.kernel32.GetVolumeInformationW(
                                ctypes.c_wchar_p(drive_path),
                                None, 0, None, None, None, None, 0
                            )
                            volume_name = ctypes.create_unicode_buffer(256)
                            windll.kernel32.GetVolumeInformationW(
                                ctypes.c_wchar_p(drive_path),
                                volume_name, ctypes.sizeof(volume_name),
                                None, None, None, None, 0
                            )
                            display_name = f"{volume_name.value} ({letter}:)" if volume_name.value else f"本地磁盘 ({letter}:)"
                        except:
                            display_name = f"本地磁盘 ({letter}:)"
                        
                        paths.append({"name": display_name,"path": drive_path,"type": "drive" })
            except Exception as e:
                print(f"添加Windows磁盘驱动器失败: {str(e)}")
    
        # 添加类Unix系统常见路径
        else:
            try:
                # 常见挂载点
                common_mounts = ["/", "/home", "/usr", "/var", "/tmp", "/opt", "/mnt", "/media"]
                for mount in common_mounts:
                    if os.path.exists(mount) and os.path.isdir(mount):
                        paths.append({"name": mount,"path": mount,"type": "directory"})
                
                # 添加挂载的媒体设备
                media_dir = "/media"
                if os.path.exists(media_dir):
                    for user_dir in os.listdir(media_dir):
                        user_media_path = os.path.join(media_dir, user_dir)
                        if os.path.isdir(user_media_path):
                            paths.append({
                                "name": f"媒体/{user_dir}",
                                "path": user_media_path,
                                "type": "directory"
                            })
                
                # 添加常用符号链接
                if os.path.exists("/bin"):
                    paths.append({"name": "bin", "path": "/bin", "type": "directory"})
                if os.path.exists("/sbin"):
                    paths.append({"name": "sbin", "path": "/sbin", "type": "directory"})
                if os.path.exists("/etc"):
                    paths.append({"name": "etc", "path": "/etc", "type": "directory"})
            except Exception as e:
                print(f"添加类Unix系统路径失败: {str(e)}")
    except Exception as e:
        return create_response_dict(success=False, error=f"列出常用路径失败: {str(e)}")
    return create_response_dict(success=True, paths=paths)