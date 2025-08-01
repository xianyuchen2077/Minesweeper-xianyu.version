#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from minesweeper import MinesweeperGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("扫雷🐟版")
    app = MinesweeperGUI(root)
    print("游戏已启动！")
    root.mainloop()
