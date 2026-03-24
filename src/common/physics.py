class Entity:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.size = 28 # Un peu plus petit que 32 pour glisser plus facilement

    def update_physics(self, world):
        # Gravité et Friction
        self.vel.y += GRAVITY
        self.vel.x *= FRICTION

        # Test collision Horizontale
        new_x = self.pos.x + self.vel.x
        if not world.check_collision(new_x, self.pos.y) and \
           not world.check_collision(new_x + self.size, self.pos.y):
            self.pos.x = new_x
        else:
            self.vel.x = 0

        # Test collision Verticale
        new_y = self.pos.y + self.vel.y
        if not world.check_collision(self.pos.x, new_y) and \
           not world.check_collision(self.pos.x + self.size, new_y):
            self.pos.y = new_y
        else:
            self.vel.y = 0