// config.js - 配置相关功能

// 加载配置路径
function loadConfigPath() {
    // 检查路径输入框是否存在
    const pathInput = document.getElementById('right-panel-path-input');
    if (!pathInput) {
        console.error('路径输入框不存在');
        return;
    }

    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.get_config_path()
            .then(response => {
                if (response && response.success) {
                    if (response.path) {
                        pathInput.value = response.path;
                        // 调用loadFileList函数列出该路径下的文件
                        if (typeof loadFileList === 'function') {
                            loadFileList(response.path);
                        } else {
                            console.error('loadFileList函数不存在');
                        }
                    }
                } else {
                    console.error('获取配置路径失败:', response.error);
                }
            })
            .catch(error => {
                console.error('调用get_config_path接口失败:', error);
            });
    } else {
        // 如果pywebview API不可用，尝试使用本地存储的路径
        const storedPath = localStorage.getItem('currentPath');
        if (storedPath) {
            pathInput.value = storedPath;
            // 调用loadFileList函数列出该路径下的文件
            if (typeof loadFileList === 'function') {
                loadFileList(storedPath);
            } else {
                console.error('loadFileList函数不存在');
            }
        }
    }
}

// 导出函数，便于调试
window.loadConfigPath = loadConfigPath;

// 在页面加载完成后延迟执行，确保DOM完全加载
window.addEventListener('load', () => {
    setTimeout(() => {
        loadConfigPath();
    }, 1000); // 延迟1秒执行


});