#!/usr/bin/env python3
"""
测试前端工作流：模拟用户输入路径并点击"列出路径"按钮的行为
"""

import os
import yaml
from pathlib import Path
from data_processing.get_yaml import get_path_config, load_yaml_config
from data_processing.save_yaml import save_yaml_config
from data_processing.update_yaml import update_path_config
import disk_func

def main():
    print("=== 测试前端工作流 ===")
    
    # 1. 获取配置文件路径
    current_dir = Path(__file__).parent.parent
    config_path = os.path.join(current_dir, 'data', 'settings.yaml')
    print(f"\n1. 配置文件路径: {config_path}")
    
    # 2. 读取当前配置
    print("\n2. 当前配置:")
    current_config = get_path_config()
    print(f"   当前路径: {current_config.get('path', '未设置')}")
    
    # 3. 模拟用户输入一个新路径
    test_path = os.path.join(os.getcwd(), "test_dir")
    print(f"\n3. 模拟用户输入新路径: {test_path}")
    
    # 4. 模拟用户点击"列出路径"按钮（调用get_files函数）
    print(f"\n4. 模拟调用get_files函数...")
    
    # 创建一个测试目录（如果不存在）
    if not os.path.exists(test_path):
        os.makedirs(test_path)
        print(f"   创建测试目录: {test_path}")
    
    # 调用get_files函数
    result = disk_func.get_files(test_path)
    print(f"   get_files结果: {'成功' if result.get('success', False) else '失败'}")
    if 'contents' in result:
        print(f"   返回的文件数量: {len(result['contents'])}")
    
    # 5. 验证路径是否已保存
    print(f"\n5. 验证路径保存结果:")
    
    # 5.1 通过get_path_config获取
    new_config = get_path_config()
    print(f"   通过get_path_config获取的路径: {new_config.get('path', '未设置')}")
    
    # 5.2 直接读取yaml文件
    print(f"   直接读取yaml文件...")
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content and 'userSettings' in yaml_content:
                print(f"   YAML中的路径: {yaml_content['userSettings'].get('path', '未设置')}")
                
                if yaml_content['userSettings'].get('path') == test_path:
                    print(f"   ✓ 路径已成功保存到yaml文件")
                else:
                    print(f"   ✗ 路径未正确保存到yaml文件")
            else:
                print(f"   YAML内容: {yaml_content}")
    except Exception as e:
        print(f"   读取yaml文件失败: {e}")
    
    # 6. 清理测试目录
    if os.path.exists(test_path):
        os.rmdir(test_path)
        print(f"\n6. 清理测试目录: {test_path}")
    
    print(f"\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
