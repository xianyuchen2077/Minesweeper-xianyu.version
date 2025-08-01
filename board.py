import random

class Cell:
    def __init__(self):
        self.has_mine = False               # 是否有雷
        self.revealed = False               # 是否已翻开
        self.flagged = False                # 是否已标记
        self.adjacent_mines = 0             # 临近格子中的雷数
        self.flagged_adjacent_mines = 0     # 相邻格子中被标记的雷数

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows                                                    # 棋盘行数
        self.cols = cols                                                    # 棋盘列数
        self.mines = mines                                                  # 雷数
        self.game_over = False                                              # 游戏是否结束
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]    # 棋盘格子
        self.mines_placed = False                                           # 雷是否已放置
        self.first_click_x = None                                           # 第一次点击的x坐标
        self.first_click_y = None                                           # 第一次点击的y坐标
        self._calculate_adjacent()                                          # 计算每个格子周围的雷数
        self._calculate_flagged_adjacent()                                  # 计算每个格子周围被标记的雷数

    def _place_mines(self, first_x, first_y):
        # 确保第一次点击的位置没有雷
        safe_positions = set()
        if 0 <= first_x < self.rows and 0 <= first_y <self.cols:
            safe_positions.add(first_x * self.cols + first_y)

        # 生成所有可能的位置，排除安全位置
        all_positions = set(range(self.rows * self.cols))
        available_positions = list(all_positions - safe_positions)

        # 随机选择雷的位置
        positions = random.sample(available_positions, self.mines)
        for pos in positions:
            r, c = divmod(pos, self.cols)               # 把一维编号转换为二维坐标
            self.grid[r][c].has_mine = True             # 设置雷

        # 计算每个格子周围的雷数
        self._calculate_adjacent()
        self._calculate_flagged_adjacent()

    def _calculate_adjacent(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].has_mine:            # 如果格子有雷，跳过
                    continue
                count = 0                               # 周围雷数
                for dr in [-1, 0, 1]:                   # 遍历周围8个格子
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc                 # 计算周围格子的坐标
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].has_mine:      # 如果周围格子有雷，雷数加1
                                count += 1
                self.grid[r][c].adjacent_mines = count

    def _calculate_flagged_adjacent(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].has_mine:            # 如果格子有雷，跳过
                    continue
                count = 0                               # 周围雷数
                for dr in [-1, 0, 1]:                   # 遍历周围8个格子
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc                 # 计算周围格子的坐标
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].flagged:      # 如果周围格子有插旗，旗子数加1
                                count += 1
                self.grid[r][c].flagged_adjacent_mines = count

    def reveal(self, x, y):
        cell = self.grid[x][y]
        if cell.revealed or cell.flagged:   # 如果格子已翻开或已标记，跳过
            return

        # 如果是第一次点击，先放置雷
        if not self.mines_placed:
            self._place_mines(x, y)
            self.mines_placed = True

        cell.revealed = True
        if cell.has_mine:                   # 如果格子有雷，游戏结束
            self.game_over = True
        elif cell.adjacent_mines == 0:      # 如果周围没有雷，递归打开周围8个格子中未被打开的格子
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = x + dr, y + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if not self.grid[nr][nc].revealed:
                            self.reveal(nr, nc)
        self._calculate_flagged_adjacent()  # 重新计算所有格子周围被标记的雷数

    def flag(self, x, y):
        cell = self.grid[x][y]
        # 如果雷还没放置，不允许插旗
        if not self.mines_placed:
            return
        if not cell.revealed:                   # 如果格子未被翻开，标记格子
            cell.flagged = not cell.flagged     # 如果格子已标记，取消标记；如果格子未标记，标记
            self._calculate_flagged_adjacent()  # 重新计算所有格子周围被标记的雷数

    def is_win(self):
        # 如果雷还没放置，不可能获胜
        if not self.mines_placed:
            return False
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.has_mine and not cell.flagged:
                    count += 1
        if count > 1:                # 如果格子有雷且未被插旗的数量大于一个，返回False
            return False
        return True                     # 如果所有格子都已翻开，返回True