"""
Barcodes - Anechoicetry Collection
by Leo Kuroshita
Monochrome vertical stripes that flash and change like scanning codes
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random


class Barcodes:
    def __init__(self):
        pyxel.init(512, 512, title="Barcodes")
        
        # Initialize barcode system
        self.bars = []
        self.frame_count = 0
        self.flash_intensity = 0
        
        # Generate initial barcode pattern
        self.generate_barcode_pattern()
        
        # Initialize glitch sound design
        self.setup_sounds()
        
        pyxel.run(self.update, self.draw)
    
    def setup_sounds(self):
        # Low frequency glitch noise
        pyxel.sounds[0].set(
            "a0a0a0a0b0b0b0c1c1c1",
            "nnn",
            "7654321076543210",
            "s",
            30
        )
        
        # High frequency glitch noise
        pyxel.sounds[1].set(
            "f3g3a3f3g3a3b3c4b3a3",
            "nnn",
            "6543210654321065",
            "f",
            20
        )
        
        # Sharp digital click
        pyxel.sounds[2].set(
            "c4c4",
            "nn",
            "70",
            "f",
            5
        )
        
        # Static burst
        pyxel.sounds[3].set(
            "a3b3c4d4e4f4g4a4",
            "nnnnnnnn",
            "765432107654321076543210",
            "s",
            15
        )
        
        # Deep scanning rumble
        pyxel.sounds[4].set(
            "c1d1e1f1g1a1b1c2",
            "nnnnnnnn",
            "43210432104321043210",
            "s",
            25
        )
        
        # Data corruption sound
        pyxel.sounds[5].set(
            "c4b3a2g1f1e0d0c0",
            "nnnnnnnn",
            "76543210123456701234567",
            "f",
            12
        )
    
    def generate_barcode_pattern(self):
        self.bars = []
        x = 0
        is_fill = True  # Start with a fill (black bar)
        
        while x < 512:
            # Random bar width (1-12 pixels for variety)
            width = random.randint(1, 12)
            
            # Ensure we don't exceed screen width
            if x + width > 512:
                width = 512 - x
            
            # Alternate between fill (black) and gap (white)
            bar_type = 0 if is_fill else 1  # 0=black fill, 1=white gap
            
            # All bars have same height and alignment (proper barcode format)
            height = 512
            y_offset = 0
            
            self.bars.append({
                'x': x,
                'width': width,
                'height': height,
                'y_offset': y_offset,
                'type': bar_type,
                'glitch_timer': random.randint(0, 120),
                'flash_timer': random.randint(0, 60)
            })
            
            x += width
            is_fill = not is_fill  # Toggle between fill and gap
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.frame_count += 1
        
        # Global flash effect
        if random.random() < 0.02:
            self.flash_intensity = 255
            pyxel.play(0, 2)  # Sharp click on flash
        
        if self.flash_intensity > 0:
            self.flash_intensity -= 8
        
        # Update each bar
        for bar in self.bars:
            # Glitch timer - randomly change bar properties
            bar['glitch_timer'] -= 1
            if bar['glitch_timer'] <= 0:
                bar['glitch_timer'] = random.randint(30, 180)
                
                # Sometimes flip bar type
                if random.random() < 0.3:
                    bar['type'] = 1 - bar['type']
                    pyxel.play(0, random.choice([0, 1]))  # Glitch noise
                
                # Sometimes change width
                if random.random() < 0.1:
                    bar['width'] = random.randint(1, 12)
                
                # Keep height consistent for barcode format
                # No height changes needed
            
            # Flash timer - individual bar flashing
            bar['flash_timer'] -= 1
            if bar['flash_timer'] <= 0:
                bar['flash_timer'] = random.randint(40, 120)
                if random.random() < 0.1:
                    bar['type'] = 1 - bar['type']
                    pyxel.play(0, 3)  # Static burst
        
        # Scanning sound effects
        if self.frame_count % 30 == 0:
            if random.random() < 0.3:
                pyxel.play(0, 4)  # Deep scanning rumble
        
        # Data corruption events
        if random.random() < 0.005:
            # Corrupt a section of bars
            start_idx = random.randint(0, max(0, len(self.bars) - 10))
            for i in range(start_idx, min(len(self.bars), start_idx + random.randint(3, 8))):
                self.bars[i]['type'] = random.randint(0, 1)
            pyxel.play(0, 5)  # Data corruption sound
        
        # Occasionally regenerate entire pattern
        if random.random() < 0.001:
            self.generate_barcode_pattern()
            pyxel.play(0, random.choice([0, 1, 3]))
    
    def draw(self):
        # Clear screen to black
        pyxel.cls(0)
        
        # Draw barcode bars
        for bar in self.bars:
            color = 7 if bar['type'] == 1 else 0  # White or black
            
            # Apply flash effect
            if self.flash_intensity > 0:
                color = 7 if color == 0 else 0  # Invert on flash
            
            pyxel.rect(
                bar['x'], 
                bar['y_offset'], 
                bar['width'], 
                bar['height'], 
                color
            )
        
        # No scanning line needed
        
        # Draw glitch artifacts
        if random.random() < 0.1:
            # Random noise pixels
            for _ in range(random.randint(5, 20)):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                color = random.choice([0, 7])
                pyxel.pset(x, y, color)
        
        # Draw horizontal scan lines occasionally
        if random.random() < 0.05:
            y = random.randint(0, 511)
            pyxel.line(0, y, 512, y, 5 if random.random() < 0.5 else 6)


if __name__ == "__main__":
    Barcodes()