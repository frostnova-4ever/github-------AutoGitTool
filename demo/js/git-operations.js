// git-operations.js - Git相关功能

// 检查Git仓库状态并显示/隐藏初始化按钮
function checkGitRepositoryStatus() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.is_git_repository(currentWorkingDirectory)
            .then(response => {
                const gitInitBtn = document.getElementById('git-init-btn');
                if (gitInitBtn) {
                    if (response.is_git_repository) {
                        gitInitBtn.style.display = 'none';
                    } else {
                        gitInitBtn.style.display = 'block';
                    }
                }
            })
            .catch(error => {
                console.error('检查Git仓库状态失败:', error);
            });
    }
}

// 设置GitHub按钮文字更新器
function setupGitHubButtonTextUpdater() {
    const githubInput = document.getElementById('github-input');
    const githubBtn = document.getElementById('github-btn');

    if (githubInput && githubBtn) {
        githubInput.addEventListener('input', function() {
            updateButtonText(githubInput, githubBtn);
        });

        // 初始加载时也检查一次
        updateButtonText(githubInput, githubBtn);
    }
}

// 处理GitHub导入
function handleGitHubImport() {
    const githubInput = document.getElementById('github-input');
    if (!githubInput || !githubInput.value.trim()) {
        appendTerminal('请输入GitHub仓库地址', 'error');
        return;
    }

    const repoUrl = githubInput.value.trim();
    appendTerminal(`开始处理GitHub仓库: ${repoUrl}`);

    // 输入验证
    if (!isValidGitHubUrl(repoUrl)) {
        appendTerminal('无效的GitHub仓库地址', 'error');
        return;
    }

    // 连接后端API
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.import_github_repo(repoUrl, currentWorkingDirectory)
            .then(response => {
                if (response.success) {
                    appendTerminal('Git仓库克隆成功', 'success');
                    // 检查仓库是否已有文件
                    updateButtonText(githubInput, document.getElementById('github-btn'));
                    // 重新检查Git仓库状态
                    checkGitRepositoryStatus();
                } else {
                    appendTerminal(`Git操作失败: ${response.error}`, 'error');
                }
            })
            .catch(error => {
                appendTerminal(`API调用失败: ${error}`, 'error');
            });
    } else {
        appendTerminal('pywebview API不可用', 'error');
    }
}

// 验证GitHub URL
function isValidGitHubUrl(url) {
    const githubRegex = /^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+(\.git)?$/;
    return githubRegex.test(url);
}
