import pygame
import sys
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import *

def run(self):
        while True:
            # dt est le temps écoulé en millisecondes, on le divise par 1000 pour l'avoir en secondes
            # On cap à FPS pour la fluidité d'affichage, mais la physique utilisera dt
            dt = self.clock.tick(FPS) / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # ... garde ta gestion du grappin ici ...

            # --- PASSAGE DU DT À LA PHYSIQUE ---
            self.player.update_physics(self.world, dt)
            

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DDNet Prototype - Greybox")
        self.clock = pygame.time.Clock()
        
        # Initialisation du monde et du joueur
        self.world = World()
        self.player = Entity(100, 100)

    def run(self):
        while True:
            # 1. Événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 2. Entrées Clavier (Contrôles simples)
            keys = pygame.key.get_pressed()
            # On considère qu'on est au sol si la vélocité Y est nulle 
            # (Note: Ce sera amélioré avec une détection précise plus tard)
            on_ground = abs(self.player.vel.y) < 0.1 

            if keys[pygame.K_q]: self.player.move_left(on_ground)
            if keys[pygame.K_d]: self.player.move_right(on_ground)
            if (keys[pygame.K_z] or keys[pygame.K_SPACE]) and on_ground:
                self.player.jump()

            # 3. Mise à jour Physique (On passe le monde en paramètre !)
            self.player.update_physics(self.world)

            # 4. Rendu
            self.screen.fill(COLOR_BG)

            # Dessiner la Map (les blocs gris)
            for row_index, row in enumerate(GAME_MAP):
                for col_index, tile in enumerate(row):
                    if tile == 1:
                        pygame.draw.rect(self.screen, (100, 100, 100), 
                                         (col_index * TILE_SIZE, row_index * TILE_SIZE, 
                                          TILE_SIZE - 1, TILE_SIZE - 1)) # -1 pour voir la grille

            # Dessiner le joueur (le carré rouge)
            pygame.draw.rect(self.screen, COLOR_PLAYER, 
                            (self.player.pos.x, self.player.pos.y, 
                             self.player.size, self.player.size))
            
            pygame.display.flip()
            self.clock.tick(FPS)