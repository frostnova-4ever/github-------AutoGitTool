// ui-setup.js - UI设置相关功能

// 设置UI
function setupUI() {
    // 加载常用路径
    if (typeof loadCommonPaths === 'function') {
        loadCommonPaths();
    }

    // GitHub导入按钮事件监听器
    const githubBtn = document.getElementById('github-btn');
    if (githubBtn) {
        githubBtn.addEventListener('click', handleGitHubImport);
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
        rightListBtn.addEventListener('click', function() {
            // 获取输入框中的路径
            const pathInput = document.getElementById('right-panel-path-input');
            if (pathInput && pathInput.value.trim()) {
                // 如果输入框中有路径，直接加载
                loadFileList(pathInput.value);
            } else {
                // 如果输入框中没有路径，打开文件夹选择对话框
                selectFolder();
            }
        });
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
    const btnText = mainBtn.querySelector('.scm-btn-text');
    const dropdownArrow = document.getElementById('scm-dropdown-arrow');
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
        btnText.textContent = actionNames[currentAction];

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

    if (scmDropdown && mainBtn && dropdownMenu && btnText && dropdownArrow) {
        // 初始化按钮和菜单
        updateButtonAndMenu();

        // 检查Git仓库状态并显示/隐藏初始化按钮
        checkGitRepositoryStatus();

        // 主按钮点击事件：执行当前操作
        mainBtn.addEventListener('click', (e) => {
            // 如果点击的是下拉箭头，则不执行操作
            if (e.target === dropdownArrow || dropdownArrow.contains(e.target)) {
                return;
            }
            e.stopPropagation();

            // 模拟执行当前操作
            if (currentAction === 'commit' && commitInput) {
                const m = commitInput.value.trim();
                if (!m) { appendTerminal('请输入提交信息', 'error'); return; }
                appendTerminal(`提交: ${m}`);
                setTimeout(() => appendTerminal('已提交', 'success'), 800);
                commitInput.value = '';
            } else if (currentAction === 'push') {
                appendTerminal('推送中...');
                setTimeout(() => appendTerminal('推送完成', 'success'), 1000);
            } else if (currentAction === 'auto' && commitInput) {
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
        });

        // 下拉箭头点击事件：切换菜单显示/隐藏
        dropdownArrow.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            dropdownMenu.classList.toggle('show');
        });

        // 菜单项点击事件
        dropdownItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const action = item.getAttribute('data-action');

                // 更新当前按钮功能
                currentAction = action;

                // 更新按钮显示和菜单
                updateButtonAndMenu();

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

    // 监听GitHub输入框变化，用于动态更新按钮文字
    setupGitHubButtonTextUpdater();

    // GitHub API功能按钮事件

    // 调用loadConfigPath函数加载配置
    loadConfigPath();
}
