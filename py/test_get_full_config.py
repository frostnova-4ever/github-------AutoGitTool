#!/usr/bin/env python3
"""
测试get_config_path API方法是否能正确返回完整的yaml配置内容
"""

from data_processing.get_yaml import load_yaml_config
from response_utils import create_response_dict
import yaml

def main():
    print("=== 测试get_config_path API方法（完整配置） ===")
    
    try:
        # 模拟调用get_config_path方法
        config = load_yaml_config()
        yaml_content = yaml.dump(config, allow_unicode=True, default_flow_style=False)
        response = create_response_dict(success=True, yaml_content=yaml_content)
        
        print(f"\nAPI响应:")
        print(f"  成功: {response['success']}")
        print(f"  返回类型: {type(response['yaml_content'])}")
        
        if response['yaml_content']:
            print(f"\n✓ 成功获取到完整的yaml配置内容")
            print(f"\n配置内容预览:")
            print(response['yaml_content'][:500] + "..." if len(response['yaml_content']) > 500 else response['yaml_content'])
        else:
            print("\n⚠️  配置文件中没有内容")
            
    except Exception as e:
        response = create_response_dict(success=False, error=str(e))
        print(f"\nAPI响应:")
        print(f"  成功: {response['success']}")
        print(f"  错误: {response['error']}")
        print("\n✗ 获取配置内容失败")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
