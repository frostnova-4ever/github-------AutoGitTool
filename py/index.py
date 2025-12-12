import webview
import os
import json
from datetime import datetime
from pathlib import Path
from response_utils import create_response_dict
import disk_func
import format_func
import command_func
# 全局窗口变量
global_window = None


    
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

def on_window_loaded():
    """
    窗口加载完成后的回调函数
    """
    global global_window
    print("窗口已加载完成")

if __name__ == '__main__':
    try:
        # 创建API实例
        api = Api()

        # 使用pathlib处理路径
        current_script = Path(__file__).resolve()
        html_path = current_script.parent.parent / "demo" / "index.html"

        # 检查文件是否存在
        if not html_path.exists():
            print(f"HTML文件不存在: {html_path}")
            exit(1)

        # 直接使用文件路径而不是读取内容
        global_window = webview.create_window(
            '文件浏览器',
            url="../demo/index.html",
            js_api=api,
            width=1000,
            height=700,
            resizable=True
        )

        # 启动应用
        webview.start(on_window_loaded, debug=True)
    except Exception as e:
        print(f"启动应用失败: {str(e)}")
