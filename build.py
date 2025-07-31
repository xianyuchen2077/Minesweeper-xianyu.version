import os
import subprocess
import sys

def build_exe():
    """打包扫雷游戏为exe文件"""
    print("开始打包扫雷游戏...")

    # 检查PyInstaller是否已安装
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",                        # 打包成单个exe文件
        "--windowed",                       # 不显示控制台窗口
        "--name=扫雷游戏咸鱼版",             # 设置exe文件名
        "--icon=icon.ico",                  # 图标文件
        "--add-data=leaderboard.json;.",    # 包含排行榜文件
        "--distpath=demo",                  # 输出到demo文件夹
        "minesweeper.py"                    # 主程序文件
    ]

    # 确保图标文件存在
    if not os.path.exists("icon.ico"):
        print("正在生成图标文件...")
        try:
            import create_icon
            create_icon.create_minesweeper_icon()
        except Exception as e:
            print(f"生成图标失败: {e}")
            cmd.remove("--icon=icon.ico")
            print("将使用默认图标")
    else:
        print("✅ 找到图标文件: icon.ico")

    print("执行打包命令:", " ".join(cmd))

    try:
        subprocess.check_call(cmd)
        print("\n✅ 打包成功！")
        print("exe文件位置: demo/扫雷游戏咸鱼版.exe")
        print("你可以将demo文件夹中的exe文件分享给其他人使用")

    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

    return True

if __name__ == "__main__":
    build_exe()