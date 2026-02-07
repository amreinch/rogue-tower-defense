import pygame
import math
from entities.projectile import Projectile
import config

class Tower:
    def __init__(self, x, y, tower_type, upgrades=None):
        self.x = x
        self.y = y
        self.type = tower_type
        self.upgrades = upgrades or {}
        
        # Base stats
        self.damage = tower_type["damage"]
        self.range = tower_type["range"]
        self.fire_rate = tower_type["fire_rate"]
        self.color = tower_type["color"]
        self.name = tower_type["name"]
        
        # Apply upgrades
        damage_bonus = self.upgrades.get("tower_damage", 0) * 0.1
        range_bonus = self.upgrades.get("tower_range", 0) * 0.1
        
        self.damage *= (1 + damage_bonus)
        self.range *= (1 + range_bonus)
        
        # State
        self.target = None
        self.cooldown = 0
        self.projectiles = []
        
    def update(self, dt, enemies):
        # Update cooldown
        if self.cooldown > 0:
            self.cooldown -= dt
            
        # Update projectiles
        for proj in self.projectiles[:]:
            proj.update(dt)
            if not proj.alive:
                self.projectiles.remove(proj)
                
        # Find target
        self.target = self._find_target(enemies)
        
        # Shoot if ready
        if self.target and self.cooldown <= 0:
            self._shoot()
            self.cooldown = 1.0 / self.fire_rate
            
    def _find_target(self, enemies):
        # Find closest enemy in range
        closest = None
        min_dist = float('inf')
        
        for enemy in enemies:
            # Skip flying enemies if tower can't target them
            if enemy.flying and not self.type.get("flying", False):
                if self.name != "Sniper":  # snipers can hit flying
                    continue
                    
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range and dist < min_dist:
                closest = enemy
                min_dist = dist
                
        return closest
        
    def _shoot(self):
        proj = Projectile(
            self.x, self.y,
            self.target.x, self.target.y,
            self.damage,
            self.type
        )
        self.projectiles.append(proj)
        
    def render(self, screen):
        # Draw range (when selected)
        # pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), int(self.range), 1)
        
        # Draw tower
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 12)
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), 12, 2)
        
        # Draw projectiles
        for proj in self.projectiles:
            proj.render(screen)
            
    def get_cost(self):
        return self.type["cost"]
