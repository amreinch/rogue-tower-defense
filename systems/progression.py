import json
import os
import config

class Progression:
    def __init__(self):
        self.save_file = "progression.json"
        self.currency = 0  # earned across runs
        self.upgrades = {key: 0 for key in config.UNLOCKS.keys()}
        self.total_waves_completed = 0
        self.best_wave = 0
        self.total_gold_earned = 0
        
        self.load()
        
    def load(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.currency = data.get("currency", 0)
                    self.upgrades = data.get("upgrades", self.upgrades)
                    self.total_waves_completed = data.get("total_waves", 0)
                    self.best_wave = data.get("best_wave", 0)
                    self.total_gold_earned = data.get("total_gold", 0)
            except:
                pass
                
    def save(self):
        data = {
            "currency": self.currency,
            "upgrades": self.upgrades,
            "total_waves": self.total_waves_completed,
            "best_wave": self.best_wave,
            "total_gold": self.total_gold_earned
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def end_run(self, wave_reached, gold_earned):
        """Called when player dies"""
        # Award currency based on performance
        self.currency += wave_reached * 10 + gold_earned // 10
        
        self.total_waves_completed += wave_reached
        if wave_reached > self.best_wave:
            self.best_wave = wave_reached
            
        self.total_gold_earned += gold_earned
        self.save()
        
    def purchase_upgrade(self, upgrade_name):
        """Try to purchase an upgrade"""
        if upgrade_name not in config.UNLOCKS:
            return False
            
        unlock = config.UNLOCKS[upgrade_name]
        current_level = self.upgrades.get(upgrade_name, 0)
        
        if current_level >= unlock["max_level"]:
            return False  # maxed out
            
        cost = unlock["cost"] * (current_level + 1)
        
        if self.currency >= cost:
            self.currency -= cost
            self.upgrades[upgrade_name] = current_level + 1
            self.save()
            return True
            
        return False
        
    def get_upgrade_cost(self, upgrade_name):
        if upgrade_name not in config.UNLOCKS:
            return 0
        unlock = config.UNLOCKS[upgrade_name]
        current_level = self.upgrades.get(upgrade_name, 0)
        if current_level >= unlock["max_level"]:
            return None  # maxed
        return unlock["cost"] * (current_level + 1)
        
    def get_starting_gold(self):
        base = config.STARTING_GOLD
        bonus = self.upgrades.get("starting_gold", 0) * config.UNLOCKS["starting_gold"]["bonus"]
        return int(base + bonus)
        
    def get_upgrades_dict(self):
        """Return upgrades as dict for tower creation"""
        return self.upgrades.copy()
