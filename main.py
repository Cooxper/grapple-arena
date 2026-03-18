import pygame
import random

pygame.init()


SCREEN_W, SCREEN_H = 900, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Grapple Arena Solo – Gravité & Caméra")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)


WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
BLUE = (0, 160, 255)


WORLD_W, WORLD_H = 2400, 1600


player = pygame.Rect(200, 200, 24, 24)
vel_x = 0
vel_y = 0
player.x = 800
player.y = 660

SPEED = 6
GRAVITY = 0.5
JUMP_POWER = -10
on_ground = False



grapple_active = False
grapple_point = None
GRAPPLE_RANGE = 800
GRAPPLE_FORCE = 1.8



camera_x = 0
camera_y = 0


walls = []

def generate_map():
    walls.clear()

   
    walls.append(pygame.Rect(0, 0, 2000, 20))       
    walls.append(pygame.Rect(0, 1180, 2000, 20))   
    walls.append(pygame.Rect(0, 0, 20, 1200))        
    walls.append(pygame.Rect(1980, 0, 20, 1200))    

    
    walls.append(pygame.Rect(500, 700, 700, 20))


    walls.append(pygame.Rect(200, 200, 20, 500))
    walls.append(pygame.Rect(200, 500, 200, 20))
    walls.append(pygame.Rect(400, 200, 20, 250))

 
    walls.append(pygame.Rect(1300, 300, 400, 20))
    walls.append(pygame.Rect(1500, 300, 20, 250))
    walls.append(pygame.Rect(1500, 550, 200, 20))
    walls.append(pygame.Rect(1700, 550, 20, 300))

   
    walls.append(pygame.Rect(300, 350, 120, 20))
    walls.append(pygame.Rect(1650, 420, 120, 20))

generate_map()


def get_grapple_point(start, end):
    steps = 40
    for i in range(steps):
        t = i / steps
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        point = pygame.Rect(x, y, 4, 4)

        for wall in walls:
            if wall.colliderect(point):
                return (x, y)
    return None



def draw_text(txt, x, y):
    img = font.render(txt, True, BLACK)
    screen.blit(img, (x, y))

def move_and_collide(rect, dx, dy):
    rect.x += dx
    for wall in walls:
        if rect.colliderect(wall):
            if dx > 0:
                rect.right = wall.left
            if dx < 0:
                rect.left = wall.right

    rect.y += dy
    global on_ground
    on_ground = False
    for wall in walls:
        if rect.colliderect(wall):
            if dy > 0:
                rect.bottom = wall.top
                on_ground = True
                return
            if dy < 0:
                rect.top = wall.bottom
                return


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            world_mouse = (mx + camera_x, my + camera_y)

            px, py = player.center
            dx = world_mouse[0] - px
            dy = world_mouse[1] - py
            distance = (dx**2 + dy**2) ** 0.5

            if distance <= GRAPPLE_RANGE:
                hit = get_grapple_point((px, py), world_mouse)
                if hit:
                    grapple_point = hit
                    grapple_active = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            grapple_active = False
            grapple_point = None

        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    vel_x = 0

    if keys[pygame.K_q] or keys[pygame.K_a]:
        vel_x = -SPEED
    if keys[pygame.K_d]:
        vel_x = SPEED
    if (keys[pygame.K_z] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and on_ground:
        vel_y = JUMP_POWER

  
    vel_y += GRAVITY
    if vel_y > 12:
        vel_y = 12

    move_and_collide(player, vel_x, vel_y)


    if grapple_active and grapple_point:
        dx = grapple_point[0] - player.centerx
        dy = grapple_point[1] - player.centery
        dist = (dx**2 + dy**2) ** 0.5

        if dist > 10:
            vel_x += dx * GRAPPLE_FORCE / dist
            vel_y += dy * GRAPPLE_FORCE / dist
        else:
            grapple_active = False
            grapple_point = None

    camera_x = player.centerx - SCREEN_W // 2
    camera_y = player.centery - SCREEN_H // 2

    camera_x = max(0, min(camera_x, WORLD_W - SCREEN_W))
    camera_y = max(0, min(camera_y, WORLD_H - SCREEN_H))


    screen.fill(WHITE)

    for wall in walls:
        pygame.draw.rect(
            screen,
            BLACK,
            pygame.Rect(
                wall.x - camera_x,
                wall.y - camera_y,
                wall.width,
                wall.height,
            ),
        )

    pygame.draw.rect(
        screen,
        BLUE,
        pygame.Rect(
            player.x - camera_x,
            player.y - camera_y,
            player.width,
            player.height,
        ),
    )

    if grapple_active and grapple_point:
        pygame.draw.line(
            screen,
            (50, 50, 50),
            (player.centerx - camera_x, player.centery - camera_y),
            (grapple_point[0] - camera_x, grapple_point[1] - camera_y),
            2
        )


  
    draw_text("Déplacements : Q/D ou ← →", 10, SCREEN_H - 60)
    draw_text("Saut : Z / ESPACE", 10, SCREEN_H - 40)
    draw_text("Objectif : explorer la map", 10, SCREEN_H - 20)

    pygame.display.flip()

pygame.quit()
