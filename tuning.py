# tuning.h — valeurs exactes DDNet, aucune modification
SERVER_TICK_SPEED     = 50

GRAVITY               = 0.5
GROUND_CONTROL_SPEED  = 10.0
GROUND_CONTROL_ACCEL  = 100.0 / SERVER_TICK_SPEED  # 2.0
GROUND_FRICTION       = 0.5
GROUND_JUMP_IMPULSE   = 13.2
AIR_JUMP_IMPULSE      = 12.0
AIR_CONTROL_SPEED     = 250.0 / SERVER_TICK_SPEED   # 5.0
AIR_CONTROL_ACCEL     = 1.5
AIR_FRICTION          = 0.95
HOOK_FIRE_SPEED       = 80.0
HOOK_DRAG_ACCEL       = 3.0
HOOK_DRAG_SPEED       = 15.0
HOOK_LENGTH           = 380.0
VELRAMP_START         = 550.0
VELRAMP_RANGE         = 2000.0
VELRAMP_CURVATURE     = 1.4

# gamecore.h — états du grappin
HOOK_IDLE    = 0
HOOK_FLYING  = 1
HOOK_GRABBED = 4

# Taille physique du Tee (PhysicalSize())
PHYS_SIZE = 28.0