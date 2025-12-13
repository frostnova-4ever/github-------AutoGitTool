#!/usr/bin/env python3
"""
测试get_config_path API方法是否正常工作
"""

from data_processing.get_yaml import get_path_config
from response_utils import create_response_dict

def main():
    print("=== 测试get_config_path API方法 ===")
    
    try:
        # 模拟调用get_config_path方法
        config = get_path_config()
        response = create_response_dict(success=True, path=config.get('path', ''))
        
        print(f"\nAPI响应:")
        print(f"  成功: {response['success']}")
        print(f"  路径: {response['path']}")
        
        if response['path']:
            print("\n✓ 成功获取到配置路径")
        else:
            print("\n⚠️  配置文件中没有保存的路径")
            
    except Exception as e:
        response = create_response_dict(success=False, error=str(e))
        print(f"\nAPI响应:")
        print(f"  成功: {response['success']}")
        print(f"  错误: {response['error']}")
        print("\n✗ 获取配置路径失败")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
