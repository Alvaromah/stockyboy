import math
import random

from .helpers import *

class Decoration():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        self.rect.y -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Decorations():
    def __init__(self, width, height, images):
        self.width = width
        self.height = height
        self.images = images
        self.selector_line = RandomSequence([1, 2, 3, 4], 2)
        self.selector_image = RandomSequence([n for n in range(len(self.images))], 5)
        self.steps = 0
        self.items = []

    def add_item(self):
        line = self.selector_line.get_next()
        x = line * 104
        y = self.height
        i = self.selector_image.get_next()
        self.items.append(Decoration(x, y, self.images[i]))

    def update(self, speed):
        # Add new item randomly
        self.steps = (self.steps + 1) % (128 // speed)
        if self.steps == 0 and random.random() < 0.5:
            self.add_item()

        # Update items and remove off-screen
        for item in self.items:
            item.update(speed)
            if item.rect.y < -64:
                self.items.remove(item)

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

class Obstacle():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        self.rect.y -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Obstacles():
    def __init__(self, width, height, images):
        self.width = width
        self.height = height
        self.images = images
        self.selector_line = RandomSequence([1, 2, 3, 4], 2)
        self.selector_image = RandomSequence([n for n in range(len(self.images))], 2)
        self.steps = 0
        self.items = []

    def add_item(self):
        line = self.selector_line.get_next()
        x = line * 102 + line * 2
        y = self.height
        i = self.selector_image.get_next()
        self.items.append(Obstacle(x, y, self.images[i]))

    def update(self, speed, add_new):
        if add_new:
            # Add new item randomly
            self.steps = (self.steps + 1) % (128 // speed)
            if self.steps == 0 and random.random() < 0.5:
                self.add_item()

        # Update items and remove off-screen
        for item in self.items:
            item.update(speed)
            if item.rect.y < -64:
                self.items.remove(item)

    def get_rects(self):
        rects = []
        for item in self.items:
            rects.append(item.rect)
        return rects       

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

class Box():
    GRAVITY = 0.30

    def __init__(self, x, y, velocity, angle, image):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.angle_radians = math.radians(angle)
        self.vx = velocity * math.cos(self.angle_radians)
        self.vy = velocity * math.sin(self.angle_radians)
        self.falling = True

    def update(self, speed):
        if self.falling:
            self.x += self.vx
            self.y -= self.vy
            self.vy -= self.GRAVITY
            if self.y > 600:
                self.falling = False
        else:
            self.y -= speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Boxes():
    Y0 = 400
    VELOCITY = 18
    ANGLE = 70
    LINE_PARAMS = [
            (-457, Y0, VELOCITY, ANGLE),
            (-353, Y0, VELOCITY, ANGLE),
            (873, Y0, VELOCITY, 180-ANGLE),
            (977, Y0, VELOCITY, 180-ANGLE)
        ]

    def __init__(self, width, height, images):
        self.width = width
        self.height = height
        self.images = images
        self.selector_line = RandomSequence([1, 2, 3, 4], 2)
        self.selector_image = RandomSequence([n for n in range(len(self.images))], 2)
        self.steps = 0
        self.items = []

    def add_item(self):
        line = self.selector_line.get_next()
        i = self.selector_image.get_next()
        x, y, velocity, angle = self.LINE_PARAMS[line - 1]
        self.items.append(Box(x, y, velocity, angle, self.images[i]))

    def update(self, speed, add_new):
        if add_new:
            # Add new item randomly
            self.steps = (self.steps + 1) % (128 // speed)
            if self.steps == 0 and random.random() < 0.20:
                self.add_item()

        # Update items and remove off-screen
        for item in self.items:
            item.update(speed)
            if item.rect.y < -128:
                self.items.remove(item)

    def get_rects(self):
        rects = []
        for item in self.items:
            if not item.falling:
                rects.append(item.rect)
        return rects       

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)
