# Foster Cavender
# CS1400 online 7 week

import pygame


class Cursor:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.pos = [0, 0]

    def update_pos(self, pos):
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)
