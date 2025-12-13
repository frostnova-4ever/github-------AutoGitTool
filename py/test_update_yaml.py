#!/usr/bin/env python3
"""
测试update_yaml.py模块的功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 导入update_yaml模块中的函数
from py.data_processing.update_yaml import (
    load_yaml_config,
    save_yaml_config,
    update_yaml_config,
    update_git_config,
    update_path_config,
    update_ui_config,
    add_allowed_extension,
    remove_allowed_extension,
    update_configs
)

def test_load_yaml_config():
    """测试加载YAML配置"""
    print("测试load_yaml_config...")
    config = load_yaml_config()
    print(f"   加载成功: {config}")
    return config is not None

def test_update_yaml_config():
    """测试更新特定键"""
    print("测试update_yaml_config...")
    # 测试更新单个键
    result = update_yaml_config("test_key", "test_value")
    print(f"   更新test_key: {'成功' if result else '失败'}")
    
    # 测试更新嵌套键
    result = update_yaml_config("test_nested.key1.key2", "nested_value")
    print(f"   更新test_nested.key1.key2: {'成功' if result else '失败'}")
    
    return result

def test_update_git_config():
    """测试更新Git配置"""
    print("测试update_git_config...")
    git_config = {
        "repo": "https://github.com/test/repo.git",
        "name": "test_user"
    }
    result = update_git_config(git_config)
    print(f"   更新Git配置: {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        user_settings = config["userSettings"]
        print(f"   GitHub仓库: {user_settings.get('github_repo')}")
        print(f"   用户名: {user_settings.get('name')}")
    
    return result

def test_update_path_config():
    """测试更新路径配置"""
    print("测试update_path_config...")
    path_config = {
        "path": "C:/test/path",
        "allowed_extensions": [".txt", ".py", ".md"]
    }
    result = update_path_config(path_config)
    print(f"   更新路径配置: {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        user_settings = config["userSettings"]
        print(f"   路径: {user_settings.get('path')}")
        print(f"   允许的扩展名: {user_settings.get('allowed_extensions')}")
    
    return result

def test_update_ui_config():
    """测试更新界面配置"""
    print("测试update_ui_config...")
    ui_config = {
        "theme": "light",
        "language": "zh-CN",
        "show_hidden_files": True,
        "default_view": "list"
    }
    result = update_ui_config(ui_config)
    print(f"   更新界面配置: {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        user_settings = config["userSettings"]
        print(f"   主题: {user_settings.get('theme')}")
        print(f"   语言: {user_settings.get('language')}")
        print(f"   显示隐藏文件: {user_settings.get('show_hidden_files')}")
        print(f"   默认视图: {user_settings.get('default_view')}")
    
    return result

def test_add_allowed_extension():
    """测试添加允许的文件扩展名"""
    print("测试add_allowed_extension...")
    # 先确保扩展名为空或重置
    update_path_config({"allowed_extensions": [".txt"]})
    
    # 测试添加单个扩展名
    result = add_allowed_extension(".pdf")
    print(f"   添加.pdf扩展名: {'成功' if result else '失败'}")
    
    # 测试添加不带点的扩展名
    result = add_allowed_extension("docx")
    print(f"   添加docx扩展名(不带点): {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        allowed_extensions = config["userSettings"].get("allowed_extensions", [])
        print(f"   允许的扩展名: {allowed_extensions}")
        expected_extensions = [".txt", ".pdf", ".docx"]
        if all(ext in allowed_extensions for ext in expected_extensions):
            print("   所有预期的扩展名都已添加")
    
    return result

def test_remove_allowed_extension():
    """测试移除允许的文件扩展名"""
    print("测试remove_allowed_extension...")
    # 先设置扩展名为[.txt, .pdf, .docx]
    update_path_config({"allowed_extensions": [".txt", ".pdf", ".docx"]})
    
    # 测试移除单个扩展名
    result = remove_allowed_extension(".pdf")
    print(f"   移除.pdf扩展名: {'成功' if result else '失败'}")
    
    # 测试移除不带点的扩展名
    result = remove_allowed_extension("docx")
    print(f"   移除docx扩展名(不带点): {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        allowed_extensions = config["userSettings"].get("allowed_extensions", [])
        print(f"   允许的扩展名: {allowed_extensions}")
        if ".pdf" not in allowed_extensions and ".docx" not in allowed_extensions:
            print("   所有预期的扩展名都已移除")
    
    return result

def test_update_configs():
    """测试更新所有配置"""
    print("测试update_configs...")
    configs = {
        "git": {
            "repo": "https://github.com/comprehensive/repo.git",
            "name": "comprehensive_user"
        },
        "path": {
            "path": "C:/comprehensive/path",
            "allowed_extensions": [".txt", ".py"]
        },
        "ui": {
            "theme": "dark",
            "language": "en-US",
            "show_hidden_files": False,
            "default_view": "grid"
        }
    }
    result = update_configs(configs)
    print(f"   更新所有配置: {'成功' if result else '失败'}")
    
    # 验证更新是否成功
    config = load_yaml_config()
    if "userSettings" in config:
        user_settings = config["userSettings"]
        print(f"   GitHub仓库: {user_settings.get('github_repo')}")
        print(f"   用户名: {user_settings.get('name')}")
        print(f"   路径: {user_settings.get('path')}")
        print(f"   允许的扩展名: {user_settings.get('allowed_extensions')}")
        print(f"   主题: {user_settings.get('theme')}")
        print(f"   语言: {user_settings.get('language')}")
    
    return result

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("开始测试update_yaml模块")
    print("="*50)
    
    tests = [
        test_load_yaml_config,
        test_update_yaml_config,
        test_update_git_config,
        test_update_path_config,
        test_update_ui_config,
        test_add_allowed_extension,
        test_remove_allowed_extension,
        test_update_configs
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   测试失败: {e}")
        print()  # 空行分隔测试结果
    
    print("="*50)
    print(f"测试完成: {passed}/{total} 个测试通过")
    print("="*50)
    
    return passed == total

if __name__ == "__main__":
    # 运行所有测试
    success = run_all_tests()
    
    if success:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
        sys.exit(1)