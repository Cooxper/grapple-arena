import pygame
from .settings import *

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28
        self.is_hooked = False
        self.hook_pos = pygame.math.Vector2(0, 0)

    def jump(self, on_ground):
        if on_ground:
            self.vel.y = JUMP_FORCE
            # On a déjà sauté une fois, il nous reste le saut en l'air
            self.can_double_jump = True 
        elif self.can_double_jump:
            self.vel.y = JUMP_FORCE
            # On consomme le dernier saut disponible
            self.can_double_jump = False

    def fire_hook(self, target_pos, world):
        # On part du centre du joueur
        start_pos = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
        
        # Vecteur direction vers la souris
        diff = target_pos - start_pos
        if diff.length() == 0: return
        direction = diff.normalize()
        
        # Raycasting simple : on avance de 10px en 10px jusqu'à HOOK_REACH
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
        # 1. Détection du sol
        on_ground = world.check_collision(self.pos.x + 4, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size + 1)

        if on_ground:
            self.can_double_jump = True
        
        if input_data['jump']:
            self.jump(on_ground)
            input_data['jump'] = False

        # 2. Application des forces horizontales
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        if input_data['left']: self.vel.x -= accel
        if input_data['right']: self.vel.x += accel

        # 3. Traction du Grappin
        if self.is_hooked:
            target = pygame.math.Vector2(self.hook_pos)
            current = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
            diff = target - current
            
            if diff.length() > 0:
                direction = diff.normalize()
                # On tire le joueur vers le point d'accroche
                self.vel += direction * HOOK_PULL_ACCEL
                
                # Cap de vitesse spécial grappin
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

        # 5. Cap de vitesse standard (si pas de grappin)
        if not self.is_hooked:
            max_s = MAX_SPEED_GROUND if on_ground else MAX_SPEED_AIR
            if abs(self.vel.x) > max_s:
                self.vel.x *= 0.95 

        # 6. Résolution des collisions (Verticale puis Horizontale)
        self.pos.y += self.vel.y
        if self.vel.y > 0: # Descente
            if world.check_collision(self.pos.x + 4, self.pos.y + self.size) or \
               world.check_collision(self.pos.x + self.size - 4, self.pos.y + self.size):
                self.pos.y = (int((self.pos.y + self.size) / TILE_SIZE) * TILE_SIZE) - self.size
                self.vel.y = 0
        elif self.vel.y < 0: # Montée
            if world.check_collision(self.pos.x + 4, self.pos.y) or \
               world.check_collision(self.pos.x + self.size - 4, self.pos.y):
                self.pos.y = (int(self.pos.y / TILE_SIZE) + 1) * TILE_SIZE
                self.vel.y = 0

        self.pos.x += self.vel.x
        if self.vel.x > 0: # Droite
            if world.check_collision(self.pos.x + self.size, self.pos.y + 4) or \
               world.check_collision(self.pos.x + self.size, self.pos.y + self.size - 4):
                self.pos.x = (int((self.pos.x + self.size) / TILE_SIZE) * TILE_SIZE) - self.size
                self.vel.x = 0
        elif self.vel.x < 0: # Gauche
            if world.check_collision(self.pos.x, self.pos.y + 4) or \
               world.check_collision(self.pos.x, self.pos.y + self.size - 4):
                self.pos.x = (int(self.pos.x / TILE_SIZE) + 1) * TILE_SIZE
                self.vel.x = 0