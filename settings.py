# ============================================================
#  settings.py  –  Constantes globales du jeu (aucun import local)
# ============================================================

# --- Fenêtre ---
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 120          # fréquence de rendu (peut dépasser 100)
TITLE         = "Grappling Platformer – DDNet Style"

# --- Physique ---
TICK_RATE      = 0.01        # 100 ticks/s  →  dt = 0.01 s
SUBSTEPS       = 4           # sub-steps par tick pour les collisions
GRAVITY        = 2800.0      # px/s²
MAX_FALL_SPEED = 1400.0      # px/s  (terminal velocity)

# --- Joueur ---
PLAYER_RADIUS     = 14       # px  (collision circulaire)
PLAYER_MOVE_ACCEL = 2200.0   # accélération horizontale sol  (px/s²)
PLAYER_AIR_ACCEL  = 1400.0   # accélération horizontale air
PLAYER_FRICTION   = 0.015    # coeff de friction sol  (multiplicateur vitesse)
PLAYER_MAX_SPEED  = 520.0    # vitesse horizontale max  (px/s)
PLAYER_JUMP_VEL   = -780.0   # vitesse verticale au saut
PLAYER_JUMP2_VEL  = -680.0   # double saut légèrement moins puissant
PLAYER_START_POS  = (200, 200)

# --- Grappin ---
HOOK_SPEED        = 2400.0   # vitesse du projectile grappin (px/s) [inutilisé : tir instantané]
HOOK_MAX_LEN      = 600.0    # longueur max du câble (px)
HOOK_PULL_ACCEL   = 1800.0   # accélération d'attraction vers l'accroche (px/s²)
HOOK_DAMPING      = 0.55     # amortissement appliqué quand le câble tire

# --- Tuiles ---
TILE_SIZE     = 32           # px
TILE_EMPTY    = 0
TILE_SOLID    = 1            # mur / sol  →  collision
TILE_KILL     = 2            # tuile mortelle (rouge)

# --- Caméra ---
CAM_SMOOTH    = 8.0          # lerp factor  (plus grand = plus réactif)
ZOOM_MIN      = 0.4
ZOOM_MAX      = 3.0
ZOOM_STEP     = 0.1
ZOOM_DEFAULT  = 1.0

# --- Carte ---
MAP_PATH      = "assets/maps/map_level_1.png"
MAP_SCALE_DIV = 2            # diviser la taille de l'image par cette valeur au chargement

# --- Couleurs ---
COLOR_BG         = (30,  30,  35)
COLOR_SOLID      = (80,  90, 100)
COLOR_SOLID_EDGE = (110, 125, 140)
COLOR_KILL       = (180,  40,  40)
COLOR_PLAYER     = (240, 200,  60)
COLOR_HOOK_LINE  = (200, 200, 200)
COLOR_HOOK_POINT = (255, 255, 100)
