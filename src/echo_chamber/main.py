"""
Echo Chamber - Anechoicetry Collection
by Leo Kuroshita
Rippling patterns bounce off invisible walls, creating visual echoes
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Ripple:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = 0
        self.max_radius = random.randint(40, 80)
        self.color = color
        self.life = 1.0
        self.speed = random.uniform(0.8, 1.5)
        self.echoes = []
        self.has_bounced = False
        
    def update(self):
        self.x += self.vx * 0.5
        self.y += self.vy * 0.5
        self.radius += self.speed
        
        if self.radius > self.max_radius:
            self.life -= 0.02
            
        bounce_margin = 50
        if not self.has_bounced:
            if self.x - self.radius < bounce_margin:
                self.vx = abs(self.vx)
                self.has_bounced = True
                return 'left'
            elif self.x + self.radius > 512 - bounce_margin:
                self.vx = -abs(self.vx)
                self.has_bounced = True
                return 'right'
            elif self.y - self.radius < bounce_margin:
                self.vy = abs(self.vy)
                self.has_bounced = True
                return 'top'
            elif self.y + self.radius > 512 - bounce_margin:
                self.vy = -abs(self.vy)
                self.has_bounced = True
                return 'bottom'
                
        return None
        
    def is_alive(self):
        return self.life > 0
        
    def draw(self):
        if self.life > 0:
            alpha = self.life
            for i in range(3):
                r = self.radius - i * 3
                if r > 0:
                    fade = 1 - (i / 3)
                    if alpha * fade > 0.3:
                        pyxel.circb(self.x, self.y, r, self.color)

class WallSegment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.activation = 0
        
    def activate(self):
        self.activation = 1.0
        
    def update(self):
        if self.activation > 0:
            self.activation -= 0.02
            
    def draw(self):
        if self.activation > 0:
            segments = 20
            for i in range(segments):
                t1 = i / segments
                t2 = (i + 1) / segments
                x1 = self.x1 + (self.x2 - self.x1) * t1
                y1 = self.y1 + (self.y2 - self.y1) * t1
                x2 = self.x1 + (self.x2 - self.x1) * t2
                y2 = self.y1 + (self.y2 - self.y1) * t2
                
                wave = math.sin(i * 0.5 + pyxel.frame_count * 0.1) * self.activation * 2
                offset_x = -(self.y2 - self.y1) / 100 * wave
                offset_y = (self.x2 - self.x1) / 100 * wave
                
                color = 7 if self.activation > 0.5 else 5
                pyxel.line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y, color)

class EchoChamber:
    def __init__(self):
        pyxel.init(512, 512, title="Echo Chamber")
        pyxel.cls(0)
        
        self.ripples = []
        self.walls = self.create_walls()
        self.frame_count = 0
        self.next_ripple = 0
        self.ripple_sources = []
        
        for _ in range(3):
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(100, 200)
            x = 256 + math.cos(angle) * dist
            y = 256 + math.sin(angle) * dist
            self.ripple_sources.append((x, y, angle))
            
        self.setup_sound()
        pyxel.run(self.update, self.draw)
        
    def setup_sound(self):
        pyxel.sounds[0].set(
            "c2",
            "p",
            "7",
            "v",
            8
        )
        
        pyxel.sounds[1].set(
            "g1",
            "p",
            "7",
            "v",
            6
        )
        
        pyxel.sounds[2].set(
            "e1",
            "p",
            "7",
            "v",
            5
        )
        
        pyxel.sounds[3].set(
            "a1",
            "p",
            "7",
            "v",
            4
        )
        
        pyxel.sounds[4].set(
            "c1e1g1c2",
            "s",
            "7",
            "n",
            20
        )
        
    def create_walls(self):
        walls = []
        segments = 32
        for i in range(segments):
            angle1 = i * 2 * math.pi / segments
            angle2 = (i + 1) * 2 * math.pi / segments
            
            r = 200 + math.sin(i * 3) * 20
            x1 = 256 + math.cos(angle1) * r
            y1 = 256 + math.sin(angle1) * r
            x2 = 256 + math.cos(angle2) * r
            y2 = 256 + math.sin(angle2) * r
            
            walls.append(WallSegment(x1, y1, x2, y2))
            
        return walls
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.frame_count += 1
        
        if self.frame_count >= self.next_ripple:
            source = random.choice(self.ripple_sources)
            x, y, base_angle = source
            
            angle = base_angle + random.uniform(-0.5, 0.5)
            speed = random.uniform(1, 2)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = random.choice([1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12])
            self.ripples.append(Ripple(x, y, vx, vy, color))
            
            self.next_ripple = self.frame_count + random.randint(20, 60)
            
            if random.random() < 0.3:
                pyxel.play(0, random.randint(0, 3))
                
        new_ripples = []
        for ripple in self.ripples:
            bounce = ripple.update()
            
            if bounce:
                if bounce in ['left', 'right']:
                    wall_x = 50 if bounce == 'left' else 462
                    for wall in self.walls:
                        if abs(wall.x1 - wall_x) < 100 or abs(wall.x2 - wall_x) < 100:
                            wall.activate()
                else:
                    wall_y = 50 if bounce == 'top' else 462
                    for wall in self.walls:
                        if abs(wall.y1 - wall_y) < 100 or abs(wall.y2 - wall_y) < 100:
                            wall.activate()
                            
                if random.random() < 0.7:
                    echo_x = ripple.x
                    echo_y = ripple.y
                    echo_vx = ripple.vx * 0.7 + random.uniform(-0.3, 0.3)
                    echo_vy = ripple.vy * 0.7 + random.uniform(-0.3, 0.3)
                    echo_color = ripple.color
                    new_ripples.append(Ripple(echo_x, echo_y, echo_vx, echo_vy, echo_color))
                    
                pyxel.play(1, 4)
                
        self.ripples.extend(new_ripples)
        self.ripples = [r for r in self.ripples if r.is_alive()]
        
        for wall in self.walls:
            wall.update()
            
        if random.random() < 0.01:
            idx = random.randint(0, len(self.ripple_sources) - 1)
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(100, 200)
            x = 256 + math.cos(angle) * dist
            y = 256 + math.sin(angle) * dist
            self.ripple_sources[idx] = (x, y, angle)
            
    def draw(self):
        pyxel.cls(0)
        
        for wall in self.walls:
            wall.draw()
            
        for source in self.ripple_sources:
            x, y, _ = source
            pyxel.pset(x, y, 7)
            pyxel.circb(x, y, 3, 5)
            
        for ripple in self.ripples:
            ripple.draw()
            
        pyxel.rectb(50, 50, 412, 412, 1)

EchoChamber()