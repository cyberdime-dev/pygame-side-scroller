import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.jumping = False

    def update(self, keys_pressed):
        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            dx = PLAYER_SPEED

        self.vel_y += GRAVITY
        dy = self.vel_y

        if keys_pressed[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -JUMP_POWER
            self.jumping = True

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.jumping = False
