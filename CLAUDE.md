# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Anechoicetry is a collection of generative audiovisual art pieces built with the Pyxel game engine. Each piece explores "poetic low-fi pixel reels" through minimal code and emergent complexity.

## Commands

### Build & Package
```bash
# Package a source file into a .pyxapp
pyxel package <app_dir> <main.py>

# Example: Package the breath_of_form app
pyxel package src/breath_of_form main.py
```

### Run & Test
```bash
# Run a Python script directly
pyxel run <script.py>

# Play a packaged .pyxapp file
pyxel play <app.pyxapp>

# Example: Run source directly
pyxel run src/urban_growth/main.py

# Example: Play packaged app
pyxel play apps/urban_growth.pyxapp
```

### Deploy to Web
```bash
# Convert .pyxapp to HTML for web deployment
pyxel app2html <app.pyxapp>

# Example: Generate HTML version
pyxel app2html apps/urban_growth.pyxapp
```

## Architecture

### Directory Structure
- **src/**: Source code for each art piece, organized by project name
- **apps/**: Packaged .pyxapp files (ZIP format with embedded Python)
- **docs/**: HTML versions for web deployment
- **etc/**: Project documentation and metadata

### Technical Constraints
- Canvas: 512x512 pixels (fixed)
- Frame rate: 30fps default
- Color palette: Pyxel's 16 colors only
- Exit key: Q (unified across all pieces)

### Code Standards
Each piece follows a standardized header format:
```python
"""
Title - Anechoicetry Collection
by Leo Kuroshita
Description of the piece
Site: https://kurogedelic.com
License: CC BY-SA-NC 4.0
Version: X.X.X
"""
```

### Aesthetic Philosophy
- Minimal code for maximum poetic expression
- Meaningless beautiful movement
- Musical rhythm without sound
- Avoid perfect symmetry
- Include subtle irregularities
- Leave space for interpretation

### Common Patterns
- Use `math.sin/cos` for organic movement
- Phase differences for asynchronous behavior
- Subtle variations in size, position, and color
- Elements that occasionally appear/disappear
- Non-interactive observation pieces

### Code Architecture
Each piece follows a standardized class-based structure:
```python
class PieceName:
    def __init__(self):
        pyxel.init(512, 512, title="Piece Name")
        # Initialize sound design (5-7 sounds per piece)
        # Set up procedural systems
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Update logic here
    
    def draw(self):
        # Rendering logic here
```

### Sound Design Integration
All pieces include comprehensive audio landscapes:
- 5-7 sounds per piece using `pyxel.sounds[n].set()`
- Event-driven playback with `pyxel.play()`
- Probabilistic triggers for ambient audio
- Contextual sounds for visual events

### Development Workflow
```bash
# Develop and test changes
pyxel run src/<piece_name>/main.py

# Package for distribution
pyxel package src/<piece_name> main.py

# Deploy to web (generates docs/<piece_name>.html)
pyxel app2html apps/<piece_name>.pyxapp
```