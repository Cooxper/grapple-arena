# settings.py modifié pour une map plus grande
TILE_SIZE = 32
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

# --- VALEURS OFFICIELLES DDNET / TEEWORLDS ---
GRAVITY = 0.5
# Friction (multiplicateur par tick)
FRICTION_GROUND = 0.5    # ground_friction
FRICTION_AIR = 0.95      # air_friction

# Accélération (ajoute à la vélocité par tick)
ACCEL_GROUND = 2.0       # ground_control_accel
ACCEL_AIR = 1.5          # air_control_accel

# Vitesse maximale (cap)
MAX_SPEED_GROUND = 10.0  # ground_control_speed
MAX_SPEED_AIR = 5.0      # air_control_speed

# Saut (impulsion verticale)
JUMP_FORCE = -13.2       # ground_jump_impulse

# Grappin (Hook)
HOOK_REACH = 380.0       # hook_length (pixels)
HOOK_PULL_ACCEL = 3.0    # hook_drag_accel
HOOK_MAX_SPEED = 15.0    # hook_drag_speed
HOOK_FIRE_SPEED = 80.0   # Vitesse du projectile du grappin

def update_physics(self, world):
        # 1. Détection du sol pour savoir quel Tuning utiliser
        # On vérifie si les pieds touchent un mur
        on_ground = world.check_collision(self.pos.x, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size, self.pos.y + self.size + 1)

        # 2. Application de la Friction et Gravité
        if on_ground:
            self.vel.x *= FRICTION_GROUND
        else:
            self.vel.x *= FRICTION_AIR
            self.vel.y += GRAVITY

        # 3. Cap de vitesse (pour ne pas accélérer à l'infini avec les touches)
        # Note: Le grappin peut dépasser ce cap, mais pas la marche
        max_speed = MAX_SPEED_GROUND if on_ground else MAX_SPEED_AIR
        if abs(self.vel.x) > max_speed:
            # On freine si on dépasse la vitesse max (sauf si projeté)
            self.vel.x *= 0.9 

        # 4. Logique du Grappin (Traction)
        if self.is_hooked:
            direction = (self.hook_pos - self.pos).normalize()
            self.vel += direction * HOOK_PULL_ACCEL
            # Cap de vitesse du grappin
            if self.vel.length() > HOOK_MAX_SPEED:
                self.vel = self.vel.normalize() * HOOK_MAX_SPEED

        # 5. Résolution des collisions (ton bloc actuel est bon)
        # ...

# Couleurs
COLOR_BG = (30, 30, 30)
COLOR_PLAYER = (255, 50, 50)
HOOK_COLOR = (200, 200, 200)

# Map agrandie (environ 40 colonnes de large)
GAME_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]