import sys
import os

# On force Python à regarder dans le dossier courant pour trouver 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.client.game import main

if __name__ == "__main__":
    main()