import pygame
from Game.piece import Piece
import random


class Game:
    def __init__(self, cell_size=25, fps=60, bg_color=(0, 0, 0)):
        self.screen = pygame.display.get_surface()
        self.cell_size = cell_size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.line_score = 300
        self.is_game_over = False
        self.counter = 0
        self.bg_color = bg_color

        self.shapes = {
            "I": [[1, 1, 1, 1]],
            "J": [[1, 0, 0], [1, 1, 1]],
            "L": [[0, 0, 1], [1, 1, 1]],
            "O": [[1, 1], [1, 1]],
            "S": [[0, 1, 1], [1, 1, 0]],
            "T": [[0, 1, 0], [1, 1, 1]],
            "Z": [[1, 1, 0], [0, 1, 1]],
        }

        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (255, 0, 255),
        }

        self.grid_width = self.screen.get_width() // self.cell_size
        self.grid_height = self.screen.get_height() // self.cell_size
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        self.spawn_piece()

    def spawn_piece(self):
        self.current_piece = Piece(
            shape=self.shapes[random.choice(list(self.shapes.keys()))],
            color=self.colors[random.choice(list(self.colors.keys()))],
            bg_color=self.bg_color,
            cell_size=self.cell_size,
        )
        self.piece_position = (self.grid_width // 2 - len(self.current_piece.shape[0]) // 2, 0)

    def update(self):
        self.screen.fill(self.bg_color)
        self.counter += 1

        if self.counter >= 0.8 * self.fps and not self.is_game_over:
            self.move_piece(0, 1)
            self.counter = 0

        self.draw_grid()
        self.draw_piece()
        self.draw_score()

        if self.is_game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_grid(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        pygame.Rect(
                            x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    global_x = self.piece_position[0] + x
                    global_y = self.piece_position[1] + y
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece.color,
                        pygame.Rect(
                            global_x * self.cell_size,
                            global_y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def move_piece(self, dx, dy):
        new_x = self.piece_position[0] + dx
        new_y = self.piece_position[1] + dy

        if self.valid_move(new_x, new_y):
            self.piece_position = (new_x, new_y)
        else:
            # the piece has landed on the bottom of the grid or on another block. In this case, it should be locked in place.
            if dy > 0:
                self.lock_piece()

    def valid_move(self, new_x, new_y):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = new_x + x
                    grid_y = new_y + y
                    if (
                        grid_x < 0
                        or grid_x >= self.grid_width
                        or grid_y >= self.grid_height
                        or (grid_y >= 0 and self.grid[grid_y][grid_x])
                    ):
                        #print("Invalid move")
                        return False
        return True

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_position[0] + x
                    grid_y = self.piece_position[1] + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_piece.color

        self.clear_complete_lines()
        self.spawn_piece()
        if not self.valid_move(self.piece_position[0], self.piece_position[1]):
            self.is_game_over = True

    def clear_complete_lines(self):
        new_grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        new_row_index = self.grid_height - 1
        lines_cleared = 0

        for row_index in range(self.grid_height - 1, -1, -1):
            if None in self.grid[row_index]:
                new_grid[new_row_index] = self.grid[row_index]
                new_row_index -= 1
            else:
                lines_cleared += 1

        self.grid = new_grid
        self.score += self.line_score * lines_cleared

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text, text_rect)

    def draw_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

    def restart_game(self):
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.score = 0
        self.is_game_over = False
        self.spawn_piece()

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and not self.is_game_over:
                print("down")
                self.move_piece(0, 1)
                self.score += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if not self.valid_move(self.piece_position[0], self.piece_position[1]):
                            # Undo rotation if it's not a valid move
                            for _ in range(3):  # Rotate three more times to revert
                                self.current_piece.rotate()
                    elif event.key == pygame.K_SPACE and self.is_game_over:
                        self.restart_game()

            self.screen.fill((0, 0, 0))
            self.update()
            self.clock.tick(self.fps)

        pygame.quit()
