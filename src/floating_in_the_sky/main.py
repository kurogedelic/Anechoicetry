"""
Floating in the Sky - Anechoicetry Collection
by Leo Kuroshita
Tribute to René Magritte: surrealist floating clouds and umbrellas in impossible sky
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class FloatingElement:
    def __init__(self, x, y, element_type):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.element_type = element_type  # 'cloud', 'umbrella', 'bowler_hat', 'apple'
        
        # Surrealist movement patterns
        self.float_speed = random.uniform(0.3, 0.8)
        self.float_amplitude_x = random.uniform(20, 60)
        self.float_amplitude_y = random.uniform(15, 40)
        self.float_phase_x = random.uniform(0, math.pi * 2)
        self.float_phase_y = random.uniform(0, math.pi * 2)
        
        # Element properties
        if element_type == 'cloud':
            self.size = random.uniform(30, 80)
            self.color = 7  # White
            self.secondary_color = 6  # Light gray
            self.puffiness = random.randint(4, 8)
        elif element_type == 'umbrella':
            self.size = random.uniform(40, 70)
            self.color = 0  # Black (classic Magritte)
            self.handle_length = self.size * 0.8
            self.rotation = random.uniform(0, math.pi * 2)
            self.rotation_speed = random.uniform(-0.02, 0.02)
        elif element_type == 'bowler_hat':
            self.size = random.uniform(25, 45)
            self.color = 0  # Black
            self.rotation = random.uniform(-0.3, 0.3)
        elif element_type == 'apple':
            self.size = random.uniform(15, 25)
            self.color = 8  # Red (Son of Man reference)
            self.leaf_color = 11  # Green
        
        # Surrealist properties
        self.gravity_direction = random.choice([-1, 1])  # Some elements float up
        self.dream_phase = random.uniform(0, math.pi * 2)
        self.impossibility_factor = random.uniform(0.5, 1.5)
        
    def update(self, time):
        # Dreamlike floating movement
        self.float_phase_x += self.float_speed * 0.01
        self.float_phase_y += self.float_speed * 0.008
        
        # Magritte-inspired impossible physics
        self.x = self.base_x + self.float_amplitude_x * math.sin(self.float_phase_x) * self.impossibility_factor
        self.y = self.base_y + self.float_amplitude_y * math.cos(self.float_phase_y) * self.gravity_direction
        
        # Subtle rotation for umbrellas
        if self.element_type == 'umbrella':
            self.rotation += self.rotation_speed
        
        # Dream phase for surreal effects
        self.dream_phase += 0.02
        
        # Gentle drift
        self.base_x += math.sin(time * 0.001) * 0.1
        self.base_y += math.cos(time * 0.0008) * 0.05
        
        # Wrap around screen boundaries with surreal logic
        if self.x < -100:
            self.x = 612
        elif self.x > 612:
            self.x = -100
        if self.y < -100:
            self.y = 612
        elif self.y > 612:
            self.y = -100
    
    def draw(self):
        x = int(self.x)
        y = int(self.y)
        
        if self.element_type == 'cloud':
            self.draw_cloud(x, y)
        elif self.element_type == 'umbrella':
            self.draw_umbrella(x, y)
        elif self.element_type == 'bowler_hat':
            self.draw_bowler_hat(x, y)
        elif self.element_type == 'apple':
            self.draw_apple(x, y)
    
    def draw_cloud(self, x, y):
        """Draw a fluffy Magritte-style cloud"""
        size = int(self.size)
        
        # Multiple overlapping circles for cloud puffiness
        for i in range(self.puffiness):
            offset_x = random.randint(-size//3, size//3)
            offset_y = random.randint(-size//4, size//4)
            radius = random.randint(size//4, size//2)
            
            cloud_x = x + offset_x
            cloud_y = y + offset_y
            
            if 0 <= cloud_x < 512 and 0 <= cloud_y < 512:
                # White center
                pyxel.circ(cloud_x, cloud_y, radius, self.color)
                # Gray outline for definition
                pyxel.circb(cloud_x, cloud_y, radius, self.secondary_color)
    
    def draw_umbrella(self, x, y):
        """Draw a floating umbrella (Magritte motif)"""
        size = int(self.size)
        
        # Umbrella canopy
        canopy_points = []
        for i in range(8):
            angle = (i / 8) * math.pi * 2 + self.rotation
            ux = x + (size * 0.8) * math.cos(angle)
            uy = y + (size * 0.3) * math.sin(angle)
            canopy_points.append((int(ux), int(uy)))
        
        # Draw canopy outline
        for i in range(len(canopy_points)):
            x1, y1 = canopy_points[i]
            x2, y2 = canopy_points[(i + 1) % len(canopy_points)]
            if (0 <= x1 < 512 and 0 <= y1 < 512 and 
                0 <= x2 < 512 and 0 <= y2 < 512):
                pyxel.line(x1, y1, x2, y2, self.color)
        
        # Umbrella handle
        handle_x = x
        handle_y = y + size//2
        handle_end_y = handle_y + int(self.handle_length)
        
        if 0 <= handle_x < 512 and 0 <= handle_y < 512 and 0 <= handle_end_y < 512:
            pyxel.line(handle_x, handle_y, handle_x, handle_end_y, self.color)
            # Curved handle end
            pyxel.line(handle_x, handle_end_y, handle_x + 5, handle_end_y, self.color)
    
    def draw_bowler_hat(self, x, y):
        """Draw a floating bowler hat (Magritte signature)"""
        size = int(self.size)
        
        # Hat crown (ellipse)
        crown_width = size
        crown_height = size // 2
        
        # Simple ellipse approximation
        for angle_deg in range(0, 360, 10):
            angle = math.radians(angle_deg)
            px = x + (crown_width // 2) * math.cos(angle)
            py = y + (crown_height // 2) * math.sin(angle) + self.rotation * 10
            if 0 <= px < 512 and 0 <= py < 512:
                pyxel.pset(int(px), int(py), self.color)
        
        # Hat brim
        brim_y = y + crown_height // 2
        brim_width = crown_width + 10
        
        if 0 <= brim_y < 512:
            pyxel.line(max(0, x - brim_width//2), brim_y, 
                      min(511, x + brim_width//2), brim_y, self.color)
            # Brim thickness
            pyxel.line(max(0, x - brim_width//2), brim_y + 1, 
                      min(511, x + brim_width//2), brim_y + 1, self.color)
    
    def draw_apple(self, x, y):
        """Draw a floating apple (Son of Man reference)"""
        size = int(self.size)
        
        # Apple body
        if 0 <= x < 512 and 0 <= y < 512:
            pyxel.circ(x, y, size//2, self.color)
            
            # Apple leaf
            leaf_x = x + size//3
            leaf_y = y - size//2
            if 0 <= leaf_x < 512 and 0 <= leaf_y < 512:
                pyxel.line(leaf_x, leaf_y, leaf_x + 3, leaf_y - 3, self.leaf_color)
                pyxel.line(leaf_x + 3, leaf_y - 3, leaf_x + 6, leaf_y - 1, self.leaf_color)

class FloatingInTheSky:
    def __init__(self):
        pyxel.init(512, 512, title="Floating in the Sky")
        
        # Sound design - surreal, dreamlike, atmospheric
        pyxel.sounds[0].set("c3e3g3", "t", "654", "f", 45)    # Dreamy atmosphere
        pyxel.sounds[1].set("f2a2c3", "s", "321", "v", 35)    # Floating whisper
        pyxel.sounds[2].set("g2b2d3", "t", "543", "s", 25)    # Surreal harmony
        pyxel.sounds[3].set("e3g3", "n", "76", "f", 20)       # Impossible sound
        pyxel.sounds[4].set("a2d3f3", "s", "432", "v", 40)    # Sky movement
        pyxel.sounds[5].set("c2f2", "t", "65", "s", 15)       # Distant echo
        
        # Create floating elements in surreal arrangement
        self.elements = []
        
        # Clouds (most prominent)
        for _ in range(8):
            x = random.uniform(50, 462)
            y = random.uniform(50, 462)
            self.elements.append(FloatingElement(x, y, 'cloud'))
        
        # Umbrellas (Magritte classic)
        for _ in range(6):
            x = random.uniform(80, 432)
            y = random.uniform(80, 432)
            self.elements.append(FloatingElement(x, y, 'umbrella'))
        
        # Bowler hats (Magritte signature)
        for _ in range(4):
            x = random.uniform(100, 412)
            y = random.uniform(100, 412)
            self.elements.append(FloatingElement(x, y, 'bowler_hat'))
        
        # Apples (Son of Man reference)
        for _ in range(3):
            x = random.uniform(120, 392)
            y = random.uniform(120, 392)
            self.elements.append(FloatingElement(x, y, 'apple'))
        
        # Sky state
        self.time = 0
        self.sky_phase = 0
        self.dream_intensity = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all floating elements
        for element in self.elements:
            element.update(self.time)
        
        # Update surreal atmosphere
        self.sky_phase += 0.01
        self.dream_intensity = (math.sin(self.sky_phase) + 1) / 2
        
        # Sound triggers - surreal and atmospheric
        if self.time % 150 == 0 and random.random() < 0.4:
            pyxel.play(0, 0, loop=False)  # Dreamy atmosphere
        
        if self.time % 200 == 100 and random.random() < 0.3:
            pyxel.play(1, 1, loop=False)  # Floating whisper
        
        # Surreal harmony
        if self.time % 180 == 90 and random.random() < 0.35:
            pyxel.play(2, 2, loop=False)  # Surreal harmony
        
        # Impossible sounds
        if self.time % 120 == 60 and random.random() < 0.25:
            pyxel.play(1, 3, loop=False)  # Impossible sound
        
        # Sky movement
        if self.time % 240 == 120 and random.random() < 0.4:
            pyxel.play(0, 4, loop=False)  # Sky movement
        
        # Distant echoes
        if self.time % 300 == 150 and random.random() < 0.2:
            pyxel.play(2, 5, loop=False)  # Distant echo
        
        self.time += 1
    
    def draw(self):
        # Magritte sky - surreal blue with subtle gradation
        base_color = 12  # Blue
        
        # Create subtle sky gradation
        for y in range(512):
            gradient_factor = y / 512
            if gradient_factor < 0.3:
                sky_color = 12  # Blue
            elif gradient_factor < 0.7:
                sky_color = 6   # Light gray
            else:
                sky_color = 7   # White (clouds blending into sky)
            
            # Draw gradient line with dream intensity variation
            if random.random() < 0.95 + self.dream_intensity * 0.05:
                pyxel.line(0, y, 512, y, sky_color)
        
        # Sort elements by distance (depth illusion)
        sorted_elements = sorted(self.elements, key=lambda e: e.y + e.size, reverse=True)
        
        # Draw all floating elements
        for element in sorted_elements:
            element.draw()
        
        # Occasional surreal effects
        if int(self.sky_phase * 100) % 300 < 50:
            self.draw_impossible_shadows()
    
    def draw_impossible_shadows(self):
        """Draw shadows that don't correspond to objects (Magritte style)"""
        shadow_color = 5  # Dark gray
        
        # Random impossible shadows
        for _ in range(3):
            if random.random() < 0.3:
                shadow_x = random.randint(50, 450)
                shadow_y = random.randint(400, 480)
                shadow_width = random.randint(30, 80)
                shadow_height = random.randint(8, 15)
                
                # Draw elliptical shadow
                for x in range(shadow_width):
                    for y in range(shadow_height):
                        if ((x - shadow_width//2) ** 2) / (shadow_width//2) ** 2 + \
                           ((y - shadow_height//2) ** 2) / (shadow_height//2) ** 2 <= 1:
                            px = shadow_x + x - shadow_width//2
                            py = shadow_y + y - shadow_height//2
                            if 0 <= px < 512 and 0 <= py < 512:
                                pyxel.pset(px, py, shadow_color)

FloatingInTheSky()