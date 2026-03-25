import pygame
from .settings import GAME_MAP, TILE_SIZE

class World:
    def __init__(self):
        self.tile_map = GAME_MAP

    def check_collision(self, x, y):
        """ Vérifie si un point x,y touche un mur (1) """
        grid_x = int(x // TILE_SIZE)
        grid_y = int(y // TILE_SIZE)
        
        # Vérifier les limites de la liste pour éviter les crashs
        if 0 <= grid_y < len(self.tile_map) and 0 <= grid_x < len(self.tile_map[0]):
            return self.tile_map[grid_y][grid_x] == 1
        return True # Si on sort de la map, on considère que c'est un mur