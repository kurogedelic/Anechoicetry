"""
Supremus - Anechoicetry Collection
by Leo Kuroshita
Inspired by Kazimir Malevich: orange, red, black, blue, and green shapes move slowly on flesh-colored canvas
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class SuprematistShape:
    def __init__(self, x, y, shape_type):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.shape_type = shape_type  # 'rectangle', 'circle', 'line', 'cross'
        self.width = random.uniform(40, 120)  # Larger components
        self.height = random.uniform(40, 120) if shape_type == 'rectangle' else self.width
        self.rotation = random.uniform(0, math.pi * 2)
        # Correct Malevich colors: red, orange, black, blue, green
        self.color = random.choice([8, 9, 0, 12, 11])  # Red, orange, black, blue, green
        
        # Movement properties
        self.drift_speed = random.uniform(0.005, 0.02)
        self.drift_angle = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-0.005, 0.005)
        self.orbit_radius = random.uniform(10, 30)
        self.orbit_speed = random.uniform(0.01, 0.03)
        self.orbit_phase = random.uniform(0, math.pi * 2)
        
        # Connection properties
        self.connected_to = []
        self.connection_strength = random.uniform(0.02, 0.08)
        
    def update(self, time, all_shapes):
        # Slow orbital drift
        self.orbit_phase += self.orbit_speed
        orbital_x = self.orbit_radius * math.cos(self.orbit_phase)
        orbital_y = self.orbit_radius * math.sin(self.orbit_phase) * 0.7  # Flattened orbit
        
        # Linear drift
        self.drift_angle += random.uniform(-0.01, 0.01)
        drift_x = math.cos(self.drift_angle) * self.drift_speed * 20
        drift_y = math.sin(self.drift_angle) * self.drift_speed * 20
        
        # Update position
        self.x = self.base_x + orbital_x + drift_x
        self.y = self.base_y + orbital_y + drift_y
        
        # Slow rotation
        self.rotation += self.rotation_speed
        
        # Connection forces (invisible magnetic-like attraction)
        for other in self.connected_to:
            if other in all_shapes:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance > 0:
                    # Maintain optimal distance (creates gaps between shapes)
                    optimal_distance = 100
                    force_strength = (distance - optimal_distance) * self.connection_strength * 0.001
                    
                    self.x += (dx / distance) * force_strength
                    self.y += (dy / distance) * force_strength
        
        # Keep within canvas bounds with gentle force
        margin = 50
        if self.x < margin:
            self.x += (margin - self.x) * 0.01
        elif self.x > 512 - margin:
            self.x += (512 - margin - self.x) * 0.01
            
        if self.y < margin:
            self.y += (margin - self.y) * 0.01
        elif self.y > 512 - margin:
            self.y += (512 - margin - self.y) * 0.01
    
    def draw(self):
        if self.shape_type == 'rectangle':
            self.draw_rotated_rectangle()
        elif self.shape_type == 'circle':
            self.draw_circle()
        elif self.shape_type == 'line':
            self.draw_line()
        elif self.shape_type == 'cross':
            self.draw_cross()
    
    def draw_rotated_rectangle(self):
        # Calculate rotated rectangle corners
        half_w = self.width / 2
        half_h = self.height / 2
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        
        corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h)
        ]
        
        rotated_corners = []
        for x, y in corners:
            rx = x * cos_r - y * sin_r
            ry = x * sin_r + y * cos_r
            rotated_corners.append((int(self.x + rx), int(self.y + ry)))
        
        # Draw filled rectangle using scanline algorithm
        self.draw_filled_polygon(rotated_corners)
    
    def draw_filled_polygon(self, corners):
        if len(corners) < 3:
            return
            
        # Simple polygon fill - draw horizontal lines with better precision
        min_y = min(corner[1] for corner in corners)
        max_y = max(corner[1] for corner in corners)
        
        for y in range(min_y, max_y + 1):
            if y < 0 or y >= 512:
                continue
                
            intersections = []
            
            # Find intersections with polygon edges
            for i in range(len(corners)):
                x1, y1 = corners[i]
                x2, y2 = corners[(i + 1) % len(corners)]
                
                if y1 != y2:  # Not horizontal line
                    if min(y1, y2) <= y < max(y1, y2):  # Avoid double counting at vertices
                        # Calculate intersection with better precision
                        x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        intersections.append(x)
            
            # Sort intersections and draw lines between pairs
            intersections.sort()
            for i in range(0, len(intersections) - 1, 2):
                x1, x2 = int(intersections[i]), int(intersections[i + 1])
                # Draw with slight overlap to fill gaps
                for x in range(max(0, x1), min(512, x2 + 2)):
                    pyxel.pset(x, y, self.color)
                    # Fill potential gaps with neighboring pixels
                    if x > 0:
                        pyxel.pset(x - 1, y, self.color)
                    if x < 511:
                        pyxel.pset(x + 1, y, self.color)
    
    def draw_circle(self):
        # Draw filled circle
        radius = int(self.width / 2)
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    x = int(self.x + dx)
                    y = int(self.y + dy)
                    if 0 <= x < 512 and 0 <= y < 512:
                        pyxel.pset(x, y, self.color)
    
    def draw_line(self):
        # Draw thick line
        length = self.width
        thickness = max(2, int(self.height / 8))
        
        end_x = self.x + length * math.cos(self.rotation)
        end_y = self.y + length * math.sin(self.rotation)
        
        # Draw thick line as series of circles
        steps = int(length)
        for i in range(steps):
            t = i / max(1, steps - 1)
            x = int(self.x + t * (end_x - self.x))
            y = int(self.y + t * (end_y - self.y))
            
            for r in range(thickness):
                for angle in range(0, 360, 30):
                    px = x + r * math.cos(math.radians(angle))
                    py = y + r * math.sin(math.radians(angle))
                    if 0 <= px < 512 and 0 <= py < 512:
                        pyxel.pset(int(px), int(py), self.color)
    
    def draw_cross(self):
        # Draw suprematist cross
        arm_length = self.width / 2
        thickness = max(3, int(self.height / 6))
        
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        
        # Horizontal arm
        for t in range(-int(arm_length), int(arm_length)):
            for thick in range(-thickness, thickness):
                x = self.x + t * cos_r - thick * sin_r
                y = self.y + t * sin_r + thick * cos_r
                if 0 <= x < 512 and 0 <= y < 512:
                    pyxel.pset(int(x), int(y), self.color)
        
        # Vertical arm
        for t in range(-int(arm_length), int(arm_length)):
            for thick in range(-thickness, thickness):
                x = self.x - t * sin_r - thick * cos_r
                y = self.y + t * cos_r - thick * sin_r
                if 0 <= x < 512 and 0 <= y < 512:
                    pyxel.pset(int(x), int(y), self.color)

class Supremus:
    def __init__(self):
        pyxel.init(512, 512, title="Supremus")
        
        # Sound design - footstep-like white noise rustle
        pyxel.sounds[0].set("c2", "n", "543", "f", 20)        # Soft footstep rustle
        pyxel.sounds[1].set("f2", "n", "432", "f", 18)        # Light step noise
        pyxel.sounds[2].set("g2", "n", "321", "f", 15)        # Gentle rustle
        pyxel.sounds[3].set("d2", "n", "654", "f", 25)        # Heavier step
        pyxel.sounds[4].set("a1", "n", "765", "f", 30)        # Deep footfall
        pyxel.sounds[5].set("e2", "n", "21", "f", 10)         # Subtle shuffle
        
        # Create suprematist shapes
        self.shapes = []
        
        # Malevich-inspired composition - distributed across canvas
        shape_types = ['rectangle', 'rectangle', 'rectangle', 'circle', 'line', 'cross']
        
        # Define regions across the canvas for better distribution
        regions = [
            (128, 128),   # Top-left quadrant
            (384, 128),   # Top-right quadrant
            (256, 256),   # Center
            (128, 384),   # Bottom-left quadrant
            (384, 384),   # Bottom-right quadrant
            (256, 160),   # Upper center
        ]
        
        for i, shape_type in enumerate(shape_types):
            # Use region as base but add variation
            base_x, base_y = regions[i % len(regions)]
            
            # Add significant variation from region center
            x = base_x + random.uniform(-80, 80)
            y = base_y + random.uniform(-80, 80)
            
            # Keep within canvas bounds
            x = max(60, min(452, x))
            y = max(60, min(452, y))
            
            shape = SuprematistShape(x, y, shape_type)
            self.shapes.append(shape)
        
        # Add more scattered elements throughout canvas
        for _ in range(4):
            x = random.uniform(80, 432)
            y = random.uniform(80, 432)
            shape_type = random.choice(['rectangle', 'circle', 'line'])
            shape = SuprematistShape(x, y, shape_type)
            shape.width *= random.uniform(0.6, 0.9)  # Vary sizes
            shape.height *= random.uniform(0.6, 0.9)
            self.shapes.append(shape)
        
        # Establish invisible connections between shapes
        self.establish_connections()
        
        self.time = 0
        self.composition_phase = 0
        
        pyxel.run(self.update, self.draw)
    
    def establish_connections(self):
        """Create invisible connections between shapes for spatial harmony"""
        for i, shape1 in enumerate(self.shapes):
            # Connect each shape to 1-3 nearby shapes
            distances = []
            for j, shape2 in enumerate(self.shapes):
                if i != j:
                    dx = shape1.x - shape2.x
                    dy = shape1.y - shape2.y
                    distance = math.sqrt(dx * dx + dy * dy)
                    distances.append((distance, shape2))
            
            # Sort by distance and connect to closest 1-2 shapes
            distances.sort()
            num_connections = random.randint(1, 2)
            
            for k in range(min(num_connections, len(distances))):
                connected_shape = distances[k][1]
                if connected_shape not in shape1.connected_to:
                    shape1.connected_to.append(connected_shape)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all shapes
        for shape in self.shapes:
            shape.update(self.time, self.shapes)
        
        # Update composition dynamics
        self.composition_phase += 0.005
        
        # Sound triggers - rhythmic footstep sequence
        # Main rhythmic pattern - every 60 frames (2 seconds)
        if self.time % 60 == 0:
            pyxel.play(0, 0, loop=False)  # Soft footstep rustle
        
        if self.time % 60 == 20:
            pyxel.play(1, 1, loop=False)  # Light step noise
        
        if self.time % 60 == 40:
            pyxel.play(2, 2, loop=False)  # Gentle rustle
        
        # Secondary rhythm - every 120 frames (4 seconds)
        if self.time % 120 == 60:
            pyxel.play(0, 3, loop=False)  # Heavier step
        
        # Accent pattern - every 240 frames (8 seconds)  
        if self.time % 240 == 0:
            pyxel.play(1, 4, loop=False)  # Deep footfall
        
        if self.time % 240 == 80:
            pyxel.play(2, 5, loop=False)  # Subtle shuffle
        
        if self.time % 240 == 160:
            pyxel.play(0, 1, loop=False)  # Light step accent
        
        
        self.time += 1
    
    def draw(self):
        # White canvas background
        pyxel.cls(7)  # White color
        
        # Optional: Add subtle texture to canvas
        if random.random() < 0.01:
            for _ in range(5):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                # Very subtle texture variation
                texture_color = random.choice([4, 9])  # Slight variation in flesh tone
                pyxel.pset(x, y, texture_color)
        
        # Draw all suprematist shapes
        for shape in self.shapes:
            shape.draw()
        
        # Optional: Draw very subtle connection lines (barely visible)
        if self.time % 600 < 300:  # Only show connections half the time
            for shape in self.shapes:
                for connected in shape.connected_to:
                    if random.random() < 0.1:  # Very rarely visible
                        # Draw faint line
                        x1, y1 = int(shape.x), int(shape.y)
                        x2, y2 = int(connected.x), int(connected.y)
                        
                        # Only draw a few pixels of the connection
                        mid_x = (x1 + x2) // 2
                        mid_y = (y1 + y2) // 2
                        
                        if 0 <= mid_x < 512 and 0 <= mid_y < 512:
                            pyxel.pset(mid_x, mid_y, 1)  # Very dark dot

Supremus()