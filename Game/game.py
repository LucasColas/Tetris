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
        self.piece_position = (0, 0)
        self.counter = 0

    def update(self):
        # self.input()

        self.counter += 1
        self.draw_pieces()

        if self.counter >= 0.8 * self.fps:
            self.counter = 0
            self.piece_position = (
                self.piece_position[0],
                self.piece_position[1] + self.cell_size,
            )

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
        pygame.display.flip()

    def draw_pieces(self):
        for piece, position in self.pieces:
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        global_x = position[0] + x * self.cell_size
                        global_y = position[1] + y * self.cell_size
                        pygame.draw.rect(
                            self.screen,
                            piece.color,
                            pygame.Rect(
                                global_x, global_y, self.cell_size, self.cell_size
                            ),
                        )

    def check_piece_position(self):
        if self.piece_position[0] < 0:
            self.piece_position = (0, self.piece_position[1])

        if (
            self.piece_position[0]
            > self.screen.get_width() - self.current_piece.get_width()
        ):
            self.piece_position = (
                self.screen.get_width() - self.current_piece.get_width(),
                self.piece_position[1],
            )

    def clear_complete_lines(self):
        # Check for complete lines and clear them
        rows_to_clear = set()

        # Identify complete lines
        for y in range(self.screen.get_height() // self.cell_size):
            row_filled = True
            for x in range(self.screen.get_width() // self.cell_size):
                cell_filled = any(
                    global_y == y * self.cell_size and global_x == x * self.cell_size
                    for piece, position in self.pieces
                    for py, row in enumerate(piece.shape)
                    for px, cell in enumerate(row)
                    if cell
                    for global_x in [position[0] + px * self.cell_size]
                    for global_y in [position[1] + py * self.cell_size]
                )
                if not cell_filled:
                    row_filled = False
                    break
            if row_filled:
                rows_to_clear.add(y)

        if rows_to_clear:
            self.score += len(rows_to_clear) * 300
            new_pieces = []

            for piece, position in self.pieces:
                new_shape = []
                for py, row in enumerate(piece.shape):
                    new_row = []
                    for px, cell in enumerate(row):
                        if cell:
                            global_y = position[1] + py * self.cell_size
                            if global_y // self.cell_size not in rows_to_clear:
                                new_row.append(cell)
                            else:
                                new_row.append(0)
                        else:
                            new_row.append(0)
                    new_shape.append(new_row)
                new_piece = Piece(
                    new_shape, piece.color, piece.bg_color, piece.cell_size
                )
                new_pieces.append((new_piece, position))

            self.pieces = [
                (piece, (x, y + self.cell_size * len(rows_to_clear)))
                for piece, (x, y) in new_pieces
            ]

    def check_collision(self):
        # Check if the piece is colliding with the board or another piece
        collision = False
        if (
            self.piece_position[1] + self.current_piece.get_height()
            >= self.screen.get_height()
        ):
            collision = True

        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    global_x = self.piece_position[0] + x * self.cell_size
                    global_y = self.piece_position[1] + y * self.cell_size

                    # Check collision with other pieces
                    for other_piece, other_position in self.pieces:
                        for oy, o_row in enumerate(other_piece.shape):
                            for ox, o_cell in enumerate(o_row):
                                if o_cell:
                                    other_x = other_position[0] + ox * self.cell_size
                                    other_y = other_position[1] + oy * self.cell_size

                                    if (global_x == other_x) and (
                                        global_y + self.cell_size == other_y
                                    ):
                                        collision = True
                                        break
                            if collision:
                                break
                    if collision:
                        break
            if collision:
                break

        if collision:
            # Store the current piece on the board
            self.pieces.append((self.current_piece, self.piece_position))

            self.clear_complete_lines()

            # Spawn a new piece
            self.current_piece = Piece(
                shape=self.shapes["I"],
                color=self.colors[random.choice(list(self.colors.keys()))],
                bg_color=(0, 0, 0),
                cell_size=self.cell_size,
            )
            self.piece_position = (self.screen.get_width() // 2 - self.cell_size, 0)

    def run(self):
        # Game loop
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.piece_position = (
                    self.piece_position[0],
                    self.piece_position[1] + self.cell_size,
                )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

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
