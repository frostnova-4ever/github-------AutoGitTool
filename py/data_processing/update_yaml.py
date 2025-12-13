#!/usr/bin/env python3
"""
YAML配置更新工具模块
专门用于更新YAML配置文件中的信息
"""

import os
import yaml
from pathlib import Path

# 从get_yaml模块导入加载函数
from .get_yaml import load_yaml_config

# 从save_yaml模块导入保存函数
from .save_yaml import save_yaml_config





def update_yaml_config(key_path, value, config_path=None):
    """
    更新YAML配置文件中的特定键值
    
    参数:
        key_path (str): 配置键的路径，使用点分隔（如"userSettings.github_repo"）
        value: 要设置的值
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 更新是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 解析键路径
    keys = key_path.split('.')
    current = config
    
    # 导航到要更新的键的父节点
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # 更新值
    current[keys[-1]] = value
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def update_git_config(git_config, config_path=None):
    """
    更新Git相关配置
    
    参数:
        git_config (dict): 包含Git配置的字典，应包含以下键:
            - repo: 默认仓库
            - name: 默认用户名
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 更新是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 更新Git配置
    if "repo" in git_config:
        user_settings["github_repo"] = git_config["repo"]
    if "name" in git_config:
        user_settings["name"] = git_config["name"]
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def update_path_config(path_config, config_path=None):
    """
    更新路径相关配置
    
    参数:
        path_config (dict): 包含路径配置的字典，应包含以下键:
            - path: 默认路径
            - allowed_extensions: 允许的文件扩展名列表
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 更新是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 更新路径配置
    if "path" in path_config:
        user_settings["path"] = path_config["path"]
    if "allowed_extensions" in path_config:
        user_settings["allowed_extensions"] = path_config["allowed_extensions"]
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def update_ui_config(ui_config, config_path=None):
    """
    更新界面相关配置
    
    参数:
        ui_config (dict): 包含界面配置的字典，应包含以下键:
            - theme: 主题名称
            - language: 界面语言
            - show_hidden_files: 是否显示隐藏文件
            - default_view: 默认文件视图（list/grid）
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 更新是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 更新界面配置
    if "theme" in ui_config:
        user_settings["theme"] = ui_config["theme"]
    if "language" in ui_config:
        user_settings["language"] = ui_config["language"]
    if "show_hidden_files" in ui_config:
        user_settings["show_hidden_files"] = ui_config["show_hidden_files"]
    if "default_view" in ui_config:
        user_settings["default_view"] = ui_config["default_view"]
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def add_allowed_extension(extension, config_path=None):
    """
    向允许的文件扩展名列表中添加新的扩展名
    
    参数:
        extension (str): 要添加的文件扩展名（如".pdf"）
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 添加是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 确保allowed_extensions键存在
    if "allowed_extensions" not in user_settings:
        user_settings["allowed_extensions"] = []
    
    allowed_extensions = user_settings["allowed_extensions"]
    
    # 确保扩展名以点开头
    if not extension.startswith('.'):
        extension = f".{extension}"
    
    # 如果扩展名不存在，则添加
    if extension not in allowed_extensions:
        allowed_extensions.append(extension)
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def remove_allowed_extension(extension, config_path=None):
    """
    从允许的文件扩展名列表中移除指定的扩展名
    
    参数:
        extension (str): 要移除的文件扩展名（如".pdf"）
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 移除是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 确保allowed_extensions键存在
    if "allowed_extensions" not in user_settings:
        user_settings["allowed_extensions"] = []
        return True  # 扩展名列表不存在，视为成功
    
    allowed_extensions = user_settings["allowed_extensions"]
    
    # 确保扩展名以点开头
    if not extension.startswith('.'):
        extension = f".{extension}"
    
    # 如果扩展名存在，则移除
    if extension in allowed_extensions:
        allowed_extensions.remove(extension)
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


def update_configs(configs, config_path=None):
    """
    更新所有配置
    
    参数:
        configs (dict): 包含所有配置的字典，应包含以下键:
            - git: Git配置
            - path: 路径配置
            - ui: 界面配置
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 更新是否成功
    """
    # 加载配置
    config = load_yaml_config(config_path)
    
    # 确保userSettings键存在
    if "userSettings" not in config:
        config["userSettings"] = {}
    
    user_settings = config["userSettings"]
    
    # 更新Git配置
    if "git" in configs:
        git_config = configs["git"]
        if "repo" in git_config:
            user_settings["github_repo"] = git_config["repo"]
        if "name" in git_config:
            user_settings["name"] = git_config["name"]
    
    # 更新路径配置
    if "path" in configs:
        path_config = configs["path"]
        if "path" in path_config:
            user_settings["path"] = path_config["path"]
        if "allowed_extensions" in path_config:
            user_settings["allowed_extensions"] = path_config["allowed_extensions"]
    
    # 更新界面配置
    if "ui" in configs:
        ui_config = configs["ui"]
        if "theme" in ui_config:
            user_settings["theme"] = ui_config["theme"]
        if "language" in ui_config:
            user_settings["language"] = ui_config["language"]
        if "show_hidden_files" in ui_config:
            user_settings["show_hidden_files"] = ui_config["show_hidden_files"]
        if "default_view" in ui_config:
            user_settings["default_view"] = ui_config["default_view"]
    
    # 保存更新后的配置
    return save_yaml_config(config, config_path)


# 当直接运行此模块时，执行测试
if __name__ == "__main__":
    print("=== YAML配置更新模块测试 ===")
    
    # 测试更新特定键
    print("\n1. 测试更新特定键:")
    result = update_yaml_config("test_key.test_subkey", "test_value")
    print(f"   更新test_key.test_subkey: {'成功' if result else '失败'}")
    
    # 测试更新Git配置
    print("\n2. 测试更新Git配置:")
    result = update_git_config({"repo": "https://github.com/test/repo.git", "name": "test_user"})
    print(f"   更新Git配置: {'成功' if result else '失败'}")
    
    # 测试添加扩展名
    print("\n3. 测试添加扩展名:")
    result = add_allowed_extension(".pdf")
    print(f"   添加.pdf扩展名: {'成功' if result else '失败'}")
    
    print("\n所有测试完成!")