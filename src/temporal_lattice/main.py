"""
Temporal Lattice - Anechoicetry Collection
by Leo Kuroshita
A grid structure that distorts and flows based on temporal rhythms
License: CC BY-SA-NC 4.0
Version: 1.0.0
"""

import pyxel
import math
import random

class GridNode:
    def __init__(self, x, y, row, col):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.phase = random.uniform(0, math.pi * 2)
        self.frequency = random.uniform(0.02, 0.04)
        self.amplitude = random.uniform(10, 20)
        self.time_offset = (row + col) * 0.1
        self.color_phase = random.uniform(0, math.pi * 2)
        self.distortion = 0
        self.pulse = 0
        
    def update(self, global_time, wave_center_x, wave_center_y):
        time = global_time + self.time_offset
        
        wave_dist = math.sqrt((self.base_x - wave_center_x)**2 + (self.base_y - wave_center_y)**2)
        wave_influence = math.sin(wave_dist * 0.02 - global_time * 0.05) * 0.5 + 0.5
        
        dx = math.sin(time * self.frequency + self.phase) * self.amplitude * wave_influence
        dy = math.cos(time * self.frequency * 0.8 + self.phase) * self.amplitude * wave_influence
        
        self.x = self.base_x + dx
        self.y = self.base_y + dy
        
        self.distortion = math.sqrt(dx**2 + dy**2) / self.amplitude
        
        if random.random() < 0.001:
            self.pulse = 1.0
            pyxel.play(0, random.randint(0, 2))
        if self.pulse > 0:
            self.pulse -= 0.02
            
        self.color_phase += 0.01
        
    def get_color(self):
        base_colors = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        color_index = int((math.sin(self.color_phase) * 0.5 + 0.5) * len(base_colors))
        color = base_colors[color_index % len(base_colors)]
        
        if self.pulse > 0:
            color = 7
        elif self.distortion > 0.7:
            color = 13
            
        return color

class TemporalLattice:
    def __init__(self):
        pyxel.init(512, 512, title="Temporal Lattice")
        pyxel.cls(0)
        
        self.grid_size = 16
        self.cell_size = 512 / self.grid_size
        self.nodes = []
        
        for row in range(self.grid_size + 1):
            node_row = []
            for col in range(self.grid_size + 1):
                x = col * self.cell_size
                y = row * self.cell_size
                node = GridNode(x, y, row, col)
                node_row.append(node)
            self.nodes.append(node_row)
            
        self.global_time = 0
        self.wave_center_x = 256
        self.wave_center_y = 256
        self.wave_target_x = 256
        self.wave_target_y = 256
        self.temporal_zones = []
        
        for _ in range(3):
            zone = {
                'x': random.randint(100, 412),
                'y': random.randint(100, 412),
                'radius': random.randint(50, 100),
                'speed_multiplier': random.uniform(0.5, 2.0),
                'phase': random.uniform(0, math.pi * 2)
            }
            self.temporal_zones.append(zone)
            
        self.setup_sound()
        pyxel.run(self.update, self.draw)
        
    def setup_sound(self):
        pyxel.sounds[0].set(
            "f2f2e2",
            "t",
            "7",
            "f",
            12
        )
        
        pyxel.sounds[1].set(
            "c1g1e2",
            "t",
            "7",
            "f",
            15
        )
        
        pyxel.sounds[2].set(
            "a2a2g2",
            "t",
            "7",
            "f",
            10
        )
        
        pyxel.sounds[3].set(
            "d1f1a1d2",
            "s",
            "7",
            "n",
            18
        )
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        self.global_time += 0.1
        
        if random.random() < 0.02:
            self.wave_target_x = random.randint(100, 412)
            self.wave_target_y = random.randint(100, 412)
            
        self.wave_center_x += (self.wave_target_x - self.wave_center_x) * 0.05
        self.wave_center_y += (self.wave_target_y - self.wave_center_y) * 0.05
        
        for zone in self.temporal_zones:
            zone['x'] += math.sin(zone['phase'] + self.global_time * 0.02) * 0.5
            zone['y'] += math.cos(zone['phase'] + self.global_time * 0.02) * 0.5
            
        for row in self.nodes:
            for node in row:
                time_multiplier = 1.0
                
                for zone in self.temporal_zones:
                    dist = math.sqrt((node.base_x - zone['x'])**2 + (node.base_y - zone['y'])**2)
                    if dist < zone['radius']:
                        influence = 1 - (dist / zone['radius'])
                        time_multiplier = time_multiplier * (1 + (zone['speed_multiplier'] - 1) * influence)
                        
                node.update(self.global_time * time_multiplier, self.wave_center_x, self.wave_center_y)
                
        if random.random() < 0.005:
            idx = random.randint(0, len(self.temporal_zones) - 1)
            self.temporal_zones[idx]['speed_multiplier'] = random.uniform(0.5, 2.0)
            pyxel.play(0, random.randint(0, 3))
            
    def draw(self):
        pyxel.cls(0)
        
        for zone in self.temporal_zones:
            steps = 32
            for i in range(steps):
                angle = i * 2 * math.pi / steps
                x = zone['x'] + math.cos(angle) * zone['radius']
                y = zone['y'] + math.sin(angle) * zone['radius']
                color = 1 if zone['speed_multiplier'] < 1 else 5
                pyxel.pset(x, y, color)
                
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                n1 = self.nodes[row][col]
                n2 = self.nodes[row][col + 1]
                n3 = self.nodes[row + 1][col + 1]
                n4 = self.nodes[row + 1][col]
                
                color = n1.get_color()
                
                pyxel.line(n1.x, n1.y, n2.x, n2.y, color)
                pyxel.line(n2.x, n2.y, n3.x, n3.y, color)
                pyxel.line(n3.x, n3.y, n4.x, n4.y, color)
                pyxel.line(n4.x, n4.y, n1.x, n1.y, color)
                
                if n1.distortion > 0.5:
                    center_x = (n1.x + n2.x + n3.x + n4.x) / 4
                    center_y = (n1.y + n2.y + n3.y + n4.y) / 4
                    pyxel.line(n1.x, n1.y, center_x, center_y, color)
                    pyxel.line(n3.x, n3.y, center_x, center_y, color)
                    
        for row in self.nodes:
            for node in row:
                if node.pulse > 0:
                    radius = node.pulse * 10
                    pyxel.circb(node.x, node.y, radius, 7)

TemporalLattice()