import sys
# On importe le GameClient que nous avons écrit dans src/client/game.py
from src.client.game import GameClient

def main():
    print("Démarrage du prototype Greybox...")
    
    # On crée une instance de ton jeu
    app = GameClient()
    
    # On lance la boucle infinie
    app.run()

if __name__ == "__main__":
    # Ce bloc permet de s'assurer que le jeu ne se lance 
    # que si on exécute ce fichier précisément.
    main()