import webview
import os
import json
from datetime import datetime
from pathlib import Path

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

if __name__ == '__main__':
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
    window = webview.create_window(
        '文件浏览器',
        url="../demo/index.html",
        js_api=api,
        width=1000,
        height=700,
        resizable=True
    )

    # 启动应用
    webview.start(debug=True)
