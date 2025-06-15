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
    def __init__(self, signal_type, color=11):
        self.signal_type = signal_type  # 'sine', 'square', 'sawtooth', 'triangle', 'noise'
        self.frequency = random.uniform(0.01, 0.05)
        self.amplitude = random.uniform(50, 150)
        self.phase = random.uniform(0, math.pi * 2)
        self.y_offset = random.uniform(100, 400)
        self.color = color  # Waveform color
        
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
                        pyxel.line(x - 2, prev_y + thickness, x, y + thickness, self.color)
                    if thickness > 0 and 0 <= y - thickness < 512:
                        pyxel.line(x - 2, prev_y - thickness, x, y - thickness, self.color)
            
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
        
        # Sound design - 3 channel long tone chord construction
        # Channel 0: Root notes (bass)
        pyxel.sounds[0].set("e2e2e2e2e2e2e2e2", "t", "44444444", "n", 60)  # Long Em root
        # Channel 1: Third notes (harmony)  
        pyxel.sounds[1].set("g2g2g2g2g2g2g2g2", "t", "33333333", "n", 60)  # Long Em third
        # Channel 2: Fifth notes (top)
        pyxel.sounds[2].set("b2b2b2b2b2b2b2b2", "t", "22222222", "n", 60)  # Long Em fifth
        
        # Create 3 wave signals corresponding to the 3 audio channels
        self.signals = []
        # Use different waveforms and colors for each chord tone
        signal_types = ['sine', 'triangle', 'square']  # Root, Third, Fifth
        signal_colors = [11, 3, 10]  # Bright green, dark green, light green
        
        for i in range(3):
            signal_type = signal_types[i]
            signal = WaveSignal(signal_type, signal_colors[i])
            # Set frequencies that correspond to the chord tones
            signal.frequency = 0.02 + i * 0.01  # Different frequencies for each voice
            signal.y_offset = 128 + i * 128  # Separate vertical positions
            signal.amplitude = 80 - i * 10  # Different amplitudes
            self.signals.append(signal)
        
        # Oscilloscope components
        self.grid = OscilloscopeGrid()
        self.scan_line = ScanLine()
        
        # System state
        self.time = 0
        self.screen_flicker = 0
        self.chord_index = 0  # Track current chord in progression
        
        # Chord progression: Em - C - G - D with corresponding waveform shapes
        self.chords = [
            ("e2", "g2", "b2"),  # Em
            ("c2", "e2", "g2"),  # C
            ("g2", "b2", "d3"),  # G  
            ("d2", "f2", "a2")   # D
        ]
        
        # Waveform shape patterns for each chord (Root, Third, Fifth)
        self.chord_waveforms = [
            ['sine', 'triangle', 'square'],     # Em - flowing, soft to sharp
            ['square', 'sine', 'triangle'],     # C - strong, pure, soft
            ['triangle', 'square', 'sine'],     # G - building, strong, pure
            ['sawtooth', 'triangle', 'square']  # D - rising, building, strong
        ]
        
        pyxel.run(self.update, self.draw)
    
    def update_chord_sounds(self, chord_notes):
        """Update the 3 channels with new chord notes for long tone construction"""
        root, third, fifth = chord_notes
        
        # Channel 0: Root (bass) - long sustained tone
        pyxel.sounds[0].set(f"{root}{root}{root}{root}{root}{root}{root}{root}", "t", "44444444", "n", 60)
        # Channel 1: Third (harmony) - long sustained tone
        pyxel.sounds[1].set(f"{third}{third}{third}{third}{third}{third}{third}{third}", "t", "33333333", "n", 60)  
        # Channel 2: Fifth (top) - long sustained tone
        pyxel.sounds[2].set(f"{fifth}{fifth}{fifth}{fifth}{fifth}{fifth}{fifth}{fifth}", "t", "22222222", "n", 60)
        
        # Update visual frequencies and waveform shapes to match chord tones
        self.update_visual_frequencies(chord_notes)
        self.update_waveform_shapes(self.chord_index)
    
    def update_visual_frequencies(self, chord_notes):
        """Update visual waveform frequencies to correspond to chord tones"""
        # Note frequency mapping (approximate relative frequencies)
        note_freq_map = {
            'e2': 0.020, 'f2': 0.021, 'g2': 0.024, 'a2': 0.027, 'b2': 0.030,
            'c2': 0.016, 'd2': 0.018, 'c3': 0.032, 'd3': 0.036
        }
        
        root, third, fifth = chord_notes
        
        # Update each signal to match its corresponding chord tone
        if len(self.signals) >= 3:
            self.signals[0].frequency = note_freq_map.get(root, 0.020)    # Root
            self.signals[1].frequency = note_freq_map.get(third, 0.024)   # Third  
            self.signals[2].frequency = note_freq_map.get(fifth, 0.030)   # Fifth
    
    def update_waveform_shapes(self, chord_idx):
        """Update waveform shapes based on current chord progression"""
        current_waveforms = self.chord_waveforms[chord_idx % len(self.chord_waveforms)]
        
        # Update each signal's waveform type
        for i, signal in enumerate(self.signals[:3]):  # Only update first 3 signals
            signal.signal_type = current_waveforms[i]
    
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
        
        # Sound triggers - 3 channel long tone chord construction
        # Change chord every 4 seconds (120 frames) for longer harmonic development
        if self.time % 120 == 0:
            current_chord = self.chords[self.chord_index]
            self.update_chord_sounds(current_chord)
            self.chord_index = (self.chord_index + 1) % 4  # Cycle through chords
        
        # Start playing all 3 channels together for sustained chord
        if self.time % 120 == 10:  # Slight delay after chord update
            pyxel.play(0, 0, loop=True)   # Root - continuous loop
            pyxel.play(1, 1, loop=True)   # Third - continuous loop  
            pyxel.play(2, 2, loop=True)   # Fifth - continuous loop
        
        # Occasionally stop all channels for breathing space
        if self.time % 480 == 240:  # Every 16 seconds, pause for 4 seconds
            pyxel.stop(0)
            pyxel.stop(1) 
            pyxel.stop(2)
        
        self.time += 1
    
    def draw(self):
        # Black background (CRT screen)
        pyxel.cls(0)
        
        # Draw grid first
        self.grid.draw()
        
        # Draw all 3 waveform signals simultaneously (synced to chord tones)
        for i, signal in enumerate(self.signals):
            # Always draw all signals to visualize the 3-part harmony
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