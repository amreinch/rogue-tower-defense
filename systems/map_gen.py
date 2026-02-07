import random
import config

def generate_path():
    """Generate a random path from left to right"""
    path = []
    
    # Start on left side
    y = random.randint(3, config.MAP_HEIGHT - 3)
    path.append((1, y))
    
    x = 2
    direction = random.choice([-1, 0, 1])  # up, straight, down
    
    while x < config.MAP_WIDTH - 1:
        # Occasionally change direction
        if random.random() < 0.3:
            direction = random.choice([-1, 0, 1])
            
        # Move
        y += direction
        y = max(2, min(config.MAP_HEIGHT - 2, y))  # stay in bounds
        
        path.append((x, y))
        x += 1
        
    # Convert to pixel coordinates
    pixel_path = [(px * config.TILE_SIZE + config.TILE_SIZE // 2,
                   py * config.TILE_SIZE + config.TILE_SIZE // 2)
                  for px, py in path]
    
    return pixel_path

def get_buildable_tiles(path):
    """Return list of tiles where towers can be placed"""
    # Convert path to tile coordinates
    path_tiles = set()
    for px, py in path:
        tx = px // config.TILE_SIZE
        ty = py // config.TILE_SIZE
        path_tiles.add((tx, ty))
        # Add adjacent tiles to path (for wider path)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                path_tiles.add((tx + dx, ty + dy))
    
    # All tiles except path are buildable
    buildable = []
    for x in range(config.MAP_WIDTH):
        for y in range(config.MAP_HEIGHT):
            if (x, y) not in path_tiles:
                buildable.append((x, y))
                
    return buildable
