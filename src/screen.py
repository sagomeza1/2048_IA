
import pygame

from game import Game

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

class Screen:
    def __init__(self, 
                 WIDTH: int = 400, 
                 HEIGHT: int = 500,
                 GRID_SIZE: int = 4,
                 CELL_SIZE: int = 90,
                 GRID_PADDING: int = 10,
                 FPS: int = 60,
                 COLORS: dict = None):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_SIZE = GRID_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.GRID_PADDING = GRID_PADDING
        self.FPS = FPS
        self.COLORS = COLORS if COLORS else COLORS
        self.screen, self.clock, self.font, self.small_font = self.init_pygame()
        
    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("2048")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 24)
        return screen, clock, font, small_font
    
    def draw_grid(self, game: Game):
        if self.COLORS:
            self.screen.fill(self.COLORS['bg'])
            score_text = self.font.render(f"Score: {game.score}", True, self.COLORS['score'])
        else:
            self.screen.fill((187, 173, 160))
            score_text = self.font.render(f"Score: {game.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        grid_x = (self.WIDTH - (self.CELL_SIZE*self.GRID_SIZE + self.GRID_PADDING*(self.GRID_SIZE - 1))) // 2
        grid_y = 100
        
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                value = game.grid[i][j]
                if self.COLORS:
                    color = self.COLORS[value] if value in self.COLORS else self.COLORS[0]
                else:
                    color = (238, 228, 218)
                x = grid_x + j*(self.CELL_SIZE + self.GRID_PADDING)
                y = grid_y + i*(self.CELL_SIZE + self.GRID_PADDING)
                pygame.draw.rect(self.screen, color, (x, y, self.CELL_SIZE, self.CELL_SIZE), border_radius=5)
                
                if value != 0:
                    if self.COLORS:
                        text = self.font.render(str(value), True, self.COLORS["text"])
                    else:
                        text = self.font.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=(x+self.CELL_SIZE//2, y+self.CELL_SIZE//2))
                    self.screen.blit(text, text_rect)
                    
        if game.is_game_over():
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))
            self.screen.blit(overlay, (0, 0))
            text = self.font.render("Game Over!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
            self.screen.blit(text, text_rect)
                
                
                
        

def main():
    pass


if __name__ == "__main__":
    main()