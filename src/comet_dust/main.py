"""
Comet Dust - Anechoicetry Collection
by Leo Kuroshita
Tiny light particles move with trails against dark background, quickly disappearing
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class CometDust:
    def __init__(self):
        pyxel.init(512, 512, title="Comet Dust")
        
        self.time = 0
        self.particles = []
        self.trails = []
        self.jet_timer = 0
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def setup_sound(self):
        # Jet propulsion sound (low frequency noise-like)
        pyxel.sounds[0].set("c0d0e0f0", "n", "7654", "s", 30)
        pyxel.sounds[1].set("g0a0b0c1", "n", "6543", "s", 25)
        
        # Sparkle sounds (high frequency short bursts)
        pyxel.sounds[2].set("c4e4g4c3", "t", "7", "v", 5)
        pyxel.sounds[3].set("d4f4a4d3", "t", "7", "v", 4)
        pyxel.sounds[4].set("e4g4b4e3", "t", "7", "v", 3)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        # Continuous jet sound
        self.jet_timer += 1
        if self.jet_timer > 60:
            pyxel.play(0, random.choice([0, 1]))
            self.jet_timer = 0
        
        if random.random() < 0.08:
            self.particles.append({
                'x': random.randint(0, 512),
                'y': random.randint(0, 512),
                'vx': random.uniform(-4, 4),
                'vy': random.uniform(-4, 4),
                'life': random.randint(40, 120),
                'max_life': random.randint(40, 120),
                'size': random.uniform(3, 8),
                'glow_size': random.uniform(8, 15),
                'brightness': random.uniform(0.7, 1.0)
            })
            
            # Sparkle sound when new particle appears
            if random.random() < 0.6:
                pyxel.play(1, random.randint(2, 4))
        
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            self.trails.append({
                'x': particle['x'],
                'y': particle['y'],
                'life': 15,
                'max_life': 15,
                'size': particle.get('size', 2) * 0.7
            })
            
            if random.random() < 0.3:
                self.trails.append({
                    'x': particle['x'] + random.uniform(-2, 2),
                    'y': particle['y'] + random.uniform(-2, 2),
                    'life': 10,
                    'max_life': 10,
                    'size': particle.get('size', 2) * 0.5
                })
            
            if particle['life'] <= 0 or particle['x'] < 0 or particle['x'] > 512 or particle['y'] < 0 or particle['y'] > 512:
                self.particles.remove(particle)
        
        for trail in self.trails[:]:
            trail['life'] -= 1
            if trail['life'] <= 0:
                self.trails.remove(trail)

    def draw(self):
        pyxel.cls(0)
        
        for trail in self.trails:
            if 0 <= trail['x'] < 512 and 0 <= trail['y'] < 512:
                opacity = trail['life'] / trail['max_life']
                trail_size = int(trail.get('size', 2))
                
                if opacity > 0.3:
                    color = 6 if opacity > 0.7 else 5
                    
                    for dx in range(-trail_size, trail_size + 1):
                        for dy in range(-trail_size, trail_size + 1):
                            if dx*dx + dy*dy <= trail_size*trail_size:
                                px = int(trail['x']) + dx
                                py = int(trail['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    fade = 1 - (math.sqrt(dx*dx + dy*dy) / trail_size)
                                    if random.random() < opacity * fade:
                                        pyxel.pset(px, py, color)
        
        for particle in self.particles:
            if 0 <= particle['x'] < 512 and 0 <= particle['y'] < 512:
                life_ratio = particle['life'] / particle['max_life']
                size = int(particle.get('size', 3) * life_ratio) + 1
                glow_size = int(particle.get('glow_size', 6) * life_ratio)
                brightness = particle.get('brightness', 1.0) * life_ratio
                
                if life_ratio > 0.8:
                    core_color = 15
                elif life_ratio > 0.5:
                    core_color = 7
                elif life_ratio > 0.2:
                    core_color = 6
                else:
                    core_color = 5
                
                center_x = int(particle['x'])
                center_y = int(particle['y'])
                
                for dx in range(-glow_size, glow_size + 1):
                    for dy in range(-glow_size, glow_size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        px = center_x + dx
                        py = center_y + dy
                        
                        if 0 <= px < 512 and 0 <= py < 512:
                            if distance <= size:
                                pyxel.pset(px, py, core_color)
                            elif distance <= glow_size:
                                glow_intensity = 1 - (distance - size) / (glow_size - size)
                                if random.random() < glow_intensity * brightness * 0.6:
                                    glow_color = 6 if glow_intensity > 0.5 else 5
                                    pyxel.pset(px, py, glow_color)
                
                if life_ratio > 0.7 and brightness > 0.8:
                    for _ in range(int(brightness * 8)):
                        spark_angle = random.uniform(0, 2 * math.pi)
                        spark_dist = random.uniform(size, glow_size * 1.5)
                        spark_x = center_x + int(spark_dist * math.cos(spark_angle))
                        spark_y = center_y + int(spark_dist * math.sin(spark_angle))
                        if 0 <= spark_x < 512 and 0 <= spark_y < 512:
                            pyxel.pset(spark_x, spark_y, 15)

if __name__ == "__main__":
    CometDust()