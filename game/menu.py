import pygame

class Menu():
    def __init__(self, screen, assets):
        self.screen = screen
        self.background = assets['menu.png']

    def run(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
