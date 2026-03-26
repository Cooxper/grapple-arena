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

def load_map_from_image(filename):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    map_path = os.path.join(base_path, 'assets', 'maps', filename)
    
    if not os.path.exists(map_path):
        print(f"ERREUR : {map_path} introuvable.")
        return [[1]*50, [1]+[0]*48+[1], [1]*50], (100, 100)

    img = pygame.image.load(map_path)
    width, height = img.get_size()
    new_map = []
    
    # Spawn par défaut (haut-gauche)
    player_spawn = (128, 128) 
    found_spawn = False

    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = img.get_at((x, y))
            
            # --- CORRECTION DE LA LOGIQUE DES COULEURS ---
            
            # 1. Noir PUR -> C'est un MUR
            # On tolère un noir très léger, mais pas le gris foncé
            if r < 15 and g < 15 and b < 15:
                row.append(1)
            
            # 2. Rouge PUR -> C'est de la MORT (Kill Brick)
            # Dominance rouge claire, pas un rouge-brun
            elif r > 200 and g < 50 and b < 50:
                row.append(2)
            
            # 3. Spawn point par détection d'air
            # Si aucun pixel bleu n'est trouvé, on cherche une zone d'air
            elif not found_spawn and r > 100 and g > 100 and b > 100:
                # On a trouvé de l'air ! On spawn ici
                row.append(0)
                player_spawn = (x * TILE_SIZE, y * TILE_SIZE)
                found_spawn = True
                print(f"Note : Spawn détecté dans l'air à ({x}, {y})")

            # 4. Tout le reste est de l'AIR (ton fond gris)
            else:
                row.append(0)
        new_map.append(row)
    
    if not found_spawn:
        print("Note : Pas de zone d'air trouvée, spawn en (128, 128)")
    
    print(f"Succès : Map chargée ({width}x{height} tuiles).")
    return new_map, player_spawn