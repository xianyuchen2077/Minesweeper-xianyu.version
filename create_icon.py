from PIL import Image, ImageDraw, ImageFont
import os

def create_minesweeper_icon():
    """创建扫雷游戏图标"""
    # ==================== 图标尺寸设置 ====================
    # 修改这里的数字来改变整个图标的大小
    # 推荐尺寸：256, 128, 64, 32, 16
    # 当前设置为256（标准尺寸）
    size = 256

    # 根据尺寸自动调整缩放比例
    scale_factor = size / 256  # 以256为基准计算缩放比例
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ==================== 颜色配置 ====================
    # 修改RGB值来改变颜色 (红, 绿, 蓝)
    background_color = (135, 206, 235)  # 背景颜色——浅蓝色
    border_color = (200, 162, 200)      # 边框颜色——浅紫色
    cell_color = (128, 128, 128)        # 格子颜色——灰色
    mine_color = (0, 0, 0)              # 地雷颜色——黑色
    flag_color = (255, 0, 0)            # 旗子颜色——红色

    # ==================== 背景和边框设置 ====================
    # 绘制背景
    draw.rectangle([0, 0, size, size], fill=background_color)

    # 边框设置
    # 根据尺寸自动调整边框粗细
    border_width = max(1, int(8 * scale_factor))  # 最小1像素，确保边框可见
    draw.rectangle([border_width, border_width, size-border_width, size-border_width],
                outline=border_color, width=border_width)

    # ==================== 网格设置 ====================
    # 修改这个数字来改变网格的大小（比如改为4就是4x4网格）
    grid_size = 3

    # 计算格子大小（自动根据图标尺寸调整）
    # 边距根据尺寸自动调整
    margin = max(4, int(20 * scale_factor))  # 最小4像素边距
    cell_size = max(4, (size - 2 * border_width - 2 * margin) // grid_size)  # 最小4像素格子

    # 网格起始位置（距离边框的距离）
    # 根据尺寸自动调整位置
    start_x = border_width + margin
    start_y = border_width + margin

    # ==================== 绘制格子 ====================
    for i in range(grid_size):
        for j in range(grid_size):
            x = start_x + i * cell_size
            y = start_y + j * cell_size

            # 绘制格子背景
            # 格子间距根据尺寸自动调整
            spacing = max(1, int(2 * scale_factor))  # 最小1像素间距
            # 确保坐标有效
            rect_x1 = min(x + cell_size - spacing, size - 1)
            rect_y1 = min(y + cell_size - spacing, size - 1)
            draw.rectangle([x, y, rect_x1, rect_y1],
                        fill=cell_color, outline=(169, 169, 169))

            # ==================== 地雷设置 ====================
            # 修改这里的条件来改变地雷的位置
            # 当前设置在中心格子 (1,1)，可以改为其他位置
            if i == 1 and j == 1:
                # 地雷位置（中心点）
                center_x = x + cell_size // 2
                center_y = y + cell_size // 2

                # 地雷大小 - 修改//4来改变地雷的大小
                radius = cell_size // 4
                draw.ellipse([center_x - radius, center_y - radius,
                            center_x + radius, center_y + radius],
                            fill=mine_color)

                # 地雷爆炸效果
                # 爆炸线条粗细根据尺寸自动调整
                explosion_width = max(1, int(3 * scale_factor))  # 最小1像素
                for angle in range(0, 360, 45):
                    import math
                    rad = math.radians(angle)
                    end_x = center_x + int(radius * 1.5 * math.cos(rad))
                    end_y = center_y + int(radius * 1.5 * math.sin(rad))
                    draw.line([center_x, center_y, end_x, end_y],
                            fill=mine_color, width=explosion_width)

            # ==================== 旗子设置 ====================
            # 修改这里的条件来改变旗子的位置
            # 当前设置在左上角格子 (0,0)，可以改为其他位置
            elif i == 0 and j == 0:
                # 旗子位置 - 根据尺寸自动调整
                flag_x = x + cell_size // 2.5
                flag_y = y + cell_size // 5

                # 旗子大小 - 根据尺寸自动调整
                flag_size = cell_size // 1.5

                # 旗杆 - 粗细根据尺寸自动调整
                flag_pole_width = max(1, int(2 * scale_factor))  # 最小1像素
                draw.line([flag_x, flag_y, flag_x, flag_y + flag_size],
                        fill=(139, 69, 19), width=flag_pole_width)

                # 旗子形状
                # 修改//2和//4来改变旗子的形状
                draw.polygon([flag_x, flag_y, flag_x + flag_size//2, flag_y + flag_size//4,
                            flag_x, flag_y + flag_size//2], fill=flag_color)

    # ==================== 保存设置 ====================
    # 图标文件名 - 修改"icon.ico"来改变保存的文件名
    icon_path = "icon.ico"

    # 保存为ICO文件，包含多种尺寸
    # 修改sizes列表来改变生成的图标尺寸
    # 推荐尺寸：[256, 128, 64, 32, 16]
    img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

    print(f"✅ 图标已创建: {icon_path}")
    print(f"图标尺寸: {size}x{size} 像素")
    print("图标包含以下元素:")
    print(f"- 背景颜色: RGB{background_color}")
    print(f"- 边框颜色: RGB{border_color}")
    print(f"- 格子颜色: RGB{cell_color}")
    print(f"- 地雷颜色: RGB{mine_color}")
    print(f"- 旗子颜色: RGB{flag_color}")
    print(f"- 网格大小: {grid_size}x{grid_size}")
    print(f"- 缩放比例: {scale_factor:.2f}x")

    return icon_path

if __name__ == "__main__":
    try:
        create_minesweeper_icon()
    except ImportError:
        print("❌ 需要安装Pillow库来创建图标")
        print("请运行: pip install pillow")
    except Exception as e:
        print(f"❌ 创建图标失败: {e}")