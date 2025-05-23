# title: Scan
# author: Leo Kuroshita
# desc: QR code-like cellular automaton.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import random

class Scan:
    def __init__(self):
        pyxel.init(512, 512, title="Scan")
        
        # Cellular automaton sound definitions
        pyxel.sounds[0].set("c3", "s", "4", "n", 10)    # Generation sound 1
        pyxel.sounds[1].set("g3", "s", "3", "n", 8)     # Generation sound 2
        pyxel.sounds[2].set("e3", "p", "5", "n", 12)    # Generation sound 3
        pyxel.sounds[3].set("f3", "s", "2", "n", 15)    # Generation sound 4
        pyxel.sounds[4].set("a3", "p", "6", "n", 6)     # Generation sound 5
        pyxel.sounds[5].set("d3", "s", "4", "n", 20)    # Generation sound
        
        self.time = 0
        
        # QR code size and cells
        self.grid_size = 32  # 32x32 grid
        self.cell_size = 512 // self.grid_size
        
        # Cellular automaton grid
        self.current_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.next_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Target marker positions and sizes
        self.markers = [
            {"x": 1, "y": 1, "size": 8},      # Top-left (large)
            {"x": 23, "y": 1, "size": 8},     # Top-right (large)
            {"x": 1, "y": 23, "size": 8},     # Bottom-left (large)
            {"x": 23, "y": 27, "size": 4}     # Bottom-right (small)
        ]
        
        # Cellular automaton parameters
        self.generation = 0
        self.generation_timer = 0
        self.generation_interval = 30  # Frame count
        
        # Initialize
        self.setup_markers()
        self.randomize_automaton_area()
        
        pyxel.run(self.update, self.draw)
    
    def setup_markers(self):
        """Set up target markers"""
        for marker in self.markers:
            x, y, size = marker["x"], marker["y"], marker["size"]
            
            # Outer frame
            for i in range(size):
                for j in range(size):
                    if i == 0 or i == size-1 or j == 0 or j == size-1:
                        if 0 <= x+i < self.grid_size and 0 <= y+j < self.grid_size:
                            self.current_grid[y+j][x+i] = 1
            
            # Inner square (for size 6 or larger)
            if size >= 6:
                inner_start = 2
                inner_end = size - 2
                for i in range(inner_start, inner_end):
                    for j in range(inner_start, inner_end):
                        if 0 <= x+i < self.grid_size and 0 <= y+j < self.grid_size:
                            self.current_grid[y+j][x+i] = 1
    
    def randomize_automaton_area(self):
        """Randomly initialize cellular automaton area"""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if not self.is_marker_area(x, y):
                    self.current_grid[y][x] = random.choice([0, 1])
    
    def is_marker_area(self, x, y):
        """Check if specified coordinates are in marker area"""
        for marker in self.markers:
            mx, my, size = marker["x"], marker["y"], marker["size"]
            if mx <= x < mx + size and my <= y < my + size:
                return True
        return False
    
    def apply_cellular_automaton(self):
        """Apply cellular automaton rules"""
        # Initialize next generation grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.next_grid[y][x] = self.current_grid[y][x]
        
        # Apply cellular automaton rules
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if not self.is_marker_area(x, y):
                    neighbors = self.count_neighbors(x, y)
                    current_cell = self.current_grid[y][x]
                    
                    # Conway's Game of Life variation
                    if current_cell == 1:  # Living cell
                        if neighbors < 2 or neighbors > 3:
                            self.next_grid[y][x] = 0  # Death
                    else:  # Dead cell
                        if neighbors == 3:
                            self.next_grid[y][x] = 1  # Birth
                        elif neighbors == 2 and random.random() < 0.1:  # Random element
                            self.next_grid[y][x] = 1
        
        # Update grid
        self.current_grid, self.next_grid = self.next_grid, self.current_grid
        
        # Reset markers (protection)
        self.setup_markers()
        
        self.generation += 1
    
    def count_neighbors(self, x, y):
        """Count neighboring living cells"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    count += self.current_grid[ny][nx]
        return count
    
    def play_generation_sound(self):
        """Play sound when generation changes"""
        # Select random scale sound
        sound_id = random.randint(0, 4)
        channel = random.randint(0, 3)
        
        pyxel.play(channel, sound_id, loop=False)
        
        # Occasionally play generation sound too
        if random.random() < 0.3:
            pyxel.play(2, 5, loop=False)
    
    def add_random_noise(self):
        """Add random noise (promote evolution)"""
        if random.random() < 0.1:  # 10% chance
            for _ in range(random.randint(1, 5)):
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - 1)
                
                if not self.is_marker_area(x, y):
                    self.current_grid[y][x] = random.choice([0, 1])
    
    def check_stagnation(self):
        """Check stagnation and inject new patterns"""
        if self.generation % 100 == 0:  # Every 100 generations
            # Inject random pattern in center area
            center_x = self.grid_size // 2
            center_y = self.grid_size // 2
            
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    x, y = center_x + dx, center_y + dy
                    if (0 <= x < self.grid_size and 0 <= y < self.grid_size and 
                        not self.is_marker_area(x, y)):
                        self.current_grid[y][x] = random.choice([0, 1])
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Generation update timer
        self.generation_timer += 1
        
        if self.generation_timer >= self.generation_interval:
            # Evolve cellular automaton to next generation
            self.apply_cellular_automaton()
            
            # Play sound
            self.play_generation_sound()
            
            # Add random noise
            self.add_random_noise()
            
            # Check stagnation
            self.check_stagnation()
            
            # Reset timer
            self.generation_timer = 0
            
            # Randomly change interval
            self.generation_interval = random.randint(20, 50)
        
        # Background sound
        if self.time % 200 == 0 and random.random() < 0.2:
            ambient_sound = random.choice([0, 1, 2])
            pyxel.play(3, ambient_sound, loop=False)
        
        self.time += 1
    
    def draw(self):
        # White background
        pyxel.cls(7)
        
        # Draw cellular automaton grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.current_grid[y][x] == 1:
                    px = x * self.cell_size
                    py = y * self.cell_size
                    pyxel.rect(px, py, self.cell_size, self.cell_size, 0)
        
        # Scan effect (occasionally show scan lines)
        if self.time % 120 < 60:
            scan_y = (self.time % 120) * (512 // 60)
            pyxel.rect(0, scan_y, 512, 2, 8)
            
            # Scan sound
            if self.time % 120 == 0:
                pyxel.play(1, random.choice([3, 4]), loop=False)
        
        # Data matrix-style border lines
        pyxel.rectb(0, 0, 512, 512, 0)
        
        # Display generation information
        generation_text = f"GEN:{self.generation:04d}"
        pyxel.text(5, 5, generation_text, 0)
        
        # Progress bar (progress to next generation)
        progress = self.generation_timer / self.generation_interval
        progress_width = int(100 * progress)
        pyxel.rect(5, 15, progress_width, 3, 8)
        pyxel.rectb(5, 15, 100, 3, 0)
        
        # Occasional flicker effect
        if random.random() < 0.02:
            # Noise lines across entire screen
            for _ in range(random.randint(1, 3)):
                y = random.randint(0, 511)
                pyxel.rect(0, y, 512, 1, random.choice([0, 7]))

Scan()
