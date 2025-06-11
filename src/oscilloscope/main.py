"""
Oscilloscope - Anechoicetry Collection
by Leo Kuroshita
Electronic waveforms and signal patterns in black and green, like classic oscilloscope displays
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 2.0.0
"""

import pyxel
import math
import random

class WaveSignal:
    def __init__(self, signal_type):
        self.signal_type = signal_type  # 'sine', 'square', 'sawtooth', 'triangle', 'noise'
        self.frequency = random.uniform(0.01, 0.05)
        self.amplitude = random.uniform(50, 150)
        self.phase = random.uniform(0, math.pi * 2)
        self.y_offset = random.uniform(100, 400)
        
        # Signal modulation
        self.mod_frequency = random.uniform(0.001, 0.01)
        self.mod_amplitude = random.uniform(0.1, 0.5)
        self.mod_phase = random.uniform(0, math.pi * 2)
        
        # Visual properties
        self.brightness = random.uniform(0.7, 1.0)
        self.thickness = random.randint(1, 2)
        
        # Noise properties for noise signal
        self.noise_intensity = random.uniform(0.3, 0.8)
        
    def update(self, time):
        # Update phases
        self.phase += self.frequency
        self.mod_phase += self.mod_frequency
        
        # Frequency modulation
        freq_mod = 1 + self.mod_amplitude * math.sin(self.mod_phase)
        self.phase += self.frequency * freq_mod * 0.1
        
    def get_value(self, x, time):
        """Get signal value at position x"""
        t = x * 0.01 + self.phase
        
        # Base signal generation
        if self.signal_type == 'sine':
            base_value = math.sin(t)
        elif self.signal_type == 'square':
            base_value = 1 if math.sin(t) > 0 else -1
        elif self.signal_type == 'sawtooth':
            base_value = (t % (2 * math.pi)) / math.pi - 1
        elif self.signal_type == 'triangle':
            normalized_t = (t % (2 * math.pi)) / (2 * math.pi)
            if normalized_t < 0.5:
                base_value = 4 * normalized_t - 1
            else:
                base_value = 3 - 4 * normalized_t
        elif self.signal_type == 'noise':
            # Pseudo-random noise based on position and time
            noise_seed = int((x * 31 + time * 17) % 10000)
            random.seed(noise_seed)
            base_value = (random.random() - 0.5) * 2 * self.noise_intensity
            random.seed()  # Reset to current time
        
        # Apply amplitude modulation
        amp_mod = 1 + self.mod_amplitude * 0.3 * math.cos(self.mod_phase + x * 0.02)
        
        return self.y_offset + base_value * self.amplitude * amp_mod
    
    def draw(self, time):
        """Draw the waveform across the screen"""
        prev_y = None
        
        for x in range(0, 512, 2):  # Sample every 2 pixels for performance
            y = int(self.get_value(x, time))
            
            if prev_y is not None and 0 <= y < 512 and 0 <= prev_y < 512:
                # Draw line segment
                for thickness in range(self.thickness):
                    if 0 <= y + thickness < 512:
                        pyxel.line(x - 2, prev_y + thickness, x, y + thickness, 11)  # Green
                    if thickness > 0 and 0 <= y - thickness < 512:
                        pyxel.line(x - 2, prev_y - thickness, x, y - thickness, 11)  # Green
            
            prev_y = y

