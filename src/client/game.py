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
        self.screen.fill(UI_DARK_BG)
        
        # 2. Barre de Navigation Haute
        pygame.draw.rect(self.screen, UI_NAV_BAR, (0, 0, WINDOW_WIDTH, 40))
        nav_font = pygame.font.SysFont("Arial", 14, bold=True)
        nav_tabs = ["Aimbot", "Misc", "Visuals & HUD", "Avoid", "TAS", "Settings"]
        for i, tab in enumerate(nav_tabs):
            color = UI_ACCENT_BLUE if tab == "Settings" else (200, 200, 200)
            txt = nav_font.render(tab, True, color)
            self.screen.blit(txt, (100 + i * 110, 12))

        # 3. Menu Vertical de Droite (comme sur ta photo)
        right_w = 180
        pygame.draw.rect(self.screen, UI_NAV_BAR, (WINDOW_WIDTH - right_w, 40, right_w, WINDOW_HEIGHT - 40))
        side_font = pygame.font.SysFont("Arial", 16)
        side_tabs = ["General", "Player", "Appearance", "Controls", "Graphics", "Sound"]
        
        for i, tab in enumerate(side_tabs):
            color = UI_ACCENT_BLUE if self.selected_tab == tab else (150, 150, 160)
            txt = side_font.render(tab, True, color)
            self.screen.blit(txt, (WINDOW_WIDTH - right_w + 30, 80 + i * 40))

        # 4. Panneaux de contenu (Les cartes "Hotkeys" et "Settings")
        if self.selected_tab == "Graphics" or self.selected_tab == "PHYSIQUE":
            # Carte de Gauche
            self.draw_card("Performance", 50, 70, 400, 450)
            self.draw_setting_row("Max FPS", f"{self.current_fps}", 50, 130)
            
            # Carte de Droite
            self.draw_card("Settings", 470, 70, 380, 250)
            self.draw_setting_row("Show FPS", "Enabled" if getattr(self, 'show_fps', True) else "Disabled", 470, 130)

    def draw_card(self, title, x, y, w, h):
        """Dessine les cadres arrondis de ta photo"""
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, UI_PANEL_BG, rect, border_radius=10)
        font = pygame.font.SysFont("Arial", 22, bold=True)
        txt = font.render(title, True, (255, 255, 255))
        self.screen.blit(txt, (x + 20, y + 15))

    def draw_setting_row(self, label, value, x, y):
        """Dessine une ligne de réglage style KRX"""
        font = pygame.font.SysFont("Arial", 16)
        lbl = font.render(label, True, (230, 230, 230))
        self.screen.blit(lbl, (x + 20, y))
        
        # Champ de valeur (le rectangle bleu-gris)
        pygame.draw.rect(self.screen, UI_BUTTON_BG, (x + 160, y - 5, 180, 25), border_radius=5)
        v_txt = font.render(value, True, (255, 255, 255))
        self.screen.blit(v_txt, (x + 170, y - 2))

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
        # Variables pour le Fixed Timestep (Physique 60Hz)
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

                # --- GESTION DES CLICS SOURIS ---
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    m_pos = pygame.mouse.get_pos()
                    
                    if self.state == "GAME":
                        self.player.fire_hook(pygame.math.Vector2(m_pos), self.world)
                    
                    elif self.state == "SETTINGS":
                        # 1. CLIC SUR LE MENU DE DROITE (Changement d'onglets)
                        # Largeur du menu droite = 180px (WINDOW_WIDTH - 180)
                        if m_pos[0] > WINDOW_WIDTH - 180:
                            # Chaque onglet fait environ 40px de haut, départ à y=80
                            index = (m_pos[1] - 80) // 40
                            tabs = ["General", "Player", "Appearance", "Controls", "Graphics", "Sound"]
                            if 0 <= index < len(tabs):
                                self.selected_tab = tabs[index]
                        
                        # 2. CLIC SUR LES RÉGLAGES (Exemple pour l'onglet Graphics)
                        elif self.selected_tab == "Graphics":
                            # Détection de la ligne Max FPS (y=130)
                            if 125 < m_pos[1] < 155:
                                # Si on clique dans la zone du bouton (x entre 210 et 400 environ)
                                if 210 < m_pos[0] < 410:
                                    # Alterne entre 60, 144 et 240 FPS
                                    fps_levels = [60, 144, 240]
                                    curr_idx = fps_levels.index(self.current_fps) if self.current_fps in fps_levels else 0
                                    self.current_fps = fps_levels[(curr_idx + 1) % len(fps_levels)]
                            
                            # Détection de la ligne Show FPS (y=170)
                            elif 165 < m_pos[1] < 195:
                                if 210 < m_pos[0] < 410:
                                    self.show_fps = not self.show_fps

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state == "GAME":
                        self.player.is_hooked = False

            # --- LOGIQUE PHYSIQUE ---
            if self.state == "GAME":
                while accumulator >= tick_rate:
                    keys = pygame.key.get_pressed()
                    inputs = {
                        'left': keys[pygame.K_q], 
                        'right': keys[pygame.K_d], 
                        'jump': jump_requested
                    }
                    self.player.update_physics(self.world, inputs)
                    jump_requested = False
                    accumulator -= tick_rate
            else:
                # En pause/menu, on reset l'accumulateur pour éviter un bond de physique
                accumulator = 0

            # --- RENDU ---
            if self.state == "GAME":
                self.screen.fill(COLOR_BG)
                self.draw_game()
            else:
                self.draw_settings_menu()
            
            pygame.display.flip()
            # On utilise la variable dynamique pour les FPS
            self.clock.tick(self.current_fps)