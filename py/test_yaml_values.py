#!/usr/bin/env python3
"""
测试get_yaml_str_value和get_yaml_list_value函数的功能
"""

from data_processing import get_yaml_str_value, get_yaml_list_value

print("=== 测试YAML配置值获取函数 ===\n")

# 测试字符串值获取
print("1. 测试get_yaml_str_value函数:")

# 获取字符串配置
repo_value = get_yaml_str_value("userSettings.github_repo")
print(f"   userSettings.github_repo: {repo_value} (类型: {type(repo_value).__name__})")

name_value = get_yaml_str_value("userSettings.name")
print(f"   userSettings.name: {name_value} (类型: {type(name_value).__name__})")

# 测试布尔值转换为字符串
theme_value = get_yaml_str_value("userSettings.theme")
print(f"   userSettings.theme: {theme_value} (类型: {type(theme_value).__name__})")

# 测试默认值
non_existent = get_yaml_str_value("userSettings.non_existent_key", default="默认字符串值")
print(f"   不存在的键 (默认值): {non_existent} (类型: {type(non_existent).__name__})")

# 测试列表转换为字符串
extensions_str = get_yaml_str_value("userSettings.allowed_extensions")
print(f"   allowed_extensions转换为字符串: {extensions_str} (类型: {type(extensions_str).__name__})")

# 测试列表值获取
print("\n2. 测试get_yaml_list_value函数:")

# 获取列表配置
extensions = get_yaml_list_value("userSettings.allowed_extensions")
print(f"   userSettings.allowed_extensions: {extensions} (类型: {type(extensions).__name__})")

# 测试不存在的列表（默认空列表）
empty_list = get_yaml_list_value("userSettings.non_existent_list")
print(f"   不存在的列表 (默认空列表): {empty_list} (类型: {type(empty_list).__name__})")

# 测试自定义默认值
custom_default = get_yaml_list_value("userSettings.non_existent_list", default=[".py", ".js", ".yaml"])
print(f"   不存在的列表 (自定义默认值): {custom_default} (类型: {type(custom_default).__name__})")

# 测试非列表值返回默认值
repo_list = get_yaml_list_value("userSettings.github_repo")
print(f"   非列表值 (默认空列表): {repo_list} (类型: {type(repo_list).__name__})")

print("\n=== 测试完成 ===")