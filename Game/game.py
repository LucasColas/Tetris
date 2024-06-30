import pygame
from Game.piece import Piece
import random

class Game():
    def __init__(self, cell_size=25, fps=60):
        self.screen = pygame.display.get_surface()
        self.cell_size = cell_size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.pieces = []
        
        self.shapes = {
            'I': [[1, 1, 1, 1]],
            'J': [[1, 0, 0],
                [1, 1, 1]],
            'L': [[0, 0, 1],
                [1, 1, 1]],
            'O': [[1, 1],
                [1, 1]],
            'S': [[0, 1, 1],
                [1, 1, 0]],
            'T': [[0, 1, 0],
                [1, 1, 1]],
            'Z': [[1, 1, 0],
                [0, 1, 1]],
        }

        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (255, 0, 255),
        }

        self.current_piece = Piece(shape=self.shapes['Z'], color=self.colors[random.choice(list(self.colors.keys()))], bg_color=(0, 0, 0), cell_size=self.cell_size)
        self.piece_position = (0, 0)
        self.counter = 0

    def update(self):
        #self.input()
        
        self.counter += 1
        self.draw_pieces()
        
        if self.counter >= 0.8*self.fps:
            self.counter = 0
            self.piece_position = (self.piece_position[0], self.piece_position[1] + self.cell_size)

        self.check_collision()
        self.current_piece.draw(self.piece_position)

        
        self.check_piece_position()
        pygame.display.flip()

    def draw_pieces(self):
        for piece, position in self.pieces:
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        global_x = position[0] + x * self.cell_size
                        global_y = position[1] + y * self.cell_size
                        pygame.draw.rect(self.screen, piece.color, 
                                        pygame.Rect(global_x, global_y, self.cell_size, self.cell_size))

    def check_piece_position(self):
        if self.piece_position[0] < 0:
            self.piece_position = (0, self.piece_position[1])

        if self.piece_position[0] > self.screen.get_width() - self.current_piece.get_width():
            self.piece_position = (self.screen.get_width() - self.current_piece.get_width(), self.piece_position[1])

    def check_collision(self):
        # Check if the piece is colliding with the board or another piece
        collision = False
        if self.piece_position[1] + self.current_piece.get_height() >= self.screen.get_height():
            collision = True
        print("self piece position : ", self.piece_position)
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
                                    print(global_x, global_y, other_x, other_y)
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
            # Store the current piece on the board
            self.pieces.append((self.current_piece, self.piece_position))

            # Spawn a new piece
            self.current_piece = Piece(shape=self.shapes[random.choice(list(self.shapes.keys()))], 
                                    color=self.colors[random.choice(list(self.colors.keys()))], 
                                    bg_color=(0, 0, 0), 
                                    cell_size=self.cell_size)
            self.piece_position = (self.screen.get_width() // 2 - self.cell_size, 0)
            


    def run(self):
        # Game loop
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.piece_position = (self.piece_position[0], self.piece_position[1] + self.cell_size)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()


                    if event.key == pygame.K_LEFT:
                        if self.piece_position[0] > 0:
                            self.piece_position = (self.piece_position[0] - self.cell_size, self.piece_position[1])
                        
                    if event.key == pygame.K_RIGHT:
                        
                        if self.piece_position[0] < self.screen.get_width() - self.current_piece.get_width():
                            self.piece_position = (self.piece_position[0] + self.cell_size, self.piece_position[1])    

            self.screen.fill((0, 0, 0))

            # Draw / render
            self.update()
            

            # Cap the frame rate
            self.clock.tick(self.fps)

        pygame.quit()