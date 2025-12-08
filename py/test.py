import webview

# 全局窗口变量
global_window = None

# 创建一个简单的HTML内容用于触发文件夹选择
test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>文件夹选择测试</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        button {
            padding: 12px 24px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin: 20px auto;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
            width: 80%;
            max-width: 600px;
            text-align: left;
        }
        .selected-path {
            font-family: monospace;
            background-color: #e0e0e0;
            padding: 5px 10px;
            border-radius: 3px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <h1>文件夹选择测试</h1>
    <p>点击按钮选择一个文件夹：</p>
    <button onclick="selectFolder()">选择文件夹</button>
    <div class="result" id="result"></div>
    
    <script>
        function selectFolder() {
            if (window.pywebview && window.pywebview.api) {
                window.pywebview.api.open_folder_dialog()
                    .then(selectedPath => {
                        const resultDiv = document.getElementById('result');
                        if (selectedPath) {
                            resultDiv.innerHTML = 
                                '<strong>已选择文件夹：</strong><br>' +
                                '<div class="selected-path">' + selectedPath + '</div>';
                        } else {
                            resultDiv.innerHTML = '<strong>未选择任何文件夹</strong>';
                        }
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = 
                            '<strong style="color: red;">选择失败：</strong>' + error;
                    });
            } else {
                alert('pywebview API不可用');
            }
        }
    </script>
</body>
</html>
"""

class Api:
    def open_folder_dialog(self):
        """
        打开文件夹选择对话框
        
        Returns:
            str: 选中的文件夹路径，如果用户取消则返回None
        """
        global global_window
        try:
            if global_window:
                # 使用新的FileDialog.FOLDER方式
                result = global_window.create_file_dialog(
                    dialog_type=webview.FileDialog.FOLDER,
                    allow_multiple=False
                )
                
                if result and len(result) > 0:
                    return result[0]
            return None
        except Exception as e:
            print(f"打开文件夹对话框失败: {str(e)}")
            return None

def on_window_loaded():
    """
    窗口加载完成后的回调函数
    """
    global global_window
    print("窗口已加载完成")

if __name__ == '__main__':
    try:
        # 创建API实例
        api = Api()
        
        # 创建窗口并显示测试HTML
        global_window = webview.create_window(
            '文件夹选择测试',
            html=test_html,
            js_api=api,
            width=800,
            height=500,
            resizable=True
        )
        
        # 启动应用
        webview.start(on_window_loaded, debug=True)
    except Exception as e:
        print(f"启动应用失败: {str(e)}")
