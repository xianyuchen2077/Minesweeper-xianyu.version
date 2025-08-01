@echo off
chcp 65001 >nul
echo ========================================
echo        扫雷游戏一键打包工具
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python环境
    echo 请先安装Python并添加到系统PATH
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo 正在安装必要的库...
pip install pillow pyinstaller --quiet
if errorlevel 1 (
    echo ❌ 安装库失败
    pause
    exit /b 1
)

echo ✅ 库安装完成
echo.

echo 正在清理旧文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM 保留排行榜文件，只删除exe文件
if exist "demo\扫雷游戏咸鱼版.exe" del /q "demo\扫雷游戏咸鱼版.exe"
if exist "demo" (
    echo ✅ 保留了demo文件夹中的排行榜文件
) else (
    mkdir "demo"
    echo ✅ 创建了demo文件夹
)

if exist "*.spec" del /q "*.spec"

echo ✅ 清理完成
echo.

echo 正在创建游戏图标...
python create_icon.py
if errorlevel 1 (
    echo ❌ 创建图标失败
    pause
    exit /b 1
)

echo ✅ 图标创建完成
echo.

echo 开始打包扫雷游戏...
echo 这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller --onefile --windowed --name=扫雷游戏咸鱼版 --add-data=leaderboard.json;. --distpath=demo --icon=icon.ico minesweeper.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！
    echo 请检查错误信息并重试
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 打包成功！
echo ========================================
echo.
echo 📁 可执行文件位置：demo\扫雷游戏咸鱼版.exe
echo 🎨 图标文件位置：icon.ico
echo.
echo 💡 提示：
echo    - 你可以将exe文件分享给其他人
echo    - 用户无需安装Python即可运行
echo    - 游戏会自动创建排行榜文件
echo    - exe文件已包含自定义图标
echo.
echo 按任意键打开demo文件夹...
pause >nul
explorer demo 