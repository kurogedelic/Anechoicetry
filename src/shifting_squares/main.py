"""
Shifting Squares - Anechoicetry Collection
by Leo Kuroshita
Square blocks quietly expand and contract filling the screen with subdued gradients
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class ShiftingSquares:
    def __init__(self):
        pyxel.init(512, 512, title="Shifting Squares")
        
        self.time = 0
        self.squares = []
        
        grid_size = 8
        for i in range(grid_size):
            for j in range(grid_size):
                self.squares.append({
                    'x': i * (512 // grid_size),
                    'y': j * (512 // grid_size),
                    'base_size': 512 // grid_size,
                    'phase': random.uniform(0, math.pi * 2),
                    'speed': random.uniform(0.005, 0.015),
                    'color_phase': random.uniform(0, math.pi * 2)
                })
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        for square in self.squares:
            square['phase'] += square['speed']
            square['color_phase'] += 0.003

    def draw(self):
        pyxel.cls(1)
        
        for square in self.squares:
            size_mult = 0.7 + 0.3 * math.sin(square['phase'])
            size = int(square['base_size'] * size_mult)
            
            color_val = (math.sin(square['color_phase']) + 1) * 0.5
            colors = [1, 5, 6, 7, 15]
            color_idx = int(color_val * (len(colors) - 1))
            color = colors[color_idx]
            
            center_x = square['x'] + square['base_size'] // 2
            center_y = square['y'] + square['base_size'] // 2
            
            x1 = center_x - size // 2
            y1 = center_y - size // 2
            x2 = center_x + size // 2
            y2 = center_y + size // 2
            
            if size > 4:
                pyxel.rect(x1, y1, size, size, color)
                
                inner_size = max(2, size - 4)
                inner_x = center_x - inner_size // 2
                inner_y = center_y - inner_size // 2
                
                inner_color_val = (math.sin(square['color_phase'] + 1) + 1) * 0.5
                inner_color_idx = int(inner_color_val * (len(colors) - 1))
                inner_color = colors[inner_color_idx]
                
                pyxel.rect(inner_x, inner_y, inner_size, inner_size, inner_color)

if __name__ == "__main__":
    ShiftingSquares()