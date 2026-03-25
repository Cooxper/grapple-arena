import pygame
from .settings import * # Importe GRAVITY, FRICTION, etc.

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28
        self.is_hooked = False
        self.hook_pos = pygame.math.Vector2(0, 0)

    def move_left(self, on_ground):
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        self.vel.x -= accel

    def move_right(self, on_ground):
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        self.vel.x += accel

    def jump(self):
        self.vel.y = JUMP_FORCE

    def update_physics(self, world):
        self.vel.y += GRAVITY
        self.vel.x *= FRICTION

        if self.is_hooked:
            direction = (self.hook_pos - self.pos).normalize()
            self.vel += direction * HOOK_PULL_FORCE

        # Collisions
        new_x = self.pos.x + self.vel.x
        if not world.check_collision(new_x, self.pos.y) and \
           not world.check_collision(new_x + self.size, self.pos.y):
            self.pos.x = new_x
        else:
            self.vel.x = 0

        new_y = self.pos.y + self.vel.y
        if not world.check_collision(self.pos.x, new_y) and \
           not world.check_collision(self.pos.x + self.size, new_y):
            self.pos.y = new_y
        else:
            self.vel.y = 0