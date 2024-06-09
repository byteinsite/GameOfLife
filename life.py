import numpy as np
import pygame
import time


class GameOfLife:
    def __init__(self, width, height, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = self.initialize_grid()
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + 50  # Добавили место для кнопок
        self.running = True
        self.paused = False

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game of Life")
        self.font = pygame.font.SysFont(None, 36)  # Увеличили размер шрифта

    def initialize_grid(self):
        return np.random.choice([0, 1], size=(self.width, self.height))

    def draw_grid(self, intermediate_grid=None):
        self.screen.fill((0, 0, 0))
        for i in range(self.width):
            for j in range(self.height):
                color = (0, 0, 0)
                if intermediate_grid is not None:
                    if intermediate_grid[i, j] == 1:
                        color = (255, 0, 0)  # Red for dying cells
                    elif intermediate_grid[i, j] == 2:
                        color = (0, 255, 0)  # Green for new cells
                    elif self.grid[i, j] == 1:
                        color = (255, 255, 255)  # White for living cells
                else:
                    if self.grid[i, j] == 1:
                        color = (255, 255, 255)  # White for living cells

                pygame.draw.rect(
                    self.screen, color,
                    (i * self.cell_size, j * self.cell_size, self.cell_size - 1, self.cell_size - 1))

        pygame.display.flip()

    def create_intermediate_grid(self):
        intermediate_grid = np.zeros(self.grid.shape)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                live_neighbors = np.sum(self.grid[i - 1:i + 2, j - 1:j + 2]) - self.grid[i, j]
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
                live_neighbors = np.sum(self.grid[i - 1:i + 2, j - 1:j + 2]) - self.grid[i, j]
                if self.grid[i, j] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[i, j] = 0
                else:
                    if live_neighbors == 3:
                        new_grid[i, j] = 1
        self.grid = new_grid

    def draw_buttons(self):
        pause_play_text = 'Pause' if not self.paused else 'Play'
        pause_play_button = self.font.render(pause_play_text, True, (0, 0, 0))
        button_width = self.screen_width - 20
        button_height = 40
        button_rect = pygame.Rect(10, self.screen_height - button_height - 10, button_width, button_height)

        pygame.draw.rect(self.screen, (255, 255, 255), button_rect)
        text_rect = pause_play_button.get_rect(center=button_rect.center)
        self.screen.blit(pause_play_button, text_rect)
        pygame.display.flip()
        return button_rect

    def handle_button_click(self, pos, button_rect):
        if button_rect.collidepoint(pos):
            self.paused = not self.paused

    def run(self, iterations):
        clock = pygame.time.Clock()
        button_rect = None
        for _ in range(iterations):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect:
                        self.handle_button_click(event.pos, button_rect)

            if not self.running:
                break

            self.draw_grid()
            button_rect = self.draw_buttons()
            if not self.paused:
                intermediate_grid = self.create_intermediate_grid()
                time.sleep(0.5)
                self.draw_grid(intermediate_grid)
                self.draw_buttons()
                time.sleep(0.5)
                self.update_grid()
            clock.tick(10)

        pygame.quit()


# Запуск игры
if __name__ == "__main__":
    game = GameOfLife(width=50, height=50, cell_size=10)
    game.run(iterations=100)
