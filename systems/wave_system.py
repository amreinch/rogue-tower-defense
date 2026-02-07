import random
import config
from entities.enemy import Enemy

class WaveSystem:
    def __init__(self, path):
        self.path = path
        self.wave_number = 0
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.wave_active = False
        self.wave_delay = config.WAVE_DELAY
        self.delay_timer = 0
        
    def start_next_wave(self):
        if self.wave_active:
            return
            
        self.wave_number += 1
        self.wave_active = True
        
        # Calculate enemy composition
        enemy_count = int(config.WAVE_BASE_ENEMIES * (config.WAVE_SCALING ** (self.wave_number - 1)))
        
        self.enemies_to_spawn = []
        
        # Early waves: mostly fast enemies
        if self.wave_number < 5:
            for _ in range(enemy_count):
                self.enemies_to_spawn.append(config.ENEMY_FAST)
                
        # Mid waves: mix of types
        elif self.wave_number < 10:
            for _ in range(enemy_count):
                enemy_type = random.choices(
                    [config.ENEMY_FAST, config.ENEMY_TANK, config.ENEMY_FLYING],
                    weights=[50, 30, 20]
                )[0]
                self.enemies_to_spawn.append(enemy_type)
                
        # Late waves: harder enemies + bosses
        else:
            for _ in range(enemy_count):
                enemy_type = random.choices(
                    [config.ENEMY_FAST, config.ENEMY_TANK, config.ENEMY_FLYING, config.ENEMY_BOSS],
                    weights=[30, 35, 25, 10]
                )[0]
                self.enemies_to_spawn.append(enemy_type)
                
        # Boss every 5 waves
        if self.wave_number % 5 == 0:
            for _ in range(self.wave_number // 5):
                self.enemies_to_spawn.append(config.ENEMY_BOSS)
                
        random.shuffle(self.enemies_to_spawn)
        self.spawn_timer = 0.5  # spawn one every 0.5 seconds
        
    def update(self, dt, enemies):
        if not self.wave_active:
            # Delay between waves
            self.delay_timer += dt
            return None
            
        # Spawn enemies
        if self.enemies_to_spawn:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                enemy_type = self.enemies_to_spawn.pop(0)
                enemy = Enemy(enemy_type, self.path, self.wave_number)
                enemies.append(enemy)
                self.spawn_timer = 0.5
                
        # Check if wave complete
        if not self.enemies_to_spawn and not any(e.alive and not e.reached_end for e in enemies):
            self.wave_active = False
            self.delay_timer = 0
            return "wave_complete"
            
        return None
        
    def can_start_wave(self):
        return not self.wave_active and self.delay_timer >= self.wave_delay
