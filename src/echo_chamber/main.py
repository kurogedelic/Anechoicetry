"""
Echo Chamber - Anechoicetry Collection
by Leo Kuroshita
Sound visualization through rippling geometric patterns and resonant frequencies
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class EchoSource:
    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.frequency = frequency
        self.phase = random.uniform(0, math.pi * 2)
        self.amplitude = random.uniform(20, 60)
        self.color_base = random.choice([3, 6, 8, 11, 12, 14])
        self.age = 0
        self.drift_speed = random.uniform(0.01, 0.03)
        self.drift_angle = random.uniform(0, math.pi * 2)
        self.energy = 1.0
        self.last_sound = 0
        
    def update(self, time):
        self.age += 1
        self.phase += self.frequency
        
        # Gentle orbital drift
        self.drift_angle += self.drift_speed
        drift_radius = 15 + 10 * math.sin(time * 0.02)
        self.x = self.base_x + drift_radius * math.cos(self.drift_angle)
        self.y = self.base_y + drift_radius * math.sin(self.drift_angle)
        
        # Energy fluctuation
        self.energy = 0.7 + 0.3 * math.sin(time * 0.05 + self.phase)
        
    def get_ripple_strength(self, distance, time):
        wave = math.sin(self.phase - distance * 0.1) * self.energy
        falloff = max(0, 1 - distance / self.amplitude)
        return wave * falloff

class ResonanceParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.size = random.uniform(1, 3)
        self.color = random.choice([5, 7, 10, 13])
        self.life = random.randint(60, 180)
        self.max_life = self.life
        self.phase = random.uniform(0, math.pi * 2)
        
    def update(self, echo_sources, time):
        self.life -= 1
        self.phase += 0.1
        
        # Movement influenced by nearest echo source
        nearest_force = 0
        for source in echo_sources:
            dist = math.sqrt((self.x - source.x)**2 + (self.y - source.y)**2)
            if dist < 100:
                force = source.get_ripple_strength(dist, time) * 0.01
                angle = math.atan2(source.y - self.y, source.x - self.x)
                self.vx += math.cos(angle) * force
                self.vy += math.sin(angle) * force
                nearest_force = max(nearest_force, abs(force))
        
        # Apply velocity with damping
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        self.vy *= 0.98
        
        # Subtle oscillation
        oscillation = math.sin(self.phase) * 0.5
        self.x += oscillation
        self.y += oscillation * 0.7
        
        # Boundary wrap
        self.x = self.x % 512
        self.y = self.y % 512
        
        return self.life > 0

class EchoChamber:
    def __init__(self):
        pyxel.init(512, 512, title="Echo Chamber")
        
        # Sound design - 7 layered ambient frequencies with short decays
        pyxel.sounds[0].set("c2e2g2", "t", "765", "f", 45)    # Low bass resonance
        pyxel.sounds[1].set("g2b2d3", "s", "654", "v", 35)    # Mid harmonic
        pyxel.sounds[2].set("e3g3c4", "t", "543", "f", 25)    # High crystalline
        pyxel.sounds[3].set("f2a2c3", "p", "432", "s", 40)    # Pulse rhythm
        pyxel.sounds[4].set("d3f3a3", "n", "321", "f", 30)    # Noise texture
        pyxel.sounds[5].set("a1c2e2", "t", "765", "v", 50)    # Deep echo
        pyxel.sounds[6].set("c4e4g4", "t", "421", "f", 8)     # Short decay ping
        pyxel.sounds[7].set("g3", "n", "7210", "f", 6)        # Quick pop
        pyxel.sounds[8].set("d4f4", "s", "531", "v", 10)      # Sharp click
        pyxel.sounds[9].set("a3c4", "t", "321", "f", 12)      # Brief chime
        
        self.time = 0
        
        # Echo sources - positioned in golden ratio spiral
        self.echo_sources = []
        center_x, center_y = 256, 256
        golden_angle = 137.5 * math.pi / 180
        
        for i in range(7):
            angle = i * golden_angle
            radius = 30 + i * 25
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            frequency = 0.02 + i * 0.01
            self.echo_sources.append(EchoSource(x, y, frequency))
        
        # Resonance particles
        self.particles = []
        for _ in range(150):
            x = random.randint(50, 462)
            y = random.randint(50, 462)
            self.particles.append(ResonanceParticle(x, y))
        
        # Visual parameters
        self.background_pulse = 0
        self.harmonic_shift = 0
        self.resonance_peaks = []
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update echo sources
        for source in self.echo_sources:
            source.update(self.time)
        
        # Update particles
        active_particles = []
        for particle in self.particles:
            if particle.update(self.echo_sources, self.time):
                active_particles.append(particle)
        self.particles = active_particles
        
        # Spawn new particles occasionally
        if len(self.particles) < 120 and random.random() < 0.3:
            x = random.randint(50, 462)
            y = random.randint(50, 462)
            self.particles.append(ResonanceParticle(x, y))
        
        # Background dynamics
        self.harmonic_shift += 0.01
        
        # Sound triggers based on resonance patterns
        if self.time % 90 == 0 and random.random() < 0.6:
            pyxel.play(0, 0, loop=False)
        
        if self.time % 120 == 30 and random.random() < 0.4:
            pyxel.play(1, 1, loop=False)
        
        if self.time % 180 == 60 and random.random() < 0.5:
            pyxel.play(2, 2, loop=False)
        
        # Rhythmic pulse sounds
        if self.time % 75 == 0:
            pyxel.play(3, 3, loop=False)
        
        # Ambient texture
        if self.time % 200 == 100 and random.random() < 0.3:
            pyxel.play(1, 4, loop=False)
        
        # Deep echo
        if self.time % 240 == 0 and random.random() < 0.4:
            pyxel.play(2, 5, loop=False)
        
        # Short decay sounds - more frequent
        if self.time % 15 == 0 and random.random() < 0.4:
            pyxel.play(0, 6, loop=False)  # Short ping
        
        if self.time % 25 == 5 and random.random() < 0.3:
            pyxel.play(1, 7, loop=False)  # Quick pop
        
        if self.time % 35 == 10 and random.random() < 0.35:
            pyxel.play(2, 8, loop=False)  # Sharp click
        
        if self.time % 45 == 20 and random.random() < 0.25:
            pyxel.play(3, 9, loop=False)  # Brief chime
        
        # Particle-triggered sounds
        if len(self.particles) > 100 and self.time % 8 == 0 and random.random() < 0.2:
            pyxel.play(0, 6, loop=False)
        
        # Echo source energy-based sounds
        for i, source in enumerate(self.echo_sources):
            if source.energy > 0.9 and self.time % 20 == i * 3 and random.random() < 0.15:
                sound_choice = random.choice([6, 7, 8, 9])
                pyxel.play(1, sound_choice, loop=False)
        
        self.time += 1
    
    def draw(self):
        # White background
        pyxel.cls(7)
        
        # Draw resonance field - concentric shapes from each source
        for source in self.echo_sources:
            self.draw_resonance_field(source)
        
        # Draw connecting harmonics between sources
        self.draw_harmonic_connections()
        
        # Draw particles
        for particle in self.particles:
            alpha = particle.life / particle.max_life
            if alpha > 0.2:
                size = particle.size * alpha
                color = particle.color if alpha > 0.5 else max(1, particle.color - 3)
                
                x = int(particle.x + math.sin(particle.phase) * 0.5)
                y = int(particle.y + math.cos(particle.phase * 0.7) * 0.5)
                
                if size > 1.5:
                    pyxel.circ(x, y, int(size), color)
                else:
                    pyxel.pset(x, y, color)
        
        # Central resonance core
        core_pulse = 3 + int(2 * math.sin(self.time * 0.1))
        core_color = 7 + int(3 * math.sin(self.harmonic_shift))
        pyxel.circ(256, 256, core_pulse, core_color)
        pyxel.circb(256, 256, core_pulse + 5, max(1, core_color - 2))
    
    def draw_resonance_field(self, source):
        # Multiple concentric rings emanating from source
        for ring in range(5):
            radius = 15 + ring * 12
            strength = source.get_ripple_strength(radius, self.time)
            
            if abs(strength) > 0.1:
                # Ring thickness based on strength
                thickness = max(1, int(abs(strength) * 3))
                color = source.color_base + int(strength * 2)
                color = max(1, min(15, color))
                
                # Draw segments of the ring based on strength
                segments = 24
                for i in range(segments):
                    angle = (i / segments) * 2 * math.pi
                    segment_strength = strength * (0.7 + 0.3 * math.sin(angle * 4 + source.phase))
                    
                    if abs(segment_strength) > 0.2:
                        x1 = int(source.x + radius * math.cos(angle))
                        y1 = int(source.y + radius * math.sin(angle))
                        
                        # Small arc segment
                        for t in range(thickness):
                            angle2 = angle + (t / segments) * 0.3
                            x2 = int(source.x + (radius + t) * math.cos(angle2))
                            y2 = int(source.y + (radius + t) * math.sin(angle2))
                            
                            if 0 <= x2 < 512 and 0 <= y2 < 512:
                                pyxel.pset(x2, y2, color)
    
    def draw_harmonic_connections(self):
        # Draw resonant connections between echo sources
        for i, source1 in enumerate(self.echo_sources):
            for j, source2 in enumerate(self.echo_sources[i+1:], i+1):
                distance = math.sqrt((source1.x - source2.x)**2 + (source1.y - source2.y)**2)
                
                # Only connect sources within harmonic range
                if distance < 150:
                    # Connection strength based on phase relationship
                    phase_diff = abs(source1.phase - source2.phase) % (math.pi * 2)
                    harmonic_resonance = math.cos(phase_diff) * (source1.energy + source2.energy) / 2
                    
                    if harmonic_resonance > 0.3:
                        # Draw harmonic line with varying intensity
                        segments = int(distance / 8)
                        for k in range(segments):
                            t = k / segments
                            x = int(source1.x + t * (source2.x - source1.x))
                            y = int(source1.y + t * (source2.y - source1.y))
                            
                            # Harmonic modulation along the line
                            wave = math.sin(t * math.pi * 6 + self.time * 0.1) * harmonic_resonance
                            if wave > 0.1:
                                color = int(5 + wave * 8)
                                color = max(1, min(15, color))
                                pyxel.pset(x, y, color)

EchoChamber()