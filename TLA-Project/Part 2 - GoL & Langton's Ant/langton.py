# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np

class LangtonsAnt:
    def __init__(self, N, ant_position, rules):
        """
        N: اندازه شبکه
        ant_position: (r, c)
        rules: دیکشنری به فرم {color: (next_color, direction)}
               direction به صورت 'R' یا 'L'
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.pos = list(ant_position)
        self.rules = rules
        
        # جهت‌های اصلی: 0: بالا، 1: راست، 2: پایین، 3: چپ
        # حرکت: (-1,0), (0,1), (1,0), (0,-1)
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.current_dir = 0 
        self.steps_count = 0 

    def get_states(self):
        return self.grid

    def get_current_position(self):
        return tuple(self.pos)

    def step(self):
        r, c = self.pos
        current_color = self.grid[r, c]
        
        # دریافت قوانین برای رنگ فعلی
        next_color, turn = self.rules[current_color]
        
        # تغییر رنگ
        self.grid[r, c] = next_color
        
        # چرخش
        if turn == 'R':
            self.current_dir = (self.current_dir + 1) % 4
        else: # 'L'
            self.current_dir = (self.current_dir - 1) % 4
            
            
        # حرکت به جلو
        dr, dc = self.directions[self.current_dir]
        self.pos[0] = (r + dr) % self.N
        self.pos[1] = (c + dc) % self.N
        
        self.steps_count = self.steps_count + 1 

    def update(self):
        self.step()

