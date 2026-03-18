# ══════════════════════════════════════════════
#  main.py  –  Boucle principale du jeu
# ══════════════════════════════════════════════

import pygame
from reste import (
    SCREEN_W, SCREEN_H, WORLD_W, WORLD_H,
    BG_COL, HUD_COL, WHITE, WALL_COL, WALL_EDGE,
    FINISH_COL, FINISH_EDG, GRAP_COL
)
from map import walls, FINISH, generate_map
from tee import Joueur

# ─── Initialisation ──────────────────────────
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Grapple Arena")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("consolas", 48, bold=True)
font_med   = pygame.font.SysFont("consolas", 26, bold=True)
font_small = pygame.font.SysFont("consolas", 18)

generate_map()
joueur = Joueur()

# ─── État global ─────────────────────────────
camera_x    = 0
camera_y    = 0
start_ticks = pygame.time.get_ticks()
best_time   = None
finished    = False
finish_timer= 0
elapsed     = 0

# ─── Fonctions utilitaires ───────────────────
def fmt_time(ms):
    s  = ms // 1000
    cs = (ms % 1000) // 10
    return f"{s:02d}.{cs:02d}s"

def reset():
    global start_ticks, finished, finish_timer, elapsed
    joueur.reset()
    start_ticks  = pygame.time.get_ticks()
    finished     = False
    finish_timer = 0
    elapsed      = 0

def draw_wall(wall):
    rx = wall.x - camera_x
    ry = wall.y - camera_y
    pygame.draw.rect(screen, WALL_COL,  (rx, ry, wall.w, wall.h))
    pygame.draw.rect(screen, WALL_EDGE, (rx, ry, wall.w, wall.h), 2)
    pygame.draw.line(screen, (100, 130, 180), (rx + 2, ry + 2), (rx + wall.w - 4, ry + 2), 1)

def draw_finish(rect):
    rx = rect.x - camera_x
    ry = rect.y - camera_y
    surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    surf.fill((*FINISH_COL, 60))
    screen.blit(surf, (rx, ry))
    pygame.draw.rect(screen, FINISH_COL, (rx, ry, rect.w, rect.h), 3)
    mid = rx + rect.w // 2
    pygame.draw.line(screen, FINISH_EDG, (mid, ry + 5), (mid, ry + rect.h - 5), 3)
    pts = [(mid, ry + 10), (mid + 22, ry + 18), (mid, ry + 26)]
    pygame.draw.polygon(screen, FINISH_COL, pts)

def draw_hud():
    # Chronomètre
    chrono = font_med.render(f"  {fmt_time(elapsed)}", True, HUD_COL)
    screen.blit(chrono, (SCREEN_W - chrono.get_width() - 14, 10))
    # Meilleur temps
    if best_time is not None:
        best = font_small.render(f"Meilleur : {fmt_time(best_time)}", True, FINISH_COL)
        screen.blit(best, (SCREEN_W - best.get_width() - 14, 44))
    # Contrôles
    ctrl = font_small.render("Q/D  ESPACE  Clic gauche = grappin  R = reset", True, (120, 120, 150))
    screen.blit(ctrl, (10, SCREEN_H - 24))

def draw_victoire():
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    run_time = finish_timer - start_ticks
    lines = [
        ("ARRIVEE !",        font_big,   (100, 240, 160)),
        (fmt_time(run_time), font_big,   WHITE),
    ]
    if best_time == run_time:
        lines.append(("Nouveau record !", font_med, GRAP_COL))
    lines.append(("R pour recommencer", font_small, (180, 180, 200)))

    total_h = sum(f.size(t)[1] + 12 for t, f, _ in lines)
    yy = SCREEN_H // 2 - total_h // 2
    for text, fnt, col in lines:
        surf = fnt.render(text, True, col)
        screen.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, yy))
        yy += surf.get_height() + 12

# ─── Boucle principale ───────────────────────
running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    # ── Événements ──────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_ESCAPE:
                running = False

        if not finished:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                joueur.lancer_grappin(camera_x, camera_y)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                joueur.relacher_grappin()

    # ── Mise à jour ─────────────────────────────
    if not finished:
        elapsed = now - start_ticks
        joueur.update(pygame.key.get_pressed())

        # Vérif arrivée
        if joueur.rect.colliderect(FINISH):
            if best_time is None or elapsed < best_time:
                best_time = elapsed
            finished     = True
            finish_timer = now
    else:
        if now - finish_timer > 3000:
            reset()

    # ── Caméra ──────────────────────────────────
    camera_x = max(0, min(int(joueur.x) - SCREEN_W // 2, WORLD_W - SCREEN_W))
    camera_y = max(0, min(int(joueur.y) - SCREEN_H // 2, WORLD_H - SCREEN_H))

    # ── Dessin ──────────────────────────────────
    screen.fill(BG_COL)

    # Grille de fond
    for gx in range(-(camera_x % 80), SCREEN_W, 80):
        pygame.draw.line(screen, (28, 28, 42), (gx, 0), (gx, SCREEN_H))
    for gy in range(-(camera_y % 80), SCREEN_H, 80):
        pygame.draw.line(screen, (28, 28, 42), (0, gy), (SCREEN_W, gy))

    for wall in walls:
        draw_wall(wall)

    draw_finish(FINISH)
    joueur.draw(screen, camera_x, camera_y)
    draw_hud()

    if finished:
        draw_victoire()

    pygame.display.flip()

pygame.quit()