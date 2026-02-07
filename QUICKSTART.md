# Quick Start Guide

## Installation & Running

### Step 1: Install Python (if needed)
- Download from python.org
- Version 3.8 or higher required
- Make sure "Add to PATH" is checked during install

### Step 2: Install Pygame
```bash
# In terminal/command prompt:
pip install pygame

# Or if pip doesn't work:
pip3 install pygame

# Or:
python -m pip install pygame
```

### Step 3: Run the Game
```bash
cd rogue-tower-defense
python main.py

# Or:
python3 main.py
```

---

## First Time Playing

**Controls:**
1. Press `1`, `2`, `3`, or `4` to select a tower type
2. Click on green tiles to place towers (costs gold)
3. Press `SPACE` to start the wave
4. Defend against enemies!
5. When you die, press `U` to see upgrades, `R` to restart

**Tips:**
- Mix tower types (Basic + Slow + Splash works well)
- Save gold for later waves
- Upgrades persist between runs (meta-progression)
- Each run has a different map

---

## If It Doesn't Run

**Error: "No module named pygame"**
```bash
pip install pygame
```

**Error: "Python not found"**
- Install Python from python.org
- Add to PATH

**Error: "No display"**
- Make sure you're running on a machine with a display (not headless server)

**Error: Game window doesn't appear**
- Check if Python has screen recording permissions (Mac)
- Try running as administrator (Windows)

---

## Troubleshooting

**Slow performance:**
- Edit config.py, change FPS from 60 to 30

**Window too big:**
- Edit config.py, reduce SCREEN_WIDTH and SCREEN_HEIGHT

**Want to reset progression:**
- Delete `progression.json` file

---

## Ready to Play!

Press `1` to select Basic Tower, click to place, press `SPACE` to start!

Have fun! 🎮
