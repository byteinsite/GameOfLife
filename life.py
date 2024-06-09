import numpy as np
import time
import os
import platform

# Определяем размеры поля
width, height = 20, 20
# Проверяем и записываем на какой ОС запущена программа
cmd_clear = 'cls' if platform.system() == 'Windows' else 'clear'


# Инициализация случайного начального состояния
def initialize_grid(w, h):
    return np.random.choice([0, 1], size=(w, h))


# Функция для отображения состояния поля
def print_grid(grid, intermediate_grid=None):
    for i in range(grid.shape[0]):
        row_str = ''
        for j in range(grid.shape[1]):
            if intermediate_grid is not None:
                if intermediate_grid[i, j] == 1:
                    row_str += '□ '
                elif intermediate_grid[i, j] == 2:
                    row_str += '░ '
                else:
                    row_str += '█ ' if grid[i, j] else '  '
            else:
                row_str += '█ ' if grid[i, j] else '  '
        print(row_str)
    print("\n")

# Функция для создания промежуточного кадра
def create_intermediate_grid(grid):
    intermediate_grid = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            live_neighbors = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    intermediate_grid[i, j] = 1  # Умрет
            else:
                if live_neighbors == 3:
                    intermediate_grid[i, j] = 2  # Оживёт
    return intermediate_grid

# Обновление состояния поля
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            live_neighbors = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1
    return new_grid

# Основной цикл игры
def game_of_life(width, height, iterations):
    grid = initialize_grid(width, height)
    for _ in range(iterations):
        os.system(cmd_clear)
        print_grid(grid)
        intermediate_grid = create_intermediate_grid(grid)
        time.sleep(1)
        os.system(cmd_clear)
        print_grid(grid, intermediate_grid)
        time.sleep(1)
        grid = update_grid(grid)

# Запуск игры
if __name__ == "__main__":
    game_of_life(width, height, 3)
