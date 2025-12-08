const express = require('express');
const fs = require('fs');
const path = require('path');
const util = require('util');

const app = express();
const port = process.env.PORT || 3000;

// 根目录限制：默认使用当前工作目录，可以通过环境变量 ROOT_DIR 指定
const ROOT_DIR = process.env.ROOT_DIR ? path.resolve(process.env.ROOT_DIR) : process.cwd();

app.use(express.static(__dirname));

// 列出目录接口：只允许在 ROOT_DIR 之下访问，防止任意文件读取
app.get('/api/list', async(req, res) => {
    const queryPath = req.query.path;
    if (!queryPath) {
        return res.status(400).send('missing path parameter');
    }

    // 将用户输入解析为绝对路径。如果传入相对路径，视作相对于 ROOT_DIR
    let requestedPath = queryPath;
    try {
        if (!path.isAbsolute(requestedPath)) {
            requestedPath = path.join(ROOT_DIR, requestedPath);
        }
        requestedPath = path.resolve(requestedPath);
    } catch (e) {
        return res.status(400).send('invalid path');
    }

    // 检查请求路径是否在允许的根目录下
    if (!requestedPath.startsWith(ROOT_DIR)) {
        return res.status(403).send('forbidden path');
    }

    try {
        const dirents = await fs.promises.readdir(requestedPath, { withFileTypes: true });
        const results = [];

        for (const d of dirents) {
            try {
                const full = path.join(requestedPath, d.name);
                const stat = await fs.promises.stat(full);
                const isDirectory = stat.isDirectory();
                results.push({
                    name: d.name,
                    path: full,
                    isDirectory,
                    size: stat.size,
                    mtime: stat.mtime.toISOString(),
                    ext: isDirectory ? '' : path.extname(d.name).replace('.', '').toLowerCase(),
                    sizeDisplay: isDirectory ? '' : formatBytes(stat.size)
                });
            } catch (eInner) {
                // 忽略单个文件的读取错误
            }
        }

        res.json(results);
    } catch (err) {
        // 更明确的错误码：路径不存在或不可读返回 404
        if (err && (err.code === 'ENOENT' || err.code === 'ENOTDIR')) {
            return res.status(404).send('not found');
        }
        res.status(500).send(String(err.message));
    }
});

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

app.listen(port, () => {
    console.log(`Server listening on http://localhost:${port}`);
});