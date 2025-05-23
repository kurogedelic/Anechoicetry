# title: The Quiet Point and the Line
# author: Leo Kuroshita
# desc: Points slowly draw lines and eventually disappear.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import math
import random


class QuietPointAndLine:
    def __init__(self):
        pyxel.init(512, 512, title="The Quiet Point and the Line")

        # Klee-style sound definitions (with variations)
        pyxel.sounds[0].set("c2", "t", "2", "f", 60)  # Point movement sound
        pyxel.sounds[1].set("g2", "t", "1", "f", 40)  # Line drawing sound
        pyxel.sounds[2].set("e2", "t", "3", "f", 80)  # Completion sound
        pyxel.sounds[3].set("f2", "s", "2", "v", 45)  # Static point sound (vibrato)
        pyxel.sounds[4].set(
            "a2", "t", "1", "s", 30
        )  # Large form appearance sound (slide)
        pyxel.sounds[5].set("d3", "p", "2", "f", 35)  # Disappearance sound (pulse wave)
        pyxel.sounds[6].set("b1", "n", "1", "f", 25)  # Noise sound
        pyxel.sounds[7].set("e3c3g2", "t", "321", "f", 50)  # Chord
        pyxel.sounds[8].set("c3e3g3c4", "t", "4321", "f", 60)  # Arpeggio
        pyxel.sounds[9].set("f2g2a2", "s", "234", "s", 40)  # Ascending sound

        self.time = 0
        self.drawing_points = []
        self.completed_lines = []
        self.max_lines = 20  # Increase lines
        self.static_points = []  # Static points
        self.large_shapes = []  # Large forms

        # Generate initial points and elements
        self.spawn_initial_points()

        pyxel.run(self.update, self.draw)

    def spawn_initial_points(self):
        """Generate initial drawing points and elements"""
        for _ in range(8):  # Increase drawing points
            self.spawn_drawing_point()

        for _ in range(15):  # Add static points
            self.spawn_static_point()

        for _ in range(4):  # Add large forms
            self.spawn_large_shape()

    def spawn_drawing_point(self):
        """Generate a new drawing point"""
        if len(self.drawing_points) >= 12:  # Increase number
            return

        # Random starting point
        start_x = random.randint(30, 482)
        start_y = random.randint(30, 482)

        # Larger strokes
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(120, 350)  # Longer lines
        end_x = start_x + distance * math.cos(angle)
        end_y = start_y + distance * math.sin(angle)

        # Keep within screen bounds
        end_x = max(20, min(492, end_x))
        end_y = max(20, min(492, end_y))

        point = {
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "current_x": start_x,
            "current_y": start_y,
            "progress": 0.0,
            "speed": random.uniform(0.003, 0.008),  # Slow
            "color": random.choice([8, 10, 11, 12, 14]),
            "thickness": random.randint(1, 4),  # Thicker lines
            "birth_time": self.time,
            "path": [(start_x, start_y)],  # Record trajectory
            "last_sound": 0,
            "sound_interval": random.randint(30, 90),
        }

        self.drawing_points.append(point)

        # Starting sound (variation)
        if random.random() < 0.4:
            sound_choice = random.choice(
                [0, 4, 9]
            )  # Movement, appearance, ascending sound
            pyxel.play(0, sound_choice, loop=False)

    def spawn_static_point(self):
        """Generate static points"""
        point = {
            "x": random.randint(20, 492),
            "y": random.randint(20, 492),
            "size": random.randint(2, 8),
            "color": random.choice([7, 9, 13, 15]),
            "pulse_phase": random.uniform(0, 2 * math.pi),
            "lifetime": random.randint(400, 800),
            "sound_timer": random.randint(0, 200),
            "sound_interval": random.randint(150, 300),
        }
        self.static_points.append(point)

    def spawn_large_shape(self):
        """Generate large forms"""
        shape_type = random.choice(["circle", "rect", "triangle"])

        shape = {
            "type": shape_type,
            "x": random.randint(100, 412),
            "y": random.randint(100, 412),
            "size": random.randint(40, 120),
            "color": random.choice([6, 8, 10, 12]),
            "rotation": 0,
            "rotation_speed": random.uniform(-0.02, 0.02),
            "breath_phase": random.uniform(0, 2 * math.pi),
            "lifetime": random.randint(600, 1200),
            "sound_timer": random.randint(0, 100),
            "sound_interval": random.randint(200, 400),
        }
        self.large_shapes.append(shape)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Update drawing points
        for point in self.drawing_points[:]:
            if point["progress"] < 1.0:
                # Progress
                point["progress"] += point["speed"]

                # Curved movement (Bezier-like)
                t = point["progress"]
                # Easing function for natural movement
                eased_t = t * t * (3.0 - 2.0 * t)

                # Add intermediate control point for curves
                mid_x = (point["start_x"] + point["end_x"]) / 2 + random.uniform(
                    -20, 20
                )
                mid_y = (point["start_y"] + point["end_y"]) / 2 + random.uniform(
                    -20, 20
                )

                # Quadratic Bezier curve
                point["current_x"] = (
                    (1 - eased_t) ** 2 * point["start_x"]
                    + 2 * (1 - eased_t) * eased_t * mid_x
                    + eased_t**2 * point["end_x"]
                )
                point["current_y"] = (
                    (1 - eased_t) ** 2 * point["start_y"]
                    + 2 * (1 - eased_t) * eased_t * mid_y
                    + eased_t**2 * point["end_y"]
                )

                # Add to trajectory
                point["path"].append((int(point["current_x"]), int(point["current_y"])))

                # Drawing sound (variation)
                if self.time - point["last_sound"] > point["sound_interval"]:
                    if random.random() < 0.3:
                        sound_choice = random.choice(
                            [1, 6, 7]
                        )  # Drawing sound, noise, chord
                        pyxel.play(1, sound_choice, loop=False)
                    point["last_sound"] = self.time
                    point["sound_interval"] = random.randint(40, 120)

            else:
                # Line completion
                completed_line = {
                    "path": point["path"],
                    "color": point["color"],
                    "thickness": point["thickness"],
                    "fade_time": 0,
                    "max_fade": random.randint(300, 600),  # 5-10 seconds to disappear
                }

                self.completed_lines.append(completed_line)
                self.drawing_points.remove(point)

                # Completion sound (variation)
                if random.random() < 0.6:
                    sound_choice = random.choice([2, 8])  # Completion sound, arpeggio
                    pyxel.play(2, sound_choice, loop=False)

        # Update completed lines
        for line in self.completed_lines[:]:
            line["fade_time"] += 1
            if line["fade_time"] > line["max_fade"]:
                self.completed_lines.remove(line)

        # Update static points
        for point in self.static_points[:]:
            point["lifetime"] -= 1
            point["sound_timer"] += 1

            # Static point sound
            if point["sound_timer"] >= point["sound_interval"]:
                if random.random() < 0.1:
                    pyxel.play(3, 3, loop=False)  # Vibrato sound
                point["sound_timer"] = 0
                point["sound_interval"] = random.randint(150, 300)

            if point["lifetime"] <= 0:
                # Disappearance sound
                if random.random() < 0.3:
                    pyxel.play(2, 5, loop=False)
                self.static_points.remove(point)

        # Update large forms
        for shape in self.large_shapes[:]:
            shape["rotation"] += shape["rotation_speed"]
            shape["breath_phase"] += 0.02
            shape["lifetime"] -= 1
            shape["sound_timer"] += 1

            # Large form sound
            if shape["sound_timer"] >= shape["sound_interval"]:
                if random.random() < 0.08:
                    sound_choice = random.choice([4, 7])  # Slide, chord
                    pyxel.play(1, sound_choice, loop=False)
                shape["sound_timer"] = 0
                shape["sound_interval"] = random.randint(200, 400)

            if shape["lifetime"] <= 0:
                # Large form disappearance sound
                if random.random() < 0.4:
                    pyxel.play(0, 5, loop=False)
                self.large_shapes.remove(shape)

        # Remove old lines (max number limit)
        if len(self.completed_lines) > self.max_lines:
            self.completed_lines.pop(0)

        # Generate new elements randomly
        if random.random() < 0.015:  # Drawing points
            self.spawn_drawing_point()

        if random.random() < 0.01:  # Static points
            self.spawn_static_point()

        if random.random() < 0.003:  # Large forms
            self.spawn_large_shape()

        self.time += 1

    def draw(self):
        # Warm background color
        pyxel.cls(0)

        # Draw completed lines (with fade effect)
        for line in self.completed_lines:
            fade_ratio = 1.0 - (line["fade_time"] / line["max_fade"])

            # Fade effect as color thinning
            if fade_ratio > 0.7:
                color = line["color"]
            elif fade_ratio > 0.4:
                color = max(1, line["color"] - 1)
            elif fade_ratio > 0.2:
                color = max(1, line["color"] - 2)
            else:
                color = 1

            # Draw lines
            path = line["path"]
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                pyxel.line(x1, y1, x2, y2, color)

                # Thick line simulation
                for offset in range(line["thickness"]):
                    pyxel.line(x1 + offset, y1, x2 + offset, y2, color)
                    if offset > 0:
                        pyxel.line(x1, y1 + offset, x2, y2 + offset, color)

        # Currently drawing lines
        for point in self.drawing_points:
            path = point["path"]
            color = point["color"]

            # Progressive trajectory
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                pyxel.line(x1, y1, x2, y2, color)

                for offset in range(point["thickness"]):
                    pyxel.line(x1 + offset, y1, x2 + offset, y2, color)
                    if offset > 0:
                        pyxel.line(x1, y1 + offset, x2, y2 + offset, color)

            # Current point (slightly pulsating)
            pulse = 1 + 0.3 * math.sin(self.time * 0.1)
            point_size = int(3 * pulse)  # Larger
            pyxel.circ(
                int(point["current_x"]),
                int(point["current_y"]),
                point_size,
                point["color"],
            )

        # Draw static points
        for point in self.static_points:
            pulse = 1 + 0.2 * math.sin(self.time * 0.05 + point["pulse_phase"])
            size = int(point["size"] * pulse)
            pyxel.circ(point["x"], point["y"], size, point["color"])

        # Draw large forms
        for shape in self.large_shapes:
            breath = 1 + 0.15 * math.sin(shape["breath_phase"])
            size = int(shape["size"] * breath)

            if shape["type"] == "circle":
                pyxel.circb(shape["x"], shape["y"], size, shape["color"])
            elif shape["type"] == "rect":
                half_size = size // 2
                pyxel.rectb(
                    shape["x"] - half_size,
                    shape["y"] - half_size,
                    size,
                    size,
                    shape["color"],
                )
            elif shape["type"] == "triangle":
                # Simple triangle
                points = [
                    (shape["x"], shape["y"] - size // 2),
                    (shape["x"] - size // 2, shape["y"] + size // 2),
                    (shape["x"] + size // 2, shape["y"] + size // 2),
                ]
                for i in range(3):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % 3]
                    pyxel.line(x1, y1, x2, y2, shape["color"])

        # Fine noise expressing silence (with sound)
        if random.random() < 0.02:
            for _ in range(3):
                x = random.randint(0, 511)
                y = random.randint(0, 511)
                pyxel.pset(x, y, 1)

            # Rare ambient sound
            if random.random() < 0.1:
                ambient_sound = random.choice([6, 9])  # Noise, ascending sound
                pyxel.play(3, ambient_sound, loop=False)


QuietPointAndLine()
