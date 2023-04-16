import os

class Ground():
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.image = image
        self.y = 0

    def update(self, speed):
        self.y += speed
        self.y = self.y % self.image.get_height()

    def draw(self, screen):
        repetitions = self.height // self.image.get_height() + 2
        for i in range(repetitions):
            y = i * self.image.get_height() - self.y
            screen.blit(self.image, (0, y))

class GroundParallax():
    def __init__(self, width, height, image_left, image_right):
        self.width = width
        self.height = height
        self.image_left = image_left
        self.image_right = image_right
        self.y = 0

    def update(self, speed):
        self.y += speed * 1.2
        self.y = self.y % self.image_left.get_height()

    def draw(self, screen):
        repetitions = self.height // self.image_left.get_height() + 2
        for i in range(repetitions):
            x = self.width - self.image_right.get_width()
            y = i * self.image_left.get_height() - self.y
            screen.blit(self.image_left, (0, y))
            screen.blit(self.image_right, (x, y))
