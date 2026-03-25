import pygame
from .settings import *

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.old_pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28
        self.is_hooked = False
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
        self.old_pos = pygame.math.Vector2(self.pos.x, self.pos.y)

        # 1. Sol et Gravité
        on_ground = world.check_collision(self.pos.x + 4, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size + 1)

        if on_ground: self.can_double_jump = True
        if input_data['jump']:
            self.jump(on_ground)
            input_data['jump'] = False

        move_accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        if input_data['left']: self.vel.x -= move_accel
        if input_data['right']: self.vel.x += move_accel

        # 2. Grappin
        if self.is_hooked:
            target = pygame.math.Vector2(self.hook_pos)
            current = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
            diff = target - current
            if diff.length() > 0:
                self.vel += diff.normalize() * HOOK_PULL_ACCEL
                if self.vel.length() > HOOK_MAX_SPEED:
                    self.vel = self.vel.normalize() * HOOK_MAX_SPEED

        # 3. Friction
        if on_ground:
            if self.vel.y >= 0:
                self.vel.x *= FRICTION_GROUND
                self.vel.y = 0
        else:
            self.vel.x *= FRICTION_AIR
            self.vel.y += GRAVITY

        # 4. COLLISIONS ET SUB-STEPPING (Corrigé pour les limites de map)
        steps = 4
        sub_vel = self.vel / steps
        
        # On calcule les limites réelles de la map en pixels
        map_width_px = len(GAME_MAP[0]) * TILE_SIZE
        map_height_px = len(GAME_MAP) * TILE_SIZE

        # Axe Vertical
        for _ in range(steps):
            new_y = self.pos.y + sub_vel.y
            # On vérifie les vraies limites de la MAP, pas de la WINDOW
            if 0 <= new_y <= map_height_px - self.size:
                self.pos.y = new_y
                if sub_vel.y > 0: # Descente
                    if world.check_collision(self.pos.x + 4, self.pos.y + self.size) or \
                       world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size):
                        self.pos.y = (int((self.pos.y + self.size) / TILE_SIZE)) * TILE_SIZE - self.size
                        self.vel.y = 0
                        break
                elif sub_vel.y < 0: # Montée
                    if world.check_collision(self.pos.x + 4, self.pos.y) or \
                       world.check_collision(self.pos.x + self.size - 4, self.pos.y):
                        self.pos.y = (int(self.pos.y / TILE_SIZE) + 1) * TILE_SIZE
                        self.vel.y = 0
                        break
            else:
                self.vel.y = 0
                break

        # Axe Horizontal
        for _ in range(steps):
            new_x = self.pos.x + sub_vel.x
            # On vérifie les vraies limites de la MAP (3200px au lieu de 1280px)
            if 0 <= new_x <= map_width_px - self.size:
                self.pos.x = new_x
                if sub_vel.x > 0: # Droite
                    if world.check_collision(self.pos.x + self.size, self.pos.y + 4) or \
                       world.check_collision(self.pos.x + self.size, self.pos.y + self.size - 4):
                        self.pos.x = (int((self.pos.x + self.size) / TILE_SIZE)) * TILE_SIZE - self.size
                        self.vel.x = 0
                        break
                elif sub_vel.x < 0: # Gauche
                    if world.check_collision(self.pos.x, self.pos.y + 4) or \
                       world.check_collision(self.pos.x, self.pos.y + self.size - 4):
                        self.pos.x = (int(self.pos.x / TILE_SIZE) + 1) * TILE_SIZE
                        self.vel.x = 0
                        break
            else:
                self.vel.x = 0
                break

        # 5. Kill Bricks
        points = [(self.pos.x + 4, self.pos.y + 4), (self.pos.x + self.size - 4, self.pos.y + 4),
                  (self.pos.x + 4, self.pos.y + self.size - 4), (self.pos.x + self.size - 4, self.pos.y + self.size - 4)]
        for p in points:
            grid_x, grid_y = int(p[0] // TILE_SIZE), int(p[1] // TILE_SIZE)
            if 0 <= grid_y < len(world.tile_map) and 0 <= grid_x < len(world.tile_map[0]):
                if world.tile_map[grid_y][grid_x] == 2:
                    self.pos = pygame.math.Vector2(100, 100)
                    self.vel = pygame.math.Vector2(0, 0)
                    self.is_hooked = False
                    break