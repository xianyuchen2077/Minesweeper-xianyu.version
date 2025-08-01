# 扫雷排行榜服务器

## 部署到Railway（免费）

### 1. 注册Railway账号
- 访问 https://railway.app/
- 使用GitHub账号登录

### 2. 创建新项目
- 点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 选择你的GitHub仓库
- **重要：确保选择 `server` 文件夹作为根目录**

### 3. 配置部署
- Railway会自动检测到Flask应用
- 自动安装依赖并启动服务器
- 如果遇到"no start command could be found"错误，请检查：
  - 确保选择了正确的根目录（`server` 文件夹）
  - 确保 `requirements.txt` 文件存在
  - 确保 `Procfile` 或 `railway.json` 配置正确

### 4. 获取服务器地址
- 部署完成后，Railway会提供一个URL
- 例如：https://your-app-name.railway.app

### 5. 故障排除

#### 如果遇到"no start command could be found"错误：
1. 检查项目根目录是否正确（应该是 `server` 文件夹）
2. 确保以下文件存在：
   - `requirements.txt`
   - `Procfile` 或 `railway.json`
   - `app.py`

#### 如果遇到端口错误：
- Railway会自动设置 `PORT` 环境变量
- 应用会自动使用正确的端口

## API接口

### 添加成绩
```
POST /api/scores
Content-Type: application/json

{
    "name": "玩家名",
    "difficulty": "9x9_10",
    "time": 45
}
```

### 获取排行榜
```
GET /api/scores/9x9_10
```

### 获取所有排行榜
```
GET /api/scores
```

### 健康检查
```
GET /api/health
```

## 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行服务器
python app.py

# 访问 http://localhost:5000
```

## 文件说明

- `app.py` - Flask应用主文件
- `requirements.txt` - Python依赖包
- `Procfile` - Railway启动命令配置
- `railway.json` - Railway详细配置
- `leaderboard.db` - SQLite数据库文件（自动创建）