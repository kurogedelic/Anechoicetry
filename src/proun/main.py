"""
Proun - Anechoicetry Collection
by Leo Kuroshita
Tribute to El Lissitzky: black numbers, text, red and black geometric forms in 3D space
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random
import string

class ConstructivistElement:
    def __init__(self, x, y, z, element_type):
        self.x = x
        self.y = y
        self.z = z
        self.base_x = x
        self.base_y = y
        self.base_z = z
        self.element_type = element_type  # 'number', 'text', 'square', 'circle'
        
        # Element properties - bigger sizes, no text
        if element_type == 'number':
            self.content = str(random.randint(0, 9))
            self.size = random.uniform(40, 80)  # Much bigger numbers
            self.color = 0  # Black
        elif element_type == 'text':
            # Skip text elements - convert to geometric shapes instead
            self.element_type = 'square'
            self.content = None
            self.size = random.uniform(30, 60)
            self.color = random.choice([0, 8])  # Black or red
        elif element_type == 'square':
            self.content = None
            self.size = random.uniform(30, 70)  # Bigger squares
            self.color = random.choice([0, 8])  # Black or red
        elif element_type == 'circle':
            self.content = None
            self.size = random.uniform(25, 60)  # Bigger circles
            self.color = random.choice([0, 8])  # Black or red
        
        # 3D movement properties
        self.rotation_x = random.uniform(0, math.pi * 2)
        self.rotation_y = random.uniform(0, math.pi * 2)
        self.rotation_z = random.uniform(0, math.pi * 2)
        self.rotation_speed_x = random.uniform(-0.01, 0.01)
        self.rotation_speed_y = random.uniform(-0.01, 0.01)
        self.rotation_speed_z = random.uniform(-0.01, 0.01)
        
        # Constructivist movement (architectural)
        self.movement_axis = random.choice(['x', 'y', 'z', 'xy', 'xz', 'yz'])
        self.movement_speed = random.uniform(0.3, 0.8)
        self.movement_amplitude = random.uniform(30, 80)
        self.movement_phase = random.uniform(0, math.pi * 2)
        
        # Isometric projection properties
        self.projected_x = 0
        self.projected_y = 0
        self.depth_scale = 1.0
        
    def update(self, time):
        # Update rotations
        self.rotation_x += self.rotation_speed_x
        self.rotation_y += self.rotation_speed_y
        self.rotation_z += self.rotation_speed_z
        
        # Constructivist movement patterns
        self.movement_phase += self.movement_speed * 0.02
        
        if self.movement_axis == 'x':
            self.x = self.base_x + self.movement_amplitude * math.sin(self.movement_phase)
        elif self.movement_axis == 'y':
            self.y = self.base_y + self.movement_amplitude * math.sin(self.movement_phase)
        elif self.movement_axis == 'z':
            self.z = self.base_z + self.movement_amplitude * math.sin(self.movement_phase)
        elif self.movement_axis == 'xy':
            self.x = self.base_x + self.movement_amplitude * 0.7 * math.sin(self.movement_phase)
            self.y = self.base_y + self.movement_amplitude * 0.7 * math.cos(self.movement_phase)
        elif self.movement_axis == 'xz':
            self.x = self.base_x + self.movement_amplitude * 0.7 * math.sin(self.movement_phase)
            self.z = self.base_z + self.movement_amplitude * 0.7 * math.cos(self.movement_phase)
        elif self.movement_axis == 'yz':
            self.y = self.base_y + self.movement_amplitude * 0.7 * math.sin(self.movement_phase)
            self.z = self.base_z + self.movement_amplitude * 0.7 * math.cos(self.movement_phase)
        
        # Calculate isometric projection
        self.calculate_projection()
    
    def calculate_projection(self):
        """Convert 3D coordinates to isometric 2D projection"""
        # Isometric projection matrix
        # Standard isometric angles: 30 degrees
        angle = math.radians(30)
        
        # Apply rotations first
        x_rot = self.x
        y_rot = self.y * math.cos(self.rotation_x) - self.z * math.sin(self.rotation_x)
        z_rot = self.y * math.sin(self.rotation_x) + self.z * math.cos(self.rotation_x)
        
        # Isometric projection
        self.projected_x = (x_rot - z_rot) * math.cos(angle)
        self.projected_y = (x_rot + z_rot) * math.sin(angle) - y_rot
        
        # Center on screen
        self.projected_x += 256
        self.projected_y += 256
        
        # Calculate depth for layering
        self.depth_scale = max(0.3, 1 - (z_rot + 200) / 400)
    
    def draw(self):
        if self.projected_x < -50 or self.projected_x > 562 or self.projected_y < -50 or self.projected_y > 562:
            return
        
        x = int(self.projected_x)
        y = int(self.projected_y)
        scaled_size = self.size * self.depth_scale
        
        if self.element_type == 'number':
            # Draw large number
            if scaled_size > 8:
                # Scale font by drawing multiple times with offset
                scale_factor = max(1, int(scaled_size / 10))
                for dx in range(scale_factor):
                    for dy in range(scale_factor):
                        if 0 <= x + dx < 512 and 0 <= y + dy < 512:
                            pyxel.text(x + dx, y + dy, self.content, self.color)
        
        elif self.element_type == 'text':
            # Draw text
            if scaled_size > 4:
                pyxel.text(x, y, self.content, self.color)
        
        elif self.element_type == 'square':
            # Draw rotated square
            self.draw_rotated_square(x, y, scaled_size)
        
        elif self.element_type == 'circle':
            # Draw circle
            radius = max(1, int(scaled_size / 2))
            if self.color == 8:  # Red - draw filled
                pyxel.circ(x, y, radius, self.color)
            else:  # Black - draw outline
                pyxel.circb(x, y, radius, self.color)
    
    def draw_rotated_square(self, center_x, center_y, size):
        """Draw a rotated square using the current rotation"""
        half_size = size / 2
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        # Rotate corners
        cos_z = math.cos(self.rotation_z)
        sin_z = math.sin(self.rotation_z)
        
        rotated_corners = []
        for x, y in corners:
            rx = x * cos_z - y * sin_z
            ry = x * sin_z + y * cos_z
            rotated_corners.append((int(center_x + rx), int(center_y + ry)))
        
        # Draw square
        if self.color == 8:  # Red - draw filled
            self.draw_filled_polygon(rotated_corners)
        else:  # Black - draw outline
            for i in range(4):
                x1, y1 = rotated_corners[i]
                x2, y2 = rotated_corners[(i + 1) % 4]
                if (0 <= x1 < 512 and 0 <= y1 < 512 and 
                    0 <= x2 < 512 and 0 <= y2 < 512):
                    pyxel.line(x1, y1, x2, y2, self.color)
    
    def draw_filled_polygon(self, corners):
        """Simple polygon fill"""
        if len(corners) < 3:
            return
            
        min_y = min(corner[1] for corner in corners)
        max_y = max(corner[1] for corner in corners)
        
        for y in range(min_y, max_y + 1):
            if y < 0 or y >= 512:
                continue
                
            intersections = []
            for i in range(len(corners)):
                x1, y1 = corners[i]
                x2, y2 = corners[(i + 1) % len(corners)]
                
                if y1 != y2:
                    if min(y1, y2) <= y <= max(y1, y2):
                        x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        intersections.append(int(x))
            
            intersections.sort()
            for i in range(0, len(intersections) - 1, 2):
                x1, x2 = intersections[i], intersections[i + 1]
                for x in range(max(0, x1), min(512, x2 + 1)):
                    pyxel.pset(x, y, self.color)

class Proun:
    def __init__(self):
        pyxel.init(512, 512, title="Proun")
        
        # Sound design - minimal staccato sequences
        pyxel.sounds[0].set("c3", "p", "7", "s", 8)           # Short staccato
        pyxel.sounds[1].set("f3", "p", "6", "s", 6)           # Brief note
        pyxel.sounds[2].set("g3", "p", "5", "s", 10)          # Quick pulse
        pyxel.sounds[3].set("d3", "p", "4", "s", 7)           # Minimal click
        pyxel.sounds[4].set("a2", "p", "3", "s", 9)           # Short burst
        pyxel.sounds[5].set("e3", "p", "2", "s", 5)           # Tiny staccato
        
        # Create constructivist elements in 3D space
        self.elements = []
        
        # Large numbers (prominent in Lissitzky's work) - fewer but bigger
        for _ in range(4):
            x = random.uniform(-100, 100)
            y = random.uniform(-100, 100)
            z = random.uniform(-100, 100)
            self.elements.append(ConstructivistElement(x, y, z, 'number'))
        
        # More geometric squares (replacing text)
        for _ in range(12):
            x = random.uniform(-120, 120)
            y = random.uniform(-120, 120)
            z = random.uniform(-120, 120)
            self.elements.append(ConstructivistElement(x, y, z, 'square'))
        
        # More geometric circles
        for _ in range(10):
            x = random.uniform(-100, 100)
            y = random.uniform(-100, 100)
            z = random.uniform(-100, 100)
            self.elements.append(ConstructivistElement(x, y, z, 'circle'))
        
        # System state
        self.time = 0
        self.construction_phase = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all elements
        for element in self.elements:
            element.update(self.time)
        
        # Update construction phase
        self.construction_phase += 0.01
        
        # Sound triggers - minimal staccato sequences
        if self.time % 180 == 0 and random.random() < 0.3:
            pyxel.play(0, 0, loop=False)  # Short staccato
        
        if self.time % 220 == 110 and random.random() < 0.25:
            pyxel.play(1, 1, loop=False)  # Brief note
        
        # Quick pulse
        if self.time % 160 == 80 and random.random() < 0.2:
            pyxel.play(2, 2, loop=False)  # Quick pulse
        
        # Minimal clicks
        if self.time % 140 == 70 and random.random() < 0.15:
            pyxel.play(1, 3, loop=False)  # Minimal click
        
        # Short bursts
        if self.time % 200 == 100 and random.random() < 0.2:
            pyxel.play(0, 4, loop=False)  # Short burst
        
        # Tiny staccatos
        if self.time % 120 == 60 and random.random() < 0.1:
            pyxel.play(2, 5, loop=False)  # Tiny staccato
        
        self.time += 1
    
    def draw(self):
        # White background (Lissitzky's choice)
        pyxel.cls(7)
        
        # Sort elements by depth for proper layering
        sorted_elements = sorted(self.elements, key=lambda e: e.z, reverse=True)
        
        # Draw all elements
        for element in sorted_elements:
            element.draw()
        
        # Draw construction grid lines occasionally
        if int(self.construction_phase * 10) % 100 < 30:
            self.draw_construction_grid()
    
    def draw_construction_grid(self):
        """Draw faint construction/architectural grid lines"""
        grid_color = 5  # Gray
        
        # Vertical construction lines
        for x in range(0, 512, 64):
            if random.random() < 0.3:
                pyxel.line(x, 0, x, 512, grid_color)
        
        # Horizontal construction lines
        for y in range(0, 512, 64):
            if random.random() < 0.3:
                pyxel.line(0, y, 512, y, grid_color)
        
        # Diagonal construction lines (Lissitzky style)
        if random.random() < 0.2:
            pyxel.line(0, 0, 512, 512, grid_color)
        if random.random() < 0.2:
            pyxel.line(512, 0, 0, 512, grid_color)

Proun()