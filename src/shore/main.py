"""
Shore - Anechoicetry Collection
by Leo Kuroshita
Monochrome seashore with moon, stars, and gentle waves inspired by contemplative minimalism
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Shore:
    def __init__(self):
        pyxel.init(512, 512, title="Shore - Anechoicetry")
        
        # Initialize sound design
        self.init_sounds()
        
        # Visual elements
        self.horizon_y = 256  # Horizon line at center
        
        # Moon
        self.moon_x = 256
        self.moon_y = 128
        self.moon_radius = 24
        
        # Stars
        self.stars = []
        self.init_stars()
        self.star_timer = 0
        self.star_change_interval = 90  # Frames between star changes
        
        # Water reflection lines (moon reflection)
        self.reflection_lines = []
        self.init_reflection_lines()
        self.reflection_timer = 0
        self.reflection_change_interval = 30
        
        # Sea surface lines
        self.sea_lines = []
        self.init_sea_lines()
        self.sea_line_timer = 0
        self.sea_line_change_interval = 45
        
        # Individual wave segments
        self.wave_segments = []
        self.init_wave_segments()
        self.wave_timer = 0
        self.time = 0
        
        # Frame counter and wave sound system
        self.frame = 0
        self.wave_sound_phase = 0
        self.wave_sound_intensity = 0.5
        self.continuous_wave_playing = False
        
        pyxel.run(self.update, self.draw)
    
    def init_sounds(self):
        # Sound 0: High freq wave noise (brighter)
        pyxel.sounds[0].set(
            "c2d2e2f2g2f2e2d2c2b1a1g1", "n", "2222221111111122222211", "ffffssssssssssffffffffff", 90
        )
        
        # Sound 1: High freq wave wash noise
        pyxel.sounds[1].set(
            "a1b1c2d2e2f2g2a2g2f2e2d2", "n", "322222221111", "sssssffffff", 45
        )
        
        # Sound 2: Mid-high freq water noise
        pyxel.sounds[2].set(
            "f1g1a1b1c2d2e2f2e2d2c2b1", "n", "211111122221", "ffffffffffff", 60
        )
        
        # Sound 3: High freq ambient noise (hissing)
        pyxel.sounds[3].set(
            "c2d2e2f2g2a2b2c3", "n", "11111111", "ffffffff", 30
        )
        
        # Sound 4: High freq breeze noise
        pyxel.sounds[4].set(
            "c1d1e1f1g1a1b1c2d2e2", "n", "1111111111", "ffffffffff", 120
        )
    
    def init_stars(self):
        # Create stars in upper half of screen
        star_count = 80
        for _ in range(star_count):
            self.stars.append({
                'x': random.randint(0, 511),
                'y': random.randint(0, self.horizon_y - 50),
                'brightness': random.choice([6, 7]),  # Light gray, white only
                'blink_timer': random.randint(0, 120),
                'blink_speed': random.randint(120, 300)
            })
    
    def init_reflection_lines(self):
        # Moon reflection lines
        reflection_count = 25
        for _ in range(reflection_count):
            self.reflection_lines.append({
                'x': self.moon_x + random.randint(-15, 15),
                'y': self.horizon_y + random.randint(20, 100),
                'width': random.randint(8, 20),
                'visible': random.random() > 0.3
            })
    
    def init_sea_lines(self):
        # Random water surface lines
        sea_line_count = 60
        for _ in range(sea_line_count):
            self.sea_lines.append({
                'x': random.randint(0, 511),
                'y': self.horizon_y + random.randint(0, 256),
                'width': random.randint(5, 30),
                'visible': random.random() > 0.4
            })
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.frame += 1
        
        # Update wave segments
        self.time += 1
        
        # Update each wave segment's oscillation
        for segment in self.wave_segments:
            segment['phase'] += segment['speed']
            segment['life'] -= segment['decay_rate']  # Use individual decay rates
            
            # Regenerate segments that have faded
            if segment['life'] <= 0:
                self.regenerate_wave_segment(segment)
        
        # Maintain consistent wave count by adding segments more regularly
        self.wave_timer += 1
        if self.wave_timer > 30:  # Check more frequently
            # Count visible waves
            visible_waves = sum(1 for s in self.wave_segments if s['life'] > 0.2)
            if visible_waves < 100:  # Maintain minimum count
                self.add_wave_segment()
            self.wave_timer = 0
        
        # Update stars blinking
        self.star_timer += 1
        if self.star_timer >= self.star_change_interval:
            self.star_timer = 0
            for star in self.stars:
                if random.random() < 0.1:
                    star['x'] = random.randint(0, 511)
                    star['y'] = random.randint(0, self.horizon_y - 50)
                    star['brightness'] = random.choice([6, 7])  # Fix brightness on regeneration
        
        for star in self.stars:
            star['blink_timer'] += 1
            if star['blink_timer'] >= star['blink_speed']:
                star['blink_timer'] = 0
                star['blink_speed'] = random.randint(120, 300)
        
        # Update reflection lines
        self.reflection_timer += 1
        if self.reflection_timer >= self.reflection_change_interval:
            self.reflection_timer = 0
            for line in self.reflection_lines:
                if random.random() < 0.15:
                    line['x'] = self.moon_x + random.randint(-15, 15)
                    line['y'] = self.horizon_y + random.randint(20, 100)
                    line['width'] = random.randint(8, 20)
                    line['visible'] = random.random() > 0.3
        
        # Update sea lines
        self.sea_line_timer += 1
        if self.sea_line_timer >= self.sea_line_change_interval:
            self.sea_line_timer = 0
            for line in self.sea_lines:
                if random.random() < 0.08:
                    line['x'] = random.randint(0, 511)
                    line['y'] = self.horizon_y + random.randint(0, 256)
                    line['width'] = random.randint(5, 30)
                    line['visible'] = random.random() > 0.4
        
        # Dynamic wave sound system
        self.update_wave_sounds()
        
        # Very gentle accent sounds
        if random.random() < 0.003:
            pyxel.play(2, 1)  # Soft wave
        if random.random() < 0.002:
            pyxel.play(3, 4)  # Gentle breeze
    
    def draw(self):
        # Clear to black (night sky)
        pyxel.cls(0)
        
        # Draw subtle night sky texture (removed to fix glitch)
        # Keep sky pure black for clean aesthetic
        
        # Draw horizon line
        pyxel.line(0, self.horizon_y, 511, self.horizon_y, 7)
        
        # Draw stars
        for star in self.stars:
            if star['blink_timer'] < star['blink_speed'] * 0.8:
                pyxel.pset(star['x'], star['y'], star['brightness'])
        
        # Draw moon
        pyxel.circb(self.moon_x, self.moon_y, self.moon_radius, 7)
        pyxel.circ(self.moon_x, self.moon_y, self.moon_radius - 1, 7)
        
        # Draw moon's crescent shadow
        shadow_offset_x = 8
        shadow_offset_y = -3
        pyxel.circ(self.moon_x + shadow_offset_x, self.moon_y + shadow_offset_y, self.moon_radius - 3, 0)
        
        # Fill water area with dark color
        pyxel.rect(0, self.horizon_y + 1, 512, 256, 1)
        
        # Draw moon reflection lines
        for line in self.reflection_lines:
            if line['visible']:
                start_x = line['x'] - line['width'] // 2
                end_x = line['x'] + line['width'] // 2
                pyxel.line(start_x, line['y'], end_x, line['y'], 7)
        
        # Draw sea surface lines
        for line in self.sea_lines:
            if line['visible']:
                start_x = line['x'] - line['width'] // 2
                end_x = line['x'] + line['width'] // 2
                pyxel.line(start_x, line['y'], end_x, line['y'], 6)
        
        # Draw individual oscillating wave segments
        for segment in self.wave_segments:
            if segment['life'] > 0:
                # Calculate oscillation based on phase and time
                oscillation = math.sin(segment['phase'] + self.time * 0.02) * segment['amplitude']
                
                # Current position with oscillation
                current_x = segment['base_x'] + oscillation
                current_y = segment['y']
                
                # Draw the wave segment
                start_x = int(current_x - segment['width'] / 2)
                end_x = int(current_x + segment['width'] / 2)
                
                # Ensure bounds and valid line
                start_x = max(0, start_x)
                end_x = min(511, end_x)
                
                # Only draw if line is valid
                if start_x < end_x and 0 <= current_y < 512:
                    # Color based on distance (depth)
                    if segment['y'] < self.horizon_y + 50:
                        color = 7  # White for close waves
                    elif segment['y'] < self.horizon_y + 120:
                        color = 6  # Light gray for mid-distance
                    else:
                        color = 5  # Dark gray for distant waves
                    
                    # Apply life-based alpha (fade effect) - simplified
                    if segment['life'] > 0.3:  # Remove random flicker
                        pyxel.line(start_x, current_y, end_x, current_y, color)

    def init_wave_segments(self):
        # Create initial wave segments
        segment_count = 120
        for _ in range(segment_count):
            self.add_wave_segment()
    
    def add_wave_segment(self):
        # Calculate distance-based properties
        y = self.horizon_y + random.randint(10, 240)
        distance_factor = (y - self.horizon_y) / 240  # 0 to 1, closer to farther
        
        # Width decreases with distance (perspective)
        max_width = 60 - int(distance_factor * 40)  # 60px close, 20px far
        width = random.randint(max_width // 2, max_width)
        
        # Amplitude decreases with distance
        max_amplitude = 8 - int(distance_factor * 5)  # 8px close, 3px far
        amplitude = random.uniform(1, max_amplitude)
        
        segment = {
            'base_x': random.randint(width, 512 - width),
            'y': y,
            'width': width,
            'amplitude': amplitude,
            'phase': random.uniform(0, 2 * math.pi),
            'speed': random.uniform(0.02, 0.08),
            'life': random.uniform(0.4, 1.0),  # Stagger initial life
            'decay_rate': random.uniform(0.001, 0.003)  # Vary decay rates
        }
        
        self.wave_segments.append(segment)
    
    def regenerate_wave_segment(self, segment):
        # Regenerate a faded segment with new properties
        y = self.horizon_y + random.randint(10, 240)
        distance_factor = (y - self.horizon_y) / 240
        
        max_width = 60 - int(distance_factor * 40)
        width = random.randint(max_width // 2, max_width)
        
        max_amplitude = 8 - int(distance_factor * 5)
        amplitude = random.uniform(1, max_amplitude)
        
        segment['base_x'] = random.randint(width, 512 - width)
        segment['y'] = y
        segment['width'] = width
        segment['amplitude'] = amplitude
        segment['phase'] = random.uniform(0, 2 * math.pi)
        segment['speed'] = random.uniform(0.02, 0.08)
        segment['life'] = random.uniform(0.4, 1.0)  # Stagger regenerated life
        segment['decay_rate'] = random.uniform(0.001, 0.003)  # New decay rate

    def update_wave_sounds(self):
        # Update wave sound phase for gentle periodic changes
        self.wave_sound_phase += 0.008  # Slower, more gentle rhythm
        
        # Calculate wave intensity using gentle sine waves
        primary_wave = math.sin(self.wave_sound_phase) * 0.3
        secondary_wave = math.sin(self.wave_sound_phase * 0.6 + 1.8) * 0.15
        
        # Combine waves and keep in gentle range
        self.wave_sound_intensity = 0.2 + (primary_wave + secondary_wave)
        self.wave_sound_intensity = max(0.1, min(0.6, self.wave_sound_intensity))
        
        # Play gentle wave sounds based on intensity
        if self.wave_sound_intensity > 0.45:
            # Higher intensity - gentle wave sound
            if random.random() < 0.1:  # Less frequent
                pyxel.play(0, 0)
        elif self.wave_sound_intensity > 0.35:
            # Medium intensity - soft wash
            if random.random() < 0.08:
                pyxel.play(1, 1)
        elif self.wave_sound_intensity > 0.25:
            # Low intensity - distant water
            if random.random() < 0.05:
                pyxel.play(2, 2)
        
        # Very subtle ambient noise occasionally
        if random.random() < 0.02:
            pyxel.play(3, 3)
        
        # Gentle breeze occasionally
        if random.random() < 0.008:
            pyxel.play(1, 4)

if __name__ == "__main__":
    Shore()