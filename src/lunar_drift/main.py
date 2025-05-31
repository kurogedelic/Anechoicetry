"""
Lunar Drift - Anechoicetry Collection
by Leo Kuroshita
Moon-like circles slowly fade in and out in monochrome
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class LunarDrift:
    def __init__(self):
        pyxel.init(512, 512, title="Lunar Drift")
        
        self.time = 0
        self.moons = []
        
        for _ in range(5):
            self.moons.append({
                'x': random.randint(50, 462),
                'y': random.randint(50, 462),
                'radius': random.randint(20, 80),
                'phase': random.uniform(0, math.pi * 2),
                'speed': random.uniform(0.003, 0.008),
                'opacity': 0,
                'drift_x': random.uniform(-0.1, 0.1),
                'drift_y': random.uniform(-0.1, 0.1)
            })
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        for moon in self.moons:
            moon['phase'] += moon['speed']
            moon['opacity'] = (math.sin(moon['phase']) + 1) * 0.5
            
            moon['x'] += moon['drift_x']
            moon['y'] += moon['drift_y']
            
            if moon['x'] < -100:
                moon['x'] = 612
                moon['y'] = random.randint(50, 462)
            elif moon['x'] > 612:
                moon['x'] = -100
                moon['y'] = random.randint(50, 462)
            if moon['y'] < -100:
                moon['y'] = 612
                moon['x'] = random.randint(50, 462)
            elif moon['y'] > 612:
                moon['y'] = -100
                moon['x'] = random.randint(50, 462)

    def draw(self):
        pyxel.cls(0)
        
        for moon in self.moons:
            if moon['opacity'] > 0.1:
                center_x = int(moon['x'])
                center_y = int(moon['y'])
                radius = moon['radius']
                
                opacity_levels = int(moon['opacity'] * 4)
                color = [0, 5, 6, 7, 15][min(opacity_levels, 4)]
                
                for y in range(center_y - radius, center_y + radius + 1):
                    for x in range(center_x - radius, center_x + radius + 1):
                        dx = x - center_x
                        dy = y - center_y
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        if distance <= radius:
                            if 0 <= x < 512 and 0 <= y < 512:
                                edge_fade = 1 - (distance / radius)
                                if edge_fade > 0.3:
                                    if distance < radius * 0.8:
                                        pyxel.pset(x, y, color)
                                    elif random.random() < edge_fade:
                                        pyxel.pset(x, y, 5)

if __name__ == "__main__":
    LunarDrift()