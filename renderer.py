import pygame
import math
import os

class Renderer:
    """Enhanced rendering with sprites or improved shapes"""
    
    def __init__(self):
        self.sprites = {}
        self.use_sprites = self._load_sprites()
        
    def _load_sprites(self):
        """Try to load sprites, fall back to enhanced shapes if not found"""
        sprite_paths = {
            'tower_basic': 'assets/sprites/tower_basic.png',
            'tower_sniper': 'assets/sprites/tower_sniper.png',
            'tower_splash': 'assets/sprites/tower_splash.png',
            'tower_slow': 'assets/sprites/tower_slow.png',
            'enemy_fast': 'assets/sprites/enemy_fast.png',
            'enemy_tank': 'assets/sprites/enemy_tank.png',
            'enemy_flying': 'assets/sprites/enemy_flying.png',
            'enemy_boss': 'assets/sprites/enemy_boss.png',
        }
        
        loaded = 0
        for name, path in sprite_paths.items():
            if os.path.exists(path):
                try:
                    self.sprites[name] = pygame.image.load(path).convert_alpha()
                    loaded += 1
                except:
                    pass
                    
        return loaded > 0
        
    def draw_tower(self, screen, tower):
        """Draw tower with sprite or enhanced shape"""
        x, y = int(tower.x), int(tower.y)
        
        sprite_name = f"tower_{tower.name.lower()}"
        if sprite_name in self.sprites:
            sprite = self.sprites[sprite_name]
            rect = sprite.get_rect(center=(x, y))
            screen.blit(sprite, rect)
        else:
            # Enhanced shape rendering
            self._draw_enhanced_tower(screen, tower)
            
    def _draw_enhanced_tower(self, screen, tower):
        """Draw tower with gradients and shadows"""
        x, y = int(tower.x), int(tower.y)
        
        # Shadow
        shadow_color = (0, 0, 0, 60)
        shadow_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, shadow_color, (15, 15), 15)
        screen.blit(shadow_surf, (x - 15 + 2, y - 15 + 2))
        
        # Base
        base_color = self._darken_color(tower.color, 0.7)
        pygame.draw.circle(screen, base_color, (x, y), 18)
        
        # Main body with gradient effect
        for i in range(5):
            radius = 16 - i
            color = self._lerp_color(tower.color, (255, 255, 255), i * 0.1)
            pygame.draw.circle(screen, color, (x - i//2, y - i//2), radius)
            
        # Border/outline
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 16, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 17, 1)
        
        # Type indicator (small icon in center)
        indicator_colors = {
            'Basic': (255, 255, 100),
            'Sniper': (255, 100, 100),
            'Splash': (255, 180, 100),
            'Slow': (100, 255, 255)
        }
        indicator_color = indicator_colors.get(tower.name, (255, 255, 255))
        pygame.draw.circle(screen, indicator_color, (x, y), 6)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 6, 1)
        
    def draw_enemy(self, screen, enemy):
        """Draw enemy with sprite or enhanced shape"""
        if not enemy.alive:
            return
            
        x, y = int(enemy.x), int(enemy.y)
        
        sprite_name = f"enemy_{enemy.name.lower()}"
        if sprite_name in self.sprites:
            sprite = self.sprites[sprite_name]
            rect = sprite.get_rect(center=(x, y))
            screen.blit(sprite, rect)
        else:
            self._draw_enhanced_enemy(screen, enemy)
            
        # Always draw health bar
        self._draw_health_bar(screen, enemy)
        
    def _draw_enhanced_enemy(self, screen, enemy):
        """Draw enemy with enhanced graphics"""
        x, y = int(enemy.x), int(enemy.y)
        size = 12 if not enemy.flying else 10
        
        # Shadow
        if not enemy.flying:
            shadow_surf = pygame.Surface((size*2+4, size*2+4), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surf, (0, 0, 0, 40), (size+2, size+2), size)
            screen.blit(shadow_surf, (x-size-2+2, y-size-2+2))
        
        # Body with gradient
        base_color = self._darken_color(enemy.color, 0.8)
        pygame.draw.circle(screen, base_color, (x, y), size)
        
        for i in range(3):
            radius = size - i - 2
            if radius > 0:
                color = self._lerp_color(enemy.color, (255, 255, 255), i * 0.2)
                pygame.draw.circle(screen, color, (x-i, y-i), radius)
        
        # Outline
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), size+1, 1)
        
        # Flying indicator
        if enemy.flying:
            wing_offset = int(math.sin(pygame.time.get_ticks() * 0.01) * 3)
            pygame.draw.circle(screen, (200, 200, 255), (x-size, y+wing_offset), 3)
            pygame.draw.circle(screen, (200, 200, 255), (x+size, y+wing_offset), 3)
            
        # Slow effect
        if enemy.slow_amount > 0:
            for angle in range(0, 360, 60):
                rad = math.radians(angle + pygame.time.get_ticks() * 0.1)
                px = x + math.cos(rad) * (size + 4)
                py = y + math.sin(rad) * (size + 4)
                pygame.draw.circle(screen, (100, 255, 255), (int(px), int(py)), 2)
                
    def _draw_health_bar(self, screen, enemy):
        """Draw health bar above enemy"""
        x, y = int(enemy.x), int(enemy.y)
        bar_width = 24
        bar_height = 4
        health_pct = enemy.health / enemy.max_health
        
        bar_x = x - bar_width // 2
        bar_y = y - 18
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x-1, bar_y-1, bar_width+2, bar_height+2))
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))
        
        # Health (gradient from green to red)
        health_color = self._lerp_color((255, 50, 50), (50, 255, 50), health_pct)
        health_width = int(bar_width * health_pct)
        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x-1, bar_y-1, bar_width+2, bar_height+2), 1)
        
    def draw_projectile(self, screen, proj):
        """Draw projectile with trail effect"""
        if not proj.alive:
            return
            
        x, y = int(proj.x), int(proj.y)
        color = proj.tower_type.get('color', (255, 255, 255))
        
        # Trail effect
        trail_length = 3
        for i in range(trail_length):
            trail_x = x - int(proj.vx * 0.01 * i)
            trail_y = y - int(proj.vy * 0.01 * i)
            trail_alpha = 150 - i * 40
            trail_color = (*color, trail_alpha)
            trail_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, trail_color, (4, 4), 4 - i)
            screen.blit(trail_surf, (trail_x-4, trail_y-4))
        
        # Main projectile
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
        pygame.draw.circle(screen, color, (x, y), 4)
        pygame.draw.circle(screen, self._lighten_color(color, 1.5), (x-1, y-1), 2)
        
    def draw_map_tile(self, screen, x, y, tile_type, tile_size):
        """Draw enhanced map tiles"""
        rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        
        if tile_type == 'buildable':
            # Grass-like pattern
            base_color = (52, 101, 36)
            color_var = ((x + y) * 7) % 20 - 10
            color = (
                max(0, min(255, base_color[0] + color_var)),
                max(0, min(255, base_color[1] + color_var)),
                max(0, min(255, base_color[2] + color_var))
            )
            pygame.draw.rect(screen, color, rect)
            
            # Checkerboard subtle pattern
            if (x + y) % 2 == 0:
                overlay = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                pygame.draw.rect(overlay, (255, 255, 255, 10), (0, 0, tile_size, tile_size))
                screen.blit(overlay, rect)
                
        # Grid lines
        pygame.draw.rect(screen, (0, 0, 0, 30), rect, 1)
        
    def _lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t)
        )
        
    def _darken_color(self, color, factor):
        """Darken a color"""
        return (
            int(color[0] * factor),
            int(color[1] * factor),
            int(color[2] * factor)
        )
        
    def _lighten_color(self, color, factor):
        """Lighten a color"""
        return (
            min(255, int(color[0] * factor)),
            min(255, int(color[1] * factor)),
            min(255, int(color[2] * factor))
        )
