// page-operations.js - 页面操作相关功能

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
