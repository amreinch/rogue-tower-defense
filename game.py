import pygame
import config
from systems.map_gen import generate_path, get_buildable_tiles
from systems.wave_system import WaveSystem
from systems.progression import Progression
from entities.tower import Tower
from entities.enemy import Enemy

class Game:
    def __init__(self):
        # Meta-progression
        self.progression = Progression()
        
        # Game state
        self.reset()
        
    def reset(self):
        """Start new run"""
        self.health = config.STARTING_HEALTH
        self.gold = self.progression.get_starting_gold()
        self.total_gold_earned = 0
        
        # Generate map
        self.path = generate_path()
        self.buildable_tiles = get_buildable_tiles(self.path)
        
        # Game objects
        self.towers = []
        self.enemies = []
        self.wave_system = WaveSystem(self.path)
        
        # UI state
        self.selected_tower_type = None
        self.game_over = False
        self.victory = False
        
    def update(self, dt):
        if self.game_over:
            return
            
        # Update towers
        for tower in self.towers:
            tower.update(dt, self.enemies)
            
            # Check projectile hits
            for proj in tower.projectiles:
                hits = proj.check_hit(self.enemies)
                for enemy in hits:
                    died = enemy.take_damage(proj.damage)
                    
                    # Apply slow effect
                    if "slow_amount" in tower.type:
                        enemy.apply_slow(
                            tower.type["slow_amount"],
                            tower.type["slow_duration"]
                        )
                    
                    # Award gold on kill
                    if died:
                        self.gold += enemy.reward
                        self.total_gold_earned += enemy.reward
                        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt)
            
            if enemy.reached_end:
                self.health -= 1
                self.enemies.remove(enemy)
                if self.health <= 0:
                    self.game_over = True
                    self.progression.end_run(self.wave_system.wave_number, self.total_gold_earned)
                    
            elif not enemy.alive:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                    
        # Update wave system
        result = self.wave_system.update(dt, self.enemies)
        
        if result == "wave_complete":
            # Award interest bonus
            interest_level = self.progression.upgrades.get("interest", 0)
            if interest_level > 0:
                bonus = int(self.gold * interest_level * 0.05)
                self.gold += bonus
                
    def place_tower(self, mouse_x, mouse_y):
        if not self.selected_tower_type or self.game_over:
            return
            
        # Convert to tile coordinates
        tile_x = mouse_x // config.TILE_SIZE
        tile_y = mouse_y // config.TILE_SIZE
        
        # Check if buildable
        if (tile_x, tile_y) not in self.buildable_tiles:
            return
            
        # Check if already occupied
        pixel_x = tile_x * config.TILE_SIZE + config.TILE_SIZE // 2
        pixel_y = tile_y * config.TILE_SIZE + config.TILE_SIZE // 2
        
        for tower in self.towers:
            if abs(tower.x - pixel_x) < config.TILE_SIZE and abs(tower.y - pixel_y) < config.TILE_SIZE:
                return  # spot taken
                
        # Check cost
        if self.gold < self.selected_tower_type["cost"]:
            return
            
        # Place tower
        tower = Tower(pixel_x, pixel_y, self.selected_tower_type, self.progression.get_upgrades_dict())
        self.towers.append(tower)
        self.gold -= tower.get_cost()
        
    def start_wave(self):
        if self.wave_system.can_start_wave():
            self.wave_system.start_next_wave()
            
    def render(self, screen):
        # Background
        screen.fill(config.COLOR_BG)
        
        # Draw grid
        for x in range(config.MAP_WIDTH):
            for y in range(config.MAP_HEIGHT):
                rect = pygame.Rect(
                    x * config.TILE_SIZE,
                    y * config.TILE_SIZE,
                    config.TILE_SIZE,
                    config.TILE_SIZE
                )
                
                if (x, y) in self.buildable_tiles:
                    pygame.draw.rect(screen, config.COLOR_BUILDABLE, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                
        # Draw path
        if len(self.path) > 1:
            pygame.draw.lines(screen, config.COLOR_PATH, False, self.path, config.PATH_WIDTH * config.TILE_SIZE)
            
        # Draw towers
        for tower in self.towers:
            tower.render(screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.render(screen)
            
        # Draw UI
        self._render_ui(screen)
        
    def _render_ui(self, screen):
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Health
        health_text = font.render(f"Health: {self.health}", True, config.COLOR_HEALTH)
        screen.blit(health_text, (10, 10))
        
        # Gold
        gold_text = font.render(f"Gold: {self.gold}", True, config.COLOR_GOLD)
        screen.blit(gold_text, (10, 50))
        
        # Wave
        wave_text = font.render(f"Wave: {self.wave_system.wave_number}", True, config.COLOR_WAVE)
        screen.blit(wave_text, (10, 90))
        
        # Tower selection
        y_offset = 140
        for i, tower_type in enumerate(config.TOWER_TYPES):
            is_selected = self.selected_tower_type == tower_type
            color = (255, 255, 0) if is_selected else (200, 200, 200)
            
            can_afford = self.gold >= tower_type["cost"]
            if not can_afford:
                color = (100, 100, 100)
                
            text = small_font.render(
                f"{i+1}. {tower_type['name']} (${tower_type['cost']})",
                True, color
            )
            screen.blit(text, (10, y_offset + i * 30))
            
        # Start wave button
        if self.wave_system.can_start_wave():
            button_text = font.render("Press SPACE to start wave", True, (0, 255, 0))
            screen.blit(button_text, (config.SCREEN_WIDTH // 2 - 200, config.SCREEN_HEIGHT - 50))
            
        # Game over
        if self.game_over:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            wave_text = font.render(f"Reached Wave {self.wave_system.wave_number}", True, (255, 255, 255))
            restart_text = small_font.render("Press R to restart or U for upgrades", True, (255, 255, 255))
            
            screen.blit(game_over_text, (config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT // 2 - 50))
            screen.blit(wave_text, (config.SCREEN_WIDTH // 2 - 150, config.SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (config.SCREEN_WIDTH // 2 - 200, config.SCREEN_HEIGHT // 2 + 50))
