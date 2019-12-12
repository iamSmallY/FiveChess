from Game import *
import pygame


if __name__ == '__main__':
    pygame.init()
    game = Game(GAME_NAME+' '+GAME_VERSION)
    while True:
        game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit('GoodBye~')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game.mouse_click(mouse_x, mouse_y)
