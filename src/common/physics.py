import pygame
from .settings import *

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.old_pos = pygame.math.Vector2(x, y) # Pour l'interpolation
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28
        self.is_hooked = False # L'attribut qui causait l'erreur
        self.hook_pos = pygame.math.Vector2(0, 0)
        self.can_double_jump = True

    def jump(self, on_ground):
        if on_ground:
            self.vel.y = JUMP_FORCE
            self.can_double_jump = True 
        elif self.can_double_jump:
            self.vel.y = JUMP_FORCE
            self.can_double_jump = False

    def fire_hook(self, target_pos, world):
        start_pos = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
        diff = target_pos - start_pos
        if diff.length() == 0: return
        direction = diff.normalize()
        
        curr_pos = pygame.math.Vector2(start_pos)
        distance = 0
        while distance < HOOK_REACH:
            curr_pos += direction * 10
            distance += 10
            if world.check_collision(curr_pos.x, curr_pos.y):
                self.hook_pos = pygame.math.Vector2(curr_pos)
                self.is_hooked = True
                return
        self.is_hooked = False

    def update_physics(self, world, input_data):
        # 1. Sauvegarde pour l'interpolation
        self.old_pos = pygame.math.Vector2(self.pos.x, self.pos.y)

        # 2. Détection du sol
        on_ground = world.check_collision(self.pos.x + 4, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size + 1)

        if on_ground:
            self.can_double_jump = True
        
        if input_data['jump']:
            self.jump(on_ground)
            input_data['jump'] = False

        # 3. Accélération (Clavier + Grappin)
        move_accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        if input_data['left']: self.vel.x -= move_accel
        if input_data['right']: self.vel.x += move_accel

        if self.is_hooked:
            target = pygame.math.Vector2(self.hook_pos)
            current = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
            diff = target - current
            if diff.length() > 0:
                self.vel += diff.normalize() * HOOK_PULL_ACCEL
                if self.vel.length() > HOOK_MAX_SPEED:
                    self.vel = self.vel.normalize() * HOOK_MAX_SPEED

        # 4. Friction et Gravité
        if on_ground:
            if self.vel.y >= 0:
                self.vel.x *= FRICTION_GROUND
                self.vel.y = 0
        else:
            self.vel.x *= FRICTION_AIR
            self.vel.y += GRAVITY

        # 5. RÉSOLUTION SÉCURISÉE DES COLLISIONS (Plus de TP)
        # --- Axe Vertical ---
        self.pos.y += self.vel.y
        if self.vel.y > 0: # Descente
            if world.check_collision(self.pos.x + 4, self.pos.y + self.size) or \
               world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size):
                # On recale précisément au pixel près au-dessus du bloc
                self.pos.y = (int((self.pos.y + self.size) / TILE_SIZE)) * TILE_SIZE - self.size
                self.vel.y = 0
        elif self.vel.y < 0: # Montée
            if world.check_collision(self.pos.x + 4, self.pos.y) or \
               world.check_collision(self.pos.x + self.size - 4, self.pos.y):
                # On recale précisément en dessous du bloc
                self.pos.y = (int(self.pos.y / TILE_SIZE) + 1) * TILE_SIZE
                self.vel.y = 0

        # --- Axe Horizontal ---
        self.pos.x += self.vel.x
        if self.vel.x > 0: # Droite
            if world.check_collision(self.pos.x + self.size, self.pos.y + 4) or \
               world.check_collision(self.pos.x + self.size, self.pos.y + self.size - 4):
                self.pos.x = (int((self.pos.x + self.size) / TILE_SIZE)) * TILE_SIZE - self.size
                self.vel.x = 0
        elif self.vel.x < 0: # Gauche
            if world.check_collision(self.pos.x, self.pos.y + 4) or \
               world.check_collision(self.pos.x, self.pos.y + self.size - 4):
                self.pos.x = (int(self.pos.x / TILE_SIZE) + 1) * TILE_SIZE
                self.vel.x = 0