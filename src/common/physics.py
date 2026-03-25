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

    def update_physics(self, world, input_data):
        # 1. Détection du sol
        on_ground = world.check_collision(self.pos.x, self.pos.y + self.size + 1) or \
                    world.check_collision(self.pos.x + self.size, self.pos.y + self.size + 1)

        # Si on touche le sol, on réinitialise le double saut (sécurité)
        if on_ground:
            self.can_double_jump = False 

        if input_data['jump']:
            self.jump(on_ground)
            input_data['jump'] = False # On consomme l'input immédiatement

        # 2. Application des entrées
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        if input_data['left']: self.vel.x -= accel
        if input_data['right']: self.vel.x += accel
        
        # On passe on_ground à la fonction jump pour qu'elle décide quel saut faire
        if input_data['jump']: 
            self.jump(on_ground)
            # Important : on vide l'input jump pour ne pas sauter à chaque frame
            input_data['jump'] = False
        # 2. Application des entrées clavier (Marche et Saut)
        accel = ACCEL_GROUND if on_ground else ACCEL_AIR
        if input_data['left']: self.vel.x -= accel
        if input_data['right']: self.vel.x += accel
        if input_data['jump'] and on_ground: self.vel.y = JUMP_FORCE

        # 3. Logique de traction du Grappin (Hook)
        if self.is_hooked:
            # Calcul du vecteur entre le joueur et le point d'attache
            target = pygame.math.Vector2(self.hook_pos)
            current = pygame.math.Vector2(self.pos.x + self.size/2, self.pos.y + self.size/2)
            diff = target - current
            
            if diff.length() > 0:
                direction = diff.normalize()
                # On applique l'accélération du grappin
                self.vel += direction * HOOK_PULL_ACCEL
                
                # Cap de vitesse spécifique au grappin
                if self.vel.length() > HOOK_MAX_SPEED:
                    self.vel = self.vel.normalize() * HOOK_MAX_SPEED

        # 4. Friction et Gravité (Tick Fixe)
        if on_ground:
            self.vel.x *= FRICTION_GROUND
        else:
            self.vel.x *= FRICTION_AIR
            self.vel.y += GRAVITY

        # 5. Cap de vitesse de marche (si on ne grappine pas)
        if not self.is_hooked:
            max_s = MAX_SPEED_GROUND if on_ground else MAX_SPEED_AIR
            if abs(self.vel.x) > max_s:
                self.vel.x *= 0.9

        # 6. Résolution des collisions (Verticale)
        new_y = self.pos.y + self.vel.y
        if not world.check_collision(self.pos.x, new_y) and \
           not world.check_collision(self.pos.x + self.size, new_y) and \
           not world.check_collision(self.pos.x, new_y + self.size) and \
           not world.check_collision(self.pos.x + self.size, new_y + self.size):
            self.pos.y = new_y
        else:
            if self.vel.y < 0: self.vel.y = 0.1
            else: self.vel.y = 0

        # 7. Résolution des collisions (Horizontale)
        new_x = self.pos.x + self.vel.x
        if not world.check_collision(new_x, self.pos.y) and \
           not world.check_collision(new_x + self.size, self.pos.y) and \
           not world.check_collision(new_x, self.pos.y + self.size) and \
           not world.check_collision(new_x + self.size, self.pos.y + self.size):
            self.pos.x = new_x
        else:
            self.vel.x = 0