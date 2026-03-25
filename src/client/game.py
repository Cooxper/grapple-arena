import pygame
import sys
import time
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import *

class GameClient:
    def __init__(self):
        pygame.init()
        # Initialisation de la fenêtre avec les constantes de settings.py
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Grapple Arena - KRX Style")
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Entity(100, 100)
        
        # --- ÉTATS DU MENU ---
        self.state = "GAME"
        self.selected_tab = "Graphics"
        self.show_fps = True
        self.current_fps = FPS
        self.current_gravity = GRAVITY


    def draw_game(self):
        """Affiche le gameplay : Map, Grappin, Joueur et FPS"""
        # 1. Dessin de la Map
        for row_index, row in enumerate(GAME_MAP):
            for col_index, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(self.screen, (100, 100, 100), 
                                     (col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
        
        # 2. Dessin de la corde du Grappin
        if self.player.is_hooked:
            p_center = (self.player.pos.x + self.player.size/2, self.player.pos.y + self.player.size/2)
            pygame.draw.line(self.screen, HOOK_COLOR, p_center, self.player.hook_pos, 2)
        
        # 3. Dessin du Joueur
        pygame.draw.rect(self.screen, COLOR_PLAYER, (self.player.pos.x, self.player.pos.y, self.player.size, self.player.size))

        # 4. HUD : Affichage des FPS style DDNet
        if self.show_fps:
            fps_val = int(self.clock.get_fps())
            font = pygame.font.SysFont("Arial", 14, bold=True)
            txt = font.render(f"{fps_val} FPS", True, (0, 255, 0))
            self.screen.blit(txt, (10, 10))

    def draw_settings_menu(self):
        """Affiche l'interface de réglages inspirée de KRX"""
        self.screen.fill(UI_DARK_BG)
        
        # 1. Barre de Navigation Haute
        pygame.draw.rect(self.screen, UI_NAV_BAR, (0, 0, WINDOW_WIDTH, 40))
        nav_tabs = ["Aimbot", "Misc", "Visuals & HUD", "Avoid", "TAS", "Settings"]
        for i, tab in enumerate(nav_tabs):
            color = UI_ACCENT_BLUE if tab == "Settings" else UI_TEXT
            txt = pygame.font.SysFont("Arial", 14, bold=True).render(tab, True, color)
            self.screen.blit(txt, (80 + i * 110, 12))

        # 2. Menu Vertical de Droite
        right_w = 180
        pygame.draw.rect(self.screen, UI_NAV_BAR, (WINDOW_WIDTH - right_w, 40, right_w, WINDOW_HEIGHT - 40))
        side_tabs = ["General", "Player", "Appearance", "Controls", "Graphics", "Sound"]
        for i, tab in enumerate(side_tabs):
            color = UI_ACCENT_BLUE if self.selected_tab == tab else (150, 150, 160)
            txt = pygame.font.SysFont("Arial", 16).render(tab, True, color)
            self.screen.blit(txt, (WINDOW_WIDTH - right_w + 30, 80 + i * 40))

        # 3. Contenu Central dynamique selon l'onglet
        if self.selected_tab == "Graphics":
            self.draw_card("Performance", 50, 70, 400, 300)
            self.draw_setting_row("Max FPS", f"{self.current_fps}", 50, 130)
            self.draw_setting_row("Show FPS", "ON" if self.show_fps else "OFF", 50, 170)
        
        elif self.selected_tab == "General":
            self.draw_card("Physique", 50, 70, 400, 300)
            self.draw_setting_row("Gravité", f"{self.current_gravity:.2f}", 50, 130)


    def draw_card(self, title, x, y, w, h):
        """Dessine une carte (panel) avec bordures arrondies"""
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, UI_PANEL_BG, rect, border_radius=10)
        txt = pygame.font.SysFont("Arial", 20, bold=True).render(title, True, (255, 255, 255))
        self.screen.blit(txt, (x + 20, y + 15))


    def draw_setting_row(self, label, value, x, y):
        font = pygame.font.SysFont("Arial", 16)
        lbl = font.render(label, True, UI_TEXT)
        self.screen.blit(lbl, (x + 20, y))
        
        # Champ de valeur
        pygame.draw.rect(self.screen, UI_BUTTON_BG, (x + 160, y - 5, 180, 25), border_radius=5)
        
        # Transformation du texte si 999
        display_value = "Unlimited" if value == "999" else value
        
        v_txt = font.render(display_value, True, (255, 255, 255))
        self.screen.blit(v_txt, (x + 170, y - 2))


    def run(self):
        """Boucle principale avec Fixed Timestep (60Hz)"""
        tick_rate = 1.0 / 60.0
        accumulator = 0.0
        last_time = time.time()
        jump_requested = False

        while True:
            current_time = time.time()
            frame_time = current_time - last_time
            last_time = current_time
            accumulator += frame_time

            # 1. Gestion des Événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "SETTINGS" if self.state == "GAME" else "GAME"
                    
                    if self.state == "GAME":
                        if event.key in [pygame.K_z, pygame.K_SPACE]:
                            jump_requested = True

                # 2. Gestion des Clics
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    m_pos = pygame.mouse.get_pos()
                    
                    if self.state == "GAME":
                        self.player.fire_hook(pygame.math.Vector2(m_pos), self.world)
                    
                    elif self.state == "SETTINGS":
                        # Clic sur le menu de droite
                        if m_pos[0] > WINDOW_WIDTH - 180:
                            idx = (m_pos[1] - 80) // 40
                            tabs = ["General", "Player", "Appearance", "Controls", "Graphics", "Sound"]
                            if 0 <= idx < len(tabs): self.selected_tab = tabs[idx]
                        
                        # Interaction avec les réglages Graphics
                        if self.selected_tab == "Graphics":
                            # Détection de la ligne Max FPS (y=130)
                            if 125 < m_pos[1] < 155 and 210 < m_pos[0] < 410:
                                # On passe à l'index suivant dans la liste [60, 120, 180, 240, 999]
                                self.fps_idx = (self.fps_idx + 1) % len(self.fps_options)
                                self.current_fps = self.fps_options[self.fps_idx]
                            
                            # Détection de la ligne Show FPS (y=170)
                            if 165 < m_pos[1] < 195 and 210 < m_pos[0] < 410:
                                self.show_fps = not self.show_fps

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state == "GAME":
                        self.player.is_hooked = False

            # 3. Logique de Physique Fixe
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
                accumulator = 0 # Évite le "saut" temporel après la pause

            # 4. Rendu Final
            if self.state == "GAME":
                self.screen.fill(COLOR_BG)
                self.draw_game()
            else:
                self.draw_settings_menu()
            
            pygame.display.flip()
            self.clock.tick(self.current_fps) # Utilise la valeur modifiée en jeu