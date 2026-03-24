# Fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60

# Physique
GRAVITY = 0.5
FRICTION = 0.9
ACCEL_GROUND = 0.6
ACCEL_AIR = 0.4
JUMP_FORCE = -12.0

# Grappin
HOOK_REACH = 400
HOOK_PULL_FORCE = 1.2
HOOK_COLOR = (200, 200, 200)

# Couleurs
COLOR_BG = (30, 30, 30)
COLOR_PLAYER = (255, 50, 50)

TILE_SIZE = 32

# Une petite map de test (1 = Mur, 0 = Vide)
# Tu peux modifier les 1 pour créer des plateformes
GAME_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]