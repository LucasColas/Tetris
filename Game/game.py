import pygame
from Game.piece import Piece
import random


import pygame
from Game.piece import Piece
import random

class Game:
    def __init__(self, cell_size=25, fps=60):
        self.screen = pygame.display.get_surface()
        self.cell_size = cell_size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.pieces = []
        self.score = 0
        self.line_score = 300
        self.is_game_over = False

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

        self.current_piece = Piece(
            shape=self.shapes["I"],
            color=self.colors[random.choice(list(self.colors.keys()))],
            bg_color=(0, 0, 0),
            cell_size=self.cell_size,
        )
        self.piece_position = (self.screen.get_width() // 2 - self.cell_size, -self.current_piece.get_height())
        self.counter = 0

        # Grid representation for the board
        self.grid_width = self.screen.get_width() // self.cell_size
        self.grid_height = self.screen.get_height() // self.cell_size
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def update(self):
        self.counter += 1
        self.draw_pieces()

        if self.counter >= 0.8 * self.fps and not self.is_game_over:
            self.counter = 0
            self.piece_position = (self.piece_position[0], self.piece_position[1] + self.cell_size)

        self.check_collision()

        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    global_x = self.piece_position[0] + x * self.cell_size
                    global_y = self.piece_position[1] + y * self.cell_size
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece.color,
                        pygame.Rect(global_x, global_y, self.cell_size, self.cell_size),
                    )

        self.check_piece_position()
        self.draw_score()
        self.game_over()
        
        if self.is_game_over:
            self.draw_game_over()
            
        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)

    def draw_pieces(self):
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        pygame.Rect(
                            x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                        ),
                    )

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text, text_rect)

    def check_piece_position(self):
        if self.piece_position[0] < 0:
            self.piece_position = (0, self.piece_position[1])

        if self.piece_position[0] > self.screen.get_width() - self.current_piece.get_width():
            self.piece_position = (
                self.screen.get_width() - self.current_piece.get_width(),
                self.piece_position[1],
            )

    def clear_complete_lines(self):
        rows_to_clear = []
        for y in range(self.grid_height):
            if all(self.grid[y]):
                rows_to_clear.append(y)

        if rows_to_clear:
            self.score += self.line_score * len(rows_to_clear)

            # Clear rows and shift the grid down
            for row in rows_to_clear:
                del self.grid[row]
                self.grid.insert(0, [None for _ in range(self.grid_width)])
            
            # Update pieces' positions according to the new grid
            new_pieces = []
            for piece, position in self.pieces:
                new_position = position
                new_shape = piece.shape

                # Adjust position based on cleared rows
                for clear_y in rows_to_clear:
                    if position[1] // self.cell_size < clear_y:
                        new_position = (position[0], position[1] + self.cell_size)
                
                new_pieces.append((piece, new_position))
            self.pieces = new_pieces

    def check_collision(self):
        collision = False
        if self.piece_position[1] + self.current_piece.get_height() >= self.screen.get_height():
            collision = True

        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    global_x = self.piece_position[0] + x * self.cell_size
                    global_y = self.piece_position[1] + y * self.cell_size

                    for other_piece, other_position in self.pieces:
                        for oy, o_row in enumerate(other_piece.shape):
                            for ox, o_cell in enumerate(o_row):
                                if o_cell:
                                    other_x = other_position[0] + ox * self.cell_size
                                    other_y = other_position[1] + oy * self.cell_size

                                    if (global_x == other_x) and (global_y + self.cell_size == other_y):
                                        collision = True
                                        break
                            if collision:
                                break
                    if collision:
                        break
            if collision:
                break

        if collision:
            self.pieces.append((self.current_piece, self.piece_position))
            
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid_x = (self.piece_position[0] // self.cell_size) + x
                        grid_y = (self.piece_position[1] // self.cell_size) + y
                        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
                            self.grid[grid_y][grid_x] = self.current_piece.color

            self.clear_complete_lines()

            self.score += len(self.current_piece.shape) * 10
            self.current_piece = Piece(
                shape=self.shapes[random.choice(list(self.shapes.keys()))],
                color=self.colors[random.choice(list(self.colors.keys()))],
                bg_color=(0, 0, 0),
                cell_size=self.cell_size,
            )
            self.piece_position = (self.screen.get_width() // 2 - self.cell_size, -self.current_piece.get_height())

    def game_over(self):
        for _, position in self.pieces:
            if position[1] <= 0:
                self.is_game_over = True

    def restart_game(self):
        self.pieces = []
        self.score = 0
        self.is_game_over = False
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = Piece(
            shape=self.shapes[random.choice(list(self.shapes.keys()))],
            color=self.colors[random.choice(list(self.colors.keys()))],
            bg_color=(0, 0, 0),
            cell_size=self.cell_size,
        )
        self.piece_position = (self.screen.get_width() // 2 - self.cell_size, -self.current_piece.get_height())
        self.counter = 0


    def run(self):
        # Game loop
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and not self.is_game_over:
                self.piece_position = (
                    self.piece_position[0],
                    self.piece_position[1] + self.cell_size,
                )
                self.score += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.is_game_over:
                        self.restart_game()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()

                    if event.key == pygame.K_LEFT:
                        if self.piece_position[0] > 0:
                            self.piece_position = (
                                self.piece_position[0] - self.cell_size,
                                self.piece_position[1],
                            )

                    if event.key == pygame.K_RIGHT:

                        if (
                            self.piece_position[0]
                            < self.screen.get_width() - self.current_piece.get_width()
                        ):
                            self.piece_position = (
                                self.piece_position[0] + self.cell_size,
                                self.piece_position[1],
                            )

            self.screen.fill((0, 0, 0))

            # Draw / render
            self.update()

            # Cap the frame rate
            self.clock.tick(self.fps)

        pygame.quit()
