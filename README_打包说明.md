# 扫雷游戏打包说明

## 方法一：一键打包（推荐）

1. **运行一键打包脚本**
   ```bash
   一键打包.bat
   ```

2. **等待打包完成**
   - 脚本会自动安装必要的库
   - 自动生成游戏图标
   - 打包过程可能需要几分钟
   - 完成后会在`demo`文件夹中生成`扫雷游戏咸鱼版.exe`

## 方法二：使用Python脚本

1. **运行打包脚本**
   ```bash
   python build.py
   ```

2. **等待打包完成**
   - 脚本会自动安装PyInstaller（如果未安装）
   - 打包过程可能需要几分钟
   - 完成后会在`demo`文件夹中生成`扫雷游戏咸鱼版.exe`

## 方法三：手动打包

1. **安装PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **执行打包命令**
   ```bash
   pyinstaller --onefile --windowed --name=扫雷游戏咸鱼版 --add-data=leaderboard.json;. --distpath=demo --icon=icon.ico minesweeper.py
   ```

## 打包参数说明

- `--onefile`: 打包成单个exe文件
- `--windowed`: 不显示控制台窗口
- `--name=扫雷游戏咸鱼版`: 设置exe文件名
- `--add-data=leaderboard.json;.`: 包含排行榜文件
- `--distpath=demo`: 输出到demo文件夹
- `--icon=icon.ico`: 设置图标

## 文件结构

打包后的文件结构：
```
demo/
└── 扫雷游戏咸鱼版.exe    # 可执行文件
```

## 注意事项

1. **文件大小**: 打包后的exe文件大约20-50MB
2. **运行环境**: 不需要安装Python，可以在任何Windows系统上运行
3. **排行榜**: 排行榜数据会保存在exe同目录下的`leaderboard.json`文件中
4. **杀毒软件**: 某些杀毒软件可能会误报，这是正常现象

## 分发说明

1. 将`demo/扫雷游戏咸鱼版.exe`文件分享给其他人
2. 用户双击即可运行，无需安装任何依赖
3. 游戏会自动创建排行榜文件
4. exe文件包含自定义扫雷图标

## 故障排除

如果打包失败：
1. 确保Python环境正确
2. 检查是否有足够的磁盘空间
3. 尝试以管理员身份运行命令提示符
4. 检查防火墙和杀毒软件设置