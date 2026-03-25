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
FRICTION_GROUND = 0.6 
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


# 0 = Vide, 1 = Mur, 2 = Kill Brick
GAME_MAP = [
    [1]*100,
    [1] + [0]*98 + [1],
    [1] + [0]*98 + [1],
    [1] + [0]*10 + [1,1,1] + [0]*85 + [1],
    [1] + [0]*98 + [1],
    [1] + [0]*20 + [1,1,1,1] + [0]*74 + [1],
    [1] + [0]*98 + [1],
    [1] + [0]*35 + [1,1] + [0]*61 + [1],
    [1] + [0]*98 + [1],
    [1] + [0]*5 + [2,2,2,2,2] + [0]*88 + [1], # Piège au début
    [1] + [0]*98 + [1],
    [1] + [0]*50 + [1,1,1,1,1,1] + [0]*42 + [1],
    [1] + [0]*98 + [1],
    [1] + [0]*70 + [2,2,2,2,2,2,2,2] + [0]*20 + [1], # Long piège
    [1] + [0]*98 + [1],
    [1]*100,
]