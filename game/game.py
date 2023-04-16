import pygame

from .player import Player
from .ground import Ground, GroundParallax
from .artifacts import Decorations, Obstacles, Boxes

PLAYER_X = 102 * 3
PLAYER_Y = 64 * 4

class Game():
    def __init__(self, screen, assets, font, fps=60):
        self.fps = fps
        self.font = font
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.running = False
        self._init_artifacts(assets)
        self.music = assets['music.ogg']
        self.jump = assets['jump.wav']
        self.crash = assets['crash.wav']

    def _init_artifacts(self, assets):
        self.decorations = []
        self.ground = Ground(self.width, self.height, assets['ground.png'])
        self.ground_parallax = GroundParallax(self.width, self.height, assets['ground-left.png'], assets['ground-right.png'])
        self.player = Player(PLAYER_X, PLAYER_Y, assets['player'])
        self.decorations = Decorations(self.width, self.height, assets['atrezzo'])
        self.obstacles = Obstacles(self.width, self.height, assets['obstacles'])
        self.boxes = Boxes(self.width, self.height, assets['boxes'])
        self.live = assets.get_image('life.png', 1)

    def run(self, speed):
        lives = 3
        score = 0
        ready_count = 0
        self.running = True
        
        self.music.play(loops=-1)
        while self.running:
          
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1, 102, 10)
            if keys[pygame.K_RIGHT]:
                self.player.move(1, 102, 10)
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.player.jump()
                self.jump.play()

            # Save screenshot
            if keys[pygame.K_s]:
                pygame.image.save(self.screen, f'screenshot{score:0000}.png')

            if ready_count > 0:
                ready_count -= 1
                if ready_count == 0:
                    lives -= 1
                    if lives == 0:
                        self.music.stop()
                        self.running = False

            add_new = ready_count == 0

            self.ground.update(speed)
            self.ground_parallax.update(speed)
            self.decorations.update(speed)
            self.obstacles.update(speed, add_new)
            self.player.update(speed)
            self.boxes.update(speed, add_new)

            if ready_count == 0:
                score += 1
                collide = self.player.collide(self.obstacles.get_rects())
                if not collide:
                    collide = self.player.collide_box(self.boxes.get_rects())
                if collide:
                    self.crash.play()
                    ready_count = 200

            self.ground.draw(self.screen)
            self.ground_parallax.draw(self.screen)
            self.decorations.draw(self.screen)
            self.obstacles.draw(self.screen)
            if lives > 0:
                self.player.draw(self.screen)
            self.boxes.draw(self.screen)
            self.draw_lives(lives)
            self.draw_score(score)

            self.clock.tick(self.fps)
            pygame.display.flip()
        return True

    def draw_lives(self, lives):
        for i in range(lives):
            self.screen.blit(self.live, (4 + i * 30, 8))

    def draw_score(self, score):
        score_text = f'Score {score}'
        score_surface = self.font.render(score_text, True, (250, 250, 250))
        text_width, _ = score_surface.get_size()
        text_position = (self.width - text_width - 20, 10)
        self.screen.blit(score_surface, text_position)
