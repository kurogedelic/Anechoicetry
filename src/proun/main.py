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
        
        # Element properties - much bigger sizes, no text
        if element_type == 'number':
            # Include number 2 more frequently in the selection
            numbers = [0, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9]  # More 2s
            self.content = str(random.choice(numbers))
            self.size = random.uniform(60, 120)  # Much bigger numbers
            self.color = 0  # Black
        elif element_type == 'text':
            # Skip text elements - convert to geometric shapes instead
            self.element_type = 'square'
            self.content = None
            self.size = random.uniform(50, 90)
            self.color = random.choice([0, 8])  # Black or red
        elif element_type == 'square':
            self.content = None
            self.size = random.uniform(50, 100)  # Much bigger squares
            self.color = random.choice([0, 8])  # Black or red
        elif element_type == 'circle':
            self.content = None
            self.size = random.uniform(40, 80)  # Much bigger circles
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
        
        # Draw square - all filled, no borders
        self.draw_filled_polygon(rotated_corners)
    
    def draw_filled_polygon(self, corners):
        """Robust polygon fill without gaps"""
        if len(corners) < 3:
            return
            
        min_y = min(corner[1] for corner in corners) - 1
        max_y = max(corner[1] for corner in corners) + 1
        
        for y in range(min_y, max_y + 1):
            if y < 0 or y >= 512:
                continue
                
            intersections = []
            for i in range(len(corners)):
                x1, y1 = corners[i]
                x2, y2 = corners[(i + 1) % len(corners)]
                
                # Handle horizontal edges
                if y1 == y2:
                    if y == y1:
                        intersections.extend([x1, x2])
                    continue
                
                # Check if scan line intersects edge
                if min(y1, y2) < y < max(y1, y2):
                    x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x)
                elif y == y1:
                    intersections.append(x1)
                elif y == y2:
                    intersections.append(x2)
            
            if len(intersections) >= 2:
                intersections.sort()
                # Remove duplicates
                unique_intersections = []
                for x in intersections:
                    if not unique_intersections or abs(x - unique_intersections[-1]) > 0.5:
                        unique_intersections.append(x)
                
                # Fill between pairs
                for i in range(0, len(unique_intersections) - 1, 2):
                    if i + 1 < len(unique_intersections):
                        x1, x2 = int(unique_intersections[i]), int(unique_intersections[i + 1])
                        if x1 > x2:
                            x1, x2 = x2, x1
                        
                        # Fill with extra coverage to eliminate gaps
                        for x in range(max(0, x1 - 1), min(512, x2 + 2)):
                            if 0 <= x < 512 and 0 <= y < 512:
                                pyxel.pset(x, y, self.color)

class Proun:
    def __init__(self):
        pyxel.init(512, 512, title="Proun")
        
        # Sound design - minimal staccato sequences with drum sounds
        pyxel.sounds[0].set("c3", "p", "7", "s", 8)           # Short staccato
        pyxel.sounds[1].set("f3", "p", "6", "s", 6)           # Brief note
        pyxel.sounds[2].set("g3", "p", "5", "s", 10)          # Quick pulse
        pyxel.sounds[3].set("d3", "p", "4", "s", 7)           # Minimal click
        pyxel.sounds[4].set("a2", "p", "3", "s", 9)           # Short burst
        pyxel.sounds[5].set("e3", "p", "2", "s", 5)           # Tiny staccato
        pyxel.sounds[6].set("c1", "n", "7", "n", 15)          # Low kick drum
        pyxel.sounds[7].set("c4", "n", "4", "n", 8)           # High snare
        
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
        
        # Sound triggers - synchronized rhythmic sequence with white noise drums
        beat = self.time % 120  # 4-second loop at 30fps
        
        # White noise kick drum - on beats 1 and 3
        if beat in [0, 60]:
            pyxel.play(0, 6, loop=False)  # White noise kick
        
        # White noise snare - on beats 2 and 4
        if beat in [30, 90]:
            pyxel.play(1, 7, loop=False)  # White noise snare
        
        # Melodic elements synchronized to the drum pattern
        if beat == 0:  # Downbeat
            pyxel.play(2, 0, loop=False)  # Short staccato
        
        if beat == 15:  # Off-beat
            pyxel.play(1, 1, loop=False)  # Brief note
        
        if beat == 30:  # Snare beat
            pyxel.play(0, 2, loop=False)  # Quick pulse
        
        if beat == 45:  # Syncopated
            pyxel.play(2, 3, loop=False)  # Minimal click
        
        if beat == 60:  # Half note
            pyxel.play(1, 4, loop=False)  # Short burst
        
        if beat == 75:  # Off-beat accent
            if random.random() < 0.6:
                pyxel.play(0, 5, loop=False)  # Tiny staccato
        
        # Additional rhythmic fills
        if beat in [105, 110, 115]:  # End of phrase fills
            if random.random() < 0.3:
                pyxel.play(2, 7, loop=False)  # Snare fill
        
        self.time += 1
    
    def draw(self):
        # White background (Lissitzky's choice)
        pyxel.cls(7)
        
        # Sort elements by depth for proper layering
        sorted_elements = sorted(self.elements, key=lambda e: e.z, reverse=True)
        
        # Draw all elements
        for element in sorted_elements:
            element.draw()
        
    

Proun()