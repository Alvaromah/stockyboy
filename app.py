import pygame

from game import *

SCREEN_WIDTH = 612
SCREEN_HEIGHT = 800

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Stocky Boy")

    assets = Assets(scale=2)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)

    font_path = pygame.font.match_font("couriernew", 0, 0)
    font = pygame.font.Font(font_path, 28)
    font.set_bold(True)

    menu = Menu(screen, assets)
    game = Game(screen, assets, font)

    while True:
        if menu.run():
            if game.run(speed=6):
                continue
        break
    
    pygame.quit()

if __name__ == "__main__":
    main()
