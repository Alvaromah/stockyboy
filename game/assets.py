import os
import pygame

ASSETS_IMAGES = 'assets/images'
ASSETS_SOUNDS = 'assets/sounds'

class Assets():
    _instance = None

    def __new__(cls, scale=1):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.scale = scale
        return cls._instance

    def get_image(self, name, scale=None):
        scale = scale or self.scale
        if name not in self.images:
            filename = os.path.join(ASSETS_IMAGES, name)
            image = pygame.image.load(filename).convert_alpha()
            if scale != 1:
                size = (int(image.get_width() * self.scale), int(image.get_height() * self.scale))
                image = pygame.transform.scale(image, size)
            self.images[name] = image
        return self.images[name]
    
    def get_sound(self, name):
        if name not in self.sounds:
            filename = os.path.join(os.path.join(ASSETS_SOUNDS), name)
            sound = pygame.mixer.Sound(filename)
            self.sounds[name] = sound
        return self.sounds[name]

    def __getitem__(self, name):
        ext = os.path.splitext(name)[1]
        if ext == '':
            path = os.path.join(ASSETS_IMAGES, name)
            if os.path.isdir(path):
                return [self.get_image(os.path.join(name, fn)) for fn in os.listdir(path)]
            else:
                raise ValueError("Path not found: " + path)
        else:
            if ext == ".png" or ext == ".jpg":
                return self.get_image(name)
            elif ext == ".ogg" or ext == ".wav":
                return self.get_sound(name)
            else:
                raise ValueError("Unsupported file type: " + ext)
