"""
Fermata - Anechoicetry Collection
by Leo Kuroshita
Final piece: colorful pastel tiles with dancing pale curves inspired by Paul Klee
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 2.0.0
"""

import pyxel
import math
import random

class PastelTile:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        # Thinner, more delicate pastel palette
        self.colors = [6, 7, 15, 14, 10, 11, 5]  # Light gray, white, peach, pink, yellow, green, dark gray
        self.color = random.choice(self.colors)
        self.base_color = self.color
        self.target_color = self.color
        
        # Tile properties
        self.brightness_phase = random.uniform(0, math.pi * 2)
        self.brightness_speed = random.uniform(0.01, 0.03)
        self.pattern_type = random.choice(['solid', 'striped', 'dotted', 'cross'])
        self.pattern_phase = random.uniform(0, math.pi * 2)
        
        # Color swapping properties
        self.color_swap_timer = random.randint(120, 300)
        self.fade_progress = 0.0
        self.fade_speed = 0.02
        self.is_fading = False
        
    def update(self, time):
        # Gentle brightness oscillation
        self.brightness_phase += self.brightness_speed
        brightness = 0.8 + 0.2 * math.sin(self.brightness_phase)
        
        # Subtle pattern animation
        self.pattern_phase += 0.02
        
        # Color swapping and fading
        self.color_swap_timer -= 1
        if self.color_swap_timer <= 0 and not self.is_fading:
            # Start fade to new color
            self.target_color = random.choice([c for c in self.colors if c != self.color])
            self.is_fading = True
            self.fade_progress = 0.0
            self.color_swap_timer = random.randint(180, 400)
        
        # Handle cross-fade between colors
        if self.is_fading:
            self.fade_progress += self.fade_speed
            if self.fade_progress >= 1.0:
                self.color = self.target_color
                self.is_fading = False
                self.fade_progress = 0.0
        
    def draw(self):
        x, y = int(self.x), int(self.y)
        size = int(self.size)
        
        # Draw base tile with cross-fade effect
        if 0 <= x < 512 and 0 <= y < 512:
            if self.is_fading:
                # Cross-fade between colors using dithering pattern
                fade_threshold = self.fade_progress
                for dy in range(min(size, 512-y)):
                    for dx in range(min(size, 512-x)):
                        px, py = x + dx, y + dy
                        # Create dithering pattern for smooth fade
                        dither_value = ((px + py) % 4) / 4.0
                        if dither_value < fade_threshold:
                            pyxel.pset(px, py, self.target_color)
                        else:
                            pyxel.pset(px, py, self.color)
            else:
                pyxel.rect(x, y, min(size, 512-x), min(size, 512-y), self.color)
            
            # Add thinner pattern details
            if self.pattern_type == 'striped':
                self.draw_stripes(x, y, size)
            elif self.pattern_type == 'dotted':
                self.draw_dots(x, y, size)
            elif self.pattern_type == 'cross':
                self.draw_cross(x, y, size)
    
    def draw_stripes(self, x, y, size):
        """Draw subtle stripes on tile"""
        stripe_color = (self.color + 1) % 16
        for i in range(0, size, 4):
            if x + i < 512:
                pyxel.line(x + i, y, x + i, min(y + size, 511), stripe_color)
    
    def draw_dots(self, x, y, size):
        """Draw dots on tile"""
        dot_color = (self.color + 2) % 16
        for i in range(4, size - 4, 8):
            for j in range(4, size - 4, 8):
                if x + i < 512 and y + j < 512:
                    pyxel.pset(x + i, y + j, dot_color)
    
    def draw_cross(self, x, y, size):
        """Draw cross pattern on tile"""
        cross_color = (self.color + 3) % 16
        mid_x, mid_y = x + size//2, y + size//2
        if mid_x < 512 and mid_y < 512:
            # Horizontal line
            pyxel.line(x, mid_y, min(x + size, 511), mid_y, cross_color)
            # Vertical line
            pyxel.line(mid_x, y, mid_x, min(y + size, 511), cross_color)

