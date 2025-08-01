import tkinter as tk
from tkinter import messagebox
from typing import Optional
import time
import json
import os
from board import Board

class MinesweeperGUI:
    def __init__(self, master, rows=9, cols=9, mines=10):
        self.master = master
        self.board = Board(rows, cols, mines)
        self.buttons: list[list[Optional[tk.Button]]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.game_started = False
        self.start_time = 0
        self.timer_running = False
        self.is_paused = False
        self.pause_time = 0                                 # 暂停的累计时间
        self.current_difficulty = f"{rows}x{cols}_{mines}"  # 当前难度标识
        self.leaderboard_file = "leaderboard.json"
        self.create_menu()
        self.create_widgets(rows, cols)
        self.create_timer()
        self.update_buttons()

    def load_leaderboard(self):
        """加载排行榜数据"""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_leaderboard(self, leaderboard):
        """保存排行榜数据"""
        with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, ensure_ascii=False, indent=2)

    def add_score(self, difficulty, player_name, time_seconds):
        """添加新成绩到排行榜"""
        leaderboard = self.load_leaderboard()

        if difficulty not in leaderboard:
            leaderboard[difficulty] = []

        # 添加新成绩
        leaderboard[difficulty].append({
            "name": player_name,
            "time": time_seconds
        })

        # 按时间排序（时间越短越好）
        leaderboard[difficulty].sort(key=lambda x: x["time"])

        # 只保留前10名
        leaderboard[difficulty] = leaderboard[difficulty][:10]

        self.save_leaderboard(leaderboard)
        return True

    def show_leaderboard(self):
        """显示排行榜"""
        leaderboard = self.load_leaderboard()

        dialog = tk.Toplevel(self.master)
        dialog.title("排行榜")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.configure(bg='lightyellow')

        # 居中显示
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")

        # 标题
        tk.Label(dialog, text="🏆 排行榜 🏆",
                font=("楷体", 24, "bold"),
                bg='lightyellow', fg='darkorange').pack(pady=10)

        # 创建滚动框架
        canvas = tk.Canvas(dialog, bg='lightyellow')
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='lightyellow')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 难度名称映射
        difficulty_names = {
            "9x9_10": "基础难度",
            "16x16_40": "普通难度",
            "16x30_99": "困难难度"
        }

        # 显示每个难度的排行榜
        for difficulty, scores in leaderboard.items():
            if not scores:  # 跳过空排行榜
                continue

            # 难度标题
            diff_name = difficulty_names.get(difficulty, f"自定义难度 ({difficulty})")
            tk.Label(scrollable_frame, text=f"📊 {diff_name}",
                    font=("楷体", 16, "bold"),
                    bg='lightyellow', fg='darkblue').pack(pady=(20, 10))

            # 成绩列表
            for i, score in enumerate(scores, 1):
                rank_emoji = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"#{i}"
                score_text = f"{rank_emoji} {score['name']} - {score['time']}秒"
                tk.Label(scrollable_frame, text=score_text,
                        font=("楷体", 12),
                        bg='lightyellow', fg='black').pack(pady=2)

            tk.Label(scrollable_frame, text="─" * 30,
                    font=("楷体", 12),
                    bg='lightyellow', fg='gray').pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # 按钮框架
        button_frame = tk.Frame(dialog, bg='lightyellow')
        button_frame.pack(pady=10)

        # 关闭按钮
        tk.Button(button_frame, text="关闭",
                font=("楷体", 12, "bold"),
                bg='lightcoral', fg='darkred',
                command=dialog.destroy).pack(padx=10)

    def show_name_input(self, time_seconds):
        """显示用户名输入对话框"""
        dialog = tk.Toplevel(self.master)
        dialog.title("记录成绩")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.configure(bg='lightgreen')

        # 居中显示
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"400x350+{x}+{y}")

        # 标题
        tk.Label(dialog, text="🎉 恭喜获胜！",
                font=("楷体", 20, "bold"),
                bg='lightgreen', fg='darkgreen').pack(pady=20)

        tk.Label(dialog, text=f"用时: {time_seconds} 秒",
                font=("楷体", 16, "bold"),
                bg='lightgreen', fg='darkgreen').pack(pady=10)

        tk.Label(dialog, text="请输入你的名字:",
                font=("楷体", 14),
                bg='lightgreen', fg='darkgreen').pack(pady=10)

        # 输入框
        name_var = tk.StringVar()
        name_entry = tk.Entry(dialog, textvariable=name_var,
                            font=("楷体", 14), width=20)
        name_entry.pack(pady=10)
        name_entry.focus()

        # 状态标签
        status_label = tk.Label(dialog, text="",
                            font=("楷体", 10),
                            bg='lightgreen', fg='gray')
        status_label.pack(pady=5)

        def save_score():
            player_name = name_var.get().strip()
            if not player_name:
                messagebox.showerror("错误", "请输入名字")
                return

            # 禁用按钮防止重复提交
            save_btn.config(state='disabled')
            status_label.config(text="正在保存成绩...", fg='blue')
            dialog.update()

            # 添加成绩到排行榜
            success = self.add_score(self.current_difficulty, player_name, time_seconds)

            if success:
                status_label.config(text="✅ 成绩保存成功！", fg='green')
                dialog.after(1500, dialog.destroy)  # 1.5秒后自动关闭
                messagebox.showinfo("成功", f"成绩已保存！\n{player_name} - {time_seconds}秒")
            else:
                status_label.config(text="❌ 保存失败", fg='red')
                save_btn.config(state='normal')  # 重新启用按钮

        # 按钮框架
        button_frame = tk.Frame(dialog, bg='lightgreen')
        button_frame.pack(pady=20)

        save_btn = tk.Button(button_frame, text="保存成绩",
                font=("楷体", 14, "bold"),
                bg='lightblue', fg='darkblue',
                command=save_score)
        save_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="跳过",
                font=("楷体", 14, "bold"),
                bg='lightcoral', fg='darkred',
                command=dialog.destroy).pack(side=tk.LEFT, padx=10)

        # 回车键绑定
        name_entry.bind('<Return>', lambda e: save_score())

    def create_timer(self):
        # 创建顶部框架，包含时间和暂停按钮
        self.top_frame = tk.Frame(self.master, bg='lightgray')
        self.top_frame.grid(row=0, column=0, columnspan=self.board.cols, sticky='ew', pady=5)

        # 配置列权重让时间标签居中
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)
        self.top_frame.grid_columnconfigure(2, weight=1)

        # 左侧占位
        tk.Label(self.top_frame, text="", bg='lightgray').grid(row=0, column=0)

        # 中间时间标签
        self.timer_label = tk.Label(self.top_frame, text="时间: 0秒",
                                font=("楷体", 16, "bold"),
                                bg='lightgray', fg='darkblue')
        self.timer_label.grid(row=0, column=1, padx=10)

        # 右侧暂停按钮
        self.pause_button = tk.Button(self.top_frame, text="⏸️暂停",
                                    font=("楷体", 12, "bold"),
                                    bg='lightyellow', fg='darkred',
                                    command=self.toggle_pause)
        self.pause_button.grid(row=0, column=2, sticky='e', padx=10)

        # 启动计时器更新
        self.update_timer()

    def update_timer(self):
        if self.game_started and not self.board.game_over and not self.board.is_win() and not self.is_paused:
            elapsed_time = int(time.time() - self.start_time - self.pause_time)
            self.timer_label.config(text=f"时间: {elapsed_time} 秒")
        self.master.after(1000, self.update_timer)  # 每秒更新一次

    def toggle_pause(self):
        """切换暂停状态"""
        if not self.game_started or self.board.game_over or self.board.is_win():
            return

        if self.is_paused:
            # 恢复游戏
            self.is_paused = False
            self.pause_time += time.time() - self.pause_start_time
            self.pause_button.config(text="⏸️暂停", bg='lightyellow')
        else:
            # 暂停游戏
            self.is_paused = True
            self.pause_start_time = time.time()
            self.pause_button.config(text="▶️继续", bg='lightcoral')

    def resume_from_pause(self):
        """从暂停状态恢复（点击方格时调用）"""
        if self.is_paused:
            self.is_paused = False
            self.pause_time += time.time() - self.pause_start_time
            self.pause_button.config(text="⏸️暂停", bg='lightyellow')

    def start_game_timer(self):
        if not self.game_started:
            self.game_started = True
            self.start_time = time.time()
            self.pause_time = 0
            self.is_paused = False

    def create_widgets(self, rows, cols):
        for r in range(rows):
            for c in range(cols):
                btn = tk.Button(self.master, width=4, height=2,     # 改成正方形，调大一点
                                command=lambda x=r, y=c: self.on_left_click(x, y))
                btn.bind('<Button-3>', lambda e, x=r, y=c: self.on_right_click(x, y))
                btn.grid(row=r+1, column=c)                         # 从第1行开始，第0行是计时器
                self.buttons[r][c] = btn

    def create_menu(self):
        menubar = tk.Menu(self.master)
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0, font=("楷体", 11))
        game_menu.add_command(label="新游戏", command=self.restart_game)
        game_menu.add_separator()

        # 难度子菜单
        difficulty_menu = tk.Menu(game_menu, tearoff=0, font=("楷体", 11))
        difficulty_menu.add_command(label="基础 (9x9, 10雷)", command=lambda: self.change_difficulty(9, 9, 10))
        difficulty_menu.add_command(label="普通 (16x16, 40雷)", command=lambda: self.change_difficulty(16, 16, 40))
        difficulty_menu.add_command(label="困难 (16x30, 99雷)", command=lambda: self.change_difficulty(16, 30, 99))
        difficulty_menu.add_separator()
        difficulty_menu.add_command(label="自定义难度", command=self.show_custom_difficulty)
        game_menu.add_cascade(label="难度", menu=difficulty_menu)

        game_menu.add_separator()
        game_menu.add_command(label="排行榜", command=self.show_leaderboard)
        game_menu.add_command(label="退出", command=self.master.quit)
        menubar.add_cascade(label="游戏", menu=game_menu)
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0, font=("楷体", 11))
        help_menu.add_command(label="关于游戏", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        self.master.config(menu=menubar)

    def change_difficulty(self, rows, cols, mines):
        """改变游戏难度"""
        self.board = Board(rows, cols, mines)
        self.game_started = False
        self.start_time = 0
        self.pause_time = 0
        self.is_paused = False
        self.timer_label.config(text="时间: 0")
        self.pause_button.config(text="⏸️暂停", bg='lightyellow')
        self.current_difficulty = f"{rows}x{cols}_{mines}"

        # 重新创建按钮网格
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]

        # 重新配置顶部框架的列数
        self.top_frame.grid_configure(columnspan=cols)

        self.create_widgets(rows, cols)
        self.update_buttons()

    def show_custom_difficulty(self):
        """显示自定义难度对话框"""
        dialog = tk.Toplevel(self.master)
        dialog.title("自定义难度")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.configure(bg='lightblue')

        # 居中显示
        dialog.transient(self.master)
        dialog.grab_set()
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")

        # 标题
        tk.Label(dialog, text="自定义难度设置",
                font=("楷体", 20, "bold"),
                bg='lightblue', fg='darkblue').pack(pady=20)

        # 输入框架
        input_frame = tk.Frame(dialog, bg='lightblue')
        input_frame.pack(pady=20)

        # 行数输入
        tk.Label(input_frame, text="行数:", font=("楷体", 12), bg='lightblue').grid(row=0, column=0, padx=10, pady=5)
        rows_var = tk.StringVar(value="9")
        rows_entry = tk.Entry(input_frame, textvariable=rows_var, width=10, font=("楷体", 12))
        rows_entry.grid(row=0, column=1, padx=10, pady=5)

        # 列数输入
        tk.Label(input_frame, text="列数:", font=("楷体", 12), bg='lightblue').grid(row=1, column=0, padx=10, pady=5)
        cols_var = tk.StringVar(value="9")
        cols_entry = tk.Entry(input_frame, textvariable=cols_var, width=10, font=("楷体", 12))
        cols_entry.grid(row=1, column=1, padx=10, pady=5)

        # 雷数输入
        tk.Label(input_frame, text="雷数:", font=("楷体", 12), bg='lightblue').grid(row=2, column=0, padx=10, pady=5)
        mines_var = tk.StringVar(value="10")
        mines_entry = tk.Entry(input_frame, textvariable=mines_var, width=10, font=("楷体", 12))
        mines_entry.grid(row=2, column=1, padx=10, pady=5)

        # 按钮框架
        button_frame = tk.Frame(dialog, bg='lightblue')
        button_frame.pack(pady=30)

        def start_custom_game():
            try:
                rows = int(rows_var.get())
                cols = int(cols_var.get())
                mines = int(mines_var.get())

                # 验证输入
                if rows < 5 or rows > 16:
                    messagebox.showerror("错误", "行数必须在5-16之间")
                    return
                if cols < 5 or cols > 30:
                    messagebox.showerror("错误", "列数必须在5-30之间")
                    return
                if mines < 1 or mines > rows * cols - 9:
                    messagebox.showerror("错误", f"雷数必须在1-{rows * cols - 9}之间")
                    return

                dialog.destroy()
                self.change_difficulty(rows, cols, mines)

            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")

        tk.Button(button_frame, text="开始游戏",
                font=("楷体", 14, "bold"),
                bg='lightgreen', fg='darkgreen',
                command=start_custom_game).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="取消",
                font=("楷体", 14, "bold"),
                bg='lightcoral', fg='darkred',
                command=dialog.destroy).pack(side=tk.LEFT, padx=10)

    def restart_game(self):
        # 重新开始游戏，保持当前难度
        current_rows = self.board.rows
        current_cols = self.board.cols
        current_mines = self.board.mines
        self.change_difficulty(current_rows, current_cols, current_mines)

    def show_about(self):
        messagebox.showinfo("关于游戏", "扫雷游戏\n作者：咸鱼\n时间：2025.7.31\npython库：使用tkinter实现\n作者自述：坐高铁，闲的慌，ai写一半，我写一半")

    def on_left_click(self, x, y):
        # 如果游戏暂停，自动恢复
        self.resume_from_pause()

        # 第一次点击时启动计时器
        self.start_game_timer()

        if self.board.grid[x][y].revealed:
            # 添加功能一键展开
            if self.board.grid[x][y].adjacent_mines == self.board.grid[x][y].flagged_adjacent_mines:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = x + dr, y + dc
                        if 0 <= nr < self.board.rows and 0 <= nc < self.board.cols:
                            if not self.board.grid[nr][nc].revealed and not self.board.grid[nr][nc].flagged:
                                self.board.reveal(nr, nc)
                self.update_buttons()   # 更新界面显示
                # 检查一键展开后是否游戏结束
                if self.board.game_over:
                    self.show_game_over()
                # 检查是否获胜
                elif self.board.is_win():
                    self.show_win()
            return
        else:
            self.board.reveal(x, y)
            self.update_buttons()
            # 检查是否游戏结束
            if self.board.game_over:
                self.show_game_over()
            # 检查是否获胜
            elif self.board.is_win():
                self.show_win()
            return

    def on_right_click(self, x, y):
        # 如果游戏暂停，自动恢复
        self.resume_from_pause()

        self.board.flag(x, y)
        self.update_buttons()

    def update_buttons(self):
        # 数字颜色配置，可以在这里修改颜色
        number_colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'purple',
            5: 'maroon',
            6: 'turquoise',
            7: 'black',
            8: 'gray'
        }

        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.buttons[r][c]
                if btn is None:
                    continue
                if cell.revealed:
                    if cell.has_mine:
                        btn.config(text='💣', bg='red', fg='white')
                    else:
                        if cell.adjacent_mines > 0:
                            # 显示数字，使用配置的颜色
                            color = number_colors.get(cell.adjacent_mines, 'black')
                            btn.config(text=str(cell.adjacent_mines), bg='lightgrey', fg=color)
                        else:
                            # 空白格子
                            btn.config(text='', bg='lightgrey')
                elif cell.flagged:
                    # 用红色三角形代替旗子
                    btn.config(text='▲', bg='yellow', fg='red')
                else:
                    # 未翻开的格子
                    btn.config(text='', bg='SystemButtonFace')

    def show_win(self):
        # 计算最终时间
        final_time = int(time.time() - self.start_time - self.pause_time) if self.game_started else 0

        # 创建获胜对话框
        dialog = tk.Toplevel(self.master)
        dialog.title("恭喜获胜！")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        # 设置对话框背景色
        dialog.configure(bg='lightgreen')     # 浅绿色背景

        # 居中显示
        dialog.transient(self.master)
        dialog.grab_set()

        # 计算屏幕中心位置
        dialog.update_idletasks()           # 更新对话框尺寸
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")

        # 添加内容
        tk.Label(dialog, text="🎉 恭喜获胜！🎉\n你成功完成了扫雷！",
                font=("楷体", 32, "bold"),
                bg='lightgreen', fg='darkgreen').pack(pady=30)
        tk.Label(dialog, text=f"用时: {final_time} 秒",
                font=("楷体", 20, "bold"),
                bg='lightgreen', fg='darkgreen').pack(pady=10)
        tk.Label(dialog, text="太棒了！你找到了所有的地雷！",
                font=("楷体", 24, "bold"),
                bg='lightgreen', fg='darkgreen').pack(pady=20)

        # 按钮框架
        button_frame = tk.Frame(dialog, bg='lightgreen')
        button_frame.pack(pady=40)

        # 创建按钮
        record_btn = tk.Button(button_frame, text="记录成绩",
                            font=("楷体", 18, "bold"),
                            width=10, height=40,
                            relief=tk.RAISED,               # 凸起的边框效果
                            bd=3,                           # 边框宽度
                            bg='lightblue',                 # 背景色
                            fg='darkblue',                  # 文字颜色
                            activebackground='skyblue',     # 点击时的背景色
                            activeforeground='white',       # 点击时的文字颜色
                            command=lambda: [dialog.destroy(), self.show_name_input(final_time)])
        record_btn.pack(side=tk.LEFT, padx=30)

        restart_btn = tk.Button(button_frame, text="再来一局",
                            font=("楷体", 18, "bold"),
                            width=10, height=40,
                            relief=tk.RAISED,               # 凸起的边框效果
                            bd=3,                           # 边框宽度
                            bg='lightblue',                 # 背景色
                            fg='darkblue',                  # 文字颜色
                            activebackground='skyblue',     # 点击时的背景色
                            activeforeground='white',       # 点击时的文字颜色
                            command=lambda: [dialog.destroy(), self.restart_game()])
        restart_btn.pack(side=tk.LEFT, padx=30)

        quit_btn = tk.Button(button_frame, text="退出游戏",
                            font=("楷体", 18, "bold"),
                            width=10, height=30,
                            relief=tk.RAISED,               # 凸起的边框效果
                            bd=3,                           # 边框宽度
                            bg='lightcoral',                # 背景色
                            fg='darkred',                   # 文字颜色
                            activebackground='salmon',      # 点击时的背景色
                            activeforeground='white',       # 点击时的文字颜色
                            command=lambda: [dialog.destroy(), self.master.quit()])
        quit_btn.pack(side=tk.LEFT, padx=30)

    def show_game_over(self):
        # 计算最终时间
        final_time = int(time.time() - self.start_time - self.pause_time) if self.game_started else 0

        # 显示所有地雷
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.buttons[r][c]
                if btn is not None and cell.has_mine:
                    btn.config(text='💣', bg='red', fg='white')

        # 创建自定义对话框
        dialog = tk.Toplevel(self.master)
        dialog.title("游戏结束")
        dialog.geometry("600x400")
        dialog.resizable(False, False)

        # 设置对话框背景色
        dialog.configure(bg='lavender')     # 浅紫色背景

        # 居中显示
        dialog.transient(self.master)
        dialog.grab_set()

        # 计算屏幕中心位置
        dialog.update_idletasks()           # 更新对话框尺寸
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")

        # 添加内容
        tk.Label(dialog, text="BOOM!💣\n游戏结束",
                font=("楷体", 32, "bold"),
                bg='lavender', fg='black').pack(pady=30)
        tk.Label(dialog, text=f"用时: {final_time} 秒",
                font=("楷体", 20, "bold"),
                bg='lavender', fg='black').pack(pady=10)
        tk.Label(dialog, text="很遗憾，你踩到雷了！",
                font=("楷体", 24, "bold"),
                bg='lavender', fg='black').pack(pady=20)

        # 按钮框架
        button_frame = tk.Frame(dialog, bg='lavender')
        button_frame.pack(pady=40)

        # 创建更大的按钮，使用更大的字体
        restart_btn = tk.Button(button_frame, text="重新开始",
                            font=("楷体", 18, "bold"),
                            width=10, height=40,
                            relief=tk.RAISED,               # 凸起的边框效果
                            bd=3,                           # 边框宽度
                            bg='lightblue',                 # 背景色
                            fg='darkblue',                  # 文字颜色
                            activebackground='skyblue',     # 点击时的背景色
                            activeforeground='white',       # 点击时的文字颜色
                            command=lambda: [dialog.destroy(), self.restart_game()])
        restart_btn.pack(side=tk.LEFT, padx=30)

        quit_btn = tk.Button(button_frame, text="退出游戏",
                            font=("楷体", 18, "bold"),
                            width=10, height=30,
                            relief=tk.RAISED,               # 凸起的边框效果
                            bd=3,                           # 边框宽度
                            bg='lightcoral',                # 背景色
                            fg='darkred',                   # 文字颜色
                            activebackground='salmon',      # 点击时的背景色
                            activeforeground='white',       # 点击时的文字颜色
                            command=lambda: [dialog.destroy(), self.master.quit()])
        quit_btn.pack(side=tk.LEFT, padx=30)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("扫雷🐟版")
    app = MinesweeperGUI(root)
    root.mainloop()