"""
Signal Static - Anechoicetry Collection
by Leo Kuroshita
Television-style noise patterns that occasionally resolve into recognizable shapes
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random
import math

class StaticPixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.intensity = random.random()
        self.color = self.get_static_color()
        self.update_timer = random.randint(1, 8)
        
    def get_static_color(self):
        # TV static colors - mostly grays with occasional other colors
        if random.random() < 0.7:
            return random.choice([0, 5, 6, 7])  # Black to white
        else:
            return random.choice([1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15])  # Colored noise
    
    def update(self):
        self.update_timer -= 1
        if self.update_timer <= 0:
            self.intensity = random.random()
            self.color = self.get_static_color()
            self.update_timer = random.randint(1, 8)

class RecognizableShape:
    def __init__(self, shape_type, center_x, center_y):
        self.shape_type = shape_type
        self.center_x = center_x
        self.center_y = center_y
        self.visibility = 0  # 0 = invisible, 1 = fully visible
        self.target_visibility = 0
        self.fade_speed = 0.02
        self.size = random.uniform(30, 80)
        self.rotation = 0
        self.rotation_speed = random.uniform(-0.02, 0.02)
        self.life_timer = 0
        self.max_life = random.randint(180, 360)
        self.static_overlay = 0.3  # Amount of static overlay on shape
        
    def update(self):
        # Update visibility
        if self.visibility < self.target_visibility:
            self.visibility += self.fade_speed
        elif self.visibility > self.target_visibility:
            self.visibility -= self.fade_speed
        
        self.visibility = max(0, min(1, self.visibility))
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Update life timer
        self.life_timer += 1
        
        # Manage visibility lifecycle
        if self.life_timer < 60:  # Fade in
            self.target_visibility = min(1.0, self.life_timer / 60)
        elif self.life_timer > self.max_life - 60:  # Fade out
            remaining = self.max_life - self.life_timer
            self.target_visibility = max(0, remaining / 60)
        else:  # Full visibility with occasional flicker
            if random.random() < 0.05:
                self.target_visibility = random.uniform(0.3, 1.0)
            else:
                self.target_visibility = 0.8
        
        return self.life_timer < self.max_life
    
    def draw_shape_pixel(self, x, y, base_color):
        """Draw a pixel with static overlay"""
        if 0 <= x < 512 and 0 <= y < 512:
            if random.random() < self.static_overlay:
                # Static overlay
                static_color = random.choice([0, 5, 6, 7])
                pyxel.pset(x, y, static_color)
            else:
                # Shape color with visibility
                if random.random() < self.visibility:
                    pyxel.pset(x, y, base_color)
    
    def draw(self):
        if self.visibility <= 0:
            return
            
        base_color = 7  # White for most shapes
        
        if self.shape_type == 'circle':
            # Draw circle
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                for r in range(int(self.size)):
                    x = int(self.center_x + r * math.cos(rad))
                    y = int(self.center_y + r * math.sin(rad))
                    if r > self.size - 3:  # Only draw border
                        self.draw_shape_pixel(x, y, base_color)
        
        elif self.shape_type == 'square':
            # Draw square
            half_size = int(self.size // 2)
            for i in range(-half_size, half_size):
                for j in range(-half_size, half_size):
                    # Rotate point
                    cos_r = math.cos(self.rotation)
                    sin_r = math.sin(self.rotation)
                    rx = i * cos_r - j * sin_r
                    ry = i * sin_r + j * cos_r
                    
                    x = int(self.center_x + rx)
                    y = int(self.center_y + ry)
                    
                    # Only draw border
                    if abs(i) > half_size - 3 or abs(j) > half_size - 3:
                        self.draw_shape_pixel(x, y, base_color)
        
        elif self.shape_type == 'triangle':
            # Draw triangle
            points = []
            for i in range(3):
                angle = self.rotation + (i / 3) * math.pi * 2
                x = int(self.center_x + self.size * math.cos(angle))
                y = int(self.center_y + self.size * math.sin(angle))
                points.append((x, y))
            
            # Draw triangle edges
            for i in range(3):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % 3]
                self.draw_line_with_static(x1, y1, x2, y2, base_color)
        
        elif self.shape_type == 'cross':
            # Draw cross
            half_size = int(self.size // 2)
            thickness = 3
            
            # Horizontal bar
            for x in range(-half_size, half_size):
                for y in range(-thickness, thickness):
                    cos_r = math.cos(self.rotation)
                    sin_r = math.sin(self.rotation)
                    rx = x * cos_r - y * sin_r
                    ry = x * sin_r + y * cos_r
                    
                    px = int(self.center_x + rx)
                    py = int(self.center_y + ry)
                    self.draw_shape_pixel(px, py, base_color)
            
            # Vertical bar
            for x in range(-thickness, thickness):
                for y in range(-half_size, half_size):
                    cos_r = math.cos(self.rotation)
                    sin_r = math.sin(self.rotation)
                    rx = x * cos_r - y * sin_r
                    ry = x * sin_r + y * cos_r
                    
                    px = int(self.center_x + rx)
                    py = int(self.center_y + ry)
                    self.draw_shape_pixel(px, py, base_color)
    
    def draw_line_with_static(self, x1, y1, x2, y2, color):
        """Draw a line with static interference"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steps = max(dx, dy)
        
        if steps == 0:
            return
            
        x_inc = (x2 - x1) / steps
        y_inc = (y2 - y1) / steps
        
        for i in range(steps):
            x = int(x1 + i * x_inc)
            y = int(y1 + i * y_inc)
            self.draw_shape_pixel(x, y, color)