class PaleCurve:
    def __init__(self):
        # Curve properties
        self.points = []
        self.num_points = random.randint(8, 16)
        
        # Generate smooth curve points
        for i in range(self.num_points):
            t = i / (self.num_points - 1)
            base_x = t * 512
            base_y = 256 + 100 * math.sin(t * math.pi * 2 + random.uniform(0, math.pi))
            self.points.append([base_x, base_y])
        
        # Curve movement
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.005, 0.02)
        self.amplitude_x = random.uniform(10, 30)
        self.amplitude_y = random.uniform(15, 40)
        
        # Thinner, more ethereal colors for curves
        self.curve_colors = [6, 7, 5, 13, 15, 14]  # Light gray, white, dark gray, lavender, peach, pink
        self.color = random.choice(self.curve_colors)
        self.target_color = self.color
        self.thickness = random.randint(1, 2)  # Thinner curves
        
        # Curve color fading
        self.color_fade_timer = random.randint(180, 360)
        self.curve_fade_progress = 0.0
        self.curve_fade_speed = 0.015
        self.curve_is_fading = False
        
        # Dancing properties
        self.dance_phase_x = random.uniform(0, math.pi * 2)
        self.dance_phase_y = random.uniform(0, math.pi * 2)
        self.dance_speed_x = random.uniform(0.01, 0.03)
        self.dance_speed_y = random.uniform(0.008, 0.025)
        
    def update(self, time, global_rhythm):
        # Update dance phases
        self.dance_phase_x += self.dance_speed_x
        self.dance_phase_y += self.dance_speed_y
        
        # Update curve movement
        self.phase += self.speed
        
        # Color fading for curves
        self.color_fade_timer -= 1
        if self.color_fade_timer <= 0 and not self.curve_is_fading:
            # Start fade to new color
            self.target_color = random.choice([c for c in self.curve_colors if c != self.color])
            self.curve_is_fading = True
            self.curve_fade_progress = 0.0
            self.color_fade_timer = random.randint(240, 480)
        
        # Handle curve color cross-fade
        if self.curve_is_fading:
            self.curve_fade_progress += self.curve_fade_speed
            if self.curve_fade_progress >= 1.0:
                self.color = self.target_color
                self.curve_is_fading = False
                self.curve_fade_progress = 0.0
        
        # Apply dancing movement to each point
        for i, point in enumerate(self.points):
            t = i / (len(self.points) - 1)
            
            # Base oscillation
            wave_x = self.amplitude_x * math.sin(self.phase + t * math.pi * 2)
            wave_y = self.amplitude_y * math.cos(self.phase + t * math.pi * 1.5)
            
            # Dancing movement
            dance_x = 15 * math.sin(self.dance_phase_x + t * math.pi * 3) * global_rhythm
            dance_y = 10 * math.cos(self.dance_phase_y + t * math.pi * 2.5) * global_rhythm
            
            # Apply movements
            base_x = t * 512
            base_y = 256 + 100 * math.sin(t * math.pi * 2 + self.phase * 0.5)
            
            point[0] = base_x + wave_x + dance_x
            point[1] = base_y + wave_y + dance_y
    
    def draw(self):
        # Draw smooth curve through points with color fading
        for i in range(len(self.points) - 1):
            x1, y1 = int(self.points[i][0]), int(self.points[i][1])
            x2, y2 = int(self.points[i + 1][0]), int(self.points[i + 1][1])
            
            # Draw curve segment with thickness and cross-fade
            if (0 <= x1 < 512 and 0 <= y1 < 512 and 
                0 <= x2 < 512 and 0 <= y2 < 512):
                
                if self.curve_is_fading:
                    # Cross-fade using alternating pixels
                    fade_threshold = self.curve_fade_progress
                    for thickness in range(self.thickness):
                        # Draw line with alternating colors based on fade progress
                        self.draw_fading_line(x1, y1 + thickness, x2, y2 + thickness, fade_threshold)
                        if thickness > 0:
                            self.draw_fading_line(x1, y1 - thickness, x2, y2 - thickness, fade_threshold)
                else:
                    for thickness in range(self.thickness):
                        pyxel.line(x1, y1 + thickness, x2, y2 + thickness, self.color)
                        if thickness > 0:
                            pyxel.line(x1, y1 - thickness, x2, y2 - thickness, self.color)
    
    def draw_fading_line(self, x1, y1, x2, y2, fade_threshold):
        """Draw a line with cross-fade between two colors"""
        # Simple line drawing with color interpolation
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        pixel_count = 0
        
        while True:
            if 0 <= x < 512 and 0 <= y < 512:
                # Alternate between colors based on position and fade progress
                dither_pattern = (x + y + pixel_count) % 3
                if dither_pattern / 3.0 < fade_threshold:
                    pyxel.pset(x, y, self.target_color)
                else:
                    pyxel.pset(x, y, self.color)
            
            if x == x2 and y == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
            
            pixel_count += 1

