"""
Mars - Anechoicetry Collection
by Leo Kuroshita
Dark Martian landscape with scrolling orange mountains, falling asteroids, and distant blinking stars
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class Mars:
    def __init__(self):
        pyxel.init(512, 512, title="Mars - Anechoicetry")
        
        # Initialize sound design
        self.init_sounds()
        
        # Parallax layers
        self.back_mountains_offset = 0
        self.mid_mountains_offset = 0
        self.front_mountains_offset = 0
        
        self.back_speed = 0.1
        self.mid_speed = 0.2
        self.front_speed = 0.3
        
        # Generate gentle terrain profiles
        self.back_mountains = []
        self.mid_mountains = []
        self.front_mountains = []
        
        # Background mountains - distant, gentle
        for i in range(600):
            height = 350 + 20 * math.sin(i * 0.01) + 10 * math.sin(i * 0.03)
            self.back_mountains.append(512 - height)
            
        # Mid mountains - medium distance
        for i in range(600):
            height = 280 + 35 * math.sin(i * 0.015) + 15 * math.sin(i * 0.04)
            self.mid_mountains.append(512 - height)
            
        # Front mountains - closer, more detail
        for i in range(600):
            height = 200 + 45 * math.sin(i * 0.02) + 20 * math.sin(i * 0.06) + 10 * math.sin(i * 0.12)
            self.front_mountains.append(512 - height)
        
        # Asteroids
        self.asteroids = []
        self.asteroid_timer = 0
        
        # Stars
        self.stars = []
        for _ in range(150):
            self.stars.append({
                'x': random.randint(0, 511),
                'y': random.randint(0, 200),
                'blink_timer': random.randint(0, 120),
                'blink_speed': random.randint(60, 180)
            })
        
        # Frame counter for various effects
        self.frame = 0
        
        pyxel.run(self.update, self.draw)
    
    def init_sounds(self):
        # Sound 0: Asteroid falling (wind/whoosh)
        pyxel.sounds[0].set(
            "c1e1g1c2e2g2c3e3", "p", "7654321", "nfsv", 30
        )
        
        # Sound 1: Explosion impact
        pyxel.sounds[1].set(
            "c1c1c1", "n", "7531", "vvs", 10
        )
        
        # Sound 2: Noise burst
        pyxel.sounds[2].set(
            "c1d1e1f1g1a1b1c2", "n", "7777777", "vvvv", 8
        )
        
        # Sound 3: Ambient wind
        pyxel.sounds[3].set(
            "a0b0c1d1", "p", "3210", "nfsv", 60
        )
        
        # Sound 4: Distant rumble
        pyxel.sounds[4].set(
            "c0d0e0f0", "n", "4321", "svfn", 40
        )
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        self.frame += 1
        
        # Scroll parallax layers
        self.back_mountains_offset -= self.back_speed
        self.mid_mountains_offset -= self.mid_speed
        self.front_mountains_offset -= self.front_speed
        
        if self.back_mountains_offset <= -1:
            self.back_mountains_offset += 1
        if self.mid_mountains_offset <= -1:
            self.mid_mountains_offset += 1
        if self.front_mountains_offset <= -1:
            self.front_mountains_offset += 1
        
        # Update asteroids
        self.asteroid_timer += 1
        if self.asteroid_timer > random.randint(60, 180):
            self.spawn_asteroid()
            self.asteroid_timer = 0
        
        # Update existing asteroids
        for asteroid in self.asteroids[:]:
            asteroid['x'] += asteroid['vx']
            asteroid['y'] += asteroid['vy']
            asteroid['vy'] += 0.1  # Gravity
            asteroid['rotation'] += asteroid['rot_speed']
            
            # Check for ground collision
            mountain_height = self.get_front_mountain_height(asteroid['x'])
            if asteroid['y'] >= mountain_height - 10:
                # Explosion
                self.create_explosion(asteroid['x'], mountain_height)
                self.asteroids.remove(asteroid)
                
                # Play explosion sounds
                if random.random() < 0.7:
                    pyxel.play(0, 1)
                if random.random() < 0.5:
                    pyxel.play(1, 2)
            
            # Remove asteroids that go off screen
            elif asteroid['x'] < -20 or asteroid['x'] > 532 or asteroid['y'] > 520:
                self.asteroids.remove(asteroid)
        
        # Update stars blinking
        for star in self.stars:
            star['blink_timer'] += 1
            if star['blink_timer'] >= star['blink_speed']:
                star['blink_timer'] = 0
                star['blink_speed'] = random.randint(60, 180)
        
        # Ambient sounds
        if random.random() < 0.01:
            pyxel.play(2, 3)
        if random.random() < 0.005:
            pyxel.play(3, 4)
    
    def spawn_asteroid(self):
        asteroid = {
            'x': random.randint(-50, 562),
            'y': random.randint(-100, -20),
            'vx': random.uniform(-1, 1),
            'vy': random.uniform(0.5, 2),
            'size': random.randint(2, 6),
            'rotation': random.uniform(0, 360),
            'rot_speed': random.uniform(-5, 5)
        }
        self.asteroids.append(asteroid)
        
        # Play falling sound occasionally
        if random.random() < 0.3:
            pyxel.play(1, 0)
    
    def create_explosion(self, x, y):
        # Visual explosion particles (could be expanded)
        pass
    
    def get_mountain_height(self, x, mountains, offset):
        # Get mountain height at specific x position
        index = int((x + offset * 200) % len(mountains))
        return mountains[index]
        
    def get_front_mountain_height(self, x):
        return self.get_mountain_height(x, self.front_mountains, self.front_mountains_offset)
    
    def draw(self):
        # Clear screen to darker space
        pyxel.cls(0)  # Black
        
        # Draw deep space gradient
        for y in range(300):
            if y < 100:
                color = 0  # Black
            elif y < 200:
                if random.random() < 0.02:
                    color = 1  # Very dark blue
                else:
                    color = 0
            else:
                if random.random() < 0.01:
                    color = 1
                else:
                    color = 0
            
            if color > 0:
                for x in range(0, 512, 4):
                    pyxel.pset(x + random.randint(0, 3), y, color)
        
        # Draw blinking stars
        for star in self.stars:
            if star['blink_timer'] < star['blink_speed'] * 0.7:
                brightness = random.choice([7, 6, 13])  # White, light gray, light blue
                pyxel.pset(star['x'], star['y'], brightness)
        
        # Draw parallax mountain layers
        self.draw_mountain_layers()
        
        # Draw asteroids
        for asteroid in self.asteroids:
            self.draw_asteroid(asteroid)
    
    def draw_mountain_layers(self):
        # Draw background mountains (darkest, most distant)
        for x in range(512):
            height = self.get_mountain_height(x, self.back_mountains, self.back_mountains_offset)
            for y in range(int(height), 512):
                pyxel.pset(x, y, 1)  # Very dark
        
        # Draw mid mountains (medium tone)
        for x in range(512):
            height = self.get_mountain_height(x, self.mid_mountains, self.mid_mountains_offset)
            for y in range(int(height), 512):
                distance_from_peak = y - height
                if distance_from_peak < 15:
                    color = 2  # Dark red/brown
                else:
                    color = 1  # Very dark
                pyxel.pset(x, y, color)
        
        # Draw front mountains (brightest, most detailed)
        for x in range(512):
            height = self.get_mountain_height(x, self.front_mountains, self.front_mountains_offset)
            for y in range(int(height), 512):
                distance_from_peak = y - height
                if distance_from_peak < 10:
                    color = 4  # Dark orange/red
                elif distance_from_peak < 25:
                    color = 9  # Orange
                elif distance_from_peak < 50:
                    color = 4  # Dark orange/red
                else:
                    color = 2  # Dark red/brown
                pyxel.pset(x, y, color)
    
    def draw_asteroid(self, asteroid):
        x, y = int(asteroid['x']), int(asteroid['y'])
        size = asteroid['size']
        
        # Draw irregular asteroid shape
        for i in range(size):
            for j in range(size):
                if random.random() < 0.7:  # Irregular shape
                    offset_x = int(i - size/2)
                    offset_y = int(j - size/2)
                    
                    # Rotate point
                    angle = math.radians(asteroid['rotation'])
                    rot_x = offset_x * math.cos(angle) - offset_y * math.sin(angle)
                    rot_y = offset_x * math.sin(angle) + offset_y * math.cos(angle)
                    
                    px = x + int(rot_x)
                    py = y + int(rot_y)
                    
                    if 0 <= px < 512 and 0 <= py < 512:
                        color = 6 if random.random() < 0.3 else 5  # Gray variations
                        pyxel.pset(px, py, color)

if __name__ == "__main__":
    Mars()