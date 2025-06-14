"""
Diatomea Computer - Anechoicetry Collection
by Leo Kuroshita
Kaleidoscope of recursive fractals unfolding endlessly in digital space
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 2.0.0
"""

import pyxel
import random
import math

class DiatomaComputer:
    def __init__(self):
        pyxel.init(512, 512, title="Diatomea Computer")
        
        # Initialize sound design
        self.init_sounds()
        
        # Kaleidoscope state
        self.frame = 0
        self.center_x = 256
        self.center_y = 256
        self.rotation = 0
        self.scale = 1.0
        self.recursion_depth = 6
        
        # Fractal parameters that evolve over time
        self.angle_offset = 0
        self.size_factor = 100
        self.branch_count = 6  # Number of kaleidoscope segments
        
        # Colors - only black (0) and green (3)
        self.green = 3
        self.black = 0
        
        # Audio sequencer state
        self.sequencer_step = 0  # Current 1/16 note step
        self.chord_index = 0     # Current chord in progression
        self.pattern_length = 16 # 16 steps per pattern
        
        pyxel.run(self.update, self.draw)
    
    def draw_fractal_branch(self, x, y, size, angle, depth):
        """Draw a recursive fractal branch"""
        if depth <= 0 or size < 2:
            return
        
        # Calculate end point of current branch
        end_x = x + size * math.cos(angle)
        end_y = y + size * math.sin(angle)
        
        # Draw the branch line
        pyxel.line(int(x), int(y), int(end_x), int(end_y), self.green)
        
        # Add some geometric shapes at branch points
        if depth % 2 == 0:
            pyxel.circb(int(end_x), int(end_y), max(1, int(size / 10)), self.green)
        else:
            rect_size = max(1, int(size / 15))
            pyxel.rectb(int(end_x - rect_size), int(end_y - rect_size), 
                       rect_size * 2, rect_size * 2, self.green)
        
        # Recursive branches with different angles and sizes
        new_size = size * 0.7
        angle_spread = math.pi / 4 + math.sin(self.frame * 0.02) * 0.2
        
        # Create multiple sub-branches
        for i in range(2):
            new_angle = angle + ((-1) ** i) * angle_spread + self.angle_offset
            self.draw_fractal_branch(end_x, end_y, new_size, new_angle, depth - 1)
    
    def draw_kaleidoscope_segment(self, segment_angle):
        """Draw one segment of the kaleidoscope"""
        # Start from center and draw outward
        start_size = self.size_factor * (1 + 0.3 * math.sin(self.frame * 0.01))
        
        # Main branch
        self.draw_fractal_branch(
            self.center_x, self.center_y, 
            start_size, segment_angle, 
            self.recursion_depth
        )
        
        # Add spiral patterns
        spiral_radius = 50 + 30 * math.sin(self.frame * 0.015)
        for i in range(8):
            spiral_angle = segment_angle + i * math.pi / 4 + self.rotation
            spiral_x = self.center_x + spiral_radius * math.cos(spiral_angle)
            spiral_y = self.center_y + spiral_radius * math.sin(spiral_angle)
            
            # Draw smaller fractals at spiral points
            if spiral_x >= 0 and spiral_x < 512 and spiral_y >= 0 and spiral_y < 512:
                self.draw_fractal_branch(
                    spiral_x, spiral_y,
                    start_size * 0.4, spiral_angle + math.pi, 
                    self.recursion_depth - 2
                )
    
    def init_sounds(self):
        # Define chord progressions (using note numbers for easier transposition)
        # i-VI-III-VII progression in A minor (Am-F-C-G)
        self.chord_progression = [
            ["A3", "C4", "E4"],    # Am
            ["F3", "A3", "C4"],    # F
            ["C3", "E3", "G3"],    # C
            ["G3", "B3", "D4"],    # G
            ["A3", "C4", "E4"],    # Am (repeat)
            ["F3", "A3", "C4"],    # F
            ["E3", "G3", "B3"],    # Em
            ["G3", "B3", "D4"]     # G
        ]
        
        # Channel 0: Bass line (staccato quarter notes)
        pyxel.sounds[0].set(
            notes="A2R R R ",  # Will be updated dynamically
            tones="T",
            volumes="4111",
            effects="N",
            speed=8  # Faster for staccato effect
        )
        
        # Channel 1: Mid-range harmony (syncopated)
        pyxel.sounds[1].set(
            notes="C4R E4R ",  # Will be updated dynamically
            tones="T",
            volumes="3232",
            effects="N",
            speed=8
        )
        
        # Channel 2: High melodic line (sparse)
        pyxel.sounds[2].set(
            notes="E4R R R ",  # Will be updated dynamically
            tones="P",  # Pulse wave for brighter sound
            volumes="4111",
            effects="N",
            speed=8
        )
        
        # Channel 3: Rhythmic accent (percussion-like)
        pyxel.sounds[3].set(
            notes="G2R R R ",  # Will be updated dynamically
            tones="N",  # Noise for percussive effect
            volumes="6222",
            effects="N",
            speed=8
        )
    
    def get_current_chord(self):
        """Get the current chord based on progression and time"""
        return self.chord_progression[self.chord_index % len(self.chord_progression)]
    
    def update_sound_patterns(self):
        """Update sound patterns based on current chord and step"""
        chord = self.get_current_chord()
        
        # Bass pattern (root note on beats 1 and 3)
        if self.sequencer_step % 8 == 0 or self.sequencer_step % 8 == 4:
            bass_note = chord[0][:-1] + "2"  # Root note in bass octave
            pyxel.sounds[0].set(
                notes=f"{bass_note}R R R ",
                tones="T",
                volumes="5111",
                effects="N",
                speed=8
            )
        
        # Mid harmony (chord tones on off-beats)
        if self.sequencer_step % 4 == 2:
            mid_note = chord[1]  # Third of chord
            pyxel.sounds[1].set(
                notes=f"{mid_note}R R R ",
                tones="T",
                volumes="3111",
                effects="N",
                speed=8
            )
        
        # High melody (fifth on specific beats)
        if self.sequencer_step % 8 == 1 or self.sequencer_step % 8 == 6:
            high_note = chord[2]  # Fifth of chord
            pyxel.sounds[2].set(
                notes=f"{high_note}R R R ",
                tones="P",
                volumes="4111",
                effects="N",
                speed=8
            )
        
        # Rhythmic accent (every 4th beat)
        if self.sequencer_step % 4 == 0:
            pyxel.sounds[3].set(
                notes="G2R R R ",
                tones="N",
                volumes="4111",
                effects="N",
                speed=8
            )
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.frame += 1
        
        # Update kaleidoscope parameters for endless unfolding
        self.rotation += 0.01  # Slow rotation
        self.angle_offset = math.sin(self.frame * 0.005) * 0.5  # Breathing angle changes
        
        # Evolving size factor for pulsing effect
        self.size_factor = 80 + 40 * math.sin(self.frame * 0.008)
        
        # Occasionally change recursion depth for variety
        if self.frame % 300 == 0:  # Every 10 seconds
            self.recursion_depth = random.randint(4, 7)
        
        # Change branch count occasionally for different kaleidoscope patterns
        if self.frame % 600 == 0:  # Every 20 seconds
            self.branch_count = random.choice([4, 5, 6, 8])
        
        # Update sequencer (1/16 notes at ~120 BPM)
        # 120 BPM = 2 beats per second = 8 sixteenth notes per second
        # At 30 FPS: 30/8 = 3.75 frames per sixteenth note
        if self.frame % 4 == 0:  # Every ~4 frames = 1/16 note at 120 BPM
            self.update_sound_patterns()
            
            # Trigger the appropriate channel based on pattern
            chord = self.get_current_chord()
            
            # Bass on strong beats
            if self.sequencer_step % 8 == 0 or self.sequencer_step % 8 == 4:
                pyxel.play(0, 0)
            
            # Mid harmony on syncopated beats
            if self.sequencer_step % 4 == 2:
                pyxel.play(1, 1)
            
            # High melody on specific beats
            if self.sequencer_step % 8 == 1 or self.sequencer_step % 8 == 6:
                pyxel.play(2, 2)
            
            # Rhythmic accent
            if self.sequencer_step % 4 == 0:
                pyxel.play(3, 3)
            
            # Advance sequencer
            self.sequencer_step += 1
            
            # Change chord every 32 steps (2 bars)
            if self.sequencer_step % 32 == 0:
                self.chord_index += 1
            
            # Reset pattern every 16 steps
            if self.sequencer_step >= self.pattern_length:
                self.sequencer_step = 0
    
    def draw(self):
        pyxel.cls(self.black)  # Black background
        
        # Draw kaleidoscope - multiple segments arranged in a circle
        for i in range(self.branch_count):
            segment_angle = (2 * math.pi * i / self.branch_count) + self.rotation
            self.draw_kaleidoscope_segment(segment_angle)
        
        # Add central ornament
        center_size = 20 + 10 * math.sin(self.frame * 0.03)
        pyxel.circb(self.center_x, self.center_y, int(center_size), self.green)
        
        # Add some flowing particles that follow the fractal paths
        for i in range(20):
            particle_angle = self.rotation * 2 + i * math.pi / 10
            particle_radius = 100 + 50 * math.sin(self.frame * 0.02 + i * 0.5)
            particle_x = self.center_x + particle_radius * math.cos(particle_angle)
            particle_y = self.center_y + particle_radius * math.sin(particle_angle)
            
            if 0 <= particle_x < 512 and 0 <= particle_y < 512:
                pyxel.pset(int(particle_x), int(particle_y), self.green)
        
        # Add outer ring pattern
        outer_radius = 200 + 50 * math.cos(self.frame * 0.01)
        for i in range(36):  # 36 points around the circle
            ring_angle = i * math.pi / 18 + self.rotation * 0.5
            ring_x = self.center_x + outer_radius * math.cos(ring_angle)
            ring_y = self.center_y + outer_radius * math.sin(ring_angle)
            
            if 0 <= ring_x < 512 and 0 <= ring_y < 512:
                if i % 3 == 0:  # Every third point gets a small shape
                    pyxel.circb(int(ring_x), int(ring_y), 2, self.green)

if __name__ == "__main__":
    DiatomaComputer()