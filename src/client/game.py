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
        pygame.display.set_caption("Grapple Arena - Camera & KillBricks")
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Entity(PLAYER_START_POS[0], PLAYER_START_POS[1])
        self.state = "GAME"
        self.camera_zoom = 1.0
        self.selected_tab = "Graphics"
        self.show_fps = True
        self.fps_options = [60, 120, 180, 240, 999]
        self.fps_idx = 0 
        self.current_fps = self.fps_options[self.fps_idx]
        self.current_gravity = GRAVITY

    def draw_game(self, alpha):
        # 1. Calcul position et caméra
        interp_x = self.player.old_pos.x + (self.player.pos.x - self.player.old_pos.x) * alpha
        interp_y = self.player.old_pos.y + (self.player.pos.y - self.player.old_pos.y) * alpha
        cam_x = interp_x - WINDOW_WIDTH // 2
        cam_y = interp_y - WINDOW_HEIGHT // 2

        # 2. OPTIMISATION : On calcule quelles tuiles sont visibles
        start_col = max(0, int(cam_x // TILE_SIZE))
        end_col = min(len(GAME_MAP[0]), int((cam_x + WINDOW_WIDTH) // TILE_SIZE) + 1)
        start_row = max(0, int(cam_y // TILE_SIZE))
        end_row = min(len(GAME_MAP), int((cam_y + WINDOW_HEIGHT) // TILE_SIZE) + 1)

        # 3. Rendu de la map visible UNIQUEMENT
        self.screen.fill(COLOR_BG)
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                tile = GAME_MAP[r][c]
                if tile > 0:
                    x = c * TILE_SIZE - cam_x
                    y = r * TILE_SIZE - cam_y
                    color = (60, 60, 70) if tile == 1 else COLOR_KILL
                    pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE-1, TILE_SIZE-1))

        # 4. Grappin et Joueur (Inchangé)
        if self.player.is_hooked:
            p_center = (interp_x + self.player.size/2 - cam_x, interp_y + self.player.size/2 - cam_y)
            h_pos = (self.player.hook_pos.x - cam_x, self.player.hook_pos.y - cam_y)
            pygame.draw.line(self.screen, HOOK_COLOR, p_center, h_pos, 2)

        pygame.draw.rect(self.screen, COLOR_PLAYER, (interp_x - cam_x, interp_y - cam_y, self.player.size, self.player.size))

    def draw_settings_menu(self):
        self.screen.fill(UI_DARK_BG)
        pygame.draw.rect(self.screen, UI_NAV_BAR, (0, 0, WINDOW_WIDTH, 40))
        right_w = 180
        pygame.draw.rect(self.screen, UI_NAV_BAR, (WINDOW_WIDTH - right_w, 40, right_w, WINDOW_HEIGHT - 40))
        
        if self.selected_tab == "Graphics":
            self.draw_card("Performance", 50, 70, 400, 300)
            fps_label = "Unlimited" if self.current_fps == 999 else str(self.current_fps)
            self.draw_setting_row("Max FPS", fps_label, 50, 130)
            self.draw_setting_row("Show FPS", "ON" if self.show_fps else "OFF", 50, 170)

    def draw_card(self, title, x, y, w, h):
        pygame.draw.rect(self.screen, UI_PANEL_BG, (x, y, w, h), border_radius=10)
        txt = pygame.font.SysFont("Arial", 20, bold=True).render(title, True, (255, 255, 255))
        self.screen.blit(txt, (x + 20, y + 15))

    def draw_setting_row(self, label, value, x, y):
        font = pygame.font.SysFont("Arial", 16)
        lbl = font.render(label, True, UI_TEXT)
        self.screen.blit(lbl, (x + 20, y))
        pygame.draw.rect(self.screen, UI_BUTTON_BG, (x + 160, y - 5, 180, 25), border_radius=5)
        v_txt = font.render(value, True, (255, 255, 255))
        self.screen.blit(v_txt, (x + 170, y - 2))

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
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "SETTINGS" if self.state == "GAME" else "GAME"
                    if self.state == "GAME" and event.key in [pygame.K_z, pygame.K_SPACE]:
                        jump_requested = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    m_pos = pygame.mouse.get_pos()
                    if self.state == "GAME":
                        # Pour le grappin, on doit ajouter l'offset caméra à la position souris
                        # sinon on tire au mauvais endroit sur la map
                        cam_x = self.player.pos.x - WINDOW_WIDTH // 2
                        cam_y = self.player.pos.y - WINDOW_HEIGHT // 2
                        real_target = pygame.math.Vector2(m_pos[0] + cam_x, m_pos[1] + cam_y)
                        self.player.fire_hook(real_target, self.world)
                    elif self.state == "SETTINGS":
                        if m_pos[0] > WINDOW_WIDTH - 180:
                            idx = (m_pos[1] - 80) // 40
                            tabs = ["General", "Player", "Appearance", "Controls", "Graphics", "Sound"]
                            if 0 <= idx < len(tabs): self.selected_tab = tabs[idx]
                        elif self.selected_tab == "Graphics":
                            if 125 < m_pos[1] < 155 and (50+160) < m_pos[0] < (50+160+180):
                                self.fps_idx = (self.fps_idx + 1) % len(self.fps_options)
                                self.current_fps = self.fps_options[self.fps_idx]
                            if 165 < m_pos[1] < 195 and (50+160) < m_pos[0] < (50+160+180):
                                self.show_fps = not self.show_fps
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state == "GAME": self.player.is_hooked = False

            if self.state == "GAME":
                while accumulator >= tick_rate:
                    keys = pygame.key.get_pressed()
                    self.player.update_physics(self.world, {'left': keys[pygame.K_q], 'right': keys[pygame.K_d], 'jump': jump_requested})
                    jump_requested = False
                    accumulator -= tick_rate
                alpha = accumulator / tick_rate
            else:
                accumulator = 0
                alpha = 0

            if self.state == "GAME":
                self.screen.fill(COLOR_BG)
                self.draw_game(alpha)
            else:
                self.draw_settings_menu()
            
            pygame.display.flip()
            self.clock.tick(self.current_fps)