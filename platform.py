import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/platform.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
