"""
Numbers in Nummern - Anechoicetry Collection
by Leo Kuroshita
Tribute to Kraftwerk: digital matrix display with evolving number patterns
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 2.0.0
"""

import pyxel
import random
import math

class KraftwerkMatrix:
    def __init__(self):
        pyxel.init(512, 512, title="Numbers in Nummern - Tribute to Kraftwerk")
        
        # Sound design - electronic ambient soundscape
        pyxel.sounds[0].set("c2", "n", "4", "n", 120)     # Deep electronic pulse
        pyxel.sounds[1].set("g3", "n", "2", "n", 60)      # Mid frequency hum
        pyxel.sounds[2].set("c4", "p", "1", "v", 30)      # Digital blips
        pyxel.sounds[3].set("f2", "n", "3", "n", 90)      # Bass drone
        pyxel.sounds[4].set("d4", "t", "1", "n", 15)      # High frequency pulse
        
        # Atari 8x8 bitmap font data
        self.font_data = {
            '0': [0x3C, 0x66, 0x6E, 0x76, 0x66, 0x66, 0x3C, 0x00],
            '1': [0x18, 0x38, 0x18, 0x18, 0x18, 0x18, 0x7E, 0x00],
            '2': [0x3C, 0x66, 0x06, 0x0C, 0x18, 0x30, 0x7E, 0x00],
            '3': [0x3C, 0x66, 0x06, 0x1C, 0x06, 0x66, 0x3C, 0x00],
            '4': [0x0C, 0x1C, 0x2C, 0x4C, 0x7E, 0x0C, 0x0C, 0x00],
            '5': [0x7E, 0x60, 0x7C, 0x06, 0x06, 0x66, 0x3C, 0x00],
            '6': [0x3C, 0x60, 0x60, 0x7C, 0x66, 0x66, 0x3C, 0x00],
            '7': [0x7E, 0x06, 0x0C, 0x18, 0x30, 0x30, 0x30, 0x00],
            '8': [0x3C, 0x66, 0x66, 0x3C, 0x66, 0x66, 0x3C, 0x00],
            '9': [0x3C, 0x66, 0x66, 0x3E, 0x06, 0x0C, 0x78, 0x00],
            ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        }
        
        # Grid system: 64x64 grid (8x8 pixel cells)
        self.grid_size = 64
        self.cell_size = 8
        self.grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.intensity_grid = [[0.0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Animation cycle (360 frames = 12 seconds at 30fps)
        self.cycle_length = 360
        self.frame_counter = 0
        
        # States: 0=noise, 1=numbers, 2=noise (removed sequence state)
        self.current_state = 0
        
        # Big number overlay system with enhanced transitions
        self.big_number_active = False
        self.big_number_char = '0'
        self.big_number_timer = 0
        self.big_number_duration = 0
        self.transition_active = False
        self.transition_timer = 0
        self.transition_phase = 0  # 0=mask_in, 1=display, 2=mask_out
        self.mask_in_duration = 60   # 2 seconds to mask in
        self.display_duration = 60   # 2 seconds display
        self.mask_out_duration = 60  # 2 seconds to mask out
        self.big_number_mask = []  # Which cells are part of big number
        self.next_big_number_time = random.randint(180, 480)  # 6-16 seconds
        
        # Green grayscale colors (16 levels)
        self.green_colors = [0, 1, 1, 1, 3, 3, 3, 11, 11, 11, 11, 11, 7, 7, 7, 7]
        
        # Sound timing
        self.sound_timer = 0
        self.last_pulse = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.frame_counter += 1
        self.sound_timer += 1
        
        # Determine current state based on cycle
        cycle_pos = self.frame_counter % self.cycle_length
        if cycle_pos < 120:  # 0-119: noise
            self.current_state = 0
        elif cycle_pos < 240:  # 120-239: numbers
            self.current_state = 1
        else:  # 240-359: noise
            self.current_state = 2
        
        # Update grid content based on state
        self.update_grid_content()
        
        # Manage big number overlay
        self.manage_big_number()
        
        # Sound management
        self.manage_sound()
    
    def update_grid_content(self):
        # Skip updates during display phase only
        if self.transition_active and self.transition_phase == 1:
            return
            
        if self.current_state == 0 or self.current_state == 2:  # Noise states
            # Random noise with numbers and spaces (2x density)
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if random.random() < 0.6:  # 60% chance to change (2x density)
                        if random.random() < 0.85:  # 85% numbers, 15% spaces
                            self.grid[y][x] = str(random.randint(0, 9))
                            self.intensity_grid[y][x] = random.uniform(0.1, 1.0)
                        else:
                            self.grid[y][x] = ' '
                            self.intensity_grid[y][x] = 0.0
        
        elif self.current_state == 1:  # Numbers state
            # More numbers, higher intensity (2x density)
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if random.random() < 0.8:  # 80% chance to change (2x density)
                        if random.random() < 0.95:  # 95% numbers, 5% spaces
                            self.grid[y][x] = str(random.randint(0, 9))
                            self.intensity_grid[y][x] = random.uniform(0.2, 1.0)
                        else:
                            self.grid[y][x] = ' '
                            self.intensity_grid[y][x] = 0.0
    
    def manage_big_number(self):
        # Check if it's time to trigger a big number transition
        if not self.big_number_active and not self.transition_active and self.frame_counter >= self.next_big_number_time:
            self.transition_active = True
            self.transition_timer = 0
            self.transition_phase = 0  # Start with mask in
            self.big_number_char = str(random.randint(0, 9))
            self.create_big_number_mask()
            
            # Fill grid completely with numbers for transition start
            self.fill_grid_with_numbers()
            
            # Play special sound for big number
            pyxel.play(3, 4, loop=False)
        
        # Update transition phases
        if self.transition_active:
            self.transition_timer += 1
            
            if self.transition_phase == 0:  # Mask in phase
                if self.transition_timer >= self.mask_in_duration:
                    self.transition_phase = 1
                    self.transition_timer = 0
                    
            elif self.transition_phase == 1:  # Display phase
                if self.transition_timer >= self.display_duration:
                    self.transition_phase = 2
                    self.transition_timer = 0
                    
            elif self.transition_phase == 2:  # Mask out phase
                if self.transition_timer >= self.mask_out_duration:
                    self.transition_active = False
                    self.transition_phase = 0
                    # Schedule next big number
                    self.next_big_number_time = self.frame_counter + random.randint(180, 480)
    
    def create_big_number_mask(self):
        # Create mask showing which cells are part of the big number
        self.big_number_mask = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        if self.big_number_char not in self.font_data:
            return
        
        bitmap = self.font_data[self.big_number_char]
        cells_per_bit = 8
        total_width = 8 * cells_per_bit
        total_height = 8 * cells_per_bit
        
        start_x = (self.grid_size - total_width) // 2
        start_y = (self.grid_size - total_height) // 2
        
        # Mark cells that are part of the big number
        for row in range(8):
            byte_data = bitmap[row]
            for col in range(8):
                if byte_data & (0x80 >> col):
                    for dy in range(cells_per_bit):
                        for dx in range(cells_per_bit):
                            grid_x = start_x + col * cells_per_bit + dx
                            grid_y = start_y + row * cells_per_bit + dy
                            
                            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                                self.big_number_mask[grid_y][grid_x] = True
    
    def fill_grid_with_numbers(self):
        # Fill entire grid with random numbers for transition start
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = str(random.randint(0, 9))
                self.intensity_grid[y][x] = random.uniform(0.5, 1.0)
    
    # Removed old create_transition_pixels - now using mask-based system
    
    def manage_sound(self):
        # Electronic ambient soundscape
        if self.sound_timer % 90 == 0:  # Every 3 seconds
            pyxel.play(0, 0, loop=True)  # Deep pulse
        
        if self.sound_timer % 60 == 30:  # Offset mid frequency
            pyxel.play(1, 1, loop=True)  # Mid hum
        
        if self.sound_timer % 120 == 60:  # Bass drone
            pyxel.play(2, 3, loop=True)
        
        # Digital blips based on state changes
        current_pulse = self.frame_counter // 30
        if current_pulse != self.last_pulse and self.current_state in [1, 3]:
            pyxel.play(3, 2, loop=False)  # Digital blip
            self.last_pulse = current_pulse
        
        # High frequency pulse during sequence state
        if self.current_state == 3 and self.sound_timer % 20 == 0:
            pyxel.play(3, 4, loop=False)
    
    def draw_character(self, char, grid_x, grid_y, intensity):
        if char not in self.font_data:
            return
        
        bitmap = self.font_data[char]
        
        # Calculate screen position
        screen_x = grid_x * self.cell_size
        screen_y = grid_y * self.cell_size
        
        # Choose color based on intensity
        color_index = int(intensity * 15)
        color = self.green_colors[color_index]
        
        # Draw 8x8 bitmap
        for row in range(8):
            byte_data = bitmap[row]
            for col in range(8):
                if byte_data & (0x80 >> col):  # Check if bit is set
                    pixel_x = screen_x + col
                    pixel_y = screen_y + row
                    if 0 <= pixel_x < 512 and 0 <= pixel_y < 512:
                        pyxel.pset(pixel_x, pixel_y, color)
    
    # Removed old draw_big_character - now using mask-based transition system
    
    def draw(self):
        # Clear screen with black
        pyxel.cls(0)
        
        # Draw grid content or transition effect
        if self.transition_active:
            self.draw_transition()
        else:
            # Normal grid drawing
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    char = self.grid[y][x]
                    intensity = self.intensity_grid[y][x]
                    if char != ' ' and intensity > 0:
                        self.draw_character(char, x, y, intensity)
    
    def draw_transition(self):
        # Handle different transition phases
        if self.transition_phase == 0:  # Mask in: fade out non-mask areas
            fade_progress = self.transition_timer / self.mask_in_duration
            
            # Update numbers continuously during mask in phase
            if random.random() < 0.6:  # 60% chance to update some cells
                for _ in range(random.randint(5, 15)):  # Update 5-15 random cells
                    x = random.randint(0, self.grid_size - 1)
                    y = random.randint(0, self.grid_size - 1)
                    if random.random() < 0.85:
                        self.grid[y][x] = str(random.randint(0, 9))
                        self.intensity_grid[y][x] = random.uniform(0.1, 1.0)
                    else:
                        self.grid[y][x] = ' '
                        self.intensity_grid[y][x] = 0.0
            
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    char = self.grid[y][x]
                    if char != ' ':
                        if self.big_number_mask[y][x]:
                            # Keep mask area visible
                            intensity = self.intensity_grid[y][x]
                        else:
                            # Fade out non-mask areas with random timing
                            cell_fade_delay = (x + y * self.grid_size) % 30  # Faster stagger fade
                            if self.transition_timer > cell_fade_delay:
                                fade_amount = min(1.0, (self.transition_timer - cell_fade_delay) / 30)
                                intensity = self.intensity_grid[y][x] * (1.0 - fade_amount)
                            else:
                                intensity = self.intensity_grid[y][x]
                        
                        if intensity > 0.05:
                            self.draw_character(char, x, y, intensity)
                            
        elif self.transition_phase == 1:  # Display: show only mask area
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if self.big_number_mask[y][x]:
                        char = self.grid[y][x]
                        if char != ' ':
                            # Add slight flickering to big number
                            base_intensity = self.intensity_grid[y][x]
                            flicker = 0.9 + 0.1 * math.sin(self.transition_timer * 0.1 + x * 0.1 + y * 0.1)
                            intensity = base_intensity * flicker
                            self.draw_character(char, x, y, intensity)
                            
        elif self.transition_phase == 2:  # Mask out: fade in background around mask
            fade_progress = self.transition_timer / self.mask_out_duration
            
            # Update background numbers continuously during mask out
            if random.random() < 0.4:  # 40% chance to update some cells
                for _ in range(random.randint(3, 10)):  # Update 3-10 random cells
                    x = random.randint(0, self.grid_size - 1)
                    y = random.randint(0, self.grid_size - 1)
                    if not self.big_number_mask[y][x]:  # Only update non-mask areas
                        if random.random() < 0.85:
                            self.grid[y][x] = str(random.randint(0, 9))
                            self.intensity_grid[y][x] = random.uniform(0.3, 1.0)
                        else:
                            self.grid[y][x] = ' '
                            self.intensity_grid[y][x] = 0.0
            
            # Draw the big number (fading out)
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if self.big_number_mask[y][x]:
                        char = self.grid[y][x]
                        if char != ' ':
                            intensity = self.intensity_grid[y][x] * (1.0 - fade_progress)
                            if intensity > 0.05:
                                self.draw_character(char, x, y, intensity)
            
            # Draw background numbers (fading in)
            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    if not self.big_number_mask[y][x]:
                        char = self.grid[y][x]
                        if char != ' ':
                            # Fade in with staggered timing
                            cell_appear_delay = ((x * 7 + y * 11) % 40)  # Faster random stagger
                            if self.transition_timer > cell_appear_delay:
                                appear_amount = min(1.0, (self.transition_timer - cell_appear_delay) / 20)
                                intensity = self.intensity_grid[y][x] * appear_amount
                                if intensity > 0.05:
                                    self.draw_character(char, x, y, intensity)

KraftwerkMatrix()