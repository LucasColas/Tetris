import pygame
from Game.game import Game
pygame.init()

def main(Width=450, Height=700, Title="Tetris", fps=60):
    # Initialize the game
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption(Title)
    tetris = Game(fps)
    tetris.run()


if __name__ == "__main__":
    main()
    

    
