// file-operations.js - 文件操作相关功能

// 全局变量，供其他函数使用
const fileData = [];
const fileIcons = {
    folder: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z"/></svg>',
    document: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M13,9V3.5L18.5,9M6,2C4.89,2 4,2.89 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2H6Z"/></svg>'
};

// 当前工作目录
let currentWorkingDirectory = 'C:\\Users\\Documents';

// 目录切换事件监听器
function onDirectoryChanged(newPath) {
    currentWorkingDirectory = newPath;
    // 通知其他模块目录已改变
    if (window.onDirectoryChanged) {
        window.onDirectoryChanged(newPath);
    }
}

// 向终端添加消息
function appendTerminal(msg, level = 'info') {
    const terminalContent = document.getElementById('terminal-content');
    if (!terminalContent) return;

    const line = document.createElement('div');
    line.className = `terminal-line ${level}`;
    line.textContent = msg;

    terminalContent.appendChild(line);
    terminalContent.scrollTop = terminalContent.scrollHeight;
}

// 处理终端输入
function handleTerminalInput() {
    const terminalInput = document.getElementById('terminal-input');
    const terminalContent = document.getElementById('terminal-content');

    if (!terminalInput || !terminalContent) return;

    // 获取用户输入的命令
    const command = terminalInput.value.trim();
    if (!command) return;

    // 显示用户输入的命令
    const userInputLine = document.createElement('div');
    userInputLine.className = 'terminal-line user-input';
    userInputLine.innerHTML = `<span class="prompt">$</span> ${command}`;
    terminalContent.appendChild(userInputLine);

    // 清空输入框
    terminalInput.value = '';

    // 执行命令
    executeCommand(command);

    // 滚动到底部
    terminalContent.scrollTop = terminalContent.scrollHeight;
}

// 执行命令
function executeCommand(command) {
    // 发送命令到Python后端执行
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.execute_command(command, currentWorkingDirectory)
            .then(response => {
                // 显示命令输出
                if (response.output) {
                    appendTerminal(response.output, 'info');
                }
                // 显示命令错误
                if (response.error) {
                    appendTerminal(response.error, 'error');
                }
                // 更新当前工作目录
                if (response.cwd && response.cwd !== currentWorkingDirectory) {
                    onDirectoryChanged(response.cwd);
                }
            })
            .catch(error => {
                appendTerminal(`执行命令失败: ${error}`, 'error');
            });
    } else {
        // 如果pywebview API不可用，使用模拟实现
        appendTerminal(`执行命令: ${command}`, 'info');
        appendTerminal('(仅模拟模式 - 实际命令需在完整环境中执行)', 'warning');
    }
}

// 执行 ls 命令
function executeLs(args) {
    // 如果有路径参数，使用该路径，否则使用当前目录
    const path = args.length > 0 ? args[0] : currentWorkingDirectory;

    // 调用 webview API 获取文件列表
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_files(path)
            .then(response => {
                if (response.error) {
                    appendTerminal(`错误: ${response.error}`, 'error');
                } else {
                    if (Array.isArray(response.contents)) {
                        response.contents.forEach(f => {
                            let line = '';
                            if (f.is_file) {
                                line = `${f.name} (${f.size_formatted})`;
                            } else {
                                line = `${f.name}/`;
                            }
                            appendTerminal(line, 'info');
                        });
                    }
                }
            })
            .catch(error => {
                appendTerminal(`获取文件列表失败: ${error}`, 'error');
            });
    } else {
        // 模拟输出
        appendTerminal('模拟文件列表:', 'info');
        appendTerminal('file1.txt (1.2 KB)', 'info');
        appendTerminal('file2.js (3.4 KB)', 'info');
        appendTerminal('folder1/', 'info');
        appendTerminal('folder2/', 'info');
    }
}

// 执行 pwd 命令
function executePwd() {
    appendTerminal(currentWorkingDirectory, 'info');
}

// 执行 cd 命令
function executeCd(args) {
    if (args.length === 0) {
        // 切换到用户目录
        currentWorkingDirectory = 'C:\\Users\\';
    } else if (args[0] === '..') {
        // 切换到父目录
        const parts = currentWorkingDirectory.split('\\');
        if (parts.length > 1) {
            parts.pop();
            currentWorkingDirectory = parts.join('\\');
        }
    } else {
        // 切换到指定目录
        const newPath = args[0].startsWith('\\') ? args[0] : `${currentWorkingDirectory}\\${args[0]}`;
        currentWorkingDirectory = newPath;
    }
    appendTerminal(currentWorkingDirectory, 'info');
}

// 执行 clear 命令
function executeClear() {
    const terminalContent = document.getElementById('terminal-content');
    if (terminalContent) {
        terminalContent.innerHTML = '';
        appendTerminal('欢迎使用系统终端!', 'success');
        appendTerminal('您可以执行任何系统命令，例如: dir, cd, mkdir, python 等。', 'info');
        appendTerminal('输入 help 查看系统命令帮助。', 'info');
        appendTerminal('当前工作目录: ' + currentWorkingDirectory, 'info');
        appendTerminal('', 'info');
    }
}

// 执行 help 命令
function executeHelp() {
    appendTerminal('可用命令:', 'info');
    appendTerminal('ls [path] - 列出文件和目录', 'info');
    appendTerminal('pwd - 显示当前工作目录', 'info');
    appendTerminal('cd [path] - 切换目录', 'info');
    appendTerminal('clear - 清空终端', 'info');
    appendTerminal('help - 显示帮助信息', 'info');
}

