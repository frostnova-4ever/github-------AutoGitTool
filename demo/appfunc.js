// appfunc.js - 公共函数库

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

// 显示左侧页面
function showLeftPage(id, pushHash = true) {
    const left = document.querySelector('.left-content');
    if (!left) return;
    left.querySelectorAll('.left-page').forEach(p => {
        if (p.id === id) {
            p.style.display = '';
            p.setAttribute('aria-hidden', 'false');
        } else {
            p.style.display = 'none';
            p.setAttribute('aria-hidden', 'true');
        }
    });
    if (pushHash) {
        try { if (location.hash !== `#${id}`) location.hash = `#${id}`; } catch (e) {}
    }
    // 如果显示的是自动提交页面，尝试触发工作流画布刷新
    if (id === 'page-auto-submit' && typeof window.wf_refresh === 'function') {
        try { window.wf_refresh(); } catch (e) { console.error('wf_refresh error', e); }
    }
}

// 处理哈希变化
function handleHash() {
    const h = (location.hash || '').replace('#', '');
    if (h) showLeftPage(h, false);
}

// 设置节点信息
function setNodeInfo(info) {
    const name = document.getElementById('node-name');
    const status = document.getElementById('node-status');
    const last = document.getElementById('node-last');
    const details = document.getElementById('node-details');
    if (name) name.textContent = info.name || '本地节点';
    if (status) status.textContent = info.status || '空闲';
    if (last) last.textContent = info.last || '-';
    if (details) details.textContent = info.details || '-';
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
                    // 自动调用get_files API获取文件列表
                    window.pywebview.api.get_files(selectedPath)
                        .then(data => {
                            // 渲染文件列表
                            const fileList = document.getElementById('right-file-list');
                            if (fileList) {
                                fileList.innerHTML = '';
                                if (data.files && data.files.length > 0) {
                                    data.files.forEach(file => {
                                        const fileItem = document.createElement('div');
                                        fileItem.className = 'file-item';
                                        fileItem.style.display = 'flex';
                                        fileItem.style.padding = '5px 0';
                                        fileItem.innerHTML = `
                                            <div class="file-name" style="flex: 1;">${file.name}</div>
                                            <div class="file-size" style="width: 120px;">${file.size}</div>
                                        `;
                                        fileList.appendChild(fileItem);
                                    });
                                } else {
                                    fileList.innerHTML = '<div class="empty-message" style="padding: 10px; color: #666;">该目录为空</div>';
                                }
                            }
                        })
                        .catch(error => {
                            if (resultDiv) {
                                resultDiv.innerHTML += `\n$ 获取文件列表失败: ${error} [${timestamp}]`;
                            }
                        });
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

// 页面切换功能
function setupPageSwitching() {
    const menuItems = document.querySelectorAll('.menu-item');
    const pages = document.querySelectorAll('.left-page');

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有active类
            menuItems.forEach(i => i.classList.remove('active'));
            // 隐藏所有页面
            pages.forEach(page => page.style.display = 'none');

            // 设置当前active
            this.classList.add('active');
            const target = this.getAttribute('data-target');
            document.getElementById(target).style.display = 'block';
        });
    });
}

