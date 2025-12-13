#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Git提交和推送功能的脚本
"""

import os
import sys
import time

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from command_func import git_commit, git_push, git_commit_and_push
from response_utils import create_response_dict

def test_git_operations():
    """
    测试Git提交和推送功能
    """
    # 获取当前目录作为测试仓库路径
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    print(f"测试仓库路径: {repo_path}")
    print(f"是否存在.git目录: {os.path.exists(os.path.join(repo_path, '.git'))}")
    
    # 测试1: git add .
    print("\n=== 测试1: git add . ===")
    add_result = git_commit(repo_path, "测试提交 - 仅测试add")
    print(f"git add 结果: {add_result}")
    
    # 测试2: git commit
    print("\n=== 测试2: git commit ===")
    commit_result = git_commit(repo_path, "测试提交 - 测试commit")
    print(f"git commit 结果: {commit_result}")
    
    # 测试3: git push
    print("\n=== 测试3: git push ===")
    push_result = git_push(repo_path)
    print(f"git push 结果: {push_result}")
    
    # 测试4: git commit and push
    print("\n=== 测试4: git commit and push ===")
    commit_push_result = git_commit_and_push(repo_path, "测试提交 - 测试commit and push")
    print(f"git commit and push 结果: {commit_push_result}")

if __name__ == "__main__":
    test_git_operations()
