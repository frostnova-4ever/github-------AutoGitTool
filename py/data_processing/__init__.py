#!/usr/bin/env python3
"""
data_processing模块的初始化文件
用于导出模块的核心功能
"""

# 从content模块导入内容管理功能
from .content import YAMLKeys

# 从get_yaml模块导入YAML读取功能
from .get_yaml import (
    load_yaml_config,
    get_git_config,
    get_path_config,
    get_ui_config,
    get_all_configs,
    get_yaml_str_value,
    get_yaml_list_value,
    set_config_needs_reload  # 新增函数：设置配置需要重新加载的标志
)

# 从save_yaml模块导入YAML保存功能
from .save_yaml import (
    save_yaml_config
)

# 从update_yaml模块导入配置更新功能
from .update_yaml import (
    update_yaml_config,
    update_git_config,
    update_path_config,
    update_ui_config,
    add_allowed_extension,
    remove_allowed_extension,
    update_configs
)

# 定义模块的公共接口
__all__ = [
    # content模块
    "YAMLKeys",
    
    # get_yaml模块
    "load_yaml_config",
    "get_git_config",
    "get_path_config",
    "get_ui_config",
    "get_all_configs",
    "get_yaml_str_value",
    "get_yaml_list_value",
    "set_config_needs_reload",  # 导出新增函数
    
    # save_yaml模块
    "save_yaml_config",
    
    # update_yaml模块
    "update_yaml_config",
    "update_git_config",
    "update_path_config",
    "update_ui_config",
    "add_allowed_extension",
    "remove_allowed_extension",
    "update_configs"
]
