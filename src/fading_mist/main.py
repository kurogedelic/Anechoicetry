"""
Fading Mist - Anechoicetry Collection
by Leo Kuroshita
Mist-like white particles drift and slowly expand and contract
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class FadingMist:
    def __init__(self):
        pyxel.init(512, 512, title="Fading Mist")
        
        self.time = 0
        self.mist_particles = []
        self.star_blink_timer = 0
        
        for _ in range(300):
            self.mist_particles.append({
                'x': random.uniform(0, 512),
                'y': random.uniform(0, 512),
                'vx': random.uniform(-0.2, 0.2),
                'vy': random.uniform(-0.2, 0.2),
                'size': random.uniform(2, 8),
                'opacity': random.uniform(0.1, 0.8),
                'phase': random.uniform(0, math.pi * 2)
            })
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def setup_sound(self):
        # High-frequency star twinkle sounds
        pyxel.sounds[0].set("c4", "t", "7", "v", 3)
        pyxel.sounds[1].set("e4", "t", "7", "v", 3) 
        pyxel.sounds[2].set("g4", "t", "7", "v", 3)
        pyxel.sounds[3].set("c3", "t", "7", "v", 2)
        pyxel.sounds[4].set("e3", "t", "7", "v", 2)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        # Star blink sound trigger
        self.star_blink_timer += 1
        if self.star_blink_timer > random.randint(30, 120):
            pyxel.play(0, random.randint(0, 4))
            self.star_blink_timer = 0
        
        expansion = (math.sin(self.time * 0.008) + 1) * 0.5
        
        for particle in self.mist_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            particle['phase'] += 0.01
            particle['opacity'] = 0.3 + 0.3 * math.sin(particle['phase'])
            
            particle['size'] = 1 + 2 * expansion + 0.5 * math.sin(particle['phase'] * 1.3)
            
            if particle['x'] < -10:
                particle['x'] = 522
            elif particle['x'] > 522:
                particle['x'] = -10
            if particle['y'] < -10:
                particle['y'] = 522
            elif particle['y'] > 522:
                particle['y'] = -10

    def draw(self):
        pyxel.cls(0)
        
        for particle in self.mist_particles:
            if particle['opacity'] > 0.1:
                size = int(particle['size'])
                alpha_levels = int(particle['opacity'] * 3)
                color = [0, 5, 6, 7][min(alpha_levels, 3)]
                
                for dx in range(-size, size + 1):
                    for dy in range(-size, size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        if distance <= size:
                            fade = 1 - (distance / size)
                            if fade > 0.3 and random.random() < fade:
                                px = int(particle['x']) + dx
                                py = int(particle['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    pyxel.pset(px, py, color)

if __name__ == "__main__":
    FadingMist()