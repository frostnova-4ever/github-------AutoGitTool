// appfunc.js - 主应用功能
// 文件操作相关功能已分离到file-operations.js

// 显示左侧页面
function showLeftPage(id, pushHash = true) {
    const left = document.querySelector('.middle-panel');
    const rightPanel = document.querySelector('.right-panel');
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

    // 处理工作流页面的特殊显示逻辑
    if (id === 'page-workflow') {
        // 隐藏右侧面板
        if (rightPanel) {
            rightPanel.style.display = 'none';
        }
        // 确保工作流页面的iframe能够填充空间
        const workflowPage = document.getElementById('page-workflow');
        if (workflowPage) {
            workflowPage.style.display = 'flex';
            workflowPage.style.width = '100%';
            workflowPage.style.height = '100%';
        }
        const workflowIframe = document.getElementById('workflow-iframe');
        if (workflowIframe) {
            workflowIframe.style.width = '100%';
            workflowIframe.style.height = '100%';
        }
    } else {
        // 显示右侧面板
        if (rightPanel) {
            rightPanel.style.display = 'flex';
        }
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



// 页面切换功能
function setupPageSwitching() {
    const menuItems = document.querySelectorAll('.menu-item');
    const pages = document.querySelectorAll('.left-page');
    const rightPanel = document.querySelector('.right-panel');

    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有active类
            menuItems.forEach(i => i.classList.remove('active'));
            // 隐藏所有页面
            pages.forEach(page => page.style.display = 'none');

            // 设置当前active
            this.classList.add('active');
            const target = this.getAttribute('data-target');
            const targetPage = document.getElementById(target);
            targetPage.style.display = 'block';

            // 处理工作流页面的特殊显示逻辑
            if (target === 'page-workflow') {
                // 隐藏右侧面板
                if (rightPanel) {
                    rightPanel.style.display = 'none';
                }
                // 确保工作流页面的iframe能够填充空间
                targetPage.style.display = 'flex';
                targetPage.style.width = '100%';
                targetPage.style.height = '100%';
                const workflowIframe = document.getElementById('workflow-iframe');
                if (workflowIframe) {
                    workflowIframe.style.width = '100%';
                    workflowIframe.style.height = '100%';
                }
            } else {
                // 显示右侧面板
                if (rightPanel) {
                    rightPanel.style.display = 'flex';
                }
            }
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

    // 左侧面板路径输入框已移除，相关事件监听器代码已删除

    // 左侧面板的浏览按钮已移除

    // 右侧面板的列出路径按钮事件监听器
    const rightListBtn = document.getElementById('right-panel-list-btn');
    if (rightListBtn) {
        rightListBtn.addEventListener('click', selectFolder);
    }

    // 清空终端按钮事件监听器
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            // 调用终端的clear命令
            executeClear();
        });
    }

    const commitInput = document.getElementById('commit-input');

    // 下拉菜单交互功能
    const scmDropdown = document.querySelector('.scm-dropdown');
    const mainBtn = document.getElementById('scm-main-btn');
    const dropdownMenu = document.getElementById('scm-dropdown-menu');
    const dropdownItems = document.querySelectorAll('.scm-dropdown-item');

    // 设置按钮当前功能
    let currentAction = 'commit';
    const actionNames = {
        'commit': '提交',
        'push': '推送',
        'auto': '提交并推送'
    };

    // 更新按钮显示和下拉菜单
    function updateButtonAndMenu() {
        // 更新按钮文字
        mainBtn.innerHTML = `${actionNames[currentAction]}<span class="scm-dropdown-arrow">▼</span>`;

        // 更新下拉菜单项
        dropdownItems.forEach(item => {
            const action = item.getAttribute('data-action');
            if (action === currentAction) {
                // 隐藏当前功能的选项
                item.style.display = 'none';
            } else {
                // 显示其他功能选项
                item.style.display = 'block';
                // 更新菜单项文字
                if (action === 'commit') {
                    item.textContent = '提交';
                } else if (action === 'push') {
                    item.textContent = '推送';
                } else if (action === 'auto') {
                    item.textContent = '提交并推送';
                }
            }
        });
    }

    if (scmDropdown && mainBtn && dropdownMenu) {
        // 初始化按钮和菜单
        updateButtonAndMenu();

        // 检查Git仓库状态并显示/隐藏初始化按钮
        checkGitRepositoryStatus();

        // 主按钮点击事件：切换菜单显示/隐藏
        mainBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        });

        // 菜单项点击事件
        dropdownItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const action = item.getAttribute('data-action');

                // 更新当前按钮功能（无论操作是否成功都会切换）
                currentAction = action;

                // 更新按钮显示和菜单
                updateButtonAndMenu();

                // 执行对应操作
                if (action === 'commit' && commitInput) {
                    const m = commitInput.value.trim();
                    if (!m) { appendTerminal('请输入提交信息', 'error'); return; }
                    appendTerminal(`提交: ${m}`);
                    setTimeout(() => appendTerminal('已提交', 'success'), 800);
                    commitInput.value = '';
                } else if (action === 'push') {
                    appendTerminal('推送中...');
                    setTimeout(() => appendTerminal('推送完成', 'success'), 1000);
                } else if (action === 'auto' && commitInput) {
                    commitInput.value = commitInput.value || '自动提交';

                    // 模拟提交
                    const m = commitInput.value.trim();
                    appendTerminal(`提交: ${m}`);
                    setTimeout(() => {
                        appendTerminal('已提交', 'success');

                        // 延迟后模拟推送
                        appendTerminal('推送中...');
                        setTimeout(() => appendTerminal('推送完成', 'success'), 1000);
                    }, 800);

                    commitInput.value = '';
                }

                // 关闭菜单
                dropdownMenu.classList.remove('show');
            });
        });

        // 点击页面其他地方关闭菜单
        document.addEventListener('click', () => {
            dropdownMenu.classList.remove('show');
        });

        // 防止菜单内部点击事件冒泡
        dropdownMenu.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

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

    // Git初始化按钮点击事件
    const gitInitBtn = document.getElementById('git-init-btn');
    if (gitInitBtn) {
        gitInitBtn.addEventListener('click', function() {
            if (window.pywebview && window.pywebview.api) {
                window.pywebview.api.execute_command('git init', currentWorkingDirectory)
                    .then(response => {
                        if (response.output) {
                            appendTerminal(response.output, 'info');
                        }
                        if (response.error) {
                            appendTerminal(response.error, 'error');
                        } else {
                            appendTerminal('Git仓库初始化成功', 'success');
                            // 重新检查Git仓库状态，隐藏初始化按钮
                            checkGitRepositoryStatus();
                        }
                    })
                    .catch(error => {
                        appendTerminal(`执行git init命令失败: ${error}`, 'error');
                    });
            }
        });
    }
}



// 检查Git仓库状态
function checkGitRepositoryStatus() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.is_git_repository(currentWorkingDirectory)
            .then(isGit => {
                const initBtn = document.getElementById('git-init-btn');
                if (initBtn) {
                    initBtn.style.display = isGit ? 'none' : 'inline-block';
                }
            })
            .catch(error => {
                console.error('检查Git仓库状态失败:', error);
            });
    }
}

// 设置额外的事件监听器
function setupAdditionalEventListeners() {
    // 监听pywebviewready事件，确保JS API完全初始化
    window.addEventListener('_pywebviewready', () => {
        console.log('_pywebviewready事件触发，重新加载常用路径');
        loadCommonPaths();
    });

    // 初始化终端
    if (typeof initTerminal === 'function') {
        initTerminal();
    }

    // 测试按钮已移除，不再需要此事件监听器
}

// 全局目录切换事件处理函数
window.onDirectoryChanged = function(newPath) {
    // 重新检查Git仓库状态
    checkGitRepositoryStatus();
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