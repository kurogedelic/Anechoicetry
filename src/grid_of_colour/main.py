# title: Grid of Colour
# author: Leo Kuroshita
# desc: Colorful squares grow from the center auto-generatively.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import math
import random


class GridOfColour:
    def __init__(self):
        pyxel.init(512, 512, title="Grid of Colour")

        # Colorful sound definitions
        pyxel.sounds[0].set("c3", "t", "4", "f", 30)  # Grid generation sound
        pyxel.sounds[1].set("e3", "t", "3", "f", 25)  # Color sound 1
        pyxel.sounds[2].set("g3", "t", "3", "f", 25)  # Color sound 2
        pyxel.sounds[3].set("c4", "t", "2", "f", 20)  # Color sound 3
        pyxel.sounds[4].set("f2", "s", "2", "f", 40)  # Growth sound
        pyxel.sounds[5].set("d2", "t", "1", "f", 60)  # Disappearance sound
        pyxel.sounds[6].set("a3g3e3", "t", "321", "f", 35)  # Chord

        self.time = 0
        self.grid_size = 16  # 16x16 grid
        self.cell_size = 512 // self.grid_size

        # Grid state management
        self.grid = {}  # (x, y): cell_data
        self.center_x = self.grid_size // 2
        self.center_y = self.grid_size // 2

        # Color palette (vibrant colors)
        self.vibrant_colors = [8, 9, 10, 11, 12, 13, 14, 15]

        # Growth parameters
        self.growth_timer = 0
        self.growth_interval = 15  # Frame interval
        self.max_distance = 0

        # Generate initial center cell
        self.spawn_center_cell()

        pyxel.run(self.update, self.draw)

    def spawn_center_cell(self):
        """Generate center cell"""
        cell = {
            "color": random.choice(self.vibrant_colors),
            "age": 0,
            "max_age": random.randint(400, 800),  # Time until fading
            "birth_time": self.time,
            "original_color": None,
            "fade_stage": 0,  # 0:vibrant, 1:medium, 2:dark, 3:black
        }
        cell["original_color"] = cell["color"]
        self.grid[(self.center_x, self.center_y)] = cell

        # Generation sound
        pyxel.play(0, 0, loop=False)

    def get_neighbors(self, x, y):
        """Get coordinates of adjacent cells"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        return neighbors

    def grow_grid(self):
        """Grow the grid"""
        new_cells = []

        # Generate new cells at adjacent positions of existing cells
        for (x, y), cell in list(self.grid.items()):
            if cell["fade_stage"] < 2:  # Only vibrant cells grow
                neighbors = self.get_neighbors(x, y)
                for nx, ny in neighbors:
                    if (nx, ny) not in self.grid and random.random() < 0.3:
                        # Color influence by distance from center
                        distance = math.sqrt(
                            (nx - self.center_x) ** 2 + (ny - self.center_y) ** 2
                        )

                        # Fine-tune color by distance from center
                        if distance < 3:
                            color_pool = self.vibrant_colors
                        elif distance < 6:
                            color_pool = [8, 10, 11, 12, 14]
                        else:
                            color_pool = [8, 10, 12]

                        new_cell = {
                            "color": random.choice(color_pool),
                            "age": 0,
                            "max_age": random.randint(300, 700),
                            "birth_time": self.time,
                            "original_color": None,
                            "fade_stage": 0,
                        }
                        new_cell["original_color"] = new_cell["color"]
                        new_cells.append(((nx, ny), new_cell))

                        # Update distance
                        self.max_distance = max(self.max_distance, distance)

        # Add new cells
        for (x, y), cell in new_cells:
            self.grid[(x, y)] = cell

            # Growth sound (probabilistically)
            if random.random() < 0.1:
                sound_id = random.choice([1, 2, 3])
                pyxel.play(1, sound_id, loop=False)

    def update_cells(self):
        """Update cell age and fading"""
        for (x, y), cell in list(self.grid.items()):
            cell["age"] += 1

            # Calculate fading stage
            age_ratio = cell["age"] / cell["max_age"]

            if age_ratio > 0.8:
                new_stage = 3  # Black
                new_color = 0
            elif age_ratio > 0.6:
                new_stage = 2  # Dark
                new_color = max(1, cell["original_color"] - 6)
            elif age_ratio > 0.3:
                new_stage = 1  # Medium
                new_color = max(2, cell["original_color"] - 3)
            else:
                new_stage = 0  # Vibrant
                new_color = cell["original_color"]

            # Sound when stage changes
            if new_stage > cell["fade_stage"]:
                cell["fade_stage"] = new_stage
                if new_stage == 3:  # When turning black
                    if random.random() < 0.1:
                        pyxel.play(2, 5, loop=False)
                elif new_stage == 2:  # When turning dark
                    if random.random() < 0.05:
                        pyxel.play(3, 6, loop=False)

            cell["color"] = new_color

            # Remove completely black cells
            if cell["age"] > cell["max_age"] * 1.2:
                del self.grid[(x, y)]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Grid growth
        self.growth_timer += 1
        if self.growth_timer >= self.growth_interval:
            self.grow_grid()
            self.growth_timer = 0

            # Growth sound
            if len(self.grid) % 10 == 0 and random.random() < 0.3:
                pyxel.play(0, 4, loop=False)

        # Update cells
        self.update_cells()

        # Restart when grid becomes empty
        if len(self.grid) == 0:
            self.spawn_center_cell()
            self.max_distance = 0

        # Occasional chord
        if self.time % 200 == 0 and len(self.grid) > 20:
            if random.random() < 0.4:
                pyxel.play(1, 6, loop=False)

        self.time += 1

    def draw(self):
        # Deep background
        pyxel.cls(0)

        # Draw grid
        for (x, y), cell in self.grid.items():
            # Cell position and size
            px = x * self.cell_size
            py = y * self.cell_size

            # Slight breathing effect
            age_ratio = min(1.0, cell["age"] / cell["max_age"])
            breath = 1 + 0.05 * math.sin(self.time * 0.05 + x + y)
            size = int(self.cell_size * breath)

            # Draw cell
            pyxel.rect(px, py, size, size, cell["color"])

            # Border (thins as it fades)
            if cell["fade_stage"] < 2:
                border_color = 7
            elif cell["fade_stage"] < 3:
                border_color = 1
            else:
                border_color = 0

            if border_color > 0:
                pyxel.rectb(px, py, self.cell_size, self.cell_size, border_color)

        # Display center point (fine light)
        if len(self.grid) > 0:
            center_px = self.center_x * self.cell_size + self.cell_size // 2
            center_py = self.center_y * self.cell_size + self.cell_size // 2

            # Center pulsation
            pulse = 1 + 0.3 * math.sin(self.time * 0.1)
            pulse_size = int(2 * pulse)

            # Small light point at center
            if self.time % 60 < 30:  # Blinking
                pyxel.circ(center_px, center_py, pulse_size, 7)

        # Growth ripple effect
        if self.growth_timer < 5 and len(self.grid) > 1:
            center_px = self.center_x * self.cell_size + self.cell_size // 2
            center_py = self.center_y * self.cell_size + self.cell_size // 2

            ripple_radius = int(self.max_distance * self.cell_size * 0.8)
            ripple_alpha = 1.0 - (self.growth_timer / 5.0)

            if ripple_alpha > 0:
                # Draw ripple (circumference only)
                for angle in range(0, 360, 10):
                    rad = math.radians(angle)
                    x = center_px + ripple_radius * math.cos(rad)
                    y = center_py + ripple_radius * math.sin(rad)
                    if 0 <= x < 512 and 0 <= y < 512:
                        pyxel.pset(int(x), int(y), 13)


GridOfColour()
