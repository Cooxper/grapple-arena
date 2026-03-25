import pygame
import os

TILE_SIZE = 32
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 600
FPS = 60

# --- COULEURS UI (KRX Style) ---
UI_DARK_BG = (10, 15, 30)
UI_NAV_BAR = (15, 20, 40)
UI_PANEL_BG = (45, 55, 90)
UI_ACCENT_BLUE = (100, 150, 255)
UI_BUTTON_BG = (70, 85, 130)
UI_TEXT = (230, 230, 230)

# --- COULEURS JEU ---
COLOR_BG = (20, 20, 25)
COLOR_PLAYER = (255, 50, 50)
HOOK_COLOR = (200, 200, 200)
COLOR_KILL = (255, 50, 50) # Rouge pour les pièges

# --- VALEURS PHYSIQUES DDNET ---
GRAVITY = 0.5
FRICTION_GROUND = 0.67
FRICTION_AIR = 0.95      
ACCEL_GROUND = 5.5
ACCEL_AIR = 0.7         
MAX_SPEED_GROUND = 10.0  
MAX_SPEED_AIR = 10.0      
JUMP_FORCE = -13.2       
HOOK_REACH = 380.0
HOOK_PULL_ACCEL = 1.3
HOOK_MAX_SPEED = 15.0    
HOOK_FIRE_SPEED = 80.0   

COLOR_BG = (30, 30, 30)
COLOR_PLAYER = (255, 50, 50)
HOOK_COLOR = (200, 200, 200)

pygame.init()

def load_map_from_image(filename):
    """
    Lit une image PNG et la convertit en grille de jeu.
    Noir (0,0,0) -> Mur (1)
    Rouge (255,0,0) -> KillBrick (2)
    Bleu (0,0,255) -> Spawn (0 + renvoie coords)
    """
    # Construction du chemin absolu pour éviter les erreurs
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    map_path = os.path.join(base_path, 'assets', 'maps', filename)
    
    print(f"Chargement de la map depuis : {map_path}")
    
    try:
        # Chargement de l'image via Pygame
        img = pygame.image.load(map_path)
    except pygame.error as e:
        print(f"ERREUR : Impossible de charger l'image de map.\n{e}")
        # Map par défaut pour éviter le crash
        return [[1,1,1],[1,0,1],[1,1,1]], (1, 1)

    width, height = img.get_size()
    new_map = []
    player_spawn = (100, 100) # Spawn par défaut
    
    # Légende des couleurs précises (RGB)
    COLOR_WALL = (0, 0, 0)
    COLOR_RESPAWN = (255, 0, 0)
    COLOR_SPAWN_POINT = (0, 0, 255)

    for y in range(height):
        row = []
        for x in range(width):
            # Récupération de la couleur du pixel (x, y)
            pixel_color = img.get_at((x, y))
            r, g, b, a = pixel_color # On récupère les composantes

            if (r, g, b) == COLOR_WALL:
                row.append(1)
            elif (r, g, b) == COLOR_RESPAWN:
                row.append(2)
            elif (r, g, b) == COLOR_SPAWN_POINT:
                row.append(0) # Air
                # Calcul des coordonnées réelles en pixels
                player_spawn = (x * TILE_SIZE, y * TILE_SIZE)
                print(f"Point de spawn détecté à : ({x}, {y})")
            else:
                row.append(0) # Air pour tout le reste (blanc, etc.)
        new_map.append(row)
        
    print(f"Map chargée : {width}x{height} tuiles.")
    return new_map, player_spawn

# --- GENERATION DE LA MAP ET DU SPAWN ---
# On charge 'map_level_1.png'
GAME_MAP, PLAYER_START_POS = load_map_from_image('map_level_1.png')