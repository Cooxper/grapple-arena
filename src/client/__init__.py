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