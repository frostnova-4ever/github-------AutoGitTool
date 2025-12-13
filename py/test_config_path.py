#!/usr/bin/env python3
"""
测试配置路径获取功能
"""

from index import Api

def test_get_config_path():
    """测试获取配置路径"""
    api = Api()
    response = api.get_config_path()
    print("API响应:", response)
    
    if response.get('success'):
        print("✓ 成功获取到配置路径")
        if response.get('path'):
            print(f"  配置文件路径: {response.get('path')}")
        else:
            print("  配置文件中没有设置路径")
    else:
        print(f"✗ 获取配置路径失败: {response.get('error')}")

if __name__ == "__main__":
    test_get_config_path()
