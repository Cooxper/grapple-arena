# ============================================================
#  world.py  –  Grille de tuiles, chargement depuis PNG
# ============================================================
from __future__ import annotations
import pygame
from src.common.settings import (
    TILE_SIZE, TILE_EMPTY, TILE_SOLID, TILE_KILL,
    MAP_PATH, MAP_SCALE_DIV,
)


class World:
    """Grille de tuiles chargée depuis une image PNG.

    Convention couleurs de l'image :
      - Blanc  (r>200, g>200, b>200)  →  TILE_EMPTY  (0)
      - Gris / sombre                  →  TILE_SOLID  (1)
      - Rouge  (r>150, g<80, b<80)     →  TILE_KILL   (2)
    """

    def __init__(self):
        self.grid: list[list[int]] = []
        self.width  = 0   # colonnes
        self.height = 0   # lignes
        self.pixel_width  = 0
        self.pixel_height = 0

    # ----------------------------------------------------------
    #  Chargement
    # ----------------------------------------------------------
    def load_from_image(self, path: str = MAP_PATH):
        raw = pygame.image.load(path).convert()
        # Divise la taille par MAP_SCALE_DIV pour les performances
        w = raw.get_width()  // MAP_SCALE_DIV
        h = raw.get_height() // MAP_SCALE_DIV
        img = pygame.transform.scale(raw, (w, h))

        self.width  = w // TILE_SIZE
        self.height = h // TILE_SIZE
        self.pixel_width  = self.width  * TILE_SIZE
        self.pixel_height = self.height * TILE_SIZE

        self.grid = [[TILE_EMPTY] * self.width for _ in range(self.height)]

        for row in range(self.height):
            for col in range(self.width):
                # Pixel au centre de la tuile
                px = col * TILE_SIZE + TILE_SIZE // 2
                py = row * TILE_SIZE + TILE_SIZE // 2
                if px < w and py < h:
                    r, g, b, *_ = img.get_at((px, py))
                    self.grid[row][col] = _classify_pixel(r, g, b)

        print(f"[World] Grille chargée : {self.width}×{self.height} tuiles "
              f"({self.pixel_width}×{self.pixel_height} px)")

    # ----------------------------------------------------------
    #  Accès aux tuiles
    # ----------------------------------------------------------
    def get_tile_grid(self, col: int, row: int) -> int:
        """Retourne le type de la tuile à (col, row). TILE_SOLID hors limites."""
        if col < 0 or row < 0 or col >= self.width or row >= self.height:
            return TILE_SOLID
        return self.grid[row][col]

    def get_tile(self, world_x: float, world_y: float) -> int:
        """Retourne le type de la tuile aux coordonnées monde (px)."""
        col = int(world_x // TILE_SIZE)
        row = int(world_y // TILE_SIZE)
        return self.get_tile_grid(col, row)

    # ----------------------------------------------------------
    #  Tuiles visibles dans un rectangle donné  (pour le rendu)
    # ----------------------------------------------------------
    def visible_tiles(self, cam_x: float, cam_y: float,
                      screen_w: int, screen_h: int,
                      zoom: float):
        """Yield (col, row, tile_type) pour toutes les tuiles visibles."""
        inv_zoom = 1.0 / zoom
        left   = cam_x - screen_w * 0.5 * inv_zoom
        top    = cam_y - screen_h * 0.5 * inv_zoom
        right  = cam_x + screen_w * 0.5 * inv_zoom
        bottom = cam_y + screen_h * 0.5 * inv_zoom

        col0 = max(0, int(left  / TILE_SIZE))
        col1 = min(self.width  - 1, int(right  / TILE_SIZE))
        row0 = max(0, int(top   / TILE_SIZE))
        row1 = min(self.height - 1, int(bottom / TILE_SIZE))

        for row in range(row0, row1 + 1):
            for col in range(col0, col1 + 1):
                t = self.grid[row][col]
                if t != TILE_EMPTY:
                    yield col, row, t


# ----------------------------------------------------------
#  Classification d'un pixel en type de tuile
# ----------------------------------------------------------
def _classify_pixel(r: int, g: int, b: int) -> int:
    # Rouge → mort
    if r > 150 and g < 80 and b < 80:
        return TILE_KILL
    # Sombre / gris → solide
    if r < 180 and g < 180 and b < 180:
        return TILE_SOLID
    # Blanc / clair → vide
    return TILE_EMPTY

