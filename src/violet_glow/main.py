"""
Violet Glow - Anechoicetry Collection
by Leo Kuroshita
Screen glows in pale violet with slowly changing intensity - minimal variation
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class VioletGlow:
    def __init__(self):
        pyxel.init(512, 512, title="Violet Glow")
        
        self.time = 0
        self.base_intensity = 0.3
        self.glow_phase = 0
        self.energy_particles = []
        self.pulse_rings = []
        
        for _ in range(100):
            self.energy_particles.append({
                'x': random.randint(0, 512),
                'y': random.randint(0, 512),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'phase': random.uniform(0, math.pi * 2),
                'size': random.uniform(1, 3)
            })
        
        self.setup_sound()
        pyxel.run(self.update, self.draw)

    def setup_sound(self):
        # Deep violet glow tones
        pyxel.sounds[0].set("a0", "s", "7", "v", 15)
        pyxel.sounds[1].set("c1", "s", "6", "v", 12)
        pyxel.sounds[2].set("e1", "s", "5", "v", 10)
        
        # Pulsing glow effects
        pyxel.sounds[3].set("a1c2e2", "s", "543", "v", 8)
        pyxel.sounds[4].set("c2e2g2", "s", "432", "v", 6)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        self.glow_phase += 0.002
        
        # Deep pulsing glow sounds
        if self.time % 180 == 0:  # Every 3 seconds
            pyxel.play(0, random.randint(0, 2))
        
        if self.time % 300 == 0:  # Every 5 seconds
            pyxel.play(1, random.randint(3, 4))
        
        for particle in self.energy_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['phase'] += 0.05
            
            if particle['x'] < 0 or particle['x'] > 512:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > 512:
                particle['vy'] *= -1
        
        if random.random() < 0.02:
            self.pulse_rings.append({
                'x': 256,
                'y': 256,
                'radius': 0,
                'max_radius': random.randint(80, 150),
                'life': 100,
                'intensity': random.uniform(0.5, 1.0)
            })
            # Pulse ring sound
            if random.random() < 0.7:
                pyxel.play(1, random.randint(3, 4))
        
        for ring in self.pulse_rings[:]:
            ring['radius'] += 2
            ring['life'] -= 1
            if ring['life'] <= 0 or ring['radius'] > ring['max_radius']:
                self.pulse_rings.remove(ring)

    def draw(self):
        intensity_variation = math.sin(self.glow_phase) * 0.1
        current_intensity = self.base_intensity + intensity_variation
        
        secondary_variation = math.sin(self.glow_phase * 1.3) * 0.05
        final_intensity = current_intensity + secondary_variation
        
        final_intensity = max(0.1, min(0.6, final_intensity))
        
        if final_intensity < 0.2:
            color = 1
        elif final_intensity < 0.35:
            color = 2
        elif final_intensity < 0.5:
            color = 8
        else:
            color = 9
        
        pyxel.cls(color)
        
        center_x, center_y = 256, 256
        glow_radius = 250 + 50 * math.sin(self.glow_phase * 0.7)
        
        for y in range(0, 512, 1):
            for x in range(0, 512, 1):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if distance < glow_radius:
                    glow_strength = 1 - (distance / glow_radius)
                    glow_strength *= final_intensity
                    
                    layered_glow = glow_strength + 0.3 * math.sin(distance * 0.05 + self.glow_phase * 2)
                    
                    if layered_glow > 0.6:
                        if final_intensity > 0.4:
                            pyxel.pset(x, y, 14)
                        else:
                            pyxel.pset(x, y, 9)
                    elif layered_glow > 0.4:
                        pyxel.pset(x, y, 8)
                    elif layered_glow > 0.2 and random.random() < layered_glow:
                        pyxel.pset(x, y, 2)
        
        for ring in self.pulse_rings:
            life_ratio = ring['life'] / 100
            ring_intensity = ring['intensity'] * life_ratio
            
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = ring['x'] + ring['radius'] * math.cos(rad)
                y = ring['y'] + ring['radius'] * math.sin(rad)
                
                if 0 <= x < 512 and 0 <= y < 512:
                    thickness = 3 + int(ring_intensity * 5)
                    for t in range(-thickness, thickness + 1):
                        inner_x = x + t * math.cos(rad + math.pi/2)
                        inner_y = y + t * math.sin(rad + math.pi/2)
                        if 0 <= inner_x < 512 and 0 <= inner_y < 512:
                            if random.random() < ring_intensity:
                                color = 14 if ring_intensity > 0.7 else 9
                                pyxel.pset(int(inner_x), int(inner_y), color)
        
        for particle in self.energy_particles:
            brightness = (math.sin(particle['phase']) + 1) * 0.5
            if brightness > 0.3:
                size = int(particle['size'] * brightness) + 1
                color = 14 if brightness > 0.8 else (9 if brightness > 0.5 else 2)
                
                for dx in range(-size, size + 1):
                    for dy in range(-size, size + 1):
                        if dx*dx + dy*dy <= size*size:
                            px = int(particle['x']) + dx
                            py = int(particle['y']) + dy
                            if 0 <= px < 512 and 0 <= py < 512:
                                pyxel.pset(px, py, color)

if __name__ == "__main__":
    VioletGlow()