// 初始化终端
function initTerminal() {
    const terminalInput = document.getElementById('terminal-input');

    if (terminalInput) {
        // 添加回车键事件监听
        terminalInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                handleTerminalInput();
            }
        });

        // 显示欢迎信息
        appendTerminal('欢迎使用系统终端!', 'success');
        appendTerminal('您可以执行任何系统命令，例如: dir, cd, mkdir, python 等。', 'info');
        appendTerminal('输入 help 查看系统命令帮助。', 'info');
        appendTerminal('当前工作目录: ' + currentWorkingDirectory, 'info');
        appendTerminal('', 'info');

        // 自动聚焦到输入框
        terminalInput.focus();
    }
}

// 选择文件夹功能
function selectFolder() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.open_folder_dialog()
            .then(selectedPath => {
                const resultDiv = document.querySelector('.terminal-content');
                const pathInput = document.getElementById('right-panel-path-input');
                if (selectedPath) {
                    // 填充路径到输入框
                    pathInput.value = selectedPath;
                    // 更新终端信息
                    if (resultDiv) {
                        const timestamp = new Date().toLocaleString();
                        resultDiv.innerHTML += `\n$ 已选择文件夹: ${selectedPath} [${timestamp}]`;
                    }
                    // 自动调用loadFileList函数获取文件列表
                    loadFileList(selectedPath);
                } else {
                    if (resultDiv) {
                        const timestamp = new Date().toLocaleString();
                        resultDiv.innerHTML += `\n$ 未选择任何文件夹 [${timestamp}]`;
                    }
                }
            })
            .catch(error => {
                const resultDiv = document.querySelector('.terminal-content');
                if (resultDiv) {
                    const timestamp = new Date().toLocaleString();
                    resultDiv.innerHTML += `\n$ 选择文件夹失败: ${error} [${timestamp}]`;
                }
            });
    } else {
        alert('pywebview API不可用');
    }
}

// 加载常用路径
function loadCommonPaths() {
    // 检查webview API是否可用
    console.log('loadCommonPaths: 开始');
    console.log('loadCommonPaths: window.pywebview:', window.pywebview);
    console.log('loadCommonPaths: window.pywebview.api:', window.pywebview ? window.pywebview.api : '不可用');

    if (window.pywebview && window.pywebview.api) {
        // 调用list_paths接口获取常用路径
        console.log('loadCommonPaths: 调用window.pywebview.api.list_paths()');
        window.pywebview.api.list_paths()
            .then(response => {
                console.log('loadCommonPaths: list_paths响应:', response);

                if (response.error) {
                    console.error('获取常用路径失败:', response.error);
                    appendTerminal(`获取常用路径失败: ${response.error}`, 'error');
                } else if (Array.isArray(response.paths)) {
                    console.log('loadCommonPaths: 调用createPathSelector()');
                    // 创建路径选择下拉菜单
                    createPathSelector(response.paths);
                } else {
                    console.error('list_paths返回的数据格式不正确:', response);
                    appendTerminal('获取常用路径失败: 数据格式不正确', 'error');
                }
            })
            .catch(error => {
                console.error('调用list_paths接口失败:', error);
                appendTerminal(`调用list_paths接口失败: ${error}`, 'error');
            });
    } else {
        console.error('webview API不可用');
        appendTerminal('无法连接到文件系统', 'error');
    }
}

// 创建路径选择模态弹窗
function createPathSelector(paths) {
    // 为左侧面板添加路径选择按钮
    addPathSelectorToPanel('#filemanager-path-input', paths);

    // 为右侧面板添加路径选择按钮
    addPathSelectorToPanel('#right-panel-path-input', paths);
}

// 为指定面板添加路径选择功能
function addPathSelectorToPanel(inputSelector, paths) {
    // 浏览按钮已移除，不再创建路径选择功能
    return;
}

// 全局函数：加载文件列表
function loadFileList(path) {
    const p = path.trim();
    if (!p) return; // 如果路径为空，不执行

    appendTerminal(`请求目录: ${p}`);
    // 调用webview的JavaScript API获取文件列表
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_files(p)
            .then(response => {
                if (response.error) {
                    appendTerminal(`错误: ${response.error}`, 'error');
                } else {
                    // 使用返回的文件数据渲染文件列表
                    if (Array.isArray(response.contents)) {
                        fileData.length = 0;
                        response.contents.forEach(f => {
                            // 确定文件类型
                            let type = f.is_file ? 'file' : 'folder';

                            // 如果是文件，根据扩展名确定类型
                            if (f.is_file) {
                                const ext = f.name.split('.').pop().toLowerCase();
                                if (['pdf', 'doc', 'docx', 'txt'].includes(ext)) {
                                    type = 'document';
                                } else if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) {
                                    type = 'image';
                                } else if (['mp4', 'avi', 'mov'].includes(ext)) {
                                    type = 'video';
                                }
                            }

                            fileData.push({
                                name: f.name || '',
                                type: type,
                                date: f.modified_time || '',
                                size: f.size_formatted || ''
                            });
                        });
                        renderFileList();
                        appendTerminal(`列出完成: ${response.path || p}`, 'success');
                    }
                }
            })
            .catch(error => {
                appendTerminal(`获取文件列表失败: ${error}`, 'error');
            });
    } else {
        appendTerminal('无法连接到文件系统', 'error');
    }
}

// 渲染文件列表
function renderFileList() {
    const fileList = document.querySelector('.file-list');
    if (!fileList) return;

    fileList.innerHTML = '';
    fileData.forEach(f => {
        const row = document.createElement('div');
        row.className = 'file-item-detailed';
        row.innerHTML = `
            <div class="file-cell file-size">${f.size || ''}</div>
            <div class="file-cell file-name">${f.name || ''}</div>
        `;
        row.addEventListener('click', () => appendTerminal(`点击: ${f.name}`));
        fileList.appendChild(row);
    });
}