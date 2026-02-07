import pygame
import math

class Enemy:
    def __init__(self, enemy_type, path, wave_num=1):
        self.type = enemy_type
        self.path = path
        self.path_index = 0
        
        # Scale health with wave number
        self.max_health = enemy_type["health"] * (1 + (wave_num - 1) * 0.15)
        self.health = self.max_health
        self.speed = enemy_type["speed"]
        self.reward = enemy_type["reward"]
        self.color = enemy_type["color"]
        self.name = enemy_type["name"]
        self.flying = enemy_type.get("flying", False)
        
        # Position
        start = path[0]
        self.x = start[0]
        self.y = start[1]
        
        # State
        self.alive = True
        self.reached_end = False
        self.slow_amount = 0
        self.slow_timer = 0
        
    def update(self, dt):
        if not self.alive or self.reached_end:
            return
            
        # Update slow
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_amount = 0
                
        # Move along path
        current_speed = self.speed * (1 - self.slow_amount)
        
        if self.path_index >= len(self.path):
            self.reached_end = True
            return
            
        target = self.path[self.path_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = math.hypot(dx, dy)
        
        if dist < current_speed * dt:
            # Reached waypoint
            self.x = target[0]
            self.y = target[1]
            self.path_index += 1
        else:
            # Move towards waypoint
            self.x += (dx / dist) * current_speed * dt
            self.y += (dy / dist) * current_speed * dt
            
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True  # died
        return False
        
    def apply_slow(self, amount, duration):
        self.slow_amount = max(self.slow_amount, amount)
        self.slow_timer = max(self.slow_timer, duration)
        
    def render(self, screen):
        if not self.alive:
            return
            
        # Draw enemy
        size = 10 if not self.flying else 8
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
        
        # Draw health bar
        bar_width = 20
        bar_height = 3
        health_pct = self.health / self.max_health
        
        bar_x = int(self.x - bar_width // 2)
        bar_y = int(self.y - 15)
        
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width * health_pct), bar_height))
        
        # Draw slow indicator
        if self.slow_amount > 0:
            pygame.draw.circle(screen, (100, 255, 255), (int(self.x), int(self.y)), size, 2)
