#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试配置管理模块
演示如何使用ConfigManager加载和管理YAML配置
"""

import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import (ConfigManager, global_config, 
                   load_config, get_config, set_config, 
                   save_config, get_all_config)

def test_config_manager():
    """测试配置管理类"""
    print("=== 测试配置管理模块 ===")
    
    # 使用全局配置实例
    print("\n1. 使用全局配置实例:")
    print(f"服务器地址: {get_config('server.host')}")
    print(f"服务器端口: {get_config('server.port')}")
    print(f"GitHub API地址: {get_config('github.api_url')}")
    print(f"界面语言: {get_config('ui.language')}")
    print(f"允许的文件扩展名: {get_config('storage.allowed_extensions')}")
    
    # 测试默认值
    print("\n2. 测试默认值:")
    print(f"不存在的配置: {get_config('non.existent.key', '默认值')}")
    
    # 测试修改配置
    print("\n3. 测试修改配置:")
    set_config('server.debug', False)
    print(f"修改后调试模式: {get_config('server.debug')}")
    
    # 测试添加新配置
    print("\n4. 测试添加新配置:")
    set_config('new_section.new_key', '新值')
    print(f"新添加的配置: {get_config('new_section.new_key')}")
    
    # 测试获取所有配置
    print("\n5. 测试获取所有配置:")
    all_config = get_all_config()
    print(f"配置总数: {len(all_config.keys())}")
    print(f"配置部分: {list(all_config.keys())}")
    
    # 测试保存配置
    print("\n6. 测试保存配置:")
    # 注意：这里只是演示，实际运行时会修改配置文件
    # save_config()
    print("配置保存功能已准备就绪")
    
    # 测试创建新的配置管理器实例
    print("\n7. 测试创建新的配置管理器实例:")
    custom_config = ConfigManager()
    print(f"自定义配置实例 - 服务器地址: {custom_config.get('server.host')}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_config_manager()
