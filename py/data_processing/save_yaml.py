#!/usr/bin/env python3
"""
YAML配置保存工具模块
专门用于保存YAML配置文件
"""

import os
import yaml
from pathlib import Path

# 从get_yaml模块导入设置重新加载标志的函数
from .get_yaml import set_config_needs_reload

def save_yaml_config(config, config_path=None):
    """
    保存YAML配置文件
    
    参数:
        config (dict): 要保存的配置字典
        config_path (str, optional): YAML配置文件的路径。如果为None，则使用默认路径
    
    返回:
        bool: 保存是否成功
    """
    if config_path is None:
        # 默认配置文件路径
        current_dir = Path(__file__).parent.parent.parent  # 上上级目录
        config_path = os.path.join(current_dir, 'data', 'settings.yaml')
    
    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True, indent=2)
        # 设置配置需要重新加载的标志
        set_config_needs_reload()
        return True
    except yaml.YAMLError:
        return False
    except Exception:
        return False