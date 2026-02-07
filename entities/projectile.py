import pygame
import math

class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, tower_type):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.tower_type = tower_type
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            self.vx = (dx / dist) * 400  # projectile speed
            self.vy = (dy / dist) * 400
        else:
            self.vx = 0
            self.vy = 0
            
        self.alive = True
        self.max_distance = 500
        self.traveled = 0
        
    def update(self, dt):
        if not self.alive:
            return
            
        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.traveled += abs(self.vx * dt) + abs(self.vy * dt)
        
        # Check if traveled too far
        if self.traveled > self.max_distance:
            self.alive = False
            
    def check_hit(self, enemies):
        if not self.alive:
            return
            
        hits = []
        
        for enemy in enemies:
            if not enemy.alive:
                continue
                
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            
            # Direct hit
            if dist < 15:
                hits.append(enemy)
                
                # Splash damage
                if "splash_radius" in self.tower_type:
                    for other in enemies:
                        if other != enemy and other.alive:
                            splash_dist = math.hypot(other.x - enemy.x, other.y - enemy.y)
                            if splash_dist < self.tower_type["splash_radius"]:
                                hits.append(other)
                                
                self.alive = False
                break
                
        return hits
        
    def render(self, screen):
        if not self.alive:
            return
            
        color = self.tower_type.get("color", (255, 255, 255))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 4)
