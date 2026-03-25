import pygame
import sys
import time
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import *

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Grapple Arena - Settings")
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Entity(100, 100)
        self.state = "GAME"
        
        # Variables dynamiques (pour pouvoir les modifier dans le menu)
        self.current_fps = FPS
        self.current_gravity = GRAVITY
        self.selected_tab = "PHYSIQUE"

    def draw_game(self):
        # (Ton code de dessin habituel)
        for row_index, row in enumerate(GAME_MAP):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(self.screen, (100, 100, 100), 
                                     (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
        if self.player.is_hooked:
            p_center = (self.player.pos.x + self.player.size/2, self.player.pos.y + self.player.size/2)
            pygame.draw.line(self.screen, HOOK_COLOR, p_center, self.player.hook_pos, 2)
        pygame.draw.rect(self.screen, COLOR_PLAYER, (self.player.pos.x, self.player.pos.y, self.player.size, self.player.size))

    def draw_settings_menu(self):
        # 1. Fond principal
        self.screen.fill(UI_BG)
        
        # 2. Panneau latéral (Tabs)
        pygame.draw.rect(self.screen, UI_PANEL, (0, 0, 200, WINDOW_HEIGHT))
        font = pygame.font.SysFont("Arial", 20, bold=True)
        
        tabs = ["GÉNÉRAL", "PHYSIQUE", "CONTRÔLES"]
        for i, tab in enumerate(tabs):
            color = UI_ACCENT if self.selected_tab == tab else UI_TEXT
            txt = font.render(tab, True, color)
            self.screen.blit(txt, (40, 100 + i * 50))

        # 3. Zone de contenu
        content_font = pygame.font.SysFont("Arial", 18)
        title_font = pygame.font.SysFont("Arial", 30, bold=True)
        
        title_txt = title_font.render(f"RÉGLAGES : {self.selected_tab}", True, (255, 255, 255))
        self.screen.blit(title_txt, (250, 50))

        if self.selected_tab == "PHYSIQUE":
            self.draw_setting_row("Gravité", f"{self.current_gravity:.2f}", 150, "GRAV")
            self.draw_setting_row("FPS Max", f"{self.current_fps}", 210, "FPS")

    def draw_setting_row(self, label, value, y, id):
        """Dessine une ligne de réglage avec des boutons +/-"""
        font = pygame.font.SysFont("Arial", 20)
        # Label
        lbl = font.render(label, True, UI_TEXT)
        self.screen.blit(lbl, (250, y))
        
        # Boîte de valeur
        pygame.draw.rect(self.screen, UI_PANEL, (400, y-5, 100, 30), border_radius=5)
        val_txt = font.render(value, True, UI_ACCENT)
        self.screen.blit(val_txt, (410, y))

        # Boutons (On les dessine, la détection est dans run())
        pygame.draw.rect(self.screen, (60, 65, 80), (510, y-5, 30, 30), border_radius=5) # Moins
        pygame.draw.rect(self.screen, (60, 65, 80), (545, y-5, 30, 30), border_radius=5) # Plus
        self.screen.blit(font.render("-", True, (255, 255, 255)), (520, y))
        self.screen.blit(font.render("+", True, (255, 255, 255)), (555, y))

    def run(self):
        tick_rate = 1.0 / 60.0
        accumulator = 0.0
        last_time = time.time()
        jump_requested = False

        while True:
            current_time = time.time()
            frame_time = current_time - last_time
            last_time = current_time
            accumulator += frame_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "SETTINGS" if self.state == "GAME" else "GAME"
                    
                    if self.state == "GAME":
                        if event.key in [pygame.K_z, pygame.K_SPACE]:
                            jump_requested = True

                # --- CLICS SOURIS ---
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    m_pos = pygame.mouse.get_pos()
                    
                    if self.state == "GAME":
                        self.player.fire_hook(pygame.math.Vector2(m_pos), self.world)
                    
                    elif self.state == "SETTINGS":
                        # Logique simplifiée de clic sur les boutons +/-
                        # (On vérifie la position Y pour savoir quelle ligne est cliquée)
                        if 145 < m_pos[1] < 175: # Ligne Gravité
                            if 510 < m_pos[0] < 540: self.current_gravity -= 0.05
                            if 545 < m_pos[0] < 575: self.current_gravity += 0.05
                            # Mise à jour immédiate de la physique globale
                            import src.common.settings as st
                            st.GRAVITY = self.current_gravity
                        
                        if 205 < m_pos[1] < 235: # Ligne FPS
                            if 510 < m_pos[0] < 540: self.current_fps -= 10
                            if 545 < m_pos[0] < 575: self.current_fps += 10
                            self.current_fps = max(30, self.current_fps)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state == "GAME":
                        self.player.is_hooked = False

            # --- LOGIQUE ---
            if self.state == "GAME":
                while accumulator >= tick_rate:
                    keys = pygame.key.get_pressed()
                    inputs = {'left': keys[pygame.K_q], 'right': keys[pygame.K_d], 'jump': jump_requested}
                    self.player.update_physics(self.world, inputs)
                    jump_requested = False
                    accumulator -= tick_rate
            else:
                accumulator = 0

            # --- RENDU ---
            if self.state == "GAME":
                self.screen.fill(COLOR_BG)
                self.draw_game()
            else:
                self.draw_settings_menu()
            
            pygame.display.flip()
            self.clock.tick(self.current_fps)