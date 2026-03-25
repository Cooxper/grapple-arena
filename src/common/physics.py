import pygame
from .settings import *

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28
        self.is_hooked = False
        self.hook_pos = pygame.math.Vector2(0, 0)

    def move_left(self, on_ground, dt):
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        self.vel.x -= accel * (dt * 60)

    def move_right(self, on_ground, dt):
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        self.vel.x += accel * (dt * 60)

    def jump(self):
        self.vel.y = JUMP_FORCE

    def update_physics(self, world, dt):
        # Normalisation sur 60 FPS
        time_scale = dt * 60 

        # Détection du sol
        on_ground = world.check_collision(self.pos.x, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size, self.pos.y + self.size + 1)

        # Application Friction et Gravité selon le sol ou l'air
        if on_ground:
            self.vel.x *= pow(FRICTION_GROUND, time_scale)
        else:
            self.vel.x *= pow(FRICTION_AIR, time_scale)
            self.vel.y += GRAVITY * time_scale

        # 4. Déplacement réel (appliqué avec time_scale)
        # On calcule les collisions avec la nouvelle vélocité
        
        # Collision Verticale
        new_y = self.pos.y + self.vel.y * time_scale
        if not world.check_collision(self.pos.x, new_y) and \
           not world.check_collision(self.pos.x + self.size, new_y) and \
           not world.check_collision(self.pos.x, new_y + self.size) and \
           not world.check_collision(self.pos.x + self.size, new_y + self.size):
            self.pos.y = new_y
        else:
            if self.vel.y < 0: self.vel.y = 0.1
            else: self.vel.y = 0

        # Collision Horizontale
        new_x = self.pos.x + self.vel.x * time_scale
        if not world.check_collision(new_x, self.pos.y) and \
           not world.check_collision(new_x + self.size, self.pos.y) and \
           not world.check_collision(new_x, self.pos.y + self.size) and \
           not world.check_collision(new_x + self.size, self.pos.y + self.size):
            self.pos.x = new_x
        else:
            self.vel.x = 0