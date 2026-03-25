import time
from src.common.physics import Entity
from src.common.world import World
from src.common.settings import FPS

class GameServer:
    def __init__(self):
        self.world = World()
        self.player = Entity(100, 100)
        self.running = True

    def run(self):
        tick_rate = 1.0 / 60.0 # Toujours 60 Ticks
        while self.running:
            start_time = time.time()
            
            # Ici, plus tard, on récupérera les inputs du réseau
            # Pour le test local, on peut imaginer un dictionnaire vide
            fake_inputs = {'left': False, 'right': False, 'jump': False}
            
            self.player.update_physics(self.world, fake_inputs)
            
            # On dort pour maintenir les 60 Ticks
            sleep_time = tick_rate - (time.time() - start_time)
            if sleep_time > 0:
                time.sleep(sleep_time)