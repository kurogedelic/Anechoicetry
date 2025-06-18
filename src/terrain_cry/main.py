"""
Terrain Cry - Anechoicetry Collection
by Leo Kuroshita
Interactive terrain map where cursor movement generates location-based environmental sounds
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random
import math

class TerrainCell:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.color = self.get_terrain_color()
        self.flash_timer = 0
        
    def get_terrain_color(self):
        # Terrain colors based on height (z-value)
        if self.height < 2:
            return 1   # Dark blue (water)
        elif self.height < 4:
            return 3   # Dark green (grass)
        elif self.height < 6:
            return 11  # Light green (rocks)
        else:
            return 7   # White (mountain peaks)
    
    def get_terrain_sound(self):
        # Return sound configuration based on terrain type
        if self.height < 2:
            # Water - bubbling sounds
            return (0, "a3c3a3", "p", "4321", "v", 15)
        elif self.height < 4:
            # Grass - chirping sounds  
            return (1, "c3e3g3", "p", "543", "v", 20)
        elif self.height < 6:
            # Rock - rumbling sounds
            return (2, "g1g1g1", "n", "432", "v", 25)
        else:
            # Mountain - high beeping
            return (3, "b2", "s", "54", "v", 30)
    
    def flash(self):
        self.flash_timer = 10
    
    def update(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1

class TerrainMap:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.cells = []
        self.generate_terrain()
        
    def generate_terrain(self):
        # Simple Perlin-like noise generation
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Create undulating terrain using sine waves with noise
                base_height = (
                    3 * math.sin(x * 0.3) + 
                    2 * math.cos(y * 0.4) + 
                    1.5 * math.sin((x + y) * 0.2) +
                    random.uniform(-1, 1)
                )
                # Normalize to 0-8 range
                height = max(0, min(8, base_height + 4))
                cell = TerrainCell(x, y, height)
                row.append(cell)
            self.cells.append(row)
    
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

class TerrainCry:
    def __init__(self):
        pyxel.init(512, 512, title="Terrain Cry")
        
        # Sound design - terrain-based environmental sounds
        # Water bubbling
        pyxel.sounds[0].set("a3c3a3", "p", "4321", "v", 15)
        # Grass chirping  
        pyxel.sounds[1].set("c3e3g3", "p", "543", "v", 20)
        # Rock rumbling
        pyxel.sounds[2].set("g1g1g1", "n", "432", "v", 25)
        # Mountain beeping
        pyxel.sounds[3].set("b2", "s", "54", "v", 30)
        
        # Terrain map
        self.terrain = TerrainMap(16, 16)
        self.cell_size = 32  # Each terrain cell is 32x32 pixels
        
        # Player cursor
        self.player_x = 8.0
        self.player_y = 8.0
        self.target_x = 8.0
        self.target_y = 8.0
        self.player_blink_timer = 0
        self.move_cooldown = 0
        
        # Auto-pilot mode (starts automatically)
        self.autopilot_mode = True
        self.autopilot_timer = 0
        self.autopilot_interval = 60  # frames between moves
        self.move_speed = 0.1  # smooth movement speed
        
        # Visual effects
        self.screen_flash = 0
        self.last_sound_time = 0
        
        # Sound management
        self.sound_cooldown = 0
        
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update timers
        self.time += 1
        self.player_blink_timer += 1
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
        if self.screen_flash > 0:
            self.screen_flash -= 1
        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1
        
        # Update terrain cells
        for row in self.terrain.cells:
            for cell in row:
                cell.update()
        
        # Check for key input to switch from autopilot to manual
        any_key_pressed = (
            pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or
            pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or
            pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or
            pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or
            pyxel.btn(pyxel.KEY_SPACE)
        )
        
        if any_key_pressed and self.autopilot_mode:
            self.autopilot_mode = False
            # Snap to current grid position when switching to manual
            self.player_x = round(self.player_x)
            self.player_y = round(self.player_y)
            self.target_x = self.player_x
            self.target_y = self.player_y
        
        moved = False
        cell_changed = False
        
        if self.autopilot_mode:
            # Autopilot movement - smooth random walking
            self.autopilot_timer += 1
            
            # Smooth movement towards target
            if abs(self.player_x - self.target_x) > 0.01:
                self.player_x += (self.target_x - self.player_x) * self.move_speed
            else:
                self.player_x = self.target_x
                
            if abs(self.player_y - self.target_y) > 0.01:
                self.player_y += (self.target_y - self.player_y) * self.move_speed
            else:
                self.player_y = self.target_y
            
            # Check if we've moved to a new grid cell
            current_cell_x = int(self.player_x)
            current_cell_y = int(self.player_y)
            if hasattr(self, 'last_cell_x') and hasattr(self, 'last_cell_y'):
                if current_cell_x != self.last_cell_x or current_cell_y != self.last_cell_y:
                    cell_changed = True
            self.last_cell_x = current_cell_x
            self.last_cell_y = current_cell_y
            
            # Choose new target when reached current one
            if (abs(self.player_x - self.target_x) < 0.1 and 
                abs(self.player_y - self.target_y) < 0.1 and 
                self.autopilot_timer >= self.autopilot_interval):
                
                # Pick a new random adjacent target
                possible_moves = []
                current_x = round(self.player_x)
                current_y = round(self.player_y)
                
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                    new_x = current_x + dx
                    new_y = current_y + dy
                    if 0 <= new_x < self.terrain.width and 0 <= new_y < self.terrain.height:
                        possible_moves.append((new_x, new_y))
                
                if possible_moves:
                    self.target_x, self.target_y = random.choice(possible_moves)
                    self.autopilot_timer = 0
                    self.autopilot_interval = random.randint(30, 90)  # Vary walking rhythm
        else:
            # Manual movement
            if self.move_cooldown == 0:
                if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
                    if self.player_x > 0:
                        self.player_x -= 1
                        moved = True
                elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
                    if self.player_x < self.terrain.width - 1:
                        self.player_x += 1
                        moved = True
                elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                    if self.player_y > 0:
                        self.player_y -= 1
                        moved = True
                elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
                    if self.player_y < self.terrain.height - 1:
                        self.player_y += 1
                        moved = True
        
        # If player moved to new cell, trigger terrain sound
        if moved or cell_changed:
            if moved:
                self.move_cooldown = 8  # Prevent too rapid movement in manual mode
            self.trigger_terrain_sound()
    
    def trigger_terrain_sound(self):
        if self.sound_cooldown > 0:
            return
            
        current_cell = self.terrain.get_cell(int(self.player_x), int(self.player_y))
        if current_cell:
            # Get sound configuration for this terrain type
            sound_data = current_cell.get_terrain_sound()
            sound_id = sound_data[0]
            
            # Play the terrain sound
            pyxel.play(0, sound_id, loop=False)
            
            # Visual feedback
            current_cell.flash()
            self.screen_flash = 5
            self.last_sound_time = self.time
            self.sound_cooldown = 15  # Prevent sound spam
    
    def draw(self):
        # Background color with optional screen flash
        bg_color = 0
        if self.screen_flash > 0:
            bg_color = 5 if self.screen_flash % 2 == 0 else 0
        pyxel.cls(bg_color)
        
        # Draw terrain map
        for y in range(self.terrain.height):
            for x in range(self.terrain.width):
                cell = self.terrain.cells[y][x]
                
                # Calculate screen position
                screen_x = x * self.cell_size
                screen_y = y * self.cell_size
                
                # Choose color (flash effect if cell was just activated)
                color = cell.color
                if cell.flash_timer > 0:
                    color = 15 if cell.flash_timer % 4 < 2 else cell.color
                
                # Draw terrain cell
                pyxel.rect(screen_x, screen_y, self.cell_size, self.cell_size, color)
                
                # Draw height indication with small dots
                height_dots = min(int(cell.height), 6)
                for i in range(height_dots):
                    dot_x = screen_x + 4 + (i % 3) * 6
                    dot_y = screen_y + 4 + (i // 3) * 6
                    pyxel.pset(dot_x, dot_y, 0)
        
        # Draw player cursor
        player_screen_x = self.player_x * self.cell_size
        player_screen_y = self.player_y * self.cell_size
        
        # Player blinking effect
        if self.player_blink_timer % 20 < 10:
            # Draw player as a pulsing circle
            center_x = player_screen_x + self.cell_size // 2
            center_y = player_screen_y + self.cell_size // 2
            radius = 6 + 2 * math.sin(self.time * 0.3)
            
            # Draw ripples when sound was recently played
            if self.time - self.last_sound_time < 30:
                ripple_radius = (self.time - self.last_sound_time) * 2
                pyxel.circb(center_x, center_y, ripple_radius, 15)
            
            pyxel.circb(center_x, center_y, int(radius), 15)
            pyxel.circ(center_x, center_y, int(radius - 2), 8)
        
        # Draw terrain info text
        current_cell = self.terrain.get_cell(int(self.player_x), int(self.player_y))
        if current_cell:
            terrain_types = ["Water", "Grass", "Rocky", "Mountain"]
            terrain_idx = min(int(current_cell.height // 2), 3)
            terrain_name = terrain_types[terrain_idx]
            height_text = f"Height: {current_cell.height:.1f}"
            
            # Mode indicator
            mode_text = "Auto-walk" if self.autopilot_mode else "Manual"
            instruction_text = "Press any key to control" if self.autopilot_mode else "Move: WASD/Arrows"
            
            pyxel.text(10, 10, f"Mode: {mode_text}", 15)
            pyxel.text(10, 20, f"Terrain: {terrain_name}", 15)
            pyxel.text(10, 30, height_text, 15)
            pyxel.text(10, 40, instruction_text, 7)
            pyxel.text(10, 50, "Q: Quit", 7)

TerrainCry()