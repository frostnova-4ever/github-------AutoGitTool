// file-operations.js - 文件操作相关功能

// 全局变量，供其他函数使用
const fileData = [];
const fileIcons = {
    folder: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z"/></svg>',
    document: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M13,9V3.5L18.5,9M6,2C4.89,2 4,2.89 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2H6Z"/></svg>'
};

// 向终端添加消息
function appendTerminal(msg, level = 'info') {
    const t = document.querySelector('.terminal-content');
    if (!t) return;
    const el = document.createElement('div');
    el.textContent = `${new Date().toLocaleTimeString()} ${msg}`;
    if (level === 'success') el.classList.add('status-success');
    if (level === 'error') el.classList.add('status-error');
    t.appendChild(el);
    t.scrollTop = t.scrollHeight;
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
    const list = document.querySelector('.file-list');
    if (!list) return;
    list.innerHTML = '';
    fileData.forEach(f => {
        const row = document.createElement('div');
        row.className = 'file-item-detailed';
        row.innerHTML = `
            <div class="file-cell file-size">${f.size || ''}</div>
            <div class="file-cell file-name">${f.name || ''}</div>
        `;
        row.addEventListener('click', () => appendTerminal(`点击: ${f.name}`));
        list.appendChild(row);
    });
}
