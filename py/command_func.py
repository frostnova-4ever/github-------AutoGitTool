import os
import subprocess
import shlex
import re
from response_utils import create_response_dict


def execute_system_command(command, cwd=None):
    """执行系统命令"""
    if not cwd:
        cwd = os.getcwd()
    try:
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(command,cwd=cwd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        else:  # Linux/macOS
            process = subprocess.Popen(shlex.split(command),cwd=cwd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode
    except Exception as e:
        return "", str(e), -1


def execute_system_command_with_response(command, cwd=None):
    """执行系统命令并返回统一格式的响应"""
    stdout, stderr, returncode = execute_system_command(command, cwd)
    return create_response_dict(success=returncode == 0, output=stdout, error=stderr, cwd=cwd)


class GitHubCommand:
    """GitHub命令处理类"""
    
    @staticmethod
    def parse_github_url(url):
        """解析GitHub URL"""
        patterns = [
            r'^https?://github\.com/([^/]+)/([^/\.]+)(?:\.git)?/?$',
            r'^git@github\.com:([^/]+)/([^/\.]+)(?:\.git)?$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, url)
            if match:return match.group(1), match.group(2)
        return None
    
    @staticmethod
    def test_github_connection_with_git(github_url):
        """测试GitHub连接"""
        command = f"git ls-remote --heads {github_url}"
        return execute_system_command_with_response(command)
    
    @staticmethod
    def handle_github_import(github_url):
        """处理GitHub导入"""
        repo_info = GitHubCommand.parse_github_url(github_url)
        if repo_info:
            owner, repo_name = repo_info
            clone_url = f"https://github.com/{owner}/{repo_name}.git"
            return GitHubCommand.test_github_connection_with_git(clone_url)
        return create_response_dict(success=False, error="无效的GitHub URL")
    
    @staticmethod
    def git_clone(github_url, target_path):
        """克隆GitHub仓库"""
        command = f"git clone {github_url} {target_path}"
        return execute_system_command_with_response(command)
    
    @staticmethod
    def git_pull(repo_path, remote_url=None):
        """拉取仓库更新"""
        if remote_url:
            # 先设置远程仓库
            has_origin, _, _ = execute_system_command("git remote -v", cwd=repo_path)
            if "origin" in has_origin:
                execute_system_command(f"git remote set-url origin {remote_url}", cwd=repo_path)
            else:
                execute_system_command(f"git remote add origin {remote_url}", cwd=repo_path)
        
        # 执行拉取
        return execute_system_command_with_response("git pull", cwd=repo_path)
    
    @staticmethod
    def associate_git_repo(repo_path, remote_url):
        """关联Git仓库"""
        # 检查是否是Git仓库
        if not os.path.exists(os.path.join(repo_path, '.git')):
            execute_system_command("git init", cwd=repo_path)
        
        # 设置远程仓库
        has_origin, _, _ = execute_system_command("git remote -v", cwd=repo_path)
        if "origin" in has_origin:
            command = f"git remote set-url origin {remote_url}"
        else:
            command = f"git remote add origin {remote_url}"
        
        return execute_system_command_with_response(command, cwd=repo_path)
    
    @staticmethod
    def git_commit(repo_path, commit_message):
        """提交Git仓库更改"""
        # 添加所有更改
        add_result = execute_system_command_with_response("git add .", cwd=repo_path)
        
        if not add_result["success"]:
            return create_response_dict(success=False, error=add_result["error"] or "添加更改失败")
        
        # 执行提交
        commit_command = f"git commit -m \"{commit_message}\""
        commit_result = execute_system_command_with_response(commit_command, cwd=repo_path)
        
        # 检查是否是因为没有需要提交的内容而导致的"失败"
        if not commit_result["success"]:
            # 获取错误信息，优先检查error字段，然后是output字段
            error_message = commit_result.get("error", "") or commit_result.get("output", "")
            if "nothing to commit" in error_message:
                # 这不是真正的错误，而是正常状态
                return create_response_dict(success=True, output=error_message or "没有需要提交的内容")
        
        return commit_result
    
    @staticmethod
    def git_push(repo_path, branch="main"):
        """推送Git仓库更改"""
        push_command = f"git push origin {branch}"
        return execute_system_command_with_response(push_command, cwd=repo_path)
    
    @staticmethod
    def git_commit_and_push(repo_path, commit_message, branch="main"):
        """
        提交并推送Git仓库更改
        """
        # 先提交
        commit_result = GitHubCommand.git_commit(repo_path, commit_message)
        if not commit_result["success"]:
            return commit_result
        # 再推送
        return GitHubCommand.git_push(repo_path, branch)


# 保持原有函数接口不变，向后兼容
def parse_github_url(url):
    return GitHubCommand.parse_github_url(url)

def test_github_connection_with_git(github_url):
    return GitHubCommand.test_github_connection_with_git(github_url)

def handle_github_import(github_url):
    return GitHubCommand.handle_github_import(github_url)

def git_clone(github_url, target_path):
    return GitHubCommand.git_clone(github_url, target_path)

def git_pull(repo_path, remote_url=None):
    return GitHubCommand.git_pull(repo_path, remote_url)

def associate_git_repo(repo_path, remote_url):
    return GitHubCommand.associate_git_repo(repo_path, remote_url)


def git_commit(repo_path, commit_message):
    return GitHubCommand.git_commit(repo_path, commit_message)


def git_push(repo_path, branch="main"):
    return GitHubCommand.git_push(repo_path, branch)


def git_commit_and_push(repo_path, commit_message, branch="main"):
    return GitHubCommand.git_commit_and_push(repo_path, commit_message, branch)


def execute_command(command, cwd=None):
    """执行系统命令"""
    if not cwd:
        cwd = os.getcwd()
    
    # 处理cd命令的特殊情况
    if command.strip().lower().startswith('cd '):
        new_dir = command.strip()[3:]
        # 处理相对路径
        if new_dir.startswith('.') or not os.path.isabs(new_dir):
            new_dir = os.path.join(cwd, new_dir)
        # 标准化路径
        new_dir = os.path.normpath(new_dir)
        # 检查路径是否存在
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            return create_response_dict(success=True, output=f"切换到目录: {new_dir}", error="", cwd=new_dir)
        else:
            return create_response_dict(success=False, output="", error=f"目录不存在: {new_dir}", cwd=cwd)
    
    # 执行系统命令
    stdout, stderr, returncode = execute_system_command(command, cwd=cwd)
    
    return create_response_dict(success=returncode == 0, output=stdout, error=stderr, cwd=cwd)
