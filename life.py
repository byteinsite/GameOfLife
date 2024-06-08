import numpy as np
import time
import os
import platform

# Определяем размеры поля
width, height = 20, 20


# Инициализация случайного начального состояния
def initialize_grid(w, h):
    return np.random.choice([0, 1], size=(w, h))


# Функция для отображения состояния поля
def print_grid(grid):
    # Очистка консоли
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    for row in grid:
        print(' '.join(['█' if cell else ' ' for cell in row]))
    print("\n")


# Обновление состояния поля
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            live_neighbors = np.sum(grid[i - 1:i + 2, j - 1:j + 2]) - grid[i, j]
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
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(0.5)


# Запуск игры
if __name__ == "__main__":
    game_of_life(width, height, 100)
