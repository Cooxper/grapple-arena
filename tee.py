# ══════════════════════════════════════════════
#  tee.py  –  Classe du joueur (Tee)
# ══════════════════════════════════════════════

import pygame
from reste import (
    SPAWN, SPEED, JUMP_POWER,
    TEE_R, TEE_BODY, TEE_BORDER, TEE_EYE, TEE_WHITE, TEE_FEET,
    GRAP_COL, WHITE
)
from physique import (
    appliquer_gravite, move_and_collide,
    appliquer_grappin, lancer_grappin
)


class Joueur:
    def __init__(self):
        self.reset()

    def reset(self):
        """Remet le joueur à la position de départ."""
        self.x, self.y     = float(SPAWN[0]), float(SPAWN[1])
        self.vel_x         = 0.0
        self.vel_y         = 0.0
        self.on_ground     = False
        self.facing        = 1        # 1 = droite, -1 = gauche
        self.grapple_active= False
        self.grapple_point = None

    # ── Grappin ──────────────────────────────────────────────────
    def lancer_grappin(self, camera_x, camera_y):
        point = lancer_grappin(self.x, self.y, camera_x, camera_y)
        if point:
            self.grapple_point  = point
            self.grapple_active = True

    def relacher_grappin(self):
        self.grapple_active = False
        self.grapple_point  = None

    # ── Mise à jour ──────────────────────────────────────────────
    def update(self, keys):
        """Applique les entrées clavier, la physique et les collisions."""
        # Déplacement horizontal
        move = 0
        if keys[pygame.K_q] or keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move = -SPEED
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move = SPEED
            self.facing = 1

        # Saut
        if (keys[pygame.K_z] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = JUMP_POWER

        # Gravité (depuis physique.py)
        self.vel_y = appliquer_gravite(self.vel_y)

        # Grappin (depuis physique.py)
        if self.grapple_active and self.grapple_point:
            self.vel_x, self.vel_y, toujours_actif = appliquer_grappin(
                self.vel_x, self.vel_y, self.x, self.y, self.grapple_point
            )
            if not toujours_actif:
                self.relacher_grappin()

        # Collisions (depuis physique.py)
        self.x, self.y, self.on_ground = move_and_collide(
            self.x, self.y, move, self.vel_y
        )

    @property
    def rect(self):
        """Rectangle de collision du joueur."""
        return pygame.Rect(self.x - TEE_R, self.y - TEE_R, TEE_R * 2, TEE_R * 2)

    # ── Dessin ───────────────────────────────────────────────────
    def draw(self, screen, camera_x, camera_y):
        """Dessine le Tee à l'écran."""
        sx = int(self.x) - camera_x
        sy = int(self.y) - camera_y
        r  = TEE_R

        # Câble du grappin
        if self.grapple_active and self.grapple_point:
            gx = int(self.grapple_point[0]) - camera_x
            gy = int(self.grapple_point[1]) - camera_y
            pygame.draw.line(screen, (80, 60, 20), (sx, sy), (gx, gy), 3)
            pygame.draw.line(screen, GRAP_COL,     (sx, sy), (gx, gy), 1)
            pygame.draw.circle(screen, GRAP_COL, (gx, gy), 5)
            pygame.draw.circle(screen, WHITE,    (gx, gy), 3)

        # Ombre au sol
        shadow = pygame.Surface((r * 3, r), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
        screen.blit(shadow, (sx - r + r // 2, sy + r - 4))

        # Corps
        pygame.draw.circle(screen, TEE_BORDER, (sx, sy), r + 2)
        pygame.draw.circle(screen, TEE_BODY,   (sx, sy), r)

        # Pieds
        foot_y = sy + r - 4
        for fx in [sx - 6, sx + 6]:
            pygame.draw.circle(screen, TEE_FEET,   (fx, foot_y), 5)
            pygame.draw.circle(screen, TEE_BORDER, (fx, foot_y), 5, 2)

        # Yeux
        eye_ox = 5 * self.facing
        pygame.draw.circle(screen, TEE_WHITE, (sx + eye_ox,               sy - 3), 5)
        pygame.draw.circle(screen, TEE_WHITE, (sx + eye_ox + 2,           sy - 3), 5)
        pygame.draw.circle(screen, TEE_EYE,   (sx + eye_ox + self.facing, sy - 3), 3)

        # Bras si grappin actif
        if self.grapple_active:
            pygame.draw.circle(screen, TEE_BORDER, (sx + self.facing * r, sy - 2), 4)