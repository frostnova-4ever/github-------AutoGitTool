#!/usr/bin/env python3
"""
测试YAML配置保存功能的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from py.data_processing import (
    get_git_config,
    get_path_config,
    get_ui_config,
    update_git_config,
    update_path_config,
    update_ui_config,
    add_allowed_extension,
    remove_allowed_extension,
    get_all_configs
)

def test_update_git_config():
    """测试更新Git配置"""
    print("=== 测试更新Git配置 ===")
    print("更新前的Git配置:", get_git_config())
    
    # 更新Git配置
    update_result = update_git_config({"repo": "https://github.com/test/repo.git", "name": "test_user"})
    print(f"更新结果: {'成功' if update_result else '失败'}")
    
    print("更新后的Git配置:", get_git_config())
    print()


def test_update_path_config():
    """测试更新路径配置"""
    print("=== 测试更新路径配置 ===")
    print("更新前的路径配置:", get_path_config())
    
    # 更新路径配置
    update_result = update_path_config({"path": "C:/test/path", "allowed_extensions": [".txt", ".md", ".pdf"]})
    print(f"更新结果: {'成功' if update_result else '失败'}")
    
    print("更新后的路径配置:", get_path_config())
    print()


def test_update_ui_config():
    """测试更新界面配置"""
    print("=== 测试更新界面配置 ===")
    print("更新前的界面配置:", get_ui_config())
    
    # 更新界面配置
    update_result = update_ui_config({"theme": "dark", "language": "en-US", "show_hidden_files": True})
    print(f"更新结果: {'成功' if update_result else '失败'}")
    
    print("更新后的界面配置:", get_ui_config())
    print()


def test_add_remove_extension():
    """测试添加和移除文件扩展名"""
    print("=== 测试添加和移除文件扩展名 ===")
    print("当前允许的扩展名:", get_path_config()["allowed_extensions"])
    
    # 添加扩展名
    add_result = add_allowed_extension(".docx")
    print(f"添加.docx扩展名: {'成功' if add_result else '失败'}")
    print("添加后的扩展名:", get_path_config()["allowed_extensions"])
    
    # 移除扩展名
    remove_result = remove_allowed_extension(".pdf")
    print(f"移除.pdf扩展名: {'成功' if remove_result else '失败'}")
    print("移除后的扩展名:", get_path_config()["allowed_extensions"])
    print()


def test_all_configs():
    """测试获取所有配置"""
    print("=== 测试获取所有配置 ===")
    all_configs = get_all_configs()
    print("所有配置:")
    for section, config in all_configs.items():
        print(f"  {section}: {config}")
    print()


if __name__ == "__main__":
    print("开始测试YAML配置保存功能...\n")
    
    # 运行所有测试
    test_all_configs()
    test_update_git_config()
    test_update_path_config()
    test_update_ui_config()
    test_add_remove_extension()
    
    # 恢复默认配置（可选）
    # update_git_config({"repo": "", "name": ""})
    # update_path_config({"path": "", "allowed_extensions": [".txt", ".md", ".json", ".yaml", ".yml"]})
    # update_ui_config({"theme": "default", "language": "zh-CN", "show_hidden_files": False})
    
    print("所有测试完成!")