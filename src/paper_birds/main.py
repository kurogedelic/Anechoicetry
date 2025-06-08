"""
Paper Birds - Anechoicetry Collection
by Leo Kuroshita
Origami-style geometric birds unfolding and refolding in impossible transformations
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class PaperBird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.current_form = 'crane'
        self.target_form = 'crane'
        self.forms = ['crane', 'swan', 'eagle', 'abstract', 'dove']
        self.transformation_progress = 0
        self.transformation_speed = 0.02
        self.size = random.uniform(0.8, 1.2)
        self.rotation = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-0.01, 0.01)
        self.fold_animation = 0
        self.fold_speed = random.uniform(0.05, 0.1)
        self.color = random.choice([0, 5, 6, 7])  # Black, gray, light gray, white
        self.drift_phase = random.uniform(0, math.pi * 2)
        self.drift_radius = random.uniform(20, 40)
        self.last_transform_time = 0
        
    def update(self, time):
        # Gentle floating motion
        self.drift_phase += 0.02
        self.x = self.base_x + math.sin(self.drift_phase) * self.drift_radius * 0.5
        self.y = self.base_y + math.cos(self.drift_phase * 0.7) * self.drift_radius * 0.3
        
        # Rotation
        self.rotation += self.rotation_speed
        
        # Fold animation
        self.fold_animation += self.fold_speed
        
        # Handle transformation
        if self.current_form != self.target_form:
            self.transformation_progress += self.transformation_speed
            if self.transformation_progress >= 1.0:
                self.current_form = self.target_form
                self.transformation_progress = 0
        
        # Occasionally start new transformation
        if time - self.last_transform_time > 300 and random.random() < 0.02:
            self.start_transformation()
            self.last_transform_time = time
    
    def start_transformation(self):
        # Choose new form
        available_forms = [f for f in self.forms if f != self.current_form]
        self.target_form = random.choice(available_forms)
        self.transformation_progress = 0
        
        # Transformation sound
        pyxel.play(random.randint(0, 2), random.choice([0, 1, 2]), loop=False)
    
    def get_form_vertices(self, form, progress=1.0):
        """Get vertices for different origami forms"""
        base_size = 30 * self.size
        
        if form == 'crane':
            return [
                (-base_size, 0),           # Body center
                (-base_size * 1.5, -base_size * 0.8),  # Wing tip 1
                (-base_size * 0.5, -base_size * 0.4),  # Wing joint 1
                (base_size * 0.3, -base_size * 0.2),   # Head
                (base_size * 0.8, 0),      # Beak
                (base_size * 0.3, base_size * 0.2),    # Head bottom
                (-base_size * 0.5, base_size * 0.4),   # Wing joint 2
                (-base_size * 1.5, base_size * 0.8),   # Wing tip 2
                (-base_size * 1.2, 0),     # Tail
            ]
        
        elif form == 'swan':
            return [
                (-base_size * 0.8, 0),     # Body
                (-base_size * 1.3, -base_size * 0.6),  # Wing 1
                (0, -base_size * 0.3),     # Neck curve
                (base_size * 0.8, -base_size * 0.8),   # Head up
                (base_size * 1.0, -base_size * 0.6),   # Beak
                (base_size * 0.8, -base_size * 0.4),   # Head down
                (0, base_size * 0.3),      # Neck bottom
                (-base_size * 1.3, base_size * 0.6),   # Wing 2
                (-base_size * 1.0, 0),     # Tail
            ]
        
        elif form == 'eagle':
            return [
                (0, 0),                    # Body center
                (-base_size * 1.8, -base_size * 0.4),  # Wing span 1
                (-base_size * 1.2, -base_size * 0.8),  # Wing tip 1
                (-base_size * 0.3, -base_size * 0.2),  # Wing root 1
                (base_size * 0.5, -base_size * 0.1),   # Head
                (base_size * 0.8, 0),      # Beak
                (base_size * 0.5, base_size * 0.1),    # Head bottom
                (-base_size * 0.3, base_size * 0.2),   # Wing root 2
                (-base_size * 1.2, base_size * 0.8),   # Wing tip 2
                (-base_size * 1.8, base_size * 0.4),   # Wing span 2
                (-base_size * 0.8, 0),     # Tail
            ]
        
        elif form == 'dove':
            return [
                (-base_size * 0.5, 0),     # Body
                (-base_size * 1.0, -base_size * 0.5),  # Wing 1
                (-base_size * 0.2, -base_size * 0.3),  # Wing joint 1
                (base_size * 0.4, -base_size * 0.1),   # Head
                (base_size * 0.6, 0),      # Beak
                (base_size * 0.4, base_size * 0.1),    # Head bottom
                (-base_size * 0.2, base_size * 0.3),   # Wing joint 2
                (-base_size * 1.0, base_size * 0.5),   # Wing 2
                (-base_size * 0.8, 0),     # Tail
            ]
        
        elif form == 'abstract':
            # Geometric abstract pattern
            angles = [i * math.pi * 2 / 8 for i in range(8)]
            radii = [base_size * (0.5 + 0.5 * math.sin(i * 1.3)) for i in range(8)]
            return [(r * math.cos(a), r * math.sin(a)) for a, r in zip(angles, radii)]
        
        return [(0, 0)]  # Fallback
    
    def interpolate_vertices(self, vertices1, vertices2, t):
        """Interpolate between two sets of vertices"""
        # Ensure both vertex lists have the same length
        max_len = max(len(vertices1), len(vertices2))
        
        # Pad shorter list
        v1 = vertices1 + [(0, 0)] * (max_len - len(vertices1))
        v2 = vertices2 + [(0, 0)] * (max_len - len(vertices2))
        
        # Interpolate
        result = []
        for (x1, y1), (x2, y2) in zip(v1, v2):
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            result.append((x, y))
        
        return result
    
    def transform_vertex(self, x, y):
        """Apply rotation and folding animation"""
        # Apply folding effect
        fold_factor = 1.0 + 0.1 * math.sin(self.fold_animation)
        x *= fold_factor
        y *= fold_factor
        
        # Apply rotation
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        
        new_x = x * cos_r - y * sin_r
        new_y = x * sin_r + y * cos_r
        
        return new_x + self.x, new_y + self.y
    
    def draw(self):
        # Get current and target vertices
        current_vertices = self.get_form_vertices(self.current_form)
        
        if self.current_form != self.target_form:
            # Interpolate during transformation
            target_vertices = self.get_form_vertices(self.target_form)
            vertices = self.interpolate_vertices(current_vertices, target_vertices, self.transformation_progress)
        else:
            vertices = current_vertices
        
        # Transform and draw vertices
        screen_vertices = []
        for x, y in vertices:
            sx, sy = self.transform_vertex(x, y)
            screen_vertices.append((int(sx), int(sy)))
        
        # Draw origami lines
        if len(screen_vertices) > 2:
            for i in range(len(screen_vertices)):
                x1, y1 = screen_vertices[i]
                x2, y2 = screen_vertices[(i + 1) % len(screen_vertices)]
                
                # Only draw if on screen
                if (0 <= x1 < 512 and 0 <= y1 < 512 and 
                    0 <= x2 < 512 and 0 <= y2 < 512):
                    pyxel.line(x1, y1, x2, y2, self.color)
        
        # Draw fold lines (internal geometric details)
        if len(screen_vertices) > 4:
            # Connect some internal vertices to create origami fold lines
            center_x, center_y = int(self.x), int(self.y)
            for i in range(0, len(screen_vertices), 2):
                x, y = screen_vertices[i]
                if 0 <= center_x < 512 and 0 <= center_y < 512 and 0 <= x < 512 and 0 <= y < 512:
                    pyxel.line(center_x, center_y, x, y, max(1, self.color - 1))

class GeometricPattern:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.max_size = random.uniform(40, 80)
        self.growth_speed = random.uniform(0.5, 1.0)
        self.rotation = 0
        self.rotation_speed = random.uniform(0.02, 0.05)
        self.life = 180
        self.color = random.choice([5, 6, 13])
        
    def update(self):
        if self.size < self.max_size:
            self.size += self.growth_speed
        
        self.rotation += self.rotation_speed
        self.life -= 1
        
        return self.life > 0
    
    def draw(self):
        if self.life <= 0:
            return
            
        # Draw geometric pattern
        sides = 6
        for i in range(sides):
            angle1 = (i / sides) * math.pi * 2 + self.rotation
            angle2 = ((i + 1) / sides) * math.pi * 2 + self.rotation
            
            x1 = int(self.x + self.size * math.cos(angle1))
            y1 = int(self.y + self.size * math.sin(angle1))
            x2 = int(self.x + self.size * math.cos(angle2))
            y2 = int(self.y + self.size * math.sin(angle2))
            
            if (0 <= x1 < 512 and 0 <= y1 < 512 and 
                0 <= x2 < 512 and 0 <= y2 < 512):
                pyxel.line(x1, y1, x2, y2, self.color)

class PaperBirds:
    def __init__(self):
        pyxel.init(512, 512, title="Paper Birds")
        
        # Sound design - paper, folding, gentle
        pyxel.sounds[0].set("c3e3g3", "t", "321", "f", 12)    # Paper rustling
        pyxel.sounds[1].set("f3a3", "s", "43", "v", 10)      # Gentle fold
        pyxel.sounds[2].set("g3b3d4", "t", "432", "f", 15)    # Transformation
        pyxel.sounds[3].set("d3f3", "p", "21", "f", 8)       # Soft crease
        pyxel.sounds[4].set("a2c3", "t", "54", "f", 18)      # Deep paper
        pyxel.sounds[5].set("e3", "s", "3", "v", 6)          # Quick fold
        
        # Create birds
        self.birds = []
        for _ in range(8):
            x = random.uniform(100, 412)
            y = random.uniform(100, 412)
            self.birds.append(PaperBird(x, y))
        
        # Geometric patterns that appear during transformations
        self.patterns = []
        
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update birds
        for bird in self.birds:
            bird.update(self.time)
        
        # Update patterns
        self.patterns = [p for p in self.patterns if p.update()]
        
        # Occasionally spawn geometric patterns
        if random.random() < 0.01:
            x = random.uniform(100, 412)
            y = random.uniform(100, 412)
            self.patterns.append(GeometricPattern(x, y))
        
        # Ambient sounds
        if self.time % 180 == 0 and random.random() < 0.4:
            pyxel.play(0, 3, loop=False)  # Soft crease
        
        if self.time % 240 == 60 and random.random() < 0.3:
            pyxel.play(1, 4, loop=False)  # Deep paper
        
        if self.time % 150 == 75 and random.random() < 0.25:
            pyxel.play(2, 5, loop=False)  # Quick fold
        
        self.time += 1
    
    def draw(self):
        # Clean white background
        pyxel.cls(7)
        
        # Draw geometric patterns
        for pattern in self.patterns:
            pattern.draw()
        
        # Draw birds
        for bird in self.birds:
            bird.draw()

PaperBirds()