// 设置UI
function setupUI() {
    // 加载常用路径
    if (typeof loadCommonPaths === 'function') {
        loadCommonPaths();
    }

    document.querySelectorAll('.menu-item').forEach(mi => mi.addEventListener('click', ev => {
        ev.preventDefault();
        ev.stopPropagation();
        document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
        mi.classList.add('active');
        const target = mi.getAttribute('data-target');
        if (target) showLeftPage(target);
    }));

    window.addEventListener('hashchange', handleHash);

    const listBtn = document.getElementById('filemanager-list-btn');
    const pathInput = document.getElementById('filemanager-path-input');
    if (listBtn && pathInput) {
        listBtn.addEventListener('click', () => {
            const p = pathInput.value.trim() || './'; // 默认当前目录
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
        });
    }

    // 为左侧面板路径输入框添加"浏览..."按钮
    const leftPathInput = document.getElementById('filemanager-path-input');
    if (leftPathInput && !leftPathInput.parentElement.querySelector('.browse-btn')) {
        const browseBtn = document.createElement('button');
        browseBtn.className = 'browse-btn';
        browseBtn.textContent = '浏览...';
        browseBtn.style.marginLeft = '10px';
        browseBtn.style.padding = '8px 12px';
        browseBtn.style.backgroundColor = 'var(--primary-color)';
        browseBtn.style.color = 'white';
        browseBtn.style.border = 'none';
        browseBtn.style.borderRadius = '4px';
        browseBtn.style.cursor = 'pointer';

        browseBtn.addEventListener('click', () => {
            console.log('左侧面板浏览按钮被点击');
            if (window.pywebview && window.pywebview.api) {
                console.log('调用open_folder_dialog接口');
                window.pywebview.api.open_folder_dialog()
                    .then(selectedPath => {
                        console.log('选择的路径:', selectedPath);
                        if (selectedPath) {
                            leftPathInput.value = selectedPath;
                            appendTerminal(`选择了路径: ${selectedPath}`, 'success');
                        }
                    })
                    .catch(error => {
                        console.error('打开文件夹对话框失败:', error);
                        appendTerminal(`打开文件夹失败: ${error}`, 'error');
                    });
            } else {
                console.error('webview API不可用');
                appendTerminal('无法连接到文件系统', 'error');
            }
        });

        leftPathInput.parentElement.appendChild(browseBtn);
    }

    // 右侧面板的列出路径按钮事件监听器
    const rightListBtn = document.getElementById('right-panel-list-btn');
    if (rightListBtn) {
        rightListBtn.addEventListener('click', selectFolder);
    }

    const commitBtn = document.getElementById('commit-btn');
    const pushBtn = document.getElementById('push-btn');
    const commitInput = document.getElementById('commit-input');
    const autoBtn = document.getElementById('auto-btn');
    if (commitBtn && commitInput) commitBtn.addEventListener('click', () => {
        const m = commitInput.value.trim();
        if (!m) { appendTerminal('请输入提交信息', 'error'); return; }
        appendTerminal(`提交: ${m}`);
        setTimeout(() => appendTerminal('已提交', 'success'), 800);
        commitInput.value = '';
    });
    if (pushBtn) pushBtn.addEventListener('click', () => {
        appendTerminal('推送中...');
        setTimeout(() => appendTerminal('推送完成', 'success'), 1000);
    });
    if (autoBtn) autoBtn.addEventListener('click', () => {
        if (commitInput) commitInput.value = commitInput.value || '自动提交';
        if (commitBtn) commitBtn.click();
        if (pushBtn) setTimeout(() => pushBtn.click(), 900);
    });

    // 自动提交页面交互
    const start = document.getElementById('auto-start-btn');
    const stop = document.getElementById('auto-stop-btn');
    if (start && stop) {
        start.addEventListener('click', function() {
            start.style.display = 'none';
            stop.style.display = '';
            setNodeInfo({
                name: '本地节点',
                status: '运行中',
                last: new Date().toLocaleString(),
                details: '自动任务已启动（主界面）。'
            });
        });
        stop.addEventListener('click', function() {
            stop.style.display = 'none';
            start.style.display = '';
            setNodeInfo({
                name: '本地节点',
                status: '已停止',
                last: new Date().toLocaleString(),
                details: '自动任务已停止（主界面）。'
            });
        });
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
    const pathInput = document.querySelector(inputSelector);
    if (!pathInput) return;

    const pathInputContainer = pathInput.parentElement;

    // 检查是否已经添加了浏览按钮，避免重复添加
    if (pathInputContainer.querySelector('.browse-btn')) {
        return;
    }

    // 创建路径选择按钮
    const browseBtn = document.createElement('button');
    browseBtn.className = 'browse-btn';
    browseBtn.textContent = '浏览...';
    browseBtn.style.padding = '8px 12px';
    browseBtn.style.border = '1px solid var(--border-color)';
    browseBtn.style.borderRadius = '4px';
    browseBtn.style.cursor = 'pointer';
    browseBtn.style.marginLeft = '5px';

    // 创建模态弹窗
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    modal.style.zIndex = '10000';
    modal.style.display = 'none';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';

    // 创建弹窗内容
    const modalContent = document.createElement('div');
    modalContent.style.backgroundColor = 'white';
    modalContent.style.borderRadius = '8px';
    modalContent.style.width = '500px';
    modalContent.style.maxHeight = '80vh';
    modalContent.style.overflow = 'hidden';
    modalContent.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';

    // 弹窗标题
    const modalTitle = document.createElement('div');
    modalTitle.textContent = '选择路径';
    modalTitle.style.padding = '16px';
    modalTitle.style.fontSize = '18px';
    modalTitle.style.fontWeight = 'bold';
    modalTitle.style.borderBottom = '1px solid var(--border-color)';

    // 弹窗内容区域
    const modalBody = document.createElement('div');
    modalBody.style.padding = '16px';
    modalBody.style.maxHeight = '60vh';
    modalBody.style.overflowY = 'auto';

    // 添加系统文件夹选择按钮
    const systemFolderBtn = document.createElement('button');
    systemFolderBtn.textContent = '选择系统文件夹...';
    systemFolderBtn.style.padding = '12px';
    systemFolderBtn.style.cursor = 'pointer';
    systemFolderBtn.style.border = '1px solid var(--primary-color)';
    systemFolderBtn.style.borderRadius = '4px';
    systemFolderBtn.style.marginBottom = '16px';
    systemFolderBtn.style.backgroundColor = 'var(--primary-color)';
    systemFolderBtn.style.color = 'white';
    systemFolderBtn.style.width = '100%';
    systemFolderBtn.style.fontWeight = 'bold';

    // 点击系统文件夹按钮时调用系统文件夹选择对话框
    systemFolderBtn.addEventListener('click', () => {
        if (window.pywebview && window.pywebview.api) {
            window.pywebview.api.open_folder_dialog()
                .then(selectedPath => {
                    if (selectedPath) {
                        pathInput.value = selectedPath;
                        modal.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('打开系统文件夹对话框失败:', error);
                });
        }
    });

    modalBody.appendChild(systemFolderBtn);

    // 添加分隔线
    const separator = document.createElement('div');
    separator.style.height = '1px';
    separator.style.backgroundColor = 'var(--border-color)';
    separator.style.marginBottom = '16px';
    modalBody.appendChild(separator);

    // 添加路径选项
    paths.forEach(path => {
        const pathItem = document.createElement('div');
        pathItem.className = 'path-option';
        pathItem.innerHTML = `
            <div style="font-weight: bold;">${path.name}</div>
            <div style="color: #666; font-size: 14px; margin-top: 2px;">${path.path}</div>
        `;
        pathItem.style.padding = '12px';
        pathItem.style.cursor = 'pointer';
        pathItem.style.borderBottom = '1px solid var(--border-color)';
        pathItem.style.borderRadius = '4px';
        pathItem.style.marginBottom = '8px';
        pathItem.style.backgroundColor = '#f9f9f9';

        // 点击路径选项时设置到输入框
        pathItem.addEventListener('click', () => {
            pathInput.value = path.path;
            modal.style.display = 'none';
        });

        // 悬停效果
        pathItem.addEventListener('mouseover', () => {
            pathItem.style.backgroundColor = 'var(--hover-bg-color)';
        });

        pathItem.addEventListener('mouseout', () => {
            pathItem.style.backgroundColor = '#f9f9f9';
        });

        modalBody.appendChild(pathItem);
    });

    // 弹窗底部
    const modalFooter = document.createElement('div');
    modalFooter.style.padding = '16px';
    modalFooter.style.borderTop = '1px solid var(--border-color)';
    modalFooter.style.textAlign = 'right';

    // 取消按钮
    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = '取消';
    cancelBtn.style.padding = '8px 16px';
    cancelBtn.style.border = '1px solid var(--border-color)';
    cancelBtn.style.borderRadius = '4px';
    cancelBtn.style.cursor = 'pointer';
    cancelBtn.style.marginRight = '8px';

    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // 确认按钮
    const confirmBtn = document.createElement('button');
    confirmBtn.textContent = '确认';
    confirmBtn.style.padding = '8px 16px';
    confirmBtn.style.border = '1px solid var(--border-color)';
    confirmBtn.style.borderRadius = '4px';
    confirmBtn.style.cursor = 'pointer';
    confirmBtn.style.backgroundColor = 'var(--primary-color)';
    confirmBtn.style.color = 'white';

    confirmBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    modalFooter.appendChild(cancelBtn);
    modalFooter.appendChild(confirmBtn);

    // 组装弹窗
    modalContent.appendChild(modalTitle);
    modalContent.appendChild(modalBody);
    modalContent.appendChild(modalFooter);
    modal.appendChild(modalContent);

    // 点击弹窗外部关闭
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // 显示弹窗
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        modal.style.display = 'flex';
    });

    // 将元素添加到DOM
    pathInputContainer.appendChild(browseBtn);
    document.body.appendChild(modal);
}

// 设置额外的事件监听器
function setupAdditionalEventListeners() {
    // 监听pywebviewready事件，确保JS API完全初始化
    window.addEventListener('_pywebviewready', () => {
        console.log('_pywebviewready事件触发，重新加载常用路径');
        loadCommonPaths();
    });

    // 为测试按钮添加点击事件处理程序
    document.addEventListener('DOMContentLoaded', () => {
        const testBtn = document.getElementById('test-list-paths-btn');
        if (testBtn) {
            testBtn.addEventListener('click', () => {
                console.log('测试按钮被点击，调用list_paths方法');
                loadCommonPaths();
            });
        }
    });
}

// 在DOM加载完成后执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setupUI();
        setupAdditionalEventListeners();
    });
} else {
    setupUI();
    setupAdditionalEventListeners();
}