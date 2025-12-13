#!/usr/bin/env python3
"""
YAML配置读取工具模块
包含YAML配置的加载和读取功能
"""

import os
import yaml
from pathlib import Path

# 全局变量：缓存的配置数据
_cached_config = None
# 全局变量：配置是否需要重新加载的标志
_config_needs_reload = True

def load_yaml_config(config_path=None):
    """
    加载YAML配置文件
    
    参数:
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        dict: 加载的配置字典
    """
    global _cached_config, _config_needs_reload
    
    # 如果不需要重新加载且已有缓存，则直接返回缓存
    if not _config_needs_reload and _cached_config is not None:
        return _cached_config
    
    if config_path is None:
        # 默认配置文件路径
        current_dir = Path(__file__).parent.parent.parent  # 上上级目录
        config_path = os.path.join(current_dir, 'data', 'settings.yaml')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            if config is None:
                config = {}
        
        # 更新缓存并重置标志
        _cached_config = config
        _config_needs_reload = False
        return config
    except FileNotFoundError:
        return {}
    except yaml.YAMLError:
        return {}
    except Exception:
        return {}


def _load_settings():
    """
    加载settings.yaml文件（内部使用）
    
    返回:
        dict: 加载的配置字典，确保包含userSettings键以保持向后兼容
    """
    config = load_yaml_config()
    # 确保返回的字典包含userSettings键以保持向后兼容
    if "userSettings" not in config:
        config["userSettings"] = {}
    return config


def set_config_needs_reload(needs_reload=True):
    """
    设置配置是否需要重新加载
    
    参数:
        needs_reload (bool): True表示需要重新加载配置，False表示不需要
    """
    global _config_needs_reload, _cached_all_configs
    _config_needs_reload = needs_reload
    
    # 如果需要重新加载，清除所有配置的缓存
    if needs_reload:
        _cached_all_configs = None


def get_git_config():
    """
    获取Git相关配置
    
    返回:
        dict: Git配置字典，包含以下键:
            - repo: 默认仓库
            - name: 默认用户名
    """
    settings = _load_settings()
    user_settings = settings.get("userSettings", {})
    
    git_config = {
        "repo": user_settings.get("github_repo", ""),
        "name": user_settings.get("name", "")
    }
    return git_config


def get_path_config():
    """
    获取路径相关配置
    
    返回:
        dict: 路径配置字典，包含以下键:
            - path: 默认路径
            - allowed_extensions: 允许的文件扩展名列表
    """
    settings = _load_settings()
    user_settings = settings.get("userSettings", {})
    
    path_config = {
        "path": user_settings.get("path", ""),
        "allowed_extensions": user_settings.get("allowed_extensions", [".txt", ".md", ".json", ".yaml", ".yml"])
    }
    return path_config


def get_ui_config():
    """
    获取界面相关配置
    
    返回:
        dict: 界面配置字典，包含以下键:
            - theme: 主题名称
            - language: 界面语言
            - show_hidden_files: 是否显示隐藏文件
            - default_view: 默认文件视图（list/grid）
    """
    settings = _load_settings()
    user_settings = settings.get("userSettings", {})
    
    ui_config = {
        "theme": user_settings.get("theme", "default"),
        "language": user_settings.get("language", "zh-CN"),
        "show_hidden_files": user_settings.get("show_hidden_files", False),
        "default_view": user_settings.get("default_view", "list")
    }
    return ui_config


# 全局变量：缓存的所有配置
_cached_all_configs = None

def get_all_configs():
    """
    获取所有配置
    
    返回:
        dict: 所有配置的字典，包含以下键:
            - git: Git配置
            - path: 路径配置
            - ui: 界面配置
    """
    global _cached_all_configs, _config_needs_reload
    
    # 如果配置需要重新加载或缓存不存在，则重新生成配置
    if _config_needs_reload or _cached_all_configs is None:
        _cached_all_configs = {
            "git": get_git_config(),
            "path": get_path_config(),
            "ui": get_ui_config()
        }
    
    return _cached_all_configs


def get_yaml_str_value(path, config_path=None, default=""):
    """
    通过字符串路径获取YAML配置的字符串值
    
    参数:
        path (str): 配置路径，使用点表示法，如 "userSettings.git.repo"
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
        default (str, optional): 路径不存在或类型不匹配时返回的默认字符串值
    
    返回:
        str: 路径对应的字符串配置值，如果路径不存在或类型不匹配则返回default
    """
    # 加载YAML配置
    config = load_yaml_config(config_path)
    
    # 解析路径
    keys = path.split('.')
    value = config
    
    # 遍历路径中的每个键
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    # 确保返回字符串类型
    return str(value) if value is not None else default


def get_yaml_list_value(path, config_path=None, default=None):
    """
    通过字符串路径获取YAML配置的列表值
    
    参数:
        path (str): 配置路径，使用点表示法，如 "userSettings.allowed_extensions"
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
        default (list, optional): 路径不存在或类型不匹配时返回的默认列表值
    
    返回:
        list: 路径对应的列表配置值，如果路径不存在或类型不匹配则返回default（默认空列表）
    """
    if default is None:
        default = []
    
    # 加载YAML配置
    config = load_yaml_config(config_path)
    
    # 解析路径
    keys = path.split('.')
    value = config
    
    # 遍历路径中的每个键
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    # 确保返回列表类型
    return value if isinstance(value, list) else default





# 当直接运行此模块时，打印配置信息
if __name__ == "__main__":
    print("=== YAML配置读取测试 ===")
    
    print("\n1. Git配置:")
    git_config = get_git_config()
    for key, value in git_config.items():
        print(f"   {key}: {value}")
    
    print("\n2. 路径配置:")
    path_config = get_path_config()
    for key, value in path_config.items():
        print(f"   {key}: {value}")
    
    print("\n3. 界面配置:")
    ui_config = get_ui_config()
    for key, value in ui_config.items():
        print(f"   {key}: {value}")

    
    print("\n4. 所有配置:")
    all_configs = get_all_configs()
    for section, config in all_configs.items():
        print(f"   {section}: {config}")
    
    print("\n5. 通过路径获取字符串配置值:")
    repo = get_yaml_str_value("userSettings.github_repo")
    print(f"   userSettings.github_repo: {repo} (类型: {type(repo).__name__})")
    
    theme = get_yaml_str_value("userSettings.theme")
    print(f"   userSettings.theme: {theme} (类型: {type(theme).__name__})")
    
    non_existent = get_yaml_str_value("userSettings.non_existent", default="不存在的键")
    print(f"   userSettings.non_existent (默认值): {non_existent} (类型: {type(non_existent).__name__})")
    
    print("\n6. 通过路径获取列表配置值:")
    extensions = get_yaml_list_value("userSettings.allowed_extensions")
    print(f"   userSettings.allowed_extensions: {extensions} (类型: {type(extensions).__name__})")
    
    empty_list = get_yaml_list_value("userSettings.non_existent_list")
    print(f"   userSettings.non_existent_list (默认值): {empty_list} (类型: {type(empty_list).__name__})")
    
    custom_default = get_yaml_list_value("userSettings.non_existent_list", default=[".py", ".js"])
    print(f"   userSettings.non_existent_list (自定义默认值): {custom_default} (类型: {type(custom_default).__name__})")
