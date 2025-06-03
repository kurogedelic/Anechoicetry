"""
Screen Damage - Anechoicetry Collection
by Leo Kuroshita
Digital corruption patterns with glitched audio and visual artifacts
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class ScreenDamage:
    def __init__(self):
        pyxel.init(512, 512, title="Screen Damage")
        
        # Wave sound parameters
        self.wave_phase = 0
        self.sparkle_particles = []
        self.horizon_y = 200
        
        # Initialize wave sounds with white noise at different frequencies
        # Deep ocean rumble
        pyxel.sounds[0].set(
            "c0c0c0c0d0d0d0d0e0e0e0e0f0f0f0f0",
            "nnnn",
            "4433221100112233",
            "f",
            30
        )
        
        # Mid-frequency wave crash
        pyxel.sounds[1].set(
            "g1g1a1a1b1b1c2c2b1b1a1a1g1g1f1f1",
            "nnnn",
            "1234567776543210",
            "s",
            25
        )
        
        # High frequency foam
        pyxel.sounds[2].set(
            "c3d3e3f3g3a3b3c4b3a3g3f3e3d3c3b2",
            "nnnn",
            "2345654321234565",
            "f",
            20
        )
        
        # Gentle lapping
        pyxel.sounds[3].set(
            "e2e2f2f2g2g2a2a2g2g2f2f2e2e2d2d2",
            "nnnn",
            "3456765432345676",
            "n",
            35
        )
        
        # Distant shore ambience
        pyxel.sounds[4].set(
            "a1b1c2d2e2f2g2a2g2f2e2d2c2b1a1g1",
            "nnnn",
            "1122334455443322",
            "v",
            40
        )
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update wave phase for sound timing
        self.wave_phase += 0.02
        
        # Play wave sounds with periodic volume changes
        if pyxel.frame_count % 30 == 0:
            channel = random.randint(0, 2)
            sound = random.randint(0, 4)
            # Modulate volume based on wave phase
            volume_mod = int(abs(math.sin(self.wave_phase)) * 3)
            pyxel.play(channel, sound)
        
        # Update sparkle particles
        self.sparkle_particles = [p for p in self.sparkle_particles if p[3] > 0]
        
        # Add new sparkles on water surface
        if random.random() < 0.3:
            x = random.randint(0, 511)
            y = random.randint(self.horizon_y, 511)
            # More sparkles closer to horizon
            if random.random() < (512 - y) / 312:
                life = random.randint(10, 30)
                self.sparkle_particles.append([x, y, random.random() * math.pi * 2, life])
        
        # Update existing sparkles
        for particle in self.sparkle_particles:
            particle[2] += 0.1  # Rotate
            particle[3] -= 1    # Decrease life
    
    def draw(self):
        # Clear with dark orange sky
        pyxel.cls(1)
        
        # Draw gradient sky
        for y in range(self.horizon_y):
            if y < 80:
                color = 1  # Dark blue/purple
            elif y < 140:
                color = 2  # Dark red
            else:
                color = 9  # Orange
            
            # Add subtle variations
            if random.random() < 0.02:
                pyxel.line(0, y, 511, y, color)
        
        # Draw sea with orange tones
        for y in range(self.horizon_y, 512):
            # Base water color gets darker with depth
            if y < self.horizon_y + 100:
                base_color = 9  # Orange
            elif y < self.horizon_y + 200:
                base_color = 4  # Dark red
            else:
                base_color = 1  # Dark blue
            
            # Wave distortion
            wave_offset = math.sin(self.wave_phase + y * 0.02) * 2
            
            for x in range(0, 512, 2):
                # Add wave patterns
                wave = math.sin(x * 0.01 + self.wave_phase + wave_offset) * \
                       math.sin(y * 0.03 + self.wave_phase * 0.5)
                
                if wave > 0.3:
                    pyxel.pset(x + int(wave_offset), y, 10)  # Bright yellow sparkle
                elif wave > 0:
                    pyxel.pset(x, y, base_color)
                else:
                    pyxel.pset(x, y, base_color - 1 if base_color > 1 else 0)
        
        # Draw sparkles
        for x, y, angle, life in self.sparkle_particles:
            if life > 20:
                sparkle_color = 10  # Bright yellow
            elif life > 10:
                sparkle_color = 9   # Orange
            else:
                sparkle_color = 4   # Dark red
            
            # Star-shaped sparkle
            size = min(3, life // 10)
            for i in range(4):
                angle_offset = angle + i * math.pi / 2
                dx = int(math.cos(angle_offset) * size)
                dy = int(math.sin(angle_offset) * size)
                pyxel.pset(x + dx, y + dy, sparkle_color)
        
        # Draw horizon line
        pyxel.line(0, self.horizon_y, 511, self.horizon_y, 9)
        
        # Add subtle beach sand at bottom
        for y in range(480, 512):
            for x in range(512):
                if random.random() < 0.1:
                    pyxel.pset(x, y, 4)  # Dark sand color

ScreenDamage()