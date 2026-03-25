import pygame
import sys
import time
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import *

class GameClient:
    def __init__(self):
        pygame.init()
        # On peut mettre 0 ou une valeur haute pour les FPS ici
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Entity(100, 100)
        
        # Variables pour le Fixed Timestep
        self.tick_rate = 1.0 / 60.0  # On veut 60 ticks de physique par seconde
        self.accumulator = 0.0
        self.last_time = time.time()

    def run(self):
        # Variables pour le Fixed Timestep (Physique bloquée à 60Hz)
        tick_rate = 1.0 / 60.0
        accumulator = 0.0
        last_time = time.time()
        
        # Variable pour capturer l'événement de saut unique
        jump_requested = False

        while True:
            # 1. Calcul du Delta Time pour l'accumulateur
            current_time = time.time()
            frame_time = current_time - last_time
            last_time = current_time
            accumulator += frame_time

            # 2. Gestion des événements (Entrées uniques)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Détection du saut (appui unique pour autoriser le double saut)
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_z, pygame.K_SPACE]:
                        jump_requested = True

            # 3. BOUCLE DE PHYSIQUE FIXE (Simulation "Serveur")
            # On rattrape le retard de physique si nécessaire
            while accumulator >= tick_rate:
                keys = pygame.key.get_pressed()
                
                # Préparation du dictionnaire d'inputs
                inputs = {
                    'left': keys[pygame.K_q],
                    'right': keys[pygame.K_d],
                    'jump': jump_requested
                }
                
                # Mise à jour de la physique (Tick fixe de 1/60s)
                self.player.update_physics(self.world, inputs)
                
                # Reset du signal de saut une fois consommé
                jump_requested = False
                accumulator -= tick_rate

            # 4. RENDU (Aussi fluide que possible)
            self.screen.fill(COLOR_BG)

            # Dessin de la Map (les blocs gris)
            for row_index, row in enumerate(GAME_MAP):
                for col_index, tile in enumerate(row):
                    if tile == 1:
                        pygame.draw.rect(self.screen, (100, 100, 100), 
                                         (col_index * TILE_SIZE, row_index * TILE_SIZE, 
                                          TILE_SIZE - 1, TILE_SIZE - 1))

            # Dessin du joueur (le carré rouge)
            pygame.draw.rect(self.screen, COLOR_PLAYER, 
                            (self.player.pos.x, self.player.pos.y, 
                             self.player.size, self.player.size))
            
            pygame.display.flip()
            
            # Limite l'affichage aux FPS définis dans settings.py (ex: 144)
            self.clock.tick(FPS)