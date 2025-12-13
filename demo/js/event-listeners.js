// event-listeners.js - 事件监听器相关功能

// 设置额外的事件监听器
function setupAdditionalEventListeners() {
    // 监听pywebviewready事件，确保JS API完全初始化
    window.addEventListener('_pywebviewready', () => {
        loadCommonPaths();
        loadConfigPath();
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
