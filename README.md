# Rogue Tower Defense

**Genre:** Tower Defense + Roguelike  
**Status:** MVP - Playable Prototype  
**Goal:** Steam Release for Indie Revenue

## 🎮 Core Concept

Defend against waves of enemies with strategically placed towers. Each run has a procedurally generated map. When you die, you keep meta-progression unlocks to get stronger for the next run.

**Roguelike Elements:**
- Permadeath (lose the run)
- Random maps each playthrough
- Meta-progression (unlock permanent upgrades)
- Increasing difficulty

**Tower Defense Elements:**
- Multiple tower types
- Resource management
- Wave-based enemies
- Strategic placement

---

## 🚀 Quick Start

**Requirements:**
- Python 3.8+
- Pygame

**Install & Run:**
```bash
pip install pygame
python main.py
```

---

## 🎯 Current MVP Features

**✅ Implemented:**
- Procedural map generation
- 4 tower types (Basic, Sniper, Splash, Slow)
- 4 enemy types (Fast, Tank, Flying, Boss)
- Wave system with scaling difficulty
- Resource economy (gold)
- Tower placement and targeting
- Health system
- Game over and restart
- Meta-progression (unlock system)
- Simple UI

**📋 Planned (Next Phase):**
- Better graphics (sprites)
- Sound effects and music
- More tower types
- More enemy varieties
- Special abilities
- Shop between waves
- Achievements
- Steam integration

---

## 🎨 Graphics Upgrade Path

**Current:** Simple colored shapes (functional placeholder)

**To upgrade:**
1. Get sprites from:
   - itch.io (many free tower defense packs)
   - OpenGameArt.org
   - Commission artist (Fiverr: $50-200)

2. Replace in code:
   - Search for `pygame.draw.circle` → replace with `blit(sprite)`
   - Sprites go in `/assets/sprites/` folder

3. Recommended sizes:
   - Towers: 32x32 or 64x64
   - Enemies: 32x32
   - UI elements: varies

---

## 💰 Steam Release Checklist

**Pre-Release:**
- [ ] Add better graphics
- [ ] Add sound/music
- [ ] 10+ hours of content (more towers, enemies, maps)
- [ ] Balancing and testing
- [ ] Build executables (PyInstaller)
- [ ] Create store page assets (screenshots, trailer)

**Steam Setup:**
- [ ] Register Steamworks account ($100 one-time fee)
- [ ] Upload build
- [ ] Set pricing ($5-15 recommended)
- [ ] Marketing (Discord, Reddit, Twitter)

**Estimated Revenue (Conservative):**
- 100 sales @ $10 = $1,000
- 500 sales @ $10 = $5,000
- 1,000 sales @ $10 = $10,000

*(Steam takes 30%, so multiply by 0.7 for your cut)*

---

## 🧩 Architecture

```
rogue-tower-defense/
├── main.py              # Entry point, game loop
├── game.py              # Core game logic
├── entities/
│   ├── tower.py         # Tower classes
│   ├── enemy.py         # Enemy classes
│   └── projectile.py    # Bullets/attacks
├── systems/
│   ├── map_gen.py       # Procedural map generation
│   ├── wave_system.py   # Enemy wave spawning
│   └── progression.py   # Meta-progression unlocks
├── ui/
│   └── hud.py           # UI rendering
├── config.py            # Game balance values
└── assets/              # Graphics, sounds (add later)
```

---

## 🔧 How to Extend

**Add new tower:**
1. Edit `entities/tower.py`
2. Add tower class with stats
3. Add to tower selection UI

**Add new enemy:**
1. Edit `entities/enemy.py`
2. Define stats and behavior
3. Add to wave spawner

**Tune difficulty:**
1. Edit `config.py`
2. Adjust WAVE_SCALING, ENEMY_HEALTH, etc.

**Add graphics:**
1. Place sprites in `/assets/sprites/`
2. Load in entity classes
3. Replace `pygame.draw.*` with `screen.blit(sprite, pos)`

---

## 📈 Monetization Strategy

**Steam Pricing:**
- Launch: $7.99 (budget-friendly)
- Sales: Drop to $4.99 (steam sales)
- After updates: Raise to $9.99

**Additional Revenue:**
- DLC: New tower packs ($1.99 each)
- Soundtrack DLC: $2.99
- Workshop support (user maps)

**Marketing:**
- Post to /r/gamedev, /r/indiegaming
- Twitter devlog updates
- YouTube gameplay trailer
- Streamers (send keys)

---

## 🛠️ Development Roadmap

**Phase 1: MVP (CURRENT) ✅**
- Core gameplay working
- Simple graphics
- Basic progression

**Phase 2: Content (1-2 months)**
- 10 tower types
- 15 enemy types
- 5 map themes
- Better graphics
- Sound/music

**Phase 3: Polish (1 month)**
- Balancing
- Particle effects
- Screen shake
- Achievements
- Tutorial

**Phase 4: Release (1 week)**
- Build for Windows/Mac/Linux
- Steam page
- Marketing push
- Launch!

---

## 💡 Tips for Success

**Game Design:**
- Keep it simple but deep
- Tune difficulty carefully (not too hard, not too easy)
- Add juice (screen shake, particles, sounds)
- Playtest with friends

**Art:**
- Consistent style (don't mix pixel art + 3D)
- Start with free assets, upgrade later
- Good UI is critical (players see it constantly)

**Marketing:**
- Build in public (Twitter, devlog)
- Make GIFs of cool moments
- Get streamers to play (send keys)
- Participate in game jams (visibility)

---

## 📝 License

MIT - Do whatever you want with this code!

---

## 🤝 Credits

**Created by:** [Your Name]  
**Engine:** Python + Pygame  
**Initial code:** AI-assisted rapid prototyping

---

**Let's make this game successful! 🎮💰**
