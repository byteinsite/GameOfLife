import numpy as np
import time
import os
import platform

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.initialize_grid()
        self.clear_command = 'cls' if platform.system() == "Windows" else 'clear'

    def initialize_grid(self):
        return np.random.choice([0, 1], size=(self.width, self.height))

    def print_grid(self, intermediate_grid=None):
        # Очистка консоли
        os.system(self.clear_command)

        for i in range(self.grid.shape[0]):
            row_str = ''
            for j in range(self.grid.shape[1]):
                if intermediate_grid is not None:
                    if intermediate_grid[i, j] == 1:
                        row_str += '□ '
                    elif intermediate_grid[i, j] == 2:
                        row_str += '░ '
                    else:
                        row_str += '█ ' if self.grid[i, j] else '  '
                else:
                    row_str += '█ ' if self.grid[i, j] else '  '
            print(row_str)
        print("\n")

    def create_intermediate_grid(self):
        intermediate_grid = np.zeros(self.grid.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                live_neighbors = np.sum(self.grid[i-1:i+2, j-1:j+2]) - self.grid[i, j]
                if self.grid[i, j] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        intermediate_grid[i, j] = 1  # Умрет
                else:
                    if live_neighbors == 3:
                        intermediate_grid[i, j] = 2  # Оживёт
        return intermediate_grid

    def update_grid(self):
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                live_neighbors = np.sum(self.grid[i-1:i+2, j-1:j+2]) - self.grid[i, j]
                if self.grid[i, j] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[i, j] = 0
                else:
                    if live_neighbors == 3:
                        new_grid[i, j] = 1
        self.grid = new_grid

    def run(self, iterations):
        for _ in range(iterations):
            self.print_grid()
            intermediate_grid = self.create_intermediate_grid()
            time.sleep(0.5)
            self.print_grid(intermediate_grid)
            time.sleep(0.5)
            self.update_grid()

# Запуск игры
if __name__ == "__main__":
    game = GameOfLife(width=20, height=20)
    game.run(iterations=2)
