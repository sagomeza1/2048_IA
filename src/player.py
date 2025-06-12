import pygame
from typing import List, Tuple
from game import Game
from screen import Screen

class Player:
    def __init__(self, name:str):
        self.name = name
        ...

    def handle_input(self, game: Game):
        pass
    
    def view_screem(self):
        pass

class Human(Player):
    def __init__(self, name:str, screen: Screen, *args, **kwargs):
        super().__init__(name)
        self.type = "Human"
        self.screen = screen(*args, **kwargs)
        self.screen.init_pygame()

    def handle_input(self, game: Game):
        # Handle human input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ...
                
        pass

    def view_screen(self):
        pass
    
def main():
    pass

if __name__=='__main__':
    main()