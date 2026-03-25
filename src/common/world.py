import pygame
from .settings import GAME_MAP, TILE_SIZE

class World:
    def __init__(self):
        # On utilise la map chargée depuis l'image
        self.tile_map = GAME_MAP

    def check_collision(self, x, y):
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        # Vérification des limites de la liste pour éviter les crashs
        if 0 <= grid_y < len(self.tile_map) and 0 <= grid_x < len(self.tile_map[0]):
            # Renvoie True si c'est un mur (1) ou un pic (2)
            return self.tile_map[grid_y][grid_x] > 0
        return True # On considère le hors-map comme un mur