// main.js - 主入口文件，整合所有功能模块

// 导入各个功能模块
// 注意：由于浏览器不支持ES6模块语法，我们将通过HTML文件中的script标签顺序来确保依赖关系

// 页面加载完成后初始化应用
function initApp() {
    // 设置UI
    if (typeof setupUI === 'function') {
        setupUI();
    }

    // 设置页面切换
    if (typeof setupPageSwitching === 'function') {
        setupPageSwitching();
    }

    // 设置额外事件监听器
    if (typeof setupAdditionalEventListeners === 'function') {
        setupAdditionalEventListeners();
    }

    // 初始化Git相关功能
    if (typeof setupGitHubButtonTextUpdater === 'function') {
        setupGitHubButtonTextUpdater();
    }

    // 检查Git仓库状态
    if (typeof checkGitRepositoryStatus === 'function') {
        checkGitRepositoryStatus();
    }
}

// 在DOM加载完成后执行初始化
function onDOMLoaded() {
    initApp();

    // 确保加载配置路径
    if (typeof loadConfigPath === 'function') {
        loadConfigPath();
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onDOMLoaded);
} else {
    onDOMLoaded();
}