import pygame
from game import Game
from screen import Screen
from player import Player, Human

# Colores
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'bg': (187, 173, 160),
    'text': (119, 110, 101),
    'score': (255, 255, 255)
}

# path=f"{self.name}_movement_data.csv"
def main():
    Alejandro = Human("Alejandro", Screen, COLORS=COLORS)
    game = Game()
    Alejandro.save_movement_data(
        state=game.get_flattened_grid(), 
        score=game.score, 
        action="X", 
        path=f"{Alejandro.name}_movement_data.csv"
    )
    
    while True:
        Alejandro.handle_input(game)
        Alejandro.view_screen(game)
        pygame.display.update()
        Alejandro.screen.clock.tick(Alejandro.screen.FPS)
        

if __name__== "__main__":
    main()