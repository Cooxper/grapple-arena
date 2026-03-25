import pygame
import sys
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import *

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DDNet Prototype - Greybox")
        self.clock = pygame.time.Clock()
        
        self.world = World()
        self.player = Entity(100, 100)

    def run(self):
        while True:
            # Calcul du Delta Time (indépendance FPS)
            dt = self.clock.tick(FPS) / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            
            # Détection du sol précise
            on_ground = self.world.check_collision(self.player.pos.x, self.player.pos.y + self.player.size + 1) or \
                        self.world.check_collision(self.player.pos.x + self.player.size, self.player.pos.y + self.player.size + 1)

            # Contrôles avec dt
            if keys[pygame.K_q]: self.player.move_left(on_ground, dt)
            if keys[pygame.K_d]: self.player.move_right(on_ground, dt)
            if (keys[pygame.K_z] or keys[pygame.K_SPACE]) and on_ground:
                self.player.jump()

            # Mise à jour avec dt
            self.player.update_physics(self.world, dt)

            # Rendu
            self.screen.fill(COLOR_BG)
            for row_index, row in enumerate(GAME_MAP):
                for col_index, tile in enumerate(row):
                    if tile == 1:
                        pygame.draw.rect(self.screen, (100, 100, 100), 
                                         (col_index * TILE_SIZE, row_index * TILE_SIZE, 
                                          TILE_SIZE - 1, TILE_SIZE - 1))

            pygame.draw.rect(self.screen, COLOR_PLAYER, 
                            (self.player.pos.x, self.player.pos.y, 
                             self.player.size, self.player.size))
            
            pygame.display.flip()