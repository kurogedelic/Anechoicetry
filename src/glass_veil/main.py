"""
Glass Veil - Anechoicetry Collection
by Leo Kuroshita
Translucent glass-like layers drift and scroll fluidly, not geometric
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class GlassVeil:
    def __init__(self):
        pyxel.init(512, 512, title="Glass Veil")
        
        self.time = 0
        self.veils = []
        
        for _ in range(3):
            self.veils.append({
                'points': self.generate_fluid_shape(),
                'offset_x': 0,
                'offset_y': 0,
                'speed_x': random.uniform(-0.3, 0.3),
                'speed_y': random.uniform(-0.2, 0.2),
                'opacity_phase': random.uniform(0, math.pi * 2),
                'deform_phase': random.uniform(0, math.pi * 2)
            })
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def setup_sound(self):
        # Crystalline glass harmonic sounds
        pyxel.sounds[0].set("c3e3g3", "t", "765", "v", 8)
        pyxel.sounds[1].set("d3f3a3", "t", "654", "v", 7)
        pyxel.sounds[2].set("e3g3b3", "t", "543", "v", 6)
        
        # Glass shimmer high notes
        pyxel.sounds[3].set("c4", "t", "7", "v", 4)
        pyxel.sounds[4].set("e4", "t", "6", "v", 3)

    def generate_fluid_shape(self):
        points = []
        center_x = 256
        center_y = 256
        
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            radius = 150 + 50 * math.sin(angle * 0.1) + random.uniform(-20, 20)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad)
            points.append((x, y))
        
        return points

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        # Glass shimmer sound occasionally
        if random.random() < 0.008:
            pyxel.play(0, random.randint(0, 2))
        
        if random.random() < 0.004:
            pyxel.play(1, random.randint(3, 4))
        
        for veil in self.veils:
            veil['offset_x'] += veil['speed_x']
            veil['offset_y'] += veil['speed_y']
            veil['opacity_phase'] += 0.005
            veil['deform_phase'] += 0.003
            
            if veil['offset_x'] > 512:
                veil['offset_x'] = -200
            elif veil['offset_x'] < -200:
                veil['offset_x'] = 512
            if veil['offset_y'] > 512:
                veil['offset_y'] = -200
            elif veil['offset_y'] < -200:
                veil['offset_y'] = 512

    def draw(self):
        pyxel.cls(0)
        
        for veil in self.veils:
            opacity = (math.sin(veil['opacity_phase']) + 1) * 0.3 + 0.2
            deform = math.sin(veil['deform_phase']) * 10
            
            transformed_points = []
            for i, (x, y) in enumerate(veil['points']):
                new_x = x + veil['offset_x'] + deform * math.sin(i * 0.5)
                new_y = y + veil['offset_y'] + deform * math.cos(i * 0.3)
                transformed_points.append((new_x, new_y))
            
            self.draw_fluid_shape(transformed_points, opacity)

    def draw_fluid_shape(self, points, opacity):
        if len(points) < 3:
            return
        
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        
        for y in range(int(max(0, min_y)), int(min(512, max_y)), 2):
            for x in range(int(max(0, min_x)), int(min(512, max_x)), 2):
                if self.point_in_polygon(x, y, points):
                    if random.random() < opacity:
                        alpha_level = int(opacity * 3)
                        color = [0, 5, 6, 7][min(alpha_level, 3)]
                        pyxel.pset(x, y, color)

    def point_in_polygon(self, x, y, points):
        n = len(points)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = points[i]
            xj, yj = points[j]
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        
        return inside

if __name__ == "__main__":
    GlassVeil()