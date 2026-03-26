import pygame
from .settings import TILE_SIZE 

class World:
    def __init__(self):
        # On importe ici pour éviter l'erreur "cannot import name GAME_MAP"
        from .settings import GAME_MAP
        self.tile_map = GAME_MAP

    def check_collision(self, x, y):
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        if 0 <= grid_y < len(self.tile_map) and 0 <= grid_x < len(self.tile_map[0]):
            # Mur (1) ou Pic (2)
            return self.tile_map[grid_y][grid_x] > 0
        return True