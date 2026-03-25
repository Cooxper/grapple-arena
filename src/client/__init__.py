def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.world = World()
        self.player = Entity(100, 100)
        
        # --- ÉTATS DU MENU ---
        self.state = "GAME"
        self.selected_tab = "Graphics" # Onglet par défaut
        self.show_fps = True           # L'option que tu voulais
        self.current_fps = FPS

# Dans le __init__ de GameClient
        self.fps_options = [60, 120, 180, 240, 999] # 999 pour "Unlimited"
        self.fps_idx = 0 # Par défaut 60 FPS
        self.current_fps = self.fps_options[self.fps_idx]