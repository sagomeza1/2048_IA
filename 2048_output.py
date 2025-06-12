import pygame
import random
import sys
import csv

# Constantes
WIDTH = 400
HEIGHT = 500
GRID_SIZE = 4
CELL_SIZE = 90
GRID_PADDING = 10
FPS = 60

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

# Inicializar Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

# Función para guardar el estado y acción
def save_training_data(state, action, path="training_data.csv"):
    with open(path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(state + [action])

class Game:
    def __init__(self):
        self.grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE)
                       for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        old_grid = [row[:] for row in self.grid]
        moved = False

        if direction in ('left', 'right'):
            for row in self.grid:
                if direction == 'left':
                    merged = self.merge_row(row)
                else:
                    merged = self.merge_row(row[::-1])[::-1]
                if row != merged:
                    moved = True
                    row[:] = merged

        elif direction in ('up', 'down'):
            for col in range(GRID_SIZE):
                column = [self.grid[row][col] for row in range(GRID_SIZE)]
                if direction == 'up':
                    merged = self.merge_row(column)
                else:
                    merged = self.merge_row(column[::-1])[::-1]
                if column != merged:
                    moved = True
                    for row in range(GRID_SIZE):
                        self.grid[row][col] = merged[row]

        if moved:
            self.add_new_tile()
            return True
        return False

    def merge_row(self, row):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row)-1):
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row.pop(i+1)
                new_row.append(0)
        new_row += [0]*(len(row)-len(new_row))
        return new_row

    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE-1):
                if self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if self.grid[j][i] == self.grid[j+1][i]:
                    return False
        return True

    def get_flattened_grid(self):
        return [cell for row in self.grid for cell in row]

def draw_grid(game):
    screen.fill(COLORS['bg'])

    score_text = font.render(f"Score: {game.score}", True, COLORS['score'])
    screen.blit(score_text, (20, 20))

    grid_x = (WIDTH - (CELL_SIZE*GRID_SIZE + GRID_PADDING*(GRID_SIZE-1))) // 2
    grid_y = 100

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = game.grid[i][j]
            color = COLORS[value] if value in COLORS else COLORS[0]
            x = grid_x + j*(CELL_SIZE + GRID_PADDING)
            y = grid_y + i*(CELL_SIZE + GRID_PADDING)
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=5)

            if value != 0:
                text = font.render(str(value), True, COLORS['text'])
                text_rect = text.get_rect(center=(x+CELL_SIZE//2, y+CELL_SIZE//2))
                screen.blit(text, text_rect)

    if game.is_game_over():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))
        screen.blit(overlay, (0, 0))
        text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

def handle_input(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
                pygame.K_s: ('down', 3)
            }

            if event.key in directions:
                dir_str, action_code = directions[event.key]
                state = game.get_flattened_grid()
                moved = game.move(dir_str)
                if moved:
                    save_training_data(state, action_code)

def main():
    game = Game()
    while True:
        handle_input(game)
        draw_grid(game)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
