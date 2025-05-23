# title: Data Duplex
# author: Leo Kuroshita
# desc: Monochrome barcode-like data streams.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import random


class DataDuplex:
    def __init__(self):
        pyxel.init(512, 512, title="Data Duplex")

        # Digital sound definitions
        pyxel.sounds[0].set("c4c3c4c3", "s", "7531", "n", 10)  # Data noise 1
        pyxel.sounds[1].set("g3f3g3f3", "p", "6420", "n", 8)  # Data noise 2
        pyxel.sounds[2].set("c2", "n", "7", "f", 15)  # Glitch sound
        pyxel.sounds[3].set("a3", "s", "3", "s", 5)  # Scan sound
        pyxel.sounds[4].set("f2g2a2b2", "n", "4321", "v", 12)  # Error sound
        pyxel.sounds[5].set("c4c4c4c4", "p", "7777", "n", 6)  # High-speed data
        pyxel.sounds[6].set("e1", "n", "5", "f", 20)  # Low frequency noise

        self.time = 0

        # Barcode parameters
        self.bar_width = 4
        self.num_bars = 512 // self.bar_width
        self.bars = []

        # Data streams
        self.data_streams = []
        self.max_streams = 8

        # Noise parameters
        self.noise_intensity = 0.3
        self.glitch_probability = 0.02
        self.scan_lines = []

        # Initialize
        self.generate_initial_bars()
        self.generate_data_streams()

        pyxel.run(self.update, self.draw)

    def generate_initial_bars(self):
        """Generate initial barcode"""
        for i in range(self.num_bars):
            bar = {
                "height": random.randint(50, 450),
                "base_height": random.randint(50, 450),
                "noise_offset": random.uniform(0, 1),
                "update_timer": random.randint(0, 20),
                "stability": random.uniform(0.1, 0.9),  # Stability level
                "data_type": random.choice(["binary", "analog", "corrupt"]),
            }
            self.bars.append(bar)

    def generate_data_streams(self):
        """Generate data streams"""
        for _ in range(self.max_streams):
            stream = {
                "y": random.randint(0, 512),
                "speed": random.uniform(1, 8),
                "width": random.randint(2, 16),
                "pattern": [random.choice([0, 1]) for _ in range(32)],
                "pattern_index": 0,
                "lifetime": random.randint(60, 300),
                "direction": random.choice([-1, 1]),
            }
            self.data_streams.append(stream)

    def update_bars(self):
        """Update barcode"""
        for i, bar in enumerate(self.bars):
            bar["update_timer"] -= 1

            if bar["update_timer"] <= 0:
                # Update according to data type
                if bar["data_type"] == "binary":
                    # Binary: sudden changes
                    if random.random() < 0.1:
                        bar["height"] = random.choice([50, 200, 350, 450])
                        # Binary sound
                        if random.random() < 0.3:
                            pyxel.play(0, random.choice([0, 1]), loop=False)

                elif bar["data_type"] == "analog":
                    # Analog: smooth changes
                    target = bar["base_height"] + random.randint(-100, 100)
                    bar["height"] += (target - bar["height"]) * 0.1
                    bar["height"] = max(20, min(480, bar["height"]))

                elif bar["data_type"] == "corrupt":
                    # Corrupted: random violent changes
                    if random.random() < 0.2:
                        bar["height"] = random.randint(10, 500)
                        # Glitch sound
                        if random.random() < 0.5:
                            pyxel.play(1, 2, loop=False)

                # Add noise
                noise = random.uniform(-30, 30) * self.noise_intensity
                bar["height"] += noise
                bar["height"] = max(10, min(500, bar["height"]))

                # Reset update interval
                if bar["stability"] > 0.7:
                    bar["update_timer"] = random.randint(10, 30)
                elif bar["stability"] > 0.3:
                    bar["update_timer"] = random.randint(3, 15)
                else:
                    bar["update_timer"] = random.randint(1, 5)

    def update_data_streams(self):
        """Update data streams"""
        for stream in self.data_streams[:]:
            stream["y"] += stream["speed"] * stream["direction"]
            stream["lifetime"] -= 1

            # Advance pattern
            stream["pattern_index"] = (stream["pattern_index"] + 1) % len(
                stream["pattern"]
            )

            # Wrap around screen edges
            if stream["y"] > 512:
                stream["y"] = -stream["width"]
            elif stream["y"] < -stream["width"]:
                stream["y"] = 512

            # Remove when lifetime ends
            if stream["lifetime"] <= 0:
                self.data_streams.remove(stream)

        # Generate new streams
        if len(self.data_streams) < self.max_streams and random.random() < 0.05:
            self.generate_data_streams()

    def generate_scan_line(self):
        """Generate scan lines"""
        if random.random() < 0.1:
            scan = {
                "y": random.randint(0, 512),
                "speed": random.uniform(5, 20),
                "width": random.randint(2, 8),
                "lifetime": random.randint(20, 60),
                "intensity": random.uniform(0.5, 1.0),
            }
            self.scan_lines.append(scan)

            # Scan sound
            if random.random() < 0.7:
                pyxel.play(2, 3, loop=False)

    def update_scan_lines(self):
        """Update scan lines"""
        for scan in self.scan_lines[:]:
            scan["y"] += scan["speed"]
            scan["lifetime"] -= 1

            if scan["y"] > 512 or scan["lifetime"] <= 0:
                self.scan_lines.remove(scan)

    def trigger_glitch(self):
        """Trigger glitch effect"""
        if random.random() < self.glitch_probability:
            # Change multiple bars simultaneously
            affected_bars = random.sample(self.bars, random.randint(5, 20))
            for bar in affected_bars:
                bar["height"] = random.randint(10, 500)
                bar["data_type"] = "corrupt"

            # Strong audio effect
            pyxel.play(0, 4, loop=False)
            pyxel.play(3, 6, loop=False)

            # Temporarily increase noise intensity
            self.noise_intensity = min(1.0, self.noise_intensity + 0.2)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Update barcode
        self.update_bars()

        # Update data streams
        self.update_data_streams()

        # Scan lines
        self.generate_scan_line()
        self.update_scan_lines()

        # Glitch effect
        self.trigger_glitch()

        # Gradually decrease noise intensity
        self.noise_intensity *= 0.995
        self.noise_intensity = max(0.1, self.noise_intensity)

        # High-speed data sound
        if self.time % 15 == 0 and random.random() < 0.4:
            pyxel.play(1, 5, loop=False)

        # Background noise
        if self.time % 120 == 0 and random.random() < 0.3:
            pyxel.play(2, 6, loop=False)

        self.time += 1

    def draw(self):
        # Black background
        pyxel.cls(0)

        # Draw barcode
        for i, bar in enumerate(self.bars):
            x = i * self.bar_width
            height = int(bar["height"])

            # Bar center position
            y_center = 256
            y_start = y_center - height // 2
            y_end = y_center + height // 2

            # Draw bar (white)
            pyxel.rect(x, y_start, self.bar_width, height, 7)

            # Effects according to data type
            if bar["data_type"] == "corrupt":
                # Corrupted data blinks
                if self.time % 4 < 2:
                    pyxel.rect(x, y_start, self.bar_width, height, 8)

            elif bar["data_type"] == "binary":
                # Binary data has sharp boundaries
                if height > 100:
                    pyxel.rect(x, y_start, self.bar_width, 2, 15)
                    pyxel.rect(x, y_end - 2, self.bar_width, 2, 15)

        # Draw data streams
        for stream in self.data_streams:
            y = int(stream["y"])

            # Draw according to pattern
            for i, bit in enumerate(stream["pattern"]):
                x = i * 16
                if x > 512:
                    break

                if bit == 1:
                    pyxel.rect(x, y, 16, stream["width"], 7)
                else:
                    # 0 data is faint
                    pyxel.rect(x, y, 16, stream["width"], 1)

        # Draw scan lines
        for scan in self.scan_lines:
            y = int(scan["y"])

            # Main line
            pyxel.rect(0, y, 512, scan["width"], 15)

            # Effect line
            if scan["width"] > 3:
                pyxel.rect(0, y + 1, 512, 1, 7)

        # Noise pixels
        noise_count = int(100 * self.noise_intensity)
        for _ in range(noise_count):
            x = random.randint(0, 511)
            y = random.randint(0, 511)
            color = random.choice([0, 7, 15])
            pyxel.pset(x, y, color)

        # Glitch effect
        if random.random() < self.glitch_probability * 0.5:
            # Horizontal line glitch
            for _ in range(random.randint(1, 5)):
                y = random.randint(0, 511)
                width = random.randint(50, 512)
                x = random.randint(0, 512 - width)
                pyxel.rect(x, y, width, 1, random.choice([0, 7, 15]))

        # Data frame border
        pyxel.rectb(0, 0, 512, 512, 1)

        # Time display (digital style)
        time_str = f"{self.time:06d}"
        pyxel.text(5, 5, time_str, 7)

        # Noise level display
        noise_bar_width = int(100 * self.noise_intensity)
        pyxel.rect(5, 15, noise_bar_width, 3, 8)
        pyxel.rectb(5, 15, 100, 3, 7)


DataDuplex()
