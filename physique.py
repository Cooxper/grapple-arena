# ══════════════════════════════════════════════
#  physique.py  –  Gravité, collisions, grappin
#  Physique inspirée de DDNet :
#   - élan conservé (pas de reset vel_x au sol)
#   - gravité réduite
#   - grappin avec contrainte de longueur
#   - friction douce pour fluidité
# ══════════════════════════════════════════════

import pygame
import math
from reste import TEE_R, GRAPPLE_RANGE, GRAPPLE_FORCE, GRAVITY, VEL_Y_MAX
from map import walls

# ─── Constantes physique avancée ─────────────────────────────
FRICTION_SOL  = 0.82   # ralentissement horizontal au sol
FRICTION_AIR  = 0.96   # très peu de résistance dans les airs (élan conservé)
GRAPPLE_LEN   = 300    # longueur max du câble avant tension


def appliquer_gravite(vel_y):
    """Gravité réduite par rapport à DDNet pour des sauts plus aériens."""
    return min(vel_y + GRAVITY, VEL_Y_MAX)


def appliquer_friction(vel_x, au_sol):
    """
    Applique la friction horizontale.
    Au sol : on freine un peu. Dans les airs : quasi rien (élan DDNet).
    """
    if au_sol:
        return vel_x * FRICTION_SOL
    return vel_x * FRICTION_AIR


def move_and_collide(x, y, dx, dy):
    """
    Déplace le joueur et résout les collisions avec les murs.
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
    point de collision avec un mur. Retourne None sinon.
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
    Physique du grappin style DDNet :
    - Force d'attraction vers le point d'accroche
    - Contrainte de longueur : si le câble est tendu, on supprime
      la composante de vitesse qui s'éloigne du point (élan latéral conservé)
    - Retourne (vel_x, vel_y, toujours_actif)
    """
    dx = grapple_point[0] - px
    dy = grapple_point[1] - py
    dist = math.hypot(dx, dy)

    if dist < 5:
        return vel_x, vel_y, False

    # Direction normalisée vers le point d'accroche
    nx = dx / dist
    ny = dy / dist

    # Force d'attraction (plus forte que avant pour feel DDNet)
    vel_x += nx * GRAPPLE_FORCE
    vel_y += ny * GRAPPLE_FORCE

    # Contrainte de longueur : si câble tendu, on annule la fuite
    if dist > GRAPPLE_LEN:
        dot = vel_x * nx + vel_y * ny
        if dot < 0:   # le joueur s'éloigne du point
            vel_x -= dot * nx
            vel_y -= dot * ny

    return vel_x, vel_y, True


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