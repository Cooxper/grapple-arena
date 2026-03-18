# collision.cpp — traduction exacte
# MoveBox, IsOnGround, IntersectLine, GetTile

import math
from tuning import PHYS_SIZE

TILE_SIZE = 32

# mapitems.h tile IDs
TILE_AIR    = 0
TILE_SOLID  = 1
TILE_DEATH  = 2
TILE_START  = 33
TILE_FINISH = 34

_tiles  = []
_width  = 0
_height = 0


def load(tiles, width, height):
    global _tiles, _width, _height
    _tiles, _width, _height = tiles, width, height


def get_tile(x, y):
    tx = int(math.floor(x)) // TILE_SIZE
    ty = int(math.floor(y)) // TILE_SIZE
    if tx < 0 or ty < 0 or tx >= _width or ty >= _height:
        return TILE_SOLID
    return _tiles[ty * _width + tx]


def is_solid(x, y):
    return get_tile(x, y) == TILE_SOLID


def is_on_ground(px, py):
    """
    CCollision::IsOnGround — vérifie 1px sous le bas du Tee
    """
    r = PHYS_SIZE / 2
    y = py + r + 1
    return is_solid(px - r + 1, y) or is_solid(px, y) or is_solid(px + r - 1, y)


def move_box(px, py, vx, vy):
    """
    CCollision::MoveBox — déplacement exact avec résolution de collision.
    Retourne (new_px, new_py, new_vx, new_vy, grounded).

    DDNet déplace séparément X puis Y.
    Pour chaque axe, on teste les 3 points de contact du côté du mouvement.
    """
    r        = PHYS_SIZE / 2
    grounded = False

    # ── Axe X ────────────────────────────────────
    px += vx
    if vx > 0:
        if (is_solid(px + r, py - r + 1) or
            is_solid(px + r, py         ) or
            is_solid(px + r, py + r - 1)):
            px = math.floor((px + r) / TILE_SIZE) * TILE_SIZE - r
            vx = 0.0
    elif vx < 0:
        if (is_solid(px - r, py - r + 1) or
            is_solid(px - r, py         ) or
            is_solid(px - r, py + r - 1)):
            px = math.ceil((px - r) / TILE_SIZE) * TILE_SIZE + r
            vx = 0.0

    # ── Axe Y ────────────────────────────────────
    py += vy
    if vy > 0:
        if (is_solid(px - r + 1, py + r) or
            is_solid(px,          py + r) or
            is_solid(px + r - 1,  py + r)):
            py       = math.floor((py + r) / TILE_SIZE) * TILE_SIZE - r
            vy       = 0.0
            grounded = True
    elif vy < 0:
        if (is_solid(px - r + 1, py - r) or
            is_solid(px,          py - r) or
            is_solid(px + r - 1,  py - r)):
            py = math.ceil((py - r) / TILE_SIZE) * TILE_SIZE + r
            vy = 0.0

    return px, py, vx, vy, grounded


def intersect_line(x0, y0, x1, y1):
    """
    CCollision::IntersectLine — rayon vers le 1er mur solide.
    Retourne (hx, hy) ou None.
    """
    dist  = math.hypot(x1 - x0, y1 - y0)
    if dist == 0:
        return None
    steps = max(int(dist / (TILE_SIZE * 0.5)), 1)
    prev_x, prev_y = x0, y0
    for i in range(1, steps + 1):
        t  = i / steps
        cx = x0 + (x1 - x0) * t
        cy = y0 + (y1 - y0) * t
        if is_solid(cx, cy):
            return prev_x, prev_y
        prev_x, prev_y = cx, cy
    return None