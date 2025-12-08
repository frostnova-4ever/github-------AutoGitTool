// appfunc.js - 主应用功能
// 文件操作相关功能已分离到file-operations.js

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
            const terminalContent = document.querySelector('.terminal-content');
            if (terminalContent) {
                terminalContent.innerHTML = '';
            }
        });
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



// 设置额外的事件监听器
function setupAdditionalEventListeners() {
    // 监听pywebviewready事件，确保JS API完全初始化
    window.addEventListener('_pywebviewready', () => {
        console.log('_pywebviewready事件触发，重新加载常用路径');
        loadCommonPaths();
    });

    // 测试按钮已移除，不再需要此事件监听器
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