# tee.py — personnage joueur
# Wrapper de CCharacterCore + dessin pygame

import pygame
import math
from gamecore import CCharacterCore
from tuning import PHYS_SIZE, HOOK_IDLE, HOOK_GRABBED

TEE_R = int(PHYS_SIZE / 2)

# Couleurs du Tee
BODY_COL   = (255, 210, 100)
BORDER_COL = (180, 130,  40)
EYE_COL    = ( 30,  30,  40)
WHITE      = (255, 255, 255)
FEET_COL   = (180, 120,  30)
HOOK_COL   = (255, 140,   0)


class Joueur:
    def __init__(self, spawn_x, spawn_y):
        self.core   = CCharacterCore()
        self.facing = 1
        self.reset(spawn_x, spawn_y)

        # positions précédente et courante pour interpolation
        self.prev_x = spawn_x
        self.prev_y = spawn_y

    def reset(self, spawn_x, spawn_y):
        self.core.reset(spawn_x, spawn_y)
        self.facing  = 1
        self.prev_x  = spawn_x
        self.prev_y  = spawn_y

    def tick(self, inp_dir, inp_jump, inp_hook, target_x, target_y):
        self.prev_x = self.core.pos_x
        self.prev_y = self.core.pos_y
        if inp_dir != 0:
            self.facing = inp_dir
        self.core.tick(inp_dir, inp_jump, inp_hook, target_x, target_y)
        self.core.tick_deferred()

    def draw(self, screen, cam_x, cam_y):
        sx = int(self.core.pos_x) - cam_x
        sy = int(self.core.pos_y) - cam_y
        r  = TEE_R

        # Câble du grappin
        if self.core.hook_state != HOOK_IDLE:
            gx = int(self.core.hook_pos_x) - cam_x
            gy = int(self.core.hook_pos_y) - cam_y
            pygame.draw.line(screen, (80, 60, 20), (sx, sy), (gx, gy), 3)
            pygame.draw.line(screen, HOOK_COL,     (sx, sy), (gx, gy), 1)
            if self.core.hook_state == HOOK_GRABBED:
                pygame.draw.circle(screen, HOOK_COL, (gx, gy), 5)
                pygame.draw.circle(screen, WHITE,    (gx, gy), 3)

        # Ombre
        shadow = pygame.Surface((r * 3, r), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
        screen.blit(shadow, (sx - r + r//2, sy + r - 4))

        # Corps
        pygame.draw.circle(screen, BORDER_COL, (sx, sy), r + 2)
        pygame.draw.circle(screen, BODY_COL,   (sx, sy), r)

        # Pieds
        fy = sy + r - 4
        for fx in [sx - 6, sx + 6]:
            pygame.draw.circle(screen, FEET_COL,   (fx, fy), 5)
            pygame.draw.circle(screen, BORDER_COL, (fx, fy), 5, 2)

        # Yeux
        eox = 5 * self.facing
        pygame.draw.circle(screen, WHITE,   (sx + eox,              sy - 3), 5)
        pygame.draw.circle(screen, WHITE,   (sx + eox + 2,          sy - 3), 5)
        pygame.draw.circle(screen, EYE_COL, (sx + eox + self.facing, sy - 3), 3)

        # Bras grappin
        if self.core.hook_state != HOOK_IDLE:
            pygame.draw.circle(screen, BORDER_COL, (sx + self.facing * r, sy - 2), 4)

    @property
    def x(self): return self.core.pos_x
    @property
    def y(self): return self.core.pos_y
    @property
    def jumps_left(self): return self.core.jumps_left