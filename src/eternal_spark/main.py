"""
Eternal Spark - Anechoicetry Collection
by Leo Kuroshita
A single point of light disappears and reappears elsewhere sporadically, no pattern
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class EternalSpark:
    def __init__(self):
        pyxel.init(512, 512, title="Eternal Spark")
        
        self.time = 0
        self.spark = {
            'x': 256,
            'y': 256,
            'visible': False,
            'life': 0,
            'max_life': 0,
            'next_appear_time': random.randint(30, 180),
            'explosion_particles': [],
            'echo_sparks': [],
            'continuous_sparks': [],
            'energy_buildup': []
        }
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def setup_sound(self):
        # Ethereal spark appearance sounds
        pyxel.sounds[0].set("c4e4g4c3", "t", "7654", "v", 6)
        pyxel.sounds[1].set("g4c4e4", "t", "765", "v", 8)
        
        # Energy buildup resonance
        pyxel.sounds[2].set("c1e1g1c2", "s", "5678", "v", 12)
        pyxel.sounds[3].set("e1g1c2e2", "s", "6789", "v", 10)
        
        # Explosive burst sounds
        pyxel.sounds[4].set("c4e4g4c3g2c2", "n", "987654", "f", 8)
        pyxel.sounds[5].set("g4c4e3g3c3", "n", "98765", "f", 10)
        
        # Echo sparkle effects
        pyxel.sounds[6].set("c3e3g3", "t", "543", "v", 5)
        pyxel.sounds[7].set("e3g3c4", "t", "321", "v", 4)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        if self.spark['visible']:
            self.spark['life'] -= 1
            
            if random.random() < 0.8:
                for _ in range(random.randint(3, 8)):
                    self.spark['continuous_sparks'].append({
                        'x': self.spark['x'] + random.uniform(-15, 15),
                        'y': self.spark['y'] + random.uniform(-15, 15),
                        'vx': random.uniform(-2, 2),
                        'vy': random.uniform(-2, 2),
                        'life': random.randint(8, 25),
                        'color': random.choice([15, 7, 6, 14]),
                        'trail_length': random.randint(3, 8)
                    })
                # Continuous spark crackle sounds
                if random.random() < 0.3:
                    pyxel.play(2, random.choice([6, 7]))
            
            if random.random() < 0.3:
                for _ in range(random.randint(5, 15)):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(20, 60)
                    self.spark['energy_buildup'].append({
                        'x': self.spark['x'] + distance * math.cos(angle),
                        'y': self.spark['y'] + distance * math.sin(angle),
                        'target_x': self.spark['x'],
                        'target_y': self.spark['y'],
                        'life': random.randint(15, 30),
                        'speed': random.uniform(0.8, 1.5)
                    })
                # Energy buildup resonance sounds
                if random.random() < 0.5:
                    pyxel.play(1, random.choice([2, 3]))
            
            if self.spark['life'] <= 0:
                for _ in range(40):
                    self.spark['explosion_particles'].append({
                        'x': self.spark['x'],
                        'y': self.spark['y'],
                        'vx': random.uniform(-6, 6),
                        'vy': random.uniform(-6, 6),
                        'life': random.randint(30, 80),
                        'color': random.choice([15, 7, 6, 14]),
                        'size': random.uniform(1, 4)
                    })
                
                for _ in range(10):
                    self.spark['echo_sparks'].append({
                        'x': self.spark['x'] + random.randint(-150, 150),
                        'y': self.spark['y'] + random.randint(-150, 150),
                        'life': random.randint(20, 60),
                        'size': random.randint(3, 8),
                        'pulse_speed': random.uniform(0.1, 0.3)
                    })
                
                for _ in range(100):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(5, 100)
                    self.spark['continuous_sparks'].append({
                        'x': self.spark['x'] + distance * math.cos(angle),
                        'y': self.spark['y'] + distance * math.sin(angle),
                        'vx': random.uniform(-4, 4),
                        'vy': random.uniform(-4, 4),
                        'life': random.randint(20, 50),
                        'color': random.choice([15, 7, 6, 14]),
                        'trail_length': random.randint(5, 12)
                    })
                
                self.spark['visible'] = False
                self.spark['next_appear_time'] = self.time + random.randint(40, 200)
                
                # Explosive burst sound
                pyxel.play(0, random.choice([4, 5]))
        else:
            if self.time >= self.spark['next_appear_time']:
                self.spark['x'] = random.randint(50, 462)
                self.spark['y'] = random.randint(50, 462)
                self.spark['life'] = random.randint(30, 120)
                self.spark['max_life'] = self.spark['life']
                self.spark['visible'] = True
                
                # Ethereal spark appearance sound
                pyxel.play(3, random.choice([0, 1]))
        
        for particle in self.spark['explosion_particles'][:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vx'] *= 0.98
            particle['vy'] *= 0.98
            if particle['life'] <= 0:
                self.spark['explosion_particles'].remove(particle)
        
        for echo in self.spark['echo_sparks'][:]:
            echo['life'] -= 1
            if echo['life'] <= 0:
                self.spark['echo_sparks'].remove(echo)
        
        for spark in self.spark['continuous_sparks'][:]:
            spark['x'] += spark['vx']
            spark['y'] += spark['vy']
            spark['life'] -= 1
            spark['vx'] *= 0.99
            spark['vy'] *= 0.99
            if spark['life'] <= 0:
                self.spark['continuous_sparks'].remove(spark)
        
        for energy in self.spark['energy_buildup'][:]:
            dx = energy['target_x'] - energy['x']
            dy = energy['target_y'] - energy['y']
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                energy['x'] += (dx / distance) * energy['speed']
                energy['y'] += (dy / distance) * energy['speed']
            energy['life'] -= 1
            if energy['life'] <= 0 or distance < 5:
                self.spark['energy_buildup'].remove(energy)

    def draw(self):
        pyxel.cls(0)
        
        for spark in self.spark['continuous_sparks']:
            if 0 <= spark['x'] < 512 and 0 <= spark['y'] < 512:
                life_ratio = spark['life'] / 25
                if life_ratio > 0.1:
                    trail_length = int(spark['trail_length'] * life_ratio)
                    for i in range(trail_length):
                        trail_x = spark['x'] - spark['vx'] * i * 0.5
                        trail_y = spark['y'] - spark['vy'] * i * 0.5
                        if 0 <= trail_x < 512 and 0 <= trail_y < 512:
                            trail_alpha = life_ratio * (1 - i / trail_length)
                            if random.random() < trail_alpha:
                                color = spark['color'] if i < 2 else max(1, spark['color'] - 1)
                                pyxel.pset(int(trail_x), int(trail_y), color)
        
        for energy in self.spark['energy_buildup']:
            if 0 <= energy['x'] < 512 and 0 <= energy['y'] < 512:
                life_ratio = energy['life'] / 30
                if life_ratio > 0.2:
                    size = int(life_ratio * 2) + 1
                    for dx in range(-size, size + 1):
                        for dy in range(-size, size + 1):
                            if dx*dx + dy*dy <= size*size:
                                px = int(energy['x']) + dx
                                py = int(energy['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    pyxel.pset(px, py, 14)
        
        for particle in self.spark['explosion_particles']:
            if 0 <= particle['x'] < 512 and 0 <= particle['y'] < 512:
                life_ratio = particle['life'] / 80
                if life_ratio > 0.1:
                    size = int(particle['size'] * life_ratio) + 1
                    for dx in range(-size, size + 1):
                        for dy in range(-size, size + 1):
                            if dx*dx + dy*dy <= size*size:
                                px = int(particle['x']) + dx
                                py = int(particle['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    pyxel.pset(px, py, particle['color'])
        
        for echo in self.spark['echo_sparks']:
            if 0 <= echo['x'] < 512 and 0 <= echo['y'] < 512:
                life_ratio = echo['life'] / 60
                if life_ratio > 0.1:
                    pulse = (math.sin(self.time * echo.get('pulse_speed', 0.2)) + 1) * 0.5
                    size = int(echo['size'] * (0.5 + 0.5 * pulse * life_ratio))
                    
                    for dx in range(-size, size + 1):
                        for dy in range(-size, size + 1):
                            distance = math.sqrt(dx*dx + dy*dy)
                            if distance <= size:
                                px = int(echo['x']) + dx
                                py = int(echo['y']) + dy
                                if 0 <= px < 512 and 0 <= py < 512:
                                    intensity = (1 - distance/size) * life_ratio * pulse
                                    if random.random() < intensity:
                                        color = 15 if intensity > 0.8 else (7 if intensity > 0.5 else 6)
                                        pyxel.pset(px, py, color)
                    
                    if life_ratio > 0.5 and random.random() < 0.4:
                        for _ in range(random.randint(2, 6)):
                            spark_angle = random.uniform(0, 2 * math.pi)
                            spark_dist = random.uniform(size, size * 2)
                            spark_x = int(echo['x'] + spark_dist * math.cos(spark_angle))
                            spark_y = int(echo['y'] + spark_dist * math.sin(spark_angle))
                            if 0 <= spark_x < 512 and 0 <= spark_y < 512:
                                pyxel.pset(spark_x, spark_y, 15)
        
        if self.spark['visible']:
            life_ratio = self.spark['life'] / self.spark['max_life']
            
            if life_ratio > 0.8:
                color = 15
                size = 8
            elif life_ratio > 0.6:
                color = 7
                size = 6
            elif life_ratio > 0.3:
                color = 6
                size = 4
            else:
                color = 5
                size = 3
            
            x, y = int(self.spark['x']), int(self.spark['y'])
            
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= size:
                        px, py = x + dx, y + dy
                        if 0 <= px < 512 and 0 <= py < 512:
                            if distance <= size * 0.5:
                                pyxel.pset(px, py, color)
                            elif random.random() < (1 - distance/size) * life_ratio:
                                pyxel.pset(px, py, max(1, color - 1))
            
            if life_ratio > 0.5:
                lightning_arms = 12
                for i in range(lightning_arms):
                    angle = (i * 2 * math.pi / lightning_arms) + self.time * 0.15
                    length = size * 3 + random.randint(-10, 25)
                    end_x = x + int(length * math.cos(angle))
                    end_y = y + int(length * math.sin(angle))
                    
                    steps = max(1, int(length / 2))
                    for step in range(steps):
                        t = step / steps
                        chaos = random.randint(-4, 4)
                        lx = int(x + t * (end_x - x) + chaos)
                        ly = int(y + t * (end_y - y) + chaos)
                        if 0 <= lx < 512 and 0 <= ly < 512 and random.random() < 0.8:
                            pyxel.pset(lx, ly, 15)
                            
                            if random.random() < 0.3:
                                for branch_dx in [-1, 0, 1]:
                                    for branch_dy in [-1, 0, 1]:
                                        if branch_dx != 0 or branch_dy != 0:
                                            branch_x = lx + branch_dx
                                            branch_y = ly + branch_dy
                                            if 0 <= branch_x < 512 and 0 <= branch_y < 512:
                                                pyxel.pset(branch_x, branch_y, 7)
            
            if life_ratio > 0.8:
                for _ in range(int(life_ratio * 30)):
                    burst_angle = random.uniform(0, 2 * math.pi)
                    burst_dist = random.uniform(size * 2, size * 4)
                    burst_x = x + int(burst_dist * math.cos(burst_angle))
                    burst_y = y + int(burst_dist * math.sin(burst_angle))
                    if 0 <= burst_x < 512 and 0 <= burst_y < 512:
                        pyxel.pset(burst_x, burst_y, random.choice([15, 7, 14]))

if __name__ == "__main__":
    EternalSpark()