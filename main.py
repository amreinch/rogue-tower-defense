#!/usr/bin/env python3
import pygame
import sys
import config
from game import Game

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        
        self.game = Game()
        self.showing_upgrades = False
        
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
                
            # Render
            if self.showing_upgrades:
                self.render_upgrades()
            else:
                self.game.render(self.screen)
                
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
        """Handle clicks on upgrade menu"""
        x, y = pos
        
        # Determine which upgrade was clicked
        start_y = 200
        upgrade_height = 80
        
        upgrade_names = list(config.UNLOCKS.keys())
        
        for i, upgrade_name in enumerate(upgrade_names):
            upgrade_y = start_y + i * upgrade_height
            
            if upgrade_y <= y <= upgrade_y + upgrade_height:
                # Try to purchase
                if self.game.progression.purchase_upgrade(upgrade_name):
                    # Success sound could go here
                    pass
                break
                
    def render_upgrades(self):
        """Render upgrade menu"""
        self.screen.fill((20, 20, 30))
        
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 32)
        tiny_font = pygame.font.Font(None, 24)
        
        # Title
        title = font.render("Meta Progression Upgrades", True, (255, 215, 0))
        self.screen.blit(title, (config.SCREEN_WIDTH // 2 - 250, 50))
        
        # Currency
        currency_text = small_font.render(f"Currency: {self.game.progression.currency}", True, (100, 255, 100))
        self.screen.blit(currency_text, (config.SCREEN_WIDTH // 2 - 100, 120))
        
        # Stats
        stats_y = 150
        stats = [
            f"Best Wave: {self.game.progression.best_wave}",
            f"Total Waves: {self.game.progression.total_waves_completed}",
            f"Total Gold Earned: {self.game.progression.total_gold_earned}"
        ]
        for stat in stats:
            text = tiny_font.render(stat, True, (200, 200, 200))
            self.screen.blit(text, (50, stats_y))
            stats_y += 25
            
        # Upgrades
        y_offset = 250
        upgrade_names = list(config.UNLOCKS.keys())
        
        for upgrade_name in upgrade_names:
            unlock = config.UNLOCKS[upgrade_name]
            current_level = self.game.progression.upgrades.get(upgrade_name, 0)
            cost = self.game.progression.get_upgrade_cost(upgrade_name)
            
            # Name and level
            name_display = upgrade_name.replace("_", " ").title()
            level_text = f"{name_display} (Level {current_level}/{unlock['max_level']})"
            
            can_afford = cost is not None and self.game.progression.currency >= cost
            color = (100, 255, 100) if can_afford else (150, 150, 150)
            
            if cost is None:
                level_text += " [MAXED]"
                color = (255, 215, 0)
            else:
                level_text += f" - Cost: {cost}"
                
            text = small_font.render(level_text, True, color)
            self.screen.blit(text, (100, y_offset))
            
            # Description
            bonus_pct = int(unlock["bonus"] * 100) if unlock["bonus"] < 1 else int(unlock["bonus"])
            desc = f"  +{bonus_pct}% per level"
            desc_text = tiny_font.render(desc, True, (180, 180, 180))
            self.screen.blit(desc_text, (120, y_offset + 35))
            
            y_offset += 80
            
        # Instructions
        inst = tiny_font.render("Click upgrade to purchase | Press U to close | Press R to start new run", True, (200, 200, 200))
        self.screen.blit(inst, (config.SCREEN_WIDTH // 2 - 350, config.SCREEN_HEIGHT - 50))

if __name__ == "__main__":
    app = GameApp()
    app.run()
