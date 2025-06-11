"""
Sketch Visuals - Anechoicetry Collection
by Leo Kuroshita
A retro game-like grid where synchronized scenes occasionally desync. Tribute to Nam June Paik
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random
import math

class VideoTile:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.scene_type = 'synchronized'
        self.frame = 0
        self.sync_offset = 0
        self.glitch_intensity = 0
        self.color_shift = 0
        self.is_rebel = False  # The tile that goes out of sync
        self.rebel_timer = 0
        self.rebel_scene_type = 'abstract'
        self.last_sync_time = 0
        
    def become_rebel(self):
        """Transform this tile into the rebellious one"""
        self.is_rebel = True
        self.rebel_timer = 0
        rebel_scenes = ['abstract', 'noise', 'geometric', 'organic']
        self.rebel_scene_type = random.choice(rebel_scenes)
        self.glitch_intensity = random.uniform(0.3, 0.8)
    
    def sync_back(self):
        """Return this tile to synchronized state"""
        self.is_rebel = False
        self.rebel_timer = 0
        self.glitch_intensity = 0
        self.color_shift = 0
    
    def update(self, global_frame):
        self.frame += 1
        
        if self.is_rebel:
            self.rebel_timer += 1
            # Rebel behavior - different timing and patterns
            self.color_shift += 0.1
            if random.random() < 0.05:
                self.glitch_intensity = random.uniform(0.2, 1.0)
        else:
            # Synchronized behavior
            self.frame = global_frame + self.sync_offset
            if random.random() < 0.01:
                self.color_shift = random.uniform(0, 0.2)
    
    def draw_synchronized_scene(self):
        """Draw the standard synchronized scene"""
        # Retro game-like patterns
        pattern_type = (self.frame // 30) % 4
        
        if pattern_type == 0:  # Moving blocks
            for i in range(0, self.tile_size, 8):
                for j in range(0, self.tile_size, 8):
                    offset = (self.frame // 4) % 16
                    if (i + j + offset) % 16 < 8:
                        color = 11 + int(self.color_shift * 3)
                        pyxel.rect(self.x + i, self.y + j, 8, 8, color)
        
        elif pattern_type == 1:  # Scrolling lines
            for i in range(self.tile_size):
                wave = int(4 * math.sin((i + self.frame * 0.5) * 0.2))
                pyxel.line(self.x, self.y + i, self.x + self.tile_size, 
                          self.y + i + wave, 6 + int(self.color_shift * 2))
        
        elif pattern_type == 2:  # Circular pattern
            center_x = self.x + self.tile_size // 2
            center_y = self.y + self.tile_size // 2
            radius = (self.frame % 40) + 5
            
            for angle in range(0, 360, 15):
                rad = math.radians(angle)
                x = int(center_x + radius * math.cos(rad))
                y = int(center_y + radius * math.sin(rad))
                if (self.x <= x < self.x + self.tile_size and 
                    self.y <= y < self.y + self.tile_size):
                    pyxel.pset(x, y, 8 + int(self.color_shift * 4))
        
        else:  # Grid pattern
            grid_size = 4
            for i in range(0, self.tile_size, grid_size):
                for j in range(0, self.tile_size, grid_size):
                    if ((i // grid_size) + (j // grid_size) + (self.frame // 8)) % 2:
                        color = 12 + int(self.color_shift * 2)
                        pyxel.rect(self.x + i, self.y + j, grid_size, grid_size, color)
    
    def draw_rebel_scene(self):
        """Draw the rebellious, desynchronized scene"""
        if self.rebel_scene_type == 'abstract':
            # Abstract expressionist-like marks
            for _ in range(int(20 * self.glitch_intensity)):
                x = self.x + random.randint(0, self.tile_size - 1)
                y = self.y + random.randint(0, self.tile_size - 1)
                size = random.randint(1, 4)
                color = random.choice([10, 14, 15, 2, 4])
                pyxel.circ(x, y, size, color)
        
        elif self.rebel_scene_type == 'noise':
            # TV static-like noise
            for _ in range(int(50 * self.glitch_intensity)):
                x = self.x + random.randint(0, self.tile_size - 1)
                y = self.y + random.randint(0, self.tile_size - 1)
                color = random.choice([0, 7, 15])
                pyxel.pset(x, y, color)
        
        elif self.rebel_scene_type == 'geometric':
            # Chaotic geometric forms
            num_shapes = int(5 * self.glitch_intensity)
            for _ in range(num_shapes):
                shape_type = random.choice(['rect', 'line', 'circle'])
                color = random.choice([3, 9, 13, 14])
                
                if shape_type == 'rect':
                    w = random.randint(4, 12)
                    h = random.randint(4, 12)
                    x = self.x + random.randint(0, max(1, self.tile_size - w))
                    y = self.y + random.randint(0, max(1, self.tile_size - h))
                    pyxel.rect(x, y, w, h, color)
                
                elif shape_type == 'line':
                    x1 = self.x + random.randint(0, self.tile_size - 1)
                    y1 = self.y + random.randint(0, self.tile_size - 1)
                    x2 = self.x + random.randint(0, self.tile_size - 1)
                    y2 = self.y + random.randint(0, self.tile_size - 1)
                    pyxel.line(x1, y1, x2, y2, color)
                
                else:  # circle
                    x = self.x + random.randint(5, self.tile_size - 5)
                    y = self.y + random.randint(5, self.tile_size - 5)
                    r = random.randint(2, 8)
                    pyxel.circb(x, y, r, color)
        
        elif self.rebel_scene_type == 'organic':
            # Organic, flowing patterns
            center_x = self.x + self.tile_size // 2
            center_y = self.y + self.tile_size // 2
            
            for i in range(int(30 * self.glitch_intensity)):
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(0, self.tile_size // 2)
                x = int(center_x + distance * math.cos(angle + self.rebel_timer * 0.05))
                y = int(center_y + distance * math.sin(angle + self.rebel_timer * 0.03))
                
                if (self.x <= x < self.x + self.tile_size and 
                    self.y <= y < self.y + self.tile_size):
                    color = int(5 + 4 * math.sin(distance * 0.1 + self.rebel_timer * 0.1))
                    pyxel.pset(x, y, color)
    
    def draw(self):
        # Draw tile border
        pyxel.rectb(self.x, self.y, self.tile_size, self.tile_size, 1)
        
        if self.is_rebel:
            self.draw_rebel_scene()
            
            # Add glitch effects
            if random.random() < self.glitch_intensity * 0.3:
                # Horizontal line glitch
                y = self.y + random.randint(0, self.tile_size - 1)
                pyxel.line(self.x, y, self.x + self.tile_size, y, 
                          random.choice([0, 15, 7]))
            
            if random.random() < self.glitch_intensity * 0.2:
                # Color corruption blocks
                for _ in range(3):
                    x = self.x + random.randint(0, self.tile_size - 4)
                    y = self.y + random.randint(0, self.tile_size - 4)
                    pyxel.rect(x, y, 4, 2, random.randint(0, 15))
        else:
            self.draw_synchronized_scene()

class SketchVisuals:
    def __init__(self):
        pyxel.init(512, 512, title="Sketch Visuals")
        
        # Sound design - video art, electronic, glitchy
        pyxel.sounds[0].set("c2e2g2b2", "p", "7654", "v", 25)    # Synchronized pulse
        pyxel.sounds[1].set("f1", "n", "76543210", "f", 20)      # Video noise
        pyxel.sounds[2].set("g2d3a3", "s", "432", "v", 18)       # Desync alert
        pyxel.sounds[3].set("c1f1a1", "n", "321", "f", 15)       # Glitch burst
        pyxel.sounds[4].set("e2g2b2d3", "t", "5432", "f", 30)    # System hum
        pyxel.sounds[5].set("a1", "n", "7654", "f", 12)          # Static pop
        
        # Create grid of video tiles
        self.tile_size = 64
        self.grid_width = 512 // self.tile_size
        self.grid_height = 512 // self.tile_size
        
        self.tiles = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x = col * self.tile_size
                y = row * self.tile_size
                tile = VideoTile(x, y, self.tile_size)
                tile.sync_offset = random.randint(0, 10)  # Small random sync offset
                self.tiles.append(tile)
        
        # System state
        self.global_frame = 0
        self.current_rebels = []  # Multiple rebel tiles
        self.max_rebels = 5  # Up to 5 rebel tiles at once
        self.rebel_change_timer = 0
        self.rebel_change_interval = 150  # More frequent changes
        self.system_glitch_timer = 0
        self.chaos_mode = False
        self.chaos_timer = 0
        
        # Audio timing
        self.sync_sound_timer = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.global_frame += 1
        
        # Update all tiles
        for tile in self.tiles:
            tile.update(self.global_frame)
        
        # Handle chaos mode
        if self.chaos_mode:
            self.chaos_timer -= 1
            if self.chaos_timer <= 0:
                self.chaos_mode = False
                # Sync back many rebels after chaos
                rebels_to_sync = self.current_rebels[5:]  # Keep first 5, sync the rest
                for rebel in rebels_to_sync:
                    rebel.sync_back()
                self.current_rebels = self.current_rebels[:5]
        
        # Manage rebel tiles
        self.rebel_change_timer += 1
        if self.rebel_change_timer >= self.rebel_change_interval:
            self.change_rebel_tile()
            self.rebel_change_timer = 0
            self.rebel_change_interval = random.randint(100, 250)  # More frequent
        
        # System glitch effects
        self.system_glitch_timer += 1
        if self.system_glitch_timer >= 120 and random.random() < 0.15:  # More frequent glitches
            # Brief system-wide glitch
            for tile in self.tiles:
                if not tile.is_rebel and random.random() < 0.4:  # Higher chance
                    tile.glitch_intensity = random.uniform(0.2, 0.7)  # Stronger glitches
            self.system_glitch_timer = 0
        
        # Audio triggers
        self.sync_sound_timer += 1
        
        # Synchronized pulse
        if self.sync_sound_timer % 120 == 0:
            pyxel.play(0, 0, loop=False)
        
        # System hum
        if self.sync_sound_timer % 180 == 90 and random.random() < 0.6:
            pyxel.play(1, 4, loop=False)
        
        # Desync sounds - more frequent with multiple rebels
        for rebel in self.current_rebels:
            if rebel.rebel_timer % 60 == 30:
                if random.random() < 0.3:
                    pyxel.play(2, 2, loop=False)  # Desync alert
        
        # Glitch sounds - scale with number of rebels
        if self.current_rebels and random.random() < (0.03 + len(self.current_rebels) * 0.01):
            pyxel.play(1, 3, loop=False)  # Glitch burst
        
        # Chaos mode audio
        if self.chaos_mode and random.random() < 0.1:
            pyxel.play(0, 1, loop=False)  # Extra video noise during chaos
        
        # Video noise
        if self.global_frame % 90 == 45 and random.random() < 0.3:
            pyxel.play(0, 1, loop=False)
        
        # Static pops
        if random.random() < 0.02:
            pyxel.play(2, 5, loop=False)
    
    def change_rebel_tile(self):
        """Manage multiple rebellious tiles"""
        # Randomly sync back some rebels
        if self.current_rebels and random.random() < 0.4:
            rebel_to_sync = random.choice(self.current_rebels)
            rebel_to_sync.sync_back()
            self.current_rebels.remove(rebel_to_sync)
        
        # Add new rebels if under max
        if len(self.current_rebels) < self.max_rebels:
            available_tiles = [t for t in self.tiles if not t.is_rebel]
            if available_tiles:
                # Add 1-3 new rebels at once for more chaos
                num_new_rebels = random.randint(1, min(3, self.max_rebels - len(self.current_rebels)))
                for _ in range(num_new_rebels):
                    if available_tiles:
                        new_rebel = random.choice(available_tiles)
                        new_rebel.become_rebel()
                        self.current_rebels.append(new_rebel)
                        available_tiles.remove(new_rebel)
                        
                        # Sound effect for rebellion
                        if random.random() < 0.6:
                            pyxel.play(1, 2, loop=False)
        
        # Chaos mode - occasionally make many tiles rebel
        if random.random() < 0.02:  # 2% chance
            self.chaos_mode = True
            self.chaos_timer = 120  # 4 seconds of chaos
            
            # Make up to 12 tiles rebel during chaos
            available_tiles = [t for t in self.tiles if not t.is_rebel]
            chaos_rebels = min(12, len(available_tiles))
            for _ in range(chaos_rebels):
                if available_tiles:
                    rebel = random.choice(available_tiles)
                    rebel.become_rebel()
                    rebel.glitch_intensity = random.uniform(0.7, 1.0)  # High intensity
                    self.current_rebels.append(rebel)
                    available_tiles.remove(rebel)
    
    def draw(self):
        # Dark background
        pyxel.cls(0)
        
        # Draw all tiles
        for tile in self.tiles:
            tile.draw()
        
        # System-wide effects
        if random.random() < 0.01:
            # Scan line effect
            y = random.randint(0, 511)
            pyxel.line(0, y, 512, y, 1)
        
        # Occasional full-screen interference - scales with rebels
        interference_chance = 0.002 + len(self.current_rebels) * 0.001
        if self.current_rebels and random.random() < interference_chance:
            interference_count = 5 + len(self.current_rebels) * 2
            for _ in range(interference_count):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                w = random.randint(4, 20)
                h = random.randint(1, 3)
                pyxel.rect(x, y, w, h, random.choice([0, 7, 15]))
        
        # Chaos mode visual effects
        if self.chaos_mode:
            # More intense screen effects during chaos
            for _ in range(20):
                if random.random() < 0.3:
                    x = random.randint(0, 511)
                    y = random.randint(0, 511)
                    pyxel.pset(x, y, random.choice([7, 15, 10, 14]))
            
            # Chaos scan lines
            if random.random() < 0.2:
                for _ in range(3):
                    y = random.randint(0, 511)
                    pyxel.line(0, y, 512, y, random.choice([1, 2, 13]))

SketchVisuals()