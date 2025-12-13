#!/usr/bin/env python3
"""
调试路径保存功能，检查完整流程
"""

import os
import yaml
from pathlib import Path
from data_processing.get_yaml import get_path_config, load_yaml_config
from data_processing.save_yaml import save_yaml_config
from data_processing.update_yaml import update_path_config

def main():
    print("=== 调试路径保存功能 ===")
    
    # 1. 打印当前配置文件路径
    print("\n1. 配置文件路径:")
    current_dir = Path(__file__).parent.parent
    config_path = os.path.join(current_dir, 'data', 'settings.yaml')
    print(f"   计算的配置文件路径: {config_path}")
    print(f"   文件是否存在: {os.path.exists(config_path)}")
    
    # 2. 读取当前配置
    print("\n2. 当前配置:")
    current_config = get_path_config()
    print(f"   当前路径: {current_config.get('path', '未设置')}")
    
    # 3. 直接读取yaml文件内容
    print("\n3. 直接读取yaml文件内容:")
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content and 'userSettings' in yaml_content:
                print(f"   YAML中的路径: {yaml_content['userSettings'].get('path', '未设置')}")
            else:
                print(f"   YAML内容: {yaml_content}")
    except Exception as e:
        print(f"   读取yaml文件失败: {e}")
    
    # 4. 尝试保存新路径
    print("\n4. 保存新路径:")
    test_path = os.getcwd()  # 使用当前工作目录作为测试路径
    print(f"   要保存的新路径: {test_path}")
    
    # 方法1: 使用update_path_config
    print(f"   使用update_path_config保存...")
    result = update_path_config({'path': test_path})
    print(f"   update_path_config结果: {'成功' if result else '失败'}")
    
    # 5. 验证保存结果
    print("\n5. 验证保存结果:")
    
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
    
    # 方法2: 直接使用save_yaml_config
    print("\n6. 尝试直接使用save_yaml_config保存:")
    test_path2 = test_path + "\\subfolder"
    print(f"   要保存的新路径: {test_path2}")
    
    # 加载配置
    config = load_yaml_config()
    if 'userSettings' not in config:
        config['userSettings'] = {}
    config['userSettings']['path'] = test_path2
    
    # 保存配置
    result = save_yaml_config(config)
    print(f"   save_yaml_config结果: {'成功' if result else '失败'}")
    
    # 验证
    print(f"   直接读取yaml文件...")
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            yaml_content = yaml.safe_load(file)
            if yaml_content and 'userSettings' in yaml_content:
                print(f"   YAML中的路径: {yaml_content['userSettings'].get('path', '未设置')}")
                
                if yaml_content['userSettings'].get('path') == test_path2:
                    print(f"   ✓ 路径已成功保存到yaml文件")
                else:
                    print(f"   ✗ 路径未正确保存到yaml文件")
            else:
                print(f"   YAML内容: {yaml_content}")
    except Exception as e:
        print(f"   读取yaml文件失败: {e}")
    
    print(f"\n=== 调试完成 ===")

if __name__ == "__main__":
    main()
