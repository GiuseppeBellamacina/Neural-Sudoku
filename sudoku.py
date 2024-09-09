import time
import random
from os import system, name

class Grid():
    def __init__(self, grid, square_root_dim):
        self.grid = grid
        self.square_root_dim = square_root_dim
        self.size = square_root_dim**2
        self.zeros = []
        self.skippable_numbers = {}
        self.index = 0
        self.count = 0
    
    @classmethod
    def from_grid(cls, grid):
        square_root_dim = int(len(grid)**0.5)
        return cls(grid, square_root_dim)
    
    @classmethod
    def from_dim(cls, square_root_dim):
        if square_root_dim < 1:
            raise ValueError('The dimension must be greater than 0')
        tmp = cls([], square_root_dim)
        tmp.generate_grid()
        return tmp
        
    def __str__(self):
        space = lambda x: ' ' * (len(str(self.size)) - len(str(x)))
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.zeros and self.grid[i][j] == 0:
                    s += space(0) +'\33[31m0\33[0m '
                elif (i, j) in self.zeros and self.grid[i][j] != 0:
                    s += space(self.grid[i][j]) +'\33[32m' + str(self.grid[i][j]) + '\33[0m '
                else:
                    s += space(self.grid[i][j]) + str(self.grid[i][j]) + ' '
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
                if self.grid[i][j] not in range(0, self.size + 1):
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
            start_row = row - row % self.square_root_dim
            start_col = col - col % self.square_root_dim
            for i in range(self.square_root_dim):
                for j in range(self.square_root_dim):
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
        start_row = row - row % self.square_root_dim
        start_col = col - col % self.square_root_dim
        for i in range(self.square_root_dim):
            for j in range(self.square_root_dim):
                if self.grid[i + start_row][j + start_col] == num and (i + start_row, j + start_col) != (row, col):
                    return False

        return True
    
    def fill_grid(self, row=0, col=0):
        if row == self.size - 1 and col == self.size:
            return True
        
        if col == self.size:
            row += 1
            col = 0
        
        if self.grid[row][col] != 0:
            return self.fill_grid(row, col + 1)
        
        nums = list(range(1, self.size + 1))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.fill_grid(row, col + 1):
                    return True
                self.grid[row][col] = 0
        return False
    
    def generate_grid(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.fill_grid()
    
    def remove_numbers(self, n):
        if n > self.size**2:
            n = self.size**2
        for _ in range(n):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            while self.grid[row][col] == 0:
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
            self.grid[row][col] = 0

    def init_solve(self):
        if self.check_grid():
            self.index = 0
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
        if self.count == 0:
            if not self.init_solve():
                return False
        if self.index == len(self.zeros):
            self.show_runtime(1, 1, 0)
            return True
        row, col = self.zeros[self.index]
        for num in range(1, self.size + 1):
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
    
    grid = Grid.from_grid(grid_data)
    #grid.remove_numbers(20)
    grid.solve(show_kwargs={'steps': 10000, 'sleep': 0.1})
    print(grid.check_grid())

if __name__ == '__main__':
    main()