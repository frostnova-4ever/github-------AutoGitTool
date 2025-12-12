#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试将get_files方法移动到disk_func模块后的功能
"""

import os
import sys
# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import disk_func

def test_get_files():
    """测试get_files函数"""
    print("=== 测试get_files函数 ===")
    
    # 获取当前目录
    current_dir = os.getcwd()
    print(f"测试目录: {current_dir}")
    
    try:
        # 调用disk_func.get_files函数
        result = disk_func.get_files(current_dir)
        
        if result.get("success", False):
            print(f"成功获取文件列表")
            print(f"目录: {result.get('path')}")
            print(f"文件数量: {len(result.get('contents', []))}")
            
            # 打印前几个文件
            print("\n前5个文件/目录:")
            for item in result.get('contents', [])[:5]:
                item_type = "文件" if item['is_file'] else "目录"
                print(f"  {item['name']} - {item_type} - {item['size_formatted']}")
        else:
            print(f"获取文件列表失败: {result.get('error')}")
            
    except Exception as e:
        print(f"测试出错: {str(e)}")

if __name__ == "__main__":
    test_get_files()
