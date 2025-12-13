#!/usr/bin/env python3
"""
演示如何在Python层面直接保存路径配置
"""

from data_processing.update_yaml import update_path_config
from data_processing.get_yaml import get_path_config

def main():
    print("=== Python层面直接保存路径演示 ===")
    
    # 要保存的路径
    test_path = "C:\\Users\\Public\\Documents\\MyProject"
    
    print(f"\n1. 当前配置的路径:")
    current_path = get_path_config()
    print(f"   当前路径: {current_path.get('path', '未设置')}")
    print(f"   允许的扩展名: {current_path.get('allowed_extensions', [])}")
    
    print(f"\n2. 保存新路径: {test_path}")
    result = update_path_config({'path': test_path})
    print(f"   保存结果: {'成功' if result else '失败'}")
    
    print(f"\n3. 验证保存的路径:")
    updated_path = get_path_config()
    print(f"   更新后的路径: {updated_path.get('path', '未设置')}")
    print(f"   允许的扩展名: {updated_path.get('allowed_extensions', [])}")
    
    print(f"\n4. 保存路径和扩展名:")
    path_with_extensions = {
        'path': "D:\\Projects\\NewFolder",
        'allowed_extensions': ['.py', '.js', '.html', '.css']
    }
    result = update_path_config(path_with_extensions)
    print(f"   保存结果: {'成功' if result else '失败'}")
    
    print(f"\n5. 验证保存的完整配置:")
    full_config = get_path_config()
    print(f"   更新后的路径: {full_config.get('path', '未设置')}")
    print(f"   更新后的扩展名: {full_config.get('allowed_extensions', [])}")
    
    print(f"\n=== 演示完成 ===")

if __name__ == "__main__":
    main()
