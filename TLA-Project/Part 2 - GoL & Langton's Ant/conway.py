"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    """
    Parses RLE (.rle) or Plaintext (.cells) pattern files correctly.
    """
    live_cells = []
    width, height = 0, 0
    
    with open(filepath, 'r') as f:
        # فیلتر خطوط در صورتی که با ! یا # شروع شده باشد
        # خطوط خالی حذف نمیشوند
        lines = [line.strip('\n\r') for line in f if not line.startswith('!') and not line.startswith('#')]
    
    # حذف خطوط خالی ابتدا و انتهای لیست 
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()

    # تشخیص فرمت RLE (تغییر نمی‌کند)
    if any('x =' in line for line in lines):
        pass 
            
    else:
        # تشخیص فرمت Plaintext (.cells) اصلاح شده
        height = len(lines)
        width = max(len(line.strip()) for line in lines) if lines else 0
        for r, line in enumerate(lines):
            for c, char in enumerate(line.strip()): 
                if char == 'O': 
                    live_cells.append((r, c))
                    
    return (width, height, live_cells)


class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):
        """
        نسخه بسیار سریع با استفاده از ndimage.convolve
        """
        # استفاده از ndimage به جای signal.convolve2d که در شبکه‌های بزرگ بسیار سریع‌تر است
        # حالت mode='wrap' برای توروئیدال (حلقوی)
        # حالت mode='constant' برای مرزهای ثابت (finite=True)
        boundary_mode = 'wrap' if not self.finite else 'constant'
        
        # محاسبه همسایگان با کرنل 3x3
        neighbor_count = ndimage.convolve(grid.astype(np.uint8), self.neighborhood.astype(np.uint8), 
                                         mode=boundary_mode, cval=0)
        
        # اعمال قوانین با استفاده از جستجوی شرطی سریع (Boolean Masking)
        # این بخش بسیار سریع است چون مستقیماً روی ماتریس اجرا می‌شود
        new_grid = np.zeros_like(grid)
        
        # حالت‌های زنده ماندن: 2 یا 3 همسایه
        # حالت‌های تولد: دقیقاً 3 همسایه
        new_grid[(grid == self.aliveValue) & ((neighbor_count == 2) | (neighbor_count == 3))] = self.aliveValue
        new_grid[(grid == self.deadValue) & (neighbor_count == 3)] = self.aliveValue
        
        return new_grid
    
    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            # [Part 1a - Core Rules] - Step-by-step cell evolution
            new_grid = np.zeros((self.rows, self.cols), dtype=np.uint)
            
            for r in range(self.rows):
                for c in range(self.cols):
                    # شمارش همسایه‌های زنده در همسایگی مور (8-connected)
                    live_neighbors = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # خود سلول شمرده نمیشود
                            
                            nr = r + dr
                            nc = c + dc
                            
                            if not self.finite:
                                # حالت حلقوی یا توروئیدال (Wrapping Boundaries)
                                nr = nr % self.rows
                                nc = nc % self.cols
                                if self.grid[nr, nc] == self.aliveValue:
                                    live_neighbors += 1
                            else:
                                # حالت مرزی محدود (Finite Boundaries)
                                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                    if self.grid[nr, nc] == self.aliveValue:
                                        live_neighbors += 1
                    
                    # اعمال قوانین چهارگانه بازی زندگی کانوی
                    current_state = self.grid[r, c]
                    if current_state == self.aliveValue:
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[r, c] = self.deadValue  # مرگ بر اثر کم‌جمعیتی یا بیش‌جمعیتی
                        else:
                            new_grid[r, c] = self.aliveValue  # بقا
                    else:
                        if live_neighbors == 3:
                            new_grid[r, c] = self.aliveValue  # تولید مثل و تولد
                        else:
                            new_grid[r, c] = self.deadValue
                            
            self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        TODO: [Part 1c - Glider Gun Fix]
        Fixed coordinates for the Gosper Glider Gun to ensure it loops infinitely.
        '''
        # Left block
        self.grid[index[0] + 5, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2] = self.aliveValue

        # Left part of the gun mechanism
        self.grid[index[0] + 3, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 11] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue

        # Right part of the gun mechanism
        self.grid[index[0] + 3, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 21] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 25] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 25] = self.aliveValue

        # Right blocks
        self.grid[index[0] + 3, index[1] + 35] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 35] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue
