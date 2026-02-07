# Graphics Upgrade Guide

## Free Asset Packs (Download & Drop In)

### Recommended FREE Tower Defense Asset Packs

**1. Kenney Tower Defense Pack (BEST)**
- **Link:** https://kenney.nl/assets/tower-defense-kit
- **License:** CC0 (Public Domain - use anywhere!)
- **Includes:** Towers, enemies, tiles, UI
- **Quality:** Professional, consistent style
- **Format:** PNG sprites, perfect for Pygame

**2. OpenGameArt Tower Defense**
- **Link:** https://opengameart.org/content/tower-defense-game-kit
- **License:** CC0/CC-BY
- **Includes:** Multiple tower/enemy sets

**3. Itch.io Free TD Assets**
- **Search:** https://itch.io/game-assets/free/tag-tower-defense
- **Many options:** Various styles (pixel art, vectors, 3D renders)

---

## How to Use (Drop-In System)

### Step 1: Download Kenney Pack
1. Go to https://kenney.nl/assets/tower-defense-kit
2. Click "Download" (free, no account needed)
3. Extract ZIP
4. Copy PNG files to `assets/sprites/` folder

### Step 2: Run the Upgraded Version
```bash
python main_enhanced.py  # I'll create this with sprite support
```

### Step 3: Customize
- Edit `assets/config.json` to map sprites to game objects
- Or manually edit sprite paths in code

---

## Sprite Naming Convention

Place these in `assets/sprites/`:

**Towers:**
- `tower_basic.png` (64x64)
- `tower_sniper.png` (64x64)
- `tower_splash.png` (64x64)
- `tower_slow.png` (64x64)

**Enemies:**
- `enemy_fast.png` (32x32)
- `enemy_tank.png` (48x48)
- `enemy_flying.png` (32x32)
- `enemy_boss.png` (64x64)

**Projectiles:**
- `projectile_bullet.png` (8x8)
- `projectile_missile.png` (16x16)
- `projectile_magic.png` (12x12)

**Tiles:**
- `tile_grass.png` (32x32)
- `tile_path.png` (32x32)
- `tile_buildable.png` (32x32)

**UI:**
- `ui_panel.png`
- `ui_button.png`
- `ui_icon_health.png`
- `ui_icon_gold.png`

---

## Alternative: Use My Enhanced Placeholder Graphics

I'll create an enhanced version with:
- Gradient circles (looks way better)
- Shadows and outlines
- Better colors
- Nicer UI
- Particle effects

**Still simple but looks 10x better!**

Run: `python main_enhanced.py`

---

## Professional Look Checklist

- [ ] Download Kenney Tower Defense pack
- [ ] Place sprites in assets/sprites/
- [ ] Run enhanced version
- [ ] Tweak colors/effects to taste
- [ ] Add sound effects
- [ ] Done! Looks professional

---

**I'm creating main_enhanced.py now with much better graphics...**
