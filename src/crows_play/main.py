"""
Crows Play - Anechoicetry Collection
by Leo Kuroshita
A flock of black crows following boids algorithm with staccato chord progressions
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Crow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.max_speed = 2.0
        self.max_force = 0.03
        self.perception_radius = 25
        self.wing_phase = random.uniform(0, math.pi * 2)
        self.wing_speed = random.uniform(0.2, 0.4)
        self.size = random.uniform(0.8, 1.2)
        
    def update(self, flock):
        # Apply boids behaviors
        sep = self.separate(flock)
        ali = self.align(flock)
        coh = self.cohesion(flock)
        
        # Weight the behaviors
        sep = self.multiply_vector(sep, 1.5)
        ali = self.multiply_vector(ali, 1.0)
        coh = self.multiply_vector(coh, 1.0)
        
        # Apply forces
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)
        
        # Boundary avoidance
        boundary_force = self.avoid_boundaries()
        self.apply_force(self.multiply_vector(boundary_force, 2.0))
        
        # Update position
        self.vx += random.uniform(-0.01, 0.01)  # Small random drift
        self.vy += random.uniform(-0.01, 0.01)
        
        # Limit speed
        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed
        
        self.x += self.vx
        self.y += self.vy
        
        # Update wing animation
        self.wing_phase += self.wing_speed
        
    def apply_force(self, force):
        self.vx += force[0]
        self.vy += force[1]
    
    def separate(self, flock):
        desired_separation = 25
        steer_x, steer_y = 0, 0
        count = 0
        
        for other in flock:
            if other != self:
                d = self.distance_to(other)
                if 0 < d < desired_separation:
                    # Calculate vector pointing away from neighbor
                    diff_x = self.x - other.x
                    diff_y = self.y - other.y
                    # Weight by distance
                    diff_x /= d
                    diff_y /= d
                    steer_x += diff_x
                    steer_y += diff_y
                    count += 1
        
        if count > 0:
            steer_x /= count
            steer_y /= count
            # Normalize and scale
            mag = math.sqrt(steer_x * steer_x + steer_y * steer_y)
            if mag > 0:
                steer_x = (steer_x / mag) * self.max_speed
                steer_y = (steer_y / mag) * self.max_speed
                steer_x -= self.vx
                steer_y -= self.vy
                # Limit force
                return self.limit_vector([steer_x, steer_y], self.max_force)
        
        return [0, 0]
    
    def align(self, flock):
        neighbor_dist = 50
        sum_x, sum_y = 0, 0
        count = 0
        
        for other in flock:
            if other != self:
                d = self.distance_to(other)
                if 0 < d < neighbor_dist:
                    sum_x += other.vx
                    sum_y += other.vy
                    count += 1
        
        if count > 0:
            sum_x /= count
            sum_y /= count
            # Normalize and scale
            mag = math.sqrt(sum_x * sum_x + sum_y * sum_y)
            if mag > 0:
                sum_x = (sum_x / mag) * self.max_speed
                sum_y = (sum_y / mag) * self.max_speed
                steer_x = sum_x - self.vx
                steer_y = sum_y - self.vy
                return self.limit_vector([steer_x, steer_y], self.max_force)
        
        return [0, 0]
    
    def cohesion(self, flock):
        neighbor_dist = 50
        sum_x, sum_y = 0, 0
        count = 0
        
        for other in flock:
            if other != self:
                d = self.distance_to(other)
                if 0 < d < neighbor_dist:
                    sum_x += other.x
                    sum_y += other.y
                    count += 1
        
        if count > 0:
            sum_x /= count
            sum_y /= count
            return self.seek(sum_x, sum_y)
        
        return [0, 0]
    
    def seek(self, target_x, target_y):
        desired_x = target_x - self.x
        desired_y = target_y - self.y
        
        # Normalize and scale to max speed
        mag = math.sqrt(desired_x * desired_x + desired_y * desired_y)
        if mag > 0:
            desired_x = (desired_x / mag) * self.max_speed
            desired_y = (desired_y / mag) * self.max_speed
        
        # Steering = Desired - Velocity
        steer_x = desired_x - self.vx
        steer_y = desired_y - self.vy
        
        return self.limit_vector([steer_x, steer_y], self.max_force)
    
    def avoid_boundaries(self):
        margin = 50
        steer_x, steer_y = 0, 0
        
        if self.x < margin:
            steer_x = self.max_speed
        elif self.x > 512 - margin:
            steer_x = -self.max_speed
            
        if self.y < margin:
            steer_y = self.max_speed
        elif self.y > 512 - margin:
            steer_y = -self.max_speed
            
        return self.limit_vector([steer_x, steer_y], self.max_force)
    
    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def multiply_vector(self, vec, scalar):
        return [vec[0] * scalar, vec[1] * scalar]
    
    def limit_vector(self, vec, max_mag):
        mag = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
        if mag > max_mag:
            return [(vec[0] / mag) * max_mag, (vec[1] / mag) * max_mag]
        return vec
    
    def draw(self):
        # Calculate crow orientation based on velocity
        angle = math.atan2(self.vy, self.vx)
        
        # Wing flapping animation
        wing_offset = math.sin(self.wing_phase) * 3 * self.size
        
        # Crow body (simple triangle pointing in direction of movement)
        body_length = 8 * self.size
        body_width = 4 * self.size
        
        # Body points
        nose_x = self.x + math.cos(angle) * body_length
        nose_y = self.y + math.sin(angle) * body_length
        
        left_wing_x = self.x + math.cos(angle + 2.5) * body_width + math.cos(angle + 1.57) * wing_offset
        left_wing_y = self.y + math.sin(angle + 2.5) * body_width + math.sin(angle + 1.57) * wing_offset
        
        right_wing_x = self.x + math.cos(angle - 2.5) * body_width + math.cos(angle - 1.57) * wing_offset
        right_wing_y = self.y + math.sin(angle - 2.5) * body_width + math.sin(angle - 1.57) * wing_offset
        
        # Draw crow as triangle
        self.draw_triangle(
            int(nose_x), int(nose_y),
            int(left_wing_x), int(left_wing_y),
            int(right_wing_x), int(right_wing_y),
            0  # Black
        )
        
    
    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color):
        # Draw filled triangle
        if (0 <= x1 < 512 and 0 <= y1 < 512 and 
            0 <= x2 < 512 and 0 <= y2 < 512 and 
            0 <= x3 < 512 and 0 <= y3 < 512):
            pyxel.tri(x1, y1, x2, y2, x3, y3, color)

class CrowsPlay:
    def __init__(self):
        pyxel.init(512, 512, title="Crows Play")
        
        # Musical chord progression - I-V-vi-IV in C major
        # Staccato 3-note chords
        pyxel.sounds[0].set("c3e3g3", "t", "321", "f", 15)  # C major (I)
        pyxel.sounds[1].set("g2b2d3", "t", "321", "f", 15)  # G major (V)
        pyxel.sounds[2].set("a2c3e3", "t", "321", "f", 15)  # A minor (vi)
        pyxel.sounds[3].set("f2a2c3", "t", "321", "f", 15)  # F major (IV)
        pyxel.sounds[4].set("e3g3c4", "t", "432", "f", 12)  # Variation chord
        pyxel.sounds[5].set("d3f3a3", "t", "321", "f", 12)  # Transition chord
        
        # Initialize flock
        self.flock = []
        self.flock_size = 25
        
        for _ in range(self.flock_size):
            x = random.randint(100, 412)
            y = random.randint(100, 412)
            self.flock.append(Crow(x, y))
        
        # Musical timing
        self.chord_timer = 0
        self.chord_interval = 90  # Staccato timing
        self.current_chord = 0
        self.chord_progression = [0, 1, 2, 3]  # I-V-vi-IV
        
        # Flock behavior tracking
        self.prev_center_x = 256
        self.prev_center_y = 256
        self.formation_changes = 0
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all crows
        for crow in self.flock:
            crow.update(self.flock)
        
        # Track flock formation changes for musical triggers
        center_x, center_y = self.get_flock_center()
        movement = math.sqrt((center_x - self.prev_center_x)**2 + (center_y - self.prev_center_y)**2)
        
        if movement > 10:  # Significant formation change
            self.formation_changes += 1
        
        self.prev_center_x = center_x
        self.prev_center_y = center_y
        
        # Musical timing - staccato chord progression
        self.chord_timer += 1
        if self.chord_timer >= self.chord_interval:
            self.play_next_chord()
            self.chord_timer = 0
            
            # Vary timing slightly for organic feel
            self.chord_interval = random.randint(75, 105)
        
        # Occasional formation change triggered sounds
        if self.formation_changes > 0 and random.random() < 0.3:
            # Play variation or transition chord
            variation_chord = random.choice([4, 5])
            pyxel.play(1, variation_chord, loop=False)
            self.formation_changes = 0
        
        self.time += 1
    
    def get_flock_center(self):
        if not self.flock:
            return 256, 256
        
        sum_x = sum(crow.x for crow in self.flock)
        sum_y = sum(crow.y for crow in self.flock)
        return sum_x / len(self.flock), sum_y / len(self.flock)
    
    def play_next_chord(self):
        chord_id = self.chord_progression[self.current_chord]
        pyxel.play(0, chord_id, loop=False)
        
        # Advance to next chord in progression
        self.current_chord = (self.current_chord + 1) % len(self.chord_progression)
        
        # Occasionally play a complementary chord on channel 1
        if random.random() < 0.4:
            complement = (chord_id + 2) % 4  # Musical fourth/fifth
            pyxel.play(1, complement, loop=False)
    
    def draw(self):
        # White background
        pyxel.cls(7)
        
        # Draw all crows
        for crow in self.flock:
            crow.draw()
        
        # Optional: Draw flock center as small dot (for debugging)
        # center_x, center_y = self.get_flock_center()
        # pyxel.circb(int(center_x), int(center_y), 3, 5)

CrowsPlay()