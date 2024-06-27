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
        self.current_piece.draw(self.piece_position)
        self.counter += 1
        
        
        if self.counter >= 0.8*self.fps:
            self.counter = 0
            self.piece_position = (self.piece_position[0], self.piece_position[1] + self.cell_size)
        
        self.check_piece_position()
        pygame.display.flip()

    def check_piece_position(self):
        if self.piece_position[0] < 0:
            self.piece_position = (0, self.piece_position[1])

        if self.piece_position[0] > self.screen.get_width() - self.current_piece.get_width():
            self.piece_position = (self.screen.get_width() - self.current_piece.get_width(), self.piece_position[1])

    

    def run(self):
        # Game loop
        while self.running:
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

            # Update
            # Draw
            self.screen.fill((0, 0, 0))

            # Draw / render
            self.update()
            

            # Cap the frame rate
            self.clock.tick(self.fps)

        pygame.quit()