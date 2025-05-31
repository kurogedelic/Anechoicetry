"""
Whispering Dust - Anechoicetry Collection
by Leo Kuroshita
Sand-like countless dots constantly disappearing and reappearing without forming lines
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class WhisperingDust:
    def __init__(self):
        pyxel.init(512, 512, title="Whispering Dust")
        
        self.time = 0
        self.dust_particles = []
        
        for _ in range(800):
            self.dust_particles.append({
                'x': random.randint(0, 512),
                'y': random.randint(0, 512),
                'life': random.randint(1, 60),
                'max_life': random.randint(20, 100),
                'flicker_phase': random.uniform(0, math.pi * 2),
                'flicker_speed': random.uniform(0.1, 0.3)
            })
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        for particle in self.dust_particles:
            particle['life'] -= 1
            particle['flicker_phase'] += particle['flicker_speed']
            
            if particle['life'] <= 0:
                particle['x'] = random.randint(0, 512)
                particle['y'] = random.randint(0, 512)
                particle['life'] = particle['max_life']
                particle['flicker_phase'] = random.uniform(0, math.pi * 2)
        
        if random.random() < 0.3:
            for _ in range(random.randint(1, 5)):
                if len(self.dust_particles) < 1000:
                    self.dust_particles.append({
                        'x': random.randint(0, 512),
                        'y': random.randint(0, 512),
                        'life': random.randint(1, 40),
                        'max_life': random.randint(20, 80),
                        'flicker_phase': random.uniform(0, math.pi * 2),
                        'flicker_speed': random.uniform(0.1, 0.3)
                    })

    def draw(self):
        pyxel.cls(0)
        
        for particle in self.dust_particles:
            flicker = (math.sin(particle['flicker_phase']) + 1) * 0.5
            life_ratio = particle['life'] / particle['max_life']
            
            visibility = flicker * life_ratio
            
            if visibility > 0.3 and random.random() < visibility:
                if visibility > 0.8:
                    color = 7
                elif visibility > 0.5:
                    color = 6
                else:
                    color = 5
                
                pyxel.pset(particle['x'], particle['y'], color)
                
                if random.random() < 0.1:
                    nearby_x = particle['x'] + random.randint(-1, 1)
                    nearby_y = particle['y'] + random.randint(-1, 1)
                    if 0 <= nearby_x < 512 and 0 <= nearby_y < 512:
                        pyxel.pset(nearby_x, nearby_y, 5)

if __name__ == "__main__":
    WhisperingDust()