"""
Aurora Spiral - Anechoicetry Collection
by Leo Kuroshita
Flowing curtains of light with drone harmonics and atmospheric resonance
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 2.0.0
"""

import pyxel
import math
import random

class AuroraCurtain:
    def __init__(self, x_start, color_scheme):
        self.x_start = x_start
        self.color_scheme = color_scheme  # 'green', 'blue', 'purple', 'yellow'
        
        # Curtain properties
        self.width = random.uniform(80, 150)
        self.height_base = 512
        self.wave_frequency = random.uniform(0.01, 0.03)
        self.wave_amplitude = random.uniform(30, 60)
        self.wave_phase = random.uniform(0, math.pi * 2)
        
        # Movement properties
        self.drift_speed = random.uniform(0.3, 0.8)
        self.drift_direction = random.uniform(-0.5, 0.5)
        self.flow_speed = random.uniform(0.5, 1.2)
        
        # Intensity and animation
        self.intensity_phase = random.uniform(0, math.pi * 2)
        self.intensity_speed = random.uniform(0.008, 0.02)
        self.flicker_phase = random.uniform(0, math.pi * 2)
        
        # Color mapping
        if color_scheme == 'green':
            self.colors = [3, 11, 10]  # Dark green, light green, yellow-green
        elif color_scheme == 'blue':
            self.colors = [1, 12, 6]   # Dark blue, blue, light blue
        elif color_scheme == 'purple':
            self.colors = [2, 13, 14]  # Purple, lavender, pink
        elif color_scheme == 'yellow':
            self.colors = [9, 10, 4]   # Orange, yellow, tan
        
    def update(self, time):
        # Update wave motion
        self.wave_phase += self.wave_frequency
        
        # Update intensity
        self.intensity_phase += self.intensity_speed
        
        # Flicker animation
        self.flicker_phase += 0.05
        
        # Drift movement
        self.x_start += self.drift_direction * self.drift_speed
        
        # Wrap around screen
        if self.x_start < -self.width:
            self.x_start = 512 + self.width
        elif self.x_start > 512 + self.width:
            self.x_start = -self.width
    
    def draw(self, time):
        # Calculate current intensity
        intensity = 0.7 + 0.3 * math.sin(self.intensity_phase)
        flicker = 0.9 + 0.1 * math.sin(self.flicker_phase * 3)
        
        # Draw curtain as flowing vertical bands
        num_bands = int(self.width // 8)
        
        for band in range(num_bands):
            band_x = self.x_start + band * 8
            
            if -20 <= band_x <= 532:  # Only draw if on screen
                # Calculate wave offset for this band
                wave_offset = self.wave_amplitude * math.sin(self.wave_phase + band * 0.3)
                
                # Draw flowing curtain from top to bottom
                for y in range(0, 512, 4):
                    # Height-based intensity variation
                    height_factor = 1.0 - (y / 512) * 0.3
                    
                    # Flow animation
                    flow_offset = 20 * math.sin(time * 0.01 + band * 0.5 + y * 0.02)
                    
                    # Final position
                    draw_x = int(band_x + wave_offset + flow_offset)
                    draw_y = y
                    
                    if 0 <= draw_x < 512 and 0 <= draw_y < 512:
                        # Color selection based on intensity and height
                        color_intensity = intensity * height_factor * flicker
                        
                        if color_intensity > 0.8:
                            color = self.colors[2]  # Brightest
                        elif color_intensity > 0.5:
                            color = self.colors[1]  # Medium
                        else:
                            color = self.colors[0]  # Darkest
                        
                        # Draw with slight thickness for curtain effect
                        pyxel.pset(draw_x, draw_y, color)
                        if draw_x + 1 < 512:
                            pyxel.pset(draw_x + 1, draw_y, color)
                        if draw_x + 2 < 512 and color_intensity > 0.6:
                            pyxel.pset(draw_x + 2, draw_y, color)

class DroneGenerator:
    def __init__(self):
        self.base_frequency = random.uniform(0.005, 0.02)
        self.harmonic_phases = [random.uniform(0, math.pi * 2) for _ in range(4)]
        self.harmonic_speeds = [random.uniform(0.008, 0.025) for _ in range(4)]
        self.intensity = 0.0
        
    def update(self, aurora_intensity):
        # Update harmonic phases
        for i in range(len(self.harmonic_phases)):
            self.harmonic_phases[i] += self.harmonic_speeds[i]
        
        # Intensity follows aurora activity
        self.intensity = aurora_intensity * 0.7 + 0.3
        
    def get_drone_value(self, time):
        """Generate drone harmony value"""
        drone = 0
        for i, phase in enumerate(self.harmonic_phases):
            harmonic_freq = self.base_frequency * (i + 1) * 0.5
            drone += math.sin(time * harmonic_freq + phase) * (1.0 / (i + 1))
        
        return drone * self.intensity * 0.3

class AuroraBorealis:
    def __init__(self):
        pyxel.init(512, 512, title="Aurora Spiral")
        
        # Sound design - simple high-pitched sequence
        pyxel.sounds[0].set("c4", "t", "2", "n", 20)            # High C
        pyxel.sounds[1].set("e4", "t", "2", "n", 20)            # High E
        pyxel.sounds[2].set("g4", "t", "2", "n", 20)            # High G
        pyxel.sounds[3].set("f4", "t", "2", "n", 20)            # High F
        
        # Create aurora curtains
        self.curtains = []
        color_schemes = ['green', 'blue', 'purple', 'yellow']
        
        # Main green curtains (most prominent)
        for _ in range(4):
            x = random.uniform(0, 512)
            self.curtains.append(AuroraCurtain(x, 'green'))
        
        # Secondary color curtains
        for _ in range(3):
            x = random.uniform(0, 512)
            color = random.choice(['blue', 'purple'])
            self.curtains.append(AuroraCurtain(x, color))
        
        # Rare yellow curtains
        for _ in range(1):
            x = random.uniform(0, 512)
            self.curtains.append(AuroraCurtain(x, 'yellow'))
        
        # Drone system
        self.drone_generator = DroneGenerator()
        
        # System state
        self.time = 0
        self.magnetic_activity = 0
        self.aurora_intensity = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update magnetic activity (affects aurora intensity)
        self.magnetic_activity = (math.sin(self.time * 0.003) + 1) / 2
        self.aurora_intensity = 0.6 + 0.4 * self.magnetic_activity
        
        # Update all curtains
        for curtain in self.curtains:
            curtain.update(self.time)
        
        # Update drone generator
        self.drone_generator.update(self.aurora_intensity)
        
        # Sound triggers - pure drone noise
        # Simple high-pitched sequence - C E G F pattern
        sequence_step = (self.time // 60) % 4  # Change every 2 seconds
        
        if self.time % 60 == 0:  # Play every 2 seconds
            if sequence_step == 0:
                pyxel.play(0, 0, loop=False)  # C4
            elif sequence_step == 1:
                pyxel.play(1, 1, loop=False)  # E4
            elif sequence_step == 2:
                pyxel.play(2, 2, loop=False)  # G4
            elif sequence_step == 3:
                pyxel.play(3, 3, loop=False)  # F4
        
        self.time += 1
    
    def draw(self):
        # Black background
        pyxel.cls(0)  # Black
        
        # Add stars
        if self.time % 5 == 0:
            for _ in range(5):
                if random.random() < 0.1:
                    star_x = random.randint(0, 511)
                    star_y = random.randint(0, 255)  # Upper half for stars
                    star_color = random.choice([6, 7])  # Light colors
                    pyxel.pset(star_x, star_y, star_color)
        
        # Draw all aurora curtains
        # Sort by distance for proper layering
        sorted_curtains = sorted(self.curtains, key=lambda c: c.x_start)
        
        for curtain in sorted_curtains:
            curtain.draw(self.time)
        
        # Add atmospheric glow effects
        self.draw_atmospheric_effects()
    
    def draw_atmospheric_effects(self):
        """Add atmospheric glow and particle effects"""
        # Subtle atmospheric glow at horizon
        horizon_y = 400
        glow_intensity = self.aurora_intensity * 0.5
        
        if random.random() < glow_intensity:
            for _ in range(10):
                glow_x = random.randint(0, 511)
                glow_y = random.randint(horizon_y, 511)
                glow_color = random.choice([3, 11])  # Green tones
                pyxel.pset(glow_x, glow_y, glow_color)
        
        # High-altitude sparkles
        if random.random() < self.magnetic_activity * 0.3:
            for _ in range(3):
                sparkle_x = random.randint(0, 511)
                sparkle_y = random.randint(0, 200)
                sparkle_color = random.choice([6, 7, 10])  # Bright colors
                pyxel.pset(sparkle_x, sparkle_y, sparkle_color)

AuroraBorealis()