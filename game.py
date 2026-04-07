# ============================================================
#  game.py  –  Client Pygame principal
# ============================================================
from __future__ import annotations
import sys
import math
import pygame

from src.common.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    TICK_RATE, SUBSTEPS,
    TILE_SIZE, TILE_SOLID, TILE_KILL,
    COLOR_BG, COLOR_SOLID, COLOR_SOLID_EDGE, COLOR_KILL,
    COLOR_PLAYER, COLOR_HOOK_LINE, COLOR_HOOK_POINT,
    PLAYER_RADIUS, PLAYER_START_POS,
    CAM_SMOOTH, ZOOM_MIN, ZOOM_MAX, ZOOM_STEP, ZOOM_DEFAULT,
    MAP_PATH,
)
from src.common.world   import World
from src.common.physics import Entity


class GameClient:
    """Boucle de jeu principale : rendu Pygame + logique de mise à jour."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # --- Monde & Joueur ---
        self.world  = World()
        self.player = Entity(*PLAYER_START_POS)

        # --- Caméra ---
        self.cam_x  = float(PLAYER_START_POS[0])
        self.cam_y  = float(PLAYER_START_POS[1])
        self.zoom   = ZOOM_DEFAULT

        # --- Inputs ---
        self.input_left  = False
        self.input_right = False
        self.jump_pressed = False   # flanc montant uniquement

        # --- Accumulateur de temps (fixed timestep) ---
        self.accumulator = 0.0

        # --- Chargement de la map ---
        self.world.load_from_image(MAP_PATH)

        # --- Police HUD ---
        self.font = pygame.font.SysFont("monospace", 16)

    # ----------------------------------------------------------
    #  Boucle principale
    # ----------------------------------------------------------
    def run(self):
        running = True
        while running:
            frame_dt = self.clock.tick(FPS) / 1000.0
            frame_dt = min(frame_dt, 0.05)   # évite les sauts après lag

            # ---- Événements ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                        self.jump_pressed = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:           # clic gauche → grappin
                        mx, my = pygame.mouse.get_pos()
                        wx, wy = self._screen_to_world(mx, my)
                        self.player.fire_hook(self.world, wx, wy)
                    elif event.button == 3:         # clic droit → lâcher
                        self.player.release_hook()
                    elif event.button == 4:         # molette haut → zoom +
                        self.zoom = min(ZOOM_MAX, self.zoom + ZOOM_STEP)
                    elif event.button == 5:         # molette bas → zoom -
                        self.zoom = max(ZOOM_MIN, self.zoom - ZOOM_STEP)

            # Touches maintenues
            keys = pygame.key.get_pressed()
            self.input_left  = keys[pygame.K_LEFT]  or keys[pygame.K_a]
            self.input_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

            # ---- Fixed-step physics ----
            self.accumulator += frame_dt
            while self.accumulator >= TICK_RATE:
                self._tick()
                self.accumulator -= TICK_RATE

            # ---- Interpolation pour le rendu ----
            alpha = self.accumulator / TICK_RATE

            # ---- Rendu ----
            self._draw(alpha)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ----------------------------------------------------------
    #  Tick physique (100 Hz)
    # ----------------------------------------------------------
    def _tick(self):
        p = self.player

        # Saut (flanc montant)
        if self.jump_pressed:
            p.try_jump()
            self.jump_pressed = False

        p.tick(self.world, self.input_left, self.input_right)

        # Respawn si mort
        if p.dead:
            self._respawn()

        # Mise à jour caméra (lerp) à 100 Hz
        t = min(1.0, CAM_SMOOTH * TICK_RATE)
        self.cam_x += (p.x - self.cam_x) * t
        self.cam_y += (p.y - self.cam_y) * t

        # Clamper la caméra dans les limites du monde
        hw = SCREEN_WIDTH  * 0.5 / self.zoom
        hh = SCREEN_HEIGHT * 0.5 / self.zoom
        self.cam_x = max(hw, min(self.world.pixel_width  - hw, self.cam_x))
        self.cam_y = max(hh, min(self.world.pixel_height - hh, self.cam_y))

    # ----------------------------------------------------------
    #  Respawn
    # ----------------------------------------------------------
    def _respawn(self):
        self.player = Entity(*PLAYER_START_POS)
        self.cam_x = float(PLAYER_START_POS[0])
        self.cam_y = float(PLAYER_START_POS[1])

    # ----------------------------------------------------------
    #  Rendu
    # ----------------------------------------------------------
    def _draw(self, alpha: float):
        self.screen.fill(COLOR_BG)

        surf = self.screen
        z    = self.zoom
        cx   = self.cam_x
        cy   = self.cam_y
        sw   = SCREEN_WIDTH
        sh   = SCREEN_HEIGHT

        def world_to_screen(wx, wy):
            sx = (wx - cx) * z + sw * 0.5
            sy = (wy - cy) * z + sh * 0.5
            return sx, sy

        ts_z = int(TILE_SIZE * z)   # taille tuile en pixels écran

        # ---- Tuiles visibles seulement ----
        for col, row, tile_type in self.world.visible_tiles(cx, cy, sw, sh, z):
            wx = col * TILE_SIZE
            wy = row * TILE_SIZE
            sx, sy = world_to_screen(wx, wy)
            rect = pygame.Rect(int(sx), int(sy), ts_z + 1, ts_z + 1)

            if tile_type == TILE_SOLID:
                pygame.draw.rect(surf, COLOR_SOLID, rect)
                pygame.draw.rect(surf, COLOR_SOLID_EDGE, rect, max(1, int(z)))
            elif tile_type == TILE_KILL:
                pygame.draw.rect(surf, COLOR_KILL, rect)

        # ---- Grappin ----
        p = self.player
        prx = p.render_x(alpha)
        pry = p.render_y(alpha)
        psx, psy = world_to_screen(prx, pry)

        if p.hook_active:
            hsx, hsy = world_to_screen(p.hook_x, p.hook_y)
            pygame.draw.line(surf, COLOR_HOOK_LINE,
                             (int(psx), int(psy)), (int(hsx), int(hsy)),
                             max(1, int(2 * z)))
            pygame.draw.circle(surf, COLOR_HOOK_POINT,
                               (int(hsx), int(hsy)), max(3, int(5 * z)))

        # ---- Joueur ----
        pr_screen = max(3, int(PLAYER_RADIUS * z))
        pygame.draw.circle(surf, COLOR_PLAYER, (int(psx), int(psy)), pr_screen)
        # Yeux (direction de la souris)
        mx, my = pygame.mouse.get_pos()
        angle  = math.atan2(my - psy, mx - psx)
        eye_dist = pr_screen * 0.45
        ex = int(psx + math.cos(angle) * eye_dist)
        ey = int(psy + math.sin(angle) * eye_dist)
        pygame.draw.circle(surf, (20, 20, 20), (ex, ey), max(2, int(pr_screen * 0.28)))

        # ---- HUD ----
        self._draw_hud(alpha)

    def _draw_hud(self, alpha: float):
        p = self.player
        lines = [
            f"Pos  : ({p.render_x(alpha):.0f}, {p.render_y(alpha):.0f})",
            f"Vel  : ({p.vx:.0f}, {p.vy:.0f})",
            f"Zoom : {self.zoom:.1f}x",
            f"Jumps: {p.jumps_left}",
            "Hook : ON" if p.hook_active else "Hook : OFF",
            "",
            "WASD/← →  : mouvement",
            "ESPACE/↑  : saut",
            "Clic G    : grappin",
            "Clic D    : lâcher",
            "Molette   : zoom",
        ]
        y = 8
        for line in lines:
            surf = self.font.render(line, True, (200, 200, 200))
            self.screen.blit(surf, (8, y))
            y += 18

    # ----------------------------------------------------------
    #  Conversion coordonnées
    # ----------------------------------------------------------
    def _screen_to_world(self, sx: float, sy: float):
        wx = (sx - SCREEN_WIDTH  * 0.5) / self.zoom + self.cam_x
        wy = (sy - SCREEN_HEIGHT * 0.5) / self.zoom + self.cam_y
        return wx, wy


# ----------------------------------------------------------
#  Point d'entrée
# ----------------------------------------------------------
def main():
    client = GameClient()
    client.run()


if __name__ == "__main__":
    main()
