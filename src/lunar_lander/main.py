"""
Lunar Lander - Anechoicetry Collection
by Leo Kuroshita
Retro monochrome tube game style - rocket drifts and fires engines repeatedly
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class LunarLander:
    def __init__(self):
        pyxel.init(512, 512, title="Lunar Lander")
        
        self.time = 0
        self.rocket = {
            'x': 100,
            'y': 200,
            'vx': 0.3,
            'vy': 0.1,
            'thrust': False,
            'thrust_particles': [],
            'engine_phase': 0
        }
        
        self.lunar_surface = self.generate_lunar_surface()
        self.stars = []
        
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, 512),
                'y': random.randint(0, 200),
                'brightness': random.uniform(0.3, 1.0)
            })
        
        pyxel.run(self.update, self.draw)

    def generate_lunar_surface(self):
        surface = []
        y = 400
        for x in range(0, 513, 8):
            y += random.randint(-15, 15)
            y = max(350, min(450, y))
            surface.append((x, y))
        return surface

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        self.rocket['engine_phase'] += 0.2
        
        if random.random() < 0.4:
            self.rocket['thrust'] = True
            thrust_duration = random.randint(10, 30)
        else:
            self.rocket['thrust'] = False
        
        if self.rocket['thrust']:
            thrust_force = 0.03
            self.rocket['vy'] -= thrust_force
            
            for _ in range(random.randint(3, 8)):
                particle_angle = math.pi/2 + random.uniform(-0.5, 0.5)
                particle_speed = random.uniform(1, 3)
                self.rocket['thrust_particles'].append({
                    'x': self.rocket['x'] + random.uniform(-2, 2),
                    'y': self.rocket['y'] + 12,
                    'vx': particle_speed * math.cos(particle_angle) * 0.3,
                    'vy': particle_speed * math.sin(particle_angle),
                    'life': random.randint(15, 25),
                    'size': random.uniform(1, 3)
                })
        
        self.rocket['vy'] += 0.01
        
        self.rocket['x'] += self.rocket['vx']
        self.rocket['y'] += self.rocket['vy']
        
        
        if self.rocket['x'] > 512:
            self.rocket['x'] = -20
        elif self.rocket['x'] < -20:
            self.rocket['x'] = 512
        
        if self.rocket['y'] > 500:
            self.rocket['y'] = 50
            self.rocket['vy'] = 0.1
        elif self.rocket['y'] < 30:
            self.rocket['y'] = 30
            self.rocket['vy'] = max(0, self.rocket['vy'])
        
        for particle in self.rocket['thrust_particles'][:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['size'] *= 0.95
            if particle['life'] <= 0 or particle['size'] < 0.1:
                self.rocket['thrust_particles'].remove(particle)

    def draw_rocket(self):
        x, y = self.rocket['x'], self.rocket['y']
        
        rocket_points = [
            (x, y - 12),
            (x - 6, y + 8),
            (x + 6, y + 8)
        ]
        
        for i in range(len(rocket_points)):
            x1, y1 = rocket_points[i]
            x2, y2 = rocket_points[(i + 1) % len(rocket_points)]
            self.draw_line(int(x1), int(y1), int(x2), int(y2), 7)
        
        self.draw_line(int(x-2), int(y+8), int(x+2), int(y+8), 7)
        
        if self.rocket['thrust']:
            flame_length = 15 + 5 * math.sin(self.rocket['engine_phase'])
            
            flame_points = [
                (x - 3, y + 8),
                (x + 3, y + 8),
                (x, y + 8 + flame_length)
            ]
            
            for i in range(len(flame_points)):
                x1, y1 = flame_points[i]
                x2, y2 = flame_points[(i + 1) % len(flame_points)]
                self.draw_line(int(x1), int(y1), int(x2), int(y2), 15)

    def draw_line(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            if 0 <= x1 < 512 and 0 <= y1 < 512:
                pyxel.pset(x1, y1, color)
            
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw(self):
        pyxel.cls(0)
        
        for star in self.stars:
            if random.random() < star['brightness']:
                pyxel.pset(int(star['x']), int(star['y']), 6)
        
        for i in range(len(self.lunar_surface) - 1):
            x1, y1 = self.lunar_surface[i]
            x2, y2 = self.lunar_surface[i + 1]
            self.draw_line(x1, y1, x2, y2, 7)
        
        
        for particle in self.rocket['thrust_particles']:
            if 0 <= particle['x'] < 512 and 0 <= particle['y'] < 512:
                life_ratio = particle['life'] / 25
                if life_ratio > 0.3:
                    size = int(particle['size'])
                    color = 15 if life_ratio > 0.7 else 7
                    for dx in range(-size, size + 1):
                        for dy in range(-size, size + 1):
                            if dx*dx + dy*dy <= size*size:
                                px = int(particle['x']) + dx
                                py = int(particle['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    pyxel.pset(px, py, color)
        
        self.draw_rocket()


if __name__ == "__main__":
    LunarLander()