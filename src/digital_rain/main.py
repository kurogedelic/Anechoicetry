"""
Digital Rain - Anechoicetry Collection
by Leo Kuroshita
Matrix-style falling digital characters with glitch aesthetics and poetic fragments
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import random
import string

class DigitalColumn:
    def __init__(self, x):
        self.x = x
        self.drops = []
        self.spawn_timer = random.randint(0, 60)
        self.speed = random.uniform(1, 3)
        self.glitch_timer = 0
        
    def update(self):
        # Spawn new drops
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_drop()
            self.spawn_timer = random.randint(20, 100)
        
        # Update existing drops
        for drop in self.drops[:]:
            drop.update()
            if drop.y > 520:
                self.drops.remove(drop)
        
        # Update glitch state
        self.glitch_timer = max(0, self.glitch_timer - 1)
    
    def spawn_drop(self):
        char = self.get_random_char()
        drop = DigitalDrop(self.x, -10, char, self.speed)
        self.drops.append(drop)
    
    def get_random_char(self):
        # Mix of different character types
        char_types = [
            string.ascii_uppercase,     # A-Z
            string.digits,              # 0-9
            "!@#$%^&*()_+-=[]{}|;:,.<>?",  # Symbols
            "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ",  # Katakana-like
        ]
        char_set = random.choice(char_types)
        return random.choice(char_set)
    
    def trigger_glitch(self):
        self.glitch_timer = random.randint(10, 30)
        # Change some existing drops
        for drop in self.drops:
            if random.random() < 0.3:
                drop.glitch()
    
    def draw(self):
        for drop in self.drops:
            drop.draw()

class DigitalDrop:
    def __init__(self, x, y, char, speed):
        self.x = x
        self.y = y
        self.char = char
        self.speed = speed
        self.age = 0
        self.max_age = random.randint(180, 360)
        self.color = 11  # Green
        self.brightness = 1.0
        self.glitch_timer = 0
        
    def update(self):
        self.y += self.speed
        self.age += 1
        
        # Fade with age
        age_ratio = self.age / self.max_age
        self.brightness = max(0.2, 1.0 - age_ratio * 0.8)
        
        # Occasional character change
        if random.random() < 0.02:
            self.char = self.get_new_char()
        
        # Update glitch
        if self.glitch_timer > 0:
            self.glitch_timer -= 1
            if random.random() < 0.5:
                self.char = self.get_new_char()
    
    def get_new_char(self):
        chars = string.ascii_uppercase + string.digits + "!@#$%^&*"
        return random.choice(chars)
    
    def glitch(self):
        self.glitch_timer = random.randint(5, 15)
        self.char = self.get_new_char()
    
    def draw(self):
        if self.glitch_timer > 0:
            # Glitch colors
            color = random.choice([7, 10, 12, 14])  # White, yellow, light blue, pink
        else:
            # Normal green with brightness
            if self.brightness > 0.7:
                color = 11  # Bright green
            elif self.brightness > 0.4:
                color = 3   # Dark green
            else:
                color = 1   # Very dark
        
        # Draw character
        if 0 <= self.x < 512 and 0 <= self.y < 512:
            pyxel.text(int(self.x), int(self.y), self.char, color)

class PoeticFragment:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.fragments = [
            "silence echoes",
            "digital dreams",
            "code whispers",
            "electric rain",
            "binary poetry",
            "cyber haiku",
            "algorithm tears",
            "virtual memory",
            "pixel ghosts",
            "data streams"
        ]
        self.text = random.choice(self.fragments)
        self.chars_revealed = 0
        self.reveal_timer = 0
        self.life = 300
        self.fade_start = 200
        
    def update(self):
        self.life -= 1
        self.reveal_timer += 1
        
        # Reveal characters gradually
        if self.reveal_timer >= 15 and self.chars_revealed < len(self.text):
            self.chars_revealed += 1
            self.reveal_timer = 0
        
        return self.life > 0
    
    def draw(self):
        if self.life <= 0:
            return
            
        # Calculate alpha based on life
        if self.life > self.fade_start:
            alpha = 1.0
        else:
            alpha = self.life / self.fade_start
        
        # Choose color based on alpha
        if alpha > 0.7:
            color = 7  # White
        elif alpha > 0.4:
            color = 6  # Light gray
        else:
            color = 5  # Dark gray
        
        # Draw revealed portion of text
        revealed_text = self.text[:self.chars_revealed]
        if revealed_text:
            pyxel.text(int(self.x), int(self.y), revealed_text, color)

class DigitalRain:
    def __init__(self):
        pyxel.init(512, 512, title="Digital Rain")
        
        # Sound design - digital/electronic theme
        pyxel.sounds[0].set("c1e1g1", "n", "765", "f", 25)    # Digital static
        pyxel.sounds[1].set("g2", "n", "7654321", "v", 15)    # Electronic droplet
        pyxel.sounds[2].set("c2e2", "p", "543", "f", 20)      # Binary rhythm
        pyxel.sounds[3].set("f3a3", "s", "321", "v", 18)      # Glitch sound
        pyxel.sounds[4].set("d2f2a2", "t", "432", "f", 22)    # Data flow
        pyxel.sounds[5].set("b1d2", "n", "654", "f", 12)      # Soft static
        
        # Initialize columns
        self.columns = []
        column_width = 8
        for x in range(0, 512, column_width):
            self.columns.append(DigitalColumn(x))
        
        # Poetic fragments
        self.fragments = []
        self.fragment_timer = 0
        
        # Global effects
        self.glitch_wave_timer = 0
        self.background_pulse = 0
        self.time = 0
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Update all columns
        for column in self.columns:
            column.update()
        
        # Update fragments
        self.fragments = [f for f in self.fragments if f.update()]
        
        # Spawn new poetic fragments occasionally
        self.fragment_timer += 1
        if self.fragment_timer >= 400 and random.random() < 0.3:
            x = random.randint(50, 400)
            y = random.randint(100, 300)
            self.fragments.append(PoeticFragment(x, y))
            self.fragment_timer = 0
        
        # Global glitch waves
        self.glitch_wave_timer += 1
        if self.glitch_wave_timer >= 300:
            if random.random() < 0.4:
                self.trigger_glitch_wave()
            self.glitch_wave_timer = 0
        
        # Background effects
        self.background_pulse += 0.05
        
        # Sound triggers
        if self.time % 120 == 0 and random.random() < 0.6:
            pyxel.play(0, 0, loop=False)  # Digital static
        
        if self.time % 45 == 0 and random.random() < 0.4:
            pyxel.play(1, 1, loop=False)  # Electronic droplet
        
        if self.time % 180 == 60 and random.random() < 0.3:
            pyxel.play(2, 2, loop=False)  # Binary rhythm
        
        # Data flow ambient
        if self.time % 200 == 100 and random.random() < 0.5:
            pyxel.play(1, 4, loop=False)
        
        # Soft static background
        if self.time % 90 == 30 and random.random() < 0.25:
            pyxel.play(2, 5, loop=False)
        
        self.time += 1
    
    def trigger_glitch_wave(self):
        # Trigger glitch across multiple columns
        affected_columns = random.sample(self.columns, random.randint(3, 8))
        for column in affected_columns:
            column.trigger_glitch()
        
        # Glitch sound
        pyxel.play(0, 3, loop=False)
    
    def draw(self):
        # Black background with subtle pulse
        bg_color = 0
        if int(self.background_pulse * 10) % 100 == 0:
            bg_color = 1  # Very subtle dark green flash
        
        pyxel.cls(bg_color)
        
        # Draw all columns
        for column in self.columns:
            column.draw()
        
        # Draw poetic fragments
        for fragment in self.fragments:
            fragment.draw()
        
        # Occasional screen-wide glitch lines
        if random.random() < 0.01:
            y = random.randint(0, 512)
            color = random.choice([7, 10, 12])
            for x in range(0, 512, 8):
                if random.random() < 0.3:
                    char = random.choice("01#*@")
                    pyxel.text(x, y, char, color)

DigitalRain()