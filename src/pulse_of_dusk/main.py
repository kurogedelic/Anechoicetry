"""
Pulse of Dusk - Anechoicetry Collection
by Leo Kuroshita
Darkness slowly brightening with pulsing particles that flicker and fade
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class PulseOfDusk:
    def __init__(self):
        pyxel.init(512, 512, title="Pulse of Dusk")
        
        self.time = 0
        self.particles = []
        self.ambient_brightness = 0
        
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, 512),
                'y': random.randint(0, 512),
                'phase': random.uniform(0, math.pi * 2),
                'brightness': 0,
                'pulse_speed': random.uniform(0.02, 0.05),
                'size': random.uniform(15, 40),
                'glow_radius': random.uniform(25, 60)
            })
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        self.ambient_brightness = (math.sin(self.time * 0.005) + 1) * 0.1
        
        for particle in self.particles:
            particle['phase'] += particle['pulse_speed']
            particle['brightness'] = max(0, math.sin(particle['phase']) * 0.7)
            
            if random.random() < 0.001:
                particle['x'] = random.randint(0, 512)
                particle['y'] = random.randint(0, 512)

    def draw(self):
        base_color = int(self.ambient_brightness * 255)
        pyxel.cls(0)
        
        if base_color > 0:
            for y in range(0, 512, 4):
                for x in range(0, 512, 4):
                    if random.random() < 0.3:
                        pyxel.pset(x, y, 5)
        
        for particle in self.particles:
            if particle['brightness'] > 0.05:
                intensity = int(particle['brightness'] * 4)
                color = [0, 5, 6, 7, 15][min(intensity, 4)]
                
                size = int(particle['brightness'] * particle['size'])
                glow_size = int(particle['brightness'] * particle['glow_radius'])
                
                center_x = int(particle['x'])
                center_y = int(particle['y'])
                
                for dx in range(-glow_size, glow_size + 1):
                    for dy in range(-glow_size, glow_size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        px = center_x + dx
                        py = center_y + dy
                        
                        if 0 <= px < 512 and 0 <= py < 512:
                            if distance <= size:
                                pyxel.pset(px, py, color)
                            elif distance <= glow_size:
                                glow_intensity = 1 - (distance - size) / (glow_size - size)
                                if random.random() < glow_intensity * particle['brightness']:
                                    glow_color = [0, 5, 6][min(int(glow_intensity * 2), 2)]
                                    pyxel.pset(px, py, glow_color)
                
                if particle['brightness'] > 0.8:
                    for _ in range(int(particle['brightness'] * 10)):
                        spark_x = center_x + random.randint(-size*2, size*2)
                        spark_y = center_y + random.randint(-size*2, size*2)
                        if 0 <= spark_x < 512 and 0 <= spark_y < 512:
                            pyxel.pset(spark_x, spark_y, 15)

if __name__ == "__main__":
    PulseOfDusk()