#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动操作模块
包含定时自动提交和推送Git仓库的功能
"""

import time
import threading
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from command_func import GitHubCommand
from response_utils import create_response_dict
from data_processing.get_yaml import get_yaml_str_value


class AutoGitHubCommand(GitHubCommand):
    """
    扩展GitHubCommand类，增加自动提交推送功能
    """
    @staticmethod
    def setup_auto_commit_push(repo_path, interval_seconds=None, commit_message="自动提交", branch="main", stop_event=None):
        """
        设置定时自动提交和推送Git仓库
        
        参数:
            repo_path: Git仓库路径
            interval_seconds: 时间间隔（秒数），如果为None则从配置文件读取
            commit_message: 提交信息，默认"自动提交"
            branch: 推送分支，默认"main"
            stop_event: 用于停止定时任务的Event对象（可选）
        
        返回:
            dict: 包含success、data、message和error字段的标准响应格式
        """
        # 如果未指定时间间隔，从配置文件读取
        if interval_seconds is None:
            try:
                time_str = get_yaml_str_value("userSettings.auto.auto_submit_and_push.time", default="10")
                interval_seconds = int(time_str)
            except ValueError:
                interval_seconds = 60  # 默认60秒
        def auto_commit_push_task():
            """自动提交推送任务函数"""
            while not (stop_event and stop_event.is_set()):
                try:
                    result = AutoGitHubCommand.git_commit_and_push(repo_path, commit_message, branch)
                    if result and result.get('success'):
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 自动提交推送成功")
                    else:
                        error_msg = "未知错误"
                        if result:
                            # 先尝试获取error字段
                            if 'error' in result:
                                error_msg = result['error'] or "无错误信息"
                            # 再尝试获取output字段
                            elif 'output' in result:
                                error_msg = result['output'] or "无错误信息"
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 自动提交推送失败: {error_msg}")
                except Exception as e:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 自动提交推送任务发生异常: {str(e)}")
                
                # 等待指定时间间隔，可中断
                for _ in range(interval_seconds):
                    if stop_event and stop_event.is_set():
                        break
                    time.sleep(1)
            
            print(f"\n自动提交推送任务已停止")
        
        # 创建停止事件（如果未提供）
        if stop_event is None:
            stop_event = threading.Event()
        
        # 创建并启动线程
        task_thread = threading.Thread(target=auto_commit_push_task, daemon=True)
        task_thread.stop_event = stop_event  # 将stop_event附加到线程对象上
        task_thread.start()
        
        # 确保所有数据都在data字段内，满足前端需求
        return create_response_dict(
            success=True,
            message="自动提交推送任务已启动",
            data={"thread_id": id(task_thread), "interval_seconds": interval_seconds}
        )
    
    @staticmethod
    def stop_auto_commit_push(thread_info):
        """
        停止自动提交推送任务
        
        参数:
            thread_info: 包含thread_id的字典，或直接传入线程对象
        """
        try:
            # 如果传入的是字典，获取thread_id
            if isinstance(thread_info, dict):
                thread_id = thread_info.get("thread_id")
                if not thread_id:
                    return create_response_dict(success=False, error="无效的线程信息，缺少thread_id")
                
                # 查找对应的线程对象
                for thread in threading.enumerate():
                    if id(thread) == thread_id and hasattr(thread, 'stop_event'):
                        task_thread = thread
                        break
                else:
                    return create_response_dict(success=False, error="未找到对应的线程对象")
            else:
                # 直接使用线程对象
                task_thread = thread_info
            
            if task_thread and hasattr(task_thread, 'stop_event'):
                task_thread.stop_event.set()
                task_thread.join(timeout=5)  # 等待最多5秒
                return create_response_dict(success=True, message="自动提交推送任务已停止")
            else:
                return create_response_dict(success=False, error="无效的线程对象，缺少stop_event属性")
        except Exception as e:
            return create_response_dict(success=False, error=f"停止自动提交推送任务时发生异常: {str(e)}")

def setup_auto_commit_push(repo_path, interval_seconds=None, commit_message="自动提交", branch="main", stop_event=None):
    return AutoGitHubCommand.setup_auto_commit_push(repo_path, interval_seconds, commit_message, branch, stop_event)

def stop_auto_commit_push(thread_info):
    return AutoGitHubCommand.stop_auto_commit_push(thread_info)

# 示例用法
if __name__ == "__main__":
    # 使用当前目录作为仓库路径示例
    current_repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 设置自动提交推送任务
    result = setup_auto_commit_push(
        repo_path=current_repo_path,
        interval_seconds=None,  # 使用配置文件中的时间间隔
        commit_message="定时自动提交",
        branch="main"
    )
    
    print(f"setup_auto_commit_push 结果: {result}")
    
    if result["success"] and "thread_id" in result:
        print(f"\n自动提交推送任务已启动，线程ID: {result['thread_id']}")
        print(f"按 Ctrl+C 停止自动提交推送任务...")
        print(f"当前使用的自动调用周期: {result.get('interval_seconds', '未知')}秒")
    else:
        print(f"\n启动自动提交推送任务失败: {result.get('error', '未知错误')}")
        sys.exit(1)
    
    try:
        # 主程序保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n正在停止自动提交推送任务...")
        stop_result = stop_auto_commit_push(result['data'])
        if stop_result["success"]:
            print("任务已停止")
        else:
            print(f"停止任务失败: {stop_result['error']}")
