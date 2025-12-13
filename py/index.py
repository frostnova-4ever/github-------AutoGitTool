import webview
import os
import json
from datetime import datetime
from pathlib import Path
from response_utils import create_response_dict
import disk_func
import format_func
import command_func
from data_processing.update_yaml import update_path_config
from data_processing.get_yaml import get_path_config
# 全局窗口变量
global_window = None
from auto import setup_auto_commit_push, stop_auto_commit_push

    
class Func:
    """
    工具函数类，包含所有辅助方法和工具函数
    """
    @staticmethod
    def create_response_dict(*args, **kwargs):
        return create_response_dict(*args, **kwargs)

class Api:
    def get_files(self, path):
        return disk_func.get_files(path)
    
    def read(self,file_path):
        result = disk_func.read_file(file_path)
        return result

    def list_paths(self) -> dict:
        return disk_func.list_common_paths()
    def open_folder_dialog(self):
        """
        API方法：打开文件夹选择对话框
        
        Returns:
            str: 选中的文件夹路径，如果用户取消则返回None
        """
        global global_window
        try:
            if global_window:
                # 使用新的FileDialog.FOLDER方式
                result = global_window.create_file_dialog(
                    dialog_type=webview.FileDialog.FOLDER,
                    allow_multiple=False
                )
                
                if result and len(result) > 0:
                    return result[0]
            return None
        except Exception as e:
            # 仅保留错误信息
            print(f"打开文件夹对话框失败: {str(e)}")
            return None
    def is_git_repository(self, path):
        return disk_func.is_git_repository(path)
    def execute_command(self, command, cwd=None):
        return command_func.execute_command(command, cwd)
    def handle_github_import(self, github_url):
        return command_func.GitHubCommand.handle_github_import(github_url)
    def git_clone(self, github_url, target_path):
        return command_func.GitHubCommand.git_clone(github_url, target_path)
    def git_pull(self, repo_path, remote_url=None):
        return command_func.GitHubCommand.git_pull(repo_path, remote_url)
    def associate_git_repo(self, repo_path, remote_url):
        return command_func.GitHubCommand.associate_git_repo(repo_path, remote_url)
    def setup_auto_commit_push(self, repo_path, interval_seconds=60, commit_message="自动提交", branch="main"):
        return setup_auto_commit_push(repo_path, interval_seconds, commit_message, branch)
    def stop_auto_commit_push(self, thread_info):
        return stop_auto_commit_push(thread_info)
    
    def get_config_path(self):
        """
        API方法：获取yaml配置文件中的path字段值
        
        Returns:
            dict: 包含path字段值的字典
        """
        try:
            from data_processing.get_yaml import get_path_config
            # 直接获取路径配置
            path_config = get_path_config()
            path_value = path_config.get('path', '')
            
            return create_response_dict(success=True, path=path_value)
        except Exception as e:
            # 仅保留错误信息
            print(f"获取配置路径失败: {str(e)}")
            return create_response_dict(success=False, error=str(e))
    
    def save_path(self, path):
        """
        API方法：保存用户输入的路径
        
        Args:
            path: 用户输入的路径
            
        Returns:
            dict: 保存结果
        """
        try:
            result = update_path_config({'path': path})
            return result
        except Exception as e:
            return create_response_dict(success=False, error=str(e))

def on_window_loaded():
    """
    窗口加载完成后的回调函数
    """
    global global_window
    # 移除调试信息

if __name__ == '__main__':
    try:
        # 创建API实例
        api = Api()

        # 使用pathlib处理路径
        current_script = Path(__file__).resolve()
        html_path = current_script.parent.parent / "demo" / "index.html"

        # 检查文件是否存在
        if not html_path.exists():
            # 保留错误信息
            print(f"HTML文件不存在: {html_path}")
            exit(1)

        # 读取HTML文件内容并注入配置路径
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 获取配置路径
        from data_processing.get_yaml import get_path_config
        path_config = get_path_config()
        config_path = path_config.get('path', '')
        
        # 替换HTML中的占位符或直接设置输入框的值
        if config_path:
            # 直接替换输入框的value属性
            html_content = html_content.replace(
                '<input type="text" id="right-panel-path-input" class="url-input" placeholder="在此输入 Windows 路径，例如 C:\\Users\\Public">',
                f'<input type="text" id="right-panel-path-input" class="url-input" value="{config_path}" placeholder="在此输入 Windows 路径，例如 C:\\Users\\Public">'
            )
        
        # 创建临时HTML文件
        temp_html_path = html_path.parent / "temp_index.html"
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 使用临时HTML文件
        global_window = webview.create_window(
            '文件浏览器',
            url=str(temp_html_path),
            js_api=api,
            width=1000,
            height=700,
            resizable=True
        )
        
        # 启动应用程序
        webview.start(on_window_loaded, debug=True)
        
        # 应用程序关闭后删除临时HTML文件
        if temp_html_path.exists():
            temp_html_path.unlink()
    except Exception as e:
        # 仅保留错误信息
        print(f"启动应用失败: {str(e)}")
