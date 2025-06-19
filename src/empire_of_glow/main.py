"""
The Empire of Glow - Anechoicetry Collection
by Leo Kuroshita
A surreal cityscape where day sky and night buildings coexist impossibly
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random
import math

class Cloud:
    def __init__(self, x, y, size, depth=1.0):
        self.x = x
        self.y = y
        self.size = size
        self.depth = depth  # For parallax effect (1.0 = foreground, 0.5 = background)
        self.base_speed = 0.3 * depth  # Faster speed with parallax
        self.speed_modifier = 1.0
        self.shape = self.generate_cloud_shape()
    
    def generate_cloud_shape(self):
        # Generate very horizontal cloud shape
        shapes = []
        for i in range(random.randint(5, 8)):
            # Much more horizontal spread
            offset_x = random.randint(-self.size * 2, self.size * 2)
            offset_y = random.randint(-self.size//4, self.size//4)
            radius = random.randint(self.size//3, self.size//2)
            shapes.append((offset_x, offset_y, radius))
        return shapes
    
    def update(self, speed_modifier=1.0):
        self.speed_modifier = speed_modifier
        self.x += self.base_speed * self.speed_modifier
        if self.x > 600:  # Wrap around
            self.x = -100
    
    def draw(self):
        # Choose colors based on depth for parallax effect
        if self.depth < 0.7:  # Background clouds
            cloud_color = 13  # Light gray
            shadow_color = 5   # Dark gray
        else:  # Foreground clouds
            cloud_color = 7    # White
            shadow_color = 6   # Gray
            
        for offset_x, offset_y, radius in self.shape:
            center_x = int(self.x + offset_x)
            center_y = int(self.y + offset_y)
            if center_x > -radius and center_x < 512 + radius:
                # Draw shadow with dither pattern (offset down and right)
                shadow_x = center_x + int(3 * self.depth)
                shadow_y = center_y + int(5 * self.depth)
                self.draw_dithered_circle(shadow_x, shadow_y, radius, shadow_color)
                
                # Draw main cloud
                pyxel.circ(center_x, center_y, radius, cloud_color)
    
    def draw_dithered_circle(self, cx, cy, radius, color):
        # Create dithered shadow effect using checkerboard pattern
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if x >= 0 and x < 512 and y >= 0 and y < 512:
                    # Check if point is within circle
                    distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if distance <= radius:
                        # Dither pattern: checkerboard based on coordinates
                        if (x + y) % 2 == 0:
                            pyxel.pset(x, y, color)

class Building:
    def __init__(self, x, base_y, width, height):
        self.x = x
        self.base_y = base_y
        self.width = width
        self.height = height
        self.windows = self.generate_windows()
        
    def generate_windows(self):
        windows = []
        # Generate window positions
        for floor in range(self.height // 8):
            for window_x in range(self.width // 6):
                if random.random() < 0.7:  # 70% chance for window
                    win_x = self.x + 2 + window_x * 6
                    win_y = self.base_y - self.height + 3 + floor * 8
                    flicker_speed = random.uniform(0.02, 0.08)
                    windows.append([win_x, win_y, flicker_speed, random.random()])
        return windows
    
    def update(self, time):
        # Update window flicker
        for window in self.windows:
            window[3] += window[2]  # Update phase
    
    def draw(self):
        # Draw building silhouette
        pyxel.rect(self.x, self.base_y - self.height, self.width, self.height, 1)  # Dark blue
        
        # Draw windows
        for win_x, win_y, flicker_speed, phase in self.windows:
            # Flicker effect
            if math.sin(phase) > 0.3:  # Window is "on"
                brightness = 0.7 + 0.3 * math.sin(phase * 2)
                if brightness > 0.8:
                    pyxel.pset(win_x, win_y, 10)  # Yellow
                    pyxel.pset(win_x+1, win_y, 10)
                    pyxel.pset(win_x, win_y+1, 10)
                    pyxel.pset(win_x+1, win_y+1, 10)

class StreetLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.glow_radius = random.randint(25, 40)
        self.flicker_phase = random.random() * math.pi * 2
        self.flicker_speed = random.uniform(0.03, 0.07)
        self.base_intensity = random.uniform(0.8, 1.0)
        
    def update(self, time):
        self.flicker_phase += self.flicker_speed
    
    def draw(self):
        # Calculate current intensity
        intensity = self.base_intensity + 0.2 * math.sin(self.flicker_phase)
        intensity = max(0.6, min(1.0, intensity))
        
        # Draw glow effect (multiple circles with decreasing intensity)
        for radius in range(self.glow_radius, 0, -3):
            alpha = intensity * (1.0 - radius / self.glow_radius) * 0.3
            if alpha > 0.1:
                color = 10 if alpha > 0.2 else 9  # Yellow or orange
                pyxel.circb(self.x, self.y, radius, color)
        
        # Draw the light source
        if intensity > 0.8:
            pyxel.circ(self.x, self.y, 2, 7)  # White center
        pyxel.pset(self.x, self.y, 10)  # Yellow core

class Tree:
    def __init__(self, x, base_y):
        self.x = x
        self.base_y = base_y
        self.trunk_height = random.randint(15, 25)
        self.crown_radius = random.randint(8, 15)
        self.branch_points = self.generate_branches()
    
    def generate_branches(self):
        branches = []
        # Generate organic branch points
        for i in range(random.randint(15, 25)):
            angle = random.random() * math.pi * 2
            distance = random.random() * self.crown_radius
            branch_x = self.x + distance * math.cos(angle)
            branch_y = self.base_y - self.trunk_height + distance * math.sin(angle)
            branches.append((int(branch_x), int(branch_y)))
        return branches
    
    def draw(self):
        # Draw trunk
        pyxel.rect(self.x-1, self.base_y - self.trunk_height, 3, self.trunk_height, 1)
        
        # Draw organic crown using branch points
        for branch_x, branch_y in self.branch_points:
            pyxel.pset(branch_x, branch_y, 1)  # Dark blue
            # Add some thickness
            if random.random() < 0.5:
                pyxel.pset(branch_x+1, branch_y, 1)
            if random.random() < 0.3:
                pyxel.pset(branch_x, branch_y+1, 1)

class EmpireOfGlow:
    def __init__(self):
        pyxel.init(512, 512, title="The Empire of Glow")
        
        # Sound design - ambient environmental soundscape
        pyxel.sounds[0].set("a1", "n", "2", "n", 120)     # Low ambient drone
        pyxel.sounds[1].set("c2", "n", "1", "n", 30)      # Deeper rumble
        pyxel.sounds[2].set("g3", "p", "1", "v", 10)      # Occasional click
        pyxel.sounds[3].set("a1g1", "n", "21", "n", 60)   # Wind-like noise
        
        # Sky and clouds with parallax layers
        self.sky_color = 12  # Light blue
        self.clouds = []
        
        # Background layer (slower, lighter)
        for i in range(3):
            x = random.randint(-100, 512)
            y = random.randint(30, 120)
            size = random.randint(80, 120)  # Larger background clouds
            depth = random.uniform(0.3, 0.6)  # Background depth
            self.clouds.append(Cloud(x, y, size, depth))
        
        # Foreground layer (faster, brighter)
        for i in range(3):
            x = random.randint(-100, 512)
            y = random.randint(60, 180)
            size = random.randint(60, 100)  # Smaller foreground clouds
            depth = random.uniform(0.8, 1.0)  # Foreground depth
            self.clouds.append(Cloud(x, y, size, depth))
        
        # Buildings (night-time silhouettes) - back to original height
        self.buildings = []
        current_x = 0
        while current_x < 512:
            width = random.randint(40, 80)
            height = random.randint(80, 180)
            base_y = 400 + random.randint(-20, 20)  # Back to original height
            self.buildings.append(Building(current_x, base_y, width, height))
            current_x += width + random.randint(5, 15)
        
        # Street lights - back to original positions
        self.street_lights = []
        for i in range(8):
            x = random.randint(50, 462)
            y = random.randint(320, 380)  # Back to original
            self.street_lights.append(StreetLight(x, y))
        
        # Trees - back to original positions
        self.trees = []
        for i in range(5):
            x = random.randint(30, 482)
            base_y = random.randint(380, 420)  # Back to original
            self.trees.append(Tree(x, base_y))
        
        # Mouse interaction
        self.mouse_influence = 1.0
        
        # Time and ambient sound
        self.time = 0
        self.ambient_timer = 0
        self.click_timer = 0
        
        # Water reflection area - raised to building lower section
        self.water_y = 350  # Higher up to reach building lower parts
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.time += 1
        
        # Mouse influence on cloud speed
        mouse_x = pyxel.mouse_x
        influence = 1.0 + (mouse_x - 256) / 512.0  # -0.5 to 1.5 range
        self.mouse_influence = max(0.1, min(2.0, influence))
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update(self.mouse_influence)
        
        # Update buildings
        for building in self.buildings:
            building.update(self.time)
        
        # Update street lights
        for light in self.street_lights:
            light.update(self.time)
        
        # Ambient sound management
        self.ambient_timer += 1
        if self.ambient_timer % 180 == 0:  # Every 3 seconds
            pyxel.play(0, 0, loop=True)  # Ambient drone
        
        if self.ambient_timer % 240 == 120:  # Offset wind sound
            pyxel.play(1, 3, loop=True)  # Wind noise
        
        # Occasional environmental clicks
        self.click_timer += 1
        if self.click_timer > random.randint(300, 900):  # 5-15 seconds
            pyxel.play(2, 2, loop=False)  # Click sound
            self.click_timer = 0
    
    def draw(self):
        # Clear with day sky color
        pyxel.cls(self.sky_color)
        
        # Draw clouds (day sky) - background to foreground
        sorted_clouds = sorted(self.clouds, key=lambda c: c.depth)
        for cloud in sorted_clouds:
            cloud.draw()
        
        # Draw water reflection area (if enabled)
        if self.water_y < 512:
            pyxel.rect(0, self.water_y, 512, 512 - self.water_y, 1)  # Dark water
            
            # Simple reflection effect for street lights
            for light in self.street_lights:
                if light.y < self.water_y:
                    reflection_y = self.water_y + (self.water_y - light.y)
                    if reflection_y < 512:
                        # Dimmed reflection
                        pyxel.circb(light.x, reflection_y, light.glow_radius//2, 9)
                        pyxel.pset(light.x, reflection_y, 9)
        
        # Draw trees (night silhouettes)
        for tree in self.trees:
            tree.draw()
        
        # Draw buildings (night silhouettes with window lights)
        for building in self.buildings:
            building.draw()
        
        # Draw street lights (night glow)
        for light in self.street_lights:
            light.draw()
        
        # No UI text - clean aesthetic

EmpireOfGlow()