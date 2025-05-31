"""
Floating Fragments - Anechoicetry Collection
by Leo Kuroshita
Geometric shapes drift through space, occasionally forming fleeting connections
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Fragment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.size = random.randint(8, 24)
        self.shape = random.choice(['square', 'triangle', 'circle'])
        self.color = random.choice([1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        self.rotation = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-0.02, 0.02)
        self.phase = random.uniform(0, math.pi * 2)
        self.pulse_speed = random.uniform(0.02, 0.05)
        self.alpha = 1.0
        self.connection_timer = 0
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        self.phase += self.pulse_speed
        
        if self.connection_timer > 0:
            self.connection_timer -= 1
        
        if self.x < -self.size:
            self.x = 512 + self.size
        elif self.x > 512 + self.size:
            self.x = -self.size
            
        if self.y < -self.size:
            self.y = 512 + self.size
        elif self.y > 512 + self.size:
            self.y = -self.size
            
        self.vx *= 0.999
        self.vy *= 0.999
        
        if abs(self.vx) < 0.1:
            self.vx += random.uniform(-0.05, 0.05)
        if abs(self.vy) < 0.1:
            self.vy += random.uniform(-0.05, 0.05)
            
    def draw(self):
        pulse = math.sin(self.phase) * 0.2 + 0.8
        size = self.size * pulse
        
        if self.shape == 'square':
            cx = self.x
            cy = self.y
            corners = []
            for i in range(4):
                angle = self.rotation + i * math.pi / 2
                dx = math.cos(angle) * size / 2
                dy = math.sin(angle) * size / 2
                corners.append((cx + dx, cy + dy))
            
            for i in range(4):
                x1, y1 = corners[i]
                x2, y2 = corners[(i + 1) % 4]
                pyxel.line(x1, y1, x2, y2, self.color)
                
        elif self.shape == 'triangle':
            cx = self.x
            cy = self.y
            corners = []
            for i in range(3):
                angle = self.rotation + i * 2 * math.pi / 3
                dx = math.cos(angle) * size / 2
                dy = math.sin(angle) * size / 2
                corners.append((cx + dx, cy + dy))
            
            for i in range(3):
                x1, y1 = corners[i]
                x2, y2 = corners[(i + 1) % 3]
                pyxel.line(x1, y1, x2, y2, self.color)
                
        elif self.shape == 'circle':
            pyxel.circb(self.x, self.y, size / 2, self.color)
            
    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class FloatingFragments:
    def __init__(self):
        pyxel.init(512, 512, title="Floating Fragments")
        pyxel.cls(0)
        
        self.fragments = []
        for _ in range(25):
            x = random.randint(50, 462)
            y = random.randint(50, 462)
            self.fragments.append(Fragment(x, y))
            
        self.connections = []
        self.frame_count = 0
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)
        
    def setup_sound(self):
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2",
            "p",
            "7",
            "s",
            25
        )
        
        pyxel.sounds[1].set(
            "c1",
            "t",
            "7",
            "f",
            10
        )
        
        pyxel.sounds[2].set(
            "g3b3",
            "s",
            "7",
            "n",
            15
        )
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.frame_count += 1
        
        for fragment in self.fragments:
            fragment.update()
            
        self.connections = []
        for i, f1 in enumerate(self.fragments):
            for j, f2 in enumerate(self.fragments[i+1:], i+1):
                dist = f1.distance_to(f2)
                if dist < 80:
                    strength = 1 - (dist / 80)
                    self.connections.append((f1, f2, strength))
                    
                    if random.random() < 0.01 and f1.connection_timer == 0:
                        f1.connection_timer = 30
                        f2.connection_timer = 30
                        pyxel.play(0, 0)
                        
                    if dist < 40:
                        dx = f2.x - f1.x
                        dy = f2.y - f1.y
                        force = 0.02 * strength
                        f1.vx -= dx * force / dist
                        f1.vy -= dy * force / dist
                        f2.vx += dx * force / dist
                        f2.vy += dy * force / dist
                        
        if self.frame_count % 300 == 0 and len(self.fragments) < 35:
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                x = random.randint(0, 512)
                y = -20
            elif edge == 'bottom':
                x = random.randint(0, 512)
                y = 532
            elif edge == 'left':
                x = -20
                y = random.randint(0, 512)
            else:
                x = 532
                y = random.randint(0, 512)
            self.fragments.append(Fragment(x, y))
            pyxel.play(1, 1)
            
        if self.frame_count % 450 == 0 and len(self.fragments) > 15:
            furthest = max(self.fragments, key=lambda f: abs(f.x - 256) + abs(f.y - 256))
            self.fragments.remove(furthest)
            pyxel.play(2, 2)
            
    def draw(self):
        pyxel.cls(0)
        
        for f1, f2, strength in self.connections:
            if strength > 0.3:
                color = 1 if strength < 0.6 else 5
                if f1.connection_timer > 0 or f2.connection_timer > 0:
                    color = 7
                pyxel.line(f1.x, f1.y, f2.x, f2.y, color)
                
        for fragment in self.fragments:
            fragment.draw()
            
            if fragment.connection_timer > 0:
                radius = (30 - fragment.connection_timer) * 2
                pyxel.circb(fragment.x, fragment.y, radius, 7)

FloatingFragments()