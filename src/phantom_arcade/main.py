"""
Phantom Arcade - Anechoicetry Collection
by Leo Kuroshita
Ghost sprites play endless games in an abandoned arcade cabinet
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class GhostSprite:
    def __init__(self, x, y, sprite_type):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.sprite_type = sprite_type
        self.frame = 0
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.speed = random.uniform(0.3, 0.8)
        self.phase = random.uniform(0, math.pi * 2)
        self.color = random.choice([3, 5, 6, 8, 11, 12, 14])
        self.trail = []
        self.max_trail = 8
        self.flicker_timer = 0
        self.power_mode = False
        self.power_timer = 0
        
    def update(self):
        self.frame += 0.1
        self.phase += 0.05
        
        self.trail.append((self.x, self.y, self.color))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
        if self.flicker_timer > 0:
            self.flicker_timer -= 1
            
        if self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer == 0:
                self.power_mode = False
                
        wave = math.sin(self.phase) * 2
        
        if self.direction == 'left':
            self.x -= self.speed
            self.y = self.base_y + wave
        elif self.direction == 'right':
            self.x += self.speed
            self.y = self.base_y + wave
        elif self.direction == 'up':
            self.y -= self.speed
            self.x = self.base_x + wave
        elif self.direction == 'down':
            self.y += self.speed
            self.x = self.base_x + wave
            
        grid_size = 32
        self.x = ((self.x + 8) // grid_size) * grid_size
        self.y = ((self.y + 8) // grid_size) * grid_size
        
        if self.x < 64:
            self.x = 64
            self.turn()
        elif self.x > 448:
            self.x = 448
            self.turn()
        if self.y < 64:
            self.y = 64
            self.turn()
        elif self.y > 448:
            self.y = 448
            self.turn()
            
        if random.random() < 0.02:
            self.turn()
            
    def turn(self):
        directions = ['left', 'right', 'up', 'down']
        directions.remove(self.direction)
        self.direction = random.choice(directions)
        self.base_x = self.x
        self.base_y = self.y
        self.flicker_timer = 10
        pyxel.play(0, 1)
        
    def activate_power(self):
        self.power_mode = True
        self.power_timer = 120
        self.speed *= 2
        pyxel.play(1, 3)
        
    def draw(self):
        if self.flicker_timer % 4 < 2:
            return
            
        for i, (tx, ty, tc) in enumerate(self.trail):
            alpha = i / len(self.trail)
            if alpha > 0.3:
                size = 8 * alpha
                if self.sprite_type == 'pacman':
                    mouth_angle = abs(math.sin(self.frame * 0.5)) * 40
                    pyxel.circ(tx, ty, size/2, tc)
                elif self.sprite_type == 'ghost':
                    pyxel.rect(tx - size/2, ty - size/2, size, size * 0.8, tc)
                    for j in range(3):
                        x = tx - size/2 + j * size/3
                        pyxel.rect(x, ty + size/2 - 2, size/3 - 1, 3, tc)
                elif self.sprite_type == 'invader':
                    pyxel.rect(tx - size/2, ty - size/2, size, size/2, tc)
                    pyxel.pset(tx - 2, ty - size/4, 0)
                    pyxel.pset(tx + 2, ty - size/4, 0)
                    
        color = 7 if self.power_mode else self.color
        if self.sprite_type == 'pacman':
            pyxel.circ(self.x, self.y, 6, color)
            if self.direction == 'right':
                pyxel.tri(self.x, self.y, self.x + 6, self.y - 4, self.x + 6, self.y + 4, 0)
            elif self.direction == 'left':
                pyxel.tri(self.x, self.y, self.x - 6, self.y - 4, self.x - 6, self.y + 4, 0)
            elif self.direction == 'up':
                pyxel.tri(self.x, self.y, self.x - 4, self.y - 6, self.x + 4, self.y - 6, 0)
            elif self.direction == 'down':
                pyxel.tri(self.x, self.y, self.x - 4, self.y + 6, self.x + 4, self.y + 6, 0)
        elif self.sprite_type == 'ghost':
            pyxel.rect(self.x - 6, self.y - 6, 12, 10, color)
            pyxel.circ(self.x, self.y - 3, 6, color)
            for i in range(3):
                x = self.x - 6 + i * 4
                pyxel.rect(x, self.y + 4, 3, 3, color)
            pyxel.pset(self.x - 3, self.y - 3, 0)
            pyxel.pset(self.x + 3, self.y - 3, 0)
        elif self.sprite_type == 'invader':
            pyxel.rect(self.x - 5, self.y - 4, 10, 5, color)
            pyxel.rect(self.x - 7, self.y - 2, 14, 3, color)
            pyxel.pset(self.x - 2, self.y - 2, 0)
            pyxel.pset(self.x + 2, self.y - 2, 0)
            pyxel.pset(self.x - 5, self.y + 3, color)
            pyxel.pset(self.x + 5, self.y + 3, color)

class PowerPellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.phase = random.uniform(0, math.pi * 2)
        self.collected = False
        
    def update(self):
        self.phase += 0.1
        
    def draw(self):
        if not self.collected:
            size = 4 + math.sin(self.phase) * 2
            pyxel.circ(self.x, self.y, size, 10)
            
class PhantomArcade:
    def __init__(self):
        pyxel.init(512, 512, title="Phantom Arcade")
        pyxel.cls(0)
        
        self.sprites = []
        sprite_types = ['pacman', 'ghost', 'invader']
        for _ in range(8):
            x = random.randint(96, 416)
            y = random.randint(96, 416)
            sprite_type = random.choice(sprite_types)
            self.sprites.append(GhostSprite(x, y, sprite_type))
            
        self.pellets = []
        for _ in range(5):
            x = random.randint(96, 416) // 32 * 32
            y = random.randint(96, 416) // 32 * 32
            self.pellets.append(PowerPellet(x, y))
            
        self.maze_fade = 1.0
        self.frame_count = 0
        self.glitch_timer = 0
        self.scan_lines = []
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)
        
    def setup_sound(self):
        # Classic arcade coin/waka sound
        pyxel.sounds[0].set(
            "c2c2",
            "t",
            "7",
            "v",
            5
        )
        
        # Ghost movement sound
        pyxel.sounds[1].set(
            "e1g1e1g1",
            "t",
            "7654",
            "v",
            8
        )
        
        # Power pellet collection
        pyxel.sounds[2].set(
            "c1c1g1g1e2e2c2c2",
            "t",
            "76543210",
            "v",
            15
        )
        
        # Power mode activation
        pyxel.sounds[3].set(
            "c3e3g3c4",
            "s",
            "7654",
            "v",
            10
        )
        
        # Collision/glitch sound
        pyxel.sounds[4].set(
            "g1g1g1g1",
            "n",
            "7654",
            "v",
            4
        )
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.frame_count += 1
        
        for sprite in self.sprites:
            sprite.update()
            
        for pellet in self.pellets:
            pellet.update()
            if not pellet.collected:
                for sprite in self.sprites:
                    dist = math.sqrt((sprite.x - pellet.x)**2 + (sprite.y - pellet.y)**2)
                    if dist < 16:
                        pellet.collected = True
                        sprite.activate_power()
                        
        for pellet in [p for p in self.pellets if p.collected]:
            self.pellets.remove(pellet)
            x = random.randint(96, 416) // 32 * 32
            y = random.randint(96, 416) // 32 * 32
            self.pellets.append(PowerPellet(x, y))
            
        for i, s1 in enumerate(self.sprites):
            for s2 in self.sprites[i+1:]:
                dist = math.sqrt((s1.x - s2.x)**2 + (s1.y - s2.y)**2)
                if dist < 16:
                    s1.turn()
                    s2.turn()
                    self.glitch_timer = 10
                    pyxel.play(2, 4)
                    
        if self.frame_count % 300 == 0:
            self.maze_fade = 0.2
            
        if self.maze_fade < 1.0:
            self.maze_fade += 0.01
            
        if self.glitch_timer > 0:
            self.glitch_timer -= 1
            
        if random.random() < 0.005:
            dead_sprite = random.choice(self.sprites)
            self.sprites.remove(dead_sprite)
            x = random.randint(96, 416)
            y = random.randint(96, 416)
            sprite_type = random.choice(['pacman', 'ghost', 'invader'])
            self.sprites.append(GhostSprite(x, y, sprite_type))
            pyxel.play(3, 2)
            
    def draw_maze(self):
        color = int(self.maze_fade * 5) + 1
        
        pyxel.rectb(64, 64, 384, 384, color)
        pyxel.rectb(96, 96, 320, 320, color)
        
        for i in range(3):
            for j in range(3):
                if (i + j) % 2 == 0:
                    x = 128 + i * 96
                    y = 128 + j * 96
                    pyxel.rectb(x, y, 64, 64, color)
                    
        for i in range(5):
            x = 96 + i * 80
            pyxel.line(x, 96, x, 160, color)
            pyxel.line(x, 352, x, 416, color)
            
        for i in range(5):
            y = 96 + i * 80
            pyxel.line(96, y, 160, y, color)
            pyxel.line(352, y, 416, y, color)
            
    def draw(self):
        pyxel.cls(0)
        
        self.draw_maze()
        
        for pellet in self.pellets:
            pellet.draw()
            
        for sprite in self.sprites:
            sprite.draw()
            
        if self.glitch_timer > 0:
            for _ in range(20):
                x = random.randint(0, 512)
                y = random.randint(0, 512)
                w = random.randint(10, 50)
                h = random.randint(1, 5)
                color = random.randint(0, 15)
                pyxel.rect(x, y, w, h, color)
                
        for y in range(0, 512, 4):
            if y % 8 == 0:
                pyxel.line(0, y, 512, y, 1)
                
        pyxel.text(5, 5, "PHANTOM ARCADE", 5)
        pyxel.text(5, 500, "INSERT COIN", 5 + int(math.sin(self.frame_count * 0.1) * 2))

PhantomArcade()