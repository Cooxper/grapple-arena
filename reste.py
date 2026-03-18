# ══════════════════════════════════════════════
#  reste.py  –  Toutes les valeurs fixes
# ══════════════════════════════════════════════

# ─── Fenêtre ─────────────────────────────────
SCREEN_W, SCREEN_H = 900, 600

# ─── Monde ───────────────────────────────────
WORLD_W, WORLD_H = 2400, 1600
SPAWN = (800, 620)

# ─── Physique (style DDNet) ──────────────────
SPEED         = 5      # accélération horizontale (pas vitesse max)
GRAVITY       = 0.35   # gravité réduite = sauts plus aériens
JUMP_POWER    = -11    # saut un peu plus haut
GRAPPLE_RANGE = 800
GRAPPLE_FORCE = 2.2    # grappin plus nerveux
TEE_R         = 14
VEL_Y_MAX     = 20     # vitesse de chute max

# ─── Couleurs générales ───────────────────────
WHITE      = (240, 240, 245)
BLACK      = (20,  20,  30)
BG_COL     = (18,  18,  28)
HUD_COL    = (240, 240, 255)

# ─── Murs ────────────────────────────────────
WALL_COL   = (60,  80, 120)
WALL_EDGE  = (40,  55,  95)

# ─── Grappin ─────────────────────────────────
GRAP_COL   = (255, 140,   0)

# ─── Zone d'arrivée ──────────────────────────
FINISH_COL = (80,  220, 140)
FINISH_EDG = (50,  180, 100)

# ─── Tee (personnage) ────────────────────────
TEE_BODY   = (255, 210, 100)
TEE_BORDER = (180, 130,  40)
TEE_EYE    = (30,  30,  40)
TEE_WHITE  = (255, 255, 255)
TEE_FEET   = (180, 120,  30)