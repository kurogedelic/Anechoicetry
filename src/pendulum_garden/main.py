"""
Pendulum Garden - Anechoicetry Collection
by Leo Kuroshita
Multiple pendulums creating mesmerizing interference patterns with realistic physics
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Pendulum:
    def __init__(self, x, y, length, initial_angle=None):
        self.anchor_x = x
        self.anchor_y = y
        self.length = length
        self.angle = initial_angle if initial_angle else random.uniform(-math.pi/3, math.pi/3)
        self.angular_velocity = 0
        self.damping = 0.999  # Air resistance
        self.gravity = 0.4
        self.trail = []
        self.max_trail_length = 60
        self.bob_size = 3
        self.color = random.choice([7, 6, 5, 13, 12])
        self.last_sound_time = 0
        
    def update(self, time, other_pendulums):
        # Simple pendulum physics
        angular_acceleration = -(self.gravity / self.length) * math.sin(self.angle)
        
        # Weak coupling with nearby pendulums
        coupling_force = 0
        for other in other_pendulums:
            if other != self:
                distance = math.sqrt((self.anchor_x - other.anchor_x)**2 + (self.anchor_y - other.anchor_y)**2)
                if distance < 100:  # Coupling range
                    angle_diff = other.angle - self.angle
                    coupling_strength = 0.001 * (1 - distance / 100)
                    coupling_force += coupling_strength * angle_diff
        
        angular_acceleration += coupling_force
        
        # Update motion
        self.angular_velocity += angular_acceleration
        self.angular_velocity *= self.damping  # Apply damping
        self.angle += self.angular_velocity
        
        # Calculate bob position
        bob_x = self.anchor_x + self.length * math.sin(self.angle)
        bob_y = self.anchor_y + self.length * math.cos(self.angle)
        
        # Add to trail
        self.trail.append((bob_x, bob_y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Check for resonance/alignment with other pendulums
        self.check_resonance(other_pendulums, time)
        
        return bob_x, bob_y
    
    def check_resonance(self, other_pendulums, time):
        # Check if pendulums are aligned (similar angles)
        if time - self.last_sound_time > 60:  # Cooldown
            for other in other_pendulums:
                if other != self:
                    angle_diff = abs(self.angle - other.angle)
                    if angle_diff < 0.1 or angle_diff > math.pi * 2 - 0.1:  # Nearly aligned
                        distance = math.sqrt((self.anchor_x - other.anchor_x)**2 + (self.anchor_y - other.anchor_y)**2)
                        if distance < 150 and random.random() < 0.3:
                            # Resonance sound
                            pyxel.play(1, random.choice([0, 1, 2]), loop=False)
                            self.last_sound_time = time
                            break
    
    def draw(self):
        # Draw trail
        for i, (x, y) in enumerate(self.trail):
            if i > 0:
                alpha = i / len(self.trail)
                if alpha > 0.3:
                    # Trail color gets dimmer with age
                    trail_color = max(1, int(self.color * alpha))
                    pyxel.pset(int(x), int(y), trail_color)
        
        # Draw string
        bob_x = self.anchor_x + self.length * math.sin(self.angle)
        bob_y = self.anchor_y + self.length * math.cos(self.angle)
        pyxel.line(int(self.anchor_x), int(self.anchor_y), int(bob_x), int(bob_y), 6)
        
        # Draw bob
        pyxel.circ(int(bob_x), int(bob_y), self.bob_size, self.color)
        
        # Draw anchor point
        pyxel.circ(int(self.anchor_x), int(self.anchor_y), 2, 1)

class HarmonicPattern:
    def __init__(self, pendulums):
        self.pendulums = pendulums
        self.pattern_timer = 0
        self.active_pattern = None
        self.pattern_duration = 0
        
    def update(self, time):
        self.pattern_timer += 1
        
        # Occasionally create harmonic patterns
        if self.pattern_timer >= 600 and random.random() < 0.2:
            self.create_harmonic_pattern()
            self.pattern_timer = 0
        
        # Update active pattern
        if self.active_pattern:
            self.pattern_duration -= 1
            if self.pattern_duration <= 0:
                self.active_pattern = None
    
    def create_harmonic_pattern(self):
        pattern_type = random.choice(['sync', 'wave', 'spiral'])
        
        if pattern_type == 'sync':
            # Synchronize some pendulums
            target_angle = random.uniform(-math.pi/4, math.pi/4)
            selected = random.sample(self.pendulums, min(4, len(self.pendulums)))
            for pendulum in selected:
                pendulum.angle = target_angle + random.uniform(-0.1, 0.1)
                pendulum.angular_velocity = random.uniform(-0.1, 0.1)
        
        elif pattern_type == 'wave':
            # Create wave pattern
            for i, pendulum in enumerate(self.pendulums):
                phase = (i / len(self.pendulums)) * math.pi * 2
                pendulum.angle = math.sin(phase) * math.pi / 6
                pendulum.angular_velocity = 0
        
        elif pattern_type == 'spiral':
            # Create spiral-like motion
            center_x = 256
            center_y = 200
            for i, pendulum in enumerate(self.pendulums):
                angle_to_center = math.atan2(pendulum.anchor_y - center_y, pendulum.anchor_x - center_x)
                pendulum.angle = angle_to_center * 0.3
                pendulum.angular_velocity = 0.05
        
        self.active_pattern = pattern_type
        self.pattern_duration = 180
        
        # Pattern creation sound
        pyxel.play(2, 3, loop=False)

class PendulumGarden:
    def __init__(self):
        pyxel.init(512, 512, title="Pendulum Garden")
        
        # Sound design - gentle, percussive, natural
        pyxel.sounds[0].set("c3e3g3", "t", "543", "f", 20)    # Wooden percussion
        pyxel.sounds[1].set("g3b3d4", "t", "432", "f", 18)    # Higher wood tone
        pyxel.sounds[2].set("f3a3c4", "t", "321", "f", 15)    # Wind chime
        pyxel.sounds[3].set("d3f3a3", "s", "654", "v", 25)    # Harmonic creation
        pyxel.sounds[4].set("a2c3e3", "t", "765", "f", 30)    # Deep resonance
        pyxel.sounds[5].set("e3g3", "t", "21", "f", 10)       # Gentle tick
        
        # Create pendulums in a centered, scaled arrangement
        self.pendulums = []
        
        # Main center pendulum
        center_x, center_y = 256, 80
        self.pendulums.append(Pendulum(center_x, center_y, 150))
        
        # Inner circle - closer to center
        for i in range(6):
            angle = (i / 6) * math.pi * 2
            radius = 80
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) * 0.3  # Flatten vertically
            length = random.uniform(120, 180)
            self.pendulums.append(Pendulum(x, y, length))
        
        # Outer circle - larger spread
        for i in range(8):
            angle = (i / 8) * math.pi * 2 + math.pi / 8  # Offset from inner circle
            radius = 140
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) * 0.4
            length = random.uniform(100, 160)
            self.pendulums.append(Pendulum(x, y, length))
        
        # Edge pendulums for full canvas coverage
        edge_positions = [
            (100, 60), (412, 60),    # Top corners
            (60, 120), (452, 120),   # Mid sides
            (180, 40), (332, 40)     # Top mid positions
        ]
        for x, y in edge_positions:
            length = random.uniform(80, 140)
            self.pendulums.append(Pendulum(x, y, length))
        
        # Harmonic pattern system
        self.harmonic_patterns = HarmonicPattern(self.pendulums)
        
        # Environment
        self.wind_timer = 0
        self.wind_strength = 0
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update wind
        self.wind_timer += 1
        if self.wind_timer >= 200:
            self.wind_strength = random.uniform(-0.02, 0.02)
            self.wind_timer = 0
        
        # Apply wind to pendulums
        for pendulum in self.pendulums:
            pendulum.angular_velocity += self.wind_strength * random.uniform(0.5, 1.5)
        
        # Update all pendulums
        for pendulum in self.pendulums:
            pendulum.update(self.time, self.pendulums)
        
        # Update harmonic patterns
        self.harmonic_patterns.update(self.time)
        
        # Environmental sounds
        if self.time % 150 == 0 and random.random() < 0.3:
            pyxel.play(0, 4, loop=False)  # Deep resonance
        
        if self.time % 90 == 45 and random.random() < 0.4:
            pyxel.play(1, 5, loop=False)  # Gentle tick
        
        # Wind sounds
        if abs(self.wind_strength) > 0.01 and self.time % 60 == 0 and random.random() < 0.5:
            pyxel.play(2, 2, loop=False)  # Wind chime
        
        self.time += 1
    
    def draw(self):
        # Soft background
        pyxel.cls(1)  # Dark blue/black
        
        # Draw subtle grid or garden elements
        if self.time % 300 < 150:  # Periodically show grid
            for x in range(0, 512, 64):
                pyxel.line(x, 0, x, 512, 1)
            for y in range(0, 512, 64):
                pyxel.line(0, y, 512, y, 1)
        
        # Draw all pendulums
        for pendulum in self.pendulums:
            pendulum.draw()
        
        # Draw harmonic connections when pattern is active
        if self.harmonic_patterns.active_pattern:
            # Draw connections between synchronized pendulums
            for i, p1 in enumerate(self.pendulums):
                for p2 in self.pendulums[i+1:]:
                    angle_diff = abs(p1.angle - p2.angle)
                    if angle_diff < 0.2:  # Similar angles
                        distance = math.sqrt((p1.anchor_x - p2.anchor_x)**2 + (p1.anchor_y - p2.anchor_y)**2)
                        if distance < 200:
                            # Draw faint connection line
                            pyxel.line(int(p1.anchor_x), int(p1.anchor_y), 
                                     int(p2.anchor_x), int(p2.anchor_y), 5)

PendulumGarden()