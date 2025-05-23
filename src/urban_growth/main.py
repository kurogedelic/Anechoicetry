# title: Urban Growth
# author: Leo Kuroshita
# desc: Isometric city simulation with 3D-style buildings.
# site: https://github.com/kurogedelic/anechoicetry/
# license: CC BY-SA-NC 4.0
# version: 1.0


import pyxel
import math
import random


class UrbanGrowth:
    def __init__(self):
        pyxel.init(512, 512, title="Urban Growth")

        # Urban sound definitions
        pyxel.sounds[0].set("c2d2e2", "s", "543", "f", 40)  # Construction sound
        pyxel.sounds[1].set("g2a2b2", "s", "432", "f", 35)  # Building complete
        pyxel.sounds[2].set("f1g1a1", "t", "765", "s", 60)  # Heavy machinery
        pyxel.sounds[3].set("c3e3g3", "p", "321", "f", 25)  # City ambient
        pyxel.sounds[4].set("d3f3a3", "s", "654", "v", 30)  # Traffic sound
        pyxel.sounds[5].set("b1c2d2", "n", "234", "f", 50)  # Industrial noise

        self.time = 0

        # Isometric parameters (larger scale)
        self.iso_tile_width = 48
        self.iso_tile_height = 24

        # Camera and world
        self.camera_x = 0
        self.camera_y = 0
        self.world_width = 64
        self.world_height = 64

        # Buildings data
        self.buildings = {}  # (grid_x, grid_y): building_data

        # Growth parameters
        self.growth_timer = 0
        self.growth_interval = 30
        self.city_center_x = self.world_width // 2
        self.city_center_y = self.world_height // 2

        # Camera tracking
        self.target_camera_x = 0
        self.target_camera_y = 0
        self.camera_speed = 0.03

        # Generate initial city center
        self.spawn_initial_buildings()

        pyxel.run(self.update, self.draw)

    def grid_to_iso(self, grid_x, grid_y):
        """Convert grid coordinates to isometric screen coordinates"""
        iso_x = (grid_x - grid_y) * (self.iso_tile_width // 2)
        iso_y = (grid_x + grid_y) * (self.iso_tile_height // 2)
        return iso_x, iso_y

    def spawn_initial_buildings(self):
        """Generate initial buildings in orderly grid pattern"""
        # Start with a small organized grid around city center
        for dy in range(-3, 4, 2):  # Every 2 spaces for neat spacing
            for dx in range(-3, 4, 2):
                if random.random() < 0.8:  # High chance for orderly placement
                    grid_x = self.city_center_x + dx
                    grid_y = self.city_center_y + dy
                    self.start_building_construction(grid_x, grid_y)

    def start_building_construction(self, grid_x, grid_y):
        """Start constructing a building"""
        if (grid_x, grid_y) in self.buildings:
            return

        building_type = random.choice(
            ["residential", "commercial", "office", "industrial"]
        )

        # Building properties by type (larger buildings)
        if building_type == "residential":
            max_height = random.randint(4, 12)
            colors = {"top": 14, "left": 6, "right": 4}  # Light, medium, dark
            width = random.randint(20, 32)
            depth = random.randint(20, 32)
        elif building_type == "commercial":
            max_height = random.randint(3, 8)
            colors = {"top": 10, "left": 8, "right": 2}
            width = random.randint(24, 36)
            depth = random.randint(24, 36)
        elif building_type == "office":
            max_height = random.randint(10, 25)
            colors = {"top": 13, "left": 12, "right": 1}
            width = random.randint(16, 24)
            depth = random.randint(16, 24)
        else:  # industrial
            max_height = random.randint(3, 8)
            colors = {"top": 5, "left": 4, "right": 2}
            width = random.randint(32, 42)
            depth = random.randint(24, 36)

        building = {
            "type": building_type,
            "current_height": 0,
            "max_height": max_height,
            "construction_speed": random.uniform(0.03, 0.08),
            "colors": colors,
            "width": width,
            "depth": depth,
            "construction_progress": 0.0,
            "completed": False,
            "last_sound": 0,
            "windows": self.generate_iso_windows(building_type, width, depth),
            "construction_start": self.time,
        }

        self.buildings[(grid_x, grid_y)] = building

        # Construction start sound
        if random.random() < 0.3:
            pyxel.play(0, 0, loop=False)

    def generate_iso_windows(self, building_type, width, depth):
        """Generate window positions for isometric building"""
        if building_type == "industrial":
            return {"left": [], "right": []}

        windows = {"left": [], "right": []}

        # Left face windows - much denser window placement
        for d in range(1, depth - 1, 2):  # Every 2 units instead of 4
            for h in range(6, 100, 6):  # Every 6 units instead of 12
                if random.random() < 0.8:  # Higher probability
                    windows["left"].append((d, h))

        # Right face windows - much denser window placement
        for w in range(1, width - 1, 2):  # Every 2 units instead of 4
            for h in range(6, 100, 6):  # Every 6 units instead of 12
                if random.random() < 0.8:  # Higher probability
                    windows["right"].append((w, h))

        return windows

    def update_buildings(self):
        """Update building construction"""
        for (grid_x, grid_y), building in self.buildings.items():
            if not building["completed"]:
                building["construction_progress"] += building["construction_speed"]

                target_height = int(building["construction_progress"])
                if target_height > building["current_height"]:
                    building["current_height"] = min(
                        target_height, building["max_height"]
                    )

                    if (
                        self.time - building["last_sound"] > 90
                        and random.random() < 0.2
                    ):
                        pyxel.play(1, 2, loop=False)
                        building["last_sound"] = self.time

                if building["current_height"] >= building["max_height"]:
                    building["completed"] = True
                    if random.random() < 0.5:
                        pyxel.play(2, 1, loop=False)

    def find_expansion_sites(self):
        """Find sites for orderly building expansion"""
        expansion_sites = []

        # Find all existing buildings and look for orderly adjacent sites
        for (grid_x, grid_y), building in self.buildings.items():
            if building["completed"]:
                # Check cardinal and diagonal directions with spacing for order
                for dx, dy in [
                    (0, 2),
                    (2, 0),
                    (0, -2),
                    (-2, 0),  # Cardinal with spacing
                    (2, 2),
                    (-2, 2),
                    (2, -2),
                    (-2, -2),  # Diagonal with spacing
                    (0, 1),
                    (1, 0),
                    (0, -1),
                    (-1, 0),  # Adjacent for density
                ]:
                    new_x, new_y = grid_x + dx, grid_y + dy

                    if (
                        0 <= new_x < self.world_width
                        and 0 <= new_y < self.world_height
                        and (new_x, new_y) not in self.buildings
                    ):
                        # Higher probability for evenly spaced positions
                        is_even_spaced = (new_x - self.city_center_x) % 2 == 0 and (
                            new_y - self.city_center_y
                        ) % 2 == 0

                        distance = math.sqrt(
                            (new_x - self.city_center_x) ** 2
                            + (new_y - self.city_center_y) ** 2
                        )

                        base_probability = max(0.1, 1.0 - (distance / 20))
                        # Bonus for orderly positions
                        if is_even_spaced:
                            base_probability *= 1.5

                        expansion_sites.append(
                            (new_x, new_y, min(base_probability, 0.9))
                        )

        return expansion_sites

    def update_camera(self):
        """Update camera to track city growth"""
        if len(self.buildings) > 0:
            building_positions = list(self.buildings.keys())
            min_x = min(pos[0] for pos in building_positions)
            max_x = max(pos[0] for pos in building_positions)
            min_y = min(pos[1] for pos in building_positions)
            max_y = max(pos[1] for pos in building_positions)

            center_grid_x = (min_x + max_x) / 2
            center_grid_y = (min_y + max_y) / 2

            iso_x, iso_y = self.grid_to_iso(center_grid_x, center_grid_y)

            self.target_camera_x = iso_x - 256
            self.target_camera_y = iso_y - 200

            self.camera_x += (self.target_camera_x - self.camera_x) * self.camera_speed
            self.camera_y += (self.target_camera_y - self.camera_y) * self.camera_speed

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_buildings()

        self.growth_timer += 1
        if self.growth_timer >= self.growth_interval:
            expansion_sites = self.find_expansion_sites()

            if expansion_sites:
                site = random.choices(
                    expansion_sites, weights=[site[2] for site in expansion_sites]
                )[0]

                if random.random() < site[2]:
                    self.start_building_construction(site[0], site[1])

            self.growth_timer = 0
            self.growth_interval = random.randint(40, 80)

        self.update_camera()

        # Ambient sounds
        if self.time % 180 == 0 and random.random() < 0.4:
            pyxel.play(3, 3, loop=False)

        self.time += 1

    def draw_iso_tile(self, screen_x, screen_y, color):
        """Draw isometric tile (diamond shape)"""
        # Diamond shape for ground tiles
        for dy in range(self.iso_tile_height):
            y = screen_y + dy
            if y < 0 or y >= 512:
                continue

            # Calculate width at this height
            if dy <= self.iso_tile_height // 2:
                width = (dy + 1) * 2
            else:
                width = (self.iso_tile_height - dy) * 2

            start_x = screen_x - width // 2

            for dx in range(width):
                x = start_x + dx
                if 0 <= x < 512:
                    pyxel.pset(x, y, color)

    def draw_building(self, grid_x, grid_y, building):
        """Draw isometric building with correct layering"""
        iso_x, iso_y = self.grid_to_iso(grid_x, grid_y)

        screen_x = int(iso_x - self.camera_x)
        screen_y = int(iso_y - self.camera_y)

        # Skip if far outside screen
        if screen_x < -100 or screen_x > 612 or screen_y < -100 or screen_y > 612:
            return

        height_pixels = building["current_height"] * 4  # Larger height scale
        width = building["width"]
        depth = building["depth"]

        if height_pixels <= 0:
            return

        # Draw building faces in correct order: left face → right face → top face

        # Left face (back-left wall)
        self.draw_building_left(
            screen_x,
            screen_y,
            depth,
            height_pixels,
            building["colors"]["left"],
            building["windows"]["left"],
        )

        # Right face (back-right wall)
        self.draw_building_right(
            screen_x,
            screen_y,
            width,
            height_pixels,
            building["colors"]["right"],
            building["windows"]["right"],
        )

        # Roof (pyramid style)
        roof_y = screen_y - height_pixels
        self.draw_building_roof(
            screen_x, roof_y, width, depth, building["colors"]["top"]
        )

    def draw_building_left(self, x, y, depth, height, color, windows):
        """Draw building left face (corrected for proper isometric angle)"""
        half_depth = depth // 2

        for h in range(height):
            for d in range(half_depth):
                px = x + d  # Fixed: + d instead of - d
                py = y - h - d // 2  # Fixed: - d instead of + d

                if 0 <= px < 512 and 0 <= py < 512:
                    pyxel.pset(px, py, color)

        # Draw windows on left face with proper isometric positioning
        if height > 8:
            for window_d, window_h in windows:
                # window_h ranges from 4 to 32, but we need it to range across the full building height
                if window_h < height:  # Use actual building height
                    # Convert window position to isometric coordinates
                    d_pos = (window_d * half_depth) // depth
                    # Scale window height to actual building height
                    h_pos = window_h  # Use window_h directly as it's already in the right range

                    px = x + d_pos
                    py = y - h_pos - d_pos // 2

                    if 0 <= px < 512 and 0 <= py < 512:
                        window_color = 14 if random.random() < 0.3 else 1
                        pyxel.pset(px, py, window_color)

    def draw_building_right(self, x, y, width, height, color, windows):
        """Draw building right face (corrected for proper isometric angle)"""
        half_width = width // 2

        for h in range(height):
            for w in range(half_width):
                px = x - w  # Fixed: - w instead of + w
                py = y - h - w // 2  # Fixed: - w instead of + w

                if 0 <= px < 512 and 0 <= py < 512:
                    pyxel.pset(px, py, color)

        # Draw windows on right face with proper isometric positioning
        if height > 8:
            for window_w, window_h in windows:
                # window_h ranges from 4 to 32, but we need it to range across the full building height
                if window_h < height:  # Use actual building height
                    # Convert window position to isometric coordinates
                    w_pos = (window_w * half_width) // width
                    # Scale window height to actual building height
                    h_pos = window_h  # Use window_h directly as it's already in the right range

                    px = x - w_pos
                    py = y - h_pos - w_pos // 2

                    if 0 <= px < 512 and 0 <= py < 512:
                        window_color = 14 if random.random() < 0.3 else 1
                        pyxel.pset(px, py, window_color)

    def draw(self):
        # Light orange background
        pyxel.cls(9)

        # Collect all buildings for depth sorting
        building_list = []
        for (grid_x, grid_y), building in self.buildings.items():
            # Improved depth sorting for isometric view
            # Buildings further back (larger x+y) should be drawn first
            depth_key = (grid_y * 1000) + grid_x  # Y has priority, then X
            building_list.append((depth_key, grid_x, grid_y, building))

        # Sort by depth (back to front)
        building_list.sort(key=lambda x: x[0])

        # Draw buildings in depth order
        for depth_key, grid_x, grid_y, building in building_list:
            self.draw_building(grid_x, grid_y, building)

        # UI overlay
        pyxel.rect(5, 5, 140, 35, 0)
        pyxel.rectb(5, 5, 140, 35, 7)

        # City stats
        total_buildings = len(self.buildings)
        completed_buildings = sum(1 for b in self.buildings.values() if b["completed"])

        pyxel.text(8, 8, f"Buildings: {total_buildings}", 7)
        pyxel.text(8, 16, f"Complete: {completed_buildings}", 7)
        pyxel.text(8, 24, f"Camera: {int(self.camera_x)},{int(self.camera_y)}", 7)
        pyxel.text(8, 32, "Isometric View", 14)

    def draw_building_roof(self, x, y, width, depth, color):
        """Draw roof as flat top surface (parallelogram)"""
        half_width = width // 2
        half_depth = depth // 2

        # Calculate the 4 corners of the building's top surface in correct order
        # Front center
        corner_front = (int(x), int(y))

        # Right edge (from right wall top)
        corner_right = (int(x - half_width), int(y - half_width // 2))

        # Back center (combining both wall offsets)
        corner_back = (
            int(x + half_depth - half_width),
            int(y - half_depth // 2 - half_width // 2),
        )

        # Left edge (from left wall top)
        corner_left = (int(x + half_depth), int(y - half_depth // 2))

        # Draw roof as parallelogram (in correct clockwise order)
        self.draw_parallelogram(
            corner_front, corner_right, corner_back, corner_left, color
        )

    def draw_parallelogram(self, p1, p2, p3, p4, color):
        """Draw filled parallelogram"""
        # Draw as two triangles: p1-p2-p3 and p1-p3-p4
        self.draw_triangle(p1, p2, p3, color)
        self.draw_triangle(p1, p3, p4, color)

    def draw_triangle(self, p1, p2, p3, color):
        """Draw filled triangle between three points"""
        # Simple triangle fill using scanline algorithm
        points = [p1, p2, p3]

        # Sort points by y coordinate
        points.sort(key=lambda p: p[1])

        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]

        # Skip degenerate triangles
        if y1 == y3:
            return

        # Draw triangle using horizontal scanlines
        for y in range(int(y1), int(y3) + 1):
            if y < 0 or y >= 512:
                continue

            # Find x intersections for this scanline
            if y <= y2:
                # Upper part of triangle
                if y2 != y1:
                    x_left = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                else:
                    x_left = x1

                if y3 != y1:
                    x_right = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
                else:
                    x_right = x1
            else:
                # Lower part of triangle
                if y3 != y2:
                    x_left = x2 + (x3 - x2) * (y - y2) / (y3 - y2)
                else:
                    x_left = x2

                if y3 != y1:
                    x_right = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
                else:
                    x_right = x1

            # Ensure x_left <= x_right
            if x_left > x_right:
                x_left, x_right = x_right, x_left

            # Draw horizontal line
            for x in range(int(x_left), int(x_right) + 1):
                if 0 <= x < 512:
                    pyxel.pset(x, y, color)


UrbanGrowth()
