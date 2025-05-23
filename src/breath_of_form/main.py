# title: Breath of the Form
# author: Leo Kuroshita
# desc: Shapes pulsate as if breathing in and out.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import math
import random


class BreathOfForm:
    def __init__(self):
        pyxel.init(512, 512, title="Breath of Form")

        # Marimba-style sound definition
        pyxel.sounds[0].set("c3", "t", "7", "f", 30)  # Breathing sound
        pyxel.sounds[1].set("e3", "t", "6", "f", 30)
        pyxel.sounds[2].set("g3", "t", "6", "f", 30)
        pyxel.sounds[3].set("c4", "t", "5", "f", 30)
        pyxel.sounds[4].set("f3", "t", "4", "f", 20)  # Connection sound
        pyxel.sounds[5].set("a3", "t", "3", "f", 15)  # Appearance sound
        pyxel.sounds[6].set("d3", "t", "3", "f", 25)  # Disappearance sound

        # Breathing rhythm
        self.time = 0
        self.breath_cycle = 180

        # Dynamic circle management
        self.max_circles = 24
        self.circles = []
        self.connection_timer = 0
        self.connection_duration = 0
        self.current_connections = []

        # Generate initial circles
        self.spawn_initial_circles()

        pyxel.run(self.update, self.draw)

    def spawn_initial_circles(self):
        """Generate initial circles"""
        for i in range(12):
            self.spawn_circle()

    def spawn_circle(self):
        """Generate a new circle"""
        if len(self.circles) >= self.max_circles:
            return

        # Random position (placed around center)
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(80, 200)
        x = 256 + radius * math.cos(angle)
        y = 256 + radius * math.sin(angle)

        circle = {
            "x": x,
            "y": y,
            "base_size": random.randint(15, 45),
            "phase": random.randint(0, 180),
            "color": 8 + random.randint(0, 6),
            "sound_trigger": random.random() < 0.3,  # 30% chance for sound
            "lifetime": random.randint(300, 900),  # 5-15 seconds lifespan
            "age": 0,
            "birth_time": self.time,
            "sound_id": random.randint(0, 3),
        }

        self.circles.append(circle)

        # Appearance sound
        if random.random() < 0.5:
            pyxel.play(2, 5, loop=False)

    def remove_circle(self, circle):
        """Remove a circle"""
        if circle in self.circles:
            # Disappearance sound
            if random.random() < 0.3:
                pyxel.play(2, 6, loop=False)
            self.circles.remove(circle)

    def generate_random_connections(self):
        """Generate random connection patterns"""
        if len(self.circles) < 2:
            return []

        connections = []
        connection_type = random.randint(0, 5)

        if connection_type == 0:
            # Radial from center
            selected = random.sample(self.circles, min(6, len(self.circles)))
            for circle in selected:
                connections.append(((256, 256), (circle["x"], circle["y"]), 13))

        elif connection_type == 1:
            # Random pair connections
            num_pairs = random.randint(2, min(8, len(self.circles) // 2))
            selected = random.sample(self.circles, num_pairs * 2)
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    c1, c2 = selected[i], selected[i + 1]
                    connections.append(((c1["x"], c1["y"]), (c2["x"], c2["y"]), 11))

        elif connection_type == 2:
            # Connect nearby circles
            for i, c1 in enumerate(self.circles):
                for j, c2 in enumerate(self.circles[i + 1 :], i + 1):
                    dist = math.sqrt(
                        (c1["x"] - c2["x"]) ** 2 + (c1["y"] - c2["y"]) ** 2
                    )
                    if dist < 120 and random.random() < 0.4:
                        connections.append(((c1["x"], c1["y"]), (c2["x"], c2["y"]), 9))

        elif connection_type == 3:
            # Star pattern
            if len(self.circles) >= 5:
                selected = random.sample(self.circles, 5)
                for i in range(5):
                    next_i = (i + 2) % 5
                    c1, c2 = selected[i], selected[next_i]
                    connections.append(((c1["x"], c1["y"]), (c2["x"], c2["y"]), 12))

        elif connection_type == 4:
            # Triangle clusters
            if len(self.circles) >= 3:
                num_triangles = random.randint(1, 3)
                for _ in range(num_triangles):
                    if len(self.circles) >= 3:
                        triangle = random.sample(self.circles, 3)
                        for i in range(3):
                            next_i = (i + 1) % 3
                            c1, c2 = triangle[i], triangle[next_i]
                            connections.append(
                                ((c1["x"], c1["y"]), (c2["x"], c2["y"]), 10)
                            )

        return connections

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Update circles and lifecycle management
        for circle in self.circles[:]:  # Iterate over copy
            circle["age"] += 1

            # Breathing sound trigger
            if circle["sound_trigger"]:
                breath_phase = (self.time + circle["phase"]) % self.breath_cycle
                if breath_phase == 0:
                    pyxel.play(0, circle["sound_id"], loop=False)

            # Lifespan check
            if circle["age"] > circle["lifetime"]:
                self.remove_circle(circle)

        # Generate new circles randomly
        if random.random() < 0.02:  # 2% chance
            self.spawn_circle()

        # Connection management
        self.connection_timer += 1
        if self.connection_timer >= self.connection_duration:
            # New connection pattern
            self.current_connections = self.generate_random_connections()
            self.connection_duration = random.randint(30, 120)  # Random duration
            self.connection_timer = 0

            # Connection sound
            if self.current_connections and random.random() < 0.7:
                pyxel.play(1, 4, loop=False)

        self.time += 1

    def draw(self):
        # Deep blue background
        pyxel.cls(1)

        # Draw circles
        for circle in self.circles:
            # Breathing calculation
            breath_phase = (self.time + circle["phase"]) % self.breath_cycle
            breath_ratio = math.sin(breath_phase * 2 * math.pi / self.breath_cycle)

            # Size change (breathing only)
            size_variation = 1 + 0.5 * breath_ratio
            current_size = max(5, int(circle["base_size"] * size_variation))

            # Position breathing sway
            x_offset = int(3 * math.sin(breath_phase * 0.1))
            y_offset = int(2 * math.cos(breath_phase * 0.07))

            x = int(circle["x"] + x_offset)
            y = int(circle["y"] + y_offset)

            # Age-based transparency effect (color change representation)
            age_ratio = circle["age"] / circle["lifetime"]
            if age_ratio > 0.8:  # Fade after 80% of lifespan
                color = max(1, circle["color"] - 2)
            else:
                color = circle["color"]

            # Draw circle
            pyxel.circb(x, y, current_size, color)

            # Inner dot
            inner_size = max(1, current_size // 3)
            pyxel.circ(x, y, inner_size, color)

        # Draw connection lines
        for connection in self.current_connections:
            start, end, color = connection
            pyxel.line(int(start[0]), int(start[1]), int(end[0]), int(end[1]), color)


BreathOfForm()
