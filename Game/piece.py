import pygame


class Piece(pygame.Surface):
    def __init__(self, shape, color, bg_color, cell_size):
        self.shape = shape
        self.color = color
        self.cell_size = cell_size
        self.bg_color = bg_color
        super().__init__(
            (self.cell_size * len(self.shape[0]), self.cell_size * len(self.shape))
        )
        self._draw_shape()
        self.surface = pygame.display.get_surface()

    def _draw_shape(self):
        # self.fill(self.bg_color)

        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self,
                        self.color,
                        pygame.Rect(
                            x * self.cell_size,
                            y * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def rotate(self):
        # Rotate the shape 90 degrees clockwise and redraw the shape with a new surface
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.__init__(self.shape, self.color, self.bg_color, self.cell_size)
        self._draw_shape()

    def draw(self, position):
        # Draw the piece on the given surface at the specified position
        self.surface.blit(self, position)