class OscilloscopeGrid:
    def __init__(self):
        self.grid_alpha = 0.3
        self.major_divisions = 8
        self.minor_divisions = 4
        
    def draw(self):
        """Draw oscilloscope grid lines"""
        grid_color = 3  # Dark green
        
        # Major grid lines
        for i in range(self.major_divisions + 1):
            # Vertical lines
            x = i * (512 // self.major_divisions)
            if random.random() < 0.8:  # Some lines fade occasionally
                pyxel.line(x, 0, x, 512, grid_color)
            
            # Horizontal lines
            y = i * (512 // self.major_divisions)
            if random.random() < 0.8:
                pyxel.line(0, y, 512, y, grid_color)
        
        # Center crosshairs
        pyxel.line(256, 0, 256, 512, grid_color)
        pyxel.line(0, 256, 512, 256, grid_color)

class ScanLine:
    def __init__(self):
        self.x = 0
        self.speed = random.uniform(1, 3)
        self.intensity = random.uniform(0.6, 1.0)
        
    def update(self):
        self.x += self.speed
        if self.x >= 512:
            self.x = 0
            self.speed = random.uniform(1, 3)
    
    def draw(self):
        """Draw vertical scan line like CRT displays"""
        if 0 <= self.x < 512:
            for y in range(0, 512, 4):
                if random.random() < self.intensity:
                    pyxel.pset(int(self.x), y, 11)  # Bright green

class Oscilloscope:
    def __init__(self):
        pyxel.init(512, 512, title="Oscilloscope")
        
        # Sound design - electronic, digital, scanning
        pyxel.sounds[0].set("c2e2g2", "s", "765", "v", 30)     # Electronic pulse
        pyxel.sounds[1].set("f1a1", "n", "54", "s", 25)        # Digital noise
        pyxel.sounds[2].set("g2c3", "t", "432", "f", 20)       # Scanning tone
        pyxel.sounds[3].set("d2f2", "s", "321", "v", 35)       # Signal sweep
        pyxel.sounds[4].set("a1d2", "n", "765", "s", 15)       # Static burst (fixed volume)
        pyxel.sounds[5].set("e2b2", "t", "654", "f", 28)       # Oscillation
        
        # Create multiple wave signals
        self.signals = []
        signal_types = ['sine', 'square', 'sawtooth', 'triangle', 'noise']
        
        for i in range(6):
            signal_type = signal_types[i % len(signal_types)]
            self.signals.append(WaveSignal(signal_type))
        
        # Oscilloscope components
        self.grid = OscilloscopeGrid()
        self.scan_line = ScanLine()
        
        # System state
        self.time = 0
        self.screen_flicker = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all signals
        for signal in self.signals:
            signal.update(self.time)
        
        # Update scan line
        self.scan_line.update()
        
        # Screen flicker effect
        self.screen_flicker = random.uniform(0.95, 1.0)
        
        # Sound triggers - electronic and scanning
        if self.time % 90 == 0 and random.random() < 0.4:
            pyxel.play(0, 0, loop=False)  # Electronic pulse
        
        if self.time % 120 == 60 and random.random() < 0.3:
            pyxel.play(1, 1, loop=False)  # Digital noise
        
        # Scanning tone
        if self.time % 150 == 75 and random.random() < 0.35:
            pyxel.play(2, 2, loop=False)  # Scanning tone
        
        # Signal sweep
        if self.time % 180 == 90 and random.random() < 0.4:
            pyxel.play(0, 3, loop=False)  # Signal sweep
        
        # Static burst
        if self.time % 200 == 100 and random.random() < 0.25:
            pyxel.play(1, 4, loop=False)  # Static burst
        
        # Oscillation
        if self.time % 100 == 50 and random.random() < 0.3:
            pyxel.play(2, 5, loop=False)  # Oscillation
        
        self.time += 1
    
    def draw(self):
        # Black background (CRT screen)
        pyxel.cls(0)
        
        # Draw grid first
        self.grid.draw()
        
        # Draw all waveform signals
        for i, signal in enumerate(self.signals):
            # Alternate between different signal displays
            if self.time % 300 < 50 * (i + 1):  # Show different signals over time
                signal.draw(self.time)
        
        # Draw scan line
        self.scan_line.draw()
        
        # CRT screen effects
        self.draw_crt_effects()
    
    def draw_crt_effects(self):
        """Draw CRT-style screen effects"""
        # Screen flicker
        if random.random() < 0.1:
            # Random bright green pixels for flicker
            for _ in range(10):
                fx = random.randint(0, 511)
                fy = random.randint(0, 511)
                pyxel.pset(fx, fy, 11)  # Bright green
        
        # Scan lines (subtle horizontal lines)
        if self.time % 3 == 0:
            for y in range(0, 512, 8):
                if random.random() < 0.2:
                    pyxel.line(0, y, 512, y, 3)  # Dark green scan line
        
        # Screen border glow
        if random.random() < 0.3:
            # Faint green glow around edges
            border_color = 3  # Dark green
            # Top and bottom
            pyxel.line(0, 0, 512, 0, border_color)
            pyxel.line(0, 511, 512, 511, border_color)
            # Left and right
            pyxel.line(0, 0, 0, 512, border_color)
            pyxel.line(511, 0, 511, 512, border_color)

Oscilloscope()