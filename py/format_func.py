import json


def format_size(size_bytes):
    """
    将字节大小格式化为人类可读的形式
    
    Args:
        size_bytes (int): 字节大小
    
    Returns:
        str: 格式化后的大小字符串
    """
    if size_bytes is None or size_bytes <= 0: return "0 Bytes"
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {units[i]}"


def format_dir(data):
    """
    将数据格式化为JSON字符串

    Args:
        data (any): 要格式化的数据

    Returns:
        str: 格式化后的JSON字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
