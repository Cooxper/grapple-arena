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
                
                # Détection du saut (appui unique)
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_z, pygame.K_SPACE]:
                        jump_requested = True

                # --- GESTION DU GRAPPIN (SOURIS) ---
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic gauche : on lance
                        m_pos = pygame.math.Vector2(pygame.mouse.get_pos())
                        self.player.fire_hook(m_pos, self.world)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # Relâcher : on décroche
                        self.player.is_hooked = False

            # 3. BOUCLE DE PHYSIQUE FIXE (Simulation "Serveur")
            while accumulator >= tick_rate:
                keys = pygame.key.get_pressed()
                
                # Préparation du dictionnaire d'inputs
                inputs = {
                    'left': keys[pygame.K_q],
                    'right': keys[pygame.K_d],
                    'jump': jump_requested
                }
                
                # Mise à jour de la physique (inclut maintenant la traction du grappin)
                self.player.update_physics(self.world, inputs)
                
                # Reset du signal de saut une fois consommé
                jump_requested = False
                accumulator -= tick_rate

            # 4. RENDU
            self.screen.fill(COLOR_BG)

            # Dessin de la Map
            for row_index, row in enumerate(GAME_MAP):
                for col_index, tile in enumerate(row):
                    if tile == 1:
                        pygame.draw.rect(self.screen, (100, 100, 100), 
                                         (col_index * TILE_SIZE, row_index * TILE_SIZE, 
                                          TILE_SIZE - 1, TILE_SIZE - 1))

            # --- DESSIN DE LA CORDE DU GRAPPIN ---
            if self.player.is_hooked:
                # On part du centre du joueur
                start_p = (self.player.pos.x + self.player.size/2, 
                           self.player.pos.y + self.player.size/2)
                # On dessine vers le point d'impact enregistré
                pygame.draw.line(self.screen, HOOK_COLOR, start_p, self.player.hook_pos, 2)

            # Dessin du joueur
            pygame.draw.rect(self.screen, COLOR_PLAYER, 
                            (self.player.pos.x, self.player.pos.y, 
                             self.player.size, self.player.size))
            
            pygame.display.flip()
            
            # Limite l'affichage aux FPS définis (ex: 144)
            self.clock.tick(FPS)