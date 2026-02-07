# Development Guide

## Project Structure

```
rogue-tower-defense/
├── main.py              # Entry point and game loop
├── game.py              # Core game state and logic
├── config.py            # All game constants and balance
├── entities/
│   ├── tower.py         # Tower classes and behavior
│   ├── enemy.py         # Enemy classes and pathfinding
│   └── projectile.py    # Bullet/attack logic
├── systems/
│   ├── map_gen.py       # Procedural map generation
│   ├── wave_system.py   # Enemy wave spawning
│   └── progression.py   # Meta-progression (roguelike)
└── ui/
    └── hud.py           # (Future: separate UI)
```

---

## Controls

**Gameplay:**
- `1/2/3/4` - Select tower type
- `Left Click` - Place selected tower
- `Space` - Start next wave
- `ESC` - Deselect tower

**Meta:**
- `R` - Restart run (after game over)
- `U` - Open upgrade menu (after game over)

---

## Adding Content

### New Tower Type

1. Edit `config.py`:
```python
TOWER_LASER = {
    "name": "Laser",
    "cost": 300,
    "damage": 50,
    "range": 180,
    "fire_rate": 3.0,
    "penetrate": True,  # custom property
    "color": (255, 0, 255)
}

TOWER_TYPES.append(TOWER_LASER)
```

2. Handle custom behavior in `entities/tower.py` if needed

3. Update controls (add key 5 in `main.py`)

---

### New Enemy Type

1. Edit `config.py`:
```python
ENEMY_SWARM = {
    "name": "Swarm",
    "health": 20,
    "speed": 120,
    "reward": 5,
    "count": 5,  # spawns in groups
    "color": (100, 255, 100)
}

ENEMY_TYPES.append(ENEMY_SWARM)
```

2. Update `systems/wave_system.py` to include in waves

---

### Balance Tuning

All balance values in `config.py`:

**Make game easier:**
- Increase `STARTING_HEALTH`
- Increase `STARTING_GOLD`  
- Decrease `WAVE_SCALING`
- Decrease enemy health/speed
- Increase tower damage/range

**Make game harder:**
- Opposite of above
- Add more boss waves
- Increase tower costs

---

## Graphics Upgrade

### Current State
Simple colored shapes (circles, rectangles)

### Upgrade Path

**Option A: Free Assets**
1. Download tower defense pack from itch.io or OpenGameArt
2. Place in `/assets/sprites/`
3. Load in entity constructors:
```python
self.sprite = pygame.image.load("assets/sprites/tower_basic.png")
```
4. Replace `pygame.draw.circle` with `screen.blit(self.sprite, pos)`

**Option B: Commission Artist**
- Fiverr: $50-200 for full sprite pack
- Specify: 32x32 or 64x64, consistent style
- Needed: 4 towers, 4 enemies, UI elements

---

## Audio

**Add sound effects:**

1. Get sounds (freesound.org, zapsplat.com)
2. Load in constructors:
```python
self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
```
3. Play on events:
```python
self.shoot_sound.play()
```

**Add music:**
```python
pygame.mixer.music.load("assets/music/background.mp3")
pygame.mixer.music.play(-1)  # loop forever
```

---

## Building for Release

### PyInstaller (Windows/Mac/Linux)

```bash
pip install pyinstaller

# Windows
pyinstaller --onefile --windowed --name "RogueTowerDefense" main.py

# Mac
pyinstaller --onefile --windowed --osx-bundle-identifier com.yourname.rtd main.py

# Linux
pyinstaller --onefile main.py
```

**Include assets:**
- Add `--add-data "assets;assets"` (Windows)
- Add `--add-data "assets:assets"` (Mac/Linux)

---

## Steam Release

### Prerequisites
1. Steamworks account ($100 one-time)
2. Game page set up
3. Build ready (executable)

### Steps

**1. Prepare Build**
```bash
# Build for each platform
pyinstaller --onefile --windowed main.py

# Test thoroughly on each OS
```

**2. Upload to Steamworks**
- Use Steamworks SDK
- Create depot for each platform
- Upload builds

**3. Set Pricing**
- Recommended: $5-15 for indie TD
- Consider regional pricing

**4. Store Page**
- Screenshots (1920x1080)
- Trailer (30-60 seconds)
- Description emphasizing roguelike + tower defense
- Tags: Tower Defense, Roguelike, Strategy, Indie

**5. Launch**
- Consider Early Access first
- Build community on Discord/Reddit
- Send keys to streamers

---

## Marketing Checklist

**Pre-Launch:**
- [ ] Twitter devlog (weekly updates)
- [ ] Reddit posts (/r/gamedev, /r/indiegaming)
- [ ] Discord server
- [ ] Gameplay GIFs
- [ ] Trailer video

**Launch:**
- [ ] Post to /r/gaming, /r/Games
- [ ] Steam announcement
- [ ] Email gaming sites
- [ ] Send keys to YouTubers/streamers
- [ ] Post on itch.io too (wider reach)

**Post-Launch:**
- [ ] Respond to feedback
- [ ] Update regularly (content patches)
- [ ] Run sales (Steam seasonal sales)
- [ ] Consider DLC (tower packs, new modes)

---

## Testing

**Manual Testing Checklist:**
- [ ] Can place all tower types
- [ ] All enemies spawn and move correctly
- [ ] Damage/health calculations correct
- [ ] Wave progression works
- [ ] Game over triggers properly
- [ ] Upgrades persist between runs
- [ ] No crashes (play 30+ minutes)

**Balance Testing:**
- [ ] Wave 10 reachable with good play
- [ ] Wave 20 challenging but possible
- [ ] All towers useful (no useless towers)
- [ ] Gold economy feels fair
- [ ] Upgrades feel impactful

---

## Common Issues

**Game runs slow:**
- Reduce FPS in config.py
- Optimize rendering (don't redraw unchanged elements)
- Profile with `python -m cProfile main.py`

**Enemies walk through towers:**
- Check buildable_tiles logic in map_gen.py
- Ensure towers block path calculation

**Balance feels off:**
- Adjust WAVE_SCALING in config.py
- Increase starting gold
- Tweak tower costs/stats

---

## Monetization Ideas

**Base Game:** $7.99-9.99

**DLC:**
- Tower Pack 1: $1.99 (3 new towers)
- Map Themes: $0.99 each (desert, snow, lava)
- Soundtrack: $2.99

**Future:**
- Mobile port (iOS/Android)
- Multiplayer co-op (2 players share map)
- Level editor + Workshop

---

## Performance Tips

**Optimize rendering:**
```python
# Only draw what changed
dirty_rects = []  # track what to update
pygame.display.update(dirty_rects)  # instead of flip()
```

**Optimize collisions:**
```python
# Spatial partitioning for large numbers of entities
# Only check nearby enemies for tower targeting
```

**Profile:**
```bash
python -m cProfile -o profile.stats main.py
python -m pstats profile.stats
# > sort time
# > stats 20
```

---

## Next Steps

**Immediate (Week 1):**
1. Playtest and balance
2. Add more tower types (6-8 total)
3. Add more enemy types (6-8 total)
4. Better placeholder graphics (colored sprites)

**Short-term (Month 1):**
1. Commission or find good sprite pack
2. Add sound effects
3. Add background music
4. Polish UI (buttons, tooltips)

**Medium-term (Months 2-3):**
1. More content (10+ towers, 10+ enemies)
2. Special abilities
3. Boss fights every 5 waves
4. Achievements
5. Tutorial mode

**Release (Month 3-4):**
1. Final testing
2. Build for all platforms
3. Steam page setup
4. Marketing push
5. Launch!

---

**Good luck! 🚀**
