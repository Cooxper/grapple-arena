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
        # On utilise dt directement pour une application linéaire sur le temps
        self.vel.x -= accel * (dt * 60)

    def move_right(self, on_ground, dt):
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        self.vel.x += accel * (dt * 60)

    def jump(self):
        self.vel.y = JUMP_FORCE

    def update_physics(self, world, dt):
        time_scale = dt * 60 

        on_ground = world.check_collision(self.pos.x, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size, self.pos.y + self.size + 1)
    
        friction = FRICTION_GROUND if on_ground else FRICTION_AIR
        self.vel.x *= pow(friction, time_scale)

        if not on_ground:
            self.vel.y += GRAVITY * time_scale

        max_s = MAX_SPEED_GROUND if on_ground else MAX_SPEED_AIR

        if abs(self.vel.x) > max_s:
             # On ramène doucement vers la vitesse max sans bloquer net
             self.vel.x *= pow(0.9, time_scale)

        # Limitation de vitesse DDNet
        max_s = MAX_SPEED_GROUND if on_ground else MAX_SPEED_AIR
        if abs(self.vel.x) > max_s:
            self.vel.x *= pow(0.9, time_scale)

        # Collisions Verticales
        new_y = self.pos.y + self.vel.y * time_scale
        if not world.check_collision(self.pos.x, new_y) and \
           not world.check_collision(self.pos.x + self.size, new_y) and \
           not world.check_collision(self.pos.x, new_y + self.size) and \
           not world.check_collision(self.pos.x + self.size, new_y + self.size):
            self.pos.y = new_y
        else:
            if self.vel.y < 0: self.vel.y = 0.1
            else: self.vel.y = 0

        # Collisions Horizontales
        new_x = self.pos.x + self.vel.x * time_scale
        if not world.check_collision(new_x, self.pos.y) and \
           not world.check_collision(new_x + self.size, self.pos.y) and \
           not world.check_collision(new_x, self.pos.y + self.size) and \
           not world.check_collision(new_x + self.size, self.pos.y + self.size):
            self.pos.x = new_x
        else:
            self.vel.x = 0