class SignalStatic:
    def __init__(self):
        pyxel.init(512, 512, title="Signal Static")
        
        # Sound design - TV/electronic interference
        pyxel.sounds[0].set("g1", "n", "7654321", "f", 25)    # Static noise
        pyxel.sounds[1].set("c2e2", "n", "543", "v", 20)      # Signal interference
        pyxel.sounds[2].set("f2", "s", "76543", "f", 18)      # Channel tuning
        pyxel.sounds[3].set("a1d2", "n", "432", "v", 15)      # Signal lock
        pyxel.sounds[4].set("g2b2", "p", "321", "f", 22)      # Signal found
        pyxel.sounds[5].set("c1", "n", "765", "f", 30)        # Deep static
        
        # Static field
        self.static_pixels = []
        self.static_density = 0.15  # Percentage of screen covered by static
        
        # Initialize static field
        num_static_pixels = int(512 * 512 * self.static_density)
        for _ in range(num_static_pixels):
            x = random.randint(0, 511)
            y = random.randint(0, 511)
            self.static_pixels.append(StaticPixel(x, y))
        
        # Recognizable shapes
        self.shapes = []
        self.shape_spawn_timer = 0
        self.shape_spawn_interval = 200
        
        # Global interference
        self.interference_level = 0.5
        self.interference_timer = 0
        self.scan_lines = True
        self.scan_line_offset = 0
        
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update static pixels
        for pixel in self.static_pixels:
            pixel.update()
        
        # Update shapes
        self.shapes = [shape for shape in self.shapes if shape.update()]
        
        # Spawn new shapes occasionally
        self.shape_spawn_timer += 1
        if self.shape_spawn_timer >= self.shape_spawn_interval:
            if len(self.shapes) < 3 and random.random() < 0.7:
                self.spawn_shape()
            self.shape_spawn_timer = 0
            self.shape_spawn_interval = random.randint(150, 300)
        
        # Update interference level
        self.interference_timer += 1
        if self.interference_timer >= 120:
            self.interference_level = random.uniform(0.2, 0.8)
            self.interference_timer = 0
        
        # Update scan lines
        self.scan_line_offset += 2
        if self.scan_line_offset >= 512:
            self.scan_line_offset = 0
        
        # Sound triggers
        if self.time % 60 == 0 and random.random() < 0.8:
            pyxel.play(0, 0, loop=False)  # Static noise
        
        if self.time % 180 == 0 and random.random() < 0.4:
            pyxel.play(1, 5, loop=False)  # Deep static
        
        # Signal interference
        if self.time % 90 == 45 and random.random() < 0.3:
            pyxel.play(1, 1, loop=False)  # Signal interference
        
        # Shape appearance sounds
        if len(self.shapes) > 0 and self.time % 120 == 60 and random.random() < 0.5:
            pyxel.play(2, 3, loop=False)  # Signal lock
        
        # Channel tuning
        if self.interference_level > 0.6 and self.time % 150 == 75 and random.random() < 0.4:
            pyxel.play(2, 2, loop=False)  # Channel tuning
        
        # Signal found
        for shape in self.shapes:
            if shape.visibility > 0.7 and random.random() < 0.02:
                pyxel.play(1, 4, loop=False)  # Signal found
        
        self.time += 1
    
    def spawn_shape(self):
        """Spawn a new recognizable shape"""
        shape_types = ['circle', 'square', 'triangle', 'cross']
        shape_type = random.choice(shape_types)
        
        x = random.randint(100, 412)
        y = random.randint(100, 412)
        
        shape = RecognizableShape(shape_type, x, y)
        self.shapes.append(shape)
    
    def draw(self):
        # Black background
        pyxel.cls(0)
        
        # Draw static field
        for pixel in self.static_pixels:
            if random.random() < self.interference_level:
                pyxel.pset(pixel.x, pixel.y, pixel.color)
        
        # Draw recognizable shapes
        for shape in self.shapes:
            shape.draw()
        
        # Draw scan lines (TV effect)
        if self.scan_lines:
            for y in range(0, 512, 4):
                scan_y = (y + self.scan_line_offset) % 512
                if random.random() < 0.3:
                    for x in range(0, 512, 8):
                        if random.random() < 0.5:
                            pyxel.pset(x, scan_y, 1)
        
        # Add random interference bursts
        if random.random() < 0.1:
            for _ in range(20):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                color = random.choice([7, 15])
                pyxel.pset(x, y, color)
        
        # Occasional full-screen interference
        if random.random() < 0.01:
            for _ in range(100):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                pyxel.pset(x, y, random.choice([0, 7, 15]))

SignalStatic()