// 精简版 app.js：保留必要代码，移除多余注释与重复片段

const fileData = [
    { name: '文档', type: 'folder', date: '2023-10-15 14:30', size: '' },
    { name: '项目文档.pdf', type: 'document', date: '2023-10-14 09:15', size: '2.4 MB' },
    { name: '产品图片.jpg', type: 'image', date: '2023-10-12 11:20', size: '1.2 MB' },
    { name: '宣传视频.mp4', type: 'video', date: '2023-10-11 10:05', size: '24.8 MB' }
];

const fileIcons = {
    folder: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z"/></svg>',
    document: '<svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M13,9V3.5L18.5,9M6,2C4.89,2 4,2.89 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2H6Z"/></svg>'
};

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

function handleHash() {
    const h = (location.hash || '').replace('#', '');
    if (h) showLeftPage(h, false);
}

function setupUI() {
    document.querySelectorAll('.menu-item').forEach(mi => mi.addEventListener('click', ev => {
        ev.preventDefault();
        ev.stopPropagation();
        document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
        mi.classList.add('active');
        const target = mi.getAttribute('data-target');
        if (target) showLeftPage(target);
    }));

    window.addEventListener('hashchange', handleHash);

    const listBtn = document.getElementById('list-btn');
    const pathInput = document.getElementById('path-input');
    if (listBtn && pathInput) {
        listBtn.addEventListener('click', async() => {
            const p = pathInput.value.trim();
            if (!p) { appendTerminal('错误: 请输入路径', 'error'); return; }
            appendTerminal(`请求目录: ${p}`);
            try {
                const res = await fetch(`/api/list?path=${encodeURIComponent(p)}`);
                if (!res.ok) { appendTerminal(`错误: ${res.status} ${res.statusText}`, 'error'); return; }
                const data = await res.json();
                if (Array.isArray(data)) {
                    fileData.length = 0;
                    data.forEach(f => fileData.push({ name: f.name || '', type: f.isDirectory ? 'folder' : (f.ext || 'file'), date: f.mtime || '', size: f.sizeDisplay || '' }));
                    renderFileList();
                    appendTerminal(`列出完成: ${p}`, 'success');
                }
            } catch (e) { appendTerminal(`请求失败: ${e.message || e}`, 'error'); }
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

    // 窗口控制与刷新按钮绑定
    const minimizeBtn = document.querySelector('.minimize-btn');
    const maximizeBtn = document.querySelector('.maximize-btn');
    const closeBtn = document.querySelector('.close-btn');
    if (minimizeBtn) minimizeBtn.addEventListener('click', () => appendTerminal('最小化窗口'));
    if (maximizeBtn) maximizeBtn.addEventListener('click', () => appendTerminal('最大化窗口'));
    if (closeBtn) closeBtn.addEventListener('click', () => appendTerminal('关闭窗口'));

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) refreshBtn.addEventListener('click', renderFileList);

    // 初始化左侧菜单为默认页面（文件管理器），避免重复的 DOMContentLoaded 绑定
    document.querySelectorAll('.menu-item').forEach(i => i.classList.remove('active'));
    const defaultMenuItem = document.querySelector('.menu-item[data-target="page-filemanager"]') || document.querySelector('.menu-item');
    if (defaultMenuItem) defaultMenuItem.classList.add('active');
    showLeftPage('page-filemanager', false);

    renderFileList();
    handleHash();
}

// 启动应用
window.addEventListener('DOMContentLoaded', setupUI);