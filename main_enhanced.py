#!/usr/bin/env python3
"""
Enhanced version with better graphics, effects, and UI
Uses sprites if available, otherwise uses polished placeholder graphics
"""
import pygame
import sys
import config
from game import Game
from renderer import Renderer

class EnhancedGameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE + " - Enhanced Graphics")
        self.clock = pygame.time.Clock()
        
        self.game = Game()
        self.renderer = Renderer()
        self.showing_upgrades = False
        
        # Particle effects
        self.particles = []
        
        # UI fonts
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(config.FPS) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        if not self.showing_upgrades:
                            self.game.place_tower(*event.pos)
                        else:
                            self.handle_upgrade_click(event.pos)
                            
            # Update
            if not self.showing_upgrades:
                self.game.update(dt)
                self.update_particles(dt)
                
            # Render
            if self.showing_upgrades:
                self.render_upgrades()
            else:
                self.render_game()
                
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
        
    def handle_keypress(self, key):
        if self.showing_upgrades:
            if key == pygame.K_ESCAPE or key == pygame.K_u:
                self.showing_upgrades = False
            elif key == pygame.K_r:
                self.showing_upgrades = False
                self.game.reset()
            return
            
        # Tower selection (1-4 keys)
        if key == pygame.K_1:
            self.game.selected_tower_type = config.TOWER_TYPES[0]
        elif key == pygame.K_2:
            self.game.selected_tower_type = config.TOWER_TYPES[1]
        elif key == pygame.K_3:
            self.game.selected_tower_type = config.TOWER_TYPES[2]
        elif key == pygame.K_4:
            self.game.selected_tower_type = config.TOWER_TYPES[3]
            
        # Start wave
        elif key == pygame.K_SPACE:
            self.game.start_wave()
            
        # Reset/Upgrades
        elif key == pygame.K_r:
            if self.game.game_over:
                self.game.reset()
        elif key == pygame.K_u:
            if self.game.game_over:
                self.showing_upgrades = True
                
        # Deselect tower
        elif key == pygame.K_ESCAPE:
            self.game.selected_tower_type = None
            
    def handle_upgrade_click(self, pos):
        x, y = pos
        start_y = 200
        upgrade_height = 80
        upgrade_names = list(config.UNLOCKS.keys())
        
        for i, upgrade_name in enumerate(upgrade_names):
            upgrade_y = start_y + i * upgrade_height
            if upgrade_y <= y <= upgrade_y + upgrade_height:
                if self.game.progression.purchase_upgrade(upgrade_name):
                    self.create_particles(x, y, (100, 255, 100), 20)
                break
                
    def render_game(self):
        # Enhanced background with gradient
        for y in range(config.SCREEN_HEIGHT):
            color_factor = y / config.SCREEN_HEIGHT
            color = (
                int(34 + color_factor * 10),
                int(32 + color_factor * 10),
                int(52 + color_factor * 10)
            )
            pygame.draw.line(self.screen, color, (0, y), (config.SCREEN_WIDTH, y))
        
        # Draw grid with enhanced tiles
        for x in range(config.MAP_WIDTH):
            for y in range(config.MAP_HEIGHT):
                if (x, y) in self.game.buildable_tiles:
                    self.renderer.draw_map_tile(self.screen, x, y, 'buildable', config.TILE_SIZE)
                    
        # Draw path with glow effect
        if len(self.game.path) > 1:
            # Glow
            glow_surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(glow_surf, (255, 255, 255, 30), False, self.game.path, config.PATH_WIDTH * config.TILE_SIZE + 10)
            self.screen.blit(glow_surf, (0, 0))
            
            # Path
            pygame.draw.lines(self.screen, (80, 80, 80), False, self.game.path, config.PATH_WIDTH * config.TILE_SIZE)
            pygame.draw.lines(self.screen, (100, 100, 100), False, self.game.path, config.PATH_WIDTH * config.TILE_SIZE - 4)
            
        # Draw towers
        for tower in self.game.towers:
            self.renderer.draw_tower(self.screen, tower)
            # Draw range circle for selected tower type
            if self.game.selected_tower_type == tower.type:
                range_surf = pygame.Surface((int(tower.range*2+4), int(tower.range*2+4)), pygame.SRCALPHA)
                pygame.draw.circle(range_surf, (255, 255, 255, 30), (int(tower.range+2), int(tower.range+2)), int(tower.range))
                pygame.draw.circle(range_surf, (255, 255, 255, 80), (int(tower.range+2), int(tower.range+2)), int(tower.range), 2)
                self.screen.blit(range_surf, (int(tower.x - tower.range - 2), int(tower.y - tower.range - 2)))
            
            # Draw projectiles
            for proj in tower.projectiles:
                self.renderer.draw_projectile(self.screen, proj)
            
        # Draw enemies
        for enemy in self.game.enemies:
            self.renderer.draw_enemy(self.screen, enemy)
            
        # Draw particles
        for particle in self.particles:
            particle['render'](self.screen)
            
        # Draw UI
        self.render_ui_enhanced()
        
    def render_ui_enhanced(self):
        # UI Panel background
        panel_height = 150
        panel_surf = pygame.Surface((config.SCREEN_WIDTH, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (20, 20, 30, 220), (0, 0, config.SCREEN_WIDTH, panel_height))
        pygame.draw.line(panel_surf, (100, 100, 120), (0, 0), (config.SCREEN_WIDTH, 0), 2)
        self.screen.blit(panel_surf, (0, 0))
        
        # Health with icon
        health_text = self.font.render(f"❤ {self.game.health}", True, (255, 100, 100))
        self.screen.blit(health_text, (20, 15))
        
        # Gold with icon  
        gold_text = self.font.render(f"⬤ {self.game.gold}", True, (255, 215, 0))
        self.screen.blit(gold_text, (20, 55))
        
        # Wave with progress
        wave_text = self.font.render(f"Wave {self.game.wave_system.wave_number}", True, (200, 200, 255))
        self.screen.blit(wave_text, (20, 95))
        
        # Tower selection with fancy boxes
        x_offset = 350
        for i, tower_type in enumerate(config.TOWER_TYPES):
            is_selected = self.game.selected_tower_type == tower_type
            can_afford = self.game.gold >= tower_type["cost"]
            
            box_x = x_offset + i * 210
            box_y = 15
            box_w = 200
            box_h = 120
            
            # Box background
            if is_selected:
                box_color = (100, 100, 50, 200)
                border_color = (255, 255, 100)
            elif can_afford:
                box_color = (40, 40, 60, 180)
                border_color = (150, 150, 200)
            else:
                box_color = (30, 30, 40, 180)
                border_color = (80, 80, 90)
                
            box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            pygame.draw.rect(box_surf, box_color, (0, 0, box_w, box_h), border_radius=8)
            pygame.draw.rect(box_surf, border_color, (0, 0, box_w, box_h), 3, border_radius=8)
            self.screen.blit(box_surf, (box_x, box_y))
            
            # Tower preview (mini version)
            preview_x = box_x + box_w // 2
            preview_y = box_y + 35
            preview_color = tower_type['color']
            
            # Shadow
            pygame.draw.circle(self.screen, (0, 0, 0, 60), (preview_x+2, preview_y+2), 20)
            # Tower
            pygame.draw.circle(self.screen, preview_color, (preview_x, preview_y), 20)
            pygame.draw.circle(self.screen, (255, 255, 255), (preview_x, preview_y), 20, 2)
            
            # Name and cost
            name_color = (255, 255, 255) if can_afford else (120, 120, 120)
            name_text = self.small_font.render(f"{i+1}. {tower_type['name']}", True, name_color)
            name_rect = name_text.get_rect(centerx=box_x + box_w//2, y=box_y + 75)
            self.screen.blit(name_text, name_rect)
            
            cost_text = self.tiny_font.render(f"${tower_type['cost']}", True, (255, 215, 0))
            cost_rect = cost_text.get_rect(centerx=box_x + box_w//2, y=box_y + 98)
            self.screen.blit(cost_text, cost_rect)
            
        # Start wave button
        if self.game.wave_system.can_start_wave():
            button_w = 300
            button_h = 50
            button_x = config.SCREEN_WIDTH // 2 - button_w // 2
            button_y = config.SCREEN_HEIGHT - 80
            
            # Pulsing effect
            pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
            glow_size = int(10 * pulse)
            
            # Glow
            glow_surf = pygame.Surface((button_w + glow_size*2, button_h + glow_size*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (100, 255, 100, 60), (glow_size, glow_size, button_w, button_h), border_radius=25)
            self.screen.blit(glow_surf, (button_x - glow_size, button_y - glow_size))
            
            # Button
            pygame.draw.rect(self.screen, (50, 150, 50), (button_x, button_y, button_w, button_h), border_radius=25)
            pygame.draw.rect(self.screen, (100, 255, 100), (button_x, button_y, button_w, button_h), 3, border_radius=25)
            
            button_text = self.font.render("START WAVE (SPACE)", True, (255, 255, 255))
            text_rect = button_text.get_rect(center=(config.SCREEN_WIDTH // 2, button_y + button_h // 2))
            self.screen.blit(button_text, text_rect)
            
        # Game over overlay
        if self.game.game_over:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 180), (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.screen.blit(overlay, (0, 0))
            
            # Game over text with shadow
            game_over_text = self.title_font.render("GAME OVER", True, (255, 50, 50))
            shadow_text = self.title_font.render("GAME OVER", True, (100, 0, 0))
            text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            self.screen.blit(shadow_text, shadow_rect)
            self.screen.blit(game_over_text, text_rect)
            
            wave_text = self.font.render(f"Reached Wave {self.game.wave_system.wave_number}", True, (255, 255, 255))
            wave_rect = wave_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(wave_text, wave_rect)
            
            restart_text = self.small_font.render("Press R to restart | Press U for upgrades", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(restart_text, restart_rect)
            
    def render_upgrades(self):
        # Same as main.py but with enhanced styling
        self.screen.fill((20, 20, 30))
        
        # Title with gradient
        title = self.title_font.render("Meta Progression", True, (255, 215, 0))
        title_shadow = self.title_font.render("Meta Progression", True, (100, 80, 0))
        self.screen.blit(title_shadow, (config.SCREEN_WIDTH // 2 - 248, 52))
        self.screen.blit(title, (config.SCREEN_WIDTH // 2 - 250, 50))
        
        # Currency display
        currency_text = self.font.render(f"Currency: {self.game.progression.currency}", True, (100, 255, 100))
        self.screen.blit(currency_text, (config.SCREEN_WIDTH // 2 - 100, 120))
        
        # Stats
        stats_y = 180
        stats = [
            f"Best Wave: {self.game.progression.best_wave}",
            f"Total Waves: {self.game.progression.total_waves_completed}",
            f"Total Gold: {self.game.progression.total_gold_earned}"
        ]
        for stat in stats:
            text = self.tiny_font.render(stat, True, (200, 200, 200))
            self.screen.blit(text, (100, stats_y))
            stats_y += 25
            
        # Upgrades
        y_offset = 250
        upgrade_names = list(config.UNLOCKS.keys())
        
        for upgrade_name in upgrade_names:
            unlock = config.UNLOCKS[upgrade_name]
            current_level = self.game.progression.upgrades.get(upgrade_name, 0)
            cost = self.game.progression.get_upgrade_cost(upgrade_name)
            
            # Upgrade box
            box_w = config.SCREEN_WIDTH - 200
            box_h = 70
            box_x = 100
            box_y = y_offset
            
            can_afford = cost is not None and self.game.progression.currency >= cost
            
            if cost is None:
                box_color = (80, 80, 30, 200)
                border_color = (255, 215, 0)
            elif can_afford:
                box_color = (40, 80, 40, 200)
                border_color = (100, 255, 100)
            else:
                box_color = (40, 40, 50, 200)
                border_color = (100, 100, 120)
                
            box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            pygame.draw.rect(box_surf, box_color, (0, 0, box_w, box_h), border_radius=10)
            pygame.draw.rect(box_surf, border_color, (0, 0, box_w, box_h), 3, border_radius=10)
            self.screen.blit(box_surf, (box_x, box_y))
            
            # Text
            name_display = upgrade_name.replace("_", " ").title()
            level_text = f"{name_display} (Level {current_level}/{unlock['max_level']})"
            
            if cost is None:
                level_text += " [MAXED]"
                text_color = (255, 215, 0)
            else:
                level_text += f" - Cost: {cost}"
                text_color = (255, 255, 255) if can_afford else (150, 150, 150)
                
            text = self.small_font.render(level_text, True, text_color)
            self.screen.blit(text, (box_x + 20, box_y + 15))
            
            # Description
            bonus_pct = int(unlock["bonus"] * 100) if unlock["bonus"] < 1 else int(unlock["bonus"])
            desc = f"+{bonus_pct}% per level"
            desc_text = self.tiny_font.render(desc, True, (180, 180, 180))
            self.screen.blit(desc_text, (box_x + 20, box_y + 45))
            
            y_offset += 80
            
        # Instructions
        inst = self.tiny_font.render("Click upgrade to purchase | Press U to close | Press R for new run", True, (200, 200, 200))
        self.screen.blit(inst, (config.SCREEN_WIDTH // 2 - 350, config.SCREEN_HEIGHT - 50))
        
    def update_particles(self, dt):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
            else:
                particle['update'](dt)
                
    def create_particles(self, x, y, color, count):
        """Create particle burst"""
        import random
        for _ in range(count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(50, 150)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            
            particle = {
                'x': x,
                'y': y,
                'vx': vx,
                'vy': vy,
                'life': 1.0,
                'color': color,
                'update': lambda dt, p=locals(): self._update_particle(p, dt),
                'render': lambda screen, p=locals(): self._render_particle(screen, p)
            }
            self.particles.append(particle)
            
    def _update_particle(self, p, dt):
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt
        p['vy'] += 200 * dt  # gravity
        
    def _render_particle(self, screen, p):
        alpha = int(255 * p['life'])
        size = int(4 * p['life'])
        if size > 0:
            surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p['color'], alpha), (size, size), size)
            screen.blit(surf, (int(p['x'] - size), int(p['y'] - size)))

if __name__ == "__main__":
    import math  # needed for particles
    app = EnhancedGameApp()
    app.run()
