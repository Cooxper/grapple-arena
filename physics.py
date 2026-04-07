# ============================================================
#  physics.py  –  Entité physique de base
# ============================================================
from __future__ import annotations
import math
from src.common.settings import (
    GRAVITY, MAX_FALL_SPEED,
    PLAYER_MOVE_ACCEL, PLAYER_AIR_ACCEL,
    PLAYER_FRICTION, PLAYER_MAX_SPEED,
    PLAYER_JUMP_VEL, PLAYER_JUMP2_VEL,
    PLAYER_RADIUS,
    HOOK_MAX_LEN, HOOK_PULL_ACCEL, HOOK_DAMPING,
    TICK_RATE, SUBSTEPS,
    TILE_SIZE, TILE_SOLID, TILE_KILL,
    PLAYER_START_POS,
)


class Entity:
    """Joueur physique avec grappin, double-saut et sub-stepping."""

    def __init__(self, x: float, y: float):
        # position courante et précédente  (pour l'interpolation)
        self.x  = float(x)
        self.y  = float(y)
        self.px = self.x          # position au tick précédent
        self.py = self.y

        self.vx = 0.0
        self.vy = 0.0

        self.on_ground   = False
        self.jumps_left  = 2      # double saut

        # --- Grappin ---
        self.hook_active  = False
        self.hook_x       = 0.0
        self.hook_y       = 0.0

        # --- Mort ---
        self.dead = False

    # ----------------------------------------------------------
    #  Propriétés interpolées pour le rendu
    # ----------------------------------------------------------
    def render_x(self, alpha: float) -> float:
        return self.px + (self.x - self.px) * alpha

    def render_y(self, alpha: float) -> float:
        return self.py + (self.y - self.py) * alpha

    # ----------------------------------------------------------
    #  Saut
    # ----------------------------------------------------------
    def try_jump(self):
        if self.jumps_left > 0:
            self.vy = PLAYER_JUMP_VEL if self.jumps_left == 2 else PLAYER_JUMP2_VEL
            self.jumps_left -= 1

    # ----------------------------------------------------------
    #  Grappin
    # ----------------------------------------------------------
    def fire_hook(self, world, mx: float, my: float):
        """Tir instantané en raycasting vers (mx, my)."""
        dx = mx - self.x
        dy = my - self.y
        dist = math.hypot(dx, dy)
        if dist < 1:
            return
        nx = dx / dist
        ny = dy / dist
        max_dist = min(dist, HOOK_MAX_LEN)

        # raycasting par pas de demi-tuile
        step = TILE_SIZE * 0.5
        steps = int(max_dist / step) + 1
        hit = False
        for i in range(1, steps + 1):
            t = min(i * step, max_dist)
            cx = self.x + nx * t
            cy = self.y + ny * t
            tile = world.get_tile(cx, cy)
            if tile == TILE_SOLID:
                self.hook_active = True
                self.hook_x = cx
                self.hook_y = cy
                hit = True
                break
        if not hit:
            self.hook_active = False

    def release_hook(self):
        self.hook_active = False

    # ----------------------------------------------------------
    #  Tick principal  (appelé 100×/s)
    # ----------------------------------------------------------
    def tick(self, world, input_left: bool, input_right: bool):
        if self.dead:
            return

        # Sauvegarde position précédente pour l'interpolation
        self.px = self.x
        self.py = self.y

        dt_sub = TICK_RATE / SUBSTEPS

        for _ in range(SUBSTEPS):
            self._substep(world, input_left, input_right, dt_sub)

        # Détection tuile mortelle
        if world.get_tile(self.x, self.y) == TILE_KILL:
            self.dead = True

    # ----------------------------------------------------------
    #  Sub-step  (appelé SUBSTEPS fois par tick)
    # ----------------------------------------------------------
    def _substep(self, world, input_left: bool, input_right: bool, dt: float):
        accel = PLAYER_MOVE_ACCEL if self.on_ground else PLAYER_AIR_ACCEL

        # --- Accélération horizontale ---
        if input_left:
            self.vx -= accel * dt
        if input_right:
            self.vx += accel * dt

        # --- Friction horizontale ---
        if self.on_ground:
            self.vx *= (1.0 - PLAYER_FRICTION) ** (dt * 100)

        # Clamp vitesse horizontale
        self.vx = max(-PLAYER_MAX_SPEED, min(PLAYER_MAX_SPEED, self.vx))

        # --- Gravité ---
        self.vy += GRAVITY * dt
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # --- Force grappin ---
        if self.hook_active:
            hdx = self.hook_x - self.x
            hdy = self.hook_y - self.y
            hdist = math.hypot(hdx, hdy)
            if hdist > 1:
                hnx = hdx / hdist
                hny = hdy / hdist
                self.vx += hnx * HOOK_PULL_ACCEL * dt
                self.vy += hny * HOOK_PULL_ACCEL * dt
                # amortissement dans l'axe perpendiculaire au câble
                dot = self.vx * hnx + self.vy * hny
                self.vx = self.vx * HOOK_DAMPING + hnx * dot * (1 - HOOK_DAMPING)
                self.vy = self.vy * HOOK_DAMPING + hny * dot * (1 - HOOK_DAMPING)

        # --- Déplacement + résolution de collision ---
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        new_x, new_y, self.vx, self.vy, self.on_ground = _resolve_collision(
            world, self.x, self.y, new_x, new_y, self.vx, self.vy, PLAYER_RADIUS
        )

        self.x = new_x
        self.y = new_y

        if self.on_ground:
            self.jumps_left = 2


