#!/usr/bin/env python3
"""
测试get_yaml_value_by_path函数的功能
"""

from data_processing import get_yaml_value_by_path

print("=== 测试get_yaml_value_by_path函数 ===\n")

# 测试1：获取现有的配置值
print("1. 测试获取现有的配置值:")
repo_value = get_yaml_value_by_path("userSettings.github_repo")
print(f"   userSettings.github_repo: {repo_value}")

name_value = get_yaml_value_by_path("userSettings.name")
print(f"   userSettings.name: {name_value}")

# 测试2：测试默认值
print("\n2. 测试不存在的路径返回默认值:")
non_existent = get_yaml_value_by_path("userSettings.non_existent_key", default="默认值")
print(f"   不存在的键: {non_existent}")

# 测试3：测试嵌套路径
print("\n3. 测试嵌套路径:")
theme_value = get_yaml_value_by_path("userSettings.theme")
print(f"   userSettings.theme: {theme_value}")

# 测试4：测试根级路径
print("\n4. 测试根级路径:")
user_settings = get_yaml_value_by_path("userSettings")
print(f"   userSettings (完整): {user_settings}")

print("\n=== 测试完成 ===")