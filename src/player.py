import pygame
from typing import List, Tuple
import csv
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
    
    def save_movement_data(
        self, 
        state:list, 
        score:str, 
        action:str, 
        path="movement_data.csv"
    ):
        with open(path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(state + [score, action])
        
        ...
        
    

class Human(Player):
    def __init__(self, name:str, screen: Screen, *args, **kwargs):
        super().__init__(name)
        self.type = "Human"
        self.screen = screen(*args, **kwargs)

    def handle_input(self, game: Game, *args, **kwargs):
        # Handle human input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.__init__()
                    
                directions = {
                    pygame.K_LEFT: ('left', 0),
                    pygame.K_RIGHT: ('right', 1),
                    pygame.K_UP: ('up', 2),
                    pygame.K_DOWN: ('down', 3),
                    pygame.K_a: ('left', 0),
                    pygame.K_d: ('right', 1),
                    pygame.K_w: ('up', 2),
                    pygame.K_s: ('down', 3),                    
                }
                
                if event.key in directions:
                    dir_str, action_code = directions[event.key]
                    state = game.get_flattened_grid()
                    moved = game.move(dir_str)
                    score = game.score
                    if moved:
                        self.save_movement_data(state, score, action_code, path=f"{self.name}_movement_data.csv", *args, **kwargs)
                        ...
                ...
    
    
                    
        pass

    def view_screen(self, game: Game):
        self.screen.draw_grid(game)
        
    
def main():
    pass

if __name__=='__main__':
    main()