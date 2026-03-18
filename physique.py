# ══════════════════════════════════════════════
#  physique.py  –  Gravité, collisions, grappin
# ══════════════════════════════════════════════

import pygame
import math
from reste import TEE_R, GRAPPLE_RANGE, GRAPPLE_FORCE, GRAVITY, VEL_Y_MAX
from map import walls


def appliquer_gravite(vel_y):
    """Augmente la vitesse verticale (chute) à chaque frame."""
    return min(vel_y + GRAVITY, VEL_Y_MAX)


def move_and_collide(x, y, dx, dy):
    """
    Déplace le joueur de (dx, dy) et corrige les collisions avec les murs.
    Retourne (nouvelle_x, nouvelle_y, au_sol).
    """
    au_sol = False

    # ── Axe horizontal ──────────────────────────────────────────
    x += dx
    circle = pygame.Rect(x - TEE_R, y - TEE_R, TEE_R * 2, TEE_R * 2)
    for wall in walls:
        if wall.colliderect(circle):
            x = wall.left - TEE_R if dx > 0 else wall.right + TEE_R
            circle = pygame.Rect(x - TEE_R, y - TEE_R, TEE_R * 2, TEE_R * 2)

    # ── Axe vertical ────────────────────────────────────────────
    y += dy
    circle = pygame.Rect(x - TEE_R, y - TEE_R, TEE_R * 2, TEE_R * 2)
    for wall in walls:
        if wall.colliderect(circle):
            if dy > 0:
                y = wall.top - TEE_R
                au_sol = True
            elif dy < 0:
                y = wall.bottom + TEE_R
            circle = pygame.Rect(x - TEE_R, y - TEE_R, TEE_R * 2, TEE_R * 2)
            break

    return x, y, au_sol


def get_grapple_point(start, end):
    """
    Trace une ligne de start vers end et retourne le premier
    point de collision avec un mur (point d'accroche du grappin).
    Retourne None si aucun mur n'est touché.
    """
    steps = 60
    for i in range(1, steps + 1):
        t = i / steps
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        pt = pygame.Rect(x - 2, y - 2, 4, 4)
        for wall in walls:
            if wall.colliderect(pt):
                return (x, y)
    return None


def appliquer_grappin(vel_x, vel_y, px, py, grapple_point):
    """
    Attire le joueur vers le point d'accroche du grappin.
    Retourne (vel_x, vel_y, grappin_toujours_actif).
    """
    dx = grapple_point[0] - px
    dy = grapple_point[1] - py
    dist = math.hypot(dx, dy)

    if dist > 10:
        vel_x += dx * GRAPPLE_FORCE / dist
        vel_y += dy * GRAPPLE_FORCE / dist
        return vel_x, vel_y, True
    else:
        # Le joueur est arrivé au point d'accroche
        return vel_x, vel_y, False


def lancer_grappin(px, py, camera_x, camera_y):
    """
    Calcule le point d'accroche depuis la position de la souris.
    Retourne le point (x, y) ou None si rien n'est touché.
    """
    import pygame as pg
    mx, my = pg.mouse.get_pos()
    world_mouse = (mx + camera_x, my + camera_y)
    dx = world_mouse[0] - px
    dy = world_mouse[1] - py
    if math.hypot(dx, dy) <= GRAPPLE_RANGE:
        return get_grapple_point((px, py), world_mouse)
    return None