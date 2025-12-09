import webview
import os
import json
from datetime import datetime
from pathlib import Path

# 全局窗口变量
global_window = None

def get_directory_contents(path):
    """
    获取指定路径下的所有文件和文件夹信息

    Args:
        path (str): 目录路径

    Returns:
        list: 包含文件/文件夹信息的列表
    """
    if not os.path.exists(path):
        return {"error": "路径不存在"}

    if not os.path.isdir(path):
        return {"error": "指定路径不是目录"}

    contents = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            stat_info = os.stat(item_path)

            # 获取文件大小
            if os.path.isfile(item_path):
                size = stat_info.st_size
                is_file = True
            else:
                size = get_directory_size(item_path)
                is_file = False

            # 获取修改时间
            mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            contents.append({
                "name": item,
                "path": item_path,
                "size": size,
                "modified_time": mtime,
                "is_file": is_file
            })
    except PermissionError:
        return {"error": "权限不足，无法访问该目录"}

    return contents

def get_directory_size(path):
    """
    递归计算目录大小

    Args:
        path (str): 目录路径

    Returns:
        int: 目录总大小(字节)
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except PermissionError:
        pass  # 忽略权限错误
    return total_size

def format_size(size_bytes):
    """
    将字节大小格式化为人类可读的格式

    Args:
        size_bytes (int): 字节大小

    Returns:
        str: 格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"

