import time
from os import system, name

class Grid():
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.zeros = []
        self.skippable_numbers = {}
        self.index = 0
        self.count = 0
        
    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.zeros and self.grid[i][j] == 0:
                    s += '\33[31m0\33[0m '
                elif (i, j) in self.zeros and self.grid[i][j] != 0:
                    s += '\33[32m' + str(self.grid[i][j]) + '\33[0m '
                else:
                    s += str(self.grid[i][j]) + ' '
            s += '\n'
        return s

    def clear_screen(self):
        if name == 'nt':  # Windows
            system('cls')
        else:  # Unix-like (Linux, macOS)
            system('clear')
    
    def check_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] not in range(0, 10):
                    print(f'Invalid number at position ({i}, {j})')
                    print(f'Number: {self.grid[i][j]}')
                    return False
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] != 0 and not self.is_valid(i, j, self.grid[i][j]):
                    print(f'Invalid number at position ({i}, {j})')
                    print(f'Number: {self.grid[i][j]}')
                    return False
        return True
    
    def find_all_zeros(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    self.zeros.append((i, j))
    
    def calculate_skippable_numbers(self):
        for pos in self.zeros:
            row, col = pos
            self.skippable_numbers[pos] = []
            for i in range(self.size):
                if self.grid[row][i] != 0:
                    self.skippable_numbers[pos].append(self.grid[row][i])
                if self.grid[i][col] != 0:
                    self.skippable_numbers[pos].append(self.grid[i][col])
            start_row = row - row % 3
            start_col = col - col % 3
            for i in range(3):
                for j in range(3):
                    if self.grid[i + start_row][j + start_col] != 0:
                        self.skippable_numbers[pos].append(self.grid[i + start_row][j + start_col])
            self.skippable_numbers[pos] = list(set(self.skippable_numbers[pos]))

    def is_valid(self, row, col, num):
        # Controllo riga
        for i in range(self.size):
            if self.grid[row][i] == num and i != col:
                return False

        # Controllo colonna
        for i in range(self.size):
            if self.grid[i][col] == num and i != row:
                return False

        # Controllo quadrato
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num and (i + start_row, j + start_col) != (row, col):
                    return False

        return True

    def init_solve(self):
        if self.check_grid():
            self.find_all_zeros()
            self.calculate_skippable_numbers()
            return True
        return False
    
    def show_runtime(self, count, steps, sleep):
        if count % steps == 0:
            self.clear_screen()
            print(self)
            print(f'Step: {self.count}')
            time.sleep(sleep)
    
    def solve(self, **kwargs):
        """
        kwargs:
            - show_kwargs: (steps, sleep) -> steps: numero di passi per visualizzare la griglia, sleep: tempo di attesa tra un passo e l'altro
        """
        if self.index == 0:
            if not self.init_solve():
                return False
        if self.index == len(self.zeros):
            self.show_runtime(1, 1, 0)
            return True
        row, col = self.zeros[self.index]
        for num in range(1, 10):
            if num not in self.skippable_numbers[(row, col)]:
                if self.is_valid(row, col, num):
                    self.grid[row][col] = num
                    self.count += 1
                    self.index += 1
                    if 'show_kwargs' in kwargs:
                        self.show_runtime(self.count,
                                          kwargs['show_kwargs']['steps'],
                                          kwargs['show_kwargs']['sleep'])
                    if self.solve(**kwargs):
                        return True
                    self.grid[row][col] = 0
                    self.count += 1
                    self.index -= 1
                    if 'steps' in kwargs:
                        self.show_runtime(self.count,
                                          kwargs['steps'],
                                          kwargs['sleep'])
        return False
    
def main():
    grid_data = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    grid = Grid(grid_data)
    grid.solve(show_kwargs={'steps': 100, 'sleep': 0.1})

if __name__ == '__main__':
    main()