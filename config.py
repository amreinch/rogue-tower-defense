# Game Configuration

# Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Rogue Tower Defense"

# Map
MAP_WIDTH = 20
MAP_HEIGHT = 15
TILE_SIZE = 32
PATH_WIDTH = 2

# Colors
COLOR_BG = (34, 32, 52)
COLOR_PATH = (68, 68, 68)
COLOR_BUILDABLE = (52, 101, 36)
COLOR_HEALTH = (220, 38, 38)
COLOR_GOLD = (255, 215, 0)
COLOR_WAVE = (255, 255, 255)

# Towers
TOWER_BASIC = {
    "name": "Basic",
    "cost": 100,
    "damage": 20,
    "range": 120,
    "fire_rate": 1.0,  # shots per second
    "color": (100, 100, 255)
}

TOWER_SNIPER = {
    "name": "Sniper",
    "cost": 250,
    "damage": 100,
    "range": 250,
    "fire_rate": 0.5,
    "color": (255, 50, 50)
}

TOWER_SPLASH = {
    "name": "Splash",
    "cost": 200,
    "damage": 15,
    "range": 100,
    "fire_rate": 0.8,
    "splash_radius": 50,
    "color": (255, 150, 50)
}

TOWER_SLOW = {
    "name": "Slow",
    "cost": 150,
    "damage": 5,
    "range": 130,
    "fire_rate": 2.0,
    "slow_amount": 0.5,  # 50% slow
    "slow_duration": 2.0,  # seconds
    "color": (100, 255, 255)
}

TOWER_TYPES = [TOWER_BASIC, TOWER_SNIPER, TOWER_SPLASH, TOWER_SLOW]

# Enemies
ENEMY_FAST = {
    "name": "Fast",
    "health": 50,
    "speed": 80,  # pixels per second
    "reward": 15,
    "color": (255, 255, 100)
}

ENEMY_TANK = {
    "name": "Tank",
    "health": 300,
    "speed": 30,
    "reward": 50,
    "color": (150, 150, 150)
}

ENEMY_FLYING = {
    "name": "Flying",
    "health": 80,
    "speed": 60,
    "reward": 25,
    "flying": True,
    "color": (200, 100, 255)
}

ENEMY_BOSS = {
    "name": "Boss",
    "health": 1000,
    "speed": 20,
    "reward": 200,
    "color": (255, 50, 50)
}

ENEMY_TYPES = [ENEMY_FAST, ENEMY_TANK, ENEMY_FLYING, ENEMY_BOSS]

# Waves
WAVE_BASE_ENEMIES = 10
WAVE_SCALING = 1.2  # each wave has 20% more enemies
WAVE_DELAY = 3.0  # seconds between waves

# Player
STARTING_HEALTH = 20
STARTING_GOLD = 400

# Meta-Progression
UNLOCKS = {
    "tower_damage": {"cost": 100, "bonus": 0.1, "max_level": 10},
    "tower_range": {"cost": 150, "bonus": 0.1, "max_level": 5},
    "starting_gold": {"cost": 200, "bonus": 50, "max_level": 5},
    "interest": {"cost": 300, "bonus": 0.05, "max_level": 3}  # gain 5% gold per wave
}
