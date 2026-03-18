# ══════════════════════════════════════════════
#  map.py  –  Génération de la map
# ══════════════════════════════════════════════

import pygame

walls = []
FINISH = pygame.Rect(1800, 460, 60, 90)

def generate_map():
    """Remplit la liste des murs."""
    walls.clear()
    # Bordures
    walls.append(pygame.Rect(0,    0,    2000, 20))
    walls.append(pygame.Rect(0,    1180, 2000, 20))
    walls.append(pygame.Rect(0,    0,    20,   1200))
    walls.append(pygame.Rect(1980, 0,    20,   1200))
    # Plateformes
    walls.append(pygame.Rect(500,  700,  700,  20))
    walls.append(pygame.Rect(200,  200,  20,   500))
    walls.append(pygame.Rect(200,  500,  200,  20))
    walls.append(pygame.Rect(400,  200,  20,   250))
    walls.append(pygame.Rect(1300, 300,  400,  20))
    walls.append(pygame.Rect(1500, 300,  20,   250))
    walls.append(pygame.Rect(1500, 550,  200,  20))
    walls.append(pygame.Rect(1700, 550,  20,   300))
    walls.append(pygame.Rect(300,  350,  120,  20))
    walls.append(pygame.Rect(1650, 420,  120,  20))

    