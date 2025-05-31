"""
Silent Swirl - Anechoicetry Collection
by Leo Kuroshita
Spiral patterns slowly rotate with changing speeds, dark and restrained colors
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class SilentSwirl:
    def __init__(self):
        pyxel.init(512, 512, title="Silent Swirl")
        
        self.time = 0
        self.rotation = 0
        self.speed_phase = 0
        self.spiral_arms = 5
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        self.speed_phase += 0.01
        
        speed_variation = 0.5 + 0.5 * math.sin(self.speed_phase)
        rotation_speed = 0.005 + 0.01 * speed_variation
        
        self.rotation += rotation_speed

    def draw(self):
        pyxel.cls(0)
        
        center_x, center_y = 256, 256
        max_radius = 250
        
        secondary_swirl = self.rotation * 0.7
        
        for radius in range(5, max_radius, 4):
            for arm in range(self.spiral_arms):
                base_angle = (arm * 2 * math.pi / self.spiral_arms)
                
                spiral_factor = radius * 0.018
                angle = base_angle + self.rotation + spiral_factor
                
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                if 0 <= x < 512 and 0 <= y < 512:
                    distance_factor = radius / max_radius
                    
                    if distance_factor < 0.2:
                        color = 15
                        size = 3
                    elif distance_factor < 0.4:
                        color = 7
                        size = 2
                    elif distance_factor < 0.6:
                        color = 6
                        size = 2
                    elif distance_factor < 0.8:
                        color = 5
                        size = 1
                    else:
                        color = 1
                        size = 1
                    
                    opacity = 1 - distance_factor * 0.3
                    
                    for dx in range(-size, size + 1):
                        for dy in range(-size, size + 1):
                            if dx*dx + dy*dy <= size*size:
                                px = int(x) + dx
                                py = int(y) + dy
                                if 0 <= px < 512 and 0 <= py < 512 and random.random() < opacity:
                                    pyxel.pset(px, py, color)
                
                secondary_angle = base_angle - secondary_swirl + spiral_factor * 0.5
                x2 = center_x + radius * 0.8 * math.cos(secondary_angle)
                y2 = center_y + radius * 0.8 * math.sin(secondary_angle)
                
                if 0 <= x2 < 512 and 0 <= y2 < 512:
                    if random.random() < 0.6:
                        trail_color = 5 if distance_factor < 0.5 else 1
                        pyxel.pset(int(x2), int(y2), trail_color)
                        
                        if distance_factor < 0.3:
                            for dx in [-1, 0, 1]:
                                for dy in [-1, 0, 1]:
                                    px = int(x2) + dx
                                    py = int(y2) + dy
                                    if 0 <= px < 512 and 0 <= py < 512 and random.random() < 0.4:
                                        pyxel.pset(px, py, trail_color)
        
        pulsating_radius = 30 + 20 * math.sin(self.rotation * 3)
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x = center_x + pulsating_radius * math.cos(rad)
            y = center_y + pulsating_radius * math.sin(rad)
            if 0 <= x < 512 and 0 <= y < 512:
                pyxel.pset(int(x), int(y), 15)

if __name__ == "__main__":
    SilentSwirl()