class Fermata:
    def __init__(self):
        pyxel.init(512, 512, title="Fermata")
        
        # Sound design - final piece, ethereal and complete
        pyxel.sounds[0].set("c4e4g4c4e4", "t", "76543", "f", 40)  # Ascending ethereal (fixed note)
        pyxel.sounds[1].set("f3a3c4f4", "s", "4321", "v", 30)     # Warm harmony (fixed volumes)
        pyxel.sounds[2].set("g3b3d4g4", "t", "4321", "s", 25)     # Dancing notes
        pyxel.sounds[3].set("e4g4b4", "n", "765", "f", 20)        # Crystalline
        pyxel.sounds[4].set("a3d4f4a4", "s", "6543", "v", 35)     # Flowing melody
        pyxel.sounds[5].set("c3f3a3", "t", "543", "s", 15)        # Final resonance
        
        # Create pastel tile grid
        self.tiles = []
        tile_size = 32
        
        for y in range(0, 512, tile_size):
            for x in range(0, 512, tile_size):
                self.tiles.append(PastelTile(x, y, tile_size))
        
        # Create dancing pale curves
        self.curves = []
        for _ in range(8):
            self.curves.append(PaleCurve())
        
        # Global state
        self.time = 0
        self.global_rhythm = 0
        self.final_harmony = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update global rhythm for dancing
        self.global_rhythm = (math.sin(self.time * 0.02) + 1) / 2
        
        # Final harmony builds over time
        self.final_harmony = min(1.0, self.time / 3600)  # Builds over 2 minutes
        
        # Update all tiles
        for tile in self.tiles:
            tile.update(self.time)
        
        # Update all curves
        for curve in self.curves:
            curve.update(self.time, self.global_rhythm)
        
        # Sound triggers - final piece soundscape
        if self.time % 180 == 0 and random.random() < 0.6:
            pyxel.play(0, 0, loop=False)  # Ascending ethereal
        
        if self.time % 150 == 75 and random.random() < 0.4:
            pyxel.play(1, 1, loop=False)  # Warm harmony
        
        # Dancing notes
        if self.time % 120 == 60 and random.random() < 0.5:
            pyxel.play(2, 2, loop=False)  # Dancing notes
        
        # Crystalline sounds
        if self.time % 90 == 45 and random.random() < 0.3:
            pyxel.play(1, 3, loop=False)  # Crystalline
        
        # Flowing melody
        if self.time % 200 == 100 and random.random() < 0.45:
            pyxel.play(0, 4, loop=False)  # Flowing melody
        
        # Final resonance (becomes more frequent over time)
        resonance_frequency = max(60, 300 - int(self.final_harmony * 240))
        if self.time % resonance_frequency == 0 and random.random() < 0.25 + self.final_harmony * 0.25:
            pyxel.play(2, 5, loop=False)  # Final resonance
        
        self.time += 1
    
    def draw(self):
        # Clear with deep pastel background
        pyxel.cls(4)  # Tan base
        
        # Draw all pastel tiles
        for tile in self.tiles:
            tile.draw()
        
        # Add animated background texture with thin colors
        if self.time % 2 == 0:  # More frequent animation
            for _ in range(30):  # More particles
                if random.random() < 0.15:
                    tx = random.randint(0, 511)
                    ty = random.randint(0, 511)
                    # Animate texture colors based on time
                    time_phase = (self.time * 0.01) % (math.pi * 2)
                    texture_colors = [6, 7, 15, 14, 5]
                    color_index = int((math.sin(time_phase + tx * 0.01) + 1) * 2.5) % len(texture_colors)
                    texture_color = texture_colors[color_index]
                    pyxel.pset(tx, ty, texture_color)
        
        # Add flowing background waves
        wave_phase = self.time * 0.005
        for i in range(0, 512, 8):
            wave_y = int(256 + 50 * math.sin(wave_phase + i * 0.02))
            if 0 <= wave_y < 512:
                wave_color = 5 if (i // 8) % 2 == 0 else 6
                if random.random() < 0.3:
                    pyxel.pset(i, wave_y, wave_color)
        
        # Draw dancing pale curves on top
        for curve in self.curves:
            curve.draw()
        
        # Final harmony effect - subtle sparkles
        if self.final_harmony > 0.3:
            sparkle_count = int(self.final_harmony * 10)
            for _ in range(sparkle_count):
                if random.random() < 0.3:
                    sx = random.randint(0, 511)
                    sy = random.randint(0, 511)
                    sparkle_color = random.choice([7, 15])  # White, peach
                    pyxel.pset(sx, sy, sparkle_color)

Fermata()