# ----------------------------------------------------------
#  Résolution de collision circulaire contre la grille
# ----------------------------------------------------------
def _resolve_collision(world, ox, oy, nx, ny, vx, vy, radius):
    """Résout les collisions d'un cercle contre les tuiles solides.
    Retourne (new_x, new_y, new_vx, new_vy, on_ground).
    """
    on_ground = False
    r = radius
    ts = TILE_SIZE

    # Déplacement en X puis Y séparément (sweep AABB simplifié)
    # --- Axe X ---
    cx = nx
    cy = oy
    # tuiles à tester
    for tile_x, tile_y in _overlapping_tiles(cx, cy, r, ts):
        if world.get_tile_grid(tile_x, tile_y) == TILE_SOLID:
            tx_min = tile_x * ts
            tx_max = tx_min + ts
            ty_min = tile_y * ts
            ty_max = ty_min + ts
            if cy + r > ty_min and cy - r < ty_max:
                if cx + r > tx_min and cx - r < tx_max:
                    if ox + r <= tx_min + 1:
                        cx = tx_min - r
                        vx = 0
                    elif ox - r >= tx_max - 1:
                        cx = tx_max + r
                        vx = 0

    # --- Axe Y ---
    fx = cx
    fy = ny
    for tile_x, tile_y in _overlapping_tiles(fx, fy, r, ts):
        if world.get_tile_grid(tile_x, tile_y) == TILE_SOLID:
            tx_min = tile_x * ts
            tx_max = tx_min + ts
            ty_min = tile_y * ts
            ty_max = ty_min + ts
            if fx + r > tx_min and fx - r < tx_max:
                if fy + r > ty_min and fy - r < ty_max:
                    if oy + r <= ty_min + 1:
                        fy = ty_min - r
                        vy = 0
                        on_ground = True
                    elif oy - r >= ty_max - 1:
                        fy = ty_max + r
                        if vy < 0:
                            vy = 0

    return fx, fy, vx, vy, on_ground


def _overlapping_tiles(cx, cy, r, ts):
    """Retourne les coordonnées grille des tuiles qui pourraient se superposer au cercle."""
    x0 = int((cx - r) / ts)
    x1 = int((cx + r) / ts)
    y0 = int((cy - r) / ts)
    y1 = int((cy + r) / ts)
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            yield tx, ty
