import random

class Game:
    def __init__(self, GRID_SIZE:int=4):
        self.GRID_SIZE = GRID_SIZE
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.GRID_SIZE) 
                       for j in range(self.GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            
    def move(self, direction):
        old_grid = [row[:] for row in self.grid]
        moved = False
        
        if direction in ('left', 'right'):
            for row in self.grid:
                if direction == "left":
                    merged = self.merge_row(row)
                else:
                    merged = self.merge_row(row[::-1])[::-1]
                if row != merged:
                    moved = True
                    row[:] = merged
                    
        elif direction in ('up', 'down'):
            for col in range(self.GRID_SIZE):
                column = [self.grid[row][col] for row in range(self.GRID_SIZE)]
                if direction == "up":
                    merged = self.merge_row(column)
                else:
                    merged = self.merge_row(column[::-1])[::-1]
                if column != merged:
                    moved = True
                    for row in range(self.GRID_SIZE):
                        self.grid[row][col] = merged[row]
                        
        if moved:
            self.add_new_tile()
            return True
        return False
    
    def merge_row(self, row:list):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row.pop(i + 1)
                new_row.append(0)
                
        new_row += [0] * (len(row) - len(new_row))
        return new_row
    
    def is_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True
    
    def get_flattened_grid(self):
        return [cell for row in self.grid for cell in row]
            

def main():
    pass

if __name__ == "__main__":
    main()