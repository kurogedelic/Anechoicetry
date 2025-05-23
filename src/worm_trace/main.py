# title: Worm Trace
# author: Leo Kuroshita
# desc: Wandering worm traces random paths.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0

import pyxel
import random
import math


class WormTrace:
    def __init__(self):
        pyxel.init(512, 512, title="Worm Trace")

        # Sound definitions
        pyxel.sounds[0].set("c3e3g3", "p", "432", "f", 20)  # Turn sound
        pyxel.sounds[1].set("f2a2c3", "n", "321", "s", 15)  # Collision sound
        pyxel.sounds[2].set("g1c2e2", "t", "543", "v", 25)  # Growth sound

        self.time = 0

        # Worm properties
        self.worm_body = [(256, 256)]  # Start at center
        self.max_length = 200  # Maximum worm length
        self.direction = random.choice(
            [(0, -1), (1, 0), (0, 1), (-1, 0)]
        )  # Up, Right, Down, Left
        self.speed = 10  # Pixels per step

        # Movement parameters
        self.move_timer = 0
        self.move_interval = 1  # Steps between movements
        self.turn_probability = 0.12  # Probability to turn each step
        self.last_direction = self.direction

        # Trail fade system
        self.trail_fade = {}  # Position -> fade_time
        self.fade_duration = 300  # Frames to fade

        pyxel.run(self.update, self.draw)

    def get_opposite_direction(self, direction):
        """Get opposite direction to prevent immediate backtracking"""
        dx, dy = direction
        return (-dx, -dy)

    def get_available_directions(self):
        """Get all directions except the opposite of current direction"""
        all_directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        opposite = self.get_opposite_direction(self.direction)
        return [d for d in all_directions if d != opposite]

    def check_collision(self, x, y):
        """Check if position collides with walls or worm body"""
        # Wall collision
        if x < 10 or x >= 502 or y < 10 or y >= 502:
            return True

        # Self collision (check against body except head)
        for i, (bx, by) in enumerate(self.worm_body[1:], 1):
            if abs(x - bx) < 3 and abs(y - by) < 3:
                return True

        return False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.move_timer += 1

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            # Random direction change
            if random.random() < self.turn_probability:
                available_directions = self.get_available_directions()
                new_direction = random.choice(available_directions)

                if new_direction != self.direction:
                    self.last_direction = self.direction
                    self.direction = new_direction
                    # Turn sound
                    if random.random() < 0.7:
                        pyxel.play(0, 0, loop=False)

            # Calculate next position
            head_x, head_y = self.worm_body[0]
            dx, dy = self.direction
            next_x = head_x + dx * self.speed
            next_y = head_y + dy * self.speed

            # Check collision
            if self.check_collision(next_x, next_y):
                # Collision sound
                if random.random() < 0.8:
                    pyxel.play(1, 1, loop=False)

                # Try to find alternative direction
                available_directions = self.get_available_directions()
                random.shuffle(available_directions)

                found_direction = None
                for test_direction in available_directions:
                    test_dx, test_dy = test_direction
                    test_x = head_x + test_dx * self.speed
                    test_y = head_y + test_dy * self.speed

                    if not self.check_collision(test_x, test_y):
                        found_direction = test_direction
                        break

                if found_direction:
                    self.direction = found_direction
                    dx, dy = self.direction
                    next_x = head_x + dx * self.speed
                    next_y = head_y + dy * self.speed
                else:
                    # No direction available, reset worm
                    self.reset_worm()
                    return

            # Move worm
            self.worm_body.insert(0, (next_x, next_y))

            # Maintain maximum length
            if len(self.worm_body) > self.max_length:
                removed_pos = self.worm_body.pop()
                # Add to trail fade
                self.trail_fade[removed_pos] = self.time

                # Growth sound occasionally
                if random.random() < 0.1:
                    pyxel.play(2, 2, loop=False)

        # Update trail fade
        positions_to_remove = []
        for pos, fade_start in self.trail_fade.items():
            if self.time - fade_start > self.fade_duration:
                positions_to_remove.append(pos)

        for pos in positions_to_remove:
            del self.trail_fade[pos]

        self.time += 1

    def reset_worm(self):
        """Reset worm to a random position"""
        self.worm_body = [(random.randint(50, 462), random.randint(50, 462))]
        self.direction = random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])
        self.trail_fade.clear()

    def draw(self):
        # Clear with light background
        pyxel.cls(127)

        # Draw fading trail
        for pos, fade_start in self.trail_fade.items():
            x, y = pos
            fade_progress = (self.time - fade_start) / self.fade_duration

            if fade_progress < 1.0:
                # Fade from dark to light
                if fade_progress < 0.3:
                    color = 1  # Dark blue
                elif fade_progress < 0.6:
                    color = 5  # Gray
                else:
                    color = 6  # Light gray

                pyxel.rect(x - 1, y - 1, 4, 4, color)

        # Draw worm body
        for i, (x, y) in enumerate(self.worm_body):
            if i == 0:
                # Head - larger square
                pyxel.rect(x - 4, y - 4, 10, 10, 0)  # Black head
                pyxel.rect(x - 2, y - 2, 6, 6, 8)  # Red center
            else:
                # Body - get darker towards tail
                if i < 5:
                    color = 0  # Black
                elif i < 20:
                    color = 1  # Dark blue
                elif i < 50:
                    color = 5  # Gray
                else:
                    color = 6  # Light gray

                pyxel.rect(x - 1, y - 1, 4, 4, color)

        # UI
        pyxel.rect(5, 5, 120, 25, 0)
        pyxel.rectb(5, 5, 120, 25, 7)
        pyxel.text(8, 8, f"Length: {len(self.worm_body)}", 7)
        pyxel.text(8, 16, f"Trail: {len(self.trail_fade)}", 7)


WormTrace()
