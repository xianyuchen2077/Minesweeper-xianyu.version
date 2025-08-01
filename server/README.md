# 扫雷排行榜服务器

## 部署到Railway（免费）

### 1. 注册Railway账号
- 访问 https://railway.app/
- 使用GitHub账号登录

### 2. 创建新项目
- 点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 选择你的GitHub仓库

### 3. 自动部署
- Railway会自动检测到Flask应用
- 自动安装依赖并启动服务器

### 4. 获取服务器地址
- 部署完成后，Railway会提供一个URL
- 例如：https://your-app-name.railway.app

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