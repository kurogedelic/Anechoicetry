# title: Planets of Reflection
# author: Leo Kuroshita
# desc: Colorful marble planets in orbital system.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0


import pyxel
import math
import random


class PlanetsOfReflection:
    def __init__(self):
        pyxel.init(512, 512, title="Planets of Reflection")

        # Cosmic sound definitions
        pyxel.sounds[0].set("c2e2g2", "t", "753", "f", 80)  # Large planet sound
        pyxel.sounds[1].set("g3c4e4", "t", "531", "f", 60)  # Medium planet sound
        pyxel.sounds[2].set("c4e4g4c4", "t", "4321", "f", 40)  # Small planet sound
        pyxel.sounds[3].set("f2a2c3", "s", "642", "v", 90)  # Orbital resonance sound
        pyxel.sounds[4].set("d2f2a2d3", "t", "7531", "s", 70)  # Gravity sound
        pyxel.sounds[5].set("g1c2e2g2", "t", "7642", "f", 100)  # Space sound

        self.time = 0
        self.planets = []
        self.orbital_center_x = 256
        self.orbital_center_y = 256

        # Planet color palette (single flat colors)
        self.planet_colors = [8, 9, 10, 11, 12, 13, 14, 15, 6, 7]

        # Orbital parameters
        self.orbital_layers = [
            {"radius": 80, "max_planets": 2, "size_range": (25, 40)},
            {"radius": 130, "max_planets": 3, "size_range": (20, 35)},
            {"radius": 180, "max_planets": 4, "size_range": (15, 30)},
            {"radius": 230, "max_planets": 5, "size_range": (12, 25)},
            {"radius": 280, "max_planets": 6, "size_range": (8, 20)},
            {"radius": 330, "max_planets": 8, "size_range": (6, 15)},
        ]

        # Generate initial planets
        self.generate_planets()

        pyxel.run(self.update, self.draw)

    def generate_planets(self):
        """Generate planets"""
        for layer_idx, layer in enumerate(self.orbital_layers):
            for i in range(layer["max_planets"]):
                angle = (i / layer["max_planets"]) * 2 * math.pi + random.uniform(
                    0, 0.5
                )

                planet = {
                    "orbit_radius": layer["radius"] + random.uniform(-10, 10),
                    "angle": angle,
                    "angular_speed": random.uniform(0.005, 0.02) / (layer_idx + 1),
                    "size": random.randint(*layer["size_range"]),
                    "color": random.choice(self.planet_colors),
                    "rotation": 0,
                    "rotation_speed": random.uniform(-0.1, 0.1),
                    "layer": layer_idx,
                    "sound_timer": random.randint(0, 200),
                    "sound_interval": random.randint(300, 600),
                    "orbital_phase": random.uniform(0, 2 * math.pi),
                    "vertical_oscillation": random.uniform(0.2, 0.8),
                    "breathing": random.uniform(0.02, 0.05),
                }

                self.planets.append(planet)

    def update_planets(self):
        """Update planet positions and states"""
        for planet in self.planets:
            # Orbital motion
            planet["angle"] += planet["angular_speed"]

            # Rotation
            planet["rotation"] += planet["rotation_speed"]

            # Calculate orbital position
            base_x = self.orbital_center_x + planet["orbit_radius"] * math.cos(
                planet["angle"]
            )
            base_y = self.orbital_center_y + planet["orbit_radius"] * math.sin(
                planet["angle"]
            )

            # Vertical oscillation (elliptical orbit effect)
            vertical_offset = (
                planet["vertical_oscillation"]
                * 20
                * math.sin(planet["angle"] * 2 + planet["orbital_phase"])
            )

            planet["x"] = base_x
            planet["y"] = base_y + vertical_offset

            # Sound timer
            planet["sound_timer"] += 1
            if planet["sound_timer"] >= planet["sound_interval"]:
                self.play_planet_sound(planet)
                planet["sound_timer"] = 0
                planet["sound_interval"] = random.randint(200, 400)  # More frequent

    def play_planet_sound(self, planet):
        """Play sound according to planet size"""
        if random.random() < 0.6:  # Increase probability
            if planet["size"] > 30:
                pyxel.play(0, 0, loop=False)  # Large planet
            elif planet["size"] > 20:
                pyxel.play(1, 1, loop=False)  # Medium planet
            else:
                pyxel.play(2, 2, loop=False)  # Small planet

    def check_orbital_resonance(self):
        """Check orbital resonance"""
        if self.time % 180 == 0:  # Periodic check
            # Check angle difference between nearby orbit planets
            for i, p1 in enumerate(self.planets):
                for p2 in self.planets[i + 1 :]:
                    orbit_diff = abs(p1["orbit_radius"] - p2["orbit_radius"])
                    if orbit_diff < 30:  # Nearby orbit
                        angle_diff = abs(p1["angle"] - p2["angle"]) % (2 * math.pi)
                        if (
                            angle_diff < 0.3 or angle_diff > 2 * math.pi - 0.3
                        ):  # Close angle
                            if random.random() < 0.4:
                                pyxel.play(1, 3, loop=False)  # Resonance sound

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Update planets
        self.update_planets()

        # Check orbital resonance
        self.check_orbital_resonance()

        # Space sound (more frequent)
        if self.time % 150 == 0 and random.random() < 0.5:
            pyxel.play(2, 5, loop=False)

        # Gravity sound (more frequent)
        if self.time % 80 == 0 and random.random() < 0.4:
            pyxel.play(0, 4, loop=False)

        self.time += 1

    def draw_planet(self, planet):
        """Draw planet (simple flat color)"""
        x, y = int(planet["x"]), int(planet["y"])
        base_size = planet["size"]

        # Breathing effect
        breathing = 1 + planet["breathing"] * math.sin(
            self.time * 0.05 + planet["angle"]
        )
        size = int(base_size * breathing)

        # Draw planet with flat color
        pyxel.circ(x, y, size, planet["color"])

        # Highlight
        highlight_x = x - size // 3
        highlight_y = y - size // 3
        highlight_size = max(2, size // 4)
        pyxel.circ(highlight_x, highlight_y, highlight_size, 7)

        # Shadow
        shadow_x = x + size // 4
        shadow_y = y + size // 4
        shadow_size = max(1, size // 6)
        pyxel.circ(shadow_x, shadow_y, shadow_size, 0)

    def draw_orbital_paths(self):
        """Draw orbital paths"""
        for layer in self.orbital_layers:
            radius = layer["radius"]

            # Orbital ellipse
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = self.orbital_center_x + radius * math.cos(rad)
                y = self.orbital_center_y + radius * math.sin(rad)

                # Orbit considering vertical oscillation
                vertical_offset = 20 * 0.5 * math.sin(rad * 2)
                y += vertical_offset

                if 0 <= x < 512 and 0 <= y < 512:
                    # Faint orbital line
                    if self.time % 120 < 60:  # Blinking
                        pyxel.pset(int(x), int(y), 1)

    def draw_background_stars(self):
        """Draw background stars"""
        # Fixed constellation pattern
        star_seed = 42
        random.seed(star_seed)

        for _ in range(50):
            x = random.randint(0, 511)
            y = random.randint(0, 511)

            # Star blinking
            brightness_phase = (self.time * 0.01 + x * 0.01 + y * 0.01) % (2 * math.pi)
            brightness = 0.5 + 0.5 * math.sin(brightness_phase)

            if brightness > 0.7:
                size = 1 if brightness > 0.9 else 0
                pyxel.circ(x, y, size, 7)

        # Reset random seed
        random.seed()

    def draw(self):
        # Deep space background
        pyxel.cls(1)

        # Background stars
        self.draw_background_stars()

        # Orbital paths
        self.draw_orbital_paths()

        # Draw planets in size order (far to near)
        sorted_planets = sorted(
            self.planets, key=lambda p: p["orbit_radius"], reverse=True
        )

        for planet in sorted_planets:
            self.draw_planet(planet)

        # Central gravity source (sun)
        sun_pulse = 1 + 0.1 * math.sin(self.time * 0.03)
        sun_size = int(15 * sun_pulse)
        pyxel.circ(self.orbital_center_x, self.orbital_center_y, sun_size, 9)
        pyxel.circ(self.orbital_center_x, self.orbital_center_y, sun_size - 3, 10)
        pyxel.circ(self.orbital_center_x, self.orbital_center_y, sun_size - 6, 14)

        # Gravity wave representation
        if self.time % 90 < 45:
            for radius in range(20, 60, 10):
                ripple_alpha = 1.0 - ((self.time % 90) / 45.0)
                if ripple_alpha > 0:
                    for angle in range(0, 360, 15):
                        rad = math.radians(angle)
                        x = self.orbital_center_x + radius * math.cos(rad)
                        y = self.orbital_center_y + radius * math.sin(rad)
                        if 0 <= x < 512 and 0 <= y < 512:
                            pyxel.pset(int(x), int(y), 6)


PlanetsOfReflection()