def format_dir(data):
    """
    将数据格式化为JSON字符串

    Args:
        data (any): 要格式化的数据

    Returns:
        str: 格式化后的JSON字符串
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
class Api:
    def get_files(self, path):
        """
        API方法：获取指定路径下的文件列表
        Args:
            path (str): 目录路径
        Returns:
            dict: 文件列表信息
        """
        contents = get_directory_contents(path)

        # 如果返回的是错误信息，直接返回
        if isinstance(contents, dict) and "error" in contents:
            return contents

        # 格式化大小信息
        for item in contents:
            if item['is_file']:
                item['size_formatted'] = format_size(item['size'])
            else:
                item['size_formatted'] = format_size(item['size']) + " (目录)"

        return {
            "path": path,
            "contents": contents
        }
    
    def read(self,file_path):
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return "文件不存在"

            # 检查是否为文件
            if not os.path.isfile(file_path):
                return "指定路径不是文件"
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return  f"读取文件失败: {str(e)}"

    def list_paths(self) -> dict:
        """
        API方法：列出系统中的常用路径
        Returns:dict: 包含常用路径的列表
        """
        paths = []
        try:
            # 添加当前目录
            current_dir = os.getcwd()
            paths.append({"name": "当前目录", "path": current_dir, "type": "directory"})
            
            home_dir = os.path.expanduser("~")
            paths.append({"name": "用户主目录", "path": home_dir, "type": "directory"})
            
            if os.name == 'nt':
                # 获取Windows特殊文件夹路径
                self._add_windows_special_folders(paths, home_dir)
                # 获取Windows磁盘驱动器
                self._add_windows_drives(paths)
            return {"paths": paths}
        except Exception as e:
            return {"error": f"获取路径列表失败: {str(e)}", "paths": paths}
            
    def _add_windows_special_folders(self, paths: list, home_dir: str) -> None:
        """
        添加Windows特殊文件夹路径到列表中
        
        Args:
            paths: 要添加路径的列表
            home_dir: 用户主目录路径
        """
        try:
            import win32com.shell
            from win32com.shell import shell, shellcon
            
            # 使用pywin32获取Windows特殊文件夹
            special_folders = [
                ("桌面", shellcon.CSIDL_DESKTOP),
                ("文档", shellcon.CSIDL_PERSONAL),
                ("下载", shellcon.CSIDL_DOWNLOADS),
                ("音乐", shellcon.CSIDL_MYMUSIC),
                ("图片", shellcon.CSIDL_MYPICTURES),
                ("视频", shellcon.CSIDL_MYVIDEO),
                ("程序", shellcon.CSIDL_PROGRAMS),
                ("系统", shellcon.CSIDL_SYSTEM)
            ]
            
            for name, csidl in special_folders:
                try:
                    folder_path = shell.SHGetFolderPath(0, csidl, None, 0)
                    if os.path.exists(folder_path):
                        paths.append({"name": name, "path": folder_path, "type": "directory"})
                except Exception:
                    # 单个文件夹获取失败不影响其他文件夹
                    continue
        except Exception:
            # pywin32调用失败，回退到传统方法
            traditional_folders = [
                ("桌面", "Desktop"),
                ("文档", "Documents"),
                ("下载", "Downloads")
            ]
            
            for name, subdir in traditional_folders:
                folder_path = os.path.join(home_dir, subdir)
                if os.path.exists(folder_path):
                    paths.append({"name": name, "path": folder_path, "type": "directory"})
    
    def _add_windows_drives(self, paths: list) -> None:
        """
        添加Windows磁盘驱动器路径到列表中
        Args:
            paths: 要添加路径的列表
        """
        try:
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\\')[:-1]
            for drive in drives:
                if os.path.exists(drive):
                    paths.append({"name": f"磁盘 {drive}", "path": drive, "type": "drive"})
        except Exception:
            # pywin32调用失败，回退到传统方法
            import string
            for letter in string.ascii_uppercase:
                drive = letter + ":\\"
                if os.path.exists(drive):
                    paths.append({"name": f"磁盘 {drive}", "path": drive, "type": "drive"})
    
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
        """
        API方法：检查指定路径是否是Git仓库（是否包含.git目录）
        
        Args:
            path (str): 要检查的目录路径
            
        Returns:
            bool: 如果是Git仓库返回True，否则返回False
        """
        if not os.path.exists(path):
            return False
        if not os.path.isdir(path):
            return False
        
        git_dir = os.path.join(path, '.git')
        return os.path.exists(git_dir) and os.path.isdir(git_dir)
    
    def _execute_system_command(self, command, cwd=None, **kwargs):
        """
        通用系统命令执行模板函数
        
        Args:
            command (str): 要执行的命令字符串
            cwd (str): 命令执行的当前工作目录
            **kwargs: 传递给subprocess.Popen的其他参数
            
        Returns:
            tuple: (stdout, stderr, returncode)
        """
        import subprocess
        import shlex
        
        # 如果没有指定工作目录，使用当前目录
        if not cwd:
            cwd = os.getcwd()
        
        try:
            # 根据操作系统选择命令执行方式
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(
                    command,
                    cwd=cwd,
                    shell=True,text=True,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                    **kwargs
                )
            else:  # Linux/macOS
                process = subprocess.Popen(
                    shlex.split(command),
                    cwd=cwd,
                    shell=False,text=True,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                    **kwargs
                )
            
            # 获取命令输出和错误
            stdout, stderr = process.communicate()
            return stdout, stderr, process.returncode
        except Exception as e:
            return "", f"执行命令失败: {str(e)}", -1
    
    def execute_command(self, command, cwd=None):
        """
        API方法：执行系统命令
        Args:
            command (str): 要执行的命令字符串
            cwd (str): 命令执行的当前工作目录
        Returns:
            dict: 包含命令输出、错误和新工作目录的结果
        """
        try:
            # 如果没有指定工作目录，使用当前目录
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
                    return {
                        "output": f"切换到目录: {new_dir}",
                        "error": "",
                        "cwd": new_dir
                    }
                else:
                    return {
                        "output": "",
                        "error": f"目录不存在: {new_dir}",
                        "cwd": cwd
                    }
            
            # 使用通用模板执行命令
            stdout, stderr, returncode = self._execute_system_command(command, cwd)
            
            return {
                "output": stdout,
                "error": stderr,
                "cwd": cwd
            }
            
        except Exception as e:
            return {
                "output": "",
                "error": f"执行命令失败: {str(e)}",
                "cwd": cwd
            }
    
    def handle_github_import(self, github_url):
        """
        API方法：处理GitHub仓库导入
        Args:
            github_url (str): GitHub仓库地址
        Returns:
            dict: 导入结果
        """
        try:
            # 从URL中提取仓库信息
            repo_info = self._parse_github_url(github_url)
            
            if repo_info:
                owner, repo_name = repo_info
                print(f"提取到仓库信息: {owner}/{repo_name}")
                
                # 直接构建clone URL
                clone_url = f"https://github.com/{owner}/{repo_name}.git"
                
                # 使用git命令行测试连接
                return self._test_github_connection_with_git(clone_url)
            else:
                print("无法从URL中提取仓库信息")
                return {
                    "success": False,
                    "error": "无效的GitHub仓库URL格式",
                    "connected": False
                }
                
        except Exception as e:
            print(f"处理GitHub导入时发生错误: {str(e)}")
            return {
                "success": False,
                "error": f"处理GitHub导入时发生错误: {str(e)}",
                "connected": False
            }
            
    def _parse_github_url(self, url):
        """
        从GitHub URL中提取owner和repo_name
        Args:
            url (str): GitHub仓库URL
        Returns:
            tuple: (owner, repo_name) 或 None
        """
        # 支持多种GitHub URL格式
        patterns = [
            r'^https?://github\.com/([^/]+)/([^/\.]+)(?:\.git)?/?$',
            r'^git@github\.com:([^/]+)/([^/\.]+)(?:\.git)?$'
        ]
        
        import re
        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1), match.group(2)
        return None
        
    def _test_github_connection_with_git(self, github_url):
        """
        使用git命令行测试GitHub连接
        Args:
            github_url (str): GitHub仓库地址
        Returns:
            dict: 测试结果
        """
        try:
            test_command = f"git ls-remote --heads {github_url}"
            stdout, stderr, returncode = self._execute_system_command(test_command)
            
            if returncode == 0 and stdout:
                print(f"通过git命令行连接到GitHub仓库: {github_url}")
                return {
                    "success": True,
                    "message": f"成功连接到GitHub仓库: {github_url}",
                    "connected": True,
                    "clone_url": github_url
                }
            else:
                print(f"git命令行连接失败: {stderr.strip()}")
                return {
                    "success": False,
                    "error": f"无法连接到GitHub仓库: {stderr.strip()}",
                    "connected": False
                }
        except Exception as e:
            print(f"git命令行测试发生错误: {str(e)}")
            return {
                "success": False,
                "error": f"git命令行测试失败: {str(e)}",
                "connected": False
            }
    
    def git_clone(self, github_url, target_path):
        """
        API方法：执行Git克隆操作
        Args:
            github_url (str): GitHub仓库地址
            target_path (str): 克隆目标路径
        Returns:
            dict: 克隆结果
        """
        try:
            # 检查目标路径是否已经存在
            if os.path.exists(target_path):
                return {
                    "success": False,
                    "error": "目标路径已存在"
                }
            
            # 创建父目录（如果不存在）
            parent_dir = os.path.dirname(target_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            
            # 执行git clone命令
            clone_command = f"git clone {github_url} {target_path}"
            stdout, stderr, returncode = self._execute_system_command(clone_command)
            
            if returncode == 0:
                print(f"成功克隆仓库: {github_url} 到 {target_path}")
                return {
                    "success": True,
                    "message": "成功克隆仓库",
                    "output": stdout,
                    "error": stderr
                }
            else:
                print(f"克隆失败: {stderr.strip()}")
                return {
                    "success": False,
                    "error": f"克隆失败: {stderr.strip()}",
                    "output": stdout,
                    "stderr": stderr
                }
                
        except Exception as e:
            print(f"克隆发生错误: {str(e)}")
            return {
                "success": False,
                "error": f"克隆时发生错误: {str(e)}"
            }
    
    def git_pull(self, repo_path, remote_url=None):
        """
        API方法：执行Git拉取操作
        Args:
            repo_path (str): Git仓库路径
            remote_url (str, optional): 远程仓库URL，用于在拉取前关联仓库
        Returns:
            dict: 拉取结果
        """
        try:
            # 检查路径是否存在且是目录
            if not os.path.exists(repo_path):
                return {
                    "success": False,
                    "error": "仓库路径不存在"
                }
            
            if not os.path.isdir(repo_path):
                return {
                    "success": False,
                    "error": "指定路径不是目录"
                }
            
            # 检查是否是Git仓库
            if not self.is_git_repository(repo_path):
                return {
                    "success": False,
                    "error": "指定路径不是Git仓库"
                }
            
            # 如果提供了remote_url，则先关联仓库
            if remote_url:
                print(f"在拉取前关联仓库: {remote_url}")
                
                # 检查当前是否已有origin远程
                remote_check_command = "git remote -v"
                remote_stdout, remote_stderr, remote_returncode = self._execute_system_command(remote_check_command, cwd=repo_path)
                
                has_origin = "origin" in remote_stdout
                
                if has_origin:
                    # 更新现有的origin远程
                    remote_command = f"git remote set-url origin {remote_url}"
                    stdout, stderr, returncode = self._execute_system_command(remote_command, cwd=repo_path)
                else:
                    # 添加新的origin远程
                    remote_command = f"git remote add origin {remote_url}"
                    stdout, stderr, returncode = self._execute_system_command(remote_command, cwd=repo_path)
                
                if returncode != 0:
                    return {
                        "success": False,
                        "error": f"关联仓库失败: {stderr.strip()}"
                    }
                
                print(f"成功关联仓库: {remote_url}")
            
            # 首先尝试普通的git pull
            pull_command = "git pull"
            stdout, stderr, returncode = self._execute_system_command(pull_command, cwd=repo_path)
            
            if returncode == 0:
                print(f"成功拉取仓库: {repo_path}")
                return {
                    "success": True,
                    "message": "成功拉取仓库",
                    "output": stdout,
                    "error": stderr
                }
            else:
                # 检查是否是因为没有跟踪信息或HEAD不存在导致的失败
                error_lower = stderr.lower()
                if "no tracking information" in error_lower or "unknown revision or path" in error_lower or "ambiguous argument 'head'" in error_lower:
                    print("拉取失败，尝试直接拉取默认分支...")
                    
                    # 尝试直接拉取常见的默认分支
                    default_branches = ["main", "master"]
                    
                    for branch_name in default_branches:
                        print(f"尝试拉取origin/{branch_name}")
                        direct_pull_command = f"git pull origin {branch_name}"
                        direct_stdout, direct_stderr, direct_returncode = self._execute_system_command(direct_pull_command, cwd=repo_path)
                        
                        if direct_returncode == 0:
                            print(f"成功拉取{branch_name}分支")
                            return {
                                "success": True,
                                "message": f"成功拉取{branch_name}分支",
                                "output": f"{stdout}\n{direct_stdout}",
                                "error": f"{stderr}\n{direct_stderr}"
                            }
                    
                    # 如果所有默认分支都失败，尝试列出所有远程分支并拉取第一个
                    print("尝试列出远程分支...")
                    list_branches_command = "git branch -r"
                    branches_stdout, branches_stderr, branches_returncode = self._execute_system_command(list_branches_command, cwd=repo_path)
                    
                    if branches_returncode == 0:
                        # 解析远程分支列表，过滤出origin/开头的分支
                        remote_branches = []
                        for line in branches_stdout.splitlines():
                            branch = line.strip()
                            if branch.startswith("origin/") and not branch.endswith("HEAD -> origin/"):
                                remote_branches.append(branch[7:])  # 去掉origin/前缀
                        
                        if remote_branches:
                            # 尝试拉取第一个远程分支
                            first_branch = remote_branches[0]
                            print(f"尝试拉取第一个远程分支: {first_branch}")
                            first_branch_command = f"git pull origin {first_branch}"
                            first_stdout, first_stderr, first_returncode = self._execute_system_command(first_branch_command, cwd=repo_path)
                            
                            if first_returncode == 0:
                                print(f"成功拉取{first_branch}分支")
                                return {
                                    "success": True,
                                    "message": f"成功拉取{first_branch}分支",
                                    "output": f"{stdout}\n{first_stdout}",
                                    "error": f"{stderr}\n{first_stderr}"
                                }
                    
                    # 所有尝试都失败
                    print("所有拉取尝试都失败")
                    return {
                        "success": False,
                        "error": f"拉取失败: 无法找到可拉取的分支\n原始错误: {stderr.strip()}",
                            "output": stdout,
                            "stderr": stderr
                        }
                
                # 如果不是因为跟踪信息问题，直接返回失败
                print(f"拉取失败: {stderr.strip()}")
                return {
                    "success": False,
                    "error": f"拉取失败: {stderr.strip()}",
                    "output": stdout,
                    "stderr": stderr
                }
                
        except Exception as e:
            print(f"拉取发生错误: {str(e)}")
            return {
                "success": False,
                "error": f"拉取时发生错误: {str(e)}"
            }
    

    
    def associate_git_repo(self, repo_path, remote_url):
        """
        API方法：关联Git仓库
        Args:
            repo_path (str): Git仓库路径
            remote_url (str): 远程仓库URL
        Returns:
            dict: 关联结果
        """
        try:
            # 检查路径是否存在且是目录
            if not os.path.exists(repo_path):
                return {
                    "success": False,
                    "error": "仓库路径不存在"
                }
            
            if not os.path.isdir(repo_path):
                return {
                    "success": False,
                    "error": "指定路径不是目录"
                }
            
            # 检查是否是Git仓库，如果不是则初始化
            if not self.is_git_repository(repo_path):
                # 初始化Git仓库
                init_command = "git init"
                stdout_init, stderr_init, returncode_init = self._execute_system_command(init_command, cwd=repo_path)
                
                if returncode_init != 0:
                    return {
                        "success": False,
                        "error": f"初始化Git仓库失败: {stderr_init.strip()}"
                    }
            
            # 从URL中提取仓库信息，仅用于日志显示
            repo_info = self._parse_github_url(remote_url)
            if repo_info:
                print(f"检测到GitHub仓库: {repo_info[0]}/{repo_info[1]}")
            
            # 检查当前是否已有origin远程
            remote_check_command = "git remote -v"
            remote_stdout, remote_stderr, remote_returncode = self._execute_system_command(remote_check_command, cwd=repo_path)
            
            has_origin = "origin" in remote_stdout
            
            if has_origin:
                # 更新现有的origin远程
                remote_command = f"git remote set-url origin {remote_url}"
                stdout, stderr, returncode = self._execute_system_command(remote_command, cwd=repo_path)
            else:
                # 添加新的origin远程
                remote_command = f"git remote add origin {remote_url}"
                stdout, stderr, returncode = self._execute_system_command(remote_command, cwd=repo_path)
            
            if returncode == 0:
                print(f"成功关联仓库: {repo_path} -> {remote_url}")
                
                # 尝试获取远程分支信息
                try:
                    fetch_command = "git fetch origin"
                    fetch_stdout, fetch_stderr, fetch_returncode = self._execute_system_command(fetch_command, cwd=repo_path)
                    
                    # 尝试设置默认分支跟踪
                    if fetch_returncode == 0:
                        # 获取本地当前分支
                        branch_command = "git branch --show-current"
                        branch_stdout, branch_stderr, branch_returncode = self._execute_system_command(branch_command, cwd=repo_path)
                        
                        if branch_returncode == 0:
                            current_branch = branch_stdout.strip()
                            if current_branch:
                                # 设置跟踪关系
                                track_command = f"git branch --set-upstream-to=origin/{current_branch} {current_branch}"
                                track_stdout, track_stderr, track_returncode = self._execute_system_command(track_command, cwd=repo_path)
                                if track_returncode != 0:
                                    print(f"设置分支跟踪失败: {track_stderr.strip()}")
                except Exception as fetch_e:
                    print(f"获取远程分支信息时发生错误: {str(fetch_e)}")
                
                return {
                    "success": True,
                    "message": "成功关联仓库",
                    "output": stdout,
                    "error": stderr,
                    "remote_url": remote_url
                }
            else:
                print(f"关联失败: {stderr.strip()}")
                return {
                    "success": False,
                    "error": f"关联失败: {stderr.strip()}",
                    "output": stdout,
                    "stderr": stderr
                }
                
        except Exception as e:
            print(f"关联发生错误: {str(e)}")
            return {
                "success": False,
                "error": f"关联时发生错误: {str(e)}"
